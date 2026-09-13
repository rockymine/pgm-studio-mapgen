# Flat ground

Single islands of ground and their outlines: a 20 × 20 rectangle, the same island with its corners cut one at
a time, and the cut islands tilted. Each island is one shape on the `ground` layer, in a group of its own with
`mirrors: false`, on a board whose `mirror_mode` is `none`, standing over the void. Open it in the studio as `technique-flat-ground`, or read
`flat-ground.layout.json`.

## The ground

Every island is `base_height: 9` and paints with the map's default theme `meadow`: grass 1 and dirt 2 as a
`layered` surface 3 deep, stone for the wall and the fill, one course of bedrock, no rim. The wall starts under
the surface band, so it is plain stone — given the surface's own stack it paints a second grass course partway
down the face. **`base_height: 9` puts the top block at y8, not y9.**

## The islands

| Island | Where | Outline |
|---|---|---|
| `island-rect` | x 0–20, z 0–20 | a `rectangle`, stated by `min_x`, `min_z`, `max_x`, `max_z` |
| `island-one-cut` | x 0–20, z 28–48 | a 5-point polygon: one corner cut off, three of the rectangle's corners kept |
| `island-two-cuts` | x 0–20, z 56–76 | 6 points: a second corner cut off |
| `island-ramp` | x 28–48, z 28–48 | the 5-point outline with thicknesses `[9, 9, 15, 19, 19]` — set at two vertices, it rises along z |
| `island-tilt` | x 28–48, z 56–76 | the 6-point outline with thicknesses `[9, 12, 16, 17, 17, 14]` — set at three vertices, it rises along x and z |

## Targeting a vertex

A polygon's `vertices` are a ring, and a point's index is its place in that list, counted from 0. A rectangle
states bounds rather than points, so it is restated as a four-point polygon before any point can move. Three
routes change one point and leave every other exactly where it was drawn:

- `PATCH /api/map/{slug}/sketch/shapes/{id}/vertices/{index}` with `{x, z}` moves that point.
- `POST /api/map/{slug}/sketch/shapes/{id}/vertices` with `{after, x, z}` adds a point on the edge leaving
  vertex `after`. It lands at `after + 1`, every later index goes up by one, and the answer says where it landed.
- `DELETE /api/map/{slug}/sketch/shapes/{id}/vertices/{index}` removes one, down to three.

Cutting a corner is one move and one insert. `island-one-cut` starts as `[[0,28],[20,28],[20,48],[0,48]]`: move
vertex 2 from (20, 48) to (20, 40), then add (12, 48) after vertex 2. The second cut on `island-two-cuts` moves
vertex 1 to (20, 64) and adds (12, 56) after vertex 0, which pushes the first cut's two points from indices 2
and 3 to 3 and 4. `vertex-edits.txt` holds every call and its answer.

`anchor_heights` is one thickness per vertex, in the same ring order, set with
`PATCH /api/map/{slug}/sketch/shapes/{id}`. The studio's slope tool asks for two or three vertices and fills in
the rest from the line or the plane through them, in whole blocks. Both tilted islands end at a drop over the
void, which the studio names `SK26`.

## What checks it

- `column.txt` and `column-edge.txt` — grass y8, dirt y7–6, stone y5–1, bedrock y0, at (10, 10) and on the face at (0, 10).
- `census.txt` — `meadow` on all 1,784 cells.
- `tilt-tops.txt` — the top block of every column of the two tilted islands.
- `section.txt` — cuts along z at x 10 and x 38, and along x at z 66.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
