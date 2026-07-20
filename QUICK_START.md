# `edge-ai` Quick Start Recipe

This recipe provides a friction-free sequence to get `edge-ai` set up and verified on a fresh environment.

---

## ⚡ 3-Step Fast Track

### 1. Clone & Enter Repository

**Option A (Recommended Single-Step Clone with Submodules):**
```bash
git clone --recurse-submodules git@github.com:aomaker-org/edge-ai.git
cd edge-ai
```

**Option B (Standard Clone + Post-Clone Submodule Initialization):**
*(Note: GitHub UI only provides the standard clone URL; run `git submodule update` to fetch nested dependencies)*
```bash
git clone git@github.com:aomaker-org/edge-ai.git
cd edge-ai
git submodule update --init --recursive
```

### 2. Inspect & Verify Root Make Matrix
```bash
make help
```

### 3. Verify Out-of-Tree Build & Telemetry Sync
```bash
make build
make agy-sync
make agy-status
```

---

## 📊 Summary of Common Commands

| Command | Purpose |
| :--- | :--- |
| `make help` | Display available targets and project root path |
| `make build` | Run out-of-tree build step |
| `make test` | Execute test runner |
| `make agy-sync` | Sync AI agent prompt & response logs into `agy/` |
| `make agy-status` | Display statistics of logged AI sessions |
| `make clean` | Purge `build/` output directory |
| `make distclean` | Purge build artifacts and runtime logs |

---

For detailed environment options, see **[GETTING_STARTED.md](file:///home/fekerr/src/edge-ai/GETTING_STARTED.md)**.
For AI agent engagement guardrails, see **[AI.md](file:///home/fekerr/src/edge-ai/AI.md)**.
