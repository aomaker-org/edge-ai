#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/run_sycl_probe_advanced.py
Utility: Advanced Intel oneAPI SYCL Probe Runner
Description: Configures ONEAPI_DEVICE_SELECTOR and executes llama-ls-sycl-device.exe,
             capturing exact runtime telemetry and stdout/stderr streams.
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
        print("[ERROR] Could not find llama-ls-sycl-device.exe.")
        return

    exe_path_win = subprocess.run(
        ["wslpath", "-w", str(candidates[0])], 
        capture_output=True, text=True, check=True
    ).stdout.strip()

    # Batch script with explicit device selector and environment variables
    bat_content = f"""@echo off
set ONEAPI_DEVICE_SELECTOR=level_zero:gpu
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
echo [WIN_ENV] Launching probe with selector: %ONEAPI_DEVICE_SELECTOR%
"{exe_path_win}"
"""
    
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    bat_file_wsl = env_dir / "run_probe_adv.bat"
    bat_file_wsl.write_text(bat_content, encoding="utf-8")
    
    bat_file_win_path = r"C:\Users\feker\src\win11_env\run_probe_adv.bat"

    start_time = time.time()
    print("================================================================================")
    print(" RUNNING ADVANCED SYCL DEVICE PROBE")
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
    print(f" PROBE FINISHED (Exit Code: {return_code} | Runtime: {elapsed:.3f}s)")
    print("================================================================================")

if __name__ == "__main__":
    run_probe()
