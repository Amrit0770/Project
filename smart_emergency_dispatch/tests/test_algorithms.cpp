#include "core/CustomVector.hpp"
#include "core/CustomMinHeap.hpp"
#include "core/DisjointSet.hpp"
#include "algorithms/SortingRetrieval.hpp"
#include "algorithms/DivideConquer.hpp"
#include "algorithms/Greedy.hpp"
#include "algorithms/DynamicProgramming.hpp"
#include "algorithms/BacktrackingBB.hpp"
#include "algorithms/NetworkFlows.hpp"
#include "algorithms/StringsNumberTheory.hpp"
#include <iostream>
#include <cassert>
#include <cmath>

#define ASSERT_TRUE(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "Assertion FAILED: " #cond " at " << __FILE__ << ":" << __LINE__ << std::endl; \
            return false; \
        } \
    } while (0)

#define ASSERT_FALSE(cond) ASSERT_TRUE(!(cond))

#define ASSERT_EQ(a, b) \
    do { \
        if ((a) != (b)) { \
            std::cerr << "Assertion FAILED: (" #a " == " #b ") [" << (a) << " != " << (b) << "] at " << __FILE__ << ":" << __LINE__ << std::endl; \
            return false; \
        } \
    } while (0)

bool testCustomVector() {
    Core::CustomVector<int> v;
    ASSERT_TRUE(v.empty());
    ASSERT_EQ(v.size(), static_cast<size_t>(0));

    for (int i = 0; i < 10; ++i) {
        v.push_back(i * 10);
    }
    ASSERT_EQ(v.size(), static_cast<size_t>(10));
    ASSERT_EQ(v[0], 0);
    ASSERT_EQ(v[9], 90);

    // Copy semantics
    Core::CustomVector<int> v2 = v;
    ASSERT_EQ(v2.size(), static_cast<size_t>(10));
    v2[0] = 999;
    ASSERT_EQ(v[0], 0); // Original unaltered

    // Move semantics
    Core::CustomVector<int> v3 = std::move(v2);
    ASSERT_EQ(v3.size(), static_cast<size_t>(10));
    ASSERT_EQ(v3[0], 999);

    return true;
}

bool testCustomMinHeap() {
    Core::CustomMinHeap<int> heap;
    heap.push(50);
    heap.push(20);
    heap.push(80);
    heap.push(10);
    heap.push(30);

    ASSERT_EQ(heap.size(), static_cast<size_t>(5));
    ASSERT_EQ(heap.pop(), 10);
    ASSERT_EQ(heap.pop(), 20);
    ASSERT_EQ(heap.pop(), 30);
    ASSERT_EQ(heap.pop(), 50);
    ASSERT_EQ(heap.pop(), 80);
    ASSERT_TRUE(heap.empty());
    return true;
}

bool testSortingAndRetrieval() {
    Core::CustomVector<int> arr = {42, 12, 88, 3, 56, 17, 99, 4};
    Algorithms::SortingRetrieval::mergeSort(arr);
    for (size_t i = 0; i < arr.size() - 1; ++i) {
        ASSERT_TRUE(arr[i] <= arr[i + 1]);
    }

    Core::CustomVector<int> arr2 = {100, 3, 25, 1, 99, 50};
    Algorithms::SortingRetrieval::quickSort(arr2);
    for (size_t i = 0; i < arr2.size() - 1; ++i) {
        ASSERT_TRUE(arr2[i] <= arr2[i + 1]);
    }

    int idx_iter = Algorithms::SortingRetrieval::binarySearchIterative(arr2, 50);
    ASSERT_TRUE(idx_iter >= 0);
    ASSERT_EQ(arr2[idx_iter], 50);

    int idx_rec = Algorithms::SortingRetrieval::binarySearchRecursive(arr2, 100, 0, arr2.size() - 1);
    ASSERT_TRUE(idx_rec >= 0);
    ASSERT_EQ(arr2[idx_rec], 100);

    int not_found = Algorithms::SortingRetrieval::binarySearchIterative(arr2, 999);
    ASSERT_EQ(not_found, -1);

    return true;
}

bool testDivideAndConquer() {
    // Max Subarray
    Core::CustomVector<double> vals = {-2.0, 1.0, -3.0, 4.0, -1.0, 2.0, 1.0, -5.0, 4.0};
    auto res = Algorithms::DivideConquer::findMaxSubarray(vals, 0, vals.size() - 1);
    ASSERT_EQ(res.left_idx, 3);
    ASSERT_EQ(res.right_idx, 6);
    ASSERT_TRUE(std::abs(res.max_sum - 6.0) < 1e-6);

    // Fast Power
    double p = Algorithms::DivideConquer::fastPower(2.0, 10);
    ASSERT_TRUE(std::abs(p - 1024.0) < 1e-6);

    // Celebrity Problem
    int n = 4;
    Core::CustomVector<Core::CustomVector<int>> knows(n, Core::CustomVector<int>(n, 0));
    // Person 2 is celebrity: everyone knows 2, 2 knows no one
    for (int i = 0; i < n; ++i) {
        if (i != 2) knows[i][2] = 1;
    }
    int celeb = Algorithms::DivideConquer::findHubCelebrity(n, knows);
    ASSERT_EQ(celeb, 2);

    return true;
}

bool testGreedyShortestPathAndMST() {
    int n = 5;
    Core::CustomVector<Core::CustomVector<Core::Edge>> adj(n);
    adj[0].push_back(Core::Edge(1, 10.0));
    adj[0].push_back(Core::Edge(2, 3.0));
    adj[1].push_back(Core::Edge(2, 1.0));
    adj[1].push_back(Core::Edge(3, 2.0));
    adj[2].push_back(Core::Edge(1, 4.0));
    adj[2].push_back(Core::Edge(3, 8.0));
    adj[2].push_back(Core::Edge(4, 2.0));
    adj[3].push_back(Core::Edge(4, 7.0));
    adj[4].push_back(Core::Edge(3, 9.0));

    auto path = Algorithms::Greedy::dijkstra(n, adj, 0, 3);
    ASSERT_TRUE(path.found);
    // 0 -> 2 (3) -> 1 (4) -> 3 (2) = 9.0
    ASSERT_TRUE(std::abs(path.total_cost - 9.0) < 1e-6);

    // Prim MST
    auto prim = Algorithms::Greedy::primMST(n, adj);
    ASSERT_TRUE(prim.edges.size() == 4);

    // Activity Selection
    Core::CustomVector<Algorithms::Activity> acts;
    acts.push_back(Algorithms::Activity(1, 1.0, 4.0));
    acts.push_back(Algorithms::Activity(2, 3.0, 5.0));
    acts.push_back(Algorithms::Activity(3, 0.0, 6.0));
    acts.push_back(Algorithms::Activity(4, 5.0, 7.0));
    acts.push_back(Algorithms::Activity(5, 3.0, 9.0));
    acts.push_back(Algorithms::Activity(6, 5.0, 9.0));
    acts.push_back(Algorithms::Activity(7, 6.0, 10.0));
    acts.push_back(Algorithms::Activity(8, 8.0, 11.0));
    acts.push_back(Algorithms::Activity(9, 8.0, 12.0));
    acts.push_back(Algorithms::Activity(10, 2.0, 14.0));
    acts.push_back(Algorithms::Activity(11, 12.0, 16.0));

    auto sel = Algorithms::Greedy::activitySelection(acts);
    ASSERT_EQ(sel.size(), static_cast<size_t>(4));

    return true;
}

bool testDynamicProgramming() {
    // 0/1 Knapsack
    Core::CustomVector<Algorithms::MedicalEquipment> items;
    items.push_back(Algorithms::MedicalEquipment(1, "Item1", 10, 60));
    items.push_back(Algorithms::MedicalEquipment(2, "Item2", 20, 100));
    items.push_back(Algorithms::MedicalEquipment(3, "Item3", 30, 120));

    auto knap = Algorithms::DynamicProgramming::solveAmbulancePayloadKnapsack(items, 50);
    ASSERT_EQ(knap.max_utility, 220); // 100 + 120 = 220, wt 50

    // Floyd-Warshall
    int n = 4;
    Core::CustomVector<Core::CustomVector<Core::Edge>> adj(n);
    adj[0].push_back(Core::Edge(1, 5.0));
    adj[0].push_back(Core::Edge(3, 10.0));
    adj[1].push_back(Core::Edge(2, 3.0));
    adj[2].push_back(Core::Edge(3, 1.0));

    auto fw = Algorithms::DynamicProgramming::floydWarshall(n, adj);
    ASSERT_FALSE(fw.has_negative_cycle);
    // dist 0 to 3: 0->1(5) + 1->2(3) + 2->3(1) = 9.0 < 10.0
    ASSERT_TRUE(std::abs(fw.dist[0][3] - 9.0) < 1e-6);

    // LCS
    int lcs_val = Algorithms::DynamicProgramming::longestCommonSubsequence("TRIAGE_RED", "STAGE_RED");
    ASSERT_EQ(lcs_val, 8); // T, A, G, E, _, R, E, D

    return true;
}

bool testBacktrackingAndBB() {
    // N-Queens for N=4
    Core::CustomVector<int> queens;
    bool nq_solved = Algorithms::BacktrackingBB::solveNQueens(4, queens);
    ASSERT_TRUE(nq_solved);

    // Subset Sum
    Core::CustomVector<int> set = {10, 7, 5, 18, 12, 20, 15};
    Core::CustomVector<int> subset;
    bool ss_solved = Algorithms::BacktrackingBB::subsetSum(set, 35, subset);
    ASSERT_TRUE(ss_solved);

    int sum = 0;
    for (size_t i = 0; i < subset.size(); ++i) {
        sum += set[subset[i]];
    }
    ASSERT_EQ(sum, 35);

    return true;
}

bool testNetworkFlows() {
    // Edmonds-Karp Max Flow
    int n = 4;
    Core::CustomVector<Core::CustomVector<Algorithms::FlowEdge>> adj(n);
    Algorithms::NetworkFlows::addFlowEdge(adj, 0, 1, 10);
    Algorithms::NetworkFlows::addFlowEdge(adj, 0, 2, 10);
    Algorithms::NetworkFlows::addFlowEdge(adj, 1, 2, 2);
    Algorithms::NetworkFlows::addFlowEdge(adj, 1, 3, 4);
    Algorithms::NetworkFlows::addFlowEdge(adj, 2, 3, 9);

    auto res = Algorithms::NetworkFlows::edmondsKarpMaxFlow(n, 0, 3, adj);
    ASSERT_EQ(res.max_flow, 13); // Path 0-1-3 (4), 0-2-3 (9) = 13

    // Maximum Bipartite Matching
    int n_left = 3;
    int n_right = 3;
    Core::CustomVector<Core::CustomVector<int>> bip_adj(n_left);
    bip_adj[0].push_back(0);
    bip_adj[0].push_back(1);
    bip_adj[1].push_back(1);
    bip_adj[2].push_back(2);

    auto bpm = Algorithms::NetworkFlows::maxBipartiteMatching(n_left, n_right, bip_adj);
    ASSERT_EQ(bpm.max_matching_size, 3);

    return true;
}

bool testStringsNumberTheory() {
    std::string text = "ABC ABCDAB ABCDABCDABDE";
    std::string pattern = "ABCDABD";

    auto kmp = Algorithms::StringsNumberTheory::kmpSearch(text, pattern);
    ASSERT_EQ(kmp.size(), static_cast<size_t>(1));
    ASSERT_EQ(kmp[0], 15);

    auto rk = Algorithms::StringsNumberTheory::rabinKarpSearch(text, pattern);
    ASSERT_EQ(rk.size(), static_cast<size_t>(1));
    ASSERT_EQ(rk[0], 15);

    // CRT: x = 2 mod 3, x = 3 mod 5, x = 2 mod 7 => x = 23 mod 105
    Core::CustomVector<int64_t> rem = {2, 3, 2};
    Core::CustomVector<int64_t> mod = {3, 5, 7};
    int64_t x = Algorithms::StringsNumberTheory::solveCRT(rem, mod);
    ASSERT_EQ(x, 23);

    return true;
}

int main() {
    std::cout << "[UNIT TESTS]: Commencing Custom Algorithms Validation Suite...\n";

    bool pass = true;
    pass &= testCustomVector();
    std::cout << "  [PASS] CustomVector zero-STL dynamic array\n";

    pass &= testCustomMinHeap();
    std::cout << "  [PASS] CustomMinHeap binary heap priority queue\n";

    pass &= testSortingAndRetrieval();
    std::cout << "  [PASS] Module 1: MergeSort, QuickSort, BinarySearch (Iterative & Recursive)\n";

    pass &= testDivideAndConquer();
    std::cout << "  [PASS] Module 2: MaxSubarray, FastPower, Celebrity Problem\n";

    pass &= testGreedyShortestPathAndMST();
    std::cout << "  [PASS] Module 3: Dijkstra, Prim MST, Activity Selection\n";

    pass &= testDynamicProgramming();
    std::cout << "  [PASS] Module 4: 0/1 Knapsack, Floyd-Warshall All-Pairs DP, LCS\n";

    pass &= testBacktrackingAndBB();
    std::cout << "  [PASS] Module 5: N-Queens, Subset Sum\n";

    pass &= testNetworkFlows();
    std::cout << "  [PASS] Module 6: Edmonds-Karp Max Flow, Maximum Bipartite Matching\n";

    pass &= testStringsNumberTheory();
    std::cout << "  [PASS] Module 7: KMP, Rabin-Karp, Chinese Remainder Theorem\n";

    if (pass) {
        std::cout << "\n>>> ALL 9 UNIT TEST SUITES PASSED CLEANLY (100% SUCCESS) <<<\n";
        return 0;
    } else {
        std::cerr << "\n>>> UNIT TEST FAILURES DETECTED <<<\n";
        return 1;
    }
}
