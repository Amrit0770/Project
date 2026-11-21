#ifndef DOMAIN_INCIDENT_HPP
#define DOMAIN_INCIDENT_HPP

#include "core/Types.hpp"
#include <string>

namespace Domain {

class Incident {
private:
    int id_;
    int node_id_;
    Core::TriagePriority priority_;
    bool requires_als_;
    bool requires_icu_;
    double call_timestamp_sec_;
    std::string description_;
    bool is_assigned_;
    bool is_resolved_;
    int assigned_ambulance_id_;
    int target_hospital_id_;

public:
    Incident()
        : id_(0), node_id_(-1), priority_(Core::TriagePriority::P3_DELAYED),
          requires_als_(false), requires_icu_(false), call_timestamp_sec_(0.0),
          description_(""), is_assigned_(false), is_resolved_(false),
          assigned_ambulance_id_(-1), target_hospital_id_(-1) {}

    Incident(int id, int node_id, Core::TriagePriority priority,
             bool requires_als, bool requires_icu, double timestamp,
             std::string description = "")
        : id_(id), node_id_(node_id), priority_(priority),
          requires_als_(requires_als), requires_icu_(requires_icu),
          call_timestamp_sec_(timestamp), description_(description),
          is_assigned_(false), is_resolved_(false),
          assigned_ambulance_id_(-1), target_hospital_id_(-1) {}

    int getId() const { return id_; }
    int getNodeId() const { return node_id_; }
    Core::TriagePriority getPriority() const { return priority_; }
    double getPriorityWeight() const { return Core::getTriageWeight(priority_); }
    bool requiresAls() const { return requires_als_; }
    bool requiresIcu() const { return requires_icu_; }
    double getTimestamp() const { return call_timestamp_sec_; }
    const std::string& getDescription() const { return description_; }

    bool isAssigned() const { return is_assigned_; }
    bool isResolved() const { return is_resolved_; }
    int getAssignedAmbulanceId() const { return assigned_ambulance_id_; }
    int getTargetHospitalId() const { return target_hospital_id_; }

    void assign(int ambulance_id, int hospital_id) {
        is_assigned_ = true;
        assigned_ambulance_id_ = ambulance_id;
        target_hospital_id_ = hospital_id;
    }

    void resolve() {
        is_resolved_ = true;
    }
};

} // namespace Domain

#endif // DOMAIN_INCIDENT_HPP
