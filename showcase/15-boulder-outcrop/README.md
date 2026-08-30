# 15 — a rock, at three scales

**The technique: one outcrop of stone breaking out of the ground, stated three different ways — a placed
prop, a sculpted push, and an erected shape — so a reader can see which instrument suits which size.**

The plan is `02-theme`'s, untouched but for `meta.name`. The finish adds a `relief` block on island `team`,
two `addShapes` entries and four `dressing.props` boulders — the rock in the middle of the board, the four
boulders in a row either side of it so one render carries all four forms.

## The document

The push that swells the ground before the rock breaks it:

```json
"relief": { "team": { "base": 9, "pushes": [
  { "id": "swell",
    "ring": [[-6,0],[0,-3],[6,2],[6,13],[0,16],[-6,10]],
    "amount": 6, "falloff": 9, "roughness": 0.4, "crown": 3, "seed": 11 }
] } }
```

The rock itself, erected clear of the ground it stands in:

```json
{ "id": "crag", "type": "polygon", "operation": "add", "override": true,
  "floor": 0, "base_height": 17, "height_mode": "level", "skirt": 0,
  "relief_scope": "exclude", "theme": "outcrop",
  "vertices":       [[-6,-10], [4,-12], [6,0], [-4,2]],
  "anchor_heights": [   10,       13,     24,     17   ] }
```

The same ring, painted rather than sculpted, so the swell's own crest reads as broken rock instead of grass:

```json
{ "id": "scree", "type": "polygon", "operation": "add", "override": true, "theme": "scree",
  "vertices": [[-6,0],[0,-3],[6,2],[6,13],[0,16],[-6,10]] }
```

Debris at the rock's foot, one of four:

```json
{ "kind": "boulder", "x": 18, "z": 8, "form": "outcrop", "size": 4, "mossy": true,
  "rock": { "kind": "solid", "id": 4, "data": 0 }, "seed": 3 }
```

## Three instruments, one rock

**A boulder is a prop.** It is placed at a point, it is a few blocks across, and — the fact that decides
everything else about where it may stand — it is stamped into a box of *air*: `BoulderShapes.Of` fills an
ellipsoid seated on whatever ground is already there, and the pass never rewrites a wall, a roof or a post to
make room for one. Four forms are one lobe list each (`GET /api/terrain/boulder-forms`): `round` is an
erratic — a main mass standing on the ground with a haunch and a shoulder on seeded bearings, 30% of its
height bedded in — `angular` the same rock with its surface broken, `outcrop` wide flat lobes whose middle
stays at the surface (a slab, not a rock, and the one form that genuinely emerges), and `cairn` three
shrinking lobes stacked. `showcase/25-trees-and-boulders` is the technique on its own. `rock` is a full
`TerrainMaterial`, resolved in the boulder's own frame before it knows where on the map it lands — the cairn
here is a `voronoi` of two blocks, not a `solid`, which is one of the fourteen pattern kinds the surface
paint uses.

**A push is sculpting.** `docs/world-export/relief.md` §2.2: the `amount` lifts the push's interior over the
solved field, and `crown` adds height at the shape's own medial axis — a point for a round push, a line for a
long one. The ring here is a lobed hexagon, closer to round than to a ridge, so `crown: 3` domes it rather
than ridging it. Measured: `relief/read` answers `high: 18` against `base: 9` — exactly `9 + 6 (amount) + 3
(crown)`, the field's own peak, with nothing hand-tuned to land there.

**An erected shape is architecture standing on the field rather than shaped into it.** `06-ramp-and-slant` has
the worked account of `anchor_heights`, the triangulated top and the `<maxbuildheight>` cost of standing a
shape up — read it for that; it is not repeated here. What is new here is the *shape* of the four heights:
06's slab fell smoothly corner to corner. This one's anchors are `10, 13, 24, 17` around a quadrilateral whose
short north edge (`10`→`13`) barely clears the ground and whose adjacent corner (`13`→`24`) climbs eleven
blocks in about twelve — a near-vertical face on one side of the crag and a shallower back on the other,
which is what makes it read as a single tilted spire rather than a ramp that got tall.

## Grouping: why every rock is where it is

A boulder scattered on open grass is dressing nobody placed; the same boulder at the foot of a crag is scree.
So nothing here stands alone. The push swells the ground first — a grass shoulder rising out of the field —
and the crag stands at its crest, erected clear of the swell so its base sits *in* the mound rather than
beside it. One instrument answers "is there a rock here at all", the second answers "how big is the ground
around it", and the third answers "what fell off it" — the same rock, at scales fifteen blocks apart from
largest to smallest.

**The four boulders stand in a row rather than at the crag's foot, and the objectives are why.** Each cairn
keeps a 21-block clearance and both sit in the board's middle band, which is where the crag is; a boulder
inside one is `OB19` and is dropped (below). So the four forms are laid out at `x ±18` and `x ±28` on `z 8`,
which loses the "scree at the foot of the rock" reading and buys the one a showcase needs more: all four
forms in a single picture, at the same scale, over the same ground.

## What went wrong first

**A boulder inside a goal's clearance is dropped, and it is the objectives that do it here.** With the
`outcrop`-form boulder left at `(0, −16)`, in the middle of the board where the crag is, the build answered:

```
[decline] OB19  boulder '' rests on (0, -20), inside a goal's clearance
```

`DressingScope.GoalStandoff` is ten blocks, so each cairn keeps a 21-block square round it — `x −10..10,
z 12..32` for the one at `(0, 22)`, and its image for the other. That is a quarter of the board's middle band
gone, on a board whose objectives sit near the centre, and it is why the four boulders stand at `x ±18` and
`x ±28` rather than under the crag. The prop is not in the world; nothing else about the build complains,
because a decline costs nothing but the boulder.

**The one that was not deliberate, and cost the whole group.** The crag's dark accent band was first authored
as Gray Wool (`35:7`) — a natural-looking charcoal grey next to Stone's mid-grey, and a good contrast on the
swatch. Every boulder placed anywhere near the outcrop then declined:

```
[decline] DR-KEEP  boulder '' rests on (-5, 4),  which is built ground rather than terrain
[decline] DR-KEEP  boulder '' rests on (2, -2),  which is built ground rather than terrain
[decline] DR-KEEP  boulder '' rests on (-2, 8),  which is built ground rather than terrain
[decline] DR-KEEP  boulder '' rests on (4, -10), which is built ground rather than terrain
```

`BlockRoles.IsBuilt` names a fixed set of block ids the dressing pass reads as *construction* rather than
*terrain* — wool, sandstone, bricks, stone bricks, quartz among them — and id 35 (wool) is in it regardless of
which of the sixteen colours it is. Painting the crag's own crown with wool made every column under it read as
a structure, and since a boulder's footprint is an ellipsoid several blocks wide, a boulder placed several
blocks *away* from the crag still had part of its skirt land on a wool-topped cell and the whole prop
declined — not the boulder centred on the crag, every boulder near it. The fix was a material swap, not a
placement one: Coal Ore (`16:0`, a near-black grey and not a member of the built set at all) gives the same
dark accent and reads as ore in rock rather than as a colour choice, and every boulder that had been declined
built on the first retry with no change to where it stood.

**The one still worth watching: a prop's footprint, not its point.** The `outcrop`-form boulder is the widest
of the four (`size: 4` → a lobe `1.45×` as wide as tall), so an anchor that clears a keep-out by a block or
two does not: the skirt alone crosses the line and the whole prop declines. A boulder's placement has to clear
a keep-out by its *reach*, not by its anchor — the same lesson the road standoff (`DR-ROAD`) states for a tree
or a boulder near a path.

## What to look at

| Picture | Says |
|---|---|
| `GET …/render/section?axis=x&at=-6&from=-20&to=20&scale=10` | the crag alone — the jagged, near-vertical spire with its dark cap |
| `GET …/render/section?axis=z&at=0&from=-20&to=20&scale=10` | the crag *and* the swell together — a grass shoulder cresting into rock, which is the whole idea in one cut |
| `renders/world-ground.png` | the plan view: the dark crag in the middle and all eight boulders — four forms, twice — laid out either side of it |
| `renders/world-structure.png` | `?subject=structure` — spawn and wool in solid orange, the boulder claims as the stippled "other (context)" patch at the same coordinates, from the provenance sidecar rather than from a block-colour guess |
| `renders/boulder-round-section.png`, `-angular-`, `-outcrop-`, `-cairn-` | the four forms from `/terrain/prop-preview`, at card size, over the `scree` theme so the moss and the dark fleck read as they will on the board |
| `renders/theme-scree-surface.png` | the swatch: Stone/Coal Ore voronoi speckle, mottled rather than banded, because a domed push has no consistent "inward" to band against |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is `02-theme`'s, untouched |
| `POST …/sketch/relief/read` | island `team`: cells 10 000 · low **9** · high **16** · relief 7 · symmetry error **0** |
| crag, near its tallest vertex (anchor 24) | measured **y17** at `(2, −4)`, **y14** at `(0, −6)`; **y9** two cells outside the polygon at `(±8, −5)` — a sheer face, `skirt: 0`, exactly as stated |
| boulder heights, centre column against the y8 meadow beside them | round `(−28,8)` **y11** = 3 proud · angular `(−18,8)` **y12** = 4 · outcrop `(18,8)` **y10** = 2, low and wide as the form promises · cairn `(28,8)` **y12** = 4, three stacked lobes |
| the round boulder's own column, dead centre | 12 solid blocks, **all `1:0` Stone**, bedrock to crown — its `rock` and the meadow's own fill are the same block, so a boulder on its own kind of ground is invisible to a column read; only the section shows it is there at all |
| provenance census (`python3 -c "…Counter(o['kind'] for o in owners)…"`) | `boulder: 8`, `spawn: 2`, `destroyable: 2` — one row per boulder per orbit image, 4 authored × 2 images, and no boulder has zero rows, which is what a declined one would have shown |
| `GET /api/terrain/blocks`, the two rock materials | Stone `#7e7e7e` vs Coal Ore `#373737` — the crag's own bands read apart from each other by the same margin Grass Block (`#79c05a`) reads apart from either, so the rock does not vanish into its own crown the way `02-theme` measured Stone/Andesite/Stone Bricks/Cobblestone vanishing into one grey |
| `GET …/coverage` | 2 451 reached · **639 decorated** · 69.1% dead — against `07-hill`'s 75.5% on the same base board; the props are what the extra 639 cells are |
| `GET …/preflight` | export gate **OPEN** — round-trip, mirror, buildability and traversability all pass |

## What this did not reach

A `layered` band pointed inward (§`03-paving`'s own limit) would have given the scree a graded edge — bare
rock at the crest thinning to a scattering of stones at the grass line — rather than the flat mottle it has
now, which is a `voronoi` speckle with no distance term at all. That grading is the same "inset is read once
per island, not per shape" limit `03-paving` already measured, and nothing here works around it; the swell's
edge is a hard cut from grass to rock rather than a taper.
