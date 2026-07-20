#!/usr/bin/env bash
# ==============================================================================
# Script:       tools/agy-next-work.sh
# Purpose:      High-Autonomy AGY Launch Wrapper for edge-ai Milestone 2 Next Steps
# Standard:     260720_0834_001
# ==============================================================================

set -euo pipefail

# Determine project root dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "=================================================================="
echo " Launching AGY High-Autonomy Execution Vector for edge-ai"
echo " Project Root: ${PROJECT_ROOT}"
echo " Timestamp ID:  260720_0834_001"
echo "=================================================================="

exec agy --dangerously-skip-permissions \
    --add-dir "/home/fekerr/src/irislime" \
    --prompt-interactive "/goal Continue Milestone 2 of edge-ai development. Implement isolated hardware inference validation targets ('make test'), set up 'uv' environment dependency management in pyproject.toml, verify out-of-tree builds with 'make build' and 'make test', enforce Rule 7 (/dev/null prohibition) and Rule 8 timestamping standard, sync telemetry with 'make agy-sync', and commit milestone progress using timestamped commits."
