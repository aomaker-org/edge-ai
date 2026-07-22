#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/process_inbox.py
================================================================================
Utility: Inbox Payload Router & Auto-Dissector
Description: Parses gemini/inbox.file for guarded payload blocks, routes each
             payload to its designated file path, creates target folders, and
             triggers dual .md <-> .txt twin generation.
================================================================================
"""

import re
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INBOX_FILE = REPO_ROOT / "gemini" / "inbox.file"
MAX_COLUMNS = 120

UNICODE_MAP = {
    "├": "|", "─": "-", "└": "`", "│": "|", "┬": "-", "┴": "-", "┼": "+",
    "“": '"', "”": '"', "‘": "'", "’": "'", "…": "...", "•": "*", "—": "--"
}

def sanitize_ascii(text: str) -> str:
    """Strips non-ASCII characters and normalizes Unicode symbols."""
    for char, replacement in UNICODE_MAP.items():
        text = text.replace(char, replacement)
    return text.encode("ascii", "ignore").decode("ascii")

def process_inbox():
    if not INBOX_FILE.exists() or INBOX_FILE.stat().st_size == 0:
        print(f"[Inbox Processor] Inbox is empty or missing: {INBOX_FILE}")
        return

    content = INBOX_FILE.read_text(encoding="utf-8", errors="ignore")
    
    # Regex pattern to extract FILENAME BEGIN / END blocks
    pattern = re.compile(
        r"================================================================================\s*"
        r"FILENAME BEGIN:\s*(?P<rel_path>[^\n]+)\s*"
        r"================================================================================\s*"
        r"(?P<body>.*?)\s*"
        r"================================================================================\s*"
        r"FILENAME END:\s*(?P=rel_path)\s*"
        r"================================================================================",
        re.DOTALL
    )

    matches = list(pattern.finditer(content))

    if not matches:
        print("[Inbox Processor] No valid guarded file payloads found in inbox.file.")
        print("  Expected format:\n  FILENAME BEGIN: path/to/file\n  ... content ...\n  FILENAME END: path/to/file")
        return

    print(f"[Inbox Processor] Discovered {len(matches)} file payload(s) in inbox...\n")

    for match in matches:
        rel_path_str = match.group("rel_path").strip()
        body = match.group("body")

        # Resolve target path relative to REPO_ROOT
        target_path = (REPO_ROOT / rel_path_str).resolve()

        # Security check: Prevent path traversal outside repository
        if not str(target_path).startswith(str(REPO_ROOT)):
            print(f"  [SECURITY REJECTED] Path lies outside repo root: {rel_path_str}")
            continue

        # Enforce directory creation
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Sanitize and format content
        clean_body = sanitize_ascii(body).strip()
        
        header = f"================================================================================\n" \
                 f"FILENAME BEGIN: {rel_path_str}\n" \
                 f"================================================================================\n\n"
        footer = f"\n\n================================================================================\n" \
                 f"FILENAME END: {rel_path_str}\n" \
                 f"================================================================================\n"

        guarded_payload = header + clean_body + footer

        # Write primary file
        target_path.write_text(guarded_payload, encoding="ascii")
        print(f"  -> Dispatched: {target_path.relative_to(REPO_ROOT)}")

        # Create/Sync Mirrored Twin (.md <-> .txt)
        if target_path.suffix == ".md":
            twin_path = target_path.with_suffix(".txt")
            twin_path.write_text(guarded_payload, encoding="ascii")
            print(f"     Mirrored : {twin_path.relative_to(REPO_ROOT)}")
        elif target_path.suffix == ".txt":
            twin_path = target_path.with_suffix(".md")
            twin_path.write_text(guarded_payload, encoding="ascii")
            print(f"     Mirrored : {twin_path.relative_to(REPO_ROOT)}")

    # Clear inbox after successful routing
    INBOX_FILE.write_text("", encoding="utf-8")
    print(f"\n[Inbox Processor] Processing complete. Cleared {INBOX_FILE.name}")

if __name__ == "__main__":
    process_inbox()
