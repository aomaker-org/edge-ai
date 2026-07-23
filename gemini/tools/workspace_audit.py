#!/usr/bin/env python3
"""
workspace_audit.py
Scans the edge-ai workspace, categorizing codebases (Rust, C++, Python, Headers)
and inspecting submodule states without flooding the terminal.
"""

import os
from pathlib import Path
import subprocess
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_git_cmd(args):
    result = subprocess.run(["git"] + args, cwd=ROOT_DIR, capture_output=True, text=True)
    return result.stdout.strip()

def audit_workspace():
    print("==================================================")
    print("         EDGE-AI WORKSPACE AUDITOR v1.0           ")
    print("==================================================")
    
    # 1. Submodule Status
    print("\n[+] Submodule Status (deps/llama.cpp):")
    sub_status = run_git_cmd(["submodule", "status"])
    print(sub_status if sub_status else "   No submodules active.")

    # 2. File Categorization in src/ and root
    print("\n[+] Scanning Codebase Files...")
    extensions = {".rs": "Rust", ".cpp": "C++", ".hpp": "C++ Header", ".py": "Python", ".c": "C", ".h": "C Header", ".md": "Markdown"}
    counts = {v: 0 for v in extensions.values()}
    other_count = 0

    src_path = ROOT_DIR / "src"
    if src_path.exists():
        for path in src_path.rglob("*"):
            if path.is_file():
                if "target" in path.parts:
                    continue
                ext = path.suffix.lower()
                if ext in extensions:
                    counts[extensions[ext]] += 1
                else:
                    other_count += 1

    for lang, count in counts.items():
        if count > 0:
            print(f"   - {lang}: {count} files")
    print(f"   - Other / Assets: {other_count} files")

    # 3. Git Working Tree Status Summary
    print("\n[+] Git Modified / Untracked Summary:")
    status_output = run_git_cmd(["status", "--porcelain"])
    if status_output:
        for line in status_output.splitlines():
            code, filepath = line[:2], line[3:]
            print(f"   [{code.strip()}] {filepath}")
    else:
        print("   Working tree is completely clean.")
    print("==================================================")

if __name__ == "__main__":
    audit_workspace()
