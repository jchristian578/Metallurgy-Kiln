import board
import digitalio
import adafruit_max31856

# Deprecated: Reference temperature thresholds and temperature thresholds have been added to the TC initialization. 

# --- CONFIGURATION ---
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D27) # Change D5 if needed
cs.direction = digitalio.Direction.OUTPUT

sensor = adafruit_max31856.MAX31856(spi, cs)

print("--- CURRENT SETTINGS ---")
print(f"Current Cold Junction Temp: {sensor.reference_temperature} C")

# Read current limits (returns a tuple: (low, high))
try:
    low, high = sensor.reference_temperature_thresholds
    print(f"Current CJ Limits: Low={low} C, High={high} C")
except AttributeError:
    print("Could not read current limits (Attribute mismatch).")

# --- THE FIX ---
print("\n--- RESETTING THRESHOLDS ---")
# Set (Low Limit, High Limit)
# Default is usually (-10, 80)
sensor.reference_temperature_thresholds = (-10.0, 85.0)

# Verify
new_low, new_high = sensor.reference_temperature_thresholds
print(f"NEW CJ Limits: Low={new_low} C, High={new_high} C")

# Check status
print("\n--- FAULT CHECK ---")
faults = sensor.fault
if any(faults.values()):
    print("Faults still active:", faults)
else:
    print("FAULTS CLEARED! System is healthy.")