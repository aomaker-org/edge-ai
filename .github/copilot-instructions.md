# GitHub Copilot Instructions & Task Sharing Directives (`copilot-instructions.md`)

Welcome GitHub Copilot! This repository (**`edge-ai`**) is an optimized edge AI development and localized SLM runtime acceleration platform derived from `irislime`.

When generating code, creating pull requests, or assisting developers in VS Code or on GitHub, you **MUST** follow these mandatory workspace rules:

---

## 🏛️ Core Workspace Guardrails

1. **Rule 1: Strict Root Directory Hygiene**
   - Do **NOT** create loose scripts (`.sh`, `.py`), log files (`.log`), zip archives, or temporary notes in the root directory.
   - Root contains **ONLY**: `Makefile`, `README.md`, `GETTING_STARTED.md`, `QUICK_START.md`, `AI.md`, `TODO.md`, `.gitignore`, `pyproject.toml`, `Dockerfile`, `.dockerignore`.
   - Place all C++/Python code in `src/`, Make modules in `infra/make/`, utilities in `tools/`, specs in `docs/`, learning in `learning/`.

2. **Rule 2: Absolute Root Anchoring (`PROJECT_ROOT`)**
   - Makefiles and scripts must resolve paths dynamically relative to `$(PROJECT_ROOT)` or `PROJECT_ROOT="${PROJECT_ROOT:-...}"`.

3. **Rule 4: Out-of-Tree Builds & Ephemeral Outputs**
   - All build outputs, compilation object files, and logs must be placed into `build/` (e.g. `build/base_release`, `build/base_debug`, `build/linux_gcc`) or `logs/`.
   - Never generate build output inside source submodules (`irislime/irislime/`).

4. **Rule 7: Strict Prohibition of Un-documented `/dev/null` Redirections**
   - **NO piping or redirecting output to `/dev/null`** (`> /dev/null`, `2> /dev/null`, `> /dev/null 2>&1`) unless strictly necessary (e.g., silent binary probes).
   - **Mandatory Inline Comment**: Include `# NECESSARY NULL PIPE: <rationale>`.
   - **Mandatory Documentation**: Register any exception in [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md).

5. **Rule 8: Mandatory `YYMMDD_HHMM_NNN` Timestamp Standard**
   - All session logs, build output journals, and timestamped task ledger entries must use the `YYMMDD_HHMM_NNN` timestamp format.

---

## 🛠️ Preferred Makefile Commands for Task Completion

- `make build`: Prepare and execute base CPU build out-of-tree.
- `make build-debug`: Execute isolated Debug build in `build/base_debug` and `logs/debug/`.
- `make test-all`: Discover and execute 41 unit tests under throttled load, saving logs to `logs/tests/`.
- `make watch-logs`: Launch anti-flicker 1Hz log watcher visualizer.
- `make manifest-build`: Audit built executables, libraries, tests, and logs into `docs/BUILD_AND_TEST_MANIFEST.md`.
- `make agy-sync`: Idempotently sync session telemetry to `agy/`.

---

## 🤝 Task Sharing Interop: Copilot & Google Jules (`jules.google.com`)

When creating task descriptions or handover notes for peer AI agents (such as Google Jules or AGY subagents):
- Always cite exact line numbers using Markdown links (`[filename](file:///path/to/file#L10-L20)`).
- Include empirical command output verification logs.
- Reference active task status in [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md).
