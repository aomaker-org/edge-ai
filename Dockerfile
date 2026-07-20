# ==============================================================================
# Dockerfile:  edge-ai Containerized Execution & Build Environment
# Target OS:   Ubuntu 24.04 LTS (Noble Numbat)
# Architecture: Out-of-tree builds (/workspace/build), zero-root-pollution
# ==============================================================================

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PROJECT_ROOT=/workspace \
    BUILD_DIR=/workspace/build \
    LOGS_DIR=/workspace/logs \
    AGY_DIR=/workspace/agy \
    PATH="/root/.local/bin:${PATH}"

# 1. Install system prerequisites and build toolchains
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    clang \
    cmake \
    ninja-build \
    make \
    git \
    python3 \
    python3-pip \
    curl \
    jq \
    clinfo \
    ccache \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Install uv toolchain manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Establish workspace root and out-of-tree output directories
WORKDIR /workspace
RUN mkdir -p /workspace/build /workspace/logs /workspace/agy

# 4. Copy repository contents
COPY . /workspace

# 5. Default build and verification entrypoint
CMD ["bash", "-c", "make build && make test"]
