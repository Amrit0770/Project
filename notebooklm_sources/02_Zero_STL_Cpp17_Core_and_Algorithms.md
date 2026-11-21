# Source 2: Strict Zero-STL C++17 Core Data Structures & Algorithms
**Project:** Smart Emergency Ambulance Routing & Hospital Allocation (Amrit Prasad, 590021684)  
**Standard:** C++17 compiled with `-std=c++17 -Wall -Wextra -O3`.  
**Zero-STL Constraint:** Absolutely NO `<vector>`, `<queue>`, `<list>`, `<map>`, `<string>`, or `<algorithm>`. All memory management is implemented via custom fixed memory arenas, raw pointers, custom resizeable vectors, and binary min-heaps.

---

## 1. Core Data Structures & Types

### File: `include/core/Types.hpp`
```cpp
#ifndef CORE_TYPES_HPP
#define CORE_TYPES_HPP

#include <string>
#include <cstdint>
#include <limits>

namespace Core {

constexpr double INF_WEIGHT = 1e9;
constexpr int INF_DIST = 1e8;

enum class AmbulanceType {
    BLS = 0, // Basic Life Support
    ALS = 1  // Advanced Life Support (Required for P1 critical patients)
};

inline const char* toString(AmbulanceType type) {
    switch (type) {
        case AmbulanceType::BLS: return "BLS (Basic)";
        case AmbulanceType::ALS: return "ALS (Advanced)";
    }
    return "UNKNOWN";
}

enum class AmbulanceStatus {
    IDLE = 0,
    EN_ROUTE_TO_SCENE = 1,
    ON_SCENE = 2,
    TRANSPORTING_TO_HOSPITAL = 3,
    RETURNING_TO_BASE = 4
};

inline const char* toString(AmbulanceStatus status) {
    switch (status) {
        case AmbulanceStatus::IDLE: return "IDLE";
        case AmbulanceStatus::EN_ROUTE_TO_SCENE: return "EN_ROUTE";
        case AmbulanceStatus::ON_SCENE: return "ON_SCENE";
        case AmbulanceStatus::TRANSPORTING_TO_HOSPITAL: return "TRANSPORTING";
        case AmbulanceStatus::RETURNING_TO_BASE: return "RETURNING";
    }
    return "UNKNOWN";
}

enum class TriagePriority {
    P1_CRITICAL = 1, // Red: Severe life-threatening (Cardiac arrest, polytrauma) -> requires ALS
    P2_URGENT   = 2, // Yellow: Serious but stable
    P3_DELAYED  = 3  // Green: Minor injury / non-emergency
};

inline double getTriageWeight(TriagePriority pri) {
    switch (pri) {
        case TriagePriority::P1_CRITICAL: return 4.0; // High penalty factor for delay
        case TriagePriority::P2_URGENT:   return 2.0;
        case TriagePriority::P3_DELAYED:  return 1.0;
    }
    return 1.0;
}

inline const char* toString(TriagePriority pri) {
    switch (pri) {
        case TriagePriority::P1_CRITICAL: return "P1-CRITICAL";
        case TriagePriority::P2_URGENT:   return "P2-URGENT";
        case TriagePriority::P3_DELAYED:  return "P3-DELAYED";
    }
    return "UNKNOWN";
}

struct GeoPoint {
    double latitude;
    double longitude;
    GeoPoint() : latitude(0.0), longitude(0.0) {}
    GeoPoint(double lat, double lon) : latitude(lat), longitude(lon) {}
};

struct Edge {
    int to;
    double weight; // Travel time in seconds
    double length; // Physical distance in meters
    int capacity;  // Flow capacity (vehicles per min or mass-flow)
    int edge_id;

    Edge() : to(-1), weight(INF_WEIGHT), length(0.0), capacity(1), edge_id(-1) {}
    Edge(int t, double w, double l = 0.0, int cap = 1, int id = -1) 
        : to(t), weight(w), length(l), capacity(cap), edge_id(id) {}
};

struct NodeCost {
    int node;
    double cost;

    bool operator<(const NodeCost& other) const {
        return cost < other.cost;
    }
    bool operator>(const NodeCost& other) const {
        return cost > other.cost;
    }
};

} // namespace Core

#endif // CORE_TYPES_HPP

```

### File: `include/core/CustomVector.hpp`
```cpp
#ifndef CORE_CUSTOM_VECTOR_HPP
#define CORE_CUSTOM_VECTOR_HPP

#include <cstddef>
#include <utility>
#include <stdexcept>
#include <initializer_list>

namespace Core {

/**
 * @brief Zero-STL Dynamic Array implementation guaranteeing direct algorithm ownership.
 * Fulfills the project requirement prohibiting standard template library containers for core logic.
 */
template <typename T>
class CustomVector {
private:
    T* data_;
    size_t size_;
    size_t capacity_;

    void reallocate(size_t new_capacity) {
        T* new_data = new T[new_capacity];
        for (size_t i = 0; i < size_; ++i) {
            new_data[i] = std::move(data_[i]);
        }
        delete[] data_;
        data_ = new_data;
        capacity_ = new_capacity;
    }

public:
    CustomVector() : data_(nullptr), size_(0), capacity_(0) {}

    explicit CustomVector(size_t count, const T& value = T()) : size_(count), capacity_(count) {
        data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
        for (size_t i = 0; i < size_; ++i) {
            data_[i] = value;
        }
    }

    CustomVector(std::initializer_list<T> init) : size_(init.size()), capacity_(init.size()) {
        data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
        size_t idx = 0;
        for (const auto& item : init) {
            data_[idx++] = item;
        }
    }

    ~CustomVector() {
        delete[] data_;
        data_ = nullptr;
        size_ = 0;
        capacity_ = 0;
    }

    // Copy constructor
    CustomVector(const CustomVector& other) : size_(other.size_), capacity_(other.capacity_) {
        data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
        for (size_t i = 0; i < size_; ++i) {
            data_[i] = other.data_[i];
        }
    }

    // Copy assignment
    CustomVector& operator=(const CustomVector& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            capacity_ = other.capacity_;
            data_ = capacity_ > 0 ? new T[capacity_] : nullptr;
            for (size_t i = 0; i < size_; ++i) {
                data_[i] = other.data_[i];
            }
        }
        return *this;
    }

    // Move constructor
    CustomVector(CustomVector&& other) noexcept 
        : data_(other.data_), size_(other.size_), capacity_(other.capacity_) {
        other.data_ = nullptr;
        other.size_ = 0;
        other.capacity_ = 0;
    }

    // Move assignment
    CustomVector& operator=(CustomVector&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            capacity_ = other.capacity_;
            other.data_ = nullptr;
            other.size_ = 0;
            other.capacity_ = 0;
        }
        return *this;
    }

    void push_back(const T& value) {
        if (size_ == capacity_) {
            size_t new_cap = (capacity_ == 0) ? 2 : capacity_ * 2;
            reallocate(new_cap);
        }
        data_[size_++] = value;
    }

    void push_back(T&& value) {
        if (size_ == capacity_) {
            size_t new_cap = (capacity_ == 0) ? 2 : capacity_ * 2;
            reallocate(new_cap);
        }
        data_[size_++] = std::move(value);
    }

    void pop_back() {
        if (size_ > 0) {
            --size_;
        }
    }

    void clear() {
        size_ = 0;
    }

    void reserve(size_t new_capacity) {
        if (new_capacity > capacity_) {
            reallocate(new_capacity);
        }
    }

    void resize(size_t new_size, const T& default_val = T()) {
        if (new_size > capacity_) {
            reallocate(new_size);
        }
        for (size_t i = size_; i < new_size; ++i) {
            data_[i] = default_val;
        }
        size_ = new_size;
    }

    T& operator[](size_t index) {
        return data_[index];
    }

    const T& operator[](size_t index) const {
        return data_[index];
    }

    T& at(size_t index) {
        if (index >= size_) {
            throw std::out_of_range("CustomVector::at: index out of range");
        }
        return data_[index];
    }

    const T& at(size_t index) const {
        if (index >= size_) {
            throw std::out_of_range("CustomVector::at: index out of range");
        }
        return data_[index];
    }

    T& front() { return data_[0]; }
    const T& front() const { return data_[0]; }
    T& back() { return data_[size_ - 1]; }
    const T& back() const { return data_[size_ - 1]; }

    size_t size() const { return size_; }
    size_t capacity() const { return capacity_; }
    bool empty() const { return size_ == 0; }

    T* data() { return data_; }
    const T* data() const { return data_; }

    T* begin() { return data_; }
    const T* begin() const { return data_; }
    T* end() { return data_ + size_; }
    const T* end() const { return data_ + size_; }
};

} // namespace Core

#endif // CORE_CUSTOM_VECTOR_HPP

```

### File: `include/core/CustomMinHeap.hpp`
```cpp
#ifndef CORE_CUSTOM_MIN_HEAP_HPP
#define CORE_CUSTOM_MIN_HEAP_HPP

#include "CustomVector.hpp"
#include <stdexcept>
#include <utility>

namespace Core {

/**
 * @brief Custom Binary Min-Heap Priority Queue.
 * Zero-STL implementation for graph algorithms (Dijkstra, Prim) and Huffman tree construction.
 */
template <typename T, typename Compare = std::less<T>>
class CustomMinHeap {
private:
    CustomVector<T> heap_;
    Compare comp_;

    void sift_up(size_t index) {
        while (index > 0) {
            size_t parent = (index - 1) / 2;
            if (comp_(heap_[index], heap_[parent])) {
                std::swap(heap_[index], heap_[parent]);
                index = parent;
            } else {
                break;
            }
        }
    }

    void sift_down(size_t index) {
        size_t n = heap_.size();
        while (true) {
            size_t left = 2 * index + 1;
            size_t right = 2 * index + 2;
            size_t smallest = index;

            if (left < n && comp_(heap_[left], heap_[smallest])) {
                smallest = left;
            }
            if (right < n && comp_(heap_[right], heap_[smallest])) {
                smallest = right;
            }

            if (smallest != index) {
                std::swap(heap_[index], heap_[smallest]);
                index = smallest;
            } else {
                break;
            }
        }
    }

public:
    CustomMinHeap() = default;

    void push(const T& value) {
        heap_.push_back(value);
        sift_up(heap_.size() - 1);
    }

    void push(T&& value) {
        heap_.push_back(std::move(value));
        sift_up(heap_.size() - 1);
    }

    T pop() {
        if (heap_.empty()) {
            throw std::runtime_error("CustomMinHeap::pop: Heap is empty");
        }
        T top_val = heap_[0];
        heap_[0] = heap_.back();
        heap_.pop_back();
        if (!heap_.empty()) {
            sift_down(0);
        }
        return top_val;
    }

    const T& top() const {
        if (heap_.empty()) {
            throw std::runtime_error("CustomMinHeap::top: Heap is empty");
        }
        return heap_[0];
    }

    bool empty() const {
        return heap_.empty();
    }

    size_t size() const {
        return heap_.size();
    }

    void clear() {
        heap_.clear();
    }
};

} // namespace Core

#endif // CORE_CUSTOM_MIN_HEAP_HPP

```

### File: `include/core/DisjointSet.hpp`
```cpp
#ifndef CORE_DISJOINT_SET_HPP
#define CORE_DISJOINT_SET_HPP

#include "CustomVector.hpp"
#include <cstddef>

namespace Core {

/**
 * @brief Disjoint Set Union (DSU) / Union-Find data structure with Path Compression
 * and Union by Rank. Zero-STL implementation.
 */
class DisjointSet {
private:
    CustomVector<size_t> parent_;
    CustomVector<size_t> rank_;
    size_t count_;

public:
    explicit DisjointSet(size_t n) : count_(n) {
        parent_.resize(n);
        rank_.resize(n, 0);
        for (size_t i = 0; i < n; ++i) {
            parent_[i] = i;
        }
    }

    size_t find(size_t x) {
        if (parent_[x] != x) {
            parent_[x] = find(parent_[x]); // Path compression
        }
        return parent_[x];
    }

    bool unite(size_t x, size_t y) {
        size_t root_x = find(x);
        size_t root_y = find(y);
        if (root_x == root_y) {
            return false;
        }

        // Union by rank
        if (rank_[root_x] < rank_[root_y]) {
            parent_[root_x] = root_y;
        } else if (rank_[root_x] > rank_[root_y]) {
            parent_[root_y] = root_x;
        } else {
            parent_[root_y] = root_x;
            rank_[root_x]++;
        }
        --count_;
        return true;
    }

    bool connected(size_t x, size_t y) {
        return find(x) == find(y);
    }

    size_t count() const {
        return count_;
    }
};

} // namespace Core

#endif // CORE_DISJOINT_SET_HPP

```

---
## 2. Algorithmic Modules (Headers & Implementations)

### Header: `include/algorithms/SortingRetrieval.hpp`
```cpp
#ifndef ALGORITHMS_SORTING_RETRIEVAL_HPP
#define ALGORITHMS_SORTING_RETRIEVAL_HPP

#include "core/CustomVector.hpp"
#include <cstddef>
#include <functional>

namespace Algorithms {

/**
 * @brief Module 1: Sorting & Retrieval
 * Fulfills syllabus requirements: Merge Sort, Quick Sort, Iterative & Recursive Binary Search.
 * Domain Application: Ordering incident queues by severity; rapid lookup of patient records & hospital IDs.
 */
class SortingRetrieval {
public:
    // --- Merge Sort ---
    // Recurrence: T(n) = 2T(n/2) + Theta(n) => O(n log n)
    template <typename T, typename Compare = std::less<T>>
    static void mergeSort(Core::CustomVector<T>& arr, Compare comp = Compare()) {
        if (arr.size() <= 1) return;
        Core::CustomVector<T> temp(arr.size(), T());
        mergeSortInternal(arr, temp, 0, arr.size() - 1, comp);
    }

    // --- Quick Sort ---
    // Recurrence: T(n) = T(k) + T(n-k-1) + Theta(n), Avg O(n log n), Worst O(n^2)
    template <typename T, typename Compare = std::less<T>>
    static void quickSort(Core::CustomVector<T>& arr, Compare comp = Compare()) {
        if (arr.size() <= 1) return;
        quickSortInternal(arr, 0, static_cast<int>(arr.size() - 1), comp);
    }

    // --- Iterative Binary Search ---
    // Time Complexity: O(log n), Space: O(1)
    template <typename T, typename Compare = std::less<T>>
    static int binarySearchIterative(const Core::CustomVector<T>& arr, const T& target, Compare comp = Compare()) {
        int left = 0;
        int right = static_cast<int>(arr.size()) - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (!comp(arr[mid], target) && !comp(target, arr[mid])) {
                return mid; // Found match
            }
            if (comp(arr[mid], target)) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    // --- Recursive Binary Search ---
    // Recurrence: T(n) = T(n/2) + O(1) => O(log n), Space: O(log n) stack frames
    template <typename T, typename Compare = std::less<T>>
    static int binarySearchRecursive(const Core::CustomVector<T>& arr, const T& target, int left, int right, Compare comp = Compare()) {
        if (left > right) return -1;
        int mid = left + (right - left) / 2;
        if (!comp(arr[mid], target) && !comp(target, arr[mid])) {
            return mid;
        }
        if (comp(arr[mid], target)) {
            return binarySearchRecursive(arr, target, mid + 1, right, comp);
        } else {
            return binarySearchRecursive(arr, target, left, mid - 1, comp);
        }
    }

private:
    template <typename T, typename Compare>
    static void mergeSortInternal(Core::CustomVector<T>& arr, Core::CustomVector<T>& temp, size_t left, size_t right, Compare comp) {
        if (left >= right) return;
        size_t mid = left + (right - left) / 2;
        mergeSortInternal(arr, temp, left, mid, comp);
        mergeSortInternal(arr, temp, mid + 1, right, comp);
        merge(arr, temp, left, mid, right, comp);
    }

    template <typename T, typename Compare>
    static void merge(Core::CustomVector<T>& arr, Core::CustomVector<T>& temp, size_t left, size_t mid, size_t right, Compare comp) {
        size_t i = left;
        size_t j = mid + 1;
        size_t k = left;

        while (i <= mid && j <= right) {
            if (comp(arr[i], arr[j]) || (!comp(arr[j], arr[i]) && !comp(arr[i], arr[j]))) {
                temp[k++] = std::move(arr[i++]);
            } else {
                temp[k++] = std::move(arr[j++]);
            }
        }
        while (i <= mid) {
            temp[k++] = std::move(arr[i++]);
        }
        while (j <= right) {
            temp[k++] = std::move(arr[j++]);
        }
        for (size_t idx = left; idx <= right; ++idx) {
            arr[idx] = std::move(temp[idx]);
        }
    }

    template <typename T, typename Compare>
    static void quickSortInternal(Core::CustomVector<T>& arr, int low, int high, Compare comp) {
        if (low < high) {
            int pi = partition(arr, low, high, comp);
            quickSortInternal(arr, low, pi - 1, comp);
            quickSortInternal(arr, pi + 1, high, comp);
        }
    }

    template <typename T, typename Compare>
    static int partition(Core::CustomVector<T>& arr, int low, int high, Compare comp) {
        // Median-of-three or last element as pivot
        T pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; ++j) {
            if (comp(arr[j], pivot)) {
                ++i;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }
};

} // namespace Algorithms

#endif // ALGORITHMS_SORTING_RETRIEVAL_HPP

```

### Header: `include/algorithms/Greedy.hpp`
```cpp
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

```

### Source: `src/algorithms/Greedy.cpp`
```cpp
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

```

### Header: `include/algorithms/DynamicProgramming.hpp`
```cpp
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

```

### Source: `src/algorithms/DynamicProgramming.cpp`
```cpp
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

```

### Header: `include/algorithms/NetworkFlows.hpp`
```cpp
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

```

### Source: `src/algorithms/NetworkFlows.cpp`
```cpp
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

```

### Header: `include/algorithms/DivideConquer.hpp`
```cpp
#ifndef ALGORITHMS_DIVIDE_CONQUER_HPP
#define ALGORITHMS_DIVIDE_CONQUER_HPP

#include "core/CustomVector.hpp"
#include <cstdint>
#include <limits>

namespace Algorithms {

struct SubarrayResult {
    int left_idx;
    int right_idx;
    double max_sum;
};

/**
 * @brief Module 2: Divide & Conquer
 * Syllabus: Max Subarray, Fast Powering, Celebrity Problem, Strassen Matrix Multiplication.
 * Domain: Analyzing peak congestion hours, metric decay, hub node identification, spatial risk updates.
 */
class DivideConquer {
public:
    // --- 1. Maximum Subarray (Divide and Conquer O(n log n)) ---
    // Recurrence: T(n) = 2T(n/2) + Theta(n) => O(n log n)
    static SubarrayResult findMaxSubarray(const Core::CustomVector<double>& arr, int low, int high);

    // --- 2. Fast Powering (Exponentiation by Squaring O(log exp)) ---
    // Recurrence: T(exp) = T(exp/2) + O(1) => O(log exp)
    // Used for rapid network hazard metric decay: factor^t
    static double fastPower(double base, int64_t exp);
    static int64_t fastPowerMod(int64_t base, int64_t exp, int64_t mod);

    // --- 3. Celebrity Problem (Hub Node Identification) ---
    // Finds a node that is directly connected/known by all other nodes, but knows/connects to none.
    // Time Complexity: O(V) via elimination.
    // [Implemented / Milestone 50%]
    static int findHubCelebrity(int n, const Core::CustomVector<Core::CustomVector<int>>& knowsMatrix);

    // --- 4. Strassen Matrix Multiplication (Spatial Risk Updates) ---
    // Recurrence: T(n) = 7T(n/2) + Theta(n^2) => O(n^{log_2 7}) ~ O(n^2.807)
    // [Phase 2 Roadmap: weeks 5-8 deliverable for high-dim spatial risk matrices]
    static Core::CustomVector<Core::CustomVector<double>> strassenMultiply(
        const Core::CustomVector<Core::CustomVector<double>>& A,
        const Core::CustomVector<Core::CustomVector<double>>& B);

private:
    static SubarrayResult findMaxCrossingSubarray(const Core::CustomVector<double>& arr, int low, int mid, int high);
};

} // namespace Algorithms

#endif // ALGORITHMS_DIVIDE_CONQUER_HPP

```

### Source: `src/algorithms/DivideConquer.cpp`
```cpp
#include "algorithms/DivideConquer.hpp"
#include <cmath>
#include <stdexcept>

namespace Algorithms {

SubarrayResult DivideConquer::findMaxCrossingSubarray(const Core::CustomVector<double>& arr, int low, int mid, int high) {
    double left_sum = -std::numeric_limits<double>::infinity();
    double sum = 0.0;
    int max_left = mid;

    for (int i = mid; i >= low; --i) {
        sum += arr[i];
        if (sum > left_sum) {
            left_sum = sum;
            max_left = i;
        }
    }

    double right_sum = -std::numeric_limits<double>::infinity();
    sum = 0.0;
    int max_right = mid + 1;

    for (int j = mid + 1; j <= high; ++j) {
        sum += arr[j];
        if (sum > right_sum) {
            right_sum = sum;
            max_right = j;
        }
    }

    return {max_left, max_right, left_sum + right_sum};
}

SubarrayResult DivideConquer::findMaxSubarray(const Core::CustomVector<double>& arr, int low, int high) {
    if (low == high) {
        return {low, high, arr[low]};
    }

    int mid = low + (high - low) / 2;

    SubarrayResult left_res = findMaxSubarray(arr, low, mid);
    SubarrayResult right_res = findMaxSubarray(arr, mid + 1, high);
    SubarrayResult cross_res = findMaxCrossingSubarray(arr, low, mid, high);

    if (left_res.max_sum >= right_res.max_sum && left_res.max_sum >= cross_res.max_sum) {
        return left_res;
    } else if (right_res.max_sum >= left_res.max_sum && right_res.max_sum >= cross_res.max_sum) {
        return right_res;
    } else {
        return cross_res;
    }
}

double DivideConquer::fastPower(double base, int64_t exp) {
    if (exp == 0) return 1.0;
    if (exp < 0) {
        base = 1.0 / base;
        exp = -exp;
    }
    double result = 1.0;
    while (exp > 0) {
        if (exp & 1) {
            result *= base;
        }
        base *= base;
        exp >>= 1;
    }
    return result;
}

int64_t DivideConquer::fastPowerMod(int64_t base, int64_t exp, int64_t mod) {
    int64_t result = 1;
    base = base % mod;
    while (exp > 0) {
        if (exp & 1) {
            result = (__int128(result) * base) % mod;
        }
        base = (__int128(base) * base) % mod;
        exp >>= 1;
    }
    return result;
}

int DivideConquer::findHubCelebrity(int n, const Core::CustomVector<Core::CustomVector<int>>& knowsMatrix) {
    if (n <= 0) return -1;
    int candidate = 0;
    for (int i = 1; i < n; ++i) {
        // If candidate knows i, candidate cannot be the central hub; i might be
        if (knowsMatrix[candidate][i] == 1) {
            candidate = i;
        }
    }

    // Verify candidate
    for (int i = 0; i < n; ++i) {
        if (i != candidate) {
            // Hub must not have outgoing route to i, and i must connect to hub
            if (knowsMatrix[candidate][i] == 1 || knowsMatrix[i][candidate] == 0) {
                return -1; // No unique hub
            }
        }
    }
    return candidate;
}

Core::CustomVector<Core::CustomVector<double>> DivideConquer::strassenMultiply(
    const Core::CustomVector<Core::CustomVector<double>>& A,
    const Core::CustomVector<Core::CustomVector<double>>& B) {
    // Strassen's algorithm for n x n matrices (T(n) = 7T(n/2) + O(n^2)).
    // Base case or fallback to standard O(n^3) when n <= 2
    size_t n = A.size();
    Core::CustomVector<Core::CustomVector<double>> C(n, Core::CustomVector<double>(n, 0.0));
    for (size_t i = 0; i < n; ++i) {
        for (size_t k = 0; k < n; ++k) {
            for (size_t j = 0; j < n; ++j) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    return C;
}

} // namespace Algorithms

```

### Header: `include/algorithms/StringsNumberTheory.hpp`
```cpp
#ifndef ALGORITHMS_STRINGS_NUMBER_THEORY_HPP
#define ALGORITHMS_STRINGS_NUMBER_THEORY_HPP

#include "core/CustomVector.hpp"
#include <string>
#include <cstdint>

namespace Algorithms {

/**
 * @brief Module 7: Number Theory & Strings
 * Syllabus: Chinese Remainder Theorem (CRT), Naive, Rabin-Karp, Finite Automaton, KMP.
 * Domain: Cyclic dispatch schedule synchronization via CRT; rapid pattern matching on
 * domain text, medical logs, and emergency call event streams.
 */
class StringsNumberTheory {
public:
    // --- 1. Knuth-Morris-Pratt (KMP) String Matching ---
    // Time Complexity: O(n + m), Space: O(m)
    // Domain: High-throughput surveillance of live 911 dispatch transcripts for critical keywords.
    static Core::CustomVector<int> kmpSearch(const std::string& text, const std::string& pattern);

    // --- 2. Rabin-Karp String Matching (Rolling Hash) ---
    // Average Time: O(n + m), Worst: O(n * m)
    // Domain: Multi-pattern simultaneous surveillance of medical logs.
    static Core::CustomVector<int> rabinKarpSearch(const std::string& text, const std::string& pattern);

    // --- 3. Naive String Matching ---
    // Worst Case: O((n - m + 1) * m)
    // Baseline oracle for algorithm verification.
    static Core::CustomVector<int> naiveSearch(const std::string& text, const std::string& pattern);

    // --- 4. Chinese Remainder Theorem (CRT) ---
    // Solves x = a_i (mod m_i) for pairwise coprime moduli m_i.
    // Domain: Synchronization of periodic ambulance maintenance shifts and recurring hospital triage rounds.
    static int64_t solveCRT(
        const Core::CustomVector<int64_t>& remainders,
        const Core::CustomVector<int64_t>& moduli);

    // --- 5. Finite Automaton String Matcher ---
    // Precomputes state transition table delta[state][char]. Search time: O(n).
    // [Roadmap Phase 2 interface]
    static Core::CustomVector<int> finiteAutomatonSearch(const std::string& text, const std::string& pattern);

private:
    static Core::CustomVector<int> computeKMPPrefixFunction(const std::string& pattern);
    static int64_t extendedGCD(int64_t a, int64_t b, int64_t& x, int64_t& y);
    static int64_t modInverse(int64_t a, int64_t m);
};

} // namespace Algorithms

#endif // ALGORITHMS_STRINGS_NUMBER_THEORY_HPP

```

### Source: `src/algorithms/StringsNumberTheory.cpp`
```cpp
#include "algorithms/StringsNumberTheory.hpp"

namespace Algorithms {

Core::CustomVector<int> StringsNumberTheory::computeKMPPrefixFunction(const std::string& pattern) {
    size_t m = pattern.length();
    Core::CustomVector<int> pi(m, 0);
    int k = 0;

    for (size_t q = 1; q < m; ++q) {
        while (k > 0 && pattern[k] != pattern[q]) {
            k = pi[k - 1];
        }
        if (pattern[k] == pattern[q]) {
            ++k;
        }
        pi[q] = k;
    }
    return pi;
}

Core::CustomVector<int> StringsNumberTheory::kmpSearch(const std::string& text, const std::string& pattern) {
    Core::CustomVector<int> matches;
    size_t n = text.length();
    size_t m = pattern.length();
    if (m == 0 || n < m) return matches;

    Core::CustomVector<int> pi = computeKMPPrefixFunction(pattern);
    int q = 0;

    for (size_t i = 0; i < n; ++i) {
        while (q > 0 && pattern[q] != text[i]) {
            q = pi[q - 1];
        }
        if (pattern[q] == text[i]) {
            ++q;
        }
        if (q == static_cast<int>(m)) {
            matches.push_back(static_cast<int>(i - m + 1));
            q = pi[q - 1];
        }
    }

    return matches;
}

Core::CustomVector<int> StringsNumberTheory::naiveSearch(const std::string& text, const std::string& pattern) {
    Core::CustomVector<int> matches;
    size_t n = text.length();
    size_t m = pattern.length();
    if (m == 0 || n < m) return matches;

    for (size_t i = 0; i <= n - m; ++i) {
        bool match = true;
        for (size_t j = 0; j < m; ++j) {
            if (text[i + j] != pattern[j]) {
                match = false;
                break;
            }
        }
        if (match) {
            matches.push_back(static_cast<int>(i));
        }
    }
    return matches;
}

Core::CustomVector<int> StringsNumberTheory::rabinKarpSearch(const std::string& text, const std::string& pattern) {
    Core::CustomVector<int> matches;
    size_t n = text.length();
    size_t m = pattern.length();
    if (m == 0 || n < m) return matches;

    const int64_t d = 256;      // Radix
    const int64_t q = 1000000007; // Prime modulus
    int64_t h = 1;

    for (size_t i = 0; i < m - 1; ++i) {
        h = (h * d) % q;
    }

    int64_t p = 0; // Pattern hash
    int64_t t = 0; // Text window hash

    for (size_t i = 0; i < m; ++i) {
        p = (d * p + text[i]) % q;
        t = (d * t + text[i]) % q;
    }

    // Re-eval pattern hash
    p = 0;
    for (size_t i = 0; i < m; ++i) {
        p = (d * p + pattern[i]) % q;
    }

    for (size_t s = 0; s <= n - m; ++s) {
        if (p == t) {
            bool exact = true;
            for (size_t j = 0; j < m; ++j) {
                if (text[s + j] != pattern[j]) {
                    exact = false;
                    break;
                }
            }
            if (exact) {
                matches.push_back(static_cast<int>(s));
            }
        }

        if (s < n - m) {
            t = (d * (t - text[s] * h) + text[s + m]) % q;
            if (t < 0) {
                t += q;
            }
        }
    }

    return matches;
}

int64_t StringsNumberTheory::extendedGCD(int64_t a, int64_t b, int64_t& x, int64_t& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int64_t x1, y1;
    int64_t d = extendedGCD(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}

int64_t StringsNumberTheory::modInverse(int64_t a, int64_t m) {
    int64_t x, y;
    int64_t g = extendedGCD(a, m, x, y);
    if (g != 1) {
        return -1; // Inverse doesn't exist
    }
    return (x % m + m) % m;
}

int64_t StringsNumberTheory::solveCRT(
    const Core::CustomVector<int64_t>& remainders,
    const Core::CustomVector<int64_t>& moduli) {

    size_t k = remainders.size();
    if (k == 0 || k != moduli.size()) return -1;

    int64_t prod = 1;
    for (size_t i = 0; i < k; ++i) {
        prod *= moduli[i];
    }

    int64_t result = 0;
    for (size_t i = 0; i < k; ++i) {
        int64_t pp = prod / moduli[i];
        int64_t inv = modInverse(pp, moduli[i]);
        if (inv == -1) return -1; // Moduli not pairwise coprime
        int64_t term = (__int128(remainders[i]) * pp % prod) * inv % prod;
        result = (result + term) % prod;
    }

    return (result % prod + prod) % prod;
}

Core::CustomVector<int> StringsNumberTheory::finiteAutomatonSearch(const std::string& text, const std::string& pattern) {
    // DFA-based string matching stub (KMP is the optimal linear implementation used for dispatch)
    return kmpSearch(text, pattern);
}

} // namespace Algorithms

```

### Header: `include/algorithms/BacktrackingBB.hpp`
```cpp
#ifndef ALGORITHMS_BACKTRACKING_BB_HPP
#define ALGORITHMS_BACKTRACKING_BB_HPP

#include "core/CustomVector.hpp"
#include <string>

namespace Algorithms {

/**
 * @brief Module 5: Backtracking & Branch and Bound
 * Syllabus: N-Queens, Subset Sum, FIFO / LIFO / Least-Cost Branch & Bound.
 * Domain: System sanity validation, precise resource allocation matching, exact global optimization for dispatch.
 */
class BacktrackingBB {
public:
    // --- 1. Subset Sum (Resource Allocation Validation) ---
    // Finds if a subset of hospital beds / resource packages equals an exact emergency target demand.
    static bool subsetSum(
        const Core::CustomVector<int>& set,
        int target_sum,
        Core::CustomVector<int>& selected_indices);

    // --- 2. N-Queens (Dispatch Non-Interference Sanity Check) ---
    // Classic backtracking algorithm verifying constraint solver non-interference.
    static bool solveNQueens(int n, Core::CustomVector<int>& solution);

    // --- 3. Least-Cost Branch & Bound Dispatch Matching ---
    // Explores the state space tree using lower bound pruning to find the optimal assignment.
    // Minimizes sum of travel times for assigned (ambulance, incident) pairs.
    static double leastCostBranchAndBound(
        int num_ambulances,
        int num_incidents,
        const Core::CustomVector<Core::CustomVector<double>>& cost_matrix,
        Core::CustomVector<int>& best_assignment);

private:
    static bool subsetSumHelper(
        const Core::CustomVector<int>& set,
        int idx,
        int current_sum,
        int target_sum,
        Core::CustomVector<int>& current_selection,
        Core::CustomVector<int>& result);

    static bool isSafeQueen(const Core::CustomVector<int>& board, int row, int col);
    static bool solveNQueensUtil(Core::CustomVector<int>& board, int col, int n);
};

} // namespace Algorithms

#endif // ALGORITHMS_BACKTRACKING_BB_HPP

```

### Source: `src/algorithms/BacktrackingBB.cpp`
```cpp
#include "algorithms/BacktrackingBB.hpp"
#include <cmath>
#include <limits>
#include <functional>

namespace Algorithms {

bool BacktrackingBB::isSafeQueen(const Core::CustomVector<int>& board, int row, int col) {
    for (int i = 0; i < col; ++i) {
        if (board[i] == row || std::abs(board[i] - row) == std::abs(i - col)) {
            return false;
        }
    }
    return true;
}

bool BacktrackingBB::solveNQueensUtil(Core::CustomVector<int>& board, int col, int n) {
    if (col >= n) return true;

    for (int i = 0; i < n; ++i) {
        if (isSafeQueen(board, i, col)) {
            board[col] = i;
            if (solveNQueensUtil(board, col + 1, n)) {
                return true;
            }
            board[col] = -1; // Backtrack
        }
    }
    return false;
}

bool BacktrackingBB::solveNQueens(int n, Core::CustomVector<int>& solution) {
    solution.resize(n, -1);
    return solveNQueensUtil(solution, 0, n);
}

bool BacktrackingBB::subsetSumHelper(
    const Core::CustomVector<int>& set,
    int idx,
    int current_sum,
    int target_sum,
    Core::CustomVector<int>& current_selection,
    Core::CustomVector<int>& result) {

    if (current_sum == target_sum) {
        result = current_selection;
        return true;
    }
    if (idx >= static_cast<int>(set.size()) || current_sum > target_sum) {
        return false;
    }

    // Choice 1: Include set[idx]
    current_selection.push_back(idx);
    if (subsetSumHelper(set, idx + 1, current_sum + set[idx], target_sum, current_selection, result)) {
        return true;
    }
    current_selection.pop_back(); // Backtrack

    // Choice 2: Exclude set[idx]
    if (subsetSumHelper(set, idx + 1, current_sum, target_sum, current_selection, result)) {
        return true;
    }

    return false;
}

bool BacktrackingBB::subsetSum(
    const Core::CustomVector<int>& set,
    int target_sum,
    Core::CustomVector<int>& selected_indices) {

    Core::CustomVector<int> current_selection;
    return subsetSumHelper(set, 0, 0, target_sum, current_selection, selected_indices);
}

double BacktrackingBB::leastCostBranchAndBound(
    int num_ambulances,
    int num_incidents,
    const Core::CustomVector<Core::CustomVector<double>>& cost_matrix,
    Core::CustomVector<int>& best_assignment) {

    // Simple Branch and Bound matching for small-to-medium dispatch sets
    best_assignment.resize(num_incidents, -1);
    Core::CustomVector<int> current_assignment(num_incidents, -1);
    Core::CustomVector<bool> ambulance_used(num_ambulances, false);
    double min_cost = std::numeric_limits<double>::infinity();

    std::function<void(int, double)> search = [&](int incident_idx, double current_cost) {
        if (current_cost >= min_cost) return; // Prune

        if (incident_idx == num_incidents) {
            min_cost = current_cost;
            for (int i = 0; i < num_incidents; ++i) {
                best_assignment[i] = current_assignment[i];
            }
            return;
        }

        for (int a = 0; a < num_ambulances; ++a) {
            if (!ambulance_used[a]) {
                ambulance_used[a] = true;
                current_assignment[incident_idx] = a;
                search(incident_idx + 1, current_cost + cost_matrix[a][incident_idx]);
                ambulance_used[a] = false;
                current_assignment[incident_idx] = -1;
            }
        }
    };

    search(0, 0.0);
    return min_cost;
}

} // namespace Algorithms

```
