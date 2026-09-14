# Flintwick — the dark is only ever on a face

> A capture-the-wool board on two chalk headlands facing each other over a sound, worked for flint.
> Each team's two wool rooms are cut into the chalk behind its own spawn, and the only way across the
> sound is a bridge somebody builds in full view of both cliffs.

**In one sentence:** the board is white end to end and the one black material on it is painted by
*angle* rather than by place, so a black cell can only appear where the ground has an exposed face —
the sea cliff, the cut behind each wool room, the sides of a stair.

80 × 220 blocks, `rot_180`, cell 5, `maxPlayers` 24, ground y19–y35, observer y60. Ten plan pieces,
two build zones, two plan walls, six relief marks, two pushes, eleven authored shapes, four themes,
**42 props placed and none declined**.

## The wick, and why the plan has a hole in it

The first plan was one full-width headland. It read `fill-ratio 0.9 outside authored band
[0.201, 0.542]` and a frontline of `widthBlocks 80, profile straight, z ±10` — a ruler drawn across
the board, which is the tell the fault catalogue names.

The answer was the board's own name. A **wick** is a bay, and the headland was cut into two nabs with
thirty-five blocks of open water between them, joined only behind the bay head:

```
 4 |AAAAAAooooBBBBBB|     A west-nab   x -40..-11  z 10..69
 8 |AAAAAAooooBBBBBB|     B east-nab   x  10..39   z 10..69
12 |AAAAAACCCCBBBBBB|     C wick       x -10..9    z 45..84   (the bay head)
16 |AAAAAACCCCBBBBBB|     o 40 cells of enclosed void — the bay
```

Two things changed with it. The frontline became **`profile offset`, running from (−40, 10) to
(40, 45)** — one team's front is now two faces at different depths, and a raider who lands on one arm
is on that arm. And the bay is a **build zone in its own right** (`wick-water`, x −10..9, z 20..44),
because a bay a player cannot bridge is a wall drawn as water; that also took each arm's inner face
from the ten-block funnel `FR9` complains about to thirty blocks of frontline.

`WL2` then fired — `spawn-wool-distance 25 outside authored band [27, 170]` — and the two wool rooms
moved out to the board's corners, which put a five-block gap of void either side of the spawn and is
the other half of what makes the back of the board legible.

**What did not clear: `fill-ratio 0.794`, still outside `[0.201, 0.542]`, a soft term at distance
1.48 on a `score 1.479` board with `valid true`.** The corpus says a capture board is under half land;
with the wick cut out this one is four-fifths. Getting under the ceiling needs roughly another 100
cells of void inside the piece bounding box, which at this board's size means arms under 25 blocks
wide — a different board, and a thin one for 24 players. It is recorded rather than chased.
*The same term is not measured at all on this run's two destroy boards, which have the identical
piece geometry and score 0.*

## A wool room stands at the end of its own spur

The first shape of this board flanked the spawn with its two rooms: red's spawn footprint x −15..15
z 85..100 and its rooms x −40..−20 and 20..40 **in the same z band**, five blocks of void apart. A
room a defender is already standing in is not a room anybody has to reach.

**No rule says so.** `WL2`'s text is *"on a different lane than the spawn; wool↔spawn ≥ 20"* and only
the second clause is measured — and the hard floor clears easily, because a room 20 blocks wide can
put its wool block far from the spawn point while the two footprints sit side by side. `WL6`, *each
wool on a distinct lane*, has no term at all. The board evaluated at `valid true` with nothing to say
about it.

The shape it wants is the composer's own, which reports every wool unit as `boxes: 2` — the room
**and** its lane — against `boxes: 1` for a spawn or a hub. `specs/opus5-coinfall` is the worked
example here: `camp` (spawn) → `run` (piece) → `plinth` (wool-room). So:

```
 13 |AAAAAACCCCBBBBBB|    A  west-nab   x −40..−10  z  10..70
 14 |DDDD  CCCC  EEEE|    D  lane-w     x −40..−20  z  70..80   ← wall at the far seam
 16 |DDDD  CCCC  EEEE|    D' head-w     x −40..−20  z  80..95
 17 |DDDD FFFFFF EEEE|    F  staith     x −15..15   z  85..100
 19 |GGGG FFFFFF HHHH|    G  knapp-w    x −40..−20  z  95..110
 21 |GGGG        HHHH|
```

Twenty-five blocks of lane, the width of the room, running off the back of each nab — with a column
of void either side of the spawn so the two never touch. The route to a room is now spawn → wick →
nab → lane → room, and there is no short way.

`fill-ratio` fell from 0.794 to **0.733** with the lanes cut in, which is the same measurement saying
the board has more void in it than it had.

## The wall on the lane, and the two ways to get it wrong

A lane is a way to walk and not a place to dress. This one carries one thing: a **bedrock approach
wall**, stated as a `PlanWall` between `lane-w` and `head-w` so it stamps at the seam **fifteen blocks
in front of the room's door**, which is where `ST8` seats one. Stated at the lane's mouth instead it
read `approach wall … stands 25 blocks from the wool room's entrance — about 15 in front is the seat`.

`column at (−30, 79)`:

```
y 34   30:0  Cobweb      the course you climb through
y 33   7:0   Bedrock
…
y 27   7:0   Bedrock
```

Three courses of bedrock over the lane's own ground with a cobweb cap — the studio's standard
approach wall, and the structure `B99` warns reads as impassable on the traversability render while
being nothing of the kind. `GET …/preflight` walks it: *spawn ↔ objective chain connected across the
build geometry*.

**It had to be got wrong twice first.** A wall's height comes from the **plan's** surface, not from
what the relief settles on: with the lane stated at 26 and the relief putting it at 31, the wall's
top landed at y30 and the terrain buried it, cobweb and all — a wall in the document, no wall in the
world, at 200 and `OPEN`. The lane's four pieces are now stated at 31, read off the built world, and
`EL1`'s resulting five-block complaint against `west-nab` is not in the world: both solve within a
block of each other and the transect up the lane reads `worst step 0`.

And a **`level` flight on the lane cut a hole in it.** A ramp up the head, anchored 26 → 30 from the
plan's numbers rather than from the ground, put a five-course slot across the mouth — `DROP −5 at
(−30, 78)` — which made the spur one-way. The lane's own terrain already climbs it; both flights came
off. A lane needn't be flat, and what it must not have is a hole.

Up the lane now, (−30, 64) → (−30, 100):

```
rises 0, falls 0, worst step 0: 0 barrier, 0 scramble, 0 drop | walked end to end
```

and the wool sits at the end of it: `<wool team="blue-team" color="red" location="-30,30,102">`.

## The one argument the board makes

```json
{"kind": "layered", "axis": "slope", "stack": {"bands": [
  {"thickness": 12, "material": <white clay / quartz over three chalk>},
  {"thickness": 20, "material": <rubble and gravel over three chalk>},
  {"thickness": 58, "material": <FLINT / andesite / gravel over three stone-and-chalk>}]}}
```

Twelve degrees of down, twenty of shoulder, and everything over thirty-two is knapped flint — one
course of it over three of chalk, because a surfacing band that fills its own depth is how a board
comes out made of its own skin. The `wall` bucket, which is the exposed riser, carries the same
flint. So every white-to-black boundary on this board is a break of slope, and there is no band of
dark laid across a white plain anywhere on it.

**And chalk downland is grass.** The first build of this board had no soil anywhere in its palette —
white clay, quartz, gravel, shingle, flint — so every tree on it stood on a built or a bare block:
quartz, cobblestone, stained clay, and one thorn seated on **Coal Block**. A tree growing out of a
floor is not a tree. Two things answer it. The under-12° band's top course is now a `cell` that picks
grass one time in five, so the flat mottles rather than reading as a white plate; and a fourth theme,
`sward` — grass over coarse dirt over chalk — is painted in three hollows where soil actually stays:
the coombe and the lee of each arm.

`05-themes.txt`: `chalk 8 966 cells (64.3%)`, `sward 2 790 (20.0%)`, `strand 1 852 (13.3%)`,
`knap 336 (2.4%)`, with `173:0 Coal Block` present in the chalk's surface census and in the knapping
yards' and nowhere else. Borders: `chalk | sward 478 cells`, `chalk | knap 224`, `chalk | strand 190`.

Every one of the nine trees, read on the built world:

| (−34,50) | (−38,56) | (−37,48) | (30,66) | (36,64) | (16,58) | (−8,58) | (8,62) | (6,54) |
|---|---|---|---|---|---|---|---|---|
| Grass | Coarse Dirt | Grass | Coarse Dirt | Coarse Dirt | Grass | Grass | Grass | Grass |

One sarsen lies on the strand, which is where a chalk coast puts the flints the cliff has already
given up.

Angle distribution over 13 684 cells:

```
00-09° 54.7%   10-19° 15.3%   20-29° 12.3%   30-39° 9.7%   40-49° 6.6%   50-59° 1.4%
8.0% at 40° or steeper
```

`03-slopes.txt`: **12 882 walked, 568 scrambled, 494 barrier, 16 faces**, the largest 148 cells at
x −19..12 z −73..−45.

## The fault-catalogue reads

**Empty board — 0.0% dead.** `GET …/coverage`: 13 944 ground cells, **13 943 reached, 1 dead**, no
dead patch large enough to list. Two objectives a side plus a spawn between them is the shape that
reads this way by construction, and the wick is what keeps the two arms on separate journeys.

**Objective hidden — no.** `GET …/column?at=-30,92`, a wool room's own cell:

```
y 36   44:7   Quartz Slab      the room's roof
y 27   35:14  Red Wool         the wool
y 26   4:0    Cobblestone      the yard it stands on
```

A wool room is a room, so a roof over the wool is the point; what matters is the way in, and
`04-routes.txt` walks each of the four rooms end to end — `red-0 along z: rises 1, falls 0, worst step
2: 0 barrier, 1 scramble` with the scramble a +2 at (−30, 82), which is the step up out of the cut
yard into the room.

**Spawn faces away — no.** Red spawns at (0, 31, 92) with `yaw 180`. Its two targets are the enemy
wools at (±30, −92); the bearings are **170.7°** and **189.3°**, so the door is 9.3° off each and
splits them exactly.

**Spawn faces a wall — no.** (0,92) → (0,78), the first fourteen blocks out of the door:
`rises 2, falls 1, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end`.

**Stairs that end nowhere — two authored flights, one with a fault.**

## Both flights arrive, and neither fault was the flight's

The west stair's top did **not** land on the first build. `stair-w-hi` was cut to `DOWNLAND − 1` = 26
and the down it arrives on stands at 30 there, because the `nab-w` point mark and the grain are over
it — the last tread four courses under the ground it was supposed to reach, read at **(−29, 41)**.
That is `SK26`'s subject. Cut instead to the height the ground actually has, and extended from z 44 to
z 48 so the gradient holds:

It took three more reads to close, and **neither remaining fault turned out to be the flight's**.

**The east ramp's head was blocked by the board's own wall.** `BARRIER +3 at (24, 44)` and
`DROP −4 at (24, 39)` came from a plateau at y28 spanning z 40..44 — which is `wall-e`, the
cliff-top field wall, standing two courses proud straight across the head of the ramp. A wall drawn
along one line without regard to where the flight arrives. Each arm's wall is now **two runs with a
gateway between them**, and the gateway is where the way comes up: `wall-e-a` ends at x 19 and
`wall-e-b` starts at x 29, with the ramp at x 20..28 between them; the same on the west, gapped
x −31..−21 for the stair. A drystone wall with two gates is also what one actually looks like.

**The west stair was being flattened by its own paint.** Once the wall came off it, the stair read
`DROP −4 at (−29, 40)` again and the stations showed a dead-flat y31 from z 41 to z 50 — the flight
simply was not there. The cause is `sward-west`: a `raise 0` paint patch drawn **after** the flights
sets those columns back to the median ground, so a shape the author can see on the canvas is not in
the world. The three sward patches now go down first and the flights are cut into them.

| flight | run / rise | transect, after |
|---|---|---|
| `stair-w-lo` + `stair-w-hi`, x −33..−22, z 14..48 | 13 + 16 / 3 + 7 | `rises 1, falls 11, worst step 2: 0 barrier, 0 scramble, 0 drop \| walked end to end` |
| `ramp-e`, x 20..28, z 16..46 | 30 / 6 | `rises 0, falls 8, worst step 3: 0 barrier, 0 scramble, 0 drop \| walked end to end` |

`stair-w-hi`'s anchors are now read off the built world at x −29 — y24 at z 32 below the face and y31
at z 48 above it — rather than taken from the plan's `DOWNLAND`. One number for two different grounds
is what put it wrong twice.

**Stark contrast with no area separation — no**, by construction: see the slope stack above.

## The two standing relief complaints

`POST …/sketch/relief/read` → `cells 6842, low 19, high 35, relief 16, symErr 0`, and two `RL3`:

| pair | step | worst at | cells | what it is |
|---|---|---|---|---|
| `cliff` · `ledge` | 4 | (−36, 29) | 55 | the shelf halfway up the west cliff meeting the cliff foot — the board's subject, and the reason the west is a two-step climb |
| `garth` · `spawn-red` | 3 | (−15, 84) | 30 | the `swell` push at (−6, 78) lifting the garth three courses over the spawn piece's own corner |

The first is wanted; the second is not, and the fix is to move the swell off the spawn row. It is a
complaint rather than a refusal, it is at a piece corner and not on a route, and `04-routes.txt`
walks the spawn's own crossings at `worst step 1`.

## What the pipeline refused on the way

| rule | what it said | what it was |
|---|---|---|
| `G8` | `fill-ratio 0.9` | one full-width headland; became two nabs and a wick |
| `WL2` | `spawn-wool-distance 25`, band `[27, 170]` | wool rooms too close to the spawn |
| `FR8`/`FR9` | a 10-block frontline is a funnel | the bay was not a build zone |
| `ST9`/`ST10` | 24 × 11 footprint, 40 × 15 spawn piece | a spawn piece is at most 20 × 30 |
| `ST8` | the approach wall stands 25 blocks from the room's entrance | about 15 in front is the seat, so the lane is two pieces and the wall stamps at their seam |
| *(nothing)* | — | a wool room **butted onto the spawn**. `WL2` measures only its distance clause and `WL6` has no term, so a board with no lane at all evaluates clean |
| `HS4` | `doorHead.block` stone brick, fill quartz | a head's two corners and the line between them are one material |
| `SK4`/`SK3` | *'wall-e' is a path of width 0, so it draws no ground* | a **polyline states its band as `radius` and its centreline as `vertices`**, like every other shape. Given `width` and `points` it stores at 200, pre-flights OPEN, and is simply not in the world |
| *(nothing)* | — | a `raise 0` paint patch drawn after a flight **flattens it**, in silence. No rule fires; only a transect along the flight says so |

## The gate

```
round-trip       pass
mirror check     pass   spawn/protection ✓  build ✓
buildability     pass
traversability   pass
export gate      OPEN
06-claims.txt    placed 42, declined 0
world void       24 roofed void(s), 2 of them sealed
```

## What is open

- **The `garth` · `spawn-red` seam**, above.
- **`fill-ratio 0.794`**, above.
- **`04-reach.txt` now lists eight patches of standing ground it says no player can get to**, the
  largest 6 787 cells at floor y19 with reason `no-build-zone`. Two direct reads disagree: the west
  stair walks from the down to the strand (`(−29,40) → (−29,10)`: `worst step 2, 0 barrier`) and the
  strand itself walks the full width at z 12 (`worst step 0`). The file's own header says such patches
  need not be faults. Which of the two readings is right is not settled here.
- **A question for the author, not a claim:** the wick is a build zone, so the bay can be bridged as
  well as the sound. That gives a raider three crossings — the sound at either arm, and the bay
  between them — and the bay crossing is the only one that is *not* overlooked by a cliff. Is that a
  third option worth having on a capture board, or is it the one crossing that makes the other two
  pointless? Nothing in the corpus or in the rules answers it.
