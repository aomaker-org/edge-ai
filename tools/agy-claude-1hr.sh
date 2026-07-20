#!/usr/bin/env bash
# ==============================================================================
# Script:       tools/agy-claude-1hr.sh
# Purpose:      Launch high-autonomy AGY work cycle configured with Claude 3.7 Sonnet
#               for 1 hour (3600 seconds) of clock-time budget.
# Rule Tag:     260720_1402_001
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

TIMESTAMP_TAG=$(date +'%y%m%d_%H%M')
NEW_BRANCH="feat/work-cycle-claude-${TIMESTAMP_TAG}"
LOG_FILE="${PROJECT_ROOT}/logs/agy_claude_1hr_${TIMESTAMP_TAG}.log"
START_TIME=$(date +%s)
ONE_HOUR_SEC=3600

echo "=================================================================="
echo " Launching AGY Claude 3.7 Sonnet 1-Hour Work Cycle"
echo " Project Root : ${PROJECT_ROOT}"
echo " Timestamp Tag: ${TIMESTAMP_TAG}"
echo " Target Branch: ${NEW_BRANCH}"
echo " Model Target : Claude 3.7 Sonnet (Anthropic)"
echo " Clock Time   : 1 Hour Budget (3600 Seconds)"
echo " Log Location : ${LOG_FILE}"
echo "=================================================================="

# 1. Create and checkout a new branch for the work cycle
if [ "$(git rev-parse --abbrev-ref HEAD)" = "main" ]; then
    echo "[*] Creating and checking out new feature branch: ${NEW_BRANCH}"
    git checkout -b "${NEW_BRANCH}" || git checkout "${NEW_BRANCH}"
fi

# 2. Run Ingestion Report and Understanding of Work Generator
echo "[*] Generating Ingestion Report & Understanding of Work..."
python3 "${PROJECT_ROOT}/tools/generate_ingestion_report.py"

# 3. Log session initialization
mkdir -p "${PROJECT_ROOT}/logs"
{
    echo "=== AGY Claude 3.7 Sonnet 1-Hour Session Log ==="
    echo "Start Time     : $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
    echo "Start Epoch    : ${START_TIME}"
    echo "Model Config   : claude-3-7-sonnet"
    echo "Active Branch  : $(git rev-parse --abbrev-ref HEAD)"
    echo "Time Limit     : 3600 seconds (1 hour)"
    echo "================================================="
} | tee -a "${LOG_FILE}"

# 4. Spawn a background timer in bash to track 1 hour of clock time
(
    sleep "${ONE_HOUR_SEC}"
    END_TIME=$(date +%s)
    echo "" | tee -a "${LOG_FILE}"
    echo "[!] ⏱️ 1-HOUR CLOCK TIME BUDGET ELAPSED [$(date -u +'%Y-%m-%d %H:%M:%S UTC')]" | tee -a "${LOG_FILE}"
    echo "[!] Claude 3.7 Sonnet 1-hour window has expired. Please sync telemetry with 'make agy-sync'." | tee -a "${LOG_FILE}"
) &
TIMER_PID=$!

echo "[*] Background 1-hour clock-time monitor started (PID: ${TIMER_PID})."
echo "[*] Launching AGY CLI with Claude 3.7 Sonnet configuration..."

# Execute agy CLI with Claude 3.7 Sonnet model parameter
exec agy --model claude-3-7-sonnet \
    --dangerously-skip-permissions \
    --add-dir "/home/fekerr/src/irislime" \
    --prompt-interactive "/goal Execute next work cycle for edge-ai on branch $(git rev-parse --abbrev-ref HEAD) using Claude 3.7 Sonnet under 1-hour clock-time budget constraint. Perform out-of-tree builds (build/, logs/), verify unit tests with 'make test-all', generate asset manifest with 'make manifest-build', enforce <50% laptop CPU throttling, log all actions under Rule 7 (/dev/null prohibition) and Rule 8 timestamping standards, and sync telemetry with 'make agy-sync'."
