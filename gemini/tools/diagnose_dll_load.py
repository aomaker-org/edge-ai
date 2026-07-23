#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/diagnose_dll_load.py
Utility: Robust Windows DLL Load Diagnostician
Description: Writes a standalone Python ctypes test script to Windows,
             initializes oneAPI, and executes it to capture exact loader exceptions.
================================================================================
"""

import subprocess
from pathlib import Path

def main():
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Write standalone Python script
    py_test_script = env_dir / "test_dlls.py"
    py_code = """import ctypes
import sys
from pathlib import Path

print("[PYTHON] Environment active. Testing DLL loads...")

base_dll = Path(r"C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl\\bin\\ggml-base.dll")
sycl_dll = Path(r"C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl\\bin\\ggml-sycl.dll")

print(f"-> Loading: {base_dll.name}")
try:
    h_base = ctypes.CDLL(str(base_dll))
    print(f"   [SUCCESS] ggml-base.dll loaded! Handle: {h_base}")
except Exception as e:
    print(f"   [FAILED] ggml-base.dll error: {e}")

print(f"-> Loading: {sycl_dll.name}")
try:
    h_sycl = ctypes.CDLL(str(sycl_dll))
    print(f"   [SUCCESS] ggml-sycl.dll loaded! Handle: {h_sycl}")
except Exception as e:
    print(f"   [FAILED] ggml-sycl.dll error: {e}")
"""
    py_test_script.write_text(py_code, encoding="utf-8")

    # 2. Write batch runner wrapper
    bat_file = env_dir / "run_dll_test.bat"
    bat_content = """@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
python C:\\Users\\feker\\src\\win11_env\\test_dlls.py
"""
    bat_file.write_text(bat_content, encoding="utf-8")

    print("[RUN] Executing DLL load diagnostics...")
    result = subprocess.run(
        ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\run_dll_test.bat"],
        cwd="/mnt/c/Users/feker",
        capture_output=True,
        text=True
    )
    
    print("================================================================================")
    print(" DLL LOAD DIAGNOSTIC REPORT")
    print("================================================================================")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("STDERR:\n" + result.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    main()
