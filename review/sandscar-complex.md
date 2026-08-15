# Sandscar Complex — the measured record

> A DTM board built as a height progression: a river across the mid, a low desert front, a pit dug four
> surfaces down with a monument on its floor, a hill climbing twelve up with the other monument on its
> top, and a savanna crest behind. Authored by Grok with no live studio; built here from its plan with
> two rects corrected.

204 × 360 blocks, `rot_180` about the origin, base surface 40, build ceiling 76, y 31..82. Twenty-four
pieces at fourteen surfaces from 32 (the pit floor) to 52 (the hill top), compiled to 25 shapes on one
island — the largest board in the run and the most vertically ambitious.

## What was corrected

Four overlaps at different surfaces, from two mis-sized rects:

| Piece | Grok wrote | Built as | Was overlapping |
|---|---|---|---|
| `savanna-gate` | `[-8, 18, 6, 5]` | `[-8, 20, 6, 5]` | `pit-floor` (Δ10) and `pit-rim-e` (Δ5) — it started two cells inside the pit |
| `upper-east` | `[4, 28, 8, 4]` | `[4, 28, 6, 3]` | `hill-top` (Δ−5) and `crest-east` (Δ3) |

Both edits move a piece onto the row it already belongs to: `savanna-gate` at z 20 lines up with
`savanna-west` and `savanna-east`, and `upper-east` at 6 × 3 abuts `crest-east` instead of climbing into
it. Every surface and every marker is Grok's.

## Measured

| | |
|---|---|
| gamemode | `dtm`, "Destroy the enemy's monuments!" |
| teams / spawns | 2 / 2, `rot_180` |
| destroyables | 4 — `<Team> Pit Monument` on the pit floor (surface 32) and `<Team> Hill Monument` on the hill top (surface 52) per team, obsidian, `cube-3`, floats 2 and 3 |
| build ceiling | `maxbuildheight` 76 |
| zones | three build zones — `river` (200 × 10 over the axis void), `mid-build`, `pit-void` |
| traversability | 50 892 navigable columns, 4 264 bridged over void, 2 components, **0 of 4 markers isolated** |
| evaluator | score 1005.3, `valid: false` — a **hard** gap hop of 21 between `low-desert-e` and `mid-bridge` (the band is 10–20), plus fill-ratio 0.647, frontline-width 36, max-chain-length 180 (band 25–110) |

The 20-block ceiling on a void hop is the one hard term, and it misses by one block. Nothing stops the
board being built — `valid: false` from the evaluator is advice about a board's shape, and the compile's
422 is the only refusal — but it is a real statement about the board: that one crossing is a block further
than any corpus map asks a player to bridge.

**The board is fragmented, and that is the design.** `renders/02-topdown.png` shows how much void sits
between pieces: twenty-four rectangles that mostly do not abut, joined by bridges and hops rather than by
continuous ground. Traversability still reports 2 components and 0 isolated objectives, so every monument
is reachable — the fragmentation is lanes, not islands.

## The relief was deliberately not carried

Grok's `sandscar-complex.layout.json` states a relief with `base: 40` and three features (a river cut
along the axis, a depression at `(−45, 80)`, a hill at `(50, 130)`). A relief governs its **whole island**
— a shape keeps its own top only under `relief_scope: "hold"` — and this board's pieces stand from 32 to
52. Carrying it would have levelled the pit, the hill, the terraces and the crest to one plane at 40 and
then dug three landforms into the result, destroying the height progression the plan exists to state.

So the board was built from the plan's surfaces and the relief left out. The two documents contradict each
other and nothing in the pipeline would have said so; the relief file is preserved verbatim under
`specs/sandscar-complex/authored-by-grok/`.

## The paint is an approximation, and it recovers the progression

The board's eight theme names define nothing, so the committed world is default paint. The approximation in
`specs/sandscar-complex/approximated-theme.json` is three themes — `pit`, `desert`, `savanna` — assigned by
the height a shape stands at, because Grok's names key to his own shape ids and a compile does not produce
those. The bands are the ones his own names describe: pit at 37 and below, desert to 41, savanna above.

`renders/10-topdown-material-painted.png` is the result, and it is the clearest picture of what this board
is for: sand along the river front, green savanna on the high ground behind, end stone in the cut pit. The
desert→savanna progression his README claims is real and it lives in the surfaces he authored, not in the
themes he named.

## What is not here

No dressing — the props file is byte-identical to Sandscar's, so its positions belong to the other board
entirely; it was not applied here. No terrain theme: eight theme names are written on the shapes
(`desert`, `desert-pit`, `river-bank`, `savanna`, `savanna-mid`, `savanna-hill`, `savanna-peak`,
`savanna-crest`) and no `themes` registry defines any of them, so the board paints with the built-in
default.
