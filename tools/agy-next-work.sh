#!/usr/bin/env bash
# ==============================================================================
# Script:       tools/agy-next-work.sh
# Purpose:      High-Autonomy AGY Launch Wrapper for edge-ai Hardware-Throttled Build & Provisioning Vector
# Standard:     260720_0841_001
# ==============================================================================

set -euo pipefail

# Determine project root dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "=================================================================="
echo " Launching AGY High-Autonomy Execution Vector for edge-ai"
echo " Project Root: ${PROJECT_ROOT}"
echo " Timestamp ID:  260720_0841_001"
echo " Throttling:    < 50% CPU/RAM Load Limit (Cool & Quiet Execution)"
echo "=================================================================="

exec agy --dangerously-skip-permissions \
    --add-dir "/home/fekerr/src/irislime" \
    --prompt-interactive "/goal Execute next work cycle for edge-ai under strict hardware resource throttling (<50% CPU/RAM load, keeping laptop cool and quiet). Perform out-of-tree builds (edge-ai build/, logs/, docs/) incorporating submodules in edge-ai/irislime/irislime. Verify build times, laptop CPU load, memory use, SSD disk I/O, and ethernet load telemetry. Validate that README.md, GETTING_STARTED.md, and QUICK_START.md include full git clone --recurse-submodules and git submodule update --init --recursive instructions. Audit aomaker-org/llama.cpp fork changes in docs/LLAMA_CPP_FORK_AUDIT.md and confirm patch necessity. Review irislime/provision.sh and docs/PROVISIONING_NOTES.md (Win11 PS7 winget, WSL2 Ubuntu 26, Native Windows vs WSL2 builds). Implement TODO items for native Linux builds, GitHub Codespaces devcontainer, and Docker containerization. Ensure all documentation maintains both concise (TL;DR) and verbose (architectural) formats for human and agent comprehension. Enforce Rule 7 (/dev/null prohibition) and Rule 8 timestamping standard, sync telemetry with 'make agy-sync', and commit progress using timestamped commits."
