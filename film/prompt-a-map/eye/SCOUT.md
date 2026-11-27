# Location scouting guide

We are filming a comedy sketch inside real Minecraft worlds (PGM maps authored by AI). A scratch tool renders a
world folder with real block textures from any camera. Your job as a scout is to find camera positions that show
a specific thing clearly, verify them by looking at the rendered picture, and report them as JSON.

## The tool

`/tmp/claude-0/-home-user/5b5a763a-8f02-5e92-a825-a8c273c7b88d/scratchpad/eye/bin/eye <worldDir> <mode> ...`
(`<worldDir>` holds `region/*.mca`; worlds live under `/home/user/pgm-studio-mapgen/maps/<mode>/<name>/`, with a
`map.xml` beside the region folder that names spawns, objectives and regions with coordinates.)

| mode | what it does |
|---|---|
| `info [step]` | prints the bounds and a top-height grid (one char per `step` blocks: 0-9, a-z = 10-35, A-Z = 36-61, space = void) |
| `overview <outDir> <name>` | renders 4 aerial corner views + 1 straight-down view (960x540) as `<name>-c0..c3.png`, `<name>-top.png` |
| `find <id[,id]> [x0 y0 z0 x1 y1 z1]` | lists clusters (bounding boxes) of the given block ids. Useful ids: 49 obsidian, 17/162 logs, 18/161 leaves, 5 planks, 64/71/193-197 doors, 54 chest, 35 wool, 7 bedrock, 20 glass, 85 fence |
| `slice <y> [x0 z0 x1 z1]` | prints block ids at one level as a grid (3 chars per block), to read a floor plan |
| `<jobs.json> <outDir>` | renders the jobs: `[{"name":"a","w":960,"h":540,"from":{"x":0,"y":20,"z":-30,"yaw":0,"pitch":15,"fov":70}}]` -> `<outDir>/a.png` |

A render takes about a second. Scout at 960x540. Then **look at the picture with the Read tool** — never report
a camera you have not looked at. Write your own files only under the output directory you are given.

Old versions of a world: `git -C /home/user/pgm-studio-mapgen archive <commit> <path> | tar -x -C <your out dir>/worlds`
(read-only; never commit, checkout, or modify either repository).

## Camera conventions (Minecraft's own)

- `x` east, `y` up, `z` south. `yaw` 0 looks south (+z), 90 looks west (−x), 180 north (−z), −90 east (+x).
- `pitch` positive looks **down**, negative up. `fov` is horizontal, 60–80 is natural.
- To look from (x,z) toward (tx,tz): `yaw = degrees(atan2(-(tx - x), tz - z))`.
- A player's feet stand at `top block y + 1`; their eye is 1.62 above their feet; a player is 1.8 tall, 0.6 wide.
- The camera must be in open air (inside a block you get a wall of texture). If a picture is one flat texture,
  you are inside something — move.

## What makes a usable shot

- 16:9, the subject readable at a glance, not cluttered, horizon roughly level (pitch between −10 and 35 for
  ground shots; aerial establishing shots can look down more).
- Characters (blocky 1.8-tall players) are composited on top of the picture later and **cannot be hidden behind
  blocks**, so each shot needs clear, open, standable ground where they will be: report 2–4 `stand` points
  (`x`, feet `y`, `z`) that are visible in frame, 4–14 blocks from the camera, with nothing between them and
  the camera. Check the feet y with `info`/`slice`.
- For each subject give me a **wide** (establishing) shot and a **close** shot when it makes sense.

## What to report (your final answer)

A JSON array, one object per shot, plus short notes:

```json
{"id": "houses-wide", "world": "/abs/path/to/world", "cam": {"x":0,"y":20,"z":-30,"yaw":0,"pitch":15,"fov":70},
 "png": "/abs/path/to/the/picture/you/looked/at.png",
 "shows": "one sentence: what is in frame and where (left/centre/right)",
 "stand": [{"x":1,"y":9,"z":-22,"note":"on the path, centre-left"}],
 "facts": "coordinates and numbers that prove the thing (e.g. door at 12,9,40 opens onto void at z>=41)"}
```

Be honest: if the world does not show the thing, say so and give the nearest real thing you did find. Do not
describe what you have not seen in a render or read from the blocks.
