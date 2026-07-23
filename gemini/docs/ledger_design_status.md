# Edge-AI Telemetry & Ledger Framework: Design Specification

**Status:** Active / Iterative Phase  
**Version:** 1.0.0  

## Overview
The Edge-AI telemetry framework bridges raw Git repository state with offsite artifact ledgers, local metadata scans, and human-readable context graphs. It is designed around a Git-style triage model: running the utility by default highlights immediate "work to do," while switches unlock deep inspection.

---

## Core Architecture

### 1. Unified Utility (`gemini/tools/ledger.py`)
- **Git-Style Triage:** By default, checks Git status alongside local capture folders and manifest states, outputting a clear "Work to Do / Action Items" summary.
- **Precedence Hierarchy:** Configuration state follows a strict waterfall: **CLI Flags > Environment Variables (`LEDGER_ONLY`) > Persistent Config (`gemini/ledgers/.config.ledger`)**.
- **Help & Examples:** Built-in `-h` / `--help` with explicit usage examples.

### 2. Manifest & Point-In-Time Indexing (`manifest.json`)
- `.gitignore` protects local workspace indexes (`manifest.json`) from polluting Git.
- Provides lightning-fast local metadata lookup across 4,000+ files (SHA-256 hashes, sizes, modification timestamps).
- Scheduled for offsite archival sync to `gdrive:transfer/edge-ai/manifest-archive/` via `ledger.py`.

### 3. Advanced Design Concepts (Backlog & Future Roadmap)
- **Append-Only Journal & Compaction:** Mimicking Write-Ahead Logs (WAL) and Log-Structured Merge (LSM) trees. High-frequency changes append to a lightweight delta log; a background "slow-motion" compaction process consolidates them into a clean snapshot YAML ledger.
- **Recursive Documentation Graphs (`documentation_refs`):** Associating raw file binaries and source code with multiple documentation targets (files or folders). Guardrails include strict graph cycle detection to prevent infinite recursion.
- **Deterministic Sorting:** All ledger catalogs and logs are deterministically sorted by primary paths and chronological timestamps to eliminate noisy Git diffs.

---

## Backlog Reference
This design specification is tracked under backlog item `TODO-004` (see `gemini/backlog.yaml`).
