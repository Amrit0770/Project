#include "algorithms/Greedy.hpp"
#include "algorithms/SortingRetrieval.hpp"
#include <algorithm>

namespace Algorithms {

PathResult Greedy::dijkstra(
    int num_nodes,
    const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj,
    int start_node,
    int target_node) {

    PathResult result;
    result.total_cost = Core::INF_WEIGHT;
    result.found = false;

    if (start_node < 0 || start_node >= num_nodes || target_node < 0 || target_node >= num_nodes) {
        return result;
    }

    if (start_node == target_node) {
        result.total_cost = 0.0;
        result.path.push_back(start_node);
        result.found = true;
        return result;
    }

    Core::CustomVector<double> dist(num_nodes, Core::INF_WEIGHT);
    Core::CustomVector<int> parent(num_nodes, -1);
    Core::CustomVector<bool> visited(num_nodes, false);

    // Min-heap storing (cost, node)
    Core::CustomMinHeap<Core::NodeCost> pq;

    dist[start_node] = 0.0;
    pq.push({start_node, 0.0});

    while (!pq.empty()) {
        Core::NodeCost top_item = pq.pop();
        int u = top_item.node;

        if (visited[u]) continue;
        visited[u] = true;

        if (u == target_node) break;

        for (size_t i = 0; i < adj[u].size(); ++i) {
            const auto& edge = adj[u][i];
            int v = edge.to;
            double weight = edge.weight;

            if (!visited[v] && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push({v, dist[v]});
            }
        }
    }

    if (dist[target_node] < Core::INF_WEIGHT / 2.0) {
        result.total_cost = dist[target_node];
        result.found = true;

        // Reconstruct path
        Core::CustomVector<int> rev_path;
        int curr = target_node;
        while (curr != -1) {
            rev_path.push_back(curr);
            curr = parent[curr];
        }

        for (int i = static_cast<int>(rev_path.size()) - 1; i >= 0; --i) {
            result.path.push_back(rev_path[i]);
        }
    }

    return result;
}

Core::CustomVector<double> Greedy::dijkstraAll(
    int num_nodes,
    const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj,
    int start_node) {

    Core::CustomVector<double> dist(num_nodes, Core::INF_WEIGHT);
    Core::CustomVector<bool> visited(num_nodes, false);

    if (start_node < 0 || start_node >= num_nodes) return dist;

    Core::CustomMinHeap<Core::NodeCost> pq;
    dist[start_node] = 0.0;
    pq.push({start_node, 0.0});

    while (!pq.empty()) {
        Core::NodeCost top_item = pq.pop();
        int u = top_item.node;

        if (visited[u]) continue;
        visited[u] = true;

        for (size_t i = 0; i < adj[u].size(); ++i) {
            const auto& edge = adj[u][i];
            int v = edge.to;
            double weight = edge.weight;

            if (!visited[v] && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({v, dist[v]});
            }
        }
    }

    return dist;
}

MSTResult Greedy::primMST(
    int num_nodes,
    const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj) {

    MSTResult result;
    result.total_weight = 0.0;
    if (num_nodes == 0) return result;

    Core::CustomVector<bool> in_mst(num_nodes, false);
    Core::CustomMinHeap<MSTEdge> pq;

    in_mst[0] = true;
    for (size_t i = 0; i < adj[0].size(); ++i) {
        pq.push(MSTEdge(0, adj[0][i].to, adj[0][i].weight));
    }

    size_t edge_count = 0;
    while (!pq.empty() && edge_count < static_cast<size_t>(num_nodes - 1)) {
        MSTEdge edge = pq.pop();
        int v = edge.v;

        if (in_mst[v]) continue;

        in_mst[v] = true;
        result.edges.push_back(edge);
        result.total_weight += edge.weight;
        ++edge_count;

        for (size_t i = 0; i < adj[v].size(); ++i) {
            int nxt = adj[v][i].to;
            if (!in_mst[nxt]) {
                pq.push(MSTEdge(v, nxt, adj[v][i].weight));
            }
        }
    }

    return result;
}

MSTResult Greedy::kruskalMST(
    int num_nodes,
    Core::CustomVector<MSTEdge>& edge_list) {

    MSTResult result;
    result.total_weight = 0.0;
    if (num_nodes == 0) return result;

    // Sort edges by weight in ascending order using QuickSort
    SortingRetrieval::quickSort(edge_list, [](const MSTEdge& a, const MSTEdge& b) {
        return a.weight < b.weight;
    });

    Core::DisjointSet dsu(num_nodes);

    for (size_t i = 0; i < edge_list.size(); ++i) {
        int u = edge_list[i].u;
        int v = edge_list[i].v;

        if (dsu.unite(u, v)) {
            result.edges.push_back(edge_list[i]);
            result.total_weight += edge_list[i].weight;
            if (result.edges.size() == static_cast<size_t>(num_nodes - 1)) {
                break;
            }
        }
    }

    return result;
}

Core::CustomVector<Activity> Greedy::activitySelection(Core::CustomVector<Activity>& activities) {
    Core::CustomVector<Activity> selected;
    if (activities.empty()) return selected;

    // Sort by finish time ascending
    SortingRetrieval::quickSort(activities, [](const Activity& a, const Activity& b) {
        return a.finish_time < b.finish_time;
    });

    selected.push_back(activities[0]);
    size_t last_idx = 0;

    for (size_t i = 1; i < activities.size(); ++i) {
        if (activities[i].start_time >= activities[last_idx].finish_time) {
            selected.push_back(activities[i]);
            last_idx = i;
        }
    }

    return selected;
}

int Greedy::intervalPartitioningMinResources(Core::CustomVector<Activity>& activities) {
    if (activities.empty()) return 0;

    // Sort by start time
    SortingRetrieval::quickSort(activities, [](const Activity& a, const Activity& b) {
        return a.start_time < b.start_time;
    });

    // Min-heap of finish times
    Core::CustomMinHeap<double> finish_times;
    finish_times.push(activities[0].finish_time);

    for (size_t i = 1; i < activities.size(); ++i) {
        if (activities[i].start_time >= finish_times.top()) {
            finish_times.pop(); // Reuse room / crew
        }
        finish_times.push(activities[i].finish_time);
    }

    return static_cast<int>(finish_times.size());
}

std::string Greedy::huffmanCompress(const std::string& message) {
    // Alert message payload compression stub for tactical mesh
    // In full implementation, builds Huffman tree and encodes to bitstream
    return "[HUFFMAN_ENCODED: len=" + std::to_string(message.length()) + "]";
}

} // namespace Algorithms
