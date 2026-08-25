# 19 — a mountain range around an open board

**The technique: a range of mountains drawn entirely with `pushes`, on a board whose playing ground stays a
single open dale. The instrument is the push's `crown`, `falloff` and per-vertex `amounts`; the discipline is
that nothing a player stands on is pinned by a mark.**

This is the only showcase that does not fork `02-theme`'s plan. The board is `elderwold`-shaped instead: four
nested rectangles down one half, mirrored by `rot_180`, compiling to **one** shape — an open landmass with no
cut-outs, because a destroy board played across a set of separated pads is not played across anything. The
plan is 19 lines, and every decision in this folder is in the finish.

## The document

```json
"relief": { "team": {
  "base": 12, "reach": 0, "step": 1, "stairs": true,
  "grain": { "amplitude": 2.0, "scale": 13, "seed": 5 },
  "marks": [
    { "id": "coast", "kind": "rim",  "h": 12, "depth": 1 },
    { "id": "dale",  "kind": "line", "points": [[0,2],[-4,24],[3,46],[-2,66],[0,84]],
                     "h": [12,13,14,15,16], "r": 18 },
    { "id": "shelf", "kind": "area", "h": 18, "ring": [ …lobed ring, 9 vertices… ] },
    { "id": "apron", "kind": "area", "h": 16, "ring": [ …lobed ring, 11 vertices… ] }
  ],
  "pushes": [
    { "id": "massif-w", "ring": [ …ribbon round the west spine, 12 vertices… ],
      "amount": 30, "amounts": [10,26,17,30,19,12,12,19,30,17,26,10],
      "falloff": 11, "roughness": 0.38, "crown": 13, "seed": 3 },
    { "id": "spur-w",   "ring": [ … ], "amount": 14, "amounts": [7,13,8,14,14,8,13,7],
      "falloff": 8, "roughness": 0.38, "crown": 7, "seed": 11 },
    { "id": "corrie-w", "ring": [ …lobed ring, 9 vertices… ],
      "amount": 3, "falloff": 7, "roughness": 0.3, "crown": -9, "seed": 21 }
  ]
} }
```

Four marks and six pushes — a massif, a spur and a corrie on each side. The whole range is the pushes.

## How the mechanism works

### A mark is a constraint, so a mark cannot make a mountain

`docs/world-export/relief.md` §2 states it and the board proves it: a mark is a statement that *the ground
here is this height*, honoured exactly, with no falloff. A `point` at `h 47, r 8` therefore does not build a
summit — it builds a **drum**: a flat disc eight blocks across standing on a twenty-block sheer wall, because
nothing tells the ground between the disc and its surroundings what to do except the relaxation, and the
relaxation has one cell to do it in. A `line` mark with per-vertex heights is the same failure stretched: a
ridge-shaped wall with a flat top.

Both were built here before the pushes were, and `renders/` keeps the reading: `low 11 · high 55`, a heightmap
of concentric squares, and a 3D preview of five white-capped oil drums. The relief numbers were right and the
landform was not, which is the reason this showcase exists beside `07-hill` rather than inside it.

### A push is the landform, and three of its numbers are the shape

A push takes a drawn ring and lifts the ground inside it, applying to the **solved** surface rather than into
it. Three fields do the work:

- **`amounts`** — one lift per ring vertex, interpolated along the ring's arc and wrapped, so the crest falls
  along the ring the way it was drawn. West runs `10 → 26 → 17 → 30 → 19 → 12` up the spine and back down the
  other side of the ribbon: two summits with a saddle between them, stated as six numbers.
- **`crown`** — how much higher the middle stands than the edge, where "the middle" is the ring's own **medial
  axis**. For a round ring that is a point and the crown domes it; for the long ribbon here it is a line, and
  the crown puts a crest on it. This is the single field that separates a mountain from a mesa, and its record
  default is `0`. A push authored without it is a plateau.
- **`falloff`** — the skirt, measured as distance from the ring **across the land**. On a 90-block-wide board
  this is the number that decides whether there is a map left: at `20` the two massifs' skirts met in the
  middle and the dale was a 20-block ditch; at `11` the flat ground runs `x −18 … +15`.

`roughness` wobbles the skirt against a noise field so it is not a clean offset of the ring — the difference
between a hill and an extruded logo — and a **negative crown** dishes the ring instead of doming it, which is
what `corrie-w` and `corrie-e` are: a bowl bitten out of each massif's inner flank at `(±36, 44/50)`, reading
43 against a 53 rim.

### Pin only the ground that is stood on

The four marks are the coast, the dale floor, the goal's shelf and the spawn's apron — every one of them
ground a player has to walk. Nothing else is pinned, and that is the whole of the second lesson: a mark
written over a region *because the region should be about that height* leaves the solver nothing to solve, and
a board with a mark on every region is a table with bumps on it however tall the bumps are. The flanks here
carry no mark at all; they are whatever the pushes make of the relaxation between the rim and the dale.

`reach: 0` is the other half. A finite reach pulls ground back toward `base` at that distance from any
constraint, which on a board this size means the flanks decay to 12 between the marks and the range is a row
of separate hills.

### An `area` mark's ring is a shape, and a rectangle looks like one

`shelf` and `apron` are `area` marks — genuinely flat ground, which is what they are for. Written as
rectangles they built two mesas with four sheer sides, visible in the heightmap as literal squares. The same
marks on a nine- and eleven-vertex lobed ring are indistinguishable from ground. The mark did not change; only
its outline did.

### A brush stroke is clamped into the land, and derived from the spine

The 20 strokes — snow on the four summits, crag along the crests, flank below them, the two saddles and the
spawn's sward — are ordinary one-course adds, and every vertex is clamped inside the board's tiered outline
before it is written. A stroke reaching past the land is the only add on that column and builds a **speck of
bedrock standing over the void**: before the clamp, `/coverage` reported `141 cells at (-24, 91), 364 blocks
from used ground` — a disconnected island made of paint. Afterwards every dead patch is `1 block from used
ground`.

They are also placed *off the spines* rather than typed as coordinates, which is what makes the range
tunable at all: moving `SPINE_W` outward by six blocks moved four summits, and the snow moved with them.

## What to look at

| Render | Shows |
|---|---|
| `renders/world-heightmap.png` | the range as a contour map — two chains, four summits, the saddles, and the dale running the length of the board between them |
| `renders/sec-x-z20.png`, `sec-x-z56.png`, `sec-x-z80.png` | the profile across both massifs at three places: the silhouette is the push's crown |
| `renders/world-surface.png` | where each theme landed, and the stair courses the slopes are built from |
| `renders/world-traversability.png` | the dale is one connected floor; the massifs are scenery |

## What it measures

```
island team: cells 6762 · low 11 · high 64 · relief 53 · symErr 0
export gate OPEN
coverage: reached 10239 · dead 3231 of 13470 = 24.0% dead,
          every dead patch 1 block from used ground
```

Transect at `z = 44`, every third block from `x = −45`:

```
 0  0 41 44 47 56 50 38 27 16 13 13 13 13 13 13 13 13 13 13 13 21 36 47 55 57 57 57 56  0  0
```

**24% dead is the range itself** and is the honest cost of the technique: a mountain is scenery, and scenery
is ground no journey passes. On a board this size the range is a quarter of it. That is the number to carry
into a real map — the same pushes on a 200-block board are a frame around a playing field rather than half
the field.

## Limits

The valley floor is flat because the `dale` mark pins it flat, and a flat floor is what an open destroy board
wants; a floor with landform in it wants pushes of its own with a small `amount` and a positive `crown`, and
then the walkability of every route has to be re-read per block. The snowline is painted, not derived —
`themeByHeight` keys on a compiled shape's `base_height`, not on the solved elevation, so there is no theme
bucket that says "above 40" (`07`, `10`).
