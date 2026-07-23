#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/audit_windows_config.py
================================================================================
Utility: Windows Terminal & PowerShell 7 Profile Auditor & Sanitizer
Description: Locates Windows Terminal settings.json and PS7 $PROFILE via WSL,
             makes safety backups in gemini/backups/, and extracts hidden
             aliases, functions, env vars, and orphaned profiles.
================================================================================
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKUPS_DIR = REPO_ROOT / "gemini" / "backups"
BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

def strip_json_comments(json_str: str) -> str:
    """Strips // and /* */ comments from JSON (Windows Terminal allows JSONC)."""
    pattern = r'(//.*?$)|(/\*.*?\*/)'
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
    
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
    """Gets Windows %USERPROFILE% as a Linux Path."""
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

def audit_powershell_profile(win_user: Path):
    print("================================================================================")
    print(" 1. POWERSHELL 7 PROFILE AUDIT ($PROFILE)")
    print("================================================================================")
    
    ps_profile_paths = [
        win_user / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1",
        win_user / "OneDrive" / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1",
    ]

    profile_path = None
    for p in ps_profile_paths:
        if p.exists():
            profile_path = p
            break

    if not profile_path:
        print(" [NOTICE] No active PowerShell $PROFILE found at standard path.")
        return

    print(f" Profile Location : {profile_path}")

    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    bak_path = BACKUPS_DIR / f"{now}_PowerShell_profile.ps1.bak"
    content = profile_path.read_text(encoding="utf-8", errors="replace")
    
    prov_content = f"# PROVENANCE BACKUP\n# Source: {profile_path}\n# Date: {now}\n" + content
    bak_path.write_text(prov_content, encoding="utf-8")
    print(f" Backup Created   : {bak_path}")

    aliases = re.findall(r'Set-Alias\s+[\'"]?(\w+)[\'"]?\s+[\'"]?([^\r\n#]+)[\'"]?', content, re.IGNORECASE)
    functions = re.findall(r'function\s+([\w\-:]+)', content, re.IGNORECASE)
    env_vars = re.findall(r'\$env:([\w_]+)\s*=', content, re.IGNORECASE)
    prompt_mods = re.findall(r'(oh-my-posh|starship|Terminal-Icons|posh-git)', content, re.IGNORECASE)

    print("--------------------------------------------------------------------------------")
    print(f" Line Count        : {len(content.splitlines()):,}")
    print(f" Defined Functions : {len(functions)} {functions[:5] if functions else ''}")
    print(f" Defined Aliases   : {len(aliases)} {aliases[:5] if aliases else ''}")
    print(f" Env Injections    : {len(env_vars)} {env_vars[:5] if env_vars else ''}")
    print(f" Prompt Modules    : {list(set(prompt_mods)) if prompt_mods else 'None (Clean)'}")
    print("================================================================================\n")

def audit_windows_terminal(win_user: Path):
    print("================================================================================")
    print(" 2. WINDOWS TERMINAL CONFIGURATION AUDIT (settings.json)")
    print("================================================================================")

    appdata = win_user / "AppData" / "Local"
    wt_paths = [
        appdata / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState" / "settings.json",
        appdata / "Microsoft" / "WindowsTerminal" / "settings.json",
    ]

    wt_settings_path = None
    for p in wt_paths:
        if p.exists():
            wt_settings_path = p
            break

    if not wt_settings_path:
        print(" [NOTICE] Could not locate Windows Terminal settings.json.")
        return

    print(f" Settings Location: {wt_settings_path}")

    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    bak_path = BACKUPS_DIR / f"{now}_settings.json.bak"
    raw_content = wt_settings_path.read_text(encoding="utf-8", errors="replace")
    
    bak_path.write_text(raw_content, encoding="utf-8")
    print(f" Backup Created   : {bak_path}")

    try:
        clean_json = strip_json_comments(raw_content)
        data = json.loads(clean_json)
        
        profiles = data.get("profiles", {}).get("list", [])
        schemes = data.get("schemes", [])
        default_profile_guid = data.get("defaultProfile", "None")

        print("--------------------------------------------------------------------------------")
        print(f" Default Profile GUID: {default_profile_guid}")
        print(f" Total Profiles      : {len(profiles)}")
        for prof in profiles:
            p_name = prof.get("name", "Unnamed")
            p_guid = prof.get("guid", prof.get("name", ""))
            p_cmd = prof.get("commandline", "Default Shell")
            p_dir = prof.get("startingDirectory", "Default")
            is_default = " [DEFAULT]" if p_guid == default_profile_guid else ""
            print(f"   - {p_name:<20}{is_default} | Cmd: {p_cmd} | Dir: {p_dir}")

        print(f" Color Schemes       : {len(schemes)} defined schemes")
    except Exception as e:
        print(f" [WARN] Failed to parse JSONC structure: {e}")

    print("================================================================================\n")

def main():
    win_user = get_win_userprofile()
    if not win_user:
        print("[ERROR] Could not resolve Windows %USERPROFILE% from WSL.")
        sys.exit(1)

    print(f"Resolved Windows UserProfile: {win_user}")
    audit_powershell_profile(win_user)
    audit_windows_terminal(win_user)

if __name__ == "__main__":
    main()
