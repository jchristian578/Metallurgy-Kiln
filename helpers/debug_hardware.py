# helpers/debug_hardware.py — Help to find out why it wont work... — Metallurgy Kiln Controller V2
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

import board
import busio
import digitalio
import adafruit_max31856
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config as CFG

print("\n--- HARDWARE DIAGNOSTIC ---")
print(f"Configured CS Pin: {CFG.CS_PIN}")

# 1. Test SPI Bus
print("\n[1/3] Initializing SPI Bus (SCLK, MOSI, MISO)...")
try:
    spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
    while not spi.try_lock():
        pass
    spi.configure(baudrate=500000)
    spi.unlock()
    print("      PASS: SPI Bus is active.")
except Exception as e:
    print(f"      FAIL: SPI Error. Did you enable SPI in raspi-config? \n      Error: {e}")
    exit(1)

# 2. Test Chip Select (CS)
print(f"\n[2/3] Initializing Chip Select Pin ({CFG.CS_PIN})...")
try:
    # Convert string "D5" to board.D5
    pin_name = str(CFG.CS_PIN).upper()
    if not hasattr(board, pin_name):
        raise ValueError(f"Pin 'board.{pin_name}' does not exist on this Raspberry Pi.")
        
    cs_pin = getattr(board, pin_name)
    cs = digitalio.DigitalInOut(cs_pin)
    cs.direction = digitalio.Direction.OUTPUT
    cs.value = True
    print(f"      PASS: CS Pin {pin_name} is valid.")
except Exception as e:
    print(f"      FAIL: CS Pin Error. Check config.py CS_PIN. \n      Error: {e}")
    exit(1)

# 3. Test Sensor Communication
print("\n[3/3] Talking to MAX31856 Sensor...")
try:
    sensor = adafruit_max31856.MAX31856(spi, cs)
    
    # Try to read linearisation data or temp to confirm connection
    temp = sensor.temperature
    internal = sensor.reference_temperature
    faults = sensor.fault
    
    print(f"      PASS: Connection Successful!")
    print(f"      ---------------------------")
    print(f"      Thermocouple Temp: {temp:.2f} °C")
    print(f"      Internal (Cold J): {internal:.2f} °C")
    print(f"      Fault Register:    {faults}")
    
    if temp == 0.0 and internal == 0.0:
        print("\n      WARNING: Reading is 0.00. This often means the sensor is not powered or wired incorrectly (MISO/MOSI swapped).")
    while(True):
        # Try to read linearisation data or temp to confirm connection
        temp = sensor.temperature
        internal = sensor.reference_temperature
        faults = sensor.fault
        
        print(f"      Thermocouple Temp: {temp:.2f} °C")
        print(f"      Internal (Cold J): {internal:.2f} °C")
        if any(faults.values()):
            for fault_type, is_active in faults.items():
                if is_active:
                    print(f"   - {fault_type}")
        else:
            print("No faults detected.")

        print(f"      ---------------------------")

except Exception as e:
    print(f"      FAIL: The Pi cannot talk to the sensor. \n      Error: {e}")
    print("\n      TROUBLESHOOTING:")
    print("      1. Check wiring: VIN(3.3v), GND, SCK, SDI(MOSI), SDO(MISO), CS")
    print("      2. Ensure you are using the Hardware SPI pins (GPIO 10, 9, 11)")
    print("      3. Swap SDI and SDO if unsure.")