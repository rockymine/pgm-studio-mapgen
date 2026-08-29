# Slipway — a harbour DTM built to a sketched composition

`specs/opus5-slipway`, driven `2026-08-29`. 240 × 264 blocks, `rot_180`, 28 players, two destroyables a
team. Symmetry error **0**, export gate **OPEN**, and **nothing the dressing pass declined**.

The board is the author's own composition, sketched at cell scale and scaled up here: a harbour with a
brigantine on it, a crane dock west of centre with the first goal's dock beside it, a port east with a car
park, the dockside town behind the west dock, a second settlement back and to the east with the other goal
in front of it, a terrace row across the middle joining the two, and a field on each arm for a balloon to
stand over.

## What it carries

Made things, each stated a different way, which is the point of the board:

| thing | blocks | layers | shapes | how it meets the ground |
|---|---|---|---|---|
| ship | 8,897 | 8 | 598 | floats — an absolute floor at the load line, no seat |
| balloon ×2 | 3,195 | 8 | 1,160 | flies — an absolute floor, no seat |
| crane ×2 | 810 | 4 | 107 | `seat: ground` — settles onto the dock, jib out over the water |
| mini car ×8 | 208 | 4 | 19 | `seat: ground` — four boxes and four cubes, 11 × 5 × 6 |

Beside them: sixteen houses from the style library, twelve trees, four crates, five roads and a harbour.

## The crane reaches over the water, and what that cost

The author asked for a dock that is flat and raised above the water, with the crane facing it and its cargo
reaching over. The crane is 23 blocks deep from load to back stay and the old dock was 12, so it sprawled
into the town behind. The dock is now `x −52..−28, z 16..36`, a flat terrace excluded from the relief, and
the crane stands at `(−40, 18)` unturned. Measured off `sketch/columns`:

| where | what the column holds |
|---|---|
| crane foot (−46, 20) | dock to y19, leg y20–26 |
| crane foot (−46, 22) | dock to y18, leg y19–22 |
| under the load (−40, 13) | seabed to y9, **water y10–16**, crate **y22**, head y27 |
| open harbour (−40, 0) | seabed to y9, water y10–16 |
| under the ship (0, 0) | seabed to y5, **water y6**, hull y7–20 |

**The load hangs six blocks clear of the water, seven blocks past the quay's edge.** That only works because
a seat is now measured from the columns a thing *rests on* rather than its whole shadow: reading the lowest
ground under the jib found the seabed and took the whole crane down to it (`WE61`).

**3,330 columns hold water, 32,863 blocks of it.** The harbour ring is the basin piece to the block: a pool
cuts its bed wherever the ground stands above it, so the old ring — drawn 40 blocks wider than the water's
own ground — dug the quay it lapped and flooded 1,524 columns of the balloon's field into a lake.

## Where the goals stand, and what the bands say

`Crane` stands on the dock beside the crane it is named for; `Car Park` stands at the corner of the port's
own. The author moved the second ten blocks toward the cars and said outright that the pair had been too
close for this shape of board and that the bands would be adjusted after. What that reads as, measured:

| | own walk | enemy walk | ratio | band |
|---|---|---|---|---|
| `Crane`, the dock goal | 104 | 158 | 1.52 | `GO4` [40,90] out · `GO1` [3,4] out |
| `Car Park`, on the port | 94 | 184 | 1.96 | `GO4` out · `GO1` out |

| pair | blocks | band |
|---|---|---|
| own pair `Crane ~ Car Park` | 72 | `GO2` [35,65] out |
| `Crane ~ its own image` | 70 | `GO3` [85,150] out |
| `Crane ~ Car Park` across | 80 | out |
| `Car Park ~ its own image` | 126 | in |

**Every one of those is the deliberate cost of two forward objectives.** The four bands are written for goals
in a defender's rear, and solved together they fix a board before a piece is drawn: writing the spawn
separation as `S` and a goal's own walk as `d`, `GO1` fixes `d ≈ S/2` and `GO3` then reads `≈ 2d = S`, so `S`
lands in [85, 150] and everything else follows. A goal at the water and a goal at a car park are not in that
model, and this board is the measurement that says what a pair of them costs.

## What the board taught

- **A landscape takes no rim.** `rimEdges: "boundary"` caps every plateau boundary — a face against a
  structure and against level ground the paint calls a different plateau included. On a stone quay that is a
  kerb; on grass and on terracotta it draws the plan back over the ground it was supposed to become. The two
  built grounds keep their rim and the five landscapes state none, so the surface runs to the edge.
- **A ground style built from wool is unplantable.** The dressing pass reads a wool-topped column as a stamp
  and declines everything on it (`DR-KEEP`). Nine of the library's 168 styles carry wool in their palette,
  and three of them were this board's surfaces: `white stone cells` paved the quay and the port,
  `stone dark voronoi` walled every riser, `grass clay surface dark` turfed the hill. Every surface here is
  now drawn from the wool-free 159.
- **A footing needs a foundation under it.** Thirty-two library styles rang a one-course plate with a
  footing, which `HS7` calls a one-block rim round a building with nothing beneath it. Their plates are two
  courses now.
- **A piece can collide with another piece's mirror, and no gate says so.** `balloon-field` and `port` did
  not overlap; the field's `rot_180` image and the port did, over 788 columns, and the port silently came
  out at the field's height. `PL4` reads the authored half only.
- **A subtract drawn by hand goes on describing the composition it was drawn against.** The first coastline
  was eight polygons written in absolute coordinates while the pieces stood somewhere else, and the pieces
  then moved five times. What they cut in the end was not a coast: `bay-back-e` and its image were **373
  cells each of fully enclosed void**, `bay-hill-m` took 463 cells out of the middle of the hill through a
  two-block neck, and `bay-town-n` took 327 out of the dock town — which is most of the reason the town
  held two houses. **Nothing failed.** The export gate walks the ground and the ground was still walkable
  round every hole, so the board built, the gate opened and the holes were only visible in a picture.
- **The outline to redraw is the one the compile already hands back.** `POST /plan/compile` fuses abutting
  pieces of equal height into one ring apiece, and those rings are the board's silhouette: the upland here
  is a single eight-vertex polygon — a stretched T where the spawn's approach steps back out of the hill —
  and the notch in it is one vertex. Redrawing that ring through `shapePropsById` is `showcase/04`'s own
  technique. Subtracting lobes off the perimeter was a second answer to a question the repo had answered.
- **A corner is drawn out, and that is what makes it safe.** A vertex moves only where the redrawn ring
  covers every cell the compiled one did and every cell it gains was void, its `rot_180` image included. So
  it cannot erode the shore, cannot reach into a neighbouring shape, and above all cannot open a **seam**: an
  edge shared with the shape beside it is exactly an edge whose outward side is that shape's ground, and a
  move across one fails the guard on its first cell. Drawing inward has no such property — every subtract
  has to be checked for holes by hand, which is how eight of them went uncaught.
- **Carrying one edge on beats opening the angle.** A corner drawn along its own bisector swings *both* its
  edges, so where one of them is a seam the move is refused outright — the terracotta field's west corner
  took the bisector and swung its north edge into the town. Taken along an edge instead, that edge stays
  collinear and only the other swings: the field grows a headland and the seam never moves. The bisector is
  tried last, and it is what a corner with two free edges takes — the reflex vertex inside the upland's
  notch, which is the one move worth most, because drawing it across the notch turns an L into a coast.
- **No two neighbours may move**, or the edge between them merely translates and the shape is the rectangle
  it was, somewhere else. A reflex corner is offered its move first, since only one of any pair gets one.
- **A Bézier leaves the polygon the guard read.** Bowing an edge shared with the shape beside it pushes
  ground over that shape whatever the straight ring did: the upland's north edge bowed 3 blocks into the
  town and left `destroyable-2` standing **6 blocks proud one block from the goal**. So an edge is bowed only
  where it faces open water along its whole length, and the test is per edge rather than per corner — `in`
  governs the edge arriving and `out` the edge leaving, so one corner bows its coast and holds its seam with
  a zero-length handle. A drawn corner also keeps 14 blocks off a goal, because a pad drawn to an
  objective's doorstep leaves the objective standing on the step it made.
- **What it costs is ground nobody walks.** The corners drawn out, none taking more than 320 cells, grew the
  board from 200 x 264 to **240 x 264**, and almost all of that is shore. The dead share went 27.2% → 38.8%,
  and back to **29.9%** once the fields the new coast made room on carried five buildings a side and the flat
  pad behind the port was deleted.
- **A thousand columns at one height is not ground, it is unfinished map.** The piece behind the port stood
  1,071 columns every one at y23 — no route across it, no relief mark over it, nothing built on it — and its
  `rot_180` image the same. Deleting it took 2,456 cells off the board and 4 points off the dead share, and
  the upland now reaches the corner it was filling.
- **`HP3` caps a placed building at 192 blocks of footprint, inclusive of both corners** — an 11 × 15 plot
  is 12 × 16 = 192 exactly and a 12 × 15 is 208 and refuses.
- **`LN2` measures a chain of collinear rects, not a piece.** Rects sharing a cross-axis interval and
  abutting merge into one lane however many pieces they are written as: 104 blocks is this board's longest.
- **A made thing raises the build ceiling**, which is the highest column plus twenty. The balloons crown at
  y82, so `<maxbuildheight>` is **100** rather than the 53 the terrain alone would give.

## The order the board has to be built in

Four of the five rebuilds on this board cost a re-search of every house plot, and each time for the same
reason: **a plot is only valid against the ground that existed when it was chosen.** The order is not a
preference, it is a dependency chain, and every step invalidates everything downstream of it.

1. **The plan's pieces.** Their rects decide what the compile fuses, and the compile's shape ids decide
   which rings the outline redraws. Move a piece and every id below can shift.
2. **The objectives.** A goal pins a `±10` square the dressing keeps clear and a 14-block standoff the
   outline keeps off, and it is what the four bands are measured between.
3. **The outline.** Corners drawn out add ground; a coast redrawn after a plot was chosen can take the
   ground beside it and leave the house standing on a bedrock face — the balloon shed and the warehouse
   stood 29 and 22 blocks proud exactly this way.
4. **The relief and the terraces.** Which shapes are excluded decides where the ground is flat, which is
   what a plot's own rise test reads.
5. **The roads.** They claim their paving and a house may not stand on it, so they carve the bands a
   settlement has left.
6. **The houses, then the trees and crates**, each searched against the finished ground.

**And the ground a plot is searched over is the ground with nothing on it.** A search run against the last
board's output reads every standing house as a seven-course rise and refuses the plot it already used — so
the measure strips the houses, trees and boulders from the layout and keeps only what carves and claims,
which is the water and the roads.

What a plot is searched for, and why each test is there:

| test | rule it stands for |
|---|---|
| every column of the plot and a three-block ring has ground | `DR-SITE` — a footprint over void seats on its lowest column and hangs off the rest |
| the rise across the footprint is under 4 | `DR-SLOPE` — the uphill side would be under the ground beside it |
| the stamped footprint's top, less the ring's floor, is under 4 | `WX11` — and **both ends read the footprint grown by two**, because a roof's oversail widens what the foundation levels |
| four blocks clear of every route's centreline | `DR-CROSS` — a road that runs on past the far wall makes two dead ends |
| outside every goal's ±13 square | `OB19` — a prop inside a goal's clearance |
| four blocks from every other plot **and every plot's image** | `DR-CLAIM` — a plot is stated once and fanned, so its own reflection holds ground |
| `(wide+1) x (deep+1) ≤ 192` | `HP3` — the cap is inclusive of both corners |
| clear of every made thing that marks itself kept clear | `DR-KEEP` — a crane's legs are ground, a balloon's envelope is air |

`DR-WAY` is the one the search cannot answer locally: it asks whether a building sends the way between two
waypoints more than ten blocks further round, which is a fact about the whole board. It is read off the drive
and fixed by moving the building — the quay store went to the water's edge for exactly this.

## What the board still complains about

Two are the author's own calls and one is cosmetic:

| rule | count | what |
|---|---|---|
| `ST2` | 1 | the iron stands outside the spawn piece, beside its door lane — the author asked for it there |
| `SP8` | 1 | the spawn's egress steps two blocks at `fore-spawn`–`spawn` |
| `WX11` | 28 | fourteen houses stand 2–3 blocks above the cell beside them, showing that much foundation |

The `WX11` are all doorstep-sized. The ones that mattered — a shed reading as a 53-block bedrock tower
because a balloon flew over it — were a defect in what the check read, not in where the house stood
(`WE61`).

## What to look at

| picture | says |
|---|---|
| `world-iso.png`, `world-iso-turned.png` | the board in the round, off `sketch/columns` through `tools/render/iso.py`. The only read that says whether a thing has bulk: a ship is a ship-shaped patch of planks from above |
| `world-ground.png` | the ground layer in real materials — the coast, the terraces, the paint |
| `world-topdown.png` | every category at once, by recorded provenance |
| `world-structure.png` | the buildings alone. **A made thing is not in it**, which is `WE62`: the ship read as the ground it floats on and a house beside a balloon read as a house standing on one |
| `world-made.png` | the made things alone, over the terrain they stand on or fly above, with nothing the dressing pass placed in the way |
| `world-section-x0.png` | the ship afloat with the balloons over it |
| `coverage.png` | which ground a journey actually uses |

## Coverage

`reached 23,774 · decorated 6,719 · dead 10,673 of 41,166 = 25.9% dead` on a board of 240 x 264. The dead
ground is the drawn shore and the port — a car park behind a warehouse is somewhere goods leave from, not
somewhere a lane runs through.
