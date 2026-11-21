#include "domain/RoadNetwork.hpp"
#include <fstream>
#include <sstream>
#include <iostream>

namespace Domain {

RoadNetwork::RoadNetwork(int num_nodes) : num_nodes_(num_nodes) {
    if (num_nodes_ > 0) {
        resize(num_nodes_);
    }
}

void RoadNetwork::resize(int num_nodes) {
    num_nodes_ = num_nodes;
    nodes_.resize(num_nodes);
    adj_.resize(num_nodes);
    all_edges_.clear();
    edge_sources_.clear();
    for (int i = 0; i < num_nodes; ++i) {
        nodes_[i] = IntersectionNode(i, "Node_" + std::to_string(i), 0.0, 0.0);
    }
}

void RoadNetwork::setNode(int id, const IntersectionNode& node) {
    if (id >= 0 && id < num_nodes_) {
        nodes_[id] = node;
    }
}

const IntersectionNode& RoadNetwork::getNode(int id) const {
    if (id >= 0 && id < num_nodes_) {
        return nodes_[id];
    }
    static IntersectionNode dummy(-1, "INVALID", 0.0, 0.0);
    return dummy;
}

void RoadNetwork::addEdge(int from, int to, double travel_time_sec, double length_m, int capacity) {
    if (from >= 0 && from < num_nodes_ && to >= 0 && to < num_nodes_) {
        int edge_id = static_cast<int>(all_edges_.size());
        Core::Edge e(to, travel_time_sec, length_m, capacity, edge_id);
        adj_[from].push_back(e);
        all_edges_.push_back(e);
        edge_sources_.push_back(from);
    }
}

void RoadNetwork::updateEdgeWeight(int from, int to, double new_travel_time_sec) {
    if (from >= 0 && from < num_nodes_) {
        for (size_t i = 0; i < adj_[from].size(); ++i) {
            if (adj_[from][i].to == to) {
                adj_[from][i].weight = new_travel_time_sec;
                int e_id = adj_[from][i].edge_id;
                if (e_id >= 0 && static_cast<size_t>(e_id) < all_edges_.size()) {
                    all_edges_[e_id].weight = new_travel_time_sec;
                }
                break;
            }
        }
    }
}

void RoadNetwork::blockEdge(int from, int to) {
    updateEdgeWeight(from, to, Core::INF_WEIGHT);
}

bool RoadNetwork::loadFromCSV(const std::string& nodes_csv_path, const std::string& edges_csv_path) {
    std::ifstream nfile(nodes_csv_path);
    if (!nfile.is_open()) return false;

    std::string line;
    // Skip header: id,name,lat,lon,is_hospital,is_station
    std::getline(nfile, line);
    Core::CustomVector<IntersectionNode> loaded_nodes;

    while (std::getline(nfile, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string sid, name, slat, slon, shosp, sst;
        if (std::getline(ss, sid, ',') &&
            std::getline(ss, name, ',') &&
            std::getline(ss, slat, ',') &&
            std::getline(ss, slon, ',') &&
            std::getline(ss, shosp, ',') &&
            std::getline(ss, sst, ',')) {
            int id = std::stoi(sid);
            double lat = std::stod(slat);
            double lon = std::stod(slon);
            bool is_h = (std::stoi(shosp) != 0);
            bool is_s = (std::stoi(sst) != 0);
            loaded_nodes.push_back(IntersectionNode(id, name, lat, lon, is_h, is_s));
        }
    }
    nfile.close();

    resize(static_cast<int>(loaded_nodes.size()));
    for (size_t i = 0; i < loaded_nodes.size(); ++i) {
        setNode(loaded_nodes[i].id, loaded_nodes[i]);
    }

    std::ifstream efile(edges_csv_path);
    if (!efile.is_open()) return false;
    // Skip header: from,to,travel_time_sec,length_m,capacity
    std::getline(efile, line);
    while (std::getline(efile, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string sfrom, sto, stime, slen, scap;
        if (std::getline(ss, sfrom, ',') &&
            std::getline(ss, sto, ',') &&
            std::getline(ss, stime, ',') &&
            std::getline(ss, slen, ',') &&
            std::getline(ss, scap, ',')) {
            int from = std::stoi(sfrom);
            int to = std::stoi(sto);
            double t = std::stod(stime);
            double l = std::stod(slen);
            int cap = std::stoi(scap);
            addEdge(from, to, t, l, cap);
        }
    }
    efile.close();
    return true;
}

} // namespace Domain
