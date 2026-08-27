# 06 — a ramp, and a slab that leans

**The technique: `anchor_heights`. One field, two opposite uses — below the build cap it is a way up, above
the ground beside it it is an obstacle — and the ceiling it moves for the whole board.**

The plan is `02-theme`'s, untouched. The finish states a terrace nine blocks over the field, a ramp up onto
it, and a leaning slab on the far flank — all three in the layout, because none of them is a thing a plan can
say.

## What an anchor is

A shape's height is a single `base_height` unless it says otherwise. `anchor_heights` states **one height per
vertex**, in the vertex array's own order, and the surface between them is triangulated — the outline is
ear-clipped and every cell takes the barycentric height of the triangle it falls in.

```json
{ "id": "ramp", "type": "polygon", "operation": "add", "override": true,
  "relief_scope": "exclude", "theme": "ramp",
  "vertices":       [[24,-8],[40,-8],[40,12],[24,12]],
  "anchor_heights": [   9,      9,     18,     18   ] }
```

Two anchors at 9 and two at 18 over a 20-block run: a plane, climbing nine blocks in twenty. Measured up the
middle of it:

```
GET …/column?at=32,z
  z −8  y  8      z  0  y 11      z  6  y 14      z 12  y 17   ← flush with the terrace
  z −6  y  9      z  2  y 12      z  8  y 15      z 14  y 17
  z −4  y 10      z  4  y 13      z 10  y 16
```

Every rise is 0 or 1. That is the number that matters and it is the only one a picture will not give you.

**The terrace is the other half of the gesture, and it is one line.** A ramp to nowhere is a wedge:

```json
{ "id": "terrace", "type": "rectangle", "operation": "add", "override": true,
  "floor": 0, "base_height": 18, "relief_scope": "exclude", "theme": "ramp",
  "min_x": 24, "min_z": 12, "max_x": 44, "max_z": 36 }
```

One `base_height` where the ramp needed four anchors, because a level plateau is the case `base_height`
already answers. The two share a theme and meet flush at `z 12`, so the join is not a seam in the world.

**Control lives on the outline.** Every height an anchored shape can state is at a *vertex*, so the maximum of
the surface is always on the edge — a hill in the middle of a shape is unreachable this way by construction,
and a concave footprint gets triangulated *across* its own notch. That is where relief starts and this stops;
`07-hill` is the other instrument.

## The same field, standing up

```json
{ "id": "slab", "type": "polygon", "operation": "add", "override": true,
  "relief_scope": "exclude", "theme": "slab",
  "vertices":       [[-40,14],[-29,12],[-26,32],[-38,35]],
  "anchor_heights": [   26,      19,      17,      24   ] }
```

Four differing anchors on a shape whose ground is seventeen blocks below it: a leaning slab, its top falling
from y25 to y16 across fourteen blocks, its sides vertical. Measured across it:

```
GET …/column?at=x,20
  x −41  y  8   the meadow            x −32  y 19
  x −38  y 23   the slab's high side  x −29  y 17   its low side
  x −35  y 21                         x −26  y  8   the meadow again
```

It is terrain — it takes a theme, it holds its own height because `relief_scope: "exclude"` keeps it out of
the island's solve — and it is an obstacle, because nothing walks up a 15-block face.

**Which way it leans is a decision about which side players are funnelled to.** This one falls east, toward
the board's middle, so the flank behind it is covered and the way past it is on the low side.

**All three are drawn on one half of the board, and that is not decoration.** `rot_180` fans every authored
shape, so each one has to stay clear of the *others'* reflections as well as of the others: the terrace at
`x 24..44, z 12..36` images onto `x −45..−25, z −37..−13`, which is where the slab would have been had it
kept the position it was drawn at on a board twice as long.

## The cost nobody mentions: it raises the ceiling for everyone

`BuildIntent.MaxHeight` is derived at build time as twenty blocks over the **highest ground the world
actually builds**, and an erected shape is one of those columns. Measured, on two boards that differ only by
this shape:

| Board | highest ground | `<maxbuildheight>` |
|---|---|---|
| `02-theme` | y8 | **29** |
| `06-ramp-and-slant` | y25 (the slab) | **45** |

So the slab bought sixteen blocks of clear air over the *whole* board, including over itself. A shape tall
enough to be un-bridgeable raises the cap that would have capped a bridge over it — which is why a tall shape
is a **colonnade, a picket or a spine** that costs an attacker material and visible time, and is not a wall
nobody passes.

## The plan lints see none of it, in both directions

Nine blocks of elevation appear on this board and **`/plan/evaluate` scores it 0 with no lint at all** — the
same answer it gives `02-theme`, which is flat. `WL11` and `EL1` read *plan-piece surfaces*, and every piece
here is at the global 9; a terrace, a ramp and a fifteen-block slab authored in the layout are a level below
anything either can see.

That cuts both ways and the second way is the one to remember. On `05-steps` the same lints complain about a
flight that is walkable; here they are silent about a slab nothing can climb. **A lint that cannot see the
ground is a lint whose silence and whose complaint are worth the same**, and the read that settles either is
the column transect.

## Ramp or stair?

`05-steps` climbs four blocks over twenty and this climbs nine, and they are different instruments rather
than two settings of one:

| | `05-steps` | `06-ramp-and-slant` |
|---|---|---|
| stated in | the **plan** — one piece per tread | the **layout** — one polygon, four anchors |
| granularity | the cell: a 5-block tread | the block: the surface moves every one or two |
| reads as | built masonry — nosing, riser, going | a graded way up |
| paint | a theme per tread, alternating | one theme over the run |
| costs | seven pieces cut out of the field, two themes, four `themeById` keys | one shape |
| climbs | 4 blocks over 20 | 9 blocks over 20 |

A board wants both, in different places: a flight where the ground is architecture, a ramp where it is
landscape.

## What to look at

| Picture | Says |
|---|---|
| `GET …/render/section?axis=z&at=32&from=-12&to=40&scale=10` | the ramp in elevation, meeting the terrace |
| `GET …/render/section?axis=x&at=20&from=-45&to=-20&scale=10` | the slab's lean, and its vertical sides |
| `renders/world-heightmap.png` | ramp, terrace and slab from above, where the ramp's grade is not legible |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, **no lint** — the plan is `02-theme`'s |
| ramp | 9 blocks over 20, every rise 0 or 1, flush with the terrace at y17 |
| slab | top y25 → y16 over 14 blocks, standing 8–17 over ground at y8 |
| `<maxbuildheight>` | **45**, against 29 on the same board without the slab |
| `GET …/preflight` | export gate **OPEN** |
