# Android Hardware Acceleration & Device Subsystem (`devices/android/`)

> **Subsystem:** Android AI/ML/SLM Execution Environment  
> **Timestamp:** `260720_1547_001`

---

## 1. Directory Structure

```
devices/android/
├── README.md                           # This document
├── common/                             # Shared Android C++ & Python infrastructure
│   ├── include/
│   │   ├── ai_inference_engine.h       # C++ Abstract Inference Engine Base Interface
│   │   └── adb_rpc_protocol.h          # ADB JSON-RPC Protocol Definitions
│   ├── src/
│   │   ├── ai_inference_engine.cpp     # Base Engine Factory & Mock Engine implementation
│   │   └── adb_rpc_protocol.cpp        # Serialization / Deserialization helpers
│   ├── scripts/
│   │   ├── adb_testbed_runner.py       # Automated ADB driver & benchmarking tool
│   │   ├── adb_chat_cli.py             # Terminal Chatbot UI over ADB
│   │   └── build_and_deploy.sh         # Android NDK / Gradle build & deploy script
│   └── proto/
│       └── chat_service.json           # API Schema Specification
├── Pixel6a/                            # Google Pixel 6a (Tensor G1) App & Testbed
│   ├── README.md                       # Research & Hardware Specs
│   ├── Makefile                        # Build targets for Pixel 6a
│   ├── app/                            # Android App (Kotlin + Compose Chatbot)
│   └── native_cli/                     # Native C++ CLI binary for adb shell
└── Pixel10proxl/                       # Google Pixel 10 Pro XL (Tensor G5) App & Testbed
    ├── README.md                       # Research & Hardware Specs
    ├── Makefile                        # Build targets for Pixel 10 Pro XL
    ├── app/                            # Android App (Kotlin + Compose + Gemini Nano)
    └── native_cli/                     # Native C++ CLI binary for adb shell
```

---

## 2. ADB Integration & Host-Device Communication

### Method 1: ADB Reverse Tunneling (Recommended for Web/Chatbot UI)
1. Establish reverse tunnel:
   ```bash
   adb reverse tcp:8080 tcp:8080
   ```
2. The Android application runs an embedded HTTP server listening on `127.0.0.1:8080`.
3. The host Python script (`adb_chat_cli.py`) sends HTTP requests to `http://localhost:8080/api/v1/chat`:
   ```json
   {
     "request_id": "req_260720_001",
     "device": "Pixel10ProXL",
     "prompt": "Explain Quantum Computing in 2 sentences.",
     "max_tokens": 128,
     "temperature": 0.7,
     "use_npu": true
   }
   ```

### Method 2: ADB Shell CLI Execution (Recommended for NDK & Benchmarking)
1. Build native executable using Android NDK (e.g. `aarch64-linux-android34-clang++`).
2. Push binary and model weights to device `/data/local/tmp/`:
   ```bash
   adb push build/devices/pixel6a_infer_cli /data/local/tmp/
   adb shell chmod +x /data/local/tmp/pixel6a_infer_cli
   ```
3. Run inference directly over ADB shell:
   ```bash
   adb shell /data/local/tmp/pixel6a_infer_cli --prompt "Hello Edge AI" --backend vulkan
   ```

---

## 3. Acceleration Backends by Device

| Device | Primary Backend | Secondary Backend | Fallback |
| :--- | :--- | :--- | :--- |
| **Pixel 6a** (Tensor G1) | LiteRT GPU Delegate (OpenCL/Mali) | ExecuTorch XNNPACK | CPU OpenMP (NEON) |
| **Pixel 10 Pro XL** (Tensor G5) | Gemini Nano / AICore NPU | LiteRT-LM CompiledModel (TPU) | Vulkan FP16 / CPU |
