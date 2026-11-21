#ifndef ALGORITHMS_GREEDY_HPP
#define ALGORITHMS_GREEDY_HPP

#include "core/CustomVector.hpp"
#include "core/CustomMinHeap.hpp"
#include "core/DisjointSet.hpp"
#include "core/Types.hpp"
#include <string>

namespace Algorithms {

struct Activity {
    int id;
    double start_time;
    double finish_time;
    std::string description;

    Activity() : id(0), start_time(0.0), finish_time(0.0), description("") {}
    Activity(int i, double s, double f, std::string d = "") 
        : id(i), start_time(s), finish_time(f), description(d) {}
};

struct PathResult {
    double total_cost;
    Core::CustomVector<int> path;
    bool found;
};

struct MSTEdge {
    int u;
    int v;
    double weight;
    MSTEdge() : u(-1), v(-1), weight(0.0) {}
    MSTEdge(int src, int dst, double w) : u(src), v(dst), weight(w) {}

    bool operator<(const MSTEdge& other) const {
        return weight < other.weight;
    }
    bool operator>(const MSTEdge& other) const {
        return weight > other.weight;
    }
};

struct MSTResult {
    double total_weight;
    Core::CustomVector<MSTEdge> edges;
};

/**
 * @brief Module 3: Greedy Strategy
 * Mandatory Algorithms: Activity Selection, Interval Partitioning, Huffman, Dijkstra, Prim, Kruskal.
 * Domain: Shift scheduling, alert message compression, shortest-path ambulance routing, min cost layout.
 */
class Greedy {
public:
    // --- 1. Dijkstra's Shortest Path Algorithm ---
    // Time Complexity: O((V + E) log V) with CustomMinHeap, Space: O(V)
    // Core engine for urban emergency ambulance routing!
    static PathResult dijkstra(
        int num_nodes,
        const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj,
        int start_node,
        int target_node);

    // Dijkstra single-source all-destinations
    static Core::CustomVector<double> dijkstraAll(
        int num_nodes,
        const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj,
        int start_node);

    // --- 2. Prim's Minimum Spanning Tree ---
    // Time Complexity: O(E log V) with Min-Heap
    // Domain: Optimal communication backbone & sensor network layout across regional hospital hubs.
    static MSTResult primMST(
        int num_nodes,
        const Core::CustomVector<Core::CustomVector<Core::Edge>>& adj);

    // --- 3. Kruskal's Minimum Spanning Tree ---
    // Time Complexity: O(E log E) using DisjointSet (Union-Find with path compression & rank)
    // Domain: Minimum cost physical road network reinforcement.
    static MSTResult kruskalMST(
        int num_nodes,
        Core::CustomVector<MSTEdge>& edge_list);

    // --- 4. Activity Selection Problem ---
    // Greedy strategy: sort by finish time, select earliest finishing compatible activity.
    // Time Complexity: O(n log n)
    // Domain: EMS crew shift scheduling and rapid unit task allocation.
    static Core::CustomVector<Activity> activitySelection(Core::CustomVector<Activity>& activities);

    // --- 5. Interval Partitioning (EMS Staging Scheduling) ---
    // Schedules all activities using the minimum number of ambulances/crews.
    static int intervalPartitioningMinResources(Core::CustomVector<Activity>& activities);

    // --- 6. Huffman Coding (Alert Message Compression) ---
    // Compresses emergency alert payloads before transmitting over low-bandwidth tactical mesh.
    // [Roadmap Phase 2 interface]
    static std::string huffmanCompress(const std::string& message);
};

} // namespace Algorithms

#endif // ALGORITHMS_GREEDY_HPP
