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
| `plan` | `Raster`, the plan as every column's floor and kind, with `Symmetry` drawn in the plan; `rect`, `poly`, `where`, `flight` |
| `plangraph` | the walk over a plan: `graph`, `jumps`, `dijkstra`, `route`, `path`, `arrivals` per team, `pad_edges` |
| `sight` | `line_clear`, `visibility`, `hidden`, with an opaque test for a plan or a built world |
| `sketch` | the annotated sheet: map panels (a plan raster or a built top-down) with heights, places, markers, routes, jumps, zones and callouts; true-scale and unrolled sections; the checker's numbers against their targets |
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
sight, slope without wrapping, save and load, rendering, a sketch sheet with every kind of panel, map.xml, and a
Curio plot passing the plot check.

## What it does not do yet

**The assessment's building and pattern modules are not here yet.** `build` (one roof field for the six gable
roofs, the `Frame` house at any angle, parapets) and `facade` (insets, flutes, glyph rows, floor figures) are the
next to write, against the studio's own `RoofField` and stamper so the two do not drift.

**Course plans are not here yet.** The boards built of pieces (the water drop, the wool run) need a `Pieces` plan
beside `Raster`.

**`write_world.cs` names the studio's path in its project line.** C# cannot read an environment variable there, so
a checkout elsewhere edits that one line. `world.write` finds the studio by `PGM_STUDIO_ROOT` for everything else.

**The reads of a built world are a stopgap.** The repository's rule allows them for a world that is not a stored
map. When the studio can read an uploaded region folder, `walk`, `render` and `audit` belong there; the plan-phase
modules have no such overlap.
