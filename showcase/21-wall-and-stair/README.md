# 21 — a wall you can walk on, and the two passes that eat it

**The technique: a defensive wall as an override add on the ground layer, a gate as a gap in it, a
flight up as one anchored polygon — and `keepClear`, which is what stops the road repainting its top
and the channel cutting it out.**

This forks `02-theme`. No storeys: everything here is on the ground layer, which is the point — a wall
built out of terrain is *terrain*, and that is the whole difficulty.

## The document

```json
"addShapes": [
  { "id": "wall", "type": "rectangle", "operation": "add", "override": true, "keepClear": true,
    "floor": 0, "base_height": 14, "theme": "wall",
    "min_x": -40, "min_z": -2, "max_x": -4, "max_z": 2 },
  { "id": "stair", "type": "polygon", "operation": "add", "override": true, "keepClear": true,
    "floor": 0, "base_height": 14, "theme": "wall", "height_mode": "level", "skirt": 0,
    "vertices":       [[8,-7],[12,-7],[12,-2],[8,-2]],
    "anchor_heights": [   9,    9,      14,     14  ] }
]
```

**Two shapes for a wall right across the board with a gate in it and a stair on each face** — because
`rot_180` fans them. The wall is drawn from the west edge to `x −4` and its image runs from `x 3` to
the east edge; the gap between the two is the gate, and it is a gap rather than a hole because a hole
in a shape is a subtract and a subtract is a claim about the whole stack (`20-undercroft` measures
that). The stair climbs the wall's north face on the east side, and its image climbs the south face on
the west.

Fourteen courses (`floor 0`, `base_height 14`) over ground at y8 means the rampart is walked at y13 —
five courses of it.

**A wall across the mirror has to be drawn once.** Written as two boxes either side of the gate, each
one's image lands on the other and the wall comes out twice its stated thickness, with the gate
narrowed by the offset a cell mirror carries (`−1−x`, not `−x`). Drawing half of it and letting the
fan finish it is not a shortcut; it is the only statement that means what it looks like.

## The flight is one rectangle a course

One polygon, four vertices, two anchors at 9 and two at 14 over a five-block run. Measured up the
middle of it:

```
GET …/column?at=10,z
  z −8  y 8   the meadow      z −5  y 10      z −3  y 12
  z −7  y 8   the foot        z −4  y 11      z −2  y 13   ← the rampart
  z −6  y 9
```

Five courses over five blocks, every rise exactly one. **A ramp does do this**, at any gradient: the
rasterizer samples a shape's own surface at each cell's centre and **floors** it into the column, so a
1:1 grade lands one course a cell rather than alternating noughts and twos. Rounding to nearest puts
every sample of that grade exactly on the boundary, which is what made a flight of rectangles the only
reliable form before. It is not any more, and a flight is one shape.

The image of the same polygon descends the wall's south face on the other half of the board:

```
GET …/column?at=-11,z    z 1  y 13   z 3  y 11   z 5  y 9
                         z 2  y 12   z 4  y 10   z 6  y 8
```

## What the two passes do to it, and what stops them

The dressing pass runs after the painter and works off **the surface**. Two of its props rewrite what
they cross, and neither can tell a wall from the ground beside it, because the painter wrote both with
a theme:

- **A stroke swaps the top block of every column it crosses.** A road through the gate would repaint
  the wall's top course in gravel, fourteen courses above the road.
- **A channel's water line is the *lowest* surface its band crosses**, and every other column in the
  band is cut down to that line. A wall standing five courses over a moat comes out as a **hole
  through the wall, filled with water** — measured on the map this board was cut from: stone brick
  stopping at y24 with water at y26–27, twenty courses gone.

Both guards that already exist — `IsKeptClear`, `IsStamp` — miss it, because a wall drawn as an
override add is terrain by construction. `keepClear: true` is the answer: the shape's own columns join
the keep-out as `KeepOut.Structure`, **exactly and with no margin**, and a prop that lands there is
`DR-KEEP` naming the cell. No margin is the design point — a two-block verge either side would close
the gate the road runs through.

This board carries both props to prove it:

```json
"dressing": { "props": [
  { "kind": "stroke", "id": "gate-road", "route": true, "radius": 3,
    "points": [[0, -16], [0, 16]], "pave": { "kind": "solid", "id": 13 } },
  { "kind": "water", "id": "moat", "radius": 5, "depth": 3, "shore": 3,
    "points": [[-40, 8], [40, 8]] }
] }
```

The road runs the length of the board through the gate; the moat runs its width eight blocks south of
the wall, so its band reaches the wall's own columns. Read back:

```
GET …/column?at=0,0     y8  Gravel        — the gate lane, paved, between the two halves of the wall
GET …/column?at=-20,0   y13 Stone Bricks  — the wall, kept, top course and all
GET …/column?at=-20,3   y8  Water         — the moat, one block past the wall's own face
```

**A keep-out stops a prop; it does not route one.** The road stops at the wall's columns and resumes
past them. Where a road would cross a marked shape rather than run through a gap in it, the road wants
redrawing — marking the shape only saves it from being eaten.

## What to look at

| | |
|---|---|
| `GET …/render/section?axis=x&at=0&from=-50&to=50&scale=6` | the wall along its own line, the gate in the middle of it |
| `GET …/render/section?axis=z&at=10&from=-20&to=10&scale=10` | the five treads in section, one course each |
| `renders/world-heightmap.png` | the wall as one band across the board, a stair notched into each face |
| `GET …/column?at=0,0` · `?at=-20,0` | the gate paved, the wall kept |

```bash
python3 tools/drive.py showcase/21-wall-and-stair "Wall and Stair" --out showcase/21-wall-and-stair/world
```
