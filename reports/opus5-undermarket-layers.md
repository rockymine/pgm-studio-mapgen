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

**A read can be asked for one storey by name.** `render/topdown?layer=yard` draws the yard's own ground and
everything standing on it, up to where the terrace's floor starts — the cut this board was drawn to need, and
the one `renders/topdown-under.png` had to approximate with `ymax=19`. `section` and `column` take no `layer`,
because they keep Y and show every storey already.

**Provenance names a pass, not a layer.** `region/provenance.json` carries a `pass` key, and it is keyed
`(X, Z)` with no Y — which is why a read that colours by it cannot tell this board's two storeys apart.

## The renders

| File | Is |
|---|---|
| `topdown.png` | by material: grass across the middle, stone brick around it, oak on the spans |
| `topdown-under.png` | `ymax=19`, below the deck — **no grass anywhere**, the yard showing through where the terrace was |
| `topdown-category.png` | the same board read by category rather than by block |
| `section-z0.png` | the cut at z = 0: the yard, the void over it, the deck, and a span standing out over nothing |
| `traversability.png` | one component — the yard and the terrace, joined only by a rise nothing bounds |

Counted off `topdown.png`: **17,440 px of grass** on the deck against **28,320 px of stone-brick grey** on the
yard. `topdown-under.png` holds no green at all.

## Not a map

Two teams, two wools, and spawns the export put on the **terrace**. The intent states both at `y 6`, on the
yard — `{"team": "red", "point": {"x": -24, "y": 6, "z": 0}}` — and `map.xml` carries
`<point id="red-spawn-point">-24,24,0</point>`, because a stamp resolves its Y from the column's top surface
and `(-24, 0)` is inside the terrace band. Naming a `layer` on the placement is how an author says otherwise
(`WE24`); this board names none, so it takes the top one, which is the documented behaviour and not what was
meant here. The wools stay on the yard at `y 5`: `(-20, 20)` and `(20, -20)` are outside the band, so their
columns have no terrace over them.

The board has no cover and no second route, and the spans go outward over void rather than anywhere. It is a
fixture.

## What the walk says about its storeys

The walk stands a player in a place rather than on a cell, so this board is 5,182 places over 3,600 cells and
the terrace twenty blocks over the yard is ground of its own. Flooded at `Walk.FreeRise`, the two come apart:
the yard at `(0, 0, 6)` is a component of **3,472** places and the terrace at `(0, 0, 24)` — where both spawns
stand — is a component of **1,390**. Nothing on this board climbs between them.

The export gate is nevertheless right to pass it, because its question is whether anyone can get there rather
than whether the ground joins. Flooded with no bound on the rise, the board is one component: at
`(0, -13, 6)`, a yard cell at the terrace's edge with open sky over it, an eighteen-block step onto
`(0, -12, 24)` is a step the clearance admits — a player pillars up. A slab with a roof over it would not
admit it, which is the distinction the two floods are for.

`traversability.png` draws that one component. The complaint the same read raises beside it — `wool red` for
`red-team`, `wool blue` for `blue-team` — is wrong, and wrong on any board carrying the studio's own
`You may not enter your own wool room` rule: a wool's team is read off a key the map document does not carry,
so every team is asked to reach every wool including the one it defends (`RP56`).
