#ifndef DOMAIN_HOSPITAL_HPP
#define DOMAIN_HOSPITAL_HPP

#include <string>

namespace Domain {

class Hospital {
private:
    int id_;
    std::string name_;
    int node_id_;
    int total_beds_;
    int available_beds_;
    int icu_capacity_;
    int available_icu_;
    int trauma_level_; // Level 1 (comprehensive), 2 (major), 3 (general)

public:
    Hospital() 
        : id_(0), name_(""), node_id_(-1), total_beds_(0), available_beds_(0),
          icu_capacity_(0), available_icu_(0), trauma_level_(3) {}

    Hospital(int id, std::string name, int node_id, int total_beds, int available_beds,
             int icu_capacity, int available_icu, int trauma_level = 1)
        : id_(id), name_(name), node_id_(node_id), total_beds_(total_beds),
          available_beds_(available_beds), icu_capacity_(icu_capacity),
          available_icu_(available_icu), trauma_level_(trauma_level) {}

    int getId() const { return id_; }
    const std::string& getName() const { return name_; }
    int getNodeId() const { return node_id_; }
    int getTotalBeds() const { return total_beds_; }
    int getAvailableBeds() const { return available_beds_; }
    int getIcuCapacity() const { return icu_capacity_; }
    int getAvailableIcu() const { return available_icu_; }
    int getTraumaLevel() const { return trauma_level_; }

    double getOccupancyRate() const {
        if (total_beds_ <= 0) return 1.0;
        return 1.0 - (static_cast<double>(available_beds_) / total_beds_);
    }

    bool hasCapacity(bool requires_icu = false) const {
        if (requires_icu) {
            return available_icu_ > 0 && available_beds_ > 0;
        }
        return available_beds_ > 0;
    }

    bool admitPatient(bool requires_icu = false) {
        if (!hasCapacity(requires_icu)) return false;
        available_beds_--;
        if (requires_icu) {
            available_icu_--;
        }
        return true;
    }

    void releasePatient(bool requires_icu = false) {
        if (available_beds_ < total_beds_) {
            available_beds_++;
        }
        if (requires_icu && available_icu_ < icu_capacity_) {
            available_icu_++;
        }
    }

    void setAvailableBeds(int beds) { available_beds_ = beds; }
    void setAvailableIcu(int icu) { available_icu_ = icu; }
};

} // namespace Domain

#endif // DOMAIN_HOSPITAL_HPP
