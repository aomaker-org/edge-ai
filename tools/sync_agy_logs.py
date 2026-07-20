#!/usr/bin/env python3
"""
tools/sync_agy_logs.py

Idempotent, append-only synchronization tool for edge-ai.
Captures AI agent prompts, responses, and session telemetry into agy/.
"""

import os
import sys
import glob
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

def get_search_dirs(custom_brain_dir=None):
    dirs = []
    if custom_brain_dir:
        dirs.append(Path(custom_brain_dir))
    
    env_brain = os.environ.get("AGY_LOG_DIR") or os.environ.get("APP_DATA_DIR")
    if env_brain:
        dirs.append(Path(env_brain))
        dirs.append(Path(env_brain) / "brain")

    default_cli = Path.home() / ".gemini" / "antigravity-cli"
    dirs.append(default_cli / "brain")
    dirs.append(default_cli / "conversations")
    return dirs

def hash_entry(cid: str, step_index: int, content: str) -> str:
    raw = f"{cid}:{step_index}:{content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def load_existing_hashes(prompts_file: Path) -> set:
    existing = set()
    if not prompts_file.exists():
        return existing
    with open(prompts_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "entry_hash" in data:
                    existing.add(data["entry_hash"])
            except json.JSONDecodeError:
                continue
    return existing

def parse_transcript(transcript_path: Path):
    entries = []
    cid = transcript_path.parent.parent.name if ".system_generated" in str(transcript_path) else transcript_path.stem
    if not transcript_path.exists():
        return cid, entries

    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                step = json.loads(line)
                step_idx = step.get("step_index", 0)
                step_type = step.get("type", "")
                content = step.get("content", "")
                
                # Capture User Prompts and Agent Responses
                if step_type in ("USER_INPUT", "PLANNER_RESPONSE") or "USER_REQUEST" in str(content):
                    ehash = hash_entry(cid, step_idx, str(content)[:200])
                    entries.append({
                        "conversation_id": cid,
                        "step_index": step_idx,
                        "type": step_type,
                        "content": content,
                        "entry_hash": ehash,
                        "synced_at": datetime.now().isoformat()
                    })
            except json.JSONDecodeError:
                continue

    return cid, entries

def format_timestamp(seq: int = 1) -> str:
    now = datetime.now()
    return f"{now.strftime('%y%m%d_%H%M')}_{seq:03d}"

def sync_logs(workspace_root: Path, custom_brain_dir=None, sequence_start: int = 1):
    agy_dir = workspace_root / "agy"
    sessions_dir = agy_dir / "sessions"
    prompts_file = agy_dir / "prompts.jsonl"
    
    agy_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir.mkdir(parents=True, exist_ok=True)

    existing_hashes = load_existing_hashes(prompts_file)
    search_dirs = get_search_dirs(custom_brain_dir)

    new_entries_count = 0
    sessions_updated = set()
    seq_counter = sequence_start

    for sdir in search_dirs:
        if not sdir.exists():
            continue
        transcript_files = list(sdir.glob("**/transcript*.jsonl")) + list(sdir.glob("*.jsonl"))
        for tf in transcript_files:
            cid, entries = parse_transcript(tf)
            new_for_cid = []
            for entry in entries:
                if entry["entry_hash"] not in existing_hashes:
                    new_for_cid.append(entry)
                    existing_hashes.add(entry["entry_hash"])

            if new_for_cid:
                # Append to prompts.jsonl (Append-Only)
                with open(prompts_file, "a", encoding="utf-8") as pf:
                    for entry in new_for_cid:
                        pf.write(json.dumps(entry) + "\n")
                        new_entries_count += 1
                
                sessions_updated.add(cid)
                
                # Write / Update session summary markdown using YYMMDD_HHMM_NNN format
                ts_prefix = format_timestamp(seq_counter)
                session_md = sessions_dir / f"{ts_prefix}_session_{cid[:8]}.md"
                mode = "a" if session_md.exists() else "w"
                with open(session_md, mode, encoding="utf-8") as sm:
                    if mode == "w":
                        sm.write(f"# AGY Session Record: `{cid}`\n\n")
                        sm.write(f"Timestamp ID: `{ts_prefix}`\n")
                        sm.write(f"Created: {datetime.now().isoformat()}\n\n---\n\n")
                    for entry in new_for_cid:
                        sm.write(f"### Step {entry['step_index']} [{entry['type']}]\n")
                        sm.write(f"```text\n{entry['content']}\n```\n\n")
                seq_counter += 1

    print(f"[agy-sync] Synced {new_entries_count} new telemetry entries across {len(sessions_updated)} sessions.")
    print(f"[agy-sync] Total unique entries tracked: {len(existing_hashes)}")

def print_status(workspace_root: Path):
    agy_dir = workspace_root / "agy"
    prompts_file = agy_dir / "prompts.jsonl"
    sessions_dir = agy_dir / "sessions"

    if not prompts_file.exists():
        print("[agy-status] Telemetry log file agy/prompts.jsonl does not exist yet. Run 'make agy-sync'.")
        return

    existing_hashes = load_existing_hashes(prompts_file)
    session_files = list(sessions_dir.glob("session_*.md")) if sessions_dir.exists() else []

    print("==================================================================")
    print(" AGY AI Agent Telemetry Status")
    print("==================================================================")
    print(f" Prompts File:        {prompts_file}")
    print(f" Total Logged Steps:  {len(existing_hashes)}")
    print(f" Session Records:     {len(session_files)}")
    print(f" Storage Size:        {prompts_file.stat().st_size} bytes")
    print("==================================================================")

def main():
    parser = argparse.ArgumentParser(description="AGY Log Sync Utility")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Workspace root path")
    parser.add_argument("--brain-dir", type=Path, default=None, help="Custom brain/transcript directory")
    parser.add_argument("--seq-start", type=int, default=1, help="Starting sequence number (nnn, default=1)")
    parser.add_argument("--status", action="store_true", help="Print telemetry status")
    args = parser.parse_args()

    if args.status:
        print_status(args.workspace)
    else:
        sync_logs(args.workspace, args.brain_dir, sequence_start=args.seq_start)

if __name__ == "__main__":
    main()
