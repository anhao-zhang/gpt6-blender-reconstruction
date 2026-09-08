# Environment

## Codex
- Codex CLI: 0.153.4
- Model: gpt-6-astra
- Baseline reasoning effort: low

## Blender
- Blender: 5.2.1 LTS
- Install path: /amax/zhanganhao/tools/blender-5.2.1
- User resources: /amax/zhanganhao/blender_user

## Blender MCP
- Official repo path: /amax/zhanganhao/tools/blender-mcp-official
- Baseline commit: 4309a39
- blender-mcp package: 1.0.0
- mcp SDK: 1.29.1

## Important compatibility note
Blender MCP currently requires MCP Python SDK < 2 because the current implementation imports:
`mcp.server.fastmcp.FastMCP`

## MCP bridge
- Host: localhost
- Port: 9876

## Baseline restrictions
Allowed:
- GPT-6 Astra visual/spatial reasoning
- Blender MCP
- Blender primitives/modifiers/direct editing
- iterative refinement

Not allowed:
- external 3D assets
- external 3D generation models
- segmentation/depth/point cloud/registration pipeline
