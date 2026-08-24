#!/bin/bash

cd /home/mininet/OpenSDNLab

printf '\nRestarting OpenSDNLab...\n'

sudo pkill -9 -f "[p]ython3 -m server.app" 2>/dev/null || true \
    >/dev/null 2>&1 || true

sleep 2

nohup env PYTHONPATH=/home/mininet/OpenSDNLab \
    python3 -m server.app \
    >/tmp/opensdn.log 2>&1 &

printf 'OpenSDNLab started in background\n\n'
