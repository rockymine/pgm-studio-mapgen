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
a small island.

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

### The compiler groups islands by mirror, not by landmass

Every fanned piece lands in one island called `team` however many separate rocks they are, and every
on-axis piece in `neutral`. An archipelago of a team island plus a flanking skerry is therefore **one**
relief keyed `team` covering two landmasses — which works, because the relaxation only ever steps onto
land and a mark on one says nothing to the other across the void.

Two consequences worth having before authoring one. **Nothing on `neutral` is mirrored for you**: a
non-fanned island's relief is stated once and used once, so every mark on it has to be authored as an
explicit pair about the origin or the two teams play different ground in the middle. And
**`tools/drive.py` appends every `addShapes` entry to `islands[0]`**, so an authored shape joins the
fanned group and is fanned — right for a shape on the team island, and right for one on an on-axis
island **only if that island is its own rot_180 image**. Authoring such a ring as half its points plus
their negations makes it exactly that, at no cost.

## Buildings

### A room's building is sized by its piece, and by nothing else

`WX1` makes the shell the piece rect inset one block on every side, so a **20 × 20** spawn piece
stamps an **18 × 18** house — a hall, not a spawn hut — and there is no field that separates the two.
The only way to a smaller building is a smaller piece: **10 × 10** gives an 8 × 8 shell, which is a
cottage. The trade is that the piece is also the protection region and the spawn's own ground, so a
wide protected apron with a small house on it is not expressible.

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

### Three things nothing checks about a placed building

A house is placed by hand and no gate filters it the way the pass filters a scattered prop, so three
faults reach the world silently and each is cheap to check before posting.

**A standing stone is terrain, so `DR-CLAIM` cannot see it.** An authored `addShapes` polygon is
ground, not a prop, and a building drawn over one stands inside it and is reported by nothing. Test
every footprint against every authored shape's ring yourself.

**A prop is judged at every image of its orbit.** A rock beside a building on an on-axis island is a
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
that overhangs the sea by two cells builds two seven-block stubs at bedrock beside the island. It is
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

### An island that does not mirror stamps its shapes once; its dressing still fans

Two different rules, and they are easy to swap. `SketchRasterizer` mirrors a shape only when its
**island meta** says `mirrors`, so a middle island built as its own `rot_180` image stamps each of
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
islands}}`, and a cell's column is that layer's `[floor, top]` shifted by `base_y`. The same `(x, z)`
may appear on several layers, which is the whole feature — two solid spans in one column with air
between them.

```python
if not layout.get("layers"):                     # the compiled document carries `layers: null`
    layout["layers"] = [{"id": "ground", "name": "Ground",
                         "base_y": 0, "layout": layout.pop("layout")}]
layout["layers"].append({"id": "terrace", "name": "Terrace", "base_y": 20,
                         "layout": {"shapes": [...], "islands": [...]}})
```

**Pop the old `layout` key.** `SketchRasterizer.ResolveLayers` reads `layers` *or* `layout` and
returns on the first, but `SketchLayout.IslandIds` reads both without an early return, so leaving it
behind doubles every island id.

**`floor` is the underside**, measured inside the layer: `base_y 20` + `floor 4` is a soffit at y24,
and the slab's thickness is its solved surface minus that. **Relief solves per layer**, keyed by
island id, and `ReliefFields` shifts the result into world Y before returning it — so `relief/read`
answers an upper island in world coordinates.

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
twelve-block slot, and the deck an island in the air. **Overlap the two footprints by a column** and
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

### A goal states its storey on the intent, because the plan has no field for it

`DestroyablePlacement` and `CorePlacement` carry `id · piece · at · style · materials · float · name`
and no `layer`; `DestroyableIntent` and `CoreIntent` carry `layer` as their first property, as do the
other four intent placements and `PlacedProp`. So a plan-built goal on a stacked board always
resolves against `SurfaceTop` — the highest layer — and a monument stated for a hall lands on the
deck roofing it, with nothing declined.

The word has to be written onto the **compiled intent**, on every orbit image, before
`PUT …/intent/from-plan`. `drive.py`'s `goalLayers` key does it, matching on `stamp.unit`:

```python
{"goalLayers": {"destroyable-1": "under", "destroyable-4": "deck"}}
```

Naming a layer the board has no ground on is a `DR-LAYER` decline for a prop; for a goal it is the
top surface again.

### A ramp at one course a cell builds as treads of two, and a two-block rise is a placed block

A `ramp` polygon falling 18 → 6 over **12** cells rasterized as `18 16 16 14 14 12 12 10 10 8 8` —
six steps of two — and `…/walk?aim=reach` answered `blocks 3` climbing it, because the walk prices a
rise of δ at δ−1 placed blocks. The same 12 courses over **20** cells reads one course a cell and
walks both ways for nothing. The rule to author by: **run at least twice the rise** on any stair
meant to be climbed rather than fallen down. (A 20-course ramp over 32 cells was right first time.)

### A prop's keep-out mask is 2-D, and `layer` does not reach it

`DR-CLAIM` declined a building on the `deck` layer at y38 as "claimed by" a building on the `ground`
layer at y18, twenty blocks below it. `PlacedProp.Layer` decides where a prop is *seated* and not
whether two props are in each other's way, so two kiosks on different storeys have to be moved apart
in plan. The same applies to `DR-ROAD` against a stroke on another storey.

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
`RasterizeLayout` writes the solved surface back over every cell in a solved island's footprint:
`cells[(x,z)] = (Math.Max(column.Floor + 1, field.At(x, z)), column.Floor)`. So an override-add's flattened
column is repaired to the solved height, and on a board where every cell is in some island's solve an
override brush works perfectly. Measured that way on `showcase/07-hill`, a bare `override: true` rectangle
over the west hill read **y13 · y16 · y12** across the summit — the hill, repainted.

**Where there is no field, there is no repair.** A shape carrying `relief_scope: "exclude"` takes its cells
*out* of the island's footprint (`SolveRelief` puts them in `excluded`, and the relaxation bends round them
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
kind. That reads as a modelling detail and it decides what terrain can be authored at all.

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
