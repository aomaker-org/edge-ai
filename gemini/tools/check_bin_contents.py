#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/check_bin_contents.py
Utility: Targeted Bin Directory Inspector
Description: Lists only the compiled executables and DLLs in the staging bin folder.
================================================================================
"""

from pathlib import Path

def inspect_bin():
    bin_dir = Path("/mnt/c/Users/feker/src/win11_env/staging/build_sycl/bin")
    print(f"Inspecting Bin Dir: {bin_dir}\n")
    
    if not bin_dir.exists():
        print("[ERROR] bin directory does not exist.")
        return

    for f in sorted(bin_dir.glob("*")):
        if f.is_file():
            size_kb = f.stat().st_size / 1024
            print(f"  [{size_kb:8.1f} KB] {f.name}")

if __name__ == "__main__":
    inspect_bin()
