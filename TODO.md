# `edge-ai` Task Tracking Ledger (`TODO.md`)

> **[!] OPERATIONAL POLICY FOR AI AGENTS:**  
> This ledger operates under an **Append-Only** rule for automated/AI agents.  
> - **AI Agents**: You may ONLY append new task sections or update task check states (`[ ]` -> `[x]`). You must NEVER delete, rewrite, or clear past task history.  
> - **Human Agents**: Human maintainers hold sole authority to reorganize, edit, or purge historical tasks.

---

## 📌 Active Development Milestones

### Milestone 1: Repository Foundation & Core Hygiene
- [x] Initialized Git repository and set remote to `git@github.com:aomaker-org/edge-ai.git`.
- [x] Pushed baseline `main` branch to remote.
- [x] Implemented root-anchored [Makefile](file:///home/fekerr/src/edge-ai/Makefile) and [infra/make/base.mk](file:///home/fekerr/src/edge-ai/infra/make/base.mk).
- [x] Created `agy/` directory structure and idempotent log sync script ([tools/sync_agy_logs.py](file:///home/fekerr/src/edge-ai/tools/sync_agy_logs.py)).
- [x] Established core workspace documentation ([README.md](file:///home/fekerr/src/edge-ai/README.md), [GETTING_STARTED.md](file:///home/fekerr/src/edge-ai/GETTING_STARTED.md), [QUICK_START.md](file:///home/fekerr/src/edge-ai/QUICK_START.md), [AI.md](file:///home/fekerr/src/edge-ai/AI.md), [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md)).
- [x] Enforced Rule 7 (NO PIPE TO NULL unless necessary, commented, and registered) in [AI.md](file:///home/fekerr/src/edge-ai/AI.md) and established [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md).

### Milestone 2: Core Hardware & Subsystem Migration (Upcoming)
- [ ] Port C++ engine build modules from `irislime` into modular makefiles (`infra/make/*.mk`).
- [ ] Establish isolated hardware inference validation targets (`make test`).
- [ ] Implement `uv` environment dependency management in `pyproject.toml`.

---

## 📜 Historical Task Log (Append-Only Section)

*Timestamped log of completed tasks will be appended below as development progresses.*

- `2026-07-20 08:00` - Initialized repository structure, dynamic Make anchor, and `agy` telemetry pipeline.
- `2026-07-20 08:04` - Created `docs/` directory and established `/dev/null` redirection policy registry ([docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md)). Audited codebase (0 `/dev/null` redirections currently present).

