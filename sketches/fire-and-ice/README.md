# Fire and ice — the composed sketch

**This folder turns the author's hand-built sketch world into one integrated map, in colour-coded wool.** The
sketch is a CTW and DTC hybrid for a fire-and-ice contest: a bunker set into a mountain with the core in its face,
an underground wool lane under a flat shelf of terrain, and a valley floor between them. `compose.py` keeps only
the footprints of the sketch's structures, rebuilds the ground around them area by area, and turns the half 180
degrees into the whole map.

**The source world is not in the repository.** It is the author's, uploaded to a session as its four region
files, and the script reads it and never writes over it. Everything new is wool in a colour of its own and the
ground under every surface is stone, so texturing is left open.

## Running it

```bash
python3 sketches/fire-and-ice/compose.py <sketch>/region <out>/region --xray <out>/xray/region
```

```bash
python3 sketches/fire-and-ice/render.py <out>/region top.png top -60,110,_,99,-110,210 3
```

```bash
python3 sketches/fire-and-ice/render.py <out>/region lane.png iso 26,68,0,60,-72,34 5 1
```

**A build takes about five seconds and prints its own report.** It names every piece's height and extent, the
mountains' steps between neighbouring columns, and the three closure readings below. `--no-rotate` builds the one
half alone; `--xray <dir>` writes a second copy without the ground fill, to look at the underground in. The four
region files drop into a copy of the sketch world's `region/` folder.

## What it builds

| Piece | Where, in the half's own coordinates |
|---|---|
| Bunker | the sketch's floating copy moved by (−35, −61, −43) onto the original, as its rough form; the original's lava core kept |
| Roof plates | the clay and light-grey plates over the spawn wing at y 67, carried back to x −28 in the same six-block checker |
| H dome and the shelf's walls | each as its rough form, where the sketch has them |
| Pit under the core | its ramp and back room open from the top, with no floor laid over them |
| Wool lane | the floating lane brought down unchanged: walk at y 14 on its bedrock, raised to y 20 at its south end where it starts to climb |
| Flat roof | bedrock at y 29, fifteen over the walk, from the wool area south to z −26; walls bedrock to y 17 and stone above |
| Entrance | the lane's west wall carried on past the roof: y 25 by the boulder, y 23 by the entrance, then up in steps of three beside the ramp |
| Retaining strip | lime and green, two thick, holding the floor back over the carried wall; five to seven blocks tall |
| Ramp | on from the lane's end at y 20 up to the floor at z 19, through irregular rows of points |
| Shelf | flat at the shelf walls' top, y 50, everywhere inside their angle up to the north peak |
| Mountains | the sketch's yellow and light-blue areas, drawn as one surface through points off the sketch's own surfaces |
| Spawn room and tunnels | a room behind the door frame under the plates; tunnels to a hall, on to the lane's west arm, and up to the core's terrace inside the south peak |
| Middle | floor from the valley floor's south edge to the centre line at z 48 |
| Turn | 180 degrees about block (24, 48) |

## The structures, as their rough form

**A structure is carried as plain stone with its detail taken out.** Every stair, slab, fence, pane, torch, wire
and button goes; every other building block becomes stone; and every one-block recess in a wall is filled, so
each face is one plane. Bedrock, obsidian, lava, the clay plates and every wool colour keep their own block, and
so does the nether-brick fence the antenna is built of, as stone.

**The plates roof the spawn wing's body.** Under them the ground is solid down to the bottom of the world, except
the spawn room and its stairwell, so the facade stands on a body rather than in front of open space. The bunker's
house is solid up to the core's terrace at y 56.

## The mountains

**The mountains are one surface drawn through the sketch's own heights.** About one column in thirty of the
sketch's yellow and light-blue shells is taken as a control point, at irregular places, and a thin-plate spline
is laid through them; the sketch's shells themselves give way. `terrain.py` holds the spline.

**Where a mountain meets something, it meets it at that thing's height.** Points along the shelf walls hold the
shelf at their top, points along the retaining planes hold the yellow at the planes' top, points round the H
dome hold the ground at its base, and points along the plates' edge bring the peak north of them down onto them. A
column over anything buried is raised to five above it.

**Each column keeps the sketch's colour.** Yellow stays yellow and light blue stays light blue; a column the
sketch left bare takes the colour nearest it, and the shelf is yellow. The build reports how many neighbouring
columns step by how much.

## What keeps it closed

**Every space the composition carves is registered, and the ground is filled solid around them last.** The
tunnels, the hall, the spawn room, the lane's cavity, the canyon, the cut over the ramp, the pit and the back room
each mark their cells as air. The fill then runs every column straight down from its surface to the bottom of the
world and skips only those cells.

**The build reads three things back and prints each one.** A surface reading lists every patch of columns with
no ground under it and closes the enclosed ones. A closure reading floods the sky's air inward and names every
place it reaches the underground, each matched to an entry or reported as a `LEAK`. A depth reading lists every
tunnel column whose roof is not below the ground over it, and the least cover on each route.

**The entries are the ones the composition means to have.** The lane runs out into the canyon and the ramp, and
its long side is open to the void on the east; the spawn door opens onto the valley; the core stairs have a cut in
the south peak's foot and an opening in the terrace; the back room opens with the pit under the core.

## Colour key

| Block | Is |
|---|---|
| light grey wool | the floor, the ramp and the middle |
| white wool | the lane's walk surface |
| lime / green wool | the retaining planes and strip, face and back |
| yellow / light blue wool | the flatter and the more mountainous terrain |
| stone | a structure's rough form, and the solid ground under every surface |
| clay / light grey wool at y 67 | the roof plates |
| cyan, brown, blue wool | tunnel walls, floors and roofs; orange for stair flights, magenta for halls |
| black wool, red wool | the wool's plinth and the goal block on it |

## Files

| File | Is |
|---|---|
| `compose.py` | the composition, its parameters and every point list |
| `terrain.py` | the thin-plate spline the mountains are drawn through |
| `loft.py` | curves, lofted surfaces and their voxels: the ramp, the retaining strip, the middle |
| `anvilw.py` | a 1.8 Anvil region writer; lighting is left for the server to compute and the biome is Ice Plains |
| `render.py` · `colours.py` | top-down and isometric pictures, leaving out the sketch's floating reference pieces |
