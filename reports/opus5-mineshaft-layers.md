# Opus 5 — Mineshaft: the smallest board that is genuinely two storeys

## What it is for

A worked example, not a playable map. `opus5-undercroft` raised the question of what a stack of
layers actually does; this board is the minimum geometry that answers it — a gallery running under a
meadow, an adit climbing out of its east end — built so that every claim on the studio's layer track
can be measured against one file instead of a paragraph.

`maps/opus5-mineshaft`, `specs/opus5-mineshaft/`.

## What it is

Eighty blocks square, two layers, six shapes, no relief and no dressing.

The **mine level** (layer `ground`, `base_y 0`) is four wall rectangles **clamped around** a tucked-in gallery floor —
`wall-n`, `wall-s`, `wall-w`, `wall-e` at `floor 0` `base_height 20`, and `gallery` at `floor 0`
`base_height 4` in the channel they leave (x −30..24, z −6..6). A `ramp` polygon over x 0..24 carries
`anchor_heights [4, 26, 26, 4]`, climbing the gallery floor to meadow height.

The **meadow** (layer `surface`, `base_y 20`) is one `deck` rectangle over the whole board at `base_height 6`, with a
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
`[16,22)`, in both draw orders. The lower shape is erased. The gate names it now — `SK9` raises one
`Decline` per contesting pair, saying which of the two shapes is not in the world (`TS27`) — and the
committed variants `opus5-mineshaft.one-layer-a` and `-b` are what it is measured on, while the
two-layer mineshaft beside them stays silent.

## What the reads say about it

The export gate is open. Round-trip, mirror and buildability pass; traversability answers a complaint
rather than a refusal, and the complaint is wrong — it names `wool red` for `red-team` and `wool blue`
for `blue-team`, each wool's own defender, which its room's `enter` rule bars by design. A wool's team is
read off a key the map document does not carry, so no wool names one at all and every team is asked to
reach every wool (`RP56`).

`GET …/walk?from=0,30&to=0,-30`, spawn to spawn across the middle, answers **reachable, distance 60,
blocks 0, drops 0**. The route runs dead straight along x = 0 and stays on the meadow at 26 the whole
way. The walk stands a player in a place rather than on a cell, so the gallery floor at 4 under the same
columns is a second node and not a surface the route flips onto: a twenty-two block fall between two
storeys is a step no clearance admits (`TS21`).

The two storeys are nevertheless one board, which is what the adit is for. Flooded at `Walk.FreeRise`,
6,670 of the board's 6,962 places are a single component, and the gallery floor at `(0, 0, 4)` and the
meadow at `(0, 0, 26)` are both in it — joined by the ramp climbing out of the east end, not by the
column they share.

`render/topdown` draws the meadow, because the deck roofs all 6,400 cells. `?layer=ground` cuts the
read to the mine storey — that layer's own ground and everything standing on it, up to where the
meadow's floor starts — so the cut is the layer the author drew rather than a height they had to guess
(`WS12`). The two ids this board answers to are `ground` and `surface`, which is what the 422 lists when
a caller names neither.
The blunt cut is still there: `renders/topdown-mine.png` is `ymax=19`, and it shows both spawn cubes,
which stand on the meadow at 26. A read that colours by **provenance** keeps them wherever it is cut,
because a provenance claim is keyed `(X, Z)` with no Y — the reason `C48` attributed the 3-D preview's
runs to the rasterizer's own spans instead of to it.

`renders/section-z0.png` is the picture that never needed a cut: the vertical read at z = 0 shows the
meadow slab, the void under it, the wool room standing on the gallery floor, and the adit climbing out
to the right.

## The renders

| File | Is |
|---|---|
| `topdown.png` | the meadow, which is all a top-down read can see |
| `topdown-mine.png` | `ymax=19` — the gallery, and the two spawn cubes a height cut cannot drop |
| `section-z0.png` | the cut at z = 0: slab, void, floor, adit |
| `heightmap.png` · `surface.png` | elevation and paint, both of the deck only |
| `traversability.png` | one component, which the adit makes true of the storeys and not only of the columns |

## Not a map

Two teams, two wools at the west end of the gallery, spawns on the meadow north and south. They exist
so the export gate has something to check and so the section has a structure in it. The board has no
symmetry worth the name, no cover, no second route and a twenty-two block drop where the meadow meets
the gallery. It is a fixture.
