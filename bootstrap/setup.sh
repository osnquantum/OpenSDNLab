#!/usr/bin/env bash

##############################################################################
#
# OpenSDNLab Bootstrap Installer
#
# Version : 0.1.0-alpha
#
##############################################################################

set -e

PROJECT="OpenSDNLab"
VERSION="0.1.0-alpha"

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RESET="\033[0m"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOTSTRAP_DIR="${ROOT_DIR}/bootstrap"

clear

echo "=============================================================="
echo "                 ${PROJECT}"
echo "             Bootstrap Installer ${VERSION}"
echo "=============================================================="
echo

##############################################################################
# Functions
##############################################################################

info() {
    echo -e "${BLUE}[INFO]${RESET} $1"
}

ok() {
    echo -e "${GREEN}[ OK ]${RESET} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${RESET} $1"
}

fail() {
    echo -e "${RED}[FAIL]${RESET} $1"
}

##############################################################################
# Root Check
##############################################################################

if [[ $EUID -eq 0 ]]; then
    fail "Please run as a normal user."
    exit 1
fi

##############################################################################
# Bootstrap Directory
##############################################################################

if [[ ! -d "$BOOTSTRAP_DIR" ]]; then
    fail "bootstrap directory not found."
    exit 1
fi

ok "Bootstrap directory found"

##############################################################################
# Execute Modules
##############################################################################

MODULES=(
verify_environment.sh
install_packages.sh
create_structure.sh
initialize_database.sh
generate_configs.sh
healthcheck.sh
)

for MODULE in "${MODULES[@]}"
do

    if [[ -f "${BOOTSTRAP_DIR}/${MODULE}" ]]; then

        info "Running ${MODULE}"

        bash "${BOOTSTRAP_DIR}/${MODULE}"

        echo

    else

        warn "${MODULE} not found. Skipping."

    fi

done

echo
echo "=============================================================="
ok "OpenSDNLab installation completed."
echo "=============================================================="
