# Architecture Decision Record: Manifest & Scan Data Formats
## `docs/MANIFEST_AND_SCAN_ARCHITECTURE.md`

> **ADR Status**: Active  
> **Decision Date**: `260720_1419_001`  
> **Authors**: fekerr / AGY  
> **Applies To**: `edge-ai`, `irislime` (derived), all downstream forks

---

## 1. Problem Statement

The `edge-ai` project operates across **multiple heterogeneous execution environments** simultaneously:

| Environment | Host | Path Convention | Key Constraints |
| :--- | :--- | :--- | :--- |
| **WSL2 Ubuntu 24/26** | `fekerr-core12` | `/home/fekerr/src/edge-ai` | Native git, Make, Python 3.14 |
| **Linux Native** | `fekerr-core12` | `/home/fekerr/src/edge-ai` | Same path as WSL2, distinct kernel |
| **Windows 11 Native** | `fekerr-core12` | `C:\Users\fekerr\src\edge-ai` | MSVC/Ninja, `\` separators, no `bash` |
| **Docker Container** | any | `/workspace/edge-ai` | Ephemeral, volume-mapped, no host state |
| **GitHub Codespaces** | cloud VM | `/workspaces/edge-ai` | Ephemeral, CI-integrated, cloud path |
| **Remote Dev Server** | TBD | `/home/fekerr/...` | SSH tunnel, possible WSL2 overlay |

Any manifest or scan system that uses a **single shared file** will produce **merge conflicts, path corruption, or silent data loss** when two environments write simultaneously. This document defines the canonical data format decisions and multi-environment strategy to solve this.

---

## 2. Format Candidates — Evaluation Matrix

### 2.1 The Candidate Formats

| Format | Comments | Stdlib (Py 3.11+) | Cross-Plat Path Safe | Human Editable | Delta/Merge | Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **JSON** | No | Yes `json` | Yes (with normalization) | Verbose | Yes | **Primary machine format** |
| **JSONC** | Yes | No (custom parser) | Yes | Yes | Fragile | **Rejected** (see §2.2) |
| **JSONL** | No | Yes `json` line-by-line | Yes | Append-only | Yes | **Primary event stream format** |
| **TOML** | Yes | Yes `tomllib` (3.11+) | Yes | Excellent | Not for large arrays | **Human config files only** |
| **YAML** | Yes | No (`pyyaml` / `ruamel`) | Tabs vs spaces issue | Good | Fragile | **Deferred** (see §2.4) |
| **CSV** | No | Yes `csv` | Yes | Spreadsheet | Append | **Flat telemetry only** (existing) |
| **SQLite** | No | Yes `sqlite3` | Yes | Binary | SQL queries | **Future aggregated catalog** |

---

### 2.2 JSONC — Explicitly Rejected

> [!CAUTION]
> **Do not use JSONC for any machine-generated or machine-consumed data file in `edge-ai`.**

**Reasons for rejection:**

1. **Not a standard.** JSONC is a VS Code convention, not an IETF/ECMA specification. There is no canonical grammar, no RFC, no IANA registration.
2. **No stdlib parser.** Python's `json` module will **reject** JSONC files with a `JSONDecodeError` on the first `//` comment. Every consumer requires a custom stripping pre-processor, creating a fragile bespoke dependency.
3. **Inconsistent tooling.** `jq`, `curl | python3 -m json.tool`, GitHub Actions `fromJSON()`, `cat | node -e "JSON.parse()"` — all fail silently or loudly on JSONC. Cross-environment debugging becomes a parser archaeology exercise.
4. **Comments belong in config, not data.** If a file needs comments, it should be TOML (for human config) or use a `"_comment"` key (for machine data needing embedded metadata). Mixing comment syntax into data is a design smell indicating the file serves two roles.

**Exception:** `.vscode/settings.json`, `devcontainer.json`, `.jules/config.yaml` — third-party tooling conventions we do not control and must accept as-is.

---

### 2.3 TOML — Human Configuration Files Only

**Python 3.11+ ships `tomllib` (read-only) in stdlib.** This system runs Python 3.14, so `tomllib` is available without extra installs. Write support requires `tomli-w` (small, pure Python).

**Use TOML for:**
- `tools/log_watcher.toml` ✅ (already exists — correct choice)
- `tools/scan_config.toml` (future scan include/exclude rules, throttle limits)
- `infra/config/<env>.toml` (future per-environment build overrides)

**Do NOT use TOML for:**
- Machine-generated manifests with large arrays of file objects (TOML array-of-tables syntax is verbose and painful for 1000+ entries).
- Append-only event logs (TOML has no append semantics).

**Example valid TOML scan config:**
```toml
[scan]
schema_version = "1.0"
max_depth = 10
throttle_hz = 0.5

[scan.exclude_dirs]
always = [".git", "build", "logs", "__pycache__", ".venv"]
on_docker = ["irislime/irislime"]

[scan.include_patterns]
source = ["*.py", "*.mk", "*.md", "*.toml", "*.json", "*.sh"]
```

---

### 2.4 YAML — Deferred, Not Recommended for New Data Files

YAML has desirable human-readability but carries significant correctness risks:

- **The Norway Problem**: `NO`, `yes`, `True`, `on`, `off` are parsed as booleans in YAML 1.1 (default for PyYAML). `NOEXIT=OFF` silently becomes `False`. This is a silent data corruption bug.
- **Tab sensitivity**: YAML forbids tab indentation. Cross-environment editors silently produce invalid YAML.
- **No stdlib**: Requires `pyyaml` or `ruamel.yaml`. `pyyaml`'s `yaml.load()` without `Loader=` is a **remote code execution vector** (arbitrary Python object deserialization). Safe usage requires `yaml.safe_load()` everywhere — a rule routinely violated.

**Current YAML usage:** `.jules/config.yaml` (Jules agent tooling convention — accept as-is, do not extend).

**Policy:** No new YAML files shall be created for `edge-ai`-owned data. If a future external tool requires YAML input, generate it programmatically from a TOML or JSON source of truth.

---

### 2.5 JSONL — Append-Only Event Streams

JSON Lines (one JSON object per newline, `.jsonl`) is the correct format for any **append-only log or event stream**:

```jsonl
{"ts":"260720_1413_001","event":"scan_start","env":"wsl2","host":"fekerr-core12"}
{"ts":"260720_1413_002","event":"file_added","path":"tools/new_tool.py","size":1234}
{"ts":"260720_1413_003","event":"scan_complete","files_scanned":391,"duration_ms":142}
```

**Advantages:**
- Each line is independently parseable. A crash mid-write loses only the last partial line.
- `tail -f`, `grep`, `jq` all work line-by-line without loading the entire file into memory.
- Git handles JSONL append-only files gracefully when different environments write to separate files (see §4).
- Python: `json.loads(line)` in a loop. No external library needed.

---

### 2.6 SQLite — Future Aggregated Catalog

For cross-environment aggregation and queryable history:

- **Universal**: ships with Python, available on Win11 (`sqlite3.exe`), WSL2, Docker, Codespaces.
- **ACID**: concurrent reads are safe; WAL journal mode enables concurrent writes from separate processes.
- **Queryable**: `SELECT path, env, MAX(ts) FROM file_state GROUP BY path` is trivial.
- **Not git-friendly**: binary format means no meaningful diffs. Must be treated as a **derived/ephemeral artifact** in `.gitignore`, regenerated from JSONL source-of-truth logs.

---

## 3. Data Type → Format Decision Table

| Data Type | Format | Location | Notes |
| :--- | :--- | :--- | :--- |
| **Human-authored scan/watcher config** | **TOML** | `tools/scan_config.toml` | Comments allowed, human editable |
| **Environment-specific config overrides** | **TOML** | `infra/config/<env>.toml` | Per-env include/exclude rules |
| **Machine-generated file state snapshot (baseline)** | **JSON** | `logs/manifests/state_<env>_<host>.json` | Full walk result; overwritten each run |
| **Delta records (what changed since last scan)** | **JSON** | `logs/manifests/delta_<env>_<host>_<YYMMDD_HHMM_NNN>.json` | One file per run; immutable |
| **Scan event stream (append-only)** | **JSONL** | `logs/scan_events/<env>_<host>.jsonl` | One line per event; never overwritten |
| **Build telemetry (flat metrics)** | **CSV** | `logs/telemetry_builds.csv` | Existing; maintain format |
| **AGY session telemetry** | **JSONL** | `agy/prompts.jsonl`, `agy/sessions/*.jsonl` | Existing; maintain format |
| **Cross-environment aggregated catalog** | **SQLite** | `logs/scan_catalog.db` | Future; not git-tracked |
| **irislime full workspace manifest** | **JSON** | `irislime/irislime_manifest.json` | Existing; add delta awareness |
| **Build asset inventory** | **JSON** | `build/build_manifest.json` | Ephemeral; not git-tracked |
| **Third-party tooling config** | JSONC/YAML | `.vscode/`, `.devcontainer/`, `.jules/` | Accept as-is, do not extend |

---

## 4. Multi-Environment Strategy: Per-Host Scan Files

### 4.1 The Core Problem

If two environments (WSL2 + Docker) both write to `irislime_manifest.json`, you get a **last-write-wins race condition** or a git merge conflict. Neither is acceptable.

### 4.2 Solution: Host Identity Envelope + Per-Environment Files

Every machine-generated scan file carries a **host identity envelope** and is written to an **environment-namespaced path**:

```
logs/manifests/
├── state_wsl2_fekerr-core12.json               <- WSL2 baseline (overwritten each run)
├── state_linux_fekerr-core12.json              <- Linux native baseline
├── state_docker_edge-ai-dev.json               <- Docker container baseline
├── state_codespaces_bright-spoon-abc.json      <- Codespaces baseline
├── delta_wsl2_fekerr-core12_260720_1413_001.json    <- Immutable delta record
├── delta_docker_edge-ai-dev_260720_1415_001.json
└── ...

logs/scan_events/
├── wsl2_fekerr-core12.jsonl                    <- WSL2 event stream (append-only)
├── docker_edge-ai-dev.jsonl                    <- Docker event stream
└── ...
```

### 4.3 Host Identity Schema (required in every scan file header)

```json
{
  "scan_metadata": {
    "schema_version": "1.0",
    "rule8_timestamp": "260720_1413_001",
    "iso_timestamp": "2026-07-20T14:13:42-07:00",
    "host": {
      "hostname": "fekerr-core12",
      "env_type": "wsl2",
      "os": "Linux",
      "os_version": "6.6.87.2-microsoft-standard-WSL2",
      "python_version": "3.14.4",
      "container_id": null,
      "codespace_name": null,
      "project_root": "/home/fekerr/src/edge-ai",
      "git_branch": "feat/work-cycle-260720_1407",
      "git_commit": "4ed877c"
    }
  }
}
```

**`env_type` canonical values:**

| Value | Meaning |
| :--- | :--- |
| `wsl2` | WSL2 Ubuntu shell |
| `linux` | Linux native (bare metal or VM) |
| `win11` | Windows 11 native (MSVC/PowerShell) |
| `docker` | Docker container |
| `codespaces` | GitHub Codespaces |
| `ci` | GitHub Actions / CI runner |
| `remote` | Remote SSH dev server |

### 4.4 Environment Detection (Python)

```python
import os, platform

def detect_env_type() -> str:
    """Detect canonical env_type for the current execution environment."""
    if os.environ.get("CODESPACE_NAME"):
        return "codespaces"
    if os.path.exists("/.dockerenv") or os.environ.get("container"):
        return "docker"
    if os.environ.get("GITHUB_ACTIONS"):
        return "ci"
    if platform.system() == "Windows":
        return "win11"
    try:
        with open("/proc/version") as f:
            if "microsoft" in f.read().lower():
                return "wsl2"
    except FileNotFoundError:
        pass
    return "linux"
```

---

## 5. Delta Scan Architecture

### 5.1 Three-File Design Per Environment

```
state_<env>_<host>.json          <- Rolling baseline. Overwritten each run.
delta_<env>_<host>_<TS>.json     <- Immutable delta since last baseline.
scan_events/<env>_<host>.jsonl   <- Append-only event log (one line per scan).
```

### 5.2 Delta Scan Algorithm (pseudocode for `tools/scan_workspace.py`)

```python
def run_delta_scan(project_root, env_type, hostname):
    baseline_path = f"logs/manifests/state_{env_type}_{hostname}.json"

    # 1. Load previous baseline (empty on first run)
    prev_state = load_json(baseline_path) if exists(baseline_path) else {}
    prev_files = {f["path"]: f for f in prev_state.get("files", [])}

    # 2. Scan current filesystem state
    curr_files = walk_and_classify(project_root)
    # -> {path: {size_bytes, mtime, sha256_prefix, category}}

    # 3. Compute delta
    added    = [f for f in curr_files if f not in prev_files]
    removed  = [f for f in prev_files if f not in curr_files]
    modified = [f for f in curr_files
                if f in prev_files
                and (curr_files[f]["mtime"] != prev_files[f].get("mtime")
                     or curr_files[f]["size_bytes"] != prev_files[f].get("size_bytes"))]

    # 4. Write immutable delta record (one per run, never overwritten)
    ts = rule8_timestamp()
    delta = {
        "scan_metadata": host_identity_envelope(env_type, hostname, ts),
        "previous_baseline_ts": prev_state.get("scan_metadata", {}).get("rule8_timestamp", "none"),
        "delta": {"added": added, "removed": removed, "modified": modified},
        "summary": {"added": len(added), "removed": len(removed), "modified": len(modified)}
    }
    write_json(f"logs/manifests/delta_{env_type}_{hostname}_{ts}.json", delta)

    # 5. Append one-line summary to JSONL event stream
    append_jsonl(f"logs/scan_events/{env_type}_{hostname}.jsonl", {
        "ts": ts, "event": "scan_complete",
        "prev_ts": delta["previous_baseline_ts"],
        **delta["summary"]
    })

    # 6. Overwrite baseline with new current full state
    write_json(baseline_path, {
        "scan_metadata": host_identity_envelope(env_type, hostname, ts),
        "files": list(curr_files.values())
    })

    return delta
```

### 5.3 Agent Query — "What Changed Since Last Scan?"

An agent starting a new session can answer this instantly, without a re-scan:

```bash
# Most recent delta for current environment:
ls -t logs/manifests/delta_wsl2_fekerr-core12_*.json | head -1 | xargs python3 -m json.tool

# Cross-environment summary table:
for f in logs/manifests/delta_*.json; do
    python3 -c "
import json; d = json.load(open('$f'))
m = d['scan_metadata']; s = d['summary']
print(f\"{m['rule8_timestamp']} | {m['host']['env_type']:<12} | +{s['added']} -{s['removed']} ~{s['modified']}\")"
done
```

---

## 6. Path Normalization — Cross-Platform Safety

> [!WARNING]
> Windows paths (`C:\Users\fekerr\src`) stored raw in JSON manifests will **break** `os.path.exists()` on Linux/WSL2 and vice versa. All stored paths MUST be normalized.

### 6.1 Canonical Path Rules

1. **Always use forward slashes** (`/`) in stored paths, even on Windows.
2. **Store paths relative to `project_root`** — not absolute. This makes manifests portable across all mount points.
3. **Strip drive letters**: `C:/Users/fekerr/src/edge-ai/tools/foo.py` → `tools/foo.py`.
4. **Docker volume paths**: `/workspace/edge-ai/tools/foo.py` → `tools/foo.py`.
5. **Codespaces paths**: `/workspaces/edge-ai/tools/foo.py` → `tools/foo.py`.

```python
def normalize_path(abs_path: str, project_root: str) -> str:
    """Return forward-slash relative path from project_root."""
    import os
    rel = os.path.relpath(abs_path, project_root)
    return rel.replace("\\", "/")  # Windows backslash -> forward slash
```

---

## 7. .gitignore Policy for Scan Files

```gitignore
# Ephemeral per-host scan baselines (regenerated; not shared via git)
logs/manifests/state_*.json
logs/scan_events/*.jsonl
logs/scan_catalog.db

# Delta records: optionally commit at milestone boundaries for audit trail.
# Recommended: keep in .gitignore during active development; commit at milestones
# via 'make manifest-delta-commit'. Uncomment to track all deltas in git:
# !logs/manifests/delta_*.json
```

> [!NOTE]
> **Delta files carry the most value for cross-session continuity.** At milestone commit boundaries, stage and commit `delta_*.json` files alongside `TODO.md` entries. This gives agents (and humans) a machine-readable answer to "what changed?" without requiring a full re-scan.

---

## 8. Make Targets Roadmap

| Target | Description | Status |
| :--- | :--- | :--- |
| `make manifest-gen` | Full rescan of irislime workspace, emit JSON+MD | Existing |
| `make manifest-build` | Full rescan of build/logs assets, emit JSON+MD | Existing |
| `make scan` | Delta scan for current env; write delta JSON + JSONL event | **Planned** |
| `make scan-status` | Print most recent delta summary per known environment | **Planned** |
| `make manifest-delta` | Alias for `make scan`; human-readable diff since last baseline | **Planned** |
| `make manifest-delta-commit` | Stage + git commit latest delta files with Rule 8 timestamp | **Planned** |

---

## 9. Summary of Decisions

| Decision | Choice | Rationale |
| :--- | :--- | :--- |
| Machine-generated snapshots | **JSON** | stdlib, universal tooling, no parser surprises |
| Human-authored config | **TOML** | comments, readable, stdlib in Python 3.11+ |
| Append-only event logs | **JSONL** | append-safe, crash-resilient, line-addressable |
| Flat build telemetry | **CSV** | existing, simple, spreadsheet-compatible |
| Cross-env aggregation (future) | **SQLite** | queryable, ACID, not git-tracked |
| JSONC | **Rejected** | no stdlib parser, not a standard, tooling fragility |
| YAML | **Deferred** | Norway problem, no stdlib, security footgun |
| Multi-env conflict avoidance | **Per-host files** | no merge conflicts, full audit trail |
| Path storage | **Relative, forward-slash** | cross-platform portable |
| Delta baseline | **Overwrite** (state file) | always reflects current truth |
| Delta event records | **Immutable** (new file per run) | audit trail, no data loss |

---

*This document is append-only per Rule 3 (AI agents may update decision table rows and roadmap status; human maintainers hold authority to reorganize sections).*
