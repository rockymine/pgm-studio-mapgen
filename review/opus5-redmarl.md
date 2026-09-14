# Redmarl — the gully is crossed on the diagonal

> A capture-the-wool board cut into a red marl gully. Each team's dyehouses stand on its own bank
> above a dry red watercourse; the wool is fetched out of the enemy's dyehouse, carried down into the
> gully and back up the far bank to a plinth at your own back.

**In one sentence:** the deepest and most saturated board of the warm set, where half the bounding box
is void and the only ground both teams stand on is a 56-block neck of dry riverbed that each side
comes onto at the opposite corner.

104 × 176 blocks, `rot_180`, seven plan pieces and one build zone, maxPlayers 20, ground y15..y32.

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
| flat, one theme, empty | `coverage` · `incline` | **0.0% dead** — two wool rooms, a spawn and two plinths a side put every cell on somebody's journey; angles 45.8 / 35.6 / 13.7 / 3.3 / 1.2 / 0.3 % |
| straight frontline | the `gully-pan` ring, plus bent `apron-26`/`apron-23` | the height boundary wanders; the theme boundary follows the channel |
| stark contrast, no separation | `05-themes.txt` + `transect -36,-96 → -28,-96` | marl 72.0%, works 23.4%, wash 4.6%; **every** works cell stands one course proud — the transect reads `-1` then `+1` at the yard edge |

`03-slopes.txt`: **11 236 walked, 258 scrambled, 202 barrier; 14 faces, largest 38** at x 1..4
z -32..-19 — the stair's east revetment, which is a wall on purpose.

The palette answer to *a sharp change of material needs a change of ground under it*: the pale built
family appears only on the three yards (a one-block plinth), on the revetments (walls) and on the
stair (a flight), and its surface was warmed with hardened clay so that where it does meet red ground
the two are nearer in value than smooth sandstone alone would be. The `wash` theme lies only in the
channel's own pans, so its edge is a break of slope.

## Limits

- `04-routes.txt` reports `barrier +3` and `+7` on the two routes out of red's own spawn. Those are
  the **iron cube** and the **spawn hall's wall**: the route walker treats both as terrain. The four
  routes that matter — each spawn to the two enemy wool rooms — read `worst step 0, walked end to end`.
- The dressing pass declined ten props on the first three builds and **nothing** on the last:
  the door approaches and the two vat pads claim more ground than they look like they do, two props
  cannot stand within about eight blocks of each other, and a prop is mirrored like everything else —
  three boulders spread across the gully neck each landed inside their own image's claim.
  `06-claims.txt` is the raster that says where to try; `placed 36, declined 0`.
- Nobody has played it. Whether a four-block face with two ways down per team is the right amount of
  wall in front of a wool carry is a question for the author, not for a read.
