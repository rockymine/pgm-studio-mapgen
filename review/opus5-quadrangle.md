# Quadrangle — four teams, from a composed two-team unit

**In one sentence:** four walled quadrangles set corner to corner round a crossed court, each with a
cloistered yard in the middle of it and two faces to defend instead of one.

`GET /api/compose` answers **400** for `rot_90` and for `teams=4`. The composer is what refuses four
teams; the plan tier does not. What is composed here is the *arrangement*: the unit is the ring hub
of `GET /api/compose?players=30&symmetry=rot_180&seed=7` — hub `ring` with a yard in the middle,
frontline `none`, wools `i`/`i`, card score 1.881, 56 land cells, the smallest board in the first two
hundred seeds scanned — reshaped to fit a quadrant and then fanned with `globals.symmetry: "rot_90"`,
which `Symmetry.Order` reads as **4**.

The board built. `POST /plan/evaluate` answers **score 0, valid, no violations and no lint**;
`POST /plan/compile` emits four teams — red, blue, yellow, green — and `GET …/preflight` ends:

```
intent → generate: 4 teams · 8 wools · 37 regions · 40 filters · 20 apply-rules
round-trip: codec parity — no field lost in XML ↔ dict
mirror check: spawn/protection ✓ wool/room ✓ build ✓
buildability: all 12 spawn / wool / monument placements on solid ground
traversability: spawn ↔ objective chain connected across the build geometry
export gate OPEN — GET /map/opus5-quadrangle/xml → 200
```

## What four teams took

**The unit has to fit a quadrant before the symmetry is flipped, not after.** Seed 7's unit spans
`x −35..30` by `z 10..60` about the origin. Under `rot_90` a point `(x, z)` has images `(−z, x)`,
`(−x, −z)` and `(z, −x)`; a unit straddling the axes walks straight through its own images. Redrawn
strictly inside the `+x/+z` quadrant — `x 10..80` by `z 10..90` — the four images tile the plane and
never touch. That is the whole of the trick, and it is a translation and a redraw rather than a new
idea: the arrangement is still hub, spawn hung off it, two wool spurs, frontline facing the mid.

**One zone, because `rot_90` maps a cross onto itself.** The composer emits one mid band between two
fanned images; four teams need a shape that reaches all four. A single arm, `x −10..10` by
`z −60..60`, fans into a crossed court whose four quadrants are the four teams' ground. Each unit
meets it along two faces — its west edge and its south edge — so every team has **two** fronts and
two neighbours across 20 blocks of void, with the third team diagonally opposite.

**Destroy objectives are order-2 only**, so this is CTW and carries no destroyable and no core.

**A quadrant unit is tighter than a half.** `WL9`'s `spawn-wool-ratio` band is [1.031, 1.22] and the
two wools have to sit inside a wedge with the spawn in its outer corner. Seven arrangements were
evaluated before one came in at 0: a 5-block slip beside the walled wool approach is what finally
gave `SP9`'s door its fifteen blocks of ground without shortening the walk to the wool behind it.

## How it is meant to play

Each quadrangle turns a battered angle on the crossing. Its two outer lips carry a crenellated
curtain four courses over a terrace that is itself three courses over the court, with an angle tower
inside the bevel where the two runs meet. There are exactly two ways off the rampart into the court,
one per face, each a twelve-block flight set into a re-entrant cut for it.

Inside, the ring hub's yard is kept as the hole the composer made it — a 10 × 20 shaft the compiler
cuts as a `subtract` — and twelve pillars stand round it on the ring itself. A player crosses the
quadrangle through its cloister or round the outside of it, and a raider who takes the rampart still
has to come down a stair somebody is standing at the bottom of.

The two wools hang off the hub's north and east arms, each on one twenty-block seam, and both seams
carry bedrock. The spawn is in the outer corner behind them.

## The techniques, and what each one bought

**A `teamTint` run in the terrace's `wallDiagonal`, on a board where it finally means something.**
A tint is one colour per canonical island, and here the four quadrants are four islands, so each
rampart wears its own garrison's colour and a player reads whose wall they are under from the court.
On a single-landmass board the same statement paints the whole map one colour (`PT5`).

**A cloister drawn as an annulus.** `SK13` reads the compiled subtract as the board's negative space
and refuses any add that fills it, so the cloister's flagged floor is one even-odd ring — outer 17,
thickness 5 — clearing the yard's circumscribed radius of 11.2 by a comfortable margin.

**Vertex edits on both compiled outlines**: the two stair re-entrants and a battered outer angle on
the terrace, four chamfered corners and a bite out of the long back edge on the court. Every move is
inward.

**Numbers.** `coverage`: 14000 reached, **0.0% dead**, with 150 blocks (1%) off every route.
`03-slopes.txt`: 12684 walked, 264 scrambled, 200 barrier, 12 faces, largest 28. Relief: `level`
0.589, `largestField` 0.334, range 9 over 2316 cells, `faceCount` 0, `symmetryError` 0, **no seams**.
Themes: court 60.2%, rampart 28.7%, cloister 11.1%. Both flights transect `worst step 1, walked end
to end`.

## What went wrong

**Two room styles refused with `HS9`** — `@sb-assay` and `@lk-terrace` lay beams and no course of any
wall is a laid log. The tell is `beams.any: true` with no `laidLog` band; `@sb-blockhouse` and
`@showcase-cage` carry `any: false` and pass.

**A forked style with `"beams": null` is a 500, not a 400.** Dropping the key outright parses. That
is the same class as the note about a bare `HouseStyle` being a 500: the parse throws before any gate
reads it.

**There is no building on this board, and that is a measured limit rather than a choice.** A quadrant
unit is built from ranges ten blocks deep. `DR-PASS` wants eight blocks of passable ground along a
building's whole side, and a five-deep house in a ten-deep range leaves four — and
`POST …/sketch/seats?kind=house` offers the seat anyway, because it is asked about the walls and the
roof reaches a block past them. The quadrangle's architecture is its curtain, its angle tower and its
cloister, all of them made layers, which that rule does not judge.

**The court was a table on the first pass**: `level` 0.740, `largestField` 0.483, with one flat
`area` mark 19 blocks across pinning most of the hub. Shrinking it to 15 — the colonnade only needs
flat ground at radius 12 — and raising the grain to amplitude 2 brought it to 0.589.

## The lopsided wool, with four teams

`GET …/plan/flow` reads one attacker against one wool at a time, and on a four-team board "the
attacker" is one of three enemies. What it reports is **160 blocks to the far wool and 131 to the
near one, a ratio of 1.22** — worse than the two-team boards here and about what the composer's own
boards read. `WL9` is satisfied (the two wools are within 1.22 of each other **from their own
spawn**) and `WL10` is satisfied, but the attack ratio is not closed, for the reason board 1's review
sets out at length: the spawn sits in the outer corner of its own wedge and the locus that would
close both readings runs outside it. On a quadrant the spawn has nowhere else to go.

## Coordinates (one quadrant; the other three are its images)

| thing | at |
|---|---|
| the crossed court (build zone) | x −10..10 by z −60..60, fanned |
| the terrace | the L along x 10..25 and z 10..20, surface 14 |
| south curtain | x 16..55, z 10..12, four courses |
| west curtain | x 10..12, z 16..60 |
| angle tower | (19, 19), drum, outer 4, 14 tall |
| south stair | x 34..42, z 16..28, 14 → 11 |
| west stair | x 18..30, z 34..42, 14 → 11 |
| the yard | x 35..45, z 30..50, void |
| the cloister | twelve pillars at radius 12 from (40, 40) |
| bedrock walls | z = 60, x 30..50; x = 55, z 30..50 |
| spawn | x 65..75, z 55..65 |
| wools | (35, 80) and (70, 40) |
