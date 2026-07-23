# `edge-ai` Provisioning & Environment Setup Specifications (`PROVISIONING_NOTES.md`)

This document provides both **Concise (TL;DR)** and **Verbose (Architectural)** specifications for provisioning host machines running `edge-ai` across **Windows 11 (Native & WSL2)** and **Linux**.

---

## ⚡ 1. Concise Provisioning Guide (TL;DR)

### A. Windows 11 Host Provisioning (PowerShell 7)
Open **PowerShell 7 (Administrator)** and run:
```powershell
# 1. Install core dev toolchain & WSL2 via winget
winget install --id Microsoft.PowerShell -e --source winget
winget install --id Git.Git -e --source winget
winget install --id Microsoft.VisualStudio.2022.BuildTools --override "--passive --config C:\Path\To\.vsconfig"
winget install --id Canonical.Ubuntu.2404 -e --source winget

# 2. Enable WSL2 feature
wsl --install -d Ubuntu-24.04
```

### B. WSL2 / Ubuntu 26 Development Provisioning
Inside WSL2 / Ubuntu shell:
```bash
# Execute idempotent provisioning script derived from irislime
curl -fsSL https://raw.githubusercontent.com/aomaker-org/edge-ai/main/tools/provision.sh | bash
```

---

## 🏛️ 2. Verbose Environment Architecture & Provisioning Analysis

### A. Native Windows vs. WSL2 Environment Comparison

| Attribute | Native Windows 11 Build | WSL2 Ubuntu (Linux Container) Build |
| :--- | :--- | :--- |
| **Toolchain** | MSVC (`cl.exe`), Ninja, CMake | `gcc`/`clang`, GNU Make, `uv`, CMake |
| **GPU Acceleration** | DirectX12, DirectML, Vulkan native drivers | CUDA, ROCm, Vulkan via WSLg/DXCore |
| **Build Speed** | Native NTFS I/O speed | Fast inside Linux ext4 virtual disk; slow cross-FS (`/mnt/c`) |
| **Hardware Interop** | Low-level hardware register & driver access | Virtualized GPU memory / Direct3D 12 pass-through |
| **Agent / Automation** | PowerShell 7 scripts (`.ps1`) | POSIX Shell (`.sh`), `agy` CLI native Linux binary |

> **[!] Recommendation**: For core engine development and out-of-tree POSIX build matrices, **WSL2 Ubuntu** is the primary target. For native DirectML and low-latency DirectX hardware validation, use **Native Windows 11**.

---

## 🛠️ 3. Windows 11 Provisioning Script (`tools/host/provision_ps7.ps1`)

Derived from `irislime/derived_components/tools/host/provision_ps7.ps1`, this PowerShell script automates host toolchain installation:

```powershell
# Requires PowerShell 7+
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Provisioning Windows 11 Host for edge-ai Development" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Install Git, CMake, Python, Ninja, and BuildTools
winget install --id Git.Git --exact --accept-package-agreements --accept-source-agreements
winget install --id Kitware.CMake --exact --accept-package-agreements --accept-source-agreements
winget install --id Ninja-build.Ninja --exact --accept-package-agreements --accept-source-agreements
winget install --id Python.Python.3.12 --exact --accept-package-agreements --accept-source-agreements
```

---

## 🐧 4. Linux / WSL2 Provisioning Script (`tools/provision.sh`)

Derived from `irislime/derived_components/tools/provision.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " Provisioning Linux / WSL2 Environment for edge-ai"
echo "=========================================================="

sudo apt-get update -y
sudo apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    python3 \
    python3-pip \
    curl \
    jq

# Install uv for Python environment management
curl -LsSf https://astral.sh/uv/install.sh | sh
```
