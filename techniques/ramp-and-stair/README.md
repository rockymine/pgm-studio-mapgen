# Ramp and stair

Five ways up the same eight blocks, side by side, each ending on a platform. Open it in the studio as
`technique-ramp-and-stair`, or read `ramp-and-stair.layout.json`.

The ground is one rectangle on the `ground` layer, 9 thick, so its top block is y8. Every flight and platform
stands on the `flights` layer at `base_y` 9, so a shape `N` thick tops out at y `8 + N`. Each lane is its own
group with `mirrors: false`, on a board whose `mirror_mode` is `none`. The ground paints with the same `meadow` theme as `flat-ground`, grass over dirt
over stone, and every flight and platform with one `material`: stone brick for the flights, planks for the
platforms.

| Lane | Shapes | Treads | Built with |
|---|---|---|---|
| ramp | `ramp`, `ramp-top` | 7, each 1 deep and 1 high | one polygon, `anchor_heights` `[1, 1, 7, 7]` over 7 blocks |
| stair | `stair`, `stair-top` | 7, each 2 deep and 1 high | one polygon, `anchor_heights` `[0.5, 0.5, 7.5, 7.5]` over 14 blocks |
| turned | `turn-lower`, `turn-landing`, `turn-upper`, `turn-top` | 4 up, a landing 4 deep, 2 back the other way | two polygons with half-block anchors, a rectangle between them |
| steps | `steps-1` … `steps-7`, `steps-top` | 7, each 2 deep and 1 high | one rectangle per tread, `base_height` 1 … 7 |
| floating | `float-1` … `float-7`, `float-top` | 7, each 2 deep and 1 high | one two-course slab per tread, raised with `floor` 0 … 5 |

## The one mistake

`anchor_heights` are heights at a polygon's corners, and every block reads the slope at its own centre and
rounds. A flight therefore comes out even only when the anchors sit half a riser past its first and last
tread: a 2-deep stair whose treads are 1 to 7 states 0.5 and 7.5. Whole-number anchors 8 and 1 over 16 blocks
build treads 1, 2 and 3 deep. The ramp works with whole numbers because one block up per block rounds cleanly.

The studio's canvas rounds anchor heights to whole blocks, so the half-block form can only be written into the
document. To draw an even stair by hand, use one rectangle per tread, as `steps` and `floating` do.

## What checks it

- `section.txt` — the studio's cut along each lane, one character a block.
- `GET /api/map/technique-ramp-and-stair/walk?from=26,-6&to=30,0&aim=reach&format=text` — the turned stair:
  24 blocks, 0 placed, worst step 0. Each other lane answers the same from `(x, -6)` to its platform.
- `POST /api/map/technique-ramp-and-stair/sketch/columns` with the layout — the top block along x 3, 15, 26,
  30, 41 and 53 is the tread list above.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west).
