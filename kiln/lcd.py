# kiln/lcd.py — 20x4 LCD support — Metallurgy Kiln Controller V2
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

import threading
import time
import datetime
import socket
import logging

#sudo apt install -y python3-smbus i2c-tools
#sudo pip3 install RPLCD




# Setup Logger
log = logging.getLogger("LCD")

class LCDThread(threading.Thread):
    def __init__(self, controller_ref, config):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ctrl = controller_ref
        self.cfg = config
        self.running = True
        
        # Load Settings
        self.interval = getattr(config, 'LCD_PRINT_INTERVAL_SEC', 2.0)
        self.cols = getattr(config, 'LCD_COLS', 20)
        self.rows = getattr(config, 'LCD_ROWS', 4)
        self.ip_address = self.get_ip()
        self.lcd = None

        # Try Importing RPLCD
        try:
            from RPLCD.i2c import CharLCD
            self.lcd = CharLCD(
                i2c_expander=getattr(config, 'LCD_I2C_EXPANDER', 'PCF8574'),
                address=getattr(config, 'LCD_ADDRESS', 0x27), 
                port=1, 
                cols=self.cols, 
                rows=self.rows, 
                dotsize=getattr(config, 'LCD_DOTSIZE', 8), 
                charmap=getattr(config, 'LCD_CHARMAP', 'A02'), 
                auto_linebreaks=getattr(config, 'LCD_AUTO_LINEBREAKS', True), 
                backlight_enabled=getattr(config, 'LCD_BACKLIGHT', True)
            )
            self.lcd.clear()
            log.info(f"LCD Initialized at {hex(getattr(config, 'LCD_ADDRESS', 0x27))}")
        except ImportError:
            log.warning("RPLCD library not found. LCD Disabled.")
            self.running = False
        except Exception as e:
            log.error(f"LCD Hardware Init Failed: {e}")
            self.running = False

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "No Network"

    def get_progress_bar(self, percent, width=12):
        if percent > 100: percent = 100
        hashes = int((percent) * (width - 2))
        return "[" + ("=" * hashes) + (" " * (width - 2 - hashes)) + "]"

    def format_time(self, seconds):
        """Formats seconds into strict HH:MM:SS"""
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def run(self):
        if not self.running or not self.lcd: return
        
        log.info("LCD Thread Started")
        
        while True:
            try:
                # Fetch Status
                data = self.ctrl.status()
                
                running = data.get('running')
                if running:
                    state = "RUNNING"
                else:
                    state = "IDLE"

                cur_temp = data.get('temps', {}).get('tc', 0.0)
                setpoint = data.get('setpoint_c', 0.0)
                
                # Check Unit
                unit = getattr(self.cfg, 'DEF_TEMP_UNIT', 'C')
                
                # Unit Conversion
                if unit == 'F':
                    cur_temp = (cur_temp * 1.8) + 32
                    setpoint = (setpoint * 1.8) + 32
                
                # --- ROW 1 ---
                temp_str = f"{cur_temp:.2f}{unit}"
                padding = self.cols - len(state) - len(temp_str)
                if padding < 0: padding = 0
                row1 = f"{state}{' ' * padding}{temp_str}"
                
                self.lcd.cursor_pos = (0, 0)
                self.lcd.write_string(row1[:self.cols])

                if state == "RUNNING":
                    # --- ROW 2 (Centered) ---
                    heat_duty = data.get('relays', {}).get('r1', {}).get('duty', 0)
                    row2 = f"Tgt:{int(setpoint)}{unit:<3} Out:{int(heat_duty)}%"
                    self.lcd.cursor_pos = (1, 0)
                    # Use :^ to center the text within the total columns
                    self.lcd.write_string(f"{row2:^{self.cols}}")

                    # --- ROW 3 (Centered) ---
                    prof = data.get('running_profile_name') or "Unknown"
                    self.lcd.cursor_pos = (2, 0)
                    # Truncate profile name then center it
                    self.lcd.write_string(f"{prof[:self.cols]:^{self.cols}}")

                    # --- ROW 4 (Left Aligned for Progress Bar) ---
                    runtime_sec = data.get('kiln_runtime_sec', 0)
                    
                    # Get clean HH:MM:SS string
                    time_str = self.format_time(runtime_sec) 

                    prof_duration_sec = data.get('profile_duration_sec')
                    percent = runtime_sec/prof_duration_sec

                    bar = self.get_progress_bar(percent, width=12)
                    row4 = f"{time_str}{bar}"
                    self.lcd.cursor_pos = (3, 0)
                    self.lcd.write_string(f"{row4:<{self.cols}}")
                    
                else:
                    # --- IDLE SCREEN (Centered) ---
                    self.lcd.cursor_pos = (1, 0)
                    self.lcd.write_string(" " * self.cols) # Clear Row 2

                    self.lcd.cursor_pos = (2, 0)
                    # Center the static text
                    self.lcd.write_string(f"{'CONNECT TO UI AT:':^{self.cols}}")

                    self.lcd.cursor_pos = (3, 0)
                    # Center the IP address
                    self.lcd.write_string(f"{self.ip_address:^{self.cols}}")

            except Exception as e:
                log.error(f"LCD Loop Error: {e}")
            
            time.sleep(self.interval)