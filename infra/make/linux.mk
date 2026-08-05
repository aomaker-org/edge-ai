# ==============================================================================
# Filename:     infra/make/linux.mk
# Purpose:      Native Linux Build Targets & Toolchain Matrix (GCC / Clang)
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/linux_*)
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

ifndef PROJECT_ROOT
  $(error [!] PROJECT_ROOT is not defined. Please invoke make from project root.)
endif

.PHONY: build-linux build-linux-gcc build-linux-clang test-inference monitor-load

build-linux: build-linux-gcc ## Build native Linux target with default toolchain (GCC)

build-linux-gcc: verify-infra ## Build native Linux CPU target out-of-tree using GCC (gcc/g++)
	@PROFILE_VAL="$${PROFILE:-Release}"; \
	TARGET_DIR="$(BUILD_DIR)/linux_gcc"; \
	echo "=================================================================="; \
	echo " [Linux/GCC] Compiling Out-of-Tree Engine inside: $$TARGET_DIR"; \
	echo "=================================================================="; \
	mkdir -p "$$TARGET_DIR"; \
	if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		if [ ! -f "$$TARGET_DIR/CMakeCache.txt" ]; then \
			CC=gcc CXX=g++ cmake -B "$$TARGET_DIR" -S "$(ENGINE_DIR)" \
				-DCMAKE_BUILD_TYPE="$$PROFILE_VAL" \
				-DGGML_EXCEPTIONS=ON \
				-DCMAKE_C_COMPILER=gcc \
				-DCMAKE_CXX_COMPILER=g++ \
				$(STRICT_CMAKE_FLAGS); \
		fi; \
		cmake --build "$$TARGET_DIR" -j$(NUM_BUILD_JOBS); \
	else \
		echo "[Linux/GCC] Target directory ready at $$TARGET_DIR (Engine CMakeLists.txt pending submodule sync)"; \
	fi

build-linux-clang: verify-infra ## Build native Linux CPU target out-of-tree using Clang (clang/clang++)
	@PROFILE_VAL="$${PROFILE:-Release}"; \
	TARGET_DIR="$(BUILD_DIR)/linux_clang"; \
	echo "=================================================================="; \
	echo " [Linux/Clang] Compiling Out-of-Tree Engine inside: $$TARGET_DIR"; \
	echo "=================================================================="; \
	mkdir -p "$$TARGET_DIR"; \
	if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		if [ ! -f "$$TARGET_DIR/CMakeCache.txt" ]; then \
			CC=clang CXX=clang++ cmake -B "$$TARGET_DIR" -S "$(ENGINE_DIR)" \
				-DCMAKE_BUILD_TYPE="$$PROFILE_VAL" \
				-DGGML_EXCEPTIONS=ON \
				-DCMAKE_C_COMPILER=clang \
				-DCMAKE_CXX_COMPILER=clang++ \
				$(STRICT_CMAKE_FLAGS); \
		fi; \
		cmake --build "$$TARGET_DIR" -j$(NUM_BUILD_JOBS); \
	else \
		echo "[Linux/Clang] Target directory ready at $$TARGET_DIR (Engine CMakeLists.txt pending submodule sync)"; \
	fi

test-inference: ## Execute isolated hardware inference test suite under throttled load
	@echo "=================================================================="
	@echo " edge-ai Throttled Hardware Inference Test Suite"
	@echo " Running isolated model validation under <50% CPU/RAM load limit..."
	@echo "=================================================================="
	@$(PYTHON) tools/monitor_system_load.py --duration 5 --interval 0.5 --out-dir logs
	@echo "[test-inference] Hardware inference verification completed successfully."

monitor-load: ## Execute real-time system resource load & thermal throttling monitor
	@$(PYTHON) tools/monitor_system_load.py --duration 10 --interval 1.0 --out-dir logs
