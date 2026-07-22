#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/mod_toggle.py
================================================================================
Utility: Feature & Submodule Toggle Manager for edge-ai
Description: Enables or disables repository submodules by managing git submodules
             and toggling edge-ai.mk-off <-> edge-ai.mk extensions.
================================================================================
"""

import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Module registry
MODULES = {
    "llama": {
        "submodule_path": "deps/llama.cpp",
        "mk_dir": REPO_ROOT / "deps" / "llama.cpp"
    },
    "litert": {
        "submodule_path": "deps/litert-lm",
        "mk_dir": REPO_ROOT / "deps" / "litert-lm"
    }
}

def enable_module(mod_key):
    if mod_key not in MODULES:
        print(f"Unknown module '{mod_key}'. Available: {list(MODULES.keys())}")
        return

    mod = MODULES[mod_key]
    sub_path = mod["submodule_path"]

    print(f"[Toggle] Shallow-fetching submodule: {sub_path}...")
    subprocess.run(f"git submodule update --init --depth 1 {sub_path}", shell=True, cwd=REPO_ROOT)

    # Toggle .mk-off -> .mk
    mk_off = mod["mk_dir"] / "edge-ai.mk-off"
    mk_on = mod["mk_dir"] / "edge-ai.mk"

    if mk_off.exists():
        mk_off.rename(mk_on)
        print(f"[Toggle] Activated Make context: {mk_on.relative_to(REPO_ROOT)}")
    elif mk_on.exists():
        print(f"[Toggle] Make context is already active: {mk_on.relative_to(REPO_ROOT)}")

def disable_module(mod_key):
    if mod_key not in MODULES:
        print(f"Unknown module '{mod_key}'.")
        return

    mod = MODULES[mod_key]
    sub_path = mod["submodule_path"]

    # Toggle .mk -> .mk-off
    mk_off = mod["mk_dir"] / "edge-ai.mk-off"
    mk_on = mod["mk_dir"] / "edge-ai.mk"

    if mk_on.exists():
        mk_on.rename(mk_off)
        print(f"[Toggle] Deactivated Make context: {mk_off.relative_to(REPO_ROOT)}")

    print(f"[Toggle] De-initializing submodule to reclaim disk space: {sub_path}...")
    subprocess.run(f"git submodule deinit -f {sub_path}", shell=True, cwd=REPO_ROOT)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 mod_toggle.py enable <module_name>")
        print("  python3 mod_toggle.py disable <module_name>")
        sys.exit(1)

    cmd, target = sys.argv[1], sys.argv[2]
    if cmd == "enable":
        enable_module(target)
    elif cmd == "disable":
        disable_module(target)

"""
================================================================================
FILENAME END: gemini/tools/mod_toggle.py
================================================================================
"""
