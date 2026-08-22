# Generation notes — what the API does not say

Everything here was learned by driving the live API and reading a column back. **What the studio can state
about itself is not repeated here**: the routes and their fields are in `GET /api/openapi/v1.json`, every rule
id is in `GET /api/rules` with what it means and how to fix it, and a posted field that went unread comes back
as `RQ3` naming its own JSON path. This file is only what none of those can say — a fact about how two correct
mechanisms interact, a number a gate does not check, a read-back that lies.

Measured against `pgm-studio` at `b45b154` (22 August 2026) by rebuilding `opus5-wheal-hazel` and
`opus5-wheal-hazel-v2` through `tools/drive.py`.

---

## Before a plan is posted

### The board is written in cells, so read it as cells

`tools/board.py` renders a plan's rectangles as an ASCII grid off the plan file, and
`GET /api/map/{slug}/plan/ascii` does the same off the stored plan. Take one before posting anything.

The faults that cost the most are **relations between two rectangles**, and a grid is the only view that puts
two rectangles on the same rows:

```
  -1 |    MMMMMMMMMMMMMMMM    |     M = a neutral bar, sixteen cells wide
   1 |          NNNN    OOOO  |     N = the build zone that reaches it, four
```

Sixteen against four is a landform most of which no journey reaches, and it is one glance. The renders that
get looked at instead — the ground map, the heightmap, the theme swatches — are pictures of a *world*, and a
picture makes a long bar look like a good idea. Nothing in the picture states the width of the window that
reaches it. The same grid catches the rest of the family: a wool room touching the spawn apron (`LN1`), an
approach whose wall can be walked round because the ground reaches past it, a spur that connects to nothing.

### Reachable is not used, and every gate before coverage measures the first one

`CT12` on the strait, the traversability components, the goal ratios, the island symmetry error — every gate a
board passes before it exports asks whether ground **can be got to**. None asks whether any journey **goes
there**. A board can pass all of them while carrying whole landforms no player has a reason to walk.

`GET /api/map/{slug}/coverage` is the read that answers the other question, and
`GET /api/map/{slug}/plan/flow` is the same question off the plan alone, before a world exists to measure.
Rebuilt today, the two Wheal Hazel boards read:

| board | ground | reached | decorated | dead | dead share |
|---|---|---|---|---|---|
| `opus5-wheal-hazel` | 9 798 | 5 656 | 1 474 | 2 668 | **27.2%** |
| `opus5-wheal-hazel-v2` | 11 276 | 10 980 | 209 | 87 | **0.8%** |

The difference between them is one decision: v1's neutral bar spans `x −40..40` and the build zone that
crosses it spans `x −10..10`, so every journey over the bar is a bridge through that twenty-block window and
the ground either side of it is dead by construction. v2 cut the bar to the build zone's own width. The
general shape of the mistake: **a mid-board stepping stone is used only across the width of the build zone
that reaches it**, and the corridor margin buys back six blocks and no more. A water lane buys back none — a
lane sits outside the build slice and therefore outside the navigable set, so no route is walked through one.

Coverage is a **measurement, not a gate**: nothing refuses on it, which is exactly why a run that does not
read it lets a board ship with a third of its ground unused.

### A plan carries holes by arrangement, not by subtraction

**There is no way to cut a hole inside a piece from a plan.** A `buffer` drawn over a generating piece is
inert — it can declare a void but never destroy ground — so the fill ratio does not move and no hole appears.
A hole in a plan is made by **arrangement**: pieces ring a gap, no piece covers it, and `PlanVoids.Declare`
names every such gap a `void-N` buffer on every compile whether or not the author drew one.

The instrument for cutting a hole *through* ground is a layout `subtract`, which is downstream. Shape the
**pieces** to shape a coast, and cut the holes in the layout.

This is also why `POST /api/plan/evaluate`'s `G8 fill-ratio` reads a board denser than it is built: it
measures the plan's rectangles, which do not know about a layout `subtract`.

**A wool board is where holes belong.** Over 400 boards composed at `players=32`, `rot_180`, 63% of hubs are
`ring` or `double-hole`, 19% of frontlines are `twin`, and 10% of wool approaches are `donut` — all bodies
with a void in them. Of the 98 shape cards, 73 are donuts. `examples/generator-32/` holds six of those boards
as plans and as grids; `docs/gameplay/match-flow.md` §3.2 is what the holes are for.

---

## Authoring the layout

### Height and paint resolve overlaps by *different* rules

- **Height**: `RasterGroup`/`MergeCell` — *the taller add-shape wins* the column.
- **Paint**: `ShapeScopeOwners` — *the smallest-area shape wins* the cell (the most specific scope).

The documented way to make an organic tier is to let the tier below **run under** it, so the upper one can
pull inward without opening a hole. But where the lower tier is the *smaller* shape, it keeps the paint while
the upper tier keeps the height — a band of the wrong material laid across the top of the upper terrace, as
deep as the underlap.

Measured on a five-tier board at `x = 0`, with `shelf` (`base_height 22`, quartz, ~3 300 cells) overlapping
`terr-mid` (`base_height 18`, grass over sandstone, ~1 500 cells):

| column | ground top | painted | should be |
|---|---|---|---|
| `(0, 70)` | y21 | Quartz Block | Quartz — shelf alone, correct |
| `(0, 58)` | **y21** | **Grass / Dirt / Sandstone** | Quartz — shelf's height, `terr-mid`'s paint |
| `(0, 50)` | y17 | Grass / Dirt / Sandstone | correct — `terr-mid` alone |

**Check which way round each join sits before building.** Where the upper tier is the smaller shape the
problem does not arise at all. Where it is not, author the two edges to overlap by two to four blocks and the
seam reads as a transition rather than a stripe.

### A relief posted to `sketch/from-plan` loses to the one already stored

`from-plan` merges, and a relief is carried across the merge under its own rule. On a map that already
holds one, posting a **changed** relief answers 200 and builds the terrain that was already there. The
failure is silent and worse than silent, because the two reads disagree and both are correct:
`POST …/sketch/relief/read` measures the layout in the request body, so it reports the new numbers, while
`GET …/render/heightmap` builds the stored document, so it draws the old ground. An iteration loop that
watches the readback sees its edits land and an iteration loop that watches the render does not.

`PUT …/sketch` replaces the blob verbatim and is what an edit loop wants. `from-plan` is right for a
first build — `drive.py` runs it against a map row created moments earlier, which has no stored relief to
win — and `?force=true` does not change this: force accepts an *orphaned* relief (`SK1`, 409), it does
not make a posted relief beat a stored one.

### `base_height: N` puts the top block at `y = N−1`

Confirmed at every tier on every board that has traced a real map. Any plan matching absolute heights is one
low until this is applied.

### `relief_scope: exclude` takes a tier out of the elevation model entirely

A five-tier board of ~19 000 ground cells reports 4 294 cells to `relief/read` — the one tier that is neither
`hold` nor `exclude`. Everything above the base tier is outside the solve, so its variation has to come from
shapes: `raise` landforms, `sink` basins, `anchor_heights` tilts and ramps. Budget for that when designing a
stepped board, because "add relief" is not available as a later fix.

`hold` and `exclude` differ in how the join reads, not in whether the shape stays flat: `hold` lets the ground
ramp up to meet the shape, `exclude` meets the tier below at a face. A terrace wants `exclude`.

### A ramp between two tiers is four fields and works first time

`height_mode: "level"` plus `anchor_heights` is a tilted plane — vertices in order, one height each:

```json
{ "id": "ramp-d", "type": "polygon", "operation": "add", "floor": 0,
  "base_height": 22, "height_mode": "level", "skirt": 0, "relief_scope": "exclude",
  "vertices": [[-46,68],[-34,68],[-34,82],[-46,82]], "anchor_heights": [22,22,26,26] }
```

Measured down `x = −40`, joining a shelf at 22 to a crest at 26: z66 → y20, z70 → y22, z74 → y23, z80 → y25.
A path prop laid over it paves the slope, so the ramp reads as a built stair. Four of these turn a stack of
terraces from a series of one-way drops into a zigzag climb.

### Bézier `controls` — the semantics, and where the curve actually is

`controls` is keyed by **vertex index as a string**, and the handles are **absolute board coordinates**:

```json
"controls": { "5": { "in": [77, 25], "out": [77, 35] } }
```

The edge from vertex *i* to *j* is the cubic `p0 = V[i]`, `c1 = controls[i].out`, `c2 = controls[j].in`,
`p3 = V[j]`. So a vertex's **`out` bends the edge after it and its `in` bends the edge before it** — one
vertex's handles belong to two different edges. A missing handle falls back to the endpoint itself.

**The extremum sits between vertices, never at one.** Probing the vertex is the natural check and it is
worthless — the vertex is a fixed point of the curve. Probe near `t = 0.5`.

**A handle that travels further away from its edge than along it makes a lobe, not a corner.** Place every
handle as `c1 = p0 + d·t + n·bulge`, `c2 = p3 − d·t + n·bulge`, with `d` the edge vector, `n` its outward unit
normal and `t` a forward fraction (0.3 works). Two constraints keep it a corner:

| | |
|---|---|
| `t·\|d\| ≥ bulge` | the handle travels further along the edge than away from it |
| `bulge ≤ 0.35·\|d\|` | a short edge cannot carry a big bulge |

Break the first and the cubic doubles back into a cusp, and past that a self-intersecting loop that rasterizes
as a detached scrap of land. Break the second — an 8-block handle on a 15-block edge — and you get a deep U
hanging off the shape, which flattens without self-intersecting and still reads as a bulb. Flatten the
finished ring and test every non-adjacent segment pair for intersection before posting: a curve that *looks*
right in numbers can still cross itself.

**And keep the curve away from two things.** A **seam** a player walks — bow it and the two pieces stop
touching. And a **wall**: its width was fixed at compile from the plan's seam, so bowing the coast beside it
widens the lane past the wall's ends and hands players a way round it. The wall rects are in
`POST /api/plan/inspect`'s structures feed; veto every edge within 10 blocks of one.

### A corner recipe does not make a coastline: a closed ring wants tangent continuity

The handle construction above — `c1 = p0 + d·t + n·bulge`, with `t·|d| ≥ bulge` and
`bulge ≤ 0.35·|d|` — is the recipe for **one** corner, and it is correct for one. Applied to every edge
of a closed outline it constrains each edge against itself and says nothing about the two edges meeting
at a vertex, so every edge bows outward and meets its neighbour in a cusp. A 24-vertex island authored
that way, with both constraints satisfied and no self-intersection, rasterizes as a **gear**: twenty-four
points around a blob.

An organic outline is a smoothness constraint between edges, not a bulge on each. Catmull-Rom converted
to Bézier gives it in one line and is tangent-continuous at every vertex by construction:

```
c1 = P1 + (P2 − P0)/6        # controls[i].out,  edge i → j
c2 = P2 − (P3 − P1)/6        # controls[j].in
```

with `P0`/`P3` the ring neighbours. Raising the divisor flattens the curve toward the polygon; 6 is a
natural coastline at a 12–20 block vertex spacing.

**Leave the seam edge alone.** On a `rot_180` board the edge a shape shares with its own image — the run
along `z = 0` — takes no handles at all: straight, the mirror lands on it exactly, and the two halves are
one island. That is the same warning the entry above gives about bowing a seam, and it is the one edge of
the ring that must be excluded from whichever construction is used.

### `shapePropsById` reaches a compiled shape's geometry, not only its knobs

`tools/README.md` lists the mergeable fields as `relief_scope`, `controls`, `anchor_heights` and
`height_mode`. The merge is a plain dict update over the compiled shape, so **`vertices` merges too** —
which is what lets a plan of three rectangles compile to one polygon and that polygon be replaced by a
hand-authored ring with a full handle table. A 24-vertex ring and 24 control entries posted this way draw
no `RQ3`. Pieces at one `surface` fuse into one shape, so keeping every generating piece at the same
height is what makes there be exactly one shape to replace.

### A theme and a house style are snapshots, and `RQ3` does not reach inside them

Everywhere else, a field the studio did not read comes back named. A **theme** and a **house style** are
stored as opaque snapshots, so a misspelled field inside one is dropped in silence and the pattern renders as
a flat swatch at 200.

**`GET /api/terrain/patterns` is the field list** — fourteen kinds with their exact field names. The ones that
have been guessed wrong: `noise` takes `stops`, not `palette`; `voronoi` takes `bands` of `{material, depth}`,
not `palette`; `checker` takes `even`/`odd`, not `a`/`b`; `layered`'s axis is `axis`/`beyond` over a `stack`,
and there is no `inset`; `teamTint` takes `blockId` and `neutral`. Read the endpoint rather than the type name,
and preview what you wrote: `POST /api/terrain/material-preview?format=png` answers the pattern as an image.

**A theme's `fill` is what fills a tall shape; the surface is only its top courses.** A 44-block hoodoo banded
through `surface` alone comes out banded in its top four courses and plain below. Put the `layered` stack in
`fill` as well and the strata run the whole column.

**A style fork that repaints `wall` and not `storeys[*].wall` is half a fork.** The storey stack carries its
own wall, and on a two-storey preset the storey is most of what a section shows. The exception is `Stilts`,
whose whole idiom *is* storey 0's wall (air over a beam course) — repaint that and the stilts disappear.

### A material's `kind` has to be the first property of its object

`kind` is read positionally, so moving it and nothing else turns a document that answers 200 into a **400
naming a kind that is right there** — *"a material names no kind, or names one that does not exist"*. Any
generic tool that reorders JSON does this: a formatter, a re-serializer, `json.dumps(…, sort_keys=True)`.
Measured on a room style that previews at 200 as authored and 400 with `kind` moved last in every material,
the two documents comparing equal as data.

Write materials `kind` first, and never round-trip a theme or a style through anything that sorts keys.
Fixed in the studio as `TL2` — the reader takes `kind` wherever it sits. A theme or a style written against
an older build still wants `kind` first.

### Two words differ between a save request and a snapshot

`porch.edge: "front"` is a save-request word. On a **snapshot** — `preview-snapshot`, `roomStyles`, a dressing
`style` — the field is a nullable enum and the word for "the door wall" is **`null`**; `"front"` refuses with
`RQ1`. Same document, two layers, two vocabularies.

---

## Buildings

### Wing corners are inclusive, and the joint roles are ridge-derived

An `AuthoredWing`'s `corners` name cells inclusively: `[[0,6],[9,10]]` covers row 6 *and* row 10. Two wings
sharing a coordinate row therefore **overlap** (`HJ1`); a touching wing starts one row past its hall
(`maxZ` 77 → wing `minZ` 78).

**Which rectangle is the hall and which the wing follows from the ridges**, not from your drawing — the wing's
ridge runs *into* the shared edge. So an explicit `ridge` stated to dodge an `HJ3` tie can silently swap the
roles, and checking a rule against the rectangle you *drew* as the wing reads a firing `HJ5` as satisfied. The
refusal names the derived roles ("the wing (rectangle 1)…"): read the indices in the message, not your drawing.

**A roughly square hall ties its ridge `AlongX`, which is `HJ4` waiting to happen.** A square-ish hall meeting
a wing on a vertical shared edge ties toward x, the wing then also runs into that edge, and both-into-it is
`HJ4`. State the **hall's** ridge along the shared edge (`AlongZ` for a vertical seam) and the wing's into it.

`POST /api/terrain/prop-preview` answers all of this before a build — but its body is `{propJson, themeJson}`
with the documents as **strings**, and a house prop's `style` must be the resolved `HouseStyle`, not a library
reference.

---

## Paths

### A path's band follows the spline, not your polyline

`PathBand.Centerline` runs the drawn points through a **Catmull-Rom spline** before the band is derived, and a
Catmull-Rom overshoots the outside of every corner — by several blocks when the segments are long. The band
does not touch buildings (the road runs to the porch), but it decides where the *road itself* runs and what the
scatter is refused over, so margin arithmetic against the polyline is arithmetic against the wrong line.

Chamfer every sharp corner with two bracketing points — the spline then has nothing to overshoot — and read
`region/dressing-report.json` after a build, where a prop the band refused is named with its colliding cell.

---

## Dressing density

### A tree's ground claim scales with its height, and varies with its seed

`DR-CLAIM` names the pair after the fact; nothing answers how far apart two oaks must stand *before* they
are placed. Measured against the pass over four builds of the same wood, two template oaks clash below a
Chebyshev separation of roughly

```
(height_a + height_b) / 5
```

so a pair of 9s may stand 4 apart and a pair of 14s may not stand 5 apart. It is not a species constant:
`Decorator.CanopyRadius` measures the crown the build will actually write, and the crown is hash-keyed
off the prop's `seed`, so **the same pair of heights is not always the same distance** — a `(9, 11)` pair
at Chebyshev 4 survived one build and was declined the next after an unrelated edit shifted the seeds.
Divide by 4.7 rather than 5 to sit clear of the variance; at 5 exactly, a board builds clean and its next
revision does not.

Dart-throwing beats a jittered lattice here for the same reason. A lattice at the spacing either reads as
a grid (no jitter) or breaks its own minimum (with jitter, which is what the rule charges for); thrown
points accepted against the test pack right up against it. On a 40 × 50 wood: 60 trees thrown against
23 latticed, at the same rule.

### A texture path is an exclusion zone as wide as itself

Using the path prop as a brush — a wide `rough` or `worn` band whose `pave` says what a stretch of ground
*is* — is the way to get dedicated ground out of a single theme, and `DR-ROAD` prices it: a tree keeps
**three** blocks from the nearest paved cell and a boulder **two**, measured from the prop's resting
cells, so a radius-10 brush is a 26-wide strip nothing can stand in. A paved forest floor is an empty
forest. Brush the ground that is meant to be open — the fighting ring round a goal, a quarry pan, a
trampled heath, a shore — and leave the wood's floor to the theme and the flora overlay.

## After the intent, and at the export

### `OB19`'s keep-out is bigger than it sounds

A **10-block square about the goal's anchor**, tested against a prop's footprint **plus its eaves**, and
against **every orbit image** of it. For a goal at `(0, 45)` the box is `x −10..10, z 35..55`, and a building
drawn at `x −12..−1, z 54..61` is refused on its eave. It is raised by the export, at 409, after the whole
world has been built — nothing earlier predicts it. Compute the box, add one for the overhang, and keep
buildings, trees and boulders out of it.

### A compile cannot see a layout `subtract`

A goal the plan gate passed can be refused at export. A destroyable placed on the centre of a plan piece,
with a sally port then cut through that piece in the layout, compiles at 200 and exports `OB17 — is 1×1 and
overhangs the void`. The plan gate judges rectangles; the export gate judges the ground the rasterizer built.
**Cut the holes first, then place the goal.**

### An erected shape raises the build cap twenty blocks above itself

The ceiling is `BuildCeiling.Of(highestGround)` — the tallest **terrain** column plus 20 — and an erected
shape is a terrain column. Five hoodoos topping at y43 over ground topping at y14 wrote
`<maxbuildheight>64</maxbuildheight>`: twenty-one blocks of clear air over the picket they were meant to be
un-bridgeable above.

**Erected terrain cannot be used as an unbridgeable wall.** It is an obstacle nobody climbs; it is not one
nobody bridges. The same arithmetic means one tall shape hands the whole board a ceiling it did not want.

### A board whose ground crosses the origin gets a bedrock observer platform in its middle

The compiled intent puts the observer at `(0, observerY, 0)` and `observerY` defaults to `surface + 15` — a
bedrock pad over the centre of the board. `globals.observerY` is the only control a plan has over it; 55–60
keeps it out of the way.

### A spawn shape's interior is never painted by its theme

Measured again today on `opus5-wheal-hazel-v2`: `(0, 85)`, inside the spawn, tops out at raw `Stone` y12,
while `(0, 70)` on the same board and the same theme reads Grass Block over Coarse Dirt. Four runs have now
reported it. On an otherwise fully themed map that is a stone patch under every spawn.

### Export into a fresh, empty directory

A rebuild writes over a region directory it never clears (`B102`, open), so an `.mca` a previous build left
behind survives into the new map and reads back as part of it. `tools/drive.py` deletes its `--out` before
extracting for exactly this reason. If two builds of the same map disagree in a way that makes no sense, this
is why.

---

## Reading the world back

**The reads answer over HTTP now**, one route each under `GET /api/map/{slug}/…` — `render/topdown`,
`render/section`, `render/heightmap`, `render/surface`, `render/traversability`, `render/structures`,
`render/mirror`, and `column`. The schema names each one's own query words, and every route's summary carries
what it draws and where it is known to mislead, so what follows here is only what a summary cannot hold. The
`PgmStudio.RoundTrip` flags still take the same readings off a region directory, and `--help` prints the same
sentences.

### `--column` is the only honest answer

Every other read is a projection. Probe the coordinate you already expect something at.

A column through the middle of a house reads floor, air, roof — the walls are at the perimeter. That is a
correct building, not a broken one.

### The provenance sidecar records an intent to claim, not the blocks

`--topdown --layer structure` reads `region/provenance.json` and says so
(`STRUCTURE READING: RECORDED PROVENANCE`). Its owners list is a literal census of the dressing, and a prop
that landed nothing has no row at all:

```python
import json; from collections import Counter
p = json.load(open('maps/<slug>/region/provenance.json'))
print(Counter(o['kind'] for o in p['owners']))
```

**An approach wall is recorded one column wider than it is built, on both axes.** `StructureStamper.StampWall`
walks its footprint max-**exclusive**, which is what the intent's rect means; `ClaimStructures` hands the same
rect to `WorldProvenance.ClaimRect`, which walks it max-**inclusive**. A 25 × 2 wall draws as a 26 × 3 bar.
Measured on `maps/grok-ridge`:

| column | top block |
|---|---|
| `(−25, 34)` · `(−25, 35)` · `(−12, 34)` · `(−12, 35)` · `(−1, 34)` | cobweb y21 over bedrock y20…16 — the wall |
| `(−25, 36)` · `(−12, 36)` · `(−1, 36)` | stone brick y17 — the mid terrace, no wall |

Worth knowing twice over: a wall read from a render looks thicker than it plays, and a bedrock line's
thickness is exactly what decides whether it can be built over.

### A section's lines are the renderer's, not the world's

`--section` blends a horizontal scale over the image: a white line at 16% alpha every `--ticks` blocks of Y
(default 8) and a **yellow** one at 36% every fifth tick. There are **no vertical gridlines at all** — every
vertical division in a section is a real block. The two backgrounds are two different answers: pale `#E7ECF3`
is air inside a loaded chunk, near-black `#0E0E12` is no chunk at all. And it samples **one plane**, so
anything a few blocks either side of the cut is not in the picture.

### `--traversability-map` reports an approach wall's cobweb as impassable

Every board carrying an approach wall reads isolated except one whose wool lane has a second land seam. The
renderer's ground search steps past decoration but its headroom test does not, so the cobweb course capping
every wall reads as blocking (`B99`, open). The export gate navigates on `WorldColumns.Membership` and never
sees it, so all of those boards pass. A wall is meant to be crossed — over the top, cutting the web with the
shears the kit carries.
