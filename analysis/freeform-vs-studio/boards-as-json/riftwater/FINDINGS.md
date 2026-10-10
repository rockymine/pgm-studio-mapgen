# Riftwater as layers: findings (the pgmvox port; the standalone original as comparison)

Evidence: `ANATOMY.md`, `ORIGINAL-STANDALONE.md`, `riftwater.layers.json` (131 ops), `method/`.

## How the board is expressed today

**The port is 1,529 lines of world-producing Python around library calls, run in five seconds.** `plan.py` holds the data (27 named places, 13 routes, 29 house records, cave and mine waypoints) and computes the red half's heightfield with formulas plus five landform calls. `gen.py` runs one `terrain.lay` call (90.7% of all blocks) with a local finishing pass, the cave and mine (library `tunnel`, `chamber`, `dress_cave`, `gallery`, `shaft`, plus 7 local pieces), `works.build` (library `build.house`, `site`, `route.pave`, `facade.carpet`; local towers, bridges, mill), `dress.build` (library `trees`; local field, Cutting, vines, cover), then `turn_world` mirrors red onto blue and `Objectives.stamp` places the monuments. `map.xml` is generated from the same objectives. 97.5% of blocks are written inside a pgmvox call. The original uses no library and types `map.xml` by hand.

## Shares

| | blocks | visible (exposed) blocks |
|---|---:|---:|
| A layer operation | 95.86% | 81.3% |
| B library entry + placement | 4.08% | 18.5% |
| C bespoke (made) | 0.057% (570 blocks) | 0.24% |

By what a player sees: terrain 56.8% (all A), buildings and roads 20.8% (B 18.3%), dressing 19.9% (A 19.7%), underground 2.5%. The original gives 96.45 / 3.50 / 0.057%. Existing ops cover 97.6% of blocks; 2.3% need something new.

## Would the agent lose freedom?

**No freedom of computation; some freedom of reach.** The agent still writes a script, and it emits JSON: coordinates, loops and noise-derived positions stay computable. In the port 89.8% of `set` calls already happen inside library ops, so for them the JSON is their arguments. What the JSON cannot say today:

- **Heightfield formulas** (rift lip with bays, wandering ridge foot, asymmetric valley, elliptical stage, gaussian mounds, two-distance underside): 14 new or extended ground ops, or relief marks. Fallback: a made heightfield.
- **`terrain.lay` finishing** (position-aware top, per-column bottom, wet beds): an extension; today it lays then clears 455,476 blocks.
- **Nine lambdas** (ground accessor, `keep=red`, route level profile, monument-clearance mask, carpet pattern): named references.
- **Reads of the world while writing** (198,169 reads, 74% in the library): houses seat on the world's top, trees avoid built ground, `pave` is guarded around walls, the mill reads the river line. These are rules the interpreter must implement; a missing rule is a gap only `made` covers.
- **Cross-op values** (`floor_of`, `shaft_top`, the square's mask): named outputs.
- **Towers, bridges, mill, headframe, village furniture**: templates, otherwise `made`. **Cellar and cave-mouth ledge**: `made`.

**`made` loses editing, not placement.** It can be moved, mirrored and reviewed in a render; its parameters cannot be changed in the browser and a diff shows blocks. Were every not-yet-existing op made, 23,696 blocks (2.4%) would be.

## Problems the JSON form brings

- **Ordering** is real and implicit: pads before walls (works.py:50), roads before houses, houses before the tree mask, the gaol ladder after the gaol (gen.py:30), monuments read the finished ground. The requested group order puts `pieces` before `buildings`, so the monument op carries an `after`.
- **Randomness.** One stream per module is shared by 5 ops in `under.py` and 4 in `dress.py`. Reseeding the underground and spoil-heap streams per op changes 2,004 cells (0.20%); in the original, per-op seeds change 23,834 (2.37%), cascading into trees. A JSON world is equivalent, not bit-identical, and noise seeds reproduce only in an interpreter that ports `fbm` exactly.
- **Symmetry** is easy (one op, 50% of blocks); its side effect is a recolour that also turns blue's stall awnings.
- **Size.** 82 KB for 131 ops against 74 KB of source; the trees stay a library (209 KB). One world snapshot is 16 MB, so per-step caching needs diffs.
- **Port against original.** Ids match in 86.7% of cells and natural-ground height is within 3 blocks in 98.4% of columns, but only 66% of the original's visible blocks match; 1,034 blocks of dressing are not ported. The port's monuments hang one block over the floor, the original's three (a later playtest rule).

## Ops and templates still needed, ranked by blocks

1. **Ground ops** for the heightfield: zero blocks of their own, 918,000 depend on them.
2. **`terrain.lay` finish** 9,528.
3. **`landform.field`** (wheat, ditches, scarecrow) 3,856.
4. **Tower templates** (belfry 1,162, watch tower and terrace 922, headframe 412, brick stack) about 2,500 plus the stack.
5. **Village furniture** (well, forge, stack, spoil mound) 1,726.
6. **Bridge template** (arch, half-arch, trestle) 1,650.
7. **Flora cover** 1,288 (in the studio, not pgmvox).
8. **Waterworks** (race, wheel, weir) 1,146.
9. Rift-face vines 832; waterfall 754; sinkhole rubble 484; vault 518 (C); lake pool 346; Cutting 152; pillars 122; mouth ledge 52 (C).

## Monuments and play pieces

**The contract is 8 blocks and a generated file; the rest is look.** Four monuments are two obsidian blocks each. The contract is those blocks, four cuboids, two spawn points with kit and protect box, and a build rule on the rift. The port derives the cuboid from the stamped `Box`; the original types both. Within 12 blocks of the monuments are 655 and 542 visible blocks, nearly all look: square floor, stalls, trees, paving, houses. The approach rules (trees 4 plus crown away) sit in `dress.py` as a mask. There are no wool rooms (a destroy map). How a monument hangs is the author's call.
