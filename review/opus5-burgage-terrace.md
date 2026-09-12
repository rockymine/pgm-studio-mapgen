# Burgage Terrace — one boundary, and everything that happens at it

> A destroy board whose whole idea is a line: made ground meets grown ground along one notched edge,
> six courses tall, and the monument stands four blocks back from its lip.

**In one sentence:** a market terrace over a water meadow, with two flights set **into** the retaining
wall rather than leaning on it, a row of burgage plots along the back, and a retaining wall striped
diagonally in whichever team holds the town.

80 × 220 blocks, `rot_180`, three surfaces (12 · 14 · 18), four pieces, maxPlayers 16.

## The boundary is the board

`holm` at 12 and `terrace` at 18 are two pieces at two surfaces, and the terrace is
`relief_scope: "exclude"`. That is deliberate and it is the whole design: `hold` lets the relief bring
the meadow **up** to the terrace and there is then no six courses and no reason for a flight; `exclude`
takes the footprint out of the solve and the two tiers meet at a face. `03-slopes.txt` reads **377
barrier cells in 4 faces, the largest 240**, and that face is the retaining wall.

The boundary is not straight. Ten vertex inserts cut two re-entrants and one salient into the
terrace's own front edge:

```
(-40,50) (-20,50) (-20,56) (-12,56) (-12,50) (2,50) (6,44) (20,50) (20,56) (28,56) (28,50) (40,50)
```

Each re-entrant is **exactly the flight that fills it**, so a stair is set into the wall the way a town
stair is, and between them the terrace pushes a salient out over the meadow — a bastion the market
place looks down from. The meadow's own seaward coast is drawn the same way, with three headlands and
two bays, so the crossing is 26 blocks at one and 40 at another.

## The two flights

Sixteen blocks of run for six courses each. Measured up the west one at `x -16`:

```
z  42 43 44 45 46 47 48 49 50 51 52 53 54 55 56
y  12 13 13 14 14 14 15 15 15 16 16 17 17 17 18
rises 6, falls 0, worst step 1: 0 barrier, 0 scramble, 0 drop — walked end to end
```

`EL1` names the seam as a six-block step at the plan tier, which cannot see an authored flight. The
transect is the answer.

## What the ground is made of

Three themes, three places.

- **`holm`**, the water meadow: a `layered` stack on the **slope** axis — turf, a coarse shoulder, bare
  rock past 40°. Flat where it matters, because the terrace above has to be looking down on something.
- **`burgage`**, the terrace: setts of stone brick, andesite and cobble, a chiselled coping on the rim,
  and its wall a **`wallDiagonal`** — stripes sheared by height so they climb the face at a slope
  instead of standing upright. One of its four runs is a **`teamTint`** on stained clay, so the town
  wears the colour of whoever holds it and you can read from the far bank whose terrace you are looking
  at. That pattern is the reason this board exists; nothing sampled from the plane does it.
- **`silt`**, two splotches at the water's edge where a river used to put it. A shape, not a field.

The first painted build left `themeById` unset, so the terrace took the map default and came out as a
green field with a grey cliff — the diagonal wall, which is the point of the board, was simply not
there. The isometric said so in one look and no finding did.

## The buildings

**Three authored plots a side, one style, differing in height and footprint and in nothing else** —
which is what makes a row read as one town rather than three ideas. A three-storey merchant's house
with a dark oak roof, and two of two storeys, one of them with a cross wing. The spawn hall is the same
style again, as the town gate.

Three families: the ground is verdant over grey stone and the terrace is grey stone laid in courses, so
what is **built** on it is timber over a brick plinth with hardened-clay walls — never the material
underfoot. Every roof is a gable at pitch 2. No footing. No shed.

Each storey carries its own wall stack sized to its own clear, so the building reads as three rooms:
brick-and-clay at the shop, oak with a course of **laid** oak at the solar for the beams to end on, and
a shorter attic above. The posts are oak log; the wall is deliberately not a log checker in that same
log, which would have read as one mass.

## Numbers

| read | answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` |
| `GET /rules/terms` | ratio **3.40** (GO1 wants 3–4); own-spawn walk 47 (GO4 wants 40–90) |
| `GET …/preflight` | **export gate OPEN** |
| `GET …/coverage` | reached 6 040 · decorated 2 387 · dead 4 663 of 13 090 = **35.6% dead** |
| `03-slopes.txt` | 12 733 walked · 79 scrambled · 377 barrier; 4 faces |
| `06-claims.txt` | placed 20, declined **0** |

## What went wrong on the way

- **An insert names the edge LEAVING that vertex.** `{"after": 8}` on the meadow's ring landed on the
  board's back edge rather than its west flank and folded the polygon; the world then carried ten
  blocks of void **inside** the meadow at `x -30, z 40..49`. Nothing refused it — the store answered
  200, the gate answered OPEN, and a transect is what found it. The index to give is the one *before*
  the edge wanted, and after a run of inserts that is not the index it started as.
- **`HJ5`: which rectangle is the wing follows from the ridges, not from the drawing.** A wing's ridge
  runs *into* the shared edge, so stating `alongZ` on the big rectangle of a horizontal joint made the
  hall the wing and the refusal read backwards against what was drawn. The hall's ridge runs **along**
  the shared edge and the wing's into it.
- **`ST10` and `ST9` are different caps on different rectangles.** The spawn piece is the protection
  region (20 × 30) and the footprint is the building raised on it (20 × 20), and the ring between them
  is what `WX8`'s iron cubes need — their own 3 × 3 plus two blocks of clear air to the shell.

## Open, and not the author's to settle here

The monument stands on the terrace, four blocks back from a six-course wall with two stair chokepoints
and a bridged void in front of it. Whether that is a defence a sixteen-a-side attack can break, or a
stalemate with a good view, is a question about how a map plays. Built as stated.
