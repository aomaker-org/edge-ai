#!/usr/bin/env bash
# ==============================================================================
# FILENAME BEGIN: gemini/tools/setup_linux_oneapi.sh
# Utility: Intel oneAPI APT Repository Setup & DPC++ Compiler Installer
# Description: Registers official Intel APT keys and installs icx/icpx in Ubuntu.
# ==============================================================================

set -e

echo "================================================================================"
echo " CHECKING / INSTALLING INTEL ONEAPI DPC++ COMPILER IN WSL UBUNTU"
echo "================================================================================"

if command -v icx >/dev/null 2>&1 || [ -f /opt/intel/oneapi/setvars.sh ]; then
    echo "[SUCCESS] Intel oneAPI is already installed at /opt/intel/oneapi."
    if [ -f /opt/intel/oneapi/setvars.sh ]; then
        source /opt/intel/oneapi/setvars.sh > /dev/null 2>&1 || true
        echo "[ENV] Sourced /opt/intel/oneapi/setvars.sh"
    fi
    icx --version
    exit 0
fi

echo "[1/4] Downloading Intel GPG repository key..."
sudo mkdir -p /etc/apt/keyrings
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    | gpg --dearmor | sudo tee /etc/apt/keyrings/oneapi-archive-keyring.gpg > /dev/null

echo "[2/4] Adding Intel oneAPI APT repository..."
echo "deb [signed-by=/etc/apt/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" \
    | sudo tee /etc/apt/sources.list.d/oneAPI.list > /dev/null

echo "[3/4] Updating package index and installing intel-oneapi-compiler-dpcpp-cpp..."
sudo apt update
sudo apt install -y intel-oneapi-compiler-dpcpp-cpp

echo "[4/4] Configuring auto-sourcing for future sessions..."
echo 'source /opt/intel/oneapi/setvars.sh > /dev/null 2>&1' | sudo tee /etc/profile.d/intel-oneapi.sh > /dev/null

source /opt/intel/oneapi/setvars.sh > /dev/null 2>&1 || true

echo "--------------------------------------------------------------------------------"
echo "[SUCCESS] Intel oneAPI DPC++/C++ compiler installed successfully!"
icx --version
echo "--------------------------------------------------------------------------------"

# ==============================================================================
# FILENAME END: gemini/tools/setup_linux_oneapi.sh
# ==============================================================================
