# Riftwater on pgmvox: how the port is expressed

Subject: `freeform/lib/ports/riftwater/` (scripts, `PORT-REPORT.md`), the form of Riftwater that is written with pgmvox. The standalone original (`freeform/opus55-freeform-riftwater/`) is the comparison, in section 7 and in `ORIGINAL-STANDALONE.md`. Every number below was measured by running the port's own `gen.py`; line references are to the port's files unless a path says otherwise.

## 0. What was run, and how close the run is to the committed port

The port ships no region files (`world/` holds `map.xml` only), so its world is whatever `gen.py` writes. `gen.py` was run unmodified from a scratch copy (`/tmp/riftwater-anatomy/freeform/...`, nothing written into the repository) against the library as it stands now, pgmvox 0.21.0. The port was last built with 0.10.0 (`renders/build-info.txt`).

| | committed `renders/gen.txt` (0.10.0) | this run (0.21.0) |
|---|---|---|
| blocks | 1,002,206 | 1,002,206 |
| tile entities | 22 | 22 |
| blocks carved underground | 5,568 | 5,568 |
| houses / trees | 29 / 53 | 29 / 53 |
| two runs | | `volume.bin` byte-identical |

`PORT-REPORT.md` quotes 1,001,926 blocks, 110 trees and 16 tile entities; those are the numbers from before its review pass and the committed `gen.txt` is the later one. So the library's moves between 0.10.0 and 0.21.0 have not changed this board's output.

**Attribution method.** `method/port/instrument_port.py` wraps `World.set`, `fill`, `column`, `terrain.lay`, `turn_world` and `ground.lay_ground`, and for every write walks the Python stack to name (a) the line of `gen.py` that led to it, (b) the port function and line that call went on to run, and (c) the writer: `port code` when no pgmvox frame lies between that line and `World.set`, otherwise the pgmvox function the port called. Writes made by array slicing (all of `terrain.lay`, `turn_world`, the local pass in `ground.lay_ground`) are caught by diffing the volume around the call. A later write takes ownership from an earlier one, so the counts are blocks left in the final world. The mirrored half takes the owner of its source column.

**The instrumented run is the plain run.** Ids, data, biomes and tile entities are bit-identical to the unwrapped run, and no non-air block is unowned.

## 1. The shape of the port

**The port is data and glue around library calls: 1,885 lines in 11 files, of which 1,529 produce the world and `map.xml`.** The rest (`plan_check.py` 121, `sketch.py` 89, `renders.py` 65, `walk.py` 81) read the plan and the built world back.

| file | lines | role |
|---|---:|---|
| `plan.py` | 577 | places, routes, 29 house records, cave/mine waypoints (data); `land()` the heightfield (formulas plus 5 library landform calls and 13 `landform.grade`); `houses()` the library `House` records; `build()` a plan raster for the sketch and checks (writes no blocks); `objectives()` |
| `ground.py` | 84 | `lay_ground` (one `terrain.lay` call plus a local per-column pass), `falls` |
| `under.py` | 200 | the cave, mine, shaft, cellar: library tunnel/chamber/dress_cave/gallery/shaft plus 7 local pieces |
| `works.py` | 453 | roads, square, houses, towers, mill, bridges, headframe, village furniture, lamps |
| `dress.py` | 141 | one function: trees, field, Cutting, rift vines, cover |
| `gen.py` | 44 | the order of everything |
| `mapxml.py` | 30 | `map.xml` from the objectives |

**The port calls into these pgmvox modules.** `landform` (blend x2, spire, terraces, watercourse, grade), `noise` (fbm x17, smoothstep x17, spline x3), `shapes`, `terrain` (lay, Strata, beds, by_angle, slope_deg), `under` (tunnel, chamber, dress_cave, gallery_line, gallery, shaft), `build` (House, site, house, stairs, parapet), `facade` (carpet, tiles, border, first_of), `route.pave`, `trees` (load, kinds, scatter, plant), `props.stalls`, `objectives`, `orient.turn_world`, `mapxml.Doc`, `plan.Raster`/`Symmetry`.

## 2. The pipeline, in `gen.py` order

How a step writes is one of: **H** a heightfield turned into columns by array slicing; **S** a loop over a computed shape calling `w.set`; **L** a hand-placed list of blocks; **P** a library call that places a whole object (house, tree); **M** a copy of the other half.

| gen.py line | step (file:lines) | builds, with world coordinates | how it writes |
|---|---|---|---|
| 22 | `plan.land()` (plan.py:178-324, cached) | No blocks. The red half's grids, 120 x 176 over x -120..-1, z -88..87: outline with the ragged rift lip at x about -11 (188-193); town bluff 49..52 falling to the rift, chapel hill, fields 47..49, ridge crest 73 at x < -100 (195-207, 230-244); river valley with a 7-block bluff on the town side and a 14-block bank on the field side, centre line (-74,22) to (-11,0) (209-218, 262-267); pond centre (-84,20) with a spit (220-228); spawn shoulder levelled at 59 around (-97,-7) (246-251); square level 52 at (-66,-44) and green level 50 at (-66,48) via `landform.blend` (253-256); knoll (-22,74) via `landform.spire` (258-260); 13 routes graded with `landform.grade` (279-289); square floor, sinkhole funnel centre (-50,38) radius 10.5, spoil heap (-101,79) (291-309); the underside from two distances to the void (311-317). | numpy formulas on whole grids; library calls return new height arrays |
| 23 | `World(-120,-88,240,176,sy=128)` | the volume | |
| 24 | `ground.lay_ground` (ground.py:68-111) | Every land column, 36,240 in both halves: rock in andesite beds that follow the surface (`Strata`, `beds`), dirt, grass or rock on top by slope (`by_angle`), laid from y 3 by `terrain.lay` (71-74). Then a local loop over the columns (81-106): clears everything under the column's own bottom, lays pond and river bed (clay/sand/dirt, gravel/sand/andesite), fills water, patches of coarse dirt and andesite on mid slopes, rock tops above 55 degrees, a sand lip within 5.2 of the river; biomes (108-110). | **H**: `terrain.lay` writes whole columns by slicing; the local pass writes the same arrays directly |
| 25 | `ground.falls` (ground.py:114-128) | The river pouring off the lip: 377 flowing-water blocks at x -11..-10, z -3..3, y 8..45. | **S**: nested loops with `w.set` |
| 27 | `under.build` (under.py:185-200) | Calls, in order: 5 `U.tunnel` branches (188) and 10 `U.chamber` halls (190), carved from the cave waypoints (gallery from the mouth at (-9,36,2) to the lake chamber centre (-40,31,15); south to the sinkhole (-50,39,38); north to the cellar (-53,42,-27); the grotto at (-60,33,6); west to the mine); pillar hall pillars around (-46,34,26) (191); `U.dress_cave` over box (-64..-9, 26..46, -30..45) (192); grotto stash (193); lake pool at (-40,31,15) (194); mouth ledge x -11..-10, z 1..9, y 34..35 (195); sinkhole rubble (196); `U.gallery` along the mine line from the adit (-104,59,5) to the breakthrough (-57,39,37), then the portal and the foreman's chest at (-61,40,42) (197); `U.shaft` at (-84,56) from y 45 (198); the gaol cellar x -55..-49, z -37..-31, floor 43 (199). | carves are **S** inside the library (`tunnel`, `chamber` set air); `dress_cave`, `gallery`, `shaft` are library **S** loops; pillars, pool, mouth, rubble, portal, cellar are local **S** and **L** |
| 29 | `works.build` (works.py:439-453) | 442 `roads`: `route.pave` per route through the `Guarded` proxy, trestle legs under the plank deck at x -72..-68, z 12..27; 443 `square`: Market Square floor x -76..-57, z -53..-35 at y 52; 444 `houses`: all `build.site` pads first, then 29 `build.house` calls and 5 shop signs; 445 `chapel`: belfry x -55..-51, z -79..-73, 20 high, pad, doors, pews; 446 `watch`: stone tower x -107..-103, z -10..-4, 16 high with a battlement, wool banner at x -108, terrace x -93..-86, z -12..-2 at y 59, steps; 447 `mill`: race x -68..-54, z 9..11, wheel centre (-62,46) at z 10, weir at x -67; 448 `stone_bridge`: x -38..-34, z -10..14; 449 `old_bridge`: z -44, x -15..-4; 450 `headframe` at (-84,56), 17 high; 451 `ironhollow`: engine stack (-74,50), forge, well (-87,46), spoil-heap rubble; 452 `lamps` along the three streets. | roads, houses and the square are library calls (**P**/**S** inside pgmvox); towers, bridges, mill, headframe and village furniture are local **S** loops and **L** lists |
| 30 | `under.gaol_ladder` (under.py:173-182) | 10 ladder blocks at (-50, 43..52, -33) from the cellar to the gaol's floor, after the gaol exists. | **S** |
| 33-36 | `props.stalls` | 3 market stalls at x -75, z -50/-45/-40 | **P** (library) |
| 37 | `dress.build` (dress.py:29-141, one 113-line function) | 57-60 four `T.scatter` zones (north wood, ridge, south wood, the Cutting's ring); 61 the knoll oak at (-22,74); 68 ten hand-listed trees; 82-98 the wheat field x -50..-31, z 45..69 with ditches, fence and gate, scarecrow at (-40,*,54); 106-112 the Cutting at (-110,68); 124 vines on the rift face; 138-140 flowers and grass. | trees: **P** through `trees.scatter`/`plant`; the rest local **S** loops |
| 39-40 | `turn_world(w,"mirror_x",X<0,recolour=...)` | Blue's half: every column x -120..-1 copied to x' = -1 - x, data turned, wool 14 recoloured to 11, biomes and tile entities copied. | **M** |
| 41-42 | `P.objectives().stamp(w)` | The 4 monuments, 2 obsidian blocks each: red-square (-66,54..55,-44), red-green (-66,52..53,48) and their images at x 65. | library **S** |
| 43 | `w.save(...)` | `volume.bin`, `tiles.json`, `level.json` (spawn (0,90,0)) | |

## 3. How `map.xml` is produced, and how the second team's half is

**`map.xml` is generated from the same objects that stamp the blocks.** `mapxml.py` builds a `Doc`, adds the kit by hand with `E` (14 items, no helper exists), calls `P.objectives().write(d)` for teams, spawns, observer and the four destroyables with their cuboids, then adds the void filter, the rift rectangle (-16,-88)..(16,88) and `maxbuildheight 90` (mapxml.py:5-40). The monument cuboid is the `Box` that `Destroyable` stamps (plan.py:575), so block and region cannot disagree. In the original `map.xml` is a hand-written file whose monument coordinates are typed a second time.

**Blue's half costs one call.** `turn_world` (gen.py:39-40) copies the finished red half across x' = -1 - x with a data table that turns stairs, doors, ladders, torches, signs, beds, vines and gates, and maps wool 14 to 11. Nothing in `under.py`, `works.py` or `dress.py` writes at x >= -1: carves and trees are held back with `keep=red` / `allowed=red`. Objectives are drawn once and mirrored by `Objectives.add` under `Symmetry("mirror_x")`. Half the world (501,103 of 1,002,206 blocks) is that copy. The recolour is applied to the whole image, so blue's stall awnings coloured 14 also turn blue; the original recoloured the tower's box only.

## 4. Block attribution, measured

Blocks left in the final world, both halves, by step. `exposed` counts blocks with an air face (what a player can see from somewhere). `carved` counts blocks a step removed. `class` and `op exists today` are defined in section 5.

| # | step (rolled up from the call chain) | writer | class | op exists today | blocks left | share of non-air | exposed blocks | carved to air (both halves) |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 | ground: terrain.lay (rock, beds, soil, slope paint) | pgmvox | A | yes | 908,648 | 90.665% | 82,372 | |
| 2 | ground: lay_ground local pass (underside, water beds, patches, sand lip) | port code | A | no (new) | 9,528 | 0.951% | 4,904 | 910,952 |
| 3 | ground: falls over the lip | port code | A | no (new) | 754 | 0.075% | 654 | |
| 4 | cave: 5 tunnels | - | A | yes | 0 | 0.000% | 0 | 4,430 |
| 5 | cave: 10 chambers | - | A | yes | 0 | 0.000% | 0 | 3,076 |
| 6 | cave: pillar hall pillars | port code | A | no (new) | 122 | 0.012% | 122 | |
| 7 | cave: dress_cave | pgmvox | A | yes | 1,822 | 0.182% | 1,790 | |
| 8 | cave: grotto stash | port code | A | yes | 8 | 0.001% | 8 | |
| 9 | cave: lake pool | port code | A | no (new) | 346 | 0.035% | 140 | |
| 10 | cave: mouth ledge + vines | port code | C | no (made) | 52 | 0.005% | 46 | |
| 11 | cave: sinkhole rubble | port code | A | no (new) | 484 | 0.048% | 482 | |
| 12 | mine: gallery (under.gallery) | pgmvox | A | yes | 1,052 | 0.105% | 840 | 2,036 |
| 13 | mine: adit portal + foreman chest | port code | A | no (new) | 24 | 0.002% | 22 | 24 |
| 14 | mine: shaft | pgmvox | A | yes | 182 | 0.018% | 134 | 104 |
| 15 | gaol cellar (vault, cells, breach) | port code | C | no (made) | 518 | 0.052% | 326 | 400 |
| 16 | roads: route.pave x13 | pgmvox | A | yes | 2,938 | 0.293% | 2,924 | |
| 17 | roads: trestle legs under the footbridge | port code | B | no (new) | 42 | 0.004% | 6 | |
| 18 | square: facade.carpet | pgmvox | A | yes | 724 | 0.072% | 688 | |
| 19 | houses: build.site (pads) | pgmvox | B | yes | 10,956 | 1.093% | 3,232 | 1,732 |
| 20 | houses: build.house (29 buildings) | pgmvox | B | yes | 22,510 | 2.246% | 20,758 | 2 |
| 21 | houses: shop signs | port code | B | no (new) | 10 | 0.001% | 10 | |
| 22 | chapel: build.site pad | pgmvox | B | yes | 96 | 0.010% | 60 | 92 |
| 23 | chapel: belfry tower, spire, pews | port code | B | no (new) | 1,162 | 0.116% | 980 | 84 |
| 24 | watch: tower, terrace walls, wool | port code | B | no (new) | 922 | 0.092% | 722 | 96 |
| 25 | watch: parapet, terrace carpet, steps (build/facade) | pgmvox | A | yes | 272 | 0.027% | 254 | |
| 26 | mill: race, wheel, weir, sacks | port code | B | no (new) | 1,146 | 0.114% | 550 | 558 |
| 27 | stone_bridge | port code | B | no (new) | 828 | 0.083% | 568 | 68 |
| 28 | old_bridge | port code | B | no (new) | 780 | 0.078% | 360 | |
| 29 | headframe | port code | B | no (new) | 412 | 0.041% | 404 | 10 |
| 30 | ironhollow: engine stack, forge, well, spoil rubble | port code | B | no (new) | 1,726 | 0.172% | 664 | 28 |
| 31 | lamps x3 streets | port code | B | yes | 30 | 0.003% | 30 | |
| 32 | gaol_ladder | port code | A | yes | 20 | 0.002% | 12 | |
| 33 | stalls (props.stalls) | pgmvox | B | yes | 120 | 0.012% | 120 | |
| 34 | trees: scatter x4 zones | pgmvox | A | yes | 23,024 | 2.297% | 22,648 | |
| 35 | trees: knoll oak | pgmvox | A | yes | 1,520 | 0.152% | 1,514 | |
| 36 | trees: hand-placed singles | pgmvox | A | yes | 3,292 | 0.328% | 3,204 | |
| 37 | wheat_field + scarecrow | port code | A | no (new) | 3,856 | 0.385% | 1,050 | 486 |
| 38 | cutting: stumps, log piles | port code | B | no (new) | 152 | 0.015% | 134 | |
| 39 | rift face vines | port code | A | no (new) | 832 | 0.083% | 832 | |
| 40 | cover (grass, ferns, flowers) | port code | A | yes | 1,288 | 0.129% | 1,288 | |
| 41 | monuments: objectives.stamp | pgmvox | A | yes | 8 | 0.001% | 8 | |

**By writer.** 977,164 blocks (97.5%) are written inside a pgmvox call and 25,042 (2.5%) by port code. One call, `terrain.lay`, writes 908,648 (90.7%); outside it, 68,516 of 93,558 blocks (73.2%) come from pgmvox and 25,042 (26.8%) from local code. Of 120,506 `World.set` calls, 108,208 (89.8%) happen inside pgmvox. Of 198,169 `World.get`/`id` reads, 147,423 (74%) happen inside pgmvox.

**By what a player sees (exposed blocks).** Terrain 56.8%, buildings and roads 20.8%, dressing 19.9%, underground 2.5%, pieces 0.01%. By raw blocks the same four are 91.7%, 4.4%, 3.4%, 0.46%: 847,346 blocks (84.5%) have no air face, nearly all of it rock under the surface.

## 5. Classification

**A** is a layer operation with parameters; **B** is a library entry plus a placement; **C** is bespoke and would be a made structure. **op exists today** means pgmvox or the studio already has an op or template of that name, whether or not the port calls it (the port writes `lamps`, `cover` and `grotto` locally though the concepts exist).

| | blocks | share of non-air | exposed share |
|---|---:|---:|---:|
| **A** layer operation | 960,744 | 95.86% | 81.3% |
| **B** library entry + placement | 40,892 | 4.08% | 18.5% |
| **C** bespoke (made) | 570 | 0.057% | 0.24% |
| op exists today (A+B) | 978,510 | 97.64% | 91.6% |
| needs a new op or template (A+B) | 23,126 | 2.31% | 8.1% |

The two C steps are the gaol cellar (518 blocks) and the cave-mouth ledge (52). **Outside the 908,648 blocks of `terrain.lay`, the split is A 55.7%, B 43.7%, C 0.6%.** The class of every step is in the table above; the reasoning for each is in `riftwater.layers.json` (`class`, `lib`, `new`, `gap`).

**Code follows blocks poorly.** Of the port's 1,213 lines of world-producing code (docstrings, comments and blanks excluded), plan data is 139, heights 190, underground 154, buildings and furniture 296 (`works`) plus 50 (house records), roads and the guard 61, dressing 131, play pieces 31, glue 34 and a plan-only raster 127. `works.py`'s local building code (towers, bridges, mill, headframe, village furniture: 296 lines, 24% of the world-producing lines) leaves 7,058 blocks, 0.70% of the world.

## 6. Does the port's world match the original's?

**It matches closely on the ground and the places, and loosely on the details a player stands next to.** `PORT-REPORT.md` says the two are hard to tell apart from above and the south-east and compares counts and walks; this is the voxel comparison (`method/port/compare_worlds.py`) against the original's committed world, which a re-run of the original reproduces bit for bit.

| measure | value |
|---|---|
| non-air blocks | original 1,007,266, port 1,002,206 |
| cells non-air in either | 1,041,668 |
| same block id at the same cell | 902,908 (86.7% of those) |
| same id and data | 574,322 (55.1%); the rock's andesite beds differ in data |
| original's exposed blocks that the port has as the same id | 66.2% (same id and data 47.5%) |
| surface height of the natural ground, over 36,348 common columns | equal in 78.4%, within 1 block in 94.3%, within 3 in 98.4%, mean difference 0.33 |
| highest solid non-leaf block per column (roofs, towers and logs included), same columns | equal in 73.5%, within 2 in 89.7% |
| terrain (original's `write_land`) cells that differ in id | 6.5% |
| underground / buildings / dressing cells that differ in id | 67.7% / 39.6% / 71.6% |

**Where they differ on purpose or by omission.**

- **Not ported (1,034 original blocks):** the barn's fittings, haystacks, hay cart, jetty and rowboat, spring, gardens, benches, boulders, hedgerow, worn ground, the inn's sign, the Cutting's sawhorse, interior furnishing of every house, the door paths (`PORT-REPORT.md` table). Houses: 29 against 31 (no barn; the watch tower is a masonry tower, not a house). Trees: 53 per half including the knoll oak, against 54.
- **Monuments hang one block over the floor in the port** (obsidian y 54..55 over a floor at 52; 52..53 over 50) and the port's `map.xml` cuboids are [54,56) and [52,54). The original, after its fourth playtest, hangs them three over (y 56..57 and 54..55). This is a state difference, not a porting error: the port copied the earlier rule.
- **The ridge shows more bare rock** (`landform.terraces` cuts its steps harder), the natural ground is within 3 blocks in 98.4% of columns and the 568 columns (1.6%) that differ more cluster at the sinkhole (-50,38) and along Spawn Lane south (x -80..-60, z -20..0), and the **sinkhole is a 10.5-radius bowl at one block per block** (the plan check found the original's 1.6 per block unclimbable).
- **Spawn and goal walks agree**: 65 and 83 blocks from each spawn to its monuments (original 63 and 81), per `renders/walks.txt`.

## 7. Comparison with the original standalone board

**The original uses no pgmvox.** `grep pgmvox` over `freeform/opus55-freeform-riftwater/` finds nothing. Its imports are `plan`, `mc` (its own `World` and 1.8 block ids), `mirror`, `noise` (its own fbm, spline, `polyline_distance`), `terrain`, `underground`, `buildings`, `house`, `dressing` and numpy/scipy/PIL. The one outside dependency is the studio's C# Anvil writer, called from `write_world.cs`. pgmvox's `under.tunnel` takes the same `(x, floor_y, z, radius)` waypoints as the original's `CAVE`, and its `gallery`, `shaft` and `dress_cave` correspond to `underground.mine`, `shaft` and `dress_cave`; that is consistent with the library having been distilled from boards like this one, and cannot be proven from the imports.

**Blocks: the same families, the writer moved.** Both boards total about 1.0 M non-air blocks, and the sums by feature family reconcile exactly to each total.

| feature family | original blocks | port blocks | how the port writes it |
|---|---:|---:|---|
| rock, soil, paint (ground columns) | 925,382 | 918,176 | terrain.lay + a local pass |
| falls over the lip | 754 | 754 | local |
| cave dressing | 1,932 | 1,822 | under.dress_cave |
| pillars, lake pool, grotto, mouth | 510 | 528 | local |
| sinkhole rubble | 230 | 484 | local |
| mine gallery, portal, chest | 1,250 | 1,076 | under.gallery + local |
| shaft | 250 | 182 | under.shaft |
| gaol cellar and ladder | 560 | 538 | local |
| Market Square floor | 694 | 724 | facade.carpet |
| houses (original also furnished inside) | 29,046 | 33,572 | build.house, build.site |
| chapel belfry, watch tower, terrace | 1,278 | 2,356 | local + build.parapet, build.stairs, facade.carpet |
| headframe | 422 | 412 | local |
| engine stack, forge, well, spoil heap | 894 | 1,726 | local |
| mill works | 946 | 1,146 | local |
| three bridges | 1,854 | 1,650 | local |
| streets, lanes, paths (+ door paths in the original) | 4,136 | 2,938 | route.pave |
| stalls | 120 | 120 | props.stalls |
| street lamps | 130 | 30 | local |
| trees | 29,586 | 27,836 | trees.scatter, trees.plant |
| wheat field and scarecrow | 3,814 | 3,856 | local |
| the Cutting | 168 | 152 | local |
| rift-face vines | 730 | 832 | local |
| grass, ferns, flowers | 1,538 | 1,288 | local |
| monuments | 8 | 8 | objectives.stamp |
| not ported (barn fittings, haystacks, cart, jetty and boat, spring, gardens, benches, boulders, hedgerow, worn ground, inn sign, hut fittings, blue-wool recolour step) | 1,034 | 0 | - |
| **total non-air** | **1,007,266** | **1,002,206** | |

**In the original every block is written by the board's own code. In the port 97.5% are written inside a pgmvox call.** The families whose writing code moved wholesale into the library hold 992,404 of the original's blocks (98.5%): ground columns, cave dressing, gallery, shaft, square floor, houses, streets, trees, stalls, monuments.

**Lines: 2,260 become 1,213, and what stayed is the board's own.** Counted without docstrings, comments or blanks, on the world-producing code only (renderers and read-backs excluded on both sides):

| | original | port |
|---|---:|---:|
| world, block ids, noise, mirror table (`mc`, `noise`, `mirror`) | 274 | 0 (library) |
| houses (`house.py`, house calls, signs, door paths) | 328 | 50 |
| underground | 341 | 154 |
| ground and heights | 231 (+25 unassigned) | 190 |
| roads, square | 73 | 61 |
| towers, bridges, mill, headframe, village furniture | 352 | 296 |
| dressing (original also barn, jetty, spring, gardens, boulders, hedgerow, worn ground) | 495 | 131 |
| play pieces | 5 (`map.xml` is 77 hand-written lines) | 31 |
| plan data | 104 | 139 |
| plan-only raster for the sketch and checks | 0 | 127 |
| glue (`gen`) | 32 | 34 |
| **total** | **2,260** | **1,213** |

**What the library took and what it did not.** The 274 lines of world, ids, noise and mirror are gone; houses fell from 328 to 50 and the underground from 341 to 154. Towers, bridges, the mill, the headframe, village furniture, the wheat field, the falls, the cellar and the heightfield formulas stayed local (about 900 lines by the port's own count, `PORT-REPORT.md`). Part of the dressing drop is features that were dropped, not features that were moved.

## 8. Reproducing

`cd /tmp/riftwater-anatomy` after copying `freeform/lib/pgmvox`, `freeform/lib/ports/riftwater`, `freeform/opus55-freeform-riftwater/scripts/trees.json` and `tools/` to the same relative places; then `python3 method/port/instrument_port.py <scratch>/freeform/lib/ports/riftwater/scripts <out>`, `rollup_port.py`, `expose_port.py`, `compare_worlds.py`. The scripts keep their `/tmp/riftwater-anatomy` paths; they are scratch tooling and read the repository only.
