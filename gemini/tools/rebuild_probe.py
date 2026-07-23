#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/rebuild_probe.py
Utility: Batch-backed Incremental Rebuilder for SYCL Probe
Description: Writes a dedicated rebuild.bat script, executes it in a native Windows
             environment context, and streams output live with timestamps.
================================================================================
"""

import time
from datetime import datetime
import subprocess
from pathlib import Path

def main():
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    
    bat_file_wsl = env_dir / "rebuild.bat"
    bat_content = """@echo off
echo [WIN_ENV] Initializing Intel oneAPI Environment for Build...
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] oneAPI setvars.bat failed!
    exit /b 1
)
echo [WIN_ENV] Navigating to build directory...
cd /d C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl
echo [WIN_ENV] Running Ninja for llama-ls-sycl-device...
ninja llama-ls-sycl-device
exit /b %errorlevel%
"""
    bat_file_wsl.write_text(bat_content, encoding="utf-8")
    bat_file_win_path = r"C:\Users\feker\src\win11_env\rebuild.bat"

    start_time = time.time()
    print("================================================================================")
    print(" STARTING INCREMENTAL BUILD STREAM")
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
    print(f" BUILD COMPLETE (Exit Code: {return_code} | Runtime: {elapsed:.3f}s)")
    print("================================================================================")

    if return_code == 0:
        print("[SUCCESS] Incremental build passed! Now running instrumented probe...")
        # Now run the probe
        probe_bat = env_dir / "run_probe_inst.bat"
        probe_content = """@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
set ONEAPI_DEVICE_SELECTOR=level_zero:gpu
"C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl\\bin\\llama-ls-sycl-device.exe"
"""
        probe_bat.write_text(probe_content, encoding="utf-8")
        
        probe_res = subprocess.run(
            ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\run_probe_inst.bat"],
            cwd="/mnt/c/Users/feker",
            capture_output=True,
            text=True
        )
        print("--------------------------------------------------------------------------------")
        print(f" INSTRUMENTED PROBE OUTPUT (Exit Code: {probe_res.returncode})")
        print("--------------------------------------------------------------------------------")
        if probe_res.stdout.strip():
            print("STDOUT:\n" + probe_res.stdout.strip())
        if probe_res.stderr.strip():
            print("STDERR:\n" + probe_res.stderr.strip())
        print("--------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
