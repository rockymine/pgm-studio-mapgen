# Polylines

A polyline is a line with a width: its points are a centreline, and the band `radius` blocks to each side of it
is ground. Every shape here is on the `ground` layer, `base_height: 9`, painted with the same `meadow` theme as
`flat-ground`, and each row is a group of its own with `mirrors: false`, on a board whose `mirror_mode` is `none`. Open it in the studio as
`technique-polylines`, or read `polylines.layout.json`.

| Row | Shapes | Where | What it shows |
|---|---|---|---|
| edges | `line-solid`, `line-rough`, `line-tapered` | z 0–20, from x 0, 50 and 100 | one S-curve of four points, `radius` 3, once in each `stroke_edge` |
| bridge | `bridge-west`, `bridge`, `bridge-east` | z 34–54 | a polyline 4 wide whose ends lie inside two islands, joining them into one |
| rise | `rise-low`, `rise`, `rise-high` | z 74–94 | a polyline with `anchor_heights` `[9, 12, 14, 17]`, climbing from ground at y8 to ground at y16 |
| yard | `yard`, `wall` | z 110–130 | a polyline of `radius` 1, 13 thick, in stone brick, standing on its island as a wall 4 courses tall |

## How a polyline becomes ground

The points are smoothed first — a centripetal Catmull-Rom spline, eight samples between each pair — and only then
offset `radius` blocks to either side, so four points draw a curve rather than three chords. The ends are cut
square. `stroke_edge` decides the band's two long edges: `solid` keeps one width, `rough` lets it swing up to 45%
either way with the two sides wandering apart (`stroke_seed` picks the wander), and `tapered` narrows it to 35%
at the ends. `anchor_heights` on a polyline are heights at its points, and every block takes the height of the
nearest place along the line.

On one layer the taller shape takes the whole column, so the `wall`'s columns are its own from the bottom up:
at (4, 114) the column is stone brick from y1 to y12, with no grass or dirt of the yard's under it.

A polyline shape is ground. The `stroke` prop, which looks alike, repaints the top course of what it crosses and
adds no ground.

## The one mistake

A band that turns tighter than it is wide laps itself, and the lap is lost. The band is one outline filled
even-odd, so where its two sides cross they cancel and build void, and the studio names it `SK25`. Four points
across 26 blocks at `radius` 3 lap in every bend; the same four points spread over 40 blocks clear. A coil is
drawn as one polyline per part-turn.

## What checks it

- `heightmap.txt` — every band from above, two blocks to a character.
- `walks.txt` — across the bridge and up the rise: 67 blocks each, nothing placed, worst step 0.
- `column-wall.txt` — the wall's column at (4, 114).
- `census.txt` — `meadow` on every ground cell.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
