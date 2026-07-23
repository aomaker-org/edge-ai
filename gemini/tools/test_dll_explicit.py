#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/test_dll_explicit.py
Utility: Explicit Intel oneAPI DLL Loader Test
Description: Uses os.add_dll_directory() to explicitly include Intel compiler
             and runtime paths before loading ggml-base.dll and ggml-sycl.dll.
================================================================================
"""

import os
import ctypes
from pathlib import Path

def main():
    print("[PYTHON] Testing explicit DLL loading with os.add_dll_directory()...")
    
    # Explicitly add Intel oneAPI compiler and bin directories
    intel_paths = [
        Path(r"C:\Program Files (x86)\Intel\oneAPI\compiler\latest\bin"),
        Path(r"C:\Program Files (x86)\Intel\oneAPI\compiler\latest\windows\redist\intel64\compiler"),
        Path(r"C:\Program Files (x86)\Intel\oneAPI\mkl\latest\bin"),
    ]
    
    for p in intel_paths:
        if p.exists():
            try:
                os.add_dll_directory(str(p))
                print(f"  [DLL_DIR ADDED] {p}")
            except Exception as e:
                print(f"  [WARNING] Could not add {p}: {e}")
        else:
            print(f"  [NOT FOUND] {p}")

    bin_dir = Path(r"C:\Users\feker\src\win11_env\staging\build_sycl\bin")
    if bin_dir.exists():
        os.add_dll_directory(str(bin_dir))
        print(f"  [DLL_DIR ADDED] {bin_dir}")

    base_dll = bin_dir / "ggml-base.dll"
    sycl_dll = bin_dir / "ggml-sycl.dll"
    probe_exe = bin_dir / "llama-ls-sycl-device.exe"

    print(f"\n-> Loading: {base_dll.name}")
    try:
        h_base = ctypes.CDLL(str(base_dll))
        print(f"   [SUCCESS] ggml-base.dll loaded! Handle: {h_base}")
    except Exception as e:
        print(f"   [FAILED] ggml-base.dll error: {e}")

    print(f"\n-> Loading: {sycl_dll.name}")
    try:
        h_sycl = ctypes.CDLL(str(sycl_dll))
        print(f"   [SUCCESS] ggml-sycl.dll loaded! Handle: {h_sycl}")
    except Exception as e:
        print(f"   [FAILED] ggml-sycl.dll error: {e}")

if __name__ == "__main__":
    main()
