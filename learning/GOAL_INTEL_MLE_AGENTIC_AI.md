# Intel Machine Learning Engineer Target Learning Goal (`GOAL_INTEL_MLE_AGENTIC_AI.md`)

This document defines the **Master Learning Goal Specification** for `edge-ai`, derived from the official Intel Machine Learning Engineer / Data Scientist requisition (**JR0284870** - Agentic AI & Edge SLM Architecture).

---

## ⚡ 1. Concise Learning Goal Summary (TL;DR)

### The Vision: Privacy-First Agentic AI on Edge Hardware
> *"Build agentic AI that combines the best of local and cloud intelligence — private, affordable, and sustainable by design. Small, efficient models run directly on the user's machine (AI PC, edge, on-prem, and beyond)... while powerful cloud models handle complex reasoning."*

### Key Skill Mappings to `edge-ai` Repository Architecture

| Intel Requisition Focus Area | Required Competency | Mapped `edge-ai` Implementation Subsystem |
| :--- | :--- | :--- |
| **Agent Harness & Tooling** | Context engineering, agent memory, tools, skills | AGY CLI wrapper (`tools/agy-next-work.sh`), `.vscode/`, `.jules/` |
| **Edge SLM Optimization** | Making small models punch above their weight on edge hardware | `irislime/llama.cpp`, SYCL, OpenVINO, Vulkan, LiteRT backends |
| **Runtime Throttling & Limits** | Managing thermal load, memory bounds, and GPU bottlenecks | [tools/monitor_system_load.py](file:///home/fekerr/src/edge-ai/tools/monitor_system_load.py) (<50% CPU/RAM limit) |
| **Evaluation & Benchmarks** | Designing robust metrics and verifiable evaluation frameworks | [tools/test_runner_matrix.py](file:///home/fekerr/src/edge-ai/tools/test_runner_matrix.py) (`make test-all`) |
| **Debug-First Engineering** | Deep code/log analysis to isolate numerical and build issues | [tools/log_watcher.py](file:///home/fekerr/src/edge-ai/tools/log_watcher.py) & `ai-log-diff/` |

---

## 🏛️ 2. Verbose Curriculum & Milestone Breakdown

### Pillar 1: Agent Harness & Context Engineering Architecture
- **Goal**: Design and iterate on agent harnesses, integrating tools, skills, long-term memory, and context window management.
- **`edge-ai` Practice**:
  1. Configure multi-agent interop across VS Code Copilot, Google Jules (`jules.google.com`), and AGY local CLI.
  2. Implement append-only session telemetry in `agy/prompts.jsonl`.
  3. Maintain context boundaries using `PROJECT_ROOT` absolute anchoring.

---

### Pillar 2: Edge SLM Runtime Acceleration & Hardware Heterogeneity
- **Goal**: Understand how model architecture choices interact with hardware constraints on Intel AI PCs, integrated GPUs (Iris Xe / UHD), discrete GPUs, and NPUs.
- **`edge-ai` Practice**:
  1. Compile out-of-tree engine targets across `infra/make/` (`sycl.mk`, `openvino.mk`, `vulkan.mk`, `litert.mk`).
  2. Measure per-layer compute latency and memory bandwidth utilization.
  3. Enforce out-of-tree build separation (`build/base_release/`, `build/base_debug/`, `build/telemetry_release/`).

---

### Pillar 3: Post-Training, Quantization & Model Optimization
- **Goal**: Develop reproducible workflows for model fine-tuning, quantization (GGUF Q4_K_M / Q8_0), LoRA adapter exportation, and checkpoint deployment.
- **`edge-ai` Practice**:
  1. Utilize `llama-quantize` and `llama-export-lora` binaries in `build/base_release/bin/`.
  2. Evaluate trade-offs between model quantization depth, accuracy loss, and memory footprint.

---

### Pillar 4: Benchmark Frameworks & Empirical Verification
- **Goal**: Construct evaluation benchmarks that accurately measure model capability improvements, alignment quality, and execution reliability.
- **`edge-ai` Practice**:
  1. Discover and execute unit tests across `build/` using `tools/test_runner_matrix.py` (`make test-all`).
  2. Audit workspace executables, libraries, and separated test logs into [docs/BUILD_AND_TEST_MANIFEST.md](file:///home/fekerr/src/edge-ai/docs/BUILD_AND_TEST_MANIFEST.md).

---

### Pillar 5: Debug-First Mindset & Real-Time Telemetry Analytics
- **Goal**: Resolve multi-threaded bottlenecks, memory leaks, numerical instabilities, and build regressions.
- **`edge-ai` Practice**:
  1. Live-stream sectioned log streams using `make watch-logs` ([tools/log_watcher.py](file:///home/fekerr/src/edge-ai/tools/log_watcher.py)) at max 1Hz refresh rate.
  2. Compare build logs using `ai-log-diff/tools/semantic_log_differ.py`.
