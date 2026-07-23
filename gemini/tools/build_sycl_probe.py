#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/build_sycl_probe.py
Utility: Intel oneAPI / SYCL Native Windows Diagnostic Staging Runner
Description: Syncs source tree to C:\ NVMe staging and logs builds to both
             timestamped log files and a sycl_probe_latest.log symlink.
================================================================================
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LLAMA_DIR = REPO_ROOT / "deps" / "llama.cpp"
LOG_DIR = REPO_ROOT / "gemini" / "logs"

WIN_STAGING_WSL = Path("/mnt/c/Users/feker/src/win11_env/staging/llama.cpp")
WIN_STAGING_WIN = r"C:\Users\feker\src\win11_env\staging\llama.cpp"
WIN_BUILD_WIN   = r"C:\Users\feker\src\win11_env\staging\build_sycl"

LOG_DIR.mkdir(parents=True, exist_ok=True)
WIN_STAGING_WSL.mkdir(parents=True, exist_ok=True)

quiet_env = os.getenv("QUIET", "0").strip()
verbose_env = os.getenv("V", "0").strip()
IS_QUIET = (quiet_env == "1") and (verbose_env != "1")

def copy_to_clipboard(text: str):
    try:
        subprocess.run(["clip.exe"], input=text, text=True, check=True)
        print("[CLIPBOARD] Copied SYCL summary to Windows clipboard!")
    except Exception as e:
        print(f"[CLIPBOARD NOTICE] Could not pipe to clip.exe: {e}")

def sync_to_native_windows():
    if not IS_QUIET:
        print("[SYNC] Mirroring llama.cpp source to native Windows C:\\ NVMe drive...")
    
    win_src = subprocess.check_output(["wslpath", "-w", str(LLAMA_DIR)], text=True).strip()
    
    cmd = [
        "robocopy.exe", win_src, WIN_STAGING_WIN,
        "/MIR", "/NDL", "/NFL", "/NJH", "/NJS", "/nc", "/ns", "/np",
        "/XD", "build", ".git", "out"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_build():
    sync_to_native_windows()

    if not IS_QUIET:
        print("================================================================================")
        print(" BUILDING INTEL ONEAPI SYCL TARGETS (NATIVE C:\\ NVME STAGING)")
        print("================================================================================")
    else:
        print("[BUILD-SYCL] Compiling Intel oneAPI SYCL device probe natively on C:\\...")

    WIN11_ENV_DIR = Path("/mnt/c/Users/feker/src/fekerr-dev/win11_env")
    bat_file_wsl = WIN11_ENV_DIR / "run_sycl_build.bat"
    bat_file_win = r"C:\Users\feker\src\fekerr-dev\win11_env\run_sycl_build.bat"

    bat_content = f"""@echo off
set "ONEAPI_VARS=C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat"
if not exist "%ONEAPI_VARS%" goto :NO_ONEAPI
call "%ONEAPI_VARS%" >nul 2>&1

git config --global --add safe.directory "*" >nul 2>&1

if not exist "{WIN_BUILD_WIN}" mkdir "{WIN_BUILD_WIN}"
cd /d "{WIN_BUILD_WIN}"

if exist CMakeCache.txt del /f /q CMakeCache.txt
if exist CMakeFiles rmdir /s /q CMakeFiles

cmake "{WIN_STAGING_WIN}" -G "Ninja" ^
    -DCMAKE_C_COMPILER=icx ^
    -DCMAKE_CXX_COMPILER=icx ^
    -DGGML_SYCL=ON ^
    -DLLAMA_BUILD_EXAMPLES=ON ^
    -DGGML_AVX=ON ^
    -DGGML_AVX2=ON ^
    -DGGML_FMA=ON ^
    -DGGML_AVX512=OFF ^
    -DGGML_CCACHE=OFF ^
    -DLLAMA_CURL=OFF ^
    -DCMAKE_BUILD_TYPE=Release

cmake --build . --config Release --target llama-ls-sycl-device -j 4
set "ERR=%ERRORLEVEL%"
exit /b %ERR%

:NO_ONEAPI
echo [WIN11_ENV] Intel oneAPI setvars.bat not found at %ONEAPI_VARS%.
exit /b 1
"""
    bat_file_wsl.write_text(bat_content, encoding="utf-8")

    start_time = datetime.now()
    timestamp_str = start_time.strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"sycl_probe_{timestamp_str}.log"
    latest_log_path = LOG_DIR / "sycl_probe_latest.log"

    output_lines = []

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"=== SYCL BUILD TELEMETRY LOG ===\nTimestamp: {start_time.isoformat()}\n\n")

        proc = subprocess.Popen(
            ["cmd.exe", "/c", bat_file_win],
            cwd="/mnt/c/Users/feker",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in iter(proc.stdout.readline, ''):
            if not IS_QUIET:
                sys.stdout.write(line)
                sys.stdout.flush()
            log_file.write(line)
            log_file.flush()
            output_lines.append(line)

        proc.stdout.close()
        return_code = proc.wait()

    # Update latest symlink / copy shortcut
    try:
        if latest_log_path.exists() or latest_log_path.is_symlink():
            latest_log_path.unlink()
        latest_log_path.symlink_to(log_path.name)
    except Exception:
        latest_log_path.write_text(log_path.read_text(encoding="utf-8"), encoding="utf-8")

    elapsed = (datetime.now() - start_time).total_seconds()

    if return_code == 0:
        summary = f"[SUCCESS] SYCL device probe built in {elapsed:.3f}s on native C:\\ NVMe!\nLog: {log_path}"
        print(summary)
        copy_to_clipboard(summary)
    else:
        real_errors = [
            line for line in output_lines 
            if not line.strip().startswith("--") 
            and any(k in line.lower() for k in ["error", "fatal", "ninja:"])
        ]
        summary = f"[NOTICE] SYCL Host Build Outcome ({elapsed:.3f}s):\n" + "".join(real_errors[:5])
        print(summary)
        copy_to_clipboard(summary)

if __name__ == "__main__":
    run_build()

# ==============================================================================
# FILENAME END: gemini/tools/build_sycl_probe.py
# ==============================================================================
