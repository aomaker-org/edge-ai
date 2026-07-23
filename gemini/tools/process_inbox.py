#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/process_inbox.py
================================================================================
Utility: Provenance-Aware Inbox Payload Router & Auto-Dissector
Description: Parses gemini/inbox.file for guarded payload blocks, creates 
             provenance-stamped safety backups in gemini/backups/ before 
             modifying existing files, enforces idempotency, and syncs .md <-> .txt.
================================================================================
"""

import re
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GEMINI_DIR = REPO_ROOT / "gemini"
INBOX_FILE = GEMINI_DIR / "inbox.file"
BACKUP_DIR = GEMINI_DIR / "backups"

UNICODE_MAP = {
    "├": "|", "─": "-", "└": "`", "│": "|", "┬": "-", "┴": "-", "┼": "+",
    "“": '"', "”": '"', "‘": "'", "’": "'", "…": "...", "•": "*", "—": "--"
}

def sanitize_ascii(text: str) -> str:
    """Strips non-ASCII characters and normalizes Unicode symbols."""
    for char, replacement in UNICODE_MAP.items():
        text = text.replace(char, replacement)
    return text.encode("ascii", "ignore").decode("ascii")

def create_safety_backup(target_path: Path, actor: str = "fekerr + gemini / agy"):
    """Creates a timestamped backup with explicit path and actor provenance headers."""
    if not target_path.exists():
        return None

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    file_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    rel_path_str = str(target_path.relative_to(REPO_ROOT))
    
    # Sanitize path separators for flat backup file naming to prevent collisions
    safe_backup_filename = f"{file_ts}_{rel_path_str.replace('/', '_')}.bak"
    backup_path = BACKUP_DIR / safe_backup_filename

    # Read existing original content
    raw_content = target_path.read_text(encoding="utf-8", errors="ignore")

    # Build Provenance Header
    prov_header = (
        f"================================================================================\n"
        f"BACKUP PROVENANCE METADATA\n"
        f"================================================================================\n"
        f"ORIGINAL FILENAME : {rel_path_str}\n"
        f"BACKUP TIMESTAMP  : {timestamp_str}\n"
        f"MODIFIED BY       : {actor}\n"
        f"================================================================================\n\n"
    )

    full_backup_payload = prov_header + raw_content
    backup_path.write_text(full_backup_payload, encoding="utf-8")
    return backup_path

def process_inbox():
    if not INBOX_FILE.exists() or INBOX_FILE.stat().st_size == 0:
        print(f"[Inbox Processor] Inbox is empty or missing: {INBOX_FILE}")
        return

    content = INBOX_FILE.read_text(encoding="utf-8", errors="ignore")
    
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
        print("  Expected signature: FILENAME BEGIN: <path> ... FILENAME END: <path>")
        return

    print(f"[Inbox Processor] Discovered {len(matches)} file payload(s) in inbox...\n")

    for match in matches:
        rel_path_str = match.group("rel_path").strip()
        body = match.group("body")

        target_path = (REPO_ROOT / rel_path_str).resolve()

        if not str(target_path).startswith(str(REPO_ROOT)):
            print(f"  [SECURITY REJECTED] Path lies outside repo root: {rel_path_str}")
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        clean_body = sanitize_ascii(body).strip()
        
        header = f"================================================================================\n" \
                 f"FILENAME BEGIN: {rel_path_str}\n" \
                 f"================================================================================\n\n"
        footer = f"\n\n================================================================================\n" \
                 f"FILENAME END: {rel_path_str}\n" \
                 f"================================================================================\n"

        guarded_payload = header + clean_body + footer

        # Idempotency Check: Skip if exact payload is already present on disk
        if target_path.exists():
            existing_content = target_path.read_text(encoding="ascii", errors="ignore")
            if existing_content == guarded_payload:
                print(f"  [SKIPPED (IDEMPOTENT)] {rel_path_str} is already up to date.")
                continue

            # Provenance Protection: Backup existing file with path & actor metadata
            backup_file = create_safety_backup(target_path)
            if backup_file:
                print(f"  [BACKUP CREATED] {backup_file.relative_to(REPO_ROOT)}")

        # Write primary file
        target_path.write_text(guarded_payload, encoding="ascii")
        print(f"  -> Dispatched: {target_path.relative_to(REPO_ROOT)}")

        # Sync Mirrored Twin (.md <-> .txt)
        if target_path.suffix == ".md":
            twin_path = target_path.with_suffix(".txt")
            if twin_path.exists() and twin_path != target_path:
                create_safety_backup(twin_path)
            twin_path.write_text(guarded_payload, encoding="ascii")
            print(f"     Mirrored : {twin_path.relative_to(REPO_ROOT)}")
        elif target_path.suffix == ".txt":
            twin_path = target_path.with_suffix(".md")
            if twin_path.exists() and twin_path != target_path:
                create_safety_backup(twin_path)
            twin_path.write_text(guarded_payload, encoding="ascii")
            print(f"     Mirrored : {twin_path.relative_to(REPO_ROOT)}")

    INBOX_FILE.write_text("", encoding="utf-8")
    print(f"\n[Inbox Processor] Processing complete. Cleared {INBOX_FILE.name}")

if __name__ == "__main__":
    process_inbox()

"""
================================================================================
FILENAME END: gemini/tools/process_inbox.py
================================================================================
"""
