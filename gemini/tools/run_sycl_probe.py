#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/run_sycl_probe.py
Utility: Intel oneAPI SYCL Device Probe Executor (Diagnostic Mode)
Description: Executes llama-ls-sycl-device.exe without suppressing initialization
             errors, capturing real-time stdout/stderr with timestamps.
================================================================================
"""

import time
from datetime import datetime
import subprocess
from pathlib import Path

def run_probe():
    build_dir = Path("/mnt/c/Users/feker/src/win11_env/staging/build_sycl")
    
    candidates = list(build_dir.glob("**/llama-ls-sycl-device.exe"))
    if not candidates:
        print("[ERROR] Could not find llama-ls-sycl-device.exe under the staging build directory.")
        return

    exe_path_wsl = candidates[0]
    
    res_path = subprocess.run(["wslpath", "-w", str(exe_path_wsl)], capture_output=True, text=True, check=True)
    exe_path_win = res_path.stdout.strip()
    print(f"[PROBE] Found binary at: {exe_path_win}")

    # Do NOT suppress setvars.bat output so we can see if oneAPI fails to initialize
    bat_content = f"""@echo off
echo [WIN_ENV] Initializing Intel oneAPI Environment...
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat"
if errorlevel 1 (
    echo [ERROR] oneAPI setvars.bat failed with code %errorlevel%
    exit /b %errorlevel%
)
echo [WIN_ENV] Environment ready. Launching probe...
"{exe_path_win}"
"""
    
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    bat_file_wsl = env_dir / "run_probe.bat"
    bat_file_wsl.write_text(bat_content, encoding="utf-8")
    
    bat_file_win_path = r"C:\Users\feker\src\win11_env\run_probe.bat"

    start_time = time.time()
    print("================================================================================")
    print(" STARTING DIAGNOSTIC SYCL PROBE EXECUTION")
    print("================================================================================")

    proc = subprocess.Popen(
        ["cmd.exe", "/c", bat_file_win_path],
        cwd="/mnt/c/Users/feker",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    import selectors
    sel = selectors.DefaultSelector()
    sel.register(proc.stdout, selectors.EVENT_READ, data="stdout")
    sel.register(proc.stderr, selectors.EVENT_READ, data="stderr")

    while sel.get_map():
        for key, _ in sel.select():
            stream = key.fileobj
            stream_name = key.data
            line = stream.readline()
            if not line:
                sel.unregister(stream)
                continue
            
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(f"({ts}): [{stream_name}]: {line.rstrip()}")

    return_code = proc.wait()
    elapsed = time.time() - start_time

    print("================================================================================")
    print(f" SYCL DEVICE PROBE COMPLETE (Exit Code: {return_code} | Runtime: {elapsed:.3f}s)")
    print("================================================================================")

if __name__ == "__main__":
    run_probe()
