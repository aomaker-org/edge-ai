# `edge-ai` Build & Test Asset Manifest (`BUILD_AND_TEST_MANIFEST.md`)

This manifest provides both **Concise (TL;DR)** and **Verbose (Architectural)** asset tracking for all compiled executables, shared libraries, test binaries, and separated telemetry log files across `edge-ai`.

- **Generated Timestamp**: `2026-07-20T09:34:43.130715`
- **Rule 8 Timestamp Tag**: `260720_0934_001`
- **Project Root**: `/home/fekerr/src/edge-ai`

---

## ⚡ 1. Concise Asset Summary (TL;DR)

| Asset Category | Total Items Found | Primary Output Directory | Status |
| :--- | :--- | :--- | :--- |
| 🚀 **Built Executables** | **81** binaries | `build/base_release/bin/`, `build/*/bin/` | **Validated** |
| 📦 **Shared Libraries & Artifacts** | **1711** libraries/objects | `build/*/bin/`, `build/*/` | **Validated** |
| 🧪 **Test Executables** | **41** unit test binaries | `build/*/bin/` | **Validated** |
| 📝 **Separated Log & Telemetry Files** | **5** log files | `logs/`, `logs/tests/`, `logs/debug/`, `agy/` | **Separated & Active** |

---

## 🏛️ 2. Verbose Asset Inventory by Section

### A. 🚀 Built Executables & Engine Binaries (81 Files)

| Binary Name | Relative File Path | File Size | SHA256 Prefix | Executable |
| :--- | :--- | :--- | :--- | :--- |
| `CMakeDetermineCompilerABI_C.bin` | `build/base_debug/CMakeFiles/4.2.3/CMakeDetermineCompilerABI_C.bin` | 15.6 KB | `c6ec47bb5780897f` | ✅ |
| `CMakeDetermineCompilerABI_CXX.bin` | `build/base_debug/CMakeFiles/4.2.3/CMakeDetermineCompilerABI_CXX.bin` | 15.7 KB | `7aad0854c05cc22f` | ✅ |
| `a.out` | `build/base_debug/CMakeFiles/4.2.3/CompilerIdC/a.out` | 15.7 KB | `7a1142938e504e0b` | ✅ |
| `a.out` | `build/base_debug/CMakeFiles/4.2.3/CompilerIdCXX/a.out` | 15.7 KB | `a761a1ebb40e916e` | ✅ |
| `ompver_C.bin` | `build/base_debug/CMakeFiles/FindOpenMP/ompver_C.bin` | 15.9 KB | `03282ec0c8e57f6b` | ✅ |
| `ompver_CXX.bin` | `build/base_debug/CMakeFiles/FindOpenMP/ompver_CXX.bin` | 16.0 KB | `5a1e1b933e4a8bd1` | ✅ |
| `libggml-base.so.0` | `build/base_debug/bin/libggml-base.so.0` | 4.20 MB | `8c480b5a4f4d85b7` | ✅ |
| `libggml-base.so.0.15.2` | `build/base_debug/bin/libggml-base.so.0.15.2` | 4.20 MB | `8c480b5a4f4d85b7` | ✅ |
| `libggml-cpu.so.0` | `build/base_debug/bin/libggml-cpu.so.0` | 3.70 MB | `1d7b9785061b79d3` | ✅ |
| `libggml-cpu.so.0.15.2` | `build/base_debug/bin/libggml-cpu.so.0.15.2` | 3.70 MB | `1d7b9785061b79d3` | ✅ |
| `libggml.so.0` | `build/base_debug/bin/libggml.so.0` | 722.1 KB | `094b229f47c304a4` | ✅ |
| `libggml.so.0.15.2` | `build/base_debug/bin/libggml.so.0.15.2` | 722.1 KB | `094b229f47c304a4` | ✅ |
| `CMakeDetermineCompilerABI_C.bin` | `build/base_release/CMakeFiles/4.2.3/CMakeDetermineCompilerABI_C.bin` | 15.6 KB | `c6ec47bb5780897f` | ✅ |
| `CMakeDetermineCompilerABI_CXX.bin` | `build/base_release/CMakeFiles/4.2.3/CMakeDetermineCompilerABI_CXX.bin` | 15.7 KB | `7aad0854c05cc22f` | ✅ |
| `a.out` | `build/base_release/CMakeFiles/4.2.3/CompilerIdC/a.out` | 15.7 KB | `7a1142938e504e0b` | ✅ |
| `a.out` | `build/base_release/CMakeFiles/4.2.3/CompilerIdCXX/a.out` | 15.7 KB | `a761a1ebb40e916e` | ✅ |
| `ompver_C.bin` | `build/base_release/CMakeFiles/FindOpenMP/ompver_C.bin` | 15.9 KB | `03282ec0c8e57f6b` | ✅ |
| `ompver_CXX.bin` | `build/base_release/CMakeFiles/FindOpenMP/ompver_CXX.bin` | 16.0 KB | `5a1e1b933e4a8bd1` | ✅ |
| `export-graph-ops` | `build/base_release/bin/export-graph-ops` | 233.6 KB | `5ecede73c958a9ba` | ✅ |
| `libggml-base.so.0` | `build/base_release/bin/libggml-base.so.0` | 909.0 KB | `9dcc068e161f9b22` | ✅ |
| `libggml-base.so.0.15.2` | `build/base_release/bin/libggml-base.so.0.15.2` | 909.0 KB | `9dcc068e161f9b22` | ✅ |
| `libggml-cpu.so.0` | `build/base_release/bin/libggml-cpu.so.0` | 1.10 MB | `a26cdf4cc70b2378` | ✅ |
| `libggml-cpu.so.0.15.2` | `build/base_release/bin/libggml-cpu.so.0.15.2` | 1.10 MB | `a26cdf4cc70b2378` | ✅ |
| `libggml.so.0` | `build/base_release/bin/libggml.so.0` | 58.2 KB | `399063ec7b7e6a25` | ✅ |
| `libggml.so.0.15.2` | `build/base_release/bin/libggml.so.0.15.2` | 58.2 KB | `399063ec7b7e6a25` | ✅ |
| `libllama-common.so.0` | `build/base_release/bin/libllama-common.so.0` | 5.73 MB | `fa26585f09735836` | ✅ |
| `libllama-common.so.0.0.9802` | `build/base_release/bin/libllama-common.so.0.0.9802` | 5.73 MB | `fa26585f09735836` | ✅ |
| `libllama.so.0` | `build/base_release/bin/libllama.so.0` | 3.69 MB | `d40596852219ef0a` | ✅ |
| `libllama.so.0.0.9802` | `build/base_release/bin/libllama.so.0.0.9802` | 3.69 MB | `d40596852219ef0a` | ✅ |
| `libmtmd.so.0` | `build/base_release/bin/libmtmd.so.0` | 1.39 MB | `7cd02cce49cbca2b` | ✅ |
| `libmtmd.so.0.0.9802` | `build/base_release/bin/libmtmd.so.0.0.9802` | 1.39 MB | `7cd02cce49cbca2b` | ✅ |
| `llama` | `build/base_release/bin/llama` | 48.0 KB | `a8d7a93ed63b8d8b` | ✅ |
| `llama-batched` | `build/base_release/bin/llama-batched` | 39.7 KB | `1a781aa69e5610e4` | ✅ |
| `llama-batched-bench` | `build/base_release/bin/llama-batched-bench` | 15.6 KB | `d118e9ec3353eb19` | ✅ |
| `llama-bench` | `build/base_release/bin/llama-bench` | 17.5 KB | `11ba69acb8da527a` | ✅ |
| `llama-cli` | `build/base_release/bin/llama-cli` | 17.5 KB | `f65ee163cf3bc94d` | ✅ |
| `llama-completion` | `build/base_release/bin/llama-completion` | 15.6 KB | `c895419f5a2d410f` | ✅ |
| `llama-convert-llama2c-to-ggml` | `build/base_release/bin/llama-convert-llama2c-to-ggml` | 71.9 KB | `448575e4ea136acc` | ✅ |
| `llama-cvector-generator` | `build/base_release/bin/llama-cvector-generator` | 82.2 KB | `c96bd6cdb901f65b` | ✅ |
| `llama-debug` | `build/base_release/bin/llama-debug` | 239.9 KB | `abf6f241b99f229c` | ✅ |
| `llama-debug-template-parser` | `build/base_release/bin/llama-debug-template-parser` | 205.2 KB | `31aa441aabfb55b9` | ✅ |
| `llama-diffusion-cli` | `build/base_release/bin/llama-diffusion-cli` | 70.0 KB | `adc9072c378e6fc1` | ✅ |
| `llama-embedding` | `build/base_release/bin/llama-embedding` | 62.1 KB | `dc7569f40d08230b` | ✅ |
| `llama-eval-callback` | `build/base_release/bin/llama-eval-callback` | 34.6 KB | `e590069065907f50` | ✅ |
| `llama-export-lora` | `build/base_release/bin/llama-export-lora` | 78.2 KB | `5ae20c751ffd2d61` | ✅ |
| `llama-finetune` | `build/base_release/bin/llama-finetune` | 34.9 KB | `843d25c7045b8fae` | ✅ |
| `llama-fit-params` | `build/base_release/bin/llama-fit-params` | 15.6 KB | `dda297322f161dc8` | ✅ |
| `llama-gemma3-cli` | `build/base_release/bin/llama-gemma3-cli` | 16.6 KB | `082174eb234c7db7` | ✅ |
| `llama-gen-docs` | `build/base_release/bin/llama-gen-docs` | 54.1 KB | `fcd093bbb46e6352` | ✅ |
| `llama-gguf` | `build/base_release/bin/llama-gguf` | 27.8 KB | `dbee5afb3698b7ae` | ✅ |
| `llama-gguf-hash` | `build/base_release/bin/llama-gguf-hash` | 108.8 KB | `19b847fe8330663e` | ✅ |
| `llama-gguf-split` | `build/base_release/bin/llama-gguf-split` | 46.7 KB | `bbe0e4449a28ee13` | ✅ |
| `llama-idle` | `build/base_release/bin/llama-idle` | 34.6 KB | `288711feeb60f878` | ✅ |
| `llama-imatrix` | `build/base_release/bin/llama-imatrix` | 329.6 KB | `61ba4c62d2fe4104` | ✅ |
| `llama-llava-cli` | `build/base_release/bin/llama-llava-cli` | 16.6 KB | `082174eb234c7db7` | ✅ |
| `llama-lookahead` | `build/base_release/bin/llama-lookahead` | 48.4 KB | `14d73ae29ae6183d` | ✅ |
| `llama-lookup` | `build/base_release/bin/llama-lookup` | 49.8 KB | `93fccd9647996263` | ✅ |
| `llama-lookup-create` | `build/base_release/bin/llama-lookup-create` | 35.1 KB | `f59762c12b5efaed` | ✅ |
| `llama-lookup-merge` | `build/base_release/bin/llama-lookup-merge` | 21.8 KB | `f8c41249a1998229` | ✅ |
| `llama-lookup-stats` | `build/base_release/bin/llama-lookup-stats` | 40.2 KB | `2ad025516f2d4b83` | ✅ |
| `llama-minicpmv-cli` | `build/base_release/bin/llama-minicpmv-cli` | 16.6 KB | `082174eb234c7db7` | ✅ |
| `llama-mtmd-cli` | `build/base_release/bin/llama-mtmd-cli` | 75.9 KB | `db5b6a33f6c7c267` | ✅ |
| `llama-mtmd-debug` | `build/base_release/bin/llama-mtmd-debug` | 48.2 KB | `31267ba55b198f85` | ✅ |
| `llama-parallel` | `build/base_release/bin/llama-parallel` | 62.4 KB | `0a81e54a13f0ff70` | ✅ |
| `llama-passkey` | `build/base_release/bin/llama-passkey` | 48.4 KB | `58da699b6e3c3c59` | ✅ |
| `llama-perplexity` | `build/base_release/bin/llama-perplexity` | 15.6 KB | `48bb6e4bbd346424` | ✅ |
| `llama-q8dot` | `build/base_release/bin/llama-q8dot` | 20.4 KB | `74d8bba9834986d0` | ✅ |
| `llama-quantize` | `build/base_release/bin/llama-quantize` | 17.5 KB | `a81c11f0b16e8af5` | ✅ |
| `llama-qwen2vl-cli` | `build/base_release/bin/llama-qwen2vl-cli` | 16.6 KB | `082174eb234c7db7` | ✅ |
| `llama-results` | `build/base_release/bin/llama-results` | 40.4 KB | `ace9ce6fa4a5dd04` | ✅ |
| `llama-retrieval` | `build/base_release/bin/llama-retrieval` | 67.0 KB | `b4a3bde379744465` | ✅ |
| `llama-server` | `build/base_release/bin/llama-server` | 17.5 KB | `32daa34fa38058a3` | ✅ |
| `llama-simple` | `build/base_release/bin/llama-simple` | 26.6 KB | `2e637ace8c5860aa` | ✅ |
| `llama-simple-chat` | `build/base_release/bin/llama-simple-chat` | 31.5 KB | `27ec1da407e741e4` | ✅ |
| `llama-speculative` | `build/base_release/bin/llama-speculative` | 71.9 KB | `523d62ae3ee389b3` | ✅ |
| `llama-speculative-simple` | `build/base_release/bin/llama-speculative-simple` | 78.8 KB | `fe3685d687a51b99` | ✅ |
| `llama-template-analysis` | `build/base_release/bin/llama-template-analysis` | 201.6 KB | `04d940f26227acfb` | ✅ |
| `llama-tokenize` | `build/base_release/bin/llama-tokenize` | 30.8 KB | `fab087471fe8cd60` | ✅ |
| `llama-tts` | `build/base_release/bin/llama-tts` | 411.7 KB | `602c7c9f6d678c2b` | ✅ |
| `llama-vdot` | `build/base_release/bin/llama-vdot` | 21.3 KB | `b92fcd1e015478e5` | ✅ |
| `llama-ui-embed` | `build/base_release/tools/ui/llama-ui-embed` | 73.7 KB | `70a4f24195fea097` | ✅ |

---

### B. 📦 Shared Libraries & Compiled Artifacts (1711 Files)

| Artifact Name | Relative File Path | File Size | Category |
| :--- | :--- | :--- | :--- |
| `CMakeCache.txt` | `build/base_debug/CMakeCache.txt` | 35.6 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/CTestTestfile.cmake` | 0.5 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/cmake_install.cmake` | 7.2 KB | Build Artifact |
| `llama-config.cmake` | `build/base_debug/llama-config.cmake` | 1.7 KB | Build Artifact |
| `llama-version.cmake` | `build/base_debug/llama-version.cmake` | 2.7 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/tools/CTestTestfile.cmake` | 0.7 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/tools/cmake_install.cmake` | 4.8 KB | Build Artifact |
| `CMakeDirectoryInformation.cmake` | `build/base_debug/tools/completion/CMakeFiles/CMakeDirectoryInformation.cmake` | 0.7 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/completion/CMakeFiles/llama-completion-impl.dir/DependInfo.cmake` | 0.9 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/completion/CMakeFiles/llama-completion-impl.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/completion/CMakeFiles/llama-completion-impl.dir/link.txt` | 0.5 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/completion/CMakeFiles/llama-completion.dir/DependInfo.cmake` | 0.9 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/completion/CMakeFiles/llama-completion.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/completion/CMakeFiles/llama-completion.dir/link.txt` | 0.4 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/tools/completion/CTestTestfile.cmake` | 0.3 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/tools/completion/cmake_install.cmake` | 3.7 KB | Build Artifact |
| `CMakeDirectoryInformation.cmake` | `build/base_debug/tools/llama-bench/CMakeFiles/CMakeDirectoryInformation.cmake` | 0.7 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/llama-bench/CMakeFiles/llama-bench-impl.dir/DependInfo.cmake` | 0.9 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/llama-bench/CMakeFiles/llama-bench-impl.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/llama-bench/CMakeFiles/llama-bench-impl.dir/link.txt` | 0.5 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/llama-bench/CMakeFiles/llama-bench.dir/DependInfo.cmake` | 0.9 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/llama-bench/CMakeFiles/llama-bench.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/llama-bench/CMakeFiles/llama-bench.dir/link.txt` | 0.4 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/tools/llama-bench/CTestTestfile.cmake` | 0.3 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/tools/llama-bench/cmake_install.cmake` | 3.6 KB | Build Artifact |
| `CMakeDirectoryInformation.cmake` | `build/base_debug/tools/perplexity/CMakeFiles/CMakeDirectoryInformation.cmake` | 0.7 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/perplexity/CMakeFiles/llama-perplexity-impl.dir/DependInfo.cmake` | 0.9 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/perplexity/CMakeFiles/llama-perplexity-impl.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/perplexity/CMakeFiles/llama-perplexity-impl.dir/link.txt` | 0.5 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/perplexity/CMakeFiles/llama-perplexity.dir/DependInfo.cmake` | 0.9 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/perplexity/CMakeFiles/llama-perplexity.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/perplexity/CMakeFiles/llama-perplexity.dir/link.txt` | 0.4 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/tools/perplexity/CTestTestfile.cmake` | 0.3 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/tools/perplexity/cmake_install.cmake` | 3.7 KB | Build Artifact |
| `CMakeDirectoryInformation.cmake` | `build/base_debug/tools/tokenize/CMakeFiles/CMakeDirectoryInformation.cmake` | 0.7 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/tokenize/CMakeFiles/llama-tokenize.dir/link.txt` | 0.4 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/tools/tokenize/CTestTestfile.cmake` | 0.3 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/tools/tokenize/cmake_install.cmake` | 2.5 KB | Build Artifact |
| `CMakeDirectoryInformation.cmake` | `build/base_debug/tools/ui/CMakeFiles/CMakeDirectoryInformation.cmake` | 0.7 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui-assets.dir/DependInfo.cmake` | 0.6 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui-assets.dir/cmake_clean.cmake` | 0.2 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui-embed.dir/DependInfo.cmake` | 0.8 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui-embed.dir/cmake_clean.cmake` | 0.4 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/ui/CMakeFiles/llama-ui-embed.dir/link.txt` | 0.1 KB | Build Artifact |
| `DependInfo.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui.dir/DependInfo.cmake` | 0.7 KB | Build Artifact |
| `cmake_clean.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui.dir/cmake_clean.cmake` | 0.3 KB | Build Artifact |
| `cmake_clean_target.cmake` | `build/base_debug/tools/ui/CMakeFiles/llama-ui.dir/cmake_clean_target.cmake` | 0.0 KB | Build Artifact |
| `link.txt` | `build/base_debug/tools/ui/CMakeFiles/llama-ui.dir/link.txt` | 0.1 KB | Build Artifact |
| `CTestTestfile.cmake` | `build/base_debug/tools/ui/CTestTestfile.cmake` | 0.3 KB | Build Artifact |
| `cmake_install.cmake` | `build/base_debug/tools/ui/cmake_install.cmake` | 1.5 KB | Build Artifact |

---

### C. 🧪 Test Executables & Unit Test Suite (41 Files)

| Test Binary | Relative File Path | File Size | Target Status |
| :--- | :--- | :--- | :--- |
| `test-alloc` | `build/base_release/bin/test-alloc` | 49.1 KB | Discovered / Ready |
| `test-arg-parser` | `build/base_release/bin/test-arg-parser` | 54.5 KB | Discovered / Ready |
| `test-autorelease` | `build/base_release/bin/test-autorelease` | 17.8 KB | Discovered / Ready |
| `test-backend-ops` | `build/base_release/bin/test-backend-ops` | 1.14 MB | Discovered / Ready |
| `test-backend-sampler` | `build/base_release/bin/test-backend-sampler` | 105.8 KB | Discovered / Ready |
| `test-barrier` | `build/base_release/bin/test-barrier` | 25.7 KB | Discovered / Ready |
| `test-c` | `build/base_release/bin/test-c` | 15.4 KB | Discovered / Ready |
| `test-chat` | `build/base_release/bin/test-chat` | 1.23 MB | Discovered / Ready |
| `test-chat-auto-parser` | `build/base_release/bin/test-chat-auto-parser` | 769.4 KB | Discovered / Ready |
| `test-chat-peg-parser` | `build/base_release/bin/test-chat-peg-parser` | 708.1 KB | Discovered / Ready |
| `test-chat-template` | `build/base_release/bin/test-chat-template` | 255.9 KB | Discovered / Ready |
| `test-col2im-1d` | `build/base_release/bin/test-col2im-1d` | 21.3 KB | Discovered / Ready |
| `test-gbnf-validator` | `build/base_release/bin/test-gbnf-validator` | 26.5 KB | Discovered / Ready |
| `test-gguf` | `build/base_release/bin/test-gguf` | 79.6 KB | Discovered / Ready |
| `test-gguf-model-data` | `build/base_release/bin/test-gguf-model-data` | 206.2 KB | Discovered / Ready |
| `test-grammar-integration` | `build/base_release/bin/test-grammar-integration` | 229.8 KB | Discovered / Ready |
| `test-grammar-parser` | `build/base_release/bin/test-grammar-parser` | 36.2 KB | Discovered / Ready |
| `test-jinja` | `build/base_release/bin/test-jinja` | 750.6 KB | Discovered / Ready |
| `test-json-schema-to-grammar` | `build/base_release/bin/test-json-schema-to-grammar` | 412.0 KB | Discovered / Ready |
| `test-llama-archs` | `build/base_release/bin/test-llama-archs` | 60.6 KB | Discovered / Ready |
| `test-llama-grammar` | `build/base_release/bin/test-llama-grammar` | 41.1 KB | Discovered / Ready |
| `test-log` | `build/base_release/bin/test-log` | 17.9 KB | Discovered / Ready |
| `test-model-load-cancel` | `build/base_release/bin/test-model-load-cancel` | 16.1 KB | Discovered / Ready |
| `test-mtmd-c-api` | `build/base_release/bin/test-mtmd-c-api` | 16.5 KB | Discovered / Ready |
| `test-opt` | `build/base_release/bin/test-opt` | 61.9 KB | Discovered / Ready |
| `test-peg-parser` | `build/base_release/bin/test-peg-parser` | 1.02 MB | Discovered / Ready |
| `test-quant-type-selection` | `build/base_release/bin/test-quant-type-selection` | 242.5 KB | Discovered / Ready |
| `test-quantize-fns` | `build/base_release/bin/test-quantize-fns` | 17.1 KB | Discovered / Ready |
| `test-quantize-perf` | `build/base_release/bin/test-quantize-perf` | 40.8 KB | Discovered / Ready |
| `test-quantize-stats` | `build/base_release/bin/test-quantize-stats` | 226.8 KB | Discovered / Ready |
| `test-reasoning-budget` | `build/base_release/bin/test-reasoning-budget` | 30.7 KB | Discovered / Ready |
| `test-recurrent-state-rollback` | `build/base_release/bin/test-recurrent-state-rollback` | 39.5 KB | Discovered / Ready |
| `test-regex-partial` | `build/base_release/bin/test-regex-partial` | 58.0 KB | Discovered / Ready |
| `test-rope` | `build/base_release/bin/test-rope` | 20.9 KB | Discovered / Ready |
| `test-sampling` | `build/base_release/bin/test-sampling` | 55.2 KB | Discovered / Ready |
| `test-save-load-state` | `build/base_release/bin/test-save-load-state` | 49.2 KB | Discovered / Ready |
| `test-state-restore-fragmented` | `build/base_release/bin/test-state-restore-fragmented` | 34.9 KB | Discovered / Ready |
| `test-thread-safety` | `build/base_release/bin/test-thread-safety` | 40.7 KB | Discovered / Ready |
| `test-tokenizer-0` | `build/base_release/bin/test-tokenizer-0` | 51.3 KB | Discovered / Ready |
| `test-tokenizer-1-bpe` | `build/base_release/bin/test-tokenizer-1-bpe` | 27.2 KB | Discovered / Ready |
| `test-tokenizer-1-spm` | `build/base_release/bin/test-tokenizer-1-spm` | 22.8 KB | Discovered / Ready |

---

### D. 📝 Separated Log & Telemetry Files (5 Files)

| Log File Name | Subsystem Path | File Size | Format |
| :--- | :--- | :--- | :--- |
| `build_debug_260720_0932_001.log` | `logs/debug/build_debug_260720_0932_001.log` | 9.0 KB | Build Log |
| `telemetry_260720_0843_001.csv` | `logs/telemetry_260720_0843_001.csv` | 0.5 KB | CSV Telemetry |
| `telemetry_260720_0843_001.jsonl` | `logs/telemetry_260720_0843_001.jsonl` | 1.3 KB | JSONL Session |
| `test_results_260720_0934_001.csv` | `logs/tests/test_results_260720_0934_001.csv` | 4.2 KB | CSV Telemetry |
| `test_run_260720_0934_001.log` | `logs/tests/test_run_260720_0934_001.log` | 26.1 KB | Build Log |

---

## 🔒 3. Out-of-Tree Separation Policy Verification

- **Log Separation Invariant**: All test execution logs, build journals, and hardware telemetry outputs are strictly written into `logs/` and `logs/subdirectories/`, completely isolated from `build/`.
- **Root Directory Hygiene Invariant**: No temporary test scripts, build objects, or log outputs are located in the repository root.
