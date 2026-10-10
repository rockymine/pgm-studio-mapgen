# The layer document, draft 1

A board stated as data: ordered layers, each one operation over the areas it is drawn in, built in fixed stages
and kept as it ran. This is the shape the sketch tool's document takes in Studio 2.0. `pgmvox.document` builds
it, and `freeform/lib/examples/layers/island.layers.json` is a whole board written in it.

## What it is for

**The document replaces the sketch, and the drawing tools stay.** A rectangle, a polygon, a lasso or a polyline no
longer is ground; it is the area or the line of a layer, and the layer says what happens there. The order of the
layers is the order the board is built in. Review notes attach to layers and places, and the history of a board
is the history of its layers.

**Every layer is kept as it ran.** The builder returns each layer with the heights after it and the columns it
changed. A stepper through a board, which the Riftwater page had to instrument the board's code for, falls out of the
build.

## The stages

**A document builds in seven stages, always in this order.** A layer belongs to one stage, and within a stage the
layers run as listed.

| Stage | Key | What it does |
|---|---|---|
| fields | `fields` | named noise, read by name from any layer |
| ground | `ground` | the heights: outline, base, landforms, rivers, graded paths |
| paint | `paint` | the top block of each column: the first paint layer that applies wins |
| lay | `lay` | columns laid to the heights, rock in beds, soil by slope, the paint on top, the underside |
| water | `water` | the water each river holds, its bed painted by its own stack |
| build | `build` | what stands on the finished ground: a path's surface and steps, walls, hedges, fences |
| dress | `dress` | trees and scattered things |

## Areas

**An area is where a layer works, and every area gives the same thing: a distance.** It is 0 at the area's centre
or deepest point, 1 on its rim and over 1 outside. That one number is what lets any area carry any operation, so a
crater drawn with the lasso is the same crater as one stated as a circle.

| Area | Written | The distance |
|---|---|---|
| circle | `{"circle": {"at": [x, z], "r": 10}}` | from the centre, in radii |
| ellipse | `{"ellipse": {"at": [x, z], "rx": 14, "rz": 11, "angle": 30}}` | from the centre, 1 on the rim |
| polygon | `{"polygon": [[x, z], ...]}` | 1 − depth / deepest inside, so highest where widest |
| rectangle | `{"rect": [x0, z0, x1, z1]}` | as a polygon |
| line | `{"line": {"pts": [[x, z], ...], "width": 6}}`, or `{"near": "fluss"}` | from the line, in half-widths |
| board | `{"board": {}}` | 0 everywhere |

**Two keys go on any area.** `rough` (`amp`, `cell`, `seed`) adds noise to its distance, which bends a circle out of
round and frays a polygon's rim. `rise`, `depth` or `top` overrides the layer's own number for that one area.

## Ground layers

**A ground layer is one operation, its numbers and its areas.** Four words, common to every operation, say how it
meets the ground and itself.

| Key | Means |
|---|---|
| `mode` | `set`, `lift` (only raises) or `cut` (only lowers) |
| `join` | the p by which the areas of one layer melt together; 0 is the plain maximum, 1.6 fills the saddle |
| `melt` | the k in blocks over which a form with its own surface (a crater's bowl) rounds into the ground |
| `soft` | the outer share of each area over which the change eases to nothing |

**The operations draft 1 builds:**

| `op` | Numbers | From pgmvox |
|---|---|---|
| `outline` | `box`, `insets` per side (a number or a field) | `shapes.island` |
| `base` | `height`, `terms`: `ramp`, `gauss`, `tilt`, `noise` | `field.terms` |
| `mound` | `rise`, `power` | the rise of `landform.mound`, joined |
| `crater` | `floor`, `flat`, `slope`, `melt` | `landform.crater`'s bowl through `smooth_min` |
| `level` | `top` (a height or `median`), `inner`, `outer` | `landform.level` |
| `noise` | `field`, `rise` | a field added inside the areas |
| `river` | `line`, `width`, `depth`, `water`, `bank` | `landform.watercourse` |
| `path` | `line`, `width`, `max_grade`, `shoulder` | `landform.grade` |

**The island's twin hills are one layer of two ellipses.** `"join": 1.6` melts them into one ridge with a saddle,
and the second states its own `rise`:

```json
{"id": "zwillingshuegel", "op": "mound", "mode": "lift", "rise": 11, "join": 1.6, "soft": 0.3,
 "areas": [{"ellipse": {"at": [-38, 14], "rx": 14, "rz": 11}},
           {"ellipse": {"at": [-18, 20], "rx": 12, "rz": 9, "angle": 30}, "rise": 9}]}
```

## Paint

**Painting is a stack, and for each column the first layer that applies wins.** A paint layer is a block and its
conditions: a slope range in degrees, an area, a height band and bounds on a noise field. The area may be drawn or
may name another layer's line, so the river's sandy bank is the river's own line, twelve blocks wide:

```json
{"block": "SAND", "slope": [null, 30], "area": {"line": {"near": "fluss", "width": 12}}}
```

**A column no layer takes is grass, or stone past 55 degrees.** Under the top, `lay` puts soil whose depth follows
the slope and rock in beds that follow the surface. The water's bed has a stack of its own under `water.bed`.

## Build layers

**What stands on the ground comes after the ground is final, so it follows the ground without being told to.**

| `op` | Numbers | From pgmvox |
|---|---|---|
| `surface` | `near` (a path layer), `blocks`, `weights`, `steps`: none, `stairs` (`stair`) or `half` (`slab`) | `route.pave`, `route.steps`, `route.halfsteps` |
| `wall` | `line` or `near` + `offset`, `height`, `width`, `crown` (`follow`, `level`, `grade`), `run`, `blocks`, `weights`, `cap`, `crenel`, `gap`, `closed` | `build.line_wall` |

**A hedge, a wall and a fence are the same layer with different blocks.** The island's hedge runs four blocks off
the road with a gap every fourteen, and its curtain wall holds its crown level over runs of five:

```json
{"id": "hecke", "op": "wall", "near": "strasse", "offset": 4, "height": 1, "blocks": [["LEAVES", 4]], "gap": [14, 2]}
```

**A path is two layers, because it does two things at two times.** The `path` layer grades the ground in the
ground stage; the `surface` layer lays its blocks and steps once the ground is laid. Half steps are blocks and
slabs held to half a block between neighbours, the way Tamarisk Wash lays its ghats; stairs put a stair on every
one-block rise.

## What draft 1 does not hold

**Riftwater is not yet a layer document.** Its ground splits north from south along the river's line and mixes
two term sets by a weight, and five of its steps are still its own code: the mill pond, the westfall, the pond
bed, the square's exact level and most of its dressing. A `mix` layer and a `lake` operation would carry the first
four.

**Three stages have no layers yet.** Volume (caves, arches, bores, slabs at their own height), buildings (houses on
their sites) and pieces (objectives, spawns) are pgmvox calls a board makes after `document.build`. Symmetry is not
in the document either: the island is built whole.

**`melt` works on the crater alone.** A level top or a butte with a surface of its own would melt the same way
through `smooth_max`, and the operation list grows one row at a time from the shapes pgmvox already carries.
