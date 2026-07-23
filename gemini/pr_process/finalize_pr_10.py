#!/usr/bin/env python3
"""
finalize_pr_10.py
Commits PR process scripts, pushes updates, merges PR #10, and syncs main.
"""
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    subprocess.run(args, cwd=ROOT_DIR, check=True)

def main():
    print("[+] Starting execution: finalize_pr_10.py")
    
    # 1. Stage and commit pr_process scripts
    run_cmd(["git", "add", "gemini/pr_process/"])
    
    # Check if there are changes to commit
    status_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT_DIR)
    if status_check.returncode != 0:
        run_cmd(["git", "commit", "-m", "feat(gemini): add PR automation script framework to repository"])
    
    # 2. Push updates
    run_cmd(["git", "push", "origin", "feat/tools-and-src-inventory"])
    
    # 3. Merge PR #10
    run_cmd(["gh", "pr", "merge", "10", "--merge", "--delete-branch"])
    
    # 4. Switch to main and pull
    run_cmd(["git", "checkout", "main"])
    run_cmd(["git", "pull", "origin", "main"])
    
    print("[+] Completed execution: finalize_pr_10.py")
    print("[+] PR #10 successfully finalized and merged!")

if __name__ == "__main__":
    main()
