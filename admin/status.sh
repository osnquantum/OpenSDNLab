#!/bin/bash

echo "=== Flask ==="
pgrep -af "server.app"

echo
echo "=== Controller ==="
ss -lntp | grep 6653

echo
echo "=== OVS ==="
ovs-vsctl show

echo
echo "=== Readiness ==="
curl -s http://localhost:8000/api/readiness
echo
