#include "domain/Dispatcher.hpp"
#include <iostream>
#include <limits>

namespace Domain {

Dispatcher::Dispatcher(RoadNetwork* network)
    : road_network_(network), cumulative_objective_Z_(0.0) {}

void Dispatcher::addAmbulance(const Ambulance& ambulance) {
    ambulances_.push_back(ambulance);
}

void Dispatcher::addHospital(const Hospital& hospital) {
    hospitals_.push_back(hospital);
}

void Dispatcher::addIncident(const Incident& incident) {
    incidents_.push_back(incident);
}

bool Dispatcher::dispatchIncidentDijkstra(int incident_idx, DispatchRecord& out_record) {
    if (!road_network_ || incident_idx < 0 || incident_idx >= static_cast<int>(incidents_.size())) {
        return false;
    }

    Incident& inc = incidents_[incident_idx];
    if (inc.isAssigned()) return false;

    int num_nodes = road_network_->numNodes();
    const auto& adj = road_network_->getAdjacencyList();

    int best_amb_idx = -1;
    int best_hosp_idx = -1;
    double min_weighted_cost = std::numeric_limits<double>::infinity();
    Algorithms::PathResult best_pickup_path;
    Algorithms::PathResult best_hosp_path;

    double priority_weight = inc.getPriorityWeight();

    // 1. Iterate over eligible available ambulances
    for (size_t a = 0; a < ambulances_.size(); ++a) {
        if (ambulances_[a].getStatus() != Core::AmbulanceStatus::IDLE) {
            continue;
        }

        // Triage constraint: P1 requires ALS if available
        if (inc.requiresAls() && ambulances_[a].getType() != Core::AmbulanceType::ALS) {
            // Check if there are ANY idle ALS ambulances
            bool any_als_available = false;
            for (size_t k = 0; k < ambulances_.size(); ++k) {
                if (ambulances_[k].getStatus() == Core::AmbulanceStatus::IDLE &&
                    ambulances_[k].getType() == Core::AmbulanceType::ALS) {
                    any_als_available = true;
                    break;
                }
            }
            if (any_als_available) {
                continue; // Wait/reserve ALS unit for this critical patient
            }
        }

        int amb_node = ambulances_[a].getCurrentNodeId();
        Algorithms::PathResult path_to_scene = Algorithms::Greedy::dijkstra(
            num_nodes, adj, amb_node, inc.getNodeId());

        if (!path_to_scene.found) continue;

        // 2. Iterate over destination hospitals with available capacity
        for (size_t h = 0; h < hospitals_.size(); ++h) {
            if (!hospitals_[h].hasCapacity(inc.requiresIcu())) {
                continue; // Capacity ceiling constraint
            }

            int hosp_node = hospitals_[h].getNodeId();
            Algorithms::PathResult path_to_hosp = Algorithms::Greedy::dijkstra(
                num_nodes, adj, inc.getNodeId(), hosp_node);

            if (!path_to_hosp.found) continue;

            // Mathematical Objective:
            // Z_ijk = w_pri(P_i) * [ d(loc(j), loc(i)) + d(loc(i), loc(k)) ]
            double total_time = path_to_scene.total_cost + path_to_hosp.total_cost;
            double weighted_cost = priority_weight * total_time;

            if (weighted_cost < min_weighted_cost) {
                min_weighted_cost = weighted_cost;
                best_amb_idx = static_cast<int>(a);
                best_hosp_idx = static_cast<int>(h);
                best_pickup_path = path_to_scene;
                best_hosp_path = path_to_hosp;
            }
        }
    }

    if (best_amb_idx == -1 || best_hosp_idx == -1) {
        return false; // No feasible dispatch under constraints
    }

    // Commit assignment
    Ambulance& chosen_amb = ambulances_[best_amb_idx];
    Hospital& chosen_hosp = hospitals_[best_hosp_idx];

    inc.assign(chosen_amb.getId(), chosen_hosp.getId());
    chosen_hosp.admitPatient(inc.requiresIcu());
    chosen_amb.dispatchToScene(inc.getId(), inc.getNodeId(), best_pickup_path.path, best_pickup_path.total_cost);

    out_record.incident_id = inc.getId();
    out_record.ambulance_id = chosen_amb.getId();
    out_record.hospital_id = chosen_hosp.getId();
    out_record.priority = inc.getPriority();
    out_record.pickup_travel_time_sec = best_pickup_path.total_cost;
    out_record.hospital_travel_time_sec = best_hosp_path.total_cost;
    out_record.weighted_cost = min_weighted_cost;
    out_record.pickup_route = best_pickup_path.path;
    out_record.hospital_route = best_hosp_path.path;
    out_record.notes = "Dispatched via Dijkstra Greedy Optimization";

    history_.push_back(out_record);
    cumulative_objective_Z_ += min_weighted_cost;

    return true;
}

int Dispatcher::dispatchPendingIncidentsPriorityQueue() {
    // 1. Gather all unassigned incident indices
    Core::CustomVector<size_t> pending_indices;
    for (size_t i = 0; i < incidents_.size(); ++i) {
        if (!incidents_[i].isAssigned()) {
            pending_indices.push_back(i);
        }
    }

    if (pending_indices.empty()) return 0;

    // 2. Sort incidents using custom Merge Sort: P1 > P2 > P3, then earlier timestamp
    Algorithms::SortingRetrieval::mergeSort(pending_indices, [&](size_t a, size_t b) {
        const Incident& incA = incidents_[a];
        const Incident& incB = incidents_[b];
        // Lower enum value = higher priority (P1 = 1, P2 = 2, P3 = 3)
        if (static_cast<int>(incA.getPriority()) != static_cast<int>(incB.getPriority())) {
            return static_cast<int>(incA.getPriority()) < static_cast<int>(incB.getPriority());
        }
        return incA.getTimestamp() < incB.getTimestamp();
    });

    // 3. Dispatch each incident in priority sequence
    int dispatched_count = 0;
    for (size_t i = 0; i < pending_indices.size(); ++i) {
        DispatchRecord rec;
        if (dispatchIncidentDijkstra(static_cast<int>(pending_indices[i]), rec)) {
            dispatched_count++;
        }
    }

    return dispatched_count;
}

int Dispatcher::dispatchBatchBipartiteMatching() {
    // 1. Identify idle ambulances (Left partition)
    Core::CustomVector<int> idle_amb_indices;
    for (size_t i = 0; i < ambulances_.size(); ++i) {
        if (ambulances_[i].getStatus() == Core::AmbulanceStatus::IDLE) {
            idle_amb_indices.push_back(static_cast<int>(i));
        }
    }

    // 2. Identify unassigned incidents (Right partition)
    Core::CustomVector<int> unassigned_inc_indices;
    for (size_t i = 0; i < incidents_.size(); ++i) {
        if (!incidents_[i].isAssigned()) {
            unassigned_inc_indices.push_back(static_cast<int>(i));
        }
    }

    if (idle_amb_indices.empty() || unassigned_inc_indices.empty()) {
        return 0;
    }

    int n_left = static_cast<int>(idle_amb_indices.size());
    int n_right = static_cast<int>(unassigned_inc_indices.size());

    // Build bipartite adjacency list
    Core::CustomVector<Core::CustomVector<int>> bip_adj(n_left);

    for (int l = 0; l < n_left; ++l) {
        const Ambulance& amb = ambulances_[idle_amb_indices[l]];
        for (int r = 0; r < n_right; ++r) {
            const Incident& inc = incidents_[unassigned_inc_indices[r]];
            // Match condition: ALS requirement compatibility
            if (!inc.requiresAls() || amb.getType() == Core::AmbulanceType::ALS) {
                bip_adj[l].push_back(r);
            }
        }
    }

    Algorithms::BipartiteMatchResult match_res =
        Algorithms::NetworkFlows::maxBipartiteMatching(n_left, n_right, bip_adj);

    int committed = 0;
    for (int l = 0; l < n_left; ++l) {
        int r = match_res.match_left_to_right[l];
        if (r >= 0) {
            int inc_idx = unassigned_inc_indices[r];
            int amb_idx = idle_amb_indices[l];

            // Route to best hospital
            int best_hosp = -1;
            double best_hosp_cost = std::numeric_limits<double>::infinity();
            Algorithms::PathResult best_hosp_path;

            for (size_t h = 0; h < hospitals_.size(); ++h) {
                if (hospitals_[h].hasCapacity(incidents_[inc_idx].requiresIcu())) {
                    auto path = Algorithms::Greedy::dijkstra(
                        road_network_->numNodes(), road_network_->getAdjacencyList(),
                        incidents_[inc_idx].getNodeId(), hospitals_[h].getNodeId());
                    if (path.found && path.total_cost < best_hosp_cost) {
                        best_hosp_cost = path.total_cost;
                        best_hosp = static_cast<int>(h);
                        best_hosp_path = path;
                    }
                }
            }

            if (best_hosp >= 0) {
                auto pickup_path = Algorithms::Greedy::dijkstra(
                    road_network_->numNodes(), road_network_->getAdjacencyList(),
                    ambulances_[amb_idx].getCurrentNodeId(), incidents_[inc_idx].getNodeId());

                if (pickup_path.found) {
                    incidents_[inc_idx].assign(ambulances_[amb_idx].getId(), hospitals_[best_hosp].getId());
                    hospitals_[best_hosp].admitPatient(incidents_[inc_idx].requiresIcu());
                    ambulances_[amb_idx].dispatchToScene(
                        incidents_[inc_idx].getId(), incidents_[inc_idx].getNodeId(),
                        pickup_path.path, pickup_path.total_cost);

                    DispatchRecord rec;
                    rec.incident_id = incidents_[inc_idx].getId();
                    rec.ambulance_id = ambulances_[amb_idx].getId();
                    rec.hospital_id = hospitals_[best_hosp].getId();
                    rec.priority = incidents_[inc_idx].getPriority();
                    rec.pickup_travel_time_sec = pickup_path.total_cost;
                    rec.hospital_travel_time_sec = best_hosp_cost;
                    rec.weighted_cost = incidents_[inc_idx].getPriorityWeight() * (pickup_path.total_cost + best_hosp_cost);
                    rec.pickup_route = pickup_path.path;
                    rec.hospital_route = best_hosp_path.path;
                    rec.notes = "Dispatched via Maximum Bipartite Matching";

                    history_.push_back(rec);
                    cumulative_objective_Z_ += rec.weighted_cost;
                    committed++;
                }
            }
        }
    }

    return committed;
}

bool Dispatcher::dispatchIncidentFloydWarshall(
    int incident_idx,
    const Algorithms::AllPairsResult& ap_result,
    DispatchRecord& out_record) {

    if (!road_network_ || incident_idx < 0 || incident_idx >= static_cast<int>(incidents_.size())) {
        return false;
    }

    Incident& inc = incidents_[incident_idx];
    if (inc.isAssigned()) return false;

    int best_amb_idx = -1;
    int best_hosp_idx = -1;
    double min_weighted_cost = std::numeric_limits<double>::infinity();
    double best_pickup_time = 0.0;
    double best_hosp_time = 0.0;

    double priority_weight = inc.getPriorityWeight();
    int inc_node = inc.getNodeId();

    for (size_t a = 0; a < ambulances_.size(); ++a) {
        if (ambulances_[a].getStatus() != Core::AmbulanceStatus::IDLE) continue;
        if (inc.requiresAls() && ambulances_[a].getType() != Core::AmbulanceType::ALS) continue;

        int amb_node = ambulances_[a].getCurrentNodeId();
        double d_scene = ap_result.dist[amb_node][inc_node];
        if (d_scene >= Core::INF_WEIGHT / 2.0) continue;

        for (size_t h = 0; h < hospitals_.size(); ++h) {
            if (!hospitals_[h].hasCapacity(inc.requiresIcu())) continue;

            int hosp_node = hospitals_[h].getNodeId();
            double d_hosp = ap_result.dist[inc_node][hosp_node];
            if (d_hosp >= Core::INF_WEIGHT / 2.0) continue;

            double cost = priority_weight * (d_scene + d_hosp);
            if (cost < min_weighted_cost) {
                min_weighted_cost = cost;
                best_amb_idx = static_cast<int>(a);
                best_hosp_idx = static_cast<int>(h);
                best_pickup_time = d_scene;
                best_hosp_time = d_hosp;
            }
        }
    }

    if (best_amb_idx == -1 || best_hosp_idx == -1) return false;

    // Commit
    Ambulance& chosen_amb = ambulances_[best_amb_idx];
    Hospital& chosen_hosp = hospitals_[best_hosp_idx];

    inc.assign(chosen_amb.getId(), chosen_hosp.getId());
    chosen_hosp.admitPatient(inc.requiresIcu());

    // Reconstruct path from next_node matrix
    Core::CustomVector<int> pickup_path;
    int curr = chosen_amb.getCurrentNodeId();
    pickup_path.push_back(curr);
    while (curr != inc_node) {
        curr = ap_result.next_node[curr][inc_node];
        if (curr == -1) break;
        pickup_path.push_back(curr);
    }

    chosen_amb.dispatchToScene(inc.getId(), inc_node, pickup_path, best_pickup_time);

    out_record.incident_id = inc.getId();
    out_record.ambulance_id = chosen_amb.getId();
    out_record.hospital_id = chosen_hosp.getId();
    out_record.priority = inc.getPriority();
    out_record.pickup_travel_time_sec = best_pickup_time;
    out_record.hospital_travel_time_sec = best_hosp_time;
    out_record.weighted_cost = min_weighted_cost;
    out_record.pickup_route = pickup_path;
    out_record.notes = "Dispatched via Floyd-Warshall All-Pairs DP";

    history_.push_back(out_record);
    cumulative_objective_Z_ += min_weighted_cost;
    return true;
}

int Dispatcher::evaluateMassCasualtyFlow(int incident_scene_node, int total_casualties) {
    if (!road_network_) return 0;

    // Source S = 0
    // Incident scene = 1
    // Intermediate road network nodes = 2 .. N+1
    // Regional Hospitals = N+2 .. N+1+H
    // Super Sink T = N+2+H
    int base_nodes = road_network_->numNodes();
    int h_count = static_cast<int>(hospitals_.size());
    int total_flow_nodes = base_nodes + 2 + h_count;
    int source = 0;
    int incident_flow_node = 1;
    int sink = total_flow_nodes - 1;

    Core::CustomVector<Core::CustomVector<Algorithms::FlowEdge>> flow_adj(total_flow_nodes);

    // Source to incident scene
    Algorithms::NetworkFlows::addFlowEdge(flow_adj, source, incident_flow_node, total_casualties);

    // Incident scene to road network
    Algorithms::NetworkFlows::addFlowEdge(flow_adj, incident_flow_node, incident_scene_node + 2, total_casualties);

    // Road network edges
    const auto& road_adj = road_network_->getAdjacencyList();
    for (int u = 0; u < base_nodes; ++u) {
        for (size_t i = 0; i < road_adj[u].size(); ++i) {
            int v = road_adj[u][i].to;
            int cap = road_adj[u][i].capacity;
            Algorithms::NetworkFlows::addFlowEdge(flow_adj, u + 2, v + 2, cap);
        }
    }

    // Road nodes to hospital nodes & sink
    for (int h = 0; h < h_count; ++h) {
        int hosp_node = hospitals_[h].getNodeId();
        int hosp_flow_node = base_nodes + 2 + h;
        // Connect road network node to hospital entrance
        Algorithms::NetworkFlows::addFlowEdge(flow_adj, hosp_node + 2, hosp_flow_node, hospitals_[h].getTotalBeds());
        // Connect hospital entrance to super sink with available bed capacity
        Algorithms::NetworkFlows::addFlowEdge(flow_adj, hosp_flow_node, sink, hospitals_[h].getAvailableBeds());
    }

    Algorithms::FlowResult flow_res =
        Algorithms::NetworkFlows::edmondsKarpMaxFlow(total_flow_nodes, source, sink, flow_adj);

    return flow_res.max_flow;
}

void Dispatcher::stepSimulation(double delta_sec) {
    for (size_t i = 0; i < ambulances_.size(); ++i) {
        ambulances_[i].advanceSimulationTime(delta_sec);
    }
}

} // namespace Domain
