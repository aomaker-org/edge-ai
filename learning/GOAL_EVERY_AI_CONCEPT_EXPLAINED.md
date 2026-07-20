# "Every AI Concept Explained Intuitively" Master Learning Goal (`GOAL_EVERY_AI_CONCEPT_EXPLAINED.md`)

This document incorporates the complete 38 AI topic breakdown from the landmark educational guide ***"Every AI Concept Explained Intuitively!"*** (YouTube ID: [`LlYcDGrnXeY`](https://youtu.be/LlYcDGrnXeY?si=smZn3mrlYMP9HFYQ)), deconstructing every algorithm and mapping it directly to the **`edge-ai`** system architecture.

---

## ⚡ 1. Concise 38-Topic Taxonomy & `edge-ai` Mapping (TL;DR)

| # | AI Concept / Topic | Domain Category | Mapped `edge-ai` Subsystem / Exercise |
| :---: | :--- | :--- | :--- |
| **1** | **Linear Regression** | Classical ML | Baseline predictive benchmark in `pyproject.toml` |
| **2** | **Logistic Regression** | Classical ML | Binary probability classifier in evaluation scripts |
| **3** | **Decision Trees & Random Forests** | Ensemble Learning | Tabular model validation in `tools/` |
| **4** | **Gradient Boosting (XGBoost)** | Ensemble Learning | Out-of-core tabular inference benchmark |
| **5** | **K-Means Clustering** | Unsupervised | Vector quantization for codebook generation |
| **6** | **Principal Component Analysis (PCA)** | Dimensionality Reduction | Embedding space visualization in `ai-log-diff/` |
| **7** | **Handcrafted Features (SIFT / ORB)** | Computer Vision | Legacy vision feature pipelines |
| **8** | **Word Embeddings (Word2Vec/GloVe)** | NLP Representation | Continuous dense vector co-occurrence |
| **9** | **Subword Tokenization (BPE/WordPiece)** | NLP Tokenization | `test-tokenizer-0`, `test-tokenizer-1-bpe` in `build/` |
| **10** | **Vector Databases & Cosine Similarity** | Information Retrieval | RAG indexing & nearest-neighbor search |
| **11** | **Perceptrons & MLPs** | Neural Core | Multi-layer feed-forward activation layers |
| **12** | **Backpropagation & AutoDiff** | Optimization | Automatic differentiation & gradient updates |
| **13** | **Convolutional Neural Networks (CNNs)** | Spatial Vision | Sliding kernel convolutions in vision backends |
| **14** | **RNNs & LSTMs** | Sequential Processing | Recurrent hidden state rollback (`test-recurrent-state-rollback`) |
| **15** | **Autoencoders** | Compression | Latent space bottleneck reconstruction |
| **16** | **Encoder-Decoder & Skip Connections** | Network Topology | U-Net spatial feature preservation |
| **17** | **Scaled Dot-Product Attention** | Transformer Core | Query-Key-Value matrix alignment |
| **18** | **Multi-Head Self-Attention** | Transformer Core | Parallel subspace attention in `irislime/llama.cpp` |
| **19** | **Positional Encodings (RoPE)** | Transformer Core | Rotary positional embeddings (`test-rope`) |
| **20** | **Masked Language Modeling (BERT)** | Pre-training | Bidirectional encoder pre-training |
| **21** | **Causal Language Modeling (GPT)** | Pre-training | Autoregressive next-token prediction in `llama-cli` |
| **22** | **Mixture of Experts (MoE)** | Model Architecture | Sparse router gating & expert dispatch |
| **23** | **Generative Adversarial Networks (GANs)** | Generative AI | Min-max generator-discriminator game |
| **24** | **Variational Autoencoders (VAEs)** | Generative AI | Probabilistic latent sampling & KL divergence |
| **25** | **Diffusion Models (DDPM / Latent)** | Generative AI | Noise-to-structure iterative denoising |
| **26** | **Multimodal Vision-Language (MTMD)** | Multimodal AI | Multimodal CLI binaries (`llama-mtmd-cli`, `libmtmd.so`) |
| **27** | **Audio & Speech Synthesis (TTS)** | Multimodal AI | Text-to-speech engine (`llama-tts` in `build/`) |
| **28** | **Q-Learning & Deep Q-Networks (DQN)** | Reinforcement Learning | Action-value function estimation |
| **29** | **Policy Gradient Methods (PPO / DPO)** | Reinforcement Learning | Direct preference optimization |
| **30** | **RLHF (RL from Human Feedback)** | Preference Alignment | Reward model training & alignment tuning |
| **31** | **Monte Carlo Tree Search (MCTS)** | Reasoning / Search | Heuristic search tree exploration |
| **32** | **Agentic Harness & Tool Use** | Agentic AI | AGY CLI, VS Code Copilot, Google Jules interop |
| **33** | **Retrieval-Augmented Generation (RAG)** | Grounded Generation | Dynamic knowledge base context injection |
| **34** | **Quantization (INT8/INT4/GGUF)** | Edge Compression | `llama-quantize` binary & GGUF format |
| **35** | **LoRA & PEFT Parameter Efficiency** | Fine-Tuning | `llama-export-lora` binary & adapter loading |
| **36** | **Speculative Decoding** | Runtime Acceleration | Dual-model draft generation (`llama-speculative`) |
| **37** | **KV Cache Management (PagedAttention)** | Memory Optimization | Dynamic Key-Value cache allocation |
| **38** | **Thermal Throttling & Power Awareness** | Edge Hardware | [tools/monitor_system_load.py](file:///home/fekerr/src/edge-ai/tools/monitor_system_load.py) (<50% CPU limit) |

---

## 🏛️ 2. Verbose Curriculum Deconstruction by Subsystem

### Section 1: Classical Machine Learning & Feature Space (Topics 1-10)
- **Mathematical Foundations**: Linear and logistic regression provide closed-form and gradient-descent optimization baselines. Tree ensembles (Random Forests, XGBoost) establish non-linear decision boundaries for tabular telemetry logs.
- **Dimensionality & Embeddings**: SIFT/ORB represent classical handcrafted computer vision features. Word2Vec and GloVe introduce continuous vector space semantics, paving the way for subword tokenization (BPE/WordPiece) evaluated in `test-tokenizer-0` and `test-tokenizer-1-bpe`.

---

### Section 2: Deep Learning & Attention Architectures (Topics 11-22)
- **Neural Core**: Multi-Layer Perceptrons and Backpropagation form the computational backbone. CNNs process 2D spatial features, while RNNs/LSTMs manage sequential memory (`test-recurrent-state-rollback`).
- **The Transformer Era**: Attention mechanisms replace recurrence by calculating pairwise Q-K-V token relevance. Positional Encodings (RoPE, tested in `test-rope`) inject sequence order into multi-head self-attention. BERT (Masked LM) and GPT (Causal LM) define bidirectional and autoregressive pre-training paradigms. Sparse Mixture-of-Experts (MoE) scales parameters while maintaining constant compute per token.

---

### Section 3: Generative, Multimodal & Agentic Systems (Topics 23-33)
- **Generative Frontiers**: GANs, VAEs, and Denoising Diffusion Models generate rich synthetic data. Multimodal systems integrate vision and language embeddings, mirrored by `edge-ai` multimodal binaries (`llama-mtmd-cli`, `libmtmd.so`) and speech synthesis (`llama-tts`).
- **Agentic AI & Reasoning**: Q-Learning, PPO, DPO, and RLHF align model outputs with human intent. Monte Carlo Tree Search (MCTS) enables multi-step planning. The Agentic Harness (context engineering, memory, tool usage) powers multi-agent collaboration across AGY CLI, GitHub Copilot, and Google Jules (`jules.google.com`).

---

### Section 4: Edge SLM Optimization & Thermal Throttling (Topics 34-38)
- **Quantization & LoRA**: `llama-quantize` converts 32-bit floating-point weights into 4-bit/8-bit GGUF structures, drastically reducing RAM bandwidth. `llama-export-lora` merges parameter-efficient adapters.
- **Runtime Acceleration**: Speculative decoding (`llama-speculative`) uses small draft models to accelerate target generation. KV Cache management prevents memory fragmentation during long-context processing.
- **Hardware Throttling**: Real-time load monitoring ([tools/monitor_system_load.py](file:///home/fekerr/src/edge-ai/tools/monitor_system_load.py)) enforces the strict **<50% laptop CPU/RAM load limit**, keeping hardware cool and quiet.
