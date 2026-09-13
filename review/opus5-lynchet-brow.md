# Lynchet Brow — a hillside farmed into terraces

Every fight is about getting up or down exactly one retaining wall. Four lynchets climb from a
valley bottom to the brow, each a made shelf with a drystone face, and the only walked way between
two of them is a flight cut into the wall.

Slug `opus5-lynchet-brow` · 104 × 208 blocks · rot_180 · 20 a side · core.

## How it is meant to play

The valley bottom is one holm at y20 with a lane along it, and it is the widest flat on the board.
From there the ground rises 20 courses to the brow in four steps of four. A 4-block riser is not a
step a player takes: it is a wall, and the board's barrier share — 11.3%, the highest of the four
boards in this run — is those walls. What a player can do is find a flight.

There are eight of them, two to each wall, staggered in x so the route up zigzags: you climb, you
walk the headland along the terrace, you climb again somewhere else. That is what makes the board
a sequence of single-wall fights rather than one long slope. An attacker who wants the core has to
win four of them, and a defender who loses one has three more behind it.

The core stands on the second lynchet at (−24, −50), backed against the third's wall so the casing
has ground on every side — a breach has somewhere to pool rather than an edge to fall off. It is 48
blocks from its own spawn and 150 from the enemy's.

## Where made ground meets grown ground

This is the whole board, so it is worth stating as four decisions.

**The made ground is `relief_scope: "exclude"`, never `hold`.** `hold` lets the relief ramp up to
meet the shelf, and then there is no step and no reason for a stair. `exclude` takes the footprint
out of the solve entirely: the land is whatever that outline would have produced, and the shelf
meets it at a face. The relief read proves the terraces are outside the model — 5,926 cells on a
board of 21,632, which is the grown ground alone.

**The boundary is not a straight line.** Each terrace's downhill edge carries a re-entrant at every
x a flight climbs, and each is cut to exactly the flight that fills it: `NOTCH_HALF` and
`NOTCH_RUN` are the same two numbers the stair's polygon is built from, so the stair stands in a bay
of the wall instead of sticking out of it. The uphill edge wanders a cell or two per vertex so the
shelf does not read as a rectangle.

**The height is bridged by a stair, not by the relief.** `height_mode: "level"` with
`anchor_heights`, `skirt: 0`, `keepClear: true`, and a **material** rather than a theme — a cell
patchwork of cobble and andesite, one stone the whole way up, so a flight reads as made even where
the shelf above and the floor below each have their own ground.

**The face is where the paint goes.** `wallDiagonal` shears drystone stripes by height on three
terraces; the second — the one the core stands on — carries a `wallRun` with a `teamTint` course in
it, so a player reads whose terrace they are looking at from across the valley. The tinted theme is
11.2% of the board's ground, which is one terrace and its image.

## What the ground is made of

- **ground** — green pasture. Grass over dirt, coarse dirt on the shoulders, cobble on the broken
  faces, finished on the **slope** axis so one stack does the meadow, the bank and the rock.
- **built** — drystone. Cobble, mossy cobble, andesite and stone, in every retaining wall and every
  flight. The buildings are oak and lime over a mossy-brick plinth, so a steading never reads as a
  field wall.
- **accent** — the team's own clay, one course, in one terrace's wall.

Census: `grown` 56.0% · `lynchet` 32.8% · `lynchet-tint` 11.2%, with borders between all three.

## What went wrong

**Two of the eight flights were not in the world, and the plan tier could not have said so.** The
transect is the only read that sees an authored flight at all, and it named them:

    (6, -66) -> (6, -84)   BARRIER +6 at (6, -69); DROP -7 at (6, -70); ... worst step 7

Reading the profile out — `33 33 33 39 32 32 32 33 33 33 34 34 34 35 35 35 37 40 40` — the stretch
where the stair should be is the *grown hillside* climbing gently, not a flight. The cause is the
rule that the taller shape wins a column: the top terrace was stated at y36 where the relaxation
between the holm at 20 and the brow at 40 arrives at about 37.5, so that shelf was a hollow rather
than a shelf, and the flight into it lost every column to the ground it was cut through.

The fix is arithmetic, not geometry. A made shelf has to stand **above** the line the relief solves
under it, everywhere its flight's footprint reaches. Dropping the brow to 36 puts that line at 0.27
courses a block, and shortening the runs from 12 to 8 — still twice the 4 of rise — keeps every
flight in the half of its shelf that stands proud. Six of eight walked before the change; the
measure after it is in the numbers below.

**The steading met the world with a wall of bedrock**, twice — `WX11` at (−8, −86) and its image,
4 blocks. A spawn shell levels the column under its whole footprint at the footprint's highest, and
the brow's lobed ring had left the shell's west side outside it. A rectangular `roompad` area mark
wider than the shell on all four sides cleared it, and it is now the first mark on every board here.

**`relief.stairs` is not a field.** Stated on the first build, answered `RQ3`, removed.

**Standing complaints that are not faults.** The plan tier walks pieces flat and cannot see an
authored flight, so `EL1`/`WL11` findings about the terrace seams say something true about the plan
and nothing about the board. The answer is the transect, quoted above and below, and not a
redesign.

## Numbers

    03-slopes   19,051 walked · 558 scrambled (2.6%) · 2,023 barrier (9.4%) · 17 faces, largest 288
                the highest barrier share of the four boards in this run, which is the walls
    06-claims   placed 46, declined 0
    coverage    56.1% reached · 15.3% decorated · 26.2% dead · 2.5% route
    relief      group team  cells 5,926  low 19  high 36  symErr 0 — the grown ground alone,
                which is what relief_scope "exclude" means measured rather than asserted
    preflight   round-trip · mirror · buildability · traversability all pass — gate OPEN

Flights, by transect, each `points=x,z;x,z&beside=2`:

| flight | reads |
|---|---|
| lynch1 at x −30 | rises 5, falls 0, worst step 2 — 0 barrier, 1 scramble, walked end to end |
| lynch1 at x 18 | rises 5, falls 1, worst step 2 — 0 barrier, 1 scramble, walked end to end |
| lynch2 at x 26 | rises 5, falls 1, worst step 2 — 0 barrier, 1 scramble, walked end to end |
| lynch2 at x −10 | rises 4, falls 1, worst step 2 — 0 barrier, 1 scramble, walked end to end |
| lynch3 at x −36 | rises 5, falls 1, worst step 2 — 0 barrier, 1 scramble, walked end to end |

## Coordinates to check in game

| what | where |
|---|---|
| the core, backed against the third wall | (−24, −50), on lynchet 2 |
| a flight that walks | transect (−30,−18) → (−30,−36) |
| the tinted terrace face | lynchet 2's perimeter, a `teamTint` course in the drystone |
| the holm and its lane | z −20..0, the widest flat on the board |
