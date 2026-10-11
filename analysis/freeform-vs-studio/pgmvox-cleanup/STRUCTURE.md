# pgmvox structure review

Read-only review of `freeform/lib/pgmvox/` (version 0.24.0, 9,426 lines in 34 modules plus `__init__`). Nothing in the repository was modified. Counts are lexical (Python AST over every `.py` under `freeform/` except `lib/pgmvox/` and `lib/tests/`: 497 files scanned, 156 import pgmvox). The throwaway analysis scripts live in the scratchpad, not the repository.

**How to read the counts.** `ext` is *call sites / distinct board folders*, where a board folder is one directory under `lib/boards`, `lib/examples`, `lib/ports`, `lib/trials/*/*`, plus `lib/check.py`. A reference is any use of the name through an import (`from pgmvox.m import f`, `from pgmvox import m as M` then `M.f`, `import pgmvox.m`). The ten trial boards are near-copies of one template, so many counts are inflated by up to 10x; the "boards" figure is the honest one. `t` is references in `tests/test_pgmvox.py`. Methods called on instances (`world.fill`, `sheet.map`) are not counted: a class is judged by its own name only.

**Caveats that change a verdict.** `document.py` dispatches facade pattern names by `getattr(FA, name)` (document.py:443), so `facade.panels/slits/checker/kilim_steps/rings` are reachable from a layer document (flag `DOC`). `document.py` itself has zero board callers (tests only), and every name flagged `INT:doc` is used only by it. The `opus55-freeform-*` finished boards are not scanned for hashes and only `lantern-karst` imports pgmvox (`props`); five more files under `analysis/freeform-vs-studio/pages/riftwater-layers/make/` outside `freeform/` also import `landform`, `noise`, `orient`, `blocks`, `props`, `terrain`, `shapes` (a migration must change those too).

There is no `kit` module in pgmvox (no `kit.py` exists anywhere under `freeform/` now); kit items are `mapxml.item` and `mapxml.Doc`.

An earlier read-only inventory of 0.21.0 sits at `analysis/freeform-vs-studio/pgmvox-cleanup/INVENTORY.md`; this document is written independently from the 0.24.0 code.

Flags in the `ext` column when zero: `DEAD` no caller of any kind (board, test, library); `TEST` only tests; `INT` only other pgmvox modules or itself; `INT:doc` only `document.py`; `DOC` reachable by name from `document.py`.

---

## 1. Inventory (module by module)

Module sizes at a glance (lines): objectives 695, brittle 657, document 655, build 633, sketch 548, landform 481, terrain 403, facade 362, route 352, grammar 322, plangraph 282, forms 275, orient 270, blocks 264, props 258, under 256, shapes 214, plan 213, clay 204, mapxml 202, walk 202, render 199, pieces 194, world 193, trees 175, move 152, run 148, plot 116, studioplan 108, audit 93, sight 85, field 84, noise 82, solid 68.

### `blocks.py` — 264 lines

Imports (pgmvox): none. Subject today: Block ids, block classes and colours: one table for every freeform board.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `B` | 26 | 1.8 block ids by name | 1996/23 | 269 |  |
| const `DOORS` | 207 | set of door ids | 10/8 | 1 |  |
| const `FENCES` | 208 | set of fence ids | 1/1 |  |  |
| const `FENCE_GATES` | 209 | set of fence-gate ids | 0 |  |  |
| const `TABLE` | 219 | per-id studio row table (json) | 0 | 1 |  |
| `info` | 222 | The studio's row for an id: name, role, shape flags, names a | 0 |  | DEAD |
| `name` | 227 | display name of a block id | 24/1 | 1 |  |
| const `COLOURS` | 235 | colour per (id, data) as the studio paints it | 5/5 | 1 |  |
| `colour` | 238 | (r, g, b) of a block as the studio paints it | 0 | 1 | TEST |
| const `CLIMBABLE` | 245 | id class | 0 |  |  |
| const `PASSABLE` | 248 | id class | 0 | 2 |  |
| const `NOT_GROUND` | 254 | id class | 0 |  |  |
| const `SIGHT_CLEAR` | 255 | id class | 0 | 3 |  |
| const `GRAVITY` | 257 | id class | 0 |  |  |
| const `FORBIDDEN_IN_PLAY` | 258 | id class | 0 |  |  |
| `mask` | 261 | A boolean array over an id volume: True where the id is in t | 0 |  | INT |

### `orient.py` — 270 lines

Imports (pgmvox): `blocks`. Subject today: Which way a block faces, and what its data becomes when a board is mirrored or turned.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `DIRS` | 24 | e/w/s/n to (dx, dz) | 1/1 |  |  |
| const `NAMES` | 25 | (dx, dz) to e/w/s/n | 0 |  |  |
| const `OPS` | 26 | turn lambdas: cw ccw half mirror_x mirror_z | 0 |  |  |
| `vec` | 35 | direction name or offset to unit (dx, dz) | 0 |  | INT |
| `opposite` | 45 | opposite direction name | 0 |  | INT |
| `stair` | 51 | stair data climbing toward a side | 43/14 | 6 |  |
| `ladder` | 56 | ladder/wall-sign data on a wall side | 8/4 | 2 |  |
| const `wall_sign` | 61 | wall-sign data on a side | 0 |  |  |
| `torch` | 64 | torch data on a wall or standing | 4/2 | 3 |  |
| `log_axis` | 71 | log data lying along an axis | 0 |  | DEAD |
| `slab` | 78 | slab data (top/bottom) | 0 |  | DEAD |
| `door` | 82 | door lower/upper halves data | 4/2 | 2 |  |
| `yaw` | 89 | Minecraft yaw for a facing | 0 | 1 | TEST |
| `rotation16` | 95 | sign/banner 0-15 rotation for a facing | 0 | 1 | TEST |
| `data_table` | 197 | (256,16) data-after-turn table per op | 0 | 3 | INT |
| `turn_data` | 210 | data of a block after a turn | 0 | 7 | INT |
| `turn_xz` | 216 | where a column lands under an op | 0 |  | INT |
| `turn_world` | 224 | copy part of a world onto its image | 18/18 | 2 |  |

### `world.py` — 193 lines

Imports (pgmvox): `blocks`. Subject today: The voxel volume a generator writes into, and the bridge to the studio's Anvil writer.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `seed` | 26 | seed for a named random stream | 0 |  | INT |
| `rng` | 33 | numpy generator for a named stream | 91/17 |  |  |
| class `World` | 44 | voxel volume: set/fill/column/save/load | 73/23 | 58 |  |
| `studio_root` | 176 | studio checkout location | 0 |  | INT |
| `write` | 184 | write region files through studio's Anvil writer | 0 |  | INT |

### `move.py` — 152 lines

Imports (pgmvox): none. Subject today: Minecraft 1.8 player movement, a tick at a time: the one copy of the model five boards each wrote.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `EYE` | 22 | eye height constant | 0 |  |  |
| `fly` | 34 | ballistic flight with no input | 0 |  | INT |
| `land_at` | 56 | landing test for flat ground | 0 | 1 | TEST |
| `fall` | 66 | ticks and distance of a fall off an edge | 0 | 1 | INT |
| `fall_damage` | 82 | half-hearts lost to a drop | 0 | 4 | INT |
| `jump_reach` | 90 | horizontal reach of a jump to a rise | 1/1 | 1 |  |
| `knockback` | 108 | distance a hit carries on given slipperiness | 0 | 3 | TEST |
| `solve_launch` | 130 | search pad velocity landing nearest a target | 0 | 1 | TEST |

### `noise.py` — 82 lines

Imports (pgmvox): none. Subject today: Smooth noise without a noise library: random lattices upsampled with cubic splines, summed in octaves.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `lattice` | 14 | one random-lattice octave, cubic upsampled | 0 |  | INT |
| `fbm` | 24 | fractal noise from octaves | 72/14 | 6 |  |
| `line` | 36 | wandering offset along one grid axis | 7/3 | 14 |  |
| `ragged` | 47 | wandering whole-block bite | 8/2 | 1 |  |
| `ridged` | 53 | 1 - |fbm| ridge noise | 3/3 |  |  |
| `smoothstep` | 58 | eased 0..1 ramp between edges | 30/8 | 11 |  |
| `spline` | 69 | Catmull-Rom through points | 14/5 |  |  |

### `shapes.py` — 214 lines

Imports (pgmvox): none. Subject today: Shapes over the board's grid: polygons, polylines, discs, ellipses and rings as boolean masks and distance.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `inside` | 10 | point-in-polygon mask | 10/7 |  |  |
| `seg_distance` | 25 | distance to a segment and parameter | 0 |  | INT |
| `edge_distance` | 34 | distance to polygon boundary | 0 |  | INT:doc |
| `signed_distance` | 43 | signed distance to a polygon | 0 |  | INT |
| `polyline` | 49 | distance, arc length, side to a polyline | 25/7 | 2 |  |
| `nearest_on` | 69 | one point's distance and arc length on a polyline | 3/3 | 4 |  |
| `length` | 75 | polyline length | 2/2 |  |  |
| `point_at` | 79 | point and heading at arc length | 0 |  | INT |
| `walk_cells` | 90 | four-connected cells along a polyline | 1/1 |  |  |
| `rect_cells` | 106 | cells of a rectangle by corners | 3/2 | 4 |  |
| `poly_cells` | 112 | cell set inside a polygon | 0 | 1 | TEST |
| `disc` | 121 | disc mask | 1/1 |  |  |
| `ring` | 125 | ring mask | 0 |  | DEAD |
| `ellipse_distance` | 130 | 1 on an ellipse rim, turned | 2/1 | 5 |  |
| `ellipse` | 141 | turned ellipse mask | 0 |  | DEAD |
| `stroke` | 149 | tapered stroke mask | 0 |  | DEAD |
| `boundary` | 160 | mask cells with an outside neighbour | 9/8 |  |  |
| `distance_in` | 169 | distance inside a mask (taxicab/chess/euclid) | 0 | 4 | INT |
| `edge_depth` | 178 | steps inside the edge (distance_in - 1) | 12/7 | 1 |  |
| `scatter_points` | 184 | points over a mask kept apart | 11/2 | 1 |  |
| `island` | 203 | board land from a box with inset sides, cut corners | 3/3 | 1 |  |

### `field.py` — 84 lines

Imports (pgmvox): `noise`. Subject today: Heightfields stated as terms: a base height plus ramps, mounds, tilts and noise, summed in the order given, and.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `Ramp` | 19 | term: eased rise along an axis | 8/2 | 3 |  |
| class `Gauss` | 32 | term: elliptical turned gaussian mound | 1/1 | 2 |  |
| class `Tilt` | 53 | term: plane | 0 | 1 | INT:doc |
| class `Noise` | 64 | term: scaled noise field | 4/2 |  |  |
| `terms` | 73 | base plus terms, summed in order | 5/2 | 6 |  |
| `mix` | 81 | blend two fields by a weight | 1/1 | 1 |  |

### `landform.py` — 481 lines

Imports (pgmvox): `noise`, `shapes`. Subject today: Landforms: operations that shape a heightfield the way the boards shaped theirs by hand.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `smooth_min` | 40 | lower of two with rounded seam | 0 | 3 | INT:doc |
| `smooth_max` | 51 | higher of two with rounded seam | 0 | 2 | TEST |
| `join` | 58 | several rises over one ground, melted together | 0 | 3 | INT:doc |
| `soften` | 70 | ease a form's change to nothing at its rim | 0 | 1 | TEST |
| class `Step` | 80 | one cliff of a profile cross-section | 2/1 | 5 |  |
| class `Water` | 92 | cells and surface y a landform holds | 1/1 |  |  |
| `watercourse` | 127 | river along a path with reaches and falls | 3/3 | 3 |  |
| `lake` | 166 | lake outline holding water | 3/1 | 1 |  |
| `hold` | 186 | raise dry cells beside water to its surface | 2/2 |  |  |
| `canyon` | 199 | canyon along a path with ledges | 1/1 | 1 |  |
| `spire` | 237 | spire from radius to top | 5/4 | 4 |  |
| `butte` | 248 | flat-topped butte or mesa with cliff | 4/3 | 1 |  |
| `scarp` | 261 | ground lifted on one side of a path | 2/2 |  |  |
| `terraces` | 274 | ground cut into terraces inside a mask | 1/1 | 1 |  |
| `stage` | 285 | rings of level discs stepped from outside in | 1/1 |  |  |
| `grade` | 296 | grade a route into the ground | 7/6 | 5 |  |
| `coast` | 347 | land meeting sea at an outline | 1/1 | 2 |  |
| `blend` | 367 | two terrains eased together over a mask | 9/4 |  |  |
| `profile` | 376 | cross-section by distance from a line | 2/1 | 6 |  |
| `level` | 403 | level ground inside a distance, eased back | 1/1 | 3 |  |
| `mound` | 416 | heap over a distance field | 1/1 | 4 |  |
| `crater` | 424 | bowl in one-block steps | 1/1 | 1 |  |
| `ridge` | 432 | ridge from wandering foot to crest | 2/2 | 2 |  |
| `spire_sites` | 450 | draw spire sites apart and off paths | 0 | 2 | TEST |
| `spire_field` | 470 | spires standing at given sites | 0 | 1 | TEST |

### `terrain.py` — 403 lines

Imports (pgmvox): `blocks`, `noise`, `shapes`. Subject today: Terrain at block scale: heights read and painted by slope, rock beds, scenery mountains outside the play, the.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `mountain_ring` | 25 | ring of ridged massifs outside a clear radius | 1/1 | 1 |  |
| `slope_deg` | 48 | slope per column as the studio reads it | 9/8 | 4 |  |
| class `Paint` | 80 | one top-paint layer: block, slope, place | 25/4 | 3 |  |
| `first_paint` | 98 | first applicable paint for a column | 0 |  | INT |
| `by_angle` | 106 | paint rule from slope stops | 7/7 |  |  |
| `banded` | 117 | column fill in horizontal bands | 0 |  | DEAD |
| class `Strata` | 126 | weighted rock beds by height | 12/12 | 2 |  |
| `bed_offset` | 160 | how far beds lift per column (dip, fold) | 9/9 |  |  |
| `beds` | 171 | column fill from strata with offset | 12/12 | 1 |  |
| `ledge_angle` | 193 | slope a paint reads on ledges | 0 |  | INT |
| `soil_depth` | 205 | soil depth by slope | 0 |  | INT |
| `lay` | 214 | ground columns: rock, soil, painted top, bottom | 10/9 | 3 |  |
| `fill_water` | 265 | bed and water up to each column's level | 4/4 | 1 |  |
| `island_bottom` | 281 | where floating rock ends under a column | 3/3 | 1 |  |
| `slab` | 294 | floating floors at own heights | 3/3 | 1 |  |
| `waterfall` | 316 | water falling off the board edge | 1/1 | 2 |  |
| `root_depth` | 344 | how far an underside hangs per column | 5/5 | 2 |  |
| `underside` | 363 | stamp tapering underside below a floor | 2/2 |  |  |
| `cloud_deck` | 384 | deck of cloud with billows | 5/5 |  |  |

### `route.py` — 352 lines

Imports (pgmvox): `blocks`, `orient`, `shapes`. Subject today: Routes over ground: where a road or a path goes, and laying it.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `find` | 47 | least-cost graded route over ground | 1/1 | 5 |  |
| `simplify` | 157 | Ramer-Douglas-Peucker | 2/1 | 1 |  |
| `smooth` | 172 | Chaikin corner cutting | 2/1 | 1 |  |
| `network` | 187 | roads joining places, trunks shared | 1/1 | 1 |  |
| `footprint` | 214 | columns a route of a width covers | 4/3 |  |  |
| `grades` | 220 | grade of every leg of a route | 0 |  | DEAD |
| `pave` | 230 | lay a route's surface and bridges | 8/7 |  |  |
| `steps` | 261 | stair on every one-block rise | 3/3 |  |  |
| `halfstep_levels` | 311 | steep route as half-block levels | 1/1 | 2 |  |
| `halfsteps` | 333 | lay half-block slabs and blocks | 1/1 | 1 |  |

### `trees.py` — 175 lines

Imports (pgmvox): `blocks`, `orient`, `world`. Subject today: Trees: hand-built trees planted whole, from the studio's tree library or a board's own cut.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `Tree` | 39 | tree: blocks relative to its foot | 0 |  | INT |
| `library` | 55 | studio's copied trees | 10/9 | 1 |  |
| `load` | 68 | a board's own tree cut | 1/1 |  |  |
| `kinds` | 76 | trees grouped by kind | 11/10 | 1 |  |
| `turned` | 84 | tree blocks after quarter turns | 0 |  | INT |
| `plant` | 95 | plant a tree turned, refused whole | 8/7 | 3 |  |
| `scatter` | 127 | wood over a zone, crowns apart | 9/6 | 1 |  |
| `dead_tree` | 155 | bare trunk with arms | 1/1 |  |  |

### `under.py` — 256 lines

Imports (pgmvox): `blocks`, `orient`, `shapes`, `solid`. Subject today: Under the ground: caves, mines and shafts, carved into a built world.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `carve` | 48 | air in cells above a floor, keep cover | 0 |  | INT |
| `tunnel` | 66 | cave passage through waypoints | 4/4 | 1 |  |
| `chamber` | 79 | ellipsoid hall | 2/2 |  |  |
| `dress_cave` | 85 | floors, stalactites, ore in caves | 4/4 |  |  |
| `gallery_line` | 139 | mine cells through waypoints | 5/3 | 1 |  |
| `gallery` | 157 | timbered railed mine gallery | 3/3 | 1 |  |
| `shaft` | 215 | 3x3 well shaft with logs | 3/3 | 1 |  |
| `bore` | 238 | round hole straight through rock | 0 | 1 | TEST |

### `solid.py` — 68 lines

Imports (pgmvox): none. Subject today: Solids: the repository's own `tools/sculpt/solid.py`, and what a freeform board needs on top of it.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `fill` | 30 | write a solid into a World | 0 | 1 | TEST |
| `image` | 45 | solid through a plan Symmetry | 0 | 1 | TEST |
| `turned` | 58 | solid turned about the vertical | 0 |  | DEAD |
| `count` | 63 | block count of a solid | 0 |  | DEAD |

### `forms.py` — 275 lines

Imports (pgmvox): `blocks`, `noise`, `orient`, `shapes`. Subject today: Forms: scenery built in three dimensions, block by block, where a heightfield cannot say it.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `tower` | 29 | rock tower: rings tapering up, ledges, vines | 2/2 | 1 |  |
| `skirt` | 77 | karst faces under a floating floor's rim | 2/2 | 1 |  |
| `root_vines` | 111 | vines hanging from floating roots | 2/2 |  |  |
| `masonry_tower` | 133 | hollow masonry tower with ladder, door, crenels | 3/3 | 1 |  |
| `arch` | 192 | natural arch over a deck | 1/1 | 1 |  |
| `box_cells` | 222 | cells of a turned, tilted box | 0 | 1 | INT |
| `placed_box` | 245 | monolith/slab/ring sunk into the ground | 0 | 2 | INT:doc |

### `build.py` — 633 lines

Imports (pgmvox): `blocks`, `orient`, `shapes`. Subject today: Buildings: a frame at any heading, the studio's roof field, a house, and the parts every board repeated.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `FORMS` | 34 | roof form names | 1/1 | 1 |  |
| class `Frame` | 42 | building axes at any heading | 14/8 | 3 |  |
| class `RoofField` | 107 | studio's six roof forms as a height field | 1/1 | 3 |  |
| `lay_roof` | 275 | stamp a roof field into the world | 1/1 |  |  |
| `window_rhythm` | 345 | one window in every `period` along a wall | 2/2 | 1 |  |
| class `House` | 355 | house parameters at any heading | 12/11 | 3 |  |
| `house` | 377 | build one house into a world | 12/11 | 3 |  |
| `edge_cells` | 486 | cells of a set with an outside four-neighbour | 3/2 |  |  |
| `parapet` | 492 | parapet and crenels round a cell set's edge | 4/4 |  |  |
| `site` | 502 | level ground under a footprint, ease the ring back | 6/5 |  |  |
| `stairs` | 529 | straight flight of stairs with fill beneath | 2/2 |  |  |
| `ladder` | 543 | ladder on a wall from y0 to y1 | 0 |  | DEAD |
| class `Claims` | 549 | layered occupancy map listing overlaps | 1/1 | 1 |  |
| `line_wall` | 572 | wall, hedge or fence along a line | 0 | 5 | INT:doc |

### `facade.py` — 362 lines

Imports (pgmvox): `blocks`. Subject today: Faces and floors with a pattern on them: insets, flutes, glyphs and words on a wall; borders, medallions and.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `DARK` | 32 | dark block constant | 4/1 |  |  |
| `band` | 71 | horizontal face band | 3/2 |  |  |
| `courses` | 76 | flush course of another block every n | 4/3 |  |  |
| `flutes` | 81 | vertical grooves set back | 1/1 |  |  |
| `panels` | 90 | alternating flush and set-back panels | 0 |  | DOC |
| `slits` | 99 | narrow flush windows | 0 |  | DOC |
| `checker` | 109 | inset-square field on a blank face | 0 |  | DOC |
| `glyph_row` | 136 | 5x5 glyphs inlaid along a face | 2/2 |  |  |
| `word` | 150 | word in 3x5 letters on a face | 1/1 |  |  |
| `windows` | 155 | flush windows every `period` | 4/3 |  |  |
| `faces` | 165 | face runs of a cell set | 1/1 |  |  |
| `extrude` | 193 | pour a mass and pattern its faces | 7/5 |  |  |
| `top_course` | 225 | cornice or parapet at a mass's top | 0 |  | INT |
| `coffer` | 242 | underside cut into recessed coffers | 0 |  | INT |
| `concrete` | 257 | board-formed concrete courses | 1/1 |  |  |
| class `Cell` | 264 | cell of a floor-field rectangle (u, v offsets) | 0 |  | INT |
| `border` | 276 | floor field: outer rows or ring | 20/7 |  |  |
| `medallion` | 283 | floor field: diamond medallion | 9/4 |  |  |
| `corners` | 288 | floor field: quarter medallions in corners | 2/2 |  |  |
| `diamonds` | 293 | floor field: chain of diamonds | 3/1 |  |  |
| `kilim_steps` | 301 | floor field: stepped kilim bands | 0 |  | DOC |
| `star` | 309 | floor field: eight-pointed star | 2/1 |  |  |
| `stripes` | 314 | stripes floor field | 1/1 |  |  |
| `tiles` | 318 | floor field: two-block checker | 4/3 |  |  |
| `cross` | 323 | floor field: two crossing bands | 2/2 |  |  |
| `rings` | 328 | floor field: concentric rings | 0 |  | DOC |
| `first_of` | 339 | first floor field that answers | 12/7 |  |  |
| `carpet` | 350 | lay a floor field over a rectangle | 15/8 |  |  |

### `props.py` — 258 lines

Imports (pgmvox): `blocks`, `orient`, `shapes`. Subject today: Props: small built things that dress a place, each with the way it faces and what it is made of as parameters.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `stall` | 24 | 3x3 market stall facing a way | 0 |  | INT |
| `stalls` | 54 | row of stalls along a line | 5/4 | 1 |  |
| `lamp` | 63 | lamp post on a floor | 10/7 |  |  |
| `wool_chests` | 110 | studio wool-room loot chests | 9/7 | 1 |  |
| `studio_defence` | 127 | studio defence chest contents | 0 | 1 | INT |
| `defence_chests` | 138 | defence chests set into a wall | 4/3 | 1 |  |
| `laid` | 149 | chest items drawn as rows of letters | 0 | 2 | INT |
| `brazier` | 167 | post on footing with a light | 7/4 |  |  |
| `rubble` | 175 | heap of loose stone | 5/3 | 1 |  |
| `lamps` | 192 | lamp posts beside a route | 2/2 | 1 |  |
| `crop_field` | 216 | farmland strips with ditches and fence | 1/1 | 1 |  |
| `scarecrow` | 247 | scarecrow of fence posts and hay | 1/1 |  |  |

### `grammar.py` — 322 lines

Imports (pgmvox): `blocks`, `shapes`. Subject today: A grammar for structural boards: surfaces cut into rectangular sections, each outlined and filled by rule, and.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `DIRS` | 34 | direction table | 0 |  |  |
| class `Section` | 40 | boxes at one height, a surface piece | 1/1 | 3 |  |
| `split` | 90 | cut a box into nx by nz sections | 0 | 2 | INT |
| `tile` | 97 | cut a box into module-sized squares | 0 | 1 | TEST |
| class `Ground` | 107 | every column's top, section and depth | 1/1 | 2 |  |
| `spec` | 149 | course spec: block or function of inward side | 0 |  | INT |
| class `Sunk` | 155 | course set back one block | 0 |  | INT |
| class `Accent` | 161 | bay laid every n bays along a face | 0 | 1 | INT |
| class `Face` | 179 | courses of a face, top down | 0 | 1 | INT |
| class `Lot` | 228 | section's inside as a fill sees it | 0 |  | INT |
| class `Style` | 259 | blocks a grammar is spoken in | 0 | 1 | INT |
| `lay` | 281 | lay sections in a style | 1/1 | 2 |  |

### `brittle.py` — 657 lines

Imports (pgmvox): `blocks`, `grammar`, `objectives`, `orient`. Subject today: The Brittlebush style: a board drawn as a blueprint of five-block cells and built in the look of Brittlebush I.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `CELL` | 43 | cell edge, 5 blocks | 47/3 |  |  |
| const `LAND` | 51 | cell kinds that are land | 1/1 |  |  |
| class `Cell` | 56 | one blueprint cell: kind, floor y, rise, section, deck | 6/2 | 11 |  |
| `turn_cells` | 65 | A blueprint turned k quarters clockwise about the middle: ce | 1/1 |  |  |
| `fan` | 74 | A unit drawn once, with its images under quarter turns: ({ce | 1/1 | 4 |  |
| `heights` | 85 | per-column ground top and deck top from cells | 0 |  | INT:doc |
| `pieces` | 111 | joins same-kind neighbour cells into numbered pieces | 0 |  | INT |
| `ground` | 137 | stone, bedrock, obsidian column under a floor | 0 |  | INT |
| `tree` | 148 | round birch tree | 0 |  | INT |
| `bed` | 161 | grass bed in two sandstone-stair rings | 0 |  | INT |
| `sand` | 194 | sand field with upside-down sandstone stairs | 0 |  | INT |
| `cap` | 275 | five-course edge cap of a ground face | 0 |  | DEAD |
| `sections` | 288 | blueprint pieces as grammar sections | 0 |  | INT |
| `build` | 303 | stamp the cells into a world in Brittlebush look | 3/3 | 6 |  |
| `storey` | 458 | one storey of a tiered tower | 0 |  | INT |
| `tower` | 496 | tiered tower with door over a box | 0 |  | DEAD |
| `house` | 519 | wool room: storeys of whole cells | 5/3 | 1 |  |
| `heart` | 642 | seven-wide wool heart on a wall | 0 |  | DEAD |

### `clay.py` — 204 lines

Imports (pgmvox): `blocks`, `grammar`, `orient`. Subject today: The Claywork style for pgmvox.grammar: grey stone and white clay, the team's colour inlaid. A board on bedrock,.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `squares` | 44 | one axis of the inlay squares | 0 |  | INT |
| `style` | 61 | Claywork grammar Style in a team colour | 1/1 | 1 |  |

### `studioplan.py` — 108 lines

Imports (pgmvox): `brittle`. Subject today: Read a plan drawn in the studio's planner (plan version 2) as a pgmvox.brittle blueprint of cells.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `load` | 31 | read studio plan json | 1/1 |  |  |
| `unit` | 41 | one team's part as a brittle blueprint | 1/1 | 1 |  |
| `placement` | 81 | spawns, wools, etc. with positions | 2/1 |  |  |
| `facing` | 101 | placement facing as n/e/s/w | 1/1 |  |  |

### `plan.py` — 213 lines

Imports (pgmvox): `orient`, `shapes`, `terrain`. Subject today: The plan as rasters: every column's floor and what kind of floor it is, drawn once and read by the checker,.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `Symmetry` | 23 | op + axis: point, direction, image, field, whole | 20/19 | 8 |  |
| class `Raster` | 89 | plan as per-column floor height and kind | 18/18 | 4 |  |

### `plangraph.py` — 282 lines

Imports (pgmvox): `move`. Subject today: Walking the plan: the graph of how a player moves over a raster, shortest routes, arrival times per team, and.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `PlanRules` | 30 | walking rules over a raster | 20/17 | 3 |  |
| `jumps` | 39 | every jump a raster allows | 5/4 | 1 |  |
| `node` | 84 | cell to graph node | 1/1 |  |  |
| `walkable` | 90 | standable cells per storey | 3/2 |  |  |
| `graph` | 104 | edge graph over a raster and its storeys | 23/18 | 6 |  |
| `measure` | 182 | cheapest target and cost split by move | 23/11 | 1 |  |
| `dijkstra` | 199 | cheapest cost to every node | 69/19 | 5 |  |
| `route` | 219 | cheapest target with non-walk moves listed | 5/2 |  |  |
| `path` | 234 | cells of the route to a cell | 12/7 |  |  |
| `arrivals` | 242 | per-team cheapest cost to named targets | 4/3 | 1 |  |
| `pad_edges` | 255 | graph edges for launch pads | 0 |  | DEAD |

### `pieces.py` — 194 lines

Imports (pgmvox): `move`, `plan`. Subject today: A course plan: a board made of pieces in order, and the links a player takes from one to the next.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `box` | 36 | cells of a rectangle by ranges | 10/1 | 4 |  |
| class `Piece` | 44 | one piece of a course: cells, floor, kind | 0 |  | INT |
| class `Course` | 62 | board played in order: pieces, links, audit | 1/1 | 1 |  |
| `gap` | 150 | clear void distance between two pieces | 0 |  | INT |
| `lands_at` | 161 | cell a jump comes down in | 0 |  | INT |
| `clears` | 176 | gentlest way across a gap onto a lower piece | 0 | 1 | INT |

### `walk.py` — 202 lines

Imports (pgmvox): `blocks`, `move`. Subject today: The walk over built blocks, and the checks a board reads back from them.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `MoveRules` | 31 | movement rule parameters | 33/19 | 4 |  |
| `classes` | 44 | passable/water/climbable/solid masks | 0 |  | INT |
| `standing` | 53 | cells a player can occupy | 2/2 |  |  |
| `walk` | 66 | moves to every standing place from starts | 64/20 | 7 |  |
| `nearest` | 154 | moves to nearest reached place | 53/20 | 5 |  |
| `unreached` | 167 | list of positions nobody reaches | 0 |  | DEAD |
| `no_stand_above` | 172 | columns with standing room above a region | 5/5 | 1 |  |
| `catchers` | 186 | blocks that catch a falling player | 0 |  | DEAD |
| `gap_cleared` | 198 | does a sprint jump clear a gap | 0 | 3 | TEST |

### `audit.py` — 93 lines

Imports (pgmvox): `blocks`. Subject today: Footing: the blocks that would fall or pop off when the world loads.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `footing` | 33 | blocks that fall or have nothing to hang on | 20/20 | 5 |  |
| `loose_water` | 70 | water standing against air | 7/7 | 6 |  |

### `sight.py` — 85 lines

Imports (pgmvox): `blocks`, `move`. Subject today: Sight lines: who can see whom, on a plan or in a built world.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `line_clear` | 22 | voxel sight line test | 2/2 | 2 |  |
| `plan_opaque` | 38 | opacity volume from a raster | 10/10 | 1 |  |
| `voxel_opaque` | 53 | opacity volume from a world | 3/3 |  |  |
| `eye` | 64 | eye point of a player in a cell | 19/10 | 2 |  |
| `target` | 69 | aim point of a player | 13/9 | 2 |  |
| `visibility` | 73 | share of eyes that see each target | 2/2 |  |  |
| `hidden` | 82 | targets no eye sees | 13/7 |  |  |

### `render.py` — 199 lines

Imports (pgmvox): `blocks`. Subject today: Pictures of a built world, in the studio's colours: an isometric view from any corner, a straight-on.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `xray_shell` | 21 | keep only blocks lining a roofed void | 0 |  | INT |
| `iso` | 43 | isometric view from a corner | 33/22 | 1 |  |
| `elevation` | 121 | orthographic elevation | 18/14 |  |  |
| `cutaway` | 151 | true-scale section along a polyline | 50/18 |  |  |
| `trim` | 190 | crop empty sky from a render | 26/22 |  |  |

### `sketch.py` — 548 lines

Imports (pgmvox): `blocks`, `shapes`. Subject today: The sketch: a plan drawn before anything is built, annotated so it can be reviewed, and the same annotation.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `TEAM` | 40 | team colours | 46/14 | 2 |  |
| `font` | 46 | font loader | 0 |  | INT |
| `pale` | 52 | wash colour toward white | 0 |  | INT |
| `dark` | 57 | darken colour | 0 |  | INT |
| class `Panel` | 86 | base panel | 0 |  | INT |
| class `MapPanel` | 96 | top-down annotated map panel | 4/2 |  |  |
| class `SectionPanel` | 373 | true-scale section panel | 45/18 | 2 |  |
| class `TablePanel` | 474 | measurements vs targets table | 0 |  | INT |
| class `Sheet` | 497 | stack of panels, saved as a png | 38/21 | 1 |  |

### `plot.py` — 116 lines

Imports (pgmvox): `audit`, `blocks`, `sight`, `walk`, `world`. Subject today: A plot: a bounded canvas handed to a contributor, and the check a plot passes alone before it goes on a board.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `OutOfPlot` | 25 | error: write outside the plot | 0 |  | INT |
| class `Canvas` | 29 | bounded canvas handed to a plot | 0 |  | INT |
| `load` | 59 | load a plot module | 0 | 1 | TEST |
| `draw` | 73 | run a plot's build on its ground | 0 |  | INT |
| `check_alone` | 87 | build and walk a plot alone | 0 | 2 | TEST |
| `verdict` | 109 | text verdict of a plot check | 0 | 1 | TEST |

### `objectives.py` — 695 lines

Imports (pgmvox): `blocks`, `mapxml`, `orient`. Subject today: Objectives that write themselves: each one stamps its blocks, names the cells it stands on, writes its own regions.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| const `DYES` | 32 | colour name to wool data | 10/5 |  |  |
| class `Box` | 39 | inclusive block box with cuboid() and blocks() | 52/19 | 11 |  |
| `turn_point` | 78 | point carried through a Symmetry | 0 |  | INT |
| `turn_yaw` | 83 | yaw carried through a Symmetry | 0 |  | INT |
| `centre_el` | 92 | point element at a block centre | 0 |  | INT |
| class `Teams` | 105 | team ids, names, colours, sizes | 19/19 | 3 |  |
| class `Objective` | 138 | base: team, symmetry image, region ids | 0 |  | INT |
| class `Spawn` | 175 | team spawn: stand block, yaw, kit, area | 29/19 | 5 |  |
| class `Observer` | 222 | observer/dead default spawn | 19/19 |  |  |
| class `Hill` | 232 | king-of-the-hill control point and pad | 7/4 | 2 |  |
| class `Flag` | 281 | flag and posts (CTF) | 0 |  | DEAD |
| class `Wool` | 315 | CTW wool, monument, room | 26/7 | 5 |  |
| `wool_rooms` | 397 | wool-room protection regions and filters | 0 |  | INT |
| const `FLOAT` | 416 | required air under a monument/core | 1/1 |  |  |
| `float_problems` | 419 | check monument/core floats over the floor | 0 |  | INT |
| class `Destroyable` | 439 | DTM monument box | 8/5 | 5 |  |
| class `Core` | 486 | DTC obsidian shell round lava | 2/2 | 1 |  |
| class `ScoreBox` | 524 | score box with return portal | 0 |  | INT |
| class `Portal` | 558 | portal from a box to a landing block | 0 |  | DEAD |
| class `Objectives` | 588 | the set: stamp, mirror, write XML, check | 19/19 | 3 |  |
| `build_marker` | 663 | build-region outline columns (studio rule ST5) | 0 | 12 | INT |

### `mapxml.py` — 202 lines

Imports (pgmvox): none. Subject today: Writing a PGM map.xml: an element builder and the pieces every board's writer repeated.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `E` | 24 | element builder with attribute-name rules | 174/19 | 9 |  |
| `point` | 47 | point element | 0 | 2 | INT |
| `cuboid` | 51 | cuboid element, max exclusive | 0 |  | DEAD |
| `cylinder` | 56 | cylinder element | 0 |  | DEAD |
| `circle` | 60 | circle element | 0 |  | DEAD |
| `below` | 64 | below element | 0 |  | INT |
| `negative` | 68 | negative element | 0 |  | DEAD |
| `union` | 72 | union element | 0 |  | DEAD |
| `item` | 76 | kit item element with enchants | 187/13 | 2 |  |
| `duration` | 84 | seconds as PGM duration text | 0 | 1 | INT |
| class `Doc` | 90 | map.xml document with players, spawns, time helpers | 19/19 | 6 |  |

### `document.py` — 655 lines

Imports (pgmvox): `blocks`, `brittle`, `build`, `facade`, `field`, `forms`, `landform`, `noise`, `orient`, `route`, `shapes`, `terrain`, `trees`, `world`. Subject today: The layer document: a board stated as data and built in order, every step kept.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| class `Step` | 42 | one layer as run: id, stage, heights, changed cols | 0 |  | INT |
| class `Built` | 53 | result of a build: world, heights, steps | 0 |  | INT |
| `block` | 64 | block from NAME / [NAME, data] spec | 0 |  | INT |
| class `Ctx` | 91 | what an expression reads: grid, fields, lines | 0 |  | INT |
| `expr` | 102 | a number or field stated as data, evaluated | 0 |  | INT |
| `area_distance` | 275 | 0 at area centre, 1 at rim, for any area shape | 0 |  | INT |
| `made_cells` | 390 | `made` stage as brittle cells | 0 |  | INT |
| `made_mask` | 404 | made-land mask and tops from a made stage | 0 |  | INT |
| `ground` | 451 | fields and ground stages only | 0 | 1 | INT |
| `build` | 509 | build a layer document stage by stage | 0 | 2 | TEST |

### `run.py` — 148 lines

Imports (pgmvox): `VERSION`, `world`. Subject today: Build a freeform board from nothing, in the order every board's build.sh ran it:.

| symbol | line | what | ext | t | flag |
|---|---:|---|---:|---:|---|
| `world_folder` | 37 | folder a board's world is written to | 0 |  | INT |
| `run` | 60 | pipeline: plan_check..walk | 1/1 | 1 |  |
| `main` | 133 | CLI entry | 0 |  | INT |


---

## 2. Who uses what

The `ext` and `t` columns of every §1 table carry the per-function counts. This section is the roll-up.

### 2.1 By module

| module | public defs/classes | with external callers | external call sites | boards using |
|---|---:|---:|---:|---:|
| `blocks` | 5 | 2 | 2020 (1996 are `B`) | 24 |
| `mapxml` | 11 | 3 | 380 | 20 |
| `objectives` | 19 | 9 | 181 | 19 |
| `plangraph` | 11 | 10 | 165 | 19 |
| `world` | 5 | 2 | 164 | 23 |
| `walk` | 9 | 5 | 157 | 20 |
| `noise` | 7 | 6 | 134 | 14 |
| `render` | 5 | 4 | 127 | 22 |
| `terrain` | 19 | 15 | 108 | 15 |
| `facade` | 27 | 19 | 94 | 8 |
| `sketch` | 8 | 3 | 87 | 21 |
| `shapes` | 21 | 12 | 82 | 12 |
| `orient` | 14 | 5 | 77 | 19 |
| `sight` | 7 | 7 | 62 | 10 |
| `build` | 13 | 11 | 58 | 12 |
| `landform` | 25 | 19 | 49 | 7 |
| `props` | 12 | 9 | 44 | 16 |
| `trees` | 8 | 6 | 40 | 11 |
| `plan` | 2 | 2 | 38 | 21 |
| `audit` | 2 | 2 | 27 | 20 |
| `route` | 10 | 9 | 23 | 8 |
| `under` | 8 | 6 | 21 | 5 |
| `field` | 6 | 5 | 19 | 2 |
| `brittle` | 16 | 5 | 16 | 3 |
| `pieces` | 6 | 2 | 11 | 1 |
| `forms` | 7 | 5 | 10 | 7 |
| `studioplan` | 4 | 4 | 5 | 1 |
| `grammar` | 11 | 3 | 3 | 1 |
| `clay` | 2 | 1 | 1 | 1 |
| `move` | 7 | 1 | 1 | 1 |
| `run` | 3 | 1 | 1 | 1 |
| `document` | 10 | 0 | 0 | 0 |
| `plot` | 6 | 0 | 0 | 0 |
| `solid` | 4 | 0 | 0 | 0 |
| **all** | **330** | **193** | | |

Of 330 public defs/classes, 193 have an external caller, 137 do not. Three whole modules have no board caller at all: `document` (654 lines, tests only), `plot` (115, tests only), `solid` (67, reached through `under`). `move`, `clay`, `grammar`, `studioplan` and `pieces` each serve exactly one board folder (`move` through `pieces`/`plangraph`/`walk` internally).

### 2.2 The load-bearing core (most used, 19+ boards)

`B` 1996/23 · `mapxml.item` 187/13 · `mapxml.E` 174/19 · `rng` 91/17 · `World` 73/23 · `noise.fbm` 72/14 · `plangraph.dijkstra` 69/19 · `walk.walk` 64/20 · `walk.nearest` 53/20 · `objectives.Box` 52/19 · `render.cutaway` 50/18 · `sketch.SectionPanel` 45/18 · `orient.stair` 43/14 · `sketch.Sheet` 38/21 · `render.iso` 33/22 · `walk.MoveRules` 33/19 · `render.trim` 26/22 · `objectives.Spawn` 29/19 · `audit.footing` 20/20 · `plan.Symmetry` 20/19 · `objectives.Teams` 19/19 · `objectives.Observer` 19/19 · `objectives.Objectives` 19/19 · `mapxml.Doc` 19/19 · `plan.Raster` 18/18 · `orient.turn_world` 18/18. These keep their names in the proposal.

### 2.3 Zero external callers

| class | meaning | names |
|---|---|---|
| `DEAD` (24) | no board, no test, no library caller | `blocks.info`; `orient.log_axis`, `slab`; `shapes.ring`, `ellipse`, `stroke`; `terrain.banded`; `route.grades`; `solid.turned`, `count`; `build.ladder`; `brittle.cap`, `tower`, `heart`; `plangraph.pad_edges`; `walk.unreached`, `catchers`; `objectives.Flag`, `Portal`; `mapxml.cuboid`, `cylinder`, `circle`, `negative`, `union` |
| `DOC` (5) | reachable by name from a layer document (`document.py:443`) | `facade.panels`, `slits`, `checker`, `kilim_steps`, `rings` |
| `TEST` (20) | tests only | `blocks.colour`; `orient.yaw`, `rotation16`; `move.land_at`, `knockback`, `solve_launch`; `shapes.poly_cells`; `landform.smooth_max`, `soften`, `spire_sites`, `spire_field`; `under.bore`; `solid.fill`, `image`; `grammar.tile`; `walk.gap_cleared`; `plot.load`, `check_alone`, `verdict`; `document.build` |
| `INT:doc` (7) | only `document.py` uses it | `shapes.edge_distance`; `field.Tilt`; `landform.smooth_min`, `join`; `forms.placed_box`; `build.line_wall`; `brittle.heights` |
| `INT` (81) | public name, only other pgmvox modules or itself use it | `blocks.mask`; `orient.vec`, `opposite`, `data_table`, `turn_data`, `turn_xz`; `world.seed`, `studio_root`, `write`; `move.fly`, `fall`, `fall_damage`; `noise.lattice`; `shapes.seg_distance`, `signed_distance`, `point_at`, `distance_in`; `terrain.first_paint`, `ledge_angle`, `soil_depth`; `trees.Tree`, `turned`; `under.carve`; `forms.box_cells`; `facade.top_course`, `coffer`, `Cell`; `props.stall`, `studio_defence`, `laid`; `grammar.split`, `spec`, `Sunk`, `Accent`, `Face`, `Lot`, `Style`; `brittle.pieces`, `ground`, `tree`, `bed`, `sand`, `sections`, `storey`; `clay.squares`; `pieces.Piece`, `gap`, `lands_at`, `clears`; `walk.classes`; `render.xray_shell`; `sketch.font`, `pale`, `dark`, `Panel`, `TablePanel`; `plot.OutOfPlot`, `Canvas`, `draw`; `objectives.turn_point`, `turn_yaw`, `centre_el`, `Objective`, `wool_rooms`, `float_problems`, `ScoreBox`, `build_marker`; `mapxml.point`, `below`, `duration`; `document.Step`, `Built`, `block`, `Ctx`, `expr`, `area_distance`, `made_cells`, `made_mask`, `ground`; `run.world_folder`, `main` |

Reading the table: the `DEAD` helpers are candidates for deletion (the README names `pad_edges`, `brittle.tower`/`heart` — edit it in the same commit). `objectives.Flag`, `Portal` and `ScoreBox` are PGM mode vocabulary the studio has (CTF, portals, score boxes); unused so far is not a reason to drop them from a port, so the decision is the author's. The `INT` names are fine as a public surface, but a C# port can make them `internal`. `document` is a second driver of the whole library with no board using it: it is the single largest consumer of `landform`, `route`, `forms`, `terrain` and `facade` internals and keeps `INT:doc`/`TEST` names alive.

---

## 3. Misplacements and overlaps

### 3.1 Modules that mix several subjects

| module | subjects found (line ranges) |
|---|---|
| `terrain.py` (402) | heightfield shape `mountain_ring` 25-42 · a read of heights `slope_deg` 48-71 · paint `Paint`/`first_paint`/`by_angle`/`banded` 80-123, `ledge_angle` 193-202, `soil_depth` 205-211 · rock beds `Strata`/`bed_offset`/`beds` 126-187 · laying columns `lay` 214-262 · water `fill_water` 265-279, `waterfall` 316-341 · floating ground `island_bottom` 281-291, `slab` 294-313, `root_depth` 344-360, `underside` 363-381 · sky `cloud_deck` 384-402. Seven subjects, one module; the docstring itself says "the landforms that shape the heights are in `landform`" while `mountain_ring` is one. |
| `landform.py` (480) | combinators `smooth_min/max`, `join`, `soften` 40-76 · rises `spire` 237, `butte` 248, `scarp` 261, `terraces` 274, `stage` 285, `mound` 416, `ridge` 432, `spire_sites/field` 450-479 · hollows `crater` 424, `canyon` 199 · water `Water` 92, `watercourse` 127, `lake` 166, `hold` 186, `coast` 347 · shaping `profile` 376 + `Step` 80, `level` 403, `blend` 367 · a route op `grade` 296. |
| `orient.py` (270) | directions 24-47 · what a block's data is when it faces a way 50-195 (stairs, ladder, torch, door, supplement table) · turning things through a symmetry 197-269 (`data_table`, `turn_data`, `turn_xz`, `turn_world` which also writes a `World`). |
| `objectives.py` (694) | geometry and symmetry carry `Box` 39, `turn_point` 78, `turn_yaw` 83, `centre_el` 92 · teams 105 · the objective classes 138-584 · two rule checkers sitting between `Wool` and `Destroyable`: `wool_rooms` 397, `float_problems` 419 · the set 588 · `build_marker` 663-694, which is the studio's build-region rule (ST5), not an objective, and is imported by `brittle` (brittle.py:39). |
| `brittle.py` (656) | blueprint `Cell` 56, `turn_cells` 65, `fan` 74, `heights` 85, `pieces` 111, `sections` 288 · look pieces `ground` 137, `tree` 148, `bed` 161, `sand` 194, `cap` 275, `STYLE` 265 · the build 303-377 · buildings `storey` 458, `tower` 496, `house` 519, `heart` 642. |
| `build.py` (633) | `Frame` 42, `RoofField` 107, `lay_roof` 275, `House`/`house` 355-482, then "the parts every board repeated" 485-632: `edge_cells` (a set utility), `parapet`, `site` (a terrain op), `stairs`, `ladder`, `Claims`, `line_wall` (landscape). |
| `facade.py` (362) | face patterns and the mass 70-259 · floor fields 262-361 (`border`, `medallion`, ..., `carpet`) with its own `Cell` 264. Floors are not facades. |
| `forms.py` (275) | rock `tower` 29 · floating-ground trim `skirt` 77, `root_vines` 111 · a building `masonry_tower` 133 · rock `arch` 192 · placed solids `box_cells` 222, `placed_box` 245. Five unrelated subjects. |
| `props.py` (258) | props `stall`...`scarecrow` · chests/loot `wool_chests` 110, `studio_defence` 127, `defence_chests` 138, `laid` 149 (play data, not scenery). |
| `shapes.py` (214) | polygon, polyline, mask measures · `scatter_points` 184 · `island` 203 (a board outline, terrain-level). |
| `under.py` (256) | caves `carve` 48, `tunnel` 66, `chamber` 79, `dress_cave` 85, `bore` 238 · mines `gallery_line` 139, `gallery` 157, `shaft` 215. |
| `world.py` (193) | the volume `World` 44-173 · the studio bridge `studio_root` 176, `write` 184 (spawns `dotnet`). |
| `plan.py` (213) | `Symmetry` 23-86 (not a plan: used by objectives, solid, sketch) · `Raster` 89-212. |
| `document.py` (655) | the layer DSL `expr`/`Ctx` 102-240 · stages · brittle-only `made_cells` 390, `made_mask` 404. |
| `mapxml.py` (202) | `Doc` + `E`/`item` (used) · region builders `cuboid`...`union` (never used; `Box.cuboid` builds its own). |

### 3.2 Functions whose subject is elsewhere

| function (now at) | belongs with | why |
|---|---|---|
| `terrain.mountain_ring` (25) | ground (rises) | arrays in, array out; no `World` |
| `terrain.slope_deg` (48) | ground (slope) | a read of heights; `plan.py:110` reaches up to `terrain` for it |
| `terrain.island_bottom` (281), `root_depth` (344) | ground (outline) | return arrays; shape of land, not a stamp |
| `terrain.fill_water` (265), `waterfall` (316) | surface (water) | stamps water; pair with `landform.Water` |
| `terrain.slab` (294), `underside` (363), `cloud_deck` (384) + `forms.skirt` (77), `root_vines` (111) | surface (floating) | one family: the underside of floating ground |
| `terrain.ledge_angle` (193), `soil_depth` (205), `first_paint` (98), `banded` (117) | surface (paint) / ground (slope) | paint helpers of `lay` |
| `landform.grade` (296) | routes | a road op; `route.footprint` exists "for a later route's grading" |
| `shapes.island` (203) | ground (outline) | draws the board's land |
| `build.site` (502) | surface | levels and eases ground; the `landform.level` job as a stamp |
| `build.line_wall` (572), `parapet` (492) | built (walls) | not a house |
| `build.edge_cells` (486) | geom | dup of `shapes.boundary` (§3.3) |
| `build.stairs` (529), `ladder` (543) | built (stairs) | building parts; `ladder` clashes with `orient.ladder` (56) |
| `objectives.build_marker` (663) | surface | a world rule used by `brittle`; wrong direction of dependency otherwise (grammar importing play) |
| `objectives.turn_point` (78), `turn_yaw` (83) | core/symmetry | symmetry carry |
| `objectives.Box` (39) | play/box | geometry; `cuboid()` is an XML builder |
| `plan.Symmetry` (23) | core/symmetry | used by objectives, solid, sketch, plan |
| `props.wool_chests` (110), `studio_defence` (127), `defence_chests` (138), `laid` (149) | play/chests | loot is a play rule |
| `forms.masonry_tower` (133) | built (tower) | a building |
| `brittle.tree` (148) | scenery/trees | a hard-coded birch beside `trees.plant` |
| `brittle.heart` (642) | built or grammar/brittle/buildings | a wall decoration |
| `facade` 262-361 floor fields + `Cell` (264) | built/floors | not faces; `Cell` clashes with `brittle.Cell` (56) |
| `world.studio_root` (176), `write` (184) | core/studio | tool bridge (calls `dotnet`), not the volume |
| `walk.gap_cleared` (198) | core/move | jump physics, not a world walk |
| `document.made_cells` (390), `made_mask` (404) | grammar/brittle | brittle-specific code in the generic driver |
| `pieces.box` (36) | delete | a third argument order for `shapes.rect_cells` (106) |

### 3.3 Near-duplicates: one job done twice or more

The tell in several is a docstring comparing itself to the other copy, quoted where it exists.

| job | where | note |
|---|---|---|
| cells of a rectangle | `shapes.rect_cells` 106 (corners), `pieces.box` 36 (ranges; docstring: "`shapes.rect_cells` takes corners"), `plan.Raster.box` 174 (corners) and `Raster.rect` 178 ("the older order; box takes corners") | three argument orders, four functions |
| edge cells of a set/mask | `build.edge_cells` 486 (set), `shapes.boundary` 160 (mask), `shapes.edge_depth` 178 (= `distance_in` - 1, "the measure ... a parapet inset or a terrace is cut by") | one concept in three types |
| carry a point/yaw/direction through a symmetry | `orient.turn_xz` 216 + `OPS` 26, `plan.Symmetry.point` 37 / `direction` 46, `objectives.turn_point` 78 / `turn_yaw` 83, `brittle.turn_cells` 65, `trees.turned` 84, `solid.image` 45 | six entry points, one rule |
| direction tables | `orient.DIRS` 24, `grammar.DIRS` 34 + `OPP` 35, `brittle.DIRS` 44 + `OPP` 45 + `CW` 46 | three copies of the same dict |
| walking rules | `walk.MoveRules` 31 (voxel) and `plangraph.PlanRules` 30 (plan): `max_drop`, `jumps`, `max_gap` in both | docstring of `walk.gap_cleared` 198: "the same rule the plan walk uses, so the plan and the built world agree" |
| jump / gap clearance | `move.jump_reach` 90, `walk.gap_cleared` 198, `pieces.clears` 176 + `pieces.WIDTH` 33 ("counted as walk.gap_cleared counts it"), `plangraph.jumps` 39 | the 0.6 player width appears as a literal in two places |
| a heap of ground | `field.Gauss` 32, `landform.mound` 416, `spire` 237, `butte` 248 | four ways to say "rise around a centre" |
| stepped ground | `landform.terraces` 274, `stage` 285, `profile` + `Step` 376/80 | |
| level the ground | `landform.level` 403 (heights), `build.site` 502 (blocks), `landform.blend` 367 | |
| underside of floating ground | `terrain.island_bottom` 281, `slab` 294, `root_depth` 344, `underside` 363, `forms.skirt` 77, `root_vines` 111, `shapes.island` 203 | seven functions in three modules |
| trees | `brittle.tree` 148, `trees.plant` 95 / `scatter` 127, `trees.dead_tree` 155 | |
| towers | `forms.tower` 29, `forms.masonry_tower` 133, `brittle.tower` 496 + `storey` 458 | three functions called `tower` in meaning, two in name |
| flights of stairs | `build.stairs` 529, `route.steps` 261, `route.halfsteps` 333, `under.gallery` 157, `plan.Raster.flight` 193 | |
| true-scale section | `render.cutaway` 151 (built world), `sketch.SectionPanel.raster` 392 / `along` 415 (plan raster) | different input, same output |
| top-down of a built world | `render.iso` 43 / `elevation` 121, `sketch.MapPanel.built` 183 | |
| cuboid element | `mapxml.cuboid` 51, `objectives.Box.cuboid` 54; `mapxml.union` 72 unused while `objectives.wool_rooms` 411 builds `E("union")` by hand | |
| a wandering line | `noise.line` 36, `noise.ragged` 47 (= rounded `line`) | fine, but one belongs to the other |
| banded rock/paint | `terrain.banded` 117 (unused), `Strata`/`beds` 126/171, `by_angle` 106 | |
| `load` | `trees.load` 68, `plot.load` 59, `studioplan.load` 31 | three unrelated verbs of one name |

### 3.4 Names that clash across modules

`Cell` (brittle 56, facade 264) · `Step` (document 42, landform 80) · `build` (brittle 303, document 509) · `ground` (brittle 137, document 451) · `house` (brittle 519, build 377) · `ladder` (build 543, orient 56) · `lay` (grammar 281, terrain 214) · `load` (plot 59, studioplan 31, trees 68) · `slab` (orient 78, terrain 294) · `tower` (brittle 496, forms 29) · `turned` (solid 58, trees 84). Also `walk.walk`, `plangraph.route` against `route.py`, `pieces.box` against `objectives.Box`. Every new module name in §4 avoids a function of the same name inside it.

### 3.5 Dependency direction problems today

| edge | problem |
|---|---|
| `brittle` -> `objectives` (brittle.py:39) | a look module imports the play module for `build_marker` |
| `plan` -> `terrain` (plan.py:110, lazy) | the lowest-level plan type reaches up to the terrain stamp module for `slope_deg` |
| `trees`, `run` -> `world` (`studio_root`) | a base module carries an IO bridge others import for a path |
| `document` -> 14 modules | a top-of-stack driver, correctly high, but with the largest import list and no board using it |
| `pieces` -> `plan`, `move`; `plangraph` -> `move` | fine, but `walk` -> `move` and `sight` -> `move.EYE` mean `move` is core, not a reader |
| `blocks.HERE`, `world.HERE`, `solid._PATH`, `run.REPOSITORY_TOOLS` | `__file__`-relative paths that break when a file changes depth (see §5.4) |

---

## 4. Proposed layout

Principles taken from the code: (1) a module that takes arrays and returns arrays (no `World`) is `ground`/`geom`; one that writes blocks is `surface`/`built`/`scenery`/`volume`. (2) Dependencies run one way: `core` and `geom` import nothing above them; `ground` imports `geom`; `surface`, `routes`, `scenery`, `volume`, `built`, `play`, `plan` and `read` import only `core`, `geom` and `ground` (`plan/raster` -> `ground/slope`); `grammar` adds `surface` and `scenery`; `document` imports the build layers and nothing in `play` or `read`. No cycle results: `brittle` -> `surface/marker` replaces `brittle` -> `objectives`, and `plan/raster` -> `ground/slope` replaces `plan` -> `terrain`. (3) Most files land under 250 lines so a C# class maps to one file; the exceptions are the Python-only drawing in `read/sketch.py` (461) and `read/render.py` (169), and the layer-document driver `document/layers.py` (414), none of which a port needs to follow. (4) `solid` (a bridge to `tools/sculpt/solid.py`) and the PIL drawing are Python-only and sit where the port can skip them.

```
pgmvox/
  __init__.py            VERSION; keeps `from .core.blocks import B, DYE` and `from .core.world import World, rng, seed`
  core/                  blocks.py  facing.py  symmetry.py  world.py  studio.py  move.py
  geom/                  polygon.py  polyline.py  mask.py  noise.py
  ground/                field.py  slope.py  rises.py  hollows.py  water.py  shaping.py  outline.py
  surface/               lay.py  paint.py  strata.py  water.py  floating.py  site.py  marker.py
  routes/                find.py  grade.py  lay.py
  scenery/               trees.py  rock.py
  volume/                caves.py  mines.py  solid.py  placed.py
  built/                 frame.py  roof.py  house.py  walls.py  stairs.py  tower.py  facade.py  floors.py  props.py
  grammar/               rules.py  clay.py  brittle/{blueprint.py  style.py  buildings.py  studioplan.py}
  play/                  box.py  teams.py  objectives.py  spawns.py  capture.py  destroy.py  score.py  rooms.py  chests.py  mapxml.py
  plan/                  raster.py  graph.py  course.py
  read/                  walk.py  audit.py  sight.py  plot.py  render.py  sketch.py
  document/              layers.py
  run.py                 unchanged location (keeps `python3 -m pgmvox.run`)
```

Differences from the sketch in the request, all because of what the code holds: `landform.grade` goes to `routes/` (it is a road op); `build_marker` goes to `surface/` (brittle needs it and `grammar` must not import `play`); `Box` stays in `play/` because `Box.cuboid()` builds XML; `plan.Symmetry` and `orient`'s turn code merge into one `core/symmetry.py`; `forms` is dissolved (rock to `scenery/`, floating trim to `surface/floating`, `masonry_tower` to `built/`, placed boxes to `volume/`); `terrain` is split in two by whether it returns arrays (`ground/`) or writes blocks (`surface/`); `shapes` is split by the kind of shape (polygon, polyline, mask) rather than kept whole; `facade` splits into faces and floors; chests leave `props` for `play/chests`.

### 4.1 What moves where (every public name; private helpers and module constants travel with their users)

Line counts are the summed spans of the moved definitions, not the file after the move.



#### `core/` — core — blocks, facing, symmetry, world, physics

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `core/blocks.py` | 207 | `blocks`: B, DYES, DYE, STAIRS, DOORS, FENCES, FENCE_GATES, RAILS, TABLE, info, name, COLOURS, colour, CLIMBABLE, PASSABLE, NOT_GROUND, SIGHT_CLEAR, GRAVITY, FORBIDDEN_IN_PLAY, mask |
| `core/facing.py` | 46 | `orient`: DIRS, NAMES, vec, opposite, stair, ladder, torch, log_axis, slab, door, yaw, rotation16, wall_sign |
| `core/symmetry.py` | 145 | `orient`: OPS, data_table, turn_data, turn_xz, turn_world; `plan`: Symmetry; `objectives`: turn_point, turn_yaw |
| `core/world.py` | 137 | `world`: World, rng, seed |
| `core/studio.py` | 15 | `world`: studio_root, write |
| `core/move.py` | 107 | `move`: EYE, fly, land_at, fall, fall_damage, jump_reach, knockback, solve_launch |

#### `geom/` — geom — shapes and noise, no blocks, no World

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `geom/polygon.py` | 35 | `shapes`: inside, edge_distance, signed_distance, poly_cells, rect_cells |
| `geom/polyline.py` | 63 | `shapes`: seg_distance, polyline, nearest_on, length, point_at, walk_cells, stroke |
| `geom/mask.py` | 55 | `shapes`: disc, ring, ellipse, ellipse_distance, boundary, distance_in, edge_depth, scatter_points |
| `geom/noise.py` | 56 | `noise`: lattice, fbm, line, ragged, ridged, smoothstep, spline |

#### `ground/` — ground — heightfields in, heightfields out (no World)

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `ground/field.py` | 52 | `field`: Ramp, Gauss, Tilt, Noise, terms, mix |
| `ground/slope.py` | 34 | `terrain`: slope_deg, ledge_angle |
| `ground/rises.py` | 117 | `landform`: spire, butte, scarp, terraces, stage, mound, ridge, spire_sites, spire_field; `terrain`: mountain_ring |
| `ground/hollows.py` | 26 | `landform`: crater, canyon |
| `ground/water.py` | 89 | `landform`: Water, watercourse, lake, hold, coast |
| `ground/shaping.py` | 83 | `landform`: smooth_min, smooth_max, join, soften, Step, profile, level, blend |
| `ground/outline.py` | 38 | `shapes`: island; `terrain`: island_bottom, root_depth |

#### `surface/` — surface — stamps terrain into a World

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `surface/lay.py` | 49 | `terrain`: lay |
| `surface/paint.py` | 45 | `terrain`: Paint, first_paint, by_angle, banded, soil_depth |
| `surface/strata.py` | 58 | `terrain`: Strata, bed_offset, beds |
| `surface/water.py` | 41 | `terrain`: fill_water, waterfall |
| `surface/floating.py` | 110 | `terrain`: slab, underside, cloud_deck; `forms`: skirt, root_vines |
| `surface/site.py` | 25 | `build`: site |
| `surface/marker.py` | 32 | `objectives`: build_marker |

#### `routes/` — routes — where a road goes, and laying it

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `routes/grade.py` | 35 | `landform`: grade |
| `routes/find.py` | 170 | `route`: find, simplify, smooth, network, footprint, grades |
| `routes/lay.py` | 88 | `route`: pave, steps, halfstep_levels, halfsteps |

#### `scenery/` — scenery — grown and natural things planted on ground

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `scenery/trees.py` | 126 | `trees`: Tree, library, load, kinds, turned, plant, scatter, dead_tree; `brittle`: tree |
| `scenery/rock.py` | 69 | `forms`: tower, arch |

#### `volume/` — volume — 3D carving and placed solids

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `volume/caves.py` | 100 | `under`: carve, tunnel, chamber, dress_cave, bore |
| `volume/mines.py` | 93 | `under`: gallery_line, gallery, shaft |
| `volume/solid.py` | 30 | `solid`: fill, image, turned, count, Solid |
| `volume/placed.py` | 51 | `forms`: box_cells, placed_box |

#### `built/` — built — made things: buildings, walls, facades, props

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `built/frame.py` | 73 | `build`: Frame, Claims |
| `built/roof.py` | 201 | `build`: FORMS, RoofField, lay_roof |
| `built/house.py` | 133 | `build`: House, house, window_rhythm |
| `built/walls.py` | 73 | `build`: edge_cells, parapet, line_wall |
| `built/stairs.py` | 16 | `build`: stairs, ladder |
| `built/tower.py` | 50 | `forms`: masonry_tower |
| `built/facade.py` | 145 | `facade`: DARK, band, courses, flutes, panels, slits, checker, glyph_row, word, windows, faces, extrude, top_course, coffer, concrete |
| `built/floors.py` | 74 | `facade`: Cell, border, medallion, corners, diamonds, kilim_steps, star, stripes, tiles, cross, rings, first_of, carpet |
| `built/props.py` | 125 | `props`: stall, stalls, lamp, lamps, brazier, rubble, crop_field, scarecrow |

#### `grammar/` — grammar — the structural-board grammar and its styles

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `grammar/rules.py` | 234 | `grammar`: DIRS, Section, split, tile, Ground, spec, Sunk, Accent, Face, Lot, Style, lay |
| `grammar/clay.py` | 158 | `clay`: squares, style |
| `grammar/brittle/blueprint.py` | 79 | `brittle`: CELL, LAND, Cell, turn_cells, fan, heights, pieces, sections |
| `grammar/brittle/style.py` | 147 | `brittle`: build, ground, bed, sand, cap |
| `grammar/brittle/buildings.py` | 185 | `brittle`: storey, tower, house, heart |
| `grammar/brittle/studioplan.py` | 50 | `studioplan`: load, unit, placement, facing |

#### `play/` — play — what the map is played for: objectives, XML

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `play/box.py` | 37 | `objectives`: Box |
| `play/objectives.py` | 101 | `objectives`: Objective, Objectives, centre_el |
| `play/teams.py` | 33 | `objectives`: DYES, Teams |
| `play/spawns.py` | 51 | `objectives`: Spawn, Observer |
| `play/capture.py` | 154 | `objectives`: Hill, Flag, Wool |
| `play/destroy.py` | 79 | `objectives`: Destroyable, Core |
| `play/score.py` | 58 | `objectives`: ScoreBox, Portal |
| `play/rooms.py` | 35 | `objectives`: wool_rooms, float_problems, FLOAT |
| `play/chests.py` | 49 | `props`: wool_chests, studio_defence, defence_chests, laid |
| `play/mapxml.py` | 150 | `mapxml`: E, point, cuboid, cylinder, circle, below, negative, union, item, duration, Doc |

#### `read/` — read — checks and pictures of a plan or built world

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `read/walk.py` | 147 | `walk`: MoveRules, classes, standing, walk, nearest, unreached, no_stand_above, catchers, gap_cleared |
| `read/audit.py` | 58 | `audit`: footing, loose_water |
| `read/sight.py` | 51 | `sight`: line_clear, plan_opaque, voxel_opaque, eye, target, visibility, hidden |
| `read/plot.py` | 81 | `plot`: OutOfPlot, Canvas, load, draw, check_alone, verdict |
| `read/render.py` | 169 | `render`: xray_shell, iso, elevation, cutaway, trim |
| `read/sketch.py` | 461 | `sketch`: TEAM, font, pale, dark, Panel, MapPanel, SectionPanel, TablePanel, Sheet |

#### `plan/` — plan — the plan raster and its walks

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `plan/raster.py` | 124 | `plan`: Raster |
| `plan/graph.py` | 232 | `plangraph`: PlanRules, jumps, node, walkable, graph, measure, dijkstra, route, path, arrivals, pad_edges |
| `plan/course.py` | 143 | `pieces`: box, Piece, Course, gap, lands_at, clears |

#### `document/` — document — layer-document driver

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `document/layers.py` | 414 | `document`: Step, Built, block, Ctx, expr, area_distance, made_cells, made_mask, ground, build |

#### `run/` — run — the build pipeline

| new module | ~lines | takes (old module: names) |
|---|---:|---|
| `run.py` | 101 | `run`: world_folder, run, main |

Notes on the split: the shared private helpers get an explicit home. `landform._apply` and `MODES` (used by `profile`, `level` and `mound`, landform.py:400-421), `_radial` (221; `spire`, `butte`, `stage`), `_sample` (99) and `_downhill` (122) (`watercourse`, `canyon`, `grade`, which land in three different new modules) move to one `ground/_support.py` that `rises`, `hollows`, `water`, `shaping` and `routes/grade` import. `objectives._stands` (97) and the marker constants (`MARKER_*`, `_SIDES`, `_CORNERS`) travel with their only user. `terrain._within` (74) goes with `slope_deg`.

---

## 5. Migration cost

### 5.1 What a caller edit is

There are 155 files outside `lib/pgmvox` and `lib/tests` that touch the library (the 22 hashed folders — 7 boards, 3 examples, 2 ports, 10 trials — plus `examples/drop`, `boards/common.py`, `check.py` and `opus55-freeform-lantern-karst`). Today they hold 688 imported names in about 435 import statements and 4,332 references. **2,151 of those references are `B`, `World`, `rng` through `from pgmvox import ...` and need no edit as long as `__init__.py` keeps its re-exports of `B`, `DYE`, `World`, `rng`, `seed`** (that is the package's public face, not a compatibility path; `B` alone is 1,996 sites in 23 boards).

Per move, the real edit is the import statement: a `from pgmvox.terrain import lay` line becomes `from pgmvox.surface.lay import lay`. Call sites change only where the module is split and the caller reaches it by alias (`T.lay`, `LF.mound`, `F.border` become `L.lay`, `RS.mound`, `FL.border`), counted below as "alias-qualified call sites". A name imported directly never changes at the call site. Splitting one module into several turns one import statement into up to as many statements; a caller of `terrain` that uses lay, Paint and Strata gets three lines.

### 5.2 Per new module

`*` marks an old module whose names go to more than one new module (the callers of that module are the ones that gain import lines). Counts are board-script side only (including the trials' copies); tests are in the last column; library-internal imports (85 relative `from .` lines in the 34 modules) are extra and mechanical.

| new module | from | boards | files | import stmts | alias-qualified call sites | test sites |
|---|---|---:|---:|---:|---:|---:|
| `core/blocks` | `blocks` | 24 | 56 | 15 | 0 | 280 |
| `core/facing` | `orient`* | 14 | 18 | 18 | 0 | 15 |
| `core/move` | `move` | 1 | 1 | 1 | 0 | 11 |
| `core/studio` | `world`* | 0 | 0 | 0 | 0 | 0 |
| `core/symmetry` | `objectives`*, `orient`*, `plan`* | 20 | 37 | 37 | 0 | 20 |
| `core/world` | `world`* | 23 | 72 | 0 | 0 | 59 |
| `geom/mask` | `shapes`* | 11 | 17 | 18 | 22 | 11 |
| `geom/noise` | `noise` | 14 | 22 | 26 | 0 | 32 |
| `geom/polygon` | `shapes`* | 9 | 10 | 10 | 9 | 5 |
| `geom/polyline` | `shapes`* | 7 | 12 | 12 | 30 | 6 |
| `ground/field` | `field` | 2 | 2 | 2 | 0 | 13 |
| `ground/hollows` | `landform`* | 2 | 2 | 2 | 2 | 2 |
| `ground/outline` | `shapes`*, `terrain`* | 8 | 8 | 11 | 8 | 4 |
| `ground/rises` | `landform`*, `terrain`* | 7 | 7 | 7 | 17 | 16 |
| `ground/shaping` | `landform`* | 4 | 4 | 4 | 14 | 23 |
| `ground/slope` | `terrain`* | 8 | 9 | 9 | 3 | 4 |
| `ground/water` | `landform`* | 3 | 3 | 3 | 10 | 6 |
| `surface/floating` | `forms`*, `terrain`* | 8 | 9 | 11 | 14 | 2 |
| `surface/lay` | `terrain`* | 9 | 9 | 9 | 7 | 3 |
| `surface/marker` | `objectives`* | 0 | 0 | 0 | 0 | 0 |
| `surface/paint` | `terrain`* | 7 | 7 | 7 | 14 | 3 |
| `surface/site` | `build`* | 5 | 5 | 5 | 6 | 0 |
| `surface/strata` | `terrain`* | 12 | 12 | 12 | 27 | 3 |
| `surface/water` | `terrain`* | 4 | 4 | 4 | 3 | 3 |
| `routes/find` | `route`* | 3 | 3 | 3 | 10 | 8 |
| `routes/grade` | `landform`* | 6 | 6 | 6 | 7 | 5 |
| `routes/lay` | `route`* | 8 | 8 | 8 | 13 | 3 |
| `scenery/rock` | `forms`* | 3 | 3 | 3 | 3 | 2 |
| `scenery/trees` | `brittle`*, `trees` | 11 | 11 | 11 | 40 | 6 |
| `volume/caves` | `under`* | 4 | 4 | 4 | 10 | 2 |
| `volume/mines` | `under`* | 3 | 6 | 7 | 10 | 3 |
| `volume/placed` | `forms`* | 0 | 0 | 0 | 0 | 0 |
| `volume/solid` | `solid` | 0 | 0 | 0 | 0 | 0 |
| `built/facade` | `facade`* | 5 | 5 | 5 | 28 | 0 |
| `built/floors` | `facade`* | 8 | 8 | 8 | 70 | 0 |
| `built/frame` | `build`* | 8 | 9 | 9 | 0 | 4 |
| `built/house` | `build`* | 11 | 17 | 17 | 20 | 7 |
| `built/props` | `props`* | 11 | 12 | 12 | 31 | 4 |
| `built/roof` | `build`* | 2 | 2 | 2 | 3 | 4 |
| `built/stairs` | `build`* | 2 | 2 | 2 | 2 | 0 |
| `built/tower` | `forms`* | 3 | 3 | 3 | 3 | 1 |
| `built/walls` | `build`* | 5 | 5 | 5 | 7 | 5 |
| `grammar/brittle/blueprint` | `brittle`* | 3 | 7 | 7 | 17 | 15 |
| `grammar/brittle/buildings` | `brittle`* | 3 | 3 | 3 | 0 | 1 |
| `grammar/brittle/studioplan` | `studioplan` | 1 | 1 | 1 | 0 | 1 |
| `grammar/brittle/style` | `brittle`* | 3 | 3 | 3 | 0 | 6 |
| `grammar/clay` | `clay` | 1 | 1 | 1 | 0 | 2 |
| `grammar/rules` | `grammar` | 1 | 1 | 1 | 0 | 16 |
| `play/box` | `objectives`* | 19 | 19 | 19 | 0 | 11 |
| `play/capture` | `objectives`* | 11 | 25 | 25 | 0 | 7 |
| `play/chests` | `props`* | 7 | 7 | 7 | 13 | 5 |
| `play/destroy` | `objectives`* | 7 | 8 | 8 | 0 | 6 |
| `play/mapxml` | `mapxml` | 20 | 20 | 20 | 0 | 20 |
| `play/objectives` | `objectives`* | 19 | 19 | 19 | 0 | 3 |
| `play/rooms` | `objectives`* | 1 | 1 | 1 | 0 | 0 |
| `play/score` | `objectives`* | 0 | 0 | 0 | 0 | 0 |
| `play/spawns` | `objectives`* | 19 | 28 | 28 | 0 | 5 |
| `play/teams` | `objectives`* | 19 | 29 | 29 | 0 | 3 |
| `plan/course` | `pieces` | 1 | 1 | 1 | 0 | 6 |
| `plan/graph` | `plangraph` | 19 | 20 | 21 | 0 | 17 |
| `plan/raster` | `plan`* | 18 | 18 | 18 | 0 | 4 |
| `read/audit` | `audit` | 20 | 20 | 20 | 0 | 11 |
| `read/render` | `render` | 22 | 22 | 22 | 0 | 1 |
| `read/sketch` | `sketch` | 21 | 38 | 38 | 0 | 5 |
| `read/plot` | `plot` | 0 | 0 | 0 | 0 | 0 |
| `read/sight` | `sight` | 10 | 13 | 13 | 0 | 7 |
| `read/walk` | `walk` | 20 | 20 | 20 | 0 | 20 |
| `document/layers` | `document` | 0 | 0 | 0 | 0 | 0 |
| `run` | `run` | 1 | 1 | 1 | 0 | 1 |

### 5.3 Suggested order, one commit each, `python3 check.py` after each

Each step moves code and rewrites every caller in the same commit, per the repository's rule: boards, `lib/tests/test_pgmvox.py` (37 import lines, 766 references), `lib/README.md` and `lib/AGENT-GUIDE.md` (the two documents `check.py` puts through the prose gate), and the five `analysis/freeform-vs-studio/pages/riftwater-layers/make/*.py` scripts. Order is leaf-consumers first, base last: new modules of an early step still import the old flat base modules (`from .. import shapes`), so no step needs a temporary alias, and the highest fan-in step (core/geom, pure renames with no judgment) is last and mechanical.

| step | what | board folders | files | import stmts rewritten | alias-qualified call sites | test sites |
|---|---|---:|---:|---:|---:|---:|
| 0 | Prune the `DEAD` names (§2.3) that are not mode vocabulary; fix the `README` rows for `pad_edges`, `brittle.tower/heart`, `walk` | 0 | 0 | 0 | 0 | 0 |
| 1 | Dedupe in place, no module moves: one rectangle order (drop `Raster.rect` 61 call sites in 15 folders, `pieces.box` 10 sites in 1, keep corner order), `build.edge_cells` -> `shapes.boundary` (3 sites in 2 folders), one `DIRS`, `Box.cuboid` via `mapxml.cuboid`, one jump width | about 16 | about 40 | 1 | about 75 argument-order edits | about 10 |
| A | `scenery/ volume/ routes/` | 14 | 23 | 36 | 93 | 29 |
| B | `ground/ surface/` | 15 | 27 | 45 | 125 | 82 |
| C | `built/ grammar/` | 18 | 33 | 53 | 181 | 66 |
| D | `play/` | 21 | 62 | 64 | 13 | 60 |
| E | `plan/ read/` | 24 | 98 | 132 | 0 | 71 |
| F | `core/ geom/` | 25 | 105 | 113 | 61 | 439 |
| G | `document/ run` | 1 | 1 | 1 | 0 | 1 |

Step 0 cannot move a hash (no caller exists). Step 1 can, because it changes code rather than paths; its jump-width and rule-class merge also moves the walk numbers in `examples/*` snapshots if done wrongly, which `python3 check.py` shows as a snapshot diff, so do the jump-width merge last or leave it for the port. Steps A to G are path changes only: `rng` streams are named per board and stream, not per module (README: "moving a function does not change what it draws"), so every hash must stay identical and `--update` must never be needed. A hash that moves in A-G is a bug in the move.

Cost shape: A and B are small (14-15 board folders, under 50 statements each) and carry most of the judgment (the `terrain`/`landform` split). C and D touch 18-21 folders; D gains import lines because `objectives` splits into seven files (`objectives` has 37 importing files today, the split makes about 128 import statements; keeping the objective classes together in one `play/objectives.py` and extracting only `box`, `teams`, `rooms`, `chests`, `mapxml` saves about 40 of those, at the cost of a 446-line file; the `play/` class split is worth it only for the port). E is the widest by files (98) but changes only module paths. F touches the most files (105) and the most tests (439 test references) but 2,151 references need nothing.

Totals: about 445 import statements rewritten once each (155 files, many in several steps), 473 alias-qualified call sites, about 770 test references.

### 5.4 Things that break silently on a move

| hazard | where | action |
|---|---|---|
| `__file__`-relative paths grow one `..` per package level | `blocks.py:23,214` (`HERE/data/blocks.json`), `world.py:23,181,186` (`data/write_world.cs`, the studio checkout), `solid.py:19` (`../../../tools/sculpt/solid.py`), `run.py:34,68` | keep `data/` at the package root and compute `PACKAGE_ROOT` and `REPO_ROOT` once in `core/studio.py`; `blocks` and `solid` read them |
| `python3 -m pgmvox.run` is documented in `lib/README.md` (lines 45, 499, 500) and `check.py:78` imports `pgmvox.run.run` | `run.py` | leave it at the package root |
| `solid.py` publishes its names with `globals()[_name] = getattr(_mod, _name)` (solid.py:27) | `volume/solid.py` | keep as is; callers import `volume.solid` |
| `document.py:443` `getattr(FA, name)` dispatches facade patterns by string | `built/facade.py` | pass the new module or keep the five `DOC` names there; do not prune them as dead |
| `trees.library()` and `run.py` reach the studio through `world.studio_root` | `scenery/trees.py`, `run.py` | import from `core/studio` |
| names that clash after a move must not shadow a module (`walk.walk`, `plangraph.route`, `trees.load`) | `read/walk.py`, `plan/graph.py` | keep as is; a package named `walk/` would shadow the function on `from pgmvox.read import walk` |
| the finished `opus55-freeform-*` boards | only `lantern-karst` imports (`props`) | edit that one line (`props` -> `built/props` or `play/chests`) |

### 5.5 What the review did not do

It did not run `check.py` (read-only, and it writes to scratch folders); it did not build any board. All counts are static. Class methods and `getattr` access to instance attributes are not in the call-site counts, so a class listed `0` could still be used through an instance it never names; none of the 24 `DEAD` names is a class used that way except `Flag` and `Portal`, which are constructed by name and therefore would show in an import. 
