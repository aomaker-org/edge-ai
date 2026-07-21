# ==============================================================================
# Filename:     provision_win11.ps1
# Purpose:      Top-Level Entrypoint for edge-ai Windows 11 Provisioner
# ==============================================================================
[CmdletBinding()]
param(
    [switch]$InstallMissing,
    [switch]$GenerateEnvSnapshot
)

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $RootDir "infra\win11\provision_win11.ps1") -InstallMissing:$InstallMissing -GenerateEnvSnapshot:$GenerateEnvSnapshot
