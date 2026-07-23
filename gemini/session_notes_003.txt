================================================================================
FILENAME BEGIN: gemini/session_notes_003.txt
================================================================================
================================================================================
EDGE-AI GEMINI SESSION NOTES #003
Timestamp: 2026-07-22 14:31 UTC
Host Scope: WSL2 Ubuntu (~/src/edge-ai, ~/src/irislime, ~/src/fekerr-dev)
================================================================================

1. MULTI-REPO ARCHITECTURE & CROSS-POLLINATIONS
--------------------------------------------------------------------------------
- Primary Active Workstation : ~/src/edge-ai (Current Edge/Local AI dev)
- Upstream / Parent Lineage  : ~/src/irislime (Original foundational repo)
- Sandbox / Dev Separator    : ~/src/fekerr-dev (Experimental / isolated dev)
- Seeding Protocol: Bootstrap context files (AI_gemini_001.txt, AI_gemini_002.txt,
  rulebook_001.txt) are cross-pollinated into irislime and fekerr-dev so new 
  AI sessions can attach to any tree seamlessly.

2. INFRASTRUCTURE SUITE SUMMARY (10/10 VERIFIED)
--------------------------------------------------------------------------------
  - process_inbox.py : Provenance-aware payload router with non-destructive 
                       backups in gemini/backups/ and .txt/.md twin mirroring.
  - inbox_watcher.py : Safe background directory monitor filtering for 
                       'FILENAME BEGIN:' magic bytes before processing.
  - mod_toggle.py    : Shallow submodule manager (llama.cpp, litert-lm) with 
                       .mk-off <-> .mk Make toggling and deinit space recovery.
  - clip_logger.py   : Incrementing capture logger with UTF-16LE clip.exe interop.
  - sync_session.py  : Automated 10-tool healthcheck & environment auditor.
  - quick_sync.py    : Multi-repo tree traverser, SHA-256 header extractor, and 
                       dual .tar.gz / .zip archive optimizer.
  - token_ledger.py  : Quantitative token burn tracker (5-hour / 7-day rolling).
  - build_runner.py  : Out-of-tree build runner emitting JSON telemetry sidecars.
  - audit_scaffold.sh: Multi-repo git status and directory structure auditor.
  - build_agy_prompt.py: Interactive prompt builder with slash commands (/goal, /plan).

3. SAFETY, PROVENANCE & NON-DESTRUCTIVE OVERWRITES
--------------------------------------------------------------------------------
- Zero File Destruction: Overwriting existing files creates a timestamped safety
  backup in gemini/backups/ containing explicit original filename metadata and 
  actor attribution (fekerr + gemini / agy).
- Idempotency: Re-processing identical inbox payloads results in an instant 
  skip with zero redundant disk writes.

4. TELEMETRY, LOGGING & EDGE MESH VISION
--------------------------------------------------------------------------------
- Three-Tier Storage: Git (Logic/Code) -> Rclone (Mass telemetry/Logs/Weights) ->
  Release Engine (Binary ELFs/Firmware).
- Heterogeneous Edge Mesh: Store-and-forward asynchronous node network across 
  RP2040/RP235x (Nano), Raspberry Pi/PocketBeagle (Micro), and WSL2 Host (Macro) 
  using signed Ed25519 packets.

================================================================================
FILENAME END: gemini/session_notes_003.txt
================================================================================
