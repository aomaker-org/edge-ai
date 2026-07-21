# ==============================================================================
# Android Pixel Mobile Hardware Acceleration Build Module (devices/android)
# Timestamp: 260720_1547_001
# Architecture: Root-Anchored, Out-of-tree Compilation & Host Simulation Testing
# ==============================================================================

DEVICES_DIR      := $(PROJECT_ROOT)/devices
ANDROID_DEV_DIR  := $(DEVICES_DIR)/android
BUILD_DEVICES    := $(BUILD_DIR)/devices

.PHONY: devices-build devices-test pixel6a-build pixel10-build clean-devices

devices-build: pixel6a-build pixel10-build ## Compile all Android Pixel C++ native CLI testbeds out-of-tree

pixel6a-build: ## Compile Pixel 6a (Tensor G1) C++ native inference CLI
	@echo "[Pixel6a] Building native C++ inference CLI out-of-tree..."
	@mkdir -p $(BUILD_DEVICES)/pixel6a
	@cmake -S $(ANDROID_DEV_DIR)/Pixel6a/native_cli -B $(BUILD_DEVICES)/pixel6a -DCMAKE_BUILD_TYPE=Release
	@cmake --build $(BUILD_DEVICES)/pixel6a --config Release

pixel10-build: ## Compile Pixel 10 Pro XL (Tensor G5) C++ native inference CLI
	@echo "[Pixel10ProXL] Building native C++ inference CLI out-of-tree..."
	@mkdir -p $(BUILD_DEVICES)/pixel10
	@cmake -S $(ANDROID_DEV_DIR)/Pixel10proxl/native_cli -B $(BUILD_DEVICES)/pixel10 -DCMAKE_BUILD_TYPE=Release
	@cmake --build $(BUILD_DEVICES)/pixel10 --config Release

devices-test: devices-build ## Run host RPC simulation test suite for mobile device testbeds
	@echo "=================================================================="
	@echo " Android Pixel AI Testbed Host Simulation & RPC Protocol Audit"
	@echo " Timestamp Tag: 260720_1547_001"
	@echo "=================================================================="
	@$(BUILD_DEVICES)/pixel6a/pixel6a_infer_cli --prompt "Smoke Test Pixel 6a" --backend vulkan
	@echo ""
	@$(BUILD_DEVICES)/pixel10/pixel10_infer_cli --prompt "Smoke Test Pixel 10 Pro XL" --backend npu
	@echo ""
	@$(PYTHON) $(ANDROID_DEV_DIR)/common/scripts/adb_testbed_runner.py --device Pixel10ProXL --prompt "System verification check"

clean-devices: ## Purge built Android testbed binaries under build/devices
	@echo "[clean-devices] Purging $(BUILD_DEVICES)"
	@rm -rf $(BUILD_DEVICES)
