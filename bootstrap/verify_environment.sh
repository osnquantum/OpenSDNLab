#!/usr/bin/env bash

###############################################################################
# OpenSDNLab Environment Verification
###############################################################################

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RESET="\033[0m"

PASS=0
FAIL=0
WARN=0

check() {

    NAME="$1"
    CMD="$2"

    printf "%-30s" "$NAME"

    if eval "$CMD" >/dev/null 2>&1
    then
        echo -e "${GREEN}✔${RESET}"
        ((PASS++))
    else
        echo -e "${RED}✘${RESET}"
        ((FAIL++))
    fi

}

echo
echo "----------------------------------------------------------"
echo "Environment Verification"
echo "----------------------------------------------------------"

check "Ubuntu" "grep -qi ubuntu /etc/os-release"

check "Python3" "command -v python3"

check "Git" "command -v git"

check "Mininet" "command -v mn"

check "Open vSwitch" "command -v ovs-vsctl"

check "iperf3" "command -v iperf3"

check "tcpdump" "command -v tcpdump"

check "SQLite CLI" "command -v sqlite3"

check "Tree" "command -v tree"

check "PyYAML" "python3 -c 'import yaml'"

check "SQLAlchemy" "python3 -c 'import sqlalchemy'"

check "Rich" "python3 -c 'import rich'"

check "Pydantic" "python3 -c 'import pydantic'"

echo
echo "----------------------------------------------------------"

echo "Passed : $PASS"

echo "Failed : $FAIL"

echo "Warnings : $WARN"

echo "----------------------------------------------------------"

if [ "$FAIL" -gt 0 ]
then
    echo
    echo "Some required components are missing."
    echo
else
    echo
    echo "Environment looks good."
    echo
fi
