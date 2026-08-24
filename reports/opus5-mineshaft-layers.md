# Opus 5 — Mineshaft: the smallest board that is genuinely two storeys

## What it is for

A worked example, not a playable map. `opus5-undercroft` raised the question of what a stack of
layers actually does; this board is the minimum geometry that answers it — a gallery running under a
meadow, an adit climbing out of its east end — built so that every claim on the studio's layer track
can be measured against one file instead of a paragraph.

`maps/opus5-mineshaft`, `specs/opus5-mineshaft/`.

## What it is

Eighty blocks square, two layers, six shapes, no relief and no dressing.

The **mine level** (`base_y 0`) is four wall rectangles **clamped around** a tucked-in gallery floor —
`wall-n`, `wall-s`, `wall-w`, `wall-e` at `floor 0` `base_height 20`, and `gallery` at `floor 0`
`base_height 4` in the channel they leave (x −30..24, z −6..6). A `ramp` polygon over x 0..24 carries
`anchor_heights [4, 26, 26, 4]`, climbing the gallery floor to meadow height.

The **meadow** (`base_y 20`) is one `deck` rectangle over the whole board at `base_height 6`, with a
`mouth` subtracted where the adit breaks the surface (x 14..24, z −6..6).

Read back off `POST …/sketch/columns`, a column is:

| where | segments | stands at |
|---|---|---|
| gallery, x −30..0 | `[0,3]` · `[20,25]` | 4 below, 26 above — sixteen blocks of air between |
| adit under the deck, x 13 | `[0,15]` · `[20,25]` | 16 below, 26 above |
| adit at the mouth, x 14..24 | `[0,16]` … `[0,25]` | one mass, open to the sky |
| meadow, everywhere else | `[0,25]` | 26 |

The road from the gallery floor to the meadow rises 4 → 26 across twenty-four cells with **no step
over one block**, so it is walkable at `Walk.FreeRise`.

## The clamp is the whole trick

A layer is a slab: one `(Top, Floor)` per cell, and a taller add replaces it outright, floor included.
So a roofed gallery is **not** a low shape drawn inside a tall one — draw the walls as one rectangle
over the whole board and the gallery floor inside it and the gallery is swallowed, because the taller
add wins the cell. Four wall shapes *around* a channel leaves the channel for the floor shape to claim,
and the roof goes on the layer above.

Two variants were built and measured against this one.

A `subtract`-and-`override` recipe — one wall mass, the channel carved out, the ramp put back as an
override — produces the **identical** geometry. It works because the set algebra is
`((adds − subs) ∪ override-adds) − override-subs` **by category rather than document order**, but it
is a workaround for a drawing mistake and is not needed.

Both shapes on **one** layer at two floors does not build at all: 480 cells, 0 stacked, every column
`[16,22)`, in both draw orders. The lower shape is erased and **nothing is raised** — no finding, no
complaint, a board that reads as authored. That silence is the reason the studio's board now carries
`TS27`.

## What the reads say about it, and where they are wrong

The export gate passes cleanly — round-trip, mirror, buildability and traversability all green,
`export gate OPEN`. Two of those pass for the wrong reason.

`GET …/walk?from=0,30&to=0,-30`, spawn to spawn across the middle, answers **reachable, distance 60,
blocks 21, drops 1, worstDrop 22**. The route runs dead straight along x = 0 — over the meadow, across
the gallery, out the far side. It is not a route: the standing surface flips from the deck at 26 to the
mine floor at 4 where the gallery begins, because the walk stands a player on the **lowest** surface in
a column carrying headroom, and a twenty-two block fall is scored as a drop on one continuous surface
rather than as two storeys with no way between them. Preflight's traversability check calls the same
chain connected. Both are `TS21`.

`render/topdown` draws the meadow and nothing else, because the deck roofs all 6,400 cells. The only
cut a caller has is `ymax`, and `renders/topdown-mine.png` is that cut at 19 — it shows the gallery and
the wool room, and it **also shows both spawn cubes**, which stand on the meadow at 26 and have no
business in a picture of the mine. Provenance keys a claim `(X, Z)` with no Y, so the structure layer
is drawn whole whatever the cut says. That is `WS12` and the second half of `TS22`.

`renders/section-z0.png` is the one honest picture: the vertical cut at z = 0 shows the meadow slab,
the void under it, the wool room standing on the gallery floor, and the adit climbing out to the right.

## The renders

| File | Is |
|---|---|
| `topdown.png` | the meadow, which is all a top-down read can see |
| `topdown-mine.png` | `ymax=19` — the gallery, and the two spawn cubes that should not be in it |
| `section-z0.png` | the cut at z = 0: slab, void, floor, adit |
| `heightmap.png` · `surface.png` | elevation and paint, both of the deck only |
| `traversability.png` | one component, which is true of the columns and false of the board |

## Not a map

Two teams, two wools at the west end of the gallery, spawns on the meadow north and south. They exist
so the export gate has something to check and so the section has a structure in it. The board has no
symmetry worth the name, no cover, no second route and a twenty-two block drop where the meadow meets
the gallery. It is a fixture.
