#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/sync_session.py
================================================================================
Utility: Gemini Session Environment Sync & Verification Tool
Description: Audits the ./gemini directory infrastructure, verifies tool 
             permissions, checks inbox status, writes to an incrementing log, 
             and loads the summary into the Windows clipboard.
================================================================================
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GEMINI_DIR = REPO_ROOT / "gemini"
TOOLS_DIR = GEMINI_DIR / "tools"
CAPTURES_DIR = GEMINI_DIR / "captures"

REQUIRED_TOOLS = [
    "audit_scaffold.sh",
    "build_runner.py",
    "mod_toggle.py",
    "process_inbox.py",
    "clip_logger.py",
    "sync_session.py"
]

def load_windows_clipboard(text_payload):
    """Pipes UTF-8 text to Windows clip.exe using UTF-16LE encoding."""
    try:
        utf16_bytes = text_payload.encode("utf-16le")
        proc = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE)
        proc.communicate(input=utf16_bytes)
        return proc.returncode == 0
    except Exception:
        return False

def audit_gemini_env():
    output_lines = []
    
    def log(msg):
        print(msg)
        output_lines.append(msg)

    log("================================================================================")
    log(" EDGE-AI GEMINI INFRASTRUCTURE SYNC AUDIT")
    log("================================================================================")
    log(f" Repository Root : {REPO_ROOT}")
    log(f" Gemini Directory: {GEMINI_DIR}\n")

    # 1. Check Tools and Permissions
    log("[1] Checking Tool Suite Permissions:")
    for tool_name in REQUIRED_TOOLS:
        tool_path = TOOLS_DIR / tool_name
        if not tool_path.exists():
            log(f"  - [MISSING]     {tool_name}")
        else:
            is_exec = os.access(tool_path, os.X_OK)
            status = "OK (Executable)" if is_exec else "WARNING (Not Executable)"
            log(f"  - [{status}] {tool_name}")

    # 2. Check Inbox Status
    inbox_file = GEMINI_DIR / "inbox.file"
    log("\n[2] Checking Inbox Status:")
    if inbox_file.exists():
        size = inbox_file.stat().st_size
        log(f"  - gemini/inbox.file present ({size} bytes).")
    else:
        log("  - [NOTICE] gemini/inbox.file missing. Creating empty inbox...")
        inbox_file.write_text("", encoding="utf-8")

    # 3. Check Session Notes
    log("\n[3] Session Notes Inventory:")
    notes = sorted(GEMINI_DIR.glob("session_notes_*.txt"))
    if notes:
        for note in notes:
            log(f"  - Found: {note.name}")
    else:
        log("  - No session_notes_*.txt files found.")

    log("\n================================================================================")
    log(" Sync audit complete! System ready.")
    log("================================================================================")

    # 4. Save to Captures Log & Load Clipboard
    full_text = "\n".join(output_lines)
    CAPTURES_DIR.mkdir(parents=True, exist_ok=True)
    
    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    existing = list(CAPTURES_DIR.glob(f"{now_str}_*_audit.txt"))
    seq_num = len(existing) + 1
    
    log_file = CAPTURES_DIR / f"{now_str}_{seq_num:03d}_audit.txt"
    log_file.write_text(full_text, encoding="utf-8")
    
    clip_ok = load_windows_clipboard(full_text)
    
    print("\n--------------------------------------------------------------------------------")
    print(f" Saved Audit Log  : {log_file}")
    print(f" Clipboard Status : {'LOADED (Ctrl+V Ready)' if clip_ok else 'FAILED'}")
    print("--------------------------------------------------------------------------------")
    print(" TRIPLE-CLICK COMMAND LINES:")
    print("--------------------------------------------------------------------------------")
    print(f"cat {log_file}")
    print(f"cat {log_file} > {GEMINI_DIR}/inbox.file")
    print(f"{GEMINI_DIR}/inbox.sh")
    print("================================================================================\n")

if __name__ == "__main__":
    audit_gemini_env()
