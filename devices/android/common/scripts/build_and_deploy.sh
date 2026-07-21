#!/usr/bin/env bash
# ==============================================================================
# Build & Deploy Script for Android Pixel Testbeds (Pixel 6a & Pixel 10 Pro XL)
# Timestamp: 260720_1547_001
# Architecture: Out-of-tree NDK C++ CLI & Gradle APK build driver
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMON_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ANDROID_DIR="$(cd "${COMMON_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${ANDROID_DIR}/../.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build/devices"

mkdir -p "${BUILD_DIR}"

echo "=================================================================="
echo " Pixel Testbed Build & Deploy Automation Driver"
echo " Project Root: ${PROJECT_ROOT}"
echo " Output Dir:   ${BUILD_DIR}"
echo " Timestamp:    260720_1547_001"
echo "=================================================================="

# 1. Compile Host Simulation & Native CLI executables
echo "[1/3] Compiling Native C++ Testbed Executables (Out-of-tree)..."
cd "${BUILD_DIR}"

cmake "${PROJECT_ROOT}/devices/android/Pixel6a/native_cli" \
    -B "${BUILD_DIR}/pixel6a" \
    -DCMAKE_BUILD_TYPE=Release

cmake --build "${BUILD_DIR}/pixel6a" --config Release

cmake "${PROJECT_ROOT}/devices/android/Pixel10proxl/native_cli" \
    -B "${BUILD_DIR}/pixel10" \
    -DCMAKE_BUILD_TYPE=Release

cmake --build "${BUILD_DIR}/pixel10" --config Release

echo "[2/3] Verifying Built Artifacts..."
ls -lh "${BUILD_DIR}/pixel6a/pixel6a_infer_cli" || true
ls -lh "${BUILD_DIR}/pixel10/pixel10_infer_cli" || true

echo "[3/3] Checking ADB Connection..."
if command -v adb > /dev/null 2>&1; then
    # Inline comment for Rule 7 exception EXC-018: command -v check for adb CLI presence
    echo "[ADB] ADB is installed and available."
    adb devices -l
else
    echo "[ADB] Notice: ADB not found in host PATH. Native CLI binaries compiled successfully in build/devices/."
fi

echo "=================================================================="
echo " Build & Deploy Pre-flight Check Complete."
echo "=================================================================="
