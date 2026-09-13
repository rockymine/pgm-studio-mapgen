# Curved outlines

Outlines that are not made of straight edges. Each is one island of ground on the `ground` layer, one shape in a
group of its own with `mirrors: false` on a board whose `mirror_mode` is `none`, `base_height: 9`, painted with the same `meadow` theme as `flat-ground`.
Open it in the studio as `technique-curved-outlines`, or read `curved-outlines.layout.json`.

| Island | Where | Stated as | Cells |
|---|---|---|---|
| `island-circle` | centre (10, 10) | a `circle`: `center_x`, `center_z` and `radius` 10. The studio draws it as a 64-sided polygon | 320 |
| `island-lasso` | around (44, 10) | a `lasso` of 16 points. In the document a lasso is a polygon; the difference is the canvas, which traces it freehand and simplifies the trace at a four-block tolerance | 308 |
| `island-bowed` | x 68–88, z 0–20 | a square `polygon` whose north edge is bowed out by two handles: `"0": {"out": [74.67, -6]}` and `"1": {"in": [81.33, -6]}` | 458 |
| `island-rounded` | x 102–122, z 0–20 | the same square with an `in` and an `out` handle at every corner, making one smooth ring through all four corners — it swells past the square's edges | 500 |

## Bézier handles

`controls` is keyed by a vertex's index as a string, and every handle is an absolute point on the board. The edge
from vertex *i* to vertex *i + 1* is a cubic curve from vertex *i*, pulled by `controls[i].out` and
`controls[i + 1].in`, to vertex *i + 1*. So a vertex's `out` bends the edge after it, and its `in` bends the edge
before it. The studio samples every curved edge 16 times, and the curve still passes through every vertex.

A ring rounded smoothly through its own vertices takes, at each vertex `P` with neighbours `previous` and `next`:
`in = P − (next − previous) / 6` and `out = P + (next − previous) / 6`. That is how `island-rounded` is stated.

## The one mistake

A handle that pulls further away from its edge than along it draws a loop, not a bulge. Keep each handle at
least as far along its edge as it is away from it, and the bulge under about a third of the edge's length:
`island-bowed` pulls 6 out on an edge 20 long, with each handle a third of the way along.

## What checks it

- `heightmap.txt` — the four outlines from above, two blocks to a character; the bowed edge reaches z −4.
- `section.txt` — the cut along x at z 10 through all four islands.
- `column.txt` — grass y8, dirt y7–6, stone y5–1, bedrock y0, at the circle's centre.
- `census.txt` — `meadow` on all 1,614 cells.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
