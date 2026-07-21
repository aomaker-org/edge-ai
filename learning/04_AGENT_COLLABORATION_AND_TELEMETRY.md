# Lesson 4: Autonomous Agent Collaboration & Telemetry Sync (`04_AGENT_COLLABORATION_AND_TELEMETRY.md`)

This lesson covers multi-agent interop between GitHub Copilot, Google Jules (`jules.google.com`), and AGY local session synchronization.

---

## ⚡ 1. TL;DR Summary

- **GitHub Copilot**: Configured via `.vscode/settings.json` and `.github/copilot-instructions.md`.
- **Google Jules**: Configured via `.jules/config.yaml` and [docs/JULES_AGENT_INTEGRATION.md](file:///home/fekerr/src/edge-ai/docs/JULES_AGENT_INTEGRATION.md).
- **AGY CLI**: Configured via `AI.md` and launched via `./agy-next-work.sh`.
- **Sync Command**: `make agy-sync` (idempotently syncs agent prompts and responses to `agy/prompts.jsonl`).

---

## 🏛️ 2. Architectural Deep-Dive

### Multi-Agent Handover Cycle
When passing work between GitHub Copilot, Google Jules, and AGY:

1. **Verify State**: Read [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md) and [docs/BUILD_AND_TEST_MANIFEST.md](file:///home/fekerr/src/edge-ai/docs/BUILD_AND_TEST_MANIFEST.md).
2. **Execute Work**: Implement code in `src/`, `infra/make/`, or `tools/`.
3. **Verify Build & Tests**: Run `make build` and `make test-all`.
4. **Sync Telemetry**: Run `make agy-sync` to persist conversation telemetry.
5. **Commit Progress**: Commit with a Rule 8 timestamped commit message (`YYMMDD_HHMM_NNN`).

### Exercise
Run `make agy-sync` followed by `make agy-status` to inspect logged AI session telemetry.
