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
