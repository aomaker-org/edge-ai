#!/usr/bin/env python3
"""
submit_tools_pr.py
Automates branch creation, staging, committing, and PR submission
for the new Gemini tools, documentation, and src codebase components.
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    res = subprocess.run(args, cwd=ROOT_DIR, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr and res.returncode != 0:
        print(res.stderr, file=sys.stderr)
    return res.returncode

def main():
    branch_name = "feat/tools-and-src-inventory"
    
    print(f"[*] Ensuring we are on main and up to date...")
    run_cmd(["git", "checkout", "main"])
    run_cmd(["git", "pull", "origin", "main"])

    print(f"[*] Creating and switching to branch {branch_name}...")
    # Check if branch exists locally; delete or checkout accordingly
    branch_check = subprocess.run(["git", "rev-parse", "--verify", branch_name], cwd=ROOT_DIR, capture_output=True)
    if branch_check.returncode == 0:
        run_cmd(["git", "checkout", branch_name])
    else:
        run_cmd(["git", "checkout", "-b", branch_name])

    print("[*] Staging tools, docs, and source files...")
    run_cmd(["git", "add", "gemini/tools/", "gemini/docs/", "src/"])

    # Check if there are changes staged
    diff_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT_DIR)
    if diff_check.returncode == 0:
        print("[!] No staged changes found to commit. Workspace may already be clean.")
        return

    print("[*] Committing changes...")
    commit_msg = "feat(gemini): add workspace audit tools, src inventory docs, and codebase components"
    run_cmd(["git", "commit", "-m", commit_msg])

    print("[*] Pushing branch to origin...")
    run_cmd(["git", "push", "-u", "origin", branch_name])

    print("[*] Creating Pull Request via GitHub CLI...")
    title = "feat(gemini): add workspace audit tools, src inventory docs, and codebase components"
    body = (
        "## Summary\n"
        "- Adds Python workspace audit (`workspace_audit.py`) and source inspection (`inspect_src.py`) utilities under `gemini/tools/`.\n"
        "- Adds formal tools inventory documentation (`tools_inventory.md`) under `gemini/docs/`.\n"
        "- Incorporates `src/` utility components (`gix_manifest`, `host_info.cpp`, `win_bench`)."
    )

    pr_code = run_cmd([
        "gh", "pr", "create",
        "--base", "main",
        "--head", branch_name,
        "--title", title,
        "--body", body
    ])

    if pr_code == 0:
        print("[+] PR created successfully!")
    else:
        print("[!] PR creation encountered an issue (it may already exist). Check `gh pr status`.")

if __name__ == "__main__":
    main()
