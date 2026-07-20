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
- [x] Created high-autonomy launch script ([tools/agy-run-20260720.sh](file:///home/fekerr/src/edge-ai/tools/agy-run-20260720.sh)), root symlink `agy-run-20260720.sh`, and `make agy-launch` Makefile target.

### Milestone 2: Core Hardware & Subsystem Migration (Upcoming)
- [x] Port C++ engine build modules from `irislime` into modular makefiles (`infra/make/*.mk`).
- [x] Establish isolated hardware inference validation targets (`make test`).
- [x] Implement `uv` environment dependency management in `pyproject.toml`.
- [x] Configure native Linux build targets and toolchain matrix (`gcc`/`clang`).
- [x] Create GitHub Codespaces `.devcontainer/devcontainer.json` configuration.
- [x] Build Docker containerization image (`Dockerfile`) for isolated edge-ai execution.
- [x] Implement real-time system load monitoring telemetry script to enforce <50% laptop CPU/RAM load limit.

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
- `260720_0827_001` - Created executable launcher script `tools/agy-run-20260720.sh`, root symlink `agy-run-20260720.sh`, and `make agy-launch` target for high-autonomy AGY session startup.
- `260720_0831_001` - Ported hardware acceleration make modules (`base.mk`, `litert.mk`, `openvino.mk`, `sycl.mk`, `vulkan.mk`) from `irislime/derived_components` into `infra/make/`, verified out-of-tree builds with `make build`, enforced Rule 7 (`/dev/null` prohibition & registry) and Rule 8 (`YYMMDD_HHMM_NNN`) timestamping, and synced telemetry with `make agy-sync`.
- `260720_0834_001` - Merged feature branch into `main` (approving initial repo creation commits), created `tools/agy-next-work.sh` launcher script with root symlink `agy-next-work.sh`, and added `make agy-next` target.
- `260720_0841_001` - Created provisioning specifications ([docs/PROVISIONING_NOTES.md](file:///home/fekerr/src/edge-ai/docs/PROVISIONING_NOTES.md)), hardware load throttling & telemetry guidelines ([docs/RESOURCE_THROTTLING_AND_TELEMETRY.md](file:///home/fekerr/src/edge-ai/docs/RESOURCE_THROTTLING_AND_TELEMETRY.md)), and llama.cpp fork necessity audit ([docs/LLAMA_CPP_FORK_AUDIT.md](file:///home/fekerr/src/edge-ai/docs/LLAMA_CPP_FORK_AUDIT.md)). Updated top-level documentation with dual concise/verbose formats and submodule clone instructions.
- `260720_0845_001` - Executed full work cycle: created real-time hardware load & thermal throttling monitor script (`tools/monitor_system_load.py`), native Linux GCC/Clang build targets (`infra/make/linux.mk`), GitHub Codespaces devcontainer (`.devcontainer/devcontainer.json`), Docker containerization (`Dockerfile`, `.dockerignore`), Win11/WSL2 provisioners (`tools/provision.sh`, `tools/host/provision_ps7.ps1`), `pyproject.toml`, registered Rule 7 exceptions `EXC-007`..`EXC-011`, verified out-of-tree builds & telemetry, and synced AGY logs.
- `260720_0926_001` - Created real-time log file tree watcher script (`tools/tree_log_watcher.sh`), added `make watch-logs` target, registered Rule 7 exceptions `EXC-012`..`EXC-015`, and verified live event-driven / polling refresh.
- `260720_0931_001` - Extended log watcher with max 1Hz refresh rate limit (`tools/log_watcher.py`), created TOML configuration specification (`tools/log_watcher.toml`), added sectioned tree displays, auto-discovery log populator, live prompt activity notifications, concise/verbose specification ([docs/LOG_WATCHER_SPECIFICATION.md](file:///home/fekerr/src/edge-ai/docs/LOG_WATCHER_SPECIFICATION.md)), and registered Rule 7 exception `EXC-016`.
- `260720_0932_001` - Established isolated Debug (`build/base_debug`, `logs/debug/`) and extra Telemetry (`build/telemetry_release`, `logs/telemetry/`) out-of-tree build targets (`infra/make/telemetry_debug.mk`), updated `tools/log_watcher.toml`, and launched background matrix compilation.
- `260720_0934_001` - Created test discovery & execution runner (`tools/test_runner_matrix.py`, `make test-all`), executing 41 unit tests under throttled load and saving logs into `logs/tests/`. Built manifest audit engine (`tools/generate_build_manifest.py`, `make manifest-build`) categorizing executables (81), libraries (1711), tests (41), and separated logs (5) into [docs/BUILD_AND_TEST_MANIFEST.md](file:///home/fekerr/src/edge-ai/docs/BUILD_AND_TEST_MANIFEST.md) and `build/build_manifest.json`.
- `260720_0940_001` - Configured VS Code workspace (`.vscode/settings.json`, `tasks.json`, `launch.json`), GitHub Copilot instructions (`.github/copilot-instructions.md`), Google Jules agent configuration (`.jules/config.yaml`, [docs/JULES_AGENT_INTEGRATION.md](file:///home/fekerr/src/edge-ai/docs/JULES_AGENT_INTEGRATION.md)), and instantiated `edge-ai/learning/` domain with master lesson plans (`learning/LESSON_PLANS.md`, `01_*.md`, `02_*.md`, `03_*.md`, `04_*.md`).


