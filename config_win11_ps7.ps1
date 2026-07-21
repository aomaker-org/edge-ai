# ==============================================================================
# Filename:     config_win11_ps7.ps1
# Purpose:      Top-Level Entrypoint for edge-ai PowerShell 7 Loader
# ==============================================================================
[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$Unset,
    [string]$Tag = ""
)

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $RootDir "infra\win11\config_win11_ps7.ps1") -Force:$Force -Unset:$Unset -Tag $Tag
