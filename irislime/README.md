# IrisLime Derived Domain (`irislime/`)

This directory serves as the root domain for components, specifications, and build patterns derived from the [`irislime`](git@github.com:aomaker-org/irislime.git) baseline repository.

---

## 📂 Subdirectory Structure

- **`irislime/derived_components/`**: Holds refactored engine abstractions, acceleration wrappers, tool scripts, and makefile recipes ported from `irislime` into `edge-ai`.

---

## 🏛️ Provenance & Integration Rules

1. All code placed under `irislime/derived_components/` must be adapted to conform to `edge-ai` rules (see [AI.md](file:///home/fekerr/src/edge-ai/AI.md)):
   - Absolute root anchoring via `$(PROJECT_ROOT)` in Make targets.
   - Out-of-tree builds directed to `build/`.
   - Strict prohibition of un-documented `/dev/null` output redirections.
   - Timestamp compliance following `YYMMDD_HHMM_NNN`.
