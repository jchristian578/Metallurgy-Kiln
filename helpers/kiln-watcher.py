#!/usr/bin/env python3
import requests
import json
import time
import datetime
import logging
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config as CFG

# --- SETUP FROM CONFIG ---
HOST_IP = "127.0.0.1" if CFG.WEB_HOST == "0.0.0.0" else CFG.WEB_HOST
KILN_BASE_URL = f"http://{HOST_IP}:{CFG.WEB_PORT}"

POLL_INTERVAL = float(CFG.WATCHER_POLL_INTERVAL_SEC)

# Runaway Protection Settings
RUNAWAY_DELTA_C = float(CFG.WATCHER_RUNAWAY_DELTA_C) # Alert if Temp > Setpoint + 30

# RPi Temperature Alert Threshold
MAX_RPI_TEMP_C = getattr(CFG, 'WATCHER_MAX_RPI_TEMP', 75.0) 

# API Push Notification Config (Pushover, etc.)
API_URL = "https://api.pushover.net/1/messages.json" 
API_KEY = ""
USER_KEY = ""

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger("KILN-WATCHER")

class Watcher:
    def __init__(self):
        self.url = f"{KILN_BASE_URL}/api/status"
        
        # State Tracking
        self.last_state = "IDLE"
        self.last_profile = None
        self.last_setpoint = None
        self.target_reached_flag = False
        self.last_auto_resumed = False  # Track previous auto-resume state
        self.last_step = None  # Track last step
        
        # Error Detection Vars
        self.temp_history = []
        self.max_temp_run = 0.0
        self.runaway_alerted = False
        self.open_loop_alerted = False
        self.rpi_high_temp_alerted = False # State tracking for RPi temp
        self.tracking_error_alerted = False

    def send_alert(self, title, msg):
        """Sends the API Push Notification"""
        try: 
            data = {
                "token": API_KEY, 
                "user": USER_KEY, 
                "message": msg, 
                "title": title
            }
            headers = {'Content-Type': 'application/json'}
            
            if API_KEY and USER_KEY:
                r = requests.post(API_URL, data=json.dumps(data), headers=headers)
                if r.status_code == 200:
                    log.info(">> Push Notification sent successfully.")
                else:
                    log.warning(f"Error sending notification: Status {r.status_code}")
        except Exception as e:
            log.error(f"Exception sending alert: {e}")
            pass

    def notify(self, topic, message, level="INFO"):
        """Logs to console AND triggers the API push notification with Emojis"""
        
        # 1. Determine Emoji based on Topic/Level
        emoji = "ℹ️" # Default
        if level == "ERROR": emoji = "🚨"
        elif level == "WARNING": emoji = "⚠️"
        elif topic == "STARTED": emoji = "🔥"
        elif topic == "ENDED": emoji = "✅"
        elif topic == "TARGET REACHED": emoji = "🎯"
        elif topic == "RUNAWAY DETECTED": emoji = "🌋"
        elif topic == "RUNAWAY CLEARED": emoji = "❄️"
        elif topic == "OPEN LOOP DETECTED": emoji = "🔌"
        elif topic == "POWER RESTORED": emoji = "⚡"
        elif topic == "AUTO-RESUMED": emoji = "🔄"
        elif topic == "RPI OVERHEATING": emoji = "🌡️" # [NEW]
        elif topic == "RPI TEMP COOLED": emoji = "🟢" # [NEW]

        full_title = f"{emoji} Kiln: {topic}"
        full_msg = message
        
        if level == "ERROR":
            log.error(f"{full_title} - {full_msg}")
        elif level == "WARNING":
            log.warning(f"{full_title} - {full_msg}")
        else:
            log.info(f"{full_title} - {full_msg}")

        self.send_alert(full_title, full_msg)

    def get_status(self):
        try:
            r = requests.get(self.url, timeout=2)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            log.debug(f"Connection error: {e}")
        return None

    def get_rpi_temperature(self):
        """ Reads the Raspberry Pi internal CPU temperature safely."""
        try:
            if os.path.exists("/sys/class/thermal/thermal_zone0/temp"):
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                    # File returns milli-degrees Celsius (e.g. 52000 for 52C)
                    return float(f.read().strip()) / 1000.0
        except Exception as e:
            log.error(f"Failed to read RPi temperature: {e}")
        return None

    def check_rpi_thermal(self):
        """ Checks if the Raspberry Pi hardware environment is too hot."""
        cpu_temp = self.get_rpi_temperature()
        if cpu_temp is None: 
            return

        if cpu_temp > MAX_RPI_TEMP_C:
            if not self.rpi_high_temp_alerted:
                self.notify(
                    "RPI OVERHEATING", 
                    f"Raspberry Pi CPU is running dangerously hot at {cpu_temp:.1f}°C! (Threshold: {MAX_RPI_TEMP_C}°C). Check enclosure cooling.", 
                    level="ERROR"
                )
                self.rpi_high_temp_alerted = True
        else:
            # Clear flag if it cools 3 degrees below threshold to prevent rapid toggle spam
            if self.rpi_high_temp_alerted and cpu_temp < (MAX_RPI_TEMP_C - 3.0):
                self.rpi_high_temp_alerted = False
                self.notify(
                    "RPI TEMP COOLED", 
                    f"Raspberry Pi CPU has returned to a safe temperature ({cpu_temp:.1f}°C).", 
                    level="INFO"
                )

    def check_runaway(self, current_temp, setpoint):
        """
        Checks if current temp is dangerously higher than setpoint.
        """
        if setpoint <= 0: return

        if current_temp > (setpoint + RUNAWAY_DELTA_C):
            if not self.runaway_alerted:
                self.notify("RUNAWAY DETECTED", 
                    f"Temp ({current_temp:.1f}°C) is {RUNAWAY_DELTA_C}°C higher than Setpoint ({setpoint}°C)! Check Relay!", 
                    level="ERROR")
                self.runaway_alerted = True
        else:
            # Reset alert flag if temp comes back down (with 2 degrees hysteresis)
            if self.runaway_alerted and current_temp < (setpoint + RUNAWAY_DELTA_C - 2):
                self.runaway_alerted = False
                self.notify("RUNAWAY CLEARED", "Temperature has returned to safe range.", level="INFO")

    def check_open_loop(self, status):
        """
        Detects if kiln is powering 100% but temp isn't moving.
        Logic: If duty > 95% for 5 minutes AND temp rise < 2°C -> Alarm
        """
        raw_temp = status.get('temps', {}).get('tc')
        current_temp = float(raw_temp) if raw_temp is not None else 0.0
        duty = status.get('relays', {}).get('r1', {}).get('duty', 0)

        now = time.time()
        self.temp_history.append({'t': now, 'temp': current_temp, 'duty': duty})
        cutoff = now - 300
        self.temp_history = [x for x in self.temp_history if x['t'] > cutoff]

        if len(self.temp_history) < 10: return 

        avg_duty = sum(d['duty'] for d in self.temp_history) / len(self.temp_history)
        start_temp = self.temp_history[0]['temp']
        end_temp = self.temp_history[-1]['temp']
        delta_temp = end_temp - start_temp

        if avg_duty > 95 and delta_temp < 3.0:
            if not self.open_loop_alerted:
                self.notify("OPEN LOOP DETECTED", 
                    f"Power is {avg_duty:.1f}% but temp only rose {delta_temp:.1f}°C in 5 mins.", 
                    level="ERROR")
                self.open_loop_alerted = True
        else:
            self.open_loop_alerted = False

    def check_tracking_error(self, current_temp, setpoint):
        """
        Alerts if the kiln is struggling and lagging too far behind the setpoint.
        """
        MAX_LAG_C = getattr(CFG, 'WATCHER_MAX_LAG_C', 40.0)  # Alert if the kiln falls behind the target
        
        if setpoint <= 0: return

        if (setpoint - current_temp) > MAX_LAG_C:
            if not self.tracking_error_alerted:
                self.notify("TRACKING ERROR", 
                    f"Kiln is lagging! Temp ({current_temp:.1f}°C) is {MAX_LAG_C}°C behind the Setpoint ({setpoint}°C).", 
                    level="WARNING")
                self.tracking_error_alerted = True
        else:
            # Reset if it catches back up (with 5 degrees hysteresis)
            if self.tracking_error_alerted and (setpoint - current_temp) < (MAX_LAG_C - 5.0):
                self.tracking_error_alerted = False
                self.notify("TRACKING RECOVERED", "Kiln has caught back up to the profile schedule.", level="INFO")

    def run(self):
        log.info(f"Watcher started. Monitoring {self.url} (Poll: {POLL_INTERVAL}s)")
        
        # Notify on startup (implies power restore or service restart)
        self.notify("POWER RESTORED", "Kiln Watcher is online and monitoring.", level="INFO")
        
        while True:
            # --- ALWAYS RUN ENVIRONMENTAL HARDWARE CHECKS ---
            # Evaluates regardless of whether the api endpoint is responsive or kiln status
            self.check_rpi_thermal()

            status = self.get_status()
            
            if not status:
                time.sleep(POLL_INTERVAL)
                continue

            # --- 1. PARSE STATE ---
            is_running = status.get('running', False)
            fault = status.get('fault')
            auto_resumed = status.get('auto_resumed', False)

            if fault:
                state = "ERROR"
                err_msg = str(fault)
            elif is_running:
                state = "RUNNING"
            else:
                state = "IDLE"

            # --- 2. EXTRACT VALUES ---
            profile_name = status.get('running_profile_name') or "Manual"
            current_step = status.get('current_step') # Get the profile step index
            raw_temp = status.get('temps', {}).get('tc')
            current_temp = float(raw_temp) if raw_temp is not None else 0.0
            raw_sp = status.get('setpoint_c')
            setpoint = float(raw_sp) if raw_sp is not None else 0.0
            runtime = status.get('kiln_runtime_sec', 0)

            if state == 'RUNNING' and current_temp > self.max_temp_run:
                self.max_temp_run = current_temp

            # --- 3. DETECT START ---
            if self.last_state == "IDLE" and state == "RUNNING":
                # Only notify "Started" if it wasn't an auto-resume (handled below)
                if not auto_resumed:
                    self.notify("STARTED", f"Profile '{profile_name}' has started.")
                
                self.max_temp_run = current_temp
                self.target_reached_flag = False
                self.runaway_alerted = False
                self.open_loop_alerted = False
                self.temp_history = []

            # --- DETECT AUTO-RESUME ---
            if auto_resumed and not self.last_auto_resumed:
                self.notify("AUTO-RESUMED", 
                    f"Profile '{profile_name}' resumed automatically after power loss.", 
                    level="WARNING")
            
            # --- 4. DETECT STOP (SUCCESS or ABORT) ---
            if self.last_state == "RUNNING" and state == "IDLE":
                duration = str(datetime.timedelta(seconds=int(runtime)))
                self.notify("ENDED", 
                    f"Profile '{self.last_profile}' finished/stopped. Duration: {duration}. Max Temp: {self.max_temp_run:.1f}°C")

            # --- 5. DETECT SETPOINT REACHED ---
            if state == "RUNNING" and setpoint > 0:
                is_new_target = False
                
                # If running a profile, ONLY allow a new alert when the Step changes.
                # This completely eliminates the 800, 799, 798 ramp spam.
                if profile_name != "Manual" and current_step is not None:
                    if current_step != self.last_step:
                        is_new_target = True
                else:
                    # Fallback for Manual Mode: Reset whenever the user types a new setpoint.
                    # We use a > 2.0°C jump threshold to ignore tiny PID fluctuations.
                    if abs(setpoint - (self.last_setpoint or 0.0)) > 2.0:
                        is_new_target = True

                # If a new target/step is confirmed, reset the flags
                if is_new_target:
                    self.target_reached_flag = False
                    self.last_step = current_step
                    self.last_setpoint = setpoint
                
                # Trigger the notification once the temp catches up to the setpoint
                if not self.target_reached_flag and abs(current_temp - setpoint) < 3.0:
                    step_info = f"Step {current_step}" if current_step is not None else "Manual"
                    self.notify("TARGET REACHED", f"Reached {current_temp:.1f}°C ({step_info} Target: {setpoint:.1f}°C)")
                    self.target_reached_flag = True

            # --- 6. SAFETY CHECKS (Only while running) ---
            if state == "RUNNING":
                self.check_open_loop(status)
                self.check_runaway(current_temp, setpoint)
                self.check_tracking_error(current_temp, setpoint)

            # --- 7. DETECT CONTROLLER ERROR ---
            if state == "ERROR" and self.last_state != "ERROR":
                self.notify("SYSTEM ERROR", f"Fault Detected: {err_msg}", level="ERROR")

            # Update state for next loop
            self.last_state = state
            self.last_profile = profile_name
            self.last_auto_resumed = auto_resumed
            
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    Watcher().run()
