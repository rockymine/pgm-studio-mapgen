# Hoarstone — five islands, thirteen standing stones, four plan shapes

> The same design language as Elderwold, smaller, and abstract: erected pieces standing out of the
> terrain in materials the ground is not made of, a snow-and-stone landscape, template spruce, and
> houses that are actually an L, a T, a U and a single range.

**In one sentence:** a frozen archipelago where each team holds one island, three neutral rocks lie
between them, and a ring of six ice-banded monoliths stands on the middle one — with a row of black
basalt blades stepping across each team's ground toward a green cairn on a wind-scoured bench.

130 × 210 blocks, `rot_180` about the origin, base surface 12, ground y6..y44, build ceiling 64.
Five landmasses: two team islands, two skerries (one fanned pair), one on-axis core.

## The board

Four plan pieces, three build zones, two markers.

| Piece | Cells | Blocks | Island |
|---|---|---|---|
| `shore` | `[-13, 8, 26, 13]` | x −65..65, z 40..105 | the team island |
| `spawn` | `[-2, 17, 4, 4]` | x −10..10, z 85..105 | at `ST9`'s 20×20 cap |
| `skerry` | `[8, 2, 5, 4]` | x 40..65, z 10..30 | fanned — one a side |
| `core` | `[-6, -4, 12, 8]`, `mirrors: false` | x −30..30, z −20..20 | on the axis, so it stays one |

`plan/inspect` reads the three straits as **20 / 10 / 10** blocks, all inside `G5`'s 10–20 for a
crossing a route depends on, and each is spanned by a build zone. The goal ratio is **3.6**, inside
`GO1`. `evaluate` is `valid: true` at score 2.14, with the same two soft terms a solid board always
carries.

**The compiler groups by mirror, not by landmass.** `shore` and `skerry` are both fanned, so they
land in **one** island called `team`; `core` is on-axis and is its own `neutral`. A relief is keyed
by island, so the board has two reliefs and the first of them covers two separate rocks. That works
because the relaxation only ever steps onto land: a mark on the shore says nothing to the skerry
twenty blocks of void away, and the two solve independently inside one field.

**Nothing on `neutral` is mirrored for you.** Every mark on the core island is authored as an
explicit pair about the origin — a `point` at `(24, 6)` and one at `(−24, −6)` — because a
non-fanned island's relief is stated once and used once. Author one horn and one team plays a
different middle from the other.

## The coasts, three ways

| Shape | Treatment | Why |
|---|---|---|
| `shore` | 20 vertices, Catmull-Rom handles on every edge | a coastline: smooth, with a west bay and a back cape |
| `skerry` | 7 vertices, **no handles at all** | a shard. Sharp corners read as broken rock, and a smoothed one would have read as a small island |
| `core` | 12 vertices, smoothed, and **its own rot_180 image** | authored as six points plus their negations, so a prop fanned onto it lands on it |

The core's symmetry is not cosmetic. Every standing stone is appended to island `team`, so every one
of them is fanned — which is right for the shore's (each side gets its own) and right for the
skerry's (the pair swap), and is only right for the core's because the core is its own mirror. The
check is in the build script: worst point-to-mirror distance **0.000 blocks**.

## The standing stones

Thirteen authored shapes, `height_mode: raise`, `skirt: 0`, `floor: 0`, five or six vertices each,
no Bézier handles, and `anchor_heights` to slant every top. Each carries its own theme.

| Group | Where | Theme | Lift |
|---|---|---|---|
| `row-1..4` | stepping across the team island toward the cairn | `basalt` | 12, 15, 13, 18 |
| `watcher` | the front-east headland | `ochre` | 21 |
| `thumb` | the west shoulder | `ochre` | 11 |
| `tarn-shard` | leaning out of the tarn's rim | `rime` | 9 |
| `shard-1/2` | the skerry | `ochre` / `basalt` | 14 / 10 |
| `ring-1..3` | the core island — **six** once fanned | `rime` | 17, 14, 19 |
| `altar` | inside the ring, off-centre | `basalt` | 8 |

**`raise` means over the ground, and the anchors slant that.** Probed on flat ground at y11: a
`raise` of 10 with no anchors tops out at y21 everywhere; the same shape with
`anchor_heights: [4,4,16,16]` runs y19 → y25 across its own footprint. So a stone dragged onto a
slope keeps its height above the slope, and the slant is stated per vertex rather than per plane.

**A pillar theme's stack goes in `fill`, not only in `surface`.** A `layered` stack in `surface`
alone bands the top four courses and leaves the rest plain — which on a 30-block monolith is the
whole face. Every one of the three pillar themes puts the identical stack in `surface`, `wall` and
`fill`, and the column read at `(−12, 64)` runs black clay, coal, gray, obsidian, black clay from
y10 to y27 — the strata the whole way up.

**They are not in the ground's tone family, and that was a correction.** The first cut painted them
andesite, polished andesite and cobble — grey stone on a board whose exposed ground is grey stone.
The surface read showed them as terrain wearing a different seed. Black stained clay, ice-blue clay
and ochre terracotta each read at a glance and each stands at least three times.

## The ice

One map theme, `firn`: a `noise` of snow, snow and stone in the top course over snow and gravel, a
`void`-edged voronoi rim of gravel and stone, and a wall banded stone / andesite / **packed ice** /
stone, so every coast cliff is a glacier face. `render/surface` reads white with grey patches.

The **areas** are brushes, the same instrument Elderwold used: five wide path props that carry no
traffic and say what a stretch of ground is — a scree slope of stone and gravel under the moraine,
a frozen tarn of ice and packed ice in the sunk hollow, a wind-scoured bench of bare rock around the
cairn, a podzol patch (the board's only soil, and therefore the only place a plant grows), and a
cobbled hearth inside the ring of stones.

## The houses

Four shapes, four roof forms, four storey stacks. `HP3` caps a placed building at **192 blocks** of
wing — a number the endpoint states in its refusal — so each is drawn to fit under it.

| Building | Plan | Wings | Roof | Storeys |
|---|---|---|---|---|
| `steading` | **U** | 16×7 hall + two 5×7 wings = 182 | `gambrel`, snow body | 2 — layered stone/cobble below, spruce over a log band above |
| `watch` | **T** | 15×8 hall + 7×9 wing = 183 | `hip`, andesite body | 3 — polished-andesite plinth and brick, then a log-and-timber checker with panes, then spruce under a fence course |
| `longhall` | **L** | 14×8 hall + 7×10 wing = 182 | `gable`, snow body | 1 — a rubble base under four courses of spruce |
| `store` / `bothy` | **I** | 10×8 = 80 | `shed`, spruce body | 1 — cobble under a packed-ice/white-clay checker |

The joint rules are what decide the geometry: `HJ2` wants the whole of the shorter edge met, so a
wing's full width abuts the hall's flank; `HJ5` wants the wing no longer along that edge than the
hall is deep across it, so every wing is 5–7 wide against a hall 7–8 deep; and corners are
inclusive, so a touching wing starts one row past its hall.

**A storey carries `clear + 1` courses, and a stack longer than that is invisible.** The first cut
gave the watch a seven-band wall — three brick, one checker, three spruce — on storeys of clear 3.
Four courses fit, so it built brick and checker and no spruce ever appeared, and the section read as
one grey mass. Each storey now names its own wall, sized to its own clear, which is also what makes
the three storeys read as three different rooms.

## What went wrong

**A house is placed by hand, and nothing checks it.** The dressing pass declines a *prop* that rests
on another prop's ground, but a standing stone is **terrain**, so `DR-CLAIM` never sees it — the
first build stood the L-plan shrine inside `ring-1`'s footprint and reported nothing. The build
script now audits every house footprint against the islands, the stones and the goal ring itself,
which found nine faults on the first pass and none on the last.

**Three of the first build's four declines were mirror images, not originals.** A boulder beside the
shrine on the core island is a boulder inside the shrine's own twin, and the pass declines the whole
prop rather than the image. The site filter now tests `(x, z)` and `(−x, −z)` against every prop.

**The authored ring is not the coast.** Testing a footprint against the polygon's vertices reads the
island as smaller than it is wherever the Bézier bulges out — and, worse, as larger wherever it
bulges in. The steading's north-west corner sat 1.5 blocks inside the drawn polygon and 1 block
outside the built one. The filter flattens every ring to the 24-samples-per-edge outline the
rasterizer draws before testing anything against it.

**A brush is an exclusion zone as wide as itself, and this island is half Elderwold's.** The first
dressing put a radius-11 scree brush and a radius-7 duff brush across the wood; between them and the
spawn lane the wood placed **five** trees. Shrinking the brushes and giving the wood the whole
middle-west band took it to 32.

## Coordinates

| Thing | At |
|---|---|
| cairn (red) | `<cuboid id="greenstone-region" min="17,23,62" max="19,25,64"/>` — 3×3 emerald, floating 4 over a bench at y19 |
| cairn (blue) | `min="-19,23,-64" max="-17,25,-62"` |
| spawn (red) | piece `x −10..10, z 85..105`, marker `(0, 95)`, door facing −Z |
| the ring | six `rime` stones about the origin, tops y29–y33; the `altar` inside it at `(−9..2, 5..15)` |
| the tallest stone | `row-4`, top **y36** at `(30, 74)`; build ceiling 64 |
| the straits | 20 blocks shore↔core, 10 shore↔skerry, 10 skerry↔core, each spanned by a build zone |
| relief | `team` 8 076 cells, y7..27, symmetry error 0 · `neutral` 1 874 cells, y9..18, symmetry error 0 |
