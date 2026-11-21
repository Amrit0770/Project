#ifndef CORE_TYPES_HPP
#define CORE_TYPES_HPP

#include <string>
#include <cstdint>
#include <limits>

namespace Core {

constexpr double INF_WEIGHT = 1e9;
constexpr int INF_DIST = 1e8;

enum class AmbulanceType {
    BLS = 0, // Basic Life Support
    ALS = 1  // Advanced Life Support (Required for P1 critical patients)
};

inline const char* toString(AmbulanceType type) {
    switch (type) {
        case AmbulanceType::BLS: return "BLS (Basic)";
        case AmbulanceType::ALS: return "ALS (Advanced)";
    }
    return "UNKNOWN";
}

enum class AmbulanceStatus {
    IDLE = 0,
    EN_ROUTE_TO_SCENE = 1,
    ON_SCENE = 2,
    TRANSPORTING_TO_HOSPITAL = 3,
    RETURNING_TO_BASE = 4
};

inline const char* toString(AmbulanceStatus status) {
    switch (status) {
        case AmbulanceStatus::IDLE: return "IDLE";
        case AmbulanceStatus::EN_ROUTE_TO_SCENE: return "EN_ROUTE";
        case AmbulanceStatus::ON_SCENE: return "ON_SCENE";
        case AmbulanceStatus::TRANSPORTING_TO_HOSPITAL: return "TRANSPORTING";
        case AmbulanceStatus::RETURNING_TO_BASE: return "RETURNING";
    }
    return "UNKNOWN";
}

enum class TriagePriority {
    P1_CRITICAL = 1, // Red: Severe life-threatening (Cardiac arrest, polytrauma) -> requires ALS
    P2_URGENT   = 2, // Yellow: Serious but stable
    P3_DELAYED  = 3  // Green: Minor injury / non-emergency
};

inline double getTriageWeight(TriagePriority pri) {
    switch (pri) {
        case TriagePriority::P1_CRITICAL: return 4.0; // High penalty factor for delay
        case TriagePriority::P2_URGENT:   return 2.0;
        case TriagePriority::P3_DELAYED:  return 1.0;
    }
    return 1.0;
}

inline const char* toString(TriagePriority pri) {
    switch (pri) {
        case TriagePriority::P1_CRITICAL: return "P1-CRITICAL";
        case TriagePriority::P2_URGENT:   return "P2-URGENT";
        case TriagePriority::P3_DELAYED:  return "P3-DELAYED";
    }
    return "UNKNOWN";
}

struct GeoPoint {
    double latitude;
    double longitude;
    GeoPoint() : latitude(0.0), longitude(0.0) {}
    GeoPoint(double lat, double lon) : latitude(lat), longitude(lon) {}
};

struct Edge {
    int to;
    double weight; // Travel time in seconds
    double length; // Physical distance in meters
    int capacity;  // Flow capacity (vehicles per min or mass-flow)
    int edge_id;

    Edge() : to(-1), weight(INF_WEIGHT), length(0.0), capacity(1), edge_id(-1) {}
    Edge(int t, double w, double l = 0.0, int cap = 1, int id = -1) 
        : to(t), weight(w), length(l), capacity(cap), edge_id(id) {}
};

struct NodeCost {
    int node;
    double cost;

    bool operator<(const NodeCost& other) const {
        return cost < other.cost;
    }
    bool operator>(const NodeCost& other) const {
        return cost > other.cost;
    }
};

} // namespace Core

#endif // CORE_TYPES_HPP
