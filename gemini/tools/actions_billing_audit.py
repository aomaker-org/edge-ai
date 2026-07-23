#!/usr/bin/env python3
"""
actions_billing_audit.py
Queries GitHub API for organization actions minutes and shared storage consumption.
Part of the edge-ai telemetry and audit framework.
"""

import subprocess
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = ROOT_DIR / "gemini" / "logs"

def run_gh_api(endpoint):
    try:
        res = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[!] API call failed for {endpoint}: {e.stderr.strip()}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[!] Error parsing response for {endpoint}: {e}", file=sys.stderr)
        return None

def main():
    print("[+] Starting execution: actions_billing_audit.py")
    
    org = "aomaker-org"
    print(f"[*] Querying billing metrics for organization: {org}")
    
    actions_data = run_gh_api(f"/orgs/{org}/settings/billing/actions")
    storage_data = run_gh_api(f"/orgs/{org}/settings/billing/shared-storage")
    
    print("\n--------------------------------------------------")
    print("          GITHUB ACTIONS & STORAGE USAGE         ")
    print("--------------------------------------------------")
    
    timestamp = datetime.now(timezone.utc).isoformat()
    report = {
        "timestamp": timestamp,
        "org": org,
        "actions": actions_data,
        "storage": storage_data
    }
    
    if actions_data:
        print(f"   - Total Minutes Included: {actions_data.get('included_minutes', 'N/A')}")
        print(f"   - Minutes Used: {actions_data.get('total_minutes_used', 'N/A')}")
        print(f"   - Paid Minutes Used: {actions_data.get('total_paid_minutes_used', 'N/A')}")
        print(f"   - Estimated Gross Cost: ${actions_data.get('estimated_paid_minutes_used_amount', 0.0)}")
    else:
        print("   [!] Actions billing data unavailable (check authentication or admin PAT permissions).")
        
    if storage_data:
        print(f"   - Included Storage (GB): {storage_data.get('included_gigabytes', 'N/A')}")
        print(f"   - Estimated Paid Storage GB-Months: {storage_data.get('estimated_paid_storage_for_month', 'N/A')}")
    else:
        print("   [!] Storage billing data unavailable.")
        
    # Append telemetry locally
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "actions_billing_telemetry.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(report) + "\n")
    print(f"\n[+] Telemetry appended to: {log_file.relative_to(ROOT_DIR)}")
    print("--------------------------------------------------")
    print("[+] Completed execution: actions_billing_audit.py")

if __name__ == "__main__":
    main()
