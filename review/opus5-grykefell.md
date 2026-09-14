# Grykefell — the ground is the cover

> A destroy-the-monument board on a limestone pavement fell. There is nothing built to hide behind
> anywhere on it: the cover is the rock itself — clints, grikes, a dry gill and one scar — and the
> monument stands in the open on a scoured slab with a different kind of approach onto it from each
> quarter.

**In one sentence:** the whole board is one material and one colour, and every decision on it is made
on the `slope` axis instead — where the pavement is flat you are seen, where it breaks you are not.

80 × 200 blocks, `rot_180`, cell 5, `maxPlayers` 24, ground y21–y36, observer y58. Two plan pieces,
five relief marks, two pushes, three themes, eight authored shapes, **36 props placed and none
declined**. `score 0`, `valid true`, nothing refused.

## The board is two pieces and a drawn coast

`fell` (16 × 15 cells) and `bield` (the spawn row, 6 × 3). That is the whole plan: the arrangement,
and nothing else. Every landform on the board is authored downstream, which is why there is no theme
per piece — there are only two pieces to hang one on.

**The frontline is not the rectangle's edge.** The plan's own run is `widthBlocks 80, profile
straight, z ±10` — a ruler across the board, and the tell the fault catalogue names. Sixteen vertex
inserts on `bield-24` answer it: eight of them draw the seaward edge as headland–bay–headland–bay–
headland and eight round the east and west coasts.

Measured on the built world at z 12, one block inland of the plan's line:

| x | −36 | −24 | −12 | 0 | 12 | 24 | 36 |
|---|---|---|---|---|---|---|---|
| ground at z 12 | y22 | void | y22 | y22 | void | void | y22 |

Three headlands stand at z 12 and four bays are still open water there. The crossing is therefore a
choice of place, not a width.

## What the ground is made of, and why it is not flat

`fell` carries 70.1% of the board, `turf` 27.5% and `scree` 2.4%. The pavement is the subject and it
is finished on the **slope** axis, and the board has a real angle distribution under it:

```
ground by angle:  00-09° 57.6%   10-19° 16.1%   20-29° 9.9%
                  30-39° 5.5%    40-49° 6.0%    50-59° 4.8%
11 987 cells sampled; 10.9% at 40° or steeper
```

No spike anywhere in it — a distribution with a spike is a board reporting its own `step` quantum
rather than its shape. A pavement fell is *meant* to be more than half flat; what matters is that the
other 43% is graded rather than cliffed, and it is.

`03-slopes.txt`: **10 905 cells walked, 438 scrambled, 644 barrier, 18 faces**, the largest 99 cells
at x 13..33 z −51..−30 — the scar, which is the board's one one-way approach and is supposed to be
impassable from below.

`POST …/sketch/relief/read`: `level 0.584`, `largestField 0.307`, **no seams and no silent marks**.
Five marks — two areas, a `line` for the gill, a `scarp` for the scar, one point — and not one pair of
them meets on a step taller than a scramble. That is the number the fault catalogue's "flat, one
theme, empty" row is really about, and the board passes it from the other side: it is flat *enough*,
with nothing ungraded in it.

## Six shelves of turf, and a wood that stands on soil

Three of the six birches stood on bare **Diorite** — `birk-0` (−36, 40), `birk-2` (−36, 76) and
`birk-5` (−26, 30) — and a tree growing out of pavement does not read. Two more shelves of `turf`
answer it, `turf-scarth` west of the gill and `turf-nab` on the northern shoulder, each placed where
soil would actually gather on a limestone fell: out of the weather, off the rock's own fall. One tree
moved, from (−26, 30) to (−30, 36), to reach the nearer of them.

Read back on the built world, the ground under every birch:

| tree | (−36,40) | (−34,58) | (−36,76) | (−30,68) | (−24,46) | (−30,36) |
|---|---|---|---|---|---|---|
| stands on | Grass | Grass | Grass | Grass | Grass | Grass |

The turf went from 15.4% of the board to 27.5%, and `fell | turf` from 449 border cells to 627.

## The barn stands on one ground level, and that is the whole fix

The barn was at x 16..33, z 24..34, and a transect across its cross wing read **`BARRIER +5 at
(18, 28)`**: y22 on the wing's west half and y27 on its east. The hillside ran through the building —
the only house in the run with terrain inside its footprint.

Nudging it was not the fix. The cause is a structure sized to one ground level standing across two, so
the answer is to give it one: the shelf right of the spawn stands **level at y31 from x 21 to x 37**
(read at z 72, 78 and 84 — every station 31), and `barn-garth` is a `relief_scope: "exclude"` pad over
x 17..37, z 70..84 that holds it there. Exclude takes the footprint out of the relief solve, so the
fell meets the yard at a face and can never come through a wall again.

Across the cross wing now, x 16 → 38 at z 77:

```
rises 1, falls 0, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end
```

`way-barn` re-routed to (9,75) → (14,76) → (18,77), off the main way and into the byre's west door.

## The fault-catalogue reads, taken on the built world

**Objective hidden — no.** The Cairn is a **`cube-3`**, not a `pillar-2`: 27 blocks of end stone round
a bedrock core, region `19,31,53 … 22,34,56`. The goal is 42–43 blocks from its own spawn with 20
blocks of lateral offset, and two blocks of obsidian is not the time pressure that distance needs.
`GET …/column?at=20,54`:

```
y 71..69   35:14  Red Wool    the studio's own marker
y 33       121:0  End Stone   the cube's lid
y 32       7:0    Bedrock     its core
y 31       121:0  End Stone   its floor
y 26       1:3    Diorite     the slab it stands over
```

Five courses of air under it, which is how a destroyable is meant to stand, and nothing at all between
y34 and y68. Nothing roofs it and nothing stands beside it inside twelve blocks.

**Spawn faces away — no.** Red spawns at (0, 92) with `yaw 180`; the bearing from there to the enemy
cairn at (−20.5, −54.5) is **172°** — 8° off. Blue spawns at (0, −92) with `yaw 0` against a bearing
of **−8°** — the same 8°. Both well inside the ~90° the fault wants.

**Spawn faces a wall — no.** The first fourteen blocks straight out of the red door, (0,92) → (0,78):
`rises 0, falls 0, worst step 0: 0 barrier, 0 scramble, 0 drop | walked end to end`. The door opens
onto the paved way and the way is level to the gill.

**Spawn to objective — walked.** (0,92) → (−20,−55): `rises 4, falls 5, worst step 2: 0 barrier, 1
scramble, 0 drop | walked end to end`, the one scramble a +2 at (−19,−44). Blue's mirror reads the
same with its scramble at (18,43).

**Stairs that end nowhere — none authored.** There is no authored flight on this board; the gill is a
`line` mark with `tread: 2` and the scar a `scarp`, and both are read as terrain rather than as
construction. Both spawn→goal transects walk end to end, which is the read that settles it.

**Stark contrast with no area separation — no.** `05-themes.txt` borders: `fell | turf 627 cells`,
`fell | scree 124`. The turf is the hag the birches stand on, which is a push with its own skirt, and
the scree is under the scar's face. Both boundaries are breaks of slope rather than lines drawn on a
plane.

**Empty board — 13.1% dead.** `GET …/coverage`: 13 032 ground cells, 10 196 reached, 1 130 decorated,
**1 706 dead (13.1%)**. Every one of the five largest patches is **one block from used ground**:

| area | centroid | distance to used ground |
|---|---|---|
| 378 | (−38, −41) | 1 |
| 376 | (36, 39) | 1 |
| 322 | (37, −42) | 1 |
| 306 | (−39, 41) | 1 |
| 112 | (29, −82) | 1 |

That is the Glassmere shape of dead ground — the board's own edges, a step off a route — and not the
Ruddle Brink shape, which is a front nobody crosses.

## What the dressing pass refused, and where the props went

The first build of this board placed 28 and declined 5 — four of six erratics and one birch, on
`OB19` (inside a goal's clearance), `DR-SITE` twice (no ground), `DR-CLAIM` (claimed by the paving
`way-shore`) and `DR-ROAD`. The erratics were the thing meant to break the pavement's biggest flat and
none of them was in the world.

`loop.py --candidates` settled it in two passes of eight positions each: of fourteen tried, four
stand — **(−30, 52), (−34, 22), (34, 60), (−8, 62)** — and the board is crowded enough that ten did
not. The birch moved to (−30, 68). `placed 36, declined 0`.

## The gate

```
round-trip       pass   codec parity — no field lost in XML ↔ dict
mirror check     pass   spawn/protection ✓  build ✓
buildability     pass   all 2 spawn / wool / monument placements on solid ground
traversability   pass   spawn ↔ objective chain connected across the build geometry
export gate      OPEN   GET /map/opus5-grykefell/xml → 200
```

`intent → generate: 2 teams · 0 wools · 9 regions · 18 filters · 5 apply-rules`.

## What is open

- **`largestField` 0.307** — a third of the fell is one flat field. For a limestone pavement that is
  the subject rather than a defect, but it is the number to watch if the board is ever called empty.
- **The old barn site, x 16..33 z 24..34, is now empty ground** on the rigg. It is not a fault; it is
  a place with nothing on it that used to have a building, and it is the obvious site for the next
  thing this board grows.
- **A question for the author, not a claim:** the scar is deliberately one-way — 121 cells of barrier
  face, approachable from above and not from below. On a destroy board with a single monument, is a
  one-way approach into the objective's quarter a good thing (it makes the defender's position
  legible) or a bad one (it halves the attacker's options)? Nothing in the corpus or the code answers
  that; it is a question about how the map plays.
