#!/usr/bin/env python3
"""
Packages the entire Smart Emergency Dispatch & Route Optimizer codebase into
structured Markdown sources specifically formatted for Google NotebookLM ingestion.
Outputs to:
  - /Users/amrit/Documents/notebooklm_sources/
  - /Users/amrit/.gemini/antigravity/brain/21d083f1-1391-4bc4-9c6b-af882ba99045/browser_sandbox/uploads/
"""

import os
import shutil

DOCS_DIR = "/Users/amrit/Documents"
CPP_DIR = os.path.join(DOCS_DIR, "smart_emergency_dispatch")
PY_DIR = os.path.join(DOCS_DIR, "route_optimizer")
OUT_DIR = os.path.join(DOCS_DIR, "notebooklm_sources")
UPLOADS_DIR = "/Users/amrit/.gemini/antigravity/brain/21d083f1-1391-4bc4-9c6b-af882ba99045/browser_sandbox/uploads"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

def read_file_safe(path):
    if not os.path.exists(path):
        return f"[File not found: {path}]\n"
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"[Error reading {path}: {e}]\n"

# ==============================================================================
# SOURCE 1: Academic Poster, Architecture & Analytical Report
# ==============================================================================
print("Generating Source 1: Academic Poster, Architecture & Theory...")
s1 = """# Source 1: UPES Academic Project Specifications, Architecture & Theory
**Project Title:** Smart Emergency Ambulance Routing & Hospital Allocation: Minimizing Response Time, Saving Lives  
**Institution:** School of Computer Science (SoCS), University of Petroleum and Energy Studies (UPES), Dehradun  
**Student Researcher:** Amrit Prasad (SAP ID: 590021684, Batch: B.Tech CSE AIML 2025–2029)  
**Subject Teacher & Mentor:** Sandeep Chand Kumain  
**Technology Stack:** C++17 (Strict Zero-STL Custom Memory Management), Python 3.9, Leaflet.js, OSRM (Open Source Routing Machine), Google OR-Tools, Docker.

---

## 1. Project Abstract & Poster Formulation
In critical medical emergencies (e.g., Acute Myocardial Infarction, Severe Polytrauma, Hypoxia), every second saved directly determines patient survival ('The Golden Hour'). Traditional dispatching systems suffer from static fleet allocation, disregard for hospital bed capacity, inability to account for dynamic road traffic, and total lack of in-transit diversion when emergency departments saturate.

This project delivers an end-to-end, mathematically rigorous Emergency Medical Services Computer-Aided Dispatch (EMS CAD) platform featuring:
1. **Clinical Triage Queueing:** Priority 1 Critical (weight = 4.0, requires ALS + ICU), Priority 2 Urgent (weight = 2.0, BLS/ALS), Priority 3 Delayed (weight = 1.0, BLS).
2. **Shortest Path Optimization:** Dijkstra's Algorithm with custom binary min-heap ($O((V+E)\log V)$) vs. Floyd-Warshall ($O(V^3)$).
3. **Advanced Lifesaving Ambulance Fleet Matching:** Advanced Life Support (ALS) vs. Basic Life Support (BLS) matching patient clinical urgency.
4. **Dynamic Hospital Bed Ceiling Allocation:** Multi-criteria ER and ICU bed reservation avoiding emergency department overcrowding.
5. **In-Transit Hospital Saturation Diversion:** Real-time Mobile Data Terminal (MDT) alerts and dynamic Dijkstra re-routing from the vehicle's exact live street coordinates when an assigned hospital hits 100% capacity mid-route.
6. **Real-Time Map Traffic Ingestion:** Google Maps real-time traffic flow overlay and corridor congestion sensing (Ballupur Chowk, Clock Tower, Saharanpur Rd, Rajpur Rd, Haridwar Bypass) dynamically penalizing transit durations.

---

## 2. Mathematical Formulations

### 2.1 Cumulative Objective Function
$$\\min Z = \\sum_{i \\in \\text{Incidents}} W_{\\text{pri}}(i) \\cdot \\Big[ d_{\\text{eff}}(\\text{amb}_i, \\text{inc}_i) + d_{\\text{eff}}(\\text{inc}_i, \\text{hosp}_i) \\Big]$$
Where:
- $W_{\\text{pri}}(P1) = 4.0, \\quad W_{\\text{pri}}(P2) = 2.0, \\quad W_{\\text{pri}}(P3) = 1.0$
- Baseline Academic Evaluation Score: $Z = 5347.0000$

### 2.2 Dynamic Traffic-Aware Travel Time
$$d_{\\text{eff}}(u, v) = \\frac{\\text{Dist}(u, v)}{v_{\\text{nominal}}(u, v) \\cdot (1 - \\text{JamFactor}(u, v))} + \\sum_{c \\in \\text{Corridors}} \\Delta t_{\\text{delay}}(c)$$

### 2.3 Capacity Ceilings & Edmonds-Karp Residual Flow
$$\\sum_{i: \\text{hosp}_i = H} \\text{BedsAllocated}(i) \\le \\text{Capacity}(H)$$
$$\\sum_{i: \\text{hosp}_i = H, \\text{requires\\_icu}(i)} \\text{ICUAllocated}(i) \\le \\text{ICUCapacity}(H)$$

---

## 3. Midterm Analytical Report
""" + read_file_safe(os.path.join(CPP_DIR, "docs", "MIDTERM_ANALYTICAL_REPORT.md"))

with open(os.path.join(OUT_DIR, "01_Academic_Poster_Architecture_and_Theory.md"), "w", encoding="utf-8") as f:
    f.write(s1)

# ==============================================================================
# SOURCE 2: Zero-STL C++17 Core & Algorithms
# ==============================================================================
print("Generating Source 2: Zero-STL C++17 Core & Algorithms...")
s2 = """# Source 2: Strict Zero-STL C++17 Core Data Structures & Algorithms
**Project:** Smart Emergency Ambulance Routing & Hospital Allocation (Amrit Prasad, 590021684)  
**Standard:** C++17 compiled with `-std=c++17 -Wall -Wextra -O3`.  
**Zero-STL Constraint:** Absolutely NO `<vector>`, `<queue>`, `<list>`, `<map>`, `<string>`, or `<algorithm>`. All memory management is implemented via custom fixed memory arenas, raw pointers, custom resizeable vectors, and binary min-heaps.

---

## 1. Core Data Structures & Types
"""
for h in ["Types.hpp", "CustomVector.hpp", "CustomMinHeap.hpp", "DisjointSet.hpp"]:
    p = os.path.join(CPP_DIR, "include", "core", h)
    s2 += f"\n### File: `include/core/{h}`\n```cpp\n{read_file_safe(p)}\n```\n"

s2 += "\n---\n## 2. Algorithmic Modules (Headers & Implementations)\n"
algo_pairs = [
    ("SortingRetrieval.hpp", None),
    ("Greedy.hpp", "Greedy.cpp"),
    ("DynamicProgramming.hpp", "DynamicProgramming.cpp"),
    ("NetworkFlows.hpp", "NetworkFlows.cpp"),
    ("DivideConquer.hpp", "DivideConquer.cpp"),
    ("StringsNumberTheory.hpp", "StringsNumberTheory.cpp"),
    ("BacktrackingBB.hpp", "BacktrackingBB.cpp")
]

for h_name, cpp_name in algo_pairs:
    hp = os.path.join(CPP_DIR, "include", "algorithms", h_name)
    s2 += f"\n### Header: `include/algorithms/{h_name}`\n```cpp\n{read_file_safe(hp)}\n```\n"
    if cpp_name:
        cp = os.path.join(CPP_DIR, "src", "algorithms", cpp_name)
        s2 += f"\n### Source: `src/algorithms/{cpp_name}`\n```cpp\n{read_file_safe(cp)}\n```\n"

with open(os.path.join(OUT_DIR, "02_Zero_STL_Cpp17_Core_and_Algorithms.md"), "w", encoding="utf-8") as f:
    f.write(s2)

# ==============================================================================
# SOURCE 3: C++ Domain Models, Simulation & Benchmarks
# ==============================================================================
print("Generating Source 3: C++ Domain Models, Simulation & Benchmarks...")
s3 = """# Source 3: C++ Domain Models, Simulation Engine & Benchmark Suite
**Project:** Smart Emergency Ambulance Routing & Hospital Allocation (Amrit Prasad, 590021684)  
This source covers the domain entities (Ambulance, Hospital, Incident, RoadNetwork, Dispatcher), the simulation scenarios, the comprehensive benchmark suite, and unit test suites.

---

## 1. Domain Entities
"""
domain_files = [
    ("Ambulance.hpp", None),
    ("Hospital.hpp", None),
    ("Incident.hpp", None),
    ("RoadNetwork.hpp", "RoadNetwork.cpp"),
    ("Dispatcher.hpp", "Dispatcher.cpp")
]
for h_name, cpp_name in domain_files:
    hp = os.path.join(CPP_DIR, "include", "domain", h_name)
    s3 += f"\n### Header: `include/domain/{h_name}`\n```cpp\n{read_file_safe(hp)}\n```\n"
    if cpp_name:
        cp = os.path.join(CPP_DIR, "src", "domain", cpp_name)
        s3 += f"\n### Source: `src/domain/{cpp_name}`\n```cpp\n{read_file_safe(cp)}\n```\n"

s3 += "\n---\n## 2. Simulation Engine & Scenarios\n"
sim_files = [
    ("Simulator.hpp", "Simulator.cpp"),
    ("Scenarios.hpp", "Scenarios.cpp")
]
for h_name, cpp_name in sim_files:
    hp = os.path.join(CPP_DIR, "include", "simulation", h_name)
    s3 += f"\n### Header: `include/simulation/{h_name}`\n```cpp\n{read_file_safe(hp)}\n```\n"
    if cpp_name:
        cp = os.path.join(CPP_DIR, "src", "simulation", cpp_name)
        s3 += f"\n### Source: `src/simulation/{cpp_name}`\n```cpp\n{read_file_safe(cp)}\n```\n"

s3 += "\n---\n## 3. Empirical Benchmark Suite\n"
s3 += f"\n### Header: `include/benchmark/Benchmark.hpp`\n```cpp\n{read_file_safe(os.path.join(CPP_DIR, 'include', 'benchmark', 'Benchmark.hpp'))}\n```\n"
s3 += f"\n### Source: `src/benchmark/Benchmark.cpp`\n```cpp\n{read_file_safe(os.path.join(CPP_DIR, 'src', 'benchmark', 'Benchmark.cpp'))}\n```\n"

s3 += "\n---\n## 4. Main Entrypoint, Makefile & Tests\n"
s3 += f"\n### Main CLI: `src/main.cpp`\n```cpp\n{read_file_safe(os.path.join(CPP_DIR, 'src', 'main.cpp'))}\n```\n"
s3 += f"\n### Build System: `Makefile`\n```makefile\n{read_file_safe(os.path.join(CPP_DIR, 'Makefile'))}\n```\n"
s3 += f"\n### Unit Test: `tests/test_algorithms.cpp`\n```cpp\n{read_file_safe(os.path.join(CPP_DIR, 'tests', 'test_algorithms.cpp'))}\n```\n"
s3 += f"\n### Unit Test: `tests/test_dispatch.cpp`\n```cpp\n{read_file_safe(os.path.join(CPP_DIR, 'tests', 'test_dispatch.cpp'))}\n```\n"

with open(os.path.join(OUT_DIR, "03_Cpp_Domain_Simulation_and_Benchmarks.md"), "w", encoding="utf-8") as f:
    f.write(s3)

# ==============================================================================
# SOURCE 4: Real-Time EMS CAD Engine & Traffic API
# ==============================================================================
print("Generating Source 4: Real-Time EMS CAD Engine & Traffic API...")
s4 = """# Source 4: Real-Time EMS CAD Engine & Dynamic Traffic Architecture
**Project:** Smart Emergency Ambulance Routing & Hospital Allocation (Amrit Prasad, 590021684)  
This source covers the real-time Python/Web architecture:
- `emergency_engine.py`: Live corridor traffic sensing, Google Traffic tile integration, In-transit GPS diversion state machine, native Zero-STL C++ IPC bridge, and Mission Elapsed Time / Real wall-clock formatting.
- `app.py`: High-contrast Dark EMS CAD command center, Leaflet.js Google Live Traffic map layer control, Mobile Data Terminal (MDT) in-transit audio siren alert modal, and live REST dispatch endpoints.

---

## 1. Real-Time Emergency Engine: `emergency_engine.py`
```python
""" + read_file_safe(os.path.join(PY_DIR, "emergency_engine.py")) + """
```

---

## 2. EMS CAD Web Server & Interactive Dashboard: `app.py`
```python
""" + read_file_safe(os.path.join(PY_DIR, "app.py")) + """
```
"""

with open(os.path.join(OUT_DIR, "04_Real_Time_EMS_CAD_Engine_and_Traffic_API.md"), "w", encoding="utf-8") as f:
    f.write(s4)

# ==============================================================================
# SOURCE 5: Fleet CVRPTW Optimizer & OSRM Stack
# ==============================================================================
print("Generating Source 5: Fleet CVRPTW Optimizer & OSRM Stack...")
s5 = """# Source 5: Commercial Fleet CVRPTW Optimizer & OSRM Docker Infrastructure
**Project:** Smart Emergency Ambulance Routing & Hospital Allocation (Amrit Prasad, 590021684)  
This source provides the commercial fleet logistics module:
- Capacitated Vehicle Routing Problem with Time Windows (CVRPTW) using Google OR-Tools.
- Geocaching and distance matrix generation using local Docker OSRM.
- Folium HTML interactive route map generator.
- Docker and OSRM container scripts.

---

## 1. Fleet Optimizer: `vrp_optimizer.py`
```python
""" + read_file_safe(os.path.join(PY_DIR, "vrp_optimizer.py")) + """
```

---

## 2. Docker & OSRM Setup: `docker-compose.yml` & `setup_osrm.sh`
### `docker-compose.yml`
```yaml
""" + read_file_safe(os.path.join(PY_DIR, "docker-compose.yml")) + """
```

### `setup_osrm.sh`
```bash
""" + read_file_safe(os.path.join(PY_DIR, "setup_osrm.sh")) + """
```

### `requirements.txt`
```text
""" + read_file_safe(os.path.join(PY_DIR, "requirements.txt")) + """
```
"""

with open(os.path.join(OUT_DIR, "05_Fleet_VRP_OSRM_Docker_and_Tests.md"), "w", encoding="utf-8") as f:
    f.write(s5)

# ==============================================================================
# SOURCE 6: Complete Consolidated Master Knowledge Base
# ==============================================================================
print("Generating Source 6: Complete Consolidated Master Knowledge Base...")
s_master = f"""# Smart Emergency Ambulance Routing & Hospital Allocation: Complete System Knowledge Base
**Institution:** School of Computer Science (SoCS), UPES Dehradun  
**Student Researcher:** Amrit Prasad (SAP ID: 590021684, Batch: B.Tech CSE AIML 2025–2029)  
**Subject Teacher & Guide:** Sandeep Chand Kumain  
**Date:** November 2026  

================================================================================
TABLE OF CONTENTS
================================================================================
1. Academic Poster Formulation, Mathematical Rigor & Architecture
2. Strict Zero-STL C++17 Core Data Structures (CustomVector, CustomMinHeap, DisjointSet)
3. Algorithmic Modules (Dijkstra, Floyd-Warshall, MergeSort, Knapsack, Edmonds-Karp, D&C, Strings)
4. Domain Models, Simulation Engine & Scenarios (Urban, Capacity Shock, UPES Dehradun)
5. Zero-STL Empirical Benchmarking Suite & Unit Tests
6. Real-Time EMS CAD Engine & Google Maps Live Traffic Stream
7. In-Transit Mobile Data Terminal (MDT) Dynamic Diversion State Machine
8. Commercial Fleet CVRPTW Optimizer & Local OSRM Docker Infrastructure
================================================================================

{s1}

================================================================================
MODULE 2: STRICT ZERO-STL C++17 CORE & ALGORITHMS
================================================================================
{s2}

================================================================================
MODULE 3: DOMAIN MODELS, SIMULATION & BENCHMARKS
================================================================================
{s3}

================================================================================
MODULE 4: REAL-TIME EMS CAD & DYNAMIC TRAFFIC ENGINE
================================================================================
{s4}

================================================================================
MODULE 5: FLEET LOGISTICS CVRPTW & OSRM DOCKER
================================================================================
{s5}
"""

with open(os.path.join(OUT_DIR, "Smart_Emergency_Dispatch_Complete_Codebase.md"), "w", encoding="utf-8") as f:
    f.write(s_master)

# Also copy all files to uploads dir for browser subagent
for fn in os.listdir(OUT_DIR):
    src_f = os.path.join(OUT_DIR, fn)
    dst_f = os.path.join(UPLOADS_DIR, fn)
    shutil.copy2(src_f, dst_f)

print(f"Packaging complete! Successfully generated 6 sources in:\n- {OUT_DIR}\n- {UPLOADS_DIR}")
