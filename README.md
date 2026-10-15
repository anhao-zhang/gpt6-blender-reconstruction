# GPT-6 Blender Single-Image Reconstruction

**Agentic 3D scene reconstruction from a single RGB image using GPT-6 Astra, OpenAI Codex, Blender MCP, and Blender.**

This repository documents experiments in which a multimodal agent interprets a tabletop image, constructs an approximate 3D scene in Blender using tools, then iteratively inspects and refines the rendered result. The emphasis is on **visual/spatial reasoning, tool use, and iterative scene editing**, rather than training a dedicated 3D reconstruction model.

## Results

### Experiment 1 — Multi-object tabletop scene


| Input image | Reconstructed render |
|:---:|:---:|
| <img src="experiments/reconstruct_001/inputs/test_im1.png" width="450"> | <img src="experiments/reconstruct_001/previews/reconstruction_final.png" width="450"> |


The agent approximates the tabletop, background, and visible objects (including a bottle, headphones, mouse, and pens), together with their relative placement, scale, and camera viewpoint.

### Experiment 2 — Scene with significant occlusion


| Input image | Reconstructed render |
|:---:|:---:|
| <img src="experiments/reconstruct_001/inputs/image_occ8.png" width="450"> | <img src="experiments/reconstruct_001/previews/image_occ8_render_final.png" width="450"> |

This experiment focuses on partially occluded objects, front-to-back ordering, approximate hidden geometry, and overall scene consistency.

**Scope:** These are qualitative reconstruction demonstrations from two input images, not a quantitative benchmark. Geometry, materials, and invisible surfaces are inferred and may differ from the real scene.

## Approach

1. **Scene interpretation:** GPT-6 Astra analyzes the input image, identifying visible objects, approximate geometry, spatial relationships, and likely camera viewpoint.
2. **Tool-based construction:** Codex operates Blender through Blender MCP to create and edit scene geometry, materials, lighting, and the camera.
3. **Render and inspect:** Blender renders the current scene so the agent can assess visible mismatches.
4. **Iterative refinement:** The agent adjusts scene geometry, object placement, appearance, and camera parameters over a bounded number of iterations.
5. **Experiment logging:** Prompts, configuration, selected execution traces, and final rendered previews are retained for inspection.

The experiments use Blender primitives, modifiers, and direct scene editing. They do **not** use external 3D assets, external 3D generation models, segmentation, depth prediction, point clouds, or registration pipelines.

## Experimental configuration

| Component | Configuration |
|---|---|
| Model | GPT-6 Astra (`gpt-6-astra`) |
| Reasoning effort | `low` |
| Agent interface | OpenAI Codex CLI 0.153.4 |
| 3D environment | Blender 5.2.1 LTS |
| Tool bridge | Blender MCP (commit `4309a39`; package 1.0.0) |
| MCP SDK | 1.29.1 |
| Refinement budget | Up to 5 iterations |

See [environment details](configs/environment.md) and [experiment metadata](experiments/reconstruct_001/metadata.json).

## Repository contents

| Path | Description |
|---|---|
| [`prompts/`](prompts/) | Base and occlusion-aware reconstruction prompts |
| [`experiments/reconstruct_001/inputs/`](experiments/reconstruct_001/inputs/) | Two input RGB images |
| [`experiments/reconstruct_001/previews/`](experiments/reconstruct_001/previews/) | Final rendered previews |
| [`experiments/reconstruct_001/trajectories/`](experiments/reconstruct_001/trajectories/) | Selected agent interaction and tool-execution traces |
| [`experiments/reconstruct_001/metadata.json`](experiments/reconstruct_001/metadata.json) | Experiment configuration and input/output mapping |
| [`scripts/`](scripts/) | Blender session setup, MCP launch, and trajectory extraction utilities |
| [`configs/environment.md`](configs/environment.md) | Software versions and environment notes |

## Reproduction notes

This repository records the experimental workflow and supporting utilities; **it is not a one-command end-to-end reconstruction package**.

Prerequisites include a compatible Blender installation, Blender MCP, Codex access to GPT-6 Astra, and a working MCP connection. The experiment used the versions listed above. The MCP Python SDK requirement is **version < 2** for the recorded Blender MCP implementation.

To prepare a Blender session on a suitably configured machine:

```bash
bash scripts/create_clean_session.sh /path/to/session.blend
bash scripts/start_blender_mcp.sh /path/to/session.blend
```

Then, in a Codex session configured to use the Blender MCP tools, supply an input image and the relevant prompt template:

- [Standard reconstruction prompt](prompts/reconstruction_base.md)
- [Occlusion-aware reconstruction prompt](prompts/reconstruction_occlusion.md)

The model-driven scene-building and refinement steps are interactive/tool-mediated; the repository does not currently include a fully automated launcher for those steps. The recorded trajectories can be inspected to understand the experiments.

## Limitations

- **Single-view ambiguity:** Object dimensions, hidden surfaces, and materials cannot be uniquely determined from a single RGB image.
- **Geometric inaccuracies:** Reconstructed objects may have inaccurate shapes, proportions, scales, or spatial arrangements compared with the reference image.
- **Object interpenetration:** Some reconstructed objects may intersect or penetrate one another, indicating limitations in the agent's understanding of 3D geometry and physical constraints.
- **Limited physical consistency:** Although the agent can approximate visible scene layouts, the generated geometry does not always satisfy realistic spatial and physical constraints.

This is an exploratory, tool-using 3D scene reconstruction project built on existing models and Blender tooling, not a claim of a novel trained reconstruction model.
