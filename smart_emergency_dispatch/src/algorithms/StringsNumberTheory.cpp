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
