#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/check_sycl_deps.py
Utility: Intel oneAPI SYCL Dependency & DLL Auditor (Extended)
Description: Audits both the probe executable and ggml-sycl.dll for missing
             or unresolvable DLL dependencies using MSVC dumpbin.
================================================================================
"""

import subprocess
from pathlib import Path

def audit_deps():
    build_dir = Path("/mnt/c/Users/feker/src/win11_env/staging/build_sycl")
    
    exe_candidates = list(build_dir.glob("**/llama-ls-sycl-device.exe"))
    dll_candidates = list(build_dir.glob("**/ggml-sycl.dll"))
    
    if not exe_candidates or not dll_candidates:
        print("[ERROR] Could not find probe executable or ggml-sycl.dll.")
        return

    exe_win = subprocess.run(["wslpath", "-w", str(exe_candidates[0])], capture_output=True, text=True, check=True).stdout.strip()
    dll_win = subprocess.run(["wslpath", "-w", str(dll_candidates[0])], capture_output=True, text=True, check=True).stdout.strip()

    bat_content = f"""@echo off
call "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" >nul 2>&1
echo ===============================================================================
echo [AUDIT] DEPENDENTS OF: {exe_win}
echo ===============================================================================
dumpbin /dependents "{exe_win}"

echo ===============================================================================
echo [AUDIT] DEPENDENTS OF: {dll_win}
echo ===============================================================================
dumpbin /dependents "{dll_win}"
"""
    
    env_dir = Path("/mnt/c/Users/feker/src/win11_env")
    bat_file = env_dir / "check_deps.bat"
    bat_file.write_text(bat_content, encoding="utf-8")
    
    result = subprocess.run(
        ["cmd.exe", "/c", r"C:\Users\feker\src\win11_env\check_deps.bat"],
        cwd="/mnt/c/Users/feker",
        capture_output=True,
        text=True
    )

    print("================================================================================")
    print(" SYCL FULL DEPENDENCY AUDIT")
    print("================================================================================")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("[STDERR]:", result.stderr.strip())
    print("================================================================================")

if __name__ == "__main__":
    audit_deps()
