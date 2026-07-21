# ==============================================================================
# Filename:     infra/make/base.mk
# Purpose:      RAM-Aware Topology Parsing & Safe Toolchain Pre-flight Sanity Check
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/)
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

# Strict Environment Guard Interlock
ifndef PROJECT_ROOT
  $(error [!] PROJECT_ROOT is not defined. Please invoke make from project root.)
endif

# --- GLOBAL SHELL CONFIGURATION ---
SHELL        := bash
.SHELLFLAGS  := -euo pipefail -c

QUIET ?= 0

# --- HARDWARE TOPOLOGY & MEMORY PARSER ---
# Rule 7 Exceptions: EXC-001 to EXC-004 registered in docs/PIPE_TO_NULL_EXCEPTIONS.md
TOTAL_THREADS := $(shell nproc 2>/dev/null || echo 4) # Rule 7 Exception: EXC-001 (silent nproc fallback)
NUM_P_THREADS := $(shell grep -l ',' /sys/devices/system/cpu/cpu*/topology/thread_siblings_list 2>/dev/null | wc -l) # Rule 7 Exception: EXC-002 (silent sysfs P-core topology check)
NUM_E_THREADS := $(shell grep -L ',' /sys/devices/system/cpu/cpu*/topology/thread_siblings_list 2>/dev/null | wc -l) # Rule 7 Exception: EXC-003 (silent sysfs E-core topology check)

# Forensic Memory Check (Graceful fallback if /proc/meminfo is absent natively)
TOTAL_RAM_GB  := $(shell grep MemTotal /proc/meminfo 2>/dev/null | awk '{print int($$2/1024/1024)}') # Rule 7 Exception: EXC-004 (silent /proc/meminfo memory check)
ifeq ($(TOTAL_RAM_GB),)
  TOTAL_RAM_GB := 16
endif
RAM_SAFE_JOBS := $(shell echo $$(( $(TOTAL_RAM_GB) / 4 )))

# Calculate CPU Build Capacity and Physical Inference Cores
ifeq ($(NUM_P_THREADS),0)
  CALIBRATED_CPU_JOBS := $(TOTAL_THREADS)
  NUM_INF_THREADS     := $(shell echo $$(( $(TOTAL_THREADS) / 2 )))
else
  CALIBRATED_CPU_JOBS := $(shell echo $$(( $(NUM_P_THREADS) + ($(NUM_E_THREADS) / 2) )))
  NUM_INF_THREADS     := $(shell echo $$(( $(NUM_P_THREADS) / 2 )))
endif

# Ensure RAM constraints take precedence if memory space is tight
CALIBRATED_BUILD_JOBS := $(shell if [ $(RAM_SAFE_JOBS) -lt $(CALIBRATED_CPU_JOBS) ] && [ $(RAM_SAFE_JOBS) -gt 0 ]; then echo $(RAM_SAFE_JOBS); else echo $(CALIBRATED_CPU_JOBS); fi)

ifeq ($(CALIBRATED_BUILD_JOBS),0)
  CALIBRATED_BUILD_JOBS := 2
endif

# --- VARIABLE INTERPOLATION GATES ---
NUM_BUILD_JOBS ?= $(CALIBRATED_BUILD_JOBS)

# --- SHARED CONFIGURATION MATRIX ---
ENGINE_DIR    ?= $(PROJECT_ROOT)/deps/llama.cpp
BUILD_DIR     ?= $(PROJECT_ROOT)/build
LOGS_DIR      ?= $(PROJECT_ROOT)/logs
AGY_DIR       ?= $(PROJECT_ROOT)/agy
# Rule 8 Compliance: YYMMDD_HHMM_NNN Timestamping Standard
TIMESTAMP     := $(shell date +%y%m%d_%H%M_001)
METRICS_FILE  := $(LOGS_DIR)/telemetry_builds.csv

# Ensure workspace output directories exist idempotently
$(shell mkdir -p $(BUILD_DIR) $(LOGS_DIR) $(AGY_DIR)/sessions)

define log_telemetry
	echo "$(TIMESTAMP),$(1),$(2),$(3)" >> $(METRICS_FILE)
endef

.PHONY: verify-infra track-workspace show-topology build-base clean-base

show-topology: ## Audit and display host platform core topologies and memory boundaries
	@echo "=================================================================="
	@echo " edge-ai Hardware & Memory Telemetry Report"
	@echo "=================================================================="
	@echo "  Total System Memory Detected       : $(TOTAL_RAM_GB) GB"
	@echo "  Memory-Safe Max Parallel Jobs      : $(RAM_SAFE_JOBS)"
	@echo "  Detected Total Logical Processors  : $(TOTAL_THREADS)"
	@echo "  Performance Core Threads Detected  : $(NUM_P_THREADS) (Physical P-Cores: $(NUM_INF_THREADS))"
	@echo "  Efficient Core Threads Detected    : $(NUM_E_THREADS)"
	@echo "------------------------------------------------------------------"
	@echo "  CALIBRATED CONCURRENCY CAPACITY   : $(CALIBRATED_BUILD_JOBS)"
	@echo "  ACTIVE RUNNER CONCURRENCY VALUE    : $(NUM_BUILD_JOBS)"
	@echo "  CALIBRATED INFERENCE THREADS (-t)  : $(NUM_INF_THREADS)"
	@echo "=================================================================="

verify-infra: ## Validate internal modular build folder workspace directory structures
	@if [ ! -d "$(PROJECT_ROOT)/infra/make" ]; then \
		echo "[!] Critical Error: Modular build directory structure missing at infra/make"; \
		exit 1; \
	fi

track-workspace: ## List active binary assets and log configurations inside active build folders
	@echo ""
	@echo "[+] Mapping current edge-ai variant tree structure for: $(BUILD_DIR)"
	@if command -v tree > /dev/null 2>&1; then \ # Rule 7 Exception: EXC-005 (silent tree existence probe)
		tree -f $(BUILD_DIR); \
	else \
		find $(BUILD_DIR) -type f -name "*.log" -o -name "llama-cli" 2>/dev/null || true; \ # Rule 7 Exception: EXC-005 (silent find fallback query)
	fi

build-base: verify-infra ## Compile base CPU inference target (out-of-tree in build/)
	@PROFILE_VAL="$${PROFILE:-$${CMAKE_BUILD_TYPE:-Release}}"; \
	PROFILE_LOWER=$$(echo "$$PROFILE_VAL" | tr '[:upper:]' '[:lower:]'); \
	TARGET_DIR="$(BUILD_DIR)/base_$$PROFILE_LOWER"; \
	echo "[Make] Initializing Base CPU compilation inside: $$TARGET_DIR"; \
	mkdir -p "$$TARGET_DIR"; \
	if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		if [ ! -f "$$TARGET_DIR/CMakeCache.txt" ]; then \
			cmake -B "$$TARGET_DIR" -S "$(ENGINE_DIR)" \
				-DCMAKE_BUILD_TYPE="$$PROFILE_VAL" \
				-DGGML_EXCEPTIONS=ON \
				-DLLAMA_BUILD_TESTS=ON \
				-DCMAKE_C_COMPILER_LAUNCHER=ccache \
				-DCMAKE_CXX_COMPILER_LAUNCHER=ccache; \
		fi; \
		cmake --build "$$TARGET_DIR" -j$(NUM_BUILD_JOBS); \
	else \
		echo "[build-base] Out-of-tree build directory validated at $$TARGET_DIR (Engine CMakeLists.txt pending submodule sync)"; \
	fi

clean-base: ## Purge build/base_* out-of-tree build directories
	@echo "[Clean] Removing $(BUILD_DIR)/base_* directories"
	rm -rf $(BUILD_DIR)/base_*
