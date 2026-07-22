# Structured Project Tree Walkthrough & Workflow Guide

This document outlines the authoritative workflow, development standards, and
directory layout guidelines for the `edge-ai` repository.

---

## 1. Master Goal & Environment Strategy

Our master goal is to establish a robust, throttled, hardware-accelerated
inference testbed on local host topologies while maintaining pristine workspaces.

### Development Platform Preferences
- **WSL2 Ubuntu Bash**: The preferred and primary compiler host. All target compiles,
  make runs, and telemetry tracking should be driven from the WSL2 terminal.
- **Windows Host Cross-Compilation**: When Windows binaries are needed, we leverage
  cross-compilation or use the VS Code Task runner to execute commands on the
  Windows host side, keeping source trees separated.
- **Root Hygiene**: Never output built files, logs, or diagnostic dumps into the
  root directory. All build targets are out-of-tree.

---

## 2. Directory Tree Layout & Segregation

The repository separates code, dependencies, build matrices, and telemetry:
- `infra/make/`: Modular makefiles routing compiler targets (base, sycl, openvino, etc.)
- `deps/`: Git submodules and third-party dependencies (`deps/llama.cpp`, `deps/litert-lm`).
- `build/`: Isolated, out-of-tree build profiles (base, gcc, clang, vulkan, etc.).
- `logs/`: Profiling stats, tests logs, compiler logs, and resource telemetry.
- `agy/`: Persistent AI agent session logs and prompt history.
- `users/`: Training materials, workflows, checklists, and exceptions logs.

### Separation of Concerns
- **User Environmental Configuration**: Keep all personal machine configs (such as
  shell settings, API keys, local paths) in gitignored files (e.g. `config_env`,
  `*local*`, `~/.gemini/`) distinct from project build scripts.
- **Out-of-Tree Output Segregation**: All compiled binaries must sit in custom paths
  inside `build/` matching their profile (e.g., `build/base_release`, `build/linux_gcc`).

---

## 3. Build Matrix, Profiles & Telemetry

All builds support modular targets with baked-in debugging and telemetry tracking.

### Build Profiles
- **Debug**: Built into `build/*_debug/` with full debug symbols (-g) and sanity
  checks.
- **Release**: Built into `build/*_release/` with optimizations (-O3).
- **Telemetry & Profiling**: Built with instrumentation to trace runtime behavior.

### Strictness Control
The build system supports variable-driven compile strictness:
- Invoke builds with `STRICT=1` to enforce strict warning audits.
- In strict mode, `-Wall -Wextra -Werror` is enforced via CMake, causing any compiler
  warning to raise an exit-code failure.
  ```sh
  make build STRICT=1
  ```

---

## 4. Telemetry, Tracking & Manifests

To ensure integrity across multi-agent collaborations, we track files and artifacts.

### Fast Hashing & File Manifests
- Artifact trees and build outputs are periodically scanned and mapped using the
  manifest generator script.
- Manifests (e.g., `docs/BUILD_AND_TEST_MANIFEST.md`, `build/build_manifest.json`)
  classify files using byte counters (`wc -c`) and SHA-256 hashes.
  ```sh
  make manifest-build
  ```

### Rclone Synchronization (Windows Side Integration)
- Artifacts that are not managed by Git (such as model weights `.gguf`, test logs,
  or telemetry datasets) are indexed in rclone configuration matrices.
- The `tools/rclone_transfer.sh` and `rclone_transfer.ps1` scripts can be invoked from the
  Windows terminal environment to synchronize large local assets with cloud mirrors.

---

# EOF: users/structured_workflow.md
