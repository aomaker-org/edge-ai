================================================================================
FILENAME BEGIN: gemini/AI_gemini_002.txt
================================================================================
================================================================================
EDGE-AI WORKSPACE CONTEXT BOOTSTRAP (AI_gemini_002)
================================================================================

PRIMARY WORKSPACE : ~/src/edge-ai
RELATED REPOS     : ~/src/irislime (Upstream parent), ~/src/fekerr-dev (Sandbox)
GIT BRANCH        : fixup-infra
HOST ENVIRONMENT  : WSL2 Ubuntu on Win11 (User: fekerr)

1. REPOSITORY IDENTITY & OPERATING MODES
--------------------------------------------------------------------------------
- Purpose: Local LLM runtimes (llama.cpp, litert-lm), quantization, bare-metal 
  C++/Rust systems engineering, and Edge AI mesh architecture.
- Human CLI Mode: Pure offline make/cmake/cargo/g++ workflows (Zero API/tokens).
- AI Mode: Automated payload routing, context packing, and session logging.

2. TOOL SUITE QUICK REFERENCE (ALL EXECUTABLE IN ./gemini/tools/)
--------------------------------------------------------------------------------
- process_inbox.py : Dissects guarded payloads from inbox.file; creates 
                     provenance backups in gemini/backups/ before overwriting.
- inbox_watcher.py : Background monitor enforcing 'FILENAME BEGIN:' verification.
- quick_sync.py    : Multi-repo tree scanner, header extractor, and archive 
                     optimizer (.tar.gz vs .zip).
- sync_session.py  : Performs environment healthcheck and auto-clip logging.
- token_ledger.py  : Tracks API token usage over 5-hour and 7-day rolling windows.
- build_runner.py  : WSL out-of-tree build runner with JSON telemetry sidecars.

3. WORKSPACE CONVENTIONS & CONSTRAINTS
--------------------------------------------------------------------------------
- Line Width: Strict 80-120 column line wrapping for LLM context window efficiency.
- Formatting: Clean ASCII text preferred over box-drawing Unicode characters.
- Payload Schema: All code changes must use FILENAME BEGIN / END headers.
- Triple-Click CLI: Command outputs include full isolated paths for instant selection.

================================================================================
FILENAME END: gemini/AI_gemini_002.txt
================================================================================
