# ==============================================================================
# Path:         irislime/derived_components/make/sycl.mk
# Purpose:      Intel oneAPI SYCL Engine Compilation Blueprint (Profile-Aware)
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/)
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

SYCL_PROFILE    ?= $(if $(PROFILE),$(shell echo "$(PROFILE)" | tr '[:upper:]' '[:lower:]'),release)
SYCL_BUILD_DIR  = $(if $(filter debug,$(SYCL_PROFILE)),$(BUILD_DIR)/sycl_debug,$(BUILD_DIR)/sycl_relwithdebinfo)
SYCL_CMAKE_TYPE = $(if $(filter debug,$(SYCL_PROFILE)),Debug,RelWithDebInfo)
SYCL_LITERT_DIR = $(if $(filter debug,$(SYCL_PROFILE)),$(BUILD_DIR)/litert_debug,$(BUILD_DIR)/litert_release)

.PHONY: build-sycl clean-sycl

build-sycl: bootstrap-headers ## Configure and compile Intel SYCL target
	@echo "[Make] Profile Target Locked: SYCL_PROFILE=$(SYCL_PROFILE)"
	@echo "[Make] Initializing Intel oneAPI SYCL inside: $(SYCL_BUILD_DIR)"
	@mkdir -p $(SYCL_BUILD_DIR) $(LOGS_DIR)/sycl_profile
	@if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		START_TIME=$$(date +%s); \
		cd $(SYCL_BUILD_DIR) && rm -f CMakeCache.txt && \
		M_ROOT=$${MKLROOT:-/opt/intel/oneapi/mkl/latest} && \
		M_DIR="$$M_ROOT/lib/cmake/mkl" && \
		CC=icx CXX=icpx MKLROOT="$$M_ROOT" MKL_ROOT="$$M_ROOT" \
		cmake "$(ENGINE_DIR)" \
			-DGGML_SYCL=ON \
			-DCMAKE_BUILD_TYPE=$(SYCL_CMAKE_TYPE) \
			-DCMAKE_PREFIX_PATH="$(SYCL_LITERT_DIR);$$M_ROOT" \
			-DMKL_DIR="$$M_DIR" \
			-DMKL_ROOT="$$M_ROOT" \
			-DIRISLIME_LITERT_DIR="$(SYCL_LITERT_DIR)" \
			-DLLAMA_BUILD_TESTS=ON \
			-DCMAKE_C_COMPILER_LAUNCHER=ccache \
			-DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
			$(CMAKE_FLAGS) && \
		cmake --build . -j$(NUM_BUILD_JOBS) --config $(SYCL_CMAKE_TYPE); \
		STATUS=$$?; \
		END_TIME=$$(date +%s); \
		DURATION=$$((END_TIME - START_TIME)); \
		if [ $$STATUS -ne 0 ]; then \
			echo "[!] SYCL Compilation Macro Failed."; \
			exit $$STATUS; \
		fi; \
		echo "$(TIMESTAMP),sycl,$(SYCL_CMAKE_TYPE),$${DURATION}" >> $(METRICS_FILE); \
	else \
		echo "[build-sycl] Out-of-tree SYCL build directory validated at $(SYCL_BUILD_DIR)"; \
	fi

clean-sycl: ## Purge runtime generation artifacts and logs for the SYCL engine
	@echo "[!] Purging target space: $(SYCL_BUILD_DIR)"
	rm -rf $(SYCL_BUILD_DIR)
