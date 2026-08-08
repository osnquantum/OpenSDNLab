#!/bin/bash

PROJECT=$HOME/OpenSDNLab
EXP_ID=$1

if [ -z "$EXP_ID" ]; then
    echo "Usage: ./tools/run_experiment.sh EXP_ID"
    exit 1
fi

cd $PROJECT

echo "=============================="
echo " Cleaning Mininet"
echo "=============================="

sudo mn -c


echo "=============================="
echo " Starting Flask"
echo "=============================="

sudo -E bash -c "PYTHONPATH=$PROJECT python3 -m server.app" \
> flask_live.log 2>&1 &

SERVER_PID=$!


sleep 5


echo "=============================="
echo " Running Experiment"
echo "=============================="

curl -X POST \
http://localhost:8000/api/research/experiment/$EXP_ID/run


echo ""
echo "=============================="
echo " OVS Controller Status"
echo "=============================="

sudo ovs-vsctl show | grep -A3 Controller || echo "No controller attached"


echo "=============================="
echo " OpenFlow Rules"
echo "=============================="

for sw in s1 s2 s3 s4 s5
do
    echo "---- $sw ----"
    sudo ovs-ofctl -O OpenFlow13 dump-flows $sw 2>/dev/null || true
done


echo "=============================="
echo " Database Runs"
echo "=============================="

sqlite3 storage/database/opensdnlab.db \
"SELECT experiment_id,run_number,average_rtt,throughput,packet_loss FROM experiment_runs ORDER BY id DESC LIMIT 5;"


echo "=============================="
echo " Flask Last Log"
echo "=============================="

tail -50 flask_live.log


kill $SERVER_PID 2>/dev/null || true

echo "DONE"
