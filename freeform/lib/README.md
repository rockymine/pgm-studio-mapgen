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
| `plan` | `Raster`, the plan as every column's floor and kind, with `Symmetry` drawn in the plan; `rect`, `poly`, `where`, `flight`; `storey(n)`, an upper storey drawn the same way |
| `objectives` | spawns, the observer point, hills, flags, wools and monuments, destroyables, cores, score boxes and portals: each stamps its blocks, writes its regions and XML, carries itself to the other team, and checks the built world |
| `solid` | the repository's `tools/sculpt/solid.py` (booleans, turns, revolves, extrusions, tubes), with `fill` into a `World` and `image` through a plan `Symmetry` |
| `pieces` | `Course`, the plan of a board played in order (a water drop, a parkour run): pieces by step with their images, the links between steps, and an audit of each link's gap, drop, way across, landing cell and damage; `raster()` turns a course into a `Raster` |
| `plangraph` | the walk over a plan and its storeys: `graph`, `jumps`, `dijkstra`, `route`, `path`, `arrivals` per team, `pad_edges` |
| `sight` | `line_clear`, `visibility`, `hidden`, with an opaque test for a plan or a built world |
| `sketch` | the annotated sheet: map panels (a plan raster or a built top-down) with heights, places, markers, routes, jumps, zones and callouts; true-scale and unrolled sections; the checker's numbers against their targets |
| `build` | `Frame`, a building's own axes at any heading; `RoofField`, the studio's six roof forms block for block, and `lay_roof`; `house`; `parapet`, `site`, `stairs`, `ladder`, `Claims` |
| `facade` | face patterns (`band`, `courses`, `flutes`, `panels`, `slits`, `checker`, `windows`, `glyph_row`, `word`) set back or flush on an `extrude`d mass, `coffer`, `top_course`; floor fields (`border`, `medallion`, `corners`, `diamonds`, `steps`, `star`, `cross`, `tiles`) composed by `first_of` and laid by `carpet` |
| `terrain` | `mountain_ring`, `slope_deg`, `lay` (ground painted by slope, rock bands, snow line), `underside`, `cloud_deck` |
| `walk` | the voxel walk over built blocks with `MoveRules`; `no_stand_above`, `catchers`, `unreached`, `nearest`, `gap_cleared` |
| `audit` | `footing`: blocks that would fall, or have nothing to hang on |
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

## Storeys and solids

**A plan can have storeys.** `R.storey(1)` is a raster over the same ground, drawn with the same methods, with
"none" where it has no floor. Ground cells keep their (x, z) names, and a storey's cells are (x, z, n).

**The walk graph joins the storeys.** A player steps onto a roof from a floor one below, walks it, and drops off
its edge. The ground under a storey is walked only where two blocks of air are left over it.

**Solids are the repository's one solid module.** `pgmvox.solid` loads `tools/sculpt/solid.py` rather than copying
it, and adds `fill` and `image`. A sculpture is drawn once and its other half is its image under the plan's own
symmetry, block for block.

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

## Tests

```
cd freeform/lib && python3 -m unittest discover -s tests -v
```

**The tests check what each module promises.** They cover the studio-exported table, turns and their round trips,
the physics numbers the boards measured, the headroom fix, ladders, footing, plan symmetry and fair arrivals,
sight, slope without wrapping, save and load, rendering, a sketch sheet with every kind of panel, the roof
against the studio's own, a house at 45 degrees with no gap in its walls, a word read from both sides, a course
and its mirrored audit, a roof walked over the ground, solids turned with the plan, objectives mirrored, written
and read back, map.xml, and a Curio plot passing the plot check.

**The studio's reader is run by hand,** since it needs the studio's checkout and the .NET SDK:

```
cd /tmp && dotnet run /path/to/freeform/lib/pgmvox/data/read_mapxml.cs -- /path/to/map.xml
```

## What it does not do yet

**The house is simpler than the studio's.** It has one rectangle per storey, so no wings, porches or dormers,
and its timber frame and window rhythm come from the boards, not from the studio's `HouseStyle`. Only the roof
is held to the studio's formulas.

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
