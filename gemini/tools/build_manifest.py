#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/build_manifest.py
================================================================================
Utility: Root manifest.json Generator & Rclone Asset Tracker
Description: Scans edge-ai workspace, cross-references Git state (tracked vs. 
             ignored), calculates SHA-256 hashes, and flags heavy assets and 
             ignored logs as candidates for Rclone cloud sync.
================================================================================
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "manifest.json"
GEMINI_DIR = REPO_ROOT / "gemini"
CAPTURES_DIR = GEMINI_DIR / "captures"

IGNORE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "target", "build", ".pytest_cache"}
LARGE_FILE_THRESHOLD_BYTES = 10 * 1024 * 1024  # 10 MB

def load_windows_clipboard(text_payload: str) -> bool:
    """Pipes UTF-8 text to Windows clip.exe using UTF-16LE encoding."""
    try:
        utf16_bytes = text_payload.encode("utf-16le")
        proc = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE)
        proc.communicate(input=utf16_bytes)
        return proc.returncode == 0
    except Exception:
        return False

def get_git_ignored_set():
    """Runs git status --ignored --porcelain to find all ignored/untracked paths."""
    ignored_paths = set()
    try:
        res = subprocess.run(
            ["git", "status", "--ignored", "--porcelain"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True
        )
        for line in res.stdout.splitlines():
            if line.startswith("!!") or line.startswith("??"):
                rel_path = line[3:].strip().rstrip("/")
                ignored_paths.add(rel_path)
    except Exception:
        pass
    return ignored_paths

def is_git_ignored(file_path: Path) -> bool:
    """Checks if a specific file path is ignored by git."""
    try:
        res = subprocess.run(
            ["git", "check-ignore", "-q", str(file_path)],
            cwd=REPO_ROOT
        )
        return res.returncode == 0
    except Exception:
        return False

def calculate_sha256(file_path: Path, max_bytes_to_hash: int = 100 * 1024 * 1024) -> str:
    """Calculates SHA-256 for files up to 100MB."""
    stat = file_path.stat()
    if stat.st_size > max_bytes_to_hash:
        return "SKIPPED_TOO_LARGE"

    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return "HASH_ERROR"

def build_manifest():
    print("================================================================================")
    print(" GENERATING ROOT MANIFEST.JSON FOR EDGE-AI")
    print(f" Root Directory : {REPO_ROOT}")
    print("================================================================================")

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    files_manifest = {}
    rclone_candidates_count = 0
    total_bytes = 0

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file_name in files:
            file_path = Path(root) / file_name
            rel_path = str(file_path.relative_to(REPO_ROOT))
            
            # Skip manifest.json itself
            if rel_path == "manifest.json":
                continue

            stat = file_path.stat()
            size_bytes = stat.st_size
            total_bytes += size_bytes
            mtime_utc = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

            git_ignored = is_git_ignored(file_path)
            
            # Identify Rclone Cloud Sync Candidates
            is_rclone_candidate = False
            category = "source"

            if rel_path.startswith("logs/"):
                is_rclone_candidate = True
                category = "build_telemetry"
            elif rel_path.startswith("gemini/captures/"):
                is_rclone_candidate = True
                category = "capture_archive"
            elif rel_path.startswith("gemini/backups/"):
                is_rclone_candidate = True
                category = "provenance_backup"
            elif size_bytes >= LARGE_FILE_THRESHOLD_BYTES:
                is_rclone_candidate = True
                category = "large_blob"
            elif git_ignored:
                is_rclone_candidate = True
                category = "ignored_asset"

            if is_rclone_candidate:
                rclone_candidates_count += 1

            files_manifest[rel_path] = {
                "size_bytes": size_bytes,
                "sha256": calculate_sha256(file_path),
                "modified_utc": mtime_utc,
                "git_status": "ignored" if git_ignored else "tracked",
                "rclone_candidate": is_rclone_candidate,
                "category": category
            }

    root_payload = {
        "metadata": {
            "generated_utc": now_utc,
            "repo_name": "edge-ai",
            "repo_root": str(REPO_ROOT),
            "total_files": len(files_manifest),
            "total_bytes": total_bytes,
            "rclone_candidates_count": rclone_candidates_count,
            "schema_version": "1.0.0"
        },
        "files": files_manifest
    }

    # Write root manifest.json
    MANIFEST_PATH.write_text(json.dumps(root_payload, indent=2), encoding="utf-8")

    summary_lines = [
        "================================================================================",
        " ROOT MANIFEST.JSON GENERATED SUCCESSFULLY",
        "================================================================================",
        f" Output Location     : {MANIFEST_PATH}",
        f" Total Files Ingested: {len(files_manifest):,}",
        f" Total Workspace Size: {total_bytes / (1024*1024):.2f} MB",
        f" Rclone Sync Targets : {rclone_candidates_count:,} candidate files",
        "--------------------------------------------------------------------------------",
        " TRIPLE-CLICK COMMAND LINES:",
        "--------------------------------------------------------------------------------",
        f"cat {MANIFEST_PATH} | head -n 30",
        f"jq '.metadata' {MANIFEST_PATH}",
        f"jq '.files[] | select(.rclone_candidate == true)' {MANIFEST_PATH} | head -n 30",
        "================================================================================\n"
    ]

    summary_text = "\n".join(summary_lines)
    print(summary_text)

    load_windows_clipboard(summary_text)

if __name__ == "__main__":
    build_manifest()

"""
================================================================================
FILENAME END: gemini/tools/build_manifest.py
================================================================================
"""
