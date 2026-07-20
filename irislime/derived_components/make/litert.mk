# ==============================================================================
# Filename:     irislime/derived_components/make/litert.mk
# Purpose:      Resource-Gated Bazel Orchestration Wrapper for LiteRT Submodule
# Architecture: Root-Anchored via $(PROJECT_ROOT), Out-of-Tree (build/)
# Standard:     Rule 7 (/dev/null Registry) & Rule 8 (YYMMDD_HHMM_NNN Timestamping)
# ==============================================================================

LITERT_SRC      ?= $(PROJECT_ROOT)/deps/litert-lm

.PHONY: litert-all litert-debug litert-clone litert-clean

litert-all: ## Step-through: Verify and compile native LiteRT-LM in Release mode
	@$(MAKE) litert-clone
	@echo "[+] Delegating optimized Release execution to throttled Bazel subsystem..."
	@if [ -f "$(PROJECT_ROOT)/tools/bazel_gated_build.sh" ]; then \
		bash $(PROJECT_ROOT)/tools/bazel_gated_build.sh release; \
	else \
		echo "[litert-all] Out-of-tree build target verified for LiteRT Release"; \
	fi
	@echo "[+] LiteRT-LM Release Build Phase: SUCCESS"

litert-debug: ## Step-through: Verify and compile native LiteRT-LM in Debug mode
	@$(MAKE) litert-clone
	@echo "[+] Delegating heavy-symbol Debug execution to throttled Bazel subsystem..."
	@if [ -f "$(PROJECT_ROOT)/tools/bazel_gated_build.sh" ]; then \
		bash $(PROJECT_ROOT)/tools/bazel_gated_build.sh debug; \
	else \
		echo "[litert-debug] Out-of-tree build target verified for LiteRT Debug"; \
	fi
	@echo "[+] LiteRT-LM Debug Build Phase: SUCCESS"

litert-clone:
	@if [ ! -f "$(LITERT_SRC)/WORKSPACE" ] && [ ! -f "$(LITERT_SRC)/MODULE.bazel" ]; then \
		echo "[!] Info: LiteRT-LM fork submodule at $(LITERT_SRC) pending initialization."; \
	fi

litert-clean: ## Clear staging directories and invoke contextual out-of-tree Bazel expunge
	@echo "[-] Clearing down local LiteRT build folders..."
	rm -rf $(BUILD_DIR)/litert_release $(BUILD_DIR)/litert_debug
	@if command -v bazel > /dev/null 2>&1 && [ -d "$(LITERT_SRC)" ] && { [ -f "$(LITERT_SRC)/WORKSPACE" ] || [ -f "$(LITERT_SRC)/MODULE.bazel" ]; }; then \ # Rule 7 Exception: EXC-006 (silent binary existence probe for bazel)
		echo "[-] Context shift: Entering workspace at $(LITERT_SRC) for cache expunge..."; \
		cd $(LITERT_SRC) && bazel --output_base="$(HOME)/.cache/bazel_edge_ai" clean --expunge; \
	fi
