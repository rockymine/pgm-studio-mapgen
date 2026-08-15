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

## The house styles do stamp

`specs/sandscar/style-previews/` holds all three of Grok's styles previewed from his own JSON:
`desert-hall` in sandstone with a brick roof, `savanna-cottage` under a hip, `monument-shelter` under a
shed. The styles were never the problem — the props file's footprints were. `desert-hall`'s `sill` is
written `{"material": {…}}`, one wrapper deeper than the model reads, which is the fault the export gate
names as `style.sill.kind`; `monument-shelter` states `"gableWindows": null` and `"doorHead": null`, which
crashes the stamper rather than being read as "no such part".

## The buildings, recovered — and two the gate refused

The README's "spawn hall + two monument shelters" is an assignment, and `desert-hall` bound as
`roomStyles.spawn` puts the hall over each spawn pad with no rescaling — a bound room's frame comes from the
plan piece, so the prop cap never applies. `renders/11-topdown-material-buildings.png` is that board.

The two monument shelters are the one thing left out, and the studio is the one that left them out:

```
GET /api/map/{slug}/export → 409 OB19
building 'west-shelter' at (-30, 73) stands inside a goal's clearance;
building 'east-shelter' at (27, 73) stands inside a goal's clearance
```

They were placed over the monuments — which the ×5 reading puts within a few blocks of the goals — and
roofing a destroyable is a real fault rather than a formatting one. The gate named both by id and
coordinate. Everything else in that document built.

## The paint is an approximation

Nothing defines `desert-savanna` or `savanna-crest`, the two names Grok's layout writes on its shapes, so
the committed world paints with the built-in default. `specs/sandscar/approximated-theme.json` is the
README's one line ("sandstone + endstone + birch + brick roofs") written as a real theme — sandstone and
end stone in a voronoi surface, a chiselled sandstone lip, a smooth sandstone riser — and
`renders/10-topdown-material-painted.png` is the board under it. The block ids are his; the bucket
structure is mine.

## The dressing

`specs/sandscar/sandscar.dressing.json`, translated at ×5 (Grok's props are in plan cells; a dressing
document is in blocks). Four acacia and all four paths land — including `river-meander`, which is not a
`water` prop at all but a `path` paved with a `cell` material over blocks 8 and 9, and reads as a river in
`renders/06-topdown-dressed.png`. All three houses are dropped: `spawn-hall` covers 1 500 blocks² against
a 192-block² cap, and the drop is silent.

`renders/07-topdown-dressed-literal-units.png` is the same dressing at ×1, and is the proof of the unit
error rather than an argument about it: the spawn hall builds, at the plateau's front lip instead of on
the spawn pad, and the trees fall off the board.
