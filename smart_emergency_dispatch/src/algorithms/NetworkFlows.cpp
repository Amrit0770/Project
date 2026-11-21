#include "algorithms/NetworkFlows.hpp"
#include <algorithm>
#include <limits>

namespace Algorithms {

void NetworkFlows::addFlowEdge(
    Core::CustomVector<Core::CustomVector<FlowEdge>>& adj,
    int from,
    int to,
    int capacity) {

    FlowEdge a{to, static_cast<int>(adj[to].size()), capacity, 0};
    FlowEdge b{from, static_cast<int>(adj[from].size()), 0, 0};
    adj[from].push_back(a);
    adj[to].push_back(b);
}

FlowResult NetworkFlows::edmondsKarpMaxFlow(
    int num_nodes,
    int source,
    int sink,
    const Core::CustomVector<Core::CustomVector<FlowEdge>>& initial_adj) {

    FlowResult result;
    result.max_flow = 0;
    result.residual_graph = initial_adj;

    if (source < 0 || source >= num_nodes || sink < 0 || sink >= num_nodes || source == sink) {
        return result;
    }

    while (true) {
        // BFS to find shortest augmenting path in terms of number of edges
        Core::CustomVector<int> parent_node(num_nodes, -1);
        Core::CustomVector<int> parent_edge_idx(num_nodes, -1);
        Core::CustomVector<bool> visited(num_nodes, false);

        // Simple zero-STL queue using CustomVector
        Core::CustomVector<int> q;
        size_t head = 0;

        visited[source] = true;
        q.push_back(source);

        while (head < q.size()) {
            int u = q[head++];
            if (u == sink) break;

            for (size_t i = 0; i < result.residual_graph[u].size(); ++i) {
                const auto& edge = result.residual_graph[u][i];
                if (!visited[edge.to] && edge.capacity - edge.flow > 0) {
                    visited[edge.to] = true;
                    parent_node[edge.to] = u;
                    parent_edge_idx[edge.to] = static_cast<int>(i);
                    q.push_back(edge.to);
                }
            }
        }

        // If sink not reached, no more augmenting paths
        if (!visited[sink]) {
            break;
        }

        // Find bottleneck capacity along the augmenting path
        int push_flow = std::numeric_limits<int>::max();
        for (int curr = sink; curr != source; curr = parent_node[curr]) {
            int p = parent_node[curr];
            int e_idx = parent_edge_idx[curr];
            int residual = result.residual_graph[p][e_idx].capacity - result.residual_graph[p][e_idx].flow;
            if (residual < push_flow) {
                push_flow = residual;
            }
        }

        // Augment flow along path
        for (int curr = sink; curr != source; curr = parent_node[curr]) {
            int p = parent_node[curr];
            int e_idx = parent_edge_idx[curr];
            result.residual_graph[p][e_idx].flow += push_flow;
            int rev_idx = result.residual_graph[p][e_idx].rev;
            result.residual_graph[curr][rev_idx].flow -= push_flow;
        }

        result.max_flow += push_flow;
    }

    return result;
}

bool NetworkFlows::bpmDFS(
    int u,
    const Core::CustomVector<Core::CustomVector<int>>& adj,
    Core::CustomVector<bool>& visited,
    Core::CustomVector<int>& match_right) {

    for (size_t i = 0; i < adj[u].size(); ++i) {
        int v = adj[u][i];
        if (!visited[v]) {
            visited[v] = true;
            // If right node v is not matched, or previously matched node has an alternate path
            if (match_right[v] < 0 || bpmDFS(match_right[v], adj, visited, match_right)) {
                match_right[v] = u;
                return true;
            }
        }
    }
    return false;
}

BipartiteMatchResult NetworkFlows::maxBipartiteMatching(
    int num_left_nodes,
    int num_right_nodes,
    const Core::CustomVector<Core::CustomVector<int>>& bipartite_adj) {

    BipartiteMatchResult result;
    result.max_matching_size = 0;
    result.match_left_to_right.resize(num_left_nodes, -1);
    result.match_right_to_left.resize(num_right_nodes, -1);

    for (int u = 0; u < num_left_nodes; ++u) {
        Core::CustomVector<bool> visited(num_right_nodes, false);
        if (bpmDFS(u, bipartite_adj, visited, result.match_right_to_left)) {
            result.max_matching_size++;
        }
    }

    // Populate left to right inverse mapping
    for (int v = 0; v < num_right_nodes; ++v) {
        if (result.match_right_to_left[v] >= 0) {
            result.match_left_to_right[result.match_right_to_left[v]] = v;
        }
    }

    return result;
}

} // namespace Algorithms
