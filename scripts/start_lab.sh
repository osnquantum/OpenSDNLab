#!/bin/bash

PROJECT_DIR="$HOME/OpenSDNLab"

echo "======================================"
echo " Starting OpenSDNLab Environment"
echo "======================================"

cd "$PROJECT_DIR" || exit 1


echo "[1/6] Stopping old Flask API..."
sudo pkill -f "python3 -m server.app" || true


echo "[2/6] Stopping old OS-Ken controller..."
sudo pkill -f "osken-manager" || true


echo "[3/6] Cleaning stale Mininet..."
sudo mn -c >/dev/null 2>&1 || true


sleep 2


echo "[4/6] Starting OS-Ken controller..."

sudo PYTHONPATH=$PROJECT_DIR \
osken-manager \
engine.controllers.apps.simple_switch_13 \
> logs/osken.log 2>&1 &


sleep 3


if sudo ss -lntp | grep -q 6653; then
    echo "      ✓ Controller ready on port 6653"
else
    echo "      ✗ Controller failed to start"
    exit 1
fi


echo "[5/6] Starting Flask API..."

sudo PYTHONPATH=$PROJECT_DIR \
python3 -m server.app \
> logs/flask.log 2>&1 &


sleep 3


if sudo ss -lntp | grep -q 8000; then
    echo "      ✓ API ready on port 8000"
else
    echo "      ✗ API failed to start"
    exit 1
fi


echo "[6/6] Environment Status"

echo ""
echo "======================================"
echo " OpenSDNLab READY"
echo "======================================"
LAB_IP=$(hostname -I | awk '{print $1}')

echo " Controller : tcp://$LAB_IP:6653"
echo " API        : http://$LAB_IP:8000"
echo "======================================"

