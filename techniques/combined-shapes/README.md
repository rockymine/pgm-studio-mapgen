# Combined shapes

Four shapes combined into one island, twice: once all at one height, once at four. Two themes paint them —
`meadow`, the grass ground of `flat-ground`, and `works`, a built one. Open it in the studio as
`technique-combined-shapes`, or read `combined-shapes.layout.json`.

Both islands are the same arrangement on the `ground` layer, each in one group with `mirrors: false`, on a board whose `mirror_mode` is `none`. The flat
island's shapes are named `flat-…` and start at x 0; the stepped island's are `step-…` and start at x 70.

| Shape | Kind | Theme | Flat | Stepped |
|---|---|---|---|---|
| `meadow` | rectangle 30 × 40 | the map default, `meadow` | 9 | 9, top y8 |
| `spur` | a 4-point polygon abutting the meadow's west edge | the map default | 9 | 7, top y6 |
| `yard` | rectangle 26 × 24, overlapping the meadow's east edge by 8 | `works` | 9 | 13, top y12 |
| `green` | a circle of radius 6 inside the yard | `meadow`, stated on the shape | 9 | 15, top y14 |

`works` states a surface of smooth andesite 1 deep, a stone brick rim 1 deep where its ground drops — over the
void as well as over lower ground — a wall striped stone brick 1, cyan stained clay 1, smooth andesite 2, and
stone for the fill. A band stack does not cycle: past its last band, `"ending": "repeat"` hands every further
course to that last band, so the four-course run is written out four times to stripe a face 16 courses tall.

## How shapes combine

Shapes in one group whose ground touches or overlaps build one island, and the store answers `islands: 2`.

**The height and the paint of an overlap are decided separately.** Where two shapes cover a cell, the taller
one gives the column its height, and the paint goes to the smallest themed shape whose top is that tallest
top.

**So the two answers come apart on the flat island and together on the stepped one.** On the flat island the
yard is the smaller of the two, so it paints the 8 blocks it shares with the meadow — andesite at (26, 12) —
and the lawn, smaller again, paints the middle of the yard with grass. On the stepped island the yard is
also the taller, so it holds both.

A face shows wherever a shape stands higher than the ground beside it, and the face is what the wall bucket
paints. The flat yard is andesite over plain stone inside, and striped only on its faces over the void. The
stepped yard's west face at (92, 12) reads, from the top: the stone brick rim at y12, stone brick y11, cyan clay
y10, andesite y9 — only the courses standing above the meadow's top at y8 are face.

## The one mistake

A lower shape drawn inside a higher one on the same layer is not in the world: the taller shape takes the whole
column, and the studio names it `SK9`. That is why the lawn is raised above the yard rather than sunk into it. A
sunken place inside a raised one is drawn as shapes around it, or on a layer of its own.

## What checks it

- `columns.txt` — both yards, both lawns, the overlap at (26, 12), the terrace face at (92, 12), the stepped
  meadow, both spurs, and both yards' faces over the void at (117, 20) and (47, 20).
- `census.txt` — `meadow` 2,692 cells (72.6%) and `works` 1,016 (27.4%), bordering over 176 cells.
- `heightmap.txt` — the stepped island's four heights beside the flat island's one.
- `section.txt` — the cut along x at z 20 through both islands.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
