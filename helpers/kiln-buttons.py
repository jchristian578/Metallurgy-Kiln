# helpers/kiln-buttons.py — Physical buttons to control the kiln — Metallurgy Kiln Controller V2
'''
-------------------------------------------------------------------
------------------- Metallurgy Kiln Controller --------------------
-------------------------------------------------------------------
----------------------- By: Jacob Christian -----------------------
----------------------- Besslen Bladewords ------------------------
-------------------------------------------------------------------
---------------- https://www.WootzSmithForum.com/ -----------------
---------- https://www.instagram.com/besslenbladeworks/ -----------
----------- https://www.youtube.com/@besslenbladeworks ------------
----------------- V2 Completed January 3rd, 2026 ------------------
-------------------------------------------------------------------
'''

# OUT OF BAND BUTTON CONTROLL - WILL STILL WORK EVEN IF THE MAIN KILN CONTROLLER PROGRAM IS HUNG. 

#!/usr/bin/env python3
import time
import subprocess
import requests
import RPi.GPIO as GPIO
import logging
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [BUTTONS] %(message)s')

# --- CONFIGURATION ---
PIN_STOP = config.BUTTON_PROFILE_STOP_PIN
PIN_RESTART = config.BUTTON_RESTART_SERVICES_PIN
PIN_SYSTEM_REBOOT = config.BUTTON_SYSTEM_REBOOT_PIN 

HOLD_TIME = config.BUTTON_HOLD_TIME_SEC
API_URL = f"http://{config.WEB_HOST}:{config.WEB_PORT}/api/stop"

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # Setup buttons with Internal Pull-Up Resistors
    # (Default state is HIGH (1), Pressed state is LOW (0))
    GPIO.setup(PIN_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_RESTART, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_SYSTEM_REBOOT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def trigger_stop():
    """Sends an API request to the main controller to stop the profile."""
    try:
        logging.info("🛑 STOP Button Pressed. Sending API request...")
        r = requests.post(API_URL, json={}, timeout=2)
        if r.status_code == 200:
            logging.info("✅ Kiln Stop Command Successful.")
        else:
            logging.warning(f"⚠️ Kiln returned status {r.status_code}")
    except Exception as e:
        logging.error(f"❌ Failed to contact Kiln Controller: {e}")

def trigger_restart():
    """Restarts the systemd service for the main controller."""
    logging.info("🔄 SERVICE RESTART Button Held. Restarting Service...")
    # We use subprocess to call systemctl
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'kilncontroller.service'], check=True)
        logging.info("✅ Service Restart Triggered.")
    except Exception as e:
        logging.error(f"❌ Failed to restart service: {e}")

def trigger_system_reboot():
    """Reboots the physical Raspberry Pi."""
    logging.warning("⚠️ SYSTEM REBOOT Button Held. Rebooting Pi...")
    try:
        # Calls the linux reboot command
        subprocess.run(['sudo', 'reboot'], check=True)
    except Exception as e:
        logging.error(f"❌ Failed to reboot system: {e}")

def main():
    setup_gpio()
    logging.info("Physical Button Monitor Started.")
    
    # State tracking for Service Restart Button
    restart_press_start = 0
    restart_held = False

    # [NEW] State tracking for System Reboot Button
    reboot_press_start = 0
    reboot_held = False
    
    try:
        while True:
            # --- HANDLE STOP BUTTON (Simple Click) ---
            if GPIO.input(PIN_STOP) == GPIO.LOW:
                # Debounce: wait 0.05s and check again to ensure it's a real press
                time.sleep(0.05)
                if GPIO.input(PIN_STOP) == GPIO.LOW:
                    trigger_stop()
                    # Wait until button is released so we don't spam the API
                    while GPIO.input(PIN_STOP) == GPIO.LOW:
                        time.sleep(0.1)
            
            # --- HANDLE SERVICE RESTART BUTTON (Hold for X seconds) ---
            if GPIO.input(PIN_RESTART) == GPIO.LOW:
                if restart_press_start == 0:
                    restart_press_start = time.time()
                
                duration = time.time() - restart_press_start
                
                # Check if held long enough
                if duration > HOLD_TIME and not restart_held:
                    trigger_restart()
                    restart_held = True # Prevent double triggering
            else:
                # Button released, reset counters
                restart_press_start = 0
                restart_held = False

            # --- [NEW] HANDLE SYSTEM REBOOT BUTTON (Hold for X seconds) ---
            if GPIO.input(PIN_SYSTEM_REBOOT) == GPIO.LOW:
                if reboot_press_start == 0:
                    reboot_press_start = time.time()
                
                duration = time.time() - reboot_press_start
                
                # Check if held long enough
                if duration > HOLD_TIME and not reboot_held:
                    trigger_system_reboot()
                    reboot_held = True # Prevent double triggering
            else:
                # Button released, reset counters
                reboot_press_start = 0
                reboot_held = False

            time.sleep(0.1) # Poll rate

    except KeyboardInterrupt:
        logging.info("Stopping Button Monitor")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()