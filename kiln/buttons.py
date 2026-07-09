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
import logging
import json
from pathlib import Path

# Requires: pip install gpiozero
from gpiozero import Button 

log = logging.getLogger("AUX_BTNS")

class AuxButtonThread(threading.Thread):
    def __init__(self, controller, config):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ctrl = controller
        self.cfg = config
        self.buttons = []
        self.running = True

        # [NEW] Get hold time from config, default to 1.0 second if missing
        self.hold_time = float(getattr(self.cfg, "AUX_BUTTON_HOLD_TIME_SEC", 1.0))
        
        log.info(f"Initializing Aux Buttons (Hold Time: {self.hold_time}s)...")

        # Setup Buttons 1-4
        for i in range(1, 5):
            self._setup_button(i)

    def _setup_button(self, index):
        pin = getattr(self.cfg, f"AUX_BUTTON_{index}_PIN", None)
        prof_name = getattr(self.cfg, f"AUX_BUTTON_{index}_PROFILE", None)

        # Only create if PIN is set (not None)
        if pin is not None:
            try:
                # Use the configured hold_time
                btn = Button(pin, hold_time=self.hold_time)
                
                # Use a lambda to capture the specific index/profile
                btn.when_held = lambda b: self.trigger_profile(index, prof_name)
                
                self.buttons.append(btn)
                log.info(f"   [Button {index}] GPIO {pin} -> Profile: '{prof_name}'")
            except Exception as e:
                log.error(f"   [Button {index}] Failed to init on GPIO {pin}: {e}")

    def trigger_profile(self, index, profile_name):
        if not self.running: return
        
        # 1. Check if Kiln is already running (Safety)
        status = self.ctrl.status()
        if status.get("running"):
            log.warning(f"Aux Button {index} ignored: Kiln is currently RUNNING.")
            return

        if not profile_name:
            log.warning(f"Aux Button {index} pressed, but no profile configured.")
            return

        log.info(f"Aux Button {index} pressed. Loading '{profile_name}'...")

        # 2. Load Profile from Disk
        try:
            # Ensure name matches file system (strip .json if user added it in config)
            safe_name = profile_name.replace(".json", "")
            path = self.cfg.PROFILE_DIR / f"{safe_name}.json"
            
            if not path.exists():
                log.error(f"Profile file not found: {path}")
                return

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            steps = data.get("steps", [])
            if not steps:
                log.error("Profile has no steps.")
                return

            # 3. Start the Controller
            self.ctrl.start_profile(steps, name=safe_name)
            log.info(f"Successfully started Aux Profile: {safe_name}")

        except Exception as e:
            log.error(f"Error starting aux profile: {e}")

    def run(self):
        # Keep thread alive
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False
        for b in self.buttons:
            b.close()