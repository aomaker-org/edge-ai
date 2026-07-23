# ==============================================================================
# FILENAME BEGIN: Makefile
# Description: Master Edge-AI workspace Makefile with verbosity control (QUIET=1/0)
# ==============================================================================

PROJECT_ROOT ?= $(CURDIR)
export PROJECT_ROOT

# Verbosity Control (Default QUIET=0 for full streaming; set QUIET=1 for silent builds)
QUIET ?= 0
export QUIET

.PHONY: all default win_probe sycl_probe linux_tools clean help

default: help
all: win_probe linux_tools

-include infra/make/base.mk
-include infra/make/linux.mk
-include infra/make/sycl.mk
-include infra/make/openvino.mk
-include infra/make/litert.mk
-include infra/make/vulkan.mk
-include infra/make/android.mk
-include infra/make/telemetry_debug.mk

win_probe:
	@python3 gemini/tools/build_iris_probe.py

sycl_probe:
	@python3 gemini/tools/build_sycl_probe.py

CXX ?= g++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++20

linux_tools:
	@mkdir -p build/linux src/linux_tools
	@if [ ! -f src/linux_tools/host_info.cpp ]; then \
		echo '// FILENAME BEGIN: src/linux_tools/host_info.cpp' > src/linux_tools/host_info.cpp; \
		echo '#include <iostream>' >> src/linux_tools/host_info.cpp; \
		echo 'int main() { std::cout << "[WSL LINUX NATIVE TOOL] Host execution active.\n"; return 0; }' >> src/linux_tools/host_info.cpp; \
		echo '// FILENAME END: src/linux_tools/host_info.cpp' >> src/linux_tools/host_info.cpp; \
	fi
	$(CXX) $(CXXFLAGS) -o build/linux/host_info src/linux_tools/host_info.cpp
	@echo "[SUCCESS] Built WSL binary: build/linux/host_info"

clean:
	@echo "==> Purging build artifacts and logs..."
	rm -rf build/* gemini/logs/*.log
	@echo "[CLEAN] Workspace build directories purged."

help:
	@echo "================================================================================"
	@echo " EDGE-AI MASTER WORKSPACE MAKEFILE"
	@echo "================================================================================"
	@echo "  make help             - Show this help menu"
	@echo "  make sycl_probe       - Build SYCL probe with live streaming output"
	@echo "  make sycl_probe QUIET=1 - Build SYCL probe silently (summary only)"
	@echo "  make win_probe        - Build Windows Iris Xe probe via MSVC"
	@echo "  make linux_tools      - Build native Linux tools via GCC"
	@echo "  make clean            - Remove all compiled binaries and telemetry logs"
	@echo "================================================================================"

# ==============================================================================
# FILENAME END: Makefile
# ==============================================================================
