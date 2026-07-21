# Lesson 3: Hardware Acceleration & Resource Throttling (`03_HARDWARE_ACCELERATION_AND_THROTTLING.md`)

This lesson covers hardware compute backends (SYCL, OpenVINO, LiteRT, Vulkan), <50% laptop resource throttling, and real-time log monitoring.

---

## ⚡ 1. TL;DR Summary

- **Resource Limit**: Maintain < 50.0% CPU and RAM utilization to keep the laptop cool and quiet.
- **Monitoring Script**: `python3 tools/monitor_system_load.py --duration 10 --interval 1.0`
- **Real-Time Log Visualizer**: `make watch-logs` (1Hz anti-flicker log visualizer)
- **Test Discovery & Execution**: `make test-all` (executes 41 unit test binaries and logs to `logs/tests/`)

---

## 🏛️ 2. Architectural Deep-Dive

### Hardware Compute Backend Matrix

| Backend Subsystem | Make Module | Target Hardware | Compute Drivers |
| :--- | :--- | :--- | :--- |
| **CPU (OpenMP/AVX2)** | `infra/make/base.mk` | Multi-core x86 CPUs | OpenMP, Native SIMD |
| **Intel SYCL / OneAPI** | `infra/make/sycl.mk` | Intel Iris Xe / Discrete iGPUs | Level Zero / OpenCL |
| **Intel OpenVINO** | `infra/make/openvino.mk` | Intel Core NPU / iGPU | OpenVINO Runtime |
| **Google LiteRT** | `infra/make/litert.mk` | Edge SLM Accelerators | LiteRT / FlatBuffers |
| **Vulkan Compute** | `infra/make/vulkan.mk` | Cross-vendor GPUs | Vulkan SDK / SPIR-V |

### Exercise
Run `make watch-logs` in Terminal 2 while executing `make test-all` in Terminal 1. Observe real-time test execution logs landing in `logs/tests/`.
