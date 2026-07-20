# `edge-ai` Master Lesson Plans & Educational Roadmap (`LESSON_PLANS.md`)

This document presents both **Concise (TL;DR)** and **Verbose (Architectural)** lesson plans for mastering edge AI engineering, modular make builds, hardware resource throttling, and autonomous AI agent collaboration.

---

## ⚡ 1. Concise Lesson Plan Matrix (TL;DR)

| Stage / Module | Primary Focus | Practical Hands-On Exercise | Key Deliverable |
| :--- | :--- | :--- | :--- |
| **Stage 1: Foundation** | Root Hygiene & Make Anchoring | Run `make help`, verify `PROJECT_ROOT`, update `TODO.md` | Clean root environment |
| **Stage 2: Out-of-Tree Builds** | Git Submodules & Out-of-Tree CMake | Run `git submodule update`, `make build`, `make build-debug` | Isolated `build/` & `logs/` outputs |
| **Stage 3: Acceleration & Telemetry** | Hardware Backends & Throttling | Run `make watch-logs`, `make test-all`, `make monitor-load` | <50% CPU load compliance |
| **Stage 4: Agent Interop** | Copilot & Google Jules Integration | Configure `.vscode/`, `.github/`, `.jules/`, run `make agy-sync` | Multi-agent task sharing |

---

## 🏛️ 2. Verbose Curriculum & Lesson Plan Details

### Module 1: Foundation, Root Hygiene & Operational Invariants
- **Objective**: Understand repository structure, root directory hygiene (Rule 1), dynamic root anchoring (Rule 2), Rule 7 (`/dev/null` prohibition & registry), and Rule 8 (`YYMMDD_HHMM_NNN` timestamping).
- **Core Concepts**:
  1. Root directory contains only entrypoints (`Makefile`, `README.md`, `GETTING_STARTED.md`, `QUICK_START.md`, `AI.md`, `TODO.md`, `.gitignore`, `pyproject.toml`, `Dockerfile`, `.dockerignore`).
  2. Makefiles anchor paths dynamically via `PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))`.
  3. Every `/dev/null` redirection must include `# NECESSARY NULL PIPE:` and be registered in [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md).
- **Verification Exercise**: Run `make help` and verify `PROJECT_ROOT` output.

---

### Module 2: Out-of-Tree Build Matrices & Submodule Management
- **Objective**: Learn Git submodule initialization (`git clone --recurse-submodules`, `git submodule update --init --recursive`) and CMake out-of-tree builds.
- **Core Concepts**:
  1. Source code lives in `irislime/irislime/llama.cpp`.
  2. Compilations land strictly out-of-tree in `build/base_release`, `build/base_debug`, `build/telemetry_release`, `build/linux_gcc`.
  3. Build journals and test logs land in `logs/`, `logs/debug/`, `logs/telemetry/`, `logs/tests/`.
- **Verification Exercise**: Run `make build` followed by `make manifest-build` to generate `docs/BUILD_AND_TEST_MANIFEST.md`.

---

### Module 3: Hardware Acceleration & Resource Throttling Telemetry
- **Objective**: Configure compute backends (SYCL, OpenVINO, LiteRT, Vulkan) while maintaining strict laptop thermal throttling (<50% CPU/RAM load).
- **Core Concepts**:
  1. Hardware acceleration make modules in `infra/make/*.mk`.
  2. Real-time load monitoring via [tools/monitor_system_load.py](file:///home/fekerr/src/edge-ai/tools/monitor_system_load.py).
  3. Real-time anti-flicker 1Hz log watching via `make watch-logs`.
- **Verification Exercise**: Run `make test-all` in Terminal 1 while observing live updates via `make watch-logs` in Terminal 2.

---

### Module 4: Multi-Agent Collaboration (GitHub Copilot & Google Jules)
- **Objective**: Configure VS Code, GitHub Copilot, and Google Jules (`jules.google.com`) for seamless autonomous task handoff.
- **Core Concepts**:
  1. VS Code settings, tasks, and debug launchers in `.vscode/`.
  2. Copilot directives in `.github/copilot-instructions.md`.
  3. Google Jules agent configuration in `.jules/config.yaml` and [docs/JULES_AGENT_INTEGRATION.md](file:///home/fekerr/src/edge-ai/docs/JULES_AGENT_INTEGRATION.md).
  4. Telemetry synchronization via `make agy-sync`.
- **Verification Exercise**: Execute `make agy-sync` and inspect captured telemetry statistics using `make agy-status`.
