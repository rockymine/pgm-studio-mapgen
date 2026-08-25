# 14 — a water course down a valley

**The technique: a river is two statements that agree — a relief `line` mark whose `h` falls along its arc,
and a chain of `water` props laid into the cut it makes. A single long `water` prop cannot show a fall at
all; the course has to be several, each pooling at its own low point.**

The plan is `02-theme`'s, untouched, renamed **Sedgewater**. The finish gains a `relief` block on island
`team` and four chained `water` props.

## The document

```json
"relief": { "team": {
  "base": 9, "reach": 20, "step": 1, "stairs": true,
  "marks": [
    { "id": "coast",  "kind": "rim",  "h": 9, "depth": 1 },
    { "id": "strand", "kind": "line", "points": [[-40,18],[0,18],[40,18]], "h": [9,9,9], "width": 5 },
    { "id": "valley", "kind": "line",
      "points": [[-34,73],[-34,58],[-34,42],[-34,28],[-34,18]],
      "h": [9,8,6,4,2], "r": 5 }
  ] } },
"dressing": { "props": [
  { "kind": "water", "id": "sedge-1", "points": [[-34,73],[-34,58]], "radius": 3, "depth": 2, "form": "natural", "seed": 31 },
  { "kind": "water", "id": "sedge-2", "points": [[-34,58],[-34,42]], "radius": 3, "depth": 2, "form": "natural", "seed": 32 },
  { "kind": "water", "id": "sedge-3", "points": [[-34,42],[-34,28]], "radius": 3, "depth": 2, "form": "natural", "seed": 33 },
  { "kind": "water", "id": "sedge-4", "points": [[-34,28],[-34,18]], "radius": 3, "depth": 2, "form": "stream",  "seed": 34 }
] }
```

`valley` runs down the same west-flank corridor `07-hill` and `09-mesa-and-hollow` use for their own
landforms — the 15-block-wide strip of real ground between the coast and the island's own interior void. It
is written **after** `strand`, which is the whole of what makes a river possible here (below).

## A line's `h` is one number per vertex, and `r` is a radius

`valley` states five heights against five points, one per vertex: 9, 8, 6, 4, 2, run from the source (z 73,
deep in team territory) down to the mouth (z 18, the coast). The solver interpolates linearly along the
drawn arc between them, so the ground itself falls in a smooth ramp rather than in the five discrete shelves
the vertex list might suggest — `08-cliff`'s ramp marks state the same fact for a climb; this states it for a
descent. `r: 5` is a radius exactly as a point mark's is: the constrained band reaches 5 blocks either side of
the centerline, so the valley `line` writes is **10 blocks wide**, confirmed at z 42 by the columns below —
ambient height (y8) holds until x −38, the cut runs from there to x −31, and ambient resumes at x −30. Seven
to nine blocks of visible cut against a nominal ten is the relaxation's own edge softening the band's stated
one, not a second mechanism.

## The mouth: why `valley` has to be written after `strand`

`strand` states one flat height, 9, across the entire 80-block width at z 18 — the level bank both teams need
to bridge the strait. Marks resolve in order and the last one wins a contested cell, so writing `valley`
*after* `strand` lets the river's own five-block band **override** that flat bank wherever the two cross,
cutting a inlet through it, while every other block of `strand` stays exactly as flat as `07-hill` and
`08-cliff` leave it. Measured at z 18: `x −20` (clear of the river) holds `strand`'s **y8**, untouched;
`x −38` and `x −30` (either edge of the river's own band) both read **y1**, the river's own mouth height, cut
straight through. The rule already stated for a rim and a summit — write the constraint every cell defaults to
first, the feature that needs an exception to it after — is exactly what a river's mouth needs, read the other
way round: reversing the order would let `strand` win at the coast, which dams the river flat at y8 one block
short of the sea — the ground never "runs uphill," but the water sitting behind that dam would have nowhere
to go, which is the practical shape the question takes.

## What went wrong first

The first build carried one `water` prop, its points running the whole course from the source (z 73) to the
mouth (z 18) in a single centerline. `WaterBed`'s water line is not per-cell: it is the **single lowest
ground surface** the whole prop's band touches, and every column under the band fills to that one line
regardless of where along the run it sits. With one prop spanning a course whose relief fell from height 9 to
height 2, the entire 55-block run pooled dead flat at the mouth's own level:

| z along the course | with one prop, source to mouth | with four chained props |
|---|---|---|
| 73 (source) | y3 — flooded to the mouth's own level | **y6** |
| 58 | y3 | **y6** |
| 42 | y3 | **y4** |
| 28 | y3 | **y2** |
| 18 (mouth) | y3 | **y1** |

A relief that falls six blocks read as one motionless lake, because the fall was real in the ground and
invisible in the water sitting on it. The fix was not a field on the prop — there is no field that varies a
channel's level along its own length — but **four separate props**, one per stretch between consecutive
valley vertices, each pooling at its own low end. The result is a staircase, not a slope: each reach is flat
within itself and steps down 1–2 blocks into the next, which is what the numbers above show and what a
`section` along the course shows as a run of terraces rather than a ramp.

## The ford: a graded bed crosses a route without a bridge

The west flank is one of the board's own ways in, so the river crosses it. A perpendicular read at z 42 (a
`water: natural` reach) shows the bed step down and back up in single blocks either side of a flat pool
floor — y8 ambient, y5 bank, y4 water surface for six blocks, y5 bank, y8 ambient — never more than one block
between adjacent columns. `WalkGround.Steps` reads exactly that delta and nothing about what block sits on
top of it, so a graded U-shaped bed crosses as a shallow ford rather than a wall, and `coverage` and
`preflight` both come back exactly as `02-theme`'s do: `coverage` counts cells, not height, so it is
unmoved by a relief that only reshapes ground it already owned, and `traversability` reports the spawn ↔
objective chain **still connected**, because nothing on this crossing exceeds the one-block step the walk
already tolerates elsewhere.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-topdown.png` | the river down the flank on both teams' territory, reaching the void at the coast — water is one of the five categories this render separates |
| `renders/section-river-profile.png` | the whole course in one cut — four flat terraces stepping down, not a ramp |
| `renders/section-mouth-x18.png` | the notch the river cuts through the otherwise-flat strand, right at the coast |
| `renders/world-heightmap.png` | the valley as the one "under water" band on an otherwise flat board |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| `POST …/sketch/relief/read` | cells 4 125 · low **2** · high 9 · relief 7 · symmetry error 0 |
| `GET …/column?at=-34,73…18` (source → mouth) | **y6 → y6 → y4 → y2 → y1**, four flat reaches, not a slope |
| `GET …/column?at=-20,18` vs `at=-38,18` | strand **y8** clear of the river, **y1** at either edge of its own band |
| ford at z 42, x −40 → −26 | y8 · y5 · **y4 (water, 6 blocks)** · y5 · y8 — never more than one block of step |
| `GET …/coverage` | 3.3% dead — unchanged from `02-theme`; coverage counts cells, not height |
| `GET …/preflight` | export gate **OPEN**, traversability spawn ↔ objective **connected** |
