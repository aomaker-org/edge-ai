# Lesson 2: Out-of-Tree Builds & Submodule Management (`02_OUT_OF_TREE_BUILDS_AND_SUBMODULES.md`)

This lesson covers Git submodule management, out-of-tree CMake compilation, and asset manifest generation in `edge-ai`.

---

## ⚡ 1. TL;DR Summary

- **Submodule Clone**: `git clone --recurse-submodules git@github.com:aomaker-org/edge-ai.git`
- **Submodule Sync**: `git submodule update --init --recursive`
- **Out-of-Tree Build**: `make build` (compiles inside `build/base_release/`)
- **Isolated Debug**: `make build-debug` (compiles inside `build/base_debug/` and logs to `logs/debug/`)
- **Asset Manifest**: `make manifest-build` (generates `docs/BUILD_AND_TEST_MANIFEST.md` and `build/build_manifest.json`)

---

## 🏛️ 2. Architectural Deep-Dive

### Out-of-Tree Compilation Flow
Out-of-tree builds prevent build artifacts, object files, and CMake caches from polluting source submodules (`irislime/irislime/llama.cpp`):

```text
Source Submodule:  irislime/irislime/llama.cpp/ (Clean Source Tree)
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
build/base_release/  build/base_debug/  build/telemetry_release/
  ├── bin/             ├── bin/           ├── bin/
  │   ├── llama        │   ├── llama-cli  │   └── libggml.so
  │   └── llama-cli    └── ...            └── ...
  └── CMakeCache.txt
```

### Exercise
1. Run `make build-debug` to compile the isolated Debug engine profile.
2. Run `make manifest-build` and view the updated asset inventory in [docs/BUILD_AND_TEST_MANIFEST.md](file:///home/fekerr/src/edge-ai/docs/BUILD_AND_TEST_MANIFEST.md).
