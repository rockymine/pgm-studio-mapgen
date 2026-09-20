# Opus 5 — Hushwater: one composed micro board, adapted

## What I set out to build

A Capture the Wool board in the micro band, two teams, taken off `GET /api/compose` and adapted into a
place rather than painted. The sentence, written before the first shape:

> **A lead hush — two mine heads facing each other across the gill their own water tore out of the fell,
> where the made ground at the top is flat and stated to be flat and everything below it is raw ground at
> an angle.**

The board is `specs/opus5-hushwater/`, the world `maps/opus5-hushwater/`, the review
`review/opus5-hushwater.md`. The decision journal is `specs/opus5-hushwater/decisions.md` and the
composer's own numbers against the built board's are `specs/opus5-hushwater/composed-vs-adapted.md`.

Descriptor, which reproduces the starting point byte for byte:
`players=18 teams=2 symmetry=rot_180 cell=4 seed=5 composerVersion=body-first-1 schema=1`.

---

## What I could not say

**The iron cube, on a board whose spawn comes from a plan. — Out of reach, not missing.**
I wanted a renewing iron block in the spawn. `ST2` wants an iron marker's whole cube inside a **spawn-role
piece**; `WX8` wants it outside the room shell with two blocks of clear air; `WX1` makes the shell *the
piece inset one block on every side*. Those three cannot all hold: a plan-compiled spawn leaves a
one-block ring and the cube needs three. I checked `openapi.json` before concluding: `WoolPlacement`
carries a `footprint` field and `SpawnPlacement` does not, and `WX13` says a shell's footprint is the
region inset one block *"wherever the document states no footprint of its own"* — so the mechanism exists
at the intent tier and the plan tier has no word for it. I dropped the iron rather than grow the spawn
region past `ST10`'s 20 × 30 cap chasing it. The composer emits `"iron": []` and was right to.

**Two pieces at one surface in one component cannot be scoped apart. — Out of reach.**
`relief_scope` is what decides whether a piece of ground is made or grown, and a flat composed plan
compiles to one polygon per *distinct height per component*. So two pieces that should differ — a spur
that is moor and a lane that is a laid floor — have to be given different surfaces to become different
shapes, even where the height difference is not wanted for its own sake. `shapePropsByHeight` keys on the
height and `shapePropsById` names the fused shape; neither reaches a piece. This is not a gap: an
`addShapes` override with its own `relief_scope` reaches any footprint at all. It is a consequence of the
plan tier's partition being by height, and it is why this board carries seven surfaces where four would
have described its ground.

**A pad between two edges sixteen blocks apart cannot satisfy both `G2` and `G5`.** Not a gap; arithmetic.
`G5` wants a hop of 10–20 blocks and `G2` wants a zone at least 10 blocks of corridor width, so a pad
sixteen blocks clear of one neighbour has four blocks of facing left for the other. I report it because
it is the reason one of my two bing planks is 12 blocks and not 16, and because it is invisible until the
evaluator refuses at score 2000.

**`POST …/sketch/seats` takes the layout in the body.** Its knobs are query words (`kind`, `width`,
`depth`), so I posted it with no body and got `seats: 0, bounds: {0,0,-1,-1}` — an empty board, 200, no
finding. Posting the stored layout answers 149 seats for a 9 × 7 house as a character raster. **Mistaken,
not missing**: the adaptation brief says to use it before placing buildings and I read the route before I
read the brief's sentence about it.

---

## What I got wrong

**I painted half the board grey and blamed the band cuts.** The first finish excluded the whole hub ring
from the relief and themed it as made floor. `05-themes.txt` read `floor 50.5% · moor 35.6% · hush 13.8%`
and the isometric read as stone plateaus with green in patches. My first instinct was to move the slope
cuts — and the `incline` histogram said the moor that existed was already 79% turf. The fault was that
**64% of the board was stated to be grey ground before any band was cut.** A mine head is a patch of laid
stone in a fell, not a floor with a fell round it. Putting the ring back into the solve took it to
`moor 57.5% · floor 23.8% · hush 18.7%` (56.8 · 24.5 · 18.7 as shipped, after the dam and the
chimney). The wrong claim looked right because the symptom (grey) matches
the documented cause (banding by height), and the histogram was the only thing that separated them.

**I authored two flights before there was any ground to measure them against.** The east one read
`(18,32) 20 · (18,33) 15 DROP -5` on a transect: the `knowe` mark and the `brow` push had lifted that
bank *above* the yard the flight was climbing to, so the flight was a five-block trench cut across a
knoll. Nothing refuses this — `EL1` and `WL11` walk the plan flat and cannot see an authored flight at
all, and the board stored, pre-flighted OPEN and exported with it in. `03-slopes.txt` is what showed it:
`8 faces, largest 44`. Moving the flight to the shore, where a transect measured real two-block scrambles
at `(8,21)` and `(8,31)`, gave `6 faces, largest 16` and took barrier cells from 132 to 54.

**`jitter` is an integer percentage.** I wrote `0.4`. `DR-DOC` refused it on a prop's pave — and the same
mistake was sitting in three theme snapshots, where `RQ3` does not reach and nothing would ever have said
so. The lesson generalises: a value inside a theme or a house style is only checked by the gate that
happens to read it.

**I put the dam pool across the spawn's own door lane.** It placed cleanly — 14 props, 0 declines — and
then `04-routes.txt` read `206 blocks, 55 placed, worst drop 10` on one raid against `30 placed` on its
mirror. A pond is an obstacle a walk routes round, and the walk read is the only thing that saw it.
Moving it eight blocks west brought all four raids back to 30 placed.

**I thought the sky wool was a bug.** A 3 × 3 × 3 wool cube floats at y56–58 over each wool room with
thirty courses of air under it, and three other boards in `specs/` read `top 21..23` at their wools. It is
`GoalMarkerStamper`: a marker stamped `BuildCeiling.MarkerOver` = five blocks above the build cap so that
nobody can reach or grief it. I read `column`, then a section, then the source, and filed nothing. The
repository's history says this is the third time that check would have been the difference between a
finding and a wrong bug.

**`04-reach.txt` reads a correct CTW board as 24 stranded patches, and I nearly believed it.** Its header
is the tell: `components 25 · navigable 8790 columns · **bridgeable 0**`. It walks; it does not build. On a
board whose two halves are joined only over a gill, the other team's half *is* a separate component — 3856
cells of it — and so are the shoal, the two bings and every roof. `GET …/preflight` runs the check that
counts the build geometry and answers `traversability: spawn ↔ objective chain connected across the build
geometry`, per team; `coverage` reads 1.6% dead. Two reads disagreeing is not two answers: it is one read
answering a different question.

**I put a made layer where people walk.** The chimney stood beside the engine house at the mine head
first, and the defence's own walk to its east wool went from `3 placed` to `30 placed, worst drop 13` —
everything downstream of a stacked cell reads one number, the surface top, so the walk climbed the stack
and fell off it. The store answered 200, the export gate stayed OPEN and `03-slopes` did not move; only
`04-routes.txt` saw it. It stands on the bing now, which is the one piece of ground no land route passes.

**I read a line mark's `width` as the band and it is the half-reach.** Caught from the schema
(`"A line's band is twice it, since it reaches either side of the centerline"`) before it cost a build.

---

## What worked first time

- **Pinning a composed board and reading it back.** `GET /compose` → `POST /compose/pin` → `planJson` →
  `DELETE /plans/{id}`, copied from `specs/band-suite/build-suite.py`. The plan that comes back is an
  ordinary `PlanModel` and every adaptation after that is editing a dict.
- **The `walls` entry.** One line — `{"a": "hub-t4", "b": "wool-b-t1"}` — and `/plan/inspect` answered the
  stamped rect: `x 35..37, z 60..76, floor 0, top 21`. Two thick, sixteen long, five courses above the
  lane, exactly as `ST8` describes it.
- **A `rot_180`-symmetric mid built from two `mirrors: false` pieces** that are each other's images. It
  compiled into one neutral group with one shape and no symmetry error.
- **`relief_scope: "exclude"` on the made ground.** The mine head, the spawn and the walled lane came out
  flat at their stated heights with the fell solving around them, first try.
- **The `slope`-axis `layered` material.** One stack finishes the turf, the shoulder and the crag of the
  same hillside, and `GET …/incline?format=text` says where to cut it. Nothing about it needed a build to
  test.
- **`loop.py --candidates`.** Eight boulder positions answered in one twenty-second pass, each with its
  rule and its coordinate. The first dressing pass declined seven of fourteen props; the last placed 28
  of 28.
- **`plan/flow` and `walk` agreeing.** The flow read off the plan said 210 against 213 blocks for the two
  raids; the built walk said 206 against 211, 30 placed each way. The cheap read predicted the expensive
  one.

---

## Open gameplay questions

No oracle was available. Both were decided, built, and are recorded as questions.

1. **Is a bedrock approach wall with no door fair to the team that owns the wool behind it?** Measured,
   the defence pays three placed blocks to cross its own wall against four to reach the unwalled wool on
   the other flank, so it is not a large tax — but it is a tax every rotation for a defender who has not
   bridged the bing first. I decided yes and built the bing as the answer, so the wall is a prepared line
   the defence can also plan around. The alternative reading is that a wall on a wool the defence must
   reach belongs on the *attack* side of a seam the defence does not use, which this board has no such
   seam for.

2. **Should the two hops across a mid be equal?** I made them 12 and 20 blocks and mirrored them, so each
   team gets the short one on the opposite hand. That gives one cheap contested crossing and one long
   safe one per side and makes the two halves of the middle read differently without being unfair. Equal
   hops would be simpler to read and less interesting to fight over. I do not know which the author
   prefers, and nothing in `G5` or `CT12` distinguishes them — both are in band.

3. **Does a team transient-link earn 192 cells of ground that no land route passes?** `plan/flow` calls
   144 of the bing's blocks "off every route"; `coverage` reads the whole board at 1.6% dead. The two
   disagree because the flow read walks land and the bing is reached only over its own team's zones,
   which is what a transient link *is*. I kept it. If the author's answer is that a pad no walk reaches is
   dead ground whatever its function, the bing should be halved or dropped.
