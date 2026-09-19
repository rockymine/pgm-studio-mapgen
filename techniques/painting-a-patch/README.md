# Painting a patch

A patch of ground painted differently from the ground around it is an authored shape carrying a `theme`.
What that shape may say about its own height is much narrower than it looks, and saying it wrong loses the
paint in silence. Eight panels carry the same island, the same relief and the same lobed outline under the
same scree theme, and only the shape's own statement about its height changes. Open it in the studio as
`technique-painting-a-patch`, or run `build.py`.

**A shape owns the paint on a cell only where its own drawn top is the tallest drawn top on that cell.**
`SketchRasterizer.ShapeScopeOwners` gives a cell to the smallest shape whose top **equals** the tallest one
there — `scopes && (standing || top == held.Ground) && area < held.Area` — so a patch drawn thinner than the
landmass under it forms no surface and paints nothing at all.

**Every panel's island is drawn twelve courses high, which is the number every patch is tested against.**
Four of the eight patches clear it and four do not, and the built world looks the same either way:
`census.txt` names the four that landed and is the only witness there is.

## The document

Eight groups on the `ground` layer, one ground theme and eight scree themes with one paint between them, and
one relief per group with the same hill pushed up on its east side. The plain solves to y7 in every panel.

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

```json
{"id": "patch-level-with-it", "type": "polygon", "operation": "add",
 "floor": 0, "base_height": 12, "theme": "scree-level-with-it",
 "vertices": [[34.8, -37.0], [34.47, -35.62], [33.56, -34.44], "…"]}
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

**The override is also the only form the store says anything about.** Both override panels draw `SK14` as a
**complaint**, not a refusal: *"is an override add stating a top of y1, and group 'override-thin' carries a
relief that solves a surface through it — the world builds it to whatever the relief says."* The two panels
that quietly own nothing draw no finding at all.

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
patch's is 88, because the missing 30 are now the map's own edge.

## Where the bands were cut

**`incline.txt` is what the ground theme's slope bands were cut against, and this board is mostly flat.**
61% of its ground stands under 10° and 19.7% at 40° or steeper, and the hill's own flank fills the 30–49°
buckets with a quarter of the board. So the bands cut at 60° and 75°, above the flank rather than through it.

**A band edge inside the flank's own population stripes the flank.** A cut at 25° puts every cell of a 30–49°
hillside in one band and paints the whole of it bare earth; a cut at 45° puts the hillside on the edge and
alternates it block by block down the slope. Above the flank the hill is grass, with earth showing only where
a riser stands near vertical.

**So the number is read off the board every time, never carried over from another one.** `made-ground` and
`marks-and-pushes` cut at 25 and 45, `water` at 35 and 55, `pushes` and `winding-roads` at the default 15 and
40, and this one at 60 and 75 — four cuts over five boards, each read off its own histogram.

## The recipe

**Draw the patch at the same `floor` and `base_height` as the ground it sits on, and let the relief settle
the height.**

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
- **read `themes/census` after every build.** A patch that owns nothing builds a world that looks right.

## What checks it

- `census.txt` — five themes over 30,772 cells: the moor and the **four** scree themes that landed, out of
  eight drawn. The four missing names are the card.
- `columns.txt` — thirteen columns: one in the middle of each patch, and the ground beside the four that
  needed a comparison.
- `transects.txt` — five profiles: the flush patch changing nothing, the raise brush's one-course plate, the
  median plate across the flank, the trench through the excluded shelf, and the new coast.
- `incline.txt` — the histogram the slope bands were cut against.
- `slopes.txt` — what the brushes did to the walk: the raise brush's rim is walked, the flank plate's two
  edges are not.
- `painting-a-patch.layout.json` — the one document the board was stored from. It stores with two `SK14`
  complaints and no refusal, which is itself one of the claims.

Renders: `row1-owning.png` — four statements, one patch visible; `row2-ground.png` — the four that own their
paint and what each did to the ground; `section-plates.png` and `section-hole.png` for the geometry;
`iso.png` for all eight.
