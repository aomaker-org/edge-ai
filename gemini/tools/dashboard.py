#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/dashboard.py
================================================================================
Utility: Interactive Terminal Status Dashboard
Description: Renders real-time metrics for Git/Gix state, manifest status,
             device targets, backups, logs, and rclone connectivity.
================================================================================
"""

import os
import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GEMINI_DIR = REPO_ROOT / "gemini"
MANIFEST_PATH = REPO_ROOT / "manifest.json"
GIX_BIN = REPO_ROOT / "src/tools/gix_manifest/target/release/gix_manifest"

def get_git_info():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO_ROOT, text=True).strip()
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, text=True).strip()
        status_lines = subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True).splitlines()
        return branch, commit, len(status_lines)
    except Exception:
        return "unknown", "unknown", 0

def check_device_targets():
    devices = ["rp2040", "rp235x"]
    status = {}
    for dev in devices:
        dev_path = REPO_ROOT / "devices" / dev
        status[dev] = "PRESENT" if dev_path.exists() else "MISSING"
    return status

def get_manifest_stats():
    if not MANIFEST_PATH.exists():
        return None
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        return data.get("metadata", {})
    except Exception:
        return None

def check_rclone():
    try:
        res = subprocess.run(["rclone", "version"], capture_output=True, text=True)
        return "INSTALLED" if res.returncode == 0 else "NOT_FOUND"
    except Exception:
        return "NOT_INSTALLED"

def render_dashboard():
    branch, commit, uncommitted = get_git_info()
    devices = check_device_targets()
    manifest_meta = get_manifest_stats()
    rclone_status = check_rclone()

    gix_status = "READY (Compiled)" if GIX_BIN.exists() else "NOT_COMPILED (Run cargo build)"

    backups_count = len(list((GEMINI_DIR / "backups").glob("*.bak"))) if (GEMINI_DIR / "backups").exists() else 0
    captures_count = len(list((GEMINI_DIR / "captures").glob("*"))) if (GEMINI_DIR / "captures").exists() else 0

    print("================================================================================")
    print("                 EDGE-AI WORKSPACE TERMINAL DASHBOARD                           ")
    print("================================================================================")
    print(f" Repo Root       : {REPO_ROOT}")
    print(f" Git State       : Branch [{branch}] @ Commit [{commit}] ({uncommitted} uncommitted files)")
    print(f" Gix Fast Engine : {gix_status}")
    print("--------------------------------------------------------------------------------")
    print(" DEVICE TARGETS:")
    for dev, stat in devices.items():
        print(f"   - devices/{dev:<10}: [{stat}]")
    print("--------------------------------------------------------------------------------")
    print(" MANIFEST & ASSETS METRICS:")
    if manifest_meta:
        print(f"   - Total Workspace Files : {manifest_meta.get('total_files', 0):,}")
        print(f"   - Total Workspace Size  : {manifest_meta.get('total_bytes', 0) / (1024*1024):.2f} MB")
        print(f"   - Rclone Sync Targets   : {manifest_meta.get('rclone_candidates_count', 0):,} candidates")
        print(f"   - Last Manifest Update  : {manifest_meta.get('generated_utc', 'N/A')}")
    else:
        print("   - [NOTICE] manifest.json missing. Run ./git_good.sh sync")
    print("--------------------------------------------------------------------------------")
    print(" ARCHIVES & STORAGE:")
    print(f"   - Provenance Backups    : {backups_count} backup files in gemini/backups/")
    print(f"   - Capture Artifacts     : {captures_count} artifacts in gemini/captures/")
    print(f"   - Rclone CLI Tool       : [{rclone_status}]")
    print("================================================================================")
    print(" QUICK COMMAND VERBS:")
    print("   ./git_good.sh status  |  ./git_good.sh save \"msg\"  |  ./git_good.sh sync")
    print("   python3 gemini/tools/dashboard.py  |  gemini/tools/export_to_gdrive.sh")
    print("================================================================================")

if __name__ == "__main__":
    render_dashboard()

"""
================================================================================
FILENAME END: gemini/tools/dashboard.py
================================================================================
"""
