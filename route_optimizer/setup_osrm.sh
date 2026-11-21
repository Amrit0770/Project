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
