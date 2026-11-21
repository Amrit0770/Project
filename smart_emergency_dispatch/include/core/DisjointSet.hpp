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
