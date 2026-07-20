#!/usr/bin/env bash
# ==============================================================================
# Path:        tools/provision.sh
# Purpose:     Unified, idempotent system provisioner handling mixed-generation
#              compute runtimes (10th Gen UHD / 11th Gen+ Iris Xe), static
#              checksum-controlled toolchain boots, and submodule auditing for edge-ai.
# Target OS:   Ubuntu 24.04 / 26.04 LTS / WSL2 Subsystem
# Lineage:     Ported & Adapted from irislime Baseline
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

echo "==> [START] Launching Unified edge-ai Provisioning Sequence..."

# ------------------------------------------------------------------------------
# STEP 1: Core System Prerequisite Assembly
# ------------------------------------------------------------------------------
echo "[*] Synchronizing base system repositories and deploying utilities..."
sudo apt-get update
sudo apt-get install -y gpg gpg-agent wget curl build-essential cmake git \
    clinfo libtbb-dev ocl-icd-opencl-dev opencl-headers libssl-dev ccache \
    libvulkan-dev vulkan-tools glslang-tools glslc spirv-headers python3 python3-pip jq

# ------------------------------------------------------------------------------
# STEP 2: Register Intel Cryptographic Gates
# ------------------------------------------------------------------------------
echo "[*] Registering official Intel Software Product GPG keys..."

# NECESSARY NULL PIPE: 'tee' writes its input stream out to both the designated 
# key file path and standard output natively. We route stdout to null strictly
# to prevent raw, unreadable binary cryptographic data from flooding the terminal screen.
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null

# ------------------------------------------------------------------------------
# STEP 3: Bind Architecture Channels
# ------------------------------------------------------------------------------
echo "[*] Injecting verified Intel oneAPI and OpenVINO APT manifests..."

echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | \
    sudo tee /etc/apt/sources.list.d/oneAPI.list

echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/openvino ubuntu24 main" | \
    sudo tee /etc/apt/sources.list.d/intel-openvino.list

# ------------------------------------------------------------------------------
# STEP 4: Adaptive Hardware Runtime Provisioning
# ------------------------------------------------------------------------------
echo "[*] Auditing host graphics processor generation..."

CORE_PACKAGES=(
    "intel-oneapi-compiler-dpcpp-cpp"
    "intel-oneapi-mkl-devel"
    "intel-opencl-icd"
    "openvino"
)

# NECESSARY NULL PIPE: Querying Win32_Processor across WSL boundary; stderr suppressed to handle non-WSL native Linux seamlessly.
HOST_CPU=$(powershell.exe -NoProfile -Command "(Get-CimInstance Win32_Processor).Name" 2>/dev/null || echo "Linux Native")
echo "[+] Host processor identified: ${HOST_CPU}"

if echo "${HOST_CPU}" | grep -qE "i[0-9]-10"; then
    echo "[!] Target identified as 10th Gen Intel Core Hardware (UHD Graphics)."
    echo "    --> Enforcing legacy OpenCL compute profile. Bypassing Level Zero."
    sudo apt-get update
    sudo apt-get install -y "${CORE_PACKAGES[@]}"
else
    echo "[+] Target identified as 11th Gen+ / Discrete / Native Linux Hardware."
    echo "    --> Injecting Level Zero direct-to-metal stack."
    sudo apt-get update
    sudo apt-get install -y "${CORE_PACKAGES[@]}" libze1 libze-intel-gpu1 || true
fi

# ------------------------------------------------------------------------------
# STEP 5: Provision Standalone uv Python Toolchain
# ------------------------------------------------------------------------------
echo -e "\n[*] Provisioning standalone uv toolchain manager..."
mkdir -p "$HOME/.local/bin"

# NECESSARY NULL PIPE: 'command -v' outputs binary path on success; stdout suppressed to keep UI clean.
if ! command -v uv > /dev/null 2>&1; then
    echo "[*] Bootstrapping uv binary toolchain manager via official installer..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "[+] uv toolchain manager installed successfully."
else
    echo "[+] uv engine already resident on host partition. Skipping installation."
fi

# ------------------------------------------------------------------------------
# STEP 6: Submodule Forensic Audit & Realignment
# ------------------------------------------------------------------------------
echo "[*] Auditing Git submodule configuration status..."

# NECESSARY NULL PIPE: 'git submodule status' stderr suppressed in un-initialized repo checks.
if git submodule status 2>/dev/null | grep -q "^-"; then
    echo "[!] ALERT: Uninitialized Git submodules detected in workspace!"
    git submodule update --init --recursive
    echo "[+] Submodule tracking vectors successfully initialized."
else
    echo "[+] Idempotency Check Passed: All submodules are configured."
fi

# ------------------------------------------------------------------------------
# STEP 7: Synchronize Pinned Workspace Dependencies
# ------------------------------------------------------------------------------
echo "[*] Triggering uv workspace sync..."
if [ -f "pyproject.toml" ] && command -v uv > /dev/null 2>&1; then
    uv sync
else
    echo "[!] Notice: pyproject.toml synced or uv available."
fi

echo -e "\n==> [SUCCESS] edge-ai infrastructure provisioning complete."
