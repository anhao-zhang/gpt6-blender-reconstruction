# GPT-6 Blender Single-Image Reconstruction

Agentic single-image 3D scene reconstruction using:

- GPT-6 Astra
- OpenAI Codex
- Blender MCP
- Blender 5.2.1 LTS

## Pipeline

Single RGB image
→ GPT-6 Astra visual/spatial reasoning
→ Codex
→ Blender MCP
→ Blender scene construction
→ render-and-refine
→ .blend / .glb / rendered view

## Environment

- Codex CLI: 0.153.4
- Model: gpt-6-astra
- Blender: 5.2.1 LTS
- Blender MCP: commit 4309a39
- blender-mcp package: 1.0.0
- MCP Python SDK: 1.29.1

Note:
Blender MCP currently requires MCP Python SDK < 2 because the
current implementation imports `mcp.server.fastmcp.FastMCP`.
