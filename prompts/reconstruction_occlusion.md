You are connected to a running Blender instance through Blender MCP.

Your task is to reconstruct a 3D tabletop scene from a single input image with significant occlusion.

Input image:
{{INPUT_IMAGE}}

Goal:
Build a 3D scene in Blender that matches the input image as closely as possible from the camera view.

Important reconstruction priorities:
1. Correctly identify visible objects and partially occluded objects.
2. Infer approximate occlusion relationships: which object is in front of which.
3. Infer hidden geometry conservatively. Do not invent unnecessary detail.
4. Prioritize global scene consistency, object layout, scale relationships, and camera viewpoint over fine-grained surface detail or exact branding/text.

Requirements:
1. Inspect the input image carefully.
2. Start from a clean scene.
3. Reconstruct the supporting environment:
   - tabletop / desk surface
   - background wall or vertical background plane
4. Reconstruct all major visible objects.
5. For each object, infer:
   - identity
   - approximate geometry
   - position
   - rotation
   - scale
6. Pay special attention to:
   - partial visibility
   - severe occlusion
   - front/back ordering
   - consistency of object sizes and placement
7. Use Blender primitives, modifiers, and direct scene editing only.
8. Do not use external 3D assets.
9. Do not use external 3D generation models.
10. Set up the camera so the rendered view resembles the input image.
11. Inspect the initial reconstruction and refine iteratively.
12. Perform up to 5 refinement iterations.

Output:
- Save the final Blender scene.
- Save at least one final rendered preview.
- GLB export is optional if Blender headless export fails.

Important:
- Actually perform the reconstruction through Blender MCP tools.
- Do not merely output Blender Python code as text.
- At the end summarize:
  - inferred objects
  - occlusion assumptions
  - camera assumptions
  - geometric assumptions
  - reconstruction limitations
