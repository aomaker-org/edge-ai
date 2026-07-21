# ==============================================================================
# Filename:     infra/win11/config_win11.ps1
# Purpose:      PowerShell 7 Native Windows 11 Environment Loader for edge-ai
# Type:         Dot-Sourced (. .\infra\win11\config_win11.ps1)
# Attribution:  fekerr & Antigravity (20260720 / Initial Win11 Native Pass)
# ==============================================================================
#
# Usage:
#   1. Open Windows Terminal with VS2022/VS2026 dev tools profile chaining
#   2. Navigate to edge-ai root:  cd C:\Users\feker\src\edge-ai
#   3. Dot-source:  . .\infra\win11\config_win11.ps1
#   4. Options:
#        . .\infra\win11\config_win11.ps1 -Force            # Force reload
#        . .\infra\win11\config_win11.ps1 -Unset            # Tear down env
#        . .\infra\win11\config_win11.ps1 -Tag "myproject"  # Set prompt tag
#
# ==============================================================================

[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$Unset,
    [string]$Tag = ""
)

# ---------------------------------------------------------------
# 1. Source Guard (Prevent direct execution via pwsh -File)
# ---------------------------------------------------------------
# Note: PowerShell doesn't have bash's BASH_SOURCE equivalent for sourcing
# detection in the same way. This is informational guidance:
# Always invoke via `. .\infra\win11\config_win11.ps1` (dot-source)

# ---------------------------------------------------------------
# 2. Handle Explicit Unset
# ---------------------------------------------------------------
if ($Unset) {
    Write-Host "[!] Tearing down edge-ai PowerShell environment..." -ForegroundColor Yellow
    Remove-Variable -Name EDGEAI_READY -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_ROOT -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name PROJECT_ROOT -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_PLATFORM -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_BUILD_DIR -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_LOGS_DIR -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_MODELS_DIR -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_TEST_MODEL -Scope Global -ErrorAction SilentlyContinue
    Remove-Variable -Name EDGEAI_PROMPT_TAG -Scope Global -ErrorAction SilentlyContinue

    # Remove environment variables
    [Environment]::SetEnvironmentVariable("PROJECT_ROOT", $null, "Process")
    [Environment]::SetEnvironmentVariable("EDGEAI_BUILD_DIR", $null, "Process")
    [Environment]::SetEnvironmentVariable("EDGEAI_PLATFORM", $null, "Process")

    # Remove custom functions
    Remove-Item Function:\Invoke-EdgeAICMake -ErrorAction SilentlyContinue
    Remove-Item Function:\Invoke-EdgeAIBuild -ErrorAction SilentlyContinue
    Remove-Item Function:\Invoke-EdgeAIClean -ErrorAction SilentlyContinue
    Remove-Item Function:\Show-EdgeAIStatus -ErrorAction SilentlyContinue

    Write-Host "[+] edge-ai PowerShell environment unset." -ForegroundColor Green
    return
}

# ---------------------------------------------------------------
# 3. Force Reload Handling
# ---------------------------------------------------------------
if ($Force) {
    Write-Host "[!] Force reload detected. Cycling environment state..." -ForegroundColor Yellow
    Remove-Variable -Name EDGEAI_READY -Scope Global -ErrorAction SilentlyContinue
    if ($Tag) { $Global:EDGEAI_PROMPT_TAG = $Tag } else { $Global:EDGEAI_PROMPT_TAG = "default" }
} elseif ($Tag) {
    $Global:EDGEAI_PROMPT_TAG = $Tag
}

# ---------------------------------------------------------------
# 4. Idempotency Guard
# ---------------------------------------------------------------
if ($Global:EDGEAI_READY) {
    Write-Host "[!] edge-ai environment already loaded. Use -Force to re-verify." -ForegroundColor Yellow
    return
}

# ---------------------------------------------------------------
# 5. Project Root Anchoring (Absolute, Never Relative)
# ---------------------------------------------------------------
# This script lives at infra/win11/config_win11.ps1 => root is 2 levels up
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Global:EDGEAI_ROOT = (Resolve-Path (Join-Path $ScriptDir "..\.." )).Path
$Global:PROJECT_ROOT = $Global:EDGEAI_ROOT

# Export as process-level environment variable for child processes (cmake, make, etc.)
[Environment]::SetEnvironmentVariable("PROJECT_ROOT", $Global:PROJECT_ROOT, "Process")

Write-Host "[+] PROJECT_ROOT anchored to: $($Global:PROJECT_ROOT)" -ForegroundColor Cyan

# ---------------------------------------------------------------
# 6. Validate Inherited Toolchains
# ---------------------------------------------------------------
Write-Host "[*] Verifying inherited developer toolchains..." -ForegroundColor Gray

$toolchainChecks = @(
    @{ Name = "Microsoft C/C++ Compiler (cl.exe)"; Command = "cl.exe"; Critical = $true },
    @{ Name = "CMake"; Command = "cmake.exe"; Critical = $true },
    @{ Name = "Ninja Build System"; Command = "ninja.exe"; Critical = $false },
    @{ Name = "Git"; Command = "git.exe"; Critical = $false },
    @{ Name = "Python 3"; Command = "python.exe"; Critical = $false }
)

$allCriticalPassed = $true
foreach ($tool in $toolchainChecks) {
    $found = Get-Command $tool.Command -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host "  [+] $($tool.Name)" -ForegroundColor Green -NoNewline
        # Show version for key tools
        switch ($tool.Command) {
            "cmake.exe" {
                $ver = (cmake --version 2>&1 | Select-Object -First 1) -replace "cmake version ", ""
                Write-Host " (v$ver)" -ForegroundColor DarkGray
            }
            "git.exe" {
                $ver = (git --version 2>&1) -replace "git version ", ""
                Write-Host " (v$ver)" -ForegroundColor DarkGray
            }
            default { Write-Host "" }
        }
    } else {
        if ($tool.Critical) {
            Write-Host "  [-] MISSING: $($tool.Name)" -ForegroundColor Red
            $allCriticalPassed = $false
        } else {
            Write-Host "  [i] Optional: $($tool.Name) not found" -ForegroundColor DarkYellow
        }
    }
}

if (-not $allCriticalPassed) {
    Write-Host "`n[!] CRITICAL: Required toolchains missing." -ForegroundColor Red
    Write-Host "    Ensure VS2022/VS2026 Developer PowerShell or vcvarsall.bat is chained." -ForegroundColor Red
    Write-Host "    Environment NOT loaded.`n" -ForegroundColor Red
    return
}

# ---------------------------------------------------------------
# 7. Intel oneAPI Detection
# ---------------------------------------------------------------
if ($env:ONEAPI_ROOT) {
    Write-Host "[+] Intel oneAPI root detected: $($env:ONEAPI_ROOT)" -ForegroundColor Green
} elseif ($env:MKLROOT) {
    Write-Host "[+] Intel MKL environment detected." -ForegroundColor Green
} else {
    Write-Host "[i] Intel oneAPI not detected. SYCL backend targets unavailable." -ForegroundColor DarkYellow
}

# ---------------------------------------------------------------
# 8. Configure Build Environment
# ---------------------------------------------------------------
$Global:EDGEAI_PLATFORM = "win11_native_ps7"
$Global:EDGEAI_BUILD_DIR = Join-Path $Global:PROJECT_ROOT "build"
$Global:EDGEAI_LOGS_DIR = Join-Path $Global:PROJECT_ROOT "logs"

[Environment]::SetEnvironmentVariable("EDGEAI_BUILD_DIR", $Global:EDGEAI_BUILD_DIR, "Process")
[Environment]::SetEnvironmentVariable("EDGEAI_PLATFORM", $Global:EDGEAI_PLATFORM, "Process")

# Model configuration
if (-not $Global:EDGEAI_MODELS_DIR) {
    $Global:EDGEAI_MODELS_DIR = Join-Path $Global:PROJECT_ROOT "..\models"
}
if (-not $Global:EDGEAI_TEST_MODEL) {
    $Global:EDGEAI_TEST_MODEL = Join-Path $Global:EDGEAI_MODELS_DIR "tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
}

# Ensure out-of-tree directories exist
@($Global:EDGEAI_BUILD_DIR, $Global:EDGEAI_LOGS_DIR) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null  # Idempotent directory creation
        Write-Host "  [+] Created: $_" -ForegroundColor DarkGreen
    }
}

# ---------------------------------------------------------------
# 9. Load Local Overrides (Machine-Specific, Git-Ignored)
# ---------------------------------------------------------------
$localConfig = Join-Path $Global:PROJECT_ROOT "config_local.ps1"
if (Test-Path $localConfig) {
    Write-Host "[*] Loading machine-specific overrides from config_local.ps1..." -ForegroundColor Gray
    . $localConfig
}

# ---------------------------------------------------------------
# 10. Build Helper Functions
# ---------------------------------------------------------------

function Global:Invoke-EdgeAICMake {
    <#
    .SYNOPSIS
        Configure a CMake build preset for edge-ai.
    .PARAMETER Preset
        Build preset name (e.g., "default", "sycl", "openvino").
    .PARAMETER BuildType
        CMake build type (Debug, Release, RelWithDebInfo). Default: RelWithDebInfo.
    .PARAMETER Generator
        CMake generator. Default: Ninja.
    #>
    param(
        [string]$Preset = "default",
        [string]$BuildType = "RelWithDebInfo",
        [string]$Generator = "Ninja",
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$ExtraCMakeArgs
    )
    $buildDir = Join-Path $Global:EDGEAI_BUILD_DIR $Preset
    $sourceDir = $Global:PROJECT_ROOT

    $cmakeArgs = @(
        "-S", $sourceDir,
        "-B", $buildDir,
        "-G", $Generator,
        "-DCMAKE_BUILD_TYPE=$BuildType"
    )
    $cmakeArgs += $ExtraCMakeArgs

    Write-Host "[cmake] Configuring preset '$Preset' in $buildDir" -ForegroundColor Cyan
    Write-Host "[cmake] Args: cmake $($cmakeArgs -join ' ')" -ForegroundColor DarkGray
    & cmake @cmakeArgs
}

function Global:Invoke-EdgeAIBuild {
    <#
    .SYNOPSIS
        Execute a cmake --build for a named preset.
    .PARAMETER Preset
        Build preset name matching a configured build directory.
    .PARAMETER Jobs
        Parallel build jobs. Default: auto (let cmake/ninja decide).
    #>
    param(
        [string]$Preset = "default",
        [string]$BuildType = "RelWithDebInfo",
        [int]$Jobs = 0
    )
    $buildDir = Join-Path $Global:EDGEAI_BUILD_DIR $Preset
    if (-not (Test-Path (Join-Path $buildDir "CMakeCache.txt"))) {
        Write-Host "[!] No CMake cache found in $buildDir. Run Invoke-EdgeAICMake first." -ForegroundColor Red
        return
    }

    $buildArgs = @("--build", $buildDir, "--config", $BuildType)
    if ($Jobs -gt 0) { $buildArgs += @("-j", $Jobs) }

    Write-Host "[build] Building preset '$Preset'..." -ForegroundColor Cyan
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    & cmake @buildArgs
    $sw.Stop()
    Write-Host "[build] Completed in $($sw.Elapsed.TotalSeconds.ToString('F1'))s" -ForegroundColor Green
}

function Global:Invoke-EdgeAIClean {
    <#
    .SYNOPSIS
        Remove a specific build preset directory.
    #>
    param([string]$Preset = "default")
    $buildDir = Join-Path $Global:EDGEAI_BUILD_DIR $Preset
    if (Test-Path $buildDir) {
        Remove-Item -Recurse -Force $buildDir
        Write-Host "[clean] Removed: $buildDir" -ForegroundColor Yellow
    } else {
        Write-Host "[clean] Nothing to clean: $buildDir does not exist." -ForegroundColor DarkGray
    }
}

function Global:Show-EdgeAIStatus {
    <#
    .SYNOPSIS
        Display edge-ai environment status and build directory inventory.
    #>
    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor DarkCyan
    Write-Host " edge-ai Environment Status" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkCyan
    Write-Host "  PROJECT_ROOT:   $($Global:PROJECT_ROOT)"
    Write-Host "  Platform:       $($Global:EDGEAI_PLATFORM)"
    Write-Host "  Build Dir:      $($Global:EDGEAI_BUILD_DIR)"
    Write-Host "  Logs Dir:       $($Global:EDGEAI_LOGS_DIR)"
    Write-Host "  Models Dir:     $($Global:EDGEAI_MODELS_DIR)"
    Write-Host "  Prompt Tag:     $($Global:EDGEAI_PROMPT_TAG)"
    Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray

    # List existing build presets
    if (Test-Path $Global:EDGEAI_BUILD_DIR) {
        $presets = Get-ChildItem -Directory $Global:EDGEAI_BUILD_DIR -ErrorAction SilentlyContinue
        if ($presets) {
            Write-Host "  Active Build Presets:" -ForegroundColor DarkCyan
            foreach ($p in $presets) {
                $hasCache = Test-Path (Join-Path $p.FullName "CMakeCache.txt")
                $status = if ($hasCache) { "[configured]" } else { "[empty]" }
                Write-Host "    - $($p.Name) $status" -ForegroundColor $(if ($hasCache) { "Green" } else { "DarkGray" })
            }
        } else {
            Write-Host "  No build presets found." -ForegroundColor DarkGray
        }
    }
    Write-Host "=================================================================" -ForegroundColor DarkCyan
    Write-Host ""
}

# ---------------------------------------------------------------
# 11. Custom Prompt with Git Branch & Status
# ---------------------------------------------------------------
if (-not $Global:EDGEAI_PROMPT_TAG) { $Global:EDGEAI_PROMPT_TAG = "default" }

function Global:prompt {
    $exitCode = $global:LASTEXITCODE
    $ts = Get-Date -Format "yyMM_HHmm_ss"
    $tag = $Global:EDGEAI_PROMPT_TAG

    # Git branch detection
    $gitBranch = ""
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null  # Silent check for git repo context
        if ($branch) { $gitBranch = " ($branch)" }
    } catch { }

    $statusColor = if ($exitCode -eq 0 -or $null -eq $exitCode) { "Green" } else { "Red" }
    $statusSymbol = if ($exitCode -eq 0 -or $null -eq $exitCode) { "✓" } else { "✗ $exitCode" }

    Write-Host ""
    Write-Host "$env:USERNAME@$env:COMPUTERNAME " -NoNewline -ForegroundColor Cyan
    Write-Host "[$tag] " -NoNewline -ForegroundColor Magenta
    Write-Host "- $ts " -NoNewline -ForegroundColor DarkGray
    Write-Host "[$statusSymbol]" -ForegroundColor $statusColor
    Write-Host "$(Get-Location)" -NoNewline -ForegroundColor Yellow
    Write-Host "$gitBranch" -ForegroundColor Green
    Write-Host ""
    return "; "
}

# ---------------------------------------------------------------
# 12. Final Readiness
# ---------------------------------------------------------------
$Global:EDGEAI_READY = $true

Write-Host ""
Write-Host "==================================================================" -ForegroundColor DarkCyan
Write-Host " edge-ai Windows 11 PowerShell 7 Environment Ready" -ForegroundColor Cyan
Write-Host "  Root:        $($Global:PROJECT_ROOT)" -ForegroundColor White
Write-Host "  Build:       $($Global:EDGEAI_BUILD_DIR)" -ForegroundColor White
Write-Host "  Platform:    $($Global:EDGEAI_PLATFORM)" -ForegroundColor White
Write-Host "  Tag:         $($Global:EDGEAI_PROMPT_TAG)" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "  Commands:    Invoke-EdgeAICMake | Invoke-EdgeAIBuild" -ForegroundColor DarkGray
Write-Host "               Invoke-EdgeAIClean | Show-EdgeAIStatus" -ForegroundColor DarkGray
Write-Host "==================================================================" -ForegroundColor DarkCyan
Write-Host ""
