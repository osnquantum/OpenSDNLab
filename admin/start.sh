#!/bin/bash

cd ~/OpenSDNLab

if pgrep -f "python3 -m server.app" > /dev/null
then
    echo "OpenSDNLab Flask already running"
    exit 0
fi

echo "Starting OpenSDNLab Flask..."

PYTHONPATH=/home/mininet/OpenSDNLab \
python3 -m server.app
