# The layer document, draft 3

A board stated as data: ordered layers, each one operation over the areas it is drawn in, built in fixed stages
and kept as it ran. This is the shape the sketch tool's document takes in Studio 2.0. `pgmvox.document` builds
it, `freeform/lib/examples/layers/island.layers.json` is a whole board written in it, and
`freeform/lib/ports/riftwater/riftwater.ground.layers.json` is the Riftwater port's ground, 38 layers that build its
heights and water bit for bit, and `freeform/lib/examples/layers/saumland.layers.json` puts made and grown
ground on one board.

## What it is for

**The document replaces the sketch, and the drawing tools stay.** A rectangle, a polygon, a lasso or a polyline no
longer is ground; it is the area or the line of a layer, and the layer says what happens there. The order of the
layers is the order the board is built in. Review notes attach to layers and places, and the history of a board
is the history of its layers.

**Every layer is kept as it ran.** The builder returns each layer with the heights after it and the columns it
changed. A stepper through a board, which the Riftwater page had to instrument the board's code for, falls out of the
build.

## The stages

**A document builds in twelve stages, always in this order.** A layer belongs to one stage, and within a stage
the layers run as listed.

| Stage | Key | What it does |
|---|---|---|
| made blueprint | `made.cells` | the made ground's cells, read first, so the ground may refer to them as `made` and `made_top` |
| fields | `fields` | named fields, read by name from any layer |
| ground | `ground` | the heights of the grown ground: outline, base, landforms, rivers, graded paths |
| paint | `paint` | the top block of each grown column: the first paint layer that applies wins |
| lay | `lay` | grown columns laid to the heights, rock in beds, soil by slope, the paint on top, the underside |
| water | `water` | the water each river holds, its bed painted by its own stack |
| made | `made` | the made cells through the grammar, faces as deep as the drop to the grown beside them; its houses |
| volume | `volume` | bodies set into the ground: a box turned and tilted, sunk, painted in its own frame, hollowed |
| structures | `structures` | masses with patterned faces, floors laid as fields |
| build | `build` | what stands on the finished ground: a path's surface and steps, walls, hedges, fences |
| dress | `dress` | trees and scattered things, kept `clear` blocks (3 unless stated) off everything built |
| symmetry | `symmetry` | the drawn part copied onto its image, recoloured for the other team |

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

## Numbers can be fields

**Any number a layer takes may be an expression instead.** A number is itself; `x`, `z`, `H` (the heights so far),
`W` (the water so far) and `land` are the grid; any other name is a field from `fields`, which may be expressions
themselves and are evaluated in order. A one-key object is an operation over its arguments:

| Kind | Operations |
|---|---|
| arithmetic | `add`, `sub`, `mul`, `div`, `neg`, `abs`, `min`, `max`, `pow`, `exp`, `round`, `floor`, `clip`, `hypot` |
| shaping | `smoothstep`, `mix`, `where`, `full` |
| masks | `lt`, `le`, `gt`, `ge`, `and`, `or`, `not`, `inside`, `polygon` |
| sources | `fbm`, `ridged`, `line` (noise; `fbm` with `along` is one-dimensional), `distance`, `blocks`, `line_distance`, `ellipse`, `line_z` (a line's z at each x), `at` (the heights at a point), `terms` |
| landforms | `profile`, `ridge`, `level`, `blend`, `spire`, `crater`, `mound`: the pgmvox call over `H`, returning heights |

**A `set` layer writes an expression into the heights, where a mask holds.** Together with `round` (whole blocks
from here on), `water` (a water surface where a mask holds), `watercourse` and `grade` (a route held to a grade,
keeping every route graded before it and leaving water alone), it is how a board's own formulas become data. The
Riftwater port's base is one `set` layer: two term sets split at the river's line, a third mixed in toward the
west.

**A landform as an expression keeps the board exact; a named layer keeps it readable.** `mound`, `crater` and
`level` as layers take areas, `join`, `melt` and `soft`; as expressions they take the distance and numbers the
board's code passed. The studio shows the first kind as a form and the second as a formula, and both are layers.

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

## Made ground

**Made ground is a blueprint of five-block cells, and the grammar lays it.** A cell entry is a rectangle of cells,
`[cx0, cx1, cz0, cz1]`, of one `kind` at one floor `y`: flat, keep, stair (with `rises`), stacked (with `under`),
gap, water or void. Its `section` names the piece it belongs to and its `fill` how a rectangle is filled (bed,
grass, sand). `style` names the grammar's style, Brittlebush's today, and `dye` the keep's colour.

**The grown ground keeps out of the made and is read by it.** The made cells are taken out of the grown land
before anything is laid, and the grammar reads the grown tops beside it as its neighbours, so a made edge over the
meadow is a face as deep as the drop and an edge level with it is a seam. The ground stage sees the blueprint as
`made` (a mask) and `made_top`, so a layer can hold the meadow three blocks under every rim:

```json
{"id": "unter-dem-rand", "op": "set", "height": {"min": ["H", {"sub": ["rim", 3]}]}, "where": {"lt": ["near_made", 8]}}
```

with `rim` and `near_made` the fields `{"spread": ["made_top", 8]}` and `{"near": "made"}`. A house stacks whole
cells by storey: `{"layers": [[[cx, cz], ...], ...], "floor": 22, "dye": 14, "door": [[cx, cz], "s"]}`.

## Volume, structures and symmetry

**A volume layer sets a body into the ground the way Stratum set its fragments.** `box` takes `at`, `size` (width,
height, depth), `yaw`, `tilt`, `sink` (the share of its upright height under the ground), `on` (`lowest` under its
footprint, `centre` or a y), `hole` (a frame's wall, for a ring or a gate) and `paint`: a `block`, or `bands`
along one of its own axes, with a `cap`. It writes only over ground, water and plants, so trees and earlier bodies
stand.

**A structure is a mass with patterned faces, or a floor laid as a field.** `mass` pours a footprint from the
ground to `height` and patterns its faces with pgmvox's face patterns, each stated as `{"flutes": {"period": 3,
...}}`: band, courses, flutes, panels, slits, checker, windows, glyph rows and words, first match wins. `top` is a
cornice or a parapet and `bottom` a coffer. `carpet` lays floor fields over a rectangle at a course: border,
medallion, corners, diamonds, stripes, tiles, cross, star and `rings`, concentric bands round or square.

**Symmetry is the last stage, so every stage before it draws one team's part.** `half`, `mirror_x`, `mirror_z`,
`cw` or `ccw` copies what `keep` holds onto its image, turning every block's data with it, and `recolour` maps a
team's blocks to the other's.

## What draft 3 does not hold

**Riftwater's ground is data; its world is not yet.** The heights and water are the 38 layers named above, held
equal to `plan.land()` by a test. Its paint, buildings, caves and dressing are still the port's code.

**The grammar takes cells, not sections.** Claywork builds its sections from a raster and its own piece list, and
a document would need a `sections` entry beside `cells` for it, with the clay style. The fills and faces are the
style's code; a document names them and does not state them.

**Objectives, caves and the map's XML are not layers yet.** Spawns, wools, monuments and hills, the tunnels and
chambers of `pgmvox.under`, and `map.xml` are calls a board makes after `document.build`.

**`melt` works on the crater alone.** A level top or a butte with a surface of its own would melt the same way
through `smooth_max`, and the operation list grows one row at a time from the shapes pgmvox already carries.
