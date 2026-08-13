#!/bin/bash

echo "Stopping OpenSDNLab..."

sudo pkill -9 -f "python3 -m server.app"

echo "Stopped"
