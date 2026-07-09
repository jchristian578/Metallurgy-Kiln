# server.py — FastAPI app + static UI for — Metallurgy Kiln Controller V2
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
from pathlib import Path
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, Response
from pydantic import BaseModel
from datetime import datetime
import io
import logging
import uvicorn
import config as CFG

# Import Controller but DO NOT instantiate it yet
from kiln.controller import Controller
from kiln.lcd import LCDThread
from kiln.buttons import AuxButtonThread

# --- SETUP CLEAN LOGGING ---
# Match Uvicorn's format: "INFO:     Message"
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s:\t  %(message)s'
)
log = logging.getLogger("SERVER")

# --- GLOBAL VARIABLES ---
CTRL: Optional[Controller] = None
lcd_t: Optional[LCDThread] = None
aux_t: Optional[AuxButtonThread] = None

# --- LIFESPAN EVENT (Startup & Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global CTRL, lcd_t
    
    # [STARTUP LOGIC]
    log.info("Initializing Kiln Controller Hardware...")
    CTRL = Controller(CFG)

    # Start Physical Buttons
    aux_t = AuxButtonThread(CTRL, CFG)
    aux_t.start()
    
    # Start LCD if enabled in config
    if getattr(CFG, 'USE_LCD', False):
        log.info("Starting LCD Thread...")
        lcd_t = LCDThread(CTRL, CFG)
        lcd_t.start()
    
    yield  # Application runs here
    
    # [SHUTDOWN LOGIC]
    log.info("Shutting down hardware...")
    if CTRL:
        CTRL.stop()

# --- APP SETUP ---
app = FastAPI(title=CFG.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir, html=False), name="static")

# --- ROUTES ---

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(static_dir / "index.html")

# Application redirect from old URL
@app.get("/ForgeKiln/index.html", include_in_schema=False)
async def forge_redirect():
    return RedirectResponse(url="/", status_code=301)

class StartProfileBody(BaseModel):
    name: Optional[str] = None
    steps: list[dict]

class StartQuickBody(BaseModel):
    temp_c: float
    duration_sec: int

class StartAuxBody(BaseModel):
    index: int 

@app.post("/api/start/aux")
def api_start_aux(body: StartAuxBody):
    if not CTRL: raise HTTPException(503, "Hardware not ready")
    
    # Check Status
    if CTRL.status().get("running"):
        raise HTTPException(409, "Kiln is already running")

    # Get Profile Name from Config
    idx = body.index
    profile_name = getattr(CFG, f"AUX_BUTTON_{idx}_PROFILE", None)
    
    if not profile_name:
        raise HTTPException(400, f"No profile configured for Button {idx}")

    # Load & Start
    try:
        safe_name = profile_name.replace(".json", "")
        path = CFG.PROFILE_DIR / f"{safe_name}.json"
        
        if not path.exists():
             raise HTTPException(404, f"Profile '{safe_name}' not found")
             
        import json
        with open(path, "r", encoding="utf-8") as f:
            profile_data = json.load(f)
            
        #Grab the compiled machine steps, fallback to raw steps if needed ---
        executable_steps = profile_data.get("compiled_steps")
        if not executable_steps:
            executable_steps = profile_data.get("steps", [])
            
        CTRL.start_profile(executable_steps, name=safe_name)
        return dict(ok=True, name=safe_name)
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/status")
def api_status():
    if not CTRL: return {"running": False, "fault": "Initializing"}
    return CTRL.status()

@app.get("/api/log")
def api_log():
    if not CTRL: return []
    return CTRL.log_status()

@app.get("/api/history")
def api_history():
    if not CTRL: return dict(points=[])
    return dict(points=CTRL.history.snapshot())

@app.get("/api/config")
def api_config():
    return dict(
        app_name=CFG.APP_NAME,
        host=CFG.WEB_HOST,
        port=int(CFG.WEB_PORT),
        poll_interval_sec=float(CFG.POLL_INTERVAL_SEC),
        kwh_cost=float(CFG.KWH_COST),
        kiln_wattage_w=float(CFG.KILN_WATTAGE_W),
        def_heat_rate=float(getattr(CFG, "DEFAULT_HEAT_RATE_C_PER_MIN", 30.0)),
        def_cool_rate=float(getattr(CFG, "DEFAULT_COOL_RATE_C_PER_MIN", 30.0)),
        aux_label_1 = getattr(CFG, "AUX_BUTTON_1_UI_LABEL", ""),
        aux_label_2 = getattr(CFG, "AUX_BUTTON_2_UI_LABEL", ""),
        aux_label_3 = getattr(CFG, "AUX_BUTTON_3_UI_LABEL", ""),
        aux_label_4 = getattr(CFG, "AUX_BUTTON_4_UI_LABEL", "")
    )

@app.post("/api/start/profile")
def api_start_profile(body: StartProfileBody):
    if not CTRL: raise HTTPException(503, "Hardware not ready")
    try:
        CTRL.start_profile(body.steps, body.name)
        return dict(ok=True)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/api/start/quick")
def api_start_quick(body: StartQuickBody):
    if not CTRL: raise HTTPException(503, "Hardware not ready")
    try:
        CTRL.start_quick(body.temp_c, body.duration_sec)
        return dict(ok=True)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/api/logs")
def api_logs_list():
    if not CTRL: raise HTTPException(503, "Hardware not ready")
    
    logs = []
    if CTRL.log_dir.exists():
        # Find all CSV files in the log directory
        for p in CTRL.log_dir.glob("*.csv"):
            logs.append({
                "filename": p.name,
                "timestamp": p.stat().st_mtime # Use OS modified time
            })
            
    # Sort them so the newest runs are at the top of the table
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    return logs

@app.get("/api/logs/download/{filename}")
def api_logs_download(filename: str):
    if not CTRL: raise HTTPException(503, "Hardware not ready")
    
    # Strip any path characters to prevent directory traversal attacks
    safe_name = Path(filename).name 
    file_path = CTRL.log_dir / safe_name
    
    if not file_path.exists() or not safe_name.endswith('.csv'):
        raise HTTPException(404, "Log file not found")
        
    output = io.StringIO()
    import csv
    writer = csv.writer(output)
    
    # Your updated header names
    new_headers = ["Timestamp", "ProfileMinutes", "Temp_C", "SetPoint_C", "Output_pct", "PID_Profile"]
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            # Grab the old headers to figure out column indices
            original_headers = next(reader)
            
            # Write your new clean headers to the output file
            writer.writerow(new_headers)
            
            # Find the dynamic indices so this doesn't break if you re-order columns later
            ts_idx = original_headers.index("timestamp") if "timestamp" in original_headers else -1
            tkiln_idx = original_headers.index("t_kiln") if "t_kiln" in original_headers else -1
            
            for row in reader:
                if not row: continue
                
                # 1. Convert Unix Timestamp to Datetime
                if ts_idx != -1 and len(row) > ts_idx:
                    try:
                        unix_ts = float(row[ts_idx])
                        row[ts_idx] = datetime.fromtimestamp(unix_ts).strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass 
                
                # 2. Convert Seconds to Minutes
                if tkiln_idx != -1 and len(row) > tkiln_idx:
                    try:
                        sec = float(row[tkiln_idx])
                        # Divide by 60 and format nicely to 2 decimal places
                        row[tkiln_idx] = f"{(sec / 60.0):.2f}"
                    except ValueError:
                        pass
                        
                writer.writerow(row)
        except StopIteration:
            pass
            
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={safe_name}"}
    )

@app.get("/api/logs/data/{filename}")
def api_logs_data(filename: str):
    if not CTRL: raise HTTPException(503, "Hardware not ready")
    
    safe_name = Path(filename).name 
    file_path = CTRL.log_dir / safe_name
    
    if not file_path.exists() or not safe_name.endswith('.csv'):
        raise HTTPException(404, "Log file not found")
        
    data = []
    import csv
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Skip empty lines or corrupted null lines gracefully
                if not row or not row.get('t_kiln'): continue
                
                data.append({
                    "t": float(row["t_kiln"]),
                    "temp": float(row["temp_c"]),
                    "sp": float(row["sp_c"])
                })
            except Exception:
                pass
                
    return data

@app.post("/api/stop")
def api_stop():
    if CTRL: CTRL.stop()
    return dict(ok=True)

@app.post("/api/resume/ack")
def api_resume_ack():
    if CTRL: CTRL.ack_auto_resume()
    return dict(ok=True)

PROFILES_DIR = CFG.PROFILE_DIR
PROFILES_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/api/profiles")
def api_profiles_list():
    names = []
    for p in sorted(PROFILES_DIR.glob("*.json")):
        names.append(p.stem)
    return dict(profiles=names, refresh_sec=CFG.PROFILE_REFRESH_SEC)

@app.get("/api/profiles/{name}")
def api_profiles_get(name: str):
    path = PROFILES_DIR / f"{name}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            import json
            return json.load(f)
    raise HTTPException(404, "Profile not found")

@app.post("/api/profiles")
def api_profiles_save(profile: Dict[str, Any]):
    import json
    name = (profile.get("name") or "Unnamed").strip().replace("/", "_")
    path = PROFILES_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    return dict(ok=True, name=name)

@app.delete("/api/profiles/{name}")
def api_profiles_del(name: str):
    path = PROFILES_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
    return dict(ok=True)

if __name__ == "__main__":
    # Disable Uvicorn's standard access log if you want it super clean
    # log_config=None uses basicConfig defined above
    uvicorn.run("server:app", host=CFG.WEB_HOST, port=int(CFG.WEB_PORT), reload=False)