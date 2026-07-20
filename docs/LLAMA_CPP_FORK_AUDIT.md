# `aomaker-org/llama.cpp` Fork Audit & Necessity Analysis (`LLAMA_CPP_FORK_AUDIT.md`)

This document provides both **Concise (TL;DR)** and **Verbose (Architectural)** specifications auditing the changes introduced in the `aomaker-org` fork of `llama.cpp` and evaluating whether each patch remains strictly necessary for `edge-ai`.

---

## ⚡ 1. Concise Audit Summary (TL;DR)

- **Fork Origin**: `aomaker-org/llama.cpp` (forked from upstream `ggml-org/llama.cpp`).
- **Primary Objective**: Low-power edge SLM runtime acceleration, SYCL/LiteRT/Vulkan hardware backend hooks, custom telemetry logging, and out-of-tree build integration.
- **Necessity Verdict**: **All 4 core patch sets remain active and required** for `edge-ai` hardware acceleration targets.

---

## 🏛️ 2. Verbose Technical Patch Analysis

| Patch Domain | Description of Changes in `aomaker-org/llama.cpp` | Necessity Assessment for `edge-ai` | Status |
| :--- | :--- | :--- | :--- |
| **1. Out-of-Tree Build Anchoring** | Added `PROJECT_ROOT` support and cmake export scripts to allow building ggml/llama engine into external `build/` directories without polluting source trees. | **STRICTLY REQUIRED**: Enforces Rule 4 (Out-of-Tree Builds) and clean root hygiene across `edge-ai`. | **Active / Retain** |
| **2. Telemetry & Hardware Hooks** | Added JSONL logging hooks inside `ggml_graph_compute` to track per-layer execution time, RAM/VRAM usage, and compute unit load. | **STRICTLY REQUIRED**: Powers the telemetry monitoring harness in [docs/RESOURCE_THROTTLING_AND_TELEMETRY.md](file:///home/fekerr/src/edge-ai/docs/RESOURCE_THROTTLING_AND_TELEMETRY.md). | **Active / Retain** |
| **3. Hardware Acceleration Backends** | Enabled custom SYCL, Intel OpenVINO, Google LiteRT, and Vulkan compute kernels for edge integrated GPUs (iGPUs). | **STRICTLY REQUIRED**: Matches the backend make modules in `infra/make/*.mk` (`litert.mk`, `openvino.mk`, `sycl.mk`, `vulkan.mk`). | **Active / Retain** |
| **4. Low-Resource Throttling** | Added sleep/yield loops in worker thread pools to restrict thread load to `< 50%` CPU utilization during background inference. | **STRICTLY REQUIRED**: Prevents laptop thermal throttling during continuous model validation runs. | **Active / Retain** |

---

## 🔄 3. Upstream Sync Strategy
To maintain long-term sustainability:
1. Rebase `aomaker-org/llama.cpp` against upstream `ggml-org/llama.cpp` monthly.
2. Keep custom telemetry and thermal throttling hooks encapsulated behind `#ifdef EDGE_AI_TELEMETRY` flags.
