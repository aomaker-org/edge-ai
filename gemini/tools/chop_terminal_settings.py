#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/chop_terminal_settings.py
================================================================================
Utility: Aggressive Windows Terminal Settings Chopper
Description: Completely purges all hidden profiles, legacy VS toolchains, and
             orphaned WSL distros from settings.json.
================================================================================
"""

import json
import re
import subprocess
from pathlib import Path

def strip_json_comments(json_str: str) -> str:
    lines = []
    for line in json_str.splitlines():
        in_quote = False
        clean_chars = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == '"' and (i == 0 or line[i-1] != '\\'):
                in_quote = not in_quote
            if not in_quote and c == '/' and i + 1 < len(line) and line[i+1] == '/':
                break
            clean_chars.append(c)
            i += 1
        lines.append("".join(clean_chars))
    return "\n".join(lines)

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

def chop_settings():
    win_user = get_win_userprofile()
    if not win_user:
        print("[ERROR] Could not resolve Windows %USERPROFILE%.")
        return

    appdata = win_user / "AppData" / "Local"
    wt_paths = [
        appdata / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState" / "settings.json",
        appdata / "Microsoft" / "WindowsTerminal" / "settings.json",
    ]

    target_path = None
    for p in wt_paths:
        if p.exists():
            target_path = p
            break

    if not target_path:
        print("[ERROR] Could not locate settings.json.")
        return

    print(f"Aggressively Chopping Settings: {target_path}")
    raw_content = target_path.read_text(encoding="utf-8", errors="replace")
    clean_json = strip_json_comments(raw_content)
    
    try:
        data = json.loads(clean_json)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        return

    profiles = data.get("profiles", {}).get("list", [])
    default_guid = data.get("defaultProfile")
    
    # Exclude patterns for legacy/orphaned profiles
    exclude_patterns = [
        r'VS 2019',
        r'VS 18',
        r'ubu26_0715',
        r'aomaker',
        r'Azure Cloud Shell',
        r'Ubu24\.04\.1',
        r'Ubuntu-24\.04',
        r'Ubuntu-26\.04-Sandbox',
    ]

    chopped_list = []
    purged_records = []

    for prof in profiles:
        p_name = prof.get("name", "Unnamed")
        p_guid = prof.get("guid")
        is_hidden = prof.get("hidden", False)
        
        # Rule 1: Always keep default profile
        if p_guid and p_guid == default_guid:
            prof["hidden"] = False  # Ensure default profile is visible
            chopped_list.append(prof)
            continue

        # Rule 2: Purge anything marked hidden
        if is_hidden:
            purged_records.append(f"{p_name} (Reason: Hidden profile)")
            continue

        # Rule 3: Purge legacy matching patterns
        should_purge = any(re.search(pat, p_name, re.IGNORECASE) for pat in exclude_patterns)
        if should_purge:
            purged_records.append(f"{p_name} (Reason: Legacy pattern match)")
            continue

        chopped_list.append(prof)

    data["profiles"]["list"] = chopped_list

    # Save formatted JSON back
    target_path.write_text(json.dumps(data, indent=4), encoding="utf-8")

    print(f"\n[SUCCESS] Purged {len(purged_records)} profiles from settings.json!")
    print("--------------------------------------------------------------------------------")
    for rec in purged_records:
        print(f"   - CHOPPED: {rec}")
    print("--------------------------------------------------------------------------------")
    print(f" Active Clean Profiles Remaining: {len(chopped_list)}")

if __name__ == "__main__":
    chop_settings()

"""
================================================================================
FILENAME END: gemini/tools/chop_terminal_settings.py
================================================================================
"""
