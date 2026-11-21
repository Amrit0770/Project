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
