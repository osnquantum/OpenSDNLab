#!/usr/bin/env bash

###############################################################################
# OpenSDNLab Package Installer
###############################################################################

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RESET="\033[0m"

install_apt() {

    PACKAGE=$1

    if dpkg -s "$PACKAGE" >/dev/null 2>&1
    then
        echo -e "${GREEN}✔${RESET} $PACKAGE already installed"

    else

        echo -e "${BLUE}Installing${RESET} $PACKAGE"

        sudo apt install -y "$PACKAGE"

    fi

}

echo
echo "----------------------------------------------------------"
echo "Installing Ubuntu Packages"
echo "----------------------------------------------------------"

APT_PACKAGES=(

tree
python3-sqlalchemy
python3-rich
python3-pydantic

)

for pkg in "${APT_PACKAGES[@]}"
do
    install_apt "$pkg"
done

echo
echo "----------------------------------------------------------"
echo "Python Package Verification"
echo "----------------------------------------------------------"

python3 - << EOF

modules = [
    "yaml",
    "sqlalchemy",
    "rich",
    "pydantic"
]

print()

for m in modules:

    try:

        __import__(m)

        print(f"✔ {m}")

    except Exception:

        print(f"✘ {m}")

EOF

echo
echo "Package installation completed."
