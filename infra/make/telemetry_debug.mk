# ==============================================================================
# Filename:     infra/make/telemetry_debug.mk
# Purpose:      Debug & Extra Telemetry Build Targets in Isolated Folders
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/*, logs/*)
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

ifndef PROJECT_ROOT
  $(error [!] PROJECT_ROOT is not defined. Please invoke make from project root.)
endif

.PHONY: build-debug build-telemetry build-matrix

DEBUG_BUILD_DIR     ?= $(BUILD_DIR)/base_debug
DEBUG_LOGS_DIR      ?= $(LOGS_DIR)/debug

TELEMETRY_BUILD_DIR ?= $(BUILD_DIR)/telemetry_release
TELEMETRY_LOGS_DIR  ?= $(LOGS_DIR)/telemetry

$(shell mkdir -p $(DEBUG_BUILD_DIR) $(DEBUG_LOGS_DIR) $(TELEMETRY_BUILD_DIR) $(TELEMETRY_LOGS_DIR))

build-debug: verify-infra ## Compile isolated Debug engine build into build/base_debug and logs/debug/
	@echo "=================================================================="
	@echo " [Debug Build] Initializing Debug compilation out-of-tree"
	@echo " Build Directory : $(DEBUG_BUILD_DIR)"
	@echo " Logs Directory  : $(DEBUG_LOGS_DIR)"
	@echo "=================================================================="
	@mkdir -p "$(DEBUG_BUILD_DIR)" "$(DEBUG_LOGS_DIR)"
	@if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		if [ ! -f "$(DEBUG_BUILD_DIR)/CMakeCache.txt" ]; then \
			cmake -B "$(DEBUG_BUILD_DIR)" -S "$(ENGINE_DIR)" \
				-DCMAKE_BUILD_TYPE=Debug \
				-DGGML_EXCEPTIONS=ON \
				-DGGML_DEBUG=ON \
				-DLLAMA_BUILD_TESTS=ON \
				-DCMAKE_C_COMPILER_LAUNCHER=ccache \
				-DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
				$(STRICT_CMAKE_FLAGS); \
		fi; \
		cmake --build "$(DEBUG_BUILD_DIR)" -j$(NUM_BUILD_JOBS) | tee "$(DEBUG_LOGS_DIR)/build_debug_$(TIMESTAMP).log"; \
	else \
		echo "[build-debug] Directory validated at $(DEBUG_BUILD_DIR) (Engine CMakeLists.txt pending submodule sync)"; \
	fi

build-telemetry: verify-infra ## Compile isolated Telemetry-instrumented engine build into build/telemetry_release and logs/telemetry/
	@echo "=================================================================="
	@echo " [Telemetry Build] Initializing Instrumented Telemetry compilation"
	@echo " Build Directory : $(TELEMETRY_BUILD_DIR)"
	@echo " Logs Directory  : $(TELEMETRY_LOGS_DIR)"
	@echo "=================================================================="
	@mkdir -p "$(TELEMETRY_BUILD_DIR)" "$(TELEMETRY_LOGS_DIR)"
	@if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		if [ ! -f "$(TELEMETRY_BUILD_DIR)/CMakeCache.txt" ]; then \
			cmake -B "$(TELEMETRY_BUILD_DIR)" -S "$(ENGINE_DIR)" \
				-DCMAKE_BUILD_TYPE=Release \
				-DGGML_EXCEPTIONS=ON \
				-DGGML_TELEMETRY=ON \
				-DEDGE_AI_TELEMETRY=ON \
				-DLLAMA_BUILD_TESTS=ON \
				-DCMAKE_C_COMPILER_LAUNCHER=ccache \
				-DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
				$(STRICT_CMAKE_FLAGS); \
		fi; \
		cmake --build "$(TELEMETRY_BUILD_DIR)" -j$(NUM_BUILD_JOBS) | tee "$(TELEMETRY_LOGS_DIR)/build_telemetry_$(TIMESTAMP).log"; \
	else \
		echo "[build-telemetry] Directory validated at $(TELEMETRY_BUILD_DIR) (Engine CMakeLists.txt pending submodule sync)"; \
	fi

build-matrix: build-base build-debug build-telemetry build-linux-gcc build-linux-clang ## Build full multi-variant matrix across separate build and log folders

# ==============================================================================
# Context Boundary: infra/make/telemetry_debug.mk_Complete
# ==============================================================================
