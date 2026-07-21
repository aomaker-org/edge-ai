#!/usr/bin/env bash
# ==============================================================================
# ABSTRACT & QUICK START
# ==============================================================================
# Script: tools/rclone_transfer.sh
# Purpose: WSL2 Bash Wrapper for Windows PowerShell 7 Rclone Transfers
#
# QUICK START:
#   # Standard Transfer:
#   ./tools/rclone_transfer.sh <path-to-src-zip> <path-to-manifest> [dest-remote]
#
#   # Chunker Overlay Transfer (Resilient 500MB chunk-level retries):
#   ./tools/rclone_transfer.sh --chunker <path-to-src-zip> <path-to-manifest> [dest-remote]
#
#   # Chunker Overlay with custom chunk size (e.g. 1G):
#   ./tools/rclone_transfer.sh --chunker --chunker-size 1G <path-to-src-zip> <path-to-manifest> [dest-remote]
# ==============================================================================

set -euo pipefail

ENABLE_CHUNKER="false"
CHUNKER_SIZE="500M"

# Parse optional flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --chunker|-c)
      ENABLE_CHUNKER="true"
      shift
      ;;
    --chunker-size)
      CHUNKER_SIZE="$2"
      shift 2
      ;;
    *)
      break
      ;;
  esac
done

SRC_FILE="${1:-}"
MANIFEST_FILE="${2:-}"
DEST_REMOTE="${3:-gdrive:transfer/core12/20260720_ubuntu26_build_logs}"

if [[ -z "$SRC_FILE" || ! -f "$SRC_FILE" ]]; then
    echo "Usage: $0 [--chunker] [--chunker-size 500M] <path-to-src-zip> <path-to-manifest> [dest-remote]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PS1_SCRIPT="${SCRIPT_DIR}/rclone_transfer.ps1"

WIN_SRC=$(wslpath -w "$SRC_FILE")
WIN_MANIFEST=$(wslpath -w "$MANIFEST_FILE")
WIN_PS1=$(wslpath -w "$PS1_SCRIPT")

echo "================================================================================"
echo "Starting Windows PowerShell 7 rclone transfer from WSL2..."
echo "================================================================================"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \
    "& '$WIN_PS1' -SourceFile '$WIN_SRC' -ManifestFile '$WIN_MANIFEST' -DestinationRemote '$DEST_REMOTE' -EnableChunker :\$$ENABLE_CHUNKER -ChunkerSplitSize '$CHUNKER_SIZE'"

echo "================================================================================"
echo "Rclone transfer and verification completed successfully!"
echo "================================================================================"

: '
================================================================================
                    VERBOSE / DETAILED TECHNICAL DOCUMENTATION
================================================================================

1. OVERVIEW & PURPOSE
--------------------------------------------------------------------------------
This bash script serves as a seamless interface for Linux users running inside 
WSL2 (Ubuntu/Debian) containers to execute high-bandwidth rclone uploads using 
the host Windows PowerShell 7 (`pwsh.exe` / `powershell.exe`) engine and Windows-native 
`rclone.exe`.

2. PATH TRANSLATION (WSL PATH -> WINDOWS PATH)
--------------------------------------------------------------------------------
- WSL2 Linux filesystem paths (e.g. `/home/fekerr/src/irislime/scratch/archive.zip`)
  are automatically translated into Windows UNC/drive paths 
  (e.g. `\\wsl.localhost\Ubuntu\home\fekerr\src\irislime\scratch\archive.zip`) 
  using `wslpath -w`.
- This allows native Windows binaries like `rclone.exe` to access WSL2 files directly 
  without copying files across filesystems prior to upload.

3. COMMAND LINE OPTIONS & PARAMETERS
--------------------------------------------------------------------------------
- `--chunker` / `-c`:
  Enables rclone chunker overlay. Splits large source files into smaller chunks 
  during upload to enable chunk-level upload retries if connection drops.
- `--chunker-size <size>`:
  Specifies the target split size (default: 500M). Examples: `250M`, `500M`, `1G`.
- `<path-to-src-zip>`:
  Relative or absolute path to the local archive file to upload.
- `<path-to-manifest>`:
  Path to the accompanying metadata/manifest text file describing the archive.
- `[dest-remote]`:
  Target cloud remote and path (e.g., `gdrive:transfer/core12/20260720_ubuntu26_build_logs`).

4. MULTI-CONTAINER REPEATABILITY WORKFLOW
--------------------------------------------------------------------------------
To repeat this compression, manifest generation, and upload process across 
other WSL containers:
1. Copy or mount `tools/rclone_transfer.sh` and `tools/rclone_transfer.ps1`.
2. Compress `build` and `logs` into `scratch/<container_name>_build_and_logs.zip`.
3. Generate `scratch/<container_name>_manifest.txt` with SHA256 checksum & size.
4. Run: `./tools/rclone_transfer.sh --chunker scratch/<container>_zip scratch/<container>_manifest gdrive:transfer/core12/<container>_build_logs`
5. Verify success and clean up local zip.
================================================================================
'
