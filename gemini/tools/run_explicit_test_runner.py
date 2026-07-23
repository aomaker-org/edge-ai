#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/run_explicit_test_runner.py
Utility: Native Windows DLL Load Test Runner
Description: Writes test_dll_explicit.py directly into the Windows staging
             directory and executes it with proper cwd settings.
================================================================================
"""

import subprocess
from pathlib import Path

def main():
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    
    # Write Python test script to native Windows path
    py_test_script = env_dir / "test_dll_explicit.py"
    py_code = """import os
import ctypes
from pathlib import Path

print("[PYTHON] Testing explicit DLL loading with os.add_dll_directory()...")

intel_paths = [
    Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\bin"),
    Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\redist\\intel64\\compiler"),
    Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\mkl\\latest\\bin"),
]

for p in intel_paths:
    if p.exists():
        try:
            os.add_dll_directory(str(p))
            print(f"  [DLL_DIR ADDED] {p}")
        except Exception as e:
            print(f"  [WARNING] Could not add {p}: {e}")

bin_dir = Path(r"C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl\\bin")
if bin_dir.exists():
    os.add_dll_directory(str(bin_dir))
    print(f"  [DLL_DIR ADDED] {bin_dir}")

base_dll = bin_dir / "ggml-base.dll"
sycl_dll = bin_dir / "ggml-sycl.dll"

for dll_path in [base_dll, sycl_dll]:
    print(f"\\n-> Loading: {dll_path.name}")
    try:
        h = ctypes.CDLL(str(dll_path))
        print(f"   [SUCCESS] Loaded! Handle: {h}")
    except Exception as e:
        print(f"   [FAILED] Error: {e}")
"""
    py_test_script.write_text(py_code, encoding="utf-8")

    # Write batch wrapper
    bat_file = env_dir / "run_explicit_test.bat"
    bat_content = """@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
python C:\\Users\\feker\\src\\win11_env\\test_dll_explicit.py
"""
    bat_file.write_text(bat_content, encoding="utf-8")

    print("[RUN] Executing explicit DLL load test in native Windows context...")
    result = subprocess.run(
        ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\run_explicit_test.bat"],
        cwd="/mnt/c/Users/feker",
        capture_output=True,
        text=True
    )
    
    print("================================================================================")
    print(" EXPLICIT DLL LOAD TEST REPORT")
    print("================================================================================")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("STDERR:\n" + result.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    main()
