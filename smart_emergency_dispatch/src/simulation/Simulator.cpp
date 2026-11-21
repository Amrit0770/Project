#include "simulation/Simulator.hpp"
#include "algorithms/DynamicProgramming.hpp"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>

namespace Simulation {

Simulator::Simulator()
    : simulation_time_sec_(0.0), time_step_sec_(10.0), is_running_(false) {
    dispatcher_.setRoadNetwork(&road_network_);
}

bool Simulator::initializeStandardUrbanGrid(int grid_size) {
    int total_nodes = grid_size * grid_size;
    road_network_.resize(total_nodes);

    // 1. Create 2D Manhattan Urban Grid
    for (int r = 0; r < grid_size; ++r) {
        for (int c = 0; c < grid_size; ++c) {
            int id = r * grid_size + c;
            double lat = 12.9716 + (r * 0.015);
            double lon = 77.5946 + (c * 0.015);
            bool is_h = (id == 0 || id == grid_size - 1 || id == total_nodes - 1);
            bool is_s = (id == grid_size / 2 * grid_size + grid_size / 2);
            road_network_.setNode(id, Domain::IntersectionNode(id, "Intx_" + std::to_string(id), lat, lon, is_h, is_s));

            // Grid edges (bidirectional travel times between 60 to 180 seconds)
            if (c + 1 < grid_size) {
                int right = id + 1;
                double t = 80.0 + ((r + c) % 3) * 20.0;
                road_network_.addEdge(id, right, t, 1200.0, 15);
                road_network_.addEdge(right, id, t * 1.05, 1200.0, 15); // Slight asymmetry for real traffic
            }
            if (r + 1 < grid_size) {
                int down = id + grid_size;
                double t = 90.0 + ((r * 2 + c) % 4) * 15.0;
                road_network_.addEdge(id, down, t, 1500.0, 12);
                road_network_.addEdge(down, id, t * 1.05, 1500.0, 12);
            }
        }
    }

    // 2. Add Regional Hospitals
    // Hospital 1: St. Jude Trauma Center (Level 1) at node 0
    dispatcher_.addHospital(Domain::Hospital(1, "St. Jude Trauma Center", 0, 40, 25, 10, 6, 1));
    // Hospital 2: Metro General Hospital (Level 2) at node (grid_size - 1)
    dispatcher_.addHospital(Domain::Hospital(2, "Metro General Hospital", grid_size - 1, 30, 20, 6, 4, 2));
    // Hospital 3: East Valley Community Hospital (Level 3) at node (total_nodes - 1)
    dispatcher_.addHospital(Domain::Hospital(3, "East Valley Hospital", total_nodes - 1, 20, 14, 4, 2, 3));

    // 3. Prepare Medical Equipment catalog for Ambulance Knapsack Loadout
    Core::CustomVector<Algorithms::MedicalEquipment> catalog;
    catalog.push_back(Algorithms::MedicalEquipment(1, "Cardiac Defibrillator (AED/Pacer)", 18, 95, true));
    catalog.push_back(Algorithms::MedicalEquipment(2, "Transport Ventilator", 22, 90, true));
    catalog.push_back(Algorithms::MedicalEquipment(3, "Advanced Trauma & Hemorrhage Kit", 12, 85, true));
    catalog.push_back(Algorithms::MedicalEquipment(4, "Vital Signs Multi-Parameter Monitor", 10, 75, false));
    catalog.push_back(Algorithms::MedicalEquipment(5, "Portable Suction Unit", 8, 60, false));
    catalog.push_back(Algorithms::MedicalEquipment(6, "Infusion Pump Set", 6, 50, true));
    catalog.push_back(Algorithms::MedicalEquipment(7, "Immobilization & Cervical Collar Kit", 14, 55, false));
    catalog.push_back(Algorithms::MedicalEquipment(8, "Portable Oxygen Cylinders (2x)", 25, 80, false));

    // 4. Add Fleet Ambulances with 0/1 Knapsack optimal clinical equipment loadouts
    int station_node = grid_size / 2 * grid_size + grid_size / 2;
    for (int a = 1; a <= 6; ++a) {
        Core::AmbulanceType type = (a <= 3) ? Core::AmbulanceType::ALS : Core::AmbulanceType::BLS;
        int payload_cap = (type == Core::AmbulanceType::ALS) ? 80 : 50;
        std::string callsign = (type == Core::AmbulanceType::ALS) ? "MEDIC-" + std::to_string(a) : "AMB-" + std::to_string(a);

        Domain::Ambulance amb(a, callsign, type, station_node, payload_cap);
        auto loadout = Algorithms::DynamicProgramming::solveAmbulancePayloadKnapsack(catalog, payload_cap);
        amb.equipLoadout(loadout);
        dispatcher_.addAmbulance(amb);
    }

    // 5. Add initial emergency calls/incidents
    dispatcher_.addIncident(Domain::Incident(101, 3, Core::TriagePriority::P1_CRITICAL, true, true, 0.0, "Massive Acute Myocardial Infarction"));
    dispatcher_.addIncident(Domain::Incident(102, 11, Core::TriagePriority::P2_URGENT, false, false, 45.0, "Multi-Vehicle Collison - Fractures"));
    dispatcher_.addIncident(Domain::Incident(103, 17, Core::TriagePriority::P1_CRITICAL, true, true, 70.0, "Severe Respiratory Failure"));
    dispatcher_.addIncident(Domain::Incident(104, 21, Core::TriagePriority::P3_DELAYED, false, false, 90.0, "Laceration with controlled bleeding"));
    dispatcher_.addIncident(Domain::Incident(105, 7, Core::TriagePriority::P2_URGENT, false, false, 120.0, "Fall from height - Concussion"));

    return true;
}

void Simulator::step(double delta_sec) {
    simulation_time_sec_ += delta_sec;
    dispatcher_.stepSimulation(delta_sec);
}

void Simulator::runSimulationSteps(int num_steps, double delta_sec) {
    for (int i = 0; i < num_steps; ++i) {
        step(delta_sec);
    }
}

void Simulator::renderLiveState() const {
    std::cout << "\n========================================================================================\n";
    std::cout << "               SMART EMERGENCY DISPATCH COMMAND SYSTEM (AGY 50-60% EVAL)                \n";
    std::cout << "========================================================================================\n";
    std::cout << "Simulation Clock: " << std::fixed << std::setprecision(1) << simulation_time_sec_ << " s | "
              << "Cumulative Objective Z: " << std::setprecision(2) << dispatcher_.getObjectiveZ() << "\n\n";

    // 1. Ambulance Fleet Status Table
    std::cout << "[AMBULANCE FLEET STATUS]\n";
    std::cout << std::left << std::setw(6) << "ID"
              << std::setw(12) << "Callsign"
              << std::setw(16) << "Type"
              << std::setw(16) << "Status"
              << std::setw(12) << "Location"
              << std::setw(16) << "Destination"
              << std::setw(12) << "ETA (s)"
              << std::setw(12) << "Equip Score\n";
    std::cout << "----------------------------------------------------------------------------------------\n";

    const auto& ambs = dispatcher_.getAmbulances();
    for (size_t i = 0; i < ambs.size(); ++i) {
        const auto& a = ambs[i];
        std::cout << std::left << std::setw(6) << a.getId()
                  << std::setw(12) << a.getCallsign()
                  << std::setw(16) << Core::toString(a.getType())
                  << std::setw(16) << Core::toString(a.getStatus())
                  << std::setw(12) << ("Node " + std::to_string(a.getCurrentNodeId()))
                  << std::setw(16) << (a.getDestinationNodeId() >= 0 ? "Node " + std::to_string(a.getDestinationNodeId()) : "None")
                  << std::setw(12) << std::fixed << std::setprecision(1) << a.getRemainingTransitTime()
                  << std::setw(12) << a.getEquipmentUtility() << "\n";
    }

    // 2. Regional Hospital Occupancy & Capacity Table
    std::cout << "\n[REGIONAL HOSPITAL CAPACITIES & ICU ALLOCATION]\n";
    std::cout << std::left << std::setw(5) << "ID"
              << std::setw(28) << "Hospital Name"
              << std::setw(10) << "Node"
              << std::setw(15) << "Avail Beds"
              << std::setw(15) << "Avail ICU"
              << std::setw(12) << "Occupancy"
              << std::setw(12) << "Trauma Lvl\n";
    std::cout << "----------------------------------------------------------------------------------------\n";

    const auto& hosps = dispatcher_.getHospitals();
    for (size_t i = 0; i < hosps.size(); ++i) {
        const auto& h = hosps[i];
        double occ = h.getOccupancyRate() * 100.0;
        std::string occ_str = std::to_string(static_cast<int>(occ)) + "%";
        std::cout << std::left << std::setw(5) << h.getId()
                  << std::setw(28) << h.getName()
                  << std::setw(10) << ("Node " + std::to_string(h.getNodeId()))
                  << std::setw(15) << (std::to_string(h.getAvailableBeds()) + "/" + std::to_string(h.getTotalBeds()))
                  << std::setw(15) << (std::to_string(h.getAvailableIcu()) + "/" + std::to_string(h.getIcuCapacity()))
                  << std::setw(12) << occ_str
                  << std::setw(12) << ("Level " + std::to_string(h.getTraumaLevel())) << "\n";
    }

    // 3. Active Emergency Incidents
    std::cout << "\n[EMERGENCY INCIDENT DISPATCH QUEUE]\n";
    std::cout << std::left << std::setw(6) << "IncID"
              << std::setw(10) << "Location"
              << std::setw(15) << "Priority"
              << std::setw(10) << "Needs ALS"
              << std::setw(12) << "Status"
              << std::setw(12) << "Assigned Amb"
              << std::setw(12) << "Target Hosp"
              << "Description\n";
    std::cout << "----------------------------------------------------------------------------------------\n";

    const auto& incs = dispatcher_.getIncidents();
    for (size_t i = 0; i < incs.size(); ++i) {
        const auto& inc = incs[i];
        std::cout << std::left << std::setw(6) << inc.getId()
                  << std::setw(10) << ("Node " + std::to_string(inc.getNodeId()))
                  << std::setw(15) << Core::toString(inc.getPriority())
                  << std::setw(10) << (inc.requiresAls() ? "YES" : "NO")
                  << std::setw(12) << (inc.isAssigned() ? "ASSIGNED" : "PENDING")
                  << std::setw(12) << (inc.getAssignedAmbulanceId() > 0 ? std::to_string(inc.getAssignedAmbulanceId()) : "-")
                  << std::setw(12) << (inc.getTargetHospitalId() > 0 ? std::to_string(inc.getTargetHospitalId()) : "-")
                  << inc.getDescription() << "\n";
    }
    std::cout << "========================================================================================\n\n";
}

void Simulator::renderCapacityAlerts() const {
    const auto& hosps = dispatcher_.getHospitals();
    for (size_t i = 0; i < hosps.size(); ++i) {
        if (hosps[i].getOccupancyRate() >= 0.85) {
            std::cout << "[ALERT] Hospital '" << hosps[i].getName()
                      << "' is nearing saturation! Available ICU: " << hosps[i].getAvailableIcu()
                      << ", Available Beds: " << hosps[i].getAvailableBeds() << "\n";
        }
    }
}

bool Simulator::exportHistoryToCSV(const std::string& filepath) const {
    std::ofstream file(filepath);
    if (!file.is_open()) return false;

    file << "IncidentId,AmbulanceId,HospitalId,Priority,PickupTimeSec,HospitalTimeSec,WeightedCost,Notes\n";
    const auto& hist = dispatcher_.getHistory();
    for (size_t i = 0; i < hist.size(); ++i) {
        file << hist[i].incident_id << ","
             << hist[i].ambulance_id << ","
             << hist[i].hospital_id << ","
             << Core::toString(hist[i].priority) << ","
             << hist[i].pickup_travel_time_sec << ","
             << hist[i].hospital_travel_time_sec << ","
             << hist[i].weighted_cost << ",\""
             << hist[i].notes << "\"\n";
    }
    file.close();
    return true;
}

bool Simulator::exportMetricsToJSON(const std::string& filepath) const {
    std::ofstream file(filepath);
    if (!file.is_open()) return false;

    file << "{\n";
    file << "  \"simulation_time_sec\": " << simulation_time_sec_ << ",\n";
    file << "  \"objective_function_Z\": " << dispatcher_.getObjectiveZ() << ",\n";
    file << "  \"fleet_size\": " << dispatcher_.getAmbulances().size() << ",\n";
    file << "  \"hospitals_count\": " << dispatcher_.getHospitals().size() << ",\n";
    file << "  \"total_incidents\": " << dispatcher_.getIncidents().size() << ",\n";
    file << "  \"dispatched_records_count\": " << dispatcher_.getHistory().size() << "\n";
    file << "}\n";
    file.close();
    return true;
}

} // namespace Simulation
