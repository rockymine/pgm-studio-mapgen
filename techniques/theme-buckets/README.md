# Theme buckets

A ground theme is five buckets — **bedrock, fill, wall, surface and rim** — and a column is assembled from
them in that order. Ten panels carry the same island solved by the same relief, and only the theme changes:
row 1 switches the buckets on one at a time, row 2 is how a bucket's material is banded. Open it in the
studio as `technique-theme-buckets`, or run `build.py`.

**Each panel is a plain at 8, a swell to 20 and a mesa to 32 whose skirt falls at 4.8 blocks a cell**, so
every one has flat ground, a graded shoulder, a face and a rim against the void — one of each thing a bucket
can claim.

## The document

Ten groups on the `ground` layer, ten themes, one relief per group with the same two pushes. A bucket is
switched off by `enabled: false` on its band, or by `wallEnabled: false`.

| panel | states | what it built |
|---|---|---|
| `fill-only` | surface, wall and rim all off | the rim column is stone from bedrock to top |
| `and-surface` | + a 3-deep `depth` stack, turf over earth | the same column, with grass over two dirt on it |
| `and-wall` | + `wallEnabled`, `wallOnTerrainFaces` | the **body under the soil** is sandstone, not stone |
| `and-rim` | + a 1-deep rim, `rimEdges: "void"` | the top course is nether brick, the wall still under it |
| `rim-boundary` | the same rim at `rimEdges: "boundary"` | **1,110 more cells** capped, every one of them inland |
| `axis-height` | the surface banded on `height`, `from` 8 | snow on the mesa, grass mid-slope, the plain unpainted |
| `axis-slope` | the same three blocks banded on `slope` | grass on every flat, snow on every face, whatever the altitude |
| `axis-inward` | the same three banded on `inward` | a sand border and a gravel ring round the island's edge |
| `fill-rise` | a `cell` fill with a `rise` of 5 | blobs of three stones through the body, read on a cut |
| `wall-run` | a `wallRun` wall of three stripes | stripes wrapping the perimeter, constant up a column |

```json
"and-rim": {
  "bedrock": {"relative": false, "value": 1},
  "rimEdges": "void",
  "rim":     {"enabled": true, "depth": 1, "material": {"kind": "solid", "id": 112}},
  "surface": {"enabled": true, "depth": 3,
              "material": {"kind": "layered", "axis": "depth", "stack": {"ending": "repeat", "bands": [
                 {"thickness": 1, "material": {"kind": "solid", "id": 2}},
                 {"thickness": 2, "material": {"kind": "solid", "id": 3}}]}}},
  "wallEnabled": true, "wallOnTerrainFaces": true,
  "wall": {"kind": "solid", "id": 24},
  "fill": {"kind": "solid", "id": 1}}
```

## The four buckets, switched on one at a time

**One column at the island's rim, read in four panels, is the whole of row 1.** At (−188, −67) with fill
alone it is stone from bedrock to top; at (−110, −67) a surface puts grass over two dirt on it; at
(−32, −67) a wall makes the body under that soil **sandstone**; at (46, −67) a rim caps it with nether brick.
Four panels, four courses of one column, one bucket each.

**So the wall is the column's body at an edge, not a coat on a slope.** It replaces the fill from the bottom
of the surface down, wherever the column stands on a void-facing edge or — with `wallOnTerrainFaces` — on a
terrain face. On this board that is 612 columns, 340 of them round the island's rim and **272 inland**, on
the mesa's own skirt.

**Which means a cliff's strata belong in the wall bucket and are read on a cut.** Nothing of the wall shows
from above, because the surface still caps every column; `section-buckets.png` is where row 1 can be seen
at all, and the isometric is where it cannot.

**`rimEdges` decides how much the rim claims, and the difference is large.** `void` caps only the landmass's
true outside; `boundary` caps every plateau boundary including the mesa's and the swell's, which on this
board is **1,110 further cells**, all of them inland. At (130, −50) the `void` panel reads grass and the
`boundary` panel reads nether brick.

## How a bucket's material is banded

**A band stack takes one of four axes, and three of them are row 2.** `depth` runs down the column and is
what every other panel's soil uses; `height` pins bands to world Y; `inward` runs in from the void-facing
edge; and on `slope` a band's thickness is a **span of degrees** rather than a count of blocks.

**The same three blocks banded on `height` and on `slope` land in different places, and that is the card.**
On `height` the mesa's top at y31 is snow and the swell's at y19 is grass — altitude decides. On `slope` the
mesa's top is **grass** because it is flat, and a cell of its skirt at 74° is **snow** — angle decides, and
the same stack now puts meadow on every flat and bare face on every steep, whatever height they stand at.

**A `height` stack leaves everything under its own `from` to the bucket beneath.** The `axis-height` panel
states `from: 8` and the plain tops at y7, so at (−135, 20) the column reads **stone** — the fill, showing
through where the stack does not start. Nothing reports it.

**`inward` is concentric rings from the edge**, and reads as a border: at (−30, 10), four cells in from the
rim, the column is sand, with a gravel ring behind it and grass inland.

## A pattern on a fill is read on a cut

**A fill is the tall bucket, so a pattern on it is seen edge-on rather than from above.** `fill-rise` states
a `cell` nine across with a `rise` of 5 over three stones, and from above the panel is plain grass — the
whole of it is in `section-fill.png`, where the mesa's cut face is blobs of sandstone, andesite and stone.

**A pattern with no `rise` is refused outright, by `PT4`.** *"fill samples its field in the plane only, so
every block of a column resolves alike and it reads as vertical stripes. A rise is the vertical period that
gives a face its grain."* The board would not store until the `rise` was added.

**A `wallRun` varies along the perimeter arc and is constant up a column** — a sawn cliff rather than a
bedded one. Its three stripes wrap the island's edge and show on the rim in the isometric; a section through
the middle cannot see them, because there is no perimeter there.

## What the theme gate refuses

**`PT1` — a surfacing block may not be a band's whole material.** *"Grass Block surfaces ground and fills
all 3 the surface's courses, because the material is a pick rather than a stack. A surfacing block is exactly
one course thick and what is under it is soil."* So every band of the `height`, `slope` and `inward` stacks
here is itself a little `depth` stack: one course of the surfacing block over two of earth.

**`PT4` — a fill or wall pattern must state a `rise`.** Both refusals are at the store door, not at the
export, and both name the exact JSON path — `themes.axis-height.surface` and `themes.fill-plane.fill.rise`.

## Where the bands cut is read off the board

**`incline.txt` is the first thing to run and the last argument about a band edge.** This board holds 59.7%
of its ground under 10° and 27.8% at 40° or steeper, because its landforms are a sheer mesa and a gentle
swell on a plain — so a slope stack cut at 20 and 45 lands its three bands on three real populations.

**A cut through the angle a board mostly stands at stripes it.** A gentle flank whose grade sits on a band
edge alternates between two blocks row by row, which is the one failure this card's own siblings each hit:
`marks-and-pushes` cuts at 25 and 45, `made-ground` the same, `water` at 35 and 55, and the flat-ground cards
at 15 and 40 — four different boards, four different histograms, four different cuts.

**So the number is never remembered, it is read.** `GET …/incline?format=text` before the theme is written,
and again after the relief changes.

## The recipe

**Write the buckets from the bottom up and give each one a job.**

```json
{"bedrock": {"relative": false, "value": 1},
 "fill":    "<the body: a solid, or a pattern with a rise>",
 "wall":    "<the strata a cut shows>", "wallEnabled": true, "wallOnTerrainFaces": true,
 "surface": {"enabled": true, "depth": 3, "material": "<a stack on the axis the board wants>"},
 "rim":     {"enabled": true, "depth": 1, "material": "<the cap>"},
 "rimEdges": "void"}
```

- **the surface is what you see from above; the wall and the fill are what a cut shows.**
- **every band of a `height`, `slope` or `inward` stack is a `depth` stack** — `PT1` refuses a bare
  surfacing block.
- **a `height` stack's `from` leaves the ground under it to the fill.**
- **a pattern on the fill needs a `rise`**, and cells wider than tall, or a cut reads as posts.
- **`rimEdges: "void"` caps the landmass; `"boundary"` caps every plateau in it** — on this board, 1,110
  more cells.
- **cut the slope bands against `incline`**, never against a number from another board.

## What checks it

- `columns.txt` — eleven columns: the same rim column in the four additive panels, an inland cell `void`
  leaves and `boundary` caps, the mesa top and the plain on `height`, the mesa top and its skirt on `slope`,
  the border on `inward`, and a blob inside the `fill-rise` mesa.
- `census.txt` — ten themes over 38,400 cells and six distinct surface blocks.
- `incline.txt` — the histogram the slope bands were cut against.
- `theme-buckets.layout.json` — the one document the board was stored from. It would not store until `PT1`
  and `PT4` were satisfied, which is two of this card's claims.

Renders: `section-buckets.png` — row 1 cut through the mesa, which is the only view a wall or a fill appears
in; `axes-row.png` — row 2 from above, which is the only view a surface axis appears in; `section-fill.png`
for the fill's blobs, and `iso.png` for all ten.
