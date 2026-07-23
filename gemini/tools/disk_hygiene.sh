#!/usr/bin/env bash
# ==============================================================================
# FILENAME BEGIN: gemini/tools/disk_hygiene.sh
# ==============================================================================
# Utility: SSD Disk Footprint Auditor & Garbage Collector
# Description: Reports disk space usage across WSL2, Docker, Cargo targets,
#             ccache, and gemini captures, providing one-shot cleanup options.
# ==============================================================================

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "================================================================================"
echo " EDGE-AI SSD DISK FOOTPRINT AUDIT"
echo "================================================================================"
echo " Root Directory: ${REPO_ROOT}"
echo "================================================================================"

# 1. System Root Disk Space
echo "\n[1] WSL2 System File System Space:"
df -h / | awk 'NR==1 || NR==2'

# 2. Build & Target Artifact Sizes
echo "\n[2] Out-of-Tree Build & Cache Sizes:"
if [ -d "${REPO_ROOT}/build" ]; then
    du -sh "${REPO_ROOT}/build" 2>/dev/null || true
else
    echo "  - build/ : 0 MB (Clean)"
fi

if [ -d "${REPO_ROOT}/src/tools/gix_manifest/target" ]; then
    du -sh "${REPO_ROOT}/src/tools/gix_manifest/target" 2>/dev/null || true
fi

# 3. Docker Disk Usage (if daemon is active)
echo "\n[3] Docker Engine Storage Status:"
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    docker system df
else
    echo "  - Docker daemon inactive or not installed."
fi

# 4. Optional Cleanup Action
if [ "$1" == "--clean" ]; then
    echo "\n================================================================================"
    echo " EXECUTING AGGRESSIVE SSD DISK CLEANUP"
    echo "================================================================================"
    echo "-> Clearing transient build/ outputs..."
    rm -rf "${REPO_ROOT}/build/*"
    
    echo "-> Pruning Cargo target directories..."
    cargo clean --manifest-path "${REPO_ROOT}/src/tools/gix_manifest/Cargo.toml" 2>/dev/null || true
    
    if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
        echo "-> Pruning unused Docker containers, networks, and build cache..."
        docker system prune -f
    fi
    
    echo "\n[SUCCESS] Cleanup complete! Disk reclaimed."
fi

echo "================================================================================"
echo " RUN WITH --clean TO RECLAIM SPACE: ./gemini/tools/disk_hygiene.sh --clean"
echo "================================================================================"

# ==============================================================================
# FILENAME END: gemini/tools/disk_hygiene.sh
# ==============================================================================
