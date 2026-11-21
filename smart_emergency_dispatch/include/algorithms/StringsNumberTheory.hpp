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
