#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
uv run python3 "${SCRIPT_DIR}/tools/process_inbox.py"
