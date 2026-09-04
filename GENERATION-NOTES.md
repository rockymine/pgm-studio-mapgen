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

### On half a box the three goal bands cannot all hold at the plan tier

`GO1` wants a goal three to four times as far from the enemy's door as from its own, `GO4` wants it at least
40 blocks from its own, and `GO3` wants the two teams' goals at least 85 apart. With the doors 134 blocks
apart on a 130 × 120 board and a goal a distance `d` along the line between them, that is `d` in [27, 34],
`d` ≥ 40 and `134 − 2d` ≥ 85 — three bands with no common point. The plan tier walks the pieces flat, so a
gill cut eight courses deep or a single bridge lengthens no route it measures; the terms are soft, and
`fable-mossgill` takes `d` = 33 — the ratio in band, the other two read and left — because it is the built
board that decides the walk, and there the beck makes every enemy route go by the bridge.

### Reachable is not used, and every gate before coverage measures the first one

`CT12` on the strait, the traversability components, the goal ratios, the group symmetry error — every gate a
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

### Two ordering facts about a relief, and each one hides a landform

**A push is applied to the solved surface, so a push over a hollow fills the hollow in.** A push and
an `area` mark are not two statements about the same field: the marks are solved first and the pushes
are added to the answer. A twenty-radius push laid across a bench meant to be five blocks down lifted
it six, and a `sink` cut from that ground came out shallow with nothing complaining.

**A later mark wins a contested cell, so a mark written over a bench replaces it.** That is the
mechanism the stacked-hollow idiom depends on — nested `area` rings written outward-in — and it is
the same mechanism that silently overrode a bench with a knoll written after it and left a
**21-block** face into a pit that no one authored.

Neither shows up in the document, in a warning, or in a top-down. Both are one
`GET /map/{slug}/column?at=…` transect across the join. Take one across every place two landforms
share ground, before believing the JSON.

### A scarp's shelf is on the +z hand of the direction its lip is traced

A `scarp` pins `high` on one side of its line and `low` on the other, and which side is which is the order the
points are written in: the `high` band is the side toward which `z` increases when the line is walked from its
first point to its last — **south** of a lip traced west to east, **north** of one traced east to west. The
field carries no `side` word, so a lip drawn along a beck's north bank with `x` increasing puts the shelf in
the beck and the drop on the bank. Measured on `fable-mossgill`: with `lip-n` traced west to east the bank
north of the beck solved at **8–9** against the 14 it states and the relief read counted **418** barrier
steps; the same points reversed put the bank at 13–14 and the count at 268, which is the two scarp faces and
nothing else. Under `rot_180` the image reverses with the original, so one lip traced the right way is both.

### A relief posted to `sketch/from-plan` loses to the one already stored

`from-plan` merges, and a relief is carried across the merge under its own rule. On a map that already
holds one, posting a **changed** relief answers 200 and builds the terrain that was already there. The two
reads disagree and both are correct: `POST …/sketch/relief/read` measures the layout in the request body,
so it reports the new numbers, while `GET …/render/heightmap` builds the stored document, so it draws the
old ground. An iteration loop that watches the readback sees its edits land and an iteration loop that
watches the render does not. The merge is no longer silent about it — one `SK1` complaint per group whose
posted relief was replaced rides back on the 200 — but the terrain still comes from the stored one.

`PUT …/sketch` replaces the blob verbatim and is what an edit loop wants; `from-plan` merges — it carries a
stored finish, relief and structural height onto the freshly compiled board, and refuses at 409 with `SK1`
where the recompile leaves an authored relief with no group to land on. `?force=true` accepts that loss; it
does not make a posted relief beat a stored one. A spec-driven build wants neither, because it posts a whole
layout every time: `drive.py` stores through `POST /map/from-documents`, which replaces the map at the slug
outright, and the merge rules above never come into it.

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

### A fill pattern is a plane until it states a `rise`

Every area pattern — `cell`, `voronoi`, `noise`, `turbulence`, `electric` — samples the plane by default
(`TP15`): a column resolves to one block, so the pattern decides the ground and nothing else. On a surface a
course or three deep that is right and cheap. On a **fill** it is a cliff of vertical stripes: a six-stone
body stated as a `cell` of `turbulence` mixes with `rise` at its default came out of `fable-millrace-revamp`'s
first build with every cut face striped floor to sky, one cell's stone the whole height of the column. State
a `rise` and the field is a volume — but a cell as tall as it is wide still reads as a column on a cut, because
a cut face shows a cell's width and its height side by side and a square blob of stone is a post. The second
Millrace build stated cells of 7 with a rise of 7 and its cliffs still read as vertical runs. Make the cells
wider than tall: `fable-millrace-revamp` and `fable-mossgill` state the body as a `cell` nine across with a rise
of five over turbulences seven across with a rise of four, and the built body's runs of one material down a
column are 40% one block long, 23% two and 16% three, a mean of **2.5** — a blob, not a stripe. The earth is
the other way: three courses deep, so a rise of eight there makes each column's earth one material (64% of
columns) and the mix shows across the ground rather than down it, which is what a cut through soil looks like.

### An override add standing in ground keeps the ground under its floor

An override add overwrites the column it lands on, and where the ground's ordinary span reaches the override's
floor the built column runs from the ground's floor to the override's top. So a wall traced along a lip may
state a floor a few courses under the bed — `floor: 12` against a bed at 17 — and the bed is still under it.
A deck stated above the ground's top keeps the air beneath it, and a slab over open void still lays the
bedrock plate below. Measured on `opus5-millrace`: the canal walls, the spawn stair and the cairn walls stood
over a void from y0 to their floors, and `maps/rockymine-ruediger-millrace` carries 25,000 blocks of hand fill
under them; `maps/fable-millrace-revamp` is the same layout built with the ground kept.

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

### The bend is the studio's, and the side is the author's

`POST /map/{slug}/sketch/shapes/{shapeId}/bend` draws a compiled outline as a coast, and `drive.py`'s
`bendShapes` calls it once the board is stored. **The outline's own vertices never move** — that is the rule
that makes one safe, and it is the studio's. Which way the cut points go is `side`: `out` is the default and
is the slight bloat that makes a compiled rectangle read as land, `in` keeps the plan's footprint where
shapes abut on a measured strait, and `both` wanders across the line the plan drew. The side is decided by
offering each inserted point both perpendiculars and taking the one that lands where it was asked to — right
for a ring wound either way and for a concave stretch as readily as a convex one, which a shoelace sign is
not.

Measured on `opus5-alderfen`'s two rings, compiled against each side:

| ring | compiled | `side: out` | `side: in` |
|---|---|---|---|
| `garth-14` | 9750 | 11033 (**+1283**) | 8467 (**−1283**) |
| `holm-mid-14` | 4800 | 5477 (**+677**) | 4123 (**−677**) |

The same magnitude with the sign reversed, which is the whole of what the side chooses. The studio's outward
coast is vertex-for-vertex the coast every bent board in `specs/` was authored against, so those boards
re-drive to the ground their props were placed on.

### Bending is a roughener; reshaping is per vertex

A bend moves every cut point on a ring at once by a formula. That is right where a whole edge should read
rougher and wrong where one place should differ from the others — pulling a bay, widening one flank, cutting
the notch a lane runs through. Those are one point each, and a bend does them by making the entire outline
uniformly wobbly and the one place unchanged.

The three routes that do it are `PATCH /map/{slug}/sketch/shapes/{id}/vertices/{index}` (move one point),
`POST …/vertices` with `{"after": n, "x": …, "z": …}` (add one on that edge, and the answer says the index it
landed at) and `DELETE …/vertices/{index}`. **Every other point of the outline is exactly where it was drawn
after each of them.** That is the property the whole thing exists for: a board's shapes abut, and an edit
that drags a ring's other points opens ground between two that were flush.

State the point in the insert rather than splitting first and moving second: the one call is atomic, so a
point that would fold the ring leaves the outline untouched, where the two-call form leaves the midpoint
behind. Omitting `x`/`z` is the other case and is the midpoint anchor — a corner half way along a wall,
placed before it is decided where it goes. Nine such calls take a one-piece plan's compiled rectangle
(4 vertices, 24,000 blocks²) to a 12-point outline of 28,084, **+17%**, with all four of the compile's own
corners still exactly where the plan put them.

`rockymine-map-experiment` is the scale a hand actually works at, and it is larger than a bend's. Its four
ground shapes are the plan's four rectangles reshaped by hand:

| plan rectangle | compiled | drawn | vertices | Δ |
|---|---|---|---|---|
| `piece-25` | 3850 | 3920 | 4 → 11 | +70 |
| `piece-30` | 5500 | 6351 | 4 → 10 | +851 |
| `piece-30-2` | 3325 | 3962 | 4 → 9 | +637 |
| `piece-4-35` | 1575 | 1774 | 4 → 6 | +199 |
| total | 14250 | 16008 | | **+1758 (+12.3%)** |

Every one grew. Of the 36 drawn vertices, 19 sit **outside** the rectangle they came from by 2 to 20 blocks,
7 sit inside by 4 to 8, and 10 stay on the edge. The document carries **no Bézier handles at all**. A reshape
that far outward and that uneven is not reachable by any whole-ring transform, and it is reachable one point
at a time.

`opus5-millrace` inherits `s0`–`s3` and both spawns from this board **vertex for vertex** and adds no handles
either — its curves are `path` shapes, which is the layout's other curve and the one nothing has to author.
The three canal walls are `wall-s`, `wall-n-w` and `wall-n-e`: three or four clicked points, `radius 1`,
`path_edge: solid`. The rasterizer runs a path's points through a centripetal Catmull-Rom spline at eight
samples a segment before offsetting the band, so four points become a twenty-five-point centreline and the
wall draws as a curve. `cairn-wall-0`–`2` are the same shape at nine or ten points over about twenty blocks.
Reach for a path wherever a wall, a lane or a watercourse should flow; reach for `controls` only on a closed
ring of ground.

### Construction before dressing: a coherent terrain first, platforms as layers

The plan states the board's **arrangement** — which ground is where, at what height, next to what. It is not
the board's shape, and cutting it into more pieces to get a shape is the failure this section exists to name.
`firnline` is the worked example of doing it wrong: **13 plan pieces at 6 surface heights**, then
`themeByHeight` mapping each of those 6 heights to a theme. The theme partition is therefore the height
partition, which is the piece partition — the board's look is decided by how it happened to be cut up rather
than by any reading of the terrain, and it comes out chopped instead of coherent.

The order that works is the other way round. Author the terrain the map is played on as **one shape**, or as
few as the arrangement genuinely needs, and reshape it per vertex until it reads as ground. Then put the
platforms a match needs — a monument shelf, a middle plateau — on **layers over it**, which is what a layer
is for: `addLayers` with a `base_y`, a footprint, and its own theme. `firnline`'s 13 pieces are one terrain
shape plus two platforms.

A plan piece earns its place by stating something the arrangement needs: a height a lane climbs, a room a
building is seated in, a footprint the symmetry fans. A piece that exists only so a theme can be hung on it
is a piece that should have been a shape scope.

### A corner recipe does not make a coastline: a closed ring wants tangent continuity

The handle construction above — `c1 = p0 + d·t + n·bulge`, with `t·|d| ≥ bulge` and
`bulge ≤ 0.35·|d|` — is the recipe for **one** corner, and it is correct for one. Applied to every edge
of a closed outline it constrains each edge against itself and says nothing about the two edges meeting
at a vertex, so every edge bows outward and meets its neighbour in a cusp. A 24-vertex group authored
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
one group. That is the same warning the entry above gives about bowing a seam, and it is the one edge of
the ring that must be excluded from whichever construction is used.

### `shapePropsById` reaches a compiled shape's geometry, not only its knobs

`tools/README.md` lists the mergeable fields as `relief_scope`, `controls`, `anchor_heights` and
`height_mode`. The merge is a plain dict update over the compiled shape, so **`vertices` merges too** —
which is what lets a plan of three rectangles compile to one polygon and that polygon be replaced by a
hand-authored ring with a full handle table. A 24-vertex ring and 24 control entries posted this way draw
no `RQ3`. Pieces at one `surface` fuse into one shape, so keeping every generating piece at the same
height is what makes there be exactly one shape to replace.

### `skirt` decides whether an erected shape is a landform or a monument

One measurement covers the whole range, probed on flat ground at y11:

| `skirt` vs `base_height` | The edge builds | Reads as |
|---|---|---|
| `0` | one sheer step of the whole lift | a monolith, a cut face |
| about half the lift | **two**-block risers | a lip: crossed with a placed block, not on foot |
| **≥ the lift** | **one**-block risers, all the way round | a landform: walked onto from any side |

So `raise 7, skirt 10` is an outcrop a player strolls up and `raise 7, skirt 0` is a standing stone,
from the same two fields. A shape meant to belong to the terrain wants the third row and a theme in
the ground's own family — plain stone under a grass meadow — rather than an accent.

**Grass painted back over it is the rest of the merge, and it is free.** A path prop replaces the
surface finish and adds no cell, so two to five `worn` brushes with a grass pave, drawn as tongues
over a crag's shoulders at different angles, let the rock show through the grass instead of the
grass stopping dead at the shape's outline. The crag stays one plain theme and the seam disappears.

**`skirt` is one number for the whole outline**, so an outcrop is uniformly walkable or uniformly
steep; `anchor_heights` tilts the *top*, not the edge. There is no per-vertex skirt.

### `height_mode: sink` is a quarry, and its anchors are its depth

`sink` with `skirt: 1` cuts sheer faces and a flat floor — measured, a lift of 6 on flat y11 ground
gives a clean 6-block drop to y5 and back. `anchor_heights` on a sink states the **depth** per
vertex, so a ring whose corners read 2, 3, 6, 6 comes out four down on average and tilted.

**Notch it rather than tilt it.** Setting most of the ring to full depth and the two vertices on one
side to 1 gives a pit that is sheer nearly all the way round with a single shallow ramp in; a linear
tilt across the same ring turns the whole shallow half into a bowl and the cut stops reading as a
cut. Without a way in, the floor is a **stranded walkable place** — `relief/read` reports it as an
extra `places` entry with the largest share below 1, which is the only thing on the board that says
so; a top-down cannot show it.

### An erected shape is the pillar idiom, and its theme has to go in `fill`

`height_mode: raise` with `skirt: 0` and `floor: 0` is one abstract monolith: the top stands a stated
amount over whatever ground the footprint covers, the face is sheer on every side, and the plan is
whatever polygon was drawn. `anchor_heights` slants that top per vertex — measured on flat ground at
y11, a raise of 10 with no anchors tops at y21 everywhere, and the same shape with
`anchor_heights: [4, 4, 16, 16]` runs y19 → y25 across its own footprint. Leave `controls` off
entirely and the corners stay sharp, which is what makes a stone read as broken rock rather than as
a small group.

This is a **different device** from a stack of plates at successive `base_height` — the way
`tools/seeds/ruediger.layout.json` builds its steps — and both are right for what each does. Plates
are a staircase; a raise is a thing standing in the terrain.

**Put the pillar theme's `layered` stack in `fill` as well as `surface`.** The surface bucket is the
top few courses, so a stack stated only there bands the head of a 30-block monolith and leaves the
whole face plain — and the face is the entire point. Stated in `surface`, `wall` and `fill`, a column
read runs the strata bedrock to top.

**And take the pillar out of the ground's tone family.** On a board whose exposed ground is stone,
a pillar painted andesite, polished andesite and cobble is terrain wearing a different seed:
`render/surface` shows it as ground. The rule the brief states for a building — never the same family
as what it stands on — is the rule for an erected landform too.

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

### The compiler groups groups by mirror, not by landmass

Every fanned piece lands in one group called `team` however many separate rocks they are, and every
on-axis piece in `neutral`. An archipelago of a team group plus a flanking skerry is therefore **one**
relief keyed `team` covering two landmasses — which works, because the relaxation only ever steps onto
land and a mark on one says nothing to the other across the void.

Two consequences worth having before authoring one. **Nothing on `neutral` is mirrored for you**: a
non-fanned group's relief is stated once and used once, so every mark on it has to be authored as an
explicit pair about the origin or the two teams play different ground in the middle. And
**`tools/drive.py` appends every `addShapes` entry to `groups[0]`**, so an authored shape joins the
fanned group and is fanned — right for a shape on the team group, and right for one on an on-axis
group **only if that group is its own rot_180 image**. Authoring such a ring as half its points plus
their negations makes it exactly that, at no cost.

## Buildings

### A room's building defaults to its piece, and `footprint` separates the two

`WX1` makes the shell the piece rect inset one block on every side where the placement says nothing, so
a **20 × 20** spawn piece stamps an **18 × 18** house — a hall, not a spawn hut. `WoolPlacement.footprint`
and `SpawnPlacement.footprint` state it instead, as `[x, z, w, h]` in blocks from the piece's minimum
corner; `WX12` refuses one that reaches outside its piece, and `ST9`'s cap reads the rectangle the export
actually stamps — the stated one, or `WX1`'s default. So a wide protected apron with a small house on it
*is* expressible, since the piece is still the protection region and the spawn's own ground.

*Measured: `[3, 3, 12, 8]` on an 18 × 14 piece, and `POST /plan/inspect` answered
`wool-cage minX -29 minZ 73 maxX -17 maxZ 81` before a map row existed (`opus5-mootgate`).*

Watch the marker parity while shrinking it (`WX3`): a piece of an even number of cells takes a whole
`at`, an odd number takes a half, and mixing them refuses.

### A placed building is capped at 192 blocks of wing, and a storey wall at `clear + 1` courses

`HP3` names the cap in its refusal — *"the wings cover 232 blocks, past the 192 a placed building may
take"* — so an L of a 16×9 hall and an 8×11 wing is refused and one of 14×8 + 7×10 is not. Draw the
plan shapes to fit it: a U of a 16×7 hall and two 5×7 wings is 182.

A **storey** carries `clear + 1` courses of wall (the top storey carries none extra, the roof being its
lid), so a wall stack longer than that is silently truncated: a seven-band brick/checker/spruce stack
on a storey of clear 3 builds four courses of brick and checker and no spruce at all, and the section
reads as one flat mass. Size each storey's own stack to its own clear — which is also what makes a
three-storey building read as three rooms rather than as one tall wall.

**`POST /terrain/prop-preview` is the read for a multi-wing house.** It takes the prop — wings and all —
plus a theme, and answers plan and section as PNG at `?format=png&view=…&scale=8`.
`room-styles/preview-snapshot` draws the style on a default box, which for an L or a U is not the
building being placed.

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
does not turn a building away for merely touching it (the road runs to the porch), but it decides where the
*road itself* runs and what the scatter is refused over, so margin arithmetic against the polyline is
arithmetic against the wrong line.

**A building may end a road and never stand across one (`DR-CROSS`).** Drop a house on the pavement and the
road ends at its wall, which is what a road running to a door is. Drop one in the *middle* of a road and the
whole building is declined: the paving carries on out the other side, so what was one way through the board
is two dead ends facing a wall. Draw the road **to** the door rather than through the house.

Chamfer every sharp corner with two bracketing points — the spline then has nothing to overshoot — and read
`region/dressing-report.json` after a build, where a prop the band refused is named with its colliding cell.

---

## Dressing density

### A copied tree is a recipe with a body, and the body is the whole of it

A `copied` tree recipe carries `body: [[x, y, z, id, data], …]` from its foot, and the placement is a point
and a seed like any other tree. The registry key minted for one stated inline counts its blocks
(`copied-716`), so state the recipes under names in `dressing.styles` — `oak-dense-2`, `fir-tall-6` — and let
the placements name those. The bodies come out of a world with `pgm-studio/tools/seed-trees.cs`, which files
them in the library under `<world>-r<row>-<n>`; `specs/fable-millrace-revamp/trees.json` is the sixteen the
Millrace revamp planted, keyed the way its placements name them. A body is written block for block, so its
seat is its foot's column and a crown overhanging a slope is cut where it meets it, exactly as a grown one.

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

### Three things nothing checks about a placed building

A house is placed by hand and no gate filters it the way the pass filters a scattered prop, so three
faults reach the world silently and each is cheap to check before posting.

**Two override adds over one column build one shape and paint the other.** The taller add wins the
*geometry*, and the theme is scoped separately — a cell goes to the **smallest-area** themed shape
covering it — so where the smaller is also the shorter it paints the taller one's blocks. A hill's outer
ring crossing a town wall leaves a wall built to its own twenty-seven courses and finished in the hill's
grass-over-dirt, sides included, since the hill theme's wall material is dirt. `SK15` names it now
(pair, both themes, the columns they contest); before that it was visible only in a column read or in
the world. Cut a mound out of what it may not land on rather than trusting the heights to sort it.

**A flight is one shape, and the gradient is what decides whether it walks.** A polygon carries a height
per vertex (`anchor_heights`) and the rasterizer interpolates between them, so a tilted quad *is* a
stair — the courses are what a sloped surface rasterizes to. What separates a stair from a wall is the
run per course, measured on a 24-block quad:

| run : rise | worst step | walks |
|---|---|---|
| 1 : 1 | **2 blocks**, nine of them in twenty-four | no — a two-block rise costs a placed block |
| 2 : 1 | 1 | yes |
| 3 : 1 | 1 | yes |

So **the run must be at least twice the rise**, and where it is, a flight is a single polygon with
`height_mode: "level"`, `skirt: 0` and a thickness per vertex. The four flights up this board's Town
Wall are one quad each — 16 blocks of run for 8 courses — where they were nine rectangles each.

**Where the space is fixed, one rectangle a course is the only correct form.** A shaft 24 blocks long
that must fall 24 courses cannot be 2:1, and neither can a slipway climbing 8 courses out of a river
16 wide. Those stay per-course, and so does anything **clipped round an obstacle**: rectangles can be
cut round a rectangle with plain arithmetic, and a single tilted polygon cannot.

**An `override: true` add is still part of its group's relief.** Override decides who wins the column
among the shapes on a layer and says nothing about the solve, so a relief's surface replaces the top of
a wall, a flight, a hill or a rim as readily as it does bare ground. A made thing keeps its stated top
only with `"height_mode": "level"` and `"skirt": 0` (level for an absolute top, skirt zero for a sheer
face); `relief_scope: "exclude"` is the stronger form, keeping the shape's ground out of the solve
entirely. `SK14` names an override add carrying neither — it was silent when this board first hit it,
and a twenty-seven-course wall came out level with the ground beside it.

**A relief is solved on the group's primary half, and its surface is copied through the mirror.** A
mark on the far half constrains cells the solve never visits and is overwritten by the image of the
near half. State every mark on the side the plan's pieces are authored on, and pin a footprint that
straddles the axis on both sides.

**A mark pins its own cells and the relaxation slopes everything within `reach`.** Two regions at
different heights with nothing between them come out as one long ramp, so a floor that must stay level
next to a lower one needs a verge pinned at its own height — otherwise a wall's footing, and the gate
in it, follow the neighbour down.

**Raising terrain under a stamped room needs the PLAN to say so.** A piece states `"surface"`; lifting
the ground with an override add instead leaves the room correctly seated on the higher ground and its
spawn marker at the height the plan still states, inside the mass. Both spawns then leave the objective
chain and `EX1` refuses the export.

**A thing built out of terrain has to say so, or a road and a river will eat it.** An override add on
the ground layer — a town wall, a crop bed, a well's rim, a flight of stairs — is written by the painter
with a theme like any other ground, so nothing separates it from the sand beside it. A stroke repaints
the top block of every column it crosses, and a channel takes the *lowest* surface its band crosses as
its water line and cuts every other column in the band down to it: a wall standing seventeen courses
over a river comes out as a hole through the wall, filled with water. Mark such a shape `keepClear`
(`TS34`) and its columns join the dressing keep-out exactly, with no margin, so a road still runs
through a gate. A keep-out **stops** a prop rather than routing one, so a stroke that would have crossed
the marked shape wants redrawing too.

**A standing stone is terrain, and `keepClear` is what makes the pass see it.** An authored `addShapes`
polygon is ground, not a prop, so a building drawn over one stands inside it and is reported by nothing —
*unless the shape sets* `keepClear`, which makes it a real dressing keep-out with no margin. A wall, a
market cross or a stair flight authored as terrain and marked that way declines what leans on it by name.
Test every footprint against every *unmarked* authored shape's ring yourself.

*Measured: `b-berm-e rests on (35, 32), which is kept clear for a stated structure` — a boulder declined
for leaning on a `keepClear` town wall (`opus5-mootgate`).*

**A prop is judged at every image of its orbit.** A rock beside a building on an on-axis group is a
rock inside that building's own rot_180 twin, and the pass declines the whole prop rather than the
image — so a site filter that tests only the authored cell is testing half the map. Measured: three of
one build's four declines were images rather than originals. Test `(x, z)` and its orbit image against
everything.

**The authored ring is not the coast.** A Bézier edge bulges *outside* the vertex polygon on a convex
stretch and *inside* it on a concave one, so testing a footprint against the raw vertices rejects good
sites and passes bad ones. One house corner sat 1.5 blocks inside the drawn polygon and 1 block past
the built shore; `DR-SITE` was the first thing to say so. Flatten every ring at the rasterizer's own
16 samples per edge before testing anything against it.

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
`render/mirror`, `render/walk`, `walk`, and `column`. The schema names each one's own query words, and every route's summary carries
what it draws and where it is known to mislead, so what follows here is only what a summary cannot hold. The
`PgmStudio.RoundTrip` flags still take the same readings off a region directory, and `--help` prints the same
sentences.

### `walk` is the read that says what ground costs

`traversability` answers whether a board joins up. `walk` answers what crossing it charges, between two
stated cells, in four units at once: whether it can be reached, how far in blocks, how many blocks a player
must **place** — a rise of Δ costing Δ−1, void bridged one a cell — and how many falls over three the way
takes. `aim` picks the route: `travel` the shortest, `reach` the one placing fewest blocks, `comfort` the
least edge-hugging of the routes within ten blocks of the shortest. `render/walk` shades the same field over
the whole board with the route on it.

**Ask it in mirrored pairs.** A single journey says what a journey costs; the same journey against its own
image under the plan's `symmetry` says whether the board is fair, and that is the question no other read
answers — `render/mirror` compares blocks, and two halves can be block-identical while the ground between
them charges one team eleven blocks the other does not pay. On Elderwold, `rot_180`, the spawn-to-cairn lines
agree to within one block and the river corridor does not: `(−24, −16)` is river bed at y5 while `(24, 16)`
is bank top at y17, and the walk turns that into 11 placed blocks for one team and 0 for the other. The
relief mark's own point list is rotationally symmetric; what moves the edge is what is laid over it
unmirrored — the `grain` field and the water props' `shoreWander`.

**The field is one-sided, and the picture does not say so.** `render/walk` measures from one `from`; a cell
shaded cheap is cheap *from there*. Two teams do not share a picture. Read one per spawn before concluding
anything about a board's balance from a colour.

### `--column` is the only honest answer

Every other read is a projection. Probe the coordinate you already expect something at.

A column through the middle of a house reads floor, air, roof — the walls are at the perimeter. That is a
correct building, not a broken one.

### The provenance sidecar records an intent to claim, not the blocks

`--topdown --layer structure` reads the provenance sidecar and says so
(`STRUCTURE READING: RECORDED PROVENANCE`). Its owners list is a literal census of the dressing, and a prop
that landed nothing has no row at all:

```python
import json; from collections import Counter
p = json.load(open('specs/<slug>/provenance.json'))
print(Counter(o['kind'] for o in p['owners']))
```

The export writes it into the world's own `region/`; the driver moves it beside the documents, because
`maps/<slug>/` is what a game server is handed. A CLI read-back pointed at that region directory finds no
record and falls back to the material estimate, stating which reading it used on its scale line.

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

### A composed board is JSON, and taking it over is four edits

`GET /api/compose?players=&symmetry=&seedStart=&count=&hub=&front=&wools=` answers cards carrying a
descriptor and an SVG; `POST /api/compose/pin` stores one and returns its `planJson`. That plan is an
ordinary `PlanModel` and everything after that is editing it:

```python
for piece in plan["pieces"]: piece["rect"][1] += 4      # shift every piece 4 cells (20 blocks) of z
for box   in plan["boxes"]:  box["rect"][1]  += 4       # the boxes travel with their members
plan["pieces"].append({"id": "mid-isle", "role": "piece",
                       "rect": [-4, -3, 8, 6], "mirrors": False})
```

The vocabulary the filter takes: hubs `ring|bar|double-hole|twin|P|G|single`, frontlines
`twin|single|bar|none`, wools `i|l|donut|u|h|clamp`. **There is no `u` frontline** — `u` is a wool
family, and the frontline that reads as a U opening forward is `twin`, a bar with two prongs off it.

### The composer's holes are made by arrangement, and nothing marks them

A double-hole hub's two slots and a U wool's notch are the *shape of the pieces*, not a region. An
add-shape dropped on one fills it in, no gate says a word, and the layout that was filtered for is
gone. The predicate to check a ring against, before using it:

```python
def is_hole(x, z, reach=16):
    """A void cell with land in all four directions within reach. Open sea is void with nothing
    beyond it, and a shape may hang over that; a hole is not."""
    if land(x, z) is not None: return False
    return all(any(land(x + dx*k, z + dz*k) is not None for k in range(1, reach))
               for dx, dz in ((1,0),(-1,0),(0,1),(0,-1)))
```

### `globals.surface` is a floor and the theme's `surface.depth` is a thickness

They are different numbers and they interact: a board flattened at 9 under a stack 9 deep has exactly
one stack's worth of ground, so a coast rim cut one block into it leaves two blocks standing over the
void. Raising the plan's surface is what buys the stack room to be a soil profile — turf, dirt,
gravel, rock — which is what a cliff face is made of when `rim` and `wall` are both off.

### Two `hold` pads side by side cannot be ramped between

`relief_scope: hold` keeps a shape at its own level and the surrounding surface is solved knowing
where it has to arrive — which is exactly the pre-raise a spawn or a wool room wants. But a relief
mark cannot climb *between* two held shapes, because neither of them will move: a room pad at 18
beside an approach pad at 14 is a hundred cells of floor nobody can walk onto, and `relief/read`
reports it only as a rise in the place count. Each pad climbs one block over the pad it is reached
from — 16 → 17 → 18.

### A line mark's `width` reaches either side of the line

Not a half-width and not a one-sided band. A `line` at z 50 with `width: 12` writes over everything
from z 38 to z 62, so a mark drawn to make a bank behind a frontline erases the frontline. Then a
push stacked on that band and the result was a seven-block wall across the necks of the launch
ground. Halve every width that was reasoned about as a corridor.

### `height_mode: raise` measures from the median ground under its whole footprint

`relief.md` §7 states it: the top is a fixed amount above "the ground under it, **read at the covered
cells' median**". One number for the shape, not a value per cell. The consequence is the one that bites
on a slope — the median is the middle of the range the footprint straddles, so an outcrop lying across
a terrain step stands `median + anchor` high while its foot on the low side is much lower, and the face
a player meets there is the lift **plus the step**. A crag with a lift of 7 across a nine-block step
read as a fourteen-block wall, and no readback mentions it.

Level the footprint first — an `area` mark at the shape's own ring, grown about 1.3× — and the median
is the pad, so the whole face is the anchor plane where it was stated, with the pad's own edge left to
the solver's one-block stairs.

### A raise over void builds from its own floor

Past the coast there is no ground to read, so the column falls back to the shape's `floor` and a ring
that overhangs the sea by two cells builds two seven-block stubs at bedrock beside the group. It is
terrain, so nothing declines it. Audit every ring for sea cells as well as hole cells before using it.

### Three points and a plane is how you tilt a shape deliberately

`anchor_heights` is per-vertex, which is one number too many to pose by hand and one too few to be a
gesture. Stating three and solving for the rest is the gesture:

```python
def plane3(ring, pts):
    """pts is three (index, height) pairs. Solves a*x + b*z + c = h through them, fills the rest."""
    (i0,h0),(i1,h1),(i2,h2) = pts
    (x0,z0),(x1,z1),(x2,z2) = ring[i0], ring[i1], ring[i2]
    det = (x1-x0)*(z2-z0) - (x2-x0)*(z1-z0)
    a = ((h1-h0)*(z2-z0) - (h2-h0)*(z1-z0)) / det
    b = ((h2-h0)*(x1-x0) - (h1-h0)*(x2-x0)) / det
    return [max(0, round(a*x + b*z + (h0 - a*x0 - b*z0))) for x, z in ring]
```

Pick the three by the axis the lean should run along — the two furthest downwind at 0, the one
furthest upwind at the lift — and every shape on the board leans together instead of each being its
own accident. On a `rot_180` board that gives each team the cliff and its own side the ramp for free.

### A group that does not mirror stamps its shapes once; its dressing still fans

Two different rules, and they are easy to swap. `SketchRasterizer` mirrors a shape only when its
**group meta** says `mirrors`, so a middle group built as its own `rot_180` image stamps each of
its shapes exactly once — a second crag on the far lobe has to be written out,
`[[-x, -z] for x, z in ring]` with the same anchor heights, which turns the plane with the ring.
`Decorator` fans **every prop over the map's symmetry order** regardless, so a stand of trees on one
lobe is already the stand on the other, and scattering a second one there finds no room.

### DR-ROAD measures to the cells a stroke claims, and a wide brush is still a road

`PlacePath` claims exactly what `PathStroke.Cells(points, radius, style, coverage, seed)` lays, and
`RouteStandoff` is 3 for a tree and 2 for a boulder off any of them. Two consequences that pull
opposite ways: a `worn` stroke under partial coverage claims a scattered subset, so a keep-out
computed at `radius × coverage` lets props through that the gate then declines; and a stroke wanders
to its full radius, so a keep-out at `radius + standoff` is right — and twenty-one path props over a
110 × 220 board with that keep-out leave **eleven** plantable cells on the whole map. Texture brushes
are paths. Budget them like roads: one tongue per feature, radius 3–4, not two at 6–7.

### DR-CLAIM between props is footprint overlap, not a standoff

`claims.Holds(x, z)` — a prop is declined for resting on a cell another prop has claimed, and that is
the whole rule. Reserving three blocks around each boulder cost twelve trees on a board that had
three hundred plantable cells; `body + size + 1` is the real margin. The tree-to-tree distance is the
separate one, and it is a Chebyshev step that grows with the two canopies: `ceil((ha + hb) / 4.7)`.

### A layer is a slab with its own base_y, and the air between two of them survives

`layers[]` replaces the legacy single `layout`: each entry is `{id, name, base_y, layout:{shapes,
groups}}`, and a cell's column is that layer's `[floor, top]` shifted by `base_y`. The same `(x, z)`
may appear on several layers, which is the whole feature — two solid spans in one column with air
between them.

```python
if not layout.get("layers"):                     # the compiled document carries `layers: null`
    layout["layers"] = [{"id": "ground", "name": "Ground",
                         "base_y": 0, "layout": layout.pop("layout")}]
layout["layers"].append({"id": "terrace", "name": "Terrace", "base_y": 20,
                         "layout": {"shapes": [...], "groups": [...]}})
```

**Pop the old `layout` key.** `SketchRasterizer.ResolveLayers` reads `layers` *or* `layout` and
returns on the first, but `SketchLayout.IslandIds` reads both without an early return, so leaving it
behind doubles every group id.

**`floor` is the underside**, measured inside the layer: `base_y 20` + `floor 4` is a soffit at y24,
and the slab's thickness is its solved surface minus that. **Relief solves per layer**, keyed by
group id, and `ReliefFields` shifts the result into world Y before returning it — so `relief/read`
answers an upper group in world coordinates.

**The gap survives because `TerrainPainter.Paint` writes only over stone.** Its band stack runs
bedrock-to-top and would fill the air between two slabs; the stone-only invariant is the one line
that makes stacking work.

### Everything downstream of a stacked cell reads one number: the surface top

`TerrainBuilder.SurfaceTops` keeps the **maximum** `YTop` per `(x, z)`, and that single grid is what
the painter, the structure floors, the placements, the dressing and every 2-D render consume. Four
consequences, all measured on `maps/opus5-undercroft`:

- **A placement climbs onto the upper layer by itself.** A destroyable stated in plan cells with
  `float: 4` landed at y34 over a terrace and at y19 on the same plan with the layers stripped.
  Putting an objective on a deck is not stated anywhere — it follows from drawing the deck over it.
- **The covered ground is unpainted.** One column resolves one band stack, so ground under a slab
  falls inside the `fill` band: no turf, no rim, no wall.
- **The covered ground cannot be dressed.** A tree stated at `(8, 53)`, where the ground is a hall
  floor at y14, stood at y28 on the roof. No decline mentions it.
- **Theme scope is 2-D.** `ShapeThemeOwners` gives a cell to the smallest-area themed shape covering
  it across every layer, so an upper shape's theme owns the ground beneath it too.

### A ground ramp meets an upper slab by touching it, and nothing else is needed

Where a relief-solved ground top equals an upper layer's top, the two columns merge into one solid
mass and the join is a single one-block rise. The failure is one column wide: a causeway whose band
reached x ±19 beside a terrace drawn to x ±18 left one column of hall floor between them — a
twelve-block slot, and the deck a group in the air. **Overlap the two footprints by a column** and
check it with a transect, because no read will say: `traversability` and `WorldColumns.Membership`
both discard Y, so a layered board is always "one component".

### A layer over open void leaves a bedrock plate at the bottom of the world

`TerrainBuilder.Build` writes bedrock at y0 under every footprint cell it fills, per layer. A bridge
slab across a strait therefore drops its own 20 × 20 shadow at y0 in the abyss, and an overhanging
deck does the same over whatever it hangs past. The theme's `bedrock` value does not reach it — the
painter only overwrites stone — and those columns join the Y0 set a void filter reads. There is no
knob; a slab over void costs this.

### Only two reads keep Y, and one of them is the section

`topdown`, `heightmap`, `surface`, `traversability`, `coverage` and `relief/read`'s walk all project
to one height per column, so a hall under a deck exists in none of them. The isometric preview stacks
layers, and `render/section` cuts a plane:

    GET /map/{slug}/render/section?axis=x&at=<z>&from=<x0>&to=<x1>&ymin=&ymax=

**`axis` names the direction the cut runs, so `at` is the other coordinate** — `axis=x` takes a z,
`axis=z` takes an x. An `at` outside the world answers 200 with a blank image rather than refusing.

### The stack is written bottom-up, or the lower storeys are painted by the upper ones

`TerrainPainter.Paint` walks `SurfaceByLayer` **in document order**, and each pass paints its layer's
whole column from the bedrock course to that layer's surface; the stone-only invariant is the only
thing keeping two passes off each other. So a storey listed *after* one that stands over it finds no
stone left, and takes whatever theme the upper storey resolved.

A compiled plan emits `layers[0] = ground`, so appending an undercroft to the end is exactly that
case. Measured on `opus5-interchange` before the fix, at `(20, 70)`: a 2 × 4 glass door panel on the
ground layer painted its own column **yellow stained glass from y0 to y25**, twenty-six courses,
including the pool floor twelve blocks under it. With the same layer inserted at index 0 the pool
reads `y5..y3` white clay and `y2..y1` hardened clay, and the corridor above it is unchanged.

`drive.py`'s `addLayers` takes `"below": true` for this. The rule is one line: **order `layers[]` by
the height its shapes stand at, lowest first**, whatever the compile handed you.

### A goal states its storey on the plan

`DestroyablePlacement` and `CorePlacement` carry `layer` beside `id · piece · at · style · materials ·
float · name`, and the compile carries it onto every orbit image. A goal naming none resolves against
`SurfaceTop` — the highest layer — so a monument stated for a hall lands on the deck roofing it, with
nothing declined:

```python
{"id": "destroyable-1", "at": [-16, 56], "layer": "under", "style": "pillar-2", "float": 2}
```

Naming a layer the board has no ground on is a `DR-LAYER` decline for a prop; for a goal it is the
top surface again. A wool's or a spawn's storey has no plan field yet and is still the intent's.

### A ramp at one course a cell builds as treads of two, and a two-block rise is a placed block

A `ramp` polygon falling 18 → 6 over **12** cells rasterized as `18 16 16 14 14 12 12 10 10 8 8` —
six steps of two — and `…/walk?aim=reach` answered `blocks 3` climbing it, because the walk prices a
rise of δ at δ−1 placed blocks. The same 12 courses over **20** cells reads one course a cell and
walks both ways for nothing. The rule to author by: **run at least twice the rise** on any stair
meant to be climbed rather than fallen down. (A 20-course ramp over 32 cells was right first time.)

### A prop's claim is a claim of one storey

`GroundClaims` is keyed on the layer as well as the cell and each placement is handed one storey's
view of it, so two props are in each other's way only where they share ground: a building on the
`deck` layer at y38 and one on `ground` at y18 do not collide, and neither does an oak on a floating
group and the river under it. `DR-CLAIM` and `DR-ROAD` both read that book, so the standoff to a
road is measured against roads on the prop's own storey. Two props on the **same** layer still have
to be moved apart in plan (`WE49`).

### A storey read only reaches its own top where the spans are read half-open

`ColumnSegment` is `[YFloor, YTop)`. A board whose lower layer meets the one over it with no gap —
rock at `under[1..18]` under `ground[18..28]`, which is what stating the rock under a landmass looks
like — is the case a closed reading gets wrong: nothing is found above, the storey is handed the rest
of the world, and `?layer=under` draws the surface under the undercroft's name. A layer with air over
it reads correctly, so the fault shows on some storeys of a board and not others (`WS18`, fixed).

The provenance record travels with it: a claim is recorded per column and carries no course, so under
a storey read it describes the column's top rather than the course being drawn. It is narrowed with
the world now — terrain at or below the layer's own top, the recorded claim only where the storey
shows the column's own top — and the picture's legend says which reading it used.

### `render/topdown?layer=` names a sketch layer, so the category isolations are gone

On a board whose `layers[]` are named, `?layer=structure`, `?layer=foliage` and `?layer=objectives`
answer **422 `RQ4`**: *"this board has no layer 'structure' — it carries ground, under, catwalk,
roofs, deck"*. One query word does two jobs and the sketch layer wins. The per-storey read is the
better half of the trade — `?layer=under` draws the undercroft and nothing over it — but the three
reads that answer *did the props land where I put them* are unavailable on any stacked board.

### The export does not object to a goal underground

`OB17` asks whether a goal stands over void, in a spawn or in a wool room, and its `IsLand` is the
set of `(x, z)` the rasterizer produced across **every** layer, so a column under a slab is land.
`EX1` reads the same spans and a cell on two layers answers twice, so an undercroft is a place the
walk can stand in. A monument sealed under a concourse exports at 200 as long as something walks to
it — which on `opus5-interchange` is a ramp, and before the ramp had headroom was `SK11` naming
3,336 places nothing could reach.

### A stroke ignores `layer`, so a floor with a roof over it is marked with a shape

Every prop kind takes `layer` and `DressingContext.GroundFor` reads it — a house, a tree and a
boulder all seat on the storey they name; measured on `opus5-interchange`, a kiosk stated for the
pool hall stands with its roof at y10 under a concourse whose floor is y12, and an oak stated for
the car deck stands at y42. **A stroke does not.** Two lane markings carrying `"layer": "under"`
came back from `POST …/sketch/dressing` with `"y": 25` and `"y": 17` — the corridor wall's coping
and the corridor floor, over the basin they were drawn for — and a worn track stated for a hall at
y18 came back at `"y": 37`, on the deck roofing it. Nothing declines, because `DR-LAYER` fires on a
layer the board does not have and these are layers it has.

**Mark a covered floor with a shape instead**: a rectangle of that floor's own `floor` and
`base_height` carrying a different `theme`. The geometry is unchanged and the theme scope resolves
per layer, so it lands exactly where it is drawn. Both of the pool's lanes are three-wide rectangles
of the basin's own two courses, themed dark prismarine.

### A point mark's radius pins a flat disc, so a radius is a mesa and not a summit

`PointMark.Pins` yields **every** cell inside its radius at the stated height, and those cells are
constraints — the relaxation only shapes what is left between them. Marks placed at radius 16–32 on
a 176-wide board nearly tile it, and the ground builds as stacked plateaus with vertical faces.

Measured on `opus5-tarnfell`, the same thirty marks at two radii, off `…/sketch/relief/read`:

| | radius 16–32 | radius 3–6 |
|---|---|---|
| walkable at one-block steps | terraced throughout | **95.1 %** |
| largest place at that tier | — | 86.5 % |
| cliffs | one at every mark's edge | **6** |

**The rolling is the relaxation's**; a radius is how much of the landform you are refusing to let it
do. Keep a summit at three to six and let `reach` spread it. An `area` mark is the other instrument
and is right where flat is the point — a lake pan, a spawn terrace, a shelf under a goal.

### A relief mark's centre may lie outside the land, and that is how a map edge cuts a mountain

`PointMark.Pins` iterates **its own** bounding box and keeps whichever cells `footprint.Inside`
answers for; `LineMark.Pins` walks `footprint.Land()` and measures each cell's distance to a
polyline that may lie anywhere. So a ridge traced twelve blocks past the coast with a radius of
fourteen pins the coastal strip at its own heights and leaves the crest off the map — and the
board's edge is a mountainside cut through rather than ground decaying to `base`.

Three of `opus5-tarnfell`'s mountain marks lie entirely outside its polygon and a fourth runs out
through both ends of it; every contour band in its heightmap closes on the frame rather than inside
it. A mark placed *wholly* out of reach does nothing and raises nothing — no `SK3`, no warning — so
the check is the heightmap, not the document.

### Two flat marks butted together build two terraces and a step at the seam

A `line` mark at y8 with radius 7 and another at y14 with radius 6, their bands touching, transected
`7 7 7 7 [+5] 12 13 13`: a five-course wall right round a lake that was meant to shelve. Seven blocks
of unpinned ground between them and the same two marks read `7 7 7 7 9 11 12 13 13`. **The gap
between two marks is not a gap in the design; it is where the design happens.**

### The material top-down draws the top *solid* block, so water reads as its own bed

`render/topdown?material=1` over a lake shows sand, not water; the category read
(`render/topdown`, no `material`) has a `WATER` class and draws it cyan, and
`…/column?at=0,22` answers `y5 Water · y4 Water · y3 Water · y2 Sand`. When two pictures disagree,
`column` is the one that is not a projection.

### `addShapes` lands on the group the compile emitted, which is called `team`

A relief keyed to any other name answers `SK3 — a relief is stated for group 'x', which the layout
does not carry`, and then `relief/read` answers no groups at all. `{"*": {...}}` is the key for a
board of one group, and the driver's own guard stops the run there rather than building a flat
world.

### Only `worn` spends `coverage` — `rough` fills its band solid

`PathStroke` decides a cell's membership in two steps: a half-width the style shapes, and then a
per-cell gate. Only `PathStyle.Worn` has the gate (`PatternNoise.Unit(x, z, seed + 11) < coverage`).
`Rough` spends its knob on the band's *edge* instead, wandering the half-width by ±45 % over a
7-block scale, and fills everything inside it. So `style="rough", coverage=0.26` is a **solid belt**,
not a freckle, and sixteen seam strokes written that way turned every boundary on `opus5-tarnfell`
into a stripe of a third material laid over the join.

A seam wants `worn`, and it wants **two grounds freckling into each other, one material to a
stroke**: a wide thin stroke at the far edge and a narrow dense one over it, so the density ramps
from a scatter to about half cover. A voronoi of three materials in one stroke is a new ground over
the boundary, which reads as noise wherever the two it stands between already differed.

### `rot_180` maps a shape centred on the origin onto itself, so a central lake may be any shape

The mirror does not force a circle; assuming it does is what produces one. Any outline with a
half-turn in it is already symmetric, so a profile of radii covering **half** a turn, repeated at
θ+180°, gives a lobed, elongated or kidney-shaped water that fans without error. Smoothstep between
the profile's entries or the outline comes out faceted, and give the helper a `swell` so an outer
ring can depart from a circle less than the waterline while staying the same shape — that is what
keeps a beach an even band round a shore that is nowhere an arc.

### Relief is keyed by group id across the whole stack, and `*` is the ground's alone

`SketchRasterizer.ReliefFields` walks every layer and looks each of its groups up in the one
`relief` dictionary, adding that layer's `base_y` to the field it solves. So a stacked board can give
each storey its own landscape — `{"team": …, "walls": …}` — and a layer's marks are stated in **its
own frame**, not the board's. `drive.py`'s `"*"` expands over the groups the *compile* emitted, so a
key stated beside it survives and names a layer added in the finish.

### `POST /plan/room` answers one footprint whatever the facing says

The route is the resolver's own answer to *what room does this piece carry*, and it is the honest thing to
copy onto a placement — except that its `footprint` does not move with the spawn's `facing`. Asked on the
same 20 x 20-block piece it answers `{"at":[10,12],"footprint":[1,5,18,14]}` for all four facings, while
the compiled shell does move: `facing: "front"` puts the shell at the piece's `+z` end with its door apron
at `-z`, and `facing: "back"` the other way round. Copying that footprint onto a `back`-facing spawn
therefore pins the five-block apron to the wall the door is not in, and `WX8` then refuses the iron cube
because the ring it needs is on the other side.

**State no footprint.** `WX1`'s default is the same rectangle and it follows the facing.

### The iron cube stands OUTSIDE the room shell

`WX8` reads *"inside the piece"* and it is easy to read that as *inside the room*. The cube is
`IronSpan` square, stands **in the ring between the shell and the piece edge**, and holds `IronGap` blocks
of clear air to the wall. On a 20 x 20 piece whose shell is the piece inset one and five in front of the
door, that ring is the five-block door apron and nothing else: the marker goes at the apron's outer edge,
three blocks of cube and two of air, and anywhere in the hall is unplaceable.

### `04-routes.txt` is not written on a board whose goals are wools

`tools/drive.py` ends every run with *the three numbers*, and on a capture board the third is always
`no route between a spawn and a goal`. The read it is made of answers fine asked by hand —
`GET /map/{slug}/walk?from=&to=&aim=reach&format=text` gave `153 blocks, 19 placed, 2 drop(s), worst drop
10` from a spawn point to an enemy wool on `opus5-quatrefoil` — so what a raid costs is knowable and is
simply not in the sweep. On a wool board, take the walks by hand: own wool, each enemy wool, and read the
placed count, which is the whole of what a crossing costs an attacker.

### A wool room must abut ground, not sit inside a piece

A `wool-room` piece drawn inside a larger `piece` rectangle shares no edge with it, and the plan tier
answers `WX6 — wool room is unreachable: no land seam and no abutting build zone to enter by`. Split
the surrounding piece into rectangles that tile around the room instead.

### The plan tier's frontline is the pieces a **build zone** touches

`FannedGraph.Build` sets `Frontline` to the nodes that touch a fanned build zone, and `SP1` asks
whether a wool is reachable from a frontline node without crossing a spawn. A plan with `zones: []`
therefore has no frontline at all, and every wool on it refuses with *"only reachable through a spawn
piece"* however open the board is. The canonical two-wool seed carries a `mid-band` zone for exactly
this reason.

### A voronoi's bands are rings inward from a cell boundary, and the last one takes the rest

`VoronoiMaterial.Resolve` walks the band list and stops **one short**, returning `Bands[^1]` for
everything the earlier bands did not claim. The value it walks is the Worley `F2 − F1` gap — small
against a cell boundary, largest at a cell's centre — so the bands are **depths measured inward from
the boundary**, not weights over an area, and the last band's stated thickness is read by nothing.

So `voronoi(seed, 7, [(SAND, 4), (RED_SAND, 2), (GRAVEL, 1)])` is not *sand with a seventh of
gravel*; it is a **gravel bed with sand along the cracks**, because gravel takes every cell interior.
Write the ground the board is made of **last** and put the veining before it:
`[(GRAVEL, 1), (RED_SAND, 2), (SAND, 1)]` is a sand wadi with gravel in the cracks and a red margin
round each patch. A voronoi is a diagram, not a mixture.

### A cliff's strata belong in the `wall` bucket, because a cliff is what that bucket paints

Nothing bands by world height and nothing needs to. A `layered` stack on the **wall** bucket is read
by `DepthFromTop`, which on a wall counts down from the top of the face — so on a board whose drops
all begin at one shelf, banding by depth **is** banding by altitude. One stack shared as the wall
material of every theme makes every cut on the board the same rock in the same order, and puts those
colours nowhere else (`opus5-kiln-row`).

The counterpart: **`wallRun` stands vertical**, because its stripes wrap the perimeter and are
constant up a column. A weathered cliff is bedded and a sawn one is scored, and the two are one
bucket and two materials (`opus5-deepcut`).

### `step` with `stairs` is the instrument for a quarry — the terracing that ruins a hillside

`ReliefSpec.Step` snaps the finished surface to a quantum, which is what turned `opus5-tarnfell`'s
hills into stacked plateaus. A worked pit **wants** that: state the rim and the floor as two `area`
marks, let the relaxation solve a smooth bowl between them, and set `step` to the bench height.
`stairs: true` then cuts a way up out of every place the terracing stranded, so the pit is walkable
without stopping being terraced. Every stated level must be a multiple of the step or the knob
rounds it away. `opus5-deepcut`: four marks and `step 4` give six benches where thirty marks gave a
hillside nobody wanted.

### Only `relief_scope: "exclude"` makes a vertical-sided spire

Every mark is a constraint the relaxation smooths *through*, so a point mark makes a cone. An
excluded shape leaves the field entirely — the solver bends round it as it bends round the void — and
keeps the column it was drawn with: a flat crown on vertical sides, joined to nothing.

### A `rim` mark states one height for **every** group in the relief

It is the right instrument for a board whose groups are level with each other and the wrong one
otherwise. To shoulder groups that stand at different heights, draw each one's polygon wider than
the `area` mark that states its top and set `base` **under all of them**: the fringe between polygon
and area is unpinned and decays toward base, so every edge falls a course or two before its drop, at
its own height (`opus5-aerie`).

### Water fills whatever is level, so the pan is the size of the pool

An `area` mark 34 × 30 at the sump's height is a 34 × 30 lake however small the `water` prop inside
it. Draw the mark at the size of the water and let the surrounding floor sit a few courses over it.

### On a bridging board the gaps are the design, so state them first

Six-block gaps between groups answer `G2` (a corridor under ten wide), `G5` (a hop outside 10–20)
and `CT12` (a strait outside 15–40) on every pair, and they are right: a six-block gap is a running
jump. Fix the four numbers — the hops and the strait — and fit the groups round them.

### A core is the forward objective and a wool is the deep one

A core cannot be carried anywhere; it is breached where it stands, so it belongs where it will be
fought over. A wool has to be fetched and brought home, so it belongs behind. On `opus5-aerie` the
first draft had them the other way round and `WL10` read a wool-front-distance of 8.

Two things about a core in particular: `float` and `leak` are one knob (the lava free-falls to the
terrain at `float` below the casing and leaks a course below `leak`), and **a core on a group in
open sky has nothing to catch its lava** — so the casing wants ground all round it, or a breach
anywhere near an edge ends it at once.

### A *flat* composed plan compiles to one merged polygon and a `subtract`, and the subtract wins

Twelve pieces go into `POST /plan/compile` and two terrain shapes come out: `s0`, one merged `add`
polygon over the whole footprint, and `s1`, a `subtract` cutting everything the pieces do not cover.
A subtract beats **every** add on its layer whatever order they are written in, so an `addShapes`
rectangle over a composed hole draws nothing at all — and `SK13` now says so, naming both shapes.

**A hole is never scenery. Do not fill one.** What the composer encircles — the middle of a `donut`
wool room, the yard of a `clamp` or a ring — is ground players go round, and the walls a board hangs
on it are drawn to guard exactly that ground. Filling it makes them guard nothing (the author's
ruling). An add that puts the ground back is **refused**, `SK13`, `422` — an override add, or any add
on **another layer**, since a subtract reaches only the layer it is on and `below: true` does not
change that.

**Where the void wants to change shape, change the subtract.** A compiled subtract is the board's
statement of its own negative space: it may be redrawn — rounded off, narrowed, moved — but never
deleted and never papered over with an add.

**Stating a surface per piece does not remove the hole.** It stops the compiler merging the pieces
into one polygon, which is what makes a composed board paintable — but `PlanVoids` reads the void per
**component** rather than per surface, so the buffer is declared and the subtract emitted either way.

**The merge is a consequence of the pieces being flat, and stating a `surface` per piece ends it.**
Give every piece its own height and there is nothing left to merge: the same twelve-piece plan
compiles to **one polygon per distinct height and no subtract at all** — nine of them on
`opus5-rimegarth`, `s0` at base 9 through `s8` at base 15 — with the hole simply a place no polygon
covers. That is also the only way a composed board can be painted in more than one theme: a theme is
stated **on a shape**, a flat plan has one shape, and `themeByHeight` therefore has nothing to bind
to until the heights exist. Heights first, then paint.

### A `walls` entry closes an interface, not a route

A plan wall stamps bedrock two thick and three tall across the interface it names, over that
interface's full width, on the attack side — so it closes exactly one seam. On a plan whose pieces
enclose something, that is not the same as closing the way through: a `donut` wool box has a lane
down **each** side of its hole, and a wall on one is walked past on the other.

Count the ways round the thing before counting the walls. Where the plan has no seam at the place a
wall is needed, **split a piece to make one**: on `opus5-rimegarth` the two long ring arms are each
cut in two level with the middle of the hole, twelve pieces to fourteen, which puts one interface in
each lane facing the other across the yard and gives both walls somewhere to stand.

### Browsing the composer is a four-call loop, and a scan is what tells you its vocabulary

`GET /compose?players=&symmetry=&seedStart=&count=` returns cards carrying the descriptor that
reproduces each board, its score, a structural read and a board SVG; `POST /compose/pin` stores one
from that descriptor; `GET /plans/{id}/png` renders it as an image; `POST /plan/{id}/author` makes a
map row. Ninety-six seeds, eleven pins and two contact sheets is a few minutes.

Two things a scan says that nothing else does. **Cell 5 is the only scale it works at** — cell 4
produced nothing in ninety-six seeds and cell 3 nothing in twelve, both `exhausted`. And **10 and 12
players give identical boards**, so the land budget buckets rather than scaling. Hub forms observed
in 48 seeds at 16 players: `bar`, `ring`, `single`, `twin`, `g`, `double-hole`, `p`; wool shapes
`i`, `l` and — five times in forty-eight — `donut`, which is five pieces round a hole.

### A composed board is corridors, so compute where a prop may stand

Every piece is ten blocks wide with a road down the middle, and there is no landscape around them —
what is not a piece is void. Placing props by eye on one gave fourteen declines, half of them
`DR-SITE — has no ground`. Given the piece rectangles, the roads with their radii, the buildings and
the doorways and the wall seams, a search over every block of the authored half is instant and
returns the truth: on
`opus5-rimegarth` it is **nine** places in a half.

Two of the rules that search has to know. **A road's standoff is measured to its paved cells, not its
centreline** — clear the stroke's radius *plus* the kind's standoff, three for a tree and two for a
boulder. And **an approach wall's interface is kept clear the way a doorway is**, so the seam a
`walls` entry names belongs in the keep-out list beside the rooms.

### A water prop fills its own band, not the level it finds

`form: "canal"` holds its stated width: a centreline down the middle of a fifteen-wide hole at radius
3 is a six-wide channel with dry ground either side of it, however flat the pan under it. The band
**is** the pond and the radius is the knob. This is the same fact `opus5-deepcut` learned from the
other end, where an oversized flat `area` mark became an oversized lake: a water prop is a stroke
that carves, not a fluid that finds its level.

### A paint patch on solved ground is an ordinary one-course add, not an override

Scoping a theme to a patch of ground is an authored shape carrying a `theme`. What that shape may say about
its own height is narrower than it looks, and the narrowing is measured rather than reasoned.

**Every shape rasterizes to a real span.** `SketchRasterizer.RasterShape` takes `floor` from `Floor ?? 0` and
its thickness from `HeightFn`, whose last line is `double bh = s.BaseHeight ?? 1` — so a shape stating **no
height at all** is one course at bedrock, not "no opinion". `RasterGroup` then resolves
`((adds − subtracts) ∪ override-adds) − override-subtracts`, and the two branches treat that course
completely differently:

- an **ordinary add** goes through `MergeCell`, where *the taller add wins the column*, so a one-course
  stroke laid over ground twenty courses high changes nothing about the height;
- an **override-add** does `result[k] = v`, which **overwrites the column outright** — floor and all.

**The relief usually hides the difference, and that is the trap.** After the set algebra,
`RasterizeLayout` writes the solved surface back over every cell in a solved group's footprint:
`cells[(x,z)] = (Math.Max(column.Floor + 1, field.At(x, z)), column.Floor)`. So an override-add's flattened
column is repaired to the solved height, and on a board where every cell is in some group's solve an
override brush works perfectly. Measured that way on `showcase/07-hill`, a bare `override: true` rectangle
over the west hill read **y13 · y16 · y12** across the summit — the hill, repainted.

**Where there is no field, there is no repair.** A shape carrying `relief_scope: "exclude"` takes its cells
*out* of the group's footprint (`SolveRelief` puts them in `excluded`, and the relaxation bends round them
as it bends round void), so nothing writes a height back. An override brush stroke over such ground stays
what the rasterizer made it: one course on the bedrock, twenty below the ground beside it.

Measured on `opus5-sandcaster`, whose lid over the workings is `relief_scope: "exclude"`: eleven strokes
punched holes. A transect at `z 51` read `x −50:0 −47:0 −44:0` against a reef surface of y21 four blocks
away, and the same shapes re-authored as ordinary adds read `−50:21 −47:21 −44:21`.

**So the form a brush takes is `operation: "add"`, `base_height: 1`, and no `override`.** Paint scopes to the
smallest shape covering a cell, so the stroke still wins the colour; the height is decided by the taller add,
so it can never lower what it is painted on. The one thing it must not do is hang over the void — a
one-course add is the only shape on a cell with no ground under it, and there it builds a speck of bedrock.

For completeness, what the other three forms do to solved ground, all measured on `07-hill`:

| The patch says | Reads across the summit |
|---|---|
| `add`, `base_height: 1`, no override | the ground, repainted — and safe over excluded ground |
| `override: true`, nothing else | the ground, repainted — **only** where a relief covers the cell |
| `base_height: 9`, `relief_scope: "hold"` | y8 flat — a plate punched through the hill |
| `relief_scope: "hold"`, no height | y0 bedrock — a shape with no override and no height loses every merge |

This is the instrument a detailed surface is painted with — a drift of sand against rock, scree at the foot of
a crag, mud in a hollow — and it is what a single large `voronoi` over a whole region is a substitute for.

## A mountain is a push. No mark can be one.

A relief mark is a **constraint**: the ground here *is* this height, honoured exactly, with no falloff of any
kind. That reads as a modelling detail and it decides what terrain can be authored at all. *A point mark's
radius pins a flat disc* above is the same fact met from the other end, and the two remedies are for two
jobs: a small radius left to `reach` is how a mark stops terracing ground it is only meant to sit on, and a
push is the only thing that builds a landform.

A `point` mark at `h 47, r 8` therefore does not build a summit. It builds a **drum** — a flat disc eight
blocks across standing on a twenty-block sheer wall — because nothing between the disc and the ground round it
is under any statement except the relaxation, and the relaxation has one cell of room to make the transition
in. A `line` mark with per-vertex heights is the same object stretched along an arc: a ridge-shaped wall with
a flat top. Both were built on `showcase/19-mountain-range` before the pushes were, and both produced correct
relief numbers (`low 11 · high 55`, `symErr 0`, gate OPEN) over a landform that reads as a row of oil drums.

A **push** is the other operation. It takes a drawn ring and lifts the solved surface inside it, and three of
its fields are the landform:

- **`amounts`** — one lift per ring vertex, interpolated along the arc and wrapped, so the crest falls along
  the ring the way it was drawn. A massif's spine is six numbers.
- **`crown`** — how much higher the middle stands than the edge, where the middle is the ring's **medial
  axis**: a point for a round ring (a dome), a line for a long one (a crest). **The record's default is `0`**,
  so a push authored without touching it is a plateau. This one field is the difference between a mountain and
  a mesa.
- **`falloff`** — the skirt, measured from the ring across the land. This is the number that decides how much
  of the board the range eats. On a 90-block-wide board, `falloff: 20` put the two massifs' skirts into each
  other and left a 20-block ditch down the middle; `falloff: 11` left flat ground from `x −18` to `x +15`.

`roughness` wobbles the skirt against a noise field so it is not a clean offset of the outline, and a
**negative crown** dishes the ring rather than doming it — a corrie, a quarry floor, a pond basin.

**The second half is what is *not* written.** Pinning a region with an `area` mark because it should be about
that height leaves the solver nothing to solve, and a board with a mark on every region is a table with bumps
on it however tall the bumps are. `19-mountain-range` pins four things — the coast, the dale floor, the goal's
shelf and the spawn's apron, every one of them ground a player walks — and the flanks carry no mark at all.
`opus5-sandcaster` pins all four of its regions, and is flat for exactly that reason.

`reach: 0` goes with it: a finite reach pulls ground back toward `base` at that distance from any constraint,
which between two distant marks means the flanks decay to the base and the range becomes separate hills.

One last shape note, cheap to fix and expensive to see: an `area` mark's ring is a **shape**, and a rectangle
looks like one. `shelf` and `apron` written as four-vertex rectangles built two mesas with sheer sides,
visible in the heightmap as literal squares; the same marks on nine- and eleven-vertex lobed rings are
indistinguishable from ground.

## Among the shapes of one layer, the taller override-add wins the column — not the later one

`RasterGroup` resolves a layer as `((adds − subtracts) ∪ override-adds) − override-subtracts`, and both the
plain adds and the override-adds are accumulated through `MergeCell`, where **the taller surface wins**.
Only the *set* an override-add belongs to is privileged; within that set, document order decides nothing.

That reads as an implementation detail and it is the difference between a tunnel and a sealed one. An end
wall drawn as one rectangle across the mouth of a ramp is 15 courses tall where the ramp under it is 7, so
the wall wins every column they share — and the way down ends in solid rock. Measured on
`opus5-sandcaster-ii` before the fix: `(−8, 60)` read solid `y0..21` with no air in it, a three-block plug
at `z 59..61` sealing both mouths, with `SK11` reporting 676 and 294 places of standable ground with no
route onto them. The same wall shape had shipped on the first Sandcaster.

**So a wall that meets a ramp is drawn in halves, one either side of it.** The general form: on one layer,
*anything shorter than what crosses it is not in the world there*, which is the same fact `SK9` reports for
a shorter shape inside a taller one and the same reason a room with a sunken floor is drawn as rectangles
clamped **around** the sunken part rather than under it. Ordering the document does not fix it, because
order is not what is read.

The cheap check is a column transect down the way in. A ramp that works reads one course of fall every two
blocks the whole way; a plugged one reads a solid run where the air should be, and nothing else on the board
says so — the export gate stays open, `render/traversability` can still answer one component, and the only
complaint is an `SK11` that is easy to write off as a quirk of a stacked board.

## A range is a wall unless its two gradients agree

A push has two slopes in it and they are set by different pairs of fields. Outside the ring the ground climbs
over the skirt, at `amount / falloff` courses a block. Inside it the ground climbs from the ring's edge to its
medial axis, at `crown / half` — `half` being the half-width the ribbon was drawn at. Where the two disagree
the landform has a step in it at its own outline, and a range with a large `amount` and a short `falloff` is a
cliff with a hill on top of it whatever its height.

Measured on `opus5-thornfell`, behind the spawn: `amount 26 · falloff 8` against `crown 10 · half 7` is 3.25
courses a block for ten blocks and then 1.4, and the section at `x 0` reads as a sheer face standing directly
on the building's back wall. The same range at `amounts 13–17 · falloff 10` against `crown 12 · half 7` — 1.7
either side — reads as one mountainside from the wall to the board's back edge.

**The height a range can be is decided by the ground in front of it, not by taste.** What is available is the
distance from whatever stands in front to the coast behind, and a peak more than about 1.7 courses a block
above that distance has to buy the difference somewhere, which it does by putting a step at the ring. Behind
Thornfell's spawn there are 20 blocks between the building's back wall and the coast, and 20 blocks at 1.7 is
what makes `high 52` on a board whose ground is 26. Wanting 80 there is wanting a wall.

The other half of the same arithmetic is where the summit goes. Setting the spine **past the coast** puts the
medial axis off the board, so what is on the board is one uninterrupted climb and the crest reads as being
behind the map. That costs the strokes that are placed from the spine — a summit blob centred past the coast
has nothing to clamp to and collapses onto its own centre — so those are taken from a crest point inside the
outline rather than from the spine itself.

## A wool room's foundation is bedrock to y 0, so it needs land on all four sides

A stamped wool room fills its whole piece and fills **downward in bedrock**: the column under
`opus5-thornfell`'s room reads floor at `y 25` and bedrock from `y 24` to `y 0`. Nothing about that is visible
in a plan view, in the relief read-back, or at the export gate. It is visible in the world as a 25-course
bedrock cliff wherever the cell beside the room is void or lower, which on a board where the room piece is the
full width of the spur it hangs off is every cell of two of its four sides.

So a room piece gets a piece of ordinary ground either side of it and one behind, and the pad mark is drawn
wide enough to cover all of them at the same height. Thornfell's rooms sit in a band of five pieces —
`ledge-w · room-w · ledge-wi` across, `crag-w` behind, `spur-w` in front — and the `roompad` ring is 22 × 10
rather than the room's own 14 × 10 for that reason. Read back, the ground either side of the room is `y 25`
and the room's own wall starts at `y 25`: the plinth is under the land rather than beside it.

The gate that hides the fault is that **a push is applied after every constraint**, so a range whose skirt
crosses the room lifts the pad the room is stamped on and the plinth grows by exactly as much. Before the
ranges were set back, the same room read floor at `y 43` over 42 courses of bedrock, with void either side.

## A finish is applied to a compiled layout, and `drive.py` writes its output under the input's name

`drive.py` ends a run by writing the layout and intent it posted into the spec directory, as
`<base>.layout.json` and `<base>.intent.json` — the same two names a board **drawn** in the Sketch tool
carries as its authored geometry. Reading those back on the next run therefore fed the driver its own output
and applied the finish a second time, and the finish's three appending keys are all silently additive:
`addLayers` inserts a storey per entry, `addShapes` appends to the first group, `bendShapes` bends a ring
that is already bent.

A spec whose finish adds two storeys stores them once on the first run and twice on the second, and the
studio says so twice:

```
SK12  2 groups answer to the id 'under', so terrain and placements stored under it have no single group
      to belong to — the first one solved takes them and the rest build flat
SK10  layers 'under' and 'ground' are driven 17 block(s) into each other over 64 column(s)
```

Nothing refuses it. The board still exports, the gate still opens, and the committed spec now differs from
the board it describes.

**The finish is what decides which shape a spec is.** A spec carrying one is compiled from its plan every
run and its layout is the run's output; a spec with no finish is a drawing and its layout is the input. That
is what the driver's own docstring always said — "either `<base>.finish.json`, or a hand-drawn
`<base>.layout.json`" — and the load now honours it. Every one of the 65 specs holding both is a compiled
board whose layout the driver wrote, so re-driving one is idempotent again; the 23 holding a layout and no
finish are the genuinely drawn ones and are unaffected.
