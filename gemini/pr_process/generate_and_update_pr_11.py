#!/usr/bin/env python3
"""
generate_and_update_pr_11.py
Generates the workflow file, stages changes, commits, and pushes to PR #11.
"""
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    subprocess.run(args, cwd=ROOT_DIR, check=True)

def main():
    print("[+] Starting execution: generate_and_update_pr_11.py")
    
    # 1. Ensure workflow directory and file exist
    workflows_dir = ROOT_DIR / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    workflow_path = workflows_dir / "actions-cost-audit.yml"
    
    workflow_content = """name: Daily Actions Usage Audit

on:
  schedule:
    - cron: '0 0 * * *' # Runs every day at 00:00 UTC
  workflow_dispatch:

jobs:
  audit-usage:
    runs-on: ubuntu-latest
    steps:
      - name: Fetch Actions Billing Data
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          echo "=== Actions Minutes Usage ==="
          gh api /orgs/aomaker-org/settings/billing/actions || echo "Org-level API requires admin PAT permissions"
          
          echo "=== Shared Storage Usage ==="
          gh api /orgs/aomaker-org/settings/billing/shared-storage || echo "Storage API requires admin PAT permissions"
"""
    workflow_path.write_text(workflow_content)
    print(f"[+] Created/verified workflow at: {workflow_path.relative_to(ROOT_DIR)}")

    # 2. Stage changes
    run_cmd(["git", "add", "gemini/backlog.yaml", ".github/workflows/actions-cost-audit.yml", "gemini/tools/"])

    # 3. Commit if changes exist
    status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT_DIR)
    if status.returncode != 0:
        run_cmd(["git", "commit", "-m", "feat(telemetry): add TODO-008 backlog item and daily actions cost audit workflow"])

    # 4. Push updates
    run_cmd(["git", "push", "origin", "feat/gitignore-and-backlog-updates"])

    print("[+] Completed execution: generate_and_update_pr_11.py")
    print("[+] PR #11 updated successfully!")

if __name__ == "__main__":
    main()
