#ifndef DOMAIN_AMBULANCE_HPP
#define DOMAIN_AMBULANCE_HPP

#include "core/Types.hpp"
#include "core/CustomVector.hpp"
#include "algorithms/DynamicProgramming.hpp"
#include <string>

namespace Domain {

class Ambulance {
private:
    int id_;
    std::string callsign_;
    Core::AmbulanceType type_;
    Core::AmbulanceStatus status_;
    int current_node_id_;
    int base_node_id_;
    int max_payload_kg_;
    Core::CustomVector<Algorithms::MedicalEquipment> equipment_;
    int total_equipment_utility_;

    // Navigation and dispatch active state
    int current_incident_id_;
    int destination_node_id_;
    Core::CustomVector<int> active_route_;
    size_t active_route_step_;
    double remaining_transit_time_sec_;

public:
    Ambulance()
        : id_(0), callsign_(""), type_(Core::AmbulanceType::BLS),
          status_(Core::AmbulanceStatus::IDLE), current_node_id_(-1),
          base_node_id_(-1), max_payload_kg_(200), total_equipment_utility_(0),
          current_incident_id_(-1), destination_node_id_(-1),
          active_route_step_(0), remaining_transit_time_sec_(0.0) {}

    Ambulance(int id, std::string callsign, Core::AmbulanceType type,
              int base_node_id, int max_payload_kg = 250)
        : id_(id), callsign_(callsign), type_(type),
          status_(Core::AmbulanceStatus::IDLE), current_node_id_(base_node_id),
          base_node_id_(base_node_id), max_payload_kg_(max_payload_kg),
          total_equipment_utility_(0), current_incident_id_(-1),
          destination_node_id_(-1), active_route_step_(0),
          remaining_transit_time_sec_(0.0) {}

    int getId() const { return id_; }
    const std::string& getCallsign() const { return callsign_; }
    Core::AmbulanceType getType() const { return type_; }
    Core::AmbulanceStatus getStatus() const { return status_; }
    int getCurrentNodeId() const { return current_node_id_; }
    int getBaseNodeId() const { return base_node_id_; }
    int getMaxPayloadKg() const { return max_payload_kg_; }
    int getCurrentIncidentId() const { return current_incident_id_; }
    int getDestinationNodeId() const { return destination_node_id_; }
    double getRemainingTransitTime() const { return remaining_transit_time_sec_; }
    const Core::CustomVector<int>& getActiveRoute() const { return active_route_; }

    void setStatus(Core::AmbulanceStatus status) { status_ = status; }
    void setCurrentNodeId(int node_id) { current_node_id_ = node_id; }

    void equipLoadout(const Algorithms::KnapsackResult& loadout) {
        equipment_ = loadout.selected_equipment;
        total_equipment_utility_ = loadout.max_utility;
    }

    int getEquipmentUtility() const { return total_equipment_utility_; }

    void dispatchToScene(int incident_id, int scene_node_id, const Core::CustomVector<int>& route, double transit_time_sec) {
        current_incident_id_ = incident_id;
        destination_node_id_ = scene_node_id;
        active_route_ = route;
        active_route_step_ = 0;
        remaining_transit_time_sec_ = transit_time_sec;
        status_ = Core::AmbulanceStatus::EN_ROUTE_TO_SCENE;
    }

    void transportToHospital(int hospital_node_id, const Core::CustomVector<int>& route, double transit_time_sec) {
        destination_node_id_ = hospital_node_id;
        active_route_ = route;
        active_route_step_ = 0;
        remaining_transit_time_sec_ = transit_time_sec;
        status_ = Core::AmbulanceStatus::TRANSPORTING_TO_HOSPITAL;
    }

    void returnToBase(const Core::CustomVector<int>& route, double transit_time_sec) {
        current_incident_id_ = -1;
        destination_node_id_ = base_node_id_;
        active_route_ = route;
        active_route_step_ = 0;
        remaining_transit_time_sec_ = transit_time_sec;
        status_ = Core::AmbulanceStatus::RETURNING_TO_BASE;
    }

    void setArrived() {
        if (status_ == Core::AmbulanceStatus::EN_ROUTE_TO_SCENE) {
            current_node_id_ = destination_node_id_;
            status_ = Core::AmbulanceStatus::ON_SCENE;
            remaining_transit_time_sec_ = 0.0;
        } else if (status_ == Core::AmbulanceStatus::TRANSPORTING_TO_HOSPITAL) {
            current_node_id_ = destination_node_id_;
            status_ = Core::AmbulanceStatus::IDLE;
            remaining_transit_time_sec_ = 0.0;
        } else if (status_ == Core::AmbulanceStatus::RETURNING_TO_BASE) {
            current_node_id_ = base_node_id_;
            status_ = Core::AmbulanceStatus::IDLE;
            remaining_transit_time_sec_ = 0.0;
        }
    }

    void advanceSimulationTime(double delta_sec) {
        if (remaining_transit_time_sec_ > 0.0) {
            remaining_transit_time_sec_ -= delta_sec;
            if (remaining_transit_time_sec_ <= 0.0) {
                remaining_transit_time_sec_ = 0.0;
                setArrived();
            }
        }
    }
};

} // namespace Domain

#endif // DOMAIN_AMBULANCE_HPP
