#include "algorithms/DynamicProgramming.hpp"
#include <algorithm>

namespace Algorithms {

KnapsackResult DynamicProgramming::solveAmbulancePayloadKnapsack(
    const Core::CustomVector<MedicalEquipment>& items,
    int max_payload_capacity) {

    KnapsackResult result;
    result.max_utility = 0;
    result.total_weight = 0;
    size_t n = items.size();
    if (n == 0 || max_payload_capacity <= 0) return result;

    // 2D DP Table of size (n + 1) x (max_payload_capacity + 1)
    Core::CustomVector<Core::CustomVector<int>> dp(
        n + 1, Core::CustomVector<int>(max_payload_capacity + 1, 0));

    for (size_t i = 1; i <= n; ++i) {
        int wt = items[i - 1].weight_kg;
        int val = items[i - 1].utility_value;

        for (int w = 0; w <= max_payload_capacity; ++w) {
            if (wt <= w) {
                dp[i][w] = std::max(dp[i - 1][w], dp[i - 1][w - wt] + val);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    result.max_utility = dp[n][max_payload_capacity];

    // Backtrack to find chosen items
    int w = max_payload_capacity;
    for (int i = static_cast<int>(n); i > 0 && w > 0; --i) {
        if (dp[i][w] != dp[i - 1][w]) {
            result.selected_equipment.push_back(items[i - 1]);
            result.total_weight += items[i - 1].weight_kg;
            w -= items[i - 1].weight_kg;
        }
    }

    return result;
}

AllPairsResult DynamicProgramming::floydWarshall(
    int num_nodes,
    const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj) {

    AllPairsResult res;
    res.has_negative_cycle = false;
    res.dist = Core::CustomVector<Core::CustomVector<double>>(
        num_nodes, Core::CustomVector<double>(num_nodes, Core::INF_WEIGHT));
    res.next_node = Core::CustomVector<Core::CustomVector<int>>(
        num_nodes, Core::CustomVector<int>(num_nodes, -1));

    for (int i = 0; i < num_nodes; ++i) {
        res.dist[i][i] = 0.0;
        res.next_node[i][i] = i;
    }

    for (int u = 0; u < num_nodes; ++u) {
        for (size_t i = 0; i < adj[u].size(); ++i) {
            int v = adj[u][i].to;
            double w = adj[u][i].weight;
            if (w < res.dist[u][v]) {
                res.dist[u][v] = w;
                res.next_node[u][v] = v;
            }
        }
    }

    // Dynamic programming triples relaxation
    for (int k = 0; k < num_nodes; ++k) {
        for (int i = 0; i < num_nodes; ++i) {
            if (res.dist[i][k] >= Core::INF_WEIGHT / 2.0) continue;
            for (int j = 0; j < num_nodes; ++j) {
                if (res.dist[k][j] >= Core::INF_WEIGHT / 2.0) continue;
                if (res.dist[i][k] + res.dist[k][j] < res.dist[i][j]) {
                    res.dist[i][j] = res.dist[i][k] + res.dist[k][j];
                    res.next_node[i][j] = res.next_node[i][k];
                }
            }
        }
    }

    // Check negative cycle
    for (int i = 0; i < num_nodes; ++i) {
        if (res.dist[i][i] < 0.0) {
            res.has_negative_cycle = true;
            break;
        }
    }

    return res;
}

Core::CustomVector<double> DynamicProgramming::bellmanFord(
    int num_nodes,
    int source,
    const Core::CustomVector<Core::Edge>& edge_list,
    const Core::CustomVector<int>& edge_sources,
    bool& has_negative_cycle) {

    has_negative_cycle = false;
    Core::CustomVector<double> dist(num_nodes, Core::INF_WEIGHT);
    if (source < 0 || source >= num_nodes) return dist;

    dist[source] = 0.0;
    size_t num_edges = edge_list.size();

    for (int iter = 1; iter < num_nodes; ++iter) {
        bool changed = false;
        for (size_t e = 0; e < num_edges; ++e) {
            int u = edge_sources[e];
            int v = edge_list[e].to;
            double w = edge_list[e].weight;

            if (dist[u] < Core::INF_WEIGHT / 2.0 && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                changed = true;
            }
        }
        if (!changed) break;
    }

    // Check negative cycle
    for (size_t e = 0; e < num_edges; ++e) {
        int u = edge_sources[e];
        int v = edge_list[e].to;
        double w = edge_list[e].weight;
        if (dist[u] < Core::INF_WEIGHT / 2.0 && dist[u] + w < dist[v]) {
            has_negative_cycle = true;
            break;
        }
    }

    return dist;
}

int DynamicProgramming::longestCommonSubsequence(const std::string& s1, const std::string& s2) {
    size_t m = s1.length();
    size_t n = s2.length();
    Core::CustomVector<Core::CustomVector<int>> dp(
        m + 1, Core::CustomVector<int>(n + 1, 0));

    for (size_t i = 1; i <= m; ++i) {
        for (size_t j = 1; j <= n; ++j) {
            if (s1[i - 1] == s2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}

int DynamicProgramming::matrixChainOrder(const Core::CustomVector<int>& p) {
    // Standard Matrix Chain DP: m[i][j] = min_{k} (m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j])
    size_t n = p.size() - 1;
    Core::CustomVector<Core::CustomVector<int>> m(
        n + 1, Core::CustomVector<int>(n + 1, 0));

    for (size_t l = 2; l <= n; ++l) {
        for (size_t i = 1; i <= n - l + 1; ++i) {
            size_t j = i + l - 1;
            m[i][j] = 1e9;
            for (size_t k = i; k < j; ++k) {
                int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                if (q < m[i][j]) {
                    m[i][j] = q;
                }
            }
        }
    }
    return m[1][n];
}

double DynamicProgramming::optimalBST(const Core::CustomVector<double>&, const Core::CustomVector<double>&, int) {
    // Optimal BST dynamic programming stub for diagnostic decision trees
    return 0.0;
}

double DynamicProgramming::tspHeldKarp(const Core::CustomVector<Core::CustomVector<double>>&, Core::CustomVector<int>&) {
    // Multi-stop tour dynamic programming stub for mass disaster triage sweep
    return 0.0;
}

} // namespace Algorithms
