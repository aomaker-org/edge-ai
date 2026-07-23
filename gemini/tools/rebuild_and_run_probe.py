#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/rebuild_and_run_probe.py
Utility: Instrumented Build & Run Probe Runner (Verbose Debug)
Description: Triggers incremental Ninja build and prints all stdout/stderr on failure.
================================================================================
"""

import subprocess
from pathlib import Path

def main():
    build_dir = Path("/mnt/c/Users/feker/src/win11_env/staging/build_sycl")
    
    print("[BUILD] Triggering incremental Ninja build for ls-sycl-device...")
    
    cmd = 'call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1 && cd /d C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl && ninja llama-ls-sycl-device'
    
    build_res = subprocess.run(
        ["cmd.exe", "/c", cmd],
        cwd="/mnt/c/Users/feker",
        capture_output=True, 
        text=True
    )
    
    print(f"[BUILD] Exit Code: {build_res.returncode}")
    if build_res.stdout.strip():
        print("--- STDOUT ---")
        print(build_res.stdout.strip())
    if build_res.stderr.strip():
        print("--- STDERR ---")
        print(build_res.stderr.strip())
        
    if build_res.returncode != 0:
        print("[ERROR] Build failed.")
        return

    print("[BUILD] Build complete! Executing instrumented probe...")
    
    candidates = list(build_dir.glob("**/llama-ls-sycl-device.exe"))
    if not candidates:
        print("[ERROR] Binary not found.")
        return
        
    exe_win = subprocess.run(["wslpath", "-w", str(candidates[0])], capture_output=True, text=True, check=True).stdout.strip()
    
    run_res = subprocess.run(
        ["cmd.exe", "/c", f'call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1 && set ONEAPI_DEVICE_SELECTOR=level_zero:gpu && "{exe_win}"'],
        cwd="/mnt/c/Users/feker",
        capture_output=True, 
        text=True
    )
    
    print("================================================================================")
    print(f" INSTRUMENTED PROBE OUTPUT (Exit Code: {run_res.returncode})")
    print("================================================================================")
    if run_res.stdout.strip():
        print("STDOUT:\n" + run_res.stdout.strip())
    if run_res.stderr.strip():
        print("STDERR:\n" + run_res.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    main()
