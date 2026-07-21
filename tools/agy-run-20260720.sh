#!/usr/bin/env bash
# ==============================================================================
# Script:       tools/agy-run-20260720.sh
# Purpose:      High-Autonomy AGY Launch Wrapper for edge-ai Milestone 2
# Standard:     260720_0827_001
# ==============================================================================

set -euo pipefail

# Determine project root dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "=================================================================="
echo " Launching AGY High-Autonomy Execution Vector for edge-ai"
echo " Project Root: ${PROJECT_ROOT}"
echo " Timestamp ID:  260720_0827_001"
echo "=================================================================="

exec agy --dangerously-skip-permissions \
    --add-dir "/home/fekerr/src/irislime" \
    --prompt-interactive "/goal Continue Milestone 2 of edge-ai development. Port the hardware acceleration make modules from irislime/derived_components into infra/make/, verify out-of-tree builds with 'make build', enforce Rule 7 (/dev/null prohibition) and Rule 8 timestamping, sync telemetry with 'make agy-sync', and commit milestone progress using timestamped commits."
