#!/bin/bash

echo "=== OVS STATUS ==="

ovs-vsctl show

echo

ovs-vsctl list-br
