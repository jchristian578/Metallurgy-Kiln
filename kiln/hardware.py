# kiln/hardware.py — MAX31856 thermocouple I/O for Kiln Controller V2 — Metallurgy Kiln Controller V2
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

from __future__ import annotations
from dataclasses import dataclass
import time
import math
import random 
from typing import Optional, Dict

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config as CFG

# Robust config accessor
def _cfg_get(cfg, key, default=None):
    if hasattr(cfg, key): return getattr(cfg, key)
    if hasattr(cfg, "Config") and hasattr(cfg.Config, key): return getattr(cfg.Config, key)
    return default

@dataclass
class ThermoReading:
    c: Optional[float]
    fault: Optional[Dict] = None
    ts: int = 0
    @property
    def ok(self) -> bool: return self.fault is None and self.c is not None
    @property
    def temp_c(self) -> Optional[float]: return self.c

@dataclass
class ThermoConfig:
    cs_pin: str = "D5"
    tc_type: str = "K"
    noise_hz: int = 60
    avg_samples: int = 4
    lpf_alpha: float = 0.25
    cal_offset_c: float = 0.0
    cal_scale: float = 1.0
    tc_min_c: float = -50.0
    tc_max_c: float = 1400.0
    cj_low_c: float = -10.0
    cj_high_c: float = 85.0
    two_decimals: bool = True
    simulate: bool = False

    @classmethod
    def from_cfg(cls, cfg) -> "ThermoConfig":
        # Handle string "0" correctly
        sim_val = _cfg_get(cfg, "SIMULATION", "0")
        is_sim = str(sim_val).strip() == "1"

        return cls(
            cs_pin=_cfg_get(cfg, "CS_PIN", "D5"),
            tc_type=str(_cfg_get(cfg, "TC_TYPE", "K")).upper(),
            noise_hz=int(_cfg_get(cfg, "TC_NOISE_FILTER_HZ", 60)),
            avg_samples=int(_cfg_get(cfg, "TC_AVG_SAMPLES", 4)),
            lpf_alpha=float(_cfg_get(cfg, "TC_LPF_ALPHA", 0.25)),
            cal_offset_c=float(_cfg_get(cfg, "CAL_OFFSET_C", 0.0)),
            cal_scale=float(_cfg_get(cfg, "CAL_SCALE", 1.0)),
            tc_min_c=float(_cfg_get(cfg, "TC_MIN_C", -50.0)),
            tc_max_c=float(_cfg_get(cfg, "TC_MAX_C", 1300.0)),
            cj_low_c=float(_cfg_get(cfg, "TC_CJ_LOW", -10.0)),
            cj_high_c=float(_cfg_get(cfg, "TC_CJ_HIGH", 85.0)),
            two_decimals=True,
            simulate=is_sim,
        )

class ThermoFault(Exception): pass

class Thermocouple:
    def read_c(self) -> float: raise NotImplementedError
    def info(self) -> dict: return {}
    def sim_inject_power(self, d1: float, d2: float): pass
    def read(self) -> "ThermoReading":
        try:
            c = self.read_c()
            return ThermoReading(c=c, fault=None, ts=int(time.time()))
        except ThermoFault as e:
            return ThermoReading(c=None, fault={"message": str(e), "code": getattr(e, "code", None)}, ts=int(time.time()))

class SimThermocouple(Thermocouple):
    """Physics-based thermal model with artificial noise."""
    def __init__(self, conf: ThermoConfig):
        self.cfg = conf
        self._t = 25.0
        self._ambient = 25.0
        self._last = time.monotonic()
        self._thermal_mass = 500.0  
        self._loss_coeff = 2.0      
        self._heater_power = 8000.0 

    def sim_inject_power(self, d1: float, d2: float):
        now = time.monotonic()
        dt = max(1e-4, now - self._last)
        self._last = now
        power_in = (d1 + d2) * 0.5 * self._heater_power
        power_loss = (self._t - self._ambient) * self._loss_coeff
        net_energy = (power_in - power_loss) * dt
        self._t += net_energy / self._thermal_mass

    def read_c(self) -> float:
        now = time.monotonic()
        if (now - self._last) > 0.5:
            self.sim_inject_power(0, 0)
        jitter = random.uniform(-0.15, 0.15)
        return round(self._t + jitter, 2)

    def info(self) -> dict:
        return {"kind": "sim", "type": self.cfg.tc_type, "note": "Physics+Noise"}

class MAX31856Thermocouple(Thermocouple):
    def __init__(self, conf: ThermoConfig):
        self.cfg = conf
        self._ema = None
        try:
            import board, busio, digitalio
            import adafruit_max31856 as MAX
        except Exception as e:
            self._fallback_to_sim(f"Import failed: {e!r}")
            return

        try:
            spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
            for _ in range(100):
                if spi.try_lock():
                    spi.configure(baudrate=500000)
                    spi.unlock()
                    break
                time.sleep(0.005)
            cs_pin_name = str(self.cfg.cs_pin).upper()
            cs_pin = getattr(board, cs_pin_name)
            cs = digitalio.DigitalInOut(cs_pin)
            
            tmap = {
                "B": MAX.ThermocoupleType.B, "E": MAX.ThermocoupleType.E,
                "J": MAX.ThermocoupleType.J, "K": MAX.ThermocoupleType.K,
                "N": MAX.ThermocoupleType.N, "R": MAX.ThermocoupleType.R,
                "S": MAX.ThermocoupleType.S, "T": MAX.ThermocoupleType.T,
            }
            max_tc_type = tmap.get(self.cfg.tc_type, MAX.ThermocoupleType.K)

            sensor = MAX.MAX31856(spi, cs, thermocouple_type=max_tc_type)

            # Apply Filters & Sampling (Robust try/except)
            try: 
                # Note: Some libs use 'noise_rejection_60hz', some use 'filter_50hz'
                # Your logic sets 50hz=True if config says 50, otherwise False (60Hz)
                sensor.filter_50hz = True if int(self.cfg.noise_hz) == 50 else False
            except: 
                pass
                
            try: 
                sensor.sampling = int(self.cfg.avg_samples)
            except: 
                pass

            # Reset Fault Thresholds (Crucial for eliminating CJ/TC High errors)
            try: 
                sensor.reference_temperature_thresholds = (self.cfg.cj_low_c, self.cfg.cj_high_c)
            except AttributeError:
                pass 
            except Exception as e:
                print(f"Warning: Could not set CJ thresholds: {e}")
                
            # Reset Temperature Range (Prevents 'tc_high' errors on reboot)
            try:
                sensor.temperature_thresholds = (self.cfg.tc_min_c, self.cfg.tc_max_c)
            except:
                pass

            self._sensor = sensor
        except Exception as e:
            self._fallback_to_sim(f"SPI/CS init failed: {e!r}")

    def _fallback_to_sim(self, note: str):
        print(f"WARNING: Hardware init failed, falling back to Simulation. Reason: {note}")
        self.sim = SimThermocouple(self.cfg)
        self.sim_note = note
        self.read_c = self._sim_read  # type: ignore
        self.info = self._sim_info    # type: ignore
        self.sim_inject_power = self.sim.sim_inject_power

    def _sim_read(self) -> float: return self.sim.read_c()
    def _sim_info(self) -> dict:
        base = self.sim.info()
        base["note"] = getattr(self, "sim_note", "")
        return base

    def _apply_cal_smooth(self, c: float) -> float:
        c = (c * float(self.cfg.cal_scale)) + float(self.cfg.cal_offset_c)
        c = max(self.cfg.tc_min_c, min(self.cfg.tc_max_c, c))
        a = max(0.0, min(1.0, float(self.cfg.lpf_alpha)))
        if self._ema is None: self._ema = c
        else: self._ema = (1 - a) * self._ema + a * c
        return round(self._ema, 2) if self.cfg.two_decimals else self._ema

    def _fault_text(self, sensor) -> str:
        try:
            f = sensor.fault
            if not f: return ""
            return f"MAX31856 fault=0x{int(f):02X}"
        except: return "MAX31856 fault"

    def read_c(self) -> float:
        try:
            raw = float(self._sensor.temperature)
            return self._apply_cal_smooth(raw)
        except Exception as e:
            raise ThermoFault(str(e))
    
    def sim_inject_power(self, d1: float, d2: float): pass

    def info(self) -> dict:
        out = {"kind": "max31856", "type": self.cfg.tc_type}
        try: out["fault"] = self._fault_text(self._sensor)
        except: pass
        return out

def build_thermocouple(cfg_module) -> Thermocouple:
    conf = ThermoConfig.from_cfg(cfg_module)
    if conf.simulate:
        return SimThermocouple(conf)
    return MAX31856Thermocouple(conf)

class Relays:
    def __init__(self, cfg):
        self.window_s = float(_cfg_get(cfg, "PWM_WINDOW_SEC", 2.0))
        self.phase_frac = float(_cfg_get(cfg, "RELAY_PHASE_FRAC", 0.5))
        self.active_high = bool(_cfg_get(cfg, "RELAY_ACTIVE_HIGH", True))
        self.pin1 = int(_cfg_get(cfg, "RELAY_1_PIN", 17))
        self.pin2 = int(_cfg_get(cfg, "RELAY_2_PIN", 27))
        self._hw = "sim"
        self._GPIO = None
        try:
            import RPi.GPIO as GPIO
            mode = str(_cfg_get(cfg, "GPIO_MODE", "BCM")).upper()
            GPIO.setmode(GPIO.BCM if mode == "BCM" else GPIO.BOARD)
            init_level = GPIO.LOW if self.active_high else GPIO.HIGH
            GPIO.setup(self.pin1, GPIO.OUT, initial=init_level)
            GPIO.setup(self.pin2, GPIO.OUT, initial=init_level)
            self._GPIO = GPIO
            self._hw = "gpio"
        except Exception:
            self._GPIO = None
            self._hw = "sim"
        self.duty1 = 0.0
        self.duty2 = 0.0
        self._t0 = time.monotonic()

    def set_duty(self, d1: float, d2: float):
        self.duty1 = max(0.0, min(100.0, float(d1)))
        self.duty2 = max(0.0, min(100.0, float(d2)))

    def _write_pin(self, pin: int, on: bool):
        if self._hw == "gpio" and self._GPIO is not None:
            level = self._GPIO.HIGH if (on == self.active_high) else self._GPIO.LOW
            self._GPIO.output(pin, level)

    def tick(self, now: float | None = None) -> tuple[int, int]:
        now = now or time.monotonic()
        w = self.window_s
        phase = self.phase_frac * w
        t_in_w1 = (now - self._t0) % w
        on1 = t_in_w1 < (self.duty1 / 100.0) * w
        t_in_w2 = (now - (self._t0 + phase)) % w
        on2 = t_in_w2 < (self.duty2 / 100.0) * w
        self._write_pin(self.pin1, on1)
        self._write_pin(self.pin2, on2)
        return (100 if on1 else 0, 100 if on2 else 0)

    # --- THIS WAS MISSING ---
    def safe_down(self):
        """Immediately turn both outputs off."""
        self.set_duty(0.0, 0.0)
        self._write_pin(self.pin1, False)
        self._write_pin(self.pin2, False)
    # ------------------------

    def close(self):
        if self._hw == "gpio" and self._GPIO is not None:
            try: self._GPIO.cleanup([self.pin1, self.pin2])
            except Exception: pass

    def info(self) -> dict:
        return {"driver": self._hw, "pins": [self.pin1, self.pin2]}