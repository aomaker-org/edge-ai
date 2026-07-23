#!/usr/bin/env python3
"""
update_pr_11.py
Stages and commits TODO-008 and the GitHub Actions workflow, then pushes to PR #11.
"""
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    subprocess.run(args, cwd=ROOT_DIR, check=True)

def main():
    print("[+] Starting execution: update_pr_11.py")
    
    run_cmd(["git", "add", "gemini/backlog.yaml", ".github/workflows/actions-cost-audit.yml", "gemini/tools/"])
    
    status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT_DIR)
    if status.returncode != 0:
        run_cmd(["git", "commit", "-m", "feat(telemetry): add TODO-008 backlog item and daily actions cost audit workflow"])
    
    run_cmd(["git", "push", "origin", "feat/gitignore-and-backlog-updates"])
    
    print("[+] Completed execution: update_pr_11.py")
    print("[+] PR #11 updated successfully with billing telemetry tools and TODO-008!")

if __name__ == "__main__":
    main()
