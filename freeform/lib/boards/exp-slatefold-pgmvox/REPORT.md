# Slatefold (pgmvox) — report

> Written from the builder's own account. The builder (Sonnet 5.5) could not write this file itself, so its final
> message is set down here as it reported it; the measurements are its read-backs in `renders/`.

**Slatefold is a capture-the-wool board for two teams of twelve: two terraced slate hillsides facing each other
across the void.** It is the pgmvox half of the experiment in `analysis/freeform-vs-studio/experiment/BRIEFS.md`;
the studio half is `exp-slatefold-studio`. Red is drawn and blue is its `mirror_z` image.

## What was built

- **Terraces** at floors 74 (spawn), 70 (row), 66 (yard), 62 (front), 58 (quarry) and 54 (pit), with the high
  bench at 82.
- **Each side** has a kiln house by the quarry (red brick, chimneys, furnaces), a winding house with a headframe on
  the high bench, cottages, slate stacks and sheds.
- **A bedrock defence wall** with its chests in the front face: red at x 28..29, z -60..-55; blue at x -60..-59,
  z -85..-79.
- **Three-stair flights** with cobble-wall rails climb from the gantries. Six spruces, patchy slate flags and moss,
  and lamps along the lip.
- **The 340-block build zone** is block 36 at y 0 with the studio's redstone outline.

## Read-back

- 40 chests, 0 windows beside a door, 0 ladders, footing 0, loose water 0.
- Bedrock lies six under every platform's floor (1272/1272, 998/998, 875/875, 2649/2649, 295/295, 117/117 columns),
  except 152/155 on one small platform.
- By the building walk the Kiln is reached in 224 moves and the Winding House in 257. No wool room is reached on
  foot or by any jump.
- The studio's reader (`read_mapxml.cs`) reads `world/map.xml` as valid.

## Times

| Phase | UTC |
|---|---|
| Reading and design | 00:55:20 – 01:01:47 |
| `plan.py` | 01:02:47 |
| Plan check passing | 01:04:41 |
| First generation and walk | 01:13:35 |
| Fixes | to 01:18:53 |
| Full pipeline | 01:20:30 |
| A late repair | about 01:39 – 01:45 |

About 25 minutes to the first complete build and about 50 with repairs. The board's scripts are 1,332 lines.

## What pgmvox could not express, and what was done instead

1. **No terrace stage and no build-area object.** The zone and its outline were encoded by hand (`marks`).
2. **No defence-wall objective.** The wall, its chests and the check that it cannot be walked round are board code
   (`bedrock_walls`).
3. **The plan's jump graph misses jumps from rails and stair tops.** A sprint jump from the gantry's cobble rail
   reached the Kiln's wall top in about 80 moves and was found only by the voxel walk; the wall moved from x 25 to
   x 28.
4. **`build.house` windows are blind to the door**, and a door at an oblique heading can face a wall. `wool_house`
   reads the library's door back and raises if it differs from the plan; windows were worked round per house.
5. **`shapes.inside` drops polygon boundary rows**, which at first left nothing connected; `plan.grown` and
   `piece_cells` are local.

## The twelve lessons

| # | Lesson | Met |
|---|---|---|
| 1 | Objective found without a map | yes: monuments in the open at (±15, 76, -86), floating |
| 2 | Made of what the mode needs | yes: wool |
| 3 | Wool-room loot; defence chests in the front face | yes: `props.wool_chests` at (55/64, 59-60, -73/-63) and (-79/-72, 83-84, -95/-87); defence chests at (28,63,-59), (28,63,-56), (-59,79,-84), (-59,79,-80) |
| 4 | Vegetation leaves the floor fightable | yes: six spruces, none over a stair or landing |
| 5 | Stairs attached and walkable | yes: three-stair flights with rails; no diagonal-ramp check exists in the library |
| 6 | Spawn exit open | yes |
| 7 | A floating platform cannot be mined away | yes, bedrock six under the floor (one platform three columns short) |
| 8 | Ladders only where needed, never in water | yes: 0 ladders |
| 9 | Joins open | yes, by the walk read-back |
| 10 | Player scale | yes |
| 11 | Ground varies in patches | yes: slate flags and moss in patches |
| 12 | A build zone shows | yes: block 36 and the 340-block redstone outline |
