# Flintwick — the dark is only ever on a face

> A capture-the-wool board on two chalk headlands facing each other over a sound, worked for flint.
> Each team's two wool rooms are cut into the chalk behind its own spawn, and the only way across the
> sound is a bridge somebody builds in full view of both cliffs.

**In one sentence:** the board is white end to end and the one black material on it is painted by
*angle* rather than by place, so a black cell can only appear where the ground has an exposed face —
the sea cliff, the cut behind each wool room, the sides of a stair.

80 × 200 blocks, `rot_180`, cell 5, `maxPlayers` 24, ground y19–y35, observer y60. Six plan pieces,
two build zones, six relief marks, two pushes, eight authored shapes, three themes, **42 props placed
and none declined**.

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

`05-themes.txt`: `chalk 11 048 cells (80.7%)`, `strand 1 852 (13.5%)`, `knap 784 (5.7%)`, with
`173:0 Coal Block` present in the chalk's surface census and in the knapping yards' and nowhere else.
Borders: `chalk | knap 224 cells`, `chalk | strand 190`. The first is the excluded pad's own face; the
second is the cliff.

Angle distribution over 13 684 cells:

```
00-09° 45.5%   10-19° 21.1%   20-29° 15.4%   30-39° 11.2%   40-49° 5.8%   50-59° 1.0%
6.9% at 40° or steeper
```

`03-slopes.txt`: **12 476 walked, 688 scrambled, 520 barrier, 20 faces**, the largest 60 cells at
x −37..−22 z −79..−68.

## The fault-catalogue reads

**Empty board — 0.0% dead.** `GET …/coverage`: 13 684 ground cells, **13 683 reached, 1 dead**, no
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

The west stair's top did **not** land on the first build. `stair-w-hi` was cut to `DOWNLAND − 1` = 26
and the down it arrives on stands at 30 there, because the `nab-w` point mark and the grain are over
it — the last tread four courses under the ground it was supposed to reach, read at **(−29, 41)**.
That is `SK26`'s subject. Cut instead to the height the ground actually has, and extended from z 44 to
z 48 so the gradient holds:

| flight | run / rise | transect, after |
|---|---|---|
| `stair-w-lo` + `stair-w-hi`, x −33..−22, z 14..48 | 13 + 19 / 3 + 8 | `rises 1, falls 11, worst step 2: 0 barrier, 0 scramble, 0 drop \| walked end to end` |
| `ramp-e`, x 20..28, z 16..46 | 30 / 6 | `rises 1, falls 7, worst step 4: 1 barrier, 0 scramble, 1 drop — BARRIER +3 at (24, 44); DROP −4 at (24, 39)` |

**The east ramp's head is still not clean.** The down on that arm stands at 26 at (24, 46) and 29 at
(24, 44), and the flight's head sits between the two: a three-course step onto it from the north and a
four-course fall inside it. It walks end to end and it is not a way up anybody should have to use.
The fix is the same one the west stair had — read the ground where the head lands and cut the anchor
to it — and it is open.

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
| `HS4` | `doorHead.block` stone brick, fill quartz | a head's two corners and the line between them are one material |
| `SK4`/`SK3` | *'wall-e' is a path of width 0, so it draws no ground* | a **polyline states its band as `radius` and its centreline as `vertices`**, like every other shape. Given `width` and `points` it stores at 200, pre-flights OPEN, and is simply not in the world |

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

- **`SK26` on `ramp-e`'s head** — `BARRIER +3 at (24, 44)` and `DROP −4 at (24, 39)`. The same fix
  that cleared the west stair, applied to the east arm's own ground heights.
- **The `garth` · `spawn-red` seam**, above.
- **`fill-ratio 0.794`**, above.
- **A question for the author, not a claim:** the wick is a build zone, so the bay can be bridged as
  well as the sound. That gives a raider three crossings — the sound at either arm, and the bay
  between them — and the bay crossing is the only one that is *not* overlooked by a cliff. Is that a
  third option worth having on a capture board, or is it the one crossing that makes the other two
  pointless? Nothing in the corpus or in the rules answers it.
