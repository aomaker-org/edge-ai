# Getting Started with `edge-ai`

This guide provides step-by-step instructions to initialize your local development environment, configure path boundaries, and run workspace verification tools for the `edge-ai` repository.

---

## 1. Prerequisites & Toolchain Dependencies

Ensure your execution environment satisfies the following baseline requirements:

- **Operating System**: Linux (Ubuntu 24.04 / 26.04 LTS or WSL2 environment).
- **Build Tools**: GNU Make (`>= 4.3`), Python 3 (`>= 3.10`), GCC/Clang or MSVC.
- **Package Manager**: `uv` or standard Python `venv`.
- **Version Control**: Git (`>= 2.34`).

---

## 2. Cloning the Repository & Submodule Initialization

Because GitHub's default web interface only provides standard `git clone` URLs without submodules, choose one of the following methods when pulling down the workspace:

### Method A: Single-Step Clone with Submodules (Recommended)
```bash
git clone --recurse-submodules git@github.com:aomaker-org/edge-ai.git
cd edge-ai
```

### Method B: Standard Clone + Manual Submodule Sync
If you cloned the repository using GitHub's standard command line:
```bash
git clone git@github.com:aomaker-org/edge-ai.git
cd edge-ai
git submodule update --init --recursive
```

---

## 3. Environment Initialization & Project Root Anchoring

The workspace enforces absolute project root resolution through the top-level [Makefile](file:///home/fekerr/src/edge-ai/Makefile).

### Step 1: Verify Project Root Resolution
Run `make help` from anywhere inside the repository to verify that `PROJECT_ROOT` resolves accurately:

```bash
make help
```

Expected output header:
```text
==================================================================
 edge-ai Master Build & Automation Interface
 Project Root: /home/fekerr/src/edge-ai
==================================================================
```

### Step 2: Initialize Build & Log Workspaces
Run `make build` to ensure out-of-tree directories (`build/`, `logs/`, `agy/sessions/`) are instantiated idempotently:

```bash
make build
```

---

## 3. Synchronizing AI Agent Telemetry (`agy/`)

The repository includes a built-in telemetry synchronization system to record AI agent interactions in an append-only, deduplicated log.

To sync current conversation transcripts into `agy/`:

```bash
make agy-sync
```

To inspect the status of logged telemetry:

```bash
make agy-status
```

---

## 4. Porting Modules from `irislime`

When migrating or adapting components from `../irislime`:

1. Maintain strict root hygiene: Place source code in `src/`, make scripts in `infra/make/`, and executable utilities in `tools/`.
2. Avoid hardcoded paths: Always anchor make targets to `$(PROJECT_ROOT)`.
3. Test for idempotency: Ensure targets can be invoked repeatedly without failing or corrupting tracking state.

---

## 5. Next Steps

- Review **[QUICK_START.md](file:///home/fekerr/src/edge-ai/QUICK_START.md)** for rapid execution recipes.
- Review **[PROVISIONING_NOTES.md](file:///home/fekerr/src/edge-ai/docs/PROVISIONING_NOTES.md)** for Win11 winget & WSL2 Ubuntu provisioning guides.
- Review **[RESOURCE_THROTTLING_AND_TELEMETRY.md](file:///home/fekerr/src/edge-ai/docs/RESOURCE_THROTTLING_AND_TELEMETRY.md)** for <50% laptop thermal & load management guidelines.
- Review **[LLAMA_CPP_FORK_AUDIT.md](file:///home/fekerr/src/edge-ai/docs/LLAMA_CPP_FORK_AUDIT.md)** for `aomaker-org/llama.cpp` patch audit and necessity analysis.
- Review **[AI.md](file:///home/fekerr/src/edge-ai/AI.md)** for rules governing AI agent interactions.
- Check **[TODO.md](file:///home/fekerr/src/edge-ai/TODO.md)** for active workspace tasks.
