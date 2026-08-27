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
      "points": [[-34,28],[-34,12],[-34,-4],[-34,-18],[-34,-28]],
      "h": [9,8,6,4,2], "r": 5 }
  ] } },
"dressing": { "props": [
  { "kind": "water", "id": "sedge-1", "points": [[-34,28],[-34,12]], "radius": 3, "depth": 2, "form": "natural", "seed": 31 },
  { "kind": "water", "id": "sedge-2", "points": [[-34,12],[-34,-4]], "radius": 3, "depth": 2, "form": "natural", "seed": 32 },
  { "kind": "water", "id": "sedge-3", "points": [[-34,42],[-34,28]], "radius": 3, "depth": 2, "form": "natural", "seed": 33 },
  { "kind": "water", "id": "sedge-4", "points": [[-34,28],[-34,18]], "radius": 3, "depth": 2, "form": "stream",  "seed": 34 }
] }
```

`valley` runs down the board's west flank at `x −34`, from `z 28` to the coast at `z −28`. It is written
**after** `strand`, which is the whole of what makes a river possible here (below).

## A line's `h` is one number per vertex, and `r` is a radius

`valley` states five heights against five points, one per vertex: 9, 8, 6, 4, 2, run from the source
(`z 28`) down to the mouth (`z −28`, the coast). The solver interpolates linearly along the drawn arc between
them, so the ground itself falls in a smooth ramp rather than in the five discrete shelves the vertex list
might suggest — `08-cliff`'s ramp marks state the same fact for a climb; this states it for a descent.
`r: 5` is a radius exactly as a point mark's is: the constrained band reaches 5 blocks either side of the
centerline, so the valley `line` writes is **10 blocks wide**, confirmed at `z −4` by the columns below —
ambient y6 holds out to `x −44`, the cut runs from `x −40` to `x −28`, and ambient resumes beyond it. The
edges soften over a block or two because the relaxation is what carries them, not a second mechanism.

## The mouth: why `valley` has to be written after `strand`

`strand` states one flat height, 9, right across the board at `z −28` — the level ground the objectives and
the spawn beyond them stand on. Marks resolve in order and the last one wins a contested cell, so writing `valley`
*after* `strand` lets the river's own five-block band **override** that flat bank wherever the two cross,
cutting a inlet through it, while every other block of `strand` stays exactly as flat as `07-hill` and
`08-cliff` leave it. Measured at `z −28`: `x −20` (clear of the river) holds `strand`'s **y8**, untouched;
`x −38` and `x −30` (either edge of the river's own band) both read **y1**, the river's own mouth height, cut
straight through. The rule already stated for a rim and a summit — write the constraint every cell defaults to
first, the feature that needs an exception to it after — is exactly what a river's mouth needs, read the other
way round: reversing the order would let `strand` win at the coast, which dams the river flat at y8 one block
short of the sea — the ground never "runs uphill," but the water sitting behind that dam would have nowhere
to go, which is the practical shape the question takes.

## What went wrong first

Write one `water` prop with its points running the whole course, source to mouth, in a single centerline and
the river becomes a lake. `WaterBed`'s water line is not per-cell: it is the **single lowest ground surface**
the whole prop's band touches, and every column under the band fills to that one line regardless of where
along the run it sits. Over a course whose relief falls from 9 to 2, the entire 56-block run pools dead flat
at the mouth's own level:

| z along the course | with one prop, source to mouth | with four chained props |
|---|---|---|
| 28 (source) | y1 — flooded to the mouth's own level | **y8** |
| 12 | y1 | **y4** |
| −4 | y1 | **y2** |
| −18 | y1 | **y1** |
| −28 (mouth) | y1 | **y1** |

A relief that falls seven blocks reads as one motionless lake, because the fall is real in the ground and
invisible in the water sitting on it — and the export gate answers **OPEN** either way, so nothing but the
column read tells them apart. The fix is not a field on the prop — there is no field that varies a channel's
level along its own length — but **four separate props**, one per stretch between consecutive valley
vertices, each pooling at its own low end. The result is a staircase, not a slope: each reach is flat
within itself and steps down 1–2 blocks into the next, which is what the numbers above show and what a
`section` along the course shows as a run of terraces rather than a ramp.

## The ford: a graded bed crosses a route without a bridge

The west flank is a way across the board, so the river crosses it. A perpendicular read at `z −4` (a
`water: natural` reach) shows the bed step down and back up either side of a flat pool floor — y6 grass,
y5 coarse dirt, **y2 water** for six blocks, y4 gravel, y5 grass, y6 grass — never more than two blocks
between adjacent columns and mostly one. `WalkGround.Steps` reads exactly that delta and nothing about what block sits on
top of it, so a graded U-shaped bed crosses as a shallow ford rather than a wall, and `coverage` and
`preflight` both come back exactly as `02-theme`'s do: `coverage` counts cells, not height, so it is
unmoved by a relief that only reshapes ground it already owned, and `traversability` reports the spawn ↔
objective chain **still connected**, because nothing on this crossing exceeds the one-block step the walk
already tolerates elsewhere.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-topdown.png` | the river down the flank on both teams' territory, reaching the void at the coast — water is one of the five categories this render separates |
| `GET …/render/section?axis=z&at=-34&from=-40&to=40&scale=6` | the whole course in one cut — flat reaches stepping down, not a ramp |
| `GET …/render/section?axis=x&at=-28&from=-50&to=0&scale=10` | the notch the river cuts through the otherwise-flat strand, right at the coast |
| `renders/world-heightmap.png` | the valley as the one "under water" band on an otherwise flat board |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| `POST …/sketch/relief/read` | cells 10 000 · low **2** · high 9 · relief 7 · symmetry error 0 |
| `GET …/column?at=-34,28…-28` (source → mouth) | **y8 → y8 → y4 → y4 → y2 → y2 → y1**, flat reaches, not a slope |
| `GET …/column?at=-20,-28` vs `at=-38,-28` | strand **y8** clear of the river, **y1** at either edge of its own band |
| ford at `z −4`, `x −44 → −24` | y6 · y5 · **y2 (water, 6 blocks)** · y4 · y5 · y6 |
| `GET …/coverage` | 75.5% dead — unchanged from `02-theme`; coverage counts cells, not height |
| `GET …/preflight` | export gate **OPEN**, traversability spawn ↔ objective **connected** |
