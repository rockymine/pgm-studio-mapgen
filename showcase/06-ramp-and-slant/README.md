# 06 — a ramp, and a slab that leans

**The technique: `anchor_heights`. One field, two opposite uses — below the build cap it is a way up, above
the ground beside it it is an obstacle — and the ceiling it moves for the whole board.**

The plan is `02-theme`'s with one number changed: the wool room stands at `surface` 17 instead of 9, eight
blocks over the lane that feeds it. Nothing on the plan gets you up there. The finish does.

## What an anchor is

A shape's height is a single `base_height` unless it says otherwise. `anchor_heights` states **one height per
vertex**, in the vertex array's own order, and the surface between them is triangulated — the outline is
ear-clipped and every cell takes the barycentric height of the triangle it falls in.

```json
{ "id": "ramp", "type": "polygon", "operation": "add", "override": true,
  "relief_scope": "exclude", "theme": "ramp",
  "vertices":       [[21,75],[34,75],[34,95],[21,95]],
  "anchor_heights": [   9,      9,      17,     17   ] }
```

Two anchors at 9 and two at 17 over a 20-block run: a plane, climbing eight blocks in twenty. Measured up the
middle of it:

```
GET …/column?at=27,z
  z 75  y  8      z 81  y 11      z 87  y 13      z 93  y 15
  z 77  y  9      z 83  y 11      z 89  y 14      z 94  y 16   ← flush with the room's own ground
  z 79  y 10      z 85  y 12      z 91  y 15
```

Every rise is 0 or 1. That is the number that matters and it is the only one a picture will not give you.

**Control lives on the outline.** Every height an anchored shape can state is at a *vertex*, so the maximum of
the surface is always on the edge — a hill in the middle of a shape is unreachable this way by construction,
and a concave footprint gets triangulated *across* its own notch. That is where relief starts and this stops;
`07-hill` is the other instrument.

## The same field, standing up

```json
{ "id": "slab", "type": "polygon", "operation": "add", "override": true,
  "relief_scope": "exclude", "theme": "slab",
  "vertices":       [[-38,34],[-27,32],[-25,52],[-36,55]],
  "anchor_heights": [   26,      19,      17,      24   ] }
```

Four differing anchors on a shape whose ground is nine blocks below it: a leaning slab, its top falling from
y26 to y17 across eleven blocks, its sides vertical. It is terrain — it takes a theme, it holds its own
height because `relief_scope: "exclude"` keeps it out of the island's solve — and it is an obstacle, because
nothing walks up a 9-block face.

**Which way it leans is a decision about which side players are funnelled to.** This one falls toward the
board's middle, so the flank behind it is covered from the strait and the way past it is on the low side.

## The cost nobody mentions: it raises the ceiling for everyone

`BuildIntent.MaxHeight` is derived at build time as twenty blocks over the **highest ground the world
actually builds**, and an erected shape is one of those columns. Measured, on two boards that differ only by
this shape:

| Board | highest ground | `<maxbuildheight>` |
|---|---|---|
| `02-theme` | y8 | **29** |
| `06-ramp-and-slant` | y26 (the slab) | **46** |

So the slab bought seventeen blocks of clear air over the *whole* board, including over itself. A shape tall
enough to be un-bridgeable raises the cap that would have capped a bridge over it — which is why a tall shape
is a **colonnade, a picket or a spine** that costs an attacker material and visible time, and is not a wall
nobody passes.

## The lint that is right about the plan and stale about the world

```
[complaint] WL11  wool room approach climbs 8 blocks at 'rise'–'room' — an attacker arrives across it,
                  so use 1-level steps or a ramp against the room
```

That is exactly what this board did: there **is** a ramp against the room. `WL11` is a plan lint and reads
plan-piece surfaces, and a ramp authored in the layout is a level below anything it can see. The complaint is
correct about the document it reads and says nothing about the world that was built.

The read that settles it is the column transect above. A lint that cannot see the ground is a lint whose
silence and whose complaint are worth the same.

## Ramp or stair?

`05-steps` climbs four blocks over the same twenty and this climbs eight, and they are different instruments
rather than two settings of one:

| | `05-steps` | `06-ramp-and-slant` |
|---|---|---|
| stated in | the **plan** — one piece per tread | the **layout** — one polygon, four anchors |
| granularity | the cell: a 5-block tread | the block: the surface moves every one or two |
| reads as | built masonry — nosing, riser, going | a graded way up |
| paint | a theme per tread, alternating | one theme over the run |
| costs | four pieces, two themes, four `themeById` keys | one shape |

A board wants both, in different places: a flight where the ground is architecture, a ramp where it is
landscape.

## What to look at

| Picture | Says |
|---|---|
| `GET …/render/section?axis=z&at=27&from=70&to=100&scale=10` | the ramp in elevation, meeting the keep |
| `GET …/render/section?axis=x&at=44&from=-45&to=-20&scale=10` | the slab's lean, and its vertical sides |
| `renders/world-heightmap.png` | both, from above, where neither is legible — which is the point of a section |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, 1 × `WL11` complaint |
| ramp | 8 blocks over 20, every rise 0 or 1, flush with the room at y16 |
| slab | top y26 → y17 over 11 blocks, standing 9–18 over ground at y8 |
| `<maxbuildheight>` | **46**, against 29 on the same board without the slab |
| `GET …/preflight` | export gate **OPEN** |
