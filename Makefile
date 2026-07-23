# ==============================================================================
# FILENAME BEGIN: Makefile
# Description: Central Edge-AI workspace Makefile incorporating modular sub-makes,
#              Windows MSVC probes, Intel oneAPI SYCL, and AGY automation.
# ==============================================================================

.PHONY: all default win_probe sycl_probe linux_tools clean help

default: help
all: win_probe linux_tools

# ------------------------------------------------------------------------------
# Modular Sub-Makefile Inclusions (infra/make/*.mk)
# ------------------------------------------------------------------------------
-include infra/make/base.mk
-include infra/make/linux.mk
-include infra/make/sycl.mk
-include infra/make/openvino.mk
-include infra/make/litert.mk
-include infra/make/vulkan.mk
-include infra/make/android.mk
-include infra/make/telemetry_debug.mk

# ------------------------------------------------------------------------------
# Cross-Platform Hardware Probes & Windows Host Pipeline
# ------------------------------------------------------------------------------

# Build native Windows Iris Xe Probe via MSVC + Python runner
win_probe:
	@echo "================================================================================"
	@echo " BUILDING MSVC WINDOWS TARGETS..."
	@echo "================================================================================"
	@python3 gemini/tools/build_iris_probe.py

# Build Intel oneAPI SYCL targets on Windows host
sycl_probe:
	@echo "================================================================================"
	@echo " BUILDING INTEL ONEAPI SYCL TARGETS..."
	@echo "================================================================================"
	@python3 gemini/tools/build_sycl_probe.py

# Build native WSL Linux C++ binaries
CXX ?= g++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++20

linux_tools:
	@echo "================================================================================"
	@echo " BUILDING WSL LINUX NATIVE TARGETS..."
	@echo "================================================================================"
	@mkdir -p build/linux src/linux_tools
	@if [ ! -f src/linux_tools/host_info.cpp ]; then \
		echo '// FILENAME BEGIN: src/linux_tools/host_info.cpp' > src/linux_tools/host_info.cpp; \
		echo '#include <iostream>' >> src/linux_tools/host_info.cpp; \
		echo 'int main() { std::cout << "[WSL LINUX NATIVE TOOL] Host execution active.\n"; return 0; }' >> src/linux_tools/host_info.cpp; \
		echo '// FILENAME END: src/linux_tools/host_info.cpp' >> src/linux_tools/host_info.cpp; \
	fi
	$(CXX) $(CXXFLAGS) -o build/linux/host_info src/linux_tools/host_info.cpp
	@echo "[SUCCESS] Built WSL binary: build/linux/host_info"

# ------------------------------------------------------------------------------
# Cleanup & Diagnostics
# ------------------------------------------------------------------------------

clean:
	@echo "==> Purging build artifacts and logs..."
	rm -rf build/* gemini/logs/*.log
	@echo "[CLEAN] Workspace build directories purged."

help:
	@echo "================================================================================"
	@echo " EDGE-AI MASTER WORKSPACE MAKEFILE"
	@echo "================================================================================"
	@echo "  make help        - Show this help menu"
	@echo "  make all         - Build both Windows MSVC binaries and Linux WSL binaries"
	@echo "  make win_probe   - Build Windows Iris Xe DXGI/OpenCL probe via MSVC"
	@echo "  make sycl_probe  - Build Intel oneAPI SYCL probe via Windows host pipeline"
	@echo "  make linux_tools - Build native Linux tools via GCC"
	@echo "  make clean       - Remove all compiled binaries and telemetry logs"
	@echo "================================================================================"

# ==============================================================================
# FILENAME END: Makefile
# ==============================================================================
