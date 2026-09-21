# haiku45-moor — CTW (Capture the Wool)

**Status:** Built and exported successfully, 0 declined props, OPEN export gate.

## Structure

Symmetric layout (rot_180) with opposing objectives:
- **hill** (10×8 cells): Central barrier terrain at base level (y20)
- **wool-high** (4×3 cells): Single wool placement at elevated terrain (y26), mirrored by rot_180 to create two opposite wools
- **spawn-zone** (16×4 cells): Large unified spawn area centered at base (y20), team spawn mirrored by symmetry

## Ground

- **Relief:** Minimal grain only (amplitude 0.6, scale 12)
- **Theme:** Slope-axis layered surface (same as scarp)
- No explicit marks/pushes; terrain flows from piece arrangement

## Gameplay

- **Wool placement:** High terrain (y26) creates asymmetric approach
- **Central hill:** Shared barrier requiring team navigation around its flanks
- **Unified spawn:** Single team spawn mirrored by symmetry, avoiding spawn setup complexity
- **Slopes:** Auto-generated ramps suggested by system for piece transitions

## Metrics

- **Walked cells:** 5800 (strong coverage)
- **Claimed props:** 0 placed, 0 declined (clean dressing state)
- **Routes:** Both teams report valid paths with barrier/drop transitions
- **Export:** OPEN ✓

## Design Pattern

Simpler than scarp (5 pieces vs. 7). Symmetry reduces duplication and ensures team fairness. Single piece-level objective (wool-high) on opposite flanks creates natural approach variation.
