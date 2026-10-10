# Hollow Mesa: how the script builds the board

Board: `freeform/opus55-freeform-hollow-mesa/` (a DTC board: two banded mesas across a canyon, the town of Gilt in the canyon round a spring, a Wash climbing to the plateau, each core floating over a well and a hole through its mesa). Everything below was read from `scripts/` and measured by running a scratch copy; nothing in the board was edited.

## Does the board use pgmvox?

**No.** Its imports are `mc` (World, block ids), `noise`, `plan`, `terrain`, `underground`, `buildings`, `dressing`, `rotate` and numpy/scipy (`gen.py:6-14`, `terrain.py:8-11`, `underground.py:6-10`, `buildings.py:9-13`, `dressing.py:8-15`). `grep -rn pgmvox` over the board folder finds nothing. `house.py` (288 lines) is imported by no file in the pipeline.

pgmvox was distilled from boards like this one: `lib/pgmvox/noise.py` carries the same `lattice`, `fbm`, `smoothstep` and `spline` as `scripts/noise.py` (diffed: only `ridged` was added and `polyline_distance` moved out), and `lib/pgmvox/world.py` has the same `World` API (`set`, `get`, `id`, `fill`, `top`, `chest`, `sign`, `save`) as `scripts/mc.py:134-208`. So a noise seed in this board means the same field in pgmvox.

## How it was measured

| Check | Result |
|---|---|
| Plain run of a scratch copy (`gen.py <dir>`, 1.9 s wall) vs the committed `world/region` files | 1,792,366 non-air blocks in both; 0 blocks in one and not the other; 0 id or data mismatches |
| Instrumented run (hooks on `World.set`/`fill` plus a diff checkpoint around every step, for writes that bypass them) vs the plain run | `volume.bin` and `tiles.json` byte-identical |
| Red half vs blue half | 896,183 non-air blocks each |
| Instrumented run time | 90 s, against 1.9 s plain (overhead is the checkpoints, not the board) |

`REPORT.md` quotes 1,794,462 blocks; the committed world has 1,792,366. The report's number does not match the world the scripts now produce (cause not established). `PLAN.md` and the "What I wanted" table in `REPORT.md` still describe the core on a stub in the cavern; `underground.py:70-90` is current.

Ownership is the last step that wrote the cell. A later write replaces the owner, and a cell later carved to air counts for nobody. The scratch copy and tools are in `/tmp/hollow-mesa-anatomy/` (`instrument.py`, `aggregate.py`, `classify.py`).

## The pipeline in the order `gen.py` runs it

The board is generated for the **red half only** (x < 0, 130 x 200 columns, 24,564 of them land) and then turned. Blocks are counted for the whole world; each is twice its red-half count, except the nine recoloured flag blocks, which belong to the recolour step in the blue half.

| # | Step | Where | What it builds | How it writes | Blocks left | Share |
|---|---|---|---|---|---|---|
| 0 | `World(...)`, `terrain.Land()` | `gen.py:33-34`, `mc.py:134-`, `terrain.py:17-26` | the volume: x -130..129, y 0..127, z -100..99 (260 x 128 x 200); red-half grids | two numpy arrays (ids `uint16`, data `uint8`), a biome grid | - | - |
| 1 | `terrain.build_heights` | `gen.py:35`, `terrain.py:85-173` | the heightfield `L.H` (38..96), water, land mask: a **cross-section** west of an odd centreline (`plan.canyon_x`, `plan.py:28`): floor y41 (26 wide), lower cliff to the **bench** y57 (10 wide), upper cliff to the **plateau** y74, each edge wandering by its own noise; the scarp at x about -96 (+6) with gullies at z 0, 34, -40; the **Wash** (z = 51 + 4 sin(x/10), x -104..-18, floor 41 -> 74); High Butte (-125, 0) top 94 and Table Rock (-80, 86) top 86; 20 spires and hoodoos (13 drawn from a seeded scatter in the Needles at x -80..-52, z -98..-60, 7 hand-placed); three level pads (fort -108,4; Rancho -104,74; headframe -78,-30); the creek and the spring pool (-0.5,-0.5, r 5.2); the island outline | numpy whole-array operations; no blocks | 0 | - |
| 2 | `terrain.build_underside` | `gen.py:36`, `terrain.py:176-183` | the bottom of each column (thickness grows with distance from the island's edge) | numpy, no blocks | 0 | - |
| 3 | `terrain.write_land` | `gen.py:37`, `terrain.py:223-282` | every column from its underside to its surface: stone below y28, clay beds above (a bed table drawn once from seed 77, undulating by noise), red sand / orange clay / soil patches / grass on the top where the slope is under 40 degrees, the creek bed and water | a **heightfield, then columns**: a Python loop over 24,564 columns assigning numpy slices (`col_i[y] = ...`, `terrain.py:241-282`); it does not call `World.set` | **1,742,764** | **97.23%** |
| 4 | `terrain.write_falls` | `gen.py:38`, `terrain.py:285-298` | the creek pouring off the island's north and south edges | `w.set` in a loop over the creek columns | 96 | 0.01% |
| 5 | `terrain.sky_arch` | `gen.py:39`, `terrain.py:301-332` | the Sky Arch, z -3..2 (ragged rows at -4 and 3), x -60..-1 (blue: 0..59): deck y76 at the crown to y74 at the rims, underside 5 blocks thick at the crown to about 23 at the rims; banded like the cliffs | `w.set` in a loop over a computed shape (x, z, y); its height is kept apart from `L.H` so the ground under it stays the ground | 5,888 | 0.33% |
| 6 | `green_mask`, `terrain.paint_biomes` | `gen.py:17-24,40-41`, `terrain.py:335-339` | Mesa biome (37) everywhere, Plains (1) on the creek banks and round the Grove, Acacia Flat and Rancho | a biome array | 0 | - |
| 7 | `underground.cavern` | `gen.py:45`, `underground.py:48-67` | **the Throat**: two ellipsoids at (-70,-24) and (-74,-20), floor y47; a paved floor; **the hole**, a cylinder r 3.2 at (-65,-24) from y47 through the island's underside (about 40 blocks of rock) to y0 | loops over a bounding box with an inequality, `w.set(AIR)`; floor and hole jitter drawn from a module RNG | 510 | 0.03% |
| 8 | `underground.chimney` | `underground.py:229-238,37-45` | the Chimney: a tube of 7 points (-30,41,-14) to (-67,47,-18), radius 1.9..2.6, mouth a cleft up the wall | a spline sampled every 0.4 block, one ellipsoid carve per sample | 0 (only air) | - |
| 9 | `underground.adit` | `underground.py:251-257,134-199` | Bench Adit: a timbered drift (-48,57,-34) to (-61,50,-33), portal, breakout onto the catwalk | a polyline walked cell by cell: air, floor, timber sets every 4, rails, ore flecks | 162 | 0.01% |
| 10 | `underground.workings` | `underground.py:241-248` | Old Workings: a drift (-80,47,-20) to (-92,47,-2), a chest at (-92,47,-3) | same `gallery` | 238 | 0.01% |
| 11 | `underground.catwalk` | `underground.py:93-131` | planks on log brackets round the north and east walls at y50, a stair down at the west end, four hanging lamps | loops along a hand-listed path; tests `w.id` for air before each write; lamps scan up for the roof | 178 | 0.01% |
| 12 | `underground.shaft` | `underground.py:202-226` | the shaft at (-78,-30) from y47 to 75: 3 x 3 inside, dark-oak corners, plank lining, ladder | loops over y and a 5 x 5 ring | 850 | 0.05% |
| 13 | `underground.core` | `underground.py:70-90` | **the core**: obsidian x -67..-64, y79..82, z -26..-23, lava 2 x 2 x 2 inside; a 2 x 2 **well** at x -66..-65, z -25..-24 cut from y47 up to the ground (y73); a ring of brown clay at y73 round it | triple loop of `w.set` | 152 | 0.01% |
| 14 | `underground.south_drift` | `underground.py:260-271` | South Drift: a drift (-39,57,80) to (-52,57,83), portal, chest (-53,57,83), cauldron "ore cart" (-49,57,82) | `gallery`, `portal`, `w.chest`, `w.set` | 204 | 0.01% |
| 15 | `buildings.build` | `gen.py:49`, `buildings.py:804-860` | everything built, in this order: plaza and spring, 11 Main Street stores, 8 adobes, chapel, water tower, tipple, Mule Trail, tram and trestle, headframe, fort, Rancho, windmill, tank, 4 ladders, 8 paved routes, the door-wall pass | see rows 15a-15i | 25,847 | 1.44% |
| 15a | `spring` | `buildings.py:370-396` | the plaza (disc r 12.5 at (-0.5,-0.5)), kerb ring, pump, trough, benches | loop over a disc with `set_ground` (levels and paints) | 260 | 0.01% |
| 15b | `false_front` x 11 | `buildings.py:102-217,811-827` | Main Street's stores: west row x -31..-18, east row x -16..-7, z -90..-28; hotel, general store, house, saloon, assay, feed store, bank, house, barber, rooms, sheriff | a template function: loops over a box, per-kind furnishing | 9,540 | 0.53% |
| 15c | `adobe` x 8 | `buildings.py:220-298,829-834` | the Adobe Quarter, x -24..-1, z 12..86 | same shape of function | 3,756 | 0.21% |
| 15d | `chapel`, `water_tower` | `buildings.py:301-367` | chapel (-10..-2, 42..49) with bell gable; water tower at (-19,-14), top y52 | `adobe` + extra loops; loops over legs and a disc | 628 + 1,060 | 0.09% |
| 15e | `tipple` | `buildings.py:518-597` | timber tower (-20..-15, 23..29) from y41 to 57, switchback stair inside, slab chute and ore bin to x -2 | hand-written loops, a `while` for the switchback | 528 | 0.03% |
| 15f | `mule_trail`, `tram`, `trestle` | `buildings.py:599-627,454-515` | stairs cut into the wall z -50 up to the plateau; 114 rail cells on the bench from (-44,58,-33) to (-34,58,80); trestle bents across the Wash near (-32,51) | a loop walking z and writing a stair per step; rail data from each cell's neighbours; bents every 4 cells down to the ground | 640 + 230 + 580 | 0.08% |
| 15g | `headframe`, `fort`, `rancho`, `windmill`, `tank`, `ladder_up` | `buildings.py:644-801,843-854` | headframe (-78,-30) 14 high; Fort Ochre x -113..-97, z -8..16, floor y75, with quarters, tower, flag, wagon; Rancho house, barn, corral, windmill, tank; windmill (-84,-62), tank (-82,-54); ladders up both tiers of High Butte and Table Rock | loops over boxes and rings; `ladder_up` walks west to the first rock face | 326 + 3,005 + 1,948 + 166 + 138 + 50 | 0.31% |
| 15h | `pave` x 8 | `buildings.py:399-424,856-858` | Fort Road, Rim Path, Grove Track, Needles Path, Ranch Road, Wash Track, Main Street, Lower Street | a spline per route; for each cell a `set_ground` that levels and paints, skipping footprints | 2,962 | 0.17% |
| 15i | `wall_beside_doors` | `buildings.py:866-882` | a wall block beside every door instead of a pane (15 panes per half) | **a post-pass over the whole array** (`np.nonzero(np.isin(...))`), writing `w.ids` directly | 30 | 0.00% |
| 16 | `dressing.build` | `gen.py:51`, `dressing.py:241-281` | in this order: the blocked mask (reads the world), ground greening at 3 places, 3 scattered woods and an orchard, 7 lone trees, 16 boulders, cemetery, hitching rails, 2 wagons, the town sign, scrub | see below | 15,468 | 0.86% |
| 16a | trees | `dressing.py:32-126` | 535 `plant` calls, 40 trees stand (Grove 16 wide at (-88,-58), Acacia Flat at (-66,78), creek banks, 2 orchard trees, 7 lone) | `plant` **stamps a recorded block list** from `trees.json` (94 hand-built trees by rockymine) with a turn, after reading the world around it | 10,360 | 0.58% |
| 16b | `green_ground`, `scrub`, `boulder`, small props | `dressing.py:104-238` | grass under the woods, dead bushes, cacti, tall grass, flowers; 16 boulders; Boot Hill, rails, wagons, sign | loops that test the world, then `w.set` | 5,108 | 0.28% |
| 17 | `rotate_world` | `gen.py:53`, `rotate.py:40-56` | blue's whole half | **a rotation of the other half** (see below) | (copy) | - |
| 18 | blue wool | `gen.py:54-59` | the nine wool blocks of the fort's flag, recoloured red -> blue | boolean mask over a box | 9 | 0.00% |
| 19 | `World.save`, `write_world.cs` | `gen.py:60`, `mc.py:197-`, `build.sh:15-17` | `volume.bin`, `tiles.json`, `level.json`, then region files | binary dump, then the studio's Anvil writer | - | - |

No step is a hand-placed block list. The nearest are small runs of literal `w.set` calls: the pump and benches (`buildings.py:392-395`), the chapel's bell (`buildings.py:309-313`), the core's ring (`underground.py:86-89`). The one place a recorded block list is stamped is a tree.

## How `map.xml` is produced

**It is not produced.** `scripts/map.xml` (71 lines) is a hand-written file, copied verbatim to `world/map.xml` by `build.sh:17` (the two are identical). No Python file writes or reads it; `renders.py:14` only passes its path to the renderer.

Its numbers are typed twice. Measured against the world:

| In `map.xml` | Duplicates | Check |
|---|---|---|
| core regions `-67,79,-26`..`-63,83,-22` and `63,79,22`..`67,83,26` (lines 59-60) | `plan.CORE` (`plan.py:45`), the blocks `core()` writes | exact, and blue is the exact half-turn |
| spawn points `-101.5,76,6.5` / `101.5,76,-6.5` (53-54) | the fort's floor y75 (`buildings.fort`); `plan.SPAWN = (-108,75,4)` is a third, different number used only by the sketch renders | consistent |
| `red-spawn` rect `-113,-8`..`-96,17` (57) | the fort's walls (`buildings.py:711`, blocks -113..-97 by -8..16) | exact |
| `blue-spawn` rect `96,-16`..`113,9` (58) | the blue fort, which the half-turn builds at z -17..7 | **off by one: the exact half-turn of red's rect is z -17..8**; checked against the world (sandstone walls at z -17 and 7, x 96 and 112, y77) |

What the file states: DTC, two teams of 16, one kit, spawns, two cores with `leak="5"`, spawn protection (enter and edit), a `no-void` filter applied to `everywhere` ("You may not build over the void, nor plug the Throat!"), `maxbuildheight` 100.

## How the second team's half is produced

`rotate.rotate_world` (`rotate.py:40-56`) asserts the volume is centred (so (x, z) -> (-1 - x, -1 - z) maps it onto itself), then:

- `w.ids[half:] = red_i[::-1, :, ::-1]` and `w.dat[half:] = t[red_i, red_d][::-1, :, ::-1]` (`rotate.py:49-50`): the red half reversed in x and z, with every block's data value passed through a 256 x 16 table (`rotate.py:13-37`) that turns stairs, doors, torches, ladders, chests, furnaces, dispensers, signs, banners, pumpkins, beds, trapdoors, vines, rails, repeaters and fence gates;
- biomes reversed the same way (`rotate.py:51`); tile entities (chests, signs) copied with turned coordinates (`rotate.py:52-56`);
- then the nine red flag blocks that the copy brought to the blue fort are recoloured (`gen.py:54-59`).

Anything written at x >= 0 before the turn is overwritten, so every builder is guarded: `carve_ellipsoid` skips `x >= -1` (`underground.py:26`), `pave` skips `X >= 0` (`buildings.py:410`), `plant` and `boulder` skip `X >= 0` (`dressing.py:41,139`). The centreline is odd about the centre (`plan.py:28-30`), so the canyon, the creek, the plaza and the spring map onto themselves; the plaza is two half-discs, one per half.

## Block ownership, measured

World totals (both halves). "Exposed" is a block with an air neighbour, a proxy for what a player can touch. Every row sums to 1,792,366.

| Step | Blocks left | Share | Exposed | Class |
|---|---|---|---|---|
| terrain.write_land | 1,742,764 | 97.233% | 132,888 | A |
| terrain.write_falls | 96 | 0.005% | 96 | A |
| terrain.sky_arch | 5,888 | 0.329% | 2,478 | A |
| underground.cavern | 510 | 0.028% | 500 | A |
| underground.adit | 162 | 0.009% | 142 | A |
| underground.workings | 238 | 0.013% | 186 | A |
| underground.catwalk | 178 | 0.010% | 178 | A |
| underground.shaft | 850 | 0.047% | 638 | A |
| underground.core | 152 | 0.008% | 136 | A |
| underground.south_drift | 204 | 0.011% | 162 | A |
| buildings.spring | 260 | 0.015% | 226 | B |
| false_front (Main Street stores) | 9,540 | 0.532% | 8,640 | B |
| adobe (Adobe Quarter) | 3,756 | 0.210% | 3,160 | B |
| buildings.chapel | 628 | 0.035% | 544 | B |
| buildings.water_tower | 1,060 | 0.059% | 788 | B |
| buildings.tipple | 528 | 0.029% | 512 | C |
| buildings.mule_trail | 640 | 0.036% | 502 | A |
| buildings.tram (rails) | 230 | 0.013% | 230 | A |
| buildings.trestle | 580 | 0.032% | 558 | B |
| buildings.headframe | 326 | 0.018% | 318 | B |
| buildings.fort (incl. quarters 1,408) | 3,005 | 0.168% | 2,485 | B |
| buildings.rancho (house 810, barn 824) | 1,948 | 0.109% | 1,698 | B |
| buildings.windmill | 166 | 0.009% | 164 | B |
| buildings.tank | 138 | 0.008% | 138 | B |
| buildings.ladder_up | 50 | 0.003% | 50 | A |
| buildings.pave | 2,962 | 0.165% | 2,898 | A |
| buildings.wall_beside_doors | 30 | 0.002% | 30 | B |
| dressing.green_ground | 2,988 | 0.167% | 2,266 | A |
| dressing.wood Olive Grove | 4,202 | 0.234% | 4,136 | A |
| dressing.wood Acacia Flat | 2,272 | 0.127% | 2,252 | A |
| dressing.wood creek banks | 1,454 | 0.081% | 1,446 | A |
| dressing.orchard | 342 | 0.019% | 334 | A |
| dressing.plant (7 lone trees) | 2,090 | 0.117% | 2,088 | A |
| dressing.boulder | 438 | 0.024% | 204 | A |
| dressing.cemetery / hitching / wagon | 86 / 66 / 88 | 0.014% | 230 | B |
| dressing.town_sign | 6 | 0.000% | 6 | A |
| dressing.scrub | 1,436 | 0.080% | 1,436 | A |
| gen.py blue-wool recolour | 9 | 0.001% | 9 | A |

`chimney`, `build_heights`, `build_underside` and `paint_biomes` leave no blocks of their own. Per-kind Main Street figures: store 2,932, hotel 2,012, bank 1,306, house 1,290, saloon 1,216, assay 784 (graded porch ground and furnishing included). Grading under a building (`set_ground`, 4,312 calls) is attributed to the building that asked.

**97.2% of the world is one rule, `write_land`**: solid rock in beds under every land column. The 49,602 blocks outside it are the things a player reads as built or planted.

## Classification

A = a layer operation with parameters. B = a library template plus a placement. C = bespoke (a `made` block volume). The assignment is per step, in the table above; the JSON states the same assignment per layer. A one-use template that is a plain parameter set (water tower, headframe, fort, chapel, plaza, cemetery, trestle) is counted B; the sensitivity is below.

| View | A | B | C |
|---|---|---|---|
| All non-air blocks (1,792,366) | 1,770,161 (98.761%) | 21,677 (1.209%) | 528 (0.029%) |
| Without the ground bulk (49,602) | 27,397 (55.2%) | 21,677 (43.7%) | 528 (1.1%) |
| Exposed blocks (174,752) | 155,261 (88.9%) | 18,979 (10.9%) | 512 (0.3%) |
| Top-down columns (49,132; the block a player sees from above) | 43,507 (88.6%) | 5,439 (11.1%) | 186 (0.4%) |

If every single-use structure were counted C instead (tipple, headframe, fort, water tower, chapel, plaza, trestle, catwalk): 6,565 blocks, 0.37% of the world, 13.2% of the non-ground blocks.

By what a player sees from above: terrain 68.8% of columns (all A), dressing 14.2% (A 13.9, B 0.3), canyon town 13.7% (A 5.7, B 7.6, C 0.4), mesa structures 3.2% (B), underground 0.2% (A; 1.1% of exposed blocks).

## What the steps depend on

The steps share mutable state, and that is what an ordered document has to keep.

- **The ground is rewritten as buildings are placed.** `set_ground` changes `L.H` (`buildings.py:41`), as does `mule_trail` (`buildings.py:616`); later steps read it: `floor_of` (median under a footprint, `buildings.py:63`), `pave`, `windmill`, `tank`, `plant`, `boulder`, `scrub`.
- **Claims.** `L.footprints` and `L.things` (`buildings.py:44-60`) are read by `pave` (`415`) and, as `L.blocked`, by every tree and prop (`dressing.py:58-83`).
- **Four module-level random streams are consumed in call order**: `terrain.RNG` (seed 2024, `terrain.py:14`: one array draw in `write_land`, then one draw per cell in `sky_arch`), `underground.RNG` (4321), `buildings.RNG` (909), `dressing.RNG` (1717); the noise fields, woods and boulders use their own seeded generators. Reordering two steps changes the world without changing any parameter.
- **Steps that read the world they are writing**: `set_ground` (`buildings.py:32-39`), `furnish` (`195-197`), the adobe ladders (`272-289`), the catwalk (`103-115`, `128`), gallery ore (`182`), tram (`487-493`), trestle legs (`508-515`), `ladder_up` (`633-639`), `plant` (`dressing.py:34-53`), `boulder` (`139`), `scrub` (`153-168`), `blocked_mask` (`69-70`), `wall_beside_doors` (`870-881`).
