# Redwash Mesa — destroy the monument

**Two badlands mesas face each other across a bottomless seam, and every crossing is made at one of three
heights.** Each mesa is a high table cut by a dry canyon. The team's cliff house stands on a ledge at the canyon's
head, one monument stands out on the table by a rock pool, and one stands in the plaza of the adobe town on the
canyon floor. The board is 192 by 128 blocks, mirrored across x = -0.5, two monuments a team, teams of twenty.

```
cd freeform/lib && python3 -m pgmvox.run trials/opus/redwash-mesa --build <scratch>/redwash-mesa --skip write
```

The run takes about 90 seconds, nearly all of it the read-back's voxel walks; generation takes one second.

## How it plays

**The land comes in three levels, and so does the seam.** The Table is at 62, across the north and the west. The
Shelf (a ledge along the canyon's north wall) and the Bench to the south are at 52. The Wash, the canyon floor,
steps down from 43 at its head to 40 at the seam. Each level meets its mirror across 18 to 24 blocks of void, so
a team chooses its crossing by height: Table to Table, Bench to Bench, or through the Gate where the two canyons
face each other, 18 across at 40.

**The spawn is the cliff house, on a ledge at 52 at the canyon's head.** The Table's cliff rises ten blocks
behind it and eleven blocks of the team's own land lie behind it. A stair of ten steps is cut up the cliff to the
Table (the Ladder), and one of nine is cut down to the canyon floor (the Head stair). So the spawn sits between
its two monuments, one up and one down.

**The table monument stands out on the Table, 54 degrees off the line between the spawns.** Two blocks of
obsidian float two over the ground at 62. The Table Path runs past it from the Ladder to the rim. The rock pool,
a basin of water at 58, lies between it and the seam, so an attacker crossing at the Table goes round it north
or south. A stand of olive (junipers) on the Table's north gives cover to within 13 blocks.

**The wash monument stands in Arroyo Town's plaza, 27 degrees off the line.** Four adobe houses stand two against
each canyon wall, with a market row along the north side, and the plaza is paved round the monument. The Shelf
looks down on it from eleven blocks up, and a stair of eleven steps climbs from the town onto the Bench.

**The two monuments are 53 apart, a north and a south, with the spawn between them.** That is the composed pair
`approaches.md` asks for: the defence is two places to hold, not one line.

### The ways onto each monument

| Monument | Way | Blue's walk onto red's (plan) | Who reaches its mouth first |
|---|---|---|---|
| table | across the rim at the Table, south of the pool | 148 (the shortest) | red 66, blue 121 |
| table | across the rim, north of the pool | 158 (x1.07) | red 73, blue 129 |
| table | through the junipers | 170 (x1.14) | red 71, blue 147 |
| table | up the Silver Drift: from the canyon floor through the gallery and up the shaft onto the Table, 19 from the monument | 179 (x1.21) | red 47, blue 124 |
| wash | up the Wash through the Gate and the town | 132 (the shortest) | red 58, blue 115 |
| wash | off the Shelf, a drop of eleven onto the plaza | 141 (x1.07) | red 33, blue 126 |
| wash | across at the Bench and down the Bench stair | 142 (x1.08) | red 59, blue 130 |

**Each monument is reached from around, above, below and through.** The table monument is reached round the
pool, through the junipers, and from below up the drift's shaft. The wash monument is reached through the town,
from above off the Shelf, and around by the Bench. No way costs more than 1.21 times the shortest, and the
defenders reach every way's mouth first.

### Walk numbers, both teams

| Walk | Plan (octile) | Built world (moves) |
|---|---|---|
| Spawn to its own table monument, red / blue | 48.2 / 48.2 | 56 / 56 |
| Spawn to its own wash monument, red / blue | 40.3 / 40.3 | 48 / 48 |
| Enemy spawn to the table monument, bridging | 148.5 / 148.5 (26 bridged) | 162 / 162 |
| Enemy spawn to the wash monument, bridging | 131.2 / 131.2 (24 bridged) | 141 / 141 |
| GO1: enemy over own, table / wash | 3.08 / 3.26 | 2.89 / 2.94 |
| Silver Drift: portal to the gallery's end, onto the Table, to the table monument | — | 23, 36, 66 |
| The Shelf over the town to the wash monument, dropping / with no drop past three | — | 11 / 23 |

**The Shelf is a perch with a way down, which the plan did not show.** The plan reads the Shelf's lower cliff as
a drop of eleven. The built walk found a walk down with no drop past three, 23 moves to the monument, where the
Shelf runs out at the canyon's east end.

**The built walk to the enemy's table monument is 162, over GO3's 150.** The plan's octile walk is 148.5; the voxel
walk counts four-way moves. Board 1's report reproduces the difference.

## Renders

| File | What it shows |
|---|---|
| `renders/00-plan-sketch.png` | the plan (v2): the board, the seven ways onto red's monuments, three cuts, red's walk unrolled, the check |
| `renders/00-plan-sketch-v1.png` | the first plan, before the hoodoos and the cut corners |
| `renders/05-topdown-annotated.png` | the built top-down with the plan's names, footprints and markers |
| `renders/30-iso-board-se.png`, `31-iso-board-sw.png` | the board from two corners |
| `renders/32-iso-arroyo-town-se.png` | the town, cut at 51 so the canyon walls do not hide it |
| `renders/33-iso-cliff-house-se.png` | the cliff house on its ledge, the Ladder and the Head stair |
| `renders/34-iso-table-monument-sw.png` | the table monument, the rock pool and the drift's hoist |
| `renders/35-iso-the-gate-se.png` | the two canyons meeting across the seam |
| `renders/40-xray-silver-drift.png` | the gallery and the shaft in x-ray |
| `renders/10-section-canyon-x-47.png` | a cut across the canyon through the wash monument |
| `renders/11-section-wash-z24.png`, `12-section-table-z-24.png` | cuts down the Wash and across both Tables |
| `renders/50-elev-cliff-house-from-the-wash.png` | the cliff house as the Wash sees it |

## Read-back

- **`Objectives.check`:** no problems.
- **`audit.footing`:** 0 problems (6 red sand blocks over air were found and fixed: see below).
- **Standable columns over the void:** 0 (2 were found and fixed).
- **The studio's reader:** valid, 2 teams, 2 spawns, 4 destroyables, 1 kit, 5 apply rules, no issues.
- **The build:** 505,436 blocks, 12 trees, 10 tile entities (the banners and the stalls' chests).

## The plan

**Arrangement.** The places on each half:

| Place | What it is | Why a player goes there |
|---|---|---|
| Cliff House | two adobe houses cut into the cliff on a ledge at 52 | the spawn |
| The Ladder, the Head stair | stairs cut into the cliffs, sandstone, open to the sky | the spawn's ways up and down |
| The Table | the mesa's top at 62, with hoodoos as cover | the table monument's ground |
| Table Monument and the Rock Pool | the monument, and a basin at 58 between it and the seam | the objective; the pool splits the front approach |
| Juniper Stand | olive on the Table's north | the covered way onto the table monument |
| The Shelf | a ledge at 52 along the canyon's north wall | the defenders' perch over the town; an attacker's drop |
| Arroyo Town | four adobe houses, a plaza, a market row | the wash monument stands in it |
| The Wash and the Gate | the canyon floor, stepping to the seam | the low crossing |
| The Bench and the Chimney | the south at 52, a butte to 70, hoodoos | the third crossing; the Chimney frames it |
| Silver Drift | a gallery rising from the canyon floor and a shaft onto the Table | the way from below onto the table monument |

**The look.** The biome is mesa, so the grass in clumps on the flats is olive and sits in the orange. The ground
is badlands: red sand, orange clay and red sandstone, with coarse dirt ringed by hardened clay as patches. The
cliffs are mesa banding at fixed heights: hardened clay with orange, yellow, white, brown and thin red and pale
beds. Building is pale (smooth sandstone adobe with dark oak vigas, sandstone stairs and trails) and the accent is
cyan clay round the windows, the pool and the banners.

**What the build adds:** the stalls, the vigas, the hoist over the shaft, dead bush and cactus on the sand at about
one column in seventy, tall grass on the grass, and the olives. No tree, stall or dressing stands within eight
blocks of a monument, and the town's nearest house is five from the wash monument, over the rule's four.

## Decisions, and why

- **Three crossing heights.** A mirror board's two halves face each other straight on; three levels give the
  attack a choice the symmetry does not, and each level leads to a different monument.
- **The spawn between its monuments.** The goal rules want each monument three to four times nearer its own
  spawn than the enemy's. A spawn up on the Table made the wash monument a long climb down; on the ledge it is
  about 45 from both.
- **Stairs cut into the cliff, not graded slopes.** A stair is made, and reads as the same stone the whole way;
  the cliffs stay sheer and banded.
- **One tree species, olive.** Board 1 used acacia; the mesa takes olive, with dead bush and cactus as its dry
  ground cover.

## What went wrong, and how it was found

- **The goal rules failed twice on the first plan.** The wash monument was 33 from its spawn (under GO4's 40), and
  the table monument's ratio was 2.87 (under GO1's 3). The check found both; the wash monument moved seven east
  and the table monument six west.
- **The way off the Shelf was unreachable in the plan.** Its waypoint was on cells that were not at 52. The
  check's "inf" found it.
- **Two adobe houses stood on the canyon wall.** Their floors came out 47 and 49 where the town is 41. The plan's
  house floors (`houses()`) showed it; the canyon was widened at the town and the houses re-seated.
- **The north stairs were laid a column off.** `build.stairs` widens to the right of the climb, so a stair rising
  north widens east and one rising south widens west. Reading the code found it before a render did.
- **Red sand hung over the Ladder's cut.** The cut was three blocks over every step and tunnelled under the
  Table's edge at the top. The read-back's footing found 6 blocks; the cuts are open to the sky now.
- **The cliff house's site eased ground out over the void.** The read-back found 2 standable columns past the
  island's edge. The houses moved two east; the library bug is below.
- **The first plan was large flats.** The v1 sketch shows the Table's north-west and the Bench's south-west
  empty; hoodoos went in as cover and the two far corners were cut back.

## What the plan missed

- **The Shelf's east end.** The plan stated the Shelf's height and not where it ends, so it did not show the walk
  down at the canyon's mouth. A row "the Shelf to the floor without a drop: none" would have caught it.
- **How a stair is laid.** The plan's flight is centred on its line; the generator's stair widens to one side.

## Friction log

### What the library lacked, written locally

- **A canyon with a shelf.** `landform.canyon` cuts walls rising to the ground as one profile. A canyon whose north
  wall carries a ledge partway up, and whose two walls rise to different grounds, is written in `plan.land`.
- **A stair cut into a cliff.** `build.stairs` lays the steps; the open cut above them and the parapet beside them
  are local.
- **The same flight in the plan and the world.** `Raster.flight` takes a width either side of its line and
  `build.stairs` a width to the right of the climb, so each flight is converted by hand in `gen.py`.
- **A shaft in the plan.** The gallery is storey 1; the shaft's ladder up onto the Table is an `extra` edge pair
  per half (`plan.links`).
- **Hoodoos.** `landform.spire` with a high taper makes them, which worked first time.
- **Fixed-height mesa beds.** `terrain.beds(strata, None)` lays them at world heights, which is what a mesa
  wants, and worked first time.

### Bugs, with reproductions

**`build.site` writes into void columns round a footprint at an island's edge.** Its eased ring is filled from
`ground_at`, and a void column's ground is -1, so it fills a wall from the bottom of the world:

```python
from pgmvox import World, B
from pgmvox import build as BLD
w = World(0, 0, 12, 12, sy=20)
w.fill(0, 1, 0, 5, 8, 11, B.STONE)            # ground only for x <= 5; x >= 6 is void
cells = {(x, z) for x in range(3, 6) for z in range(4, 8)}
BLD.site(w, cells, 10, lambda x, z: w.top(x, z), margin=2)
print(sum(1 for x in range(6, 12) for z in range(12) for y in range(20) if w.id(x, y, z)))   # 52
```

The fix is to skip a ring column whose ground is under 0, or to take a `land` mask.

### What in the guide was unclear

- **Where a destroy board's own scenery may stand near a goal.** The guide and `approaches.md` give four blocks of
  clearance; `ORDER-OF-WORK.md` speaks of a ten-block clearance tested at export. This board kept eight.

### Wanted, how hard, what it would take

| What I wanted | How hard it was | What a library or studio feature would need |
|---|---|---|
| A canyon with a ledge on one wall | 15 lines | `landform.canyon(..., shelves=[(side, height, width)])` |
| A stair cut into a cliff, drawn once | 25 lines and a bug | `build.stairs_from(R, flight)` laying the plan's flight, with `cut=True` |
| A shaft walked by the plan | 8 lines | `plangraph.ladder(R, (x, z), from_storey, to_storey)` giving both edges and their images |
| A site that stays on the land | found by the read-back | `build.site(..., land=mask)` |
| The read-back to measure the goal rules in the plan's units | not solved | a walk in octile blocks, or GO rules stated in moves |
