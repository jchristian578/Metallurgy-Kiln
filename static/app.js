// app.js — Metallurgy Kiln Controller V2

/*
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
*/

function Godzilla() {
  // Header text
  const header = `
                                                                                                    
 ░░░▓█████▒░░░░░░▒█████▒░░░░░███████▓░░░░▒████████░░░▒███▒░░░▓███░░░░░░░░▓██▓░░░░░░░░░░▒███▒░░░░░░░ 
 ░░██     ██░░░░██     ██▒░░░█      ██▒░░░▒      ▓░░░▒█ █▒░░░█  █░░░░░░░░█  █░░░░░░░░░▒█▒  █▒░░░░░░ 
 ░▒█  ███  ▓░░░░█  ███  █▒░░░█ ████▒ █▒░░▒█████ ▒█░░░▒█ █▒░░░█  █░░░░░░░░█  █░░░░░░░░░▓█   █▓░░░░░░ 
 ░▒█ ███████▒░░▒█ █▓░██ █▓░░░█ ▒▓░▓█ █▒░░░░░██  █▒░░░▒█ █▒░░░█  █░░░░░░░░█  █░░░░░░░░░█  █  █▒░░░░░ 
 ░▒█ ██    █▒░░▒█ █░░▓█ █▓░░░█ ▒▓░▒█ █▓░░░░██  █▓░░░░▒█ █▒░░░█  █░░░░░░░░█  █░░░░░░░░██ ███ ██░░░░░ 
 ░▒█ █████ █▒░░▒█ ██░██ ▓▓░░░█ ▒▓░▓█ █▒░░░██  █▒░░░░░▒█ █▒░░░█  █░░░░░░░░█  █░░░░░░░▒█       █▒░░░░ 
 ░▒█  ███  █▒░░░█  ███  █▒░░░█ ▓███  █▒░░▒█  ████▓▒░░▒█ █▒░░░█  █████▓░░░█  █████▒░░▓░ █████ ░▓░░░░ 
 ░░██     ██░░░░██     ██░░░░█      ██░░░▒▒       ▒░░▒█ █▒░░░█       ▒░░░█       ▒░░▓  █▒░▒█  ▓░░░░ 
 ░░░▒████▓▒░░░░░░▒▓███▓▒░░░░░▒█████▓▒░░░░▒▓██████▓▒░░░▓▓▓▒░░░▒███████▓░░░▒███████▒░░▒▓▓▒░░░▒▓▓▒░░░░ 
`;
  const art = `                                                                  
                                                                  :+%@@#+=:.                        
                                                                 -@@@@@@@@@@:                       
                                                               .:@@@@@@@@@@*                        
                                                             -%@@@@@@@@@@@@=.                       
                                                          .=%@@@@@@@@@@@@@@:                        
                                                         :%@@@@@@@@@@@@@@@-                         
                                                        :%@@@@@@@@@@@@@@@%.                         
                                                     :=*@@@@@@@@@@@@@@@@@#:                         
                                                    .*@@@@@@@@@@@@@@@@@@.        :=:                
                                                   +@@@@@@@@@@@@@@@@@@@@:     -%@%:   :-%@*         
                                                  =@@@@@@@@@@@@@@@@@@@@@@*. =%@@@: .-*@@@@@=        
                                                 :@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@%*%@@@@@@@@.       
                                                .#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:       
                                                =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=         
                                               +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%-            
                                              .%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-.             
                                             .*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*:               
                                            -%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.                
                                          :#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*                 
                                          +%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                 
                                          -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*                  
                                      :*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.                  
                                      .+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.                   
                                   .:-+*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                    
                                :*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                    
                                 :#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*                     
                                 =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#                      
                                .=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                           :=#@%**+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                     
                           =%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                     
                             -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                     
                             %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:                     
                             :#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*                     
                        -*=:.  .%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                    
                   .=****@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-                    
                    .+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                    
                      :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-                   
                        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                   
                         :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-                  
                          .-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.                
                    .+%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:               
                :%*===#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%-              
              :#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*:            
               :%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=.          
                 :*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.         
                    .-%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.*==%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.        
                      :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+    *@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@-        
                    .:=@@@@@@@@#@@@@@@@@@@@@@@@@@@@@=   .#@@@@@@@@@@@@@@@@@@@*%@@@@@@@@@@@@%.       
              .:-=*%@@@@@@@@@@@-@@@@@@@@@@@@@@@@@@@@*    :@@@@@@@@@@@@@@@@@@@=*@@@@@@@@@@@@@=       
             -@@@@@@@@@@@@@@@@@.#@@@@@@@@@@@@@@@@@@@@.    =@%@@@@@@@@@@@@@@@@::@@@@@@@@@@@@@@:      
    .....     :@@@@@@@@@@@@@@@= :@@@@@@@@@*@@@@@@@@@@:     . :@@@@@@@@@@@@@@:  =@@@@@@@@@@@@@#      
    =@@@@@@@@@@@@@@@@@@@@@@@@@: .@@@@@@@@@++@@@@@@@@%:      -%@@@@@@@@@@@@@@.  .@@@@@@@@@@@@@@.     
     -%@@@@@@@@@@@@@@@@@@@@@@@:  @@@@@@@-:..%@@@@@@@@:     :@@@@@@@=..:=@@@@   .@@@@@@@@@@@@@%.     
      .:=@@@@@@@@@@@@@@@@@@@@@:  @@@@@@@.   %@@@@@@@@-     :@@@@@@@.   .@@@@   .@@@@@@@@@@@@@#      
      .:%@@@@@@@@@@@@@@@@@@@@@.  @@@@@@%.   #@@@@@@@@:     :@@@%=@@.   .@@@@    @@@@@@@@@@@@@*      
  .:=#%@@@@@@@@@@@@@@@@@@@@@@@:  @@@@@@%    #@@*@@@@@.     =@@@:.@@.   .@@@@    @@@@@@@@@@@@@+      
+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.  %@@@@@#    *@= =@@@*      =@@% .%@.   .@@@%    @@@@@@@@@@@@@=      
.:#%#+=%@@@@@@@@@@@@@@@@@@@@@#   =@#@@@*    +%. .%@@+      -@@*  %@.   .@@@%    @@@@@@@@@@@@@.      
        :=*@@@@@@@@@@@@@@@@@@=   :@:@@@*    -+.  *@#:      .*%=  %=    .@@@:    *@@@@@@@@@@@%       
       .=*%@@@@@@@@@@@@@@@@+@:   .%:@@@+         +*.          . .*.    .*:*.    :%@@@@@@@@@@@.      
         :=#%@@@@@@@@@@@#%@:#     +:-::.         .                     .: .      *@@#:@@@@@@@:      
              :#@@@@@@@@..: .     .                                              .::: %@@@@@@*      
               :@@@@....                                                              #@@@@@@@:     
      :--=--:.==-::.                                                                    ..:::=#*:   
      :%@@@@@.                                                                                +@@#=:`;

  console.log(header + art);
}

// Call the function to print the art
Godzilla();

const words = ["-", " Metallurgy Kiln Controller ", "-", " By: Jacob Christian ", " Besslen Bladewords ", "-", " https://www.WootzSmithForum.com/ ", " https://www.instagram.com/besslenbladeworks/ ", " https://www.youtube.com/@besslenbladeworks ", " V2 Completed January 3rd, 2026 ", "-"]

function padAndPrint(strings, totalLength, padChar = ' ') {
    if (padChar.length !== 1) {
        throw new Error("padChar must be a single character");
    }

    strings.forEach(str => {
        if (str.length >= totalLength) {
            console.log(str);
            return;
        }

        const paddingNeeded = totalLength - str.length;
        const padStart = Math.floor(paddingNeeded / 2);
        const padEnd = paddingNeeded - padStart;

        const padded =
            padChar.repeat(padStart) +
            str +
            padChar.repeat(padEnd);

        console.log(padded);
    });
}

padAndPrint(words, 67, '-');

const $ = (sel)=>document.querySelector(sel);
const $$ = (sel)=>document.querySelectorAll(sel);

// --- GLOBAL STATE ---
let UNIT_temp_chart = "C";   
let UNIT_time_chart = "min"; 
let UNIT_builder_temp = "C"; 
let UNIT_builder_time = "min";
let xView = "kiln";          

let chart;
let previewChart; 
let chartData=[], chartSP=[], chartPlan=[]; // Added chartPlan
let lastStatus = null;
let builderSpanSec = 0;
let chartPlannedSpanSec = 0;
let plannedRangeC = null;
let builderRangeC = null;
let pollingMs = 1000;
let lastScheduleKey = "";
let currentProfileSelected = "";
let currentBuilderProfile = "";

// --- RATE DEFAULTS ---
let DEF_HEAT_RATE = 30.0; 
let DEF_COOL_RATE = 30.0;

let yBaseLo = null, yBaseHi = null;
let yExpandMinExtra = 0;
let yExpandMaxExtra = 0;
let yAutoExpandEnabled = true;
const Y_EXPAND_MARGIN_FRAC = 0.04;
const Y_EXPAND_MIN_MARGIN   = 5;
const Y_EXPAND_HEADROOM_FRAC = 0.06;
const Y_EXPAND_HEADROOM_MIN  = 8;

let COST_RATE = 0.15;
let KILN_WATTAGE_W = 0;
let pendingAction = null;
let pendingPayload = null;

// --- HELPER FUNCTIONS ---
const toF = c => (c * 9/5) + 32;
const toC = f => (f - 32) * 5/9;
const secTo = (sec, unit) => unit === "hr" ? (sec / 3600) : (sec / 60);

const fmtTime = (s) => {
  const h = Math.floor(s/3600);
  const m = Math.floor((s%3600)/60);
  const ss = Math.floor(s%60);
  const pad = (n)=> String(n).padStart(2,"0");
  return `${pad(h)}:${pad(m)}:${pad(ss)}`;
};

const num = v => {
  if(v === "" || v === null || v === undefined) return null;
  const x = parseFloat(v);
  return Number.isFinite(x) ? x : null;
};

const on = (id, ev, fn) => { 
  const el = document.getElementById(id); 
  if (el) el.addEventListener(ev, (e) => {
      if(e && e.preventDefault && e.type === 'submit') e.preventDefault(); 
      fn(e);
  }); 
  return !!el; 
};
const val = (id) => (document.getElementById(id)?.value ?? "");
const setText = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
const show = (id, on) => { const el = document.getElementById(id); if (el) el.classList.toggle("d-none", !on); };

const fmtTempDisp = (c) => {
  if (c == null || Number.isNaN(c)) return "--.--";
  const val = UNIT_temp_chart === "F" ? toF(c) : c;
  return val.toFixed(2);
};

const setActiveGroup = (ids, activeId) => {
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('active', id === activeId);
  });
};

// =========================================================
// 1. CHART LOGIC (Updated for 3 Datasets)
// =========================================================

function applyChartUnitsToUI(){
  setActiveGroup(['btnTU_C','btnTU_F'], UNIT_temp_chart === 'F' ? 'btnTU_F' : 'btnTU_C');
  setActiveGroup(['btnRunTU_C','btnRunTU_F'], UNIT_temp_chart === 'F' ? 'btnRunTU_F' : 'btnRunTU_C');
  setActiveGroup(['btnTU_min','btnTU_hr'], UNIT_time_chart === 'hr' ? 'btnTU_hr' : 'btnTU_min');
  setActiveGroup(['btnViewKiln','btnViewTotal'], xView === 'total' ? 'btnViewTotal' : 'btnViewKiln');
  setText("unitT", UNIT_temp_chart);
  setText("spUnitT", UNIT_temp_chart);
}

function axisLabel(){
  return `${UNIT_time_chart === "hr" ? "Hours" : "Minutes"} (${xView==="kiln"?"Profile Runtime":"Total Runtime"})`;
}

function xSpanUnits(spanSec){ return secTo(spanSec, UNIT_time_chart); }
function convCtoDisplay(c){ return UNIT_temp_chart==="F" ? toF(c) : c; }
function yValue(tempC){ return convCtoDisplay(tempC); }
function xValue(t_kiln, t_total){
  const sec = (xView==="kiln") ? t_kiln : t_total;
  return secTo(sec, UNIT_time_chart);
}

function updateChartAxes(){
  if (!chart) return;
  chart.options.scales.x.title.text = axisLabel();
  chart.options.scales.y.title.text = `Temperature (°${UNIT_temp_chart})`;
  applyAxisLock(true);
  
  // Update Plan line visibility based on View
  // If Kiln view -> Show Planned. If Total view -> Hide Planned.
  if (chart.data.datasets.length > 2) {
      chart.data.datasets[2].hidden = (xView === 'total');
  }
  
  chart.update();
}
/*
function makeChart(){
  const ctx = $("#chart").getContext("2d");
  chart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [
        {label:"Temp", data: chartData, borderWidth:2, pointRadius:0, tension:0, parsing:false, borderColor: '#fff'},
        {label:"Setpoint", data: chartSP, borderWidth:1, pointRadius:0, borderDash:[6,6], parsing:false, borderColor: 'rgba(255,255,255,0.5)'},
        {label:"Planned", data: chartPlan, borderWidth:2, pointRadius:0, tension:0, parsing:false, borderColor: 'rgba(13, 202, 240, 0.3)', fill: false}
      ]
    },
    options: {
      animation:false, normalized:true, spanGaps:true, responsive:true, maintainAspectRatio:false,
      interaction: { mode: 'nearest', axis: 'x', intersect: false },
      scales:{
        x:{ type:"linear", title:{ display:true, text: axisLabel() } },
        // UPDATED HERE: Added beginAtZero
        y:{ 
            title:{ display:true, text: `Temperature (°${UNIT_temp_chart})` }, 
            grace:'10%',
            beginAtZero: true 
        }
      },
      plugins:{ legend:{ labels:{ color:"#ddd" } }, decimation: { enabled:true, algorithm:"min-max" } }
    }
  });
  applyAxisLock(true);
}
*/

function makeChart(){
  const ctx = $("#chart").getContext("2d");
  chart = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [
        {label:"Temp", data: chartData, borderWidth:2, pointRadius:0, tension:0, parsing:false, borderColor: '#fff'},
        {label:"Setpoint", data: chartSP, borderWidth:1, pointRadius:0, borderDash:[6,6], parsing:false, borderColor: 'rgba(255,255,255,0.5)'},
        {label:"Planned", data: chartPlan, borderWidth:2, pointRadius:0, tension:0, parsing:false, borderColor: 'rgba(13, 202, 240, 0.3)', fill: false}
      ]
    },
    options: {
      animation:false, normalized:true, spanGaps:true, responsive:true, maintainAspectRatio:false,
      interaction: { mode: 'nearest', axis: 'x', intersect: false },
      scales:{
        x:{ 
            type:"linear", 
            title:{ display:true, text: axisLabel() },
            // Format the X-axis labels to 2 decimal places (using Number() to drop trailing zeros on whole numbers)
            ticks: { callback: function(value) { return Number(value.toFixed(2)); } }
        },
        y:{ 
            title:{ display:true, text: `Temperature (°${UNIT_temp_chart})` }, 
            grace:'10%',
            beginAtZero: true 
        }
      },
      plugins:{ 
          legend:{ labels:{ color:"#ddd" } }, 
          decimation: { enabled:true, algorithm:"min-max" },
          // Format the tooltip title to exactly 2 decimal places
          tooltip: {
              callbacks: {
                  title: (tooltipItems) => {
                      return `Time: ${tooltipItems[0].parsed.x.toFixed(2)} ${UNIT_time_chart}`;
                  }
              }
          }
      }
    }
  });
  applyAxisLock(true);
}

// Forces the "Planned" (Ghost) line to redraw using the current Units
function recalcPlanForUnits(){
  // We check if we have a status and a schedule (works for Profiles AND Quick Soaks)
  if (lastStatus && lastStatus.schedule && lastStatus.schedule.steps) {
    updateChartPlanDataset(lastStatus.schedule.steps);
  }
}

/* TODO: Insert default ramps into schedule
// --- CORE LOGIC: CALCULATE PROFILE POINTS (Used by Preview AND Main Graph) ---
function generateProfilePoints(startTempC, steps){
    let pts = [];
    let t_sec = 0; // Everything internally in seconds
    let curC = startTempC;
    
    // Add start
    pts.push({t: 0, c: curC});
    
    // Resolution for curve generation (e.g., every 60 seconds)
    const stepRes = 60; 

    for (const s of steps){
        // Convert Server step to local logic
        const targetC = s.target_c;
        const rateCmin = s.rate_c_per_min; 
        const durationSec = s.duration_sec;
        const kind = s.kind || "soak";

        if (kind === "ramp" && rateCmin > 0) {
            const deltaC = targetC - curC;
            const rampSec = (Math.abs(deltaC) / rateCmin) * 60;
            
            // Interpolate
            const segs = Math.ceil(rampSec / stepRes);
            for(let i=1; i<=segs; i++){
                const frac = i/segs;
                pts.push({
                    t: t_sec + (rampSec * frac),
                    c: curC + (deltaC * frac)
                });
            }
            t_sec += rampSec;
        } else if (kind === "soak" || (kind === "ramp" && rateCmin <= 0)) {
            // Soak
            if (durationSec > 0) {
                // Just add end point for soak is usually fine, but let's add one mid point 
                // to ensure lines draw straight
                pts.push({t: t_sec + durationSec, c: targetC});
                t_sec += durationSec;
            }
        }
        curC = targetC;
    }
    return pts;
}
*/

function generateProfilePoints(startTempC, steps){
    let pts = [];
    let t_sec = 0; // Everything internally in seconds
    let curC = startTempC;
    
    // Add start
    pts.push({t: 0, c: curC});
    
    // Resolution for curve generation
    const stepRes = 60; 

    for (const s of steps){
        const targetC = s.target_c;
        const rateCmin = s.rate_c_per_min; 
        const durationSec = s.duration_sec;
        const kind = s.kind || "soak";

        if (kind === "ramp" && rateCmin > 0) {
            const deltaC = targetC - curC;
            const rampSec = (Math.abs(deltaC) / rateCmin) * 60;
            
            // Interpolate
            const segs = Math.ceil(rampSec / stepRes);
            for(let i=1; i<=segs; i++){
                const frac = i/segs;
                pts.push({
                    t: t_sec + (rampSec * frac),
                    c: curC + (deltaC * frac)
                });
            }
            t_sec += rampSec;
        } else {
            // It is a soak. If the temperature is changing instantly (a Max Snap), 
            // we must push a vertical point on the graph before the duration starts.
            if (Math.abs(targetC - curC) > 0.01) {
                pts.push({t: t_sec, c: targetC});
            }
            
            if (durationSec > 0) {
                pts.push({t: t_sec + durationSec, c: targetC});
                t_sec += durationSec;
            }
        }
        curC = targetC;
    }
    return pts;
}

// Update the 3rd dataset (Planned) on the main chart
function updateChartPlanDataset(serverSteps){
    if (!chart) return;
    
    // Calculate points in (Seconds, C)
    // We assume the run started at ambient ~25C for the plan visualization, 
    // OR we could use the first recorded history point. Let's use 25C default or history[0].
    let startC = 25;
    if (chartData.length > 0) {
        // Convert displayed value back to C to run calc
        const val = chartData[0].y;
        startC = (UNIT_temp_chart === "F") ? toC(val) : val;
    }

    const rawPoints = generateProfilePoints(startC, serverSteps);
    
    // Convert to Chart Display Units (x: min/hr, y: C/F)
    chartPlan.length = 0;
    for(const p of rawPoints){
        chartPlan.push({
            x: xSpanUnits(p.t), // sec -> current time unit
            y: convCtoDisplay(p.c) // C -> current temp unit
        });
    }
    
    chart.update('none');
}

// ... (Rest of Chart Logic like applyAxisLock, autoExpandY...)
function applyAxisLock(resetExpansions=false){
  const spanSec = chartPlannedSpanSec || builderSpanSec || 0;
  if (spanSec > 0){
    chart.options.scales.x.min = 0;
    chart.options.scales.x.max = xSpanUnits(spanSec);
  } else {
    chart.options.scales.x.min = undefined;
    chart.options.scales.x.max = undefined;
  }
  const rng = plannedRangeC || builderRangeC;
  if (resetExpansions){ yExpandMinExtra = 0; yExpandMaxExtra = 0; }
  if (rng){
    const padC = Math.max(10, 0.08 * (rng.maxC - rng.minC || 40));
    yBaseLo = convCtoDisplay(rng.minC - padC);
    yBaseHi = convCtoDisplay(rng.maxC + padC);
    chart.options.scales.y.min = yBaseLo - yExpandMinExtra;
    chart.options.scales.y.max = yBaseHi + yExpandMaxExtra;
  } else {
    yBaseLo = yBaseHi = null;
    chart.options.scales.y.min = undefined;
    chart.options.scales.y.max = undefined;
  }
}

function autoExpandYForValue(yDisp){
  if (!yAutoExpandEnabled) return;
  if (yBaseLo == null || yBaseHi == null) return;
  const curMin = (yBaseLo - yExpandMinExtra);
  const curMax = (yBaseHi + yExpandMaxExtra);
  const span = Math.max(1, curMax - curMin);
  const margin = Math.max(Y_EXPAND_MIN_MARGIN, Y_EXPAND_MARGIN_FRAC * span);
  if (yDisp > (curMax - margin)){
    const headroom = Math.max(Y_EXPAND_HEADROOM_MIN, Y_EXPAND_HEADROOM_FRAC * span);
    yExpandMaxExtra = Math.max(yExpandMaxExtra, (yDisp + headroom) - yBaseHi);
    chart.options.scales.y.max = yBaseHi + yExpandMaxExtra;
    chart.update('none');
  } else if (yDisp < (curMin + margin)){
    const headroom = Math.max(Y_EXPAND_HEADROOM_MIN, Y_EXPAND_HEADROOM_FRAC * span);
    yExpandMinExtra = Math.max(yExpandMinExtra, (yBaseLo) - (yDisp - headroom));
    chart.options.scales.y.min = yBaseLo - yExpandMinExtra;
    chart.update('none');
  }
}

function clearChart(){
  chartData.length = 0;
  chartSP.length = 0;
  chartPlan.length = 0;
  chart.update();
}

async function fetchStatus(){
  const res = await fetch("/api/status"); 
  const j = await res.json();
  console.log(j);

  pollingMs = Math.max(200, Math.min(5000, j.tc_period_ms || pollingMs));

  const runningName = j.running_profile_name || "";
  if (runningName){
    currentProfileSelected = runningName;
    const sel = document.getElementById("profSelect");
    if (sel && sel.value !== runningName) sel.value = runningName;
    if (currentBuilderProfile !== runningName && !document.getElementById("profName").value){
      await loadProfileByName(runningName);
    }
    lastStatus = j;
  }

  const scheduleKey = JSON.stringify(j.schedule||{});
  if (scheduleKey !== lastScheduleKey){
    lastScheduleKey = scheduleKey;
    chartPlannedSpanSec = plannedSpanFrom(j.schedule, j?.temps?.tc);
    plannedRangeC = tempRangeFromScheduleIncludePV(j.schedule, j?.temps?.tc);
    clearChart(); 
    if(j.schedule && j.schedule.steps && j.schedule.steps.length > 0){
        updateChartPlanDataset(j.schedule.steps);
    }
    applyAxisLock(true);
  }

  setText("tcVal", fmtTempDisp(j?.temps?.tc));
  setText("spVal", j?.setpoint_c != null ? fmtTempDisp(j.setpoint_c) : "--.--");
  setText("runTime", fmtTime(j?.kiln_runtime_sec ?? 0));
  setText("totalTimeTile", fmtTime(j?.total_runtime_sec ?? 0));

  // --- Relay Color Logic ---
  const d1 = j?.relays?.r1?.duty ?? 0;
  const d2 = j?.relays?.r2?.duty ?? 0;
  const curT = j?.temps?.tc ?? 0;
  const setP = j?.setpoint_c ?? 0;

  const getRelayClass = (duty) => {
      if (duty <= 0) return ""; 
      if (setP < curT) return "text-info"; 
      return "text-danger"; 
  };

  const elD1 = document.getElementById("duty1");
  if (elD1) {
      elD1.textContent = d1 + "%";
      elD1.className = "tile-value " + getRelayClass(d1);
  }

  const elD2 = document.getElementById("duty2");
  if (elD2) {
      elD2.textContent = d2 + "%";
      elD2.className = "tile-value " + getRelayClass(d2);
  }
  // ------------------------------

  if (j.temps && j.temps.tc != null) autoExpandYForValue(yValue(j.temps.tc));
  if (j.setpoint_c != null) autoExpandYForValue(yValue(j.setpoint_c));

  const isRunning = !!(j && j.running);
  const profSel = document.getElementById("profSelect");
  if (profSel) profSel.disabled = isRunning;
  const badge = document.getElementById("runBadge");
  const dot = badge ? badge.querySelector(".run-dot") : null;
  const lbl = document.getElementById("runText");
  if (badge && dot && lbl){
    badge.classList.toggle("badge-run", isRunning);
    badge.classList.toggle("badge-idle", !isRunning);
    dot.classList.toggle("hidden", !isRunning);
    lbl.textContent = isRunning ? "Running" : "Idle";
  }
  // AUX BUTTONS DISABLED WHILE A PROFILE IS RUNNING
  document.querySelectorAll(".aux-btn").forEach(btn => {
      btn.disabled = isRunning;
      // Optional: Visual feedback
      btn.classList.toggle("opacity-50", isRunning);
  });

  show("btnStop",  isRunning);
  show("btnStart", !isRunning);
  show("btnQuick", !isRunning);

  // --- NEW: Update Active Profile Name Label ---
  const profileRow = document.getElementById("activeProfileRow");
  const profileLabel = document.getElementById("activeProfileLabel");

  if (profileRow && profileLabel) {
      if (isRunning) {
          profileRow.classList.remove("d-none");
          profileLabel.textContent = j.running_profile_name || "Manual";
      } else {
          profileRow.classList.add("d-none");
          profileLabel.textContent = "";
      }
  }
  // ---------------------------------------------

  if (j.auto_resumed) {
      setText("resumedProfileName", j.running_profile_name || "Unknown");
      document.getElementById("resumeModal").classList.add("show");
      document.body.classList.add("modal-open");
  } else {
      const el = document.getElementById("resumeModal");
      if (el.classList.contains("show")) {
          el.classList.remove("show");
          if(!document.querySelector(".modal-backdrop.show")) document.body.classList.remove("modal-open");
      }
  }
}
/*
async function fetchHistory(){
  const res = await fetch("/api/history"); 
  const j = await res.json();
  const pts = (j.points||[]).sort((a,b)=>a.ts-b.ts);
  chartData.length = 0;
  chartSP.length = 0;
  
  const xmax = chart?.options?.scales?.x?.max ?? null;
  
  // Logic: 
  // If Kiln View -> Use p.t_kiln. Hide Planned if Total View.
  // If Total View -> Use p.t_total.
  
  if (chart && chart.data.datasets.length > 2) {
      chart.data.datasets[2].hidden = (xView === 'total');
  }

  for (const p of pts){
    const xv = xValue(p.t_kiln, p.t_total);
    if (xmax != null && xv > xmax) continue; 
    
    if (!Number.isNaN(p.temp)) chartData.push({x:xv, y:yValue(p.temp)});
    if (!Number.isNaN(p.sp)) chartSP.push({x:xv, y:yValue(p.sp)});
  }
  chart.update('none');
}
*/

async function fetchHistory(){
  const res = await fetch("/api/history"); 
  const j = await res.json();
  const pts = (j.points||[]).sort((a,b)=>a.ts-b.ts);
  
  chartData.length = 0;
  chartSP.length = 0;
  
  const xmax = chart?.options?.scales?.x?.max ?? null;
  
  if (chart && chart.data.datasets.length > 2) {
      chart.data.datasets[2].hidden = (xView === 'total');
  }

  // 60-Second Bucketing & Averaging ---
  const buckets = {};

  for (const p of pts){
    // Determine the raw time in seconds based on current view mode
    const t_sec = (xView === "kiln") ? p.t_kiln : p.t_total;
    
    // Quick check to see if this point is past our locked X-axis max
    const xv_check = secTo(t_sec, UNIT_time_chart);
    if (xmax != null && xv_check > xmax) continue; 

    // Group into 60-second chunks (0-59, 60-119, etc.)
    const minuteKey = Math.floor(t_sec / 60);

    if (!buckets[minuteKey]) {
        buckets[minuteKey] = {
            sumTemp: 0, countTemp: 0,
            sumSP: 0, countSP: 0,
            sumSec: 0, countSec: 0
        };
    }

    const b = buckets[minuteKey];

    // Track time so we can plot the exact center-of-mass for the bucket
    b.sumSec += t_sec;
    b.countSec++;

    if (p.temp != null && !Number.isNaN(p.temp)) {
        b.sumTemp += p.temp;
        b.countTemp++;
    }
    
    if (p.sp != null && !Number.isNaN(p.sp)) {
        b.sumSP += p.sp;
        b.countSP++;
    }
  }

  // Calculate averages and push them to the chart datasets
  const sortedKeys = Object.keys(buckets).map(Number).sort((a,b) => a - b);

  for (const key of sortedKeys) {
      const b = buckets[key];
      if (b.countSec === 0) continue;

      const avgSec = b.sumSec / b.countSec;
      const avgX = secTo(avgSec, UNIT_time_chart); // Convert avg seconds to UI unit (min/hr)

      if (b.countTemp > 0) {
          const avgTemp = b.sumTemp / b.countTemp;
          chartData.push({ x: avgX, y: yValue(avgTemp) });
      }
      if (b.countSP > 0) {
          const avgSP = b.sumSP / b.countSP;
          chartSP.push({ x: avgX, y: yValue(avgSP) });
      }
  }

  chart.update('none');
}

async function tick(){
  try { await fetchStatus(); await fetchHistory(); } 
  catch (e) { console.error(e); } 
  finally { setTimeout(tick, pollingMs); }
}

// =========================================================
// PREVIEW MODAL LOGIC (Reuses new math but handles tooltip)
// =========================================================

function renderPreviewChart(){
    // We convert builder rows to "Server-Like" steps to reuse logic
    const serverSteps = builderToServerSteps(); 
    const startC = getStartTemp(); // Get current temp from UI or default
    
    const rawPoints = generateProfilePoints(startC, serverSteps);
    
    // Map to Preview Data
    let dataPoints = [];
    for(const p of rawPoints){
        dataPoints.push({
            x: (UNIT_builder_time === 'hr') ? p.t/3600 : p.t/60,
            y: (UNIT_builder_temp === 'F') ? toF(p.c) : p.c
        });
    }
    
    if (!previewChart) {
        const ctx = document.getElementById("previewChart").getContext("2d");
        previewChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Calculated Profile',
                    data: dataPoints,
                    borderColor: '#0dcaf0', 
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'nearest', axis: 'x', intersect: false },
                scales: {
                    x: { 
                        type: 'linear', 
                        title: { display: true, text: `Time (${UNIT_builder_time})` },
                        // NEW: Format the preview X-axis labels
                        ticks: { callback: function(value) { return Number(value.toFixed(2)); } }
                    },
                    y: { title: { display: true, text: `Temp (°${UNIT_builder_temp})` } }
                },
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        displayColors: false,
                        callbacks: {
                            title: (tooltipItems) => {
                                const x = tooltipItems[0].parsed.x;
                                // NEW: Change .toFixed(1) to .toFixed(2)
                                return `Time: ${x.toFixed(2)} ${UNIT_builder_time}`;
                            },
                            label: (tooltipItem) => {
                                const y = tooltipItem.parsed.y;
                                return `Temperature: ${y.toFixed(1)}°${UNIT_builder_temp}`;
                            }
                        }
                    }
                }
            }
        });
    } else {
        previewChart.data.datasets[0].data = dataPoints;
        previewChart.options.scales.x.title.text = `Time (${UNIT_builder_time})`;
        previewChart.options.scales.y.title.text = `Temp (°${UNIT_builder_temp})`;
        
        // NEW: Change .toFixed(1) to .toFixed(2)
        previewChart.options.plugins.tooltip.callbacks.title = (items) => `Time: ${items[0].parsed.x.toFixed(2)} ${UNIT_builder_time}`;
        
        previewChart.options.plugins.tooltip.callbacks.label = (item) => `Temperature: ${item.parsed.y.toFixed(1)}°${UNIT_builder_temp}`;
        previewChart.update();
    }
    
    document.getElementById("previewModal").classList.add("show");
    document.body.classList.add("modal-open");
}

// ... (Rest of Builder Logic: convert, addStepRow, etc. is SAME as before) ...

function applyBuilderUnitsToUI(){
  setActiveGroup(['btnC','btnF'], UNIT_builder_temp === 'F' ? 'btnF' : 'btnC');
  setActiveGroup(['btnMin','btnHr'], UNIT_builder_time === 'hr' ? 'btnHr' : 'btnMin');
  setText("hUnitTime", `(${UNIT_builder_time})`);
  setText("hUnitTemp", `(°${UNIT_builder_temp})`);
  setText("hUnitRate", `(°${UNIT_builder_temp}/${UNIT_builder_time})`);

  $$('#steps .step-row').forEach(r => {
    r.querySelector('.time')?.setAttribute('placeholder', `time (${UNIT_builder_time})`);
    r.querySelector('.temp')?.setAttribute('placeholder', `temp (°${UNIT_builder_temp})`);
  });
}

function convertBuilderTempUnits(toUnit){
  const from = UNIT_builder_temp;
  if (from === toUnit) return;

  $$("#steps .step-row").forEach(r => {
    const tInp = r.querySelector(".temp");
    const rInp = r.querySelector(".rate-val");
    
    const tVal = num(tInp.value);
    if (tVal != null) {
      tInp.value = (from === "C" && toUnit === "F") ? toF(tVal).toFixed(1)
                 : (from === "F" && toUnit === "C") ? toC(tVal).toFixed(1)
                 : tInp.value;
    }
    
    const rVal = num(rInp.value);
    if (rVal != null) {
        if (from === "C" && toUnit === "F") rInp.value = (rVal * 1.8).toFixed(1);
        if (from === "F" && toUnit === "C") rInp.value = (rVal / 1.8).toFixed(1);
    }
  });

  UNIT_builder_temp = toUnit;
  applyBuilderUnitsToUI();
  updateQuickModalUnitLabels();
  updateRowCalculations();
}

function convertBuilderTimeUnits(toUnit){
  const from = UNIT_builder_time;
  if (from === toUnit) return;

  $$("#steps .step-row").forEach(r => {
    const timeInp = r.querySelector(".time");
    const rInp = r.querySelector(".rate-val"); 
    
    const tVal = num(timeInp.value);
    if (tVal != null) {
      timeInp.value = (from === "min" && toUnit === "hr") ? (tVal / 60).toFixed(2)
                    : (from === "hr" && toUnit === "min") ? (tVal * 60).toFixed(0)
                    : timeInp.value;
    }

    const rVal = num(rInp.value);
    if (rVal != null) {
        if (from === "min" && toUnit === "hr") rInp.value = (rVal * 60).toFixed(1);
        if (from === "hr" && toUnit === "min") rInp.value = (rVal / 60).toFixed(1);
    }
  });

  UNIT_builder_time = toUnit;
  applyBuilderUnitsToUI();
  updateQuickModalUnitLabels();
  updateRowCalculations();
}

function setBuilderMeta(meta){
  if (meta && typeof meta === 'object'){
    if (meta.entryTemp) UNIT_builder_temp = (meta.entryTemp.toUpperCase() === 'F') ? 'F' : 'C';
    if (meta.entryTime) UNIT_builder_time = (meta.entryTime.toLowerCase() === 'hr') ? 'hr' : 'min';
  }
  applyBuilderUnitsToUI();
  updateRowCalculations();
}

function getStartTemp(){
    const txt = document.getElementById("tcVal")?.textContent;
    const flt = parseFloat(txt);
    if(Number.isFinite(flt)) {
        return (UNIT_temp_chart === "F" && UNIT_builder_temp === "C") ? toC(flt) : 
               (UNIT_temp_chart === "C" && UNIT_builder_temp === "F") ? toF(flt) : flt;
    }
    return UNIT_builder_temp === "F" ? 77 : 25;
}

function updateRowCalculations(){
    const rows = $$("#steps .step-row");
    let prevT = getStartTemp();

    rows.forEach(r => {
        const tempInp = r.querySelector(".temp");
        const btnMax  = r.querySelector(".btn-max");
        const btnSet  = r.querySelector(".btn-set");
        const rateInp = r.querySelector(".rate-val");
        const inputGroup = r.querySelector(".input-group"); // Get the container

        const targetT = num(tempInp.value) ?? prevT;
        const deltaT = targetT - prevT; 
        
        const isHeat = deltaT >= 0;
        const activeColor = isHeat ? "btn-danger" : "btn-info";
        
        btnMax.className = "btn btn-outline-secondary btn-max px-2";
        btnSet.className = "btn btn-outline-secondary btn-set px-2";
        
        const isUserSet = !rateInp.classList.contains("d-none");
        
        if (isUserSet) {
            btnSet.classList.remove("btn-outline-secondary");
            btnSet.classList.add(activeColor);
            
            // Show input -> remove centering so it fills space
            inputGroup.classList.remove("justify-content-center"); 
            
            rateInp.classList.remove("text-danger", "text-info");
            rateInp.classList.add(isHeat ? "text-danger" : "text-info");
        } else {
            btnMax.classList.remove("btn-outline-secondary");
            btnMax.classList.add(activeColor);
            
            // Hide input -> Center the buttons
            inputGroup.classList.add("justify-content-center");
        }

        prevT = targetT; 
    });
    
    computeTotal();
}

// UPDATED: addStepRow with Centering Logic for Rate Buttons
function addStepRow(step, insertBeforeNode = null){
  const wrap = document.getElementById("steps");
  if (!wrap) return;
  const row = document.createElement("div");
  row.className = "step-row row g-1 align-items-center mb-1"; 
  
  const isUserSet = (step?.rate && step.rate > 0) ? true : false;
  const rateVal = isUserSet ? step.rate : "";
  const displayClass = isUserSet ? "" : "d-none";
  
  // Initial state for centering
  const justifyClass = isUserSet ? "" : "justify-content-center";

  // Responsive Grid: 
  // Desktop: 3 | 3 | 4 | 2  (Gives Rate more room)
  // Mobile:  3 | 3 | 4 | 2  (Same ratio works well for this compact layout)
  row.innerHTML = `
    <div class="col-3 col-md-3">
      <input class="form-control form-control-sm time" type="number" step="1" placeholder="soak" value="${step?.time ?? 30}">
    </div>
    <div class="col-3 col-md-3">
      <input class="form-control form-control-sm temp" type="number" step="1" placeholder="temp" value="${step?.temp ?? 25}">
    </div>
    <div class="col-4 col-md-4">
      <div class="input-group input-group-sm w-100 ${justifyClass}">
        <button type="button" class="btn btn-outline-secondary btn-max px-2" title="Max Rate">M</button>
        <button type="button" class="btn btn-outline-secondary btn-set px-2" title="Set Rate">S</button>
        <input class="form-control rate-val px-1 ${displayClass}" type="number" placeholder="rate" value="${rateVal}">
      </div>
    </div>
    <div class="col-2 col-md-2">
      <div class="row g-0">
        <div class="col-6"><button class="btn btn-sm btn-outline-light w-100 p-0 up" style="height:24px; font-size:0.75rem;">▲</button></div>
        <div class="col-6"><button class="btn btn-sm btn-outline-light w-100 p-0 ins" style="height:24px; font-size:0.9rem;">＋</button></div>
        <div class="col-6"><button class="btn btn-sm btn-outline-light w-100 p-0 down" style="height:24px; font-size:0.75rem;">▼</button></div>
        <div class="col-6"><button class="btn btn-sm btn-outline-danger w-100 p-0 del" style="height:24px; font-size:0.8rem;">✕</button></div>
      </div>
    </div>`;

  if (insertBeforeNode && insertBeforeNode.parentNode === wrap) {
      wrap.insertBefore(row, insertBeforeNode);
  } else {
      wrap.appendChild(row);
  }

  const timeInp = row.querySelector(".time");
  const tempInp = row.querySelector(".temp");
  const rateInp = row.querySelector(".rate-val");
  const btnMax  = row.querySelector(".btn-max");
  const btnSet  = row.querySelector(".btn-set");
  const inputGroup = row.querySelector(".input-group");

  btnMax.onclick = () => {
      rateInp.classList.add("d-none");
      inputGroup.classList.add("justify-content-center"); 
      rateInp.value = ""; 
      updateRowCalculations();
  };

  btnSet.onclick = () => {
      rateInp.classList.remove("d-none");
      inputGroup.classList.remove("justify-content-center"); 
      if(!rateInp.value) rateInp.value = 100; 
      rateInp.focus();
      updateRowCalculations();
  };

  timeInp.oninput = updateRowCalculations;
  tempInp.oninput = updateRowCalculations;
  rateInp.oninput = updateRowCalculations;

  row.querySelector(".up").onclick = (e) => {
      e.preventDefault();
      if (row.previousElementSibling) {
          wrap.insertBefore(row, row.previousElementSibling);
          updateRowCalculations();
      }
  };
  
  row.querySelector(".down").onclick = (e) => {
      e.preventDefault();
      if (row.nextElementSibling) {
          wrap.insertBefore(row, row.nextElementSibling.nextElementSibling);
          updateRowCalculations();
      }
  };

  row.querySelector(".ins").onclick = (e) => {
      e.preventDefault();
      addStepRow({ time: 30, temp: parseFloat(tempInp.value)||25, rate:0 }, row);
      updateRowCalculations();
  };

  row.querySelector(".del").onclick = (e) => {
      e.preventDefault();
      row.remove();
      updateRowCalculations();
  };
  
  updateRowCalculations();
}

function readSteps(){
  const wrap = document.getElementById("steps");
  if (!wrap) return [];
  const rows = wrap.querySelectorAll(".step-row");
  const steps = [];
  rows.forEach(r=>{
    const time = parseFloat(r.querySelector(".time").value||"0")||0;
    const temp = parseFloat(r.querySelector(".temp").value||"0")||0;
    const isUserSet = !r.querySelector(".rate-val").classList.contains("d-none");
    const rateVal = isUserSet ? parseFloat(r.querySelector(".rate-val").value) : 0;
    steps.push({ time, temp, rate: rateVal });
  });
  return steps;
}

function computeTotal(){
  const steps = readSteps();
  let totalSec = 0;
  let prevT = getStartTemp();

  for (const s of steps){
      const targetT = s.temp; 
      let effectiveRate = s.rate;
      
      if (!effectiveRate || effectiveRate <= 0) {
          if (targetT >= prevT) effectiveRate = DEF_HEAT_RATE;
          else effectiveRate = DEF_COOL_RATE;
          
          if (UNIT_builder_temp === "F") effectiveRate = effectiveRate * 1.8;
          if (UNIT_builder_time === "hr") effectiveRate = effectiveRate * 60;
      }
      
      const delta = Math.abs(targetT - prevT);
      const rampTime = (effectiveRate > 0) ? (delta / effectiveRate) : 0;
      const soakTime = s.time; 
      
      const unitMult = (UNIT_builder_time==="hr" ? 3600 : 60);
      totalSec += (rampTime + soakTime) * unitMult;
      
      prevT = targetT;
  }
  
  let minC = +Infinity, maxC = -Infinity;
  for (const s of steps){
      const tempC = (UNIT_builder_temp==="F") ? toC(s.temp) : s.temp;
      if (!isNaN(tempC)){ minC = Math.min(minC,tempC); maxC = Math.max(maxC,tempC); }
  }

  builderSpanSec = totalSec;
  if (isFinite(minC) && isFinite(maxC)){
    if (maxC - minC < 20){ minC -= 10; maxC += 10; }
    builderRangeC = {minC, maxC};
  } else {
    builderRangeC = null;
  }
  
  const tEl = document.getElementById("totalTime");
  if (tEl) {
      const disp = (UNIT_builder_time==="hr") ? (totalSec/3600).toFixed(2)+" hr" : (totalSec/60).toFixed(1)+" min";
      tEl.textContent = disp;
  }
  applyAxisLock(true);
}

function builderToServerSteps(){
  const steps = readSteps();
  const out = [];
  let prevT = getStartTemp();

  for (const s of steps){
    const targetC = UNIT_builder_temp==="F" ? toC(s.temp) : s.temp;
    
    let rateCmin = 0;
    if (s.rate > 0) {
        rateCmin = s.rate;
        if (UNIT_builder_temp === "F") rateCmin /= 1.8;
        if (UNIT_builder_time === "hr") rateCmin /= 60;
    } 
    
    /*else {
        if (s.temp >= prevT) rateCmin = DEF_HEAT_RATE;
        else rateCmin = DEF_COOL_RATE;
    }*/
    
    if (Math.abs(s.temp - prevT) > 0.1) {
        out.push({ kind:"ramp", target_c: targetC, rate_c_per_min: rateCmin, duration_sec:0 });
    }
    
    if (s.time > 0) {
        const dur = s.time * (UNIT_builder_time==="hr" ? 3600 : 60);
        out.push({ kind:"soak", target_c: targetC, duration_sec: dur, rate_c_per_min: 0 });
    }
    prevT = s.temp;
  }
  return out;
}

function plannedSpanFrom(sched, currentTempC){
  if (!sched || !sched.steps) return 0;
  let lastT = (typeof currentTempC === 'number' && isFinite(currentTempC))
    ? currentTempC
    : (sched.steps.length ? sched.steps[0].target_c : 25);

  let sum = 0;
  for (const s of sched.steps){
    if (s.kind === "ramp" && s.rate_c_per_min){
      const dT = Math.abs(s.target_c - lastT);
      const dt = dT / Math.max(1e-6, s.rate_c_per_min) * 60;
      sum += dt;
      lastT = s.target_c;
    } else if (s.kind === "soak"){
      sum += (s.duration_sec || 0);
      lastT = s.target_c;
    } else {
      lastT = s.target_c;
    }
  }
  return sum;
}

function tempRangeFromScheduleIncludePV(sched, currentTempC){
  if (!sched || !sched.steps || !sched.steps.length) return null;
  let min = +Infinity, max = -Infinity;
  for (const s of sched.steps){
      if (typeof s.target_c === "number"){
          min = Math.min(min, s.target_c);
          max = Math.max(max, s.target_c);
      }
  }
  if (typeof currentTempC === 'number' && isFinite(currentTempC)){
      min = Math.min(min, currentTempC);
      max = Math.max(max, currentTempC);
  }
  if (!isFinite(min) || !isFinite(max)) return null;
  if (max - min < 20) { min -= 10; max += 10; }
  return {minC:min, maxC:max};
}

function bindToggles(){
  // Helper to run the update sequence in the correct order
  const refreshChart = async () => {
    applyChartUnitsToUI();    // 1. Update buttons/labels
    await fetchHistory();     // 2. Fetch/Convert historical data points
    recalcPlanForUnits();     // 3. Recalculate Planned Line (using new units)
    updateChartAxes();        // 4. Update Axis titles and scaling
  };

  on("btnViewKiln","click", ()=>{ xView="kiln"; refreshChart(); });
  on("btnViewTotal","click",()=>{ xView="total"; refreshChart(); });

  on("btnTU_C","click", ()=>{ UNIT_temp_chart="C"; refreshChart(); });
  on("btnTU_F","click", ()=>{ UNIT_temp_chart="F"; refreshChart(); });

  on("btnTU_min","click", ()=>{ UNIT_time_chart="min"; refreshChart(); });
  on("btnTU_hr","click",  ()=>{ UNIT_time_chart="hr";  refreshChart(); });

  on("btnRunTU_C","click", ()=>{ UNIT_temp_chart="C"; refreshChart(); });
  on("btnRunTU_F","click", ()=>{ UNIT_temp_chart="F"; refreshChart(); });

  // Builder toggles stay the same
  on("btnC", "click", ()=>{ convertBuilderTempUnits("C"); });
  on("btnF", "click", ()=>{ convertBuilderTempUnits("F"); });
  on("btnMin", "click", ()=>{ convertBuilderTimeUnits("min"); });
  on("btnHr", "click", ()=>{ convertBuilderTimeUnits("hr"); });
}

function updateQuickModalUnitLabels(){
  const tu = document.getElementById("qmTempUnit");
  const du = document.getElementById("qmTimeUnit");
  if (tu) tu.textContent = "°" + (UNIT_builder_temp || "C");
  if (du) du.textContent = (UNIT_builder_time || "min");
}

function showQuickModal(){
  updateQuickModalUnitLabels();
  document.getElementById("quickModal")?.classList.add("show");
  document.body.classList.add("modal-open");
}

function hideQuickModal(){
  document.getElementById("quickModal")?.classList.remove("show");
  document.body.classList.remove("modal-open");
}

function bindQuickModalButtons(){
  on("qmCancel","click", hideQuickModal);
  on("qmOK","click", ()=>{
    const tInp = document.getElementById("qmTemp");
    const dInp = document.getElementById("qmDur");
    let t = parseFloat(tInp?.value ?? "");
    let d = parseFloat(dInp?.value ?? "");
    
    if (!Number.isFinite(t) || !Number.isFinite(d) || t <= 0 || d <= 0){
      alert("Invalid input."); return;
    }
    const temp_c = (UNIT_builder_temp === "F") ? toC(t) : t;
    const duration_sec = (UNIT_builder_time === "hr") ? d * 3600 : d * 60;
    const name = `Quick Soak ${Math.round(temp_c)}°C`;
    const estCost = kwhCostForSeconds(duration_sec);
    
    pendingAction = 'start-quick';
    pendingPayload = { temp_c, duration_sec, name };
    
    hideQuickModal();
    showRunModal({
      title: "Start Quick Soak?", name, runtimeSec: duration_sec, cost: estCost,
      runLenLabel: "Planned run length:", costLabel: "Estimated cost:"
    });
  });
}

function fmtCurrency(n){
  try { return new Intl.NumberFormat(undefined, {style:'currency', currency:'USD', maximumFractionDigits:2}).format(n); }
  catch { return "$" + (Number(n)||0).toFixed(2); }
}

function kwhCostForSeconds(sec){
  const hours = (Number(sec)||0)/3600;
  const kwh = (Number(KILN_WATTAGE_W)||0)/1000 * hours;
  return kwh * (Number(COST_RATE)||0);
}

function showRunModal(opts){
  setText("rmTitle", opts.title || "Confirm");
  setText("rmName", opts.name || "Unnamed");
  setText("rmRuntime", fmtTime(opts.runtimeSec || 0));
  setText("rmEstCost", fmtCurrency(opts.cost || 0));
  setText("rmRunLenLabel", opts.runLenLabel || "Run length:");
  setText("rmCostLabel", opts.costLabel || "Est Cost:");
  document.getElementById("runModal").classList.add("show");
  document.body.classList.add("modal-open");
}
function hideRunModal(){
  document.getElementById("runModal").classList.remove("show");
  document.body.classList.remove("modal-open");
}

async function runPendingAction(){
  if (!pendingAction) return;
  const act = pendingAction;
  const data = pendingPayload || {};
  pendingAction = null; pendingPayload = null;

  try{
    if (act === 'start-profile'){
      await fetch("/api/start/profile", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ name: data.name, steps: data.steps })
      });
    } else if (act === 'start-quick'){
      await fetch("/api/start/quick", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ temp_c: data.temp_c, duration_sec: data.duration_sec })
      });
    } else if (act === 'stop'){
      await fetch("/api/stop", { method:"POST" });
    }
  } catch(e){ console.error(e); }
}

function bindButtons(){
  // --- NEW PROFILE BUTTON ---
  on("btnNew","click", () => {
      if(confirm("Start a new profile? Unsaved changes will be lost.")) {
          document.getElementById("steps").innerHTML = "";
          document.getElementById("profName").value = "";
          currentProfileSelected = "";
          currentBuilderProfile = "";
          // Add one default starting step
          addStepRow({ time:30, temp:25, rate:0 });
          computeTotal();
      }
  });

  on("btnAdd","click", ()=> addStepRow({ time:30, temp:25, rate:0 }));
  
  on("btnSave","click", async () => {
      const name = (val("profName")||"Unnamed").trim();
      await fetch("/api/profiles", {
          method: "POST", headers: {"Content-Type":"application/json"},
          body: JSON.stringify({
              name, 
              meta: { entryTemp: UNIT_builder_temp, entryTime: UNIT_builder_time },
              steps: readSteps(),
              // NEW: Save the compiled machine code so Aux buttons can read it!
              compiled_steps: builderToServerSteps() 
          })
      });
      await refreshProfiles();
      alert(`Saved ${name}`);
  });
  
  on("btnLoad","click", async () => {
      const name = document.getElementById("profSelect").value;
      await loadProfileByName(name);
  });

  on("profSelect", "change", async (e) => {
      if (e.target.value) await loadProfileByName(e.target.value);
  });

  on("btnDelete","click", async () => {
    const name = document.getElementById("profSelect").value;
    if(confirm(`Delete ${name}?`)) {
        await fetch(`/api/profiles/${encodeURIComponent(name)}`, { method:"DELETE" });
        refreshProfiles();
    }
  });

  on("btnRefreshProfiles","click", refreshProfiles);
  
  on("btnStart","click", () => {
      const steps = builderToServerSteps();
      if (!steps.length) { alert("Empty profile"); return; }
      const name = (val("profName")||"Unnamed").trim();
      const sec = plannedSpanFrom({steps}) || builderSpanSec || 0;
      const cost = kwhCostForSeconds(sec);
      pendingAction = 'start-profile';
      pendingPayload = { name, steps, plannedSec: sec };
      showRunModal({
        title: "Start Profile?", name, runtimeSec: sec, cost,
        runLenLabel: "Planned run length:", costLabel: "Estimated cost:"
      });
  });
  
  on("btnQuick","click", showQuickModal);
  
  on("btnStop","click", () => {
      const sec = lastStatus?.kiln_runtime_sec ?? 0;
      const cost = kwhCostForSeconds(sec);
      pendingAction = 'stop';
      showRunModal({
        title: "Stop Run?", name: lastStatus?.running_profile_name || "Run",
        runtimeSec: sec, cost, runLenLabel: "Runtime so far:", costLabel: "Cost so far:"
      });
  });
  
  on("rmCancel","click", () => {
    pendingAction = null; 
    hideRunModal();
  });
  on("rmOK","click", async () => { await runPendingAction(); hideRunModal(); });
  
  on("btnResumeAck", "click", async () => {
      await fetch("/api/resume/ack", { method: "POST" });
      document.getElementById("resumeModal").classList.remove("show");
  });

  on("btnPreview", "click", renderPreviewChart);
  on("btnClosePreview", "click", () => {
      document.getElementById("previewModal").classList.remove("show");
      document.body.classList.remove("modal-open");
  });

  on("btnCloseHistoryGraph", "click", () => {
      document.getElementById("historyGraphModal").classList.remove("show");
      document.body.classList.remove("modal-open");
  });
}

async function refreshProfiles(){
  try{
    const r = await fetch("/api/profiles");
    const j = await r.json();
    
    if (j.refresh_sec) {
        profileRefreshMs = j.refresh_sec * 1000;
    }

    const sel = document.getElementById("profSelect");
    if (sel){
      // 1. Remember the current selection
      const currentVal = sel.value; 

      sel.innerHTML = "";
      for (const name of (j.profiles||[])){
        const opt = document.createElement("option"); 
        opt.value = name; opt.textContent = name;
        sel.appendChild(opt);
      }
      
      // 2. Restore the selection if the profile still exists in the list
      if (currentVal && j.profiles.includes(currentVal)) {
          sel.value = currentVal;
      } else if (currentProfileSelected) {
          sel.value = currentProfileSelected;
      }
    }
  }catch(e){ console.error(e); }
}

async function loadProfileByName(name){
  if (!name) return;
  const j = await fetch(`/api/profiles/${encodeURIComponent(name)}`).then(r=>r.json());
  const wrap = document.getElementById("steps");
  if (wrap) wrap.innerHTML = "";
  setBuilderBadge(j.name || name);
  setBuilderMeta(j.meta || {});
  for (const s of (j.steps||[])) addStepRow(s);
  computeTotal();
  currentBuilderProfile = name;
}

function setBuilderBadge(name){
  const inp = document.getElementById("profName");
  if (inp) inp.value = (name && name.trim()) ? name.trim() : "Untitled";
}

// =========================================================
// HISTORICAL RUNS LOGIC
// =========================================================

async function fetchHistoricalLogs() {
    const tbody = document.getElementById("historicalRunsBody");
    if (!tbody) return;

    try {
        // ASSUMPTION: Your backend has an endpoint to list the CSV files
        const res = await fetch("/api/logs"); 
        if (!res.ok) throw new Error("Failed to fetch logs");
        
        const logs = await res.json();
        tbody.innerHTML = "";
        
        if (!logs || logs.length === 0) {
            tbody.innerHTML = `<tr><td colspan="3" class="text-muted">No historical runs found.</td></tr>`;
            return;
        }

        // Populate table, assuming backend returns objects like: { filename: "run_20260418-150620.csv", timestamp: 1776544060 }
        logs.forEach(log => {
            const tr = document.createElement("tr");
            
            // Format the timestamp cleanly
            const logDate = new Date(log.timestamp * 1000).toLocaleString();
            
            tr.innerHTML = `
                <td>${logDate}</td>
                <td class="text-info">${log.filename}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info px-3" onclick="viewHistoricalLog('${log.filename}')">
                        Graph
                    </button>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-success px-3" onclick="downloadLog('${log.filename}')">
                        CSV
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
        tbody.innerHTML = `<tr><td colspan="3" class="text-danger">Failed to load logs.</td></tr>`;
    }
}

function downloadLog(filename) {
    // ASSUMPTION: Your backend serves the files from this download endpoint
    window.location.href = `/api/logs/download/${encodeURIComponent(filename)}`;
}

let historyChartInstance = null;

async function viewHistoricalLog(filename) {
    try {
        const res = await fetch(`/api/logs/data/${encodeURIComponent(filename)}`);
        if (!res.ok) throw new Error("Failed to fetch log data");
        const data = await res.json();
        
        const chartData = [];
        const chartSP = [];
        
        // Convert the raw data into the user's currently selected units
        data.forEach(pt => {
            const xVal = secTo(pt.t, UNIT_time_chart);
            const yTemp = (UNIT_temp_chart === "F") ? toF(pt.temp) : pt.temp;
            const ySP = (UNIT_temp_chart === "F") ? toF(pt.sp) : pt.sp;
            
            chartData.push({x: xVal, y: yTemp});
            chartSP.push({x: xVal, y: ySP});
        });

        // Set the modal title to the filename
        document.getElementById("hgTitle").textContent = filename;

        const ctx = document.getElementById("historyGraphChart").getContext("2d");
        
        if (!historyChartInstance) {
            historyChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [
                        {label: "Temp", data: chartData, borderColor: '#fff', borderWidth: 2, pointRadius: 0, tension: 0},
                        {label: "Setpoint", data: chartSP, borderColor: 'rgba(255,255,255,0.5)', borderDash: [6,6], borderWidth: 1, pointRadius: 0}
                    ]
                },
                options: {
                    responsive: true, 
                    maintainAspectRatio: false,
                    interaction: { mode: 'nearest', axis: 'x', intersect: false },
                    scales: {
                        x: { 
                            type: 'linear', 
                            title: { display: true, text: `Time (${UNIT_time_chart})` },
                            ticks: { callback: function(value) { return Number(value.toFixed(2)); } }
                        },
                        y: { title: { display: true, text: `Temp (°${UNIT_temp_chart})` } }
                    },
                    plugins: {
                        legend: { labels: { color: "#ddd" } },
                        tooltip: { callbacks: { title: (items) => `Time: ${items[0].parsed.x.toFixed(2)} ${UNIT_time_chart}` } }
                    }
                }
            });
        } else {
            historyChartInstance.data.datasets[0].data = chartData;
            historyChartInstance.data.datasets[1].data = chartSP;
            historyChartInstance.options.scales.x.title.text = `Time (${UNIT_time_chart})`;
            historyChartInstance.options.scales.y.title.text = `Temp (°${UNIT_temp_chart})`;
            historyChartInstance.update();
        }

        document.getElementById("historyGraphModal").classList.add("show");
        document.body.classList.add("modal-open");
    } catch(e) {
        alert("Error loading graph: " + e.message);
    }
}

//*********************************************************************************/
//***************************AUX BUTTONS******************************************/
//*********************************************************************************/

async function startAuxProfile(index, label) {
    if (!confirm(`Start profile: ${label}?`)) return;
    
    try {
        const res = await fetch("/api/start/aux", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({index: index})
        });
        
        if (!res.ok) {
            const err = await res.json();
            alert("Error: " + err.detail);
        } else {
            // Success - Status update loop will catch the change
            fetchStatus();
        }
    } catch (e) {
        alert("Connection Error: " + e.message);
    }
}

async function initConfig(){
  try {
    const cfg = await fetch('/api/config').then(r=>r.json());
    if (cfg?.kwh_cost != null) COST_RATE = Number(cfg.kwh_cost);
    if (cfg?.kiln_wattage_w != null) KILN_WATTAGE_W = Number(cfg.kiln_wattage_w);
    if (cfg?.def_heat_rate) DEF_HEAT_RATE = Number(cfg.def_heat_rate);
    if (cfg?.def_cool_rate) DEF_COOL_RATE = Number(cfg.def_cool_rate);

    // --- Dynamic UI Populating ---
    if (cfg?.app_name) {
        document.title = cfg.app_name;
        setText("pageTitleDisplay", cfg.app_name);
        setText("footerAppName", cfg.app_name); // Updates the footer
    }
    
    // Populate Network Info in Footer
    if (cfg?.host) setText("footerIpAddress", cfg.host === "0.0.0.0" ? "localhost" : cfg.host);
    if (cfg?.port) setText("footerPort", cfg.port);

    // Load default temp unit
    if (cfg?.def_temp_unit) {
        UNIT_temp_chart = (cfg.def_temp_unit.toUpperCase() === 'F') ? 'F' : 'C';
    }

    // --- Setup Aux Buttons ---
    const auxRow = document.getElementById("auxButtonsRow");
    let hasAux = false;

    [1, 2, 3, 4].forEach(i => {
        const lbl = cfg[`aux_label_${i}`];
        const btn = document.getElementById(`btnAux${i}`);
        
        if (btn) {
            if (lbl && lbl !== "") {
                btn.textContent = lbl;
                btn.onclick = () => startAuxProfile(i, lbl);
                btn.parentElement.classList.remove("d-none"); 
                hasAux = true;
            } else {
                btn.parentElement.classList.add("d-none"); 
            }
        }
    });

    if (hasAux) auxRow.classList.remove("d-none");
  } catch (e) {
    console.error("Failed to load config:", e);
  }
}

window.addEventListener("load", ()=>{
  initConfig();
  makeChart();
  applyBuilderUnitsToUI();
  applyChartUnitsToUI();
  bindToggles();
  bindButtons();
  bindQuickModalButtons();
  refreshProfiles();
  computeTotal();
  tick();
  fetchHistoricalLogs();

  // Bind the refresh button on the new card
  const btnRefreshLogs = document.getElementById("btnRefreshLogs");
  if (btnRefreshLogs) btnRefreshLogs.addEventListener("click", fetchHistoricalLogs);
});