# ==============================================================================
# Pixel 6a (Tensor G1) Modular Build Router
# Timestamp: 260720_1547_001
# Architecture: Out-of-tree CMake & NDK compilation
# ==============================================================================

PROJECT_ROOT ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../../..)
BUILD_DIR    ?= $(PROJECT_ROOT)/build/devices/pixel6a

.PHONY: all build clean test

all: build

build:
	@echo "[Pixel6a] Compiling native CLI executable out-of-tree in $(BUILD_DIR)..."
	@mkdir -p $(BUILD_DIR)
	@cmake -S $(PROJECT_ROOT)/devices/android/Pixel6a/native_cli -B $(BUILD_DIR) -DCMAKE_BUILD_TYPE=Release
	@cmake --build $(BUILD_DIR) --config Release

test: build
	@echo "[Pixel6a] Executing native CLI host simulation test..."
	@$(BUILD_DIR)/pixel6a_infer_cli --prompt "Test Pixel 6a Tensor G1 Engine" --backend vulkan

clean:
	@echo "[Pixel6a] Cleaning build outputs: $(BUILD_DIR)"
	@rm -rf $(BUILD_DIR)
