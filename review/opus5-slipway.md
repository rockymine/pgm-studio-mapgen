# Slipway — a harbour DTM built to a sketched composition

`specs/opus5-slipway`, driven `2026-08-29`. 240 × 264 blocks, `rot_180`, 28 players, two destroyables a
team. Symmetry error **0**, export gate **OPEN**, and **nothing the dressing pass declined**.

The board is the author's own composition, sketched at cell scale and scaled up here: a harbour with a
brigantine on it, a crane dock west of centre with the first goal's dock beside it, a port east with a car
park, the dockside town behind the west dock, a second settlement back and to the east with the other goal
in front of it, a terrace row across the middle joining the two, and a field on each arm for a balloon to
fly over.

## What it carries

Made things, each stated a different way, which is the point of the board:

| thing | blocks | layers | shapes | how it meets the ground |
|---|---|---|---|---|
| ship | 8,897 | 8 | 598 | floats — an absolute floor at the load line, no seat |
| balloon ×2 | 3,195 | 8 | 1,160 | flies — an absolute floor at y48, no seat |
| crane ×2 | 810 | 4 | 107 | `seat: ground` — settles onto the dock, jib out over the water |
| mini car ×8 | 208 | 4 | 19 | parks — an absolute floor at the port's own surface, four boxes and four cubes, 11 × 5 × 6 |

Beside them: sixteen houses over **four** styles, fifty-four trees, five crates, five roads, a harbour and
six flights of stairs.

**A car parks rather than seats, and that is one course.** A seat lands a made thing's lowest course on the
ground's own top block — right for a building whose foundation cuts into the surface, and a course too low
for a wheel: the cars read sunk into the tarmac. The port is one flat terrace under all eight of them, so the
floor the model was drawn at is the floor it wants, and stating it outright is the whole fix. The crane still
seats, because a crane stands on a dock the relief did not promise to keep level.

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

## The port is walled on two sides, and a stair is a thickness

The port floors at y21 and two grounds stand over it: the terracotta field the balloon flies off, at y28
along the whole water side, and the settlement the spawn road comes down from, at y29 along the back. Seven
blocks and eight of bedrock face, on the one piece of the board a player crosses lengthways. Neither could
be climbed, and neither showed up in a gate: the export walks the ground and the ground is walkable *round*
a wall, so the board built, the gate opened and the wall was only visible from inside it.

**A stair is a thickness over the ground it is laid on, so it is one layer and not a shape apiece.** The
`port-stairs` layer states `base_y: 22` — the port's own surface — and every shape on it is a height above
that rather than an elevation. That is what lets a flight be one polygon: the two corners at the foot carry
one course and the two at the head carry the face's own, and the rasterizer TIN-interpolates across the
footprint and rounds per cell, which is a staircase. The anchors are stated half a course either side of
those numbers (`0.5` and `rise + 0.5`) because a cell is sampled at its **centre**: anchored on the whole
numbers every tread falls on a tie, and `Math.Round`'s banker's rounding turns a 1:1 flight into a
two-block step. Half a course off, every cell centre lands on a whole course.

**And it climbs along the face rather than into it.** A flight cut square into a wall puts a player at the
top still walking the way they climbed, and what is at the top here is a car park on one side and a street
on the other. Turned ninety degrees, the climb ends on a landing level with the ground above and that
ground is a step to the side — which is why the flight is five blocks deep rather than the width of the
thing it serves. Measured on the built board at `z 16..20`, the water face:

| x | 72–76 | 77 | 78 | 79 | 80 | 81 | 82 | 83 | 84–88 | 89–94 |
|---|---|---|---|---|---|---|---|---|---|---|
| top | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 28 | 21 |

— the port, seven treads at one block each, then a 5 × 5 landing flush with the field at `z 15`. Its foot
stands five blocks east of the car park rather than two, because a stair a player has to squeeze past a
bumper to reach is a stair in the car park.

**The back face carries a pair, and the second is the first turned about.** One flight is a way up; two
climbing away from each other is a choice of which way to go up. Measured at `z 51..55`:

| x | 44–48 | 49–53 | 54–61 | 62–72 | 73–80 | 81–85 | 86–92 |
|---|---|---|---|---|---|---|---|
| top | 21 | 29 | 29→22 | 21 | 22→29 | 29 | 21 |

**The flights face each other and the landings go to the ends**, which is the author's call and the right way
round: a landing is a solid block the full height of the face, so a pair of them in the middle reads as two
towers standing off the wall, and at the ends they read as the wall itself. What a player walking the port
meets in the middle is then stairs rather than masonry, with eleven blocks of port between the two feet.

The water face takes one flight and not two, because the frontage east of the car park is 22 blocks and a
pair wants 35 — the room is there only west of the cars, and a stair over them is the thing the first move
was undoing.

**A flight is stone and a landing is the ground it joins.** The treads are the port's own masonry carried up
the face, so the climb reads as built; the landing is the last block before a player is simply on the field
or in the settlement, so it is paved as that ground — the terracotta of the field on the water side, the
meadow on the back. Measured on the built board, the field landing comes back `#a05325` against the field's
`#a05325` at `z 15`, and a tread `#7a7a7a`. What it stops is a climb ending on a grey plate somebody has to
notice is not a floor.

Every flight and every landing is marked `keepClear`, which is what the word is for — a shape drawn to *be*
something is terrain by construction and indistinguishable from the ground beside it, so without it a road
repaints the treads and the dressing pass seats a crate on them.

**One statement, six stairs**: three are authored and the group mirrors, so each is answered at the far arm's
own face.

## The upland is a wood, and the door's fan is not

The upland is the one ground on this board a player crosses on foot the whole way, from the spawn's own
door to the settlements, and bare grass at that width reads as a field to walk over rather than as
somewhere. Forty-two oak and birch at eight to eleven blocks — the stock the rest of the board already
carries — stand on the meadow shape and nowhere else, west of the spawn's approach and east of it.

**A wood at one pitch is an orchard.** Each trunk is kept its own crown's radius plus a gap from every
other, and the gap runs between one block and six over two sines of incommensurate period, so the upland
carries thickets and glades instead of a lattice. The radius is measured rather than nominal: a tree is
deterministic and RNG-free, so an oak at h9 reaches two cells and at h11 three, and the search knows that
before any world exists.

**The ground in front of the door carries no trunk however free it reads.** A forest that closes over a
spawn's egress is a wall rather than cover, so the fan — `x −26..22` from `z 88` to the room itself — is
left open, and every trunk stands off a route's claim by four blocks where `DR-ROAD` asks three, off every
building's claim by its own crown, and outside the objectives' standoff. Zero declined.

What it bought is traffic: **decorated ground went 6,719 → 9,452 columns and the dead share 25.9% → 19.3%**,
because ground a player has reason to walk through is not dead ground.

## The ground is a stack, not a face

**Two grounds on this board are built and five are landforms, and they want different models.** A theme can
paint a column two ways: as a *face* — a one-course surface, a wall down every exposed riser, and a rim
capping the plateau boundaries — or as a *stack* of courses read down from the top block. The quay and the
seabed take the face, because a quay is masonry with a kerb along its edge and a cut wall where it drops to
the water, and the basin shelves the same way. Everything else takes the stack.

**What a wall does to a landform is draw it as a diagram of itself.** It paints every exposed riser in one
material, so a hillside comes out with a rind on it and a rim `rimEdges: "boundary"` caps every plateau the
paint can tell apart — including a face against a structure and against level ground. A hill is not a thing
with a face; it is a thing made of something, all the way down. So the three landforms are stated as courses
and the painter is left one `Fill` band spanning the whole column, over which a `layered` material on the
depth axis *is* the courses:

| ground | 0 | 1 | 2 | 3 | 4 | remainder |
|---|---|---|---|---|---|---|
| meadow | `meadow · surface` | `dirt fractal` | `dirt fractal` | `dirt fractal` | `stone fractal` | `stone fractal` |
| terracotta | `rust cells` | `rust cells` | `dirt fractal` | `dirt fractal` | `dirt fractal` | `stone dark voronoi` |
| dock | `dirt fractal` | `dirt fractal` | `stone dark voronoi` | | | `stone dark voronoi` |

Read back off the built world at `(−50, 62)`: grass, dirt, granite, granite, cobble — soil over subsoil over
rock, which is what a cut through a hill should show. At `(−88, 5)`: granite, granite, dirt, dirt, spruce,
gravel. The last band repeats, so it is the remainder however deep the ground runs.

**And one green, not three.** `grass clay surface`, `oldstone · surface` and `meadow · surface` were three
greens doing one job, and a player crossing from the dock town to the hill to the back settlement read three
grounds where the board means one. The meadow is what survives and it carries the whole upland — the dock
town, the terrace row, the hill, the spawn's approach and the settlements behind it. Sampled off the claims
it comes back `#79c05a` on 79–95% of its columns with `#5d421f` podzol in the rest, and that one figure now
answers for all three.

## The town is four roofs, not eleven

Eleven styles over sixteen plots is a catalogue rather than a town: nothing recurs, so nothing reads as
belonging anywhere. Four survive, and **the ground decides which two a plot may take** — a pair is enough,
because two roofs alternating down a street is a settlement while one is a terrace and four is a sample book.

| ground | the two it takes | the plots |
|---|---|---|
| the meadow | `@17h-hall` red-brick gable · `@sb-spawn` stone gable | cooperage, arcade-e, granary, upland-hall · sailmaker, arcade-w, counting |
| the quay and the port | `@17h-hall` · `@sn-compass-well` diorite and blue clay | quay-store, port-office · harbour-office, warehouse |
| the terracotta fields | `@hoar-longhall` white gable · `@sb-spawn` stone gable | balloon-shed, field-cottage, field-byre · balloon-store, field-barn |

**No plot moved.** A footprint is a position the board's ground was searched for and a style change is not a
reason to re-search one, so the sixteen rectangles, their fronts and their claims are exactly what they were:
zero declined, and the same seven units raise the same fourteen `WX11`.

`@sb-spawn` is the spawn hall's own style, which is why it recurs: the room a team leaves from is a building
of the same town rather than a shape from somewhere else.

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

- **A ground style built from wool is unplantable — and the rule is about the top block.** The dressing pass
  reads a wool-topped column as a stamp and declines everything on it (`DR-KEEP`). Nine of the library's 168
  styles carry wool in their palette, and three of them were this board's surfaces: `white stone cells` paved
  the quay and the port, `stone dark voronoi` walled every riser, `grass clay surface dark` turfed the hill.
  Every surface is drawn from the wool-free 159 now — but `stone dark voronoi` is back as the *remainder*
  under the terracotta and the dock, because nothing is planted on ground four courses down.
- **A road is the lane, so the lane's keep-out must not stop it.** The spawn road is authored to `(0, 114)`,
  inside the spawn's own piece, and it paved 228 cells — narrowing from seven wide to one and ending at
  `z 100`, twelve blocks short. The cause is the door approach: twenty blocks out from the room's face, in
  the keep-out mask, and `PlaceStroke` was reading the whole of that mask. But the mask is about things that
  **stand** on ground, and a stroke stands on nothing — it replaces one course of finish, and in front of a
  door it *is* the ground the approach is being kept clear for. A stroke now reads `KeepOut.Structure` alone,
  which is a room floor, a wall, an iron cube or a shape that marked itself `keepClear`; a stamped column is
  caught by the pass's own per-cell test instead, with no margin, so the road runs to the wall and stops at
  the wall. **367 cells now, full width, into the hall's doorstep at `z 116`.**
- **A tube aimed at a curved surface has to be aimed at where the surface is.** The balloon's load tapes ran
  from the load ring at y14 out to radius 13.2 at y20.5 — but the envelope's profile is only 5.1 wide there,
  so every tape ended **8.2 blocks outside the fabric**, four black sticks fanning into the air at 51° off
  the vertical. The profile passes radius 13 at y29, so that is where a tape ends now: 28° off the vertical,
  a block clear of the skin the whole way up and meeting it at the shoulder. Measured on the model, tape
  blocks touching the envelope went **0 → 24**.
- **A footing needs a foundation under it.** Thirty-two library styles rang a one-course plate with a
  footing, which `HS7` calls a one-block rim round a building with nothing beneath it. Their plates are two
  courses now.
- **Beams are a farmhouse's detail and a spawn hall has none.** `BeamStyle` runs a log out past each corner
  where two storeys meet, which is the one thing a style writes outside its own footprint — and on the
  stamped spawn it read as four oak stubs on a masonry building. `@sb-spawn` states no `beams` at all now,
  which is `BeamStyle`'s own default, and the hall's walls run to their corners.
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
- **The build ceiling clears the buildings and never the balloons.** It is twenty blocks over the highest
  block the map builds that a player meets, which on this board is the spawn hall's ridge at y48, so
  `<maxbuildheight>` is **68** and every goal marker hangs at y73. The board is what moved the rule (`G6`
  amendment 25): the balloons crown at y97 and a `SurfaceTop` measure asked for 117, clamped to
  `BuildGenerator`'s 100; the terrain alone tops at y33 and would have capped the town five blocks over its
  own roofline. A made thing is out because it is scenery hung in the air, and an objective is out because a
  goal floats by design and a cap derived from one could never be beneath it — which is the whole of `OB23`.

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
6. **The stairs**, which are ground and therefore above every prop: a flight is laid against a face the
   relief and the outline have already settled, and it raises the surface the props below it are then
   searched against.
7. **The houses, then the trees and crates**, each searched against the finished ground.

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
| `WX11` | 14 | six houses and the port goal stand 2–3 blocks above the cell beside them, showing that much foundation — seven units, each raised for its own image |

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
| `world-foliage.png` | the wood as trunks rather than as a mass, which is the only read the tree count can be taken off |
| `coverage.png` | which ground a journey actually uses |

## Coverage

`reached 23,774 · decorated 9,452 · dead 7,940 of 41,166 = 19.3% dead` on a board of 240 x 264. The dead
ground is the drawn shore and the port — a car park behind a warehouse is somewhere goods leave from, not
somewhere a lane runs through.

**`reached` did not move, and that is the honest reading of what the wood bought.** Coverage walks the
authored routes, and no route was added: every one of the 2,733 columns is `decorated`, which is ground a
player has a reason to be on rather than ground a lane crosses. What it shows up in is the patch list — the
two bare upland patches of 1,183 and 1,165 cells are gone outright, and the port and its image fell from
3,245 and 3,198 to 2,648 and 2,601. The two 410-cell patches that replace them at the top of the list are
drawn shore, 43 blocks out, which is coast rather than unfinished map.
