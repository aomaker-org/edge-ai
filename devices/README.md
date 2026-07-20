# Mobile & Edge Devices Architecture (`devices/`)

> **Project Subsystem:** Mobile AI/ML/SLM Hardware Acceleration & Testbeds  
> **Timestamp:** `260720_1547_001`  
> **Target Devices:** Google Pixel 6a (Tensor G1), Google Pixel 10 Pro XL (Tensor G5)

---

## 1. Overview & Architecture

The `devices/` directory provides device-specific testbeds, native C++ NDK harnesses, Android applications, and host communication bridges for running Small Language Models (SLMs) and Machine Learning (ML) inference directly on mobile hardware.

```
devices/
├── README.md                           # Master Mobile Subsystem Documentation
└── android/                            # Android Platform Subsystem
    ├── README.md                       # Android Architecture & ADB Bridge Guide
    ├── common/                         # Shared C++ Engine, ADB RPC Protocol & Scripts
    │   ├── include/                    # C++ Header Interfaces
    │   │   ├── ai_inference_engine.h
    │   │   └── adb_rpc_protocol.h
    │   ├── src/                        # C++ Implementation
    │   │   ├── ai_inference_engine.cpp
    │   │   └── adb_rpc_protocol.cpp
    │   ├── scripts/                    # Python/Shell ADB Drivers & Test Harnesses
    │   │   ├── adb_testbed_runner.py   # Automated ADB benchmark runner
    │   │   ├── adb_chat_cli.py         # Interactive Chatbot CLI over ADB
    │   │   └── build_and_deploy.sh     # Gradle / CMake NDK compilation & deployment
    │   └── proto/                      # RPC Protocol Specs
    │       └── chat_service.json
    ├── Pixel6a/                        # Google Pixel 6a (Tensor G1) App & Testbed
    │   ├── README.md                   # Tensor G1 AI/ML/SLM Research & Benchmarks
    │   ├── Makefile                    # Out-of-tree build wrapper
    │   ├── app/                        # Jetpack Compose Chatbot & Service App
    │   └── native_cli/                 # Standalone adb shell C++ executable
    └── Pixel10proxl/                   # Google Pixel 10 Pro XL (Tensor G5) App & Testbed
        ├── README.md                   # Tensor G5 AI/ML/SLM Research & Benchmarks
        ├── Makefile                    # Out-of-tree build wrapper
        ├── app/                        # Jetpack Compose Chatbot & Service App
        └── native_cli/                 # Standalone adb shell C++ executable
```

---

## 2. Platform Comparison: Pixel 6a vs Pixel 10 Pro XL

| Attribute | Google Pixel 6a | Google Pixel 10 Pro XL |
| :--- | :--- | :--- |
| **SoC** | Google Tensor G1 (Samsung 5nm LPE) | Google Tensor G5 (TSMC 3nm Laguna) |
| **CPU Cores** | 2x Cortex-X1 @ 2.80 GHz<br>2x Cortex-A78 @ 2.25 GHz<br>4x Cortex-A55 @ 1.80 GHz | 1x Cortex-X4 / X925 (Ultra Core)<br>5x Cortex-A720 (Performance)<br>2x Cortex-A520 (Efficiency) |
| **GPU** | Arm Mali-G78 MP20 | Next-Gen Compute GPU (OpenCL 3.0, Vulkan 1.3) |
| **NPU / TPU** | 1st-Gen Google TPU | 4th-Gen Google TPU (Laguna NPU, +60% TOPS) |
| **RAM / Memory** | 6 GB LPDDR5 (Shared System Memory) | 16 GB LPDDR5X (High-Bandwidth) |
| **System AI Service** | Android LiteRT / TFLite Delegates | Gemini Nano v3 / AICore (`com.google.android.gms.aicore`) |
| **Primary SLM Engine** | LiteRT GPU Delegate / llama.cpp Vulkan (Q4_K_M) | LiteRT-LM CompiledModel NPU / AICore SDK / llama.cpp |
| **Max Recommended Model** | 1B – 2B parameters (e.g. Gemma-2B, Qwen1.5-1.8B) | 3B – 9B parameters (e.g. Gemma-2-9B, Llama-3.2-3B, Qwen2.5-7B) |

---

## 3. Communication Protocols (Host <-> Device)

To allow seamless development, debugging, and interactive testing without requiring a touch screen on every iteration, multiple communication bridges are implemented:

1. **ADB Reverse Port Forwarding (Recommended for HTTP/REST/WebSocket)**:
   - Command: `adb reverse tcp:8080 tcp:8080`
   - Android App runs embedded HTTP/WebSocket server.
   - Host script (`devices/android/common/scripts/adb_chat_cli.py`) sends REST JSON / WebSocket streams.

2. **ADB Forward Port Forwarding**:
   - Command: `adb forward tcp:9090 tcp:9090`
   - Host runs local server; device app streams requests.

3. **ADB Shell RPC / Binary Driver**:
   - Direct execution of `/data/local/tmp/pixel6a_infer_cli` or `/data/local/tmp/pixel10_infer_cli` over `adb shell`.

---

## 4. Build & Verification Integration

All native C++ CLI testbeds integrate with the root `Makefile`:
```bash
make devices-build    # Compiles native C++ testbed binaries out-of-tree into build/devices/
make devices-test     # Runs host simulation test suite for mobile engine RPC protocols
```
