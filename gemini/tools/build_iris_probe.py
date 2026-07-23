#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/build_iris_probe.py
================================================================================
Utility: Robust Windows Iris Xe Debug Build, Log Tee & Clipboard Feeder
Description: Compiles iris_xe_probe.cpp with MSVC, tees output to logs, and
             automatically feeds build highlights to Windows clip.exe.
================================================================================
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = REPO_ROOT / "src" / "win_iris_probe"
BUILD_DIR = REPO_ROOT / "build" / "win_iris_probe"
LOG_DIR = REPO_ROOT / "gemini" / "logs"
WIN11_ENV_DIR = Path("/mnt/c/Users/feker/src/fekerr-dev/win11_env")

BUILD_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
WIN11_ENV_DIR.mkdir(parents=True, exist_ok=True)

win_src = subprocess.check_output(["wslpath", "-w", str(SRC_DIR / "iris_xe_probe.cpp")], text=True).strip()
win_out = subprocess.check_output(["wslpath", "-w", str(BUILD_DIR / "iris_xe_probe.exe")], text=True).strip()
win_build_dir = subprocess.check_output(["wslpath", "-w", str(BUILD_DIR)], text=True).strip()

def copy_to_clipboard(text: str):
    """Pipes text directly to Windows Clipboard via clip.exe."""
    try:
        subprocess.run(["clip.exe"], input=text, text=True, check=True)
        print("[CLIPBOARD] Automatically copied build summary to Windows clipboard!")
    except Exception as e:
        print(f"[CLIPBOARD NOTICE] Could not pipe to clip.exe: {e}")

def run_build():
    print("================================================================================")
    print(" BUILDING WINDOWS IRIS XE PROBE (DEBUG BUILD + TELEMETRY)")
    print("================================================================================")

    bat_file_wsl = WIN11_ENV_DIR / "run_iris_build.bat"
    bat_file_win = r"C:\Users\feker\src\fekerr-dev\win11_env\run_iris_build.bat"

    bat_content = f"""@echo off
echo [WIN11_ENV] Initializing VS2022 x64 Environment...
call "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\VsDevCmd.bat" -arch=amd64
echo [WIN11_ENV] Compiling Iris Xe Probe with MSVC cl.exe...
cl.exe /nologo /W4 /Zi /Od /EHsc /diagnostics:column /Fd"{win_build_dir}\\iris_xe_probe.pdb" /Fo"{win_build_dir}\\iris_xe_probe.obj" "{win_src}" /link dxgi.lib /OUT:"{win_out}"
"""
    bat_file_wsl.write_text(bat_content, encoding="utf-8")

    log_path = LOG_DIR / "iris_probe_build_telemetry.log"
    latest_log = LOG_DIR / "latest_build.log"

    start_time = datetime.now()

    res = subprocess.run(
        ["cmd.exe", "/c", bat_file_win],
        cwd="/mnt/c/Users/feker",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    exe_linux_path = BUILD_DIR / "iris_xe_probe.exe"
    if exe_linux_path.exists():
        os.chmod(exe_linux_path, 0o755)

    # Log Teeing
    log_body = f"=== BUILD TELEMETRY LOG ===\nTimestamp: {datetime.now().isoformat()}\nBuild Duration: {elapsed:.3f}s\nExit Code: {res.returncode}\n=== STDOUT/STDERR ===\n{res.stdout}"
    log_path.write_text(log_body, encoding="utf-8")
    latest_log.write_text(log_body, encoding="utf-8")

    print(res.stdout)

    # Extract snippet for Windows Clipboard
    if res.returncode == 0:
        summary_clip = f"[SUCCESS] MSVC Debug Build Completed in {elapsed:.3f}s!\nExecutable: {exe_linux_path}\nLog: {log_path}"
        print("--------------------------------------------------------------------------------")
        print(summary_clip)
        print("--------------------------------------------------------------------------------")
        copy_to_clipboard(summary_clip)
    else:
        # Extract compiler error lines for quick AI debugging
        error_lines = [line for line in res.stdout.splitlines() if "error" in line.lower() or "warning" in line.lower()]
        err_snippet = "\n".join(error_lines[:10])
        clip_content = f"[BUILD FAILED] Exit Code {res.returncode} ({elapsed:.3f}s)\nErrors:\n{err_snippet}"
        print("--------------------------------------------------------------------------------")
        print(f"[ERROR] Build failed with exit code {res.returncode}.")
        print("--------------------------------------------------------------------------------")
        copy_to_clipboard(clip_content)

if __name__ == "__main__":
    run_build()

"""
================================================================================
FILENAME END: gemini/tools/build_iris_probe.py
================================================================================
"""
