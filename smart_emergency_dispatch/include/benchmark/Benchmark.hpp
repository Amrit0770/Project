#ifndef BENCHMARK_BENCHMARK_HPP
#define BENCHMARK_BENCHMARK_HPP

#include <string>

namespace Benchmark {

class BenchmarkSuite {
public:
    static void runAllBenchmarks();
    static void benchmarkSortingModule(int n = 10000);
    static void benchmarkShortestPathScaling();
    static void benchmarkKnapsackAmbulanceEquipping();
    static void benchmarkStringPatternSurveillance();
    static void benchmarkNetworkFlowThroughput();
};

} // namespace Benchmark

#endif // BENCHMARK_BENCHMARK_HPP
