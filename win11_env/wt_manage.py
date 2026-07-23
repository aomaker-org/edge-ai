#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: fekerr-dev/win11_env/wt_manage.py
================================================================================
Utility: Windows Terminal Git Sync & Lifecycle Manager
Description: Manages bidirectional sync, diffing, extraction (extall), and
             installation (push) between Windows AppData and fekerr-dev repo.
================================================================================
"""

import os
import sys
import json
import difflib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_JSON_PATH = SCRIPT_DIR / "settings.json"
BACKUP_DIR = SCRIPT_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

def get_live_wt_path() -> Path:
    """Locates active Windows Terminal settings.json in AppData."""
    try:
        raw_user = subprocess.check_output(
            ["cmd.exe", "/c", "echo %USERPROFILE%"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        win_user = Path(subprocess.check_output(
            ["wslpath", "-u", raw_user],
            text=True, stderr=subprocess.DEVNULL
        ).strip())
    except Exception:
        print("[ERROR] Could not resolve Windows %USERPROFILE%.")
        sys.exit(1)

    appdata = win_user / "AppData" / "Local"
    candidates = [
        appdata / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState" / "settings.json",
        appdata / "Microsoft" / "WindowsTerminal" / "settings.json",
    ]

    for c in candidates:
        if c.exists():
            return c
    return None

def strip_comments_and_format(text: str) -> str:
    """Standardizes JSON formatting for clean diffs."""
    lines = []
    for line in text.splitlines():
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
    clean_str = "\n".join(lines)
    try:
        parsed = json.loads(clean_str)
        return json.dumps(parsed, indent=4) + "\n"
    except Exception:
        return text

def cmd_status(live_path: Path):
    print("================================================================================")
    print(" WINDOWS TERMINAL CONFIGURATION STATUS")
    print("================================================================================")
    print(f" Live AppData Path : {live_path}")
    print(f" Repo Git Path     : {REPO_JSON_PATH}")
    print("--------------------------------------------------------------------------------")

    if not REPO_JSON_PATH.exists():
        print(" Status : [MISSING IN REPO] Run './wt_manage.py pull' to extract live config.")
        return

    live_text = strip_comments_and_format(live_path.read_text(encoding="utf-8", errors="replace"))
    repo_text = strip_comments_and_format(REPO_JSON_PATH.read_text(encoding="utf-8", errors="replace"))

    if live_text == repo_text:
        print(" Status : [IN SYNC] Live Windows Terminal matches fekerr-dev Git version 100%.")
    else:
        print(" Status : [DRIFT DETECTED] Live AppData config differs from fekerr-dev Git version.")
        print("          Run './wt_manage.py diff' to view changes.")

def cmd_diff(live_path: Path):
    if not REPO_JSON_PATH.exists():
        print("[ERROR] Repo file missing. Run './wt_manage.py pull' first.")
        return

    live_lines = strip_comments_and_format(live_path.read_text(encoding="utf-8", errors="replace")).splitlines(keepends=True)
    repo_lines = strip_comments_and_format(REPO_JSON_PATH.read_text(encoding="utf-8", errors="replace")).splitlines(keepends=True)

    diff = list(difflib.unified_diff(
        repo_lines, live_lines,
        fromfile="fekerr-dev/win11_env/settings.json (Repo)",
        tofile="Windows Terminal AppData (Live)",
        n=3
    ))

    if not diff:
        print("[IN SYNC] No differences found between Repo and Live AppData config.")
    else:
        print("".join(diff))

def cmd_pull(live_path: Path):
    """Extracts live AppData config into repo (extall)."""
    formatted_content = strip_comments_and_format(live_path.read_text(encoding="utf-8", errors="replace"))
    REPO_JSON_PATH.write_text(formatted_content, encoding="utf-8")
    print("================================================================================")
    print(f"[SUCCESS] Extracted live config -> {REPO_JSON_PATH}")
    print("================================================================================")

def cmd_push(live_path: Path):
    """Deploys repo config to Windows AppData (install)."""
    if not REPO_JSON_PATH.exists():
        print("[ERROR] Repo file missing. Cannot deploy to AppData.")
        return

    # Safety backup of live file
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    bak_path = BACKUP_DIR / f"{now}_settings.json.bak"
    bak_path.write_text(live_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    print(f"[BACKUP] Saved live AppData config -> {bak_path}")

    # Copy repo JSON to live AppData location
    repo_content = REPO_JSON_PATH.read_text(encoding="utf-8")
    live_path.write_text(repo_content, encoding="utf-8")
    print("================================================================================")
    print(f"[SUCCESS] Deployed {REPO_JSON_PATH} -> Windows Terminal AppData!")
    print("================================================================================")

def main():
    verb = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    live_path = get_live_wt_path()

    if not live_path:
        print("[ERROR] Could not locate active Windows Terminal settings.json in AppData.")
        sys.exit(1)

    if verb in ("status", "st"):
        cmd_status(live_path)
    elif verb in ("diff", "df"):
        cmd_diff(live_path)
    elif verb in ("pull", "extall", "extract"):
        cmd_pull(live_path)
    elif verb in ("push", "install", "deploy"):
        cmd_push(live_path)
    else:
        print(f"Unknown verb '{verb}'. Valid verbs: status | diff | pull (extall) | push (install)")

if __name__ == "__main__":
    main()

"""
================================================================================
FILENAME END: fekerr-dev/win11_env/wt_manage.py
================================================================================
"""
