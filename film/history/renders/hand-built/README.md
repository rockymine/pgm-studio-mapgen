# Hand-built map ("fire and ice" ice map) - renders from committed block data

**Fidelity first.** These pictures show the author's hand-built **half** (x -15..104, y 0..91, z -56..101 in the
study frame, 66,754 blocks) plus a **copy turned 180 degrees** about the pivot stored in the data
((x, z) -> (119 - x, 173 - z), 133,490 blocks, 18 positions collide and take the copy). Not in the data: the middle
between the halves (the gap in every whole-map picture is real, not a render fault), the study's variant middles
(`variants.json`, not used), and anything the study's exporter skipped.

**Colours are the author's drawing colours, not the final theme.** The terrain is the author's colour-coded wool
(light blue = mountains, yellow = flatter ground, light grey = floor, lime/green = retaining walls, white/orange/pink/red =
the underground lane, magenta = the opening into it, purple = ramp under the core). The sketch is wool by design; the
map is to be repainted as ice later.

## What the data is

Source: branch `claude/compassionate-cerf-fg7m17` of pgm-studio-mapgen, commit
`4486636d9d62139cc87b8dc2dd7ba4748bfc442b`, folder `sketches/fire-and-ice/study/viewer/` (read with `git show`;
`map.json` is 1,208,813 bytes). `map.json` has `pivot`, `layers` (19, with per-layer colour and low-poly loft meshes
used only by the web viewer), `palette` (38 `[layer, "#rrggbb"]` pairs), `order`, and **`blocks`: a flat list of
`x, y, z, code` for 66,754 real placed blocks**, where `code = paletteIndex*2 + loftFlag`. They are real blocks from
the author's own world (written by `rec/export_viewer.py` from the half it loaded), not derived shapes; the lofts
are only extra meshes. But the block **identity was reduced to a colour**: the palette carries no block names, so
the 1.8 id had to be recovered from the colour, using the same colour table that `export_viewer.py` used to
produce it.

## Conversion (`convert.py`, output `blocks-full.json`)

Palette colour to 1.8 block: wool by dye (35:0 white, 1 orange, 2 magenta, 3 light blue, 4 yellow, 5 lime, 6 pink,
7 dark grey, 8 light grey, 10 purple, 13 green, 14 red, 15 black); stone 1:0; granite 1:1, polished granite 1:2,
diorite 1:3, polished diorite 1:4, polished andesite 1:5, stone variant 1:6 (as exported); cobblestone 4; stone bricks 98;
nether brick 112; brick 45; double slab 43; half slab 44; clay block 82; stained clay cyan 159:9; bedrock 7; glass 20;
obsidian 49; gold 41, iron 42, diamond 57, emerald 133.

**Lost or substituted**: all stairs, walls, fences, iron bars,
doors, chests, torches, signs, water and lava (the exporter's skip list) are absent; slab/stair/wall blocks that
share a colour with a full block come out as that full block (cobblestone for cobble wall and stairs, stone bricks
for brick stairs, brick for brick stairs); so the **core has no lava**, only its obsidian, and the staircases look
as steps only where the author built them from full blocks. Wool "ceiling" and clay roof share colours: light grey
wool 35:8 and clay 82 were chosen. Torches/beacon in the wool room are not there.

## Pictures (1920x1080, JPG q90; camera x, y, z, yaw, pitch, fov)

The renderer is the scratch `eye` tool (real 1.8 textures, no lighting); `empty` world plus `EDITS=blocks-full.json`.
Yaw 0 looks +z, 90 looks -x, -90 looks +x (Minecraft convention).

| picture | camera | shows |
|---|---|---|
| `01-whole-from-west.jpg` | -165, 130, 86, -90, 22, 70 | The whole map from the west edge, looking east: the author's half (left, the bunker with black roof and antenna seen from its back) and the half turned 180 degrees (right, facade facing us). The gap between them is the missing middle. |
| `02-whole-from-east.jpg` | 255, 130, 86, 90, 22, 70 | The whole map from the east edge, looking west: the two halves swap sides; the right-hand half shows the open wool-lane box in red and orange. |
| `03-whole-from-south-edge.jpg` | 60, 115, -125, 0, 24, 70 | One end of the map, looking along its long axis; the map is 180-degree symmetric, so the north end looks identical (no separate picture). |
| `04-whole-from-above.jpg` | 60, 240, 86, -90, 89.9, 70 | Straight down, long axis horizontal: both bunkers (black roofs), the purple ramps under the cores, magenta holes to the lanes, yellow/blue hills, red/white wool-room markers. |
| `05-facade-and-core.jpg` | 80, 40, 28, 90, 10, 75 | The bunker facade from the valley: the obsidian core as a tall dark panel above the purple ramp, windows, the gate with the high door to the right. |
| `06-facade-from-above.jpg` | 70, 70, 10, 110, 25, 75 | The facade from higher up: the checkerboard roof, the high door over the core and the hill (yellow/green) the author describes climbing to reach it. |
| `07-valley-from-east.jpg` | 125, 60, 28, 90, 20, 80 | Valley floor (light grey) between the retaining walls and hills, seen from the east: facade with core and ramp at the back, blue hills and green retaining walls around. |
| `08-core-from-the-ramp.jpg` | 70, 40, 28, 90, -5, 80 | Standing on the ramp end below the facade looking up at the core panel: how an attacker from the hollow sees it. |
| `09-under-the-core.jpg` | 72, 16, 28, 90, -28, 80 | From underneath, looking up at the building's underside with the purple ramp running into the hollow below the core. |
| `10-wool-lane-open-side.jpg` | 118, 16, 40, 90, 8, 75 | The wool lane (white floor, orange walls, red roof) from its open long side: magenta hole where the valley floor drops in, diamond marker blocks on the lane edge. |
| `11-inside-the-lane.jpg` | 72, 12, 6, -90, 5, 80 | Inside the underground lane looking east along it to the deliberate opening; white floor, orange walls on bedrock footing, pink edge under the red ceiling. |
| `12-stairwell.jpg` | 40, 45, -30, -90, 10, 75 | The stone stairwell flight at the back of the building seen from the west, between yellow hill terrain and a green retaining wall. |
| `13-wool-lookout-from-above.jpg` | 55, 85, -60, 0, 50, 75 | The back area from above: the grey round/box 'wool lookout' on the yellow shelf between the blue hills, the valley and the facade beyond it. The area a dead-ground rule would flag. |
| `14-wool-lookout-from-the-valley.jpg` | 55, 58, -15, 180, 15, 75 | The same lookout from the valley side at eye level: a stone block with a few light blocks (chest/marker places) on the yellow shelf, walled by blue hills. |
| `15-descent-hole-in-the-valley-floor.jpg` | 70, 50, 45, 180, 40, 75 | Looking down the valley floor toward the magenta hole where the floor opens into the wool lane, retaining wall and blue hill right, purple ramp left. |

`02-whole-from-east` and `03-whole-from-south-edge` repeat the symmetry: the map is two identical halves turned
180 degrees, so a view from the north end equals the one from the south end (no extra picture).

## Regenerating

```
git -C <repo> fetch origin claude/compassionate-cerf-fg7m17
git -C <repo> show 4486636d9d62139cc87b8dc2dd7ba4748bfc442b:sketches/fire-and-ice/study/viewer/map.json > map.json
python3 convert.py          # writes half.json and full.json (copy of blocks-full.json)
EDITS=full.json eye empty jobs.json out   # jobs = the table above at 1920x1080
```
`blocks-full.json` (2.2 MB) is committed for convenience.
