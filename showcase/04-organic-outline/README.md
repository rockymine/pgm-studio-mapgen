# 04 — an organic outline

**The technique: replacing a compiled polygon's vertex ring with a drawn one, and bending its edges with
Bézier controls. This is how `opus5-elderwold` and `opus5-cairnmeadow` stop looking like rectangles.**

The plan is `02-theme`'s, unchanged — same eight pieces, same evaluation, same objectives. The finish gains
one key and the board becomes a coastline.

## Why the plan is the wrong place for this

A plan is written in **cell rectangles**, so a plan can state where ground is and never what shape its edge
is. The two maps this showcase is named for prove it from the other end: `elderwold`'s whole plan is four
rectangles and `cairnmeadow`'s is three, and both read as landscapes. The outline is entirely the finish's.

## What the compile hands you

`POST /plan/compile` fuses abutting pieces of equal height into one polygon per component. On this board that
is two shapes a team:

```
s0  polygon  12 verts  [[-40,15],[40,15],[40,75],[35,75],[35,110],[20,110],[20,75],
                        [-10,75],[-10,90],[-30,90],[-30,75],[-40,75]]     the island
s1  polygon   4 verts  [[-25,30],[25,30],[25,60],[-25,60]]                the hole in it
```

Read that ring and you have the board's silhouette as a list of corners: the frontline shore, the two flanks,
the spawn tongue and the wool tongue. **Both are yours to redraw**, and the hole is as much a drawing as the
coast is.

## The whole technique

```json
"shapePropsById": {
  "s0": { "vertices": [[-39,19],[-32,15],[-23,12], … 28 in all … ],
          "controls": { "0": {"in":[-40.98,15.7],"out":[-37.02,22.3]}, … } },
  "s1": { "vertices": [[-24,34],[-8,30],[10,33],[24,37],[21,52],[6,58],[-11,56],[-25,50]],
          "controls": { … } }
}
```

`shapePropsById` merges any field onto a compiled shape, so `vertices` replaces the ring and `controls`
adds the curve. Nothing else in the document changes and nothing upstream knows.

**28 vertices for the coast, 8 for the lagoon.** The count is the whole budget: a corner every 8 to 15 blocks
gives an edge that wanders, and one every 40 gives a rectangle with rounded corners.

## The controls, and the rule that generates them

A control entry is keyed by **vertex index** and carries `in` — the handle the curve arrives on — and `out` —
the handle it leaves on. Both are **absolute world coordinates**, in the same frame as the vertices, not
offsets.

Handles written by hand fight each other and kink. The rule that does not is Catmull-Rom: **the tangent at a
vertex is the chord between its two neighbours**, and each handle reaches a fraction `k` along it.

```python
for i, (x, z) in enumerate(ring):
    px, pz = ring[i-1]; nx, nz = ring[(i+1) % len(ring)]
    tx, tz = (nx-px)*k, (nz-pz)*k
    controls[str(i)] = {"in": [x-tx, z-tz], "out": [x+tx, z+tz]}
```

`k = 0.22` here. Below about 0.15 the ring still reads as straight segments; above about 0.35 a handle
overshoots its own edge and the outline loops back on itself. This is arithmetic done once to produce a
committed document — the ring in the finish is the artifact, not the script.

## Three constraints the coast has to respect

**The strait may narrow but must not close.** The build zone spans `z −20..20` and is what joins the two
islands; the coast facing it is drawn between `z 11` and `z 20`, so the zone always overlaps land. A shore
that retreated to `z 22` would leave two blocks of unbuildable void between the zone and the ground, and the
board would come apart at the pre-flight rather than at the drawing. The headlands take the strait from 30
blocks to 22 at its narrowest, which is still inside `CT12`'s 15–40.

**The tongues stay tongues.** The spawn and the wool room are their own compiled rectangles with their own
ground, so the coast cannot strand them — but the *neck* is s0's, and pulling it in past the room's own
footprint would leave a building on an island. Here the wool tongue is drawn `x 18..38` against a room at
`x 20..35`, so the neck is wider than what stands on it.

**A hole is redrawn, not moved.** `s1` is a `subtract`, and a subtract resolves in plan only — its height is
not read. Redrawing its ring changes the shape of the lagoon and nothing else.

## What it costs, measured

| | `02-theme` | `04-organic-outline` |
|---|---|---|
| extent | 80 × 220 | **86 × 226** — the headlands bulge past the plan's own bbox |
| ground | 8 250 | **9 244** |
| dead | 271 (3.3%) | **174 (1.9%)** |
| strait | 30 blocks | 22 at the narrowest |
| plan evaluation | score 0, valid | **unchanged** — the plan was not touched |
| export gate | OPEN | OPEN |

The dead share **fell**, which is the point worth keeping: a wandering coast adds ground at the edges where
routes already run, while a rectangle adds it in corners nothing crosses.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-ground.png` | the coast and the lagoon |
| `renders/world-traversability.png` | that the strait still reads as crossed |
| `renders/coverage.png` | which of the new bays a journey actually goes into |
| `02-theme/renders/world-ground.png` | the same board as rectangles |

## Limits

The outline is drawn and the **interior is still flat**. A coast with no relief behind it reads as a table
top with a decorative edge, which is what this board is: `07-hill` onward are what goes inside it, and
`10-landform-shapes` is `cairnmeadow`'s other half — landforms authored as shapes with `height_mode` and a
`skirt` rather than as marks.
