# Relief on shapes

A relief shapes the ground a group's shapes build, and a shape can stay out of it. Three shapes make a
small place: a raised `works` yard, an upland meadow beside it and a lowland meadow below both. The card
holds the place three times, side by side.

**In `stepped` the relief smooths the two meadows into one slope** and runs up against the yard on two sides
without moving it.

**`level` draws both meadows at one height**, and the same relief builds it alike, block for block.

**`held` keeps the upland at the height it was drawn at** and leaves the yard's faces whole, spending the
relief only on the grade from the lowland up to the upland.

Open it in the studio as `technique-relief-on-shapes`, or read `relief-on-shapes.layout.json`.

## The document

Three groups on the `ground` layer, each with `mirrors: false`, on a board whose `setup.mirror_mode` is `none`.
Any other mode folds the relief across the centre, a group's `mirrors: false` does not change that, and a layout
stating no `mirror_mode` takes `rot_180`. `level` is `stepped` moved 64 blocks east and `held` is `stepped` moved
128; their shapes carry a `-level` and a `-held` suffix.

| Shape | Where, in `stepped` | `base_height` | Paint | Relief |
|---|---|---|---|---|
| `works` | x −48–−32, z −32–0 | 18 in all three | `theme: "works"` | `relief_scope: "exclude"` in all three |
| `upland` | x −32–0, z −32–0 | 13, and 9 in `level` | the map default, `meadow` | solved, and `relief_scope: "hold"` in `held` |
| `lowland` | x −48–0, z 0–16 | 9 in all three | the map default, `meadow` | solved in all three |

`stepped` and `level` carry the same relief, keyed by the group's id; `level`'s states every x 64 blocks further
east:

```json
"relief": {"stepped": {
  "base": 11, "reach": 0, "step": 1,
  "marks": [
    {"id": "upland-bench", "kind": "area", "h": 13, "bevel": 2,
     "ring": [[-28, -26], [-20, -30], [-8, -29], [-3, -22], [-4, -12], [-10, -7], [-22, -8], [-28, -14]]},
    {"id": "lowland-bench", "kind": "area", "h": 9, "bevel": 2,
     "ring": [[-46, 8], [-38, 5], [-20, 6], [-6, 5], [-2, 10], [-8, 15], [-26, 14], [-44, 15]]}],
  "pushes": [
    {"id": "knoll", "ring": [[-32, -32], [-21, -32], [-18, -25], [-22, -18], [-32, -19]],
     "amount": 1, "falloff": 3, "crown": 3.5, "roughness": 0, "seed": 1}]}}
```

Each `area` mark holds the middle of one meadow at its own height, and its `bevel` softens the edge. The ground
between the two benches is pinned by nothing, so the solve grades it — that free band is the connection. The
`knoll` push lifts the upland's corner against the yard's east face. The relief states no `grain`.

`held` carries the lowland bench alone, with no upland bench and no push:

```json
"held": {"base": 11, "reach": 0, "step": 1,
  "marks": [
    {"id": "lowland-bench", "kind": "area", "h": 9, "bevel": 2,
     "ring": [[82, 8], [90, 5], [108, 6], [122, 5], [126, 10], [120, 15], [102, 14], [84, 15]]}]}
```

## What the relief does to the meadows

As drawn, `stepped`'s meadows meet at z 0 on a wall four blocks tall: top y12 over y8. With the relief, the same
line along x −16 steps down a block at a time from z −8 to z 6, and walks end to end. The grade is spread across
both meadows, because both are solved.

## The meadows can be drawn at one height

As drawn, `level`'s two meadows are one flat field at y8. With the relief, its line along x 48 reads exactly what
`stepped`'s reads along x −16, and every one of `stepped`'s 2,304 columns has the same top as the column 64
blocks east of it: none differ. A relief replaces the top of every column it solves, and the heights it solves
come from its marks and pushes, so a solved shape's own `base_height` decides nothing about where the ground
ends up. Drawing the meadows at one height is enough; the excluded yard is the one shape whose height is its
own.

## The relief can grade only between the meadows

`held` keeps two drawn heights and lets the relief make only the join. The yard is excluded, as in the other two
plots. The upland is marked `hold`, which leaves its cells in the solve but pins them at the height the shape
states, so the ground around it is solved knowing where it has to arrive. Only the lowland is free, and the one
bench keeps its middle at 9.

Along x 112 the upland's top is y12 from z −31 to −1, flat at the height it was drawn at. The lowland climbs to
meet it: y12 at z 0, then y11, y10 and y9 two blocks each, and y8 from z 7. The line walks end to end, a block at
a time. The grade sits wholly in the lowland, which is the difference from `stepped`, where it runs from z −8.

The yard keeps every face. Nothing pushes against it, so its east face stands the five blocks it was drawn with
over the upland — a transect along z −26 drops from 18 to 13 at x 96 — and its south face stands eight over the
lowland, which is y9 against the face at (88, 0) and y8 a block out.

`exclude` on the upland would not make the join. An excluded shape is a hole in the solve, the relief bends
round its edge as it bends round the void, and nothing climbs to meet it: built that way, the lowland along
x 112 stays y8 from z 0, under the same four-block wall the plot was drawn with. `hold` is the word for a shape
that keeps its height and is still arrived at.

## What exclude does to the yard

The yard's cells are out of the solve, so the relief bends round the yard as it bends round the void, and the
yard keeps its top at y17 across its whole width in all three plots. On `stepped` the relief's ground meets it on
two sides at two different heights, and neither moves it. In transect heights, which stand one above the top
block:

- along z −26 the knoll climbs to 16 against the east face, two below the yard's 18;
- along x −40 the lowland stays at 9 right up to the south face, a drop of 9.

The walls this leaves are the yard's own faces, painted with its stripes. The slopes read counts one face per
plot, and each is its yard's edge; the largest, 95 cells at x 80–96, z −32–0, is `held`'s, whose east face nothing
lifts ground against.

## What the relief read says

`POST /api/map/technique-relief-on-shapes/sketch/relief/read` with the layout answers the same for `stepped` and
`level`: the meadows' 1,792 cells run from 9 to 17, with no seams, no silent marks, no cliffs, no complaint and a
symmetry error of 0. The knoll's two gradients agree — 0.33 blocks a block up its skirt (`amount / falloff`) and
0.31 to its crown — and a push whose two disagree steps at its own outline and raises `RL6`. `held` counts the
same 1,792 cells, held ones included, running from 9 to 13, with nothing to complain of either.

## The one mistake

A made shape with no `relief_scope` joins the solve. The same layout built without it gives the yard's top along
z −16 at y11 instead of y17: the relief replaces the height the yard was drawn at.

## What checks it

- `compare.txt` — `stepped` and `level` as drawn and with the relief, the column-by-column count between them,
  `held`'s join along x 112 as drawn, with `hold` and with `exclude` instead, the held upland's own top, and the
  yard with and without `relief_scope`.
- `transects.txt` — upland to lowland on all three plots (x −16, x 48 and x 112), yard to upland along z −26 on
  `stepped` and on `held`, yard to lowland along x −40 and x 88.
- `relief-read.json` — the relief read above, one group each.
- `columns.txt` — each plot's yard, upland, seam and lowland, and the yard faces.
- `slopes.txt` — 6,651 cells walked, 8 scrambled, 253 barrier, and three faces, one per yard.
- `heightmap.txt` and `census.txt` — `works` on 1,536 cells and `meadow` on 5,376.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
