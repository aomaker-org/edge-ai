# ==============================================================================
# Filename:     infra/make/base.mk
# Purpose:      Base environment & path validation rules for edge-ai
# ==============================================================================

ifndef PROJECT_ROOT
$(error PROJECT_ROOT is not defined. Please invoke make from project root.)
endif

# Ensure workspace directories exist idempotently
$(shell mkdir -p $(BUILD_DIR) $(LOGS_DIR) $(AGY_DIR)/sessions)
