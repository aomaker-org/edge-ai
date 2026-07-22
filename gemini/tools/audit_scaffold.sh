#!/usr/bin/env bash
# ==============================================================================
# Multi-Repo Scaffold & Git Auditor
# Target Repos: edge-ai, irislime, fekerr-dev
# Destination: gemini/captures/
# ==============================================================================

set -e

SRC_DIR="${HOME}/src"
TARGET_REPOS=("edge-ai" "irislime" "fekerr-dev")

GEMINI_DIR="${SRC_DIR}/edge-ai/gemini"
CAPTURES_DIR="${GEMINI_DIR}/captures"
mkdir -p "$CAPTURES_DIR"

TIMESTAMP=$(date -u +'%Y%m%d_%H%M%S_UTC')
OUT_FILE="${CAPTURES_DIR}/${TIMESTAMP}_multi_repo_scaffold.md"
CANONICAL_FILE="${GEMINI_DIR}/LATEST_SCAFFOLD.md"

{
  echo "# Multi-Repository Scaffold & Git Snapshot"
  echo "**Generated:** $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
  echo "**Host Environment:** WSL2 Ubuntu ($(hostname))"
  echo ""
  echo "---"
  echo ""

  for repo in "${TARGET_REPOS[@]}"; do
    REPO_PATH="${SRC_DIR}/${repo}"
    echo "## Repository: \`${repo}\`"
    echo ""

    if [ ! -d "$REPO_PATH" ]; then
      echo "> **Warning:** Directory \`${REPO_PATH}\` does not exist."
      echo ""
      continue
    fi

    cd "$REPO_PATH"

    echo "### 1. Git Status & Working Tree"
    echo '```text'
    git status --short --branch
    echo '```'
    echo ""

    echo "### 2. Remotes"
    echo '```text'
    git remote -v
    echo '```'
    echo ""

    echo "### 3. Branches (Local & Remote)"
    echo '```text'
    git branch -a -v
    echo '```'
    echo ""

    echo "### 4. Recent Commit History (Last 10)"
    echo '```text'
    git log --graph --oneline --decorate -n 10
    echo '```'
    echo ""

    echo "### 5. Submodules"
    echo '```text'
    if [ -f ".gitmodules" ]; then
      git submodule status
    else
      echo "No .gitmodules present."
    fi
    echo '```'
    echo ""

    echo "### 6. Directory Scaffold (Depth 3)"
    echo '```text'
    if command -v tree &> /dev/null; then
      tree -a -I '.git|__pycache__|.venv|venv|node_modules|target|build|dist|.pytest_cache|.DS_Store' -L 3 .
    else
      find . -maxdepth 3 -not -path '*/.*'
    fi
    echo '```'
    echo ""
    echo "---"
    echo ""
  done
} > "$OUT_FILE"

cp "$OUT_FILE" "$CANONICAL_FILE"

echo "Scaffold audit written to:"
echo "  Artifact:  $OUT_FILE"
echo "  Canonical: $CANONICAL_FILE"
