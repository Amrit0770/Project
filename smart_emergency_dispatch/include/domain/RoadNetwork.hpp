#ifndef DOMAIN_ROAD_NETWORK_HPP
#define DOMAIN_ROAD_NETWORK_HPP

#include "core/CustomVector.hpp"
#include "core/Types.hpp"
#include <string>

namespace Domain {

struct IntersectionNode {
    int id;
    std::string name;
    Core::GeoPoint coordinates;
    bool is_hospital;
    bool is_station;

    IntersectionNode() : id(0), name(""), coordinates(0.0, 0.0), is_hospital(false), is_station(false) {}
    IntersectionNode(int i, std::string n, double lat, double lon, bool hosp = false, bool st = false)
        : id(i), name(n), coordinates(lat, lon), is_hospital(hosp), is_station(st) {}
};

class RoadNetwork {
private:
    int num_nodes_;
    Core::CustomVector<IntersectionNode> nodes_;
    Core::CustomVector<Core::CustomVector<Core::Edge>> adj_;
    Core::CustomVector<Core::Edge> all_edges_;
    Core::CustomVector<int> edge_sources_;

public:
    explicit RoadNetwork(int num_nodes = 0);

    void resize(int num_nodes);
    int numNodes() const { return num_nodes_; }
    size_t numEdges() const { return all_edges_.size(); }

    void setNode(int id, const IntersectionNode& node);
    const IntersectionNode& getNode(int id) const;

    void addEdge(int from, int to, double travel_time_sec, double length_m = 0.0, int capacity = 10);
    void updateEdgeWeight(int from, int to, double new_travel_time_sec);
    void blockEdge(int from, int to); // Simulate road block / disaster obstacle

    const Core::CustomVector<Core::CustomVector<Core::Edge>>& getAdjacencyList() const {
        return adj_;
    }

    const Core::CustomVector<Core::Edge>& getAllEdges() const {
        return all_edges_;
    }

    const Core::CustomVector<int>& getEdgeSources() const {
        return edge_sources_;
    }

    // Load standard urban network from CSV
    bool loadFromCSV(const std::string& nodes_csv_path, const std::string& edges_csv_path);
};

} // namespace Domain

#endif // DOMAIN_ROAD_NETWORK_HPP
