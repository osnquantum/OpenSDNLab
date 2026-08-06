#!/usr/bin/env bash

###############################################################################
#
# OpenSDNLab Project Structure Creator
#
# Version : 0.1.0-alpha
#
###############################################################################

set -e

GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REPORT_DIR="${PROJECT_ROOT}/bootstrap/reports"
REPORT_FILE="${REPORT_DIR}/structure_report.txt"

mkdir -p "$REPORT_DIR"

echo "OpenSDNLab Structure Report" > "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo >> "$REPORT_FILE"

###############################################################################
# Helper Functions
###############################################################################

create_dir() {

    DIR="$1"

    if [[ -d "$DIR" ]]; then
        echo -e "${GREEN}✔${RESET} $(basename "$DIR")"
    else
        mkdir -p "$DIR"
        echo -e "${BLUE}Created${RESET} $DIR"
    fi

    echo "$DIR" >> "$REPORT_FILE"

}

create_file() {

    FILE="$1"

    if [[ ! -f "$FILE" ]]; then
        touch "$FILE"
        echo -e "${BLUE}Created${RESET} $FILE"
    fi

}

create_gitkeep() {

    touch "$1/.gitkeep"

}

###############################################################################
# Banner
###############################################################################

echo
echo "----------------------------------------------------------"
echo "Creating OpenSDNLab Project Structure"
echo "----------------------------------------------------------"

###############################################################################
# Directories
###############################################################################

DIRECTORIES=(

analytics
api
captures
config
controllers
core
dashboard

database
database/backups
database/migrations
database/models
database/schema
database/seed

docs
examples
experiments
exports

logs
logs/application
logs/bootstrap
logs/errors
logs/experiments

metrics
network

plugins
plugins/analytics
plugins/controllers
plugins/metrics
plugins/topology
plugins/traffic

reports
scripts
static
templates
tests
traffic
utilities

storage
storage/cache
storage/temp
storage/uploads
storage/exports

)

for DIR in "${DIRECTORIES[@]}"
do
    create_dir "${PROJECT_ROOT}/${DIR}"
done

###############################################################################
# .gitkeep
###############################################################################

GITKEEP_DIRS=(

captures
experiments
exports

logs/application
logs/bootstrap
logs/errors
logs/experiments

storage/cache
storage/temp
storage/uploads
storage/exports

reports

)

for DIR in "${GITKEEP_DIRS[@]}"
do
    create_gitkeep "${PROJECT_ROOT}/${DIR}"
done

###############################################################################
# Root Files
###############################################################################

FILES=(

README.md
LICENSE
CHANGELOG.md
VERSION
.gitignore
requirements.txt

)

for FILE in "${FILES[@]}"
do
    create_file "${PROJECT_ROOT}/${FILE}"
done

###############################################################################
# Config Files
###############################################################################

CONFIG_FILES=(

config/settings.yaml
config/default_topology.yaml
config/controllers.yaml

)

for FILE in "${CONFIG_FILES[@]}"
do
    create_file "${PROJECT_ROOT}/${FILE}"
done

###############################################################################
# Database Files
###############################################################################

DATABASE_FILES=(

database/opensdnlab.db
database/schema/schema.sql
database/seed/seed.sql

)

for FILE in "${DATABASE_FILES[@]}"
do
    create_file "${PROJECT_ROOT}/${FILE}"
done

###############################################################################
# Log Files
###############################################################################

LOG_FILES=(

logs/application/app.log
logs/bootstrap/bootstrap.log
logs/errors/error.log

)

for FILE in "${LOG_FILES[@]}"
do
    create_file "${PROJECT_ROOT}/${FILE}"
done

###############################################################################
# Report Files
###############################################################################

REPORT_FILES=(

reports/installation_report.txt
reports/health_report.txt

)

for FILE in "${REPORT_FILES[@]}"
do
    create_file "${PROJECT_ROOT}/${FILE}"
done

###############################################################################
# Finish
###############################################################################

echo
echo "----------------------------------------------------------"
echo -e "${GREEN}Project structure successfully created.${RESET}"
echo "----------------------------------------------------------"
echo

echo "Report saved to:"
echo "$REPORT_FILE"
echo
