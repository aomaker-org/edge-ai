# Google Pixel 10 Pro XL (Tensor G5) AI/ML/SLM Execution Architecture

> **Device Target:** Google Pixel 10 Pro XL (`laguna`)  
> **System-on-Chip:** Google Tensor G5 (TSMC 3nm Laguna Node)  
> **Timestamp:** `260720_1547_001`

---

## 1. Hardware Specification & Compute Topology

- **CPU Cores**:
  - 1x Arm Cortex-X4 / X925 Prime Core (@ ~3.40 GHz)
  - 5x Arm Cortex-A720 Performance Cores
  - 2x Arm Cortex-A520 Efficiency Cores
- **GPU**:
  - Next-Gen High-Performance Compute GPU (OpenCL 3.0, Vulkan 1.3)
- **NPU / TPU**:
  - 4th-Generation Google TPU ("Laguna" NPU, +60% compute throughput over Tensor G4)
- **RAM**:
  - 16 GB LPDDR5X (High-Bandwidth Shared Memory)

---

## 2. AI/ML/SLM Software Acceleration Stack

### A. Gemini Nano & Android AICore System Service (`com.google.android.gms.aicore`)
- **System Integration**: Native Android 15/16 system-level model runtime.
- **Model**: Gemini Nano v3 (Multimodal: Text, Image, Audio processing on-device).
- **Features**: Zero-latency prompt evaluation, hardware safety sandbox (Private Compute Core).

### B. LiteRT-LM & CompiledModel TPU API
- **Framework**: Open-source Google AI Edge runtime for Large & Small Language Models.
- **Execution Target**: Tensor G5 TPU delegate.
- **Supported Quantized Models**:
  - Gemma 2 2B / Gemma 2 9B (`gemma-2-9b-it.bin`)
  - Llama 3.2 1B / 3B
  - Qwen 2.5 1.5B / 7B

### C. ExecuTorch NPU Delegate & llama.cpp Vulkan
- **ExecuTorch**: PyTorch edge framework with Laguna TPU graph compilation delegate.
- **llama.cpp**: Native NDK build with Vulkan/OpenCL acceleration leveraging 16 GB LPDDR5X RAM for FP16 and `Q8_0` high-precision SLMs.

---

## 3. Pixel 10 Pro XL Testbed Structure

```
Pixel10proxl/
├── README.md                           # Research & Architecture Specification
├── Makefile                            # Target compilation router
├── app/                                # Kotlin / Jetpack Compose Android App
│   ├── build.gradle.kts                # Gradle build script
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/edgeai/pixel10proxl/
│   │       │   ├── MainActivity.kt     # Jetpack Compose UI Activity
│   │       │   ├── ui/ChatScreen.kt    # Chatbot UI with Gemini Nano Toggle
│   │       │   ├── engine/Pixel10ProXLInferenceEngine.kt
│   │       │   └── service/AdbBridgeService.kt
│   │       └── cpp/
│   │           ├── CMakeLists.txt
│   │           └── pixel10_native_engine.cpp
└── native_cli/                         # Standalone NDK C++ Binary for adb shell
    ├── CMakeLists.txt
    └── main.cpp
```

---

## 4. Build & Execution Instructions

### A. Native C++ CLI (ADB Shell)
```bash
make pixel10-build    # Compiles out-of-tree binary into build/devices/pixel10/pixel10_infer_cli
```

### B. Running Testbed over ADB
```bash
python3 devices/android/common/scripts/adb_testbed_runner.py --device Pixel10ProXL
```
