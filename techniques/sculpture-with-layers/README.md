# Sculpture with layers

**A layer is not a slab: it is one arbitrary height field, a `(floor, top)` pair per column.** Anything that
can be written in that form can be authored out of rectangles, circles and polygons, and detail is what more
layers buy. Twenty pads carry twenty made things and not one of them is a preset: sixteen drawn by hand and
four compiled from solids, which is the same instrument one rung further up. Open it in the studio as
`technique-sculpture-with-layers`, or run `build.py`.

**Two rules decide every shape on this board, and the first is that the taller add wins the column and
brings its own floor with it.** So a set of nested shapes, ordered so the one meant to own a ring of columns
is the tallest over it, writes a height field with no subtraction and no per-column authoring.

**The second is that a layer holds exactly one span per column, which is what decides how many layers a
thing needs.** A merlon standing on a string course, a rail standing on a deck and a corbel standing on a
shaft are each a second span over ground the first already claimed, and each is a layer of its own.
`SCULPTING-WITH-LAYERS.md` is the long record behind this card — the galleries, the layer counts and what
the ceiling is.

## The document

Twenty groups on the `ground` layer for the pads, and thirty-eight more layers above them. Thirty of those
are drawn and rest at a stated `base_y`; eight state `kind: "made"` and are the four compiled panels plus one
crate. Eighteen pads are flat — a shape on a ground layer states an absolute floor, so their ground is a
plain solved to y7 and their layers start at `base_y: 8` — and two are a ramp on purpose: the panel about
what that costs and the panel that answers it.

| panel | layers · shapes | what it is |
|---|---|---|
| `one-shape` | 1 · 1 | a wall: one rectangle, seven courses |
| `a-polyline` | 1 · 1 | the same wall as a splined band, which is how a curve is drawn |
| `detailed` | 4 · 11 | plinth, body, string course, eight merlons — one layer per height |
| `an-arch` | 2 · 3 | two piers and a lintel: the gateway is ground nobody drew on |
| `a-basin` | 1 · 2 | a rim and an override-add one course high inside it |
| `cover` | 1 · 5 | five crates, the simplest useful sculpture there is |
| `a-bridge` | 3 · 5 | two piers, a deck, and rails on a layer of their own |
| `a-tower` | 3 · 3 | a shaft, a corbel and a cap, each a span over the last |
| `a-dome` | 1 · 11 | eleven nested discs whose tops rise inward |
| `a-hollow-dome` | 1 · 11 | the same dome hollow: eleven rings, floor and top both curved |
| `material-only` | 1 · 4 | a ziggurat painted by one terrain material |
| `a-theme` | 1 · 4 | the same ziggurat painted by five buckets |
| `a-bowl` | 1 · 11 | eleven rings again, for a field that falls inward |
| `a-balloon` | 3 · 15 | a hollow basket, four ropes and a closed envelope of revolution |
| `two-colours` | 3 · 7 | one box in one paint, one in three bands, three in a row |
| `on-a-slope` | 4 · 4 | the same crate buried, hand-seated, floating, and told to settle |
| `compiled-wall` | 1 · 1 | `one-shape`'s wall written as a solid: the compiler draws the same rectangle |
| `a-wheel` | 2 · 116 | a torus on edge — two runs in every column, so two layers |
| `a-shell` | 2 · 190 | a hollow sphere: two runs whatever the radius |
| `seated` | 2 · 116 | the same wheel, `seat: "ground"`, settling onto a grade |

```json
{"id": "outer", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 6,
 "min_x": -129, "min_z": -45, "max_x": -105, "max_z": -25, "theme": "masonry"}
{"id": "inner", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 1,
 "min_x": -127, "min_z": -43, "max_x": -107, "max_z": -27, "override": true, "theme": "masonry"}
```

## One wall, four ways

**The least that will do is one rectangle**, and it is worth saying because most walls on most boards want
nothing more. `one-shape` is a 32 × 2 rectangle seven courses high on one layer.

**A curve is a polyline, not a run of rectangles.** `a-polyline` states nine vertices on an arc and a radius
of 1.5, and the splined band is the wall — the same shape family `winding-roads` draws a road with.

**Detail is layers, and the count is how many heights something happens at.** `detailed` is the same
straight wall with a plinth that oversails it, a body, a string course that oversails it again and eight
merlons — four layers, eleven shapes, because each of those four things wants a different footprint at a
different height. Its merlon column reads the lot in one go: merlon, string course, body, plinth, ground.

**And an opening is two shapes and a third over them, never a subtract.** `an-arch` states a west pier and
an east pier with a gap between them, and a lintel on a second layer spanning both. Under the lintel the
column reads two courses of brick at y15–16 and then nothing until the grass at y7 — the gateway is ground
nobody drew on, which is cheaper and more legible than cutting one wall with another.

## Space, and what makes it

**An override-add replaces the column it lands on whatever its height is, and that is how a solid becomes
hollow.** `a-basin` is a rectangle six courses high with a second rectangle inside it — `override: true`,
one course — so the middle is a floor at y8 and the rim beside it stands to y13. The same two lines make a
pool, a courtyard, a room or a balloon's basket.

**Air under a made thing is the layer boundary doing its work.** `a-bridge` reads one course of deck at y16
over eight courses of air, because the deck's layer starts at `base_y` 16 and the painter writes each layer
over its own span only.

**A span is two piers and a deck, and a parapet on the deck is a second layer.** `a-bridge` states its rails
at `base_y` 17 over a deck at 16, because a rail over a deck is a second span over the same ground — stated
on the deck's own layer it is `SK9`, and the world keeps only one of them.

**An overhang is the same fact turned sideways.** `a-tower` is a shaft of radius 7, a corbel of radius 8 and
a cap of radius 6, on three layers; a block past the shaft the column reads two courses of corbel at y21–22
with thirteen courses of air under them and the pad at y7.

## The round things there are no primitives for

**A solid dome is concentric discs whose tops rise inward, on one layer.** `a-dome` states eleven circles at
one `floor` with heights from `√(R² − r²)`, and because the taller add wins no disc has to be cut against
its neighbour. Its middle column is eleven courses of solid over the plain, crowned at y18.

**A hollow dome is the same field with a floor that rises too, and that is where nesting starts to cost.**
Raise the inner discs' floors and each becomes a *span* over ground the disc outside it also claimed: the
world still comes out hollow, but eleven discs on radius 11 raise **sixteen** `SK9`, and a board that raises
sixteen complaints it means has no gate left for one it does not.

**So the shell is drawn as rings, which overlap nothing at all.** An outline is filled even-odd, so a ring is
one polygon — the outer circle, a slit inward, the inner circle the other way round, and back — and eleven
of them on one layer raise **no finding**. `a-hollow-dome` reads four courses of shell at its crown over
eight of air, and seven at the springing where the shell comes down to the ground.

**A field that *falls* inward is the case nesting cannot draw at all, and nothing says so.** The disc that
should keep only its own ring is also the tallest thing over the middle, so eleven nested discs come out a
**flat plate 22 cells across at one height** — measured, with no `SK9`, no `SK10` and no complaint of any
kind. `a-bowl` states the same eleven tiers as rings and reads y17 at the rim falling to y10 in the middle.

**A closed form of revolution needs both ends of the rule.** `a-balloon`'s envelope is nine rings whose
floor *and* top come off the sphere, so the underside curves as the top does; its basket is the override-add
trick and its four ropes are 1 × 1 rectangles, and the three sit on three layers because they are three
footprints at three heights over the same columns. Under a rope the column reads basket, rope, two courses
of air, then fourteen of envelope.

## What a colour costs

**A layer is spent on paint as readily as on shape, because a run of one block is what a span is.**
`two-colours` states the same 12 × 12 box three ways and the layer count follows the columns, not the
palette.

**One box in one paint is one layer, and three boxes in three paints beside each other are still one.** No
column of the row passes through more than one of them, so nothing contests anything: three shapes, three
materials, one layer, no finding.

**The same box in three horizontal bands is three layers.** Its column reads sandstone at y8–10, stone brick
at y11–13 and planks at y14–16 — three runs in one column, and a layer holds one span, so the bands cannot
share one. That arithmetic is the whole of why a painted solid gets expensive: a Rubik's cube is one layer
of geometry and seven of colour.

## The one trap

**A made thing states an absolute floor and the relief does not know about it.** `on-a-slope` is the only
pad here with ground in it — two facing marks, y19 at the north edge falling to y7 at the south — and it
carries the same crate three times.

**Stated at the height the other fifteen pads use, it is inside the hill.** The `buried` crate's `base_y` is
8, the ground over it solved to y19, and its column reads grass, dirt and stone from y19 down to y13 and
then two courses of brick at y11–12. `SK10` names it; nothing else can, and the isometric shows an empty
pad.

**Stated too high it hangs.** The `floating` crate is the same five courses at `base_y` 20 over ground at
y7: twelve courses of air, `SK11`, and a thing no player reaches.

**And a number read off the ground is right in one cell.** `by-hand` stands at 15 because
`POST /sketch/columns` reads y14 as the highest ground under its footprint, and it comes out hovering: its
column is brick from y15 to y19, a gap at y14, then grass at y13. A made thing has one floor and a grade has
many.

## When shapes run out

**Every panel above was drawn; a thing that cannot be drawn is written as a solid and compiled.**
`tools/sculpt/solid.py` is the vocabulary — boxes, ellipsoids, frusta, tori, revolves, swept tubes and
lifted sheets, with union, intersect, difference and shell over them — and `tools/sculpt/layers.py` turns
any `{(x, y, z): material}` model into layers.

**It compiles against the rule this whole card rests on: a layer holds one span per column.** A column's
blocks split into maximal runs of one material and the n-th run of every column goes on layer n, so the
stack is as deep as the busiest column is complicated and never deeper. Nothing in row 5 states a layer
count; `compiled.txt` is what the compiler answered.

**On a shape a hand would have drawn it draws exactly that.** `compiled-wall` is `one-shape`'s wall written
as `box(cx−16, cx+15, 8, 14, cz−1, cz)` — 448 blocks in, **one layer and one rectangle** out, and the
rectangle is the one `one-shape` states by hand. The compiler is not a second system.

**Above that it answers what nesting cannot.** `a-wheel` is a torus stood on edge, so every column through
its rim passes the ring twice: 1,472 blocks, **two layers**, 116 shapes. `a-shell` is a hollow sphere two
thick and is also **two layers**, whatever its radius, because two runs is what a hollow ball has — where
row 3 needed rings to hold a dome's shell in one layer, the compiler needs no trick at all.

**What it costs is shapes.** Rows 1 to 4 are 97 rectangles, circles and polygons; row 5's four panels are
**423**. A drawn document stays editable in the Draw phase as a circle with a radius, and a compiled one is
rectangles that happen to look like a wheel — which is the whole reason to draw whatever can be drawn.

**And `SK23` reads it that way too.** 217 of this board's 240 flagged shapes are row 5's, because a compiled
shape is a thin strip by construction and every column of one is an edge. **A compiled thing wants a solid
theme or a material, not five buckets.**

## The two words that make a made thing

**`kind: "made"` says a layer is a thing standing on ground rather than being it, and the stacking rules
come off.** `a-tower`'s corbel raises `SK11` and `a-wheel`'s rim — a bigger overhang on the same board —
raises nothing: all fourteen `SK11` findings here are rows 1 to 4, where the layers are ground.

**`seat: "ground"` is the answer to row 4's trap, and it belongs to the layer, not to the compiler.**
`on-a-slope`'s fourth crate states no height at all — `kind: "made"`, a `part_of`, and `seat: "ground"` —
and the studio drops the whole thing until its lowest floor is one above the lowest ground under its
footprint, then cuts the terrain under it to that course.

**Measured side by side on one grade.** `by-hand` at `base_y` 15 reads brick y15–19, a gap at y14 and grass
at y13. `told-to-settle` ten blocks away reads brick y12–16 resting on grass at y11, where the grade beside
it tops at y13 — bedded in rather than perched. `section-compiled.png` is the same thing at wheel scale,
with the notch cut for it.

**Which is what `part_of` is for: a made thing is one thing to an author and many layers to the rasterizer.**
Layers naming the same `part_of` are seated together over the union of what they cover, so a two-layer wheel
lands as a wheel instead of coming apart at its run boundary.

## A terrain material against a theme

**`material-only` and `a-theme` are the same four rectangles at the same four heights, and they are painted
by the two instruments the studio has.** One states a `material` on the shape; the other states a `theme`.

**A material answers the same question at every course of every column.** The ziggurat's material is a
`cell` pattern with a `rise` of 4, so its top reads four mossy bricks over four plain ones over stone, and
its own face three courses down reads bricks, then **four courses of stone**, then bricks again — the
pattern cutting through the solid with no regard for where the surface is.

**A theme asks where the column is.** The same ziggurat under `masonry` reads mossy brick at its crown (the
rim), plain brick under it (the surface), and **stone all the way down** (the fill); on its face, chiseled
brick at the edge, two courses of wall, then fill. Five buckets, five answers, one per part of the thing.

**Which is why a sculpture is where the two stop being interchangeable.** Ground is seen from above and a
material is enough for it; a made thing has faces, edges, a crown and a core, and only a theme can tell
them apart.

**And a thing thinner than three cells has no core to tell apart.** Of the drawn panels `SK23` names
twenty-three shapes across eleven findings — every merlon, both rails, both piers, four ropes, the wall, the
lintel, the body, and the outermost ring of each of the four round forms — because *"not one of their
columns has ground on all eight sides, so every column is an edge, the rim and the wall are the only
buckets that paint them"*.

**Row 1 has the measurement side by side.** `one-shape`'s rectangle is two cells wide and every column of it
reads chiseled brick over plain: rim, then wall. `a-polyline`'s band at radius 1.5 is three, and its middle
column reads mossy brick, plain brick, then stone — surface, then fill. One cell of width is the difference
between a theme using two buckets and a theme using four.

**A shape stating a `material` keeps whatever theme it stands under, which the census counts honestly.**
`two-colours`' three paints are all filed under `moor`, the board's ground theme, so `census.txt` reads
seven surface blocks for that theme and two for `masonry` — a material is paint, not membership.

## The recipe

- **nest from one floor and let the taller add win** — a ziggurat, a dome and a stepped plinth are all that
  one move, and stacking the shapes on each other's tops instead is `SK9`.
- **a floor that rises, or a surface that falls, wants rings**: an even-odd outline (out, slit, back the
  other way) is one ring and no subtract, and rings that do not overlap contest nothing. Nesting a falling
  field builds a flat plate and says nothing at all.
- **a second span over the same ground is a second layer**, every time: a rail on a deck, a merlon on a
  course, a corbel on a shaft, an envelope over a rope.
- **count the layers a painted thing needs off one column**, not off the palette: bands stacked in a column
  are separate runs and cost a layer each; the same paints side by side cost nothing.
- **order the layer list by `base_y`**, or `SK20` says the document reads wrong.
- **hollow a prism with an override-add one course high** — the same two lines are a basin, a room or a
  basket.
- **an opening is a gap between two shapes**, not a subtract.
- **a shape on a ground layer states an absolute `floor`**; a layer stating `kind: "made"` and
  `seat: "ground"` is put on the ground for you, whole, and cuts its own bed.
- **draw whatever can be drawn, and compile the rest** — `solid.py` states the model, `layers.py` splits
  every column into runs and answers with the layer count. A compiled document is not editable as shapes.
- **theme what has a core; state a material on what does not**, and three cells is where a core starts —
  which makes every compiled thing a material, since a compiled shape is a strip.

## Limits

**This board raises thirty-three complaints and no refusal, and the shape of them is the card.** Eighteen
are `SK23` — 217 of the 240 shapes they name are row 5's compiled strips; fourteen are `SK11`, every one on
a ground layer in rows 1 to 4, because a `kind: "made"` layer is out of that walk; and the one `SK10` is the
`buried` crate, which is the panel.

**A made thing is not ground, and the census says so.** `masonry` holds 3,270 cells here and held 3,270 on
the same board before row 5 existed: four more sculptures added none, because `GET …/themes/census` counts
terrain and a `kind: "made"` layer is not terrain.

**What a compiled document costs is editability, and past thirty layers a board stops being readable.** A
compiled wheel is 116 rectangles nobody can adjust as a wheel; `SCULPTING-WITH-LAYERS.md` §5 has the rest
of where this stops, and §6 what would change it.

## What checks it

- `columns.txt` — thirty-three columns: one per claim, from the wall and the polyline band's two cells
  through the basin, the deck and its rail, the tower's corbel, both domes, the bowl, a balloon rope and the
  two ziggurats, to the four crates on one grade and the four compiled panels.
- `compiled.txt` — what `tools/sculpt/layers.py` answered for row 5: blocks in, layers and shapes out. No
  layer count on this board was stated by hand.
- `census.txt` — two themes over 71,680 cells and eight surface blocks, and `masonry` unchanged by row 5.
- `sculpture-with-layers.layout.json` — twenty panels, thirty-nine layers and 541 shapes: twenty pads, 97
  drawn on ground layers and 424 on made layers, 423 of them row 5's. No props at all.
- `incline.txt` — 85.8% of this board's ground under 10° and 6.5% at 40° or steeper, which is eighteen flat
  pads, two grades and the made things standing on them.
- `slopes.txt` — 68,179 cells walked, 482 scrambled and 3,019 barrier, which is the sculptures' own faces.

Renders: `row1-a-wall.png`, `row2-space.png`, `row3-round.png`, `row4-round-and-cost.png`,
`row5-compiled.png`; `section-domes.png` — the solid dome and the hollow one, the only view that difference
reads in; `section-falling.png` — the bowl and the balloon at the rope line; `section-compiled.png` — the
wheel, the shell and the seated wheel with the bed cut for it; `section-paint.png` — the two ziggurats;
`iso.png` for all twenty.
