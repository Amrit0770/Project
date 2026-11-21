# Emboolancè: Smart Emergency Ambulance Routing & Hospital Allocation System

**Academic Researcher:** Amrit Prasad (SAP ID: `590021684`)  
**Department:** B.Tech CSE AIML (2025–2029), School of Computer Science (SoCS), UPES Dehradun  
**Subject Teacher / Guide:** Sandeep Chand Kumain  
**Institution:** University of Petroleum and Energy Studies (UPES), Dehradun  

---

## 1. Unified Directory Organization (`Emboolancè/`)

All project source files, algorithms, CAD consoles, documentation, and data packages are organized inside this unified folder:

```text
Emboolancè/
├── smart_emergency_dispatch/         # 100% Native Zero-STL C++17 Core Engine
│   ├── include/                     # Zero-STL custom structures & algorithm headers
│   │   ├── algorithms/              # 7 DSA Module headers (Dijkstra, Knapsack, KMP, etc.)
│   │   ├── core/                    # Custom memory management (CustomVector, MinHeap, etc.)
│   │   ├── domain/                  # Emergency domain models (Ambulance, Hospital, RoadNetwork)
│   │   └── simulation/              # Operational simulation, scenarios, and clock stepping
│   ├── src/                         # Complete C++ implementations (100% Zero-STL compliant)
│   ├── bin/dispatch_sim             # Compiled C++17 binary
│   ├── Makefile & CMakeLists.txt     # Build systems
│   └── tests/                       # C++ unit tests & benchmark suite
├── route_optimizer/                 # Real-Time Operational CAD Web Interface & IPC Bridge
│   ├── app.py                       # HTTP server, WebSocket/REST API, dynamic traffic engine
│   ├── emergency_engine.py          # Python CAD controller & C++ Subprocess IPC bridge
│   ├── vrp_optimizer.py             # Google OR-Tools CVRPTW fleet logistics solver
│   ├── osrm_data/                   # Local OSRM engine map data
│   └── docker-compose.yml           # Local OSRM container configuration
├── notebooklm_sources/              # 6 Publication-Ready Markdown Sources for NotebookLM
│   ├── 01_Academic_Poster_Architecture_and_Theory.md
│   ├── 02_Zero_STL_Cpp17_Core_and_Algorithms.md
│   ├── 03_Cpp_Domain_Simulation_and_Benchmarks.md
│   ├── 04_Real_Time_EMS_CAD_Engine_and_Traffic_API.md
│   ├── 05_Fleet_VRP_OSRP_Docker_and_Tests.md
│   └── Smart_Emergency_Dispatch_Complete_Codebase.md
├── dispatch_history.csv             # Exported real-time dispatch log records
├── simulation_metrics.json          # Exported simulation performance telemetry
└── smart_emergency_dispatch.zip     # Compressed archive of original C++ package
```

---

## 2. Technology Stack Clarification

* **Is everything in C++?**
  * **100% of all algorithms, custom data structures, graph solvers, and optimization logic are written in pure C++17 without using the Standard Template Library (Zero-STL).** `std::vector`, `std::map`, `std::queue`, and `std::priority_queue` are completely excluded and replaced with Amrit Prasad's custom memory-managed templates (`CustomVector`, `MinHeap`, pointer-linked adjacency graphs).
  * **The Web CAD Console (`route_optimizer/`)** is the operational mission-control UI (Leaflet.js map, Google Live Traffic congestion overlay, MDT in-transit diversion alerts). It connects directly to the compiled C++17 binary (`dispatch_sim`) through real-time Subprocess IPC, executing scenarios and benchmarks in milliseconds.

---

## 3. How to Run

### A. Run Native Zero-STL C++17 Engine (Terminal Mode)
```bash
cd /Users/amrit/Documents/Emboolancè/smart_emergency_dispatch
make
./bin/dispatch_sim
```

### B. Run Full Mission-Critical Web CAD Console
```bash
cd /Users/amrit/Documents/Emboolancè/route_optimizer
./.venv/bin/python3 app.py 8080
```
Open your browser to: **`http://localhost:8080`**

---

## 4. Academic Compliance
This project strictly fulfills all syllabus milestones for **Advanced Data Structures & Algorithms (50–60% Delivery Stage)** under the mentorship of Sandeep Chand Kumain at UPES Dehradun.
