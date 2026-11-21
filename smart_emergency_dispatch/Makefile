CXX ?= clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic -O3 -Iinclude

SRCS = src/algorithms/DivideConquer.cpp \
       src/algorithms/Greedy.cpp \
       src/algorithms/DynamicProgramming.cpp \
       src/algorithms/BacktrackingBB.cpp \
       src/algorithms/NetworkFlows.cpp \
       src/algorithms/StringsNumberTheory.cpp \
       src/domain/RoadNetwork.cpp \
       src/domain/Dispatcher.cpp \
       src/simulation/Simulator.cpp \
       src/simulation/Scenarios.cpp \
       src/benchmark/Benchmark.cpp

OBJS = $(SRCS:src/%.cpp=build/%.o)

TARGET = bin/dispatch_sim
TEST_ALGO_TARGET = bin/test_algorithms
TEST_DISP_TARGET = bin/test_dispatch

.PHONY: all clean test bench scenario1 scenario2 scenario3 run

all: $(TARGET) $(TEST_ALGO_TARGET) $(TEST_DISP_TARGET)

build/%.o: src/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(TARGET): $(OBJS) build/main.o
	@mkdir -p bin
	$(CXX) $(CXXFLAGS) $^ -o $@

build/main.o: src/main.cpp
	@mkdir -p build
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(TEST_ALGO_TARGET): $(OBJS) tests/test_algorithms.cpp
	@mkdir -p bin
	$(CXX) $(CXXFLAGS) $^ -o $@

$(TEST_DISP_TARGET): $(OBJS) tests/test_dispatch.cpp
	@mkdir -p bin
	$(CXX) $(CXXFLAGS) $^ -o $@

test: $(TEST_ALGO_TARGET) $(TEST_DISP_TARGET)
	@echo "================ RUNNING ALGORITHM UNIT TESTS ================"
	@./$(TEST_ALGO_TARGET)
	@echo "================ RUNNING DISPATCH DOMAIN TESTS ==============="
	@./$(TEST_DISP_TARGET)

bench: $(TARGET)
	@./$(TARGET) --bench

scenario1: $(TARGET)
	@./$(TARGET) --scenario1

scenario2: $(TARGET)
	@./$(TARGET) --scenario2

scenario3: $(TARGET)
	@./$(TARGET) --scenario3

run: $(TARGET)
	@./$(TARGET)

clean:
	rm -rf build bin *.csv *.json
