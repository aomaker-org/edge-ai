#!/usr/bin/env bash
# ==============================================================================
# FILENAME BEGIN: gemini/tools/export_to_gdrive.sh
# ==============================================================================
# Utility: One-Shot Google Drive Exporter
# Description: Uses rclone to push manifests, curriculum PDFs, capture archives,
#             logs, and provenance backups to Google Drive.
# ==============================================================================

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REMOTE_NAME="${1:-gdrive}"
DRIVE_FOLDER="${2:-edge-ai-workspace}"

echo "================================================================================"
echo " GOOGLE DRIVE MASS EXPORTER (RCLONE)"
echo "================================================================================"
echo " Source Root  : ${REPO_ROOT}"
echo " Remote Target: ${REMOTE_NAME}:${DRIVE_FOLDER}/"
echo "================================================================================"

if ! command -v rclone >/dev/null 2>&1; then
    echo "[ERROR] rclone is not installed or not in PATH."
    echo "Install via: sudo apt-get install -y rclone"
    exit 1
fi

# Ensure latest manifest.json exists before exporting
if [ -f "${REPO_ROOT}/gemini/tools/build_manifest.py" ]; then
    echo "\n[1/5] Refreshing root manifest.json..."
    python3 "${REPO_ROOT}/gemini/tools/build_manifest.py" >/dev/null 2>&1 || true
fi

echo "\n[2/5] Syncing Manifests & Core Documentation..."
rclone copy "${REPO_ROOT}/manifest.json" "${REMOTE_NAME}:${DRIVE_FOLDER}/" --ignore-errors || true
rclone copy "${REPO_ROOT}/user/learning/Computer_Engineering_Edge_AI_Curriculum_2026.pdf" "${REMOTE_NAME}:${DRIVE_FOLDER}/docs/" --ignore-errors || true

echo "\n[3/5] Syncing Captures & Archives (gemini/captures/)..."
rclone sync "${REPO_ROOT}/gemini/captures/" "${REMOTE_NAME}:${DRIVE_FOLDER}/captures/" --progress --transfers 4 || true

echo "\n[4/5] Syncing Provenance Backups (gemini/backups/)..."
rclone sync "${REPO_ROOT}/gemini/backups/" "${REMOTE_NAME}:${DRIVE_FOLDER}/backups/" --progress --transfers 4 || true

echo "\n[5/5] Syncing Forensic Build & Test Logs (logs/)..."
rclone sync "${REPO_ROOT}/logs/" "${REMOTE_NAME}:${DRIVE_FOLDER}/logs/" --progress --transfers 4 || true

echo "\n================================================================================"
echo " EXPORT COMPLETE: All workspace assets synced to ${REMOTE_NAME}:${DRIVE_FOLDER}/"
echo "================================================================================"

# ==============================================================================
# FILENAME END: gemini/tools/export_to_gdrive.sh
# ==============================================================================
