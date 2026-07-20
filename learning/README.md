# `edge-ai` Learning & Curriculum Domain (`learning/`)

Welcome to the **`edge-ai` Learning & System Engineering Domain**. This directory contains structured educational documentation, interactive lesson plans, and practical exercises designed for both **human engineers** and **autonomous AI agents** (GitHub Copilot, Google Jules, AGY).

---

## 📚 Curriculum Overview & Lesson Plan Index

- 📖 **[LESSON_PLANS.md](file:///home/fekerr/src/edge-ai/learning/LESSON_PLANS.md)** – Comprehensive 4-stage learning roadmap and hands-on exercises.
- ⚡ **[01_FOUNDATION_AND_ROOT_HYGIENE.md](file:///home/fekerr/src/edge-ai/learning/01_FOUNDATION_AND_ROOT_HYGIENE.md)** – Lesson 1: Root directory hygiene, dynamic Makefile anchoring (`PROJECT_ROOT`), and append-only task tracking.
- 📦 **[02_OUT_OF_TREE_BUILDS_AND_SUBMODULES.md](file:///home/fekerr/src/edge-ai/learning/02_OUT_OF_TREE_BUILDS_AND_SUBMODULES.md)** – Lesson 2: Git submodules (`irislime`, `llama.cpp`), CMake out-of-tree compilation, and artifact/log separation.
- 🚀 **[03_HARDWARE_ACCELERATION_AND_THROTTLING.md](file:///home/fekerr/src/edge-ai/learning/03_HARDWARE_ACCELERATION_AND_THROTTLING.md)** – Lesson 3: Intel SYCL/OpenVINO, Google LiteRT, and Vulkan backends, <50% laptop resource throttling, and real-time load telemetry.
- 🤖 **[04_AGENT_COLLABORATION_AND_TELEMETRY.md](file:///home/fekerr/src/edge-ai/learning/04_AGENT_COLLABORATION_AND_TELEMETRY.md)** – Lesson 4: Multi-agent collaboration across GitHub Copilot, Google Jules (`jules.google.com`), and AGY session telemetry synchronization.

---

## 🎯 Target Audience & Prerequisites

- **Human Maintainers**: Systems engineers, ML infra developers, and hardware acceleration specialists.
- **Autonomous Agents**: GitHub Copilot, Google Jules (`jules.google.com`), and AGY assistants requiring structured domain context.
- **Prerequisites**: Linux/WSL2 environment, Git, CMake, Python 3.10+, GNU Make, and `uv`.
