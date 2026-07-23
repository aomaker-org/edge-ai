#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/find_all_oneapi_dlls.py
Utility: Comprehensive oneAPI DLL Finder & Dependency Loader
Description: Locates all required oneAPI dependency directories (dnnl, mkl, sycl)
             and tests loading ggml-sycl.dll.
================================================================================
"""

import subprocess
from pathlib import Path

def main():
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    
    py_script = env_dir / "test_all_dlls.py"
    py_code = """import os
import ctypes
from pathlib import Path

print("[PYTHON] Searching for all oneAPI dependency directories...")

oneapi_base = Path(r"C:\\Program Files (x86)\\Intel\\oneAPI")

targets = ["sycl9.dll", "dnnl.dll", "mkl_sycl_blas.6.dll"]
found_dirs = set()

for target in targets:
    matches = list(oneapi_base.glob(f"**/{target}"))
    if matches:
        d = matches[0].parent
        found_dirs.add(d)
        print(f"  [FOUND] {target} -> {d}")
    else:
        print(f"  [MISSING] Could not find {target}")

for d in found_dirs:
    try:
        os.add_dll_directory(str(d))
        print(f"  [DLL_DIR ADDED] {d}")
    except Exception as e:
        print(f"  [WARNING] {e}")

# Also add compiler redist and bin paths
for extra in [
    Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\bin"),
    Path(r"C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\redist\\intel64\\compiler")
]:
    if extra.exists():
        try:
            os.add_dll_directory(str(extra))
            print(f"  [DLL_DIR ADDED] {extra}")
        except:
            pass

bin_dir = Path(r"C:\\Users\\feker\\src\\win11_env\\staging\\build_sycl\\bin")
if bin_dir.exists():
    os.add_dll_directory(str(bin_dir))
    print(f"  [DLL_DIR ADDED] {bin_dir}")

sycl_dll = bin_dir / "ggml-sycl.dll"
print(f"\\n-> Loading: {sycl_dll.name}")
try:
    h = ctypes.CDLL(str(sycl_dll))
    print(f"   [SUCCESS] ggml-sycl.dll loaded! Handle: {h}")
except Exception as e:
    print(f"   [FAILED] ggml-sycl.dll error: {e}")
"""
    py_script.write_text(py_code, encoding="utf-8")

    bat_file = env_dir / "run_all_test.bat"
    bat_content = """@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
python C:\\Users\\feker\\src\\win11_env\\test_all_dlls.py
"""
    bat_file.write_text(bat_content, encoding="utf-8")

    result = subprocess.run(
        ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\run_all_test.bat"],
        cwd="/mnt/c/Users/feker",
        capture_output=True,
        text=True
    )
    
    print("================================================================================")
    print(" ALL-DLL LOAD TEST REPORT")
    print("================================================================================")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("STDERR:\n" + result.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    main()
