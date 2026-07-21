# Developer Tips & Best Practices (`DEVELOPER_TIPS_AND_BEST_PRACTICES.md`)

This guide provides both **Concise (TL;DR)** and **Verbose (Architectural)** tips and best practices for developing, testing, and maintaining `edge-ai`.

---

## ⚡ 1. Concise Quick-Reference Tips (TL;DR)

| Category | Best Practice / Pro-Tip | Key Command / File |
| :--- | :--- | :--- |
| 🧹 **Root Directory Hygiene** | Keep root clean! Code in `src/`, make modules in `infra/make/`, utilities in `tools/` | Rule 1 in [AI.md](file:///home/fekerr/src/edge-ai/AI.md) |
| 📁 **Out-of-Tree Builds** | Never build inside source trees; land all binaries in `build/` and logs in `logs/` | `make build`, `make build-debug` |
| 📊 **Real-Time Log Watching** | Avoid terminal flicker by using the 1Hz rate-limited visualizer | `make watch-logs` |
| 🧪 **Throttled Test Runner** | Execute unit tests under <50% laptop CPU load to keep machine cool and quiet | `make test-all` |
| 📋 **Build Asset Manifest** | Audit all executables, libraries, test binaries, and separated logs across sections | `make manifest-build` |
| 🤖 **Multi-Agent Handoff** | Sync conversation prompts into `agy/` before handoff to peer AI agents | `make agy-sync` |
| 🪟 **Win11 / WSL Interop** | Avoid UNC path crashes in `cmd.exe` by using `config_win11.bat` or `pwsh.exe` | [docs/WINDOWS_TERMINAL_SETTINGS_REVIEW.md](file:///home/fekerr/src/edge-ai/docs/WINDOWS_TERMINAL_SETTINGS_REVIEW.md) |

---

## 🏛️ 2. Verbose Architectural Tips & Guidelines

### Tip 1: Out-of-Tree Compilation & Clean Submodule Boundaries
Source submodules (`irislime/irislime/llama.cpp`) should remain strictly pristine. Always invoke out-of-tree CMake targets (`build/base_release`, `build/base_debug`, `build/telemetry_release`, `build/linux_gcc`). Never generate `.o` files or CMake caches inside submodules.

### Tip 2: Rule 7 `/dev/null` Exception Protocol
Never pipe command output to `/dev/null` silently. Include inline comment `# NECESSARY NULL PIPE: <rationale>` and register exceptions in [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md).

### Tip 3: Rule 8 `YYMMDD_HHMM_NNN` Timestamp Standard
All session logs, task ledgers in [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md), and git commit messages must include the standard `YYMMDD_HHMM_NNN` timestamp format.

### Tip 4: Submodule Git URL Rewriting in Headless Environments
In headless non-SSH containers (Codespaces, Docker, CI/CD), run:
```bash
git config --global url."https://github.com/".insteadOf "git@github.com:"
```

### Tip 5: Multi-Agent Handoff Workflow (Copilot <-> Jules <-> AGY)
Always run `make manifest-build` and `make agy-sync` prior to ending a turn or passing work to a peer agent. The incoming agent will read `docs/AGENT_INGESTION_AND_WORK_UNDERSTANDING.md` and generate an ingestion report.
