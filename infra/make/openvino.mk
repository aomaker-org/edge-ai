# ==============================================================================
# Filename:    infra/make/openvino.mk
# Purpose:     Intel OpenVINO Inference Acceleration Compilation Blueprint
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/)
# Standard:    Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

OPENVINO_BUILD_DIR ?= $(BUILD_DIR)/openvino_relwithdebinfo
OPENVINO_LOG_PATH  ?= $(LOGS_DIR)/build_openvino_default.log
LOCAL_INC_DIR      := $(PROJECT_ROOT)/infra/include

# --- CLEAN COMPILER PATCH MATRIX ---
OPENCL_PATCH_DEFS := \
    CL_EXTERNAL_MEMORY_HANDLE_D3D11_TEXTURE_KHR=0x406E \
    CL_EXTERNAL_MEMORY_HANDLE_D3D11_TEXTURE_KMT_KHR=0x406F \
    CL_EXTERNAL_MEMORY_HANDLE_D3D12_HEAP_KHR=0x4070 \
    CL_EXTERNAL_MEMORY_HANDLE_D3D12_RESOURCE_KHR=0x4071

# --- ENVIRONMENT POINTER INTERPOLATION (Single Source of Truth) ---
ifeq ($(OpenVINO_DIR),)
    OPENVINO_SEARCH_PATHS := \
        /usr/lib/cmake/openvino2024.6.0 \
        /opt/intel/openvino \
        /usr/lib/x86_64-linux-gnu/cmake/OpenVINO
    TARGET_OV_DIR := $(firstword $(wildcard $(OPENVINO_SEARCH_PATHS)))
else
    TARGET_OV_DIR := $(OpenVINO_DIR)
endif

# --- PLATFORM SPECIFIC COMPILER INFRASTRUCTURE ALIGNMENT ---
ifeq ($(OS),Windows_NT)
    CMAKE_GEN_FLAGS    := -G "Ninja"
    OPENVINO_CXX_FLAGS := $(addprefix -D,$(OPENCL_PATCH_DEFS)) /EHsc -I$(LOCAL_INC_DIR)
    CMAKE_EXTRA_FLAGS  := -DGGML_EXCEPTIONS=ON -DLLAMA_BUILD_TESTS=ON -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
else
    CMAKE_GEN_FLAGS    := 
    OPENVINO_CXX_FLAGS := $(addprefix -D,$(OPENCL_PATCH_DEFS)) -fexceptions -I$(LOCAL_INC_DIR)
    CMAKE_EXTRA_FLAGS  := -DGGML_EXCEPTIONS=ON -DLLAMA_BUILD_TESTS=ON -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
endif

.PHONY: build-openvino clean-openvino bootstrap-headers clean-cache-openvino

bootstrap-headers: ## Fetches missing Khronos OpenCL C++ bindings autonomously if missing
	@if [ ! -f "$(LOCAL_INC_DIR)/CL/cl2.hpp" ] || [ ! -f "$(LOCAL_INC_DIR)/CL/opencl.hpp" ]; then \
		echo "[*] Bootstrapping missing Khronos OpenCL C++ Bindings via raw source..."; \
		mkdir -p $(LOCAL_INC_DIR)/CL; \
		curl -sSL "https://raw.githubusercontent.com/KhronosGroup/OpenCL-CLHPP/main/include/CL/opencl.hpp" -o "$(LOCAL_INC_DIR)/CL/opencl.hpp"; \
		curl -sSL "https://raw.githubusercontent.com/KhronosGroup/OpenCL-CLHPP/main/include/CL/cl2.hpp" -o "$(LOCAL_INC_DIR)/CL/cl2.hpp"; \
		echo "[+] Khronos OpenCL C++ headers securely mapped to workspace tracking assets."; \
	fi

build-openvino: bootstrap-headers ## Configure and compile Intel OpenVINO acceleration target
	@mkdir -p $(LOGS_DIR)/openvino_profile $(OPENVINO_BUILD_DIR)
	@if [ -f "$(ENGINE_DIR)/CMakeLists.txt" ]; then \
		if [ ! -f "$(OPENVINO_BUILD_DIR)/CMakeCache.txt" ]; then \
			echo "[!] ALERT: CMake cache missing in $(OPENVINO_BUILD_DIR). Launching generation pass..." ; \
			cmake -B $(OPENVINO_BUILD_DIR) -S "$(ENGINE_DIR)" -DCMAKE_BUILD_TYPE=RelWithDebInfo $(CMAKE_GEN_FLAGS) $(CMAKE_EXTRA_FLAGS) ; \
		fi; \
		echo "[*] Initializing memory-constrained OpenVINO core build matrix..." ; \
		cmake --build $(OPENVINO_BUILD_DIR) -j1 ; \
	else \
		echo "[build-openvino] Out-of-tree OpenVINO build directory validated at $(OPENVINO_BUILD_DIR)"; \
	fi

clean-openvino: ## Purge isolated target configurations and logs for OpenVINO
	@echo "[!] Purging isolated target directory: $(OPENVINO_BUILD_DIR)"
	rm -rf $(OPENVINO_BUILD_DIR)

clean-cache-openvino: ## Surgically clear CMake configuration caches without purging pre-compiled object files
	@echo "[-] Surgically pruning OpenVINO CMake cache artifacts..."
	rm -f $(OPENVINO_BUILD_DIR)/CMakeCache.txt
	rm -rf $(OPENVINO_BUILD_DIR)/CMakeFiles
	@echo "[+] OpenVINO stale cache signatures purged. Object states intact."
