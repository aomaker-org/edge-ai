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
- [x] Defined and enforced Rule 8 (`YYMMDD_HHMM_NNN` timestamping standard) in [docs/TIMESTAMPING_STANDARD.md](file:///home/fekerr/src/edge-ai/docs/TIMESTAMPING_STANDARD.md) and updated [tools/sync_agy_logs.py](file:///home/fekerr/src/edge-ai/tools/sync_agy_logs.py).
- [x] Created `irislime/derived_components/` header domain ([irislime/README.md](file:///home/fekerr/src/edge-ai/irislime/README.md)) and documented full `git clone --recurse-submodules` & `git submodule update --init --recursive` commands in [README.md](file:///home/fekerr/src/edge-ai/README.md), [GETTING_STARTED.md](file:///home/fekerr/src/edge-ai/GETTING_STARTED.md), and [QUICK_START.md](file:///home/fekerr/src/edge-ai/QUICK_START.md).
- [x] Generated full file manifest of `irislime` ([irislime/irislime_manifest.md](file:///home/fekerr/src/edge-ai/irislime/irislime_manifest.md) & [`irislime_manifest.json`](file:///home/fekerr/src/edge-ai/irislime/irislime_manifest.json)) categorizing `source_files`, `built_files`, and `log_files`.
- [x] Created `ai-log-diff/` subproject ([ai-log-diff/README.md](file:///home/fekerr/src/edge-ai/ai-log-diff/README.md)), research paper ([ai-log-diff/docs/RESEARCH_AND_SPECIFICATION.md](file:///home/fekerr/src/edge-ai/ai-log-diff/docs/RESEARCH_AND_SPECIFICATION.md)), semantic log differ tool ([ai-log-diff/tools/semantic_log_differ.py](file:///home/fekerr/src/edge-ai/ai-log-diff/tools/semantic_log_differ.py)), and example logs.
- [x] Established `edge-ai/web/` domain ([web/README.md](file:///home/fekerr/src/edge-ai/web/README.md)) detailing dashboard architecture via GitHub Pages/Actions/API ([web/DASHBOARD_ARCHITECTURE.md](file:///home/fekerr/src/edge-ai/web/DASHBOARD_ARCHITECTURE.md)), infrastructure & free-tier hosting analysis ([web/INFRASTRUCTURE_AND_HOSTING.md](file:///home/fekerr/src/edge-ai/web/INFRASTRUCTURE_AND_HOSTING.md)), WireGuard/Mosquitto telemetry pipeline ([web/NETWORK_AND_TELEMETRY_PIPELINE.md](file:///home/fekerr/src/edge-ai/web/NETWORK_AND_TELEMETRY_PIPELINE.md)), and `aomaker.org` / `jason-lab.dev` integration plan ([web/AOMAKER_INTEGRATION_PLAN.md](file:///home/fekerr/src/edge-ai/web/AOMAKER_INTEGRATION_PLAN.md)).
- [x] Added `irislime/irislime` as a Git submodule tracking `git@github.com:aomaker-org/irislime.git` and generated deep review suite ([irislime/docs/review_summary.md](file:///home/fekerr/src/edge-ai/irislime/docs/review_summary.md)) auditing all 111 commits ([review_commit_history.md](file:///home/fekerr/src/edge-ai/irislime/docs/review_commit_history.md)), subsystem architecture ([review_architectural_audit.md](file:///home/fekerr/src/edge-ai/irislime/docs/review_architectural_audit.md)), and technical debt fixes ([review_technical_debt_and_improvements.md](file:///home/fekerr/src/edge-ai/irislime/docs/review_technical_debt_and_improvements.md)).

### Milestone 2: Core Hardware & Subsystem Migration (Upcoming)
- [ ] Port C++ engine build modules from `irislime` into modular makefiles (`infra/make/*.mk`).
- [ ] Establish isolated hardware inference validation targets (`make test`).
- [ ] Implement `uv` environment dependency management in `pyproject.toml`.

---

## 📜 Historical Task Log (Append-Only Section)

*Timestamped log of completed tasks will be appended below as development progresses.*

- `2026-07-20 08:00` - Initialized repository structure, dynamic Make anchor, and `agy` telemetry pipeline.
- `2026-07-20 08:04` - Created `docs/` directory and established `/dev/null` redirection policy registry ([docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md)). Audited codebase (0 `/dev/null` redirections currently present).
- `260720_0806_001` - Established `YYMMDD_HHMM_NNN` timestamping standard specification ([docs/TIMESTAMPING_STANDARD.md](file:///home/fekerr/src/edge-ai/docs/TIMESTAMPING_STANDARD.md)) with sequence override support (`--seq-start`).
- `260720_0808_001` - Created `irislime/derived_components/` header domain and updated [README.md](file:///home/fekerr/src/edge-ai/README.md), [GETTING_STARTED.md](file:///home/fekerr/src/edge-ai/GETTING_STARTED.md), and [QUICK_START.md](file:///home/fekerr/src/edge-ai/QUICK_START.md) with full Git clone submodule command lines (`--recurse-submodules` and `git submodule update --init --recursive`).
- `260720_0812_001` - Generated `irislime_manifest.md` & `irislime_manifest.json` classifying 391 files into `source_files`, `built_files`, and `log_files`. Established `ai-log-diff/` subproject framework, research specification, semantic differ tool, example logs, and `make ai-log-diff-demo` target.
- `260720_0818_001` - Created `edge-ai/web/` architecture domain detailing GitHub Pages/Actions dashboard, OCI/GCP free tier hosting analysis, WireGuard & Mosquitto MQTT network overlay, and `aomaker.org` / `jason-lab.dev` integration plan.
- `260720_0823_001` - Added `irislime/irislime` Git submodule and generated deep review suite (`review_commit_history.md`, `review_architectural_audit.md`, `review_technical_debt_and_improvements.md`, `review_summary.md`) auditing all 111 commits and technical debt resolutions.






