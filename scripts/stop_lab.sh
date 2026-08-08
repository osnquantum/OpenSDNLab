#!/bin/bash

echo "Stopping OpenSDNLab..."

sudo pkill -f "python3 -m server.app" || true

sudo pkill -f "osken-manager" || true

sudo mn -c >/dev/null 2>&1 || true

echo "OpenSDNLab stopped"
