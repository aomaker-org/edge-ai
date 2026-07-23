# Extended Log Watcher & Real-Time Telemetry Specification (`LOG_WATCHER_SPECIFICATION.md`)

This specification defines the design, configuration architecture, rate-limiting algorithms, and operational directives for the `edge-ai` interactive log watcher service.

---

## ⚡ 1. Concise Specification & Quick Start (TL;DR)

### Overview
The extended log watcher (`tools/log_watcher.py`) provides real-time, sectioned visual tracking of log files (`.log`, `.csv`, `.jsonl`) across `logs/`, `build/`, and `agy/` directories. It enforces a strict **1Hz maximum screen update frequency** (no terminal flicker), reads configuration from a structured TOML file ([tools/log_watcher.toml](file:///home/fekerr/src/edge-ai/tools/log_watcher.toml)), auto-discovers newly generated log assets, and prompts live on-screen notifications when files are created or appended.

### Key Commands

```bash
# 1. Run default sectioned log watcher via Make target (max 1Hz refresh rate)
make watch-logs

# 2. Run Python log watcher with auto-discovery and TOML config synchronization
python3 tools/log_watcher.py --config tools/log_watcher.toml

# 3. View specific section only (e.g. telemetry, build_logs, agy_sessions)
python3 tools/log_watcher.py --section telemetry

# 4. Add or subtract watching targets dynamically
python3 tools/log_watcher.py --add-path /path/to/custom_logs --pattern "*.log"
```

---

## 🏛️ 2. Verbose Architectural Specification

### A. Rate-Limiting & Anti-Flicker Algorithm (1Hz Max Refresh Rate)
To prevent terminal screen flickering during rapid concurrent file writes (e.g., high-frequency model inference logs or parallel make builds), the monitor implements a **1-second token-bucket rate limiter** (`max_refresh_hz = 1.0`):

$$\Delta t_{\text{render}} = \max\left(t_{\text{current}} - t_{\text{last\_render}}, 1.0\text{ sec}\right)$$

1. **Event Capture**: File modifications, creations, and byte-size growth are detected continuously.
2. **Debounce Buffer**: Event notifications are queued in an internal buffer.
3. **Throttled Render Pass**: Screen re-rendering (`printf '\033[2J\033[H'`) is executed **at most once per second**. If multiple file writes occur within 100ms, they are batched into a single 1Hz render update.

---

### B. TOML Configuration File Schema (`tools/log_watcher.toml`)

The configuration file follows standard TOML syntax and is automatically instantiated with discovered log files if absent:

```toml
[general]
max_refresh_hz = 1.0
scan_interval_sec = 1.0
auto_discover = true
timestamp_format = "%y%m%d_%H%M_%S"

[sections.telemetry]
name = "Hardware & Inference Telemetry Logs"
paths = ["logs"]
patterns = ["*.jsonl", "*.csv"]
enabled = true

[sections.build_logs]
name = "Out-of-Tree Build & Compiler Logs"
paths = ["build"]
patterns = ["*.log"]
enabled = true

[sections.agy_sessions]
name = "AI Agent Telemetry Sessions"
paths = ["agy"]
patterns = ["*.jsonl", "*.md"]
enabled = true

[discovered_files]
# Automatically populated by log_watcher.py during auto-discovery scans
```

---

### C. Live Prompt Notifications & Interactive Section Management

- **`[NEW FILE]` Alerts**: Displayed in bright green when a new log file is instantiated on disk.
- **`[APPENDED]` Alerts**: Displayed in cyan with byte delta size (+N bytes) when log records are appended.
- **Dynamic Section Filtering**: Allows users to include (`--add-path`) or exclude (`--remove-path`) directory trees or sections from the `tree -f` view without stopping the process.

---

## 🔒 3. Compliance & Workspace Guardrails

- **Rule 1 (Root Hygiene)**: Script stored in `tools/log_watcher.py`, configuration in `tools/log_watcher.toml`, documentation in `docs/LOG_WATCHER_SPECIFICATION.md`.
- **Rule 7 (`/dev/null` Registry)**: Any shell wrapper invocations suppressing stream noise include inline `# NECESSARY NULL PIPE:` comments and are registered in [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md).
- **Rule 8 Timestamping**: Log watcher outputs display `YYMMDD_HHMM_NNN` timestamps on every render pass.
