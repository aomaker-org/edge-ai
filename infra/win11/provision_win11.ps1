# ==============================================================================
# Filename:     infra/win11/provision_win11.ps1
# Purpose:      Automated Win11 Environment & Toolchain Provisioner for edge-ai
# Type:         Executed / Dot-Sourced (. .\infra\win11\provision_win11.ps1)
# Attribution:  fekerr & Antigravity (20260720 / Win11 Provisioning Automation)
# ==============================================================================

[CmdletBinding()]
param(
    [switch]$InstallMissing,
    [switch]$GenerateEnvSnapshot
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor DarkCyan
Write-Host " edge-ai Windows 11 Toolchain & System Environment Provisioner" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor DarkCyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path (Join-Path $ScriptDir "..\..\infra")) {
    $ProjectRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
} else {
    $ProjectRoot = (Resolve-Path $ScriptDir).Path
}

Write-Host "[+] Project Root: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

$wingetPackages = @(
    @{ Id = "Git.Git"; Name = "Git for Windows"; Command = "git.exe" },
    @{ Id = "Microsoft.PowerShell"; Name = "PowerShell 7"; Command = "pwsh.exe" },
    @{ Id = "Kitware.CMake"; Name = "CMake Build System"; Command = "cmake.exe" },
    @{ Id = "Ninja-build.Ninja"; Name = "Ninja Build Generator"; Command = "ninja.exe" },
    @{ Id = "astral-sh.uv"; Name = "uv Python Package Manager"; Command = "uv.exe" },
    @{ Id = "ShiningLight.OpenSSL"; Name = "OpenSSL Win64"; Command = "openssl.exe" }
)

$wingetAvailable = $false
$wingetCmd = Get-Command "winget.exe" -ErrorAction SilentlyContinue
if ($wingetCmd) {
    $wingetAvailable = $true
    Write-Host "[+] Winget Package Manager detected." -ForegroundColor Green
} else {
    Write-Host "[-] Winget Package Manager not detected." -ForegroundColor Yellow
}

Write-Host "`n[*] Auditing Developer Tools & Package Dependencies..." -ForegroundColor Gray
$missingPackages = @()

foreach ($pkg in $wingetPackages) {
    $found = Get-Command $pkg.Command -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "  [+] $($pkg.Name) ($($pkg.Command)): FOUND" -ForegroundColor Green
    } else {
        Write-Host "  [-] $($pkg.Name) ($($pkg.Command)): MISSING" -ForegroundColor Red
        $missingPackages += $pkg
    }
}

Write-Host "`n[*] Auditing Visual Studio C++ Compiler Infrastructure..." -ForegroundColor Gray
$programFilesX86 = ${env:ProgramFiles(x86)}
if (-not $programFilesX86) { $programFilesX86 = "C:\Program Files (x86)" }
$vswhere = Join-Path $programFilesX86 "Microsoft Visual Studio\Installer\vswhere.exe"

$vsInstalled = $false
$vsPath = ""
if (Test-Path $vswhere) {
    $vsInstallPath = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    if ($vsInstallPath) {
        $vsInstalled = $true
        $vsPath = $vsInstallPath.Trim()
        Write-Host "  [+] Visual Studio C++ Build Tools detected at: $vsPath" -ForegroundColor Green
    }
}

if (-not $vsInstalled) {
    Write-Host "  [-] Visual Studio C++ Build Tools NOT detected." -ForegroundColor Red
    if ($InstallMissing -and $wingetAvailable) {
        Write-Host "  [*] Attempting winget install for Visual Studio Community 2022..." -ForegroundColor Yellow
        winget install --id Microsoft.VisualStudio.2022.Community --override "--passive --add Microsoft.VisualStudio.Workload.NativeDesktop"
    }
}

Write-Host "`n[*] Auditing Intel Accelerator Toolchains..." -ForegroundColor Gray
$oneAPIPath = "C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
if (Test-Path $oneAPIPath) {
    Write-Host "  [+] Intel oneAPI Toolkit detected: $oneAPIPath" -ForegroundColor Green
} else {
    Write-Host "  [i] Intel oneAPI Toolkit not found at default location (Optional for SYCL)." -ForegroundColor DarkYellow
}

$openvinoDirs = Get-ChildItem "C:\Program Files\WindowsApps" -Filter "IntelCorporation.OpenVINOToolkit*" -ErrorAction SilentlyContinue
if ($openvinoDirs) {
    Write-Host "  [+] Intel OpenVINO Toolkit detected in WindowsApps: $($openvinoDirs[0].FullName)" -ForegroundColor Green
} else {
    Write-Host "  [i] Intel OpenVINO Toolkit not detected in WindowsApps." -ForegroundColor DarkYellow
}

if ($missingPackages.Count -gt 0) {
    if ($InstallMissing -and $wingetAvailable) {
        Write-Host "`n[*] Installing missing packages via winget..." -ForegroundColor Yellow
        foreach ($pkg in $missingPackages) {
            Write-Host "  -> Installing $($pkg.Name) ($($pkg.Id))..." -ForegroundColor Cyan
            winget install --id $pkg.Id --silent --accept-package-agreements --accept-source-agreements
        }
    } else {
        Write-Host "`n[!] Missing packages detected. Run with -InstallMissing to auto-install via winget." -ForegroundColor Yellow
    }
}

$ps1Snapshot = Join-Path $ProjectRoot ".edgeai_env.ps1"
if ($GenerateEnvSnapshot -or (-not (Test-Path $ps1Snapshot))) {
    $captureScript = Join-Path $ProjectRoot "infra\win11\capture_env.py"
    if ((Test-Path $captureScript) -and (Get-Command "python.exe" -ErrorAction SilentlyContinue)) {
        Write-Host "`n[*] Triggering Environment Snapshot via capture_env.py..." -ForegroundColor Cyan
        & python.exe $captureScript --output-dir $ProjectRoot
    }
}

Write-Host "`n==================================================================" -ForegroundColor DarkCyan
Write-Host " Provisioning audit complete." -ForegroundColor Green
Write-Host " Use '. .\config_win11_ps7.ps1' or 'source config_win11_bash' to load environment." -ForegroundColor Gray
Write-Host "==================================================================" -ForegroundColor DarkCyan
