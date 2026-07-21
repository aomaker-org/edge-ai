<#
.SYNOPSIS
    High-Performance Rclone File & Manifest Transfer Script (PowerShell 7)

.ABSTRACT
    Transfers large build/log archives and manifest files from WSL2/Windows to remote cloud storage 
    (Google Drive / OneDrive) via Windows rclone.exe with maximum CPU/bandwidth utilization and optional
    chunker overlay for chunk-level upload retries.

.QUICKSTART
    # Direct execution from PowerShell 7:
    .\tools\rclone_transfer.ps1 -SourceFile "scratch\archive.zip" -ManifestFile "scratch\manifest.txt" -DestinationRemote "gdrive:transfer/core12/target_folder"

    # Execution with 500M Chunker Overlay for chunk-level retry resiliency:
    .\tools\rclone_transfer.ps1 -SourceFile "scratch\archive.zip" -ManifestFile "scratch\manifest.txt" -DestinationRemote "gdrive:transfer/core12/target_folder" -EnableChunker $true -ChunkerSplitSize "500M"
#>

param (
    [Parameter(Mandatory=$true)][string]$SourceFile,
    [Parameter(Mandatory=$true)][string]$ManifestFile,
    [Parameter(Mandatory=$true)][string]$DestinationRemote,
    [int]$Transfers = 8,
    [int]$Checkers = 16,
    [string]$ChunkSize = "128M",         # Google Drive API chunk upload size
    [bool]$EnableChunker = $false,       # Enable rclone chunker overlay for chunked resume
    [string]$ChunkerSplitSize = "500M"   # Chunker split size (e.g. 500M or 1G)
)

$ErrorActionPreference = "Stop"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                RCLONE HIGH-PERFORMANCE TRANSFER (PS7)                         " -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Source File          : $SourceFile"
Write-Host "Manifest File        : $ManifestFile"
Write-Host "Destination Remote   : $DestinationRemote"
Write-Host "Transfers            : $Transfers"
Write-Host "Checkers             : $Checkers"
Write-Host "Drive Chunk Size     : $ChunkSize"
Write-Host "Enable Chunker       : $EnableChunker"
if ($EnableChunker) {
    Write-Host "Chunker Split Size   : $ChunkerSplitSize"
}
Write-Host "--------------------------------------------------------------------------------"

if (-not (Test-Path $SourceFile)) {
    Write-Error "Source file does not exist: $SourceFile"
}

# Determine effective destination remote (direct or chunker overlay)
$targetRemote = $DestinationRemote
if ($EnableChunker) {
    $targetRemote = ":chunker,remote=""$DestinationRemote"",chunk_size=$ChunkerSplitSize:"
    Write-Host "[INFO] Using rclone chunker overlay backend: $targetRemote" -ForegroundColor Green
}

# 1. Copy source zip file to destination
Write-Host "[INFO] Copying source zip archive..." -ForegroundColor Yellow
$rcloneZipArgs = @(
    "copy",
    $SourceFile,
    $targetRemote,
    "--transfers", $Transfers,
    "--checkers", $Checkers,
    "--drive-chunk-size", $ChunkSize,
    "--fast-list",
    "--stats", "5s",
    "-P"
)

& rclone.exe @rcloneZipArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Rclone copy of source zip file failed with exit code $LASTEXITCODE"
}

# 2. Copy manifest file to destination
if (Test-Path $ManifestFile) {
    Write-Host "[INFO] Copying manifest file..." -ForegroundColor Yellow
    $manifestArgs = @(
        "copy",
        $ManifestFile,
        $DestinationRemote,
        "--fast-list"
    )
    & rclone.exe @manifestArgs
    if ($LASTEXITCODE -ne 0) {
        Write-Error "[ERROR] Rclone copy of manifest file failed with exit code $LASTEXITCODE"
    }
}

# 3. Verify transfer on destination
Write-Host "--------------------------------------------------------------------------------"
Write-Host "[INFO] Verifying files on destination remote..." -ForegroundColor Cyan
$sourceFileName = Split-Path -Leaf $SourceFile
$remoteListing = & rclone.exe ls $DestinationRemote
Write-Host "Remote directory contents:`n$remoteListing"

if ($remoteListing -match [regex]::Escape($sourceFileName) -or ($EnableChunker -and $remoteListing -match "\.rclone_chunk\.")) {
    Write-Host "[SUCCESS] Verification passed: Files successfully uploaded and verified!" -ForegroundColor Green
    exit 0
} else {
    Write-Error "[FAILURE] Verification failed: $sourceFileName not found on remote $DestinationRemote"
}

<#
================================================================================
                    VERBOSE / DETAILED TECHNICAL DOCUMENTATION
================================================================================

1. ARCHITECTURE & WORKFLOW
--------------------------------------------------------------------------------
This PowerShell 7 script acts as a high-performance transfer bridge between WSL2 
and Windows host networking. Instead of relying on WSL2 loopback network translation,
the script runs natively in Windows via `powershell.exe` to drive Windows-native 
`rclone.exe`.

2. PERFORMANCE TUNING SWITCHES EXPLAINED
--------------------------------------------------------------------------------
- `--transfers 8`: Sets the number of parallel file transfer threads. Maximizes 
  network interface utilization for concurrent uploads.
- `--checkers 16`: Sets the number of parallel checkers querying file state and 
  hashes on the remote cloud storage provider.
- `--drive-chunk-size 128M`: Increases the Google Drive HTTP upload chunk size 
  from the 8MB default to 128MB. Drastically reduces HTTP round-trip overhead 
  and increases transfer speed by 3x-10x on high-speed internet connections.
- `--fast-list`: Uses HTTP recursive directory listing endpoints (where supported),
  reducing API call count and speeding up pre-transfer directory scanning.

3. RCLONE CHUNKER OVERLAY BACKEND (:chunker:)
--------------------------------------------------------------------------------
When uploading multi-gigabyte files (e.g., 5GB - 50GB zip/tar archives), network 
flakiness or API rate limits can cause standard uploads to fail near 99% completion,
requiring a full restart.

By setting `-EnableChunker $true`, the script dynamically attaches rclone's `:chunker:`
overlay backend (`:chunker,remote="<destination>",chunk_size=500M:`).

How Chunker Works:
- Large source files are split transparently into smaller chunks (e.g., 500 MB).
- Chunks are named with standard suffixes (`.rclone_chunk.001`, `.rclone_chunk.002`).
- If an upload fails mid-transfer, rclone retries ONLY the failed chunk(s).
- On download or rclone mount, rclone reconstitutes the chunks back into the 
  original single archive seamlessly.

4. VERIFICATION & ERROR HANDLING
--------------------------------------------------------------------------------
- `$ErrorActionPreference = "Stop"` ensures any failing command or missing file 
  halts script execution with a non-zero exit code.
- Post-transfer, the script queries the target remote directory listing (`rclone ls`)
  and validates that either the exact filename or chunk signatures exist before 
  returning success.
================================================================================
#>
