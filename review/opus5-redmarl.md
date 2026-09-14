# Redmarl — the gully is crossed on the diagonal

> A capture-the-wool board cut into a red marl gully. Each team's dyehouses stand on its own bank
> above a dry red watercourse; the wool is fetched out of the enemy's dyehouse, carried down into the
> gully and back up the far bank to a plinth at your own back.

**In one sentence:** the deepest and most saturated board of the warm set, where half the bounding box
is void and the only ground both teams stand on is a 56-block neck of dry riverbed that each side
comes onto at the opposite corner.

104 × 256 blocks, `rot_180`, nine plan pieces and one build zone, maxPlayers 20, ground y15..y32.

## A wool board is judged on how empty it is, and nothing else is

The plan was written twice. The first was a full rectangle — five bands spanning the whole width, no
void anywhere — and it scored **1003** with three refusals. Two of them were shape refusals no destroy
board ever sees:

| term | this board | band | who is asked |
|---|---|---|---|
| `fill-ratio` (`G8`) | 1.0 → **0.53** | 0.201 – 0.542 | **CTW only** — probed by swapping the wools for a destroyable, at which point the term disappears |
| `max-chain-length` (`LN2`) | 128 → 72 | 25 – 110 | every board; it is the longest side of a piece, in blocks |
| `WX6` | refused | — | a wool room wholly inside another piece has no seam to enter by; it must **abut** |

So the shape is not a preference. A wool board in this corpus is a lane-and-yard board with half its
box missing, and the second plan is built to that: each team's ground is offset to its own flank
(`x -52..16` for red, its image for blue), the two corners neither reaches are void, and the neck
between them is the mid piece. `heftfold` is the same idiom at 0.519.

`WL2`/`WL7`/`WL9` then fixed the back row's arithmetic: a 28-block spawn piece (`ST10` caps it at
30 × 20) cannot hold 30 blocks of separation on its own, so each **wool marker stands at the far side
of its room** — 30 blocks from the spawn point, 60 from the other marker.

## Each wool room stands at the end of its own lane

The first build put both dyehouses in one row with the spawn, sharing edges — `dye-w.maxX =
yard.minX`, `yard.maxX = dye-e.minX` — so the two rooms sat **eight blocks** from the spawn with no
lane anywhere between them. **No gate catches this.** `WL2`'s text reads *"on a different lane than the
spawn; wool↔spawn ≥ 20"* and only the second clause is implemented, and the rooms were wide enough to
put the wool block 33 blocks away while touching; `WL6` — each wool on a distinct lane — has no term at
all. `POST /plan/evaluate` answered `score 0, valid true` on a board that was wrong.

The back is now built the way the composer builds a wool unit — as **two boxes, the room and its lane**:

```
yard  (spawn)      x -32..-4   z -104..-88      the bank's back edge
lane-w (piece)     x -52..-32  z -112..-88      24 blocks, the width of the room
dye-w  (wool-room) x -52..-32  z -128..-112     at the lane's far end, two courses up
```

and the same to the east, so the spawn sits between the two lane roots and every raid commits to a
spur. The markers stand at the rooms' deep outer corners: **37.5 blocks** from the spawn, **56** from
each other, ratio **1.0**.

**The lane is a way to walk, not a place to dress.** Nothing is planted on either one. What is on them
is a **bedrock bar across each**, at z −100, in two runs with a six-block gate between — `column?at=-48,-100`
reads `y29 · y28 Bedrock` and `column?at=-41,-100` reads the track through the gap. That is the one
thing that belongs there, because it says where a raider has to come through.

**The climb into the room is a ramp, and it took two reads to get right.** `WL11` complained that the
approach climbs two blocks; it walks the pieces flat and cannot see what is authored, so a transect is
the judge. The first attempt put an authored ramp up the lane's last fourteen blocks and still read
`scramble +2 at (-41,-117)` — the dyehouse yard was standing a course **proud** of its plinth, and the
proud course sat on top of the ramp's own rise. Seating the two dyehouse yards flush with their plinths
(the spawn's yard keeps its riser; nobody has to climb that under fire) gives:

```
lane-w  (-41,-88) → (-41,-122)   rises 2, falls 2, worst step 1: 0 barrier, 0 scramble | walked end to end
lane-e  ( 6,-88) → ( 6,-122)     rises 2, falls 2, worst step 1: 0 barrier, 0 scramble | walked end to end
```

## Four grounds, and every join chosen

| ground | stated by | why |
|---|---|---|
| the marl bank, 26 | an `area` mark, bevel 4, with two dunes pushed up behind the dyehouses | the ground the row stands on |
| the apron, 23 | an `area` mark, bevel 4, one low swell | open ground, not a table |
| the brink, 21 | an `area` mark, **bevel 2** | a small bevel is what makes a lip a lip |
| the gully neck, 17 | an `area` mark, **bevel 1**, its ring wandering six blocks either side of the plan's straight `z` | the frontline is the mark's edge and not the rectangle's |

The watercourse is a `line` mark at 14.5, `r 6`, `tread 2`, running the neck's diagonal; its own
`rot_180` image comes up the other diagonal and the two meet at the centre. `seams 0`,
`silentMarks 0`, `symErr 0`, relief range 17, `level 0.464`, `largestField 0.121`.

## Two descents a team, both authored, both measured

```
wash-stair  (-2,-40)→(-2,-14)   rises 2, falls 4, worst step 1: 0 barrier, 0 scramble | walked end to end
slip-w      (-20,-40)→(-20,-14) rises 1, falls 5, worst step 1: 0 barrier, 0 scramble | walked end to end
```

`EL1` complains about all three plan seams (3, 2 and 4 blocks). It walks the pieces flat and cannot
see either flight; the transects above are the answer. The stair is `height_mode: level` with
`anchor_heights [21,21,17,17]` over sixteen blocks of run, and it carries a **material** rather than a
theme, because a stair is a thing somebody built and a theme is a place.

One thing the first build got wrong and a transect caught: the `braid` line mark passed under the
slip's foot and cut it to 15, two below the gully floor, so the slip ended in a hollow —
`scramble +2 at (-20,-16)`. Moving the braid four blocks into the neck fixed it.

## What the reads say

| fault | the read | what it says |
|---|---|---|
| objective hidden | `column?at=-48,-96` | the wool room floor is red wool at y26 on hardened clay, flush with its yard. It is a room by design |
| spawn faces away | intent yaw 0 vs bearing to (47,96) and (-11,96) | 18.4° and 2°. Within the bar |
| spawn faces a wall | `transect -18,-99 → -18,-78` | 21 stations, worst step 1, 0 barrier, walked end to end |
| stairs that end nowhere | the two transects above | both walk |
| flat, one theme, empty | `coverage` | **0.0% dead** of 13 382 — two wool rooms, a spawn and two plinths a side put every cell on somebody's journey, the lanes included |
| straight frontline | the `gully-pan` ring, plus bent `apron-26`/`apron-23` | the height boundary wanders; the theme boundary follows the channel |
| stark contrast, no separation | `05-themes.txt` | marl 72.2%, works, sward and wash the rest; the spawn's yard stands one course proud and the two dyehouse yards sit flush on their plinths, which is a ground change of its own |

`03-slopes.txt`: **12 694 walked, 441 scrambled, 513 barrier; 20 faces, largest 44** at x -6..4
z -103..-98. The barrier count trebled when the lanes went in, and all of the new barrier is the four
bedrock bars — which are walls on purpose, each with a gate through it.

The palette answer to *a sharp change of material needs a change of ground under it*: the pale built
family appears only on the three yards (a one-block plinth), on the revetments (walls) and on the
stair (a flight), and its surface was warmed with hardened clay so that where it does meet red ground
the two are nearer in value than smooth sandstone alone would be. The `wash` theme lies only in the
channel's own pans, so its edge is a break of slope.

## The author's pass: a seat of soil under four trees

Four of the six copied bodies stood on hardened clay or bare marl — `holt-1` (−8, −78), `holt-2`
(−42, −42), `holt-4` (20, −20) and `holt-5`, which stood at z +16, in the half the relief never solves,
so a patch drawn under it there would have painted nothing. It moved to (−10, −14).

The board now carries a fourth theme, **`sward`**: grass over two dirt over red sandstone, laid as
six seven-point rings with the radius wobbled per point. The cell carries red sand beside the grass so
the patch feathers out rather than ending on a line, and Mesa pulls the grass brown, so this is scrub
holding on rather than a lawn.

`transect (-46,-42) → (-38,-42)` reads flat ground at 23 with `tree holt-2` standing on it, and the
column beside the trunk reads **`y22 Grass Block · y21 Dirt · y20 Dirt`**. `05-themes.txt`:
`marl | sward` 376 cells of border, and the dressing pass declines **nothing**.

## Limits

- `04-routes.txt` reports `barrier +3` and `+7` on the two routes out of red's own spawn. Those are
  the **iron cube** and the **spawn hall's wall**: the route walker treats both as terrain. The four
  routes that matter — each spawn to the two enemy wool rooms — read `worst step 0, walked end to end`.
- The dressing pass declined ten props on the first three builds and **nothing** on the last:
  the door approaches and the two vat pads claim more ground than they look like they do, two props
  cannot stand within about eight blocks of each other, and a prop is mirrored like everything else —
  three boulders spread across the gully neck each landed inside their own image's claim.
  `06-claims.txt` is the raster that says where to try; `placed 36, declined 0`.
- `04-routes.txt` reads `barrier +6 at (-16,-91)` on the route from the spawn to the east wool. That
  coordinate is the **spawn hall's own stone-brick wall** (`column?at=-16,-91` → `y26 Stone Bricks`) —
  the route walker goes through the building rather than out of its door. Walked from east of the hall,
  `(-6,-86) → (10,-124)` reads `worst step 0, walked end to end`.
- Nobody has played it. Whether a four-block face with two ways down per team is the right amount of
  wall in front of a wool carry is a question for the author, not for a read.
