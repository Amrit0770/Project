# 🚚 Fleet Route Optimizer (CVRPTW)

An end-to-end, multi-vehicle Capacitated Vehicle Routing Problem with Time Windows (CVRPTW) optimizer with:
- **100% Free & Zero API Keys**: Runs out of the box with no paid APIs, no credit cards, and no billing setup.
- **Geocoding**: Converts text addresses into coordinates via OpenStreetMap Nominatim with local caching.
- **Road Distance & Matrix**: Computes high-precision driving time & distance matrices using OSRM (Open Source Routing Machine).
- **Fleet Solver**: Solves multi-vehicle routing with capacity constraints and customer time windows using Google OR-Tools.
- **Interactive Visualization**: Generates a rich, interactive Leaflet HTML map using Folium with real turn-by-turn road curves and color-coded vehicles.

---

## 🚀 Quick Start

### 1. Set Up Environment & Install Dependencies
```bash
cd route_optimizer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Optimizer
```bash
python3 vrp_optimizer.py
```
This will:
1. Geocode your depot and delivery stops.
2. Query the routing matrix.
3. Solve for the optimal vehicle routes under time-window and capacity constraints.
4. Generate `route_map.html` and `route_summary.json`.

To view the interactive map in your browser:
```bash
open route_map.html
```

---

## ⚡ Self-Hosting OSRM with Docker (Unlimited & Instant)

By default, `vrp_optimizer.py` automatically falls back to the public demo OSRM server. To achieve **instant matrix computation, zero network latency, and unlimited queries**, run OSRM locally with Docker.

### 1. Install Docker Desktop (if not already installed)
```bash
brew install --cask docker
```
*Open Docker Desktop once to initialize the background daemon.*

### 2. Run the Automated Setup Script
```bash
chmod +x setup_osrm.sh
./setup_osrm.sh
```
*Tip: To load a specific city, state, or country, pass any `.osm.pbf` URL from [Geofabrik](https://download.geofabrik.de):*
```bash
./setup_osrm.sh https://download.geofabrik.de/north-america/us/california-latest.osm.pbf
```

### 3. Verify Local OSRM
Check that OSRM is responding on port 5000:
```bash
curl http://localhost:5000/nearest/v1/driving/7.42,43.73
```
Once port 5000 is open, `vrp_optimizer.py` automatically detects it and uses your local instance.

---

## 📁 Project Structure

```
route_optimizer/
├── vrp_optimizer.py       # Core end-to-end pipeline & solver
├── setup_osrm.sh          # Docker setup script for local OSRM
├── docker-compose.yml     # Docker compose service definition
├── requirements.txt       # Python dependencies
├── geocache.json          # Cached address coordinates (persists across runs)
├── route_map.html         # Interactive Leaflet map output
├── route_summary.json     # Detailed schedule & route metrics
└── README.md              # Documentation
```
