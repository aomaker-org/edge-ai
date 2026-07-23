#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/check_base_deps.py
Utility: ggml-base.dll Dependency Auditor
Description: Runs MSVC dumpbin on ggml-base.dll to see its exact link requirements.
================================================================================
"""

import subprocess
from pathlib import Path

def main():
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    env_dir.mkdir(parents=True, exist_ok=True)
    
    base_dll_path = r"C:\Users\feker\src\win11_env\staging\build_sycl\bin\ggml-base.dll"
    
    bat_file = env_dir / "check_base.bat"
    bat_content = f"""@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
echo === DEPENDENTS OF ggml-base.dll ===
dumpbin /dependents "{base_dll_path}"
"""
    bat_file.write_text(bat_content, encoding="utf-8")
    
    result = subprocess.run(
        ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\check_base.bat"],
        cwd="/mnt/c/Users/feker",
        capture_output=True,
        text=True
    )
    
    print("================================================================================")
    print(" GGML-BASE.DLL DEPENDENCY AUDIT")
    print("================================================================================")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("STDERR:\n" + result.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    main()
