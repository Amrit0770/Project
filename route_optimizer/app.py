#!/usr/bin/env python3
"""
================================================================================
app.py - Smart Emergency Ambulance Routing & Hospital Allocation Command Center
================================================================================
Academic Project: UPES School of Computer Science (SoCS), UPES Dehradun
Student: Amrit Prasad | SAP ID: 590021684 | Batch: B.Tech CSE AIML (2025-2029)
Subject Teacher: Sandeep Chand Kumain
Engine Compliance: C++17 Zero-STL Core Engine IPC Integration

Tactical Emergency Operations Center (EOC) & Computer-Aided Dispatch (CAD) System:
  - Centralized Regional Hospital Bed Network & Live ICU Telemetry
  - Nearest Ambulance Dispatch (ALS/BLS matching P1/P2/P3 triage)
  - In-Transit Live Hospital Bed Saturation Diversion (MDT HUD)
  - Native C++ Binary Execution (Dijkstra, Floyd-Warshall, Ford-Fulkerson, Benchmarks)
================================================================================
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True
from emergency_engine import EmergencyDispatchEngine

# Global Emergency Dispatch Engine Instance
EMERGENCY_ENGINE = EmergencyDispatchEngine(routing_url="http://localhost:5005")

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Emergency Ambulance Routing & Hospital Allocation | UPES Dehradun</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #060913; color: #E2E8F0; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
    #emergency-map { height: 100%; min-height: 520px; background: #070B14; }
    .pulse-p1 {
      box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.8);
      animation: pulse-red 1.2s infinite;
    }
    @keyframes pulse-red {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.8); }
      70% { transform: scale(1.15); box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    .custom-scroll::-webkit-scrollbar { width: 4px; height: 4px; }
    .custom-scroll::-webkit-scrollbar-track { background: #0B1120; }
    .custom-scroll::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 2px; }
    .custom-scroll::-webkit-scrollbar-thumb:hover { background: #334155; }
  </style>
</head>
<body class="flex flex-col h-screen overflow-hidden select-none">

  <!-- ========================================================================= -->
  <!-- 1. TOP TACTICAL COMMAND BAR -->
  <!-- ========================================================================= -->
  <header class="bg-slate-950 border-b border-slate-800/90 shadow-2xl z-20">
    <div class="px-5 py-2.5 flex items-center justify-between">
      <!-- UPES & Project Identity -->
      <div class="flex items-center space-x-3.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-red-600 via-rose-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-red-950/60 border border-red-500/30">
          <i class="fa-solid fa-truck-medical text-white text-lg"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <span class="text-[10px] font-extrabold uppercase tracking-widest text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-500/40 font-mono">UPES School of Computer Science (SoCS)</span>
            <span class="text-[11px] text-slate-400 font-medium">UPES, Dehradun</span>
            <span class="text-[10px] bg-emerald-950/80 text-emerald-400 border border-emerald-700/60 px-2 py-0.5 rounded font-mono font-bold flex items-center">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span> Zero-STL C++17 Core
            </span>
          </div>
          <h1 class="text-sm font-extrabold tracking-tight text-white flex items-center space-x-2 mt-0.5">
            <span>Smart Emergency Ambulance Routing & Hospital Allocation</span>
            <span class="text-xs font-normal text-slate-400 italic font-mono">"Minimizing Response Time, Saving Lives"</span>
          </h1>
        </div>
      </div>

      <!-- Academic Evaluation Metadata Card -->
      <div class="flex items-center space-x-3 text-xs bg-slate-900/90 px-3.5 py-1.5 rounded-xl border border-slate-800 shadow-inner">
        <div>
          <span class="text-slate-400 block text-[9px] uppercase tracking-wider font-mono">Student Researcher</span>
          <span class="font-bold text-white flex items-center text-xs"><i class="fa-solid fa-user-graduate text-indigo-400 mr-1.5 text-xs"></i> Amrit Prasad</span>
        </div>
        <div class="border-l border-slate-800 pl-3">
          <span class="text-slate-400 block text-[9px] uppercase tracking-wider font-mono">SAP ID & Batch</span>
          <span class="font-mono text-emerald-400 font-bold text-xs">590021684 | AIML (25-29)</span>
        </div>
        <div class="border-l border-slate-800 pl-3">
          <span class="text-slate-400 block text-[9px] uppercase tracking-wider font-mono">Subject Teacher</span>
          <span class="font-medium text-slate-200 text-xs">Sandeep Chand Kumain</span>
        </div>
      </div>
    </div>

    <!-- Secondary Command Sub-Bar -->
    <div class="bg-slate-900/95 px-5 py-1.5 flex items-center justify-between border-t border-slate-800/80 text-xs">
      <div class="flex items-center space-x-2">
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono flex items-center mr-1">
          <i class="fa-solid fa-map-location-dot text-indigo-400 mr-1.5"></i> Scenarios:
        </span>
        <button onclick="loadScenario('urban')" id="btn-scen-urban" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-[11px] font-bold rounded-lg text-slate-200 border border-slate-700 transition">
          1. Normal Urban Grid
        </button>
        <button onclick="loadScenario('capacity_shock')" id="btn-scen-shock" class="px-2.5 py-1 bg-red-950/60 hover:bg-red-900 text-[11px] font-bold rounded-lg text-red-300 border border-red-700/60 transition">
          2. Capacity Shock (Surge)
        </button>
        <button onclick="loadScenario('dehradun')" id="btn-scen-dehradun" class="px-2.5 py-1 bg-indigo-950/60 hover:bg-indigo-900 text-[11px] font-bold rounded-lg text-indigo-300 border border-indigo-700/60 transition">
          3. UPES Dehradun Regional
        </button>

        <!-- Live Traffic Feed Indicator & Control -->
        <div class="border-l border-slate-800 pl-3 ml-1 flex items-center space-x-2">
          <div class="flex items-center space-x-1.5 px-2.5 py-1 bg-emerald-950/80 border border-emerald-600/60 rounded-lg text-emerald-300 font-mono font-bold text-[11px] shadow-sm">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>LIVE MAP TRAFFIC ACTIVE</span>
          </div>
          <button onclick="openTrafficModal()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-600/40 rounded-lg text-xs font-mono font-bold flex items-center transition">
            <i class="fa-solid fa-traffic-light mr-1.5 text-amber-400"></i> Traffic Corridors
          </button>
        </div>
      </div>

      <div class="flex items-center space-x-2 text-[11px]">
        <button onclick="executePriorityDispatch()" class="px-3 py-1 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold rounded-lg shadow-md transition flex items-center space-x-1.5">
          <i class="fa-solid fa-bolt"></i>
          <span>Execute Priority Dispatch (MergeSort + Dijkstra)</span>
        </button>
        <button onclick="openCppModal()" class="px-2.5 py-1 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 border border-indigo-700/60 flex items-center space-x-1.5 font-bold transition">
          <i class="fa-solid fa-terminal text-xs"></i>
          <span>C++ Scenario & Benchmarks</span>
        </button>
        <button onclick="openAlgoModal()" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center space-x-1.5 font-bold transition">
          <i class="fa-solid fa-microchip text-xs"></i>
          <span>Algorithms Matrix</span>
        </button>
        <a href="/presentation" target="_blank" class="px-2.5 py-1 rounded-lg bg-teal-950/80 hover:bg-teal-900 text-teal-300 border border-teal-700/60 flex items-center space-x-1.5 font-bold transition" title="Open State-Of-The-Art Interactive Academic Presentation">
          <i class="fa-solid fa-file-powerpoint text-xs"></i>
          <span>SOTA PPT</span>
        </a>
        <button onclick="exportData('csv')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700" title="Export dispatch_history.csv">
          <i class="fa-solid fa-file-csv text-emerald-400"></i>
        </button>
        <button onclick="exportData('json')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700" title="Export metrics.json">
          <i class="fa-solid fa-file-code text-blue-400"></i>
        </button>
      </div>
    </div>
  </header>

  <!-- ========================================================================= -->
  <!-- 2. MAIN CAD OPERATIONAL CONSOLE -->
  <!-- ========================================================================= -->
  <div class="flex-1 flex overflow-hidden">
    
    <!-- Left Sidebar: Operations & Telemetry (38% width) -->
    <div class="w-[38%] min-w-[390px] max-w-[460px] bg-slate-900/90 border-r border-slate-800 flex flex-col overflow-hidden shadow-2xl">
      
      <div class="flex-1 overflow-y-auto custom-scroll p-3.5 space-y-3.5">
        
        <!-- Centralized Regional Hospital Hub Banner -->
        <div class="bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950/60 p-3 rounded-xl border border-slate-800 shadow-md text-xs space-y-2">
          <div class="flex items-center justify-between font-bold">
            <span class="flex items-center text-amber-400 text-xs font-mono">
              <span class="w-2 h-2 rounded-full bg-red-500 mr-2 animate-ping"></span>
              Centralized Regional Hospital Hub
            </span>
            <span id="central-hosp-count" class="text-[10px] bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-700 font-mono">3 Hospitals Active</span>
          </div>

          <div class="grid grid-cols-3 gap-2 text-center text-[10px]">
            <div class="bg-slate-950/80 p-2 rounded-lg border border-slate-800">
              <span class="text-slate-400 block text-[9px] uppercase font-mono">Regional ER Beds</span>
              <span id="central-total-beds" class="font-bold text-sm text-blue-400 font-mono tracking-tight">-/-</span>
              <span id="central-bed-occ" class="text-[9px] text-slate-400 block">0% Occupied</span>
            </div>
            <div class="bg-slate-950/80 p-2 rounded-lg border border-slate-800">
              <span class="text-slate-400 block text-[9px] uppercase font-mono">Regional ICU Beds</span>
              <span id="central-total-icu" class="font-bold text-sm text-purple-400 font-mono tracking-tight">-/-</span>
              <span id="central-icu-occ" class="text-[9px] text-slate-400 block">0% Occupied</span>
            </div>
            <div class="bg-slate-950/80 p-2 rounded-lg border border-slate-800">
              <span class="text-slate-400 block text-[9px] uppercase font-mono">Ambulances Active</span>
              <span id="central-active-ambs" class="font-bold text-sm text-emerald-400 font-mono tracking-tight">0 / 6</span>
              <span class="text-[9px] text-emerald-400 block font-mono">GPS Tracked</span>
            </div>
          </div>
        </div>

        <!-- Regional Hospital ER & ICU Real-Time Capacity Monitoring -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center font-mono">
              <i class="fa-solid fa-hospital text-purple-400 mr-1.5"></i> Regional Hospitals & Capacity Check
            </h3>
            <span class="text-[10px] text-slate-400 font-mono">Live ER / ICU Telemetry</span>
          </div>
          <div id="hospitals-container" class="space-y-2">
            <!-- Populated dynamically -->
          </div>
        </div>

        <!-- Emergency Incident Triage Queue (P1/P2/P3) -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center font-mono">
              <i class="fa-solid fa-triangle-exclamation text-amber-400 mr-1.5"></i> Emergency Incident Queue
            </h3>
            <button onclick="openCadIntakeModal()" class="text-xs px-2.5 py-1 bg-red-600 hover:bg-red-500 text-white font-bold rounded-lg shadow transition flex items-center space-x-1">
              <i class="fa-solid fa-phone-volume mr-1"></i>
              <span>New 108 CAD Call</span>
            </button>
          </div>
          <div class="max-h-56 overflow-y-auto custom-scroll border border-slate-800 rounded-xl bg-slate-950/70">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-900 text-slate-400 sticky top-0 text-[10px] font-mono uppercase">
                <tr>
                  <th class="p-2">ID</th>
                  <th class="p-2">Priority</th>
                  <th class="p-2">Location & Clinical Condition</th>
                  <th class="p-2 text-right">CAD Action</th>
                </tr>
              </thead>
              <tbody id="emergency-incidents-body" class="divide-y divide-slate-800/80 text-xs">
                <!-- Populated dynamically -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Ambulance Fleet Status & Live Vitals -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center font-mono">
              <i class="fa-solid fa-truck-medical text-emerald-400 mr-1.5"></i> Fleet GPS Telemetry
            </h3>
            <span class="text-[10px] text-slate-400 font-mono">ALS (Adv) &middot; BLS (Basic)</span>
          </div>
          <div class="max-h-48 overflow-y-auto custom-scroll border border-slate-800 rounded-xl bg-slate-950/70">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-900 text-slate-400 sticky top-0 text-[10px] font-mono uppercase">
                <tr>
                  <th class="p-2">Unit</th>
                  <th class="p-2">Type</th>
                  <th class="p-2">Status</th>
                  <th class="p-2">Destination</th>
                  <th class="p-2 font-mono text-right">ETA</th>
                </tr>
              </thead>
              <tbody id="emergency-ambulances-body" class="divide-y divide-slate-800/80 text-xs">
                <!-- Populated dynamically -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

    </div>

    <!-- Right Pane: Tactical Leaflet Map & Bottom Telemetry Bar -->
    <div class="flex-1 flex flex-col relative overflow-hidden bg-slate-950">
      
      <!-- Leaflet Map Container -->
      <div id="emergency-map" class="flex-1"></div>

      <!-- Floating Map Live Traffic Legend & Source Status -->
      <div id="traffic-legend-pill" class="absolute top-4 left-4 z-[500] bg-slate-900/95 border border-slate-700/80 rounded-xl p-2.5 shadow-2xl backdrop-blur-md text-[11px] font-mono text-white pointer-events-auto transition-all">
        <div class="flex items-center justify-between pb-1.5 border-b border-slate-800 mb-1.5 cursor-pointer select-none" onclick="toggleTrafficPill()" title="Click to collapse/expand legend">
          <span class="font-bold flex items-center text-emerald-400 text-xs">
            <i class="fa-solid fa-satellite-dish mr-1.5 text-emerald-400"></i> GOOGLE MAP TRAFFIC
          </span>
          <div class="flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <i id="traffic-pill-chevron" class="fa-solid fa-chevron-up text-slate-400 text-[10px] ml-1"></i>
          </div>
        </div>
        <div id="traffic-pill-body">
          <div class="grid grid-cols-2 gap-x-3 gap-y-1 text-[10px]">
            <div class="flex items-center space-x-1.5"><span class="w-3 h-1.5 rounded-sm bg-emerald-500"></span><span class="text-slate-300">Fast (&gt;45 km/h)</span></div>
            <div class="flex items-center space-x-1.5"><span class="w-3 h-1.5 rounded-sm bg-amber-400"></span><span class="text-slate-300">Moderate (25-45)</span></div>
            <div class="flex items-center space-x-1.5"><span class="w-3 h-1.5 rounded-sm bg-rose-600"></span><span class="text-slate-300">Heavy (10-25)</span></div>
            <div class="flex items-center space-x-1.5"><span class="w-3 h-1.5 rounded-sm bg-red-950 border border-rose-500"></span><span class="text-slate-300">Gridlock (&lt;10)</span></div>
          </div>
          <div class="mt-2 pt-1.5 border-t border-slate-800 flex items-center justify-between text-[9px] text-slate-400">
            <span>Stream: Live Tiles</span>
            <button onclick="openTrafficModal()" class="text-amber-400 hover:underline font-bold">View Corridors &rarr;</button>
          </div>
        </div>
      </div>

      <!-- Live Vitals Telemetry Widget (Displays when an active P1 patient is in transit) -->
      <div id="patient-vitals-card" class="hidden absolute top-4 right-4 z-[500] bg-slate-900/95 border-2 border-red-500/80 rounded-xl p-3 shadow-2xl text-xs w-64 backdrop-blur-md">
        <div class="flex items-center justify-between pb-1.5 border-b border-slate-800 mb-2">
          <span class="font-bold text-red-400 flex items-center font-mono">
            <i class="fa-solid fa-heart-pulse mr-1.5 animate-bounce text-red-500"></i> LIVE PATIENT TELEMETRY
          </span>
          <span class="text-[9px] bg-red-950 text-red-300 px-1.5 py-0.5 rounded border border-red-800 font-mono font-bold">P1 CRITICAL</span>
        </div>
        <div class="grid grid-cols-3 gap-2 text-center font-mono">
          <div class="bg-slate-950 p-1.5 rounded border border-slate-800">
            <span class="text-[9px] text-slate-400 block">ECG HR</span>
            <span id="vital-hr" class="text-sm font-extrabold text-red-400">138 bpm</span>
          </div>
          <div class="bg-slate-950 p-1.5 rounded border border-slate-800">
            <span class="text-[9px] text-slate-400 block">SpO2</span>
            <span id="vital-spo2" class="text-sm font-extrabold text-blue-400">89%</span>
          </div>
          <div class="bg-slate-950 p-1.5 rounded border border-slate-800">
            <span class="text-[9px] text-slate-400 block">BP</span>
            <span id="vital-bp" class="text-sm font-extrabold text-amber-400">85/55</span>
          </div>
        </div>
        <span class="text-[9px] text-slate-400 block mt-2 text-center font-mono">Defibrillator &amp; Ventilator Online (ALS Crew)</span>
      </div>

      <!-- Bottom CAD Mission Telemetry Bar -->
      <div class="bg-slate-950 border-t border-slate-800 px-5 py-2.5 flex items-center justify-between text-xs z-10 shadow-2xl">
        
        <!-- Simulation / Real-Time CAD Clock Controller -->
        <div class="flex items-center space-x-4">
          <div>
            <span id="clock-label" class="text-slate-400 block text-[9px] uppercase tracking-wider font-mono">CAD Mission Clock</span>
            <span id="em-clock" class="text-base font-extrabold font-mono text-emerald-400 tracking-wider">T+ 00:00:00</span>
          </div>

          <div class="flex items-center space-x-1.5 border-l border-slate-800 pl-3">
            <button onclick="toggleRealTimeMode()" id="btn-realtime-toggle" class="px-2.5 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/60 rounded-lg font-bold text-xs flex items-center space-x-1.5 shadow" title="Toggle Real Wall-Clock Mode vs Historical Playback">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span id="realtime-text">Live Clock</span>
            </button>
            <button onclick="toggleSimulationPlay()" id="btn-play-pause" class="px-2.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold text-xs flex items-center space-x-1 shadow">
              <i id="play-icon" class="fa-solid fa-play text-xs"></i>
              <span id="play-text">Playback</span>
            </button>
            <button onclick="stepSimulation(15)" class="px-2 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-mono font-bold" title="Advance 15 seconds">+15s</button>
            <button onclick="stepSimulation(30)" class="px-2 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-mono font-bold" title="Advance 30 seconds">+30s</button>
            <button onclick="stepSimulation(60)" class="px-2 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-mono font-bold" title="Advance 60 seconds">+60s</button>
            <button onclick="resetSimulation()" class="px-2 py-1.5 bg-slate-800 hover:bg-slate-700 text-rose-400 rounded-lg text-xs font-mono font-bold" title="Reset Clock to Zero"><i class="fa-solid fa-arrow-rotate-left"></i></button>
          </div>

          <div class="border-l border-slate-800 pl-4 hidden xl:block">
            <span class="text-slate-400 block text-[9px] uppercase tracking-wider font-mono">Objective Function Z</span>
            <span id="em-objZ" class="text-base font-extrabold font-mono text-amber-400 tracking-wider">0.00</span>
          </div>

          <div class="border-l border-slate-800 pl-4 hidden 2xl:block">
            <span class="text-slate-400 block text-[9px] uppercase tracking-wider font-mono">Math Recurrence</span>
            <span class="text-[11px] text-slate-300 font-mono">Min Z = &sum; w<sub>pri</sub> &middot; [d(amb, inc) + d(inc, hosp)]</span>
          </div>
        </div>

        <!-- Live CAD Ticker Output -->
        <div class="flex-1 max-w-xl mx-4">
          <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center space-x-2 text-xs">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="text-slate-400 font-mono text-[10px] uppercase">CAD:</span>
            <span id="em-event-log" class="text-slate-200 truncate font-mono text-xs">System Initialized. Ready for emergency dispatches.</span>
          </div>
        </div>

      </div>

    </div>

  </div>

  <!-- ========================================================================= -->
  <!-- 3. IN-TRANSIT DRIVER ALERT POPUP (MDT Live Diversion HUD) -->
  <!-- ========================================================================= -->
  <div id="driver-alert-modal" class="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border-2 border-red-500 rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden text-white animate-bounce-once">
      
      <!-- Flashing Red Header -->
      <div class="bg-gradient-to-r from-red-700 via-rose-600 to-red-800 px-6 py-4 flex items-center justify-between border-b border-red-500">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-full bg-white text-red-700 flex items-center justify-center font-bold text-xl animate-pulse">
            <i class="fa-solid fa-triangle-exclamation"></i>
          </div>
          <div>
            <h3 class="text-base font-extrabold tracking-wide uppercase text-white flex items-center space-x-2">
              <span>🚨 IN-TRANSIT DIVERSION ALERT</span>
            </h3>
            <span id="alert-driver-unit" class="text-xs font-mono text-red-100">Mobile Data Terminal (MDT) — Unit: MEDIC-1 (ALS)</span>
          </div>
        </div>
        <span class="px-2.5 py-1 rounded-full bg-red-950 text-red-200 text-xs font-mono font-bold border border-red-800">PRIORITY 1</span>
      </div>

      <!-- Alert Body -->
      <div class="p-6 space-y-4 text-xs">
        <div class="bg-red-950/80 border border-red-700 p-3.5 rounded-xl text-red-200 space-y-1">
          <div class="font-bold text-red-100 flex items-center text-sm">
            <i class="fa-solid fa-ban text-red-400 mr-2 text-base"></i>
            <span id="alert-old-hosp-name">St. Jude Trauma Center</span>: 100% BEDS FULL
          </div>
          <p class="text-xs text-red-300">
            Emergency department & ICU capacity ceiling reached while vehicle was in transit. Access denied by Central Command.
          </p>
        </div>

        <div class="bg-slate-800/90 border border-slate-700 p-4 rounded-xl space-y-3">
          <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block font-mono">Central Dispatch Diverted Destination:</span>
          <div class="flex items-center justify-between">
            <div>
              <span id="alert-new-hosp-name" class="text-base font-extrabold text-emerald-400 block">Metro General Hospital</span>
              <span id="alert-new-hosp-meta" class="text-[11px] text-slate-300">Level 2 Trauma Center &middot; ICU Units: 4 &middot; ER Beds: 18</span>
            </div>
            <div class="text-right">
              <span class="text-[10px] text-slate-400 block uppercase font-mono">Recalculated ETA</span>
              <span id="alert-new-eta" class="text-lg font-extrabold text-amber-400 font-mono">+3.8 min</span>
            </div>
          </div>
        </div>

        <div class="bg-slate-800/50 p-3 rounded-lg border border-slate-700 text-slate-300 space-y-1">
          <div class="flex justify-between">
            <span class="text-slate-400">Patient on Board:</span>
            <b id="alert-patient-name" class="text-white">Incident #101</b>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-400">Clinical Diagnosis:</span>
            <span id="alert-patient-condition" class="text-amber-300 font-medium">Acute Myocardial Infarction</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-400">Algorithm Recalculation:</span>
            <span class="text-indigo-400 font-mono">Dijkstra Dynamic Shortest Path from Live GPS Waypoint</span>
          </div>
        </div>

        <!-- Confirm Button -->
        <button onclick="acknowledgeDriverAlert()" class="w-full py-3 px-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-sm rounded-xl shadow-lg transition flex items-center justify-center space-x-2">
          <i class="fa-solid fa-route text-base"></i>
          <span>Acknowledge & Divert Navigation to New Hospital</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 4. STRUCTURED CAD 108 CALL INTAKE MODAL (No window.prompt!) -->
  <!-- ========================================================================= -->
  <div id="cad-intake-modal" class="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl max-w-md w-full overflow-hidden text-white">
      <div class="bg-slate-950 px-5 py-4 flex items-center justify-between border-b border-slate-800">
        <h3 class="text-sm font-bold flex items-center text-white">
          <i class="fa-solid fa-headset text-red-500 mr-2"></i> 108 Emergency Incident CAD Intake
        </h3>
        <button onclick="closeCadIntakeModal()" class="text-slate-400 hover:text-white">&times;</button>
      </div>
      <div class="p-5 space-y-3.5 text-xs">
        <div>
          <label class="block text-slate-400 mb-1 font-mono uppercase text-[10px]">Caller Landmark / Location</label>
          <input id="intake-name" type="text" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-white text-xs focus:ring-1 focus:ring-red-500 outline-none" placeholder="e.g., Premnagar Chowk / City Square"/>
        </div>
        <div>
          <label class="block text-slate-400 mb-1 font-mono uppercase text-[10px]">Triage Priority (Medical MPDS Protocol)</label>
          <select id="intake-priority" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-white text-xs outline-none">
            <option value="P1-CRITICAL">P1 - CRITICAL (Cardiac Arrest, Polytrauma, Hypoxia) [Requires ALS + ICU]</option>
            <option value="P2-URGENT">P2 - URGENT (Compound Fractures, Concussion) [Requires BLS/ALS]</option>
            <option value="P3-DELAYED">P3 - DELAYED (Controlled Bleeding, Minor Sprain) [BLS Unit]</option>
          </select>
        </div>
        <div>
          <label class="block text-slate-400 mb-1 font-mono uppercase text-[10px]">Clinical Complaint / Chief Symptoms</label>
          <input id="intake-desc" type="text" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-white text-xs outline-none" placeholder="e.g., Unconscious male, chest pain, shallow breathing"/>
        </div>
        <div class="pt-2">
          <button onclick="submitCadIntake()" class="w-full py-2.5 bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl shadow transition">
            Register Incident & Trigger CAD Triage
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 5. ALGORITHMS IMPLEMENTED MATRIX & DEEP DIVE (Comprehensive Architecture) -->
  <!-- ========================================================================= -->
  <div id="algo-modal" class="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-5 hidden">
    <div class="bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl max-w-5xl w-full max-h-[92vh] flex flex-col overflow-hidden text-white">
      <!-- Modal Header -->
      <div class="bg-slate-950 px-6 py-4 flex items-center justify-between border-b border-slate-800">
        <div>
          <h3 class="text-base sm:text-lg font-extrabold flex items-center text-white">
            <i class="fa-solid fa-microchip text-indigo-400 mr-2.5"></i> Algorithms Implemented Matrix: Deep-Dive Architecture
          </h3>
          <p class="text-xs text-slate-400 font-mono mt-0.5">
            UPES SoCS Specification | C++17 Strict Zero-STL Engine | Researcher: Amrit Prasad (SAP: 590021684) | Guide: Sandeep Chand Kumain
          </p>
        </div>
        <button onclick="closeAlgoModal()" class="text-slate-400 hover:text-white text-2xl font-bold p-1">&times;</button>
      </div>

      <!-- Search & Category Filter Navigation Bar -->
      <div class="bg-slate-950/70 border-b border-slate-800/80 px-6 py-2.5 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center space-x-2 text-xs overflow-x-auto py-1 custom-scroll" id="algo-tab-buttons">
          <button onclick="filterAlgoTab('all')" id="tab-btn-all" class="px-2.5 py-1 rounded-md font-bold bg-indigo-600 text-white transition">All Modules (7)</button>
          <button onclick="filterAlgoTab('sorting')" id="tab-btn-sorting" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">1. Sorting & Triage</button>
          <button onclick="filterAlgoTab('greedy')" id="tab-btn-greedy" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">2. Routing & Greedy</button>
          <button onclick="filterAlgoTab('dp')" id="tab-btn-dp" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">3. Payload DP</button>
          <button onclick="filterAlgoTab('network')" id="tab-btn-network" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">4. Flow & Beds</button>
          <button onclick="filterAlgoTab('dc')" id="tab-btn-dc" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">5. Divide & Conquer</button>
          <button onclick="filterAlgoTab('strings')" id="tab-btn-strings" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">6. Strings & CRT</button>
          <button onclick="filterAlgoTab('backtrack')" id="tab-btn-backtrack" class="px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition">7. Backtracking & BB</button>
        </div>
        <div class="relative w-full sm:w-64">
          <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-500 text-xs"></i>
          <input type="text" id="algo-search-input" onkeyup="searchAlgoCards(this.value)" placeholder="Search algorithm, purpose, or role..." class="w-full bg-slate-900 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-mono">
        </div>
      </div>

      <!-- Modal Body (Deep-Dive Cards) -->
      <div class="p-6 overflow-y-auto custom-scroll text-xs space-y-4" id="algo-cards-container">

        <!-- MODULE 1: SORTING & RETRIEVAL -->
        <div class="algo-card p-4 rounded-xl border border-blue-900/60 bg-slate-950/90 space-y-3" data-category="sorting" data-keywords="sorting retrieval mergesort quicksort binary search triage priority dispatch queue ambulance ranking lookup">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-blue-950 text-blue-300 border border-blue-700/60 font-mono">Module 1</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-arrow-down-a-z text-blue-400 mr-2"></i> Sorting &amp; Retrieval: Priority Triage &amp; Telemetry Lookup
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-blue-300 font-semibold font-mono">MergeSort</span>, <span class="text-blue-300 font-semibold font-mono">QuickSort</span>, <span class="text-blue-300 font-semibold font-mono">Iterative &amp; Recursive Binary Search</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('1')" class="px-2.5 py-1 bg-blue-900/70 hover:bg-blue-800 text-blue-200 border border-blue-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Emergency Call Triage Sorting (MergeSort):</b> In high-casualty events, calls arrive asynchronously. The engine computes a composite severity metric (priority weight &times; wait time). MergeSort performs a <i>stable sort</i> in O(N log N) time, ensuring first-in-first-out fairness for calls of equal priority.</li>
                <li><b class="text-white">Fleet Unit Distance Ranking (QuickSort):</b> When an incident occurs, in-service ambulances are ranked by road travel time to identify primary and secondary backup units in O(N log N) average time.</li>
                <li><b class="text-white">Patient Record &amp; Vehicle Index Lookup (Binary Search):</b> Provides rapid O(log N) retrieval of telemetry and hospital bed status from pre-sorted internal registries.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">MergeSort Time:</span><span class="text-emerald-300 font-bold">O(N log N) [T(n) = 2T(n/2) + Θ(n)]</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">QuickSort Time:</span><span class="text-emerald-300 font-bold">Avg O(N log N), Worst O(N²)</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Binary Search:</span><span class="text-emerald-300 font-bold">O(log N) Time · O(1) Space</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Zero-STL CustomVector&lt;T&gt; with custom comparator</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODULE 2: GREEDY ALGORITHMS -->
        <div class="algo-card p-4 rounded-xl border border-emerald-900/60 bg-slate-950/90 space-y-3" data-category="greedy" data-keywords="greedy dijkstra prim kruskal shortest path routing minimum spanning tree emergency corridor traffic congestion">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-emerald-950 text-emerald-300 border border-emerald-700/60 font-mono">Module 2</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-diagram-project text-emerald-400 mr-2"></i> Greedy Algorithms: Traffic-Aware Shortest Path &amp; Corridor MST
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-emerald-300 font-semibold font-mono">Dijkstra's Algorithm (Min-Heap)</span>, <span class="text-emerald-300 font-semibold font-mono">Prim's MST</span>, <span class="text-emerald-300 font-semibold font-mono">Kruskal's MST</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('3')" class="px-2.5 py-1 bg-emerald-900/70 hover:bg-emerald-800 text-emerald-200 border border-emerald-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Two-Leg Emergency Routing (Dijkstra):</b> Computes Leg 1 (Station ➔ Incident Scene) and Leg 2 (Scene ➔ Receiving Hospital). Dynamic edge costs incorporate live Google Traffic congestion: travel cost = (road distance / speed limit) &times; (1 + traffic jam multiplier).</li>
                <li><b class="text-white">Emergency Communication Backbone (Prim / Kruskal):</b> Computes the Minimum Spanning Tree connecting all regional hospital hubs and dispatch repeater towers, ensuring minimal-cost, loop-free telemetry networks.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Dijkstra Runtime:</span><span class="text-emerald-300 font-bold">O((V + E) log V) via Min-Heap</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Prim / Kruskal MST:</span><span class="text-emerald-300 font-bold">O(E log V) / O(E log E)</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Live Metric (1000 Nodes):</span><span class="text-amber-300 font-bold">0.0058 ms (vs 1000 ms Floyd-Warshall)</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Custom MinHeap&lt;K, V&gt; &amp; Disjoint Set Union (DSU)</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODULE 3: DYNAMIC PROGRAMMING -->
        <div class="algo-card p-4 rounded-xl border border-purple-900/60 bg-slate-950/90 space-y-3" data-category="dp" data-keywords="dynamic programming knapsack floyd warshall lcs tsp payload equipment hospital diversion transcript diffing">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-purple-950 text-purple-300 border border-purple-700/60 font-mono">Module 3</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-cubes text-purple-400 mr-2"></i> Dynamic Programming: Ambulance Payload Optimization &amp; Hospital Diversion
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-purple-300 font-semibold font-mono">0/1 Knapsack</span>, <span class="text-purple-300 font-semibold font-mono">Floyd-Warshall All-Pairs</span>, <span class="text-purple-300 font-semibold font-mono">Longest Common Subsequence (LCS)</span>, <span class="text-purple-300 font-semibold font-mono">TSP (Bitmask DP)</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('4')" class="px-2.5 py-1 bg-purple-900/70 hover:bg-purple-800 text-purple-200 border border-purple-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Ambulance Medical Payload (0/1 Knapsack):</b> Ambulances have a strict weight budget (approx 100 kg). Paramedics carry defibrillators, ventilators, ECMO, and pediatric kits, each with an equipment weight and clinical readiness score. 0/1 Knapsack DP maximizes total life-saving utility under 100 kg in 0.0076 ms.</li>
                <li><b class="text-white">Instant Inter-Hospital Diversion Matrix (Floyd-Warshall):</b> Precomputes all-pairs shortest paths across the regional network. When an ER reaches 100% capacity, the system diverts ambulances to the closest alternate hospital with available ICU beds in instantaneous 1-step O(1) table lookup time.</li>
                <li><b class="text-white">Dispatch Transcript Diffing (LCS):</b> Compares caller audio transcripts against paramedic handover notes to detect symptom deterioration in O(M &times; N) time.</li>
                <li><b class="text-white">Multi-Stop Transfer Rounds (TSP Bitmask DP):</b> Optimizes non-emergency patient inter-facility transfers in O(N² &times; 2^N) time.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">0/1 Knapsack:</span><span class="text-emerald-300 font-bold">O(N · W) Time · O(N · W) Space</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Floyd-Warshall:</span><span class="text-emerald-300 font-bold">O(V³) Time · O(V²) Space</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">LCS String Match:</span><span class="text-emerald-300 font-bold">O(M · N) Time · O(M · N) Space</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Custom 2D matrix buffers with zero heap reallocation</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODULE 4: NETWORK FLOW & BIPARTITE MATCHING -->
        <div class="algo-card p-4 rounded-xl border border-rose-900/60 bg-slate-950/90 space-y-3" data-category="network" data-keywords="network flow max flow matching edmonds karp ford fulkerson bipartite matching mass casualty disaster evacuation hospital capacity beds">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-rose-950 text-rose-300 border border-rose-700/60 font-mono">Module 4</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-network-wired text-rose-400 mr-2"></i> Network Flow &amp; Matching: Mass-Casualty Evacuation &amp; Bed Capacity Ceiling
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-rose-300 font-semibold font-mono">Edmonds-Karp (Ford-Fulkerson Max Flow)</span>, <span class="text-rose-300 font-semibold font-mono">Maximum Bipartite Matching (Kuhn's Augmenting Path)</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('5')" class="px-2.5 py-1 bg-rose-900/70 hover:bg-rose-800 text-rose-200 border border-rose-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Mass Casualty Evacuation Ceiling (Edmonds-Karp Max Flow):</b> In regional disasters, dozens of patients must be transported simultaneously. The regional road corridors and emergency rooms are modeled as a flow network with the disaster zone as the source and regional hospital bed pools as the sink. Max Flow computes the maximum casualty throughput (patients/hour) the healthcare network can absorb without gridlock.</li>
                <li><b class="text-white">Ambulance-to-Incident Surge Matching (Bipartite Matching):</b> When multiple simultaneous 911 calls arrive, bipartite matching assigns available ALS/BLS vehicles to incidents in 1.58 µs, avoiding race conditions and maximizing lives saved.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Edmonds-Karp Max Flow:</span><span class="text-emerald-300 font-bold">O(V · E²) Time · O(V + E) Space</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Bipartite Matching:</span><span class="text-emerald-300 font-bold">O(V · E) via Kuhn's Augmenting Path</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Benchmark Metric:</span><span class="text-amber-300 font-bold">12 Disjoint Pairs Matched in 1.58 µs</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Residual graph with reverse edge capacity pointers</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODULE 5: DIVIDE & CONQUER -->
        <div class="algo-card p-4 rounded-xl border border-amber-900/60 bg-slate-950/90 space-y-3" data-category="dc" data-keywords="divide conquer max subarray fast powering celebrity problem strassen traffic surge congestion hub identification decay">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-amber-950 text-amber-300 border border-amber-700/60 font-mono">Module 5</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-code-fork text-amber-400 mr-2"></i> Divide &amp; Conquer: Traffic Congestion Spikes &amp; Transit Hub Discovery
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-amber-300 font-semibold font-mono">Maximum Subarray (Divide &amp; Conquer)</span>, <span class="text-amber-300 font-semibold font-mono">Fast Powering (O(log exp))</span>, <span class="text-amber-300 font-semibold font-mono">Celebrity Problem (Hub Discovery)</span>, <span class="text-amber-300 font-semibold font-mono">Strassen Matrix</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('2')" class="px-2.5 py-1 bg-amber-900/70 hover:bg-amber-800 text-amber-200 border border-amber-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Peak Traffic Congestion Spikes (Max Subarray):</b> Analyzes time-series speed drops on Dehradun corridors (Rajpur Road, Clock Tower). Divide &amp; Conquer in O(N log N) time pinpoints the continuous interval of peak gridlock to forward-stage ambulances before bottleneck saturation occurs.</li>
                <li><b class="text-white">Hazard Decay &amp; Cryptographic Telemetry (Fast Power):</b> Calculates exponential safety metric decay over time in fast logarithmic steps O(log t); powers modular arithmetic for authenticated MDT telemetry.</li>
                <li><b class="text-white">Emergency Transit Hub Identification (Celebrity Problem):</b> An O(V) elimination algorithm locates central transit nodes that receive road traffic from all sectors but generate minimal local egress, identifying ideal forward staging locations.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Max Subarray D&amp;C:</span><span class="text-emerald-300 font-bold">O(N log N) [T(n) = 2T(n/2) + Θ(n)]</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Fast Exponentiation:</span><span class="text-emerald-300 font-bold">O(log exp) Time · O(1) Space</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Celebrity Hub Discovery:</span><span class="text-emerald-300 font-bold">O(V) Elimination</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Recursive stack with in-place index pointer partitioning</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODULE 6: STRINGS & NUMBER THEORY -->
        <div class="algo-card p-4 rounded-xl border border-cyan-900/60 bg-slate-950/90 space-y-3" data-category="strings" data-keywords="strings number theory kmp rabin karp chinese remainder theorem crt audio transcription medical keywords dispatch schedule">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-cyan-950 text-cyan-300 border border-cyan-700/60 font-mono">Module 6</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-magnifying-glass text-cyan-400 mr-2"></i> Strings &amp; Number Theory: Emergency Call Transcript Surveillance &amp; Shift CRT
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-cyan-300 font-semibold font-mono">Knuth-Morris-Pratt (KMP)</span>, <span class="text-cyan-300 font-semibold font-mono">Rabin-Karp Rolling Hash</span>, <span class="text-cyan-300 font-semibold font-mono">Chinese Remainder Theorem (CRT)</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('7')" class="px-2.5 py-1 bg-cyan-900/70 hover:bg-cyan-800 text-cyan-200 border border-cyan-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Emergency Call Audio Surveillance (KMP &amp; Rabin-Karp):</b> Live transcripts of 911/108 calls stream into CAD. KMP runs in linear O(N + M) time with a precomputed prefix lookup table to scan for critical medical phrases: <i>"cardiac arrest"</i>, <i>"unresponsive"</i>, <i>"massive bleed"</i>. It instantly triggers automatic priority escalation from Priority 2 (Urgent) to Priority 1 (Critical) before human dispatchers finish typing. Rabin-Karp rolling hash enables simultaneous multi-keyword filtering across concurrent incoming call channels.</li>
                <li><b class="text-white">Multi-Cycle Schedule Synchronization (CRT):</b> Operational cycles run on independent schedules with coprime periodicities: ambulance fleet maintenance (every 7 days), medical sterilization (every 5 days), and trauma surgical rotations (every 11 days). The Chinese Remainder Theorem solves these simultaneous cyclic intervals to compute the exact collision-free calendar days when all maintenance and staff rotations align seamlessly.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">KMP Matcher:</span><span class="text-emerald-300 font-bold">O(N + M) Time · O(M) Space (6.33 µs)</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Rabin-Karp Hash:</span><span class="text-emerald-300 font-bold">Avg O(N + M) · Polynomial Rolling Hash</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">CRT Solver:</span><span class="text-emerald-300 font-bold">O(k log(lcm)) via Extended Euclid GCD</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Custom prefix jump table and Extended Euclidean modular inverse</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- MODULE 7: BACKTRACKING & BRANCH AND BOUND -->
        <div class="algo-card p-4 rounded-xl border border-indigo-900/60 bg-slate-950/90 space-y-3" data-category="backtrack" data-keywords="backtracking branch and bound subset sum n queens constraint satisfaction least cost dispatch matching staging">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-indigo-950 text-indigo-300 border border-indigo-700/60 font-mono">Module 7</span>
                <h4 class="font-extrabold text-white text-sm flex items-center font-mono">
                  <i class="fa-solid fa-chess-board text-indigo-400 mr-2"></i> Backtracking &amp; Branch-and-Bound: Blood Unit Bundling &amp; Staging Non-Interference
                </h4>
              </div>
              <p class="text-slate-400 text-xs mt-1">Algorithms: <span class="text-indigo-300 font-semibold font-mono">Subset Sum (Backtracking)</span>, <span class="text-indigo-300 font-semibold font-mono">Least-Cost Branch &amp; Bound</span>, <span class="text-indigo-300 font-semibold font-mono">N-Queens Constraint Solver</span></p>
            </div>
            <button onclick="launchAlgoBenchmark('9')" class="px-2.5 py-1 bg-indigo-900/70 hover:bg-indigo-800 text-indigo-200 border border-indigo-600/60 rounded-lg font-mono text-[11px] font-bold transition flex items-center space-x-1.5">
              <i class="fa-solid fa-play text-[10px]"></i> <span>Run C++ Benchmark</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-slate-300">
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-amber-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-circle-question mr-1.5 text-xs"></i> How it is used in this Dispatch System:</b>
              <ul class="space-y-1.5 list-disc list-inside text-slate-300 leading-relaxed">
                <li><b class="text-white">Transfusion Blood Pack Bundling (Subset Sum):</b> Blood banks store variable-volume whole blood and plasma units. Given a critical trauma patient needing an exact dosage (e.g. 1500 ml), Subset Sum finds a combination of units matching target requirements without wasting scarce blood supplies.</li>
                <li><b class="text-white">Spatial Staging Non-Interference (N-Queens Analogy):</b> Evaluates constraint solvers for ambulance forward standby positioning so no two ambulances share the same arterial choke corridor, guaranteeing distributed urban perimeter coverage.</li>
                <li><b class="text-white">Global Dispatch Matching (Least-Cost Branch &amp; Bound):</b> Prunes the combinatorial assignment tree using lower-bound heuristics to find the globally optimal (ambulance, incident) matching minimizing total response latency.</li>
              </ul>
            </div>
            <div class="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
              <b class="text-emerald-400 block mb-1 font-mono flex items-center"><i class="fa-solid fa-chart-line mr-1.5 text-xs"></i> Asymptotic Complexity &amp; Zero-STL Architecture:</b>
              <div class="space-y-1.5 font-mono text-[11px]">
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Subset Sum:</span><span class="text-emerald-300 font-bold">O(2ⁿ) Pruned State Space · O(N) Recursion</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">Least-Cost B&amp;B:</span><span class="text-emerald-300 font-bold">Best O(N log N) with Lower Bound Heuristic</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span class="text-slate-400">N-Queens Solver:</span><span class="text-emerald-300 font-bold">O(N!) Backtracking</span></div>
                <div class="flex justify-between pt-0.5"><span class="text-slate-400">Implementation:</span><span class="text-indigo-300">Custom recursive depth bounding and bitboard pruning</span></div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Academic Specifications Footer -->
      <div class="bg-slate-950 p-4 border-t border-slate-800 flex flex-wrap items-center justify-between text-xs font-mono text-slate-400">
        <div class="flex items-center space-x-3">
          <span class="text-amber-400 font-bold"><i class="fa-solid fa-graduation-cap mr-1.5"></i> UPES SoCS Project:</span>
          <span>Amrit Prasad (SAP ID: <b class="text-white">590021684</b>)</span>
          <span>&middot;</span>
          <span>Guide: <b class="text-white">Sandeep Chand Kumain</b></span>
        </div>
        <div class="flex items-center space-x-2 mt-2 sm:mt-0">
          <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-700/60 font-bold">C++17 Zero-STL Compliant</span>
          <span class="text-slate-500">|</span>
          <button onclick="closeAlgoModal(); openCppModal();" class="text-indigo-400 hover:text-indigo-300 underline font-bold">Open Interactive C++ Console &rarr;</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 6. REAL-TIME MAP TRAFFIC TELEMETRY & CORRIDOR SPEED MATRIX MODAL -->
  <!-- ========================================================================= -->
  <div id="traffic-modal" class="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[88vh] flex flex-col overflow-hidden text-white">
      <div class="bg-slate-950 px-6 py-4 flex items-center justify-between border-b border-slate-800">
        <div>
          <h3 class="text-base font-extrabold flex items-center text-white">
            <i class="fa-solid fa-traffic-light text-amber-400 mr-2.5"></i> Real-Time Map Traffic Telemetry &amp; Corridor Speed Matrix
          </h3>
          <p class="text-xs text-slate-400 font-mono mt-0.5">Stream: Google Real-Time Traffic Network &middot; Dynamic Traffic-Aware Dijkstra Routing</p>
        </div>
        <button onclick="closeTrafficModal()" class="text-slate-400 hover:text-white text-xl font-bold">&times;</button>
      </div>

      <div class="p-6 overflow-y-auto custom-scroll text-xs space-y-4">
        <!-- Profile Switcher & Routing Toggle -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800">
          <div>
            <label class="block text-slate-400 font-mono uppercase text-[10px] mb-1.5 font-bold">Traffic Condition Profile</label>
            <div class="grid grid-cols-2 gap-2">
              <button onclick="setTrafficProfile('normal')" id="btn-prof-normal" class="px-2.5 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/60 rounded-lg font-bold text-xs text-left flex items-center space-x-1.5">
                <i class="fa-solid fa-road text-emerald-400"></i>
                <span>🟢 Normal Live Flow</span>
              </button>
              <button onclick="setTrafficProfile('rush_hour')" id="btn-prof-rush" class="px-2.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 rounded-lg font-bold text-xs text-left flex items-center space-x-1.5">
                <i class="fa-solid fa-car-burst text-rose-400"></i>
                <span>🚗 Peak Rush Hour</span>
              </button>
              <button onclick="setTrafficProfile('monsoon_rain')" id="btn-prof-rain" class="px-2.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 rounded-lg font-bold text-xs text-left flex items-center space-x-1.5">
                <i class="fa-solid fa-cloud-showers-heavy text-blue-400"></i>
                <span>🌧️ Monsoon Delays</span>
              </button>
              <button onclick="setTrafficProfile('baseline_clear')" id="btn-prof-clear" class="px-2.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 rounded-lg font-bold text-xs text-left flex items-center space-x-1.5">
                <i class="fa-solid fa-gauge text-purple-400"></i>
                <span>⚡ Baseline Free-Flow</span>
              </button>
            </div>
          </div>

          <div class="flex flex-col justify-between">
            <div>
              <label class="block text-slate-400 font-mono uppercase text-[10px] mb-1.5 font-bold">Algorithmic Traffic Avoidance</label>
              <button onclick="toggleTrafficAwareness()" id="btn-traffic-aware" class="w-full px-3 py-2 bg-indigo-900/80 hover:bg-indigo-800 text-indigo-200 border border-indigo-600/70 rounded-lg font-bold text-xs flex items-center justify-between">
                <span class="flex items-center"><i class="fa-solid fa-route mr-2 text-indigo-400"></i> Dynamic Traffic-Aware Dijkstra</span>
                <span id="badge-traffic-aware" class="bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded text-[10px] font-mono border border-indigo-700">ACTIVE</span>
              </button>
            </div>
            <p class="text-[10px] text-slate-400 font-mono mt-2">
              When active, Dijkstra automatically penalizes congested corridors (e.g. Ballupur Chowk) and dynamically reroutes critical units via open bypass corridors (NH-7).
            </p>
          </div>
        </div>

        <!-- Active Regional Corridors List -->
        <div>
          <h4 class="font-bold text-white mb-2 font-mono flex items-center text-xs">
            <i class="fa-solid fa-tower-broadcast text-emerald-400 mr-2"></i> Monitored Road Corridors &amp; Bottlenecks
          </h4>
          <div class="border border-slate-800 rounded-xl overflow-hidden bg-slate-950">
            <table class="w-full text-left text-xs font-mono">
              <thead class="bg-slate-900 text-slate-400 uppercase text-[10px]">
                <tr>
                  <th class="p-2.5">Corridor Name</th>
                  <th class="p-2.5 text-center">Current Speed</th>
                  <th class="p-2.5 text-center">Free Flow</th>
                  <th class="p-2.5 text-center">Jam Factor</th>
                  <th class="p-2.5 text-center">Delay Added</th>
                  <th class="p-2.5 text-center">Status</th>
                </tr>
              </thead>
              <tbody id="traffic-corridors-table" class="divide-y divide-slate-800/80">
                <!-- Populated dynamically -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 7. NATIVE C++ SCENARIO & BENCHMARK RUNNER MODAL -->
  <!-- ========================================================================= -->
  <div id="cpp-modal" class="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden text-white">
      <div class="bg-slate-950 px-6 py-4 flex items-center justify-between border-b border-slate-800">
        <div>
          <h3 class="text-base font-extrabold flex items-center text-white">
            <i class="fa-solid fa-terminal text-emerald-400 mr-2.5"></i> Native Zero-STL C++17 Interactive Terminal
          </h3>
          <p class="text-xs text-slate-400 font-mono mt-0.5">Compiled Binary: <code>smart_emergency_dispatch/bin/dispatch_sim</code> &middot; Interactive STDIN Console</p>
        </div>
        <button onclick="closeCppModal()" class="text-slate-400 hover:text-white text-xl font-bold">&times;</button>
      </div>

      <div class="p-6 overflow-y-auto custom-scroll text-xs space-y-3 flex-1 flex flex-col">
        <!-- Quick Action Command Buttons -->
        <div class="flex flex-wrap gap-1.5 font-mono">
          <button onclick="runNativeScenario(1)" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-bold border border-slate-700 transition flex items-center space-x-1">
            <span class="text-emerald-400 font-bold">[4]</span>
            <span>Scenario 1 (Dijkstra vs FW)</span>
          </button>
          <button onclick="runNativeScenario(2)" class="px-2.5 py-1.5 bg-red-950/80 hover:bg-red-900 text-red-200 rounded-lg font-bold border border-red-800 transition flex items-center space-x-1">
            <span class="text-rose-400 font-bold">[5]</span>
            <span>Scenario 2 (Capacity Shock &amp; Flow)</span>
          </button>
          <button onclick="runNativeScenario(3)" class="px-2.5 py-1.5 bg-purple-950/80 hover:bg-purple-900 text-purple-200 rounded-lg font-bold border border-purple-800 transition flex items-center space-x-1">
            <span class="text-purple-400 font-bold">[6]</span>
            <span>Scenario 3 (Adversarial 1000 Nodes)</span>
          </button>
          <button onclick="runNativeBenchmarks()" class="px-2.5 py-1.5 bg-indigo-900/80 hover:bg-indigo-800 text-indigo-200 rounded-lg font-bold border border-indigo-700 transition flex items-center space-x-1">
            <span class="text-indigo-400 font-bold">[7]</span>
            <span>Empirical Benchmarks</span>
          </button>
          <button onclick="executeCppCommand('9', 'Syllabus Audit Matrix')" class="px-2.5 py-1.5 bg-amber-950/80 hover:bg-amber-900 text-amber-200 rounded-lg font-bold border border-amber-800 transition flex items-center space-x-1">
            <span class="text-amber-400 font-bold">[9]</span>
            <span>Syllabus Audit</span>
          </button>
          <button onclick="executeCppCommand('1', 'Fleet Status Dashboard')" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold border border-slate-700 transition flex items-center space-x-1">
            <span class="text-cyan-400 font-bold">[1]</span>
            <span>Fleet Status</span>
          </button>
          <button onclick="executeCppCommand('2', 'Priority Queue Dispatch')" class="px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-bold border border-slate-700 transition flex items-center space-x-1">
            <span class="text-blue-400 font-bold">[2]</span>
            <span>Priority Dispatch</span>
          </button>
        </div>

        <!-- Terminal Output Window -->
        <div class="bg-black/95 p-4 rounded-xl border border-slate-800 font-mono text-[11px] text-emerald-400 overflow-y-auto overflow-x-auto whitespace-pre leading-relaxed flex-1 min-h-[300px] max-h-[420px] shadow-inner" id="cpp-terminal-output">[READY]: Click any preset button above or type custom inputs into the interactive command prompt below.
========================================================================================
          SMART EMERGENCY AMBULANCE ROUTING &amp; HOSPITAL ALLOCATION SYSTEM                
            Course: Advanced Data Structures &amp; Algorithms | Engine: C++17               
========================================================================================
Type an option number (1-9) or click a quick action above.</div>

        <!-- Interactive Input Bar -->
        <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center space-x-2">
          <span class="text-emerald-400 font-mono font-bold text-sm pl-1">&gt;</span>
          <input id="cpp-custom-input" type="text" class="flex-1 bg-black/80 border border-slate-700 rounded-lg px-3 py-2 text-white font-mono text-xs focus:ring-1 focus:ring-emerald-400 outline-none placeholder:text-slate-500" placeholder="Type command/option (e.g. 1 to 9, or '3 60' for clock step) and press Enter..." onkeydown="if(event.key==='Enter') sendCustomCppInput()" />
          <button onclick="sendCustomCppInput()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-mono font-bold text-xs flex items-center space-x-1.5 shadow transition">
            <i class="fa-solid fa-paper-plane text-xs"></i>
            <span>Execute Input</span>
          </button>
          <button onclick="clearCppTerminal()" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-mono font-bold text-xs border border-slate-700 transition" title="Clear Console">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- 8. APPLICATION LOGIC & MAP INTERACTION SCRIPT -->
  <!-- ========================================================================= -->
  <script>
    let emergencyMap;
    let emLayers = { markers: [], routes: [] };
    let isLiveSimPlaying = false;
    let liveSimInterval = null;
    let isRealTimeClockActive = false;
    let realTimePollingInterval = null;
    let trafficCorridorLayers = [];

    window.onload = function() {
      initEmergencyMap();
      loadEmergencyState();
    };

    function initEmergencyMap() {
      emergencyMap = L.map('emergency-map', {
        zoomControl: false,
        attributionControl: false
      }).setView([30.3444, 78.0205], 12);

      // Clean zoom controls in bottom-right corner
      L.control.zoom({ position: 'bottomright' }).addTo(emergencyMap);

      // 1. Google Real-Time Traffic Base Map (Roads + real-time green/yellow/red traffic lines)
      const googleTraffic = L.tileLayer('https://mt{s}.google.com/vt/lyrs=m,traffic&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['0', '1', '2', '3'],
        attribution: 'Map & Live Traffic &copy; Google Maps'
      });

      // 2. Google Hybrid Satellite with Real-Time Live Traffic
      const googleHybrid = L.tileLayer('https://mt{s}.google.com/vt/lyrs=y,traffic&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['0', '1', '2', '3'],
        attribution: 'Satellite & Traffic &copy; Google Maps'
      });

      // 3. Tactical Dark CAD Base
      const darkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        subdomains: 'abcd',
        attribution: '&copy; CARTO &copy; OpenStreetMap'
      });

      // 4. OpenStreetMap Standard Base
      const osmStandard = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
      });

      // 5. Transparent Google Live Traffic Flow Overlay (renders on top of any layer)
      const googleTrafficOverlay = L.tileLayer('https://mt{s}.google.com/vt/lyrs=h,traffic&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['0', '1', '2', '3'],
        attribution: 'Real-Time Traffic Flow &copy; Google'
      });

      // Default: Google Real-Time Traffic active
      googleTraffic.addTo(emergencyMap);
      googleTrafficOverlay.addTo(emergencyMap);

      // Layer Switcher Control in Top-Right
      const baseMaps = {
        "🚦 Google Live Traffic (Default)": googleTraffic,
        "🛰️ Google Satellite + Traffic": googleHybrid,
        "🌑 Tactical Dark CAD": darkMatter,
        "🌐 OpenStreetMap Standard": osmStandard
      };

      const overlayMaps = {
        "🚗 Live Traffic Flow Layer": googleTrafficOverlay
      };

      L.control.layers(baseMaps, overlayMaps, { position: 'topright' }).addTo(emergencyMap);
    }

    async function loadEmergencyState() {
      try {
        const res = await fetch('/api/emergency/state');
        const data = await res.json();
        renderEmergencyDashboard(data);
      } catch (err) {
        console.error("Failed to load emergency state", err);
      }
    }

    function renderEmergencyDashboard(data) {
      document.getElementById('em-clock').innerText = isRealTimeClockActive ? ((data.real_clock_str || 'LIVE') + ' IST') : (data.clock_str || 'T+ 00:00:00');
      document.getElementById('em-objZ').innerText = Number(data.objective_Z).toFixed(2);

      // 1. Regional Network Totals
      let totalBeds = 0, availBeds = 0, totalIcu = 0, availIcu = 0;
      data.hospitals.forEach(h => {
        totalBeds += h.total_beds;
        availBeds += h.avail_beds;
        totalIcu += h.icu_capacity;
        availIcu += h.avail_icu;
      });
      const activeAmbs = data.ambulances.filter(a => a.status !== 'IDLE').length;

      document.getElementById('central-hosp-count').innerText = `${data.hospitals.length} Facilities Active`;
      document.getElementById('central-total-beds').innerText = `${availBeds} / ${totalBeds}`;
      document.getElementById('central-bed-occ').innerText = `${Math.round(((totalBeds - availBeds)/Math.max(1, totalBeds))*100)}% Occ`;
      document.getElementById('central-total-icu').innerText = `${availIcu} / ${totalIcu}`;
      document.getElementById('central-icu-occ').innerText = `${Math.round(((totalIcu - availIcu)/Math.max(1, totalIcu))*100)}% Occ`;
      document.getElementById('central-active-ambs').innerText = `${activeAmbs} / ${data.ambulances.length}`;

      // 2. Render Hospital Cards
      const hospContainer = document.getElementById('hospitals-container');
      hospContainer.innerHTML = '';
      data.hospitals.forEach(h => {
        const occPct = Math.round(((h.total_beds - h.avail_beds) / h.total_beds) * 100);
        const icuPct = Math.round(((h.icu_capacity - h.avail_icu) / h.icu_capacity) * 100);
        const isFull = (h.avail_beds === 0);
        const card = document.createElement('div');
        card.className = `p-3 rounded-xl bg-slate-950/80 border ${isFull ? 'border-red-500 bg-red-950/20' : 'border-slate-800'} shadow-sm space-y-2`;
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div>
              <span class="font-bold text-white text-xs">${h.name}</span>
              ${isFull ? '<span class="ml-1.5 text-[9px] bg-red-600 text-white font-extrabold px-1.5 py-0.5 rounded font-mono animate-pulse">100% FULL</span>' : ''}
            </div>
            <div class="flex items-center space-x-1.5">
              <span class="text-[10px] px-2 py-0.5 rounded font-mono font-bold ${h.trauma_level === 1 ? 'bg-red-950 text-red-300 border border-red-800' : 'bg-purple-950 text-purple-300 border border-purple-800'}">Trauma L${h.trauma_level}</span>
              <button onclick="triggerHospitalFull(${h.id})" title="Simulate 100% bed full surge" class="text-[9px] bg-rose-950 hover:bg-rose-900 text-rose-300 font-bold px-2 py-0.5 rounded border border-rose-700/80 transition flex items-center space-x-1">
                <i class="fa-solid fa-triangle-exclamation"></i>
                <span>Fill Beds</span>
              </button>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2 text-[10px] font-mono">
            <div>
              <div class="flex justify-between text-slate-400 mb-1">
                <span>ER Beds:</span>
                <b class="${h.avail_beds === 0 ? 'text-red-400 font-extrabold' : 'text-slate-200'}">${h.avail_beds}/${h.total_beds}</b>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="${h.avail_beds === 0 ? 'bg-red-500' : 'bg-blue-500'} h-1.5 transition-all duration-300" style="width: ${occPct}%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-slate-400 mb-1">
                <span>ICU Units:</span>
                <b class="${h.avail_icu === 0 ? 'text-red-400 font-extrabold' : 'text-slate-200'}">${h.avail_icu}/${h.icu_capacity}</b>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="${h.avail_icu === 0 ? 'bg-red-500' : 'bg-purple-500'} h-1.5 transition-all duration-300" style="width: ${icuPct}%"></div>
              </div>
            </div>
          </div>
        `;
        hospContainer.appendChild(card);
      });

      // 3. Render Incident Queue
      const incTable = document.getElementById('emergency-incidents-body');
      incTable.innerHTML = '';
      data.incidents.forEach(inc => {
        const tr = document.createElement('tr');
        const priBadge = inc.priority.includes('P1') ? 'bg-red-950 text-red-300 border border-red-800 font-bold' : (inc.priority.includes('P2') ? 'bg-amber-950 text-amber-300 border border-amber-800 font-semibold' : 'bg-blue-950 text-blue-300 border border-blue-800 font-medium');
        const stBadge = inc.status === 'PENDING' ? 'text-rose-400 font-bold' : (inc.status === 'ASSIGNED' ? 'text-amber-400 font-bold' : 'text-emerald-400 font-bold');
        tr.innerHTML = `
          <td class="p-2 font-mono font-bold text-slate-400">#${inc.id}</td>
          <td class="p-2"><span class="px-1.5 py-0.5 rounded text-[9px] font-mono ${priBadge}">${inc.priority.split('-')[0]}</span></td>
          <td class="p-2">
            <b class="text-white text-xs">${inc.name}</b><br/>
            <span class="text-slate-400 text-[11px]">${inc.description}</span>
          </td>
          <td class="p-2 text-right">
            <span class="${stBadge} block text-[11px] font-mono mb-1">${inc.status}</span>
            ${inc.status === 'PENDING' ? `
              <button onclick="dispatchSingleIncident(${inc.id})" class="text-[9px] bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-2 py-0.5 rounded shadow transition font-mono">
                <i class="fa-solid fa-truck-fast mr-1"></i> Dispatch
              </button>
            ` : ''}
          </td>
        `;
        incTable.appendChild(tr);
      });

      // 4. Render Fleet Telemetry
      const ambTable = document.getElementById('emergency-ambulances-body');
      ambTable.innerHTML = '';
      let activeP1Vitals = null;

      data.ambulances.forEach(a => {
        const tr = document.createElement('tr');
        const isTransporting = a.status === 'TRANSPORTING_HOSPITAL';
        if (isTransporting && a.patient_vitals) {
          activeP1Vitals = a.patient_vitals;
        }

        const trafficBadge = a.traffic_telemetry && a.traffic_telemetry.total_delay_min > 0 
          ? `<span class="ml-1 text-[9px] bg-amber-950 text-amber-300 px-1 py-0.5 rounded border border-amber-800 font-mono">+${a.traffic_telemetry.total_delay_min}m traffic</span>` 
          : '';

        tr.innerHTML = `
          <td class="p-2 font-bold text-white flex items-center">
            ${a.callsign}
            ${trafficBadge}
          </td>
          <td class="p-2"><span class="px-1.5 py-0.5 rounded font-mono text-[9px] font-bold ${a.type === 'ALS' ? 'bg-indigo-950 text-indigo-300 border border-indigo-700' : 'bg-slate-800 text-slate-300'}">${a.type}</span></td>
          <td class="p-2 text-[10px] font-bold ${a.status === 'IDLE' ? 'text-slate-500' : 'text-emerald-400 animate-pulse'} font-mono">${a.status}</td>
          <td class="p-2 text-[10px] text-slate-400 font-mono">${a.current_target_inc ? '#' + a.current_target_inc : '-'}</td>
          <td class="p-2 text-[10px] font-mono text-right text-slate-300">${a.eta_pickup_sec > 0 ? a.eta_pickup_sec + 's' : (a.eta_hosp_sec > 0 ? a.eta_hosp_sec + 's' : '-')}</td>
        `;
        ambTable.appendChild(tr);
      });

      // Update Patient Vitals Card if active P1 in transit
      const vitalsCard = document.getElementById('patient-vitals-card');
      if (activeP1Vitals) {
        vitalsCard.classList.remove('hidden');
        document.getElementById('vital-hr').innerText = `${activeP1Vitals.heart_rate} bpm`;
        document.getElementById('vital-spo2').innerText = `${activeP1Vitals.spo2}%`;
        document.getElementById('vital-bp').innerText = activeP1Vitals.bp;
      } else {
        vitalsCard.classList.add('hidden');
      }

      // 5. Update Map Markers & Clean Phase-Separated Polylines
      emLayers.markers.forEach(m => emergencyMap.removeLayer(m));
      emLayers.routes.forEach(r => emergencyMap.removeLayer(r));
      emLayers.markers = [];
      emLayers.routes = [];

      let bounds = [];

      // Render Hospitals
      data.hospitals.forEach(h => {
        bounds.push(h.coord);
        const isFull = (h.avail_beds === 0);
        const color = isFull ? '#EF4444' : '#9333EA';
        const m = L.marker(h.coord, {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:${color}; color:white; border-radius:10px; width:34px; height:34px; display:flex; align-items:center; justify-content:center; box-shadow:0 0 14px ${color}88; border:2px solid white;"><i class="fa-solid fa-hospital text-sm"></i></div>`,
            iconSize: [34, 34],
            iconAnchor: [17, 17]
          })
        }).bindPopup(`
          <div style="font-family:sans-serif; min-width:180px;">
            <b style="font-size:13px; color:#111;">${h.name}</b><br/>
            <span style="font-size:11px; color:#666;">Trauma Center Level ${h.trauma_level}</span><hr style="margin:4px 0;"/>
            <b>ER Beds:</b> ${h.avail_beds} / ${h.total_beds}<br/>
            <b>ICU Units:</b> ${h.avail_icu} / ${h.icu_capacity}<br/>
            <span style="font-size:10px; color:${isFull ? '#DC2626' : '#16A34A'}; font-weight:bold;">${isFull ? 'STATUS: ACCESS DENIED (FULL)' : 'STATUS: ADMITTING'}</span>
          </div>
        `).addTo(emergencyMap);
        emLayers.markers.push(m);
      });

      // Render Emergency Incidents
      data.incidents.forEach(inc => {
        bounds.push(inc.coord);
        const isP1 = inc.priority.includes('P1');
        const color = isP1 ? '#EF4444' : (inc.priority.includes('P2') ? '#F59E0B' : '#3B82F6');
        const isPending = inc.status === 'PENDING';

        const m = L.marker(inc.coord, {
          icon: L.divIcon({
            className: isP1 && isPending ? 'pulse-p1' : '',
            html: `<div style="background:${color}; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:11px; border:2px solid #ffffff; box-shadow:0 0 12px ${color}AA;"><i class="fa-solid fa-triangle-exclamation"></i></div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          })
        }).bindPopup(`
          <div style="font-family:sans-serif; min-width:200px;">
            <b style="color:${color}; font-size:13px;">${inc.priority}: #${inc.id}</b><br/>
            <b>Location:</b> ${inc.name}<br/>
            <b>Condition:</b> ${inc.description}<br/>
            <b>Status:</b> ${inc.status}
          </div>
        `).addTo(emergencyMap);
        emLayers.markers.push(m);
      });

      // Render Ambulances with Interpolated Coordinates & Phase-Separated Polylines
      data.ambulances.forEach(a => {
        bounds.push(a.current_coord);
        const isMoving = a.status !== 'IDLE';
        const color = a.type === 'ALS' ? '#06B6D4' : '#10B981';

        const m = L.marker(a.current_coord, {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:${color}; color:white; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; border:2px solid white; box-shadow:0 0 12px ${color};"><i class="fa-solid fa-ambulance text-xs ${isMoving ? 'animate-bounce' : ''}"></i></div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
          })
        }).bindPopup(`
          <div style="font-family:sans-serif; min-width:180px;">
            <b style="font-size:13px;">${a.callsign} (${a.type})</b><br/>
            <b>Status:</b> ${a.status}<br/>
            <b>Speed:</b> ${a.speed_kmh} km/h<br/>
            <b>Equipment Score:</b> ${a.equip_score} pts
          </div>
        `).addTo(emergencyMap);
        emLayers.markers.push(m);

        // Phase-Separated Rendering:
        // Leg 1: Render dashed cyan line ONLY while en route to scene
        if (a.status === 'EN_ROUTE_PICKUP' && a.route_pickup && a.route_pickup.length > 0) {
          const l1 = L.polyline(a.route_pickup, {
            color: '#06B6D4',
            weight: 4,
            dashArray: '8, 8',
            opacity: 0.85
          }).addTo(emergencyMap);
          const trfc1 = a.traffic_telemetry ? ` (Traffic Delay: +${a.traffic_telemetry.pickup_delay_min || 0}m)` : '';
          l1.bindTooltip(`<b>${a.callsign} [Leg 1: Pickup]</b>${trfc1}`, { sticky: true });
          emLayers.routes.push(l1);
        }

        // Leg 2: Render solid flashing red siren line ONLY after patient is loaded
        if (a.status === 'TRANSPORTING_HOSPITAL' && a.route_hosp && a.route_hosp.length > 0) {
          const l2 = L.polyline(a.route_hosp, {
            color: '#EF4444',
            weight: 5,
            opacity: 0.95
          }).addTo(emergencyMap);
          const trfc2 = a.traffic_telemetry ? ` (Traffic Delay: +${a.traffic_telemetry.hosp_delay_min || 0}m)` : '';
          l2.bindTooltip(`<b>${a.callsign} [Leg 2: Hospital Transport]</b>${trfc2}`, { sticky: true });
          emLayers.routes.push(l2);
        }
      });

      // Render Real-Time Traffic Corridor Zones on Leaflet Map
      trafficCorridorLayers.forEach(l => emergencyMap.removeLayer(l));
      trafficCorridorLayers = [];
      if (data.traffic_corridors && data.traffic_corridors.length > 0) {
        data.traffic_corridors.forEach(c => {
          const isGridlock = (c.status === 'GRIDLOCK');
          const isHeavy = (c.status === 'HEAVY');
          const isMod = (c.status === 'MODERATE');
          const color = isGridlock ? '#991B1B' : (isHeavy ? '#DC2626' : (isMod ? '#F59E0B' : '#10B981'));
          const circle = L.circle(c.coord, {
            radius: c.radius_km * 1000,
            color: color,
            weight: isGridlock || isHeavy ? 2 : 1,
            fillColor: color,
            fillOpacity: isGridlock ? 0.22 : (isHeavy ? 0.15 : 0.06),
            dashArray: isGridlock ? '4, 4' : null
          }).bindPopup(`
            <div style="font-family:sans-serif; min-width:210px;">
              <b style="font-size:13px; color:${color};">🚦 ${c.name}</b><br/>
              <b>Traffic Status:</b> ${c.status}<br/>
              <b>Current Speed:</b> ${c.current_speed_kmh} km/h (Limit: ${c.free_flow_kmh} km/h)<br/>
              <b>Jam Factor:</b> ${c.jam_factor} / 10<br/>
              <b>Delay Impact:</b> +${Math.round(c.base_delay_s/60)} min<br/>
              <span style="font-size:10px; color:#555; display:block; margin-top:3px;">${c.advisory}</span>
            </div>
          `).addTo(emergencyMap);
          trafficCorridorLayers.push(circle);
        });
      }

      if (bounds.length > 0) {
        emergencyMap.fitBounds(bounds, { padding: [45, 45], maxZoom: 14 });
      }
    }

    async function executePriorityDispatch() {
      const res = await fetch('/api/emergency/dispatch', { method: 'POST' });
      const data = await res.json();
      document.getElementById('em-event-log').innerText = `⚡ Triage Dispatch Completed: ${data.dispatched_count} incidents allocated via Dijkstra & MergeSort (Objective Z: ${data.objective_Z})`;
      loadEmergencyState();
    }

    async function stepSimulation(deltaSec) {
      const res = await fetch('/api/emergency/step', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ delta_sec: deltaSec })
      });
      const data = await res.json();
      if (data.events && data.events.length > 0) {
        document.getElementById('em-event-log').innerText = data.events[data.events.length - 1];
      }

      if (data.diversions && data.diversions.length > 0) {
        showDriverAlert(data.diversions[0]);
      }
      loadEmergencyState();
    }

    function toggleSimulationPlay() {
      isLiveSimPlaying = !isLiveSimPlaying;
      const btn = document.getElementById('btn-play-pause');
      const icon = document.getElementById('play-icon');
      const text = document.getElementById('play-text');

      if (isLiveSimPlaying) {
        icon.className = "fa-solid fa-pause text-xs";
        text.innerText = "Pause";
        btn.className = "px-2.5 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg font-bold text-xs flex items-center space-x-1 shadow";
        liveSimInterval = setInterval(() => stepSimulation(5), 1000); // 1 real sec = 5 sim secs
      } else {
        icon.className = "fa-solid fa-play text-xs";
        text.innerText = "Play Live";
        btn.className = "px-2.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold text-xs flex items-center space-x-1 shadow";
        clearInterval(liveSimInterval);
      }
    }

    async function resetSimulation() {
      if (isLiveSimPlaying) toggleSimulationPlay();
      await fetch('/api/emergency/scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario: 'urban' })
      });
      document.getElementById('em-event-log').innerText = "Simulation Clock reset to T+ 00:00:00.";
      loadEmergencyState();
    }

    async function triggerHospitalFull(hospId) {
      const res = await fetch('/api/emergency/hospital_full', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hospital_id: hospId })
      });
      const data = await res.json();
      if (data.diversions && data.diversions.length > 0) {
        showDriverAlert(data.diversions[0]);
      } else {
        alert(`🚨 ALERT: ${data.hospital_name} is at 100% capacity! No active ambulances are currently headed there.`);
      }
      loadEmergencyState();
    }

    async function dispatchSingleIncident(incId) {
      const res = await fetch('/api/emergency/dispatch_single', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ incident_id: incId })
      });
      const data = await res.json();
      if (data.error) {
        alert(data.error);
      } else {
        document.getElementById('em-event-log').innerText = `⚡ CAD Dispatch: ${data.ambulance.callsign} (${data.ambulance.type}) assigned to Incident #${data.incident.id} ➔ ${data.hospital.name}`;
      }
      loadEmergencyState();
    }

    function showDriverAlert(divItem) {
      document.getElementById('alert-driver-unit').innerText = `Mobile Data Terminal (MDT) — Unit: ${divItem.callsign} (${divItem.ambulance_type})`;
      document.getElementById('alert-old-hosp-name').innerText = divItem.old_hospital_name;
      document.getElementById('alert-new-hosp-name').innerText = divItem.new_hospital_name;
      document.getElementById('alert-new-hosp-meta').innerText = `Trauma Level ${divItem.new_trauma_level} · Avail ICU: ${divItem.new_avail_icu} · Avail Beds: ${divItem.new_avail_beds}`;
      document.getElementById('alert-new-eta').innerText = `+${divItem.new_eta_min} min`;
      document.getElementById('alert-patient-name').innerText = `Incident #${divItem.incident_id} (${divItem.patient_name})`;
      document.getElementById('alert-patient-condition').innerText = `${divItem.patient_condition} (${divItem.priority})`;
      document.getElementById('driver-alert-modal').classList.remove('hidden');

      // Emergency dispatch siren sound effect via Web Audio API
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.35);
        gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.35);
      } catch (e) {}
    }

    function acknowledgeDriverAlert() {
      document.getElementById('driver-alert-modal').classList.add('hidden');
      document.getElementById('em-event-log').innerText = `🚨 In-Transit Diversion Confirmed: Vehicle navigation re-routed to new facility with verified beds.`;
    }

    async function loadScenario(name) {
      await fetch('/api/emergency/scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario: name })
      });
      document.getElementById('em-event-log').innerText = `Scenario Switched to: ${name.toUpperCase()}`;
      loadEmergencyState();
    }

    function openCadIntakeModal() { document.getElementById('cad-intake-modal').classList.remove('hidden'); }
    function closeCadIntakeModal() { document.getElementById('cad-intake-modal').classList.add('hidden'); }

    async function submitCadIntake() {
      const name = document.getElementById('intake-name').value || "Emergency Call";
      const priority = document.getElementById('intake-priority').value;
      const desc = document.getElementById('intake-desc').value || "Critical Trauma";

      await fetch('/api/emergency/incident', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, priority: priority, description: desc })
      });
      closeCadIntakeModal();
      loadEmergencyState();
    }

    function openAlgoModal() { document.getElementById('algo-modal').classList.remove('hidden'); }
    function closeAlgoModal() { document.getElementById('algo-modal').classList.add('hidden'); }

    function filterAlgoTab(category) {
      const cards = document.querySelectorAll('.algo-card');
      cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });

      // Update button active state
      const tabBtns = document.querySelectorAll('#algo-tab-buttons button');
      tabBtns.forEach(btn => {
        btn.className = "px-2.5 py-1 rounded-md font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 transition";
      });
      const activeBtn = document.getElementById(`tab-btn-${category}`);
      if (activeBtn) {
        activeBtn.className = "px-2.5 py-1 rounded-md font-bold bg-indigo-600 text-white transition";
      }
    }

    function searchAlgoCards(query) {
      const q = (query || '').toLowerCase().trim();
      const cards = document.querySelectorAll('.algo-card');
      cards.forEach(card => {
        const text = (card.innerText + ' ' + card.getAttribute('data-keywords')).toLowerCase();
        if (!q || text.includes(q)) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    }

    function launchAlgoBenchmark(moduleCode) {
      closeAlgoModal();
      openCppModal();
      // Option 7 runs the core empirical benchmark suite in the C++ engine
      executeCppCommand("7", `Benchmark Module [${moduleCode}]`);
    }

    function openCppModal() { document.getElementById('cpp-modal').classList.remove('hidden'); }
    function closeCppModal() { document.getElementById('cpp-modal').classList.add('hidden'); }

    async function executeCppCommand(inputStr, label) {
      const term = document.getElementById('cpp-terminal-output');
      term.innerText = `[EXECUTING ${label || inputStr}]: Invoking C++17 binary...\n`;

      try {
        const res = await fetch('/api/cpp/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input: inputStr })
        });
        const data = await res.json();
        if (data.raw_output) {
          term.innerText = data.raw_output;
        } else {
          term.innerText = `[ERROR]: ${data.error || 'Execution failed'}\n`;
        }
      } catch (err) {
        term.innerText = `[SYSTEM ERROR]: ${err}\n`;
      }
      term.scrollTop = term.scrollHeight;
    }

    function runNativeScenario(num) {
      const labels = {
        1: "Scenario 1 (Dijkstra vs FW)",
        2: "Scenario 2 (Capacity Shock & Flow)",
        3: "Scenario 3 (Adversarial 1000 Nodes)"
      };
      // Map scenario numbers to actual C++ CLI menu options [4, 5, 6]
      const menuOpts = { 1: "4", 2: "5", 3: "6" };
      const opt = menuOpts[num] || String(num);
      executeCppCommand(opt, labels[num] || `Scenario ${num}`);
    }

    function runNativeBenchmarks() {
      executeCppCommand("7", "Core Algorithm Benchmarks Suite");
    }

    function sendCustomCppInput() {
      const inputEl = document.getElementById('cpp-custom-input');
      const val = inputEl.value.trim();
      if (!val) return;
      executeCppCommand(val, `Option [${val}]`);
      inputEl.value = '';
    }

    function clearCppTerminal() {
      document.getElementById('cpp-terminal-output').innerText = `[TERMINAL CLEARED]: Ready for input.\nType any menu option (1 to 9) below and press Enter.\n`;
    }

    function exportData(type) {
      window.open(`/api/emergency/export?type=${type}`, '_blank');
    }

    function toggleRealTimeMode() {
      isRealTimeClockActive = !isRealTimeClockActive;
      const btn = document.getElementById('btn-realtime-toggle');
      const text = document.getElementById('realtime-text');
      const label = document.getElementById('clock-label');
      if (isRealTimeClockActive) {
        btn.className = "px-2.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold text-xs flex items-center space-x-1.5 shadow";
        text.innerText = "Real-Time (ACTIVE)";
        label.innerText = "LIVE CAD WALL CLOCK";
        if (!realTimePollingInterval) {
          realTimePollingInterval = setInterval(loadEmergencyState, 2000);
        }
      } else {
        btn.className = "px-2.5 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/60 rounded-lg font-bold text-xs flex items-center space-x-1.5 shadow";
        text.innerText = "Live Clock";
        label.innerText = "CAD MISSION CLOCK";
        if (realTimePollingInterval) {
          clearInterval(realTimePollingInterval);
          realTimePollingInterval = null;
        }
      }
      loadEmergencyState();
    }

    function toggleTrafficPill() {
      const body = document.getElementById('traffic-pill-body');
      const chev = document.getElementById('traffic-pill-chevron');
      if (!body) return;
      if (body.classList.contains('hidden')) {
        body.classList.remove('hidden');
        if (chev) chev.className = 'fa-solid fa-chevron-up text-slate-400 text-[10px] ml-1';
      } else {
        body.classList.add('hidden');
        if (chev) chev.className = 'fa-solid fa-chevron-down text-slate-400 text-[10px] ml-1';
      }
    }

    function openTrafficModal() {
      fetch('/api/traffic/corridors')
        .then(res => res.json())
        .then(data => {
          renderTrafficModalContent(data);
          document.getElementById('traffic-modal').classList.remove('hidden');
        });
    }

    function closeTrafficModal() {
      document.getElementById('traffic-modal').classList.add('hidden');
    }

    function renderTrafficModalContent(data) {
      const tb = document.getElementById('traffic-corridors-table');
      if (!tb) return;
      tb.innerHTML = '';
      (data.corridors || []).forEach(c => {
        const isGridlock = (c.status === 'GRIDLOCK');
        const isHeavy = (c.status === 'HEAVY');
        const isMod = (c.status === 'MODERATE');
        const badgeColor = isGridlock ? 'bg-red-950 text-red-300 border-red-700' : (isHeavy ? 'bg-rose-950 text-rose-300 border-rose-800' : (isMod ? 'bg-amber-950 text-amber-300 border-amber-800' : 'bg-emerald-950 text-emerald-300 border-emerald-800'));
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td class="p-2.5">
            <span class="font-bold text-white">${c.name}</span>
            <span class="text-[10px] text-slate-400 block">${c.advisory}</span>
          </td>
          <td class="p-2.5 text-center font-bold text-white">${c.current_speed_kmh} km/h</td>
          <td class="p-2.5 text-center text-slate-400">${c.free_flow_kmh} km/h</td>
          <td class="p-2.5 text-center text-amber-400 font-bold">${c.jam_factor} / 10</td>
          <td class="p-2.5 text-center text-rose-400 font-bold">+${Math.round(c.base_delay_s/60)} min</td>
          <td class="p-2.5 text-center">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${badgeColor}">${c.status}</span>
          </td>
        `;
        tb.appendChild(tr);
      });

      const awareBadge = document.getElementById('badge-traffic-aware');
      if (awareBadge) {
        awareBadge.innerText = data.traffic_awareness ? "ACTIVE" : "OFF";
        awareBadge.className = data.traffic_awareness ? "bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded text-[10px] font-mono border border-indigo-700" : "bg-slate-800 text-slate-400 px-2 py-0.5 rounded text-[10px] font-mono border border-slate-700";
      }
    }

    async function setTrafficProfile(profile) {
      const res = await fetch('/api/traffic/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile: profile })
      });
      const data = await res.json();
      openTrafficModal();
      loadEmergencyState();
    }

    async function toggleTrafficAwareness() {
      const res = await fetch('/api/traffic/toggle_awareness', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();
      openTrafficModal();
      loadEmergencyState();
    }
  </script>
</body>
</html>
"""

class DualModeHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))

        elif parsed.path == "/presentation" or parsed.path == "/presentation.html":
            pres_path = "/Users/amrit/Documents/Emboolancè/Emboolance_SOTA_Presentation.html"
            if os.path.exists(pres_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(pres_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Presentation file not found")

        elif parsed.path == "/api/status":
            url = EMERGENCY_ENGINE.routing_url
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"routing_url": url}).encode("utf-8"))

        elif parsed.path == "/api/emergency/state":
            state = EMERGENCY_ENGINE.get_full_state()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(state).encode("utf-8"))

        elif parsed.path == "/api/cpp/scenario":
            num = int(params.get("num", [1])[0])
            res = EMERGENCY_ENGINE.run_cpp_ipc_scenario(num)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/cpp/benchmarks":
            res = EMERGENCY_ENGINE.run_cpp_ipc_benchmarks()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/traffic/corridors":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {
                "corridors": EMERGENCY_ENGINE.traffic_corridors,
                "profile": EMERGENCY_ENGINE.traffic_profile,
                "traffic_awareness": EMERGENCY_ENGINE.traffic_awareness,
                "source": "Google Real-Time Traffic Stream"
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif parsed.path == "/api/emergency/export":
            export_type = params.get("type", ["csv"])[0]
            if export_type == "csv":
                csv_data = "IncidentId,AmbulanceId,HospitalId,Priority,PickupTimeSec,HospitalTimeSec,WeightedCost,Notes\n"
                for h in EMERGENCY_ENGINE.dispatch_history:
                    csv_data += f"{h['incident_id']},{h['ambulance_id']},{h['hospital_id']},{h['priority']},{h['pickup_time_sec']},{h['hosp_time_sec']},{h['weighted_cost']},\"{h['notes']}\"\n"
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition", "attachment; filename=\"dispatch_history.csv\"")
                self.end_headers()
                self.wfile.write(csv_data.encode("utf-8"))
            else:
                metrics = {
                    "mission_clock_formatted": EMERGENCY_ENGINE.format_clock(EMERGENCY_ENGINE.clock_sec),
                    "simulation_clock_sec": EMERGENCY_ENGINE.clock_sec,
                    "cumulative_objective_Z": EMERGENCY_ENGINE.objective_Z,
                    "active_scenario": EMERGENCY_ENGINE.current_scenario,
                    "fleet_size": len(EMERGENCY_ENGINE.ambulances),
                    "hospitals_count": len(EMERGENCY_ENGINE.hospitals),
                    "total_incidents": len(EMERGENCY_ENGINE.incidents),
                    "dispatched_count": len(EMERGENCY_ENGINE.dispatch_history),
                    "student_name": "Amrit Prasad",
                    "sap_id": "590021684",
                    "batch": "B.Tech CSE AIML (2025-2029)",
                    "institution": "UPES School of Computer Science (SoCS), Dehradun",
                    "guide": "Sandeep Chand Kumain"
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Disposition", "attachment; filename=\"simulation_metrics.json\"")
                self.end_headers()
                self.wfile.write(json.dumps(metrics, indent=2).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8")) if content_length > 0 else {}

        if parsed.path == "/api/emergency/dispatch":
            res = EMERGENCY_ENGINE.execute_priority_dispatch()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/emergency/dispatch_single":
            inc_id = int(payload.get("incident_id", 101))
            res = EMERGENCY_ENGINE.dispatch_nearest_ambulance_to_incident(inc_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/emergency/step":
            delta_sec = float(payload.get("delta_sec", 30.0))
            res = EMERGENCY_ENGINE.step_simulation_clock(delta_sec)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/emergency/hospital_full":
            hosp_id = int(payload.get("hospital_id", 1))
            res = EMERGENCY_ENGINE.trigger_hospital_capacity_full(hosp_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/emergency/scenario":
            scen = payload.get("scenario", "urban")
            EMERGENCY_ENGINE.load_scenario(scen)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "scenario": scen}).encode("utf-8"))

        elif parsed.path == "/api/emergency/incident":
            name = payload.get("name", "Emergency Call")
            pri = payload.get("priority", "P1-CRITICAL")
            desc = payload.get("description", "Medical Emergency")
            inc = EMERGENCY_ENGINE.add_emergency_call(name, pri, desc)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(inc).encode("utf-8"))

        elif parsed.path == "/api/traffic/profile":
            prof = payload.get("profile", "normal")
            res = EMERGENCY_ENGINE.set_traffic_profile(prof)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/traffic/toggle_awareness":
            res = EMERGENCY_ENGINE.toggle_traffic_awareness()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        elif parsed.path == "/api/cpp/execute":
            raw_input = payload.get("input", "1")
            res = EMERGENCY_ENGINE.run_cpp_custom_input(raw_input)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))

        else:
            self.send_error(404, "Not Found")

def run_server(port=8080):
    server = ThreadedHTTPServer(("0.0.0.0", port), DualModeHandler)
    print(f"🚀 Mission-Critical EMS CAD Console (Multi-Threaded) running at: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
