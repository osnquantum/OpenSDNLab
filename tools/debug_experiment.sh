#!/bin/bash

PROJECT=$HOME/OpenSDNLab
EXP_ID=$1

cd $PROJECT

echo "=== CLEANUP ==="
sudo mn -c

echo "=== START EXPERIMENT SERVER ==="

sudo fuser -k 8000/tcp 2>/dev/null || true

sudo -E bash -c "PYTHONPATH=$PROJECT python3 -m server.app" \
> tools/flask_live.log 2>&1 &

SERVER_PID=$!

echo "Waiting for Flask..."

until curl -s http://localhost:8000/api/research/experiments >/dev/null
do
    sleep 1
done

echo "Flask ready"


echo "=== RUN EXPERIMENT ==="

curl -X POST \
http://localhost:8000/api/research/experiment/$EXP_ID/run


echo ""
echo "=== CHECK CONTROLLER ==="

sudo ovs-vsctl show


echo ""
echo "=== CONTROLLER CONNECTION ==="

for sw in s1 s2 s3 s4 s5
do
    echo "--- $sw ---"
    sudo ovs-vsctl get-controller $sw 2>/dev/null || true
done


echo ""
echo "=== FLOWS ==="

for sw in s1 s2 s3 s4 s5
do
    echo "--- $sw ---"
    sudo ovs-ofctl -O OpenFlow13 dump-flows $sw 2>/dev/null || true
done


echo ""
echo "=== LAST SERVER LOG ==="

tail -100 tools/flask_live.log


kill $SERVER_PID 2>/dev/null || true

echo "DONE"
