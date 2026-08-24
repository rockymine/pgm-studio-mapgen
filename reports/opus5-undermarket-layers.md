# Opus 5 — Undermarket: two storeys, two finishes, and nothing under the spans

## What it is for

A fixture for the three things the studio's layer track just gained, chosen so each one is visible in a
picture or readable at a coordinate rather than inferred from a count. `opus5-mineshaft` is the smallest board
that is genuinely two storeys; this is the smallest board that proves each storey **wears its own finish**.

`maps/opus5-undermarket`, `specs/opus5-undermarket/`. Authored through the studio's own API —
`POST /api/map/from-documents`, then `GET /api/map/{slug}/export` — not through the library.

## What it is

Eighty blocks square, three layers, four shapes, no relief and no dressing.

| Layer | `base_y` | Shape | Theme | Is |
|---|---|---|---|---|
| `yard` | 0 | `court`, x/z −30..30, `base_height` 6 | `flagstone` (stone brick) | the ground, open at its edges |
| `terrace` | 20 | `deck`, x −30..30 · z −12..12, `base_height` 4 | `meadow` (grass) | a band roofing the middle of it |
| `spans` | 14 | `span-w`, `span-e`, out to x ±44 | `plank` (oak) | two walkways over open void |

The terrace is a **band** rather than a lid on purpose: from above, the middle of the board is the deck and
the edges are the yard, so one top-down read shows both storeys' finishes side by side.

## What the board shows

**Each storey wears its own theme.** Read at `(0, 0)`, where the yard and the terrace both stand:

| where | `(x, z)` | y0 | surfaces |
|---|---|---|---|
| yard, open to the sky | `(0, 25)` | 7 bedrock | `yard@6` → **98** stone brick |
| yard under the deck | `(0, 0)` | 7 bedrock | `yard@6` → **98** stone brick · `terrace@24` → **2** grass |
| span over void, west | `(−38, 0)` | **0 air** | `spans@16` → **5** oak plank |
| span over void, east | `(38, 0)` | **0 air** | `spans@16` → **5** oak plank |
| off the board | `(60, 60)` | 0 air | — |

One cell, two surfaces, two blocks. Before the layer track landed, the upper slab took the paint of whatever
lay beneath it and the theme of the layer roofing a board landed on no block at all.

**A slab over void plates nothing under itself.** The spans read `y0 = air` while every grounded yard column
reads bedrock. A player walking off a span meets the void, and the column stays out of the Y0 set a void
filter reads.

**Provenance names a pass, not a layer.** `region/provenance.json` carries a `pass` key.

## The renders

| File | Is |
|---|---|
| `topdown.png` | by material: grass across the middle, stone brick around it, oak on the spans |
| `topdown-under.png` | `ymax=19`, below the deck — **no grass anywhere**, the yard showing through where the terrace was |
| `topdown-category.png` | the same board read by category rather than by block |
| `section-z0.png` | the cut at z = 0: the yard, the void over it, the deck, and a span standing out over nothing |
| `traversability.png` | one component — true of the columns and, on a stacked board, not yet true of the board |

Counted off `topdown.png`: **17,440 px of grass** on the deck against **28,320 px of stone-brick grey** on the
yard. `topdown-under.png` holds no green at all.

## Not a map

Two teams, two wools, spawns on the yard. They exist so the export gate has something to check and so the
section has structures in it. The board has no cover, no second route, and a terrace nothing climbs — the
spans go outward over void rather than anywhere. It is a fixture.

## What it still cannot say

`traversability.png` calls the board one component, which is true of its columns and false of its storeys —
the walk stands a player on the lowest surface carrying headroom, so the deck twenty blocks over the yard is
not a place at all. That is the open half of the track (`TS21`), and this board is a fixture for it too: the
terrace here is reachable from nothing, which a walk that could see storeys would say.
