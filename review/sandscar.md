# Sandscar — the measured record

> A DTM board of one large plateau per team and a small spawn pad behind it, two monuments 50 blocks
> apart on the same side, a hollow under one and a hill under the other, and a mid build band between the
> two images. Authored by Grok with no live studio; the only one of its three plans that compiled
> unchanged.

144 × 270 blocks, `rot_180` about the origin, base surface 40, build ceiling 76, y 30..82. Two pieces —
the 120 × 90 plateau at 40 and the 30 × 25 spawn pad at 42 — compiled to 4 shapes on one island.

## Built exactly as authored

`POST /api/plan/compile` answered 200 with no warnings and no findings on the document as written. Nothing
in the plan was changed.

## Measured

| | |
|---|---|
| gamemode | `dtm`, "Destroy the enemy's monuments!" |
| teams / spawns | 2 / 2, `rot_180` |
| destroyables | 4 — `<Team> West Monument` and `<Team> East Monument` per team, obsidian, `cube-3`, floats 2 and 3 |
| monument spacing | 50 blocks apart on each team's plateau, as the document intended |
| build ceiling | `maxbuildheight` 76 (surface 40 + headroom 36) |
| traversability | 28 692 navigable columns, 5 564 bridged over void, 2 components, **0 of 4 markers isolated** |
| evaluator | score 2.1, `valid: true` — fill-ratio 0.611, frontline-width 24, max-chain-length 120 (band 25–110) |

## The relief is Grok's, translated

Grok's relief was written in an invented vocabulary (`noise` + `features`) and nested inside `layout`,
where the model reads neither, so as authored it would have been dropped entirely. It was translated
mark-for-mark into `specs/sandscar/sandscar.relief.json` and carried onto the compiled layout:

| Grok wrote | Built as |
|---|---|
| `depression (−25, 75) r18 depth 8` "under west monument" | `point` mark, `r: 18`, `h: 32` |
| `hill (25, 75) r16 height 10` "under east monument" | `point` mark, `r: 16`, `h: 50` |
| `hill (0, 100) r12 height 4` "gentle rise toward spawn" | `point` mark, `r: 12`, `h: 44` |
| `flat (0, 45) r25` "front approach flats" | `point` mark, `r: 25`, `h: 40` (the base) |
| `noise {scale: 0.04, amp: 2.5, octaves: 3}` | `grain {amplitude: 2.5, scale: 25}` — the stated scale is a frequency, the model's a feature size, 1/0.04 = 25 |

`renders/03-heightmap.png` is that field solved: the hollow and the hill sit either side of the plateau,
one under each monument, and the approach in front of them is flat. The board's own base is 40 and the
relief's is 40, which is why this relief composes with the plan instead of fighting it — the same relief
on `sandscar-complex`'s ten-surface board would have levelled it.

## The dressing

`specs/sandscar/sandscar.dressing.json`, translated at ×5 (Grok's props are in plan cells; a dressing
document is in blocks). Four acacia and all four paths land — including `river-meander`, which is not a
`water` prop at all but a `path` paved with a `cell` material over blocks 8 and 9, and reads as a river in
`renders/06-topdown-dressed.png`. All three houses are dropped: `spawn-hall` covers 1 500 blocks² against
a 192-block² cap, and the drop is silent.

`renders/07-topdown-dressed-literal-units.png` is the same dressing at ×1, and is the proof of the unit
error rather than an argument about it: the spawn hall builds, at the plateau's front lip instead of on
the spawn pad, and the trees fall off the board.
