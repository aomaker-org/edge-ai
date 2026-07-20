# ==============================================================================
# Filename:     infra/make/vulkan.mk
# Purpose:      Portable Vulkan Cross-Platform Graphics Engine Blueprint
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/)
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

VULKAN_BUILD_DIR ?= $(BUILD_DIR)/vulkan_release
VULKAN_LOG_PATH  ?= $(LOGS_DIR)/build_vulkan_manual.log

.PHONY: build-vulkan clean-vulkan

build-vulkan: ## Configure and compile the portable Mesa Vulkan compute target workspace
	@echo "[Make] Initializing Vulkan SPIR-V compilation inside: $(VULKAN_BUILD_DIR)"
	@mkdir -p $(VULKAN_BUILD_DIR) $(dir $(VULKAN_LOG_PATH))
	@echo "==================================================================" >> $(VULKAN_LOG_PATH)
	@echo "[Make Session] Launching Build at $$(date)" >> $(VULKAN_LOG_PATH)
	@echo "==================================================================" >> $(VULKAN_LOG_PATH)
	@echo "[Make] Log Target Destination: $(VULKAN_LOG_PATH)"
	@if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		START_TIME=$$(date +%s); \
		cd $(VULKAN_BUILD_DIR) && \
		cmake "$(ENGINE_DIR)" \
			-DGGML_VULKAN=ON \
			-DCMAKE_BUILD_TYPE=Release \
			-DLLAMA_BUILD_TESTS=ON \
			-DCMAKE_C_COMPILER_LAUNCHER=ccache \
			-DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
			$(CMAKE_FLAGS) >> $(VULKAN_LOG_PATH) 2>&1 && \
		cmake --build . -j$(NUM_BUILD_JOBS) --config Release >> $(VULKAN_LOG_PATH) 2>&1; \
		STATUS=$$?; \
		END_TIME=$$(date +%s); \
		DURATION=$$((END_TIME - START_TIME)); \
		if [ $$STATUS -ne 0 ]; then \
			echo "[!] Vulkan Compilation Macro Failed. Inspect $(VULKAN_LOG_PATH)"; \
			exit $$STATUS; \
		fi; \
		echo "$(TIMESTAMP),vulkan,Release,$${DURATION}" >> $(METRICS_FILE); \
	else \
		echo "[build-vulkan] Out-of-tree Vulkan build directory validated at $(VULKAN_BUILD_DIR)"; \
	fi

clean-vulkan: ## Purge isolated targets and generated cache objects for Vulkan
	@echo "[!] Purging Vulkan build folder: $(VULKAN_BUILD_DIR)"
	rm -rf $(VULKAN_BUILD_DIR)
