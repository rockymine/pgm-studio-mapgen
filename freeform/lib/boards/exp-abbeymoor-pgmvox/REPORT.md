# Abbeymoor (pgmvox) — report

> Written from the builder's own account. The builder (Sonnet 5.5) could not write this file itself, so its final
> message is set down here as it reported it; the measurements are its read-backs in `renders/`.

**Abbeymoor is a destroy-the-monument board for two teams of sixteen: one moor island, joined by land, where each
team holds an abbey hill above a village, with a peat bog between them.** It is the pgmvox half of the experiment in
`analysis/freeform-vs-studio/experiment/BRIEFS.md`; the studio half is `exp-abbeymoor-studio`. The island is
200 × 264. Red holds the north, and blue is its half-turn image.

## What was built

- **Abbey Hill**, a plateau at y 80 with 38° slopes, carries a ruined nave. **Monument A** is an obsidian cube at
  x -41..-39, y 86..88, z -73..-71 on a dais (y 81..83).
- **Thorncombe village** (x 6..52). **Monument B** stands on the green at x 29..31, y 69..71, z -71..-69.
- **The peat bog** between the sides: pools, twelve standing stones, a boardwalk and peat cuttings. A beck runs
  along the village's east side.
- **Under each abbey a vaulted crypt** (floor 70). The Night Stair, eleven cells, comes up in the chancel. A
  60-block passage runs under the valley and comes up by the Tithe Barn's cellar stair, 14 blocks from B, with the
  barn wall about 6 from the cube.
- Eleven places a side. The board's scripts are 1,507 lines.

## Read-back

- Walks: spawn to the nave 69, to the crypt 90, to the cellar foot 84. 0 ladders, loose water 0.
- GO1 ratios 3.37 and 3.78; GO4 own walks 60 and 50.
- **GO3 is 201 and 190 against a target of 85–150, a miss the builder accepted:** the brief's 200–260 size and GO1
  cannot both be met.
- Voxel sight to the cubes from the attackers' ground: 27% (A) and 26% (B).
- The studio's reader (`read_mapxml.cs`) reads `maps/dtcm/abbeymoor_pgmvox/map.xml` as valid.

## Times

| Phase | UTC |
|---|---|
| Design | 01:20:30 |
| `land.py` | 01:26:23 |
| Plan, check and sketch | 01:30:52 |
| Generation, walk and renders | 01:38:05 |
| Final pipeline | about 01:41 |

About 21 minutes.

## What pgmvox could not express, and what was done instead

1. **No crypt, stair-from-below or passage helper.** All of `crypt.py` (158 lines: hall, Night Stair, passage,
   finish) is board code, as is the voxel objective-sight check in `walk.py`.
2. **`Destroyable` has no float or dais option**, and there is no storey-below link helper, no gallery style and no
   objective-visibility check.
3. **No heather or biome-patch API**: mycelium with alliums stands in.
4. **GO3 and the brief's size conflict** (above).

## The twelve lessons

| # | Lesson | Met |
|---|---|---|
| 1 | Objective found without a map | yes: sight 27% (A) and 26% (B); five clear on every side of each cube |
| 2 | Made of what the mode needs | yes: obsidian cubes and a diamond pickaxe (Efficiency II, unbreakable) in the kit |
| 3 | Wool-room loot | n/a |
| 4 | Vegetation leaves the floor fightable | yes: no trunk or canopy on a road; five orchard trees, spacing 8 |
| 5 | Stairs attached and walkable | yes: Night Stair floors 71, 72, 72, 73, 74, 75, 76, 76, 77, 78, 79; passage descents at x -44..-42, -39..-37, -34..-32, -29..-28 and ascents at x 11..13 and 16..18; at most four blocks of climb |
| 6 | Spawn exit open | yes: spawn (0, 69, -112), farmhouse behind at z -123..-117, fold at x -29..-15 |
| 7 | A floating platform cannot be mined away | yes: a solid island, bedrock at y 1 |
| 8 | Ladders only where needed, never in water | yes: 0 ladders |
| 9 | Joins open | yes: the crypt is reached from the nave and from the barn |
| 10 | Player scale | yes: cube 3, nave 26 × 13, houses about 8 × 6 |
| 11 | Ground varies in patches | yes: heather, podzol and dirt patches, rim ledges, 91 vines |
| 12 | A build zone shows | n/a: a not-void rule only |

## Revision 1

From the author's review (`analysis/freeform-vs-studio/experiment/REVIEW-1.md`), set down from the builder's account.
02:09–02:16 UTC, about 7 minutes; a run takes 29 seconds. The first renders are in `renders-v1/`.

| # | Review point | What changed |
|---|---|---|
| 1 | Reads like a place; keep the ruin intact | Kept. |
| 2 | The bog too oval; patches round the map | `land.bog_field`: a noise-warped outline with a fen channel wandering east and west through the middle, the paint following the same field; 15 irregular peat patches, densest across the middle; three tarns at (-58,-30), (-84,-8), (-6,-48). |
| 3 | Something missing beside the middle | Fenside, a hamlet at (-68,-17) (image at (67,16)): Fenside Cottage (-74,-22), Gorse Cottage (-63,-12), the Peat Store (-75,-11), a flank orchard, a tarn, and Fen Lane to the bog at (-17,-31). Not a hill. |
| 4 | Stone houses; clay walls | Clay walls over a stone base course on every house but the timber Hay Barn (lime-wash, ochre, brick, terracotta, umber). |
| 5 | Paths in dirt | Coarse dirt, dirt and a little gravel, no stone, 2.1 either side of the line (was 1.6). |
| 6 | More trees and rocks | 31 moor trees in 12 copses (was 5 orchard trees) and 58 boulders (was 20); still no trunk on a road, green, cutting, nave or water, and no canopy over a road. |
| 7 | A 27-block obsidian cube | Both monuments are a pillar of three obsidian blocks: A at (-40, 88..90, -72) four over its dais, B at (30, 70..72, -70) three over the green (blue's at (39, 88..90, 71) and (-31, 70..72, 70)); regions 1 × 3 × 1, the diamond pickaxe still in the kit. Voxel sight to any face of the pillar from ground 25–60 away: 43% (A), 29% (B). |

Read-backs: the studio reader reads it valid; footing 0; loose water 0; 0 windows beside doors; the crypt joined (spawn to
nave 69, crypt 90, cellar foot 84); GO1 3.36 and 3.78; GO3 still the accepted miss (201 and 190).
