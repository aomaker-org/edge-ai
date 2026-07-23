#!/usr/bin/env python3
"""
finalize_pr_11_fix.py
Removes the workflow file from git tracking, amends commit, pushes, merges PR #11, and syncs main.
"""
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_cmd(args, check=True):
    print(f"Running: {' '.join(args)}")
    return subprocess.run(args, cwd=ROOT_DIR, check=check)

def main():
    print("[+] Starting execution: finalize_pr_11_fix.py")
    
    # 1. Ensure workflow file is completely removed from disk and git index
    workflow_file = ROOT_DIR / ".github" / "workflows" / "actions-cost-audit.yml"
    if workflow_file.exists():
        workflow_file.unlink()
    run_cmd(["git", "rm", "-f", ".github/workflows/actions-cost-audit.yml"], check=False)
    
    # 2. Stage configuration, backlog, and tool scripts
    run_cmd(["git", "add", ".gitignore", "gemini/backlog.yaml", "gemini/tools/"])
    
    # 3. Amend the commit to strip out the workflow file entirely
    run_cmd(["git", "commit", "--amend", "-m", "chore(config): update recursive target ignore, backlog items, and billing audit tool"])
    
    # 4. Push branch updates safely
    run_cmd(["git", "push", "origin", "feat/gitignore-and-backlog-updates", "--force-with-lease"])
    
    # 5. Merge PR #11 via GitHub CLI and delete branch
    run_cmd(["gh", "pr", "merge", "11", "--merge", "--delete-branch"])
    
    # 6. Checkout main and pull latest
    run_cmd(["git", "checkout", "main"])
    run_cmd(["git", "pull", "origin", "main"])
    
    print("[+] Completed execution: finalize_pr_11_fix.py")
    print("[+] PR #11 successfully finalized, merged, and repository synced!")

if __name__ == "__main__":
    main()
