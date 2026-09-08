#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <session.blend>"
    exit 1
fi

SESSION="$1"

blender \
    --background \
    --online-mode \
    "$SESSION" \
    --command blender_mcp
