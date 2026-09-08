You are connected to a running Blender instance through Blender MCP.

Your task is to reconstruct a 3D tabletop scene from a single input image.

Input image:
{{INPUT_IMAGE}}

Goal:
Build a 3D scene in Blender that matches the input image as closely as possible from the camera view.

Requirements:
1. Inspect the input image carefully.
2. Start from a clean scene.
3. Reconstruct the tabletop / desk surface and background plane.
4. Reconstruct all major visible objects.
5. Infer approximate geometry, position, rotation, scale, and camera viewpoint.
6. Use Blender primitives, modifiers, and direct editing only.
7. Do not use external 3D assets.
8. Do not use external 3D generation models.
9. Refine iteratively for up to 5 rounds.
10. Save the final Blender scene and at least one rendered preview.

Important:
- Actually perform the reconstruction through Blender MCP tools.
- Do not merely output Blender Python code as text.
