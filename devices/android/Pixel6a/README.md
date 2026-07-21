# Google Pixel 6a (Tensor G1) AI/ML/SLM Execution Architecture

> **Device Target:** Google Pixel 6a (`bluejay`)  
> **System-on-Chip:** Google Tensor G1 (Samsung 5nm LPE)  
> **Timestamp:** `260720_1547_001`

---

## 1. Hardware Specification & Compute Topology

- **CPU Cores**:
  - 2x Arm Cortex-X1 @ 2.80 GHz (Ultra Performance Cores)
  - 2x Arm Cortex-A78 @ 2.25 GHz (Performance Cores)
  - 4x Arm Cortex-A55 @ 1.80 GHz (Efficiency Cores)
- **GPU**:
  - Arm Mali-G78 MP20 (20 Cores, Vulkan 1.3, OpenCL 3.0, Arm NN)
- **NPU / TPU**:
  - 1st-Generation Google TPU (Designed for TensorFlow Lite / LiteRT graph models and camera pipeline)
- **RAM**:
  - 6 GB LPDDR5 (System Shared RAM)

---

## 2. AI/ML/SLM Open-Source Runtimes & Acceleration Strategies

### A. LiteRT (formerly TensorFlow Lite) & OpenCL / Mali GPU Delegate
- **Primary Backend**: LiteRT with OpenCL GPU delegate.
- **Precision**: FP16 / INT8 quantization.
- **Best Suited For**: Vision models (MobileNet, EfficientNet, YOLOv8 edge), BERT-mini, and custom SLMs compiled via LiteRT.

### B. ExecuTorch (PyTorch Edge Runtime)
- **Backend**: XNNPACK CPU (ARM NEON) + Vulkan delegate.
- **Usage**: PyTorch model deployment targeting ARM NEON assembly instructions.

### C. llama.cpp / MLC-LLM Native C++ Execution
- **Backend**: Vulkan Compute shaders targeting Mali-G78 MP20.
- **Quantization**: `Q4_K_M` or `Q4_0` (keeps memory footprint under 2.5 GB RAM).
- **Recommended Open Models**:
  - Gemma 2B / Gemma 2 2B (`gemma-2b-it-q4_k_m.gguf`)
  - Qwen 1.5 1.8B / Qwen 2.5 1.5B
  - TinyLlama 1.1B

---

## 3. Pixel 6a Testbed Structure

```
Pixel6a/
├── README.md                           # This document
├── Makefile                            # Target compilation router
├── app/                                # Kotlin / Jetpack Compose Android App
│   ├── build.gradle.kts                # Gradle build script
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/edgeai/pixel6a/
│   │       │   ├── MainActivity.kt     # Main Jetpack Compose UI Activity
│   │       │   ├── ui/ChatScreen.kt    # Chatbot UI Component
│   │       │   ├── engine/Pixel6aInferenceEngine.kt
│   │       │   └── service/AdbBridgeService.kt
│   │       └── cpp/
│   │           ├── CMakeLists.txt
│   │           └── pixel6a_native_engine.cpp
└── native_cli/                         # Standalone NDK C++ Binary for adb shell
    ├── CMakeLists.txt
    └── main.cpp
```

---

## 4. Build & Execution Instructions

### A. Native C++ CLI (ADB Shell)
```bash
make pixel6a-build    # Compiles out-of-tree binary into build/devices/pixel6a/pixel6a_infer_cli
```

### B. Running Testbed over ADB
```bash
python3 devices/android/common/scripts/adb_testbed_runner.py --device Pixel6a
```
