# Riftwater, the standalone original: anatomy and attribution

Subject: `freeform/opus55-freeform-riftwater/` (scripts about 3,400 lines). This is the comparison board; the primary subject is the pgmvox port, in `ANATOMY.md`. Line references are to `freeform/opus55-freeform-riftwater/scripts/`. Its layers document is `riftwater-original.layers.json`.

## 0. Reproduction and method

**A re-run of `gen.py` reproduces the committed world exactly.** `gen.py` was run unmodified from a scratch copy; its `volume.bin` has 1,007,266 non-air blocks, the same ids, data and biome bytes as the committed `world/region` (read with `tools/anvil.py`): 0 id mismatches, 0 data mismatches, 0 blocks on either side missing. The instrumented run (`method/original/instrument.py`: wrappers on `World.set` plus a snapshot diff at every function boundary, to catch `write_land`'s array writes) is bit-identical to the plain run, ids, data, biomes and tile entities, with no unowned block. `REPORT.md` quotes 1,007,258 blocks, 106 trees and 16 tile entities; the build today has 1,007,266, 108 trees (54 per half, the knoll oak included) and 24 tile entities (8 chests, 16 signs).

## 1. It does not use pgmvox

`grep -rn pgmvox` over the board finds nothing. Imports: `plan`, `mc` (own `World`, 1.8 block ids), `mirror`, `noise`, `terrain`, `underground`, `buildings`, `house`, `dressing`; numpy, scipy, PIL. `cut_trees.py` (run once, wrote `trees.json`) imports `tools/anvil.py` and `tools/trees.py` of the mapgen repository. The studio's C# `PgmStudio.Minecraft` Anvil writer is called by `write_world.cs` (`#:project` line 12).

## 2. The pipeline in `gen.py` order

| gen.py line | step (file:lines) | builds | how it writes |
|---|---|---|---|
| 23-24 | `World(-120,-88,240,176)`, `terrain.Land()` (mc.py:129-203, terrain.py:18-33) | volume and the red half's grids (120 x 176) | |
| 25 | `terrain.build_heights` (terrain.py:48-172) | No blocks. 14 sub-stages of numpy formulas: ragged rift lip and board insets (54-68), town bluff/fields/west blend (70-85), river valley (87-98), pond and spit (100-110), ridge, spurs and 3-block steps (112-132), spawn shoulder at 59 (134-141), square and green levels (143-147), knoll (149-151), water grids (153-167). | heightfield formulas |
| 26 | `build_underside` (terrain.py:175-191) | No blocks. Bottom of every column: sheer 26+ under the rift, tapering elsewhere. | formula |
| 27 | `write_land` (terrain.py:203-275) | 925,382 blocks: stone with andesite beds that follow the ground, dirt/grass/rock by slope, river and pond beds, water. | **H**: a Python loop over every land column slicing `w.ids[x, bot:top, z]` |
| 28 | `write_falls` (terrain.py:290-306) | 754 flowing-water blocks, x -11..-10, z -3..3, y 8..45 | **S** |
| 29 | `paint_biomes` (terrain.py:309-316) | biome grid: forest 4, river 7, plains 1 | array assignment |
| 31-34 | `underground.build` (underground.py:397-414) | 5 cave branches and 10 chambers by `carve_tube`/`carve_ellipsoid` (40-77, 344-376, 402-405), `dress_cave` (80-112) and stalagmites (379-394), grotto (361-370), lake pool (115-129), mouth (132-146), sinkhole (149-180), mine (183-262), shaft (265-282), gaol cellar (285-337). | **S** loops over ellipsoids and boxes, **L** lists for the cellar and portal |
| 37 | `buildings.build` (buildings.py:607-638) | square, 16 town houses, gaol ladder, chapel, village (9 `house` calls), well, headframe, spoil heap, watch house, hut, mill, footbridge, stone bridge, old bridge, 13 routes paved, 26 door paths, 2 monuments. Calls `house.house` 31 times in total (house.py:105-233). | **P**/**S**: `house()` is a 129-line function of `w.set` loops; the rest are local loops |
| 39 | `dressing.build` (dressing.py:546-605) | wheat field, barn (a 31st `house` call), haystacks, hay cart, jetty and boat, spring, the Cutting, 3 stalls, 6 worn patches, lamps, gardens, benches, 4 forest zones, the knoll oak, 14 listed trees (5 land), boulders, fallen logs (writes nothing), hedgerow, rift-face vines, shop signs, cover. | **S** loops, **L** lists, trees by planting whole blocks from `trees.json` |
| 41 | `mirror_world` (mirror.py:51-67, table 12-48) | blue's half = the red half mirrored with a data-turning table | **M** |
| 42-46 | blue wool recolour | 8 blocks of wool 14 to 11 in the box x 84..110, y 50..89, z -16..2 | array assignment |
| 47 | `w.save` | `volume.bin`; `write_world.cs` then writes the region files; `build.sh:14` copies the hand-written `scripts/map.xml` to `world/map.xml` | |

**`map.xml` is written by hand** (77 lines, `scripts/map.xml`); nothing generates it. Monument cuboids (-66,56,-44), (-66,54,48) and the spawn point (-97.5,60,-6.5) are typed in a second time; the report says the map.xml regions moved with the monuments when they were raised. **Blue's half** is `mirror_world`: 503,633 of 1,007,266 blocks (50.0%).

**`plan.py` is documentation more than input.** Of its 24 places only two are read by the generator (the river line, terrain.py:37; the North Wood polygon, terrain.py:311 and dressing.py:573); the routes (13) and monuments (2) are read; the buildings, cave, ridge and fields are literals inside the functions.

## 3. Block attribution

| # | step (rolled up) | class | op exists today | blocks left | share of non-air | exposed blocks | carved to air (both halves) |
|---|---|---|---|---:|---:|---:|---:|
| 1 | write_land: rock + soil + paint | A | yes | 925,382 | 91.871% | 88,026 | |
| 2 | write_falls: water over the lip | A | no (new) | 754 | 0.075% | 650 | |
| 3 | cave carves (tubes, chambers, alcoves) | A | yes | 0 | 0.000% | 0 | 7,196 |
| 4 | pillar_hall (pillars; carve counted above) | A | no (new) | 98 | 0.010% | 98 | 1,502 |
| 5 | dress_cave + stalagmites | A | yes | 1,932 | 0.192% | 1,824 | |
| 6 | grotto (chamber + stash) | A | yes | 10 | 0.001% | 10 | 268 |
| 7 | lake chamber pool | A | no (new) | 346 | 0.034% | 158 | |
| 8 | mouth (ledge + vines in rift face) | C | no (made) | 56 | 0.006% | 48 | |
| 9 | sinkhole | A | no (new) | 230 | 0.023% | 216 | 1,116 |
| 10 | mine gallery (+ portal, chest) | A | yes | 1,250 | 0.124% | 988 | 2,086 |
| 11 | shaft | A | yes | 250 | 0.025% | 190 | 104 |
| 12 | gaol cellar (vault, cells, breach) | C | no (made) | 522 | 0.052% | 274 | 346 |
| 13 | square (plaza paving) | A | no (new) | 694 | 0.069% | 658 | |
| 14 | town: 16 houses (house + site + furnish) | B | yes | 16,460 | 1.634% | 14,842 | 1,032 |
| 15 | gaol_stair (ladder) | A | yes | 38 | 0.004% | 10 | 10 |
| 16 | chapel: nave (house + site + furnish) | B | yes | 1,828 | 0.181% | 1,514 | 106 |
| 17 | chapel: tower, spire, pews (bespoke part) | B | no (new) | 1,084 | 0.108% | 1,040 | 176 |
| 18 | inn_sign | A | no (new) | 2 | 0.000% | 2 | |
| 19 | village: 9 houses (house + site + furnish) | B | yes | 5,556 | 0.552% | 4,584 | 1,184 |
| 20 | village: engine stack + forge fittings | B | no (new) | 174 | 0.017% | 174 | 28 |
| 21 | well | B | no (new) | 70 | 0.007% | 48 | |
| 22 | headframe (timber tower + wheel) | B | no (new) | 422 | 0.042% | 406 | 2 |
| 23 | spoil_heap | A | no (new) | 650 | 0.065% | 316 | |
| 24 | watch_house: house + tower (house + site + furnish) | B | yes | 2,158 | 0.214% | 2,012 | 410 |
| 25 | watch_house: terrace, stairs, wool (bespoke part) | B | no (new) | 194 | 0.019% | 194 | 8 |
| 26 | hut: cabin (house + site + furnish) | B | yes | 666 | 0.066% | 496 | 238 |
| 27 | hut: chest, chopping block, woodpile | B | no (new) | 16 | 0.002% | 6 | |
| 28 | mill: building (house + site + furnish) | B | yes | 1,098 | 0.109% | 986 | 32 |
| 29 | mill: race, wheel, weir, sacks (bespoke part) | B | no (new) | 946 | 0.094% | 352 | 576 |
| 30 | footbridge (trestle) | B | no (new) | 306 | 0.030% | 236 | |
| 31 | stone_bridge (arch) | B | no (new) | 804 | 0.080% | 532 | 76 |
| 32 | old_bridge (broken half-arch) | B | no (new) | 744 | 0.074% | 336 | |
| 33 | pave x13 routes | A | yes | 3,690 | 0.366% | 3,310 | 364 |
| 34 | path_to_door x26 | B | no (new) | 446 | 0.044% | 446 | 70 |
| 35 | monument x2 (obsidian) | A | yes | 8 | 0.001% | 8 | |
| 36 | wheat_field | A | no (new) | 3,814 | 0.379% | 1,038 | 494 |
| 37 | barn (house + site + furnish) | B | yes | 1,280 | 0.127% | 1,180 | 120 |
| 38 | barn: wide door + hay (bespoke part) | B | no (new) | 28 | 0.003% | 28 | 24 |
| 39 | haystacks, hay_cart | B | no (new) | 62 | 0.006% | 62 | |
| 40 | jetty_and_boat (+ lilies, reeds) | B | no (new) | 140 | 0.014% | 116 | 12 |
| 41 | spring | B | no (new) | 28 | 0.003% | 18 | 6 |
| 42 | cutting (stumps, log piles, sawhorse) | B | no (new) | 168 | 0.017% | 164 | |
| 43 | stalls | B | yes | 120 | 0.012% | 120 | |
| 44 | worn ground x6 | A | no (new) | 110 | 0.011% | 110 | 110 |
| 45 | lamps along 3 streets | B | yes | 130 | 0.013% | 130 | |
| 46 | gardens | B | no (new) | 262 | 0.026% | 174 | |
| 47 | benches | B | no (new) | 4 | 0.000% | 4 | |
| 48 | forest x4 zones (rockymine trees) | A | yes | 24,962 | 2.478% | 24,690 | |
| 49 | 15 hand-placed trees | A | yes | 4,624 | 0.459% | 4,572 | |
| 50 | boulders x10 | A | yes | 336 | 0.033% | 168 | |
| 51 | fallen_logs (writes nothing) | B | no (new) | 0 | 0.000% | 0 | |
| 52 | hedgerows | A | no (new) | 24 | 0.002% | 24 | |
| 53 | rift_face (vines, ledges) | A | no (new) | 730 | 0.072% | 730 | |
| 54 | shop_signs | B | no (new) | 14 | 0.001% | 14 | |
| 55 | cover (grass, ferns, flowers) | A | yes | 1,538 | 0.153% | 1,536 | |
| 56 | gen.py: recolour blue wool | A | no (new) | 8 | 0.001% | 8 | |

Total 1,007,266; blue's half is the mirror of the red half, so every row is split 50/50.

## 4. Classification

| | blocks | share of non-air | exposed share |
|---|---:|---:|---:|
| A layer operation | 971,480 | 96.45% | 80.9% |
| B library entry + placement | 35,208 | 3.50% | 18.9% |
| C bespoke (made) | 578 | 0.057% | 0.2% |
| op exists today (A+B) | 993,316 | 98.62% | 94.6% |
| needs a new op or template (A+B) | 13,372 | 1.33% | 5.2% |

C is the gaol cellar (522) and the cave-mouth ledge (56). By code (docstrings, comments and blanks excluded): 2,260 lines; library-equivalent (world, ids, noise, mirror) 274; houses 328; underground 341; ground and heights 231; roads 73; towers, bridges, mill, headframe, village furniture 352; dressing 495; plan data 104. The original's 31 `house()` calls, 26 door paths, 13 pavings and 4 forest zones are one op each in the layers document.

## 5. Measurements worth keeping

- **Per-op seeds would not reproduce this world.** `underground.RNG` (seed 1234), `buildings.RNG` (4242) and `dressing.RNG` (777) are module-wide streams drawn by 6, 3 and 5 ops in call order. Giving each drawing op its own seed (`method/original/seedtest.py`) changes 23,834 cells (2.37%), over 10,762 of 42,240 columns, including the trees (3,094 + 2,858 + 2,432 cells in the three big zones), whose own seeds are fixed; I read that as their `blocked` masks following the changed paving (inferred, not isolated).
- **`fallen_logs` runs and writes no block** (0 `set` calls): all four sites fail the ground test.
- **40 dirt blocks carry the data value 5** (`terrain.py:261` sets one dirt below a mid slope without clearing the andesite bed's data).
- **The cave's carve removes 7,196 blocks** (both halves), the mine 2,086; the explicit `set` calls total 97,587 per half for 40,942 surviving blocks (42%); the rest are overwritten or air.
- **Timing**: generation 1.2 s (terrain 0.4, underground 0.1, buildings 0.2, dressing 0.4).
