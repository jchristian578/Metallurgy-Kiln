# config.py — Metallurgy Kiln Controller V2
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

#This file acts as the "brain" of your application, defining how the software interacts with your hardware, how it handles safety, and how it calculates heating logic.

from pathlib import Path

# ---------- PID gains  ---------- 
def _map_pid(d):
    out_min, out_max = d.get("output_limits", (0,100))
    return dict(Kp=d["Kp"], Ki=d["Ki"], Kd=d["Kd"], out_min=out_min, out_max=out_max, kd_filter=0.9, der_on_meas=True, bias=0.0)

#************************************* File Paths & App Settings *************************************
#These define where the application lives and stores its data.
#APP_NAME: The title displayed in the web browser tab (e.g., "Metallurgy Kiln V2").
#DATA_DIR: The main folder where the app stores all its dynamic data.
#STATE_FILE: A JSON file where the app saves its current status (current temp, current step, running state). Crucial for auto-resume: if the power fails, the app reads this file on reboot to know where it left off.
#PROFILE_DIR: The folder where your saved firing schedules (profiles) are stored.
#LOG_DIR: The folder where historical run logs (CSV files) are saved for review.

APP_NAME = "Metallurgy Kiln V2"
DATA_DIR    = Path("/home/jchristian/MetallurgyKiln/kiln_v2_data")
STATE_FILE  = DATA_DIR / "state.json"
PROFILE_DIR = DATA_DIR / "profiles"
LOG_DIR     = DATA_DIR / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

'''*****************************************************************************************************'''


#************************************* Server & UI Configuration *************************************
#WEB_HOST: The IP address the web server listens on. 192.168.1.110 is specific to your local network.
#WEB_PORT: Port 80 is the standard web port (so you don't have to type :5000 in the URL).
#POLL_INTERVAL_SEC: How often the main control loop runs. 1.0 means every 1 second, the kiln reads the temp, calculates PID, and adjusts the relays.
#DEF_TEMP_UNIT: The default unit (C or F) used when the app first loads.

WEB_HOST = "192.168.1.110"
WEB_PORT = int(80)
POLL_INTERVAL_SEC = float(1.0)
MOBILE_UI = True  
PROFILE_REFRESH_SEC = 600   
DEF_TEMP_UNIT = "C"

'''*****************************************************************************************************'''


#************************************* Watcher Configuration *************************************
#Settings for the independent monitoring script (watcher.py) that runs alongside the main controller.
#WATCHER_POLL_INTERVAL_SEC: How frequently (in seconds) the Watcher checks the main controller status.
#WATCHER_RUNAWAY_DELTA_C: The safety threshold for the Watcher. If the actual temperature exceeds the Setpoint by this amount (e.g., 30°C), the Watcher triggers a "Runaway" alert, assuming the relay is stuck closed.

WATCHER_POLL_INTERVAL_SEC = float(5.0)
WATCHER_RUNAWAY_DELTA_C = 30.0

'''*****************************************************************************************************'''


#************************************* Auto-Resume & Safety *************************************
#These settings determine how the kiln behaves after a power outage.
#AUTO_RESUME_ENABLED: "1" (True) allows the kiln to restart a firing automatically if power returns.
#AUTO_RESUME_DELAY_MIN: 0.5 minutes (30 seconds). The kiln waits this long after booting before resuming, allowing sensors to stabilize.
#AUTO_RESUME_MAX_GAP_MIN: 20.0. If power was out for longer than 20 minutes, it will not resume. (Too much heat lost; the metallurgy profile is likely ruined).
#AUTO_RESUME_MAX_TEMP_DROP_C: 50.0. If the temperature dropped more than 50°C during the outage, it will not resume (prevents thermal shock or invalid heat treatment).

AUTO_RESUME_ENABLED = "1"
AUTO_RESUME_DELAY_MIN = float(0.5)        
AUTO_RESUME_MAX_GAP_MIN   = float(20.0)   
AUTO_RESUME_MAX_TEMP_DROP_C = float(50.0) 

'''************************************************************************************************'''


#************************************* Simulation & Limits *************************************
#SIMULATION: "0" (False). If set to "1", the app ignores real hardware and "fakes" the temperature rise. Used for testing code without a kiln.

SIMULATION = "0"   

'''***********************************************************************************************'''


#************************************* Scheduling Behavior *************************************
#WAIT_FOR_KILN: "1" (True). This enables "Guaranteed Soak." If the kiln cannot keep up with the requested ramp rate, the clock pauses until the kiln catches up.
#CATCHUP_BAND_C: 15. The temperature must be within 15°C of the target for the clock to resume ticking.

WAIT_FOR_KILN = "1"     
CATCHUP_BAND_C = float(15)

'''***********************************************************************************************'''


#************************************* Energy & Cost *************************************
#Used solely for the UI "Estimated Cost" display.
#KWH_COST: The price of electricity in your area (dollars per kWh).
#KILN_WATTAGE_W: The total power rating of your heating elements (e.g., 7500W).

KWH_COST = float(0.2)    
KILN_WATTAGE_W = float(7500)  

'''*****************************************************************************************'''


#************************************* Thermocouple (MAX31856 Hardware) *************************************
#Settings for the digital sensor interface.
#TC_TYPE: "S". Specifies a Type S (Platinum) thermocouple.
#CS_PIN: The Chip Select pin (GPIO) for the SPI interface.


# Valid Thermocouple Types: (Use only the designated letter)
#    "B": adafruit_max31856.ThermocoupleType.B,
#    "E": adafruit_max31856.ThermocoupleType.E,
#    "J": adafruit_max31856.ThermocoupleType.J,
#    "K": adafruit_max31856.ThermocoupleType.K,
#    "N": adafruit_max31856.ThermocoupleType.N,
#    "R": adafruit_max31856.ThermocoupleType.R,
#    "S": adafruit_max31856.ThermocoupleType.S,
#    "T": adafruit_max31856.ThermocoupleType.T

TC_TYPE = "S"
CS_PIN = "D27"

'''************************************************************************************************************'''


#************************************* Signal Processing (Calibration) *************************************
#CAL_OFFSET_C / CAL_SCALE: Used to calibrate the sensor. Temp = (Raw * Scale) + Offset. Currently set to 1.0/0.0 (no correction).
#TC_LPF_ALPHA: 0.15. Low Pass Filter. This is a software smoother. 0.15 means "Trust the new reading 15%, and the old average 85%." This prevents the graph from looking jagged.
#TC_MIN_C / TC_MAX_C: The measurable range configured for the MAX31856 chip itself to prevent "Out of Range" errors (-50 to 1300C).
#TC_NOISE_FILTER_HZ: 60. Filters out 60Hz mains hum (power line interference).
#TC_AVG_SAMPLES: 10. The hardware chip averages 10 readings before sending one to the Pi, reducing signal noise.
#TC_CJ_LOW / TC_CJ_HIGH: Cold Junction (chip temperature) limits. If the box containing the Pi gets hotter than TC_CJ_HIGH (85°C), it flags an error to prevent chip damage.

CAL_OFFSET_C        = float(0.0) 
CAL_SCALE           = float(1.0)
TC_LPF_ALPHA        = float(0.15)
TC_MIN_C            = -50
TC_MAX_C            = float(1300)
TC_NOISE_FILTER_HZ  = int(60)  
TC_AVG_SAMPLES      = int(10)
TC_CJ_LOW           = -10.0
TC_CJ_HIGH          = 85.0

'''***********************************************************************************************************'''


#************************************* Limits & Default Rates *************************************
#MAX_TEMP_C: 1300.0. Hard Safety Limit. If the sensor reads higher than this, the software kills all relays immediately.
#OPEN_LOOP_FAILSAFE_SEC: 30.0. If the computer is commanding 100% power for 30 seconds but the temperature does not rise, it assumes the heating element is broken and shuts down.
#MAX_RATE_C_PER_MIN: 600.0. Prevents the user from accidentally typing an impossible ramp rate (like 10,000°/min) in the UI.
#MAX_SOAK_SEC: Safety timeout for a single step.
#GLOBAL_RUN_TIMEOUT_SEC: 72 Hours. A master safety timer. If a profile runs longer than this, the system forces a shutdown.
#DEFAULT_HEAT/COOL_RATE: When the user leaves the "Rate" box empty in the UI builder, it uses these defaults (e.g., 38°C/min) to calculate the estimated run time.

MAX_TEMP_C = float(1300.0)  
OPEN_LOOP_FAILSAFE_SEC = float(30.0) 

MAX_RATE_C_PER_MIN = 600.0 
MAX_SOAK_SEC = 48*3600 
GLOBAL_RUN_TIMEOUT_SEC = 72*3600

DEFAULT_HEAT_RATE_C_PER_MIN = 38.06
DEFAULT_COOL_RATE_C_PER_MIN = 30.0

'''**************************************************************************************************'''


#************************************* Relays / GPIO *************************************
#GPIO_MODE: "BCM". Uses Broadcom GPIO numbering (e.g., GPIO 17) rather than physical pin numbers (Pin 11).
#RELAY_ACTIVE_HIGH: "1". Tells the code that setting the pin High (3.3V) turns the relay ON.
#PWM_WINDOW_SEC: 2.0. The switching cycle. If output is 50%, the relay is ON for 1s, OFF for 1s.
#PWM_STAGGER_SEC: 1.0. Load Balancing. If you have two relays, this delays Relay 2 by 1 second so both don't turn on at the exact same millisecond.
#BUTTON_PROFILE_STOP_PIN: GPIO pin for the Red Stop button. Pressing this immediately aborts the firing.
#BUTTON_RESTART_SERVICES_PIN: GPIO pin for the Service Restart Button. Used to reboot the software if the UI freezes.
#BUTTON_SYSTEM_REBOOT_PIN: GPIO pin to fully reboot the Raspberry Pi hardware.
#BUTTON_HOLD_TIME_SEC: Safety delay (3s). You must hold the restart/reboot buttons for this long to trigger them.

GPIO_MODE = "BCM"
RELAY_1_PIN = int(23)
RELAY_2_PIN = int(24)
RELAY_ACTIVE_HIGH = "1" 
PWM_WINDOW_SEC = float(2.0) 
PWM_STAGGER_SEC = float(1.0)  

BUTTON_PROFILE_STOP_PIN = 22        # GPIO 22 (Physical Pin 15)
BUTTON_RESTART_SERVICES_PIN = 4     # GPIO 4 (Physical Pin 7)
BUTTON_SYSTEM_REBOOT_PIN = 17       # GPIO 17 (Physical Pin 11)
BUTTON_HOLD_TIME_SEC = 3            # Time to hold restart button to trigger

'''*****************************************************************************************'''


#************************************* Control Strategy (PID) *************************************
#This is the advanced math that keeps the temperature stable. You have a Dual PID setup:
#CONTROL_CROSSOVER_C: 550.0.
#Below 550°C: Uses PID_TEMPER_CONF.
#Above 550°C: Uses PID_HIGH_CONF.
#Why? Low temp tempering usually requires aggressive control (High Kp), while high-temp soaking requires gentler control to prevent overshoot.
#The PID Variables:
#Kp (Proportional): The "Muscle." How hard to push based on how far away you are.
#Ki (Integral): The "Memory." Adds power if you've been sitting below the target for a long time (fixes droop).
#Kd (Derivative): The "Brake." Reduces power if the temperature is rising too fast (prevents overshoot).

CONTROL_CROSSOVER_C = 500.0
ENABLE_DUAL_COIL_LOW_TEMP = False 
PID_TEMPER_CONF = {"Kp": 129.8795, "Ki": 4.4357, "Kd": 274.3807, "output_limits": (0, 100)}
PID_HIGH_CONF   = {"Kp": 96.1607, "Ki": 17.9295, "Kd": 37.2103, "output_limits": (0, 100)}

PID_TEMPER = _map_pid(PID_TEMPER_CONF)
PID_HIGH   = _map_pid(PID_HIGH_CONF) 

'''
******************************************
************** HIGH RESULTS **************
******************************************

[CALC] Calculating PID Values...
------------------------------------------------------------
RESULTS FOR 800.0 C
Oscillation Amp : 0.27 C
Critical Period : 2.44 sec
Ultimate Gain   : 470.1192
------------------------------------------------------------
TYPE                 | Kp         | Ki         | Kd
------------------------------------------------------------
1. Aggressive (Z-N)  | 282.0715   | 231.4105   | 85.9558
2. Balanced (T-L)    | 96.1607    | 17.9295    | 37.2103     <-- RECOMMENDED
3. No Overshoot      | 94.0238    | 77.1368    | 76.4052
------------------------------------------------------------

============================================================
COPY/PASTE BLOCKS FOR config.py
============================================================

# OPTION 1: Aggressive (Ziegler-Nichols)
PID_TEMPER_CONF = {"Kp": 282.0715, "Ki": 231.4105, "Kd": 85.9558, "output_limits": (0, 100)}

# OPTION 2: Balanced (Tyreus-Luyben) <-- RECOMMENDED
PID_TEMPER_CONF = {"Kp": 96.1607, "Ki": 17.9295, "Kd": 37.2103, "output_limits": (0, 100)}

# OPTION 3: No Overshoot
PID_TEMPER_CONF = {"Kp": 94.0238, "Ki": 77.1368, "Kd": 76.4052, "output_limits": (0, 100)}

(Note: Rename to PID_HIGH_CONF if tuning for high temp)



******************************************
************* TEMPER RESULTS *************
******************************************

[CALC] Calculating PID Values...
------------------------------------------------------------
RESULTS FOR 200.0 C
Oscillation Amp : 0.35 C
Critical Period : 22.34 sec
Ultimate Gain   : 367.6120
------------------------------------------------------------
TYPE                 | Kp         | Ki         | Kd
------------------------------------------------------------
1. Aggressive (Z-N)  | 220.5672   | 19.7448    | 615.9840
2. Balanced (T-L)    | 75.1934    | 1.5298     | 266.6597    <-- RECOMMENDED
3. No Overshoot      | 73.5224    | 6.5816     | 547.5413
------------------------------------------------------------

============================================================
COPY/PASTE BLOCKS FOR config.py
============================================================

# OPTION 1: Aggressive (Ziegler-Nichols)
PID_TEMPER_CONF = {"Kp": 220.5672, "Ki": 19.7448, "Kd": 615.9840, "output_limits": (0, 100)}

# OPTION 2: Balanced (Tyreus-Luyben) <-- RECOMMENDED
PID_TEMPER_CONF = {"Kp": 75.1934, "Ki": 1.5298, "Kd": 266.6597, "output_limits": (0, 100)}

# OPTION 3: No Overshoot
PID_TEMPER_CONF = {"Kp": 73.5224, "Ki": 6.5816, "Kd": 547.5413, "output_limits": (0, 100)}

(Note: Rename to PID_HIGH_CONF if tuning for high temp)
'''

'''**************************************************************************************************'''


#************************************* History *************************************
#HISTORY_MAX_SAMPLES: Limits the graph data to 30,000 points to prevent the Raspberry Pi from running out of RAM during very long firings.

HISTORY_MAX_SAMPLES = int(30000)  
HISTORY_DECIMATE    = int(1)

'''***********************************************************************************'''


#************************************* LCD Display *************************************
#USE_LCD: Set to True to enable the 20x4 LCD screen output. Set to False if no screen is connected.
#LCD_PRINT_INTERVAL_SEC: How often (in seconds) the screen updates. 2.0 is standard; faster updates may cause flickering.
#LCD_I2C_EXPANDER: The interface chip type. Almost always 'PCF8574' for standard LCD backpacks.
#LCD_ADDRESS: The hexadecimal I2C address of the screen. 0x27 is standard, though 0x3F is also common. (Check with i2cdetect -y 1).
#LCD_COLS / LCD_ROWS: Dimensions of the display. Set to 20 and 4 for a standard 20x4 screen.
#LCD_DOTSIZE: The pixel height of the characters. 8 is the standard default.
#LCD_CHARMAP: The internal font map. 'A02' is the standard default.
#LCD_AUTO_LINEBREAKS: If True, text too long for one row wraps to the next automatically.
#LCD_BACKLIGHT: Controls whether the screen backlight stays on (True) or off (False).

USE_LCD = True
LCD_PRINT_INTERVAL_SEC = 1.0
LCD_I2C_EXPANDER = 'PCF8574'
LCD_ADDRESS = 0x27        # Standard I2C Address (Run 'i2cdetect -y 1' to confirm)
LCD_COLS = 20
LCD_ROWS = 4
LCD_DOTSIZE = 8
LCD_CHARMAP = 'A02'
LCD_AUTO_LINEBREAKS = True
LCD_BACKLIGHT = True

'''***********************************************************************************'''

#************************************* RPi Temperature Alert *************************************
# This setting defines the maximum safe operating temperature (in Celsius) for the Raspberry Pi's internal CPU. 
# Because the controller is likely operating near a hot kiln, monitoring the ambient hardware temperature is critical. 
# If the Pi's temperature exceeds this value, the Watcher will trigger an immediate "RPI OVERHEATING" push notification. 
# To prevent  alert spam, the alarm will only reset once the Pi cools down by at least 3°C below this threshold.
#
# Reference Values:
#   • 40.0 - 65.0 : Normal operating temperature under standard load.
#   • 70.0 - 75.0 : [RECOMMENDED] Ideal alert threshold. Gives you a warning while the Pi is still functioning perfectly.
#   • 80.0        : Throttling limit. The Pi's operating system will forcefully slow down the processor to reduce heat generation.
#   • 85.0        : Critical limit. The Pi will force a hard shutdown to prevent permanent physical damage to the silicon.

WATCHER_MAX_RPI_TEMP = 75

'''***********************************************************************************'''

#************************************* WATCHER Max Temperature Lag *************************************
# This setting defines the maximum allowable temperature gap (in Celsius) between your profile's current setpoint and the actual kiln temperature. 
# If the kiln falls behind by more than this amount, the Watcher triggers a "TRACKING ERROR" warning. 
# This usually indicates that your profile's programmed
# heating rate is faster than the kiln can physically achieve, or that your heating elements are beginning to degrade/fail. 
# The alert will automatically reset once the kiln catches up to within 5°C of this threshold.
#
# Reference Values:
#   • 10.0 - 20.0 : Very strict. May cause false alarms during fast ramps.
#   • 30.0 - 50.0 : [RECOMMENDED] Ideal balance. Allows for normal PID lag during a ramp but catches genuine heating struggles.
#   • 60.0+       : Loose tracking. Best for naturally slow kilns where you only want to be alerted to massive performance drops.

WATCHER_MAX_LAG_C = 40.0

'''***********************************************************************************'''

#************************************* Aux Buttons *************************************
#AUX_BUTTON_HOLD_TIME_SEC: How long (in seconds) a button must be held to trigger the start. This prevents accidental activation if the button is bumped.
#AUX_BUTTON_x_PIN: The GPIO pin (BCM) connected to the physical button.
#AUX_BUTTON_x_PROFILE: The exact filename of the profile to load (e.g., "Normalizing.json"). If empty, the button is disabled.
#AUX_BUTTON_x_UI_LABEL: The text displayed on the button in the web interface.

# --- PHYSICAL AUX BUTTONS ---
# How long (in seconds) a button must be held to trigger the start
AUX_BUTTON_HOLD_TIME_SEC = 2.0  

# Pin Definitions (BCM numbering)
AUX_BUTTON_1_PIN = 5
AUX_BUTTON_2_PIN = 6
AUX_BUTTON_3_PIN = 26
AUX_BUTTON_4_PIN = 16

# Profile Mapping (Must match filename exactly, e.g. "Temper.json")
AUX_BUTTON_1_PROFILE = "Forging 780C 12 Hour"
AUX_BUTTON_2_PROFILE = "Forging 800C 12 Hour"
AUX_BUTTON_3_PROFILE = "Temper 190C"
AUX_BUTTON_4_PROFILE = "Temper 200C"

# UI Labels (Text shown on the web buttons)
AUX_BUTTON_1_UI_LABEL = "Forging 780C"
AUX_BUTTON_2_UI_LABEL = "Forging 800C"
AUX_BUTTON_3_UI_LABEL = "Temper 190C"
AUX_BUTTON_4_UI_LABEL = "Temper 200C"

'''***********************************************************************************'''