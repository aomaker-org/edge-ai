# IrisLime Technical Debt Analysis & `edge-ai` Architectural Fixes

**Document Standard:** `260720_0823_001`  
**Scope:** Comparative Analysis between `irislime` and `edge-ai`

---

## 🛠️ Comparative Technical Debt Matrix

| Item | `irislime` Defect / Debt | `edge-ai` Architectural Resolution |
| :--- | :--- | :--- |
| **1. Root Hygiene** | Root directory cluttered with loose scripts (`irislime.sh`), zip archives (`20260718_logs_*.zip`), draft markdown files (`AI_next_work.md`). | **Strict Root Hygiene**: Root contains ONLY top-level interface files (`Makefile`, `README.md`, `GETTING_STARTED.md`, `QUICK_START.md`, `AI.md`, `TODO.md`, `.gitignore`). |
| **2. Make Anchoring** | Makefiles hardcoded relative path assumptions (`ENGINE_DIR := llama.cpp`). | **Dynamic Root Anchoring**: `PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))` exported across all make modules. |
| **3. Output Redirection** | Scripts contained un-commented redirections (`> /dev/null 2>&1`), hiding build/test failure tracebacks. | **Rule 7 Prohibition**: No `/dev/null` redirections unless necessary, commented inline, and registered in [docs/PIPE_TO_NULL_EXCEPTIONS.md](file:///home/fekerr/src/edge-ai/docs/PIPE_TO_NULL_EXCEPTIONS.md). |
| **4. Telemetry Format** | Non-standard timestamp formats (`20260718_logs_core12_1003.zip`). | **Rule 8 Standard (`YYMMDD_HHMM_NNN`)**: Enforced timestamp standard with zero-padded sequence counter and `--seq-start` override support. |
| **5. Agent Telemetry** | Agent interaction prompts were un-synced or manually recorded in scratch files. | **`agy/` Append-Only Pipeline**: Automated, idempotent `make agy-sync` utility capturing SHA256-deduplicated prompt/response streams. |
| **6. Log Analysis** | Log comparison required manual line inspection or custom regex scripts. | **`ai-log-diff` Subproject**: AI-assisted semantic log event parser isolating error cascades and structural deltas. |
