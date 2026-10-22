# The layer document, draft 4

A board stated as data: ordered layers, each one operation over the areas it is drawn in, built in fixed stages
and kept as it ran. This is the shape the sketch tool's document takes in Studio 2.0. `pgmvox.document.layers` builds
it, `freeform/lib/examples/layers/island.layers.json` is a whole board written in it, and
`freeform/lib/boards/riftwater-pgmvox/riftwater.ground.layers.json` is the Riftwater port's ground, 38 layers that build its
heights and water bit for bit, `freeform/lib/examples/layers/saumland.layers.json` puts made and grown
ground on one board, and `freeform/lib/examples/hold/hold.layers.json` is a board on three floors: a valley, a
second ground over it, an arch, a cave and a dungeon.

## What it is for

**The document replaces the sketch, and the drawing tools stay.** A rectangle, a polygon, a lasso or a polyline no
longer is ground; it is the area or the line of a layer, and the layer says what happens there. The order of the
layers is the order the board is built in. Review notes attach to layers and places, and the history of a board
is the history of its layers.

**Every layer is kept as it ran.** The builder returns each layer with the heights after it and the columns it
changed. A stepper through a board, which the Riftwater page had to instrument the board's code for, falls out of the
build.

## The stages

**A document builds in fifteen stages, always in this order.** A layer belongs to one stage, and within a stage
the layers run as listed.

| Stage | Key | What it does |
|---|---|---|
| made blueprint | `made.cells` | the made ground's cells, read first, so the ground may refer to them as `made` and `made_top` |
| fields | `fields` | named fields, read by name from any layer |
| ground | `ground` | the heights of the grown ground: outline, base, landforms, rivers, graded paths |
| paint | `paint` | the top block of each grown column: the first paint layer that applies wins |
| lay | `lay` | grown columns laid to the heights, rock in beds, soil by slope, the paint on top, the underside |
| water | `water` | the water each river holds, its bed painted by its own stack |
| levels | `levels` | grounds of their own over an outline, each laid, painted and watered apart, resting or hanging |
| carve | `carve` | tunnels, chambers, rooms with their halls, and shafts cut out of the laid ground |
| faces | `faces` | courses on every drop of the grown ground: a grammar's face, what lies under it, its foot |
| made | `made` | the made cells through the grammar, faces as deep as the drop to the grown beside them; its houses |
| volume | `volume` | bodies set into the ground: a box turned and tilted, sunk, painted in its own frame, hollowed |
| structures | `structures` | masses with patterned faces, floors laid as fields |
| build | `build` | what stands on the finished ground: a path's surface and steps, walls, hedges, fences |
| dress | `dress` | trees and scattered things, kept `clear` blocks (3 unless stated) off everything built, their crowns `spacing` crown radii apart (0.85 unless stated) |
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

**`lay` may state its `soil`** ([[up to degrees, depth], ...]) and turn `ledges` off, so ground steeper than the last band shows rock with no dirt between.

**A column no layer takes is grass, or stone past 55 degrees.** Under the top, `lay` puts soil whose depth follows
the slope and rock in beds that follow the surface. The water's bed has a stack of its own under `water.bed`.

## Build layers

**What stands on the ground comes after the ground is final, so it follows the ground without being told to.**

| `op` | Numbers | From pgmvox |
|---|---|---|
| `surface` | `near` (a path layer), `blocks`, `weights`, `steps`: none, `stairs` (`stair`) or `half` (`slab`) | `route.pave`, `route.steps`, `route.halfsteps` |
| `wall` | `line` or `near` + `offset`, `height`, `width`, `crown` (`follow`, `level`, `grade`), `run`, `blocks`, `weights`, `courses` (from the foot up, a block or a checker pair each), `cap`, `crenel`, `crenel_stair`, `step_stair` or `step_slab`, `ruin` (from, to, seed: broken down along that stretch), `gap`, `closed` | `build.line_wall` |
| `house` | `at`, `heading`, `L`, `W`, `storeys`, `storey`, `style` (`town`, `plaster`, `brick`, `stone`, a name in `styles`, or an object), `roof`, `pitch`, `overhang`, `door`, `jetty`, `chimney`, `walk` (a path one wide from its door `to` a line, a low hedge beside it) | `build.house` |
| `blocks` | `boxes`, each a `box` (x0, y0, z0, x1, y1, z1) and a `block`; `rel` names a house whose floor the heights are counted from | the document's own |
| `graves` | `at` (points), `facing`, `stone`, `cap`, `soil`, `flowers`, `flowered` (the share with a flower) | `props.grave` |
| `field` | `rect`, `crops`, `rows`, `ditch`, `fence`, `gate`, `scarecrows`, `y` | `props.crop_field`, `props.scarecrow` |
| `stall` | `at`, `facing`, `colours` (the roof's stripes), `width`, `post`, `foot` (a full block under each post), `counter_stair`, `goods`, `banners` (front and sides), `sides` (closed, entered from the back) | `props.market_stall` |
| `posts` | `at` (points), `stack` (blocks from the ground up: a lamp, a bollard) | the document's own |
| `round_tower` | `at`, `r` or `half` (a square with its corners cut; `cut: false` keeps them), `height`, `y`, `wall`, `floor`, `crenel`, `crenel_stair`, `quoins`, `string`, `plinth`, `door`, `openings` ([angle, y]: a wall-walk's way in; `openings_from: floor` counts y from its floor), `slit` | `build.round_tower` |
| `paving` | `area`, `blocks` (each taking an equal share), `cell` (the size of a cell one block is laid over), `seed` | the document's own |
| `hedge` | `line` or `near` + `offset`, `leaves`, `modules`, `drop`, `grass` (in the checker's gaps) | `green.hedge` |
| `small_trees` | `at` (points), `trunk`, `log`, `leaves`, `bite` | `green.round_oak` |
| `flowers` | `area`, `flowers`, `along`, `rows`, `angle` | `green.flower_rows` |
| `boulders` | `at` ([x, z, r, {rz, height, angle, shape}] each), `rock`, `accent`, `accent_share`, `sink`, `rough`, `shape` | `green.boulder` |
| `crops` | `area`, `crops`, `angle`, `rows`, `ditch`, `scarecrows` | `green.crop_rows` |

**A hedge, a wall and a fence are the same layer with different blocks.** The island's hedge runs four blocks off
the road with a gap every fourteen, and its curtain wall holds its crown level over runs of five:

```json
{"id": "hecke", "op": "wall", "near": "strasse", "offset": 4, "height": 1, "blocks": [["LEAVES", 4]], "gap": [14, 2]}
```

**A house's style is data, named once under `styles` and used by name.** An object names a `base` style and the
keys it changes: the wall blocks, `plinth`, the post `log`, and `windows` as a rhythm with a phase that centres one
block in a frame's bay.

**A style's details are each off until it names them.** `sill_in` makes the wall block under a window a stair of
the facade's kind; `quoins` and `string` dress a style without posts; `stack` stands a chimney outside the gable
and `chimney_top` caps either chimney. `joists_along`, `slab_roof`, `ridge_slab` (a ridge one wide laid in slabs, one two wide in stairs rising to each other) and `verge` with `roof_bands` (the roof's ring
and bands across it in other blocks) follow, and `plain_turned` gives a turned house no windows, one post a corner
and a door only on a straight run of three.

**A house stands on the highest ground under it, its plate filled down to the rest.** Its footprint counts as
built, so a wood keeps `clear` of it. A `blocks` layer sets boxes of one block each, for what no other layer
says: the posts and roof over a well.

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

## Faces

**A faces layer dresses the walls of the grown ground and leaves its floors to the paint.** Every column standing
`min_drop` (2) or more over a neighbour or over the void gets the layer's `courses`, top down from its rim, toward its
deepest drop; an `area` limits the columns.

**A course is data, and so is the bay.** A course is a block, `null` (keep what the ground laid, so the paint stays
on the rim), `{"block", "back", "out"}` (a block with another behind it or outside it over air; `{"block": "AIR",
"back": ...}` is an inset), `{"stair": NAME, "upside_down": true, "toward": "in" | "out" | "end"}` or `{"mix":
[[block, weight], ...]}`. `accent` is the grammar's bay: `module`, `every`, `min_air`, `frame` and `inner`, a stack or
`{"per_pos": [...]}` one stack per inner column.

**A panel frames every straight run of a face as one field.** `panel` takes `ends`, the stacks one, two, three columns
in from the nearer end of a run, and `middle`, the stack of the rest; a stair `"toward": "end"` rises to that end, and
a run shorter than `min_run` takes the plain `courses`. That is Outback's wall, a frame of spruce with a two-high
inset of slabs between stairs and the team's clay behind:

```json
{"id": "felder", "courses": [P, D, D, D, D, P, ST, ST, ST, ST, P],
 "panel": {"ends": [[P, P, P, P, P, P, P, P, P, P, P], [P, D, D, D, D, P, ST, ST, ST, ST, P],
                    [P, D, {"block": {"stair": "SPRUCE_STAIRS", "upside_down": true, "toward": "end"}, "back": RED},
                     {"block": {"stair": "SPRUCE_STAIRS", "toward": "end"}, "back": RED}, D, P, ST, ST, ST, ST, P]],
           "middle": [P, D, {"block": ["WOOD_SLAB", 9], "back": RED}, {"block": ["WOOD_SLAB", 1], "back": RED}, D, P,
                      ST, ST, ST, ST, P], "min_run": 5},
 "below": {"block": "BEDROCK"}}
```

with `P` spruce planks, `D` a mix of dirt and coarse dirt, `ST` a mix of stone, cobble and cracked stone brick and
`RED` the team's clay, written out in full in the example.

**Under the courses the layer lays `below` down to the column's bottom, and `foot` rows of bedrock under that.**
`below` is a `block`, a `lattice` (`period`, `a`, `b`: Claywork's diagonals) or `bands` (`blocks`, `width`, `y0`: courses
by height, whatever the rim), each with an `else`; left out, the beds the lay stage put there stay.

`freeform/lib/examples/layers/wandbild/` is one board in five dressings: none, Outback's panels, Claywork's face with
its panels and lattice, bands by height, and Brittlebush's edge.

## Levels

**A level is a second ground over the first, and the first stays under it.** It has an `id`, a `floor` and a
`ground` list of its own, which reads the board's fields and lines and starts at that floor; its first layer is an
`outline` with an `area` instead of a box. It is laid into a world of its own and copied in where that world holds
a block, so nothing it lays clears the ground below.

**A level may state its `soil`**, the depth of dirt under its top everywhere, so a lip of rock carried over the ground below shows rock and not a band of dirt.

**A level's outline may be a `where` mask and its underside a `bottom` field.** A bottom that rises the farther the level reaches out from the ground it rests on is a face that leans out over its own foot, steeper than upright.

**Under its edges a level tapers as a floating island does.** `underside` takes `taper` (blocks at the edge,
blocks per block in), `rough`, `seed` and `clear`. Where the taper leaves fewer than `clear` blocks of air over the
surface below, the level rests on it instead: it is laid down into that ground, soil and all, and the surface below
ends there.

**A level carries its own paint and water.** `paint` and `water.bed` are stacks like the board's, read with the
level's slope, so a level's meadow and the valley's are finished apart. `falls` lists places on its rim, each `at`
and `r`, where its water falls as flowing water to the surface under the lip.

**Every floor a player can stand on is published as a surface.** The board's own ground is `ground`; a level, an
arch's deck and each carve's floor publish theirs by their ids, each with the y of its top in every column, -1 where
it is not, and the lowest block over it where that is known. A trees layer stands on the surface it names with `on`,
and on `ground` where it names none and the board has a level or a deck; a tree whose crown would reach the ceiling
over it is not planted.

## Carves

**A carve cuts air out of the laid ground and never comes nearer the surface than `cover` blocks.** The surface it
keeps under is the ground the board stood with before the stage: the top of each column's lowest solid run, so a
cave under a level that hangs is guarded by the meadow, not the level. Every carve publishes its floor.

| `op` | Numbers | From pgmvox |
|---|---|---|
| `tunnel` | `pts` ([x, floor y, z, radius] each), `mouths` (the waypoints open to the air), `lift`, `breach`, `dress` | `under.tunnel`, `under.dress_cave` |
| `chamber` | `at` [x, floor y, z], `rx`, `rz`, `h`, `dress` | `under.chamber`, `under.dress_cave` |
| `rooms` | `rooms` (`id`, `rect`, `floor`, `h`), `halls` (`from`, `to`, `via`, `width`, `h`), `lining`, `light`, `props`, `stair` | the document's own |
| `shaft` | `at` [x, z], `bottom`, `top` (`ground` or a y), `ladder_on`, `wall`, `post` | `under.shaft` |

**A tunnel's mouth is a waypoint whose cover guard is lifted.** Within its radius and a block and a half of it the
passage opens to whatever is over it, so a mouth set at the foot of a face cuts a portal and one set on a slope cuts
a trench. `dress` finishes the cave with floors, stalactites, stalagmites and ore, and never touches a block a
`rooms` or `shaft` layer laid; a tunnel that is a `breach` cuts through them.

**Rooms are rectangles at stated floors, and a hall climbs between them a block a step.** A hall leaves the first
room's middle along `via`, turns once and enters the second, and its rise is spread over the middle of its length
on stairs that face the climb; a hall too short for its rise is refused. `lining` gives the `wall`, `floor` and
`ceiling` blocks, each a block or a weighted mix, laid wherever the rock was solid, so a breach or a second carve
opens through it.

**A room is furnished from data.** `light` hangs a torch at the middle of each wall at `y` over the floor, and
`props` fills a box with a block: tombs, bars, a pool, a pillar.

## Volume, structures and symmetry

**A volume layer sets a body into the ground the way Stratum set its fragments.** `box` takes `at`, `size` (width,
height, depth), `yaw`, `tilt`, `sink` (the share of its upright height under the ground), `on` (`lowest` under its
footprint, `centre` or a y), `hole` (a frame's wall, for a ring or a gate) and `paint`: a `block`, or `bands`
along one of its own axes, with a `cap`. It writes only over ground, water and plants, so trees and earlier bodies
stand.

**An `arch` is a deck over whatever it spans.** It takes a `line`, a `width`, `deck` and `thick` as (crown, end,
power) along the span, a `camber` to its sides, `top`, `under` and `rock` blocks and `clear`. It is laid only where
the deck stands over the highest surface or water under it, so its ends grow out of the ground they meet, and its
deck is a surface trees may stand on when a trees layer names it.

**A structure is a mass with patterned faces, or a floor laid as a field.** `mass` pours a footprint from the
ground to `height` and patterns its faces with pgmvox's face patterns, each stated as `{"flutes": {"period": 3,
...}}`: band, courses, flutes, panels, slits, checker, windows, glyph rows and words, first match wins. `top` is a
cornice or a parapet and `bottom` a coffer. `carpet` lays floor fields over a rectangle at a course: border,
medallion, corners, diamonds, stripes, tiles, cross, star and `rings`, concentric bands round or square.

**Symmetry is the last stage, so every stage before it draws one team's part.** `half`, `mirror_x`, `mirror_z`,
`cw` or `ccw` copies what `keep` holds onto its image, turning every block's data with it, and `recolour` maps a
team's blocks to the other's. The surfaces are turned with the world.

## What draft 4 does not hold

**Riftwater's ground is data; its world is not yet.** The heights and water are the 38 layers named above, held
equal to `plan.land()` by a test. Its paint, buildings, caves and dressing are still the port's code.

**The grammar takes cells, not sections.** Claywork builds its sections from a raster and its own piece list, and
a document would need a `sections` entry beside `cells` for it, with the clay style. The fills and faces are the
style's code; a document names them and does not state them.

**Objectives and the map's XML are not layers yet.** Spawns, wools, monuments and hills, and `map.xml`, are calls a
board makes after `document.build`.

**Faces, the made stage, structures and build read the board's own ground.** A wall, a path's surface or a face
course on a level is not stated yet; only paint, water and trees are per surface. A mine gallery
(`under.gallery`) is not a carve either.

**`melt` works on the crater alone.** A level top or a butte with a surface of its own would melt the same way
through `smooth_max`, and the operation list grows one row at a time from the shapes pgmvox already carries.
