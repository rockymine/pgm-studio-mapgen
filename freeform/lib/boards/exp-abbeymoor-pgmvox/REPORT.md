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
- The studio's reader (`read_mapxml.cs`) reads `world/map.xml` as valid.

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
