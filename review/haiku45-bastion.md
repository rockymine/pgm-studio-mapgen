# haiku45-bastion — Mixed (Wool + Monument)

**Status:** Built and exported successfully, 0 declined props, OPEN export gate.

## Structure

Combined objectives on fortified terrain:
- **tower** (4×4 cells): Central ground structure (y20)
- **monument-peak** (2×1 cells): Elevated platform for monument (y30)
- **wool-platform** (3×3 cells): Side ledge for wool capture objective (y27)
- **rampart-left** (3×4 cells): Defense terrace (y22)
- **spawn-zone** (10×3 cells): Unified spawn area (y20)

Monument "The Bastion" (obsidian, float=2, leak=1) on monument-peak.
Wool on wool-platform (mirrored by symmetry for both teams).

## Ground

- **Relief:** Minimal grain (amplitude 0.6, scale 12)
- **Theme:** Slope-axis layered surface
- Piece arrangement creates natural elevation flow: spawn → tower/rampart → wool-platform/monument-peak

## Gameplay Concept

Dual-objective design requiring teams to both defend/assault the monument (high difficulty, central) and capture the wool (medium difficulty, offset). Monument float/leak values reduced (2/1) compared to DTM to account for additional complexity.

Elevation asymmetry (wool at y27, monument at y30) creates approach variety.

## Metrics

- **Walked cells:** 3200 (reasonable coverage for mixed mode)
- **Claimed props:** 0 placed, 0 declined
- **Routes:** Both teams report valid barrier/drop transitions
- **Export:** OPEN ✓

## Challenges Solved

- **Piece overlap:** Initial design had overlapping pieces with different surfaces (PL4 error). Resolved by carefully separating pieces and adjusting z-coordinates.
- **Symmetry coordination:** Using rot_180 symmetry required ensuring all objectives mirrored correctly and spawn zone centered.
