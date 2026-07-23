# ==============================================================================
# ARTIFACT ID: heredoc_002
# TYPE: Token-Optimized Clipboard Handoff
# PR: 001 (fixup-infra)
# ==============================================================================

[CTX:edge-ai|BR:feat/yaml-ledger-framework|PR:001|OS:Win11/WSL2|HW:Intel oneAPI SYCL]
PREV: Resolved Windows PE loader Exit Code 5 for ggml-base/sycl.dll via os.add_dll_directory + oneAPI runtime paths. Stripped heavy binaries (>1GB) from Git; established rclone offload to gdrive:transfer/edge-ai/.
NOW: Designing event-sourced YAML archive ledger (gemini/ledgers/archive_ledger.yaml) with append-only event stream, todo work queue, and ephemeral .pointer stubs.
GOAL: Implement Python ledger manager tool to automate archiving, stub generation, and local pruning.
