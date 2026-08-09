#!/bin/bash

EXP_ID="EXP-20260808-0842bf"

echo "================================"
echo "Starting 30 SDN Experiments"
echo "================================"

for i in $(seq 1 30)
do
    echo ""
    echo "==============================="
    echo "Running experiment $i / 30"
    echo "==============================="

    curl -s -X POST \
    http://localhost:8000/api/research/experiment/$EXP_ID/run

    echo ""

    sleep 10
done


echo ""
echo "================================"
echo "30 experiments completed"
echo "================================"
