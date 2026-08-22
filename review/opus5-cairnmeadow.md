# Cairnmeadow — stone folded into grass, and two goals that are the ground

> A meadow board. Two destroyables a team: one standing on an outcrop, one sunk in the cut the
> outcrop's stone was taken out of. The terrain is the whole of the design; there is one house on it.

**In one sentence:** an open green meadow over three islands, with eight irregular stone outcrops
raised out of it — walked onto rather than climbed, and painted back over with grass so they belong
to the ground — one of which carries the Tor Stone on its crown and one of which is a quarry with
the Delve Stone at the bottom of it.

128 × 236 blocks, `rot_180` about the origin, base surface 12, ground y6..y30, build ceiling 50.
Three landmasses: one island a team and one on the axis between them, crossed at two places.

## The board

Three plan pieces, two build zones, three markers.

| Piece | Cells | Blocks | Is |
|---|---|---|---|
| `meadow` | `[-13, 8, 26, 16]` | x −65..65, z 40..120 | the team island |
| `spawn` | `[-1, 21, 2, 2]` | x −5..5, z 105..115 | **10 × 10** — so the shell is 8 × 8 |
| `centre` | `[-9, -5, 18, 10]`, `mirrors: false` | x −45..45, z −25..25 | the middle, on the axis |

The spawn piece is the correction from the last two boards: a room's building is sized by its piece
(`ST9`, `WX1`), so a 20 × 20 piece stamps a 18 × 18 house, which is a hall rather than a spawn. Ten
by ten gives a cottage.

`plan/inspect`: `The Tor Stone` **3.46**, `The Delve Stone` **3.15**, both inside `GO1`. The strait
is **15** blocks. The two build zones sit either side of the front — `span-w` at x −45..−20 and
`span-e` at x 20..45 — so the **middle of the front is void** and the two ways over are the flanks.

## The outcrops

Eight `addShapes`, all `height_mode` erected, all in one theme, all with irregular seven-ish-vertex
rings and no Bézier handles. The whole board's vocabulary is one measurement:

| skirt vs lift | what it builds | measured |
|---|---|---|
| `skirt 0` | a sheer face of the whole lift | 7-block step, flat top, 7-block step |
| `skirt ≈ lift ÷ 2` | two-block risers — a lip that costs a placed block | +2 +2 +2 +1 |
| `skirt ≥ lift` | **one-block steps the whole way round** | +1 +1 +1 … |

Everything on this board but the cut is in the third row. The Tor is a lift of 7 under a skirt of
10; read down `x = 34` it runs 18, 18, 20, 19, 19, 20, 21, 22, 23, 24, 25, 25, 25, 25, 24, 24, 23,
23, 22 — a whaleback walked onto from any side, with the goal on its crown.

**The cut is the one face**, and it is a face because that is what a cut is. `height_mode: sink`,
lift 5, `skirt: 1`, and a per-vertex depth that is 5 at five of its seven corners and **1 at the two
southernmost** — a notch rather than a slope, so the pit is sheer nearly all the way round and has
one shallow way in. Read down `x = −24` from the south: 14, 14, 13, 12, 11, 8, 8, 8, 8, 7, 7, 6, 6,
5 — the haul ramp — and out the north side 5, 7, **11**. Attackers walk down into it from the front;
the defence holds the deep rim and shoots into the hole.

**Both goals are the ground they stand on.** `the-tor-stone-region` is `min="33,30,77"` — a 3-block
ender-stone cube floating four over a crown at y25, the highest thing on the island. The
`the-delve-stone-region` is `min="-24,12,70"` — an obsidian pillar whose *top* is level with the
meadow around the pit, so from the meadow you see it and cannot reach it.

## Grass painted back over stone

The crags are one theme and it is plain rock: a `noise` of stone, andesite and cobble over a wall
banded stone / andesite / cobble / stone, on a stone fill. Nothing about it is an accent — it is the
material the ground would be if the grass were scraped off, which is why it does not fight the
meadow the way three saturated palettes did on the last board.

What merges the two is **twenty path props with a grass pave**, drawn as tongues over each crag's
shoulders. A path replaces the surface finish and adds no cell, so this is free: two to five brushes
per crag, at different angles, `worn` at coverage 0.45–0.7 so the rock shows through the grass
rather than the grass stopping at a line. Read in section, the Tor is green up its flanks and grey
across its crown.

The same instrument makes the rest of the ground: brown coarse-dirt worn through the meadow where
it is walked, a scree fan of stone and gravel on the west, and a cobbled floor in the bottom of the
cut. Five routes carry traffic; the other twenty carry none.

## The terrain the crags stand in

`team` solves to relief **24** (y6..y30) at 97.7% walkable, symmetry error 0; `neutral` to relief
**10**, 96.5% walkable, **one place holding all of it**.

Six pushes lift the ground under each crag so it reads as the top of a rise rather than as a slab
dropped on a plain, and the marks give the island its own shape around them: a `backridge` behind
the spawn at 17→22→20→17, a `swale` down the middle at 10→6→6→8→10, a hollow behind the Tor, two
brow knolls at the ends, and the wide `delve-hollow` bench at 11 that the cut is sunk into.

**Two ordering facts cost a rebuild each.** A push is applied to the *solved* surface, so
`meadow-swell` laid across the quarry's hollow filled the hollow back in and the pit came out five
blocks shallower than it was drawn. And a later mark wins a contested cell, so `west-brow` — written
after `delve-hollow` and overlapping it — overrode the bench and left a **21-block** face into the
pit that nobody authored. Both were invisible in the document and obvious in one column transect.

## What is on it

18 trees: nine birch in a stand behind the Tor, nine oak on the front shoulder. Six boulders. Four
flora areas, which work here where they did not on the snow board — grass is soil, so an open meadow
is exactly the ground the overlay was written for.

**One house.** The spawn's own shell, bound through `roomStyles`: a gable cottage in oak over a
rubble course, spruce-plank roof, panes, **no beams**, one storey. There is no placed building on
the board at all.

## Coordinates

| Thing | At |
|---|---|
| The Tor Stone (red) | `min="33,30,77" max="36,33,80"` — ender stone, on a crown at y25 |
| The Delve Stone (red) | `min="-24,12,70" max="-23,15,71"` — obsidian, on a pit floor at y5–8 |
| the haul ramp | `x ≈ −24`, `z 60..76`, stepping 11 → 5 |
| the cut's deep face | `z = 72`, `x −38 → −36`: 12 → 5 |
| the Tor's walk-up | `x = 34`, `z 56..80`, one-block steps 18 → 25 |
| the crossings | `span-w` x −45..−20 and `span-e` x 20..45, both z 25..40; the middle of the front is void |
| relief | `team` 8 181 cells, y6..30, symmetry error 0 · `neutral` 3 812 cells, y9..19, one place |
