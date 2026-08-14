# Haiku Canonical Destroy

## Overview

A destroy board authored to match the fixed canonical brief for trial run B120. Designed as a one-island destroy map with the monument in the open, forest closing the west flank, a hill on the east for bridging approaches, a village behind the monument, and a void channel in front.

## Board Layout

**Dimensions:** 120×160 blocks, `rot_180` symmetry  
**Base surface:** y9, build ceiling y20  
**Surface range:** y8..26

### Pieces

- **Spawn**: 40×30 blocks, surface 9 — spawn room and iron renewal
- **Spawn approach**: 40×10 blocks, surface 10 — stepping up from spawn to village
- **Village**: 50×20 blocks, surface 10 — settlement area with stone buildings
- **Plaza**: 40×20 blocks, surface 9 — open monument area
- **Hill East**: 30×30 blocks, surface 17 — bridging approach from east
- **Forest West**: 25×30 blocks, surface 9 — cover on west flank
- **Void buffer**: 30×15 blocks — twenty-block-wide void channel in front (cuts to bedrock)

## Gameplay

**Monument placement:** In the open center of the plaza on both halves. Obsidian `cube-3` style with 4-block float.

**Approaches:**
- **Around**: The void channel forces players around the east or west sides
- **Above**: The hill provides bridging height on the east side
- **Through**: The village settlement gives cover when attacking from the side
- **Below**: No depression approach; players must commit to a side

**Attacked team defense:** Can hold from the village and plaza, with the hill providing flank security.

## What Worked

- Basic plan compiles cleanly with rot_180 symmetry
- Monument float and positioning work as intended
- The void channel cuts cleanly and has the stated 20-block width
- Stone brick and stone themes apply without issues
- Spawns and iron placement are correct

## Known Limitations

1. **No relief authoring** — all shapes stand at authored base_heights; no terrain sculpting to make approaches organic
2. **Minimal dressing** — only grass flora on a single radius; no trees, boulders, or path dressing
3. **Themes are reused** — all three shapes use the same stone/dirt theme; per-shape theming was not implemented
4. **Simple geometry** — all pieces remain rectangles; no polygons or organic outlines
5. **No defence walls** — no bedrock structure on the village/monument seam

## Plan Slug

`haiku-canonical-destroy-3`

This was the first buildable version of the canonical brief.
