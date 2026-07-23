# Edge-AI Workspace Tools & Utilities Inventory

This document provides a formal inventory and architectural reference for the utility programs, diagnostic scripts, and build components located within the `src/` directory.

---

## 1. Repository Manifest & Git Utilities (`src/tools/gix_manifest/`)
* **Language:** Rust
* **Core Purpose:** Leverages Gitoxide (`gix`) to inspect, parse, and validate local repository states and workspace manifests with high performance.
* **Key Components:**
  * `Cargo.toml`: Package configuration and dependency management.
  * `src/main.rs`: Core execution logic for manifest traversal and inspection.

## 2. Linux System Telemetry (`src/linux_tools/host_info.cpp`)
* **Language:** C++
* **Core Purpose:** Gathers low-level host telemetry, hardware metrics, and system configuration data in Linux environments.
* **Target Environment:** Linux / POSIX systems.

## 3. Windows Benchmarking Stub (`src/tools/win_bench/main.cpp`)
* **Language:** C++
* **Core Purpose:** Provides a lightweight performance benchmarking framework and execution stub tailored for Windows validation and profiling.
* **Target Environment:** Windows 11 / Native Win32 / MSVC or MinGW toolchains.

---
*Maintained under the Gemini governance and telemetry framework.*

## 4. GitHub Actions Billing & Telemetry Auditor (`gemini/tools/actions_billing_audit.py`)
* **Language:** Python 3
* **Core Purpose:** Queries the GitHub REST API (`gh api`) to retrieve organization-level Actions minute consumption, paid runner usage, and shared storage metrics.
* **Telemetry Output:** Appends timestamped JSON records to `gemini/logs/actions_billing_telemetry.jsonl`.
