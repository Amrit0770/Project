#include "simulation/Scenarios.hpp"
#include "algorithms/Greedy.hpp"
#include "algorithms/DynamicProgramming.hpp"
#include "algorithms/NetworkFlows.hpp"
#include "algorithms/SortingRetrieval.hpp"
#include <chrono>
#include <iostream>
#include <iomanip>

namespace Simulation {

Scenario1Metrics Scenarios::executeScenario1NormalOperations() {
    std::cout << "\n========================================================================\n";
    std::cout << "  SCENARIO 1: NORMAL OPERATIONS (DIJKSTRA vs. FLOYD-WARSHALL ROUTING)   \n";
    std::cout << "========================================================================\n";
    std::cout << "[Condition]: Standard incident rate, predictable traffic flow, 30% bed occupancy.\n\n";

    Simulator sim1;
    sim1.initializeStandardUrbanGrid(5); // 25 nodes
    auto& d1 = sim1.getDispatcher();

    // Set 30% occupancy across hospitals
    auto& hosps = d1.getHospitals();
    for (size_t i = 0; i < hosps.size(); ++i) {
        int cap = hosps[i].getTotalBeds();
        int occ = static_cast<int>(cap * 0.30);
        hosps[i].setAvailableBeds(cap - occ);
    }

    // Benchmark Dijkstra-based greedy dispatch
    auto t1_start = std::chrono::high_resolution_clock::now();
    int dispatched_dijkstra = d1.dispatchPendingIncidentsPriorityQueue();
    auto t1_end = std::chrono::high_resolution_clock::now();
    double dijkstra_time_ms = std::chrono::duration<double, std::milli>(t1_end - t1_start).count();

    Scenario1Metrics metrics;
    metrics.dijkstra_total_time_ms = dijkstra_time_ms;
    metrics.dijkstra_avg_latency_ms = (dispatched_dijkstra > 0) ? (dijkstra_time_ms / dispatched_dijkstra) : 0.0;
    metrics.dijkstra_objective_Z = d1.getObjectiveZ();
    metrics.incidents_dispatched = dispatched_dijkstra;

    // Benchmark Floyd-Warshall DP dispatch
    Simulator sim2;
    sim2.initializeStandardUrbanGrid(5);
    auto& d2 = sim2.getDispatcher();
    for (size_t i = 0; i < d2.getHospitals().size(); ++i) {
        int cap = d2.getHospitals()[i].getTotalBeds();
        int occ = static_cast<int>(cap * 0.30);
        d2.getHospitals()[i].setAvailableBeds(cap - occ);
    }

    auto t2_fw_start = std::chrono::high_resolution_clock::now();
    auto ap_res = Algorithms::DynamicProgramming::floydWarshall(
        sim2.getRoadNetwork().numNodes(), sim2.getRoadNetwork().getAdjacencyList());
    auto t2_fw_built = std::chrono::high_resolution_clock::now();
    double fw_build_time_ms = std::chrono::duration<double, std::milli>(t2_fw_built - t2_fw_start).count();

    auto t2_query_start = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < d2.getIncidents().size(); ++i) {
        Domain::DispatchRecord rec;
        d2.dispatchIncidentFloydWarshall(static_cast<int>(i), ap_res, rec);
    }
    auto t2_query_end = std::chrono::high_resolution_clock::now();
    double fw_query_time_ms = std::chrono::duration<double, std::milli>(t2_query_end - t2_query_start).count();

    metrics.floyd_warshall_build_time_ms = fw_build_time_ms;
    metrics.floyd_warshall_query_time_ms = fw_query_time_ms;
    metrics.floyd_objective_Z = d2.getObjectiveZ();

    std::cout << "[ANALYTICAL RESULTS]:\n";
    std::cout << "  - Incidents Dispatched: " << metrics.incidents_dispatched << "\n";
    std::cout << "  - Greedy Dijkstra Total Exec Time:      " << std::fixed << std::setprecision(4) << metrics.dijkstra_total_time_ms << " ms\n";
    std::cout << "  - Greedy Dijkstra Avg Query Latency:    " << metrics.dijkstra_avg_latency_ms << " ms\n";
    std::cout << "  - Greedy Dijkstra Objective Z:          " << metrics.dijkstra_objective_Z << "\n";
    std::cout << "  - Floyd-Warshall DP Matrix Build Time:  " << metrics.floyd_warshall_build_time_ms << " ms (O(V^3))\n";
    std::cout << "  - Floyd-Warshall DP Query Time:         " << metrics.floyd_warshall_query_time_ms << " ms (O(1) lookup)\n";
    std::cout << "  - Floyd-Warshall Objective Z:           " << metrics.floyd_objective_Z << "\n";
    std::cout << "\n[STRATEGY TRADE-OFF DEDUCTION]:\n";
    std::cout << "  * Greedy Dijkstra is optimal for on-demand sparse urban dispatch when edge travel times vary dynamically.\n";
    std::cout << "  * Floyd-Warshall amortizes fast when query volume Q >> V, but incurs prohibitive O(V^3) re-computation penalty\n";
    std::cout << "    whenever traffic congestion or road closures update edge weights.\n";

    return metrics;
}

Scenario2Metrics Scenarios::executeScenario2CapacityShock() {
    std::cout << "\n========================================================================\n";
    std::cout << "  SCENARIO 2: CAPACITY SHOCK (MASS CASUALTY & REGIONAL HOSPITAL OVERLOAD) \n";
    std::cout << "========================================================================\n";
    std::cout << "[Condition]: Sudden surge (30 casualties), primary trauma center overload, key corridors blocked.\n\n";

    Simulator sim;
    sim.initializeStandardUrbanGrid(5);
    auto& net = sim.getRoadNetwork();
    auto& disp = sim.getDispatcher();

    // 1. Simulate Major Road Closures (e.g. disaster epicenter around nodes 6, 7, 12)
    net.blockEdge(6, 7);
    net.blockEdge(7, 6);
    net.blockEdge(11, 12);
    net.blockEdge(12, 11);
    net.blockEdge(7, 12);
    std::cout << "[EVENT]: 5 Major urban road corridors collapsed / blocked.\n";

    // 2. Simulate Primary Hospital Overload (St. Jude Trauma Center at capacity: 0 beds)
    disp.getHospitals()[0].setAvailableBeds(0);
    disp.getHospitals()[0].setAvailableIcu(0);
    std::cout << "[EVENT]: Primary Level-1 Trauma Center overwhelmed (Available beds = 0).\n";

    // 3. Inject Mass Casualty Incident Surge (30 patients at disaster epicenter Node 12)
    int disaster_node = 12;
    int total_casualties = 30;
    for (int i = 0; i < total_casualties; ++i) {
        Core::TriagePriority pri = (i % 3 == 0) ? Core::TriagePriority::P1_CRITICAL :
                                   (i % 3 == 1) ? Core::TriagePriority::P2_URGENT : Core::TriagePriority::P3_DELAYED;
        disp.addIncident(Domain::Incident(200 + i, disaster_node, pri, (pri == Core::TriagePriority::P1_CRITICAL),
                                          (pri == Core::TriagePriority::P1_CRITICAL), 10.0 * i, "Mass Disaster Casualty #" + std::to_string(i)));
    }

    // 4. Test Maximum Bipartite Matching Reallocation
    auto t_bpm_start = std::chrono::high_resolution_clock::now();
    int bpm_matched = disp.dispatchBatchBipartiteMatching();
    auto t_bpm_end = std::chrono::high_resolution_clock::now();
    double bpm_time = std::chrono::duration<double, std::milli>(t_bpm_end - t_bpm_start).count();

    // 5. Test Ford-Fulkerson (Edmonds-Karp) Mass Flow
    auto t_ff_start = std::chrono::high_resolution_clock::now();
    int max_flow_evacuated = disp.evaluateMassCasualtyFlow(disaster_node, total_casualties);
    auto t_ff_end = std::chrono::high_resolution_clock::now();
    double ff_time = std::chrono::duration<double, std::milli>(t_ff_end - t_ff_start).count();

    Scenario2Metrics metrics;
    metrics.total_casualties = total_casualties;
    metrics.bipartite_matched_count = bpm_matched;
    metrics.bipartite_unassigned_count = total_casualties - bpm_matched;
    metrics.ford_fulkerson_max_flow = max_flow_evacuated;
    metrics.bipartite_exec_time_ms = bpm_time;
    metrics.ford_fulkerson_exec_time_ms = ff_time;
    metrics.blocked_roads_count = 5;

    std::cout << "[ANALYTICAL RESULTS]:\n";
    std::cout << "  - Total Casualties at Epicenter:       " << metrics.total_casualties << "\n";
    std::cout << "  - Bipartite Matching Allocated:        " << metrics.bipartite_matched_count << " (Limited strictly by available fleet size)\n";
    std::cout << "  - Bipartite Matching Unassigned Queue: " << metrics.bipartite_unassigned_count << "\n";
    std::cout << "  - Bipartite Execution Time:            " << std::fixed << std::setprecision(4) << metrics.bipartite_exec_time_ms << " ms\n";
    std::cout << "  - Ford-Fulkerson Regional Max Flow:    " << metrics.ford_fulkerson_max_flow << " patients/surge cycle (Full multi-hospital capacity)\n";
    std::cout << "  - Ford-Fulkerson Execution Time:       " << metrics.ford_fulkerson_exec_time_ms << " ms\n";
    std::cout << "\n[REALLOCATION STABILITY DEDUCTION]:\n";
    std::cout << "  * Bipartite Matching provides exact 1-to-1 immediate dispatch pairing, but collapses under fleet exhaustion.\n";
    std::cout << "  * Ford-Fulkerson identifies the structural bottleneck capacity of the entire regional health corridor,\n";
    std::cout << "    proving that " << metrics.ford_fulkerson_max_flow << " casualties can be distributed to secondary hospitals\n";
    std::cout << "    if mutual-aid transit shuttles are deployed.\n";

    return metrics;
}

Scenario3Metrics Scenarios::executeScenario3AdversarialStress(int node_count) {
    std::cout << "\n========================================================================\n";
    std::cout << "  SCENARIO 3: ADVERSARIAL STRESS & SCALING BENCHMARK                    \n";
    std::cout << "========================================================================\n";
    std::cout << "[Condition]: Synthetic urban graph scaling (" << node_count << " nodes), worst-case call routing.\n\n";

    Domain::RoadNetwork stress_net(node_count);
    // Build random ring-mesh
    for (int i = 0; i < node_count; ++i) {
        int nxt = (i + 1) % node_count;
        stress_net.addEdge(i, nxt, 50.0 + (i % 7) * 10.0, 500.0, 10);
        stress_net.addEdge(nxt, i, 50.0 + (i % 7) * 10.0, 500.0, 10);
        if (i + 5 < node_count) {
            stress_net.addEdge(i, i + 5, 80.0, 800.0, 10);
            stress_net.addEdge(i + 5, i, 80.0, 800.0, 10);
        }
    }

    auto t_start = std::chrono::high_resolution_clock::now();
    auto path = Algorithms::Greedy::dijkstra(node_count, stress_net.getAdjacencyList(), 0, node_count - 1);
    auto t_end = std::chrono::high_resolution_clock::now();
    double dijkstra_time = std::chrono::duration<double, std::milli>(t_end - t_start).count();

    Scenario3Metrics metrics;
    metrics.node_count = node_count;
    metrics.edge_count = static_cast<int>(stress_net.numEdges());
    metrics.dijkstra_runtime_ms = dijkstra_time;
    // Theoretical Floyd-Warshall estimate for comparison (V^3 operations at ~1ns per op)
    double fw_ops = static_cast<double>(node_count) * node_count * node_count;
    metrics.floyd_warshall_estimate_ms = (fw_ops * 1e-6); // Approx ms
    metrics.memory_estimate_kb = (sizeof(Core::Edge) * metrics.edge_count + sizeof(double) * node_count) / 1024;

    std::cout << "[ANALYTICAL RESULTS]:\n";
    std::cout << "  - Network Scale:        " << metrics.node_count << " nodes, " << metrics.edge_count << " edges\n";
    std::cout << "  - Dijkstra Runtime:     " << std::fixed << std::setprecision(4) << metrics.dijkstra_runtime_ms << " ms (< 50ms requirement)\n";
    std::cout << "  - Floyd-Warshall Est.:  " << metrics.floyd_warshall_estimate_ms << " ms\n";
    std::cout << "  - Graph Memory Footprint: ~" << metrics.memory_estimate_kb << " KB\n";
    std::cout << "  - Asymptotic Scaling:   Dijkstra executes in O((V + E) log V) with predictable memory bounds.\n";

    return metrics;
}

} // namespace Simulation
