#!/usr/bin/env bash
# ==============================================================================
# Path:        tools/tree_log_watcher.sh
# Purpose:     Real-time log file directory tree visualizer ("tree -f")
#              monitoring log creation and updates as produced by concurrent tasks.
# Architecture: Idempotent inotifywait event loop with fallback polling interval.
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

set -euo pipefail
IFS=$'\n\t'

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TARGET_DIR="${1:-${PROJECT_ROOT}/logs}"
INTERVAL="${2:-1}"

# Ensure target directory exists idempotently
mkdir -p "$TARGET_DIR"

# Function to render live tree -f listing
render_tree() {
    local ts
    ts=$(date +%y%m%d_%H%M_%S)
    printf "\033[2J\033[H"
    echo "=========================================================="
    echo " edge-ai Live Log Tree Monitor [${ts}]"
    echo " Target Path: ${TARGET_DIR}"
    echo "=========================================================="
    echo ""
    
    # NECESSARY NULL PIPE: 'command -v' outputs binary path on success; stdout suppressed to keep UI clean.
    if command -v tree > /dev/null 2>&1; then
        tree -f -C -P "*.log|*.csv|*.jsonl" "$TARGET_DIR" 2>/dev/null || tree -f "$TARGET_DIR"
    else
        echo "[!] Notice: 'tree' utility not installed. Falling back to find listing:"
        # NECESSARY NULL PIPE: Suppress stderr when querying find on newly instantiated directory.
        find "$TARGET_DIR" -type f \( -name "*.log" -o -name "*.csv" -o -name "*.jsonl" \) 2>/dev/null || find "$TARGET_DIR" -type f
    fi
}

# Initial render pass
render_tree

# Event-driven inotifywait watcher loop with polling fallback
# NECESSARY NULL PIPE: Mute stdout/stderr during command existence check for inotifywait.
if command -v inotifywait > /dev/null 2>&1; then
    while true; do
        # NECESSARY NULL PIPE: Mute inotifywait output stream so screen re-renders cleanly on filesystem event.
        inotifywait -qq -r -e create,modify,delete,move "$TARGET_DIR" > /dev/null 2>&1 || sleep "$INTERVAL"
        render_tree
    done
else
    while true; do
        sleep "$INTERVAL"
        render_tree
    done
fi
