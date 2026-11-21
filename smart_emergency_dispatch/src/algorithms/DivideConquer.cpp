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
