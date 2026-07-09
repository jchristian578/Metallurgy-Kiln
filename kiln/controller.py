# kiln/controller.py — — Metallurgy Kiln Controller V2
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
import time, math, threading, csv
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .pid import PID
from .hardware import build_thermocouple, Relays, ThermoReading
from pathlib import Path
import json
import os

def _finite(x):
    try:
        xf = float(x)
        return xf if math.isfinite(xf) else None
    except Exception:
        return None

@dataclass
class Step:
    kind: str
    target_c: float
    duration_sec: int = 0
    rate_c_per_min: float = 0.0

@dataclass
class HistoryPoint:
    ts: float
    t_kiln: float
    t_total: float
    temp: float
    sp: float

class HistoryRing:
    def __init__(self, capacity=10000):
        self.capacity = capacity
        self.buf: List[HistoryPoint] = []
        self.lock = threading.Lock()

    def clear(self):
        with self.lock:
            self.buf.clear()

    def append(self, p: HistoryPoint):
        with self.lock:
            self.buf.append(p)
            if len(self.buf) > self.capacity:
                self.buf = self.buf[-self.capacity:]

    def snapshot(self) -> List[Dict[str, float]]:
        with self.lock:
            out = []
            for x in self.buf:
                out.append(dict(
                    ts=x.ts,
                    t_kiln=_finite(x.t_kiln),
                    t_total=_finite(x.t_total),
                    temp=_finite(x.temp),
                    sp=_finite(x.sp),
                ))
            return out


class Controller:
    def __init__(self, config):
        self.cfg = config
        self.tc = build_thermocouple(config)
        self.relays = Relays(config)
        
        self.pid = PID(**config.PID_TEMPER)
        self.active_pid_profile = "TEMPER"
        
        self.sample_period = float(config.POLL_INTERVAL_SEC)
        self.history = HistoryRing(capacity=getattr(config, "HISTORY_MAX_SAMPLES", 20000))
        
        self.running = False
        self.running_profile_name = None
        self.start_monotonic = None
        
        # FIX: Start as None so we don't count idle time
        self.start_total = None 
        
        self.schedule: List[Step] = []
        self.current_sp = 0.0
        self.current_step_idx = 0
        self.auto_resumed = False 
        
        self.wait_for_kiln = bool(getattr(config, "WAIT_FOR_KILN", False))
        self.catchup_band_c = float(getattr(config, "CATCHUP_BAND_C", 10.0))
        
        self.crossover_c = float(getattr(config, "CONTROL_CROSSOVER_C", 550.0))
        self.dual_coil_low = bool(getattr(config, "ENABLE_DUAL_COIL_LOW_TEMP", False))
        
        self.state_path = Path(getattr(self.cfg, "STATE_FILE", "state.json"))
        self.log_dir = Path(getattr(self.cfg, "LOG_DIR", "logs"))
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._last_state_dump = 0.0
        self._csv_file = None
        self._csv_writer = None
        
        self._lock = threading.Lock()
        self._thread = None
        self._stop_flag = threading.Event()
        self._t_into = 0.0
        self._last_tick = time.monotonic()
        
        self._maybe_schedule_auto_resume()

    def ack_auto_resume(self):
        self.auto_resumed = False

    def _planned_total_runtime(self) -> float:
        if not self.schedule: return 0.0
        rt = 0.0
        last_target = self.schedule[0].target_c
        for s in self.schedule:
            if s.kind == "ramp" and s.rate_c_per_min:
                dt = abs(s.target_c - last_target) / max(1e-6, s.rate_c_per_min) * 60.0
                rt += dt
            elif s.kind == "soak":
                rt += s.duration_sec
            last_target = s.target_c
        return rt

    def _compute_sp(self, t_into: float) -> float:
        if not self.schedule: return 25.0
        last_target = self.schedule[0].target_c
        elapsed = 0.0
        for i, s in enumerate(self.schedule):
            if s.kind == "ramp" and s.rate_c_per_min:
                dt = abs(s.target_c - last_target) / s.rate_c_per_min * 60.0
                if t_into < elapsed + dt:
                    frac = (t_into - elapsed) / dt
                    sp = last_target + math.copysign(frac * abs(s.target_c - last_target), s.target_c - last_target)
                    self.current_step_idx = i
                    return sp
                elapsed += dt
                last_target = s.target_c
            else:
                target = s.target_c
                if s.kind == "soak":
                    if t_into < elapsed + s.duration_sec:
                        self.current_step_idx = i
                        return target
                    elapsed += s.duration_sec
                last_target = target
        self.current_step_idx = len(self.schedule) - 1
        return last_target

    def _state_payload(self) -> dict:
        now = time.monotonic()
        kiln_elapsed = self._t_into if self.running else 0.0
        
        # Calculate total elapsed only if running and start time is valid
        total_elapsed = 0.0
        if self.running and self.start_total is not None:
            total_elapsed = time.time() - self.start_total
        
        return {
            "version": 3,
            "ts": int(time.time()),
            "running": bool(self.running),
            "name": self.running_profile_name,
            "kiln_elapsed_sec": float(kiln_elapsed),
            "total_elapsed_sec": float(total_elapsed),
            "last_sp": self.current_sp,
            "schedule": {"steps": [s.__dict__ for s in self.schedule]},
        }

    def _dump_state(self, force: bool = False):
        try:
            now = time.monotonic()
            if not force and (now - self._last_state_dump) < 2.0: return
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 1. Create a temporary path
            temp_path = self.state_path.with_suffix('.tmp')
            
            # 2. Write to the temporary file
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self._state_payload(), f, indent=2)
                f.flush()
                os.fsync(f.fileno()) # Force write to physical disk
                
            # 3. Atomically overwrite the real state file
            # This guarantees state.json is never empty or half-written
            os.replace(temp_path, self.state_path)
            
            self._last_state_dump = now
        except Exception: pass

    def _init_csv_log(self):
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = self.log_dir / f"run_{timestamp}.csv"
            self._csv_file = open(filename, "w", newline='')
            self._csv_writer = csv.writer(self._csv_file)
            self._csv_writer.writerow(["timestamp", "t_kiln", "temp_c", "sp_c", "output_pct", "pid_profile"])
        except Exception as e:
            print(f"Failed to start CSV log: {e}")

    def _log_csv(self, t_kiln, temp, sp, output, pid_profile):
        if self._csv_writer:
            try:
                self._csv_writer.writerow([
                    f"{time.time():.2f}", 
                    f"{t_kiln:.2f}", 
                    f"{temp:.2f}", 
                    f"{sp:.2f}", 
                    f"{output:.2f}",
                    pid_profile
                ])
                self._csv_file.flush()
                # Force the OS to sync the file to the physical drive immediately
                os.fsync(self._csv_file.fileno())
            except: pass

    def _maybe_schedule_auto_resume(self):
        try:
            if not getattr(self.cfg, "AUTO_RESUME_ENABLED", False): return
            if not self.state_path.exists(): return

            with open(self.state_path, "r", encoding="utf-8") as f:
                st = json.load(f)

            if not st.get("running"): return

            steps = (st.get("schedule", {}) or {}).get("steps") or []
            if not steps: return

            last_ts = float(st.get("ts", 0))
            last_sp = float(st.get("last_sp", 0))
            
            try:
                if hasattr(self.tc, "read"):
                    current_reading = self.tc.read()
                    current_temp = current_reading.temp_c
                else:
                    current_temp = float(self.tc.read_c())

                if current_temp is not None and last_sp > 0:
                    drop = last_sp - current_temp
                    max_drop = float(getattr(self.cfg, "AUTO_RESUME_MAX_TEMP_DROP_C", 50.0))
                    if drop > max_drop:
                        print(f"ABORT RESUME: Temp dropped {drop:.1f}C (Max {max_drop}C). Structure compromised.")
                        return
            except Exception: pass

            gap_sec = max(0.0, time.time() - last_ts)
            max_gap = float(getattr(self.cfg, "AUTO_RESUME_MAX_GAP_MIN", 0.0)) * 60.0
            if max_gap > 0 and gap_sec > max_gap: return

            delay_sec = max(0.0, float(getattr(self.cfg, "AUTO_RESUME_DELAY_MIN", 0.0)) * 60.0)
            
            saved_kiln_time = float(st.get("kiln_elapsed_sec", 0))
            saved_total_time = float(st.get("total_elapsed_sec", 0))

            print(f"Auto-resuming {st.get('name', 'Unknown')} in {delay_sec}s...")
            
            def _resume():
                try:
                    self.start_profile(
                        steps, 
                        name=st.get("name"), 
                        start_at_elapsed_sec=saved_kiln_time,
                        start_total_elapsed_sec=saved_total_time
                    )
                    self.auto_resumed = True
                except Exception: pass

            self._resume_timer = threading.Timer(delay_sec, _resume)
            self._resume_timer.daemon = True
            self._resume_timer.start()
        except Exception as e:
            print(f"Resume failed: {e}")
    """
    def start_profile(self, steps: list[dict], name: str | None = None, start_at_elapsed_sec: float = 0.0, start_total_elapsed_sec: float = 0.0):
        with self._lock:
            fixed = []
            for s in steps:
                kind = s.get("kind","soak")
                target = float(s.get("target_c", 25.0))
                rate = float(s.get("rate_c_per_min", 0.0))
                dur = int(s.get("duration_sec", 0))
                fixed.append(Step(kind=kind, target_c=target, duration_sec=dur, rate_c_per_min=rate))

            self._schedule = {"steps": steps}
            self.running_profile_name = name
            self.schedule = fixed
            self.history.clear()
            
            self._t_into = max(0.0, float(start_at_elapsed_sec))
            self.start_total = time.time() - max(0.0, float(start_total_elapsed_sec))
            self.start_monotonic = time.monotonic()
            
            self._last_tick = time.monotonic()
            
            self.auto_resumed = False
            self.pid.reset()
            self.active_pid_profile = "INIT"
            
            self.running = True
            self._stop_flag.clear()
            self._init_csv_log()
            
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._loop, daemon=True)
                self._thread.start()

            self._dump_state(force=True)
    """

    def start_profile(self, steps: list[dict], name: Optional[str] = None, start_at_elapsed_sec: float = 0.0, start_total_elapsed_sec: float = 0.0):
        with self._lock:
            fixed = []
            for s in steps:
                kind = s.get("kind","soak")
                target = float(s.get("target_c", 25.0))
                rate = float(s.get("rate_c_per_min", 0.0))
                dur = int(s.get("duration_sec", 0))
                fixed.append(Step(kind=kind, target_c=target, duration_sec=dur, rate_c_per_min=rate))

            try:
                if hasattr(self.tc, "read"):
                    current_c = self.tc.read().temp_c
                else:
                    current_c = float(self.tc.read_c())
                if current_c is None: current_c = 25.0
            except Exception:
                current_c = 25.0
                
            # Insert a 0-second soak so the first ramp has a physical starting point
            fixed.insert(0, Step(kind="soak", target_c=current_c, duration_sec=0, rate_c_per_min=0.0))

            self._schedule = {"steps": steps}
            self.running_profile_name = name
            self.schedule = fixed
            self.history.clear()
            
            self._t_into = max(0.0, float(start_at_elapsed_sec))
            self.start_total = time.time() - max(0.0, float(start_total_elapsed_sec))
            self.start_monotonic = time.monotonic()
            
            self._last_tick = time.monotonic()
            
            self.auto_resumed = False
            self.pid.reset()
            self.active_pid_profile = "INIT"
            
            self.running = True
            self._stop_flag.clear()
            self._init_csv_log()
            
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._loop, daemon=True)
                self._thread.start()

            self._dump_state(force=True)

    def start_quick(self, temp_c: float, duration_sec: int):
        name = f"Quick Soak {int(round(temp_c))}°C"
        
        # Safely get the default heat rate, fallback to 30.0 if not defined
        safe_rate = float(getattr(self.cfg, "DEFAULT_HEAT_RATE_C_PER_MIN", 30.0))
        
        self.start_profile([
            #remove ramp on profile
            #dict(kind="ramp", target_c=float(temp_c), rate_c_per_min=max(1.0, safe_rate / 2.0)),
            dict(kind="soak", target_c=float(temp_c), duration_sec=int(duration_sec))
        ], name=name)

    def stop(self):
        with self._lock:
            self.running = False
            self.start_total = None # Clear total time on stop
            self.relays.safe_down()
            self._stop_flag.set()
            self.running_profile_name = None
            if self._csv_file:
                try: self._csv_file.close()
                except: pass
                self._csv_file = None
            self._dump_state(force=True)

    def _loop(self):
        while not self._stop_flag.is_set():
            now = time.monotonic()
            dt = now - self._last_tick
            self._last_tick = now

            tr = self.tc.read()
            if (not tr.ok) or (tr.temp_c is not None and tr.temp_c > self.cfg.MAX_TEMP_C):
                self.relays.safe_down()
                self.running = False
                self._dump_state(force=True)
                time.sleep(1)
                continue

            sp_candidate = self._compute_sp(self._t_into) if self.running else 25.0
            
            target_profile = "HIGH" if sp_candidate > self.crossover_c else "TEMPER"
            if target_profile != self.active_pid_profile:
                if target_profile == "HIGH":
                    conf = self.cfg.PID_HIGH_CONF
                    self.pid.update_tunings(Kp=conf["Kp"], Ki=conf["Ki"], Kd=conf["Kd"])
                else:
                    conf = self.cfg.PID_TEMPER_CONF
                    self.pid.update_tunings(Kp=conf["Kp"], Ki=conf["Ki"], Kd=conf["Kd"])
                self.active_pid_profile = target_profile

            if self.running:
                planned = self._planned_total_runtime()
                on_track = tr.ok and (abs(tr.temp_c - sp_candidate) <= self.catchup_band_c)
                
                if (not self.wait_for_kiln) or on_track:
                    self._t_into += max(0.0, dt)

                self.current_sp = self._compute_sp(self._t_into)

                if planned and self._t_into >= planned:
                    self.running = False
                    self.relays.safe_down()
                else:
                    u = self.pid.compute(self.current_sp, tr.temp_c, now=now)
                    duty_pct = max(0.0, min(100.0, u))

                    use_dual = True
                    if self.current_sp < self.crossover_c and not self.dual_coil_low:
                        use_dual = False
                    
                    if use_dual: self.relays.set_duty(duty_pct, duty_pct)
                    else: self.relays.set_duty(duty_pct, 0.0)

                    self.relays.tick(now)
                    
                    try:
                        if hasattr(self.tc, "sim_inject_power"):
                            self.tc.sim_inject_power(self.relays.duty1/100.0, self.relays.duty2/100.0)
                    except: pass
                    
                    self._log_csv(self._t_into, tr.temp_c, self.current_sp, duty_pct, self.active_pid_profile)
            else:
                self.relays.safe_down()

            t_kiln = self._t_into if self.running else 0.0
            
            # Use safe calculation for total time
            t_total = 0.0
            if self.running and self.start_total is not None:
                t_total = time.time() - self.start_total

            self.history.append(HistoryPoint(
                ts=time.time(),
                t_kiln=t_kiln,
                t_total=t_total,
                temp=round(float(tr.temp_c), 4) if tr.ok else float("nan"),
                sp=float(self.current_sp) if self.running else float("nan"),
            ))

            self._dump_state()
            time.sleep(self.sample_period)

        self.relays.safe_down()

    def status(self) -> Dict[str, Any]:
        if hasattr(self.tc, "read"):
            tr = self.tc.read()
        else:
            try: c = float(self.tc.read_c())
            except Exception: c = None
            tr = ThermoReading(c=c, fault=None if c is not None else {"message": "no reading"}, ts=int(time.time()))
        
        # Calculate Total Runtime (Wall Clock) safely
        total_runtime = 0
        if self.running and self.start_total is not None:
            total_runtime = int(time.time() - self.start_total)

        # Calculate the total planned duration of the current schedule
        profile_duration = self._planned_total_runtime()

        return dict(
            running=self.running,
            auto_resumed=self.auto_resumed,
            running_profile_name=self.running_profile_name,
            setpoint_c=_finite(round(self.current_sp, 2)) if self.running else None,
            temps={"tc": _finite(round(tr.temp_c, 2)) if tr.ok else None},
            relays={
                "r1": {"duty": int(self.relays.duty1) if math.isfinite(self.relays.duty1) else 0}, 
                "r2": {"duty": int(self.relays.duty2) if math.isfinite(self.relays.duty2) else 0}
            },
            pid_profile=getattr(self, "active_pid_profile", "UNKNOWN"),
            kiln_runtime_sec=int(_finite(self._t_into) or 0),
            total_runtime_sec=total_runtime,
            profile_duration_sec=int(profile_duration), 
            schedule={"steps":[s.__dict__ for s in self.schedule]},
            tc_period_ms=int(self.sample_period*1000),
            waiting_for_kiln = bool(self.wait_for_kiln and self.running and (abs(tr.temp_c - self.current_sp) > self.catchup_band_c)),
            fault=None if tr.ok else "thermocouple_fault"
        )
    
    def log_status(self):
        return [self.status()]