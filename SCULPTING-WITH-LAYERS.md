# Sculpting with layers

The sketch tool's layer system was built to stack storeys. This is the record of what happens when it is
asked for something else — a statue, a ring station, a car, a robot — and of the six facts that decide how far
it goes. Everything here was measured against a running studio; the boards are in `sculpture/` and
`maps/opus5-automaton`, the tools that produced them in `tools/sculpt/` and `tools/render/`.

**The short answer is that it goes further than the documentation suggests, and the ceiling is not where it
looks.** A layer is not a flat slab. It is one arbitrary *height field* — a `(floor, top)` pair per column —
and a stack of layers is a set of those fields with air between them. Any solid whatever can be written in
that form, and the number of layers it needs is not its height: it is **how many separately-coloured runs the
busiest column of it passes through**. A thirty-block statue needs eight layers. A car needs three.

---

## 1. What a layer actually is

`docs/tools/sketch.md` states the rule plainly — *"a layer is a slab … one layer holds exactly one span per
column … where two adds contest a cell the taller replaces the shorter outright, floor included"* — and the
last five words are the whole of what makes sculpture possible.

**The taller add wins the column, and it brings its own floor with it.** So a stack of nested shapes, ordered
so that the one meant to own a ring of columns is the tallest over it, writes a height field with no
subtraction and no per-column authoring. A dome is concentric discs whose tops rise inward. A *hollow* dome
is the same discs with their floors rising too, by the shell's own curvature, so what each column keeps is
the thickness of the shell at that radius. Thirteen circles, one layer, one number changed between the solid
and the hollow case.

`SK9` names a pair of stacked shapes only where one shape's **floor sits at or above another's top**. Nested
discs sharing a floor say nothing; nested discs whose floors rise by less than the shell is thick say nothing
either. The rule is aimed at a roof drawn over a floor, and it does not fire on any of this.

**There are exactly two height fields per layer, not one.** The set algebra is
`((adds − subtracts) ∪ override-adds) − override-subtracts`, and the two add sets each settle among
themselves by height before the override plane overwrites the ordinary one. An override add therefore
replaces the column it lands on *whatever its height is*, which is what puts a one-block floor inside a
twelve-block wall, and a threshold through a doorway, with neither shape cut against the other.

**Nesting can only build a field that rises inward.** A bowl falls inward, and the outer disc that should
keep only its own ring is also the tallest thing over the middle — nested discs come out as a flat plate.
A falling field needs shapes that do not overlap at all.

## 2. A ring is one polygon, and a subtract is not what it looks like

The obvious way to draw a ring is an outer circle minus an inner one. It works, and on a board with anything
else on it, it is refused.

`SK13` reads a subtract as **the board's negative space** — the void a plan's buffer pieces compile to — and
refuses any add that fills it, *on any layer*. So the deck a roundhouse stands on and the roof over it both
collide with the subtract that hollowed the roundhouse: eleven `SK13` findings and a 422 from
`POST /map/from-documents`, on the first attempt at this. The exemptions are narrow and do not help: an add
listed **earlier than the subtract in the same layer's shape array** is exempt, and a same-layer override add
whose floor is above the subtract's is read as a lid.

The way through is that **an outline is filled even-odd**. Run the outer ellipse, slit inward, run the inner
ellipse the other way round and close: a ray into the middle crosses two boundaries and lands outside the
fill, and the slit's two coincident edges cancel. That is one polygon, no subtract, no `SK13` — and it is what
every hollow form in `tools/sculpt/props.py` is written with.

Where a hollow needs a floor rather than a hole, the override plane does it: an override-add disc inside the
wall, one block thick, at the wall's own floor.

## 3. The compiler: run index, not height

For a form that is not a stack of round profiles — a figure with limbs, a car, a shelled torus — the general
decomposition is mechanical and it is **not** one layer per Y level.

Take the model's blocks. Per column, split them into maximal runs of one material. Send the *n*-th run of
every column to layer *n*. Within a layer every column then carries at most one run by construction, so the
shapes are the rectangle cover of each `(material, floor, top)` group — and the groups are disjoint, so
nothing contests anything. Two runs of one column always have air between them, so no pair of layers is ever
driven into another and `SK10` stays silent. Two shapes on a layer never overlap, so `SK9` stays silent.

`tools/sculpt/layers.py` is thirty lines of that. What it costs, measured:

| model | size (x, y, z) | blocks | layers | shapes | blocks/shape |
|---|---|---|---|---|---|
| robot | 26 × 45 × 14 | 4,486 | 16 | 746 | 6.0 |
| space station | 118 × 58 × 66 | 29,418 | 7 | 2,557 | 11.5 |
| car | 22 × 14 × 38 | 4,630 | 3 | 212 | 21.8 |
| hooded statue | 25 × 45 × 23 | 6,699 | 8 | 363 | 18.5 |

Read the layer column first, because it is the surprising one. The **station is 58 blocks tall, mostly
hollow, and takes seven layers**; the **car is 14 tall and takes three**. Height has nothing to do with it.
What sets the count is the busiest column — the one that passes through a boot, then air, then a hand, then
air, then a brim. `sculpture/models/renders/robot-layers.png` is the picture of it: layer 0 holds 1,686 of the
robot's blocks, layer 1 holds 900, and by layer 14 there is a single block left.

**Material is what makes the robot expensive, not geometry.** A layer's span carries one theme, so a colour
change inside a contiguous run splits it as surely as air does. The robot has a visor, a brow band, eyes, a
chest panel and a mouth grille all on one curved head, and each is a band the column has to leave and
re-enter. Nine of its sixteen layers hold fewer than eighty blocks each and exist entirely to carry markings.
The car, painted in four flat colours, needs three.

## 4. What the painter does to a sculpture

The terrain painter's five buckets — bedrock, fill, wall, surface, rim — are a model of **ground**: a wall
down every exposed riser, a rim capping every plateau boundary. A curved voxel form is nothing but plateau
boundaries, so a three-tone theme speckles the whole surface of a sphere. Every piece here therefore states a
**solid** theme, one block a material, and lets the geometry do the reading. The ground keeps its shading.

Two smaller facts cost time and are worth writing down:

- **Never theme a sculpture in plain stone.** The painter's stone-only invariant means a stone theme writes
  nothing and leaves its cells still stone, so the next layer's pass paints straight through them. A pillar
  themed in stone standing on ground themed in stone came out entirely as the pillar's material, floor
  included.
- **`bedrock` clamps to at least one course.** `BedrockSpec.PaintFloor` is `clamp(value, 1, surfaceTop)`, so
  y=0 is bedrock wherever a column has ground at all. It never reaches a prop standing above the terrain, and
  a prop that starts at y=0 will have a bedrock sole.

## 5. Where it stops

Four limits, each measured rather than reasoned:

**A prop cannot be seated on a relief.** A prop's shapes state an absolute `floor`; a relief moves the ground
under them. On rolling terrain every prop either floats or is buried, and `SK10` names all of them — the first
`opus5-automaton` build raised nine of these, up to seven courses deep. `height_mode: raise` is the studio's
answer for a shape *inside* an island's relief, and it does not reach a shape on another layer. The board
here is flat because of it. **The fix is two-pass and cheap**: post the ground-only layout, read
`POST …/sketch/columns` for the solved top at the prop's centre, and set the prop's floor from it. Nothing in
the API is missing; nothing calls it in that order yet.

**`SK10` misreads a prop as a storey.** A solid sculpture standing on a hill *should* sink into the hill —
there is no gap to lose. The rule's sentence ("the gap between the two storeys is not in the world there") is
about a gallery under a deck and is simply not true of a statue. It fired on nine props that were correct.

**`SK11` fires on every prop with a roof or an overhang.** The gallery raises twenty-two of them: a dome on
columns, a raised arm, an antenna ball. All are true statements ("standable ground with sky over it and no
route onto it") and none is a fault. A prop layer would want to be out of that walk.

**A board's layer list stops being readable.** `opus5-automaton` carries thirty-one layers, twenty-four of
which are `colossus-L0 … sentinel-L7`. `GET …/render/topdown?layer=` takes a sketch layer id, and the refusal
message for a bad one now prints all thirty-one. The layer strip in the Draw phase would be unusable.

## 6. What could become a tool

Three things, in the order they pay off.

**A prop library of parametric forms, emitting sketch shapes.** `tools/sculpt/props.py` is the prototype:
`ring_wall`, `ellipse_wall`, `dome`, `spire`, `ziggurat`, `arch`, `colonnade`, `tapered_tower`, `bowl`. Each
takes a footprint and a few numbers and returns shapes an author can then drag, because they *are* circles
and polygons with a floor and a height — not a stamped block soup. The cost is measured and small:

| form | layers | shapes |
|---|---|---|
| roundhouse wall, two doors, floor | 1 | 4 |
| conical roof | 1 | 9 |
| hollow dome, radius 13, 3 thick | 1 | 13 |
| hollow ellipse, 15 × 9 | 1 | 2 |
| tapered tower, 30 tall | 1 | 6 |
| ziggurat, five tiers | 1 | 5 |
| arch, 22 span | 1 | 11 |
| colonnade of twelve | 1 | 12 |
| amphitheatre, six tiers | 1 | 7 |

Eight of the nine are one layer. That is a dressing prop, not a new subsystem — it wants the same shape the
house stamper already has, emitting into the sketch document instead of into the world.

**Seat a prop against the solved ground.** Either the two-pass read above, or a `height_mode` for a whole
layer: a layer that says `"seat": "raise"` takes each shape's floor from the top of whatever ground stands
under it. That one field removes the whole `SK10` class and is what lets a prop be dragged around a hillside.

**Say that a layer is a prop.** One flag on the layer — `"kind": "prop"` — would take it out of `SK10`'s pair
walk and `SK11`'s reachability walk, and would let the storey strip and the topdown render group thirty-one
layers into four props. None of the three needs the rasterizer to change.

## 7. Running it

```bash
python3 tools/sculpt/gallery_forms.py      /tmp/forms       # the nine parametric forms
python3 tools/sculpt/gallery_sculpture.py  /tmp/sculpture   # the four compiled models
python3 tools/sculpt/make_board.py         specs/opus5-automaton
python3 tools/drive.py specs/opus5-automaton "Automaton" --out /tmp/automaton
```

Each posts to a running studio at `$PGM_STUDIO_API` (default `http://localhost:7894/api`), reads the built
world back through `POST …/sketch/columns` and renders it. The renderer is `tools/render/` — a PNG writer, an
isometric painter and an orthographic elevation, in the standard library alone, because the studio's own 3-D
preview is WebGL in the browser and there is no way to take a picture from it.
