#include "simulation/Simulator.hpp"
#include "simulation/Scenarios.hpp"
#include "benchmark/Benchmark.hpp"
#include <iostream>
#include <string>

void printHeader() {
    std::cout << "========================================================================================\n";
    std::cout << "          SMART EMERGENCY AMBULANCE ROUTING & HOSPITAL ALLOCATION SYSTEM                \n";
    std::cout << "            Course: Advanced Data Structures & Algorithms | Engine: C++17               \n";
    std::cout << "              Evaluation Stage: 50-60% Architecture & Core Engine Delivery              \n";
    std::cout << "========================================================================================\n";
}

void printMenu() {
    std::cout << "\n-------------------------------- MAIN COMMAND MENU ------------------------------------\n";
    std::cout << "  [1] Display Live Dispatcher Dashboard & Fleet Status\n";
    std::cout << "  [2] Execute Priority Queue Incident Dispatch (MergeSort + Dijkstra Optimization)\n";
    std::cout << "  [3] Step Simulation Clock Forward (+30s / +60s / +120s)\n";
    std::cout << "  [4] Run Scenario 1: Normal Operations (Dijkstra vs. Floyd-Warshall Latency)\n";
    std::cout << "  [5] Run Scenario 2: Capacity Shock (Ford-Fulkerson vs. Bipartite Matching)\n";
    std::cout << "  [6] Run Scenario 3: Adversarial Stress & Scaling Benchmark\n";
    std::cout << "  [7] Run Core Algorithm Empirical Benchmark Suite\n";
    std::cout << "  [8] Export Simulation History (CSV) & Metrics (JSON)\n";
    std::cout << "  [9] Display Syllabus Algorithm Implementation Audit (50-60% Milestone)\n";
    std::cout << "  [0] Exit Dispatch System\n";
    std::cout << "----------------------------------------------------------------------------------------\n";
    std::cout << "Enter command option [0-9]: ";
}

void printSyllabusAudit() {
    std::cout << "\n========================================================================================\n";
    std::cout << "               SYLLABUS ALGORITHM IMPLEMENTATION STATUS AUDIT (50-60%)                  \n";
    std::cout << "========================================================================================\n";
    std::cout << std::left
              << "| Module               | Mandatory Algorithms                        | Status      | Domain Mapping\n";
    std::cout << "|----------------------|---------------------------------------------|-------------|---------------------------------\n";
    std::cout << "| 1. Sorting & Retr.   | MergeSort, QuickSort, Iter/Rec BinarySearch | COMPLETED   | Incident priority & ID lookups\n";
    std::cout << "| 2. Divide & Conquer  | Max Subarray, Fast Powering, Celebrity Prob | COMPLETED   | Peak congestion, hazard decay\n";
    std::cout << "|                      | Strassen Matrix Multiplication              | Scaffolding | High-dim spatial risk matrix\n";
    std::cout << "| 3. Greedy Strategy   | Dijkstra, Prim MST, Kruskal, ActivitySelect | COMPLETED   | Shortest routing, crew shift\n";
    std::cout << "|                      | Interval Partitioning, Huffman Coding       | Scaffolding | Staging & mesh compression\n";
    std::cout << "| 4. Dynamic Prog.     | 0/1 Knapsack, Floyd-Warshall, Bellman, LCS  | COMPLETED   | Payload packing, all-pairs dist\n";
    std::cout << "|                      | Matrix Chain, Optimal BST, TSP Held-Karp    | Scaffolding | Multi-hop disaster tour\n";
    std::cout << "| 5. Backtracking & BB | N-Queens, Subset Sum, Least-Cost B&B        | COMPLETED   | Resource checks, exact matching\n";
    std::cout << "| 6. Network Flows     | Ford-Fulkerson (Edmonds-Karp), Bipartite    | COMPLETED   | Mass-casualty flow & 2-sided match\n";
    std::cout << "| 7. Strings & Num.    | KMP, Rabin-Karp, CRT                        | COMPLETED   | 911 dispatch log search & sync\n";
    std::cout << "|                      | Finite Automaton Matcher                    | Scaffolding | DFA text parser\n";
    std::cout << "========================================================================================\n";
    std::cout << "Overall Implementation Completion: ~55-60% (Full operational core with Week 5-8 roadmaps)\n";
    std::cout << "Adherence to zero-STL constraint: STRICTLY MAINTAINED across all core structures & logic.\n";
}

int main(int argc, char* argv[]) {
    // Check if non-interactive argument passed
    if (argc > 1) {
        std::string arg = argv[1];
        if (arg == "--scenario1") {
            Simulation::Scenarios::executeScenario1NormalOperations();
            return 0;
        } else if (arg == "--scenario2") {
            Simulation::Scenarios::executeScenario2CapacityShock();
            return 0;
        } else if (arg == "--scenario3") {
            Simulation::Scenarios::executeScenario3AdversarialStress(1000);
            return 0;
        } else if (arg == "--bench") {
            Benchmark::BenchmarkSuite::runAllBenchmarks();
            return 0;
        }
    }

    printHeader();

    Simulation::Simulator simulator;
    simulator.initializeStandardUrbanGrid(5);
    std::cout << "[SYSTEM]: Initialized Standard Urban Grid (25 nodes, 3 hospitals, 6 ambulances, 5 incidents).\n";

    int choice = -1;
    while (choice != 0) {
        printMenu();
        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::string discard;
            std::cin >> discard;
            continue;
        }

        switch (choice) {
            case 1: {
                simulator.renderLiveState();
                simulator.renderCapacityAlerts();
                break;
            }
            case 2: {
                int dispatched = simulator.getDispatcher().dispatchPendingIncidentsPriorityQueue();
                std::cout << "\n[DISPATCH RESULT]: Successfully assigned and routed " << dispatched << " pending incidents!\n";
                std::cout << "Current Cumulative Objective Z: " << simulator.getDispatcher().getObjectiveZ() << "\n";
                simulator.renderLiveState();
                break;
            }
            case 3: {
                std::cout << "Enter delta seconds to advance simulation [default 60]: ";
                double delta = 60.0;
                std::cin >> delta;
                simulator.step(delta);
                std::cout << "[SIMULATOR]: Advanced clock by " << delta << " seconds.\n";
                simulator.renderLiveState();
                break;
            }
            case 4: {
                Simulation::Scenarios::executeScenario1NormalOperations();
                break;
            }
            case 5: {
                Simulation::Scenarios::executeScenario2CapacityShock();
                break;
            }
            case 6: {
                Simulation::Scenarios::executeScenario3AdversarialStress(1000);
                break;
            }
            case 7: {
                Benchmark::BenchmarkSuite::runAllBenchmarks();
                break;
            }
            case 8: {
                std::string csv_file = "dispatch_history.csv";
                std::string json_file = "simulation_metrics.json";
                if (simulator.exportHistoryToCSV(csv_file)) {
                    std::cout << "[EXPORT]: Dispatched history written to '" << csv_file << "'.\n";
                }
                if (simulator.exportMetricsToJSON(json_file)) {
                    std::cout << "[EXPORT]: Simulation metrics written to '" << json_file << "'.\n";
                }
                break;
            }
            case 9: {
                printSyllabusAudit();
                break;
            }
            case 0: {
                std::cout << "\n[DISPATCH]: Shutting down smart dispatch system. Goodbye.\n";
                break;
            }
            default: {
                std::cout << "[ERROR]: Unrecognized menu option. Please select 0-9.\n";
                break;
            }
        }
    }

    return 0;
}
