# kiln/pid.py — dual PID with anti-windup and bumpless transfer support — Metallurgy Kiln Controller V2
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

from dataclasses import dataclass, field
import time
from typing import Optional

@dataclass
class PID:
    Kp: float
    Ki: float
    Kd: float
    out_min: float = 0.0
    out_max: float = 100.0
    kd_filter: float = 0.9
    der_on_meas: bool = True
    bias: float = 0.0

    _last_t: Optional[float] = field(default=None, init=False)
    _i: float = field(default=0.0, init=False)
    _last_x: Optional[float] = field(default=None, init=False)
    _last_e: Optional[float] = field(default=None, init=False)
    _d_est: float = field(default=0.0, init=False)

    def reset(self):
        self._last_t = None
        self._i = 0.0
        self._last_x = None
        self._last_e = None
        self._d_est = 0.0
    
    # --- THIS WAS MISSING ---
    def update_tunings(self, Kp=None, Ki=None, Kd=None):
        """
        Update gains on the fly for Gain Scheduling (Bumpless Transfer).
        Preserves the current integral accumulation (_i) to prevent output jumps.
        """
        if Kp is not None: self.Kp = float(Kp)
        if Ki is not None: self.Ki = float(Ki)
        if Kd is not None: self.Kd = float(Kd)
    # ------------------------

    def compute(self, sp: float, pv: float, now: Optional[float] = None) -> float:
        t = now if now is not None else time.monotonic()
        if self._last_t is None:
            self._last_t = t
            self._last_x = pv
            self._last_e = sp - pv
            return self._clamp(self.bias)

        dt = max(1e-6, t - self._last_t)
        e = sp - pv

        # Proportional
        p = self.Kp * e

        # Integral with anti-windup (clamped)
        self._i += self.Ki * e * dt
        u_unclamped = p + self._i + self.bias

        # Derivative
        if self.der_on_meas:
            dx = (pv - (self._last_x if self._last_x is not None else pv)) / dt
            d = -self.Kd * dx
        else:
            de = (e - (self._last_e if self._last_e is not None else e)) / dt
            d = self.Kd * de

        # Low-pass filter derivative for noise
        self._d_est = self.kd_filter * self._d_est + (1 - self.kd_filter) * d

        # Combine
        u = u_unclamped + self._d_est
        u_clamped = self._clamp(u)

        # Back-calc AWU
        if u != u_clamped:
            self._i += (u_clamped - u)

        self._last_t = t
        self._last_x = pv
        self._last_e = e
        return u_clamped

    def _clamp(self, v: float) -> float:
        return max(self.out_min, min(self.out_max, v))