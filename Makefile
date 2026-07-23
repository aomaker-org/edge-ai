# ==============================================================================
# EDGE-AI WORKSPACE MODULAR MULTI-TARGET MAKEFILE
# Location: ~/src/edge-ai/Makefile
# Description: Controls builds for both native WSL Linux binaries and MSVC
#              Windows executables cross-invoked from Linux.
# ==============================================================================

.PHONY: all win_probe linux_tools clean help

# Default target builds all platforms
all: win_probe linux_tools

# Build native Windows Iris Xe Probe via MSVC + Python runner
win_probe:
	@echo "================================================================================"
	@echo " BUILDING MSVC WINDOWS TARGETS..."
	@echo "================================================================================"
	@python3 gemini/tools/build_iris_probe.py

# Build native WSL Linux C++ binaries
CXX ?= g++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++20

linux_tools:
	@echo "================================================================================"
	@echo " BUILDING WSL LINUX NATIVE TARGETS..."
	@echo "================================================================================"
	@mkdir -p build/linux src/linux_tools
	@if [ ! -f src/linux_tools/host_info.cpp ]; then \
		echo '#include <iostream>' > src/linux_tools/host_info.cpp; \
		echo 'int main() { std::cout << "[WSL LINUX NATIVE TOOL] Host execution active.\\n"; return 0; }' >> src/linux_tools/host_info.cpp; \
	fi
	$(CXX) $(CXXFLAGS) -o build/linux/host_info src/linux_tools/host_info.cpp
	@echo "[SUCCESS] Built WSL binary: build/linux/host_info"

# Purge build artifacts and telemetry logs
clean:
	@echo "==> Purging build artifacts and logs..."
	rm -rf build/win_iris_probe/* build/linux/* gemini/logs/*.log
	@echo "[CLEAN] Workspace build directories purged."

# Help documentation
help:
	@echo "Edge-AI Makefile Targets:"
	@echo "  make all         - Build both Windows MSVC binaries and Linux WSL binaries"
	@echo "  make win_probe   - Build Windows Iris Xe probe binary via MSVC pipeline"
	@echo "  make linux_tools - Build native Linux tools via GCC"
	@echo "  make clean       - Remove all compiled binaries and telemetry logs"
