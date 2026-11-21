#ifndef SIMULATION_SIMULATOR_HPP
#define SIMULATION_SIMULATOR_HPP

#include "domain/Dispatcher.hpp"
#include <string>

namespace Simulation {

enum class SimulationMode {
    STEP_BY_STEP,
    CONTINUOUS,
    SCENARIO_RUN
};

class Simulator {
private:
    Domain::RoadNetwork road_network_;
    Domain::Dispatcher dispatcher_;
    double simulation_time_sec_;
    double time_step_sec_;
    bool is_running_;

public:
    Simulator();

    bool initializeStandardUrbanGrid(int grid_size = 5);
    bool loadCustomDataset(
        const std::string& nodes_csv,
        const std::string& edges_csv,
        const std::string& hospitals_csv,
        const std::string& ambulances_csv,
        const std::string& incidents_csv);

    Domain::RoadNetwork& getRoadNetwork() { return road_network_; }
    Domain::Dispatcher& getDispatcher() { return dispatcher_; }
    double getSimulationTime() const { return simulation_time_sec_; }

    void step(double delta_sec);
    void runSimulationSteps(int num_steps, double delta_sec = 10.0);

    // ASCII state rendering of live dispatcher status
    void renderLiveState() const;
    void renderCapacityAlerts() const;

    // Export metrics and history to CSV & JSON
    bool exportHistoryToCSV(const std::string& filepath) const;
    bool exportMetricsToJSON(const std::string& filepath) const;
};

} // namespace Simulation

#endif // SIMULATION_SIMULATOR_HPP
