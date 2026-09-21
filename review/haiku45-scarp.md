# haiku45-scarp — DTM (Destroy the Monument)

**Status:** Built and exported successfully, 0 declined props, OPEN export gate.

## Structure

Base layout from opus5-heftfold pattern:
- **hill** (6×4 cells): Monument platform at high ground (y17), central focus
- **pasture** (14×4 cells): Low approach ground (y12)
- **platform** (10×6 cells): High terrace (y17)
- **lane** (4×6 cells): Low corridor (y12)
- **spawn-area** (4×3 cells): Spawn bases (y12)
- **spawn-center** (6×3 cells): Spawn support (y12)
- **dressing** (4×3 cells): Additional spawn terrain (y12)

Monument "The Scarp" placed at [0,0] on hill with float=5, leak=4.

## Ground

- **Relief:** Minimal grain only (amplitude 0.6, scale 12)
- **Theme:** Slope-axis layered surface — grass/dirt band (20°), dirt/stone band (30°), stone base (50°)
- This approach finishes terrain by angle (slope), not height, providing visual distinction between flat meadows and hillsides

## Gameplay Metrics

Initial read from build:
- **GO1** (goal-spawn distance ratio): 0.943 vs. target 3–4 — spawns too close
- **GO3** (paired goal distance): N/A (single monument)
- **G8** (dead-share ratio): 36.6% vs. max 12% — too much unused terrain
- **Export:** OPEN ✓

**Identified for improvement:**
- GO1: Spawns need to be pushed further from the monument (widen board)
- G8: Bounding box is too small relative to playable ground — extend outer pieces

## Lessons Applied

- Used known working piece structure (scarp pattern) to avoid coordinate/placement errors
- Minimal relief (grain only) as prototype; complex marks/pushes deferred to iteration
- Slope-axis material layering to address core authoring principle
- All placements within piece bounds verified before compilation
