# Quatrefoil — four teams on the board as it was drawn

> A four-team capture board on one `rot_90` island: four corner quarters of mossy moor, four pale sand
> capes on the axes, and a stepped keep in the middle that every route crosses and nobody owns.

**In one sentence:** the author's own plan at the author's own scale — eleven rectangles at `cell: 1`,
their ids and their arrangement untouched — with the shaping done by piece heights and three ramps
rather than by relief, so that every one of its 5 904 ground blocks is walked without a placed block.

98 × 98 blocks, `rot_90` about the origin, cell 1, base surface 9, twelve players a team, ground
y7..y17. Nine landmasses, none of them touching: four quarters, four capes and the keep.

## The scale is the author's, and that is the whole point

The plan arrived drawn at `cell: 1`. `POST /plan/evaluate` reads it `valid: false` on `G5` — *gap hop 8
outside 10..20* — and that is where the first build of this board went wrong: `"kind": "hard"` was read
as *this will not build*, the cell was doubled to satisfy it, and everything downstream doubled with it.

**Nothing refuses on `G5`.** Driven at the author's scale the plan compiles, stores, pre-flights and
exports:

```
POST /plan/compile              200
POST /map/from-documents        200
GET  …/preflight                export gate OPEN
GET  …/coverage                 reached 5904 · dead 0 · 0.0%
GET  …/slopes                   5904 walked · 0 scrambled · 0 barrier · 0 faces
POST …/sketch/dressing          placed 39 · declined 0
```

`G5`'s 10–20 band, `G2`'s ten-block corridor and `LN1`/`LN2`'s lane figures are the composer's, learned
from generated 32-player boards. This board is a compact rush board for a small side, and it is out of
those bands on purpose. What it is *not* out of is anything that decides whether it can be played.

## What is added to the plan, and what is not

Three things the plan cannot state and the board cannot be played without:

| Added | Why |
|---|---|
| two build zones | `zones: []` leaves the board with no frontline at all, and every wool then refuses as *reachable only through a spawn*. `bz-arm` laps the arm and the quarter gap either side of it; `bz-cross` is the arm's hop onto the keep's apron |
| the wool marker moved onto the `wool` piece | the plan placed it on the `spawn` piece, which reads spawn↔wool = 1 block (`WL2`). The room the plan draws is where it belongs |
| a `footprint` on the spawn, and its iron | see *The spawn*, below |

Everything else is paint, ramps and dressing. **No rectangle moved, no piece was split, no piece was
added.** The eleven ids are the author's own — `piece`, `piece-2`, `piece-4`… — and are kept so that the
diff against the drawn document is only the `surface` line.

## The heights, and why two of them moved

| Piece | Drawn | Built | Why |
|---|---|---|---|
| `spawn` | 7 | 8 | a room two blocks under its own egress is a wall at the door |
| `piece-5` · `piece-6` (the marches) | — (9) | 9 | — |
| `piece-8` · `piece-9` (the wool approaches) | 11 | 9 | **the ramp does the climbing** — a piece stated at the ramp's own top height hides it, because the taller add wins the column |
| `wool` | 13 | 11 | a room two blocks over its own approach stands on a plinth |
| `piece-11` · `piece-2` (the arm) | — (9) | 9 | — |
| `piece` (the arm's inner run) | 11 | 9 | the ramp again |
| `piece-10` (the keep's apron) | 13 | 13 | — |
| `piece-4` (the keep) | 15 | 15 | — |

The tiers are still the author's: 9 on the quarters, 11 at the wool, 13 on the apron, 15 on the keep,
16 and 17 on its two terraces.

## The shaping is ramps, not relief

Every place the plan steps two blocks is an authored ramp over the piece that steps — a `level` shape
with a height at each vertex, `relief_scope: exclude` so the grain cannot wobble it, and a run of at
least twice its own rise so the risers are one block rather than two.

| Ramp | Over | Climbs | Read back |
|---|---|---|---|
| `ramp-wool-w` · `ramp-wool-n` | the approach in front of each wool room | 9 → 11 over 7 blocks | `9 9 9 9 9 10 10 10 10 11` — worst step **1**, walked end to end |
| `ramp-arm` | the arm's inner run | 9 → 11 over 8 blocks | — |
| `keep-ramp` | the apron, one per arm | 13 → 15 over 7 blocks | — |

**The relief carries a grain and nothing else** — no marks, no pushes. `base 9 · reach 5 · grain 0.9`
over a scale of 13, which is ±1 block of texture on ground whose shape is already stated. `reach` is 5
rather than 0 for a measured reason: zero is unlimited, and a group whose only constraint is the wool
room's own pin then solves the *whole quarter* at the room's height — the first pass of this build read
`11 11 9 9 9 10 10 11` across the ramp, a two-block drop into the climb, and that was the pin reaching
thirty blocks.

Read back over the built world: **5 904 cells walked, 0 scrambled, 0 barrier, 0 faces.** There is not a
single step on this board a player cannot walk up.

## The spawn

The region is the author's 20 × 20, because that is the ground the team owns; the **hall** is 12 × 12,
stated as a `footprint` and set in the piece's outer corner. Region and building are two rectangles, so
the protected ground stays the whole `min="-48,-48" max="-28,-28"` while the building sits inside it: a
one-block verge behind and to the west, a seven-block yard in front of each door and eight of open ground
between them. The spawn point is `-41,9,-41`, the hall's own centre.

**It has two doors, and they are not stated.** The spawn piece meets the board on exactly two sides —
`piece-5` along `+z` for thirteen blocks and `piece-6` along `+x` for thirteen — so that is where the hall
is cut, the same derivation the wool cage has always used and the same two-entry shape it has on this
board. The compiled layout carries `spawn-red: ['+z', '+x']` beside `wool-red-red: ['-x', '-z']`.

**The player looks at the corner between them.** `facing: "back-right"` is a diagonal, so the yaw is
`315` — and its three orbit images are `45`, `135`, `225`, each team turned to face the middle of the
board. No door is derivable from that angle, which is the point: the doors ride the intent instead.

```
out of the +z door, west march    (-41,-34) 9 · (-41,-31) 9 · (-41,-28) 9 · (-41,-26) 9
out of the +x door, north march   (-34,-41) 9 · (-31,-41) 9 · (-28,-41) 9 · (-26,-41) 9
both: rises 0, falls 0, worst step 0 — 0 barrier, 0 scramble, 0 drop, walked end to end
```

Both mouths read open in the world — air at `y 9` and `y 10` under a stone-brick-slab lintel at `y 11`,
at `(-41, -36)` and `(-36, -41)` — against mushroom-stem wall at `(-36, -45)` and `(-45, -36)`.

**The iron cube is beside the door, on the player's right as they leave.** It is not placed by hand:
`POST /plan/room?piece=spawn` answers `{"at":[7,7],"footprint":[1,1,12,12],"iron":[3.5,16.5]}` for this
hall, and the plan states that answer verbatim. With two doors it takes the one the facing leans into
first — the `+z` door, which ties on lean with `+x` and wins on the walls' reading order. The seat is the
nearest row outside that wall `WX8` allows — the building's own edge plus `IronGap`, so two blocks of
standing room — and the flank of the door corridor the player's right hand points at, which for a `+z`
door is the low-x side. Measured in the world at `x −46..−43, z −33..−30`, standing on the spawn's own
ground:

| column | ground top | cube |
|---|---|---|
| `(−45, −32)` | mossy cobblestone `y 8` | iron `y 9–11` |
| `(−44, −31)` | coarse dirt `y 8` | iron `y 9–11` |
| `(−41, −34)` — the door mouth | mossy cobblestone `y 8` | clear |
| `(−38, −32)` — the left flank | mossy cobblestone `y 8` | clear |

Nine courses of bedrock under a cube in the yard's inner corner (`WX11`, measured on an earlier hand
placement) do not arise here: the seat is inside the piece's own ground, not out at its rim.

## What a raid costs

| Journey | Blocks | Placed |
|---|---|---|
| red → its own wool | 25 | 1 |
| red → the quarter anti-clockwise | 63 | 15 |
| red → the quarter clockwise | 72 | 15 |
| red → the quarter opposite | 118 | 29 |

**No drops on any of them.** Every enemy wool costs fifteen placed blocks at least, because no two
landmasses on this board touch: the three build regions are the whole of the connection, and the eight
to twelve blocks of void they span are the price of leaving your own quarter.

## What the ground is made of

Four themes over 5 904 cells, on the five colours the author named, resolved through
`GET /api/terrain/blocks` to blocks that are ground rather than a stated shade — no stained clay, no
wool, no glass.

| Theme | Share | On | Says |
|---|---|---|---|
| `moor` | 58.3% | the quarters | a **cell of two blocks** — moss against bare earth — over dirt; rim **off**, because a rim caps every fall and turns a grain into contour lines |
| `strand` | 18.7% | the four capes | sandstone, sand and gravel — a mottle, because two blocks on a bar this size read as a deck |
| `brake` | 12.4% | four authored splotches | podzol and coarse dirt: bare ground worn into the moor, and the bed cut into the keep's deck |
| `keep` | 10.6% | the keep and its four aprons | **made**: a three-block checker of smooth sandstone and sandstone, a chiselled kerb on every drop (`rimEdges: drop`), and a `layered` face of cornice · smooth sandstone · **prismarine band** · stone brick · andesite |

Three families named before anything was painted. **Ground** is the mossy moor and the pale sand.
**Built by a team** is pale — polished diorite and mushroom stem, in the spawn hall and the wool cage
alike, so a team's own architecture reads as one thing. **Built long ago** is the keep's masonry.

## The keep

`piece-10` and `piece-4` carry `relief_scope: exclude`: flat where they are stated, sheer where they
end. On top of that, a ramp up each of the four faces and two concentric terraces at 16 and 17, with the
kerb running round every drop. Four beds of podzol are cut into the deck's corners with flora over them
and a birch in one — the same idea as the first build, at a quarter of the area.

## What it does not have, and why

- **Almost no dressing in the quarters.** Two tracks, a flora overlay, four trees and two erratics on the
  whole authored unit. On a 98-block board the four spawn keep-outs, the four wool-room door approaches
  and the two tracks claim nearly every cell of a quarter: `loop.py --candidates` answered *none of them*
  for a third boulder across six positions. Bare ground chosen beats dressing that would not stand.
- **No relief marks and no pushes.** The board's shape is its tiers and its ramps.

## What is left

- **`G5` · `G8` · `LN1` · `LN2`** — the composer's bands, out of band on purpose. This is a small board.
- **`WL11` ×2** — *the wool room approach climbs 2 blocks*. Read at the plan tier, where a piece is one
  flat number; the built ground is the ramp above, and the transect through it reads worst step 1.
- **`EL1`** on `piece-4`–`piece-10`, answered by `keep-ramp` for the same reason.
- **`WX11`** on the wool room's entry rows — the room's own edge is the island's edge, and the section at
  `z = −20` shows ordinary ground under it down to the bedrock course at y0 rather than a plinth.
- **`04-routes.txt` is never written on a wool board**, so the third of *the three numbers* is missing by
  construction. The walks above were taken by hand with `GET …/walk`.

## The open question

**Twelve players a team is the number the plan carried and it is kept.** `maxPlayers` is documented as
*"how many players the board is sized for, across all teams"*, and the export writes it as each team's
`max`, so this loads as 12 v 12 v 12 v 12 on 5 904 blocks of ground. The board is drawn for a small side;
whether the cap should say so is the author's call and not a measurement.
