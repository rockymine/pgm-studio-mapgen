# 05 — a stair out of plan pieces

**The technique: elevation stated on the plan, as one piece per tread — and the two things nothing will tell
you about it.**

`02-theme`'s one `field` piece is cut back to `z −50..10`, and the twenty blocks between there and the spawn
camp become four pieces one cell deep, each a block higher than the last. The camp and the terraces either
side of it stand on top of them.

## The plan diff, in full

```json
{ "id": "field",     "role": "piece", "rect": [-10, -10, 20, 12] },
{ "id": "tread-1",   "role": "piece", "rect": [-10,   2, 20,  1], "surface": 10 },
{ "id": "tread-2",   "role": "piece", "rect": [-10,   3, 20,  1], "surface": 11 },
{ "id": "tread-3",   "role": "piece", "rect": [-10,   4, 20,  1], "surface": 12 },
{ "id": "tread-4",   "role": "piece", "rect": [-10,   5, 20,  1], "surface": 13 },
{ "id": "terrace-w", "role": "piece", "rect": [-10,   6,  8,  4], "surface": 13 },
{ "id": "terrace-e", "role": "piece", "rect": [  2,   6,  8,  4], "surface": 13 },
{ "id": "camp",      "role": "spawn", "rect": [ -2,   6,  4,  4], "surface": 13 }
```

**Pieces may not overlap where their surfaces differ** — `PL4` refuses that outright — so the flight is not
laid *over* the field, it is cut *out* of it. That is what turns two pieces into eight, and it is the honest
cost of stating elevation on a plan: a step is a piece, and a piece takes its ground from its neighbours.

That is the whole of it. `surface` overrides the global height for one piece, and **the compiler makes one
shape per distinct height within a component**, so four pieces become four polygons:

```
s0  h  9   the field                      s3  h 12   tread-3
s1  h 10   tread-1                        s4  h 13   tread-4 fused with the terraces and the camp
s2  h 11   tread-2
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
GET …/column?at=20,z          the flight, one read per tread
  z  8   y  8  Grass Block      the field
  z 12   y  9  Stone Bricks     tread-1
  z 17   y 10  Andesite         tread-2
  z 23   y 11  Stone Bricks     tread-3
  z 27   y 12  Andesite         tread-4
  z 32   y 12  Andesite         the terrace the camp stands on, same shape
```

The cut is at `x 20` rather than at `x 0` because the cairn floats over the axis at `(0, 22)` and a column
read there answers the objective, not the ground. The flight runs the full width of the board, so any `x`
clear of the objectives and the spawn pads reads the same six values.

## The two things nothing tells you

**`EL1` complains, and it is right about the corpus and wrong about a stair.**

```
[complaint] EL1  piece 'tread-1' surface delta 1 is not a multiple of 2
[complaint] EL1  piece 'tread-3' surface delta 3 is not a multiple of 2
```

`GET /api/rules?rule=EL1` gives its evidence: over 137 measured **land-interface** deltas in the authored
seed corpus, every one is even, because the surface palette is base 9 plus even steps.

**The lint measures something else, and this board is the proof.** `PlanValidator.LintEl1` takes
`piece.surface − globals.surface`, not the delta across an interface — so on a flight whose every interface
delta is 1 it flags `tread-1` (delta 1 from the global) and `tread-3` (delta 3) and stays silent about
`tread-2` and `tread-4`. Half a uniform flight complained about and half not is not a judgement about the
flight; it is the wrong quantity. Filed as `G231` on `pgm-studio`'s backlog.

Even measured correctly it would be the wrong question here: EL1's evidence is where one *plateau* meets
another, and a stair is not two plateaus. Taking the complaint at face value produces the next fault, which
is:

**One gate does tell you a step is too tall, and it only looks at one step.** Building this flight with
deltas of **2** — four risers of two blocks, which no player can walk up — draws exactly one finding, from
the *last* riser:

```
[complaint] SP8  spawn egress steps 2 blocks at 'tread-2'–'camp'
                 — use 1-level steps or a ramp against the spawn
```

`SP8` reads the step **out of a spawn** and nothing else. Move the two-block riser three treads down the
flight — `field 9 · tread-1 10 · tread-2 12 · tread-3 13 · tread-4 14 · camp 15` — and it goes silent, while
`EL1` complains about tread-1, tread-2 and tread-4 and says nothing about the riser that is actually two
blocks tall:

```
POST /plan/evaluate   score 0  valid true
  [lint] EL1  piece 'tread-1' surface delta 1 is not a multiple of 2
  [lint] EL1  piece 'tread-2' surface delta 3 is not a multiple of 2
  [lint] EL1  piece 'tread-4' surface delta 5 is not a multiple of 2
```

Three complaints, none of them about the step, and the one gate that would have named it is looking at the
other end of the flight.

Traversability does not catch it either, and the reason is in the walk's own docstring: `WalkGround.Steps`
asks only whether the vertical span fits under the clearance over the lower place — *"On a board with nothing
stacked over it every place has open sky, so this never refuses a step."* It models a player **who can place
blocks**, which is correct for a capture board where the strait is crossed by bridging and wrong as a test of
whether a stair is a stair.

**Walkability is the author's, everywhere except the one step out of a spawn.** The read that settles it is a
column transect up the flight, and it is the only one that does.

## The granularity is the cell, and the cell is a choice

A tread here is **five blocks deep**, because a plan piece is a rectangle on a cell grid and this board's
`globals.cell` is 5. **Five is the default, not the unit** — `cell` is an ordinary field and takes 7, or 3,
or 1, and at `cell: 1` a piece is a single block and a flight of twenty one-block treads is a plain plan.

What it is not is a *local* choice. `cell` is one number for the whole board, so the granularity a stair
wants is also the granularity every other piece is counted in: at `cell: 1` this board's `field` stops being
`[-10, -10, 20, 12]` and becomes `[-50, -50, 100, 60]`, and every rectangle on the board is stated in
blocks. That is a real way to author — the traced corpus plans do it at other scales — and
it is a decision about the whole document rather than about the stair.

So the honest statement of the trade is: **a fine flight is reachable from the plan by making the whole board
fine, or from the layout by drawing one shape.** `06-ramp-and-slant` is the same twenty blocks stated the
second way, on a board that keeps `cell: 5` everywhere else.

The two are meant to share a board. A stepped quarter that is plainly built, against a solved quarter that is
plainly a hillside, is what `tools/seeds/ruediger.plan.json` does with 31 pieces at ten heights.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-section-x0.png` | the flight in elevation, which is the only view a riser has |
| `renders/world-heightmap.png` | the four tiers as bands right across the board |
| `renders/theme-tread-section.png` | one tread's nosing over its riser |
| `02-theme/renders/world-heightmap.png` | the same board flat |

**A section is taken along the axis the cut runs**, and `at` is the other coordinate: `axis=x&at=0` runs
down the board's length and crosses every tread, which is the cut this flight wants.

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, 2 × `EL1` complaint — see above; `G231` |
| shapes | 5 compiled — one per height — against `02`'s 1 |
| flight | 4 treads · 1 block rise · 5 block going · terrace at y12 |
| `GET …/preflight` | export gate **OPEN**, `SP8` silent — the last tread and the camp are level |
