#!/usr/bin/env bash
# ==============================================================================
# FILENAME BEGIN: gemini/tools/edge_nav.sh
# Description: Dynamically loads shell shortcuts from edge_ai_env.toml
# ==============================================================================

EDGE_TOML="/home/fekerr/src/edge-ai/edge_ai_env.toml"

if [ ! -f "$EDGE_TOML" ]; then
    echo "[EDGE-NAV ERROR] Missing $EDGE_TOML"
    return 1 2>/dev/null || exit 1
fi

eval "$(python3 - << 'PYEOF'
import sys, re
from pathlib import Path

toml_path = Path("/home/fekerr/src/edge-ai/edge_ai_env.toml")
content = toml_path.read_text(encoding="utf-8")

current_section = ""
data = {}

for line in content.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    sec_match = re.match(r'^\[([\w_]+)\]$', line)
    if sec_match:
        current_section = sec_match.group(1)
        data[current_section] = {}
        continue
    kv_match = re.match(r'^([\w_]+)\s*=\s*"([^"]+)"$', line)
    if kv_match and current_section:
        data[current_section][kv_match.group(1)] = kv_match.group(2)

shortcuts = data.get("shortcuts", {})

for shortcut_alias, path_ref in shortcuts.items():
    parts = path_ref.split(".")
    if len(parts) == 2:
        section, key = parts
        target_path = data.get(section, {}).get(key)
        if target_path:
            print(f'function {shortcut_alias}() {{ cd "{target_path}" && echo "[NAV] -> {target_path}"; }}')

PYEOF
)"

echo "[EDGE-NAV] Shell shortcuts loaded from TOML."
# ==============================================================================
# FILENAME END: gemini/tools/edge_nav.sh
# ==============================================================================
