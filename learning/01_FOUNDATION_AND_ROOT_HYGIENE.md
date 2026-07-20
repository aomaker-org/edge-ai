# Lesson 1: Foundation, Root Hygiene & Operational Guardrails (`01_FOUNDATION_AND_ROOT_HYGIENE.md`)

This lesson covers the core architectural principles governing the `edge-ai` workspace.

---

## ⚡ 1. TL;DR Summary

- **Root Hygiene (Rule 1)**: Keep the root clean. Only primary configuration and entrypoint files belong in root.
- **Root Anchoring (Rule 2)**: All Makefiles and scripts anchor to `$(PROJECT_ROOT)`.
- **Rule 7 (`/dev/null` Registry)**: No silent output redirection without `# NECESSARY NULL PIPE:` comments and registry in `docs/PIPE_TO_NULL_EXCEPTIONS.md`.
- **Rule 8 Timestamping**: Use `YYMMDD_HHMM_NNN` for all session logs, artifacts, and task ledgers.

---

## 🏛️ 2. Architectural Deep-Dive

### Root Directory Hygiene Invariant
```text
edge-ai/
├── Makefile               # Top-level root-anchored build interface
├── README.md              # Project overview
├── GETTING_STARTED.md     # Setup guide
├── QUICK_START.md         # Fast-track recipes
├── AI.md                  # Operational rules for AI agents
├── TODO.md                # Append-only task ledger
├── pyproject.toml         # uv environment dependency specification
├── Dockerfile             # Multi-stage container definition
├── .dockerignore          # Docker build exclusion rules
├── .vscode/               # VS Code tasks & launch configurations
├── .github/               # Copilot instructions & CI workflows
├── .jules/                # Google Jules agent configuration
├── learning/              # Educational documentation & lesson plans
├── infra/                 # Make modules (base.mk, linux.mk, etc.)
├── tools/                 # Python/Bash execution utilities
├── docs/                  # Architectural specs & exception registries
├── build/                 # Out-of-tree build outputs (gitignored)
└── logs/                  # Runtime & test execution logs (gitignored)
```

### Exercise
Run `make help` from any subdirectory to verify that `$(PROJECT_ROOT)` resolves to the absolute top-level directory path.
