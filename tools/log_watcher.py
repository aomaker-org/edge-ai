#!/usr/bin/env python3
"""
==============================================================================
Project:      edge-ai
Path:         tools/log_watcher.py
Purpose:      Extended real-time log file watcher with max 1Hz rate limiting,
              TOML configuration synchronization, sectioned tree displays,
              auto-discovery, and live file append prompts.
Architecture: Rate-limited rendering (<=1.0 Hz), tomllib parsing, sectioned tree.
Standard:     Rule 8 (YYMMDD_HHMM_NNN Timestamping) & Clean Root Hygiene.
==============================================================================
"""

import argparse
import datetime
import fnmatch
import os
import sys
import time

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def get_rule8_timestamp() -> str:
    """Generate Rule 8 YYMMDD_HHMM_NNN timestamp string."""
    now = datetime.datetime.now()
    return now.strftime("%y%m%d_%H%M_001")


class LogWatcher:

    def __init__(self, config_path: str, target_section: str = None, add_paths: list = None, remove_paths: list = None):
        self.project_root = os.environ.get("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        self.config_path = os.path.join(self.project_root, config_path)
        self.target_section = target_section
        self.add_paths = add_paths or []
        self.remove_paths = remove_paths or []

        self.last_render_time = 0.0
        self.min_render_interval = 1.0  # Max 1Hz update frequency limit

        self.known_files = {}  # file_path -> size
        self.notifications = []  # List of recent prompt alerts

        self.config = self.load_or_create_config()

    def load_or_create_config(self) -> dict:
        """Load TOML configuration or return default structure."""
        if os.path.exists(self.config_path) and tomllib:
            try:
                with open(self.config_path, "rb") as f:
                    return tomllib.load(f)
            except Exception as e:
                print(f"[!] Warning: Could not parse TOML config ({e}). Using default settings.")

        return {
            "general": {
                "max_refresh_hz": 1.0,
                "scan_interval_sec": 1.0,
                "auto_discover": True,
            },
            "sections": {
                "telemetry": {
                    "name": "Hardware & Inference Telemetry Logs",
                    "paths": ["logs"],
                    "patterns": ["*.jsonl", "*.csv"],
                    "enabled": True,
                },
                "build_logs": {
                    "name": "Out-of-Tree Build & Compiler Logs",
                    "paths": ["build"],
                    "patterns": ["*.log"],
                    "enabled": True,
                },
                "agy_sessions": {
                    "name": "AI Agent Telemetry Sessions",
                    "paths": ["agy"],
                    "patterns": ["*.jsonl", "*.md"],
                    "enabled": True,
                },
            },
            "discovered_files": {},
        }

    def update_toml_discovered(self, section_name: str, new_files: list):
        """Append newly discovered log files to the TOML configuration file."""
        if not new_files or not os.path.exists(self.config_path):
            return

        try:
            with open(self.config_path, "r") as f:
                content = f.read()

            block = f"\n# Auto-discovered in {section_name} at {get_rule8_timestamp()}\n"
            for nf in new_files:
                rel = os.path.relpath(nf, self.project_root)
                block += f'# "{rel}"\n'

            with open(self.config_path, "a") as f:
                f.write(block)
        except Exception:
            pass

    def scan_section_files(self, section_info: dict) -> dict:
        """Scan paths for files matching patterns within a section."""
        matched = {}
        paths = section_info.get("paths", [])
        patterns = section_info.get("patterns", ["*"])

        # Incorporate dynamic add/remove paths
        for ap in self.add_paths:
            if ap not in paths:
                paths.append(ap)
        for rp in self.remove_paths:
            if rp in paths:
                paths.remove(rp)

        for p in paths:
            abs_p = os.path.join(self.project_root, p) if not os.path.isabs(p) else p
            if not os.path.exists(abs_p):
                continue

            if os.path.isfile(abs_p):
                rel_path = os.path.relpath(abs_p, self.project_root)
                size = os.path.getsize(abs_p)
                matched[abs_p] = (rel_path, size)
            else:
                for root, _, files in os.walk(abs_p):
                    for f in files:
                        for pat in patterns:
                            if fnmatch.fnmatch(f, pat):
                                full_f = os.path.join(root, f)
                                rel_f = os.path.relpath(full_f, self.project_root)
                                size = os.path.getsize(full_f)
                                matched[full_f] = (rel_f, size)
                                break

        return matched

    def audit_changes(self, all_current_files: dict):
        """Audit for new files and appended byte changes, logging prompt alerts."""
        new_discovered = []
        now_str = datetime.datetime.now().strftime("%H:%M:%S")

        for full_path, (rel_path, current_size) in all_current_files.items():
            if full_path not in self.known_files:
                self.known_files[full_path] = current_size
                new_discovered.append(full_path)
                self.notifications.append(f"[{now_str}] 🟢 [NEW LOG FILE DISCOVERED] -> {rel_path} ({current_size} bytes)")
            else:
                prev_size = self.known_files[full_path]
                if current_size > prev_size:
                    delta = current_size - prev_size
                    self.known_files[full_path] = current_size
                    self.notifications.append(f"[{now_str}] ⚡ [LOG APPENDED (+{delta} bytes)] -> {rel_path}")

        # Limit alert buffer to last 6 prompt notifications
        if len(self.notifications) > 6:
            self.notifications = self.notifications[-6:]

        return new_discovered

    def render_display(self, sections_data: dict):
        """Render rate-limited terminal screen pass (max 1Hz)."""
        now = time.time()
        if (now - self.last_render_time) < self.min_render_interval:
            return  # Enforce strict 1Hz max refresh rate limit

        self.last_render_time = now
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        r8_ts = get_rule8_timestamp()

        # Clear screen cleanly
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

        print("==================================================================")
        print(f" edge-ai Real-Time Extended Log & Telemetry Watcher")
        print(f" Timestamp: {ts} | Rule 8 Tag: {r8_ts} | Max Refresh Rate: 1.0 Hz")
        print(f" Config: {os.path.basename(self.config_path)}")
        print("==================================================================")

        # Print prompt notification alerts if present
        if self.notifications:
            print("\n🔔 Live Log Activity Notifications:")
            for note in self.notifications:
                print(f"  {note}")
            print("------------------------------------------------------------------")

        # Render sections
        for sec_key, sec_data in sections_data.items():
            name = sec_data["name"]
            files = sec_data["files"]

            print(f"\n📂 Section: [{name}] (Key: {sec_key})")
            if not files:
                print("  └── (No active log files match filter pattern)")
            else:
                sorted_files = sorted(files.values(), key=lambda x: x[0])
                for idx, (rel_path, size) in enumerate(sorted_files):
                    prefix = "└──" if idx == len(sorted_files) - 1 else "├──"
                    size_kb = size / 1024.0
                    print(f"  {prefix} {rel_path} ({size_kb:.1f} KB)")

        print("\n==================================================================")
        print(" Controls: Ctrl+C to exit | Target Rate: <=1Hz | Rule 7/8 Validated")
        print("==================================================================")
        sys.stdout.flush()

    def run(self):
        """Main execution loop."""
        print("[*] Starting edge-ai Extended Log Watcher (Max 1Hz Refresh Rate)...")

        sections = self.config.get("sections", {})

        while True:
            sections_data = {}
            all_current_files = {}

            for sec_key, sec_info in sections.items():
                if self.target_section and sec_key != self.target_section:
                    continue

                if not sec_info.get("enabled", True):
                    continue

                sec_matched = self.scan_section_files(sec_info)
                all_current_files.update(sec_matched)

                sections_data[sec_key] = {
                    "name": sec_info.get("name", sec_key),
                    "files": sec_matched,
                }

            new_files = self.audit_changes(all_current_files)
            if new_files:
                self.update_toml_discovered("auto_discover", new_files)

            self.render_display(sections_data)
            time.sleep(1.0)


def main():
    parser = argparse.ArgumentParser(description="edge-ai Extended Log Watcher")
    parser.add_argument("--config", type=str, default="tools/log_watcher.toml", help="Path to TOML config file")
    parser.add_argument("--section", type=str, default=None, help="Filter to specific section (telemetry, build_logs, agy_sessions)")
    parser.add_argument("--add-path", type=str, action="append", help="Dynamically add path to watch")
    parser.add_argument("--remove-path", type=str, action="append", help="Dynamically remove path from watch")

    args = parser.parse_args()

    watcher = LogWatcher(
        config_path=args.config,
        target_section=args.section,
        add_paths=args.add_path,
        remove_paths=args.remove_path,
    )

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\n[+] Log watcher terminated cleanly.")


if __name__ == "__main__":
    main()
