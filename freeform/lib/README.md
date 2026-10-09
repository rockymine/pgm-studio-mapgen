# pgmvox — the shared library for freeform boards

The twenty freeform boards each carried their own copies of the same helpers, and the copies drifted.
`freeform/SHARED-LIBRARY-ASSESSMENT.md` measured it: 15,800 of about 50,000 lines were copies, there were nine
colour tables, a symmetry table that lost its rail fix, and a walk whose headroom check could never fire. pgmvox is
the one copy. New boards import it; the twenty finished boards are left as they were built.

## What is in it

| Module | What it does |
|---|---|
| `blocks` | `B`, the 1.8 ids by name; the block classes (`PASSABLE`, `CLIMBABLE`, `NOT_GROUND`, `SIGHT_CLEAR`, `GRAVITY`, `FORBIDDEN_IN_PLAY`); names and colours per id and data |
| `orient` | the data for a block facing a way (`stair`, `ladder`, `torch`, `door`, `log_axis`, `yaw`, `rotation16`); turn tables for `cw`, `ccw`, `half`, `mirror_x`, `mirror_z`; `turn_world` about a named axis |
| `world` | `World` (set, fill, column, top, heightmap, chests, signs, banners, save, load); `write` to region files through the studio's Anvil writer; `seed` and `rng` for named random streams |
| `noise` | `fbm`, `ridged`, `smoothstep`, `spline` |
| `shapes` | polygons, polylines, discs, rings, ellipses, tapered strokes, `boundary`, `edge_depth` |
| `move` | the 1.8 tick model: `fly`, `fall`, `fall_damage`, `jump_reach`, `knockback`, `solve_launch` |
| `plan` | `Raster`, the plan as every column's floor and kind, with `Symmetry` drawn in the plan; `rect`, `poly`, `where`, `flight`; `storey(n)`, an upper storey drawn the same way; `from_heights`, a plan read off shaped terrain |
| `objectives` | spawns, the observer point, hills, flags, wools and monuments, destroyables, cores, score boxes and portals: each stamps its blocks, writes its regions and XML, carries itself to the other team, and checks the built world |
| `solid` | the repository's `tools/sculpt/solid.py` (booleans, turns, revolves, extrusions, tubes), with `fill` into a `World` and `image` through a plan `Symmetry` |
| `pieces` | `Course`, the plan of a board played in order (a water drop, a parkour run): pieces by step with their images, the links between steps, and an audit of each link's gap, drop, way across, landing cell and damage; `raster()` turns a course into a `Raster` |
| `plangraph` | the walk over a plan and its storeys: `graph`, `jumps`, `dijkstra`, `route`, `path`, `arrivals` per team, `pad_edges` |
| `sight` | `line_clear`, `visibility`, `hidden`, with an opaque test for a plan or a built world |
| `sketch` | the annotated sheet: map panels (a plan raster or a built top-down) with heights, places, markers, routes, jumps, zones and callouts; true-scale and unrolled sections; the checker's numbers against their targets |
| `build` | `Frame`, a building's own axes at any heading; `RoofField`, the studio's six roof forms block for block, and `lay_roof`; `house`; `parapet`, `site`, `stairs`, `ladder`, `Claims` |
| `facade` | face patterns (`band`, `courses`, `flutes`, `panels`, `slits`, `checker`, `windows`, `glyph_row`, `word`) set back or flush on an `extrude`d mass, `coffer`, `top_course`; floor fields (`border`, `medallion`, `corners`, `diamonds`, `steps`, `star`, `cross`, `tiles`) composed by `first_of` and laid by `carpet` |
| `terrain` | `slope_deg` as the studio reads it; `lay` (ground painted by slope, a snow line); `Strata`, `bed_offset` and `beds` (rock beds that tilt and fold); `mountain_ring`; `underside` and `root_depth` (cones, flutes, spires); `cloud_deck` |
| `route` | `find` (a least-cost route over the ground, held to a grade, switchbacks and all), `network` (places joined by roads that share their trunk), `simplify`, `smooth`, `footprint`, `pave` (surface and bridges), `steps` |
| `brittle` | the Brittlebush style from a blueprint of five-block cells: flat, keep, stair, stacked, gap and water cells; the five-course cap with its birch panels, a one-block outline, sand fields and double-ringed beds; hollows and tunnels under a deck with their dark-oak pillars; `house`, storeys of whole cells; `tower`, `heart` |
| `studioplan` | a plan drawn in the studio's planner (version 2) read as a `brittle` blueprint: pieces, stairs, decks, water and bare zones, placements |
| `props` | small built things placed on a floor, facing a way: `stall` and `stalls` (a market row), `lamp`; chests drawn as rows of letters (`laid`), with a defence chest and a wool room's gear |
| `under` | caves and mines carved into a built world: `tunnel` (a level-floored passage), `chamber`, `carve`, `dress_cave` (floors, stalactites, ore), `gallery_line` and `gallery` (timbered, railed, stepped), `shaft` |
| `trees` | hand-built trees planted whole: `library` (the studio's copied trees), `load` (a board's own cut), `kinds`, `plant` (turned, refused whole), `scatter` (a wood with its crowns apart) |
| `forms` | scenery built block by block where a heightfield cannot say it: `tower` (rings tapering up a stack, ledges every few courses, bulging faces, beds in courses, a crown and vines), `skirt` (karst faces under a floating floor's rim), `root_vines` |
| `landform` | heightfield operations: `watercourse` (reaches and falls), `canyon` and washes, `spire`, `butte`, `scarp`, `terraces`, `stage`, `grade` (a route held to a grade, bridging water, keeping earlier roads), `lake`, `coast`, `hold`, `blend` |
| `walk` | the voxel walk over built blocks with `MoveRules`; `no_stand_above`, `catchers`, `unreached`, `nearest`, `gap_cleared` |
| `audit` | `footing`: blocks that would fall, or have nothing to hang on; `loose_water`: water standing against air |
| `render` | `iso`, `elevation`, `cutaway` along any polyline, x-ray, `trim`, all in the studio's colours |
| `plot` | the bounded canvas a contributor builds a plot into, and `check_alone` with its verdict |
| `mapxml` | `Doc` and `E`, an element builder with the pieces every writer repeated |
| `run` | the build pipeline: `python3 -m pgmvox.run <board-dir>` |

## The block table comes from the studio

**`data/blocks.json` is written by `data/export_blocks.cs` from the studio's own palette code.** It holds every
id's display name, colour per data value, role and shape, and the data each block takes under the five symmetry
operations, as `BlockGeometry.Turned` turns it. Re-run the export after a studio change:

```
cd /tmp && dotnet run /path/to/freeform/lib/pgmvox/data/export_blocks.cs -- /path/to/freeform/lib/pgmvox/data/blocks.json
```

**The studio leaves some families unturned on purpose, and `orient` turns them.** Its turn copies a prop, which
keeps the way it was drawn; a freeform board turns whole halves. Doors (with the hinge swapped by a mirror),
trapdoors, rails and powered rails, sign posts and standing banners, wall banners, pumpkins, beds, buttons,
levers, repeaters, hay and quartz pillars are turned through their own direction encodings. A test turns every id
and data value there and back under every operation.

## The conventions it settles

**Heights.** In a `Raster`, `H` is the y of the floor block, and a player stands at `H + 1`. In a `World`, y is a
block's own height. The early boards meant three things by "height"; the library means these two and names them.

**Symmetry.** A `Symmetry` names its operation and its axis. The default axis, (−0.5, −0.5), lies between blocks
−1 and 0, so a half turn sends (x, z) to (−1 − x, −1 − z); an axis of (0, 0) turns about block 0. The library
applies symmetry in the plan, so the checker measures both halves.

**Directions.** One vocabulary everywhere: "e", "w", "s", "n", or a (dx, dz) offset; x is east and z is south.

**Random numbers.** No module keeps a generator at module level. A board makes named streams with
`rng(board, name)` and passes them round, so moving a function does not change what it draws.

**Eye height.** One eye height, 1.62 over the feet, and one aim point, 0.9. Sight lines are sampled at a quarter
block, so the plot check's out-of-sight counts run a little higher than Curio's own kit, which sampled at half a
block and let more lines slip between block corners.

## The sketch is a reviewed drawing, not the plan

**A board has three drawings of itself, and the library keeps them apart.** The plan is data: the raster and its
pieces, with `PLAN.md` saying why. The sketch is the plan drawn and annotated before anything is built, with the
checker's numbers on the same sheet, and it is what the author reviews. The annotated top-down is the same
annotation drawn over the built world afterwards, to show the board landed where the plan put it.

**The annotations are what make a sketch readable, so they are the library's, not each board's.** Every panel's
title carries its legend. Floor heights are written on each piece, places are named with a halo, objectives and
spawns are team-coloured discs, and routes end in arrows. Between pieces only the shortest jump is drawn, with
its gap. A detail too small to write on gets a callout with a leader line.

**Symmetry is drawn as well as computed.** Given the plan's `Symmetry`, the image half is washed paler, and
anything drawn with `both=True` appears in both halves, a red marker turning blue in the image.

**A section is true scale, and it can follow a route.** `SectionPanel.raster` cuts along x or z, `along` unrolls
the plan under any polyline such as a team's walk, and `level` draws the kill height or a water line across it.
`Sheet.row` sets sections side by side as 2a and 2b. `TablePanel` lists each measurement with its target and
marks a miss in red, so the review sees it first.

**`examples/islets/` draws both.** `scripts/sketch.py` writes `renders/00-plan-sketch.png`, and `renders.py`
writes `05-topdown-annotated.png`, where the plan's island outline is ghosted over the built blocks.

## Objectives

**An objective is one object from the plan to the map.xml.** A `Hill`, a `Wool` or a `Core` stamps its own blocks,
names the ground it claims, writes its own regions and XML into a `mapxml.Doc`, and reads the built world back.

**Each one checks what makes it playable.** A spawn checks there is room to stand. A monument checks its slot is
air over something to place on. A core checks there is lava in it.

**The XML is the studio's shape, and the studio reads it.** Control points carry the long attribute names and the
defaults the studio's generator chose from the corpus. Destroyables and cores name a `{id}-region`, and a wool's
monument is a named block. `data/read_mapxml.cs` runs the studio's own parser and validity check over a written
map. It reads the library's spawns, hills, wools, destroyables and cores as a valid map, and Islets with them.

**The studio does not read every objective the boards used.** It refuses a map with flags or score boxes, which
the King of the Flag and Deathmatch boards needed. The library writes them, and the studio is where they are
missing.

**Regions follow one convention.** A `Box` is inclusive blocks written with an exclusive max, since a PGM cuboid
spans `[min, max)`. A point is a block written at its centre, where a player stands. Region ids are refused when
taken, because a duplicate silently re-points every reference.

**An objective is drawn once.** `Objectives.add` adds a team's objective and its image for the other team: boxes
and points turned, yaws turned, team and id swapped, and any field given for the image changed, such as a wool's
colour. The sketch draws every marker from the same objects, in its team's colour.

## Capture boards

**A capture board is crossed by building, and the plan walk says how much.** `plangraph.graph(bridge=zones)`
joins every cell of a build zone to its eight neighbours at any height, tagged as built, and `PlanRules(diagonals=
True)` walks corner to corner, so distances are the octile ones a capture board's targets are set against.
`measure` gives a route's cost and how much of it was built: "79, 22 of it bridged".

**A wool is drawn once and carries its room.** `Wool` places its wool in the room and its monument on the other
side, writes the spawner and the room's entry rule, and checks both blocks. `Objectives.write` keeps each team's
rooms from the other team's hands but for what an attacker brings in. A `Spawn` may name blocks that are mined in
it and grow back, and `mapxml` writes kits and a kill height by instant damage.

**The voxel walk builds too.** `MoveRules(build=(mask, (lo, hi)))` lets a player stand in a build zone's air as
on a placed block, and `kill_y` counts nothing below the kill height as a place.

**A chest is drawn as three rows of nine letters and a legend.** `props.laid` turns them into the chest's items and
refuses a row that is not filled the same from either end, so heavy stacks balance and tools sit in the middle.
`props.DEFENCE` is a defence chest for a team's wall and `props.ROOM_GEAR` a wool room's gear. An item may carry
enchantments, written into the world as the chest's own tag.

**The capture rebuild proves the set.** With its local walk and rules replaced by these, its plan check and its
walks read the same to the last digit, and the studio reads its map.xml as valid.

## Four teams

**A board for four teams is drawn once and turned a quarter three times.** `Symmetry("rot_90")` (or "cw") turns
(x, z) to (-1 - z, x), the studio's own rotation, and `orient.turn_world(w, "cw", keep)` copies a part of a square
world onto its next image with every block's data turned. `Objectives.add` fans an objective to all four teams,
each image the last carried on, and `Teams.next` names the team it lands on.

**A wool has a keeper when more than two teams play.** Three teams capture each wool, so `Wool(keeper=...)` names
the team keeping it, and its room, its entry rule and its spawner are written once however many teams capture it.

## The Brittlebush style

**`pgmvox.brittle` builds a blueprint of five-block cells in the look of Brittlebush.** A cell is flat ground, a
keep, a stair one level up in half steps of slab and block, a stacked deck, a gap or water.
`build(w, cells, only=...)` lays the cells in `only`, reading each against the whole blueprint, so an edge is
right where one team's part meets another's.

**Every edge carries the five-course cap, and every other cell along it a birch panel framed in black clay.** The
black clay runs unbroken along the edge, at the foot of the plain cells and up round each panel. A stair's sides
carry the same cap, stepping down with its rows. A panel stands only where five blocks of air lie beside it; over a
shallower drop the face keeps the plain courses.

**A piece is cells of one height and one section.** A cell's `section` names it; cells without one join whatever of
their height they touch. Two sections at one height meet in a double line of planks, each its own outline, so a
board is cut into rectangles without a change of height.

**A piece is outlined, then filled by its shape.** Its outline is one block: the rim where it falls away, spruce
planks where it meets a wall, a stair or another section. A piece one cell wide, or not a rectangle, is a sand
field: sand mixed with upside-down sandstone stairs, cacti and dead bushes on the pure sand alone. A rectangle two
cells or more each way is grass inside two rings of sandstone stairs, the outer rising inward and the inner outward,
with a birch when the grass is wide enough. `build(..., fill=)` may choose a rectangle's fill instead: a bed and its
birch, grass alone, or sand.

**Water marks itself; a gap is marked by cobwebs.** A water cell lays water at the foot of the void, with no cobweb
and no kerb, since PGM holds the water still. A gap cell lays a cobweb at the middle of each edge it shares with the
open void, so the cobwebs trace a build zone's outline where it faces the void.

**A stacked cell with `under=True` is hollow under its deck, as Brittlebush I's island beside the middle is.**
The deck's edge over the hollow is the cap without its black band, and its lower floor lies `DECK`, eight blocks,
under it. One cell of hollow along a side is an under-section; a line of them through a piece is a tunnel.

**A hollow's lower floor runs into the floor of the world.** It has no full cap: its edge is the rim, brick and
black clay, as many as fit over y 0, so it can lie as low as y 1. Where a hollow's open side runs two cells or
more, a dark-oak pillar two wide stands at its middle, laid once every hollow is cut.

**`house(w, layers, floor, dye, door)` raises a wool room as Brittlebush I does: storeys of whole cells.** Each
storey is five blocks, its wall the ground's edge read bottom up, its plate overhanging in eaves. A storey's plate
that nothing stands on is a terrace of sand, and a one-cell top storey holds a beacon under glass of `dye`.

**`pgmvox.studioplan` reads a plan drawn in the studio's planner into such a blueprint.** `unit(plan, lift,
under)` gives one team's part, which `brittle.fan` turns into the four. A piece named `stair…` is a stair cell and
one named `double…` a deck, with the cells in `under` hollow. A zone named `water…` is water and any other zone a
gap. `placement(plan, "spawns")` gives each placement's spot and footprint in blocks.

## Storeys and solids

**A plan can have storeys.** `R.storey(1)` is a raster over the same ground, drawn with the same methods, with
"none" where it has no floor. Ground cells keep their (x, z) names, and a storey's cells are (x, z, n).

**The walk graph joins the storeys.** A player steps onto a roof from a floor one below, walks it, and drops off
its edge. The ground under a storey is walked only where two blocks of air are left over it.

**Solids are the repository's one solid module.** `pgmvox.solid` loads `tools/sculpt/solid.py` rather than copying
it, and adds `fill` and `image`. A sculpture is drawn once and its other half is its image under the plan's own
symmetry, block for block.

## Terrain

**Slope is read as the studio reads it, and a test holds it there.** `slope_deg` is the studio's `SurfaceGradient`:
Horn's gradient over the tops two cells either side, a missing neighbour level with the cell, whole degrees.
`data/export_slopes.cs` writes the studio's answers over sixteen grounds at windows one to three, and the test
wants every cell. The library first read one cell either side, and a gentle grade quantised to blocks came out
0 and 27 degrees by turns instead of the 14 it is.

**Soil follows the slope, so a cliff is rock to its face.** `lay` lays three blocks of soil on gentle ground, less
on steeper and none past 55 degrees. A cell exactly level with three of its neighbours reads as a ledge, so grass
holds on it however steep its hill. With one soil depth everywhere, every riser and cliff showed a band of dirt.
Counting cells only within a block of their neighbours as ledges turned whole hillsides green.

**Rock is laid in beds.** `Strata` draws a sequence of beds from weighted choices with a thickest for each, one
for a bed that is only ever a block. `bed_offset` tilts and folds them across the ground, and `beds` hands them to
`lay`, so a cliff or a canyon wall shows its beds dipping across it.

**A landform is an operation on heights.** `pgmvox.landform` cuts rivers, canyons and terraces and lifts spires,
buttes and scarps. It grades routes, meets the sea at an outline, and blends one terrain into another. Each takes
the board's own numbers, and each only cuts or only lifts unless it says otherwise, so the board decides the order.

**A watercourse never climbs.** Its bed holds level in reaches and steps down in falls, which is how a river leaves
a canyon and drops to the sea. `lowest` keeps a bed off the sea floor. A path that starts out at sea once held a
canyon and its river fifteen blocks under the water all the way inland.

**Water stands only against something that holds it.** A river's banks rise from its surface, and every cell beside
its water is at least as high as that water, so it never stands over its banks. A demonstration river once stood a
block above them for its whole length. Air beside water is right only at a fall inside the stream.

**A river ends in water at its own level.** It runs into a `lake` or a sea with `lowest` at that surface less its
depth and `into` naming that water, so no bank is raised inside it. A river that met the sea a block low once left
a line of sand under the water across its mouth.

**The world's edge is the void, and water may run to it.** A sea that reaches the edge of the board meets open air
there by design, so neither `coast` nor `loose_water` puts a rim or a fault at the edge.

**`hold` runs last, and `audit.loose_water` proves it.** Roads graded down to a bridge cut three of the Vale's
river banks below the water; `hold` raises every dry cell beside water to its surface. `loose_water` lists every
water block with air beside it that is not a fall, a waterfall laid on purpose or the world's edge.

**A terrain board is checked before it is built.** `Raster.from_heights` reads the shaped heights as a plan, with
water and steep ground as their own kinds, and the walk graph runs over it. The Vale's plan check walks from the
harbour to every place before a block is written. With the junction fault below put back, it reports the
uplands and the canyon rim unreachable, which the built world's walk had only found after the build.

**`examples/vale/` uses every landform on one stretch of ground.** A coast, a scarp with a butte and a spire, a
canyon through it into a river with falls, a graded road, a terraced hill and a floating island with a fluted,
spired underside. Its first build showed a whole board lifted to a flat plateau: a spire raised every column to
its own base height. A test now holds a spire to its radius.

## Forms

**A tower is a stack of rings, not a heightfield.** The karst towers of a capture board were drawn this way and
the author singled them out: rings tapering up the stack, a ring of ledges every nine courses, faces bulging
between them, the rock's beds running round in courses. Rebuilt as a heightfield spire they came out as plain
terrain, so `forms.tower` keeps the recipe, with the rock, the ledges and the crown as parameters.

**A floating floor's box sides become a cliff with `skirt`.** Rock juts out in ledges under the rim, never higher
than two under the floor, is cut back where the noise is low, and carries moss and grass. `root_vines` hangs vines
from the lower roots, where they trail below an island rather than hiding against its faces.

## Underground

**A cave passage is a tube held to a level floor.** `under.tunnel` carves a tube through waypoints and leaves
solid everything under the floor interpolated along it, so a player walks a cave rather than the inside of a pipe.
Every carve stays `cover` blocks under the ground it is given and never cuts into water.

**A mine gallery rises a block at a time, and only by stairs.** `gallery_line` holds each step of the floor to one
block, and `gallery` lays its floor after the whole carve, so every rise keeps room for its stair. A floor laid cell
by cell had filled the place each stair stood.

**A timber set stands only on the level.** Over a stair its cap takes the headroom a player needs to climb it.

**A shaft leaves its foot open where a passage reaches it.** Its lining is not laid over cells already open in its
lowest three courses. A test walk found a shaft built after its gallery had walled the gallery's end shut.

## Trees

**The trees come from the studio's own library.** `trees.library()` reads its copied trees, the ones hand-built
in the tree showcase, and `kinds` groups them by name. A board with its own cut reads it with `trees.load`.

**A tree is planted whole or not at all.** `plant` seats it on the lowest ground under its bottom row, as the
studio's stamp does, and refuses it entirely if any block would land in anything but air or plants. Ground and
rock give way to a crown that meets a hillside, and leaves never decay.

**A turn turns the blocks too.** A quarter turn moves every offset and turns each block's data, so a lying
branch follows the body.

**A wood is scattered with its crowns apart.** `scatter` keeps two trees `spacing` times their crown radii
apart, so a wood reads as trees rather than one mass of leaves.

## Routes

**A route is found over the ground, not drawn on it.** `route.find` searches nodes a few blocks apart, with 48
headings out of each. A step costs its length, more for its grade and for the ground it rises and falls over,
steeply more past the grade allowed, and more for turning. On a slope too steep to climb straight, it runs long
legs across it joined by hairpins.

**The turn cost is what makes a switchback.** Without it, a route held to 1 in 8 up a 1 in 2 slope came out as 71
zig-zags a block or two long, since every zig-zag at the limit costs the same. With it, the same climb is five
legs across the slope.

**A network shares its trunk.** `network` joins places nearest first, each to the nearest road already found,
where a step costs a third of what it would. Water costs a bridge's price a block, or is refused.

**Grading keeps what is already there.** `landform.grade` runs the level from bank to bank over water, which is
where `pave` lays a bridge deck. It leaves earlier roads alone and pins its ends to their ground, so a branch
meets its road at that road's level. A footpath is graded too, at a block a block, and `steps` puts a stair on
every rise.

**The Vale's read-back found both of those the hard way.** Walked from the harbour with no jumps, the uplands,
the canyon rim and the spire were cut off. A later branch had re-graded the junction two blocks over the road it
joined, and the ungraded footpath met two-block rises. Both are fixed in the library, and the walk now reaches
every place.

**The studio's routes are strokes an author drags.** It paints them and claims their cells against the scatter,
but does not find them or grade them into the ground. Those are the two halves here.

## Course plans

**A course is a board seen as a sequence.** Each `Course.add` is one step: a piece off the symmetry axis brings
its image with it, and one whose image overlaps it is the middle. A piece links to every piece of the next step
on its own side or in the middle.

**The audit judges every link with the tick model.** It finds the nearest take-off and landing cells, names the
gentlest way across, and follows the fall to the cell it comes down in. So it says whether that cell is water
and whether it is still on the piece, and water elsewhere on the piece saves nobody. A level gap is judged by
the same rule as the walk graph's jumps, so the course and the raster plan agree.

**An image link is the mirror of the link it copies.** The nearest pair of cells can tie, and a tie broken two
ways gave the two halves different landings; the audit now mirrors the first half's answer.

**`examples/drop/` is a course in the plan phase:** eight steps from 120 down to 30, its audit, and a sketch with
every link drawn from take-off to landing and the course unrolled as a section. Its audit failed twice before
the sketch was drawn. A run off the galleries landed on the terrace's rim, a block short of its pool, and a
sixteen-block drop cost more than half a player's health.

## Buildings and patterns

**The roof is the studio's, and a test holds it there.** `build.RoofField` is a port of the studio's own
`RoofField`: gable, flat, hip, gambrel, shed and saltbox, in whole or half courses, with the eave falling to two
courses under the wall top. `data/export_roofs.cs` runs the studio's class over 300 roofs and writes every cell's
answer to `data/roofs.json.gz`. The test asks the port the same 34,500 questions and wants the same crown, riser,
slope and ridge. `lay_roof` lays a field the way the stamper does, in stairs climbing toward the higher neighbour.

**What the library adds to the studio's houses is a heading.** A `Frame` places a building's own axes on the
board at any angle, and a block belongs to a shape when its centre lies inside it. Walls come from eight
neighbours, so a 45 degree wall is closed. A roof measured in the frame is the studio's roof turned. At 0 or 90
degrees it is the studio's exactly; turned, it is laid in cubes and slabs to the half block, because a stair can
face only four ways.

**One convention settles the half blocks.** An even side wants its centre on a whole block and an odd side on a
half; `house` snaps an axis-aligned centre that way. A distance in a frame is measured from the wall line's outer
face, the same test the wall mask uses, so a wall and its roof never disagree by half a block.

**A face pattern is a function of where a block falls on its face**, so one pattern fits a long wall and a short
one. Faces are walked left to right as seen from outside, and a word in `facade.word` reads correctly on every
side. An inset sets the face back a block, so a band or a glyph is a recess and not a paint. Corners stay flush.

**A floor field is a function of where a cell falls in its rectangle.** The five carpets of the woven board were
one chain of conditions; they are now borders, medallions, diamonds and stars that `first_of` composes.

**`examples/parts/` lays every piece on one yard:** the four house styles at 0, 20, 45 and 90 degrees, the six
roof forms, a mass on piers with a word, glyphs, flutes and a coffered underside, and three carpets. Islets uses
them too: a house on each island at 20 degrees, its footprint in the plan.

**Islets' read-back caught the first such house.** Its eave hung a block past the island's edge, over the void,
because the plan held the walls and not the roof. It was moved two blocks in.

## Starting a board

**`examples/islets/` is a whole board written against the library.** It has a plan raster with its half turn, a
checker giving both teams' walk to the hill, a sketch, a generator with terrain, undersides and clouds, map.xml,
renders and a read-back. Copy its `scripts/` to start a board:

```
cd freeform/lib
python3 -m pgmvox.run examples/islets            # plan check, sketch, gen, write, map.xml, renders, walk
python3 -m pgmvox.run examples/islets --only sketch
```

**The read-back earned its place on the example's first build.** It found 1,053 places to stand over the kill
height: cloud billows rising through it. The deck now sits far below.

**A board's scripts put the library on their path themselves,** as `examples/islets/scripts/plan.py` does, and
`run` also sets `PYTHONPATH`. Every build writes `renders/build-info.txt` with the library version it used.

## Building a board with it

**`AGENT-GUIDE.md` is for an agent handed a board to build.** It is about the plan and the sketch: what a plan
must state and to what detail for each mode, the panels a sketch needs, and what must, should and may come from
the library.

## Tests

**The walk is exact and opens doors.** It takes places in order of distance, so a jump that crosses several
blocks costs exactly that many moves and a mirrored board walks the same from either side. A first-in first-out
queue had given one board 81 and 83. A wooden door or fence gate opens, an iron door does not, and a ladder or
vine catches a player falling past it.

**A running jump lands one up, level, or lower.** Across a gap it takes the first floor it meets, down to the
move rules' greatest drop, so a line of stones stepping down is crossed both ways. It had landed only one up or
level, and a line of stones read as one way.

**`python3 check.py` is the one command that says nothing is broken.** It runs the tests and the prose gate, then
rebuilds every example and compares what each reads back (its plan check, generator and walk numbers, and how many
of each block it built) with `check/snapshot.json`. A change that moves a number fails with a diff until it is
looked at and accepted with `--update`. `--studio` also re-exports the studio's tables and reads every map.xml.

```
cd freeform/lib && python3 -m unittest discover -s tests -v
```

**The tests check what each module promises.** They cover the studio-exported table, turns and their round trips,
the physics numbers the boards measured, the headroom fix, ladders, footing, plan symmetry and fair arrivals,
sight, slope without wrapping, save and load, rendering, and a sketch sheet with every kind of panel.

**The pieces are tested as built and walked.** The tests check the roof against the studio's own, a house at 45 degrees with no gap in its walls, a word read from both sides, a course
and its mirrored audit, a roof walked over the ground, solids turned with the plan, objectives mirrored, written
and read back, a tunnel and a mine walked end to end, a tree planted, turned and refused, map.xml, and a Curio plot
passing the plot check.

**The studio's reader is run by hand,** since it needs the studio's checkout and the .NET SDK:

```
cd /tmp && dotnet run /path/to/freeform/lib/pgmvox/data/read_mapxml.cs -- /path/to/map.xml
```

## What it does not do yet

**The house is simpler than the studio's.** It has one rectangle per storey, so no wings, porches or dormers,
and its timber frame and window rhythm come from the boards, not from the studio's `HouseStyle`. Only the roof
is held to the studio's formulas.

**A route finds its way in seconds, not instantly.** A network of four branches over a 200-block board takes
about twelve seconds in pure Python; a board with many routes will want it faster.

**Jumps are taken on the ground storey only.** A jump from one roof to another is not in the walk graph yet.

**A plan holds a building's walls, not its roof.** A roof's overhang is not in the raster, so the checker cannot
see an eave over the void; the read-back can.

**A course checks the nearest pair of cells only.** A player can leave a piece anywhere along its edge, and a
take-off from the far end of a wide piece may miss what the nearest one reaches. The built world's read-back has
to walk those.

**`write_world.cs` names the studio's path in its project line.** C# cannot read an environment variable there, so
a checkout elsewhere edits that one line. `world.write` finds the studio by `PGM_STUDIO_ROOT` for everything else.

**The reads of a built world are a stopgap.** The repository's rule allows them for a world that is not a stored
map. When the studio can read an uploaded region folder, `walk`, `render` and `audit` belong there; the plan-phase
modules have no such overlap.
