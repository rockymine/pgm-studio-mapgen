# Tunnels

A tunnel is a **flat base, two walls and a top layer**, and the reason it takes three of them is that a sketch
layer holds one span per column. The floor a player stands on and the ceiling over their head are two spans in
one column, so they cannot share a layer at any thickness — and the rock between them is a third. The card
holds five plots, each one the same four pieces arranged differently. Open it in the studio as
`technique-tunnels`, or read `tunnels.layout.json`.

Every plot is its own group on every layer it draws on, `mirrors: false`, on a board whose `mirror_mode` is
`none`. The bore's floor and the deck over it are stone brick, the rock either side is cobblestone, and the
top layer paints with `meadow` — grass over two dirt over stone — so the same section shows where the built
part stops and the ground begins.

## The four pieces

| Piece | Layer | Where it stands | What it is |
|---|---|---|---|
| base | `base` | `floor` 0, 4 thick — y0–y3 | the floor of the bore; its top block, y3, is what is walked on |
| two walls | `walls` | `floor` 4, 4 thick — y4–y7 | the rock either side. **The bore is where they are not drawn** |
| top layer | `lid` | `floor` 8, 4 thick — y8–y11 | the ceiling, and the board's own surface over it |
| — | `walls-2`, `lid-2` | `floor` 12 and 16 | the same two again, where a plot stacks a second bore |

Every layer is at `base_y` 0 and every shape states its `floor` absolutely, so a span reads straight off the
document: `floor` 8 and `base_height` 4 is y8 to y11. The bore that leaves is four courses of air — y4 to y7 —
five blocks wide, and it is not stated anywhere. **Nothing draws a tunnel: the tunnel is the columns the walls
layer left alone.**

```json
{ "id": "an-base",   "floor": 0, "base_height": 4, "min_x":  0, "max_x": 24, "min_z": 0, "max_z": 40 }
{ "id": "an-wall-w", "floor": 4, "base_height": 4, "min_x":  0, "max_x": 10, "min_z": 0, "max_z": 40 }
{ "id": "an-wall-e", "floor": 4, "base_height": 4, "min_x": 15, "max_x": 24, "min_z": 0, "max_z": 40 }
{ "id": "an-lid",    "floor": 8, "base_height": 4, "min_x":  0, "max_x": 24, "min_z": 0, "max_z": 40 }
```

A rectangle's bounds are **half-open** — `min_x` 0 to `max_x` 10 covers x0 to x9 — so those two walls leave
x10 to x14 open, and the column at (12, 20) reads brick to y3, air to y7, then the lid.

## The five plots

| Plot | Where | The bore | What it adds |
|---|---|---|---|
| `anatomy` | x 0–24, z 0–40 | x10–14, along z | the four pieces and nothing else |
| `corner` | x 34–58, z 0–40 | in at x44–48, out at z21–25 | the walls layer as the complement of an **L** |
| `levels` | x 68–92, z 0–40 | x78–82, climbing four courses | a ramped floor under a **stepped** ceiling |
| `crossing` | x 0–24, z 50–90 | x10–14 and z68–72, at one level | four rock blocks round a junction |
| `storeys` | x 34–58, z 50–90 | z66–70 low, x44–48 high | two bores over one another, and the deck that is both |

## A corner is the rock, not the bore

The bore turns; the walls do not become an L-shaped shape with a bend in it. What is stated is the **rock
around the turn**, and on a rectangular plot that is three rectangles:

```json
{ "id": "co-rock-w",  "min_x": 34, "min_z":  0, "max_x": 44, "max_z": 40 }
{ "id": "co-rock-ne", "min_x": 49, "min_z":  0, "max_x": 58, "max_z": 21 }
{ "id": "co-rock-s",  "min_x": 44, "min_z": 26, "max_x": 58, "max_z": 40 }
```

The three tile the plot exactly, minus the L that is left. The general form is to split the plot into z-bands
at every edge of the bore, split each band in x, and drop the parts that fall inside it.

**It is banded rather than cut because a subtract is a claim about the whole stack.** Writing the plot as one
rock rectangle with the bore taken out of it with `operation: "subtract"` states that those columns are the
board's negative space, and `SK13` refuses any add that holds a course with it — on any layer, because a
subtract's courses are compared absolutely across the stack rather than within the layer it is drawn on. A
board with no subtract anywhere in it has nothing to get wrong there, which is what the complement buys.

The subtract form is not forbidden, and the last section of this card measures the one shape of it `SK13`
allows.

## A floor can ramp; a ceiling is one rectangle a course

`levels` climbs four courses in the middle of its run and holds four of headroom the whole way. Those are two
different statements, because a shape's top can slope and **its floor cannot**: `anchor_heights` is a
thickness per vertex, and `floor` is one number.

So the floor is one polygon —

```json
{ "id": "le-ramp", "type": "polygon", "floor": 0,
  "vertices":       [[78, 22], [83, 22], [83, 26], [78, 26]],
  "anchor_heights": [4.5, 4.5, 8.5, 8.5] }
```

— and the ceiling is four rectangles, each a block deep and a course higher than the last:

```json
{ "id": "le-lid-s1", "floor":  9, "base_height": 4, "min_z": 22, "max_z": 23 }
{ "id": "le-lid-s2", "floor": 10, "base_height": 4, "min_z": 23, "max_z": 24 }
{ "id": "le-lid-s3", "floor": 11, "base_height": 4, "min_z": 24, "max_z": 25 }
{ "id": "le-lid-s4", "floor": 12, "base_height": 4, "min_z": 25, "max_z": 26 }
```

Measured up the bore at x 80, the two rise together:

```
z            21   22   23   24   25   26
floor, top    3    4    5    6    7    7
ceiling      y8   y9  y10  y11  y12  y12
headroom      4    4    4    4    4    4
```

**What makes the flight even is that its anchors differ by its own run.** Every block reads the shape's
surface at its own centre and floors it, so a rise of four thicknesses over four cells lands one course a
block and nothing else does. Measured, the same four-cell polygon over ground at y3:

| anchors | rise / run | tops, z21–z25 |
|---|---|---|
| `[4.5, 4.5, 8.5, 8.5]` | 4 / 4 | 3, 4, 5, 6, 7 |
| `[4, 4, 8, 8]` | 4 / 4 | 3, 4, 5, 6, 7 |
| `[4, 4, 7, 7]` | 3 / 4 | 3, **3**, 4, 5, 6 — a repeat at the foot, and it arrives a course low |
| `[4.5, 4.5, 10.5, 10.5]` | 6 / 4 | 3, 4, **6**, 7, **9** — two-block steps |

At one course a block the half-block offset makes no difference, because flooring absorbs it; `4.5` is the
habit rather than the requirement. At every other gradient it is the requirement, and
`techniques/ramp-and-stair` is where that is measured — a two-deep stair on whole-number anchors builds
treads one, two and three blocks deep.

The two ramped wall polygons either side of the bore state the same rise over the same run one layer up:
`floor` 8, anchors `[0.5, 0.5, 4.5, 4.5]`, so the rock tops out at y8, y9, y10, y11 and meets each lid step
with no course shared and none missed.

## Two bores in one column

`storeys` crosses one bore over another without either meeting the other: the lower runs east–west under
z66–70, the upper north–south over x44–48. Where they cross, the column carries **three spans**:

```
GET …/column?at=46,68
  y 19–16   Grass, Dirt, Dirt, Stone   the lid-2 layer — the board's surface
  y 15–12                              the upper bore
  y 11–8    Stone Bricks               the lid layer — the deck
  y  7–4                               the lower bore
  y  3–0    Stone Bricks, Bedrock      the base layer
```

**The deck is one shape doing two jobs**: it is the lower bore's ceiling and the upper bore's floor, and there
is no second shape for the second job. That is the whole reason a stack is drawn as layers rather than as
storeys — the boundary between two storeys is one span, and a span belongs to one layer.

## What it complains about, and what it leaves standing

The card stores and finishes at **200**, carrying four `SK11` complaints — one per plot whose roof is a
landmass with no way onto it:

```
SK11  960 place(s) of standable ground around (34, 0) @13 have open sky over them and no route
      onto them from the rest of the board — draw the way up, or leave it if a detached group is
      what this is
```

960 is 24 × 40, the whole lid of a plot. The complaint is right and the card leaves it standing: this board
states bores and nothing else, and a way onto a roof is the subject of `tunnel-mouths`, where three of the
four plots raise nothing at all. Four of the five roofs here are named and `anatomy`'s is not — the rule
reports the masses *no route reaches from the rest of the board*, and one of five identical detached roofs is
the rest.

**`SK10`** is the complaint beside it, and it is about the other direction: two layers driven into each other
by more than the one course a seam shares. A layer's span is inclusive of its top, so a ceiling whose `floor`
is the wall's own top course is the ordinary seam; one course lower is the finding, and the gap the layers
were drawn to have is not in the world there.

**A group id is unique across the whole board, not per layer** (`SK12`). A plot that draws on three layers
owns three groups, so each one is named for its layer: `anatomy-base`, `anatomy-walls`, `anatomy-lid`.

## The one mistake: the four pieces on one layer

Drawing `anatomy`'s four shapes on a single layer is the obvious document, and it is not refused. It stores at
**200** and it finishes at **200** — and there is no tunnel, no walls and no floor. Five `SK9`
declines say so, at the severity that means *a piece of what you posted is not in the world*:

```
[decline] SK9  'base' and 'lid' stack over the same ground on layer 'one', and a layer holds one span
               per column — the world keeps 'lid' and 'base' is not in it. Move 'lid' to its own layer,
               or clamp walls around the lower shape rather than drawing over it
```

The section is the whole story — the lid, hanging at y8 to y11 over nothing at all, with the base, both walls
and even the bedrock course gone:

```
y 12   ...........................
       ########################...
       ########################...
       ########################...
y  8   ########################...
       ...........................
```

**A decline arrives on a 200 and the status code is half the answer.** Nothing about that board refuses: the
heightmap is a flat green square either way, and the only things that say a four-shape tunnel came out as one
slab are the `warnings` array and a section nobody had a reason to take.

## The form with a subtract in it

`SK13` blesses exactly one: *a mass, a subtract stating the void inside it, and an add either side of that
void* — the floor's top at or below the subtract's floor, the ceiling's floor at or above the subtract's top.
The courses are compared absolutely, so the two adds may be on any layer. Measured against `anatomy`, one
rock rectangle over the whole plot with the bore cut out of it —

```json
{ "id": "mass", "operation": "add",      "floor": 4, "base_height": 4, "min_x": 0,  "max_x": 24 }
{ "id": "cut",  "operation": "subtract", "floor": 4, "base_height": 4, "min_x": 10, "max_x": 15 }
```

— stores and finishes at **200** with no complaint, and sections identically to the three banded walls. Take
the base from four courses to six, so its top stands inside the void, and the same document is **422**:

```
SK13  'base' fills 200 column(s) that 'cut' takes away — from (10, 0) — so the negative space the
      board states there is ground in the world. 'base' is on layer 'base' and the subtract on
      'rock', and a subtract reaches only the layer it is on
```

The subtract buys nothing on a rectangular plot — one rectangle and one subtract against three rectangles —
and it buys a great deal on a bore with several turns in it, where the complement is a dozen bands. What it
never does is let the floor and the ceiling share a layer: that is `SK9`, and it is a different rule.

## What checks it

- `voids.txt` — the covered-space scan over the built world: **six roofed voids, none sealed**, each with the
  blocks it lies between. It is the read that says a tunnel is a tunnel; a bore that came out solid is not in
  it, and one nothing can walk into is `SEALED`.
- `walks.txt` — every bore walked end to end, `from=x,z,y` with the `y` naming the storey. All seven answer
  `worst step 0`, `levels` included: a one-course rise costs a walk nothing, so the climb reads as level
  ground that happens to arrive four blocks higher.
- `columns.txt` — the anatomy across the bore, the `levels` climb course by course, and (46, 68), the column
  with two bores in it.
- `section.txt` — eight cuts, two per plot. A tunnel is invisible from above and obvious in a section.

Renders: `iso.png` (south-east) and `iso-turned.png` (south-west); `xray.png`, the only view a bore appears in
at all; and `layers.png`, one isometric per layer, which is the picture of the decomposition — every base,
every wall, every lid, side by side with its block count.
