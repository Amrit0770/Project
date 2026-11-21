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
