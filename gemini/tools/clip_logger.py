#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/clip_logger.py
================================================================================
Utility: Incrementing Clip Logger & Triple-Click Console Generator
Description: Saves input payloads to incrementing log files in gemini/captures/,
             loads the Windows clipboard via UTF-16LE clip.exe interop, and 
             prints clean, triple-clickable terminal commands.
================================================================================
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CAPTURES_DIR = REPO_ROOT / "gemini" / "captures"
MAX_COLUMNS = 120

def get_next_sequence_filepath():
    """Generates an incrementing log file path: YYYYMMDD_HHMM_seq_clip.txt"""
    CAPTURES_DIR.mkdir(parents=True, exist_ok=True)
    now_str = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Find existing captures matching today's pattern to calculate next sequence number
    existing = list(CAPTURES_DIR.glob(f"{now_str}_*_clip.txt"))
    seq_num = len(existing) + 1
    
    filename = f"{now_str}_{seq_num:03d}_clip.txt"
    return CAPTURES_DIR / filename

def load_windows_clipboard(text_payload):
    """Pipes UTF-8 text cleanly to clip.exe using UTF-16LE encoding to avoid mangling."""
    try:
        # Encode to UTF-16LE as expected by Windows clip.exe
        utf16_bytes = text_payload.encode("utf-16le")
        proc = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE)
        proc.communicate(input=utf16_bytes)
        return proc.returncode == 0
    except Exception as e:
        print(f"Notice: Clipboard pipe failed ({e})")
        return False

def main():
    if len(sys.argv) > 1:
        # Read from input file argument
        input_path = Path(sys.argv[1])
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' not found.")
            sys.exit(1)
        payload = input_path.read_text(encoding="utf-8", errors="ignore")
    else:
        # Read from standard input (pipe)
        payload = sys.stdin.read()

    if not payload.strip():
        print("Error: Input payload is empty.")
        sys.exit(1)

    # 1. Save to incrementing log file
    log_file = get_next_sequence_filepath()
    log_file.write_text(payload, encoding="utf-8")

    # 2. Load to Windows Clipboard
    clip_success = load_windows_clipboard(payload)

    # 3. Print Triple-Clickable Terminal Summary
    rel_log = log_file.relative_to(REPO_ROOT)
    
    print("\n" + "=" * MAX_COLUMNS)
    print(" CLIPBOARD & LOG CAPTURE COMPLETE")
    print("=" * MAX_COLUMNS)
    print(f" Log File Saved : {log_file}")
    print(f" Bytes Written  : {len(payload)} bytes")
    print(f" Clipboard Status: {'LOADED (Ctrl+V Ready)' if clip_success else 'FAILED'}")
    print("-" * MAX_COLUMNS)
    print(" TRIPLE-CLICK COMMAND LINES:")
    print("-" * MAX_COLUMNS)
    print(f"cat {log_file}")
    print(f"cat {log_file} > {REPO_ROOT}/gemini/inbox.file")
    print(f"{REPO_ROOT}/gemini/inbox.sh")
    print("=" * MAX_COLUMNS + "\n")

if __name__ == "__main__":
    main()

"""
================================================================================
FILENAME END: gemini/tools/clip_logger.py
================================================================================
"""
