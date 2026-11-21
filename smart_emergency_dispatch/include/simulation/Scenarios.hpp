#ifndef SIMULATION_SCENARIOS_HPP
#define SIMULATION_SCENARIOS_HPP

#include "simulation/Simulator.hpp"

namespace Simulation {

struct Scenario1Metrics {
    double dijkstra_total_time_ms;
    double dijkstra_avg_latency_ms;
    double floyd_warshall_build_time_ms;
    double floyd_warshall_query_time_ms;
    double dijkstra_objective_Z;
    double floyd_objective_Z;
    int incidents_dispatched;
};

struct Scenario2Metrics {
    int total_casualties;
    int bipartite_matched_count;
    int bipartite_unassigned_count;
    int ford_fulkerson_max_flow;
    double bipartite_exec_time_ms;
    double ford_fulkerson_exec_time_ms;
    int blocked_roads_count;
};

struct Scenario3Metrics {
    int node_count;
    int edge_count;
    double dijkstra_runtime_ms;
    double floyd_warshall_estimate_ms;
    size_t memory_estimate_kb;
};

class Scenarios {
public:
    // Mandatory Demonstration Scenario 1: Normal Operations
    static Scenario1Metrics executeScenario1NormalOperations();

    // Mandatory Demonstration Scenario 2: Capacity Shock
    static Scenario2Metrics executeScenario2CapacityShock();

    // Mandatory Demonstration Scenario 3: Adversarial Stress & Scalability
    static Scenario3Metrics executeScenario3AdversarialStress(int node_count = 500);
};

} // namespace Simulation

#endif // SIMULATION_SCENARIOS_HPP
