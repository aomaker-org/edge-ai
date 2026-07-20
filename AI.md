# AI Agent Rules of Engagement & Workspace Guardrails (`AI.md`)

> **Notice to AI Agents:** This file defines the mandatory operational directives, structural invariants, and workspace hygiene rules for all AI/LLM assistants operating within `edge-ai`.

---

## 1. System Topology & Validated Environment

- **Primary Repository:** `edge-ai` (derived from `irislime`).
- **Target OS / Environment:** Ubuntu 24.04 / 26.04 LTS (WSL2 / Linux Native).
- **Build Automation:** GNU Make (`>= 4.3`) root-anchored via `PROJECT_ROOT`.
- **Python Environment Manager:** `uv` / `python3`.
- **Telemetry System:** Append-only AGY logger in `agy/` synchronized via `tools/sync_agy_logs.py`.

---

## 2. Core Rules of Engagement

### Rule 1: Strict Root Directory Hygiene
- Do **NOT** create loose scripts (`.sh`, `.py`), log files (`.log`), zip archives, or temporary notes in the repository root.
- Root contains **ONLY** entrypoint configuration and documentation files:
  `Makefile`, `README.md`, `GETTING_STARTED.md`, `QUICK_START.md`, `AI.md`, `TODO.md`, `.gitignore`.
- All code belongs in `src/`, Make modules in `infra/make/`, utilities in `tools/`, and specs in `docs/`.

### Rule 2: Absolute Root Anchoring (`PROJECT_ROOT`)
- Never hardcode relative directory offsets or assume current working directory in Makefiles or scripts.
- Makefiles must reference `$(PROJECT_ROOT)` exported by the top-level [Makefile](file:///home/fekerr/src/edge-ai/Makefile).

### Rule 3: Append-Only & Idempotent Telemetry
- All AI interaction prompts and responses must be syncable via `make agy-sync`.
- Updating [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md) must be append-only or checkbox update (`[ ]` -> `[x]`). Do not purge historical task records.
- Make targets and python scripts must be idempotent (re-executing yields identical state without errors or duplicated side effects).

### Rule 4: Out-of-Tree Builds & Ephemeral Outputs
- All compilation binaries, object files, intermediate cmake caches, and build logs must be placed into `build/` or `logs/`.
- Never write build artifacts into source trees or track generated binaries in Git.

### Rule 5: Empirical Verification Required
- Never claim a build succeeded, a bug was fixed, or a feature works without executing the exact build/test command and reading the execution output.
- Run `make build` or `make test` to verify changes prior to concluding a turn.

### Rule 6: No Superficial Error Masking
- Never swallow exceptions, return dummy null values, or comment out failing assertions to make tests pass. Trace errors to their root cause.

### Rule 7: Strict Prohibition of Un-documented `/dev/null` Redirections
- **NO piping or redirecting output to `/dev/null`** (`> /dev/null`, `2> /dev/null`, `> /dev/null 2>&1`) unless strictly necessary (e.g. silent command existence checks).
- **Mandatory Inline Comment**: Any necessary `/dev/null` redirection **MUST** include an inline code comment explicitly explaining why the redirection is required.
- **Mandatory Documentation**: Every necessary `/dev/null` redirection **MUST** be registered in [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md).
- **Flagging & Logging**: When any un-documented `/dev/null` redirection is discovered, it must be flagged and appended to [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md) (append-only).

---

## 3. Recommended Workflow for AI Agents

1. **Inspect Tasks**: Check [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md) and current prompt.
2. **Implement Changes**: Scope edits cleanly using standard project paths (`src/`, `infra/`, `tools/`).
3. **Verify**: Run `make build` or `make test`.
4. **Sync Telemetry**: Run `make agy-sync` to ensure interaction steps are captured in `agy/`.
5. **Update Task State**: Mark completed tasks in [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md).
