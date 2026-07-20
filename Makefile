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

.PHONY: all help clean distclean agy-sync agy-status test build

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

manifest-gen: ## Regenerate irislime full file manifest (JSON & Markdown)
	@$(PYTHON) tools/generate_irislime_manifest.py

ai-log-diff-demo: ## Execute AI semantic log diff demonstration
	@$(PYTHON) ai-log-diff/tools/semantic_log_differ.py \
		--log-a ai-log-diff/examples/build_pass_001.log \
		--log-b ai-log-diff/examples/build_fail_001.log \
		--md-out $(BUILD_DIR)/log_diff_demo_report.md
	@echo "[ai-log-diff-demo] Report generated at $(BUILD_DIR)/log_diff_demo_report.md"

build: ## Build project targets (out-of-tree in build/)
	@mkdir -p $(BUILD_DIR)
	@echo "[build] Build directory ready at $(BUILD_DIR)"

test: ## Execute test suite idempotently
	@echo "[test] Test runner placeholder"

clean: ## Purge non-persistent build output directory (build/)
	@echo "[clean] Removing build outputs: $(BUILD_DIR)"
	rm -rf $(BUILD_DIR)

distclean: clean ## Purge build outputs and temporary runtime logs
	@echo "[distclean] Purging build artifacts and temporary logs"
	rm -rf $(LOGS_DIR)/*.log
