#ifndef DOMAIN_DISPATCHER_HPP
#define DOMAIN_DISPATCHER_HPP

#include "core/CustomVector.hpp"
#include "core/Types.hpp"
#include "domain/RoadNetwork.hpp"
#include "domain/Ambulance.hpp"
#include "domain/Hospital.hpp"
#include "domain/Incident.hpp"
#include "algorithms/Greedy.hpp"
#include "algorithms/DynamicProgramming.hpp"
#include "algorithms/NetworkFlows.hpp"
#include "algorithms/SortingRetrieval.hpp"

namespace Domain {

struct DispatchRecord {
    int incident_id;
    int ambulance_id;
    int hospital_id;
    Core::TriagePriority priority;
    double pickup_travel_time_sec;
    double hospital_travel_time_sec;
    double weighted_cost;
    Core::CustomVector<int> pickup_route;
    Core::CustomVector<int> hospital_route;
    std::string notes;
};

class Dispatcher {
private:
    RoadNetwork* road_network_;
    Core::CustomVector<Ambulance> ambulances_;
    Core::CustomVector<Hospital> hospitals_;
    Core::CustomVector<Incident> incidents_;
    Core::CustomVector<DispatchRecord> history_;
    double cumulative_objective_Z_;

public:
    explicit Dispatcher(RoadNetwork* network = nullptr);

    void setRoadNetwork(RoadNetwork* network) { road_network_ = network; }
    void addAmbulance(const Ambulance& ambulance);
    void addHospital(const Hospital& hospital);
    void addIncident(const Incident& incident);

    Core::CustomVector<Ambulance>& getAmbulances() { return ambulances_; }
    const Core::CustomVector<Ambulance>& getAmbulances() const { return ambulances_; }

    Core::CustomVector<Hospital>& getHospitals() { return hospitals_; }
    const Core::CustomVector<Hospital>& getHospitals() const { return hospitals_; }

    Core::CustomVector<Incident>& getIncidents() { return incidents_; }
    const Core::CustomVector<Incident>& getIncidents() const { return incidents_; }

    const Core::CustomVector<DispatchRecord>& getHistory() const { return history_; }
    double getObjectiveZ() const { return cumulative_objective_Z_; }

    // Core Dispatch Logic 1: Online Greedy Dijkstra Optimization
    // Minimizes: w_pri(P_i) * ( d(loc(j), loc(i)) + d(loc(i), loc(k)) )
    bool dispatchIncidentDijkstra(int incident_idx, DispatchRecord& out_record);

    // Core Dispatch Logic 2: Batch Incident Prioritization & Greedy Dispatch
    // Uses MergeSort on incidents by severity, then dispatches greedily
    int dispatchPendingIncidentsPriorityQueue();

    // Core Dispatch Logic 3: Maximum Bipartite Matching
    // Two-sided optimal matching between available ambulances and incident sites
    int dispatchBatchBipartiteMatching();

    // Core Dispatch Logic 4: All-Pairs DP Routing Comparison
    // Precomputes all-pairs via Floyd-Warshall and executes dispatch
    bool dispatchIncidentFloydWarshall(
        int incident_idx,
        const Algorithms::AllPairsResult& ap_result,
        DispatchRecord& out_record);

    // Mass Casualty Flow Evaluation via Edmonds-Karp Max Flow
    int evaluateMassCasualtyFlow(int incident_scene_node, int total_casualties);

    // Advance simulation clock for all ambulances
    void stepSimulation(double delta_sec);
};

} // namespace Domain

#endif // DOMAIN_DISPATCHER_HPP
