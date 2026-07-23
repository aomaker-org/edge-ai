#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/sanitize_ps_profile.py
================================================================================
Utility: PowerShell 7 Profile Sanitizer
Description: Strips MTF/AGY cruft and duplicate prompts from $PROFILE,
             restoring a clean, fast dynamic CWD prompt function.
================================================================================
"""

import re
import subprocess
from pathlib import Path

def get_win_userprofile() -> Path:
    try:
        raw_path = subprocess.check_output(
            ["cmd.exe", "/c", "echo %USERPROFILE%"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        wsl_path = subprocess.check_output(
            ["wslpath", "-u", raw_path],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        return Path(wsl_path)
    except Exception:
        return None

def sanitize_profile():
    win_user = get_win_userprofile()
    if not win_user:
        print("[ERROR] Could not resolve Windows %USERPROFILE%.")
        return

    profile_paths = [
        win_user / "OneDrive" / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1",
        win_user / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1",
    ]

    target_profile = None
    for p in profile_paths:
        if p.exists():
            target_profile = p
            break

    if not target_profile:
        print("[ERROR] Could not locate PowerShell $PROFILE.")
        return

    print(f"Sanitizing Profile: {target_profile}")
    raw_lines = target_profile.read_text(encoding="utf-8", errors="replace").splitlines()

    clean_lines = []
    in_prompt_block = False
    stripped_count = 0

    for line in raw_lines:
        # 1. Filter out MTF / AGY references and environment variables
        if re.search(r'mtf|MTF_|Get-Mtf|Write-Mtf|agy', line, re.IGNORECASE):
            stripped_count += 1
            continue

        # 2. Filter out old/duplicate prompt functions
        if re.search(r'function\s+(global:)?prompt', line, re.IGNORECASE):
            in_prompt_block = True
            stripped_count += 1
            continue

        if in_prompt_block:
            stripped_count += 1
            if line.strip() == "}":
                in_prompt_block = False
            continue

        clean_lines.append(line)

    # Remove empty trailing lines
    while clean_lines and not clean_lines[-1].strip():
        clean_lines.pop()

    # 3. Append single, clean, dynamic CWD prompt function
    clean_lines.append("")
    clean_lines.append("# ==============================================================================")
    clean_lines.append("# CLEAN DYNAMIC CWD PROMPT (RESTORED)")
    clean_lines.append("# ==============================================================================")
    clean_lines.append("function global:prompt {")
    clean_lines.append('    "PS $($executionContext.SessionState.Path.CurrentLocation)> "')
    clean_lines.append("}")
    clean_lines.append("")

    target_profile.write_text("\n".join(clean_lines) + "\n", encoding="utf-8")
    print(f"[SUCCESS] Sanitized profile written! Removed {stripped_count} lines of MTF/prompt noise.")

if __name__ == "__main__":
    sanitize_profile()

"""
================================================================================
FILENAME END: gemini/tools/sanitize_ps_profile.py
================================================================================
"""
