# Line-Width Formatting Exceptions and Todos

SECTION: LINE-WIDTH FORMATTING EXCEPTIONS
The following files are exempt from the 80/120 columns line-width standard:
- Third-party source dependencies in deps/ (e.g., deps/llama.cpp/, deps/litert-lm/)
  which follow their own style guidelines.
- Machine-generated JSON manifests (e.g., build/build_manifest.json,
  irislime/irislime_manifest.json) and telemetry CSV datasets.
- Git database objects, compiled binaries, and compressed log archives (.zip).

SECTION: ONBOARDING AND PIPELINE TODOS
* [ ] Integrate tools/md2ascii.py and tools/ascii2md.py into automated Git hooks
      to automatically synchronize Markdown documentation and ASCII text mirror copies.
* [ ] Conduct cross-compilation validation for Windows native executables from
      the WSL2 Ubuntu toolchain.
* [ ] Verify the rclone file transfer script to ensure weights are correctly synchronized.
