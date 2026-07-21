# ==============================================================================
# Filename:     infra/win11/config_win11_ps7.ps1
# Purpose:      PowerShell 7 Native Windows 11 Environment Loader for edge-ai
# Type:         Dot-Sourced (. .\infra\win11\config_win11_ps7.ps1)
# Attribution:  fekerr & Antigravity (20260720 / Native Win11 PS7 Integration)
# ==============================================================================

[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$Unset,
    [string]$Tag = ""
)

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

    [Environment]::SetEnvironmentVariable("PROJECT_ROOT", $null, "Process")
    [Environment]::SetEnvironmentVariable("EDGEAI_BUILD_DIR", $null, "Process")
    [Environment]::SetEnvironmentVariable("EDGEAI_PLATFORM", $null, "Process")

    Remove-Item Function:\Invoke-EdgeAICMake -ErrorAction SilentlyContinue
    Remove-Item Function:\Invoke-EdgeAIBuild -ErrorAction SilentlyContinue
    Remove-Item Function:\Invoke-EdgeAIClean -ErrorAction SilentlyContinue
    Remove-Item Function:\Show-EdgeAIStatus -ErrorAction SilentlyContinue

    Write-Host "[+] edge-ai PowerShell environment unset." -ForegroundColor Green
    return
}

if ($Force) {
    Write-Host "[!] Force reload detected. Cycling environment state..." -ForegroundColor Yellow
    Remove-Variable -Name EDGEAI_READY -Scope Global -ErrorAction SilentlyContinue
    if ($Tag) { $Global:EDGEAI_PROMPT_TAG = $Tag } else { $Global:EDGEAI_PROMPT_TAG = "default" }
} elseif ($Tag) {
    $Global:EDGEAI_PROMPT_TAG = $Tag
}

if ($Global:EDGEAI_READY) {
    Write-Host "[!] edge-ai environment already loaded. Use -Force to re-verify." -ForegroundColor Yellow
    return
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path (Join-Path $ScriptDir "..\..\infra")) {
    $Global:EDGEAI_ROOT = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
} else {
    $Global:EDGEAI_ROOT = (Resolve-Path $ScriptDir).Path
}
$Global:PROJECT_ROOT = $Global:EDGEAI_ROOT

[Environment]::SetEnvironmentVariable("PROJECT_ROOT", $Global:PROJECT_ROOT, "Process")
Write-Host "[+] PROJECT_ROOT anchored to: $($Global:PROJECT_ROOT)" -ForegroundColor Cyan

$clFound = Get-Command "cl.exe" -ErrorAction SilentlyContinue
if (-not $clFound) {
    $ps1Snapshot = Join-Path $Global:PROJECT_ROOT ".edgeai_env.ps1"
    $captureScript = Join-Path $Global:PROJECT_ROOT "infra\win11\capture_env.py"

    if (Test-Path $ps1Snapshot) {
        Write-Host "[*] Injected cached MSVC build environment from .edgeai_env.ps1..." -ForegroundColor Gray
        . $ps1Snapshot
    } elseif ((Test-Path $captureScript) -and (Get-Command "python.exe" -ErrorAction SilentlyContinue)) {
        Write-Host "[*] Auto-running environment capturer (capture_env.py)..." -ForegroundColor Gray
        & python $captureScript --output-dir $Global:PROJECT_ROOT | Out-Null
        if (Test-Path $ps1Snapshot) {
            . $ps1Snapshot
        }
    }
}

Write-Host "[*] Verifying developer toolchains..." -ForegroundColor Gray

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
        Write-Host "  [+] $($tool.Name)" -ForegroundColor Green
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
    Write-Host "`n[!] WARNING: Required build toolchains missing in current session." -ForegroundColor Red
}

$Global:EDGEAI_PLATFORM = "win11_native_ps7"
$Global:EDGEAI_BUILD_DIR = Join-Path $Global:PROJECT_ROOT "build"
$Global:EDGEAI_LOGS_DIR = Join-Path $Global:PROJECT_ROOT "logs"

[Environment]::SetEnvironmentVariable("EDGEAI_BUILD_DIR", $Global:EDGEAI_BUILD_DIR, "Process")
[Environment]::SetEnvironmentVariable("EDGEAI_PLATFORM", $Global:EDGEAI_PLATFORM, "Process")

if (-not $Global:EDGEAI_MODELS_DIR) {
    $Global:EDGEAI_MODELS_DIR = Join-Path $Global:PROJECT_ROOT "..\models"
}
if (-not $Global:EDGEAI_TEST_MODEL) {
    $Global:EDGEAI_TEST_MODEL = Join-Path $Global:EDGEAI_MODELS_DIR "tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
}

@($Global:EDGEAI_BUILD_DIR, $Global:EDGEAI_LOGS_DIR) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

$localConfig = Join-Path $Global:PROJECT_ROOT "config_local.ps1"
if (Test-Path $localConfig) {
    Write-Host "[*] Loading machine-specific overrides from config_local.ps1..." -ForegroundColor Gray
    . $localConfig
}

function Global:Invoke-EdgeAICMake {
    param(
        [string]$Preset = "default",
        [string]$BuildType = "RelWithDebInfo",
        [string]$Generator = "Ninja",
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$ExtraCMakeArgs
    )
    $buildDir = Join-Path $Global:EDGEAI_BUILD_DIR $Preset
    $cmakeArgs = @(
        "-S", $Global:PROJECT_ROOT,
        "-B", $buildDir,
        "-G", $Generator,
        "-DCMAKE_BUILD_TYPE=$BuildType"
    ) + $ExtraCMakeArgs

    Write-Host "[cmake] Configuring preset '$Preset' in $buildDir" -ForegroundColor Cyan
    & cmake @cmakeArgs
}

function Global:Invoke-EdgeAIBuild {
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
    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor DarkCyan
    Write-Host " edge-ai Environment Status (PowerShell 7)" -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor DarkCyan
    Write-Host "  PROJECT_ROOT:   $($Global:PROJECT_ROOT)"
    Write-Host "  Platform:       $($Global:EDGEAI_PLATFORM)"
    Write-Host "  Build Dir:      $($Global:EDGEAI_BUILD_DIR)"
    Write-Host "  Logs Dir:       $($Global:EDGEAI_LOGS_DIR)"
    Write-Host "  Models Dir:     $($Global:EDGEAI_MODELS_DIR)"
    Write-Host "  Prompt Tag:     $($Global:EDGEAI_PROMPT_TAG)"
    Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray
    if (Test-Path $Global:EDGEAI_BUILD_DIR) {
        $presets = Get-ChildItem -Directory $Global:EDGEAI_BUILD_DIR -ErrorAction SilentlyContinue
        if ($presets) {
            Write-Host "  Active Build Presets:" -ForegroundColor DarkCyan
            foreach ($p in $presets) {
                $hasCache = Test-Path (Join-Path $p.FullName "CMakeCache.txt")
                $status = if ($hasCache) { "[configured]" } else { "[empty]" }
                Write-Host "    - $($p.Name) $status" -ForegroundColor $(if ($hasCache) { "Green" } else { "DarkGray" })
            }
        }
    }
    Write-Host "=================================================================" -ForegroundColor DarkCyan
    Write-Host ""
}

Set-Alias -Name edgeai_cmake -Value Invoke-EdgeAICMake -Scope Global -ErrorAction SilentlyContinue
Set-Alias -Name edgeai_build -Value Invoke-EdgeAIBuild -Scope Global -ErrorAction SilentlyContinue
Set-Alias -Name edgeai_clean -Value Invoke-EdgeAIClean -Scope Global -ErrorAction SilentlyContinue
Set-Alias -Name show_edgeai_status -Value Show-EdgeAIStatus -Scope Global -ErrorAction SilentlyContinue

if (-not $Global:EDGEAI_PROMPT_TAG) { $Global:EDGEAI_PROMPT_TAG = "default" }

function Global:prompt {
    $exitCode = $global:LASTEXITCODE
    $ts = Get-Date -Format "yyMM_HHmm_ss"
    $tag = $Global:EDGEAI_PROMPT_TAG

    $gitBranch = ""
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
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

$Global:EDGEAI_READY = $true

Write-Host ""
Write-Host "==================================================================" -ForegroundColor DarkCyan
Write-Host " edge-ai Windows 11 PowerShell 7 Environment Ready" -ForegroundColor Cyan
Write-Host "  Root:     $($Global:PROJECT_ROOT)" -ForegroundColor White
Write-Host "  Build:    $($Global:EDGEAI_BUILD_DIR)" -ForegroundColor White
Write-Host "  Platform: $($Global:EDGEAI_PLATFORM)" -ForegroundColor White
Write-Host "  Tag:      $($Global:EDGEAI_PROMPT_TAG)" -ForegroundColor White
Write-Host ""
Write-Host "  Commands: Invoke-EdgeAICMake | Invoke-EdgeAIBuild" -ForegroundColor DarkGray
Write-Host "            Invoke-EdgeAIClean | Show-EdgeAIStatus" -ForegroundColor DarkGray
Write-Host "==================================================================" -ForegroundColor DarkCyan
Write-Host ""
