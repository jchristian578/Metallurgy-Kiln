# profileConversion/convert_profiles.py — Helper to convert old kiln profiles to the new version — Metallurgy Kiln Controller V2
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

#!/usr/bin/env python3
import json
import glob
import os
from pathlib import Path

# --- CONFIG ---
INPUT_DIR = "./oldProfiles"   # Create this folder and put old files here
OUTPUT_DIR = "./profiles"      # Where the new V2 files go
DEFAULT_TEMP_UNIT = "C"        # Assumed unit of old profiles
DEFAULT_TIME_UNIT = "min"      # New format time unit preference

def convert_old_to_new(old_json):
    name = old_json.get("name", "Converted Profile")
    points = old_json.get("data", [])
    
    # Sort by time (index 0) to ensure order
    points.sort(key=lambda x: x[0])
    
    steps = []
    
    # Old format: [ [time_sec, temp], [time_sec, temp], ... ]
    # We track 'previous' state to calculate delta/duration
    prev_time = 0
    prev_temp = 25 # Assume ambient start if first point is at t=0
    
    # If the file explicitly defines t=0, set that as our starting prev_temp
    if points and points[0][0] == 0:
        prev_temp = points[0][1]
        # Remove the t=0 point so we don't create a step for it
        points.pop(0)

    for p in points:
        t_sec = p[0]
        target_temp = p[1]
        
        duration_sec = t_sec - prev_time
        delta_temp = target_temp - prev_temp
        
        if duration_sec <= 0: continue # Skip invalid time steps
        
        # Calculate Rate (Deg per minute) needed to hit this point
        rate_per_min = (delta_temp / (duration_sec / 60))
        
        # Determine step type based on temperature change
        if abs(delta_temp) < 1.0:
            # SOAK: Temp didn't change much. 
            # In V2, rate=0 usually implies a hold/soak logic
            steps.append({
                "time": round(duration_sec / 60, 2), # Convert seconds to minutes
                "temp": target_temp,
                "rate": 0
            })
        else:
            # RAMP: Temp changed.
            # We explicitly calculate the rate so the V2 engine follows the same slope.
            steps.append({
                "time": round(duration_sec / 60, 2),
                "temp": target_temp,
                "rate": round(rate_per_min, 2)
            })
            
        prev_time = t_sec
        prev_temp = target_temp

    # Construct New V2 Object
    new_profile = {
        "name": name,
        "meta": {
            "entryTemp": DEFAULT_TEMP_UNIT,
            "entryTime": DEFAULT_TIME_UNIT
        },
        "steps": steps
    }
    return new_profile

def main():
    # Ensure output dir exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory '{INPUT_DIR}' not found.")
        print("Please create the folder 'old_profiles' and place your json files there.")
        return

    files = glob.glob(os.path.join(INPUT_DIR, "*.json"))
    print(f"Found {len(files)} files in {INPUT_DIR}...")
    
    count = 0
    for f_path in files:
        try:
            with open(f_path, 'r') as f:
                data = json.load(f)
            
            # Check validity (Must have 'data' key)
            if "data" not in data or not isinstance(data["data"], list):
                print(f"Skipping {os.path.basename(f_path)} (Does not match old format)")
                continue
                
            new_data = convert_old_to_new(data)
            
            # Save to new location with sanitized filename
            #safe_name = new_data['name'].strip().replace(" ", "_").replace("/", "-")
            safe_name = new_data['name'].strip().replace("/", "-")
            out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
            
            with open(out_path, 'w') as f:
                json.dump(new_data, f, indent=2)
                
            print(f"Converted: {new_data['name']} -> {out_path}")
            count += 1
            
        except Exception as e:
            print(f"Error converting {f_path}: {e}")

    print(f"\nDone. Converted {count} profiles.")

if __name__ == "__main__":
    main()