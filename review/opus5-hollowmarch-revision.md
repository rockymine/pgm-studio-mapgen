# Hollowmarch — what the revision changed, and what it measured

The board's own record is `review/opus5-hollowmarch.md`, written when it was built. This is what a later
pass found and fixed. Read them in that order: the first says what the board is, this says where it and
the world had come apart.

## The whole finish was keyed on ids that named nothing

Nine keys, `s0`–`s8`, from before `TS82` made a compiled shape's id its component's first piece plus the
surface it stands at. Every one of them was dead, so on any re-drive:

- **the drawn coast was absent** — `s0` carries a 49-vertex outline for the team island and `s8` a
  32-vertex one for the middle island, and both fell back to the compiler's rectangles;
- **all seven `relief_scope: hold` pads were absent**, so the spawn and the two wool approaches were in
  the solve instead of standing over it, and the relaxation fought them.

Paired against the committed layout: every bounding box agrees, except `s8`'s, whose own vertices grow the
island past the rectangle it compiles from — which is why an automatic pairing would have refused it and
left it alone.

## The relief was thrown away and rebuilt

The first pass calmed it; the author's ruling was to take it out entirely and start again, on the rough
plan with no drawn coast on it. Both Bézier outlines are gone and the ground is the compiler's own
rectangles.

Bare, the board is flat and perfect: **no barriers, no scrambles, every row crossable on foot**, and four
blocks of range, which is the held pads standing over it. Everything below is what was added back to that.

**The instrument is `step: 1` with `stairs: true`.** The surface snaps to whole courses, so every height
change is one block and is walked, and the stair pass cuts a way up wherever the terracing would strand a
player. `step: 2` was measured beside it: it terraces just as cleanly — barriers go to zero either way —
and every bench then costs a placed block, which read as **0 of 15 rows crossable on foot**. One is
walked, two is climbed, and that is the whole difference.

**Four marks, not twelve.** One `area` per place that is a different level and none for anything else:

| mark | what it does |
|---|---|
| `front-fall` h11 | the frontline falls three courses toward the middle, a course at a time |
| `lane-wool-a` h15 | the north lane climbs out of the hub to the wool approach held at 16 |
| `lane-wool-b` h15 | the same for the west lane |
| `lane-spawn` h15 | the same for the spawn's |

**Held pads exactly one course apart.** Two held pads side by side cannot be ramped between, so the
difference between them *is* the step: the three rooms came down from 18 to 17, one over the approaches at
16, and `wool-b-t2` from 17 to 16 to join the same run.

`reach` 20 over a 110-block board so the grading is spread; grain 0.8 at a period of 20 so it rides on the
steps without adding one.

| | before | first pass | now |
|---|---|---|---|
| team range | 15 | 8 | **6** |
| team barriers · scrambles | 185 · 184 | 94 · 83 | **0 · 0** |
| rows on foot, x · z | 1/15 · 0/10 | 5/15 · 10/10 | **15/15 · 10/10** |
| the island | 9 range, 50 barriers | flat | **flat, every row walked** |
| the world, `03-slopes` | 6725 walked · 655 scrambled · 645 barrier · 20 faces | — | **8590 · 286 · 24 · 3 faces** |

The 24 barrier cells left are the crags, which is what a crag is.

## What the relief was before, and why it read as it did

`POST …/sketch/relief/read` said it in one line: **`RL2` — 15 blocks of range and 1.0 scrambles for every
barrier.** Ground that rolls keeps more scrambles than barriers; this kept the same of each. And of the
fifteen rows across the team island, **one** could be walked on foot; of the ten along it, **none**.

| | before | after |
|---|---|---|
| team range | 15 | **8** |
| team barriers · scrambles | 185 · 184 | **94 · 83** |
| team rows crossable on foot, x · z | 1/15 · 0/10 | **5/15 · 10/10** |
| team cliffs | 1 | **0** |
| neutral range | 9 | **0** |
| neutral barriers | 50 | **0** |
| `RL2` | fires on both islands | **silent** |

What did it, in the order that mattered:

- **The four pushes went.** A push is added to the solved surface, and four of them at amount 3–4 with a
  crown of 2–3 are what put a swell on every part of the board that had no landform of its own. Taking
  them out halved the range, 15 → 8.
- **The middle island got a relief group of its own.** It had none, so it was solved on defaults and came
  out with 50 barriers and no row crossable on foot. A group with a flat base and a quiet grain makes it
  level: range 0, no barriers, every row walked.
- **Two pads came down a course.** `spawn-t1` and `wool-a-t1` stood at 17 over ground at 14 — a three-block
  ring, which is a wall, not a step. At 16 the same ring is a scramble. The board's own record says each
  pad is "exactly one block over the pad it is reached from"; it was three.
- The five crag pads at 17/18/20 went. The crags themselves are `addShapes` and are untouched — they are
  the board's identity — but each pad put a second cliff under one.

The relief marks the evaluator offers for a `Δ≥2` seam were tried and **made it worse** (barriers 88 → 140,
rows on foot 6 → 0): a line mark at the pad's own height, on ground the solve wants lower, pulls a ridge
the length of the mark. On a board whose pads are `hold`, the seam is graded by lowering the pad, not by
marking the ground.

## The crossing zone reached past everything it docked

`BZ9`, on the plan tier: **30 blocks of `mid-band` stood beyond the last ground it meets.** The zone spanned
`x −40..40` and the pieces it docks against reached `±25`.

In the world it read as the fault it is. The drawn coast dipped a block short of the zone's north edge at
each leg tip — vertices at `(−15, 31)` and `(10, 31)` on a zone ending at row 29 — so between the ground a
player stands on and the zone they may build in lay a row of void that is neither. Nothing on the board
says so; the column read does.

Fixed in three places, and the plan tier now raises nothing at all:

- `mid-isle` is the island as it is actually drawn, `x −30..30`, and the zone is `x −30..30` with it.
- The island's coast is pulled back to `z ±15` from `z ±20`, so the strait is the 15 the plan states rather
  than the 10 the drawing had made it.
- The legs are **15 blocks wide** where they were 10 (`FR9`), and their tips are drawn straight and flush at
  `z = 30`. Read back at `(−18, 28..31)`: void, void, ground, ground — the ground's first row abuts the
  zone's last with nothing between them.

## Also found and fixed

- `HS3` — both room styles capped a spruce roof with an oak slab. The half-course slab continues the body.
- `HS7` — both foundations ringed a one-course plate with a footing, which is a rim round nothing.
- `RQ3` — `relief.team.stairs` is a field no part of the document has.
- `SK13` — a crag reached one column the compiler's own void cut takes away.
- `SP9` — the spawn door opened onto void with nothing ahead of it. `facing: "left"` opens it onto the
  approach.
- The plan was version 1, so none of this could be re-driven until its markers were restated in blocks.

## Read and left

- `SP2` — the spawn sits on the island's east flank rather than at the back of its lane. That is the
  composer's own arrangement and moving it is a different board.
- `EL1` on six seams and `WL11` on one, all `Δ2` — scrambles, which is what the palette steps by and what
  `RL2` asks a rolling board to keep.
- `WX11` on the two wool rooms' entrance redstone, standing where the land stops: the ledge case the rule
  names as the one to ignore.
