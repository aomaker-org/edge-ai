#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/inbox_watcher.py
================================================================================
Utility: Safe Auto-Inbox Directory Watcher
Description: Monitors ./gemini/ for incoming files. Filters out code scripts (.py,
             .sh) and verifies the presence of 'FILENAME BEGIN:' magic signature
             before triggering the non-destructive inbox processor.
================================================================================
"""

import time
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GEMINI_DIR = REPO_ROOT / "gemini"
TARGET_INBOX = GEMINI_DIR / "inbox.file"
PROCESSOR_SCRIPT = GEMINI_DIR / "tools" / "process_inbox.py"

# Extensions allowed to act as inbox payloads
ALLOWED_EXTENSIONS = {".file", ".txt", ".md", ".raw", ""}
PAYLOAD_MAGIC_BYTES = "FILENAME BEGIN:"

def is_valid_inbox_payload(file_path: Path) -> bool:
    """Validates extension and peeks inside for the payload magic signature."""
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False

    try:
        # Peek at the first 1000 characters
        header_sample = file_path.read_text(encoding="utf-8", errors="ignore")[:1000]
        return PAYLOAD_MAGIC_BYTES in header_sample
    except Exception:
        return False

def scan_and_process():
    """Scans ./gemini/ for valid incoming inbox payloads."""
    for item in GEMINI_DIR.iterdir():
        if item.is_file() and item.name.lower().startswith("inbox"):
            if item.stat().st_size > 0 and is_valid_inbox_payload(item):
                print(f"[Inbox Watcher] Valid payload detected: {item.name}")
                
                if item != TARGET_INBOX:
                    item.rename(TARGET_INBOX)
                
                subprocess.run(["python3", str(PROCESSOR_SCRIPT)], check=False)
                return True
    return False

def start_watcher(poll_interval=2.0):
    print("================================================================================")
    print(" SAFE AUTO-INBOX WATCHER ACTIVE")
    print(f" Monitoring Directory : {GEMINI_DIR}")
    print(f" Target Signature     : '{PAYLOAD_MAGIC_BYTES}'")
    print(" Press Ctrl+C to stop.")
    print("================================================================================")
    
    try:
        while True:
            scan_and_process()
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\n[Inbox Watcher] Stopped.")

if __name__ == "__main__":
    start_watcher()

"""
================================================================================
FILENAME END: gemini/tools/inbox_watcher.py
================================================================================
"""
