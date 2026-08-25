# 05 — a stair out of plan pieces

**The technique: elevation stated on the plan, as one piece per tread — and the two things nothing will tell
you about it.**

`02-theme`'s `rise` — the flat 20-block strip between the lane and the wool room — becomes four pieces one
cell deep, each a block higher than the last, and the room stands on top of them.

## The plan diff, in full

```json
{ "id": "tread-1", "role": "piece", "rect": [4, 15, 3, 1], "surface": 10 },
{ "id": "tread-2", "role": "piece", "rect": [4, 16, 3, 1], "surface": 11 },
{ "id": "tread-3", "role": "piece", "rect": [4, 17, 3, 1], "surface": 12 },
{ "id": "tread-4", "role": "piece", "rect": [4, 18, 3, 1], "surface": 13 },
{ "id": "room",  "role": "wool-room", "rect": [4, 19, 3, 3], "surface": 13 }
```

That is the whole of it. `surface` overrides the global height for one piece, and **the compiler makes one
shape per distinct height within a component**, so four pieces become four polygons:

```
s0  h  9   the island                     s3  h 12   tread-3
s1  h 10   tread-1                        s4  h 13   tread-4 fused with the room's ground
s2  h 11   tread-2                        s5  —      the hole
```

Those ids are what the paint keys on. The board reaches Sketch as a flight, not as a grid of rectangles.

## The flight reads as masonry because each tread is its own shape

A tread is a plateau one block above the one below it, so it has all three of a theme's geometric buckets:
a **surface** (the going), a **rim** where it drops (the nosing) and a **wall** under that (the riser).

```json
"themeById": { "s1": "tread", "s2": "tread-alt", "s3": "tread", "s4": "tread-alt" }
```

Two themes alternating: Stone Bricks going with a Sandstone nosing, Andesite going with an End Stone nosing,
both over a riser of one course of Andesite on two of Cobblestone. The flight reads as built rather than as
a slope that happens to be quantised, and that costs two theme entries and four keys.

```
GET …/column?at=27,z          the flight, one read per tread
  z 74   y  8  Grass Block      the lane
  z 78   y  9  Stone Bricks     tread-1
  z 83   y 10  Andesite         tread-2
  z 88   y 11  Stone Bricks     tread-3
  z 93   y 12  Andesite         tread-4
  z 100  y 12  …                the wool room's plinth, same shape
```

## The two things nothing tells you

**`EL1` complains, and it is right about the corpus and wrong about a stair.**

```
[complaint] EL1  piece 'tread-1' surface delta 1 is not a multiple of 2
[complaint] EL1  piece 'tread-3' surface delta 3 is not a multiple of 2
```

`GET /api/rules?rule=EL1` gives its evidence: over 137 measured land interfaces in the authored seed corpus,
every delta is even, because the surface palette is base 9 plus even steps. That is a measurement of
**plateau** deltas — where one piece of ground meets another — and a stair is not two plateaus. Taking the
complaint at face value here produces the next fault, which is:

**The export gate will not tell you a step is too tall.** The first build of this board used deltas of **2**
— four risers of two blocks, which no player can walk up. Everything passed:

| Read | Answer on the 2-block flight |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, **no `EL1`** — the deltas were even |
| `GET …/preflight` | `traversability: spawn ↔ objective chain connected` · **export gate OPEN** |
| `GET …/coverage` | 3.3% dead, unchanged |

The board was measurably unwalkable and four gates said it was fine. The reason is in the walk's own
docstring: `WalkGround.Steps` asks only whether the vertical span fits under the clearance over the lower
place — *"On a board with nothing stacked over it every place has open sky, so this never refuses a step."*
It models a player **who can place blocks**, which is correct for a capture board where the strait is crossed
by bridging and wrong as a test of whether a stair is a stair.

**Walkability is the author's.** The read that settles it is a column transect up the flight, and it is the
only one that does.

## The granularity is the cell

A tread here is **five blocks deep**, because a plan piece is a rectangle on a cell grid and `globals.cell`
is 5. That is right for a flight of four and wrong for a flight of twelve: the plan cannot state a one-block
tread at all. The layout can — it is drawn in blocks — and `06-ramp-and-slant` is the same twenty blocks
stated there instead.

The two are meant to share a board. A stepped quarter that is plainly built, against a solved quarter that is
plainly a hillside, is what `tools/seeds/ruediger.plan.json` does with 31 pieces at ten heights.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-section-z0.png` | — the wrong cut; the flight is at x 27 |
| `GET …/render/section?axis=z&at=27&from=68&to=112&scale=10` | the flight in elevation, which is the only view a riser has |
| `renders/world-heightmap.png` | the four tiers from above |
| `renders/theme-tread-section.png` | one tread's nosing over its riser |

**A section is taken along the axis the cut runs**, and `at` is the other coordinate: `axis=z&at=27` cuts
down the stair. `axis=x&at=27` cuts across the board at z 27 and answers `RQ5 nothing stands along that cut`.

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, 2 × `EL1` complaint |
| shapes | 6 compiled — one per height — against `02`'s 2 |
| flight | 4 treads · 1 block rise · 5 block going · room plinth at y12 |
| `GET …/preflight` | export gate **OPEN** |
