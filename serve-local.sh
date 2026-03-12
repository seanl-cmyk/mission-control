#!/bin/bash
# Serve Mission Control locally for real-time activity updates
# Usage: ./serve-local.sh [port]

PORT="${1:-8080}"
DIR="/home/telnyx-user/mission-control"

echo "🎯 Mission Control — Local Server"
echo "=================================="
echo "Dashboard: http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo ""

cd "$DIR"
python3 -m http.server "$PORT" --bind 127.0.0.1
