# 04 — an organic outline

**The technique: replacing a compiled polygon's vertex ring with a drawn one, and bending its edges with
Bézier controls. This is how `opus5-elderwold` and `opus5-cairnmeadow` stop looking like rectangles.**

The plan is `02-theme`'s, unchanged — same two pieces, same evaluation, same objectives. The finish gains
one key and the square becomes a coastline.

## Why the plan is the wrong place for this

A plan is written in **cell rectangles**, so a plan can state where ground is and never what shape its edge
is. The two maps this showcase is named for prove it from the other end: `elderwold`'s whole plan is four
rectangles and `cairnmeadow`'s is three, and both read as landscapes. The outline is entirely the finish's.

The board under this one is a *square* — one 20 × 20-cell piece — which is the plainest case there is and
therefore the clearest: whatever the coast ends up being, nothing else on the board contributed to it.

## What the compile hands you

`POST /plan/compile` fuses abutting pieces of equal height into one polygon per component. On this board that
is one shape, and it is a rectangle:

```
s0  polygon  4 verts  [[-50,-50],[50,-50],[50,50],[-50,50]]     the island
```

Read that ring and you have the board's silhouette as a list of corners. **It is yours to redraw**, and
redrawing it is the whole of this document.

## The whole technique

```json
"shapePropsById": {
  "s0": { "vertices": [[46,-50],[42,-35.71],[47,-21.43],[41,-7.14], … 28 in all … ],
          "controls": { "0": {"in":[44.62,-51.38],"out":[47.38,-48.62]}, … } }
}
```

`shapePropsById` merges any field onto a compiled shape, so `vertices` replaces the ring and `controls`
adds the curve. Nothing else in the document changes and nothing upstream knows.

**28 vertices, one every 14 blocks round the square's own perimeter**, each pushed *inward* along that
edge's normal by nought to nine blocks. The count is the whole budget: a corner every 8 to 15 blocks gives an
edge that wanders, and one every 40 gives a rectangle with rounded corners. Pushing only inward is what keeps
the coast inside the board the plan drew.

**The offsets have period 14, so the ring is its own `rot_180` image.** A board-wide island is centred on the
mirror, so the fan lands back on the cells it came from; a ring that reflects onto itself makes that a no-op
by construction instead of a merge to reason about. And four of the twenty-eight — the samples over the spawn
pads at either end — are pushed **nought**, because a spawn standing off the coast is a spawn on a jetty.

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

`k = 0.22` here — the same `k` a `bendShapes` entry takes, which is the other way to ask for this. Below
about 0.15 the ring still reads as straight segments; above about 0.35 a handle overshoots its own edge and
the outline loops back on itself. This is arithmetic done once to produce a committed document — the ring in
the finish is the artifact, not the script.

## Two constraints the coast has to respect

**The spawn pads must stay on land.** A `spawn` rectangle is its own compiled shape with its own ground, so
the coast cannot strand a pad outright — but a pad standing proud of the shore is a platform in the sea, and
`WX11` says so: *"spawn `spawn-1` stands 9 blocks above the cell beside it"*. The four samples over
`x −7..7` at `z ±50` are therefore pinned at the full extent, and the complaint does not appear.

**The objectives must stay reachable.** The two cairns sit at `(0, 22)` and `(−1, −23)`, inside the ring
wherever it is drawn, and the pre-flight's traversability walk is what proves it rather than the picture.
A bay cut deep enough to isolate one would block the export gate, not merely look odd.

## A board of several shapes redraws every ring, and the seams do not move

The board under this one is one piece, so its ring is all coast and every sample is free to move. A board of
fourteen pieces at seven surfaces compiles to a ring apiece, and on those rings an edge is one of two things.
An edge facing the void is coast, and drawing it in shortens the coast. An edge **shared** with the
neighbouring shape is a seam, and drawing one side of a seam in leaves a strip of void between two pieces
that were flush — the fault looks like a coastline and is a hole.

The two are told apart by what lies two blocks off the edge, so the rule is per step rather than per shape:
walk every edge a block at a time, ask whether the cell off its outward side holds ground, take a sample at
each original vertex, at each point where an edge changes kind, and every fourteen blocks along a run of open
shore — and move only the samples strictly inside such a run. `opus5-slipway` is the worked example: nine
compiled rings, of which four have no void-facing edge at all and never move, and the upland's is a
stretched T whose notch is two vertices.

**The handles need clamping on a ring like that.** Catmull-Rom's tangent is the chord between a sample's
neighbours, which is right on this board's evenly-spaced twenty-eight and wrong where a compiled corner has
one neighbour a block away and the other seventy: the chord swings the curve clear outside the polygon.
Clamp each handle to `k` times its **shorter** edge, and give a sample that did not move no handle at all —
which is also what holds a seam still.

## What it costs, measured

| | `02-theme` | `04-organic-outline` |
|---|---|---|
| extent | 100 × 100 | **102 × 102** — the Bézier fringe bulges a block past the vertices |
| ground | 10 000 | **8 174** — the bays are the 18% taken out |
| reached | 2 451 | **2 454** — unchanged, because the journeys are unchanged |
| dead | 7 549 (75.5%) | **5 720 (70.0%)** |
| plan evaluation | score 0, valid | **unchanged** — the plan was not touched |
| export gate | OPEN | OPEN |

The dead share **fell** while the ground fell faster, which is the point worth keeping: the coast takes its
bites out of corners nothing crosses and leaves the ground the two journeys use exactly where it was.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-topdown.png` | the coast, and the two spawn pads sitting flush in it |
| `renders/world-traversability.png` | that both cairns are still in the spawns' own component |
| `renders/coverage.png` | which of the new bays a journey actually goes into |
| `02-theme/renders/world-topdown.png` | the same board as a square |

## Limits

The outline is drawn and the **interior is still flat**. A coast with no relief behind it reads as a table
top with a decorative edge, which is what this board is: `07-hill` onward are what goes inside it, and
`10-landform-shapes` is `cairnmeadow`'s other half — landforms authored as shapes with `height_mode` and a
`skirt` rather than as marks.
