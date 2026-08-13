#!/bin/bash

cd ~/OpenSDNLab

echo "Restarting OpenSDNLab..."

sudo pkill -9 -f "python3 -m server.app"

sleep 2

nohup env PYTHONPATH=/home/mininet/OpenSDNLab \
python3 -m server.app \
> /tmp/opensdn.log 2>&1 &

echo "OpenSDNLab started in background"

