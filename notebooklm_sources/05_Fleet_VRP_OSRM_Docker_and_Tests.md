# Source 5: Commercial Fleet CVRPTW Optimizer & OSRM Docker Infrastructure
**Project:** Smart Emergency Ambulance Routing & Hospital Allocation (Amrit Prasad, 590021684)  
This source provides the commercial fleet logistics module:
- Capacitated Vehicle Routing Problem with Time Windows (CVRPTW) using Google OR-Tools.
- Geocaching and distance matrix generation using local Docker OSRM.
- Folium HTML interactive route map generator.
- Docker and OSRM container scripts.

---

## 1. Fleet Optimizer: `vrp_optimizer.py`
```python
#!/usr/bin/env python3
"""
================================================================================
vrp_optimizer.py - Full End-to-End Fleet Route Optimizer (CVRPTW)
================================================================================
Pipeline:
  1. Human Addresses -> Geocoding (Nominatim / OpenStreetMap)
  2. Travel Times & Distances -> Matrix API (Local OSRM Docker or Public Fallback)
  3. Fleet Optimization -> Google OR-Tools (Capacities + Time Windows + Fleet)
  4. Road Geometry -> OSRM Route API (Turn-by-turn road curves)
  5. Interactive Visualization -> Folium HTML Map with Color-Coded Fleet Routes

Zero API Keys required. 100% Free & Open-Source.
================================================================================
"""

import os
import sys
import json
import time
import requests
import folium
from geopy.geocoders import Nominatim
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

# ------------------------------------------------------------------------------
# 1. Routing Engine Configuration
# ------------------------------------------------------------------------------
LOCAL_OSRM_URLS = ["http://localhost:5005", "http://localhost:5000"]
PUBLIC_OSRM_URL = "http://router.project-osrm.org"
CACHE_FILE = "geocache.json"

def get_routing_url() -> str:
    """Checks if local OSRM Docker is running (checking port 5005 then 5000); falls back to public demo server."""
    for url in LOCAL_OSRM_URLS:
        try:
            res = requests.get(f"{url}/nearest/v1/driving/0,0", timeout=0.8)
            if res.status_code == 200 and "code" in res.json():
                return url
        except Exception:
            pass
    return PUBLIC_OSRM_URL


# ------------------------------------------------------------------------------
# 2. Geocoding with Local Caching & Rate Limiting
# ------------------------------------------------------------------------------
def load_geocache() -> dict:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_geocache(cache: dict):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass

def geocode_address(address: str, geolocator, cache: dict) -> tuple:
    """Converts text address to (lat, lon) with caching."""
    if address in cache:
        return cache[address]["lat"], cache[address]["lon"]
    
    time.sleep(1.0)  # Respect Nominatim's fair use policy (1 req/sec)
    try:
        loc = geolocator.geocode(address)
        if loc:
            cache[address] = {"lat": loc.latitude, "lon": loc.longitude}
            save_geocache(cache)
            return loc.latitude, loc.longitude
        else:
            raise ValueError(f"Could not geocode address: {address}")
    except Exception as e:
        raise RuntimeError(f"Geocoding error for '{address}': {e}")


# ------------------------------------------------------------------------------
# 3. OSRM Matrix & Turn-by-Turn Geometry
# ------------------------------------------------------------------------------
def fetch_osrm_matrices(coords: list, base_url: str):
    """
    Fetches travel duration (seconds) and distance (meters) matrices.
    If the target coordinates fall outside a locally hosted OSRM map region
    (e.g., local OSRM has Monaco while coordinates are in San Francisco),
    it automatically falls back to the public global OSRM server.
    """
    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
    url = f"{base_url}/table/v1/driving/{coord_str}?annotations=distance,duration"
    
    try:
        response = requests.get(url, timeout=12)
        data = response.json()
        
        # Check if coordinates snapped from too far away (> 50 km) or returned zeros
        is_out_of_region = False
        if data.get("code") == "Ok" and "destinations" in data:
            for dest in data["destinations"]:
                if dest.get("distance", 0) > 50000:  # snapped > 50 km away
                    is_out_of_region = True
                    break
        
        if is_out_of_region and base_url != PUBLIC_OSRM_URL:
            # Silently fall back to global server for coordinates outside local map
            return fetch_osrm_matrices(coords, PUBLIC_OSRM_URL)

        if data.get("code") != "Ok":
            if base_url != PUBLIC_OSRM_URL:
                return fetch_osrm_matrices(coords, PUBLIC_OSRM_URL)
            raise RuntimeError(f"OSRM Matrix error: {data.get('message', 'Unknown error')}")
        
        durations = data["durations"]
        distances = data["distances"]
        return durations, distances
    except Exception as e:
        if base_url != PUBLIC_OSRM_URL:
            return fetch_osrm_matrices(coords, PUBLIC_OSRM_URL)
        raise e

def fetch_osrm_road_geometry(from_coord: tuple, to_coord: tuple, base_url: str):
    """Fetches real street polyline geometry (GeoJSON) between two stops."""
    from_lat, from_lon = from_coord
    to_lat, to_lon = to_coord
    url = f"{base_url}/route/v1/driving/{from_lon},{from_lat};{to_lon},{to_lat}?overview=full&geometries=geojson"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
            route = data["routes"][0]
            # If distance is suspiciously 0 or route is empty, try public server
            if route.get("distance", 0) == 0 and base_url != PUBLIC_OSRM_URL:
                return fetch_osrm_road_geometry(from_coord, to_coord, PUBLIC_OSRM_URL)
            geojson_coords = route["geometry"]["coordinates"]
            return [[lat, lon] for lon, lat in geojson_coords]
        elif base_url != PUBLIC_OSRM_URL:
            return fetch_osrm_road_geometry(from_coord, to_coord, PUBLIC_OSRM_URL)
    except Exception:
        if base_url != PUBLIC_OSRM_URL:
            return fetch_osrm_road_geometry(from_coord, to_coord, PUBLIC_OSRM_URL)
    return [list(from_coord), list(to_coord)]


# ------------------------------------------------------------------------------
# 4. Google OR-Tools CVRPTW Solver
# ------------------------------------------------------------------------------
def format_time_minutes(mins: int) -> str:
    """Converts minutes from midnight to HH:MM format."""
    hours = int(mins // 60)
    minutes = int(mins % 60)
    return f"{hours:02d}:{minutes:02d}"

def solve_cvrptw(data_model: dict):
    """
    Solves Capacitated Vehicle Routing Problem with Time Windows.
    Constraints:
      - Vehicle max capacities (e.g., packages)
      - Customer time windows (earliest and latest arrival)
      - Customer service/unloading durations
      - Depot operational hours
    """
    manager = pywrapcp.RoutingIndexManager(
        len(data_model["time_matrix"]),
        data_model["num_vehicles"],
        data_model["depot"]
    )
    routing = pywrapcp.RoutingModel(manager)

    # 1. Travel Time Callback (Arc Cost to minimize)
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # Travel time + service time at departure node
        service = data_model["service_times"][from_node]
        travel = data_model["time_matrix"][from_node][to_node]
        return int(service + travel)

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 2. Demand & Capacity Dimension
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data_model["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data_model["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity"
    )

    # 3. Time Windows Dimension
    routing.AddDimension(
        transit_callback_index,
        30,   # allow waiting time / slack up to 30 mins
        data_model["depot_time_window"][1],  # maximum route duration
        False,  # don't force start cumul to zero
        "Time"
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    # Set Time Window ranges for all customer locations
    for location_idx, time_window in enumerate(data_model["time_windows"]):
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    # Set Depot Shift start/end for each vehicle
    for vehicle_id in range(data_model["num_vehicles"]):
        start_index = routing.Start(vehicle_id)
        end_index = routing.End(vehicle_id)
        time_dimension.CumulVar(start_index).SetRange(
            data_model["depot_time_window"][0],
            data_model["depot_time_window"][1]
        )
        time_dimension.CumulVar(end_index).SetRange(
            data_model["depot_time_window"][0],
            data_model["depot_time_window"][1]
        )
        # Minimize vehicle schedule span
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(start_index))
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(end_index))

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 5

    solution = routing.SolveWithParameters(search_parameters)
    if not solution:
        return None

    # Parse and format the solution
    capacity_dimension = routing.GetDimensionOrDie("Capacity")
    total_time = 0
    total_distance = 0
    routes_output = []

    for vehicle_id in range(data_model["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = []
        route_dist = 0
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            cap_var = capacity_dimension.CumulVar(index)
            
            arr_min = solution.Min(time_var)
            arr_max = solution.Max(time_var)
            load = solution.Value(cap_var)
            
            plan_output.append({
                "node": node_index,
                "name": data_model["names"][node_index],
                "coord": data_model["coords"][node_index],
                "arrival_min": arr_min,
                "arrival_max": arr_max,
                "arrival_time_str": format_time_minutes(arr_min),
                "demand": data_model["demands"][node_index],
                "current_load": load,
                "time_window": data_model["time_windows"][node_index],
                "time_window_str": f"{format_time_minutes(data_model['time_windows'][node_index][0])}-{format_time_minutes(data_model['time_windows'][node_index][1])}"
            })
            
            prev_index = index
            index = solution.Value(routing.NextVar(index))
            next_node = manager.IndexToNode(index)
            route_dist += data_model["distance_matrix"][node_index][next_node]

        # Add depot return
        node_index = manager.IndexToNode(index)
        time_var = time_dimension.CumulVar(index)
        cap_var = capacity_dimension.CumulVar(index)
        plan_output.append({
            "node": node_index,
            "name": data_model["names"][node_index],
            "coord": data_model["coords"][node_index],
            "arrival_min": solution.Min(time_var),
            "arrival_max": solution.Max(time_var),
            "arrival_time_str": format_time_minutes(solution.Min(time_var)),
            "demand": 0,
            "current_load": solution.Value(cap_var),
            "time_window": data_model["depot_time_window"],
            "time_window_str": f"{format_time_minutes(data_model['depot_time_window'][0])}-{format_time_minutes(data_model['depot_time_window'][1])}"
        })

        route_duration = plan_output[-1]["arrival_min"] - plan_output[0]["arrival_min"]
        total_time += route_duration
        total_distance += route_dist

        routes_output.append({
            "vehicle_id": vehicle_id + 1,
            "stops": plan_output,
            "total_distance_meters": route_dist,
            "total_distance_km": round(route_dist / 1000.0, 2),
            "total_duration_minutes": route_duration
        })

    return {
        "routes": routes_output,
        "total_fleet_distance_km": round(total_distance / 1000.0, 2),
        "total_fleet_duration_minutes": total_time
    }


# ------------------------------------------------------------------------------
# 5. Interactive Folium Visualization
# ------------------------------------------------------------------------------
PALETTE = [
    "#2563EB",  # Vibrant Blue
    "#16A34A",  # Forest Green
    "#9333EA",  # Purple
    "#EA580C",  # Burnt Orange
    "#0891B2",  # Cyan
    "#E11D48"   # Red/Rose
]

def render_interactive_map(solution: dict, routing_url: str, output_html: str = "route_map.html"):
    """Creates a rich, multi-vehicle Folium Leaflet interactive map with real road geometry."""
    all_coords = []
    for r in solution["routes"]:
        for s in r["stops"]:
            all_coords.append(s["coord"])

    avg_lat = sum(c[0] for c in all_coords) / len(all_coords)
    avg_lon = sum(c[1] for c in all_coords) / len(all_coords)

    fmap = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    depot_drawn = False

    for r_idx, route in enumerate(solution["routes"]):
        color = PALETTE[r_idx % len(PALETTE)]
        vehicle_id = route["vehicle_id"]
        stops = route["stops"]

        # Only plot vehicles with active customer deliveries
        if len(stops) <= 2:
            continue

        feature_group = folium.FeatureGroup(name=f"Vehicle #{vehicle_id} ({route['total_distance_km']} km)")

        # 1. Plot real street turn-by-turn road polylines
        for i in range(len(stops) - 1):
            curr_coord = stops[i]["coord"]
            next_coord = stops[i + 1]["coord"]
            road_polyline = fetch_osrm_road_geometry(curr_coord, next_coord, routing_url)
            folium.PolyLine(
                locations=road_polyline,
                color=color,
                weight=5,
                opacity=0.85,
                tooltip=f"Vehicle {vehicle_id}: {stops[i]['name']} ➔ {stops[i+1]['name']}"
            ).add_to(feature_group)

        # 2. Add Stop Markers
        for stop_seq, stop in enumerate(stops):
            is_depot = (stop["node"] == 0)
            
            if is_depot:
                if not depot_drawn:
                    folium.Marker(
                        location=stop["coord"],
                        icon=folium.Icon(color="black", icon="home", prefix="fa"),
                        popup=folium.Popup(f"""
                        <div style="font-family: sans-serif; min-width: 180px;">
                            <h4 style="margin: 0; color: #111;">Central Distribution Hub</h4>
                            <p style="margin: 4px 0;"><b>Depot Hours:</b> {stop['time_window_str']}</p>
                            <span style="font-size: 11px; color: #666;">Starting & ending point for all fleet vehicles</span>
                        </div>
                        """, max_width=300),
                        tooltip="Central Depot"
                    ).add_to(fmap)
                    depot_drawn = True
                continue

            # Customer stop marker with sequence badge
            badge_html = f"""
            <div style="
                background-color: {color};
                border: 2px solid #ffffff;
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                border-radius: 50%;
                width: 28px;
                height: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.35);
            ">
                {stop_seq}
            </div>
            """

            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; min-width: 220px;">
                <div style="background:{color}; color:white; padding: 4px 8px; border-radius: 4px; font-weight:bold; margin-bottom: 6px;">
                    Vehicle #{vehicle_id} — Stop #{stop_seq}
                </div>
                <b>Location:</b> {stop['name']}<br/>
                <b>ETA:</b> {stop['arrival_time_str']}<br/>
                <b>Delivery Window:</b> {stop['time_window_str']}<br/>
                <b>Dropoff Demand:</b> {stop['demand']} units<br/>
                <b>Truck Load After Stop:</b> {stop['current_load']} units
            </div>
            """

            folium.Marker(
                location=stop["coord"],
                icon=folium.DivIcon(html=badge_html, icon_size=(28, 28), icon_anchor=(14, 14)),
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=f"V{vehicle_id} Stop #{stop_seq}: {stop['name']} (ETA: {stop['arrival_time_str']})"
            ).add_to(feature_group)

        feature_group.add_to(fmap)

    # Add Layer Control to toggle vehicles
    folium.LayerControl(collapsed=False).add_to(fmap)

    # Add Floating Dashboard Stats Panel
    dashboard_html = f"""
    <div style="
        position: fixed;
        bottom: 25px;
        left: 25px;
        z-index: 1000;
        background: white;
        padding: 14px 18px;
        border-radius: 8px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.2);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-size: 13px;
        line-height: 1.5;
        border-left: 6px solid #2563EB;
        max-width: 320px;
    ">
        <h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1E293B;">Fleet Route Summary</h4>
        <div><b>Total Fleet Distance:</b> {solution['total_fleet_distance_km']} km</div>
        <div><b>Total Fleet Time:</b> {solution['total_fleet_duration_minutes']} mins</div>
        <hr style="margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;"/>
        <div style="font-size: 11px; color: #64748B;">
            Routing Engine: <code>{routing_url}</code><br/>
            Engineered with OR-Tools & OSRM (100% Free)
        </div>
    </div>
    """
    fmap.get_root().html.add_child(folium.Element(dashboard_html))
    fmap.save(output_html)
    print(f"🗺️  Interactive Folium map saved to: {output_html}")


# ------------------------------------------------------------------------------
# 6. Main Execution Pipeline
# ------------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("🚀 Fleet Route Optimizer (CVRPTW) - End-to-End Pipeline")
    print("=" * 70)

    # Step 1: Detect Routing Server
    routing_url = get_routing_url()
    if "localhost" in routing_url:
        print(f"⚡ Using high-speed local OSRM Docker instance: {routing_url}")
    else:
        print(f"🌐 Local OSRM not running. Falling back to public OSRM server: {routing_url}")

    # Step 2: Define Problem Instance
    # Customer stops with human-readable addresses, demand (packages), and delivery time windows
    depot_data = {
        "name": "Central Depot (Union Square, San Francisco)",
        "address": "Union Square, San Francisco, CA, USA",
        "time_window": (480, 1080)  # 08:00 to 18:00 (minutes from midnight)
    }

    stops_data = [
        {
            "name": "Customer 1 (Fisherman's Wharf)",
            "address": "Fisherman's Wharf, San Francisco, CA",
            "demand": 4,
            "time_window": (540, 660),   # 09:00 - 11:00
            "service_time": 10           # 10 mins delivery time
        },
        {
            "name": "Customer 2 (Presidio of San Francisco)",
            "address": "Presidio of San Francisco, CA",
            "demand": 3,
            "time_window": (570, 720),   # 09:30 - 12:00
            "service_time": 10
        },
        {
            "name": "Customer 3 (Mission District)",
            "address": "Mission Dolores Park, San Francisco, CA",
            "demand": 5,
            "time_window": (600, 780),   # 10:00 - 13:00
            "service_time": 10
        },
        {
            "name": "Customer 4 (Oracle Park)",
            "address": "Oracle Park, San Francisco, CA",
            "demand": 4,
            "time_window": (660, 840),   # 11:00 - 14:00
            "service_time": 10
        },
        {
            "name": "Customer 5 (Golden Gate Park Concourse)",
            "address": "Music Concourse, San Francisco, CA",
            "demand": 6,
            "time_window": (720, 960),   # 12:00 - 16:00
            "service_time": 10
        },
        {
            "name": "Customer 6 (Twin Peaks Lookout)",
            "address": "Twin Peaks, San Francisco, CA",
            "demand": 3,
            "time_window": (780, 1020),  # 13:00 - 17:00
            "service_time": 10
        }
    ]

    fleet_config = {
        "num_vehicles": 2,
        "capacities": [15, 15]  # Each vehicle carries at most 15 packages
    }

    # Step 3: Geocode Addresses
    print("\n📍 Step 1: Geocoding Addresses via OpenStreetMap Nominatim...")
    geolocator = Nominatim(user_agent="fleet_route_optimizer/1.0 (amrit_route_demo)")
    cache = load_geocache()

    all_locations = [depot_data] + stops_data
    coords = []
    names = []
    demands = [0]
    time_windows = [depot_data["time_window"]]
    service_times = [0]

    for item in all_locations:
        names.append(item["name"])
        print(f"   Searching: {item['address']}...")
        lat, lon = geocode_address(item["address"], geolocator, cache)
        coords.append((lat, lon))
        print(f"   ↳ Found: ({lat:.5f}, {lon:.5f})")

    for stop in stops_data:
        demands.append(stop["demand"])
        time_windows.append(stop["time_window"])
        service_times.append(stop["service_time"])

    # Step 4: Fetch OSRM Matrix
    print("\n⏱️  Step 2: Calculating Driving Distance & Travel Time Matrix via OSRM...")
    durations_sec, distances_m = fetch_osrm_matrices(coords, routing_url)

    # Convert durations to minutes for the OR-Tools solver
    time_matrix_mins = [[int(round(d / 60.0)) for d in row] for row in durations_sec]
    distance_matrix_m = [[int(round(d)) for d in row] for row in distances_m]

    # Step 5: Solve VRP with OR-Tools
    print("\n🧠 Step 3: Solving Multi-Vehicle CVRPTW with Google OR-Tools...")
    data_model = {
        "time_matrix": time_matrix_mins,
        "distance_matrix": distance_matrix_m,
        "demands": demands,
        "vehicle_capacities": fleet_config["capacities"],
        "num_vehicles": fleet_config["num_vehicles"],
        "depot": 0,
        "time_windows": time_windows,
        "service_times": service_times,
        "depot_time_window": depot_data["time_window"],
        "names": names,
        "coords": coords
    }

    solution = solve_cvrptw(data_model)
    if not solution:
        print("❌ No feasible solution found! Check capacity or time window constraints.")
        sys.exit(1)

    print("\n🎉 Optimal Fleet Plan Discovered!")
    print(f"   Total Fleet Distance : {solution['total_fleet_distance_km']} km")
    print(f"   Total Fleet Time     : {solution['total_fleet_duration_minutes']} minutes")
    print("-" * 70)

    for route in solution["routes"]:
        v_id = route["vehicle_id"]
        stops = route["stops"]
        print(f"\n🚚 Vehicle #{v_id} (Distance: {route['total_distance_km']} km, Duration: {route['total_duration_minutes']} mins):")
        for idx, stop in enumerate(stops):
            if idx == 0:
                print(f"   [Start Depot] {stop['name']} | Departure: {stop['arrival_time_str']}")
            elif idx == len(stops) - 1:
                print(f"   [Return Depot] {stop['name']} | Return ETA: {stop['arrival_time_str']}")
            else:
                print(f"   Stop #{idx}: {stop['name']}")
                print(f"      ETA: {stop['arrival_time_str']} (Window: {stop['time_window_str']}) | Dropoff: {stop['demand']} pkgs (Truck Load: {stop['current_load']} pkgs)")

    # Step 6: Render Folium HTML Map
    print("\n🗺️  Step 4: Tracing Turn-by-Turn Road Geometry & Rendering HTML Map...")
    output_html = os.path.abspath("route_map.html")
    render_interactive_map(solution, routing_url, output_html)

    # Save summary json
    summary_path = os.path.abspath("route_summary.json")
    with open(summary_path, "w") as f:
        json.dump(solution, f, indent=2)
    print(f"📋 Route schedule JSON saved to: {summary_path}")

    print("\n" + "=" * 70)
    print(f"✅ Finished successfully! Open the interactive map:")
    print(f"   open {output_html}")
    print("=" * 70)

if __name__ == "__main__":
    main()

```

---

## 2. Docker & OSRM Setup: `docker-compose.yml` & `setup_osrm.sh`
### `docker-compose.yml`
```yaml
version: '3.8'

services:
  osrm:
    image: ghcr.io/project-osrm/osrm-backend
    container_name: osrm_server
    restart: unless-stopped
    ports:
      - "5005:5000"
    volumes:
      - ./osrm_data:/data
    command: osrm-routed --algorithm mld /data/map.osrm

```

### `setup_osrm.sh`
```bash
#!/usr/bin/env bash
# ==============================================================================
# setup_osrm.sh - Local OSRM Routing Engine Setup (Zero API Cost)
# ==============================================================================
# This script sets up a local Open Source Routing Machine (OSRM) backend
# using Docker. Once running, you get unlimited, instant distance matrices
# and turn-by-turn routes at http://localhost:5000 with 0 API keys and $0 cost.
# ==============================================================================

set -e

DATA_DIR="./osrm_data"
# Default map: Monaco (tiny, ~5MB, ready in 15 seconds for testing)
# Change REGION_URL to any region from https://download.geofabrik.de
DEFAULT_URL="https://download.geofabrik.de/europe/monaco-latest.osm.pbf"
REGION_URL="${1:-$DEFAULT_URL}"
FILENAME=$(basename "$REGION_URL")
BASE_NAME="${FILENAME%.osm.pbf}"

echo "========================================================"
echo "  Local OSRM Routing Engine Setup"
echo "========================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed or not in PATH."
    echo "👉 To install Docker on macOS:"
    echo "   1. Run: brew install --cask docker"
    echo "   2. Open 'Docker' from Applications to start the Docker daemon."
    echo ""
    echo "Note: The Python optimizer (vrp_optimizer.py) will automatically"
    echo "fallback to the public OSRM demo server until your local Docker is ready!"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "⚠️  Docker daemon is not running. Please start Docker Desktop and retry."
    exit 1
fi

mkdir -p "$DATA_DIR"
cd "$DATA_DIR"

if [ ! -f "$FILENAME" ]; then
    echo "📥 Downloading map extract: $REGION_URL..."
    curl -L -O "$REGION_URL"
else
    echo "✅ Map file $FILENAME already exists."
fi

echo "⚙️  Step 1/3: Extracting road network (car profile)..."
docker run -t -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua "/data/$FILENAME"

echo "⚙️  Step 2/3: Partitioning graph..."
docker run -t -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend osrm-partition "/data/$BASE_NAME.osrm"

echo "⚙️  Step 3/3: Customizing graph..."
docker run -t -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend osrm-customize "/data/$BASE_NAME.osrm"

echo "🚀 Starting OSRM server on http://localhost:5005 (avoids macOS port 5000 AirPlay collision)..."
docker stop osrm_server 2>/dev/null || true
docker rm osrm_server 2>/dev/null || true

docker run -d --name osrm_server -p 5005:5000 -v "$(pwd):/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld "/data/$BASE_NAME.osrm"

echo ""
echo "========================================================"
echo "🎉 OSRM is running locally at http://localhost:5005"
echo "   Test with: curl http://localhost:5005/nearest/v1/driving/7.42,43.73"
echo "   Stop with: docker stop osrm_server"
echo "========================================================"

```

### `requirements.txt`
```text
ortools>=9.8.3296
folium>=0.16.0
geopy>=2.4.1
requests>=2.31.0
polyline>=2.0.0

```
