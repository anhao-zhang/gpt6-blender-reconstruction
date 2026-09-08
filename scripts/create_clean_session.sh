#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <output.blend>"
    exit 1
fi

OUTPUT="$(realpath -m "$1")"

blender \
    --background \
    --online-mode \
    --python-expr "
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.save_as_mainfile(filepath=r'$OUTPUT')
"

echo "Created clean Blender session:"
echo "$OUTPUT"
