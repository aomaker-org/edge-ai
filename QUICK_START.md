# `edge-ai` Quick Start Recipe

This recipe provides a friction-free sequence to get `edge-ai` set up and verified on a fresh environment.

---

## ⚡ 3-Step Fast Track

### 1. Clone & Enter Repository

```bash
git clone git@github.com:aomaker-org/edge-ai.git
cd edge-ai
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

For detailed environment options, see **[GETTING_STARTED.md](file:///home/fekerr/src/edge-ai/GETTING_STARTED.md)** and **[PROVISIONING_NOTES.md](file:///home/fekerr/src/edge-ai/docs/PROVISIONING_NOTES.md)**.
For hardware throttling & telemetry guidelines, see **[RESOURCE_THROTTLING_AND_TELEMETRY.md](file:///home/fekerr/src/edge-ai/docs/RESOURCE_THROTTLING_AND_TELEMETRY.md)**.
For `aomaker-org/llama.cpp` patch necessity analysis, see **[LLAMA_CPP_FORK_AUDIT.md](file:///home/fekerr/src/edge-ai/docs/LLAMA_CPP_FORK_AUDIT.md)**.
For AI agent engagement guardrails, see **[AI.md](file:///home/fekerr/src/edge-ai/AI.md)**.
