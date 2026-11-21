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
