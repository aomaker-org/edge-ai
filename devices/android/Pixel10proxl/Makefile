# ==============================================================================
# Pixel 10 Pro XL (Tensor G5) Modular Build Router
# Timestamp: 260720_1547_001
# Architecture: Out-of-tree CMake & NDK compilation
# ==============================================================================

PROJECT_ROOT ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../../..)
BUILD_DIR    ?= $(PROJECT_ROOT)/build/devices/pixel10

.PHONY: all build clean test

all: build

build:
	@echo "[Pixel10ProXL] Compiling native CLI executable out-of-tree in $(BUILD_DIR)..."
	@mkdir -p $(BUILD_DIR)
	@cmake -S $(PROJECT_ROOT)/devices/android/Pixel10proxl/native_cli -B $(BUILD_DIR) -DCMAKE_BUILD_TYPE=Release
	@cmake --build $(BUILD_DIR) --config Release

test: build
	@echo "[Pixel10ProXL] Executing native CLI host simulation test..."
	@$(BUILD_DIR)/pixel10_infer_cli --prompt "Test Pixel 10 Pro XL Tensor G5 NPU Engine" --backend npu

clean:
	@echo "[Pixel10ProXL] Cleaning build outputs: $(BUILD_DIR)"
	@rm -rf $(BUILD_DIR)
