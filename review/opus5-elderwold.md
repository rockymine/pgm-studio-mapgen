# Elderwold — one shape, and everything else stated as relief

> A destroy board asked for as a brief rather than a spec: one endstone destroyable a side, a dense oak
> wood, a path, a river, houses — built from as few plan pieces as possible and shaped in the sketch.

**In one sentence:** a wooded island whose whole coast is a single 24-vertex polygon, cut across the
middle by a river with one paved ford, carrying a flat-topped shelf for the monument that is scarped on
its attack face and walked up only at one end, a three-step sunken hollow on the west flank, an oak wood
on the east, and a cottage on a knoll with a track up to it.

120 × 308 blocks, `rot_180` about the origin, base surface 12, ground y3..y26, build ceiling 46.
One landmass — the polygon's seam edge runs along `z = 0`, so its own image abuts it exactly and the two
halves are one island in the world.

## The board is three rectangles

The whole plan is three generating pieces at one surface, plus one build zone and two markers.

| Piece | Cells | Blocks | Is |
|---|---|---|---|
| `body` | `[-12, 0, 24, 14]` | x −60..60, z 0..70 | the front half |
| `shoulder` | `[-10, 14, 20, 8]` | x −50..50, z 70..110 | the middle, narrower |
| `bench` | `[-7, 22, 14, 4]` | x −35..35, z 110..130 | the back terrace |
| `spawn` | `[-2, 26, 4, 4]` | x −10..10, z 130..150 | the spawn room's piece, at `ST9`'s 20×20 cap |

They are all at `surface: 12`, which is the point: pieces at one height fuse, so the compile emits
**one** terrain polygon. The destroyable is authored with an empty `piece` and an absolute cell `at`,
so no rectangle had to be manufactured to carry it — it stands on ground the relief made.

`POST /plan/evaluate` answers `valid: true`, score 2.2, with two soft terms outside their bands:
`G8` fill-ratio 0.789 against [0.201, 0.496] and `LN2` max-chain-length 120 against [25, 110]. Both are
what a solid island 300 blocks long is; neither is a hard violation.

`POST /plan/inspect`: `destroyable-1` — own spawn 70 blocks, enemy spawn 250, **ratio 3.57**, inside
`GO1`'s [3.0, 4.0].

## The coast is that one polygon, bent

The compiled shape `s0` is a 16-vertex rectilinear union outline. The finish replaces its `vertices` with
24 hand-placed points and gives every edge but one a Bézier handle pair, merged through
`shapePropsById`. The handles are **Catmull-Rom in Bézier clothing** — `c1 = P1 + (P2−P0)/6`,
`c2 = P2 − (P3−P1)/6` — which is tangent-continuous at every vertex.

That mattered. The first attempt built each handle from the edge's own outward normal, per
`GENERATION-NOTES.md`'s corner recipe, and every edge bulged outward and met its neighbour in a cusp: the
island came out as a **gear**, twenty-four points around a blob. The recipe is right for one corner and
wrong for a closed coastline, where the constraint is continuity between edges rather than the shape of
each edge alone.

The edge from the last vertex to the first — the seam along `z = 0` — carries **no** handles. It is the
joint the rot_180 image abuts, and `GENERATION-NOTES.md`'s warning holds: bow it and the two halves stop
touching. Straight, the mirror lands on it exactly.

The width profile the curve produces, measured off the flattened ring:

| z | 0 | 20 | 40 | 60 | 80 | 100 | 120 | 140 | 150 |
|---|---|---|---|---|---|---|---|---|---|
| width | 118 | 108 | 109 | 108 | 108 | 83 | 86 | 52 | 33 |

120 at the widest, a waist of 83 at `z = 100` behind the shelf, and a 33-wide tip the spawn stands on.

## The relief is the map

Sixteen marks and three pushes on one island, `base 12`, `reach 24`, `step 1`, `stairs: true`,
grain amplitude 0.9 at scale 14. The readback: 13 950 cells, **low 4, high 26, relief 22**, 97.1%
walkable at the jump tier, **one** connected place holding 99.6% of it, 35 ledges, and a
**symmetry error of 0**.

| Mark | Kind | States |
|---|---|---|
| `coast` | `rim` | the outline held at 9, three below base — the shore dips to meet the void |
| `river` | `line`, 9 pts | the valley, `h` per vertex `[6,6,6,7,9,7,6,6,6]`, width 16 |
| `ridge-w` · `ridge-e` | `line` | the frontline shoulder in two runs, 15→18→16 and 16→18→15, width 11 |
| `gully` | `line`, 4 pts | 9→6, the tributary draining the hollow into the river |
| `dell` | `point` r7 | a hollow at 14 inside the wood, so the hill is not one hump |
| `hollow-1/2/3` | `area` | 10, then 7, then 4 — three nested rings, each written after the one it sits inside |
| `shelf` | `area`, 9 pts | the monument plateau, flat at 21 |
| `shelf-face` | `scarp` | 21 ↓ 13 over a 5-wide face with a 6-block band |
| `saddle` · `knoll-ramp` | `line` | 13→19 both, the two graded ways up |
| `knoll` | `point` r8 | the house hill: a pinned disc, so its top is flat by construction |
| `hamlet` · `apron` | `area` | 14 and 12 — the cottages' shelf and the ground the spawn door opens onto |

The three pushes are the organic half: `forest-hill` (a 7-vertex ring, amount 8 varying 6→9 per vertex,
falloff 12, roughness 0.4, crown 3), `east-spur` off its flank, and `west-cape` behind the shelf.
A push composes where a mark would argue, so the spur adds to the hill rather than restating it.

**A push lifts a mark.** Applied to the solved surface, a push over an `area` mark raises that mark's
cells too, so a flat top under a push is not flat. Every plateau here is therefore made of marks and
every rolling hill of pushes, and no push ring overlaps an area ring.

**The order is load-bearing.** The rim is written first: a rim written after a ridge that reaches the
outline cuts a doorway through both its ends. The hollow's three rings are written outward-in, because
a later mark wins a contested cell — that, and nothing else, is what stacks the steps.

### What the terrain charges

Transects, read column by column (`GET /map/{slug}/column`):

| Where | Reading |
|---|---|
| across the shelf, `z = 90`, `x −56 → 0` | void, void, **y9** at the coast, **+9** to y18, y20 flat from `x −44` to `x −8`, then down |
| up the scarp at `x = −35`, `z 62 → 88` | 6, **+6**, 12, 13, **+2**, **+3**, **+3**, 21, then 20 flat — a face nobody walks up |
| up the east end at `x = −12`, `z 62 → 88` | 14, 14, 15, 15, 16, 17, 18, 19, 20, 20 — **+1 the whole way**, the one walk-up |
| across the hollow, `z = 58`, `x −52 → −24` | y6, y3, y3, y6, y9, y10, y11 — the three benches, read as steps |

The scarp's own crossing count is `onFoot 0, withBlock 0, descended 13` over 18 rows. It is a **one-way
face**: attackers fall off it toward the river, and get back up only round its east end or by building.
That is the whole composition of the objective — the ground picks the approach, not a wall.

### What the walk charges

A transect reads one column at a time. `GET /map/{slug}/walk` reads the whole board at once, in the units a
player pays in: how far it is in blocks, how many blocks must be placed to get there — a rise of Δ costing
Δ−1 — and how many falls over three the way takes.

**Elderwold is walkable almost everywhere.** Of 26,816 ground cells, **20,769 — 77.5% — cost nothing at all**
to reach from red's spawn, and 92.4% cost three blocks or fewer. That is `step: 1` with `stairs: true` doing
exactly what it was set for: a relief that climbs to y26 over a base of 12 and hands a player a staircase
everywhere it does it. Only 151 cells, 0.6%, cost more than eight.

The ford is confirmed from the other direction. The straight crossing `(0, 30) → (0, −30)` costs **60 blocks
for a 60-block line** — no detour, no placed block, no fall — because the river mark peaks at `h 9` where its
neighbours sit at 6, and the cobble path lands on top of it. Thirty blocks west the same crossing costs
**77 for 60, and 11 placed blocks**.

**On the lines that decide the match the board is fair to within one block.**

| Journey | Distance | Placed | Falls |
|---|---|---|---|
| red spawn `(0, 140)` → blue's cairn `(19, −91)` | 239 | 0 | 0 |
| blue spawn `(0, −140)` → red's cairn `(−20, 90)` | 238 | 0 | 0 |
| red spawn → its own cairn | 58 | 1 | 0 |
| blue spawn → its own cairn | 57 | 1 | 0 |

The one block is the cairn anchors themselves: `x −20` against `x 19`, not `±20`. Attacking costs 4.1× what
defending costs.

**The flanks are not fair, and the walk is the only read that says so.** Under the plan's own `rot_180`,
`(x, z)` and `(−x, −z)` are the same place. Six of ten sampled pairs answer identically in both distance and
placed blocks. The four that do not are all in the river corridor and on the coasts:

| Pair | From red | From blue, mirrored | Apart |
|---|---|---|---|
| `(−24, −16)` ↔ `(24, 16)` | 173 blocks, 0 placed | 166 blocks, **11 placed** | 11 blocks a player must build |
| `(−43, −21)` ↔ `(43, 21)` | 191, 13 | 179, 10 | 12 distance, 3 placed |
| `(−46, 0)` ↔ `(46, 0)` | 165, 3 | 159, 0 | 6 distance, 3 placed |
| west coast `(−50, 120) → (−50, −120)` | 251, 27 | 238, 12 | 13 distance, 15 placed |

The cause is one column deep. At `(−24, −16)` the ground is **gravel at y5**, in the river bed; at its mirror
`(24, 16)` it is **sand at y17**, on the bank — twelve blocks apart at two cells the symmetry calls one. Two
cells north and two south of each, the pair matches exactly: `(−24, −14)`/`(24, 14)` both y5, `(−24, −18)`/
`(24, 18)` both y16. The channel's shoulder simply lands at a different `z` on the two halves. The relief
mark is not at fault — its point list is rotationally symmetric on its own — so what moves the edge is what
is laid over it unmirrored: the `grain` field at `seed 5`, and the water props' `shoreWander`.

**The falls are real and off the fought-over lines.** Every spawn-to-cairn journey takes none. Reaching
3,114 cells takes one fall over three, 114 take two, and five take three; the deepest single fall on the
board is **twelve blocks, at `(49, 0)`**, the river's east end, with ten at `(42, −52)`. Drawn as a field the
pattern is the terrain's own commitment: the eastern flank and a western wedge can only be entered by
dropping off something.

**`comfort` and `travel` agree nearly everywhere here**, which is what a board with no interior void should
do — the only edge to keep off is the coast, and the routes that matter run down the middle. They part on the
west ridge, `(−38, 60) → (−38, 10)`: travel takes 52 blocks placing 3, comfort 57 placing 4, buying itself
room on a shoulder the short way runs along.

## The paths are used twice

Eight path props, and only three of them are roads.

| Prop | Style · radius | Is |
|---|---|---|
| `road` | `solid` 2.5, gravel-over-cobble `cell` | spawn door → hamlet → the saddle → past the shelf → the ford. 14 points, the spine |
| `wood-track` | `worn` 2.0, a `noise` of coarse dirt / podzol / gravel | the east flank route through the wood |
| `house-track` | `tapered` 2.0, coarse dirt | the spur up the knoll to the cottage |
| `tex-shelf` | `rough` **10.0** | the worn fighting ground around the monument |
| `tex-hollow` | `rough` **9.0**, a gravel/dirt/stone `voronoi` | the pan on the hollow floor |
| `tex-heath` | `worn` **11.0** at coverage 0.45 | trampled heath between the two shoulder ridges |
| `tex-strand` | `stones` 4.5, sand-and-gravel `cell` | the shingle along the river |
| `yard` | `rough` 5.0, cobble `cell` | the cottages' yard |

The last five carry no traffic. A path replaces the surface finish and adds no cell, so a wide one is a
**brush**, and it is how a board painted by a single theme gets dedicated ground. The map has exactly one
theme (`elderwold`: a `void`-edged voronoi rim, a `noise` grass-and-coarse-dirt surface over two dirt, a
stone/andesite/cobble `voronoi` wall, stone fill) and five distinct kinds of ground.

**The cost is that nothing can stand on them.** `DR-ROAD` keeps a tree three blocks and a boulder two
from the nearest paved cell, so a texture patch is an exclusion zone as wide as itself. Painting the
forest floor was the first thing tried and it is not available: it would have refused every tree in the
wood. Texture belongs where the ground is meant to be open, which turned out to be the same places a
designer wants bare anyway — the fighting ground, the pan, the heath, the shore.

## The wood

53 template oaks in the authored half, 106 on the map, heights 8–14 with the mass at 9–11.
They are **dart-thrown**, not latticed: a jittered lattice either reads as a grid or breaks its own
spacing, and the spacing is exactly what the claim rule costs.

The claim is height-dependent. Measured against the pass over four builds, two oaks clash below a
Chebyshev separation of about `(hₐ + h_b) / 5`, and the crown is hash-keyed off the seed, so the same
pair of heights does not always claim the same ground — a `(9, 11)` pair at Chebyshev 4 survived in one
build and was declined in the next. The placer uses `/4.7` as the divisor, which is that fit with a
margin on it, and the board builds with **nothing declined**.

The wood is one mass on the east hill the `forest-hill` push raised, with the `wood-track` cut through
it as a ride; a stand west of the hollow, a belt over the east ford approach, and a hedgerow of ten along
the road. Four buildings a side: the cottage on the knoll, two along the road below it, and a byre out on
the heath. Nine flora areas, five boulders.

## What went wrong

**The ford drowned.** The relief states the river's bed per vertex, rising to 9 at the centre where the
road crosses. The water prop cut it flat anyway: at `(0, 0)` the bed came out at y3 with two blocks of
water over it, the bar dredged away. This is `S46`, open and named in `relief.md` §9 — the dressing
channel does not read the relief. The fix is to author **one arm** rather than one river: the west arm
runs `x −58 → −9` and stops short of the axis, and the rot_180 fan draws the east arm, which is the same
curve because the centreline is odd-symmetric. The 18-block gap between them is dry, the road paves it,
and `(0, 0)` now reads cobblestone at y8 with the water at y4–5 either side.

**The scratch loop lied for two rounds.** `PUT …/sketch/from-plan` merges, and a relief is carried across
under its own rule — so posting a *changed* relief to a map that already had one returned 200 and built
the old terrain. The readback moved (it reads the posted body) while the render did not (it builds the
stored document), which is exactly the shape of a silent failure. The plain `PUT …/sketch` replaces.

**The hollow started on the coast.** Its first three rings ran to `x −56` where the coast is at −55, so
it read as a bay rather than as a basin. Moved 8 blocks inland it reads as what it is.

## Coordinates

| Thing | At |
|---|---|
| monument (red) | `<cuboid id="endstone-cairn-region" min="-21,25,89" max="-17,29,93"/>` — 4×4 ender stone, floating 4 over a plateau whose top is y20 |
| monument (blue) | `min="18,25,-92" max="22,29,-88"` |
| spawn (red) | piece `x −10..10, z 130..150`, marker `(0, 140)`, door facing −Z |
| the walk-up | `x ≈ −12`, `z 62..80` — the only on-foot way onto the shelf from the south |
| the ford | `(0, 0)`, cobble at y8; water y4–5 from `x ±9` outward |
| the hollow's floor | `(−40, 58)`, y3; its benches at y6 and y9 |
| the knoll | `(22, 114)`, flat at y20, radius 8 |
| highest ground | y26 (the `west-cape` push); build ceiling 46 |
| the deepest fall | `(49, 0)`, twelve blocks, at the river's east end; ten at `(42, −52)` |
| where the symmetry breaks | the river's shoulder, `(−24, −16)` at y5 against `(24, 16)` at y17 |
