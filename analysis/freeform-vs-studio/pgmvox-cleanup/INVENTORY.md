# pgmvox: inventory, duplication, terrain shapes to add, and the cleanup plan

> Written by a Sonnet 5.5 agent on 2026-10-10. Read-only run: nothing in pgmvox, the boards or the studio was edited; every build ran in a scratch copy under `/tmp/pgmvox-inventory/` (the copy of `freeform/lib` plus `tools/sculpt`, `PGM_STUDIO_ROOT=/home/user/pgm-studio`, Python 3.13, numpy 2.5, scipy 1.18). Counts are lexical (greps and the Python AST) unless the text says "ran" or "measured". The scratch scripts that took the readings are not committed.

## 0. What the run found

- **pgmvox 0.21.0 is 7,800 lines in 32 modules and 32 commits (2026-10-08 19:09 to 2026-10-10 09:27).** Its 95 tests pass in 4.9 s. Its own gate `check.py` fails two of four examples (stale snapshot, section 1.4).
- **All 22 boards that have a generator still build on 0.21.0 and build the same world.** Every `gen.py` passed (longest 28 s), each volume is byte-identical across two runs, and the logged block totals and stats equal the committed `renders/gen.txt` on every board that has one. One failure only in a bare copy of `lib/`: the Riftwater port reaches outside `lib/` for `trees.json` (section 3.2).
- **Two boards read back differently.** `ports/lantern-karst` and `ports/riftwater` were built before 0.10.3 (a running jump lands lower); bisected on archived trees, their walk numbers moved at 0.10.3. Riftwater's four monuments also fail the 0.21.0 float rule (1 block of air under them, not 3).
- **pgmvox duplicates itself little and its boards duplicate it a lot.** Inside the library: three argument orders for a rectangle, two `disc`s, a hand-rolled polyline walk in `landform`, a taxicab and a Euclidean edge distance, eleven clashing names (section 2.1). In the boards: five byte-identical `kit.py` files (784 lines), six hand-written ground-finishing passes after `terrain.lay`, three copies of one underside formula, three slab-island functions, nine water-fill loops (section 2.2).
- **The terrain shapes worth adding are 14** (S1-S14; S4 in three parts). The five that serve the most boards and blocks, in order: `terrain.lay` finishing (per-column bottom, position-aware top, wet beds; 6 boards), island outline with a wandering line (8 boards), heightfield terms (8 boards, 918,000 blocks hang on them in one board), `landform.profile` (3 boards, 598,159 of 718,000 height-blocks in one), underside with a sheer side (5 boards).
- **The plan has five phases:** a baseline that freezes the 22 hashes, a no-behaviour-change tidy, promotion of the repeated non-terrain props, the terrain shapes in ranked order each proven against the board code it replaces, then the boards move over. The studio port needs eight decisions before the first op is written (section 5.6).

## 1. pgmvox as it stands

### 1.1 The package

| fact | value | evidence |
|---|---|---|
| version | `0.21.0` | `freeform/lib/pgmvox/__init__.py:12` |
| code | 7,800 lines, 32 modules + `__init__` + `data/` | `wc -l pgmvox/*.py` |
| docs | `README.md` 497 lines, `AGENT-GUIDE.md` 176 lines | `freeform/lib/` |
| tests | 95 tests in 1,065 lines; ran: OK in 4.852 s | `tests/test_pgmvox.py`, `python3 -m unittest discover -s tests` in the scratch copy |
| gate | `check.py` 185 lines: tests, prose gate, four examples against `check/snapshot.json` | ran: tests ok, prose gate "FAIL" only because the scratch copy lacks `tools/prose-check.py` (run in the repository it reports 0 paragraphs over the cap for both documents), `islets` and `parts` FAIL (section 1.4) |
| python deps | numpy, scipy, Pillow | imports in `noise.py:8-9`, `landform.py:18-20`, `render.py:13` |
| outside-the-package deps | `tools/sculpt/solid.py` (`solid.py:20`), the studio checkout for `trees.library()` (`trees.py:57`, `world.py:174`) and for the Anvil writer (`world.py:182`, `data/write_world.cs`), the studio's exporters (`data/export_*.cs`) | |
| the pipeline | `python3 -m pgmvox.run <board>` runs `plan_check, sketch, gen, write, mapxml, renders, walk` and **writes `renders/*` and `renders/build-info.txt` into the board folder** | `run.py:29-86` (`gen.txt` at `:65`, `build-info.txt` at `:83-86`) |

The 7,800 lines fall into five groups by what they are for:

| group | modules | lines |
|---|---|---:|
| foundations | `blocks` 263, `orient` 269, `world` 190, `noise` 56, `shapes` 142, `solid` 67, `mapxml` 201, `move` 151 | 1,339 |
| ground and below (the terrain half) | `landform` 314, `terrain` 294, `route` 278, `under` 246, `forms` 130, `trees` 152 | 1,414 |
| building and look | `build` 566, `facade` 376, `props` 159, `grammar` 321 | 1,422 |
| board styles (three boards' looks live in the library) | `brittle` 650, `clay` 203, `studioplan` 107 | 960 |
| plan, play and checks | `plan` 174, `plangraph` 281, `pieces` 204, `sight` 84, `walk` 201, `audit` 92, `objectives` 652, `sketch` 547, `render` 198, `plot` 115, `run` 102 | 2,650 |

### 1.2 Modules and sizes

| module | lines | role |
|---|---:|---|
| `__init__` | 15 | package marker |
| `audit` | 92 | checks on a built world |
| `blocks` | 263 | block ids, classes, colours |
| `brittle` | 650 | Brittlebush style (a board style) |
| `build` | 566 | houses, roofs, frames, sites |
| `clay` | 203 | Claywork style (a board style) |
| `facade` | 376 | wall patterns, floor fields |
| `forms` | 130 | 3-D scenery (towers, skirts) |
| `grammar` | 321 | structural-board grammar |
| `landform` | 314 | heightfield operations |
| `mapxml` | 201 | map.xml writer |
| `move` | 151 | 1.8 movement physics |
| `noise` | 56 | fbm and friends |
| `objectives` | 652 | spawns, hills, wools, monuments, cores |
| `orient` | 269 | facing and turn tables |
| `pieces` | 204 | course plans |
| `plan` | 174 | plan raster + symmetry |
| `plangraph` | 281 | walk graph over a plan |
| `plot` | 115 | contributor canvas |
| `props` | 159 | stalls, lamps, chests |
| `render` | 198 | pictures of a world |
| `route` | 278 | route finding and paving |
| `run` | 102 | build pipeline |
| `shapes` | 142 | masks and distance fields |
| `sight` | 84 | sight lines |
| `sketch` | 547 | annotated sheets |
| `solid` | 67 | wrapper of tools/sculpt/solid.py |
| `studioplan` | 107 | reads the studio planner's plan v2 |
| `terrain` | 294 | slope, lay, strata, undersides, cloud |
| `trees` | 152 | tree library and planting |
| `under` | 246 | caves, mines, shafts |
| `walk` | 201 | voxel walk |
| `world` | 190 | voxel volume, Anvil bridge |
| **total** | **7800** | 33 files, 32 modules plus `__init__`; `data/` holds `blocks.json` (225 KB), `roofs.json.gz`, `slopes.json.gz` and five `.cs` exporters |

The public functions and classes of every module, with the line they start on and the first line of their docstring, are in **Appendix A**. Four classes carry most of their API as methods and are not expanded there: `World` (`inside index grid set get id fill column top heightmap chest sign banner save load`), `Raster` (`from_heights storey has ix iz inside h kind mask cell box rect where poly flight at`), `Frame` (`local world cell along across box grid mask cells`) and `RoofField` (15 methods).

### 1.3 Version history

32 commits touch `freeform/lib/pgmvox` (`git log --oneline -- freeform/lib/pgmvox`). The versions the commit messages name, with what each added:

| version | commit | when | adds |
|---|---|---|---|
| 0.1 | `57da19de`, `2cd053d3`, `048de680` | 10-08 19:09-19:38 | blocks, orient, world, noise, shapes, move, plan, plangraph, sight, walk; terrain (mountain ring, undersides, cloud deck), render, plot, mapxml, run; `sketch` |
| 0.2 / 0.3 / 0.4 | `2916186e`, `f3b0d241`, `dd684273` | 19:50-20:18 | `build`, `facade`; `pieces` (course plans); `objectives`, storeys, `solid` |
| 0.5 / 0.6 | `380728e6`, `a97fd265` | 20:40-20:52 | terrain as the studio reads it (`slope_deg`), rock beds, `landform`; `route` |
| 0.7 / 0.8 / 0.9 / 0.10 | `2c2d9031`, `16a0206d`, `f023c1dc`, `12675ed9` | 21:41-22:16 | `forms`; soil by slope, `props`; capture boards (`Wool`, bridged plan walk); `under`, `trees` |
| 0.10.1 / 0.10.2 / 0.10.3 / 0.10.4 | `d019d19c`, `0dc77e82`, `a501480d`, `0a26f326` | 10-09 10:03-13:35 | `audit.loose_water`; the sea runs to the void; **a running jump lands lower**; Claywork review |
| 0.11 / 0.12 / 0.13 | `53747f92`, `93aed9d0`, `2a384da8` | 15:51-17:24 | four teams, `brittle`; `studioplan`, hollow decks; one-block outlines, wool houses of whole cells |
| 0.14 / 0.15 / 0.16 | `1daa30da`, `779cff79`, `4f0a3501` | 18:06-18:47 | sections and fills; `grammar`; `clay` |
| 0.17 | `fb4529a6` | 19:21 | Sandreach (grammar plus grown ground on one board) |
| 0.18 / 0.19 | `4fde791a`, `b970fcb2` | 10-10 00:30-00:46 | `props.wool_chests`; `defence_chests` |
| 0.19.x | `b1a3e9c6` | 00:59 | `Destroyable` heart, several gamemodes |
| 0.20.0 | `c7f16729` | 01:08 | **a house keeps a block of wall either side of its door, never a window** (moved Glass Pane counts in `islets` and `parts`) |
| 0.21.0 | `1f3c655d` | 09:27 | **`Destroyable`/`Core` check the float rule** (3 blocks of air under, `objectives.py:416-436`) |

Nothing in the log says which versions changed a board's output; the readings in section 3 are the first measurement of that. Versions 0.10.4 and 0.17.0 exist only as `VERSION` strings inside commits named for boards.

### 1.4 State of the library's own gates

- **`check/snapshot.json` is stale.** Last touched by `0dc77e82` (0.10.2). On 0.21.0 `check.py` reports `islets: Glass Pane (102) 10 -> 8, Stone (1) 358484 -> 358486` and `parts: Bricks 155 -> 157, Cobblestone 459 -> 460, Glass Pane 98 -> 93, Iron Bars 18 -> 17, Stone 109478 -> 109480, Stone Bricks 268 -> 269`. That is 0.20.0's door rule, and nobody accepted it with `--update`. `drop` and `vale` read back as the snapshot.
- **The test suite reaches outside `lib/`.** `tests/test_pgmvox.py:32` points `CURIO` at `../../opus55-freeform-curio/plots`; without it `test_a_curio_plot_passes` cannot run (I copied the folder into the scratch tree to get 95 passing).
- **Test coverage is uneven.** Counting names that appear in the tests under their module alias: `shapes` 0 of 15, `landform` 8 of 13 (not named: `Water hold scarp stage blend`), `terrain` 5 of 13 (not named: `by_angle banded bed_offset beds ledge_angle soil_depth underside cloud_deck`), `under` 4 of 7 (`carve chamber dress_cave`), `route` 4 of 8 (`footprint grades pave steps`), `facade` 8 of 30, `build` 6 of 12 (`lay_roof edge_cells parapet site stairs ladder`). The terrain half is the half this plan changes.
- **Dead or near-dead public names** (no reference outside the definition in `pgmvox/`, `tests/` or any board): `facade.band_from_top` (`facade.py:76`), `facade.stepped_line` (`:313`), `objectives.Portal` (`objectives.py:558`), `shapes.centroid` (`shapes.py:95`). Referenced by a test only: `move.land_at` (`move.py:56`), `orient.rotation16` (`orient.py:95`). Used by no board: `terrain.banded` (`terrain.py:98`), `route.grades` (`route.py:218`), `plangraph.pad_edges` (`plangraph.py:255`), `pieces.polygon/lands_at/clears`.

## 2. Duplication and drift

### 2.1 Inside pgmvox

Each row is one job done twice (or one name meaning two things). "Cost" is what a reader or a caller pays today.

| # | what | where | evidence | cost |
|---|---|---|---|---|
| D1 | **A rectangle has three argument orders and four types.** `Raster.box(x0, z0, x1, z1)` takes corners, `Raster.rect(x0, x1, z0, z1)` takes ranges ("the older order; box takes corners"), `pieces.box(x0, x1, z0, z1)` returns a cell set in ranges, `facade.rect_cells(x0, z0, x1, z1)` returns a cell set in corners, `objectives.Box(x0, y0, z0, x1, y1, z1)` is a 3-D type. | `plan.py:136-143`, `pieces.py:36`, `facade.py:362`, `objectives.py:39` | `.rect(` has 71 call sites (29 in `trials/sonnet/whitecliff-cistern/scripts/plan.py`, 6 in the tests, 4 in `pgmvox/plan.py`), `.box(` 33 (20 in `trials/opus/vinewatch-ruins/scripts/plan.py`). The trial summary lists it as a known fault ("`Raster.poly` leaves out its boundary cells", "`Raster.flight` lays its width by heading inconsistently", `trials/sonnet/SUMMARY.md:77-78`, `trials/opus/SUMMARY.md:68`). | every new op must pick one; two boards already hit the order |
| D2 | **Two `disc`s and a three-hop `polygon`.** `shapes.disc(X, Z, cx, cz, r)` is a boolean mask; `pieces.disc(cx, cz, r)` is a cell set with a different centre convention; `pieces.polygon` calls `facade.poly_cells`, which calls `shapes.inside`. | `shapes.py:100`, `pieces.py:42-51`, `facade.py:370-375` | no board calls `pieces.disc` or `pieces.polygon`; one board calls `shapes.disc` (`ports/riftwater/scripts/plan.py:296`) | two answers to "which cells are within r" |
| D3 | **Distance along a polyline is written four times.** `shapes.polyline` (arrays) is the one copy; `landform._side` re-walks the segments to add a side (`landform.py:186-199`); three boards carry a scalar `_arc_of` of the same loop; one board inlines the array loop. | `shapes.py:49-62`; `landform.py:186-199`; `ports/riftwater/scripts/plan.py:418`, `trials/sonnet/cinderfall/scripts/plan.py:374`, `trials/sonnet/tamarisk-wash/scripts/plan.py:327`; `boards/exp-slatefold-pgmvox/scripts/dress.py:421-428` | `_arc_of` is byte-identical in the last two | a fix to the segment maths reaches one of five |
| D4 | **Two edge distances, two metrics.** `shapes.edge_depth` is taxicab (`distance_transform_cdt`, diamond-shaped); `landform.lake` and `landform.blend` use Euclidean `distance_transform_edt`; every hand-written underside uses Euclidean. | `shapes.py:137-142` (used by `terrain.py:241,261`, `forms.py:101`); `landform.py:114,311`; `ports/riftwater/scripts/plan.py:313-314` | same island, same call site: `root_depth` hangs a diamond, the boards' own formula an ellipse | an underside from pgmvox and one from a board differ by shape, not by numbers |
| D5 | **Two implementations of "the ground's top".** `World.top` loops a column; `World.heightmap` vectorises the same rule; `grammar.Ground.top` is a third (by section); boards pass `ground_at` lambdas. | `world.py:92-107`, `grammar.py:129`, `ports/riftwater/scripts/under.py:21` | | small |
| D6 | **Names that mean two things.** `windows` (`build.py:345` a rhythm function; `facade.py:159` a face pattern), `ladder` (`orient.py:56` data; `build.py:543` blocks placed), `steps` (`route.py:259` footpath stairs; `facade.py:305` kilim bands), `stairs` (`build.py:529`, widths to the right of the climb) against `Raster.flight` (`plan.py:155`, widths either side), `Cell` (`brittle.py:54`, `facade.py:268`), `tower` (`brittle.py:490`, `forms.py:29`), `house` (`build.py:377`, `brittle.py:513`), `lay` (`terrain.py:195`, `grammar.py:281`), `underside` (`terrain.py:255`, `RoofField.underside` `build.py:218`), `checker` (`clay.py:103`, `facade.py:113`), `cuboid` (`mapxml.py:51`, `Box.cuboid` `objectives.py:54`). | | `windows`: 5 boards call one of them; the stair width clash cost a column on a trial board (`trials/opus/SUMMARY.md` item 7) | reading and grep |
| D7 | **`smoothstep(e0, e1, x)` takes reversed edges on purpose and divides by `e1 - e0`.** Boards call it with `e0 > e1` to get a falling ramp (`smoothstep(-14, -64, X)`, `ports/riftwater/scripts/plan.py:201`); `e0 == e1` is a division by zero. No test names it. | `noise.py:39-41` | 8 pgmvox boards call it, 12 calls in the Riftwater port alone | the contract is a convention, and the studio port has to reproduce it |
| D8 | **A test-data writer lives in the library.** `terrain._slope_cases` writes the grounds `data/export_slopes.cs` reads. | `terrain.py:70-84` | | belongs in `tests/` or `data/` |
| D9 | **`fbm` depends on the grid it is drawn on.** The lattice is sized from `shape`, so one seed gives a different field on a bigger grid. Measured: seed 5, cell 20, 3 octaves on 100x100 against 120x100, maximum difference on the common corner 0.7116. Measured the other way: pgmvox's `fbm` equals the standalone boards' `noise.fbm` exactly (maximum difference 0.0 on three shapes), and so does `smoothstep`. | `noise.py:12-31` | | a board's seeds are tied to its grid size; so will a C# port's be |
| D10 | **Outside-the-package paths.** Tests need `opus55-freeform-curio/plots`; the Riftwater port needs `opus55-freeform-riftwater/scripts/trees.json`; `solid` needs `tools/sculpt/solid.py`; `trees.library()` and `write` need the studio checkout; `pgmvox.run` writes into the board folder. | `tests/test_pgmvox.py:32`, `ports/riftwater/scripts/dress.py:19-20`, `solid.py:20`, `trees.py:57`, `world.py:174-190`, `run.py:65,83` | a bare copy of `lib/` could not run the Riftwater port (section 3.2) | portability, and runs that dirty the tree |

Findings that are not code duplication but drift of the documents around the code:

- **README says the capture rebuild "proves the set" with its local walk replaced** (`README.md:151-152`); `ports/lantern-karst/scripts/plan_check.py:18` still imports `from planwalk import cells_of, graph, reach`, a 53-line local copy of what `plangraph.graph(bridge=..., rules=PlanRules(diagonals=True))` does since 0.9.0 (`plangraph.py:30-36,104-145`). `trials/sonnet/hoarfrost-reach/scripts/planwalk.py` is a byte-identical second copy (diff: 0 lines) that nothing imports.
- **`analysis/freeform-vs-studio/recipe/op-catalog.md` is generated from 0.19.0** (its header) and the Hollow Mesa layer file lists two ops as `pgmvox` that 0.21.0 does not have: `under.portal` and `paint.zone` (`hollow-mesa.layers.json`, `library.ops`; no such name in `under.py` or any module). The Riftwater layer file's `pgmvox.*` references all resolve (`House(style=dict)` is valid, `build.py:380`).
- **The recipe and pgmvox spell parameters differently.** `recipe/vale.recipe.json` uses `at`, `path`, `line`, `rise`; the pgmvox signatures use `centre`, `pts`, `pts`, `height` (`landform.py:164,63,202`). Section 5.6.

### 2.2 Helpers the boards copy instead of importing

**In the 23 board folders that run on pgmvox**, no board redefines `fbm`, `smoothstep`, `polyline_distance`, `site`, `canyon`, `tunnel` or `chamber`'s maths: those moved into the library and stayed there (the one `lake` is `ports/riftwater/scripts/under.py:41`, an underground pool of 346 blocks, a different thing; `under.py:37` and `:127` are thin wrappers that call `U.chamber` and `U.shaft`). The repetition is one level up, in the glue the library does not have:

| # | repeated code | copies | evidence (file:line) | what pgmvox has | what it lacks |
|---|---|---:|---|---|---|
| R1 | **`kit.py`**: `scatter_points` 14 lines, `log_axis`, `dead_tree` 18, `rubble` 10, `brazier` 5, `tower` 47, `lamps` 21 | **5 identical files, 157 lines each** (the fifth differs by 3 lines) | `trials/sonnet/{overgrowth,whitecliff-cistern,cinderfall,tamarisk-wash,hoarfrost-reach}/scripts/kit.py`; its own header says "a thing written by a second board belongs in pgmvox" (`kit.py:1-4`) | `props.lamp` (9 boards use it), `forms.tower` (karst), `brittle.tower`, `trees.scatter` | a lamp row along a route, a masonry tower with ladder and crown, a brazier, rubble, a Poisson scatter of points over a mask |
| R2 | **Ground finishing after `terrain.lay`**: clear under the column's own bottom, lay the water bed and fill the water, repaint the top by slope **and** place and noise | **6** | `ports/riftwater/scripts/ground.py:24-67` (44 lines), `trials/sonnet/overgrowth/scripts/gen.py:46-71` (26), `trials/sonnet/cinderfall/scripts/gen.py:62-117` (56), `trials/sonnet/tamarisk-wash/scripts/gen.py:37-81` (45), `trials/opus/redwash-mesa/scripts/gen.py:55-85`, `trials/opus/cinder-reach/scripts/gen.py:66-110`. The clear-under-bottom pair `w.ids[i, :bottom, k] = 0` appears in 4 of them (`ground.py:39-40`, `cinderfall gen.py:80-81`, `cinder-reach gen.py:92-93`, `redwash gen.py:64-65`); the water-bed pair in 5 | `terrain.lay` (`terrain.py:195`) takes one `from_y`, a `top(deg, h)` callback that sees no position, and no water | per-column bottom, position-aware top, water |
| R3 | **Water from a `landform.Water` into blocks** | **9 sites** | `examples/vale/scripts/gen.py:19-24`, `boards/exp-abbeymoor-pgmvox/scripts/dress.py:114-135`, the six boards of R2, and the test helper `tests/test_pgmvox.py:211-217` | `landform.Water` (mask, surface, falls) and `audit.loose_water` | the op that writes it |
| R4 | **Island underside: the same two-distance formula** `thick = min(a + 0.9 d_outer + 4n, b + k d_rift + 4n); bottom = max(ground - thick, c + 3 fbm)` | **3 identical in shape, constants differ** (4/26, 5/30, 6/34); two single-distance variants | `ports/riftwater/scripts/plan.py:311-317`, `trials/opus/cinder-reach/scripts/plan.py:206-212`, `trials/opus/redwash-mesa/scripts/plan.py:191-197`; variants `trials/sonnet/cinderfall/scripts/plan.py:232-243`, standalone `opus55-freeform-hollow-mesa/scripts/terrain.py:176-183` | `terrain.root_depth` (taxicab cone) + `underside` | a sheer side, Euclidean distance, a bottom taken from the column's own ground |
| R5 | **Island outline: the 1-D wandering line** `X >= X_MIN + (2 + 4 fbm((n,), 16, 2, seed)).clip(0, 6)` and `lip = -8 - ragged(...)` | **5 pgmvox boards + 3 standalone** | `_ragged` is defined twice, identical: `cinder-reach/scripts/plan.py:100`, `redwash-mesa/scripts/plan.py:104`; the inline form `ports/riftwater/scripts/plan.py:167-174,188-193`; standalone `hollow-mesa/scripts/terrain.py:163-168`, `riftwater/scripts/terrain.py:56-66` | | |
| R6 | **Slab island per floor height** (`lay` per unique floor, `root_depth` capped by the floor, `underside`, a bedrock course, moss on the rim) | **3** | `boards/exp-slatefold-pgmvox/scripts/gen.py:49-74`, `ports/lantern-karst/scripts/gen.py:38-59`, `trials/sonnet/hoarfrost-reach/scripts/gen.py:51-80`: each loops `np.unique(floor[land])` because `lay` takes one `from_y` while `underside` already accepts a per-column `top_y` | `lay`, `root_depth`, `underside`, `forms.skirt` | the loop |
| R7 | **A half-turn-symmetric field** | **3 + a helper** | `boards/exp-abbeymoor-pgmvox/scripts/land.py:36-45,117-119` (`sym`, `symnoise`), `trials/sonnet/cinderfall/scripts/plan.py:137-143` (`sym`, `rot`), `trials/opus/common.py:34-43` (`full`) | `plan.Symmetry` (points, rasters) | the same for float fields |
| R8 | **Plan-check glue**: `door_cell` 7 files (4 variants), `spec` 6, `zone_mask` 6, `route_via` 4 (3 variants), `reach`/`graph` 14 and 7, `_tube_cells` 2 identical, `cells_of` 3 | see counts | `boards/exp-abbeymoor-pgmvox/scripts/plan.py:145`, `ports/riftwater/scripts/plan.py:366`, `trials/sonnet/cinderfall/scripts/plan.py:325`, ... (full list: `grep -rn "^def door_cell"`); `trials/opus/common.py` (165 lines: `full image_box gaps via set_paint cell_pick kit table`) is the one shared module, and it is outside pgmvox | `plangraph`, `sight` | route-via, gaps, a house's door cell, the plan-check table |
| R9 | **Waterfall off an island edge** | 4 (+ 2 shelf falls) | `opus55-freeform-hollow-mesa/scripts/terrain.py:285-298`, `opus55-freeform-riftwater/scripts/terrain.py:290-306`, `opus55-freeform-cloudhaven/scripts/terrain.py:121-148`, `lib/ports/riftwater/scripts/ground.py:70-84`; shelf falls `sunwell/scripts/gen.py:160-172`, `copperline/scripts/gen.py:297-306` | `audit.loose_water` allows a `WATER_FLOW:8` fall over the void | |

**On the 20 standalone boards** (`opus55-freeform-*`, no pgmvox, left as built by design): `noise.py` is one md5 in 19 folders (1,197 lines; `fbm`, `smoothstep`, `lattice`, `spline`, `polyline_distance` each defined 19 times), `mc.py` is five variants in 19 folders (4,104 lines), `walk_core.py` 8 copies, `write_world.cs` 3 variants in 20 folders, `rotate.py`/`mirror.py` 10 files. `SHARED-LIBRARY-ASSESSMENT.md` §0 puts it at 15,800 of about 50,000 lines. Local definitions of library names also appear as `site` (4 defs in 3 boards), `plant` (6 in 6), `slope_deg` (5 in 4), `set_ground` (3 in 3), `house` (3 in 3), `shaft` (2), `carve` (2), `pave` (2).

## 3. Which board uses which pgmvox version and API

### 3.1 How this was measured

- **Where.** A copy of `freeform/lib` and `tools/sculpt` under `/tmp/pgmvox-inventory/repo/`, `PGM_STUDIO_ROOT=/home/user/pgm-studio`, `PYTHONPATH` at the copy. `pgmvox.run` writes into the board folder, so running it in the repository would have changed committed files; the copy kept the repository untouched.
- **What.** Per board, three steps through `python3 -m pgmvox.run <board> --build <dir> --only <step> --skip write`: `plan_check`, `gen`, `mapxml`; then `--only walk` on the built volume. `renders` and `sketch` were not run (they draw pictures; the numbers are in the other steps). Each run had a 180 s limit; the longest was 157.1 s (`brittlebush-iii` walk), no run timed out.
- **Two readings of "still works".** (1) *Runs*: exit code 0. (2) *Reads back the same*: the normalised text of the new `renders/gen.txt` and `renders/walks.txt` (timings stripped) against the committed one. `gen` was run twice and the `volume.bin` of every board is byte-identical across the two runs, so each hash below is a repeatable baseline.
- **Not run.** The 20 standalone `opus55-freeform-*` boards (no pgmvox), `renders.py` and `sketch.py` of any board, the `write` step (needs `dotnet` and the studio's Anvil writer).

### 3.2 Result table

`built with` is `renders/build-info.txt` (written by `pgmvox.run`). Other version claims in prose: `trials/sonnet/hoarfrost-reach/REPORT.md:13` ("first built with pgmvox 0.10.0 and this build runs 0.18.0"), `boards/exp-*/PLAN.md:3` (0.19.0), `ports/riftwater/PORT-REPORT.md:3` (rebuilt on 0.6.0), `trials/{opus,sonnet}/SUMMARY.md:4` (0.10.0, since rebuilt). No `times.txt` carries a version; the two in `boards/exp-*` are phase clocks.

| board | script lines | built with (build-info) | plan_check | gen | mapxml | walk | gen output vs committed | walk read-back vs committed | volume sha256 (first 12) |
|---|---:|---|---|---|---|---|---|---|---|
| `boards/brittle-study` | 384 | 0.10.4 | no script | pass 0.6s | no script | pass 0.8s | identical | identical | 9f91f23566eb |
| `boards/brittlebush-iii` | 368 | 0.19.0 | no script | pass 1.1s | pass 0.7s | pass 157.1s | identical | identical | 2e561d06bd5b |
| `boards/brittlebush-koth` | 824 | 0.16.0 | pass 1.9s | pass 0.9s | pass 0.4s | pass 76.3s | identical | identical | 52193131fef5 |
| `boards/claywork` | 1227 | 0.19.0 | pass 3.6s | pass 1.2s | pass 0.4s | pass 83.8s | identical | identical | 1aa66a1a1856 |
| `boards/exp-abbeymoor-pgmvox` | 1656 | 0.19.0 | pass 5.6s | pass 5.7s | pass 1.1s | pass 17.5s | identical | identical | 1ebf677f630d |
| `boards/exp-slatefold-pgmvox` | 1447 | 0.19.0 | pass 5.7s | pass 1.9s | pass 0.5s | pass 16.9s | identical | identical | 94845f7c70a9 |
| `boards/sandreach` | 504 | 0.20.0 | no script | pass 1.0s | pass 0.8s | pass 136.4s | identical | identical | e3a423896295 |
| `examples/drop` | 98 | 0.11.0 | pass 0.3s | no script | no script | no script | no gen | no walk | - |
| `examples/islets` | 216 | 0.11.0 | pass 0.4s | pass 1.0s | pass 0.4s | pass 6.3s | identical | identical | ef171561d1b0 |
| `examples/parts` | 74 | 0.11.0 | no script | pass 0.5s | no script | no script | identical | no walk | 478e32a02e84 |
| `examples/vale` | 173 | 0.11.0 | pass 27.5s | pass 28.3s | no script | pass 1.1s | identical | identical | c178173ebf15 |
| `ports/lantern-karst` | 1381 | 0.8.0 | pass 2.2s | pass 3.2s | pass 0.3s | pass 10.5s | identical | 12 lines differ | 8564a5f4427d |
| `ports/riftwater` | 1885 | 0.10.0 | pass 2.3s | pass 5.2s (after supplying trees.json, see 3.3) | pass 0.7s | pass 13.8s | identical | 8 lines differ | a5debc6aaf91 |
| `trials/opus/brassmoor-works` | 1017 | 0.19.0 | pass 2.5s | pass 0.9s | pass 0.8s | pass 109.7s | identical | identical | b9094db78f4a |
| `trials/opus/cinder-reach` | 1463 | 0.20.0 | pass 2.6s | pass 10.2s | pass 0.6s | pass 122.2s | identical | identical | 2186a83b2c8d |
| `trials/opus/redwash-mesa` | 1122 | 0.20.0 | pass 2.5s | pass 1.8s | pass 0.8s | pass 99.7s | identical | identical | ab058a453e43 |
| `trials/opus/tidewell-canals` | 873 | 0.20.0 | pass 2.1s | pass 0.9s | pass 0.7s | pass 18.7s | identical | identical | bf6aadf7a393 |
| `trials/opus/vinewatch-ruins` | 853 | 0.19.0 | pass 8.3s | pass 1.1s | pass 0.9s | pass 16.0s | identical | identical | ab032be5cef8 |
| `trials/sonnet/cinderfall` | 1493 | 0.20.0 | pass 2.0s | pass 2.5s | pass 0.9s | pass 8.9s | identical | identical | d52a710d86e0 |
| `trials/sonnet/hoarfrost-reach` | 1244 | 0.20.0 | pass 1.5s | pass 1.4s | pass 0.3s | pass 7.0s | identical | identical | 1474d7985b74 |
| `trials/sonnet/overgrowth` | 1140 | 0.19.0 | pass 2.2s | pass 1.4s | pass 1.0s | pass 0.9s | identical | identical | bebf8bd669c9 |
| `trials/sonnet/tamarisk-wash` | 1742 | 0.20.0 | pass 4.1s | pass 2.7s | pass 0.5s | pass 2.3s | identical | identical | 222eaa3d8c17 |
| `trials/sonnet/whitecliff-cistern` | 1194 | 0.10.0 | pass 2.2s | pass 1.4s | pass 0.4s | pass 0.9s | identical | identical | dfaabe638f51 |

### 3.3 What the table says

- **22 of 22 buildable boards pass `plan_check`, `gen`, `mapxml` and `walk` on 0.21.0**, where the board has the step. `examples/drop` has only a plan check and a sketch.
- **One environment failure, not a library one.** The first `ports/riftwater` `gen` failed with `FileNotFoundError: .../freeform/opus55-freeform-riftwater/scripts/trees.json` (`ports/riftwater/scripts/dress.py:19-20` builds that path with four `..`). With that one file copied in, `gen` passes: 1,002,206 blocks and 22 tile entities, equal to `renders/gen.txt` and to the Anatomy's run.
- **Gen output is unchanged from the committed one on every board** (timings aside), including the three oldest builds: `ports/lantern-karst` (0.8.0), `ports/riftwater` (0.10.0) and `trials/sonnet/whitecliff-cistern` (0.10.0). Block totals equal the committed ones where printed (e.g. Tamarisk Wash 1,674,646; Claywork 364,722 with 40 tile entities).
- **Two boards read back differently, and one now fails a rule.**

| board | committed read-back | on 0.21.0 | cause (bisected) |
|---|---|---|---|
| `ports/lantern-karst` | 7,452 places reached on foot; own monuments 17 and 18 blocks away | 7,460 places; 15 and 15 blocks (both teams) | the walk moved at **0.10.3** (`a501480d`, "a running jump lands lower"): ran the port's scripts on archived trees of 0.10.2 (`0dc77e82`: identical to committed, 0 lines) and 0.10.3 (identical to 0.21.0, 0 lines) |
| `ports/riftwater` | running-jump walks square / green 60 / 72 (each team); `objectives with a problem: 0` | 49 / 62; **`objectives with a problem: 4`**: `destroyable red-square`, `blue-square`, `red-green`, `blue-green`: "1 of air under it, not 3: it must float over the floor" | the jump walk moved at 0.10.3 (0.10.2: 60 / 72; 0.10.3: 49 / 62, problems 0); the four monument problems arrive at **0.21.0** (`1f3c655d`), because the port still hangs its monuments one block over the floor (`PORT-REPORT.md`; the Anatomy §6 says the original hangs them three) |

  Both ports were last built before 0.10.3, so their committed `walks.txt` are the only stale read-backs in the repository. Neither is a regression in the sense of a bug: the model changed on purpose. What they need is a decision by the board's owner (re-measure against the plan's targets) and, for Riftwater, the monuments moved to three over the floor.
- **`check/snapshot.json` is stale for `islets` and `parts`** (section 1.4); the boards behind it still build, only the fingerprint is old.
- **Runtime.** `gen` costs 0.2-10.2 s on 21 boards and 28.3 s on `examples/vale`; the 22 builds add up to about 75 s of run time. That makes a full regression gate cheap: one run of all 22 `gen`s with a sha256 of each `volume.bin` is a minute, against the walks' 0.8-157 s each (which a gate does not need).

### 3.4 API footprint on the terrain side

Which terrain-side modules each board imports and which `landform` and `terrain` names it actually calls (AST: attribute access on the imported module alias, or a name imported from it). Boards with all cells empty use none: they are structural boards (`grammar`, `brittle`, `clay`) or plan-only.

| board | `landform` | `terrain` | `under` | `forms` | `route` | `trees` | `landform` ops called | `terrain` ops called |
|---|---|---|---|---|---|---|---|---|
| `boards/brittle-study` |  |  |  |  |  |  | - | - |
| `boards/brittlebush-iii` |  |  |  |  |  |  | - | - |
| `boards/brittlebush-koth` |  |  |  |  |  |  | - | - |
| `boards/claywork` |  |  |  |  |  |  | - | - |
| `boards/exp-abbeymoor-pgmvox` | x | x |  | x | x | x | Water, hold, lake, watercourse | Strata, bed_offset, beds, lay, slope_deg |
| `boards/exp-slatefold-pgmvox` |  | x |  | x |  | x | - | Strata, bed_offset, beds, cloud_deck, lay, root_depth, underside |
| `boards/sandreach` |  | x |  |  |  | x | - | root_depth, slope_deg |
| `examples/drop` |  |  |  |  |  |  | - | - |
| `examples/islets` |  | x |  |  |  |  | - | cloud_deck, lay, mountain_ring, underside |
| `examples/parts` |  |  |  |  |  |  | - | - |
| `examples/vale` | x | x |  |  | x |  | butte, canyon, coast, grade, hold, scarp, spire, terraces, watercourse | Strata, bed_offset, beds, by_angle, lay, root_depth, underside |
| `ports/lantern-karst` |  | x |  | x | x |  | - | Strata, bed_offset, beds, cloud_deck, lay, root_depth, underside |
| `ports/riftwater` | x | x | x |  | x | x | blend, grade, spire, terraces, watercourse | Strata, beds, by_angle, lay, slope_deg |
| `trials/opus/brassmoor-works` |  | x |  |  |  |  | - | cloud_deck |
| `trials/opus/cinder-reach` | x | x | x | x | x | x | blend, grade, spire, terraces | Strata, beds, by_angle, lay, slope_deg |
| `trials/opus/redwash-mesa` | x | x | x |  | x | x | butte, grade, spire | Strata, beds, by_angle, lay, slope_deg |
| `trials/opus/tidewell-canals` |  |  |  |  |  |  | - | - |
| `trials/opus/vinewatch-ruins` |  |  |  |  |  | x | - | - |
| `trials/sonnet/cinderfall` | x | x | x | x | x |  | blend, grade, scarp | Strata, bed_offset, beds, by_angle, lay, slope_deg |
| `trials/sonnet/hoarfrost-reach` |  | x |  |  |  | x | - | Strata, bed_offset, beds, cloud_deck, lay, root_depth, underside |
| `trials/sonnet/overgrowth` |  | x |  |  |  | x | - | Strata, bed_offset, beds, by_angle, lay, slope_deg |
| `trials/sonnet/tamarisk-wash` | x | x | x |  | x |  | blend, butte, grade, stage | Strata, bed_offset, beds, by_angle, lay, slope_deg |
| `trials/sonnet/whitecliff-cistern` |  | x |  |  |  | x | - | Strata, bed_offset, beds |

What the footprint says for the plan: `terrain.lay` is called by 12 boards, `landform.grade` by 6, `blend` by 4, `spire` by 4, and `canyon` and `coast` by one board each (the Vale example) and `stage` by one (Tamarisk Wash). Seven boards use `landform` at all; the other terrain work in this repository is in board-local formulas (section 4).

## 4. The terrain shapes to add

### 4.1 Method and scope

Sources: the two analyses (`boards-as-json/riftwater/{FINDINGS,ANATOMY}.md` + `*.layers.json`, `boards-as-json/hollow-mesa/{FINDINGS,ANATOMY}.md` + `hollow-mesa.layers.json`), the op catalogue (`recipe/op-catalog.md`, 0.19.0), and a read of the terrain code of every board: the 7 `terrain.py` files of the standalone boards, the `plan.py`/`land.py` heightfield code and the `gen.py` ground passes of the 23 pgmvox folders. **A "shape" is something that decides where ground is or which blocks the ground is made of; towers, bridges, houses and furniture are not terrain and are listed in 4.4.** "Boards" counts folders that implement the shape locally; the standalone boards are marked `(sa)` and were not rebuilt. The block figures are the analyses' (quoted with their source) except where marked "measured here".

**Two facts shape every row.** The ground stack is where the blocks are: 97.2% of Hollow Mesa (1,742,764 of 1,792,366 blocks, one rule, `write_land`) and 90.7% of the Riftwater port (908,648 blocks, one `terrain.lay` call). And the analyses agree on what blocks the JSON form: the heightfield formulas (Riftwater: "14 new or extended ground ops… zero blocks of their own, 918,000 depend on them"; Hollow Mesa: "598k of the 718k height-blocks the heightfield stages move" are one cross-section).

### 4.2 The shapes

| # | shape (proposed name) | what it does | implemented locally in (file:line) | parameters it would take (units: blocks; y absolute) | extends / new | blocks accounted for |
|---|---|---|---|---|---|---|
| **S1** | **canyon cross-section: `landform.profile`** | Ground set to a stated height at stated distances from a centreline, eased between: floor, lower cliff, bench, upper cliff, plateau, each edge wandering by its own noise, a talus against the foot, a rolling plateau, a ragged jag. Cuts and lifts (absolute, not relative to the ground as `canyon` is). | **Hollow Mesa (sa)** `opus55-freeform-hollow-mesa/scripts/terrain.py:85-114` (floor 41, half-width 26, bench 57, plateau 74; noises seeds 1-7); **Redwash Mesa** `trials/opus/redwash-mesa/scripts/plan.py:134-146` (the Wash: floor stepping down east, lower cliff to the Shelf at 52, shelf, upper cliff, half-width varying with arc fraction); **Riftwater port** `ports/riftwater/scripts/plan.py:209-218` (valley: bluff 7 blocks one side, bank 14 the other, floor level + 1 per reach); Hollow Mesa's Wash `terrain.py:125-133` is the same cross-section on a side line | `profile(H, X, Z, centre, stations, side="both", ease="smoothstep", wander=None, jag=None, talus=None, mode="set")`: `centre` a polyline or `x = f(z)`; `stations` = ordered `[(offset, y), ...]` or `(offset, "ground")`; `wander` per station `(amp, cell, octaves, seed)` along the arc (the 1-D line, S0a); `talus=(rise, reach, mix)`; `mode` `"set"`/`"lift"`/`"cut"` | **new**; `canyon` (`landform.py:135`) only cuts, one floor, one wall exponent. `watercourse`'s banks and `scarp` are its one- and two-station cases | Hollow Mesa: **598,159 of ~718,000 height-blocks** the heightfield stages move; **1,742,764 world blocks (97.23%)** stand on it (FINDINGS "Canyon cross-section"; ANATOMY step 1/3). Riftwater valley: inside the 918,000 |
| **S2** | **island outline: `shapes.island`** (with `noise.line`, S0a) | The land mask of a floating board: a box whose four edges are inset by a wandering amount, one edge a ragged lip bitten into bays and held straight at stated places (under a town, a bridge, a fall), far corners cut by a noisy polygon, a stream exempted so it can leave the board. | pgmvox boards: Riftwater port `ports/riftwater/scripts/plan.py:167-174` (`_rift_edge`) + `:188-193`; Cinder Reach `trials/opus/cinder-reach/scripts/plan.py:100-101,113-122`; Redwash Mesa `trials/opus/redwash-mesa/scripts/plan.py:104-105,117-126` (`_ragged` defined twice); Abbeymoor `boards/exp-abbeymoor-pgmvox/scripts/land.py:60-64`; Sandreach `boards/sandreach/scripts/plan.py:157-165` (radial, `r = hypot(..) + 0.22 fbm`). (sa): Hollow Mesa `terrain.py:163-168`, Riftwater `terrain.py:56-66`, Cloudhaven `terrain.py:27-34` (harmonics) | `island(X, Z, box, insets, lip=None, corners=(), exempt=None)`: `box=(x0, z0, x1, z1)` inclusive; `insets={"west": Wander(base=2, amp=4, cell=16, octaves=2, seed=22, clip=(0, 6)), ...}`; `lip=Lip(axis="x", at=-11, wobble=Wander(1.2, 10, 2, 21, clip=(-1, 0)), bays=Wander(4.5, 22, 2, 25), hold=[(centre, width, power)])`; `corners=[(polygon, jag)]` | **new**; replaces the `fbm((n,), cell, 2, seed)[None, :]` idiom (S0a) | not separate: it decides which columns of the ground stack exist (Hollow Mesa 1,742,764; Riftwater 918,000). 5 pgmvox boards + 3 (sa) |
| **S3** | **heightfield terms: `field.terms`** | A base height plus named terms summed under masks: smoothstep ramps along an axis (rising or falling), gaussian mounds (elliptical, any power), tilts, `fbm`/`ridged`; "north of the river" / "west blend" masks pick which sum applies where. The numbers stay the board's. | Riftwater port `ports/riftwater/scripts/plan.py:195-207` (`h_n`, `h_s`, `h_w` and the west blend), `:173` (power-4 gaussian hold), `:234`; Cinder Reach `plan.py:124-126,137`; Cinderfall `trials/sonnet/cinderfall/scripts/plan.py:151,171`; Abbeymoor `land.py:67-74` (`hill_term`, `ridge_term`); Sandreach `plan.py:140-142`; Redwash `plan.py:128-131`. (sa): Riftwater `terrain.py:77,117,151`, Frostholm `terrain.py:61,77,125`, Hollow Mesa `terrain.py:91-114`. `smoothstep` is called in 8 pgmvox boards (12 times in the Riftwater port) and in 5 standalone `terrain.py` files; `np.exp(-…)` gaussians in 3 pgmvox boards and 2 standalone | `terms(X, Z, base, terms, mask=None, where=None)`; term kinds `ramp(axis, frm, to, amp)` (edges as given, reversed allowed), `gauss(at, rx, rz=None, amp, power=2, angle=0)`, `tilt(dx, dz)`, `fbm(amp, cell, octaves, seed, gain)`, `ridged(...)`, `line(axis, amp, cell, octaves, seed)`; combiner `piecewise([(mask, terms), ...], blend=width)` | **new**, builds on `noise` (`fbm ridged smoothstep`) and `shapes`; the studio's relief marks state the same shapes as placed marks (Riftwater FINDINGS) | Riftwater: **0 own blocks, 918,000 depend** (FINDINGS "Ops and templates", item 1); 14 ground ops |
| **S4a** | **`terrain.lay`: per-column bottom** | `lay` fills every column from one `from_y`; boards then clear everything under the column's own underside bottom. | Riftwater port `ground.py:39-40`; Cinderfall `gen.py:80-81`; Cinder Reach `gen.py:92-93`; Redwash `gen.py:64-65` | `lay(..., bottom=None)`: an int array (world grid) or a scalar; replaces `from_y` for the rock fill | **extends** `lay` (`terrain.py:195`; `underside` already takes a per-column `top_y`, `terrain.py:255`) | Riftwater: **455,476 blocks laid then cleared** (FINDINGS "terrain.lay finishing"); 910,952 carved to air counting both halves (ANATOMY §4 row 2, which is twice 455,476) |
| **S4b** | **`terrain.lay`: position-aware top** | The top block chosen by slope **and** place: patches by noise quantile, worn edges, rock on steep ground, a sandy lip by the river, hardened-clay rings, cell-picked floors. | Riftwater `ground.py:52-62`; Overgrowth `gen.py:66-69`; Cinderfall `gen.py:82-116`; Tamarisk Wash `gen.py:60-78`; Redwash `gen.py:72-86`; Cinder Reach `gen.py:98-117`. (sa) Hollow Mesa `terrain.py:259-282`. Shared helpers outside the library: `trials/opus/common.py` `set_paint`, `cell_pick` | `lay(..., paint=None)` where `paint` is a list of layers `Paint(when, block)` with `when` = `Slope(lo, hi)` & `Band(y0, y1)` & `Mask(m)` & `Noise(cell, seed, above=q)` & `Near(polyline, d)`; blocks may be `weights`/`cell_pick(cell, shares)`. Today's `top(deg, h)` stays | **extends** `lay`; `by_angle` (`terrain.py:87`) is the one-layer case | Riftwater: **9,528 blocks of local top-painting (0.951%)**, 4,904 exposed (ANATOMY §4 row 2); the "10 layers of 9 new ops" and the "quantile-banded patches… no op" note in Hollow Mesa's layers |
| **S4c** | **wet beds: `terrain.fill_water`** | Write a `landform.Water` into the world: bed block mix (still water vs stream), water to the surface, the ground under it made the bed. | Vale `examples/vale/scripts/gen.py:19-24`; Abbeymoor `dress.py:114-135`; Riftwater `ground.py:43-51`; Overgrowth `gen.py:61-65`; Tamarisk `gen.py:55-58`; Redwash `gen.py:66-71`; Cinder Reach `gen.py:94-96`; the test helper `tests/test_pgmvox.py:211-217`. (sa) Hollow Mesa `terrain.py:249-252` | `fill_water(w, H, waters, bed=((id, data, weight), ...), still=None, flow=None)`; `waters` the `Water` list `watercourse`/`lake`/`coast` return | **new**, completes `landform.Water`/`audit.loose_water` | in the 9,528 above; water and bed not separated |
| **S5** | **underside with a sheer side: `terrain.root_depth` / `underside` variants** | How far each column hangs below the ground: tapering by distance to the void everywhere (`a + k·d_outer`), but held sheer (`b + k·d_rift`, 26-34 blocks) under a chosen edge such as the rift; bottom taken from the column's own ground, floored at a noisy level; Euclidean distance. | **3 copies of one formula**: Riftwater `plan.py:311-317`; Cinder Reach `plan.py:206-212`; Redwash `plan.py:191-197`; one distance: Cinderfall `plan.py:232-243`; (sa) Hollow Mesa `terrain.py:176-183`, Riftwater `terrain.py:175-191`. pgmvox's `root_depth` (taxicab cone, flutes, spires) is used by 5 boards (Sandreach `gen.py:71`, Slatefold, Lantern Karst, Hoarfrost, Vale) | `root_depth(mask, ..., sheer=None, taper=(base, slope), sheer_depth=(base, slope), floor=(level, amp, cell, seed), metric="euclid")` returning the bottom array, `underside(depth=)` unchanged | **extends** `root_depth`/`underside` (`terrain.py:236,255`); removes D4 | part of the column fill; Riftwater's "two-distance underside" is one of the 14 ground ops |
| **S6** | **level pad: `landform.level`** | Ground set to one level inside a disc, ellipse, rectangle or polygon (corners rounded), the median ground if no level is given, eased back to the ground over a skirt; optionally not over water. | Riftwater `plan.py:246-256` (spawn shoulder 59; square and green blend), `:291-297` (square 52, rounded corner 3.2; green 50); Hollow Mesa `terrain.py:141-146` (three pads); Abbeymoor `land.py:90-97` (village, farm, flank); Sandreach `plan.py:143-153` (stair foot, emerald plinth); Cinder Reach `plan.py:142-145` (lodge terrace, 57); Redwash `plan.py:148-` (cliff-house ledge) | `level(H, X, Z, shape, y="median", skirt=6, ease="smoothstep", jag=0.0, seed=0, not_in=None)`; `shape` = `("disc", at, r)` / `("ellipse", at, rx, rz, angle)` / `("rect", box, corner_radius)` / `("poly", pts)` | **new**; `blend` (`landform.py:308`) is the mask form, `stage` (`landform.py:226`) the stepped circular form, `build.site` (`build.py:502`) the footprint form | Riftwater layers: `square-floor`, `green-floor`, `spawn-shoulder`, zero own blocks; counted inside the 918,000 |
| **S7** | **radial features, elliptical and rotatable: `landform.mound`, `crater`, and `rz/angle/tier/crown` on `spire`, `butte`, `stage`** | A bump or bowl with an elliptical footprint, a profile exponent, a ragged edge, an optional flat crown; a butte with a lower tier round its foot and sheer sides; a sinkhole as concentric one-block steps. | Riftwater: knoll by stretching z (`plan.py:258-260`), spoil heap `:305-309`, sinkhole funnel `:299-303`, spawn shoulder oval `:246-251`; Hollow Mesa butte `terrain.py:39-45` (rx, rz, tier 6; two uses `:136-137`); Cinder Reach knolls `plan.py:128-132` (round `spire` plus a hand-made flat crown), lodge oval `:142-145`; Abbeymoor `hill_term` `land.py:67-70` plus the ragged plateau `:85-89`; Cinderfall caldera mouth `plan.py:171` | `mound(H, X, Z, at, rx, rz=None, angle=0, height, profile=1.6, jag=0, seed=0, crown=0)`; `crater(..., floor, step=1)`; add `rz`, `angle`, `tier=(rise, reach)`, `crown` to `spire`/`butte`/`stage` (`landform.py:164,174,226`) | **extends** three ops, **new** two | Hollow Mesa's two buttes: **6,047 height-blocks** per half, 671 columns (measured here, `build_heights` with and without `butte`); Riftwater spoil rubble 484 blocks + lake-pool 346 are the volume parts |
| **S8** | **ridge with a wandering foot, spurs and terraces: `landform.ridge`** | A back ridge whose foot wanders ~15 blocks, crest from noise with a bump, ragged crag from ridged noise above a threshold, spur arms with a fall per block, cut into 3-block terraces. | Riftwater `plan.py:230-244`; Cinder Reach `plan.py:134-140` (Caldera Wall) + `:147-` (Spine, crest line rising to a crag); Hollow Mesa scarp with gullies `terrain.py:116-123`; (sa) Riftwater `terrain.py:114-130` | `ridge(H, X, Z, foot=Wander(...), crest=..., crag=(amp, cell, seed, lo, hi), spurs=[(path, top, fall, reach)], terraces=(step, riser), far_fall=...)` | **new**; composes `scarp` (`landform.py:202`, lifts one side of a line) and `terraces` (`landform.py:215`) | inside the 918,000 / 1,742,764 |
| **S9** | **spire field: `landform.spire_field`** | N spires and hoodoos rejection-sampled in a zone: radius, height, needle (`1-(d/r)^1.3`) and hoodoo (`1-(d/r)^5`) profiles, spacing `r_i + r_j + 2.5`, paths kept clear. | Hollow Mesa `terrain.py:48-82` (400 tries, 13 accepted + 7 fixed = 20; the analysis notes 13 `spire` layers would do and no new op); the sampling idiom is also `kit.scatter_points` ×5 (`trials/sonnet/*/scripts/kit.py:15`) and `trees.scatter` | `spire_field(H, X, Z, zone, n, r=(1.6, 3.4), height=(8, 22), needle_share=0.7, spacing=2.5, keep_clear=[(path, margin)], seed=0, profiles=("needle", "hoodoo"))` returning H and the sites | **new**; needs `spire`'s profile exponent `taper` mapped to the two profiles | Hollow Mesa **measured here: 340 columns, 2,423 height-blocks per half** (4,846 both halves) for the 20 sites |
| **S10** | **natural arch: `form.arch`** | Deck and underside as curves over a span between two rims (or along a spline), thick at the rims and thin at the crown, ragged edge rows, banded like the cliffs; written as a storey of its own so the ground under it stays the ground. | Hollow Mesa `terrain.py:301-332` (deck `74 + 2 - 2t²`, underside `deck - 4 - 18t²`, t = \|x + 0.5\|/45.78, ragged rows at z -4 and 3); Tamarisk Wash `trials/sonnet/tamarisk-wash/scripts/gen.py:327-349` + `plan.py:339-348` (3-wide deck along a spline, thickness `1 + 5\|2s-1\|²`) | `arch(w, path, width, deck=(crown_y, rim_y, power), thick=(crown, rim, power), ragged=(rows, p, drop), rock=fn, keep_ground=True, seed)` | **new** (`forms.tower` and `forms.skirt` are the nearest, both radial) | Hollow Mesa **5,888 blocks (0.329%)**, 2,478 exposed (ANATOMY). Tamarisk: not counted |
| **S11** | **vertical bore: `under.bore`** | A cylinder (ragged radius) cut from a floor up or down through rock, optionally to the void, plus a small well lined at the top: the leak path of a core. `under.shaft` lines and ladders; this lines nothing. | Hollow Mesa `underground.py:59-67` (r 3.2 at (-65, -24), y 0-47, radius noise 0.25) and `:70-90` (2×2 well 47-73, 12-block clay ring); wells as ringed shafts: Tamarisk `desert.py:106-150` (`well_house`, `open_well_foot`), Riftwater port `works.py:342-350`, Abbeymoor `dress.py:359-373` (a surface prop only) | `bore(w, at, r, y0, y1, r_noise=0.0, seed=0, fill=AIR, lip=None)`; `lip=(y, ring_box, block)`; assertion hook `leaks_to(y)` | **new**; relates to `under.shaft` (`under.py:226`) | the hole: ~40 blocks of rock deep (ANATOMY step 7), about 1,500 air blocks carved (π·3.2²·47, **estimated**, not counted in a world); the well and lip 152 blocks |
| **S12** | **waterfall off the island edge: `landform.waterfall`** | Falling water (`WATER_FLOW:8`) from a stream's last wet column over the lip, down the rift face to the void (y 8), only into air. | Riftwater port `ground.py:70-84`; (sa) Hollow Mesa `terrain.py:285-298`, Riftwater `terrain.py:290-306`, Cloudhaven `terrain.py:121-148`; shelf falls `sunwell/scripts/gen.py:160-172`, `copperline/scripts/gen.py:297-306` | `waterfall(w, wet, surface, edge="x>=-14", to_y=8, only_into="air")` taking the `Water` of `watercourse` (its `falls` already lists stepped drops, `landform.py:81`) | **new**; `audit.loose_water` already allows exactly this (`audit.py:70`, test `tests/test_pgmvox.py:235`) | Riftwater **754 blocks (0.075%)**, 377 per half at x -11..-10, z -3..3, y 8..45; Hollow Mesa **96 (0.005%)** |
| **S13** | **crop field with ditches: `props.crop_field`** | A rectangle (or rotated plot) levelled to a plane with a tilt, farmland in strips of crop kinds with mixed ripeness, a water ditch every nth row, grass edge, fence with a gate, a scarecrow. | Riftwater port `ports/riftwater/scripts/dress.py:71-99`; (sa) Riftwater `dressing.py:172,401`, Lantern Pass `gen.py:147` (rotated plot, ditch `abs(v % 4 - 2) < 0.5`); Cinder Reach `gen.py:316-324` (small plot, no ditch) | `crop_field(w, box, plane=("median", tilt_z), strips=(width, crops), ripe=(block, p, ages), ditch=(every, offset), fence=..., gate_at=..., scarecrow=..., heading=0)` | **new** | Riftwater **3,856 blocks (0.385%)**, 1,050 exposed, 486 carved |
| **S14** | **slab island: `terrain.slab`** | A floating floor per height: rock beds laid for the floor, root hung by `root_depth` capped by the floor, a bedrock foundation course, moss/ice on the rim. | Slatefold `gen.py:49-74`; Lantern Karst `gen.py:38-59`; Hoarfrost `gen.py:51-80` | `slab(w, floor, land, beds, root=dict, foundation=3, rim=(block, p, depth))` | **new**, a loop over `lay` + `underside` + `forms.skirt` | not in the two analyses |

**S0: three primitives the rows lean on** (small, shared, tested first):

| # | primitive | evidence | parameters |
|---|---|---|---|
| S0a | `noise.line(n, cell, octaves=2, seed=0, amp=1.0, base=0.0)`: the 1-D wandering offset, `fbm((n,), cell, 2, seed)` broadcast along an axis | Riftwater `plan.py:171-172,191-193,231,234`; Cinder Reach `plan.py:100-101,135`; Redwash `plan.py:104-105,129`; (sa) Hollow Mesa `terrain.py:91-93,117,163-165`, Riftwater `terrain.py:58-65,114,117` (21 uses in 5 files) | |
| S0b | `Symmetry.field(a)` / `sym(a)`: a float field made, or completed, under the board's symmetry | R7 (`land.py:36-45`, `cinderfall plan.py:137-143`, `common.py:34-43`) | |
| S0c | `shapes.nearest_on(pts, x, z) -> (distance, arc)` and `shapes.scatter_points(zone, n, min_d, rng, taken)` | D3 (`_arc_of` ×3), R1 (`scatter_points` ×5, `needle_sites` `terrain.py:61-82`) | |

### 4.3 Boards per shape, and the order of work

The order is not a pure count. It weighs, in this order: how many boards carry the shape as copied glue, the largest block figure the analyses give, whether it is independent of the others, and whether it deletes code or only adds it. S0a/S0b/S0c come first because five rows lean on them.

| order | shape | pgmvox boards (local copies) | standalone (sa) | largest measured blocks | depends on | why here |
|---:|---|---:|---:|---|---|---|
| 0 | S0a-c primitives | 3 / 3 / 7 (the 1-D line / the symmetric field / nearest-on-polyline and scatter) | 2 / 0 / 1 | n/a | none | tiny, shared by S1, S2, S3, S5, S8, S9 |
| 1 | **S4 `lay` finishing (a, b, c)** | 6 (S4c: 9 sites) | 2 | 455,476 laid then cleared; 9,528 local | none | six hand-written passes of 26-56 lines; independent; deletes the most board code |
| 2 | **S2 island outline** | 5 | 3 | decides the whole stack | S0a | 5 copies of one idiom; `_ragged` twice verbatim |
| 3 | **S3 field terms** | 8 (smoothstep) | 5 | 918,000 hang on them | S0a | the widest reach; the numbers stay the board's, so it is a vehicle, not a recipe |
| 4 | **S1 `landform.profile`** | 2 | 1 | 598,159 of 718,000 height-blocks; 1,742,764 stand on it | S0a, S3 | biggest single block count, fewest boards; the analysis's "removes the escape hatch" item 1 |
| 5 | **S5 underside with a sheer side** | 4 (3 identical) | 2 | whole stack | S0a | one formula copied three times |
| 6 | S6 level pad | 5 | 1 | inside 918,000 | none | small, many sites |
| 7 | S7 radial / elliptical | 4 | 1 | 6,047 height-blocks (2 buttes, per half) | S6 | parameters on existing ops plus two new |
| 8 | S8 ridge | 2 | 2 | inside 918,000 | S0a, S3 | |
| 9 | S12 waterfall | 1 | 3 (+2 shelf) | 754 | S4c | small, and a play rule: the leak and `loose_water` |
| 10 | S13 crop field | 2 | 2 | 3,856 | none | props-like |
| 11 | S14 slab island | 3 | 0 | not counted | S4a | a loop over S4a and `underside` |
| 12 | S10 arch | 1 | 1 | 5,888 | none | one board each, but a block count |
| 13 | S9 spire field | 0 (a 5-copy scatter kit) | 1 | 2,423 height-blocks per half (measured here) | S0c | the analysis says 20 `spire` layers do without it |
| 14 | S11 bore | 0 (2 well variants) | 1 | about 1,500 air blocks (estimated) | none | one board, but it is the leak of a core |

### 4.4 Seen in the analyses, deliberately not terrain

Not in the plan above, and why: towers, bridges, mill, headframe, village furniture, false fronts, adobes (the analyses' "templates", 13 for Hollow Mesa; Riftwater ranks tower templates 2,500, village furniture 1,726, bridges 1,650, waterworks 1,146 blocks); the catwalk (178), tram rails (230), the tipple (528, `made`); flora cover (1,288) and the team recolour. They are building and props work. Two of them touch ground and are noted for later: `build.walkway` (reads the carved volume to hang lamps from the roof) and `route.rails` (curve data from neighbours). The Riftwater lake pool (346 blocks, `under.py:41`), pillar hall (122, `under.py:53`) and sinkhole rubble (484) are cave dressing that fit `under.dress_cave` as parameters (a pool, columns, rubble) and are cheap once S7's `crater` exists.

## 5. Cleanup and integration plan

### 5.0 Principles the order follows

1. **No library change without a baseline.** The 22 volume hashes in section 3.2 are the oracle; step 0 freezes them.
2. **Tidy before extend.** Extending `lay`, `root_depth` and `underside` while their behaviour is unpinned (no test names `underside`, `by_angle`, `beds`, `bed_offset`) would mix two kinds of change.
3. **A new op earns its place by replacing a board's own code and producing the same columns.** Each shape below is first proven equal to the formula it replaces (zero differing columns on the real board's grid), then the board moves.
4. **Parameters are decided once, for Python and for the studio's C#** (5.6), because the layer files already exist in three vocabularies.
5. **The library keeps its flat module names.** 22 buildable boards import `from pgmvox import landform as LF` and the like; new ops go into `landform`, `terrain`, `shapes`, `noise`, `under`, `forms`/`props` and one new module, `field` (terms), not into a re-packaged tree.

### 5.1 Step 0: the safety net (before any edit to `pgmvox/`)

| # | do | check |
|---|---|---|
| 0.1 | Extend `check.py` from 4 examples to the 22 buildable boards: run each `gen`, hash `volume.bin`, compare with a checked-in `check/boards.json` (the table in 3.2 is its first content). One pass is about 75 s. | the two-run determinism already measured: 22 of 22 identical |
| 0.2 | Look at the 0.20.0 drift in `islets` and `parts` (section 1.4) and accept it with `check.py --update` in its own commit. | `check.py` green on the four examples |
| 0.3 | Make `lib/` runnable alone: copy the one curio plot the test needs into `tests/fixtures/`; move `trees.json` for the Riftwater port into `ports/riftwater/`; give `pgmvox.run` an `--out` so a run does not write into the board folder. | a bare copy of `lib/` + `tools/sculpt` passes tests and all 22 builds (this inventory's scratch tree is the proof of what was missing) |
| 0.4 | Fix the two ports' read-backs: Riftwater's four monuments to three over the floor (`ports/riftwater/scripts/plan.py` monument boxes; `PORT-REPORT.md` says why), then re-record both ports' `renders/walks.txt` on 0.21.0 and re-read their plan targets. This is the board owners' decision; it is listed because it is the only place the library and a board disagree today. | `objectives with a problem: 0` for Riftwater; walks.txt matches a fresh run |
| 0.5 | Write the missing tests for what steps 1 and 3 will touch: `landform.hold/scarp/stage/blend`, `terrain.by_angle/beds/bed_offset/underside/cloud_deck`, `shapes.*` (0 of 15 named), `route.pave/steps/footprint`, `under.carve/chamber/dress_cave`. Assert the current behaviour (invariants, not copies of the output). | suite passes before and after 1.x |

### 5.2 Step 1: tidy pgmvox (no behaviour change; the 22 hashes must not move)

Order within the step: smallest blast radius first.

| # | do | evidence / call sites | hash check |
|---|---|---|---|
| 1.1 | Delete the dead: `facade.band_from_top`, `facade.stepped_line`, `shapes.centroid`, `pieces.disc`, `pieces.polygon` (after 1.3), `objectives.Portal` (README names portals, so confirm with the owner first), `terrain._slope_cases` moved to `tests/` (D8). | section 1.4; no board references any of them | unchanged |
| 1.2 | Retire the board-local copies of library code: `ports/lantern-karst/scripts/plan_check.py:18` onto `plangraph.graph(bridge=..., rules=PlanRules(diagonals=True))`; delete both `planwalk.py`. Rebuild; `plan-check.txt` and `walks.txt` must read the same to the last digit (the README already claims it, `README.md:151`). | D-notes, section 2.1 | unchanged; walks equal |
| 1.3 | **One rectangle convention.** Corners `(x0, z0, x1, z1)`, inclusive, everywhere new. Move `rect_cells`, `poly_cells`, `disc_cells` into `shapes`; keep `Raster.rect` and `pieces.box` only as documented "ranges" forms, and add a test that no new public function takes `(x0, x1, z0, z1)`. Changing the call sites (up to 71 `.rect(` and 33 `.box(`; the greps also match other classes' `.box(`) is a separate, mechanical commit per board. | D1, D2 | unchanged |
| 1.4 | **One polyline walk.** `shapes.polyline(..., side=True)` returns the side; `landform._side` and the slatefold inline loop use it. Add `shapes.nearest_on(pts, x, z)` (S0c) and replace `_arc_of` ×3 (`riftwater plan.py:418`, `cinderfall plan.py:374`, `tamarisk-wash plan.py:327`). | D3 | unchanged |
| 1.5 | **One edge distance.** `shapes.edge_depth(mask, metric="taxicab")` keeps its default; add `metric="euclid"` (used by S5 later) and use it in `landform.lake` and `blend` through the same function. | D4 | unchanged (default is the old behaviour) |
| 1.6 | `World.top` takes `heightmap()`'s rule once (`world.py:92-107`). | D5 | unchanged |
| 1.7 | Guard `noise.smoothstep` for `e0 == e1` (return a step) and document the reversed-edge convention in its docstring; add the test (D7). | D7 | unchanged |
| 1.8 | Name clashes: do the cheap ones now (`build.windows` → `build.window_rhythm`: 5 boards call it; `facade.steps` → `facade.kilim_steps`: 0 boards), leave `ladder`, `tower`, `house`, `lay`, `storey` and say so in the README's table of names. | D6 | unchanged |
| 1.9 | README and AGENT-GUIDE: the module table gains a "terrain half" subsection listing S1-S14 as they land; fix the capture-board claim of `README.md:151`; regenerate `op-catalog.md` from 0.21.0 and correct the two ops the Hollow Mesa layers list as pgmvox (`under.portal`, `paint.zone`). | section 2.1 | n/a |

### 5.3 Step 2: promote the repeated non-terrain code (R1, R7, R8)

Small, mechanical, and it removes 784 lines of identical files: `props.brazier`, `props.lamps(line, every, side)`, `props.rubble`, `trees.dead_tree`, `forms.masonry_tower` (the `kit.tower`: ladder, door side, crown), `shapes.scatter_points` (S0c), `Symmetry.field` (S0b), and `terrain.paint` helpers `set_paint`, `cell_pick` out of `trials/opus/common.py` (these feed S4b). Then five `kit.py` files become imports; the five sonnet boards' hashes must not move. `door_cell`, `route_via`, `zone_mask` stay in boards until a second reading of their variants (4 and 3 bodies) says which one is right.

### 5.4 Step 3: add the shapes, in the order of 4.3

Each shape is one change with the same five parts: (1) the A/B test written first against the board code it replaces, (2) the op in the module named in 4.2, (3) the contract tests below, (4) one board moved over, (5) the README section and the `vocabulary`-style row. **What a test for a landform asserts** (the existing tests set the pattern: a 120x120 synthetic ground in `Landforms.setUp`, `tests/test_pgmvox.py:193-197`, and properties such as "it once lifted the whole world", `:249`):

| property | how | example |
|---|---|---|
| **it touches what it says and nothing else** | compare with the input outside the influence radius; `only lifts` / `only cuts` / `sets` as declared | `LF.spire` leaves `hypot >= r` untouched (`:249-256`); `profile` leaves columns beyond the last station untouched when `mode="lift"` |
| **landmarks are exact** | heights at named stations equal the stated `y` where no noise is asked for | `profile` floor, bench, plateau equal 41, 57, 74 with `wander=None, jag=None`; `terms` ramp equals `amp` at `to`, `gauss` equals `amp` at `at` |
| **continuity and walkability** | max neighbour step in the result against a stated bound; monotone between stations | no step above `k` between floor and plateau with smoothstep ease; the plan graph from `Raster.from_heights` reaches the bench from the floor |
| **determinism and independence** | same arguments and seed twice give equal arrays; a different seed differs; document grid-shape dependence of `fbm` (D9) and test that a result is stable for the board's own grid | `noise.line` equal across calls |
| **additivity / commutation** | `terms([a, b]) == terms([a]) + terms([b])`; ops declared to commute do | `terms` under disjoint masks |
| **symmetry** | fed a half-turn-symmetric input and a symmetric mask, the output is symmetric | `island`, `terms`, `profile` on the Abbeymoor-style `sym` inputs |
| **volume ops leave a sound world** | `audit.footing(w) == []`, `audit.loose_water(w) == []`, block counts by id, nothing written outside the stated box, `only_air` honoured | `arch`: both ends attached (one connected component with the ground), clearance under the crown at least n; `waterfall`: `loose_water` empty; `fill_water`: water never beside air |
| **equal to the board code it replaces** | run the board's own formula (copied into the test as a fixture) and the op on the board's real grids; assert zero differing columns, or a stated delta | `terms` against Riftwater `plan.land()` base heights (`plan.py:195-207`); `profile` against Hollow Mesa `build_heights` (the standalone's `H` is reproducible: its plain run reproduces the committed world with 0 differing blocks, Hollow Mesa FINDINGS) |
| **the rule the shape implies, where it has one** | a core's bore leaks: the well lies inside the hole, an air column runs from the lip to y 0 | `bore` |

Per shape, the specifics that go beyond the table:

| shape | asserts beyond the general table |
|---|---|
| S4a `lay(bottom=)` | no block below `bottom` in any column; identical to `lay` then clearing (the six boards' loop) on a fixture; time not slower than the clear loop |
| S4b `lay(paint=)` | the first matching layer wins; a layer with `Slope(lo, hi)` fires only in that slope band computed by `slope_deg`; reproduces Riftwater `ground.py:52-62` columns for seed 3 and the Cinderfall pass |
| S4c `fill_water` | no loose water for a river into a lake and a river into a sea (the two existing scenarios, `tests/test_pgmvox.py:218-234`); bed under every wet column |
| S2 `island` | land is one connected component; lip never moves inside `hold` zones; inset within `clip`; box respected; equals `_rift_edge` + inset code on the Riftwater grid |
| S3 `terms` | smoothstep ramps with reversed edges equal `noise.smoothstep`; a mask partitions (sum over masks equals the piece); equals `plan.land()`'s base for the three masks |
| S1 `profile` | each edge lies within its `wander` amplitude of nominal; asymmetric sides honour their own stations; floor climbs along the arc when stations vary (the Wash); equals the standalone's `H` on the red half |
| S5 `root_depth(sheer=)` | the underside under the sheer edge is at least `sheer_depth` where the taper alone would be less; no depth where the mask is false; equal to the three boards' formula for their constants |
| S6 `level` | inside the shape the ground equals `y` (or the median) exactly; beyond `skirt` untouched; `not_in` honoured |
| S7 `mound`/`crater` | peak equals `height` at `at`; `crater` descends one block per block (the Riftwater sinkhole's climbability, `plan.py:299-303`); elliptical `rz`, `angle` equal rotating the input |
| S8 `ridge` | foot within `Wander` of nominal; terraced columns equal the nearest terrace level within `riser` |
| S12 `waterfall` | one `WATER_FLOW:8` column per wet lip column from the lip to `to_y`; only into air; `loose_water` empty |
| S13 `crop_field` | every farmland block has water within 4 blocks (1.8 hydration), crops at a stated age, a gate in the fence |
| S10 `arch` | deck and underside equal the formula at sampled stations; ends attached; the ground below untouched (the audit defect the Hollow Mesa analysis names) |
| S9 `spire_field` | no two spires closer than `r_i + r_j + spacing`; `keep_clear` paths clear; count within `n` |
| S11 `bore` | radius within `r_noise`; open from `y1` to `y0`; every well cell inside the hole's radius |

### 5.5 Step 4: moving the boards over without breaking them

| # | rule |
|---|---|
| 4.1 | **One board per shape first, the board with the most local code for it**: S4 on `ports/riftwater` (`ground.py:24-67`, `falls`), S2 and S5 on `trials/opus/cinder-reach` and `redwash-mesa` (they share the outline and underside text almost line for line), S3 and S1 on the Riftwater port's `plan.land()` (147 lines, `plan.py:178-324`), then the others. |
| 4.2 | **Heightfield first, world second.** Before moving a block-writing pass, compare the new `H`, `water`, `land`, `bottom` arrays with the board's own on the board's grid (zero differing columns); only then rebuild the world and compare hashes. |
| 4.3 | **Equal means a hash, changed means a table.** A move that is meant to change nothing keeps the `volume.bin` sha256. A move that is meant to change something (a fixed defect, a changed default) ships a table with the changed counts by block id and the first coordinates, per the repository's rule that a world finding is a per-item table with positions, and the board's `renders/gen.txt`, `plan-check.txt`, `walks.txt` are re-recorded in the same commit. |
| 4.4 | **Keep the board's seeds.** `fbm` depends on the grid shape (D9), so an op that takes `shape` and `seed` from the board reproduces the board's field; an op that picks its own seed does not. Ops take `seed` as a parameter, never a module stream (`world.rng` names stay the board's). |
| 4.5 | **Hollow Mesa and the other standalone boards are not migrated.** Their terrain code is the measurement; the migration check for S1 is the heightfield equality in 4.2, not a rebuild of the board. |
| 4.6 | **A board leaves behind what the op replaces, and the README row says so** (lines deleted: Riftwater `lay_ground` 44, `falls` 15, `land` up to 147; Overgrowth 26, Cinderfall 56, Tamarisk 45 for S4; `kit.py` ×5 for step 2). |
| 4.7 | **Every run is two runs.** The gate runs `gen` twice in the baseline and compares both hashes, since the determinism it relies on was measured, not assumed. |

### 5.6 What the studio port (C#) wants decided now

The studio's layer files already disagree with each other and with pgmvox (`recipe/vale.recipe.json`, `riftwater.layers.json`, `hollow-mesa.layers.json`, `landform.py` signatures), and the studio's own relief marks use another set (`docs/world-export/relief.md` §2). These are cheap to settle before the first op exists and expensive after.

| # | decide | the conflict, with evidence | proposal |
|---|---|---|---|
| P1 | **Names of places and paths** | pgmvox `centre`, `pts`, `height`; the Vale recipe `at`, `path`/`line`, `rise` (`vale.recipe.json`: `landform.butte` `at`; `scarp` `line`, `rise`; `canyon` `path`); Hollow Mesa layers `along`, `centre`; the studio's marks `r`, `polyline`, `height`. | `at` for a point, `path` for an open polyline, `outline` for a closed one, `top` for an absolute y, `rise` for a relative one, `r`/`rx`/`rz`/`angle` for radii; `seed`, `jag` as today. Rename pgmvox's parameters when the ops in 4.2 are written (new ops first; old ones keep their names until a board is edited). |
| P2 | **Width means full width** | pgmvox `width` is the full width (`watercourse width=6`, `canyon width=20`, `grade width=5`); the studio's marks state `r` as the reach either side, "the band it writes is twice it" (`relief.md` §2). | name the half-width `half` or `r`, never `width`; every op documents which it takes; the C# type carries the same name. |
| P3 | **Units and rounding** | pgmvox heights are floats, rounded by the board (`np.round`, round-half-to-even; `np.floor` for beds and levels, `landform.py:85,87`). `slope_deg` already copies the studio's half-to-even rounding (`terrain.py:44-67`). C# `Math.Round` defaults to the same, `(int)` truncates. | all x/z in block coordinates (a block at its integer, README "Heights" convention), y absolute world y, distances in blocks, slopes in degrees, angles in **radians** in pgmvox today (`shapes.ellipse`) and degrees in the studio: choose degrees for the shared shape and convert at the Python edge. Ops return floats; one rounding step, named, at the end. |
| P4 | **Noise** | pgmvox `fbm` is numpy PCG64 lattices upsampled with `scipy.ndimage.zoom(order=3, mode="reflect")` and sized from `shape` (D9, measured 0.71 difference between grid sizes); the studio's grain is value-noise with other defaults (`STUDIO-2-DESIGN.md` §11: cell 9, 3 octaves). A C# port cannot reproduce pgmvox's bytes without re-implementing both. | the shared contract is *statistical and invariant*, not bitwise: ops take `cell`, `octaves`, `gain`, `seed` explicitly and refuse a finest octave under about 5 blocks on walkable ground (§11); tests compare invariants; Python and C# do not claim equal arrays. Pin one of the two as the reference for a board that must be reproduced. |
| P5 | **What an op does to the ground** | the landform docstring says each op "only cuts or only lifts unless it says otherwise" (`landform.py:11-14`), but `blend`, `stage`, `grade`, `level` replace. | every op declares `mode` ∈ `lift`, `cut`, `set`, `blend`, and the recipe records it (it is what lets a step re-run alone). New ops take `mode=` where more than one is meaningful. |
| P6 | **Order and reads** | the analyses: "Order is meaning" (pads before walls, roads before houses, monuments read the finished ground); Hollow Mesa's `L.H` is regraded as buildings land, 13 sites. | each op declares `reads` (named heightfields/masks) and `writes`; ground edits after a build step are a new step, not a mutation. S10 `arch` writes its own storey. |
| P7 | **Randomness** | module streams consumed in call order (Riftwater: reseeding per op changes 2,004 cells, 0.20%; the original 23,834, 2.37%); `world.seed` is sha256 of `board/name` (`world.py:26-30`), stable across processes. | every stochastic op takes `seed` and draws from its own stream; `rng(board, name)` stays a Python helper that produces `seed`s. |
| P8 | **Symmetry as an input** | exact only if every op is clipped to one half and block data is remapped (Hollow Mesa, Riftwater); `Symmetry.field` (S0b) and `turn_world` do it in Python. | the recipe carries the symmetry once; ops that make fields take `sym` and return the full-board array; the data table for `turn_world` comes from the studio's `BlockGeometry.Turned` (`orient.py`, `data/blocks.json`), already shared. |

### 5.7 Risks and what this inventory did not do

- **The counts are lexical.** "Dead", "unused by any board" and "boards that use X" come from name tokens and the AST; a name used through `getattr` or a string would be missed. The shape tables cite the line of each local implementation, and each was opened.
- **The 20 standalone boards were not run**, and `renders`/`sketch` of no board were. A world finding in this document is the analyses' (cited) or measured on `build_heights` (S7, S9).
- **Bisection is on two ports and one commit pair** (0.10.2 / 0.10.3, plus 0.21.0). The 0.10.3 attribution rests on those two builds; the commit message ("a running jump lands lower") is the only statement of what changed.
- **S11's 1,500 air blocks are an estimate** (cylinder volume), not a count from a world.
- **`brittlebush-iii`'s walk took 157 s of the 180 s allowed**; a faster machine or a slower one changes whether it fits the same budget. The baseline gate in 0.1 does not run walks.
- **No file under `pgmvox/`, `boards/`, `ports/`, `trials/`, the studio or the analyses was edited**; `git status` in `/home/user/pgm-studio-mapgen` was clean before this file was written.

## Appendix A: public functions and classes by module

Generated from the AST of `freeform/lib/pgmvox/*.py` (0.21.0): the line each starts on and the first line of its docstring (`-` where it has none). Private names (leading underscore) are omitted.

**`audit`** (92 lines)

| line | name | one line |
|---:|---|---|
| 33 | `footing` | Every block in the world (or in box = (x0, y0, z0, x1, y1, z1)) that falls or has nothing... |
| 70 | `loose_water` | Every water block with air beside it that does not lie over lower water within `drop`... |

**`blocks`** (263 lines)

| line | name | one line |
|---:|---|---|
| 26 | `class B` | 1.8 block ids. A constant names an id; its data value (wood, colour, facing) goes beside it. |
| 222 | `info` | The studio's row for an id: name, role, shape flags, names and colours per data, turned... |
| 227 | `name` | - |
| 238 | `colour` | (r, g, b) of a block as the studio paints it. |
| 261 | `mask` | A boolean array over an id volume: True where the id is in the class. |

**`brittle`** (650 lines)

| line | name | one line |
|---:|---|---|
| 54 | `class Cell` | - |
| 63 | `turn_cells` | A blueprint turned k quarters clockwise about the middle: cell (cx, cz) -> (-1 - cz, cx), a... |
| 72 | `fan` | A unit drawn once, with its images under quarter turns: ({cell: Cell}, {cell: the image it... |
| 83 | `heights` | Per block column: G, the ground's top (an underfloor's, under a deck), and T, the top (a... |
| 109 | `pieces` | The pieces: flat cells (flat, keep, tower, a stacked piece's deck) joined to their... |
| 135 | `ground` | Under a floor at h: four courses of stone, bedrock to y 3, obsidian at y 1 and 2, block 36... |
| 146 | `tree` | A round birch over the floor at y: a trunk `height` high and a crown of leaves. |
| 159 | `bed` | A bed of grass inside two rings of sandstone stairs, as Brittlebush lays every one: the... |
| 192 | `sand` | A sand field as Brittlebush lays it: sand mixed with upside-down sandstone stairs, whose... |
| 273 | `cap` | A ground edge, top down: an upside-down spruce stair, its full side inward; brick; a... |
| 286 | `sections` | The blueprint's pieces as the grammar's sections, one a piece, its cells' boxes; a keep... |
| 301 | `build` | Every block of the cells in `only` (default all), each read against the whole blueprint, so... |
| 452 | `storey` | One storey of a tiered tower: walls of black clay one in from its plate (x0, z0, x1, z1), a... |
| 490 | `tower` | A tiered tower on the ground at base_y over box (x0, z0, x1, z1): tiers [(height, inset),... |
| 513 | `house` | A building as Brittlebush I raises its wool rooms: storeys of whole cells, five blocks... |
| 636 | `heart` | A heart seven wide and six high in `dye`, outlined and backed in black wool, standing... |

**`build`** (566 lines)

| line | name | one line |
|---:|---|---|
| 42 | `class Frame` | A building's own axes on the board: u along `heading` (degrees from east, toward south), v... |
| 107 | `class RoofField` | A roof as a height field over its plan, as the studio's RoofField answers it. |
| 275 | `lay_roof` | Lay a roof field into the world as the studio's stamper does. |
| 345 | `windows` | The window rhythm every board used: one in every `period` blocks along a wall, clear of its... |
| 355 | `class House` | A house at any heading. L along the ridge, W across; floor is the y of the plate; door is... |
| 377 | `house` | Build one house. ground_at(x, z) gives the ground's height, so the plate is filled down to... |
| 486 | `edge_cells` | The cells of a set with a four-neighbour outside it. |
| 492 | `parapet` | A parapet round the edge of a set of cells at course y, and a crenel on top where rhythm(x,... |
| 502 | `site` | Level the ground under a footprint to floor_y and ease the ground round it back over... |
| 529 | `stairs` | A straight flight of n stairs climbing toward `rises` from (x, y0, z), `width` wide to the... |
| 543 | `ladder` | A ladder from y0 to y1 on the wall at that side of the column. |
| 549 | `class Claims` | What stands where, by layer, so overlaps are listed rather than overwritten unseen. |

**`clay`** (203 lines)

| line | name | one line |
|---:|---|---|
| 44 | `squares` | One axis of the squares across a span of n: 'm' margin, 'g' grout, 'r' a square's ring, 'c'... |
| 61 | `style` | Claywork's blocks for the grammar, in the team's `dye`; `faced(x, z)` says whether a column... |

**`facade`** (376 lines)

| line | name | one line |
|---:|---|---|
| 71 | `band` | A horizontal band from course t0 to t1. |
| 76 | `band_from_top` | - |
| 80 | `courses` | A flush course of another block every so many, as poured concrete shows its pours. |
| 85 | `flutes` | Vertical grooves: `width` of every `period` blocks set back, clear of the face's ends. |
| 94 | `panels` | Whole panels alternately flush and set back, the run divided evenly about its middle. |
| 103 | `slits` | Narrow flush windows, one in every `period`, centred on the run. |
| 113 | `checker` | A field of inset squares: a pattern for a large blank face. |
| 140 | `glyph_row` | Five-by-five glyphs inlaid along the face: as many as fit at `spacing`, centred, cycling... |
| 154 | `word` | A word in the three-by-five letters, centred on the face and read left to right from outside. |
| 159 | `windows` | Flush windows `width` wide, one in every `period`, centred, from course t0 to t1. |
| 169 | `faces` | The face runs of a set of cells: (normal (dx, dz), [cells left to right seen from... |
| 197 | `extrude` | Pour a mass from y0 to y1 over a set of cells and pattern its faces. base is a block or a... |
| 229 | `top_course` | A cornice thrown out a block all round, a slab thick; or a parapet a block high, slotted... |
| 246 | `coffer` | The underside cut into recesses `size` square on a grid of `period`, a light at the heart... |
| 261 | `concrete` | Board-formed concrete: a course of a darker block every `every`. |
| 268 | `class Cell` | - |
| 280 | `border` | The outer `width` rows; or, with at, only the ring `at` blocks in. |
| 287 | `medallion` | A diamond medallion: where /u//hw + /v//hh lies between r0 and r1. |
| 292 | `corners` | Quarter medallions in the four corners, `inset` in from each side. |
| 297 | `diamonds` | A chain of diamonds down the middle, one every `period` blocks along x or z. |
| 305 | `steps` | Kilim bands across the rectangle, stepped: bands `width` wide in turn through `blocks`. |
| 313 | `stepped_line` | The kilim's zigzag: a line stepping across every other band. |
| 322 | `star` | An eight-pointed star in the middle: 0.7 of the larger offset and 0.3 of the smaller under r. |
| 327 | `stripes` | - |
| 331 | `tiles` | A checker of two blocks, `size` square. |
| 336 | `cross` | Two bands crossing at the middle, the garden carpet's water. |
| 341 | `first_of` | The first field that answers; `default` where none does. |
| 352 | `carpet` | Lay a floor field over a rectangle at course y. Returns the blocks laid by kind, for a legend. |
| 366 | `rect_cells` | - |
| 370 | `poly_cells` | - |

**`forms`** (130 lines)

| line | name | one line |
|---:|---|---|
| 29 | `tower` | A tower from y0 to top round (cx, cz), radius r at its foot. rock(y, b) gives the block at... |
| 77 | `skirt` | Karst faces under the rim of floating floors (land: a world-grid mask; floor: each column's... |
| 111 | `root_vines` | Vines hanging from the lower part of floating roots: on each side of a land column, with... |

**`grammar`** (321 lines)

| line | name | one line |
|---:|---|---|
| 40 | `class Section` | A piece of surface at one height: boxes (x0, z0, x1, z1) inclusive, in blocks. `fill` names... |
| 90 | `split` | A box cut into nx by nz sections as near equal as the blocks allow, named name-i-j. |
| 97 | `tile` | A box cut into squares `module` a side, counted from its low corner; the last row and... |
| 107 | `class Ground` | Every column's top, the section it belongs to and its depth in that section. `tops` adds... |
| 149 | `spec` | A course: (id, data), or a function of the face's inward side giving one. |
| 155 | `class Sunk` | A course set back one block: air at the face, `back` (a course) behind it, an inset. |
| 161 | `class Accent` | A bay laid instead of the plain courses every `every` bays of `module` along a face,... |
| 179 | `class Face` | The courses of a face, top down from the rim at the surface. `floor` is the lowest y a... |
| 228 | `class Lot` | A section's inside as a fill sees it: its columns from depth 1, their box, its surface, the... |
| 259 | `class Style` | The blocks a grammar is spoken in. `body(w, x, z, h)` lays what is under a surface; `faces`... |
| 281 | `lay` | Lay the sections of `ground` numbered in `only` (default all) in `style`: the body under... |

**`landform`** (314 lines)

| line | name | one line |
|---:|---|---|
| 28 | `class Water` | Where a landform holds water: the cells and the surface y over each (the top water block). |
| 63 | `watercourse` | A river along a path, flowing from its first point to its last: a bed that never climbs,... |
| 102 | `lake` | A lake: an outline r across (rz the other way) about centre, broken by `jag`, holding water... |
| 122 | `hold` | Raise every dry cell beside water to that water's surface, so nothing laid after a river or... |
| 135 | `canyon` | A canyon along a path: a floor `floor` of the width across and `depth` under the ground it... |
| 164 | `spire` | A spire: rising from the ground at radius r to `top` at its centre, its sides falling as |
| 174 | `butte` | A butte or a mesa: a flat top at `top` out to radius r, a cliff `cliff` blocks wide, and a... |
| 202 | `scarp` | A scarp: the ground on `side` of a path (+1 right walking along it, -1 left) lifted... |
| 215 | `terraces` | Ground cut into terraces `step` blocks apart inside mask: each column held to the terrace... |
| 226 | `stage` | A stepped stage: rings [(radius, y)] from the outside in, each a level disc at y, the next... |
| 237 | `grade` | A route graded into the ground: the ground along the path smoothed so it climbs or falls no... |
| 288 | `coast` | Land meeting the sea at an outline (a polygon), or at the world's edge when none is given:... |
| 308 | `blend` | One terrain inside mask and another outside, eased together over `width` blocks inside the... |

**`mapxml`** (201 lines)

| line | name | one line |
|---:|---|---|
| 24 | `E` | - |
| 47 | `point` | - |
| 51 | `cuboid` | A cuboid from block-corner min to max (max exclusive, as PGM reads a cuboid's bounds). |
| 56 | `cylinder` | - |
| 60 | `circle` | - |
| 64 | `below` | - |
| 68 | `negative` | - |
| 72 | `union` | - |
| 76 | `item` | A kit's item: item("bow", 1, enchant=[("infinity", 1)], unbreakable=True); tag "helmet",... |
| 84 | `duration` | PGM's duration text: 90 -> "1m30s". |
| 90 | `class Doc` | - |

**`move`** (151 lines)

| line | name | one line |
|---:|---|---|
| 34 | `fly` | A flight from position p = (x, y, z) with velocity v = (vx, vy, vz), no input. |
| 56 | `land_at` | A land() for flat ground at height y_floor (the top of the floor block): stops when the... |
| 66 | `fall` | Ticks to fall dy blocks after leaving an edge the given way, and how far out from the edge... |
| 82 | `fall_damage` | Health points (half-hearts) lost to a drop of dy blocks: none up to three, one a block after. |
| 90 | `jump_reach` | The horizontal distance a jump carries before the feet come back down to `rise` blocks over... |
| 108 | `knockback` | How far a hit carries a player standing on footing of slipperiness `slip`: 1.8 sets the... |
| 130 | `solve_launch` | Search pad velocities for one that lands nearest the target (x, z): start is (x, y, z),... |

**`noise`** (56 lines)

| line | name | one line |
|---:|---|---|
| 12 | `lattice` | One octave: a random lattice every `cell` blocks, cubic-upsampled to `shape`, values in... |
| 22 | `fbm` | - |
| 34 | `ridged` | Ridges: 1 - /fbm/, raised to `sharpness`; mountains are crests where it is near 1. |
| 39 | `smoothstep` | - |
| 44 | `spline` | Centripetal-ish Catmull-Rom through pts, sampled about every `step` blocks. |

**`objectives`** (652 lines)

| line | name | one line |
|---:|---|---|
| 39 | `class Box` | Inclusive blocks: Box(0, 10, 0, 3, 12, 3) is four by three by four. |
| 78 | `turn_point` | - |
| 83 | `turn_yaw` | A yaw (0 south, 90 west) carried through a symmetry. |
| 92 | `centre_el` | A point element at a block's centre, where a player stands in it. |
| 105 | `class Teams` | The teams, as (id, name, colour) or (id, name, colour, max players; 8 if not given). Two... |
| 138 | `class Objective` | - |
| 175 | `class Spawn` | A team's spawn: the block their feet stand in, the way they face, a kit, and the area kept... |
| 222 | `class Observer` | Where observers and the dead appear: <default> in <spawns>. |
| 232 | `class Hill` | A control point (King of the Hill): a pad one course thick and the box over it a player... |
| 281 | `class Flag` | A flag and its posts (CTF, King of the Flag): each post a block the flag stands in, named,... |
| 315 | `class Wool` | A wool to capture (CTW). `team` is the team that captures it, so it is the other team that... |
| 397 | `wool_rooms` | Each keeping team's rooms in one region, and their blocks kept from the other team except... |
| 419 | `float_problems` | The author's rule: a monument or core never stands on the floor; it floats, `least` blocks... |
| 439 | `class Destroyable` | A monument to break (DTM): a box of its material, owned by the team defending it. `heart`... |
| 486 | `class Core` | A core to leak (DTC): an obsidian shell round lava, owned by the team defending it. |
| 524 | `class ScoreBox` | A box that scores for `team` when one of them walks in, and sends them home through a portal. |
| 558 | `class Portal` | A portal from a box to a block a player lands standing in, facing yaw, for those `filter`... |
| 588 | `class Objectives` | - |

**`orient`** (269 lines)

| line | name | one line |
|---:|---|---|
| 35 | `vec` | A direction as a unit (dx, dz): accepts "e"/"w"/"s"/"n" or an offset. |
| 45 | `opposite` | - |
| 51 | `stair` | Stairs climbing toward a side: walking that way you go up. |
| 56 | `ladder` | A ladder (or wall sign, wall banner) hung on the wall at that side of it. |
| 64 | `torch` | A torch on the wall at that side, or standing (None). |
| 71 | `log_axis` | A log lying along x or z ("e"/"w" or "n"/"s"), or upright (None). |
| 78 | `slab` | - |
| 82 | `door` | A door's two halves: the lower carries the facing (the way it looks when shut), the upper... |
| 89 | `yaw` | Minecraft yaw for a player looking that way: 0 south, 90 west, 180 north, -90 east. |
| 95 | `rotation16` | A sign post's or standing banner's 0-15 rotation for facing that way (0 south, 4 west). |
| 197 | `data_table` | A (256, 16) table: the data each (id, data) takes under the operation. |
| 210 | `turn_data` | - |
| 216 | `turn_xz` | Where a block lands under the operation, about the axis (cx, cz): the half-integer -0.5 is... |
| 224 | `turn_world` | Copy the part of the world where keep(x, z) is True onto its image under the operation,... |

**`pieces`** (204 lines)

| line | name | one line |
|---:|---|---|
| 36 | `box` | The cells of a rectangle, inclusive. |
| 42 | `disc` | The cells whose centres lie within r of (cx, cz) (block-centre convention: block x's centre... |
| 49 | `polygon` | - |
| 55 | `class Piece` | - |
| 73 | `class Course` | - |
| 161 | `gap` | The clear distance over the void between two pieces, edge to edge (0 if they touch), with... |
| 172 | `lands_at` | The cell a player comes down in, leaving take_off's edge toward landing the given way: the... |
| 187 | `clears` | The gentlest way across a gap of g blocks onto a piece `drop` blocks lower (negative:... |

**`plan`** (174 lines)

| line | name | one line |
|---:|---|---|
| 23 | `class Symmetry` | How a board's parts relate: "half" (a half turn), "mirror_x" or "mirror_z" for two teams,... |
| 51 | `class Raster` | - |

**`plangraph`** (281 lines)

| line | name | one line |
|---:|---|---|
| 30 | `class PlanRules` | - |
| 39 | `jumps` | Every jump the raster allows, in any direction: from a walkable cell to another whose... |
| 84 | `node` | A cell's node: (x, z) on the ground storey, (x, z, n) on storey n. |
| 90 | `walkable` | Per storey, the cells a player can stand on: a walkable kind with two blocks of air over... |
| 104 | `graph` | Edges {node: [(node, cost, tag)]} over the raster and its storeys. A step to a neighbouring... |
| 182 | `measure` | The cheapest of a set of target cells, and how its cost divides by the kind of move: (cost, |
| 199 | `dijkstra` | Cheapest cost to every node from any of the starts, and the move that reached it. |
| 219 | `route` | The cheapest of a set of target cells: (cost, [the moves other than plain walking, in... |
| 234 | `path` | The cells of the route to `cell`, start first. |
| 242 | `arrivals` | For every team and every named target, the cheapest cost from the team's spawns: {target:... |
| 255 | `pad_edges` | Edges for launch pads: pads = [(name, [(x, z)...], y, (vx, vy, vz))], y the pad's floor.... |

**`plot`** (115 lines)

| line | name | one line |
|---:|---|---|
| 25 | `class OutOfPlot` | - |
| 29 | `class Canvas` | - |
| 59 | `load` | Load a plot module. Plots written against a board's own mc.py (`from mc import B`) load... |
| 73 | `draw` | Hand the plot its ground layer and run its build; returns the canvas, whose errors say what... |
| 87 | `check_alone` | Build a plot alone with `margin` blocks of street round it and walk it from the street: the... |
| 109 | `verdict` | - |

**`props`** (159 lines)

| line | name | one line |
|---:|---|---|
| 19 | `stall` | A market stall three by three on the floor at y, its counter on the side it faces: fence... |
| 49 | `stalls` | A row of stalls along a line of cells [(x, z), ...] on a floor at y, one every `every`... |
| 58 | `lamp` | A lamp post on the floor at y: a post `height` high, a light on it and a slab cap. Returns... |
| 105 | `wool_chests` | The studio's wool-room loot: two chests stacked in each inner corner of the room whose... |
| 122 | `studio_defence` | The studio's defence chest (its DefenseChest stamper), slot by slot: dark-oak planks in... |
| 133 | `defence_chests` | The studio's defence chests set into a wall: a chest at each (x, z) of the wall's face at... |
| 144 | `laid` | The items of a chest drawn as rows of letters: (rows, legend) -> [(slot, id, count,... |

**`render`** (198 lines)

| line | name | one line |
|---:|---|---|
| 21 | `xray_shell` | Keep only what lines a roofed void — a cave, a gallery, a cellar — and what stands in one. |
| 43 | `iso` | Every exposed block a small cube in the studio's colour, seen from a corner, cropped to box |
| 121 | `elevation` | An orthographic elevation of a box: the first block met looking `look` (north/south/east/west), |
| 151 | `cutaway` | A true-scale section along a polyline of (x, z) points: every block the line's vertical... |
| 190 | `trim` | Cut the empty sky round a render. |

**`route`** (278 lines)

| line | name | one line |
|---:|---|---|
| 45 | `find` | The cheapest route from start to goal (world (x, z)), or to the nearest cell of `goals` (a... |
| 155 | `simplify` | Fewer points on the same line (Ramer-Douglas-Peucker): a route's cells to the bends that... |
| 170 | `smooth` | Corners cut (Chaikin), so a switchback turns in an arc rather than a point; the ends stay... |
| 185 | `network` | Join named places, (x, z) each, with roads: the first is the root, then each place in... |
| 212 | `footprint` | The columns a route of this width covers: what a later route's grading keeps off. |
| 218 | `grades` | The grade of every leg of a route over the ground as it stands, end to end: rise over run,... |
| 228 | `pave` | Lay a route's surface: every column within width / 2 of the line takes a block from... |
| 259 | `steps` | A footpath's steps: walking the line cell by cell, wherever the ground rises a block at... |

**`run`** (102 lines)

| line | name | one line |
|---:|---|---|
| 29 | `run` | - |
| 89 | `main` | - |

**`shapes`** (142 lines)

| line | name | one line |
|---:|---|---|
| 10 | `inside` | True where the block (x, z) lies inside the polygon. |
| 25 | `seg_distance` | Distance from every (X, Z) to the segment a-b, and the parameter t of the nearest point on it. |
| 34 | `edge_distance` | Distance to the polygon's boundary. |
| 43 | `signed_distance` | Negative inside, positive outside, in blocks. |
| 49 | `polyline` | Distance to a polyline and the arc length along it of the nearest point. |
| 64 | `length` | - |
| 68 | `point_at` | The point and the unit heading at arc length s along a polyline. |
| 79 | `walk_cells` | The four-connected cells along a polyline, in order, each once. |
| 95 | `centroid` | - |
| 100 | `disc` | - |
| 104 | `ring` | - |
| 109 | `ellipse` | An ellipse, its x radius turned `angle` radians from east toward south. |
| 117 | `stroke` | A tapered stroke from a to b, w0 wide at a and w1 at b, its far end rounded. |
| 128 | `boundary` | The cells of a mask with a neighbour outside it (four neighbours, or eight). |
| 137 | `edge_depth` | For every cell of a mask, how many steps it lies inside its edge (0 on the edge, -1... |

**`sight`** (84 lines)

| line | name | one line |
|---:|---|---|
| 22 | `line_clear` | - |
| 38 | `plan_opaque` | A raster is solid up to each column's floor block; roofs (x, z) -> (y0, y1) adds a solid... |
| 53 | `voxel_opaque` | - |
| 64 | `eye` | The eye of a player standing in cell (x, z) with feet at y_feet. |
| 69 | `target` | - |
| 73 | `visibility` | For every target point, the share of eye points that see it. |
| 82 | `hidden` | The targets no eye sees (stops at the first eye that does). |

**`sketch`** (547 lines)

| line | name | one line |
|---:|---|---|
| 46 | `font` | - |
| 52 | `pale` | A colour washed toward white: the mirrored half of a symmetric board. |
| 57 | `dark` | - |
| 86 | `class Panel` | - |
| 96 | `class MapPanel` | A panel over world x, z: one block is `scale` pixels. |
| 373 | `class SectionPanel` | A cut in elevation, true scale: s runs along the cut (blocks), y up; one block is `scale`... |
| 474 | `class TablePanel` | Measurements against their targets: rows of (value, what, target, ok); ok None for a plain... |
| 497 | `class Sheet` | - |

**`solid`** (67 lines)

| line | name | one line |
|---:|---|---|
| 30 | `fill` | Write a solid into a World. block is (id, data) or a function (x, y, z) -> (id, data) or... |
| 45 | `image` | The solid carried through a plan Symmetry ("half", "mirror_x", "mirror_z" about its axis),... |
| 58 | `turned` | The solid turned about the vertical through (cx, cz), any angle: `rotate_y` under the... |
| 63 | `count` | - |

**`studioplan`** (107 lines)

| line | name | one line |
|---:|---|---|
| 31 | `load` | - |
| 41 | `unit` | The one team's part as a blueprint: {(cx, cz): Cell}. `under` names the cells of stacked... |
| 81 | `placement` | The plan's spawns, wools, iron ... of one kind: [((x, y, z) where it stands, (x0, z0, x1,... |
| 101 | `facing` | A placement's facing as a side, n e s w, where the planner names one. |

**`terrain`** (294 lines)

| line | name | one line |
|---:|---|---|
| 21 | `mountain_ring` | Heights of a ring of mountains: nothing inside `clear` blocks of the centre, rising over... |
| 44 | `slope_deg` | Each column's slope in whole degrees from level, 0 to 89, as the studio's SurfaceGradient... |
| 87 | `by_angle` | A paint rule from slope stops: [(max_degrees, (id, data)), ...] in rising order; the last... |
| 98 | `banded` | A column fill in horizontal bands: choices is a list of (id, data) repeated every `period`... |
| 107 | `class Strata` | A sequence of rock beds by height, drawn from weighted choices: each (block, weight,... |
| 141 | `bed_offset` | How far the beds are lifted at each column: a planar dip (blocks of lift per block east and... |
| 152 | `beds` | A column fill for lay(bands=...): the strata at each height, shifted by the column's... |
| 174 | `ledge_angle` | The slope a paint should read: a cell exactly level with three or more of its four... |
| 186 | `soil_depth` | How deep the soil lies on ground of each slope: `soil` is ((up to degrees, depth), ...) in... |
| 195 | `lay` | Columns of ground up to H (world heights): rock, then soil of `under`, then the top block,... |
| 236 | `root_depth` | How far a floating island's underside hangs under each column: a cone deeper inland (cone *... |
| 255 | `underside` | Hang a tapering underside below a floating floor: under every column of mask (a (sx, sz)... |
| 276 | `cloud_deck` | A deck of cloud at height y: billows rising out of it, breaks where the sky below shows.... |

**`trees`** (152 lines)

| line | name | one line |
|---:|---|---|
| 39 | `class Tree` | - |
| 55 | `library` | The studio's copied trees, {name: Tree}, from its Library/trees.json (path overrides where). |
| 68 | `load` | A board's own cut, {kind: [{"blocks": [...]}, ...]}, as {name: Tree} named kind-1, kind-2, ... |
| 76 | `kinds` | {kind: [Tree, ...]} in name order. |
| 84 | `turned` | The tree's blocks after `turn` quarter turns clockwise seen from above (x, z) -> (-z, x). |
| 95 | `plant` | Plant `tree` with its foot at (x, z), turned `turn` quarter turns. allowed(x, z) may refuse... |
| 127 | `scatter` | Plant a wood over zone (a mask over the world's columns): up to `tries` shuffled cells,... |

**`under`** (246 lines)

| line | name | one line |
|---:|---|---|
| 47 | `carve` | Air in every (x, y, z) of `cells` at or over floor(x, z), never within `cover` blocks of... |
| 78 | `tunnel` | A cave passage through waypoints (x, floor_y, z, radius): a tube whose axis runs `lift` of... |
| 90 | `chamber` | A hall: an ellipsoid rx across (rz the other way), h high, its floor level at floor_y. |
| 96 | `dress_cave` | Finish every cave inside box (x0, x1, z0, z1, y0, y1): floors of gravel, andesite, clay and... |
| 150 | `gallery_line` | A mine's cells through waypoints (x, y, z): one a block in plan, the floor (y, the lowest... |
| 168 | `gallery` | A mine gallery along a gallery_line: three wide and three high, a rough floor, a timber set... |
| 226 | `shaft` | A shaft from the floor at `bottom` up to `top`: a three-by-three well, logs at its corners,... |

**`walk`** (201 lines)

| line | name | one line |
|---:|---|---|
| 31 | `class MoveRules` | - |
| 44 | `classes` | passable, water, climbable and solid masks over an id volume; with doors, a wooden door or... |
| 53 | `standing` | A cell a player can occupy: two passable cells high, with solid ground or water under or in it. |
| 66 | `walk` | Moves to every standing place from the starts (world (x, y, z) of the feet), -1 where... |
| 154 | `nearest` | Moves to the nearest reached place within r blocks (and one up or down) of (x, y, z), or None. |
| 167 | `unreached` | The (x, y, z) feet positions of a list nobody reaches. |
| 172 | `no_stand_above` | Columns inside a region (a boolean (sx, sz) mask, or a function (X, Z) -> mask) with... |
| 186 | `catchers` | Blocks beside a course that a player falling off its edges could land on: anything solid in... |
| 198 | `gap_cleared` | Whether a running sprint jump clears a gap of `gap` blocks landing `rise` higher (the... |

**`world`** (190 lines)

| line | name | one line |
|---:|---|---|
| 26 | `seed` | A reproducible seed for one named random stream of one board, distinct from every other... |
| 33 | `rng` | - |
| 37 | `class World` | A box of the world: x in [x0, x0+sx), y in [0, sy), z in [z0, z0+sz). |
| 174 | `studio_root` | Where the studio is checked out: PGM_STUDIO_ROOT, else the sibling of this repository. |
| 182 | `write` | Write region files and level.dat from a saved build, through the studio's own Anvil writer. |

## Appendix B: reproducing the readings

All paths below are scratch; nothing is written under the repository.

```
mkdir -p /tmp/pgmvox-inventory/repo/freeform /tmp/pgmvox-inventory/repo/tools
cp -r freeform/lib   /tmp/pgmvox-inventory/repo/freeform/lib
cp -r tools/sculpt   /tmp/pgmvox-inventory/repo/tools/sculpt
cp -r freeform/opus55-freeform-curio/plots     /tmp/pgmvox-inventory/repo/freeform/opus55-freeform-curio/    # tests
cp    freeform/opus55-freeform-riftwater/scripts/trees.json  /tmp/pgmvox-inventory/repo/freeform/opus55-freeform-riftwater/scripts/
export PGM_STUDIO_ROOT=/home/user/pgm-studio PYTHONPATH=/tmp/pgmvox-inventory/repo/freeform/lib
cd /tmp/pgmvox-inventory/repo/freeform/lib
python3 -m unittest discover -s tests                      # 95 tests, OK
python3 check.py                                           # islets, parts fail (stale snapshot)
python3 -m pgmvox.run <board> --build /tmp/pgmvox-inventory/build/<slug> --only gen --skip write
python3 -m pgmvox.run <board> --build /tmp/pgmvox-inventory/build/<slug> --only walk --skip write
sha256sum /tmp/pgmvox-inventory/build/<slug>/volume.bin    # the baseline hash in 3.2
```

Archived trees for the bisection: `git archive <commit> freeform/lib | tar -x -C /tmp/pgmvox-inventory/at-<commit>` for `0dc77e82` (0.10.2) and `a501480d` (0.10.3), with the Riftwater `trees.json` beside them, then the same `pgmvox.run` calls on `ports/lantern-karst` and `ports/riftwater`. Logs: `/tmp/pgmvox-inventory/logs/`, per-step results `/tmp/pgmvox-inventory/results*.tsv`.

Measurements made on the standalone Hollow Mesa terrain (scratch copy `/tmp/pgmvox-inventory/hm/`): `build_heights` with and without `spires` (340 columns, 2,423 height-blocks changed on the red half, 20 sites) and without `butte` (671 columns, 6,047). `fbm` of the standalone `noise.py` against pgmvox's for three shapes: maximum difference 0.0; `fbm` seed 5 on 100x100 against 120x100: 0.7116 on the common corner.
