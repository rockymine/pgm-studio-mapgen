# 21 — a wall you can walk on, and the two passes that eat it

**The technique: a defensive wall as an override add on the ground layer, a gate as a gap in it, a
flight up as one rectangle per course — and `keepClear`, which is what stops the road repainting its
top and the channel cutting it out.**

This forks `02-theme`. No storeys: everything here is on the ground layer, which is the point — a wall
built out of terrain is *terrain*, and that is the whole difficulty.

## The document

```json
"addShapes": [
  { "id": "wl1", "type": "rectangle", "operation": "add", "override": true, "keepClear": true,
    "floor": 0, "base_height": 14, "theme": "wall",
    "min_x": -40, "min_z": 21, "max_x": -4, "max_z": 24 },
  { "id": "wl2", … "min_x": 4, "max_x": 40 … },
  { "id": "ws1", … "base_height": 14, "min_x": 8, "min_z": 20, "max_x": 12, "max_z": 21 },
  { "id": "ws2", … "base_height": 13, "min_x": 8, "min_z": 19, "max_x": 12, "max_z": 20 },
  …
]
```

The wall runs the board's width at `z 21..23`, fourteen courses (`floor 0`, `base_height 14`), so it
is walked at y14 over ground that stands at y9 — five courses of rampart. **The gate is the gap
between the two boxes**, `x -4..4`: a wall is not one shape with a hole in it, because a hole in a
shape is a subtract and a subtract is a claim about the whole stack (`20-undercroft` measures that).

## The flight is one rectangle a course

`ws1`…`ws5` step away from the wall's north face, each a course shorter than the last, and five more
mirror them on the south face. Five courses, five rectangles, one block of run each.

**A ramp will not do this.** A slope at one course a cell rasterizes into treads of two, and a
two-block rise costs a placed block to climb — so a rampart reached by a ramp is a rampart the walk
prices in blocks and `SK11` may call unreachable. Every flight on this board and in
`maps/opus5-liminal-dtm-ii` is stated a course at a time for that reason.

The board leaves fifteen courses of land north of its void, and a wall plus two flights has to fit in
them: three of wall and five of flight either side. That is why the wall is five high rather than
eight — geometry the board allows, not a preference.

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
    "points": [[0, 5], [0, 38]], "pave": { "kind": "solid", "id": 13 } },
  { "kind": "water", "id": "moat", "radius": 5, "depth": 3, "shore": 3,
    "points": [[-40, 30], [40, 30]] }
] }
```

Read back:

```
GET …/column?at=0,22    y8  Gravel        — the gate lane, paved
GET …/column?at=20,22   y13 Stone Bricks  — the wall, kept, top course and all
```

**A keep-out stops a prop; it does not route one.** The road stops at the wall's columns and resumes
past them. Where a road would cross a marked shape rather than run through a gap in it, the road wants
redrawing — marking the shape only saves it from being eaten.

## What to look at

| | |
|---|---|
| `renders/section-wall-z22.png` | the wall along its own line, gate and flights in it |
| `renders/section-flight-x10.png` | the five treads in section, one course each |
| `GET …/column?at=0,22` · `?at=20,22` | the gate paved, the wall kept |

```bash
python3 tools/drive.py showcase/21-wall-and-stair "Wall and Stair" --out showcase/21-wall-and-stair/world
```
