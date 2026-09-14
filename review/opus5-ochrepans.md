# Ochrepans — every sightline is broken by a wall, not by a hill

> A king-of-the-hill board on an ochre salt-works. Three square pads: a centre pan sunk in a walled
> evaporation yard, and two flank pans out on the raised pan banks.

**In one sentence:** the flattest ground of the warm set and the steepest board in it — 52% of the
surface lies under ten degrees and 6.2% stands at forty or more, because all of its height is wall.

104 × 192 blocks, `rot_180`, **two** plan pieces and a spawn, maxPlayers 16, ground y18..y26,
observer y62, `scoreLimit` 750.

## The plan states almost nothing on purpose

`works-n` (z -76..-28, its image the far half) and `works-mid` (z -28..28), both at surface 22, plus a
28 × 20 `stead`. That is the whole plan. It is two rectangles rather than one only because `LN2` bands
a piece's longest side at 110 blocks and a single 152-block works is a lane with no junction in it.

Everything else is authored: sixteen `area` marks at 21 for the pans, one at 26 for a bank, one at 18
for the yard, four polyline wall runs, four flights and two ring-wall cisterns. A plan with a piece per
pan would be a plan whose paint follows the cutting.

## The relief is quiet and the board is not

`cells 11613 · range 8 · level 0.682 · largestField 0.282 · seams 0 · silentMarks 0 · symErr 0`

By the usual reading that is a table with edges, and on this board it is the point. The height that
matters is not in the relief at all:

| the thing | how high | what it does |
|---|---|---|
| a pan | **1 down** | a bench, so the pale crust inside it never meets the ochre on flat ground |
| the yard | **4 down** | the centre pad is held from above, by whoever is on the wall |
| a pan bank | **4 up** | the flank pads are held from below |
| the yard wall | **3 proud of the flat, 7 above the yard floor** | cannot be climbed and cannot be seen over |

`03-slopes.txt`: **16 536 walked, 325 scrambled, 811 barrier; 10 faces, largest 148** at x 5..27
z -29..-9 — the yard's east wall, which is a wall.
`incline`: 52 / 32.2 / 7.4 / 2.2 / **2.5 / 2.2 / 1.6** %. The tail past forty degrees is four times any
other board here and every block of it is masonry or a cut face.

## What the reads say

| fault | the read | what it says |
|---|---|---|
| objective hidden | `column` at each pad | The Sump: white clay at y18, open sky above it but its own marker at y55–57, `ground 0° from level`. West Pan: y25, 0°. East Pan: y25, 0° |
| spawn faces away | intent yaw 0 vs bearing to (0,0) | ~1°. The board is straight ahead out of the door |
| spawn faces a wall | `transect -2,-86 → -2,-64` | worst step 0, 0 barrier, walked end to end |
| stairs that end nowhere | `walk` from the spawn to each of the three pads | `(0,0)` worst step 0 · `(-41,-19)` worst step 0 · `(41,19)` worst step 0 — all three **walked end to end** |
| flat, one theme, empty | `coverage` | **51.3% dead** — and this number is not about this board (below) |
| stark contrast, no separation | `05-themes.txt` + `transect -52,-56 → -26,-56` | ochre 73.9%, crust 13.8%, works 8.9%, sward 3.4%; `crust|ochre` 832 cells of border and the transect across a pan reads `worst step 1` — every one of those cells is a one-block bench |

## The coverage number is the read's blind spot, not the board's

`GET /coverage` answers `journeys 3` and `markers` = **two spawns and one crossing**. The three control
points are stated in the finish (`controlPoints`), never reach the plan, and are therefore not places
the coverage walk knows about — so the two largest dead patches, 4 362 and 4 149 cells, sit exactly on
the two flank pads. The ground the board is played for reads as ground nobody goes to.

`04-routes.txt` says the same thing more plainly: *no route between a spawn and a goal*. The `walk`
reads above are the substitute, and they are clean.

## The fault a transect found and a picture never would

The two pan banks were first drawn as one `area` mark each, centred on z 0 and reaching 19 blocks
either side. Built, the west bank existed from z -19 to -1 and then fell **seven blocks**, and the
control point standing on that seam answered `ground 61° from level`. Splitting the ring into two, one
each side of the centre, changed nothing.

Four columns settle why: `h(-45,-5) = h(45,5) = 26` and `h(-45,5) = h(45,-5) = 19`. **The relief is
solved for z ≤ 0 and rotated onto the rest**, so a mark centred on the centre line is built on one side
of it and not the other, and a second ring drawn in the half that is never solved contributes nothing.

The fix is the arrangement, not the ring: the bank moved wholly into z -32..-6, and its own image is the
east bank at z 6..32. The two now stand **diagonally opposite**, which gives each team a near pad and a
far one, and both pads read `ground 0° from level`. `preflight` opened the gate on the broken version,
`relief/read` reported `seams 0`, and no render showed it.

## The author's pass: two conifers and four seats

`spar-1` and `spar-2` carried the same bodies the author found on dustwath — **acacia log under birch
leaves** (`162:12` under `18:14`) at thirteen and fifteen blocks, which is a pine silhouette on a
salt-works. The feedback named dustwath only; the same check across all four boards found them here
too. Both are dropped from the style registry rather than left unused, and their two placements are
`thorn-1`/`thorn-2`, which are acacia under acacia at nine.

All four thorns stood on scraped sand. The board now carries a fourth theme, **`sward`** — grass over
two dirt over sandstone — laid as four seven-point rings, one under each. Savanna Plateau puts the grass
at olive, and the cell carries the flat's own sand beside it. `column` at all four trunks now reads
**`161:4 Acacia Leaves`**, and the dressing pass declines one boulder and nothing else.

## Limits

- There is still a four-block step at z 0 out at x ±45, where one bank's end meets the flat. It is at
  the board's far flank rather than through its middle, and both ramps onto each bank are elsewhere.
- The flat is not uniformly 22: the gates, ramps and banks each pin their own height and the unmarked
  ground between them solves to base, so the works reads between 19 and 22 in places. It is `rot_180`
  symmetric, so both teams meet the same ground.
- Nobody has played it. Whether a sunk pad and two raised pads should be worth the same per second, and
  whether a board whose cover is built rather than terrain counts as having enough of it, are questions
  for the author.
