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
