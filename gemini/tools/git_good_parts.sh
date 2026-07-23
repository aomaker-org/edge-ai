#!/usr/bin/env bash
# ==============================================================================
# FILENAME BEGIN: gemini/tools/git_good_parts.sh
# ==============================================================================
# Utility: "Git: The Good Parts" Workspace Abstraction
# Description: Simplifies Git/Gix into 4 safe, high-level verbs:
#              save, status, sync, undo. Uses gix fast-paths when present.
# ==============================================================================

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GIX_BIN="${REPO_ROOT}/src/tools/gix_manifest/target/release/gix_manifest"

action="${1:-status}"
shift || true

case "$action" in
    save)
        msg="${*:-infra: sync workspace updates}"
        echo "================================================================================"
        echo " [GOOD PARTS] SAVING WORKSPACE SNAPSHOT"
        echo "================================================================================"
        "${REPO_ROOT}/gemini/git_update_convenience.sh" "$msg"
        ;;

    status)
        echo "================================================================================"
        echo " [GOOD PARTS] WORKSPACE STATUS AUDIT"
        echo "================================================================================"
        echo " Repo Root : ${REPO_ROOT}"
        echo " Branch    : $(git rev-parse --abbrev-ref HEAD)"
        echo " Engine    : $( [ -f "$GIX_BIN" ] && echo "gix (Fast Path)" || echo "canonical git" )"
        echo "--------------------------------------------------------------------------------"
        git status --short
        echo "================================================================================"
        ;;

    sync)
        echo "================================================================================"
        echo " [GOOD PARTS] GENERATING MANIFEST & ARCHIVE SYNC"
        echo "================================================================================"
        if [ -f "$GIX_BIN" ]; then
            echo "-> Running gix_manifest (Rust fast path)..."
            "$GIX_BIN"
        else
            echo "-> Running build_manifest.py (Python fallback)..."
            python3 "${REPO_ROOT}/gemini/tools/build_manifest.py"
        fi
        python3 "${REPO_ROOT}/gemini/tools/quick_sync.py"
        ;;

    undo)
        target="$1"
        if [ -z "$target" ]; then
            echo "Usage: ./gemini/tools/git_good_parts.sh undo <relative_file_path>"
            echo "Recent backups available in gemini/backups/:"
            ls -lt "${REPO_ROOT}/gemini/backups/" | head -n 10
            exit 1
        fi
        echo "Searching for latest safety backup for: ${target}..."
        clean_name="$(echo "$target" | tr '/' '_')"
        latest_bak="$(ls -t "${REPO_ROOT}/gemini/backups/"*"_${clean_name}.bak" 2>/dev/null | head -n 1 || true)"
        
        if [ -n "$latest_bak" ]; then
            echo "Restoring from provenance backup: $(basename "$latest_bak")"
            # Strip metadata provenance header (top 7 lines) during restore
            tail -n +8 "$latest_bak" > "${REPO_ROOT}/${target}"
            echo "Restored ${target} successfully!"
        else
            echo "No matching backup found in gemini/backups/. Falling back to git checkout..."
            git checkout -- "${target}"
        fi
        ;;

    *)
        echo "Usage: git_good_parts.sh {save|status|sync|undo}"
        exit 1
        ;;
esac

# ==============================================================================
# FILENAME END: gemini/tools/git_good_parts.sh
# ==============================================================================
