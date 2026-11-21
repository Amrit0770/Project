#ifndef ALGORITHMS_NETWORK_FLOWS_HPP
#define ALGORITHMS_NETWORK_FLOWS_HPP

#include "core/CustomVector.hpp"
#include <cstddef>

namespace Algorithms {

struct FlowEdge {
    int to;
    int rev;      // Index of reverse edge in adj[to]
    int capacity;
    int flow;
};

struct FlowResult {
    int max_flow;
    Core::CustomVector<Core::CustomVector<FlowEdge>> residual_graph;
};

struct BipartiteMatchResult {
    int max_matching_size;
    Core::CustomVector<int> match_left_to_right;
    Core::CustomVector<int> match_right_to_left;
};

/**
 * @brief Module 6: Network Flows
 * Syllabus: Ford-Fulkerson, Maximum Bipartite Matching.
 * Domain: Regional mass-casualty patient flow optimization and optimal two-sided matching
 * between available ambulances and incident sites.
 * Essential for Scenario 2 (Capacity Shock evaluation).
 */
class NetworkFlows {
public:
    // --- 1. Ford-Fulkerson (Edmonds-Karp BFS Augmenting Path Implementation) ---
    // Time Complexity: O(V * E^2), Space: O(V + E)
    // Domain: Mass-casualty evacuation network routing from casualty collection points to regional hospitals.
    static FlowResult edmondsKarpMaxFlow(
        int num_nodes,
        int source,
        int sink,
        const Core::CustomVector<Core::CustomVector<FlowEdge>>& initial_adj);

    // --- 2. Maximum Bipartite Matching (Augmenting Path / Kuhn's Algorithm) ---
    // Time Complexity: O(V * E), Space: O(V)
    // Domain: Optimal 1-to-1 matching between available ambulances (U) and high-priority incidents (V).
    static BipartiteMatchResult maxBipartiteMatching(
        int num_left_nodes,
        int num_right_nodes,
        const Core::CustomVector<Core::CustomVector<int>>& bipartite_adj);

    // Helper to add directed residual edge pair
    static void addFlowEdge(
        Core::CustomVector<Core::CustomVector<FlowEdge>>& adj,
        int from,
        int to,
        int capacity);

private:
    static bool bpmDFS(
        int u,
        const Core::CustomVector<Core::CustomVector<int>>& adj,
        Core::CustomVector<bool>& visited,
        Core::CustomVector<int>& match_right);
};

} // namespace Algorithms

#endif // ALGORITHMS_NETWORK_FLOWS_HPP
