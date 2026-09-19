# Painting a patch

**The card is about which shape forms the surface of a cell; the paint is only how that is made visible.**
Twelve panels carry the same island, the same relief and the same lobed outline under the same scree theme,
and what changes between two panels is what the shape says about its own height and which layer it is drawn
on. Open it in the studio as `technique-painting-a-patch`, or run `build.py`.

**A shape owns the paint on a cell only where its own drawn top is the tallest drawn top on that cell.**
`SketchRasterizer.ShapeScopeOwners` gives a cell to the smallest shape whose top **equals** the tallest one
there — `scopes && (standing || top == held.Ground) && area < held.Area` — so a patch drawn thinner than the
landmass under it forms no surface and paints nothing at all.

**Every panel's island is drawn twelve courses high, which is the number every patch is tested against.**
Eight of the twelve patches come out with paint on the board and four do not, and the built world looks
plausible either way: `census.txt` names the ones that landed and is the only witness there is.

## The document

Twelve groups on the `ground` layer, one ground theme and twelve scree themes with one paint between them,
and one relief per group with the same hill pushed up on its east side. The plain solves to y7 in every
panel. Row 3's four patches are each on a layer of their own instead.

| panel | what the patch says | what it built |
|---|---|---|
| `says-nothing` | `add`, no height at all | one course at bedrock — **no paint** |
| `one-short` | `add`, `base_height: 11` | one course under the island — **no paint** |
| `level-with-it` | `add`, `base_height: 12` | gravel at y7, level with the plain beside it |
| `override-thin` | `override: true`, `base_height: 1` | the column overwritten, the relief wrote it back — **no paint** |
| `raise-flush` | `height_mode: "raise"`, `base_height: 0`, `skirt: 0` | gravel at y8: painted, one course proud |
| `across-a-slope` | the same brush, drawn over a flank | a plate at y14 where the ground ran y7 to y25 |
| `over-excluded` | `override: true` over a `relief_scope: "exclude"` shelf | a hole: one bedrock block at y0, 11 under the shelf |
| `over-the-void` | `add`, `base_height: 12`, drawn past the coast | new ground at y7, seven rows out into the void |
| `on-a-layer` | the same shape on a layer at `base_y: 0` | a twelve-course slab, four of them above the plain |
| `layer-on-a-hill` | the same slab, drawn over the flank | buried: **81 of 260 cells** left showing |
| `layer-on-top` | a layer at `base_y: 8`, `base_height: 1` | gravel at y8 on the plain's own grass — flush, all 260 |
| `layer-solved` | the same slab, its group carrying the ground's relief | **36 of 260**: two fields, two answers |

```json
{"id": "patch-level-with-it", "type": "polygon", "operation": "add",
 "floor": 0, "base_height": 12, "theme": "scree-level-with-it",
 "vertices": [[34.8, -74.0], [34.47, -72.62], [33.56, -71.44], "…"]}
```

## What the shape has to clear

**A shape stating no height at all is one course at bedrock, not "no opinion".** `RasterShape` takes its
floor from `Floor ?? 0` and its thickness from `HeightFn`, whose last line is `double bh = s.BaseHeight ?? 1`.
The `says-nothing` panel is that shape, and its column reads grass at y7 like the plain beside it.

**One course decides it.** `one-short` states `base_height: 11` against the island's 12 and owns nothing;
`level-with-it` states 12 and owns 260 cells. The two panels are the same drawing and the same theme, and
the census lists one of them.

**The relief hides the height a patch states, which is why the height still has to be stated.**
`RasterizeLayout` writes the solved surface back over every cell of a solved group's footprint, so
`level-with-it`'s twelve courses come out as y7 — the same y7 as the plain well clear of it. Nothing about
the built ground says the patch asked for twelve; only the paint does.

**`override: true` does not rescue a patch that is too short.** Only the *set* an override-add belongs to is
privileged — `((adds − subtracts) ∪ override-adds) − override-subtracts` — and the ownership test inside that
set is the same one. `override-thin` overwrites its column outright, the relief writes it back, and the
panel reads grass at y7 with no scree anywhere.

**The override is also the only form on the ground layer that the store says anything about.** Both override
panels draw `SK14` as a **complaint**, not a refusal: *"is an override add stating a top of y1, and group
'override-thin' carries a relief that solves a surface through it — the world builds it to whatever the
relief says."* The two panels that quietly own nothing draw no finding at all.

## The standing brush, and what it costs

**A shape that says how its top is decided is a candidate whatever its height.** `IsErected` is the three
words `level`, `raise` and `sink`, and a standing shape skips the height test entirely — `standing ||
top == held.Ground`. So `raise-flush` paints its 260 cells with `base_height: 0`, which is a shape one course
thick.

**A standing brush is never flush.** `Erect` settles a cell at `datum + rise * Math.Max(1, floor(surface))`,
and that `Max` is a floor of one course: a `raise` of zero stands one **above** the median and a `sink` of
zero one below. The `raise-flush` patch reads gravel at y8 against grass at y7, with a one-course step round
its outline that `slopes.txt` still calls walked.

**And the datum is the median of the ground the footprint covers, read once for the whole shape.** Drawn
across a flank, `across-a-slope` replaced ground running from y7 to y25 with one plate at y14 — a
`DROP -11` off its uphill edge and a `DROP -7` off its downhill one, over 21 cells of what had been a hill.
`section-plates.png` is the same brush on level ground and on that flank, side by side.

**So a standing brush belongs on ground that is already level.** On a flank it is a bench, and a bench is a
thing an author decides to build rather than a side effect of wanting a different colour of dirt.

## Two ways to lose the ground under a patch

**Where the relief never solved, nothing writes a height back and an override stays what the rasterizer
made it.** A shape carrying `relief_scope: "exclude"` takes its cells out of the group's footprint, so the
`over-excluded` panel's shelf keeps its raw column at y11 — and the override stroke on top of it keeps its
raw column too: **one block of bedrock at y0**, seventeen cells across the transect and eleven courses under
the shelf beside it. `section-hole.png` is that trench.

**The shelf also shows what `exclude` really keeps, which is the merge and not the shape.** It states
`base_height: 1` and comes out at y11, because the island under it states 12 and `MergeCell` keeps the
taller of the two. An excluded shape is the one place a drawn height is built as drawn, so it is the one
place a wrong one is visible.

**A patch is a shape, and a shape is ground: drawn past the coast, it moves the coast.** `over-the-void`'s
outline overshoots its island's north edge by seven rows, and those rows came out as ordinary ground at y7
wearing the patch's gravel. The census counts it: its border with the moor is **58 cells** where every other
whole patch's is 88, because the missing 30 are now the map's own edge.

## A patch on a layer of its own is not a patch

**A layer keeps its own span per column and its own owner per cell, so a shape on a second layer never
competes with the ground at all.** `ShapeScopeOwners` keys by `(layer, x, z)`. The shape owns its own
layer's cells outright, and whether any of that is *seen* is settled afterwards, by which layer's top block
is higher in each column.

**Which makes a twelve-course patch on a layer at `base_y: 0` a twelve-course slab.** `on-a-layer` builds
y0 to y11 with the plain's own grass still at y7 inside it, and from above it is a gravel table standing four
courses proud. `SK10` says so at the store door: *"layers 'ground' and 'over-on-a-layer' are driven 9
block(s) into each other over 260 column(s) … so they build as one solid mass."*

**Over a hill the ground wins wherever it stands higher, and it usually does.** `layer-on-a-hill` is the same
slab drawn over the flank: at (−25, 87) the column reads the hill's grass at y14 over the slab's gravel at
y11, and the census counts **81 of its 260 cells**. Nothing is clipped and nothing is refused — the slab is
built, and buried. `section-layer.png` is it going into the hill and out the other side.

**The only second-layer patch that behaves like paint is one course resting on the ground's own top.**
`layer-on-top` states `base_y: 8` and `base_height: 1`, and its column reads gravel at y8 over the plain's
grass at y7: all 260 cells, flush with the plain, and no `SK10`. Its picture is indistinguishable from
`level-with-it`'s.

**And `base_y` is one constant for a whole layer, so that trick works exactly as far as the ground is
level.** There is no per-cell base, and a layer cannot be told to follow the field under it.

**Giving the second layer its own relief makes it worse rather than better.** `layer-solved` carries a copy
of the ground group's relief, but that field is solved over the patch's own footprint instead of the
island's, so the two answers disagree: **36 of 260 cells**, gravel at y20 where the hill stands at y19 eight
blocks away, and buried at y11 where the hill stands at y14. Two fields over one piece of ground do not
agree.

**So a second layer is for what stands clear of the ground, and paint is not that.** `stacking-layers` is
the card for what layers are good at; paint belongs on the ground layer with the terrain it is painting.

## Where the bands were cut

**`incline.txt` is what the ground theme's slope bands were cut against, and this board is mostly flat.**
60.7% of its ground stands under 10° and 19.8% at 40° or steeper, and the hill's own flank fills the 30–49°
buckets with a quarter of the board. So the bands cut at 60° and 75°, above the flank rather than through it.

**A band edge inside the flank's own population stripes the flank.** A cut at 25° puts every cell of a 30–49°
hillside in one band and paints the whole of it bare earth; a cut at 45° puts the hillside on the edge and
alternates it block by block down the slope. Above the flank the hill is grass, with earth showing only where
a riser stands near vertical.

**So the number is read off the board every time, never carried over from another one.** `made-ground` and
`marks-and-pushes` cut at 25 and 45, `water` at 35 and 55, `pushes` and `winding-roads` at the default 15 and
40, and this one at 60 and 75 — four cuts over five boards, each read off its own histogram.

## The recipe

**Draw the patch on the ground layer, at the same `floor` and `base_height` as the ground it sits on, and
let the relief settle the height.**

```json
{"id": "talus", "type": "polygon", "operation": "add",
 "floor": 0, "base_height": "<the landmass shape's own base_height>",
 "vertices": ["…"], "theme": "scree"}
```

- **match the tallest shape on the cell, or beat it** — equal wins on the smaller area, short loses in silence.
- **do not reach for `override: true`**: it overwrites the column, changes no ownership, and is the one form
  that draws a complaint.
- **a `height_mode` brush paints whatever its height, and costs a course**: `raise` 0 is median + 1,
  `sink` 0 is median − 1.
- **never draw a standing brush across a slope** unless a bench is what is wanted.
- **keep a patch inside the coast**, or the coast moves out to meet it.
- **paint does not go on a second layer.** A slab at `base_y: 0` buries itself in the terrain; only a
  one-course layer at the ground's own top is flush, and only where that ground is level.
- **read `themes/census` after every build.** A patch that owns nothing builds a world that looks right.

## Limits

**This card is the shape instrument only.** The other way to put one finish over another is a path prop
whose `pave` replaces a surface without adding a cell — a stroke rather than an outline, which can feather
one theme into another but cannot follow a drawn shape, and which closes the ground it paints to flora.
That is its own card and is not built yet.

## What checks it

- `census.txt` — nine themes over 46,132 cells: the moor and the **eight** scree themes that reached a
  surface, out of twelve drawn, with `layer-on-a-hill` at 81 cells and `layer-solved` at 36. The names that
  are missing, and the two counts that are short, are the card.
- `columns.txt` — twenty columns: one in the middle of each patch, the ground beside those that needed a
  comparison, and both sides of the two layer panels the hill cuts through.
- `transects.txt` — six profiles: the flush patch changing nothing, the raise brush's one-course plate, the
  median plate across the flank, the trench through the excluded shelf, the new coast, and the slab going
  into the hill and out again.
- `incline.txt` — the histogram the slope bands were cut against.
- `slopes.txt` — what the brushes did to the walk: the raise brush's rim is walked, the flank plate's two
  edges are not.
- `painting-a-patch.layout.json` — the one document the board was stored from. It stores with two `SK14`
  and three `SK10` complaints and no refusal, which is itself several of the claims.

Renders: `row1-owning.png` — four statements, one patch visible; `row2-ground.png` — the four that own their
paint and what each did to the ground; `row3-layers.png` — the same outline off the ground layer;
`section-plates.png`, `section-hole.png` and `section-layer.png` for the geometry; `iso.png` for all twelve.
