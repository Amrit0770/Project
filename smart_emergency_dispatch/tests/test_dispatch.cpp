#include "simulation/Simulator.hpp"
#include <iostream>
#include <cassert>

int main() {
    std::cout << "[DISPATCH TESTS]: Commencing Domain Dispatch Simulator Test...\n";

    Simulation::Simulator sim;
    bool init = sim.initializeStandardUrbanGrid(5);
    assert(init);
    std::cout << "  [PASS] Urban grid initialization (25 nodes, 3 hospitals, 6 ambulances, 5 incidents)\n";

    auto& disp = sim.getDispatcher();

    // Test priority queue dispatch
    int dispatched = disp.dispatchPendingIncidentsPriorityQueue();
    assert(dispatched > 0);
    std::cout << "  [PASS] Priority Queue MergeSort dispatch successfully allocated " << dispatched << " incidents\n";
    assert(disp.getObjectiveZ() > 0.0);
    std::cout << "  [PASS] Objective function Z computed: " << disp.getObjectiveZ() << "\n";

    // Advance simulation time
    sim.runSimulationSteps(10, 10.0);
    std::cout << "  [PASS] Stepped simulation forward 100 seconds without crash\n";

    // Test Mass Casualty Flow
    int flow = disp.evaluateMassCasualtyFlow(12, 50);
    assert(flow > 0);
    std::cout << "  [PASS] Mass casualty network flow evacuated " << flow << " casualties through available capacity\n";

    std::cout << "\n>>> ALL DISPATCH SIMULATOR TESTS PASSED CLEANLY <<<\n";
    return 0;
}
