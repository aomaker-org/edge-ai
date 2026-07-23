# AI Agent Rules of Engagement & Workspace Guardrails (AI.md)
<!-- file: AI.md -->

Notice to AI Agents: This file defines mandatory operational directives,
file-header standards, line wrapping guidelines, multi-agent boundaries, and
workspace hygiene for all assistants operating within edge-ai (Gemini, Jules,
Copilot, AGY).

---

## 1. System Topology & Validated Environment

- Primary Repository: edge-ai (derived from irislime)
- Target OS / Environment: Ubuntu 24.04 / 26.04 LTS (WSL2 / Linux Native)
- Build Automation: GNU Make (>= 4.3) root-anchored via PROJECT_ROOT
- Python Environment Manager: uv / python3
- Telemetry System: Append-only AGY logger in agy/ synchronized via
  tools/sync_agy_logs.py

---

## 2. Multi-Agent Co-Existence Boundaries

| Agent | Scope & Role | Allowed Workspace Artifacts |
| :--- | :--- | :--- |
| Gemini (Web UI) | Architectural design, refactoring, AI.md governance, context integration. | gemini/ |
| Jules (Google) | Asynchronous feature tasks, automated PR generation, background VM builds. | .jules/ (Git ignored) |
| AGY (CLI Tool) | Local telemetry logging, command execution tracking, task sequencing. | agy/, tools/agy-*.sh |
| Copilot (IDE) | Real-time inline completions and localized edits in VS Code. | Standard Git tracking |

---

## 3. Allowed Root Exceptions (Rule 1 Overrides)

The following root-level entries are explicitly permitted and must NOT be
flagged as hygiene violations:

- OS & Shell Configs: config_win11_bash, config_win11_bat.bat,
  config_win11_ps7.ps1, provision_win11.ps1
- Launcher Symlinks: agy-run-20260720.sh, agy-next-work.sh, new-agy.sh
- Sub-projects / External Trees: irislime/, deps/, learning/, devices/, web/
- Agent Workspaces: gemini/, .jules/, ai-log-diff/, user/, scratch/
- Project Metadata: manifest.json, pyproject.toml, Dockerfile, .dockerignore,
  CMakeLists.txt, CMakePresets.json, .devcontainer/

---

## 4. Line Wrapping Standard (80 / 120 Columns)

- Text & Markdown Files: Attempt to wrap prose, documentation, and comments
  to 80 columns (up to a hard maximum of 120 columns) to ensure clean command-line
  diffs and readable terminal rendering.
- Source Code: Follow standard formatting conventions per language, keeping
  comments and code lines within 80-120 columns where feasible.

---

## 5. Mandatory File Header & Footer Standard

To prevent ambiguity, truncation, or misparsing during AI context passing and
multi-agent file syncs, all text files in the repository MUST follow these
framing rules:

### A. File Headers
- Every text file (when language syntax permits) MUST begin with a comment
  header containing at least the relative file path.
- The comment header MUST appear immediately after any mandatory shebang
  (#!/usr/bin/env ...) or shebang trampoline logic.
- Shebang / Trampoline Rules: Any "shebang magic" or trampoline logic (e.g.
  re-executing under bash or polyglot launchers) MUST include an inline comment
  documenting its exact operation and purpose.

### B. File Footers
- Every text file MUST conclude with an explicit end-of-file comment marker
  matching the pattern:
  # file <relative/path/filename> ends (or language-appropriate comment
  syntax).

---

## 6. Heredoc & Context Transfer Protocols

- Quote Heredoc Delimiters: When generating shell scripts or commands that
  write multi-line files or Markdown via heredocs, ALWAYS quote the delimiter
  (cat << 'EOF' > file.txt). Unquoted delimiters cause shell evaluation of
  backticks and variables, breaking text content.
- Escape Fences: Avoid raw triple-backticks inside raw LLM transfers if passing
  nested markdown snippets; use ASCII text or safe escapes.

---

## 7. Core Rules of Engagement

- Rule 1: Strict Root Directory Hygiene (only permitted exceptions in Section 3
  allowed in root).
- Rule 2: Absolute Root Anchoring (reference $(PROJECT_ROOT) in Makefiles and
  scripts).
- Rule 3: Append-Only Telemetry (sync via make agy-sync; TODO.md updates are
  append-only).
- Rule 4: Out-of-Tree Builds (compilation artifacts go strictly into build/ or
  logs/).
- Rule 5: Empirical Verification Required (always execute test/build commands
  before claiming completion).

<!-- file AI.md ends -->
