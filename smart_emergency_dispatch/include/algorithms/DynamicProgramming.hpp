#ifndef ALGORITHMS_DYNAMIC_PROGRAMMING_HPP
#define ALGORITHMS_DYNAMIC_PROGRAMMING_HPP

#include "core/CustomVector.hpp"
#include "core/Types.hpp"
#include <string>

namespace Algorithms {

struct MedicalEquipment {
    int id;
    std::string name;
    int weight_kg;
    int utility_value; // Clinical impact / life-saving score
    bool is_als_required; // Must have for ALS unit

    MedicalEquipment() : id(0), name(""), weight_kg(0), utility_value(0), is_als_required(false) {}
    MedicalEquipment(int i, std::string n, int w, int u, bool als = false)
        : id(i), name(n), weight_kg(w), utility_value(u), is_als_required(als) {}
};

struct KnapsackResult {
    int max_utility;
    int total_weight;
    Core::CustomVector<MedicalEquipment> selected_equipment;
};

struct AllPairsResult {
    Core::CustomVector<Core::CustomVector<double>> dist;
    Core::CustomVector<Core::CustomVector<int>> next_node;
    bool has_negative_cycle;
};

/**
 * @brief Module 4: Dynamic Programming
 * Syllabus: 0/1 Knapsack, Matrix Chain, LCS, Optimal BST, Bellman-Ford, Floyd-Warshall, TSP.
 * Domain: Equipping ambulances under payload/budget, multi-stage routing, protocol sequence alignment, all-pairs distance.
 */
class DynamicProgramming {
public:
    // --- 1. 0/1 Knapsack (Equipping Ambulances Under Payload/Budget) ---
    // Recurrence: DP[i][w] = max(DP[i-1][w], DP[i-1][w - wt[i]] + val[i])
    // Time Complexity: O(n * W), Space: O(n * W) or O(W)
    static KnapsackResult solveAmbulancePayloadKnapsack(
        const Core::CustomVector<MedicalEquipment>& items,
        int max_payload_capacity);

    // --- 2. Floyd-Warshall All-Pairs Shortest Path ---
    // Recurrence: d^{(k)}[i][j] = min(d^{(k-1)}[i][j], d^{(k-1)}[i][k] + d^{(k-1)}[k][j])
    // Time Complexity: O(V^3), Space: O(V^2)
    // Domain: Precomputing regional all-pairs hospital and station transit times.
    // Core benchmark comparator against Greedy Dijkstra in Scenario 1.
    static AllPairsResult floydWarshall(
        int num_nodes,
        const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj);

    // --- 3. Bellman-Ford Shortest Path ---
    // Time Complexity: O(V * E), Space: O(V)
    // Supports graphs with negative weights or penalty adjustments.
    static Core::CustomVector<double> bellmanFord(
        int num_nodes,
        int source,
        const Core::CustomVector<Core::Edge>& edge_list,
        const Core::CustomVector<int>& edge_sources,
        bool& has_negative_cycle);

    // --- 4. Longest Common Subsequence (LCS - Protocol Sequence Alignment) ---
    // Recurrence: LCS[i][j] = LCS[i-1][j-1]+1 if s1[i]==s2[j] else max(LCS[i-1][j], LCS[i][j-1])
    // Time: O(m * n). Domain: Alignment of emergency clinical triage checklists and protocol compliance.
    static int longestCommonSubsequence(const std::string& s1, const std::string& s2);

    // --- 5. Matrix Chain Multiplication (Multi-Stage Routing Optimization) ---
    // Recurrence: m[i][j] = min_{i<=k<j} (m[i][k] + m[k+1][j] + p_{i-1}p_k p_j)
    // [Roadmap Phase 2 interface]
    static int matrixChainOrder(const Core::CustomVector<int>& p);

    // --- 6. Optimal Binary Search Tree (Fast Diagnostic Query Tree) ---
    // Recurrence: e[i][j] = min_{i<=r<=j} (e[i][r-1] + e[r+1][j] + w(i,j))
    // [Roadmap Phase 2 interface]
    static double optimalBST(const Core::CustomVector<double>& p, const Core::CustomVector<double>& q, int n);

    // --- 7. Traveling Salesperson Problem (TSP - Multi-Incident Retrieval Route) ---
    // Held-Karp DP: C(S, j) = min_{i in S, i != j} (C(S - {j}, i) + dist(i, j))
    // Time Complexity: O(n^2 * 2^n)
    // [Roadmap Phase 2 interface]
    static double tspHeldKarp(const Core::CustomVector<Core::CustomVector<double>>& dist_matrix, Core::CustomVector<int>& out_tour);
};

} // namespace Algorithms

#endif // ALGORITHMS_DYNAMIC_PROGRAMMING_HPP
