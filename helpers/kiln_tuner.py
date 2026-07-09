#!/usr/bin/env python3
import time
import argparse
import sys
import math
import signal
import os

# --- ADD PARENT DIRECTORY TO PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config

# --- HARDWARE IMPORTS ---
try:
    import RPi.GPIO as GPIO
    import board
    import busio
    import digitalio
    import adafruit_max31856 
except ImportError:
    print("[ERROR] Hardware libraries missing (RPi.GPIO or adafruit-max31856).")
    print("        This script must run on the Raspberry Pi.")
    sys.exit(1)

# --- CONFIGURATION ---
print("[INFO] Loading configuration from config.py...")

RELAY_1_PIN = config.RELAY_1_PIN
RELAY_2_PIN = getattr(config, 'RELAY_2_PIN', None)
MAX_SAFE_TEMP_C = config.MAX_TEMP_C
TEMPER_THRESHOLD_C = getattr(config, 'TEMPER_THRESHOLD_C', 500) 

try:
    SPI_CS_PIN = getattr(board, config.CS_PIN)
except AttributeError:
    print(f"[WARN] Pin '{config.CS_PIN}' not found. Defaulting to D5.")
    SPI_CS_PIN = board.D5

tc_type_str = str(config.TC_TYPE).upper().strip()
valid_types = {
    "B": adafruit_max31856.ThermocoupleType.B,
    "E": adafruit_max31856.ThermocoupleType.E,
    "J": adafruit_max31856.ThermocoupleType.J,
    "K": adafruit_max31856.ThermocoupleType.K,
    "N": adafruit_max31856.ThermocoupleType.N,
    "R": adafruit_max31856.ThermocoupleType.R,
    "S": adafruit_max31856.ThermocoupleType.S,
    "T": adafruit_max31856.ThermocoupleType.T
}

if tc_type_str in valid_types:
    TC_TYPE = valid_types[tc_type_str]
else:
    print(f"[WARN] TC Type '{config.TC_TYPE}' invalid. Defaulting to Type S.")
    TC_TYPE = adafruit_max31856.ThermocoupleType.S

print(f"   - Relay 1: GPIO {RELAY_1_PIN}")
if RELAY_2_PIN:
    print(f"   - Relay 2: GPIO {RELAY_2_PIN}")
print(f"   - CS Pin: {config.CS_PIN}")
print(f"   - TC Type: {tc_type_str}")
print(f"   - Max Temp: {MAX_SAFE_TEMP_C} C")
print(f"   - Temper Threshold: {TEMPER_THRESHOLD_C} C\n")


class KilnTuner:
    def __init__(self, target_temp, unit):
        self.target_temp = target_temp
        self.unit = unit
        
        if unit == 'F':
            self.target_c = (target_temp - 32) * 5/9
        else:
            self.target_c = target_temp
            
        self.use_dual_relays = False
        if RELAY_2_PIN and self.target_c > TEMPER_THRESHOLD_C:
            self.use_dual_relays = True
            print(f"[INFO] Target ({self.target_c:.0f}C) > Threshold ({TEMPER_THRESHOLD_C}C). Using BOTH Relays.")
        else:
            print(f"[INFO] Target ({self.target_c:.0f}C) <= Threshold ({TEMPER_THRESHOLD_C}C). Using SINGLE Relay.")

        self.setup_gpio()
        self.setup_sensor()
        
        self.running = True
        self.current_temp = 0.0
        self.max_heating_rate = 0.0

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_1_PIN, GPIO.OUT)
        GPIO.output(RELAY_1_PIN, GPIO.LOW) 
        if RELAY_2_PIN:
            GPIO.setup(RELAY_2_PIN, GPIO.OUT)
            GPIO.output(RELAY_2_PIN, GPIO.LOW)

    def setup_sensor(self):
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(SPI_CS_PIN)
        cs.direction = digitalio.Direction.OUTPUT
        self.sensor = adafruit_max31856.MAX31856(spi, cs, thermocouple_type=TC_TYPE)

    def read_temp(self):
        try:
            temp_c = self.sensor.temperature
            if self.unit == 'F':
                return (temp_c * 9/5) + 32
            return temp_c
        except Exception as e:
            print(f"Sensor Error: {e}")
            return self.current_temp

    def read_temp_c(self):
        return self.sensor.temperature

    def set_relay(self, state):
        if state:
            GPIO.output(RELAY_1_PIN, GPIO.HIGH)
            if self.use_dual_relays:
                GPIO.output(RELAY_2_PIN, GPIO.HIGH)
        else:
            GPIO.output(RELAY_1_PIN, GPIO.LOW)
            if RELAY_2_PIN:
                GPIO.output(RELAY_2_PIN, GPIO.LOW)

    def cleanup(self):
        print("\n[STOP] Shutting down. Turning off relays.")
        GPIO.output(RELAY_1_PIN, GPIO.LOW)
        if RELAY_2_PIN:
            GPIO.output(RELAY_2_PIN, GPIO.LOW)
        GPIO.cleanup()

    def run_max_rate_test(self):
        print(f"\n[PHASE 1] Determining Max Heating Rate...")
        print(f"   Target for switch-over: {self.target_temp - 20:.1f} {self.unit}")
        print("   Relays: 100% ON")
        
        start_time = time.time()
        start_temp = self.read_temp()
        
        # Initialize vars for display
        rate = 0.0
        
        while self.current_temp < (self.target_temp - 20):
            self.current_temp = self.read_temp()
            self.set_relay(True)

            elapsed_min = (time.time() - start_time) / 60
            
            # Only calculate rate after 30 seconds to allow sensor to stabilize
            rate_display = "Calculating..."
            if elapsed_min > 0.5:
                delta_temp = self.current_temp - start_temp
                rate = delta_temp / elapsed_min
                if rate > self.max_heating_rate:
                    self.max_heating_rate = rate
                rate_display = f"{rate:.2f} {self.unit}/min"
            
            # --- PRINT UPDATES HERE (Every Loop) ---
            # Remove end='\r' if you want a new line every time (scrolling text)
            print(f"   Temp: {self.current_temp:.1f} {self.unit} | Rate: {rate_display} | Max: {self.max_heating_rate:.2f} {self.unit}/min   ", end='\r')
            
            if self.read_temp_c() > MAX_SAFE_TEMP_C:
                print("\n[CRITICAL] Safety Limit Exceeded!")
                return False
                
            time.sleep(1)
            
        print(f"\n[DONE] Max Heating Rate: {self.max_heating_rate:.2f} {self.unit}/min")
        return True

    def run_pid_autotune(self):
        print(f"\n[PHASE 2] PID Auto-Tune (Relay Method)")
        print("   Oscillating temperature around setpoint...")
        
        cycles = 0
        required_cycles = 3
        peaks = []
        valleys = []
        last_crossing_time = time.time()
        periods = []
        heating = True
        
        while cycles < required_cycles:
            self.current_temp = self.read_temp()
            
            if heating and self.current_temp >= self.target_temp:
                heating = False
                self.set_relay(False)
                peaks.append(self.current_temp)
                print(f"   [DOWN] Over Setpoint. Relays OFF. (Cycle {cycles+1}/{required_cycles})")
            
            elif not heating and self.current_temp <= self.target_temp:
                heating = True
                self.set_relay(True)
                valleys.append(self.current_temp)
                
                now = time.time()
                period_sec = now - last_crossing_time
                if cycles > 0:
                    periods.append(period_sec)
                    print(f"   [TIME] Period: {period_sec:.1f} sec")
                
                last_crossing_time = now
                cycles += 1
                print(f"   [UP] Under Setpoint. Relays ON. (Cycle {cycles}/{required_cycles})")
            
            if not heating:
                if len(peaks) > 0: peaks[-1] = max(peaks[-1], self.current_temp)
            else:
                if len(valleys) > 0: valleys[-1] = min(valleys[-1], self.current_temp)

            print(f"   T: {self.current_temp:.1f} {self.unit} | Target: {self.target_temp} | Status: {'Heating' if heating else 'Cooling'}   ", end='\r')
            time.sleep(0.5)

        print("\n\n[CALC] Calculating PID Values...")
        
        count = min(len(peaks), len(valleys))
        avg_peak = sum(peaks[:count])/count
        avg_valley = sum(valleys[:count])/count
        amplitude = (avg_peak - avg_valley) / 2
        
        if len(periods) == 0:
            print("Error: Not enough full cycles detected.")
            return

        Tu = sum(periods) / len(periods)
        d = 100 
        Ku = (4 * d) / (math.pi * amplitude)
        
        print("-" * 60)
        print(f"RESULTS FOR {self.target_temp} {self.unit}")
        print(f"Oscillation Amp : {amplitude:.2f} {self.unit}")
        print(f"Critical Period : {Tu:.2f} sec")
        print(f"Ultimate Gain   : {Ku:.4f}")
        print("-" * 60)
        
        kp_zn = 0.6 * Ku
        ki_zn = (2 * kp_zn) / Tu
        kd_zn = (kp_zn * Tu) / 8

        kp_tl = 0.45 * Ku / 2.2 
        ki_tl = kp_tl / (Tu * 2.2) 
        kd_tl = kp_tl * Tu / 6.3

        kp_no = 0.2 * Ku
        ki_no = (kp_no) / (Tu / 2)
        kd_no = (kp_no * Tu) / 3

        print(f"{'TYPE':<20} | {'Kp':<10} | {'Ki':<10} | {'Kd':<10}")
        print("-" * 60)
        print(f"{'1. Aggressive (Z-N)':<20} | {kp_zn:<10.4f} | {ki_zn:<10.4f} | {kd_zn:<10.4f}")
        print(f"{'2. Balanced (T-L)':<20} | {kp_tl:<10.4f} | {ki_tl:<10.4f} | {kd_tl:<10.4f}  <-- RECOMMENDED")
        print(f"{'3. No Overshoot':<20} | {kp_no:<10.4f} | {ki_no:<10.4f} | {kd_no:<10.4f}")
        print("-" * 60)

        # COPY-PASTE BLOCKS
        print("\n" + "="*60)
        print("COPY/PASTE BLOCKS FOR config.py")
        print("="*60)

        print("\n# OPTION 1: Aggressive (Ziegler-Nichols)")
        print(f'PID_TEMPER_CONF = {{"Kp": {kp_zn:.4f}, "Ki": {ki_zn:.4f}, "Kd": {kd_zn:.4f}, "output_limits": (0, 100)}}')

        print("\n# OPTION 2: Balanced (Tyreus-Luyben) <-- RECOMMENDED")
        print(f'PID_TEMPER_CONF = {{"Kp": {kp_tl:.4f}, "Ki": {ki_tl:.4f}, "Kd": {kd_tl:.4f}, "output_limits": (0, 100)}}')

        print("\n# OPTION 3: No Overshoot")
        print(f'PID_TEMPER_CONF = {{"Kp": {kp_no:.4f}, "Ki": {ki_no:.4f}, "Kd": {kd_no:.4f}, "output_limits": (0, 100)}}')
        print("\n(Note: Rename to PID_HIGH_CONF if tuning for high temp)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kiln PID Auto-Tuner")
    parser.add_argument("temp", type=float, help="Target temperature")
    parser.add_argument("-C", action="store_true", help="Use Celsius")
    parser.add_argument("-F", action="store_true", help="Use Fahrenheit")
    
    args = parser.parse_args()
    unit = 'F' if args.F else 'C'
    
    tuner = KilnTuner(args.temp, unit)
    
    def signal_handler(sig, frame):
        tuner.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    try:
        print(f"Starting Tuner for {args.temp} {unit}")
        print("[WARN] Ensure main kiln-controller service is STOPPED.")
        print("Press Ctrl+C to abort.\n")
        time.sleep(2)
        
        if tuner.run_max_rate_test():
            tuner.run_pid_autotune()
            
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        tuner.cleanup()