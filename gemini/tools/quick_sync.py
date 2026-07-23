#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/quick_sync.py
================================================================================
Utility: Multi-Repo Workspace Tree Traverser & Live Progress Logger
Description: Scans edge-ai, irislime, and fekerr-dev repositories with live 5s
             heartbeats (tailable via gemini/progress.log), timezone-aware 
             UTC timestamps, header extraction, and archive size optimization.
================================================================================
"""

import os
import sys
import time
import hashlib
import zipfile
import tarfile
import subprocess
from pathlib import Path
from datetime import datetime, timezone

HOME_SRC = Path.home() / "src"
TARGET_REPOS = ["edge-ai", "irislime", "fekerr-dev"]

PRIMARY_REPO = HOME_SRC / "edge-ai"
GEMINI_DIR = PRIMARY_REPO / "gemini"
CAPTURES_DIR = GEMINI_DIR / "captures"
PROGRESS_LOG = GEMINI_DIR / "progress.log"

IGNORE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "target", "build", ".pytest_cache", "backups", "captures"}
IGNORE_EXTS = {".png", ".jpg", ".jpeg", ".pyc", ".tar.gz", ".zip"}

def load_windows_clipboard(text_payload: str) -> bool:
    """Pipes UTF-8 text to Windows clip.exe using UTF-16LE encoding."""
    try:
        utf16_bytes = text_payload.encode("utf-16le")
        proc = subprocess.Popen(["clip.exe"], stdin=subprocess.PIPE)
        proc.communicate(input=utf16_bytes)
        return proc.returncode == 0
    except Exception:
        return False

def log_progress(msg: str, echo_console: bool = True):
    """Logs timestamped entries to gemini/progress.log and flushes stdout."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{now_utc}] {msg}"
    
    GEMINI_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        
    if echo_console:
        print(line, flush=True)

def get_file_info(file_path: Path, max_head_lines: int = 10):
    """Calculates SHA-256 hash, reads stats, and extracts top header lines."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()[:12]
    except Exception:
        return None

    stat = file_path.stat()
    size_bytes = stat.st_size
    mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    head_lines = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(max_head_lines):
                line = f.readline()
                if not line:
                    break
                head_lines.append(line.rstrip("\r\n"))
    except Exception:
        head_lines = ["<binary or unreadable content>"]

    rel_to_src = str(file_path.relative_to(HOME_SRC))
    return {
        "rel_path": rel_to_src,
        "abs_path": file_path,
        "hash": file_hash,
        "size": size_bytes,
        "mtime": mtime,
        "head": head_lines
    }

def scan_multi_repo():
    """Recursively scans target repos emitting 5-second progress heartbeats."""
    all_records = []
    last_heartbeat = time.time()
    total_bytes = 0

    log_progress("Starting workspace scan across repositories...")

    for repo_name in TARGET_REPOS:
        repo_path = HOME_SRC / repo_name
        if not repo_path.exists():
            log_progress(f"Notice: Repo directory '{repo_name}' not found, skipping.")
            continue

        log_progress(f"Scanning repository tree: {repo_name}...")

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in IGNORE_EXTS:
                    continue
                
                info = get_file_info(file_path)
                if info:
                    all_records.append(info)
                    total_bytes += info["size"]

                # Heartbeat every 5 seconds
                if time.time() - last_heartbeat >= 5.0:
                    log_progress(f"Progress Heartbeat: Scanned {len(all_records)} files ({total_bytes / (1024*1024):.2f} MB processed)...")
                    last_heartbeat = time.time()

    log_progress(f"Scan Complete: Found {len(all_records)} files ({total_bytes / (1024*1024):.2f} MB total).")
    return sorted(all_records, key=lambda x: x["rel_path"])

def create_archives(file_records, base_name_no_ext: Path):
    """Builds both .tar.gz and .zip archives with compression progress heartbeats."""
    tar_path = base_name_no_ext.with_suffix(".tar.gz")
    zip_path = base_name_no_ext.with_suffix(".zip")

    log_progress("Building .tar.gz archive...")
    with tarfile.open(tar_path, "w:gz") as tar:
        for idx, rec in enumerate(file_records, 1):
            tar.add(rec["abs_path"], arcname=rec["rel_path"])
            if idx % 100 == 0:
                log_progress(f"Tar.gz Progress: {idx}/{len(file_records)} files packed...", echo_console=False)

    log_progress("Building .zip archive...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, rec in enumerate(file_records, 1):
            zf.write(rec["abs_path"], arcname=rec["rel_path"])
            if idx % 100 == 0:
                log_progress(f"Zip Progress: {idx}/{len(file_records)} files packed...", echo_console=False)

    tar_size = tar_path.stat().st_size
    zip_size = zip_path.stat().st_size

    best_type = "tar.gz" if tar_size <= zip_size else "zip"
    best_path = tar_path if best_type == "tar.gz" else zip_path

    return {
        "tar_path": tar_path, "tar_size": tar_size,
        "zip_path": zip_path, "zip_size": zip_size,
        "best_type": best_type, "best_path": best_path
    }

def run_quick_sync():
    CAPTURES_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    # Initialize / truncate progress log for this run
    PROGRESS_LOG.write_text(f"--- Quick Sync Started at {ts} ---\n", encoding="utf-8")

    records = scan_multi_repo()
    
    manifest_lines = [
        "================================================================================",
        "MULTI-REPO QUICK SYNC WORKSPACE MANIFEST",
        f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Target Repositories: {', '.join(TARGET_REPOS)}",
        f"Total Files Scanned: {len(records)}",
        "================================================================================\n"
    ]

    for rec in records:
        manifest_lines.append(f"FILE : {rec['rel_path']}")
        manifest_lines.append(f"HASH : {rec['hash']} | SIZE : {rec['size']} bytes | MOD : {rec['mtime']}")
        manifest_lines.append("HEAD :")
        for line in rec['head'][:3]:
            manifest_lines.append(f"  | {line}")
        manifest_lines.append("-" * 80)

    manifest_path = CAPTURES_DIR / f"{ts}_multi_repo_manifest.txt"
    manifest_text = "\n".join(manifest_lines)
    manifest_path.write_text(manifest_text, encoding="utf-8")

    archive_base = CAPTURES_DIR / f"{ts}_multi_repo_workspace"
    arch_info = create_archives(records, archive_base)

    summary_lines = [
        "\n================================================================================",
        " MULTI-REPO QUICK SYNC COMPLETED",
        "================================================================================",
        f" Repos Scanned   : {', '.join(TARGET_REPOS)}",
        f" Total Files     : {len(records)} files",
        f" Manifest Path   : {manifest_path}",
        f" Tar.gz Archive  : {arch_info['tar_path']} ({arch_info['tar_size']:,} bytes)",
        f" Zip Archive     : {arch_info['zip_path']} ({arch_info['zip_size']:,} bytes)",
        f" OPTIMAL FORMAT  : .{arch_info['best_type']} (Smallest transfer size)",
        "--------------------------------------------------------------------------------",
        " TRIPLE-CLICK COMMAND LINES:",
        "--------------------------------------------------------------------------------",
        f"tail -n 20 {PROGRESS_LOG}",
        f"cat {manifest_path}",
        f"ls -lh {arch_info['best_path']}",
        "================================================================================\n"
    ]

    summary_text = "\n".join(summary_lines)
    log_progress(summary_text)

    load_windows_clipboard(summary_text)

if __name__ == "__main__":
    run_quick_sync()

"""
================================================================================
FILENAME END: gemini/tools/quick_sync.py
================================================================================
"""
