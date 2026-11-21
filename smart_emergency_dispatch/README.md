# Smart Emergency Ambulance Routing & Hospital Allocation System
### College Internal Evaluation Specification (PROJ-01) — 50–60% Milestone Delivery
**Course:** Advanced Data Structures & Algorithms  
**Domain:** Healthcare Operations & Emergency Logistics  
**Target Engine:** C11 / C++17 Compliance  
**Adherence:** Strictly Zero-STL for Core Logic & Containers  

---

## Overview

This project implements an industry-grade healthcare logistics command and ambulance dispatch system built in **C++17**. The system models urban road networks, ambulance fleets, emergency incident calls, and regional hospital emergency rooms.

When emergency calls arrive, the system calculates optimal dispatch decisions that minimize patient transit times and clinical delay penalties while strictly enforcing real-time operational constraints (ALS vehicle requirements for critical cases, hospital bed/ICU capacities, and road blockages).

### Core Optimization Objective
$$\text{Minimize } Z = \sum_{i \in I} \sum_{j \in A} \sum_{k \in H} x_{ijk} \cdot \left[ w_{pri}(P_i) \cdot \left( d(\text{loc}(j), \text{loc}(i)) + d(\text{loc}(i), \text{loc}(k)) \right) \right]$$
Subject to:
1. $\sum_{j \in A} \sum_{k \in H} x_{ijk} = 1 \quad \forall i \in I$ (Every incident assigned exactly once)
2. $\sum_{i \in I} \sum_{j \in A} x_{ijk} \leq \text{Capacity}(H_k) \quad \forall k \in H$ (Hospital capacity ceiling)
3. $x_{ijk} \in \{0, 1\} \quad \forall i, j, k$

---

## 50–60% Midterm Completion Breakdown

| System Layer | Completion | Implemented Capabilities |
| :--- | :---: | :--- |
| **Zero-STL Core Library** | **100%** | Custom dynamic array (`CustomVector<T>`), binary min-heap (`CustomMinHeap<T>`), Union-Find (`DisjointSet`). |
| **Syllabus Algorithms** | **~55-60%** | MergeSort, QuickSort, Iter/Rec BinarySearch, MaxSubarray, FastPowering, Celebrity Hub, Dijkstra, Prim MST, Kruskal MST, Activity Selection, 0/1 Knapsack, Floyd-Warshall, Bellman-Ford, LCS, N-Queens, Subset Sum, Least-Cost B&B, Edmonds-Karp Flow, Bipartite Matching, KMP, Rabin-Karp, CRT. |
| **Road Network & Graph** | **100%** | Directed weighted graph with dynamic weight updates, road blockages, coordinates, and CSV importer. |
| **Domain Logistics** | **100%** | Typed records for Ambulances (ALS/BLS, loadouts), Hospitals (beds, ICU, trauma levels), and Incidents (P1/P2/P3). |
| **Dispatch Optimizer** | **100%** | Dijkstra greedy optimization, MergeSort priority queue dispatch, Bipartite batch dispatch, and Mass-casualty flow. |
| **Demonstration Scenarios** | **100%** | Scenario 1 (Normal Operations), Scenario 2 (Capacity Shock), Scenario 3 (Adversarial Stress). |
| **Interactive CLI** | **100%** | ASCII live dashboard, vehicle tracking, simulation clock stepping, and CSV/JSON export. |
| **Tests & Benchmarks** | **100%** | 9-suite unit test engine (100% pass) and empirical Big-O runtime microbenchmark engine. |
| **Phase 2 Advanced Stubs** | **Roadmap** | Clean interfaces, mathematical recurrence documentation, and stubs for Weeks 5–8 algorithms. |

---

## Project Structure

```
smart_emergency_dispatch/
├── Makefile                          # Build system for Clang/GCC
├── CMakeLists.txt                    # Standard CMake configuration
├── README.md                         # Project documentation
├── .gitignore                        # Git ignore rules
├── docs/
│   └── MIDTERM_ANALYTICAL_REPORT.md  # Comprehensive analytical report & proofs
├── include/
│   ├── core/                         # Zero-STL data structures
│   │   ├── CustomVector.hpp          # Dynamic array with 2x geometric resizing
│   │   ├── CustomMinHeap.hpp         # Binary min-heap priority queue
│   │   ├── DisjointSet.hpp           # DSU with path compression & union-by-rank
│   │   └── Types.hpp                 # Enums, Edge, NodeCost, GeoPoint
│   ├── algorithms/                   # Syllabus algorithm headers
│   │   ├── SortingRetrieval.hpp      # MergeSort, QuickSort, BinarySearch
│   │   ├── DivideConquer.hpp         # MaxSubarray, FastPower, Celebrity, Strassen
│   │   ├── Greedy.hpp                # Dijkstra, Prim, Kruskal, ActivitySelect, Huffman
│   │   ├── DynamicProgramming.hpp    # 0/1 Knapsack, Floyd-Warshall, Bellman, LCS, TSP
│   │   ├── BacktrackingBB.hpp        # N-Queens, SubsetSum, Branch & Bound
│   │   ├── NetworkFlows.hpp          # Ford-Fulkerson, Max Bipartite Matching
│   │   └── StringsNumberTheory.hpp   # KMP, Rabin-Karp, CRT, Finite Automaton
│   ├── domain/                       # Core domain entities
│   │   ├── RoadNetwork.hpp           # Directed weighted urban network
│   │   ├── Ambulance.hpp             # Fleet vehicle entity & equipment
│   │   ├── Hospital.hpp              # Regional hospital entity & capacities
│   │   ├── Incident.hpp              # Emergency call & triage priority
│   │   └── Dispatcher.hpp            # Multi-strategy dispatch optimizer
│   ├── simulation/
│   │   ├── Simulator.hpp             # Simulation clock & ASCII dashboard
│   │   └── Scenarios.hpp             # Mandatory demonstration scenarios
│   └── benchmark/
│       └── Benchmark.hpp             # Empirical Big-O benchmark suite
├── src/                              # Implementation source files
│   ├── algorithms/                   # Algorithm implementations
│   ├── domain/                       # Domain logic implementations
│   ├── simulation/                   # Simulator & Scenario implementations
│   ├── benchmark/                    # Benchmark suite implementation
│   └── main.cpp                      # Interactive CLI entrypoint
├── tests/
│   ├── test_algorithms.cpp           # Unit tests for custom algorithms
│   └── test_dispatch.cpp             # Unit tests for domain dispatch logic
└── data/                             # Standard urban network datasets (CSV)
    ├── nodes.csv                     # Intersection coordinates & types
    ├── edges.csv                     # Road corridor travel times & capacities
    ├── hospitals.csv                 # Hospital bed & ICU capacities
    ├── ambulances.csv                # Ambulance fleet base allocations
    └── incidents.csv                 # Emergency call incident records
```

---

## Quickstart: Build & Run

### 1. Build the Complete Suite
```bash
make clean && make -j4
```
*Compiles cleanly with `-std=c++17 -Wall -Wextra -pedantic -O3` without warnings.*

### 2. Run Automated Unit Tests
```bash
make test
```
*Executes all 9 unit test suites across core data structures and algorithms.*

### 3. Run Empirical Algorithm Benchmarks
```bash
make bench
```
*Measures runtime against theoretical Big-O asymptotic bounds (Sorting, Heaps, DP, Graphs, String Search).*

### 4. Run Mandatory Demonstration Scenarios
```bash
make scenario1    # Scenario 1: Normal Operations (Dijkstra vs Floyd-Warshall)
make scenario2    # Scenario 2: Capacity Shock (Ford-Fulkerson vs Bipartite Matching)
make scenario3    # Scenario 3: Adversarial Stress & Scalability (1,000 nodes)
```

### 5. Launch the Interactive Dispatcher CLI
```bash
make run
# or
./bin/dispatch_sim
```

---

## Interactive CLI Features

When running `./bin/dispatch_sim`, an interactive menu is displayed:
- **`[1] Display Live Dashboard:`** Shows vehicle positions, status (`IDLE`, `EN_ROUTE`, `TRANSPORTING`, `RETURNING`), hospital bed/ICU occupancy rates, and pending incidents.
- **`[2] Execute Priority Queue Dispatch:`** Sorts pending incidents by triage priority (`P1 > P2 > P3`) using custom **MergeSort** and routes each using **Dijkstra's** greedy algorithm.
- **`[3] Step Simulation Clock:`** Advances simulation time forward by a specified delta, moving ambulances toward destinations and updating patient admissions.
- **`[4-6] Run Scenarios 1, 2, 3:`** Triggers the mandatory demonstration experiments.
- **`[7] Run Empirical Benchmarks:`** Executes microbenchmarks for all syllabus algorithmic paradigms.
- **`[8] Export Data:`** Writes `dispatch_history.csv` and `simulation_metrics.json`.
- **`[9] Display Syllabus Audit:`** Shows the exact module-by-module syllabus completion matrix.

---

## Zero-STL Verification Note

All core algorithmic logic avoids standard containers (`std::vector`, `std::priority_queue`, `std::map`, `std::set`, `<algorithm>`), implementing custom dynamic arrays and heaps. Standard headers are used strictly for CLI input/output (`<iostream>`, `<iomanip>`), file streams (`<fstream>`), and precision timing (`<chrono>`).
