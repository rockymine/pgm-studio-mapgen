# Heftfold — made ground over grown ground

> A capture-the-wool board on the composer's own skeleton, with the three things a composed board does
> not have: an island in the middle, a team site that is split rather than one rectangle, and two
> wools the spawn stands **between** instead of behind.

**In one sentence:** two hill farms on opposite shoulders of a pass, each an open pasture at y11 and a
drystone-walled intake at y16, so the whole board is the five feet between them — and on the saddle in
the middle, a sheepfold that is nobody's, walled, and open toward each team by the same gap.

110 × 170 blocks, `rot_180`, three surfaces (12 · 14 · 17), eight pieces, maxPlayers 24.

## What was taken from the composer, and what was changed

`GET /api/compose?players=24&symmetry=rot_180&wools=i` answers a board whose skeleton is
spawn → hub → two wool rooms → frontline → mid band. That arrangement is kept. Three things about it
are not.

| the composed board | here |
|---|---|
| the middle is a bare build zone with nothing in it | the **fold** — a 30 × 20 island on the axis, `mirrors: false`, walled, with a gap in the middle of each end. Both hops off it are 10 blocks |
| the team site is one 55 × 30 rectangle | a pasture at 12, an intake at 17 and a lane at 12 — **three levels**, joined only where a flight says so |
| spawn at one end, both wools at the other (75 and 95 blocks off) | **barn · house · byre in a row**, the spawn between them: 25 blocks to one wool and 32 to the other, measured by `…/walk` |

The seventh thing a composed board is, and this one is too, is **shifted**: the team unit sits west and
its `rot_180` image east, so the two farms face each other diagonally across the pass. That is not
decoration — it is what puts the fill ratio inside `G8`'s band. The first attempt here was symmetric
about `x = 0`, filled its own bounding box, and was refused three ways at once: `G8` at 0.774 against
[0.201, 0.542], `FR6` on a 120-block frontline against a 16-cell cap, and `LN2` on a 120-block chain.

## The five feet, and the three ways up them

The intake is `relief_scope: "exclude"`. That is the whole of why there is a board here: `hold` lets the
pasture ramp up to meet the terrace and there is then nothing to climb, where `exclude` takes the
footprint out of the solve and the two tiers meet at a face.

So every way up is **authored**, and there are three:

| flight | from | run : rise | measured |
|---|---|---|---|
| `gate` | the pasture, into a gateway set back into the wall | 10 : 5 | `transect (-26,30)→(-26,52)`: rises 5, **worst step 1**, 0 barrier, 0 scramble |
| `wicket` | the lane, half way along | 10 : 5 | `transect (2,52)→(-22,52)`: rises 5, falls 1, **worst step 1** |
| `byre-gate` | the lane, at the byre's own door | 10 : 5 | `transect (6,56)→(6,84)`: rises 5, **worst step 1**, walked end to end |

The gateway is the one place the boundary between made and grown ground is allowed to be interesting: a
14 × 6 rectangular re-entrant cut into the retaining wall by four vertex inserts, with the flight
climbing into it and three blocks of wall stub either side. Everywhere else that boundary is straight,
because a retaining wall is a straight thing and the pasture's own coast is the half that wanders.

`EL1` fires twice and `WL11` once, all three naming those seams as five-block steps. They are complaints
from the **plan** tier, which cannot see an authored flight; the transects above are the answer.

## What the ground is made of

Three themes, and each is a place rather than a piece.

- **`ley`**, the pasture: one `layered` stack on the **slope** axis — turf over soil under 26°, a
  coarse-dirt shoulder to 42°, bare rock past that. The board's variation is its own angle.
- **`garth`**, the intake: grass on top, because an intake is walled *grassland*. What is built about it
  is its **edge** — a stone-brick coping on the rim and a `wallRun` on the wall, striped along the
  perimeter. A wallRun varies along the arc, which is the one thing a field sampled from the plane
  cannot do and the one thing a retaining wall needs.
- **`yard`**, the paving: two polygons, one round the steading and one across the working yard the three
  back buildings open onto. A splotch stated on a shape, not a pattern sprinkled over the terrace.

The first painted build gave the whole intake the setts and the board came out as a car park with two
farms on it. The top-down said so immediately; nothing else did.

Three tone families, named before anything was painted: ground **verdant over grey stone**, built
**dirt** (spruce), accent **brick**. Every building on the board is therefore timber on a cobble plinth
under a brick roof — never the grey stone it stands on.

## The buildings

**One authored house per farm**, and three more the rooms stamp: the barn the first wool sits in, the
spawn hall, and the byre the second wool sits in. Four buildings in a row across the back of the yard is
a laithe farm; a fifth would be a village. A second authored barn was drawn, declined by `DR-PASS` for
leaving under five blocks of passable ground beside it, re-sited twice, and then dropped — the board did
not need it.

The steading is a 14 × 10 hall with a 7 × 7 cross wing (`HP3` caps a placed building at 192 blocks of
wing; 229 was refused). The hall's ridge runs **along** the shared edge and the wing's **into** it, which
is what keeps `HJ4` off a hall that is nearly square. Every roof is a gable at pitch 1 — no shed. No
footing: the plate is the plinth. Spruce log posts at the corners, spruce beams over the storey joint,
and a course of **laid** spruce log in the upper wall for the beams to be the end of.

## The trees

Five, and **none of them on the pasture in front of the pass**: a wool a defender cannot see across is a
wool nobody defends. They stand at the yard's edge, in the lee behind the gate, and at the foot of the
lane. Copied bodies out of `showcase/tree-showcase` — the repository author's own trees.

## Numbers

| read | answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, no violation |
| `GET …/preflight` | **export gate OPEN** |
| `GET …/coverage` | reached 9 700 · dead **0** of 9 700 = **0.0% dead** |
| `03-slopes.txt` | 8 683 walked · 52 scrambled · 492 barrier; 11 faces, the largest the fold's own coast |
| `06-claims.txt` | placed 20, declined **0** |
| `…/walk` spawn → each wool | 25 blocks (2 placed) and 32 blocks (0 placed) |
| `…/sketch/relief/read` | team: 2 076 cells, y10..y19, range 9, **no barrier and no scramble** on the solved ground |

## What went wrong on the way

- **`roomStyles: {"cage": …}` is silently the wrong key.** `SketchRoomStyles` carries `wool` and
  `spawn`; `tools/README.md` and `drive.py`'s own docstring both document the wool half as `cage`. An
  unknown key in a snapshot draws no `RQ3`, so the board stored at 200, exported at 200 and built its
  wool rooms as **bedrock boxes** — `column?at=-45,75` read `y24 Bedrock · y16 Bedrock` where the barn
  should be. `showcase/16-forest` carries the same key. Renamed to `wool`, the same column reads
  `y26 Bricks`.
- **A house style in `dressing.styles` is a 500 without its discriminator.** A `PropStyle` is
  polymorphic, so a house entry is `{"kind": "house", "shell": …}` and a bare `HouseStyle` throws
  `NotSupportedException` out of `DressingJson.ParseStyles` — `RQ2`, the studio's own fault rather than
  the document's, where a 400 naming the missing field would have said what to do.
- **`drive.py` appends an `addShapes` entry to `groups[0]`, and `groups[0]` here is `neutral`.** The
  fold is listed first in the plan, so it compiles first, so every flight and every wall went onto the
  group that does not fan — one team's stairs and half a sheepfold. Each authored shape now names
  `"group": "team"`.
- **`RQ5` refuses a wool stated as `red`** on a board whose team is red. Both wools now state no colour
  and take the dyes the compiler picks.

## Open, and not the author's to settle here

Both wools sit on the same terrace, 25 and 32 blocks from the door, and differ in their **approach**
rather than in their distance: the barn is taken across the open yard after the gate, the byre up the
lane and through a flight at its own door. Whether two wools that are equally far but unequally
defensible read as balanced is a question about how a map plays, and this session has no oracle for it.
Built as stated.
