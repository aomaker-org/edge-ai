#!/usr/bin/env python3
"""
=== BEGIN ARTIFACT ===
PATH: gemini/tools/ledger.py
ID: ledger_utility_v5
TYPE: Python CLI Tool
FORMAT: text/safe-interchange
=== HEADER ===

Unified telemetry utility bridging Git status and offsite YAML ledgers
with Git-style triage (default brief summary + action items) and 
--detail-archives support.

=== FOOTER ===
end of file gemini/tools/ledger.py
=== END HEADER ===
"""

import subprocess
import pathlib
import sys
import os
import configparser
import yaml

LEDGER_PATH = pathlib.Path("gemini/ledgers/manifest_ledger_v1.yaml")
POINTERS_DIR = pathlib.Path("gemini/captures")
CONFIG_PATH = pathlib.Path("gemini/ledgers/.config.ledger")

def print_help():
    print("""
Usage: python3 gemini/tools/ledger.py [OPTIONS]

Unified telemetry utility bridging Git status and offsite YAML ledgers.

Options:
  --ledgeronly      Run checks exclusively on offsite YAML ledgers and pointer stubs (skips git status).
  --detail-archives Show the full itemized list of all cataloged archived files.
  --persistent      Save the current --ledgeronly preference to the local config file (.config.ledger).
  -h, --help        Show this help message and exit.

Examples:
  python3 gemini/tools/ledger.py --ledgeronly
      # Temporarily view only the ledger status; for git, just use 'git status'.
      
  python3 gemini/tools/ledger.py --detail-archives
      # View full itemized list of all offloaded archives alongside summary.
      
  python3 gemini/tools/ledger.py --ledgeronly --persistent
      # Saves the preference to default to ledger-only mode permanently.
      
  python3 gemini/tools/ledger.py --persistent
      # Resets/saves preference back to the default combined view (git + ledger).
    """)

def load_config():
    config = configparser.ConfigParser()
    if CONFIG_PATH.exists():
        config.read(CONFIG_PATH)
    return config

def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

def run_git_status():
    print("=== Git Repository Status ===")
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    print(result.stdout)

def run_ledger_status(detail_archives=False):
    print("=== Offsite Ledger & Pointer Status (v1.0.0) ===")
    if not LEDGER_PATH.exists():
        print(f"[!] Warning: Ledger not found at {LEDGER_PATH}")
        return

    with open(LEDGER_PATH, "r") as f:
        data = yaml.safe_load(f) or {}

    artifacts = data.get("artifacts", [])
    total_artifacts = len(artifacts)
    missing_pointers = 0
    action_items = []

    # Scan captures directory for un-ledgered heavy binaries or missing pointers
    cataloged_names = {item.get("name") for item in artifacts}
    
    if POINTERS_DIR.exists():
        # Check for un-ledgered tar.gz or zip files in captures
        for raw_file in POINTERS_DIR.glob("*"):
            if raw_file.suffix in (".gz", ".zip", ".tar") and not raw_file.name.endswith(".pointer"):
                if raw_file.name not in cataloged_names:
                    action_items.append(f"Un-offloaded heavy binary found: {raw_file.relative_to(pathlib.Path.cwd())} (Needs offload & pointer)")

    for item in artifacts:
        name = item.get("name")
        pointer_file = POINTERS_DIR / f"{name}.pointer"
        if not pointer_file.exists():
            missing_pointers += 1
            action_items.append(f"Missing pointer stub for cataloged artifact: {name}")

    # Brief Summary (Git-style status)
    print(f"Schema Version: {data.get('schema_version', 'unknown')}")
    print(f"Destination:    {data.get('offload_destination_root', 'unknown')}")
    print(f"Catalog Summary: {total_artifacts} artifacts cataloged | {missing_pointers} missing pointer stubs")

    # Triage / Work to Do Section
    if action_items:
        print("\n--- Work to Do / Action Items ---")
        for action in action_items:
            print(f"  [!] {action}")
    else:
        print("\n--- Work to Do / Action Items ---")
        print("  [✓] All cataloged artifacts have valid local pointer stubs. No pending actions.")

    # Detailed Itemized View (if requested)
    if detail_archives:
        print("\n=== Detailed Archive Catalog ===")
        for item in artifacts:
            name = item.get("name")
            status = item.get("status")
            pointer_file = POINTERS_DIR / f"{name}.pointer"
            pointer_exists = pointer_file.exists()
            print(f"  - {name}")
            print(f"    Status:  {status}")
            print(f"    Pointer: {'[OK] Exists' if pointer_exists else '[MISSING] Stub missing'}")
    else:
        print("\n(Tip: Run with --detail-archives to view itemized archive listings)")

def main():
    args = sys.argv[1:]
    
    # Handle help flags immediately
    if "-h" in args or "--help" in args:
        print_help()
        sys.exit(0)
    
    # Load existing persistent config
    config = load_config()
    cfg_ledger_only = config.getboolean("settings", "ledger_only", fallback=False)
    
    # Check environment variable override
    env_override = os.environ.get("LEDGER_ONLY", "").lower() in ("true", "1", "yes")
    env_is_set = "LEDGER_ONLY" in os.environ
    
    # Check CLI flags
    cli_ledger_only = "--ledgeronly" in args
    detail_archives = "--detail-archives" in args
    persistent_flag = "--persistent" in args
    
    # Determine final state based on precedence: CLI > Env > Config
    if cli_ledger_only:
        ledger_only = True
    elif env_is_set:
        ledger_only = env_override
    else:
        ledger_only = cfg_ledger_only
        
    # Handle persistence request
    if persistent_flag:
        if not config.has_section("settings"):
            config.add_section("settings")
        config.set("settings", "ledger_only", str(cli_ledger_only))
        save_config(config)
        print(f"[*] Persistent configuration saved to {CONFIG_PATH} (ledger_only={cli_ledger_only})")

    # Execution
    if not ledger_only:
        run_git_status()
        print("\n" + "="*40 + "\n")
        
    run_ledger_status(detail_archives=detail_archives)

if __name__ == "__main__":
    main()
