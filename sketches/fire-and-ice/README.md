# Fire and ice — the composed sketch

**This folder turns the author's hand-built sketch world into one integrated map, in colour-coded wool.** The
sketch is a CTW and DTC hybrid for a fire-and-ice contest: a bunker sunk into a mountain with the core in its
face, an underground wool lane under a shelf of terrain, and glacier cracks in the valley floor. The sketch
holds each piece in its own place; `compose.py` lowers them into position, adds what joins them and turns the
half 180 degrees into the whole map.

**The source world is not in the repository.** It is the author's, uploaded to a session as its four region
files, and the script reads it and never writes over it. Everything the script adds is wool, so texturing is
left open, and every lofted surface keeps its control points as marker blocks the way the sketch does.

## Running it

```bash
python3 sketches/fire-and-ice/compose.py <sketch>/region <out>/region --push 6 --head 8 --head-room 8 --cover 4
```

```bash
python3 sketches/fire-and-ice/render.py <out>/region top.png top -60,110,_,99,-110,210 3
```

```bash
python3 sketches/fire-and-ice/render.py <out>/region lane.png iso 28,68,0,60,-72,42 5 1
```

**A build takes about a second and prints its own report.** It names the lane's walk height, both roofs, the
thinnest cover over them with the columns that fall short, and where each tunnel ends. `--no-rotate` builds the
one half alone. The four region files it writes drop into a copy of the sketch world's `region/` folder.

## What it builds

| Piece | Where, in the half's own coordinates |
|---|---|
| Bunker | the sketch's floating copy moved by (−35, −61, −43) onto the original, whose core and quartz terrace are kept; the purple pit sunk to y 24 |
| Wool lane | the floating lane moved by the same offset and `--push` further down: long lane x 50–65, z −51…−4; west arm x 36–65, z −39…−34; wool area x 36–59, z −63…−52 |
| Roof | bedrock from z −34 north, one layer with grey wool above; walls bedrock to four over the walk and grey wool facade above that; the long lane's east side left open |
| Drift ramp | from the lane's south end at z −6 up to the floor at z 38, curving west at the top |
| Retaining sheet | lime face, green back, two thick, along the floor's east edge through the sketch's emerald points, leaning two blocks east as its upper points do |
| Cracks | K1 from the floor into the west arm; K2 in the middle, whose turned twin makes a staggered pair across the centre line |
| Middle | floor fitted to the valley floor's measured south edge, out to the centre line at z 48, and a spur off the south peak |
| Mountain | two lofts sharing one row: low terrain from under the facade top back eight blocks, high terrain over a ridge at x −40 |
| Tunnels | a hall at x 10–21, z −46…−30; corridors and stair flights to it from the spawn and the pit's back room, on to the west arm, and up to the core terrace at y 56 |
| Turn | 180 degrees about block (24, 48) |

**Each surface is a list of rows of points, and two surfaces meet exactly where they share a row.** `loft.py`
joins a row's points with a centripetal Catmull-Rom spline, which passes through every point and rounds off a
point that sticks out, then joins the rows with a second spline across them. A crack is rings of points lofted
top to bottom into a one-block shell, with the ground inside each ring carved.

## How deep the lane sits

**The lane has to sit `headroom − 2` blocks below where its floating copy projects for four blocks of ground
to stay over its roof.** The binding place is the wool area's east wall, x 63–64 and z −65…−50, under the
shelf's rim at y 29. Measured over the 1,011 roofed columns:

| Headroom | push 4 | push 6 | push 8 |
|---|---|---|---|
| 8 | cover 3, 11 short | cover 5, none short | cover 7 |
| 10 | cover 1, 46 short | cover 3, 11 short | cover 5, none short |
| 12 | cover 0 | cover 1, 46 short | cover 3, 11 short |

## Colour key

| Block | Is |
|---|---|
| light grey wool | the floor, the ramp and the middle |
| white wool | the lane's walk surface, and the crack shells |
| lime / green wool | the retaining sheet's face and back |
| yellow / light blue wool | low and high terrain |
| grey wool | the stone-sheet facade over bedrock, and the roof's top layer |
| cyan, brown, blue wool | tunnel walls, floors and roofs; orange for stair flights, magenta for the hall |
| black wool, red wool | the wool's plinth and the goal block on it |
| emerald, iron, gold | control points: the sheet and ramp, the crack rings, the terrain rows |

## Files

| File | Is |
|---|---|
| `compose.py` | the composition, its parameters and every point list |
| `loft.py` | curves, lofted surfaces and their voxels |
| `anvilw.py` | a 1.8 Anvil region writer; lighting is left for the server to compute and the biome is Ice Plains |
| `render.py` · `colours.py` | top-down and isometric pictures, leaving out the sketch's floating reference pieces |
