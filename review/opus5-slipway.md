# Slipway — a harbour DTM, and what the goal rules make of a board

`specs/opus5-slipway`, driven `2026-08-29`. 256 × 240 blocks, `rot_180`, 28 players, two destroyables a
team. Score **0**, valid, symmetry error **0**, and nothing the dressing pass declined.

## The board's size is the goal rules, not a preference

Four bands govern where a destroy goal may stand, and solved together they fix the board's dimensions before
a single piece is drawn. `GO4` holds a goal 40–90 blocks from its own spawn by walk; `GO1` holds the enemy
walk at 3–4× that; `GO3` holds opposing goals 85–150 apart and `GO2` a team's own pair 35–65. Writing the
spawn separation as `S` and the goal's own walk as `d`, the ratio fixes `d ≈ S/2` and `GO3` then reads
`≈ 2d = S`, so **`S` lands in [85, 150] and every other band follows**. There is no small board that
satisfies them.

What the sweep found, over goal offset and town depth:

| own walk | ratio | GO2 | GO3 | in band |
|---|---|---|---|---|
| 56 | 3.20 | 40 | 126–142 | **all four** |
| 60 | 3.18 | 40 | 134–150 | at the ceiling |
| 64 | 2.92 | 40 | 126–142 | GO1 under |
| 66 | 2.85 | 48 | 126–145 | GO1 under |

The board is drawn to the first row: goals at ±20 blocks either side of the axis, 60 blocks out from a spawn
100 blocks back. That is a spawn-to-spawn walk of 238 blocks and a board 240 deep.

## What it carries

Made things, each stated a different way, which is the point of the board:

| thing | blocks | layers | shapes | how it meets the ground |
|---|---|---|---|---|
| ship | 8,897 | 8 | 598 | floats — an absolute floor at the load line, no seat |
| balloon ×2 | 3,195 | 8 | 1,160 | flies — an absolute floor, no seat |
| crane ×2 | 810 | 4 | 107 | `seat: ground` — settles onto the quay the relief left |

Beside them: eight houses a side from the style library, twenty-one trees, three roads, and a harbour.

## The harbour, measured

The basin floor is at y5 and the water line is stated at y16. Read off `sketch/columns`:

| where | what the column holds |
|---|---|
| open harbour (−60, 0) | seabed to y5, **water y6–16** |
| under the ship amidships (0, 0) | seabed to y5, **water y6**, hull y7–20 |
| under the ship, fore (−20, 0) | seabed to y5, **water y6**, hull y7, **water y8**, hull y9–20 |
| alongside the hull (0, 10) | seabed to y5, water y6–16 |
| quay (−60, 32) | ground to y21 |

**9,602 columns hold water.** Before the fill went round what floats in it the count was 8,682 and the
column under the ship read a dry gap at y6 — a ship sitting in a hole.

## What the board taught

- **A ground style built from wool is unplantable.** `all green` mixes wool into its palette, the dressing
  pass reads wool as a stamp's own block, and every tree on it is declined `DR-KEEP` as built ground rather
  than terrain. The town and ridge take `grass clay surface` instead, which is clay throughout.
- **The dressing pass fans its own props.** A hand-placed rot_180 image of a house lands on the ground the
  automatic image already claimed and is declined `DR-CLAIM`. Sculptures are `addLayers` and are placed by
  hand; houses and trees are stated once.
- **`HP3` caps a placed building at 192 blocks of footprint, inclusive of both corners** — a 12 × 14 plot is
  195 and refuses. A dock town is many small sheds.
- **`LN2` measures a chain of collinear rects, not a piece.** Rects sharing a cross-axis interval and
  abutting merge into one lane however many pieces they are written as, so a 192-block waterfront written as
  four pieces is still one 192-block lane. The basins sit either side of a slipway and the quays either side
  of that: 80 blocks the longest run.
- **A made thing raises the build ceiling**, which is the highest column plus twenty. The balloons crown at
  y96, so the ceiling is 116 rather than the 52 the terrain alone would give.
