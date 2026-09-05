# Corbel Scar — in what order a terrained board is built

## What this is

Scarrow Delph's concept restated with as few marks as it takes, built to answer one question: does the
base terrain come first and the features on top, or the other way round? The answer turned out to be
forced rather than chosen, by three facts measured on a probe board before a line of the map was
written.

`maps/opus5-corbel-scar`, `specs/opus5-corbel-scar/`. Six relief marks, no authored shapes, two
pieces a side.

## The three facts, measured

### A shape can only ever raise ground

A sketch polygon carrying `anchor_heights` is the obvious way to state a sloped terrace on an
arbitrary outline. It cannot do it on terrain. Over one probe board, the same six-sided shelf asked to
tilt from 30 down to 18:

| the shelf states | no `relief_scope` | `exclude` | `hold` |
|---|---|---|---|
| uniform 14 (under the hill) | ignored | **ignored** | 13 · 13 · 13 · 13 |
| uniform 34 (over the hill) | ignored | **33 · 33 · 33 · 33** | — |
| a tilt, 34 → 22 | ignored | **33 · 31 · 26 · 23** — the high half stands, the low half is gone | flattened to one level |

With no scope the numbers are **byte-identical to having no shape at all**. `hold` pins the footprint
at one level read at the ring's centre, so a tilt cannot survive it. `exclude` builds the shape only
where its own height beats what the board would otherwise have there, and nothing stated underneath
changes that: measured identical at `base` 20 and `base` 12, with and without an `area` mark dug to 17
directly under it. Four variants, one answer.

So a sloped shelf **cut into** a hillside is not expressible as a shape. Only a shelf standing proud of
one is, and it arrives with a sheer seam — `SK26` named its low edge as a wall to step into on the
first build of this board.

### Only a `line` mark can tilt

`ReliefMarkJson`: *"A point, an area and a rim state one and a line states one per point."* So an
`area` is a flat pad whatever its outline, and every graded thing on a board — a road, a ramp, a
terrace — is a `line`. Widened, a line is also the instrument the shape could not be: it states a
height per point **and** it is inside the solve, so it pulls the ground down to meet it as readily as
up. Measured across one at `r 14`: `29 28 28 27 27 26 25 24 23 22 21 20 19` — one course at a time,
into ground that was at 25 before it.

### A spiral line is a whole quarry

One mark whose radius shrinks as it winds cuts the benches and the road down them together. Along its
own centreline, 27 → 11: **worst step 1**. Scarrow spends five marks on the same thing — four nested
`area` rings and a twenty-one-point haul road — and the road has to be threaded through faces the
rings already cut, which is what leaves a 3-wide, 6-tall blade of uncut bench standing free on the
quarry floor at x −40..−38 (visible in its own section at z −60, and named by nothing).

## The order, then

**Base first, and the base has to be dug for the feature before the feature is placed** — but since a
shape cannot be seated in a hollow anyway, the honest form is stronger: **state everything that shapes
ground as relief, in one pass, and let the solve reconcile it.** A shape belongs on terrain only where
it stands over it.

Six marks build this board:

| mark | kind | does |
|---|---|---|
| `crest` | line, r 18 | the knoll the spawn stands on |
| `spine` | line, r 7 | the graded way off it — `SP8` asked for this and wrote the mark |
| `bank` | line, r 10 | the shoulder above the water |
| `channel` | line, r 7 | the bed, drawn symmetric about the origin so its own image lands on it |
| `delph` | line, r 5, 45 points | the quarry: the pit and its road, one statement |
| `terrace` | line, r 13 | the second monument's ground, tilted 24 → 18 |

## What it bought

| | Scarrow Delph | Corbel Scar |
|---|---|---|
| relief marks | 20 | **6** |
| walked cells | 16,810 | 17,288 |
| **scrambled (2-block)** | **1,738** | **330** |
| **barrier (3+)** | **2,412** | **1,006** |
| faces | 20 | 12 |
| `RL2` scrambles per barrier | 0.9, 613 steps too tall | 0.4, 352 |

A fifth of the scrambles and 42% of the barriers. The hard edges Scarrow is full of are not what a
quarry costs; they are what twenty marks crowded into one hillside cost. Marks far apart at `reach 0`
solve smooth: the base terrain alone, three marks a side, measures **99.6% walked**.

## What it did not fix

**A terrace stated as a line grades perfectly and stops reading as a terrace.** It blends into the
hillside because blending is what the solve does. The shape version reads as a terrace and cannot meet
the ground. There is no instrument that is both, and that is the gap this board ran into: **an
arbitrary polygon, tilted, as ground.** An `area` mark with a height per ring vertex would be it.

**The plan cannot see the sketch, and says so twice.** `SP8` refuses the 14-block seam between the
knoll and the field on every run; the `spine` mark that grades it is invisible to a plan lint. Same
class as Scarrow's `EL1`. Correct as stated and not the plan's to fix.

**23.3% of the ground is dead**, both patches on the flanks at the river — ground the two journeys
never pass. A simpler board did not make that better.

**`DR-DRY` on the river.** The channel mark and the water prop are two statements about one hollow and
they still disagree at the margins.

## Two studio findings

**A theme's pattern with a mis-named member list 500s the store.** `TerrainThemeValidation.Uncarried`
walks a pattern's members to find the ones that carry no material — and walked the member list itself
without a null guard, so a `cell` stated with `materials` where the model wants `palette` deserializes
with a null palette and throws `ArgumentNullException` out of `POST /map/from-documents`. The fault is
exactly the one that walk exists to name. Every list it reads is guarded now, and a pattern that
states no member list at all is reported as the empty pattern it is.

**`SK26` prints a negative fall.** *"the ground falls -3 within four cells"* — where the ground beyond
a flight's end is higher, not lower. The finding is right and the sentence is not.
