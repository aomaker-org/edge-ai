# Edge AI Platform (`edge-ai`)

Welcome to **`edge-ai`**, an optimized platform for edge artificial intelligence development, model validation, and localized small language model (SLM) runtime acceleration.

Derived from the foundational work in the [`irislime`](../irislime) workspace, `edge-ai` is built from the ground up prioritizing **clean architectural boundaries**, **idempotent build matrices**, and **append-only development telemetry**.

---

## 🏛️ Core Architectural Principles

1. **Clean Root Hygiene**
   The root directory contains only top-level interface documents and entrypoints (`Makefile`, `README.md`, `GETTING_STARTED.md`, `QUICK_START.md`, `AI.md`, `TODO.md`, `.gitignore`). All subsystem code, utilities, logs, and artifacts are strictly partitioned into subdirectories.

2. **Absolute Root Anchoring (`PROJECT_ROOT`)**
   All build scripts and Makefiles anchor paths dynamically via `$(PROJECT_ROOT)`. This guarantees complete portability across clone locations and prevents broken relative path dependencies.

3. **Idempotence & Out-of-Tree Builds**
   Running `make`, `make build`, or telemetry tools multiple times produces zero unintended side effects and yields deterministic results. Build outputs are confined to `build/` (gitignored).

4. **Append-Only Telemetry (`agy/`)**
   Development history, AI agent prompts, and interaction responses are captured in an append-only, SHA256-deduplicated stream in `agy/prompts.jsonl` and `agy/sessions/`.

---

## 📂 Directory Layout

```text
edge-ai/
├── Makefile               # Top-level root-anchored build interface
├── README.md              # Project overview (this file)
├── GETTING_STARTED.md     # In-depth setup and environment initialization
├── QUICK_START.md         # Zero-friction step-by-step recipe
├── AI.md                  # Operational guardrails for AI agents
├── TODO.md                # Append-only task tracking ledger
├── agy/                   # Captured AI agent session telemetry (append-only)
│   ├── prompts.jsonl      # SHA256-deduplicated append-only event stream
│   └── sessions/          # Session summary records in Markdown
├── irislime/              # Header domain for components derived from irislime
│   ├── README.md          # Provenance and rules for irislime baseline assets
│   └── derived_components/ # Ported engine code, make files, and diagnostic wrappers
├── ai-log-diff/           # AI-assisted semantic log diffing subproject
│   ├── README.md          # Subproject overview
│   └── tools/             # Log normalizer and template differ utility
├── web/                   # Web dashboard & infrastructure domain
│   ├── README.md          # Ecosystem web index
│   └── DASHBOARD_ARCHITECTURE.md # GitHub Pages, Actions, & API dashboard design
├── infra/                 # Infrastructure and Make modules
│   └── make/              # Modular makefiles (base.mk, etc.)
├── src/                   # Core C++/Python source modules
├── tools/                 # Build runners, telemetry sync, and diagnostic tools
│   └── sync_agy_logs.py   # Idempotent AGY log synchronizer
├── docs/                  # Architecture specifications and technical notes
├── build/                 # Out-of-tree build output (gitignored)
└── logs/                  # Runtime and diagnostic logs (gitignored)
```

---

## 📥 Repository Cloning

Clone the repository directly:

```bash
git clone git@github.com:aomaker-org/edge-ai.git
cd edge-ai
```

---

## 🚀 Quick Navigation

- 📖 **[GETTING_STARTED.md](file:///home/fekerr/src/edge-ai/GETTING_STARTED.md)** – Comprehensive setup guide.
- ⚡ **[QUICK_START.md](file:///home/fekerr/src/edge-ai/QUICK_START.md)** – Fast setup instructions for immediate execution.
- 💻 **[PROVISIONING_NOTES.md](file:///home/fekerr/src/edge-ai/docs/PROVISIONING_NOTES.md)** – Win11 winget, WSL2 Ubuntu, and Native vs WSL build specifications.
- ⚡ **[RESOURCE_THROTTLING_AND_TELEMETRY.md](file:///home/fekerr/src/edge-ai/docs/RESOURCE_THROTTLING_AND_TELEMETRY.md)** – <50% laptop resource throttling & telemetry guardrails.
- 🦙 **[LLAMA_CPP_FORK_AUDIT.md](file:///home/fekerr/src/edge-ai/docs/LLAMA_CPP_FORK_AUDIT.md)** – `aomaker-org/llama.cpp` patch audit and necessity analysis.
- 🤖 **[AI.md](file:///home/fekerr/src/edge-ai/AI.md)** – Rules of engagement for AI coding agents.
- 📝 **[TODO.md](file:///home/fekerr/src/edge-ai/TODO.md)** – Append-only task ledger.

---

## 🛠️ Essential Commands

```bash
make help        # Display all available build and automation targets
make build       # Prepare and run out-of-tree build matrix
make agy-sync    # Idempotently sync AI agent prompts & responses to agy/
make agy-status  # Display AI agent telemetry statistics
make clean       # Remove build/ directory
make distclean   # Remove build outputs and temporary logs
```
