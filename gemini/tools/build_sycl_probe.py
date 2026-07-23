#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/build_sycl_probe.py
Utility: Intel oneAPI / SYCL Native Windows Diagnostic Build Runner
Description: Configures and compiles llama.cpp's SYCL backend via Windows CMake 
             and Intel oneAPI setvars.bat on the host Windows environment.
================================================================================
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LLAMA_DIR = REPO_ROOT / "deps" / "llama.cpp"
BUILD_DIR = REPO_ROOT / "build" / "win_sycl"
LOG_DIR = REPO_ROOT / "gemini" / "logs"
WIN11_ENV_DIR = Path("/mnt/c/Users/feker/src/fekerr-dev/win11_env")

BUILD_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
WIN11_ENV_DIR.mkdir(parents=True, exist_ok=True)

win_llama = subprocess.check_output(["wslpath", "-w", str(LLAMA_DIR)], text=True).strip()
win_build = subprocess.check_output(["wslpath", "-w", str(BUILD_DIR)], text=True).strip()

def copy_to_clipboard(text: str):
    try:
        subprocess.run(["clip.exe"], input=text, text=True, check=True)
        print("[CLIPBOARD] Copied SYCL summary to Windows clipboard!")
    except Exception as e:
        print(f"[CLIPBOARD NOTICE] Could not pipe to clip.exe: {e}")

def run_build():
    print("================================================================================")
    print(" BUILDING INTEL ONEAPI SYCL TARGETS (WINDOWS HOST)")
    print("================================================================================")

    bat_file_wsl = WIN11_ENV_DIR / "run_sycl_build.bat"
    bat_file_win = r"C:\Users\feker\src\fekerr-dev\win11_env\run_sycl_build.bat"

    oneapi_vars = r"C:\Program Files (x86)\Intel\oneAPI\setvars.bat"

    bat_content = f"""@echo off
if exist "{oneapi_vars}" (
    call "{oneapi_vars}" >nul 2>&1
    echo [WIN11_ENV] Initialized Intel oneAPI Environment.
    cd /d "{win_build}"
    cmake "{win_llama}" -G "NMake Makefiles" -DGGML_SYCL=ON -DCMAKE_BUILD_TYPE=Release
    nmake llama-ls-sycl-device
) else (
    echo [WIN11_ENV] Intel oneAPI setvars.bat not found at {oneapi_vars}.
    echo [WIN11_ENV] Please verify Intel oneAPI Base Toolkit is installed on Windows 11 host.
    exit /b 1
)
"""
    bat_file_wsl.write_text(bat_content, encoding="utf-8")

    log_path = LOG_DIR / "sycl_probe_build.log"
    start_time = datetime.now()

    res = subprocess.run(
        ["cmd.exe", "/c", bat_file_win],
        cwd="/mnt/c/Users/feker",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    log_body = f"=== SYCL BUILD TELEMETRY LOG ===\nTimestamp: {datetime.now().isoformat()}\nDuration: {elapsed:.3f}s\nExit Code: {res.returncode}\n=== STDOUT/STDERR ===\n{res.stdout}"
    log_path.write_text(log_body, encoding="utf-8")

    print(res.stdout)

    if res.returncode == 0:
        summary = f"[SUCCESS] SYCL device probe built in {elapsed:.3f}s!\nLog: {log_path}"
        print(summary)
        copy_to_clipboard(summary)
    else:
        err_lines = [line for line in res.stdout.splitlines() if "error" in line.lower() or "not found" in line.lower()]
        summary = f"[NOTICE] SYCL Host Build Result ({elapsed:.3f}s):\n" + "\n".join(err_lines[:5])
        print("--------------------------------------------------------------------------------")
        print(summary)
        print("--------------------------------------------------------------------------------")
        copy_to_clipboard(summary)

if __name__ == "__main__":
    run_build()

# ==============================================================================
# FILENAME END: gemini/tools/build_sycl_probe.py
# ==============================================================================
