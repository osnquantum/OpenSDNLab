#!/bin/bash

PROJECT_DIR="$HOME/OpenSDNLab"
PID_FILE="$PROJECT_DIR/logs/flask.pid"

cd "$PROJECT_DIR" || exit 1

echo "Stopping old OpenSDNLab API..."

# Kill old Flask using PID file first
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    sudo kill -9 "$OLD_PID" 2>/dev/null || true
    rm -f "$PID_FILE"
fi

# Kill remaining Flask processes
sudo pkill -9 -f "python3 -m server.app" 2>/dev/null || true
sudo pkill -9 -f "sudo PYTHONPATH=.*server.app" 2>/dev/null || true

sleep 3


echo "Checking port 8000..."

sudo fuser -k 8000/tcp 2>/dev/null || true

sleep 2


echo "Starting OpenSDNLab API..."

PYTHONPATH="$PROJECT_DIR" \
python3 -m server.app \
> logs/flask.log 2>&1 &


PID=$!

echo $PID > "$PID_FILE"


sleep 3


if ss -lnt | grep -q ":8000"; then
    echo "✓ Flask running PID=$PID"
    echo "✓ API ready on port 8000"
else
    echo "✗ Flask failed"
    exit 1
fi
