# Skerry Wick — every route is a crossing somebody pays for

> A wool board of bare skerries over void. A team's two wool rooms stand on two separate
> islands on two different seas, so an attack cannot take both off one bridge and has to
> choose which water to cross first.

**In one sentence:** there is no land route anywhere on this board — every journey between
two islands is a gap of 10 to 20 blocks that somebody has to bridge under fire.

110 × 200 blocks, `rot_180`, base surface 14. Six pieces a team; land is about a quarter of
the bounding rectangle.

## The proportions are the composer's

A wool board is about half void and its size is not a matter of taste. `GET /api/compose
?players=24&symmetry=rot_180&wools=i` answers a team unit of **105 land cells** at cell 5 —
hub 44, frontline 32, two wools 20, spawn 9 — against a budget of 171. This board's unit is
**104**: home 40, two holms 2×16, reef 8, hub 32.

The shape that gets there is **not** symmetry about the centre line. The unit is drawn
offset west, spanning x −11..4 of a board running ±11, so its own `rot_180` image takes the
east of the far half and the two interlock. A unit drawn symmetric about x = 0 fills its own
bounding rectangle and cannot reach the `fill-ratio` band at any size.

## The islands

| piece | cells | is |
|---|---|---|
| `home` | 8×5 | the back island, carrying the spawn |
| `holm-far` | 4×4 | wool one, out on the open west flank |
| `holm-near` | 4×4 | wool two, east, in the hub's lee |
| `reef` | 4×2 | the stepping stone between home and hub |
| `hub` | 8×4 | the forward body, the only piece either team contests |

Every gap is 10–20 blocks — `G5`'s hop band — so each is a bridge rather than a jump.
`CT12` strait 20. Each holm is four cells to its room's two, because **a wool room's
foundation is bedrock to y 0**: beside void it builds as a plinth nothing drew, so the room
gets ordinary ground on all four sides.

## Why the two wools are side by side and not near-and-far

The board's first draft had one wool deep and one forward, which is the more interesting
idea. `WL9` holds the two wools to within **1.232×** of each other's walk from the spawn,
and a near/far pair cannot be that: the draft measured 1.55, then 1.34. The idea survives as
*separation* rather than depth — the two holms are 55 blocks apart on opposite flanks — and
the spawn door sits east in its island, which is what brought the two walks level (**ratio
1.0**, `plan/evaluate` score **1.0**, `valid True`).

## Numbers

slopes **5 553 walked, 54 scramble, 150 barrier**, faces 4 · claims **placed 10, declined
0** · coverage **9.9% dead** — the best of the eight · export gate OPEN.

Three themes: `skerry` 61.1%, `strand` 22.5%, `works` 16.3%, with 286 and 258 cells of
border. `roomStyles` carries **`wool`** and `spawn` — the wool room reads Dark Oak Planks at
y25 over Red Wool at y15, not the built-in bedrock box a key named `cage` would have given
at 200 with the gate open.

Biome **Taiga**: the grass and leaves on these islands take their colour from the biome byte
and nothing else on the board does, so it is a palette decision and not a line added at the
end.

## What went wrong

- `G5` twice. First a 5-block hop between home and the hub ring (under the 10 band), then —
  after the ring came out — a **45-block** one, because `home` and `hub` faced each other
  across x −7..−3 with nothing between. The `reef` is that nothing.
- `BZ9`: the build zone reached 40 blocks past the last ground it docked, twice, before it
  was cut to the hub's own width.
- `RL6`: the hub knoll climbed its skirt at 1.1 and its crown at 0.5. The crown's half-width
  is the **ring's**, not a number of my choosing — at r14 a crown of 7 spreads over 14, so
  the skirt had to come down to meet it (`amount 4, falloff 8`).
- Four props were placed over open void and one in the spawn keep-out, because I guessed at
  coordinates. The claims raster shows the holms are wool-room keep-out **edge to edge** — a
  20-block holm round a 10-block room leaves no cell a prop may have. Every prop now stands
  where `loop.py --candidates` said it would.

## Standing complaint

`LN1` — "lane-width 0 outside authored band [10, 30]", raised on every build and on a board
that has no lanes at all: the pieces are islands and the space between them is void. The
board is `valid` at score 1.0 and the export gate is open. I could not make it go away
without giving the board a land corridor, which is the one thing it is about not having.
