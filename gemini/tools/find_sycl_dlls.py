#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/find_sycl_dlls.py
Utility: Intel SYCL DLL Finder & Loader Tester
Description: Locates sycl9.dll under C:\\Program Files (x86)\\Intel\\oneAPI,
             adds its directory, and verifies ggml-sycl.dll loading.
================================================================================
"""

import subprocess
from pathlib import Path

def main():
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    
    py_script = env_dir / "test_sycl_load.py"
    py_code = """import os
import ctypes
from pathlib import Path

print("[PYTHON] Searching for sycl9.dll and testing ggml-sycl.dll...")

# Search for sycl9.dll under oneAPI installation
oneapi_base = Path(r"C:\\Program Files (x86)\\Intel\\oneAPI")
sycl_candidates = list(oneapi_base.glob("**/sycl9.dll"))

if sycl_candidates:
    sycl_bin_dir = sycl_candidates[0].parent
    print(f"  [FOUND] sycl9.dll at: {sycl_bin_dir}")
    try:
        os.add_dll_directory(str(sycl_bin_dir))
        print(f"  [DLL_DIR ADDED] {sycl_bin_dir}")
    except Exception as e:
        print(f"  [WARNING] {e}")
else:
    print("  [ERROR] Could not find sycl9.dll in oneAPI tree!")

# Also add compiler redist path just in case
redist_path = Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\redist\\intel64\\compiler")
if redist_path.exists():
    try:
        os.add_dll_directory(str(redist_path))
        print(f"  [DLL_DIR ADDED] {redist_path}")
    except:
        pass

compiler_bin = Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\bin")
if compiler_bin.exists():
    try:
        os.add_dll_directory(str(compiler_bin))
        print(f"  [DLL_DIR ADDED] {compiler_bin}")
    except:
        pass

bin_dir = Path(r"C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl\\bin")
os.add_dll_directory(str(bin_dir))

sycl_dll = bin_dir / "ggml-sycl.dll"
print(f"\\n-> Loading: {sycl_dll.name}")
try:
    h = ctypes.CDLL(str(sycl_dll))
    print(f"   [SUCCESS] ggml-sycl.dll loaded! Handle: {h}")
except Exception as e:
    print(f"   [FAILED] ggml-sycl.dll error: {e}")
"""
    py_script.write_text(py_code, encoding="utf-8")

    bat_file = env_dir / "run_sycl_test.bat"
    bat_content = """@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
python C:\\Users\\feker\\src\\win11_env\\test_sycl_load.py
"""
    bat_file.write_text(bat_content, encoding="utf-8")

    result = subprocess.run(
        ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\run_sycl_test.bat"],
        cwd="/mnt/c/Users/feker",
        capture_output=True,
        text=True
    )
    
    print("================================================================================")
    print(" SYCL DLL LOAD TEST REPORT")
    print("================================================================================")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("STDERR:\n" + result.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    main()
