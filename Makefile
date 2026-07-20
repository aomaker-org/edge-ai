# ==============================================================================
# Project:      edge-ai
# Purpose:      Top-Level Stateless Router & Build Matrix for Edge AI
# Architecture: Idempotent, Append-Only Telemetry, Clean Root Anchoring
# ==============================================================================

# 1. Project Root Anchoring (Dynamic & Absolute)
PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
export PROJECT_ROOT

# 2. Workspace Execution Parameter Defaults
BUILD_DIR        ?= $(PROJECT_ROOT)/build
LOGS_DIR         ?= $(PROJECT_ROOT)/logs
AGY_DIR          ?= $(PROJECT_ROOT)/agy
PYTHON           ?= python3

export BUILD_DIR LOGS_DIR AGY_DIR

# 3. Guard Rails & Core Subsystems
include infra/make/base.mk
include infra/make/linux.mk
include infra/make/telemetry_debug.mk
include infra/make/litert.mk
include infra/make/openvino.mk
include infra/make/sycl.mk
include infra/make/vulkan.mk

.PHONY: all help clean distclean agy-sync agy-status agy-launch agy-next new-agy test build build-debug build-telemetry build-matrix


all: help

help: ## Display available make targets
	@echo "=================================================================="
	@echo " edge-ai Master Build & Automation Interface"
	@echo " Project Root: $(PROJECT_ROOT)"
	@echo "=================================================================="
	@echo ""
	@echo "Available Targets:"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo "=================================================================="

agy-sync: ## Idempotently sync AI agent prompt & response history into agy/
	@$(PYTHON) tools/sync_agy_logs.py --workspace "$(PROJECT_ROOT)"

agy-status: ## Display statistics of captured AI session telemetry
	@$(PYTHON) tools/sync_agy_logs.py --status --workspace "$(PROJECT_ROOT)"

agy-launch: ## Launch high-autonomy AGY session wrapper script
	@./tools/agy-run-20260720.sh

agy-next: ## Launch next work high-autonomy AGY session wrapper script
	@./tools/agy-next-work.sh

new-agy: ## Launch high-autonomy AGY session configured with Claude 3.7 Sonnet for 1-hour clock time
	@./tools/agy-claude-1hr.sh

manifest-gen: ## Regenerate irislime full file manifest (JSON & Markdown)
	@$(PYTHON) tools/generate_irislime_manifest.py

manifest-build: ## Audit built executables, libraries, tests, and logs into docs/BUILD_AND_TEST_MANIFEST.md
	@$(PYTHON) tools/generate_build_manifest.py

watch-logs: ## Live-stream 'tree -f' output for logs as files are created/updated
	@./tools/tree_log_watcher.sh $(LOGS_DIR)

ai-log-diff-demo: ## Execute AI semantic log diff demonstration
	@$(PYTHON) ai-log-diff/tools/semantic_log_differ.py \
		--log-a ai-log-diff/examples/build_pass_001.log \
		--log-b ai-log-diff/examples/build_fail_001.log \
		--md-out $(BUILD_DIR)/log_diff_demo_report.md
	@echo "[ai-log-diff-demo] Report generated at $(BUILD_DIR)/log_diff_demo_report.md"

build: build-base ## Build project targets (out-of-tree in build/)

test-all: ## Discover and execute all compiled unit test executables under throttled load
	@$(PYTHON) tools/test_runner_matrix.py --build-dir build --logs-dir logs

test: test-inference ## Execute test suite idempotently

clean: ## Purge non-persistent build output directory (build/)
	@echo "[clean] Removing build outputs: $(BUILD_DIR)"
	rm -rf $(BUILD_DIR)

distclean: clean ## Purge build outputs and temporary runtime logs
	@echo "[distclean] Purging build artifacts and temporary logs"
	rm -rf $(LOGS_DIR)/*.log
