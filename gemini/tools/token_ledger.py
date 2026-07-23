================================================================================
FILENAME BEGIN: gemini/tools/token_ledger.py
================================================================================

#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/token_ledger.py
================================================================================
Utility: Quantitative Token Ledger & Budget Planner
Description: Tracks API token usage over time. Allows agents to log their 
             usage and query trailing 5-hour and 7-day rolling totals to 
             make intelligent routing and pause decisions.
================================================================================
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LEDGER_FILE = REPO_ROOT / "gemini" / "token_ledger.json"

def load_ledger():
    if not LEDGER_FILE.exists():
        return []
    try:
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_ledger(data):
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_usage(model, prompt_tokens, comp_tokens):
    """Records a single API call's token usage."""
    data = load_ledger()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": model,
        "prompt_tokens": int(prompt_tokens),
        "completion_tokens": int(comp_tokens),
        "total_tokens": int(prompt_tokens) + int(comp_tokens)
    }
    data.append(entry)
    save_ledger(data)
    print(f"[Token Ledger] Logged {entry['total_tokens']} tokens to {model}.")

def report_usage():
    """Calculates rolling usage for API budget planning."""
    data = load_ledger()
    if not data:
        print("Token ledger is empty.")
        return

    now = datetime.utcnow()
    past_5_hours = now - timedelta(hours=5)
    past_7_days = now - timedelta(days=7)

    stats = {
        "5h_prompt": 0, "5h_comp": 0, "5h_total": 0,
        "7d_prompt": 0, "7d_comp": 0, "7d_total": 0,
    }

    for entry in data:
        try:
            ts = datetime.fromisoformat(entry["timestamp"].replace("Z", ""))
            
            if ts >= past_7_days:
                stats["7d_prompt"] += entry.get("prompt_tokens", 0)
                stats["7d_comp"] += entry.get("completion_tokens", 0)
                stats["7d_total"] += entry.get("total_tokens", 0)
                
            if ts >= past_5_hours:
                stats["5h_prompt"] += entry.get("prompt_tokens", 0)
                stats["5h_comp"] += entry.get("completion_tokens", 0)
                stats["5h_total"] += entry.get("total_tokens", 0)
        except Exception:
            continue

    print("\n================================================================================")
    print(" TOKEN USAGE REPORT (Rolling Windows)")
    print("================================================================================")
    print(f" Past 5 Hours : {stats['5h_total']:,} total tokens")
    print(f"   |- Prompt  : {stats['5h_prompt']:,}")
    print(f"   `- Output  : {stats['5h_comp']:,}")
    print("-" * 80)
    print(f" Past 7 Days  : {stats['7d_total']:,} total tokens")
    print(f"   |- Prompt  : {stats['7d_prompt']:,}")
    print(f"   `- Output  : {stats['7d_comp']:,}")
    print("================================================================================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 token_ledger.py log <model> <prompt_tokens> <completion_tokens>")
        print("  python3 token_ledger.py report")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "log" and len(sys.argv) == 5:
        log_usage(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "report":
        report_usage()
    else:
        print("Invalid arguments.")
EOF

chmod +x ~/src/edge-ai/gemini/tools/token_ledger.py

================================================================================
FILENAME END: gemini/tools/token_ledger.py
================================================================================
