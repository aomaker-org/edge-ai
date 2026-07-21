# ==============================================================================
# Path:        tools/host/provision_ps7.ps1
# Purpose:     Host machine provisioning script for Windows 11 using PowerShell 7+
#              and winget to install build tools, Git, CMake, Ninja, and WSL2 Ubuntu.
# Architecture: Idempotent winget package management & WSL2 enablement.
# ==============================================================================

# Requires PowerShell 7+
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Provisioning Windows 11 Host for edge-ai Development" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "[*] Auditing and installing core development packages via winget..." -ForegroundColor Yellow

# Install Git
winget install --id Git.Git --exact --accept-package-agreements --accept-source-agreements --source winget

# Install CMake
winget install --id Kitware.CMake --exact --accept-package-agreements --accept-source-agreements --source winget

# Install Ninja Build System
winget install --id Ninja-build.Ninja --exact --accept-package-agreements --accept-source-agreements --source winget

# Install Python 3.12
winget install --id Python.Python.3.12 --exact --accept-package-agreements --accept-source-agreements --source winget

# Install PowerShell 7
winget install --id Microsoft.PowerShell --exact --accept-package-agreements --accept-source-agreements --source winget

# Install Ubuntu 24.04 WSL2 Distribution
winget install --id Canonical.Ubuntu.2404 --exact --accept-package-agreements --accept-source-agreements --source winget

Write-Host "[*] Enabling WSL2 subsystem..." -ForegroundColor Yellow
wsl --install -d Ubuntu-24.04 --no-launch

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Windows 11 host provisioning complete." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
