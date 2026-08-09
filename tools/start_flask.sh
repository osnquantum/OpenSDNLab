#!/bin/bash

PROJECT_DIR="/home/mininet/OpenSDNLab"

cd $PROJECT_DIR


echo "================================="
echo "Cleaning old Flask process"
echo "================================="

# Kill only Flask on port 8000
sudo fuser -k 8000/tcp 2>/dev/null


# Remove old python bytecode lock issues
find . -name "*.pyc" -delete


echo "================================="
echo "Starting OpenSDNLab Flask"
echo "================================="


sudo -E bash -c "
PYTHONPATH=$PROJECT_DIR \
python3 -m server.app
"
