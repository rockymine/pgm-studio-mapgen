# 15 — a rock, at three scales

**The technique: one outcrop of stone breaking out of the ground, stated three different ways — a placed
prop, a sculpted push, and an erected shape — so a reader can see which instrument suits which size.**

The plan is `02-theme`'s, untouched but for `meta.name`. The finish adds a `relief` block on island `team`,
two `addShapes` entries and four `dressing.props` boulders, all grouped on the west flank between the
frontline and the field's own hollow.

## The document

The push that swells the ground before the rock breaks it:

```json
"relief": { "team": { "base": 9, "pushes": [
  { "id": "swell",
    "ring": [[-40,50],[-33,47],[-27,52],[-28,63],[-34,66],[-40,60]],
    "amount": 6, "falloff": 9, "roughness": 0.4, "crown": 3, "seed": 11 }
] } }
```

The rock itself, erected clear of the ground it stands in:

```json
{ "id": "crag", "type": "polygon", "operation": "add", "override": true,
  "floor": 0, "base_height": 17, "height_mode": "level", "skirt": 0,
  "relief_scope": "exclude", "theme": "outcrop",
  "vertices":       [[-39,40], [-30,38], [-28,50], [-37,52]],
  "anchor_heights": [   10,       13,       24,       17   ] }
```

The same ring, painted rather than sculpted, so the swell's own crest reads as broken rock instead of grass:

```json
{ "id": "scree", "type": "polygon", "operation": "add", "override": true, "theme": "scree",
  "vertices": [[-40,50],[-33,47],[-27,52],[-28,63],[-34,66],[-40,60]] }
```

Debris at the rock's foot, one of four:

```json
{ "kind": "boulder", "x": -33, "z": 34, "form": "outcrop", "size": 4, "mossy": true,
  "rock": { "kind": "solid", "id": 4, "data": 0 }, "seed": 3 }
```

## Three instruments, one rock

**A boulder is a prop.** It is placed at a point, it is a few blocks across, and — the fact that decides
everything else about where it may stand — it is stamped into a box of *air*: `BoulderShapes.Of` fills an
ellipsoid seated on whatever ground is already there, and the pass never rewrites a wall, a roof or a post to
make room for one. Four forms are one lobe list each (`GET /api/terrain/boulder-forms`): `round` is a single
buried sphere, `angular` the same sphere eroded by a noise field, `outcrop` a wide flat lobe (`rx=1.45×size`,
`ry=0.45×size` — a slab, not a rock), and `cairn` three shrinking lobes stacked. `rock` is a full
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
the crag stands at its crest, erected clear of the swell so its base sits *in* the mound rather than beside
it, and the four boulders sit at the crag's foot and along the swell's flank, each a plausible piece that
could have come loose from the rock above it: `angular` (freshly broken, no moss) against the crag's own
western face, `outcrop` (a low flat slab) further out on open grass to the north where the swell hasn't
reached yet, `round` and `cairn` on the scree's own shoulder to the south. One instrument answers "is there a rock here at
all", the second answers "how big is the ground around it", and the third answers "what fell off it" — the
same rock, at scales fifteen blocks apart from largest to smallest.

## What went wrong first

**The deliberate one.** A fifth boulder was placed at (-20, 80) — inside the twenty-block approach lane in
front of the spawn hall's own door — specifically to read the refusal:

```
[decline] DR-KEEP  boulder '' rests on (-21, 79), which is kept clear for a spawn
```

The prop is not in the world; nothing else about the build complained, because a decline costs nothing but
the boulder. Moved off the lane, it built.

**The one that was not deliberate, and cost the whole group.** The crag's dark accent band was first authored
as Gray Wool (`35:7`) — a natural-looking charcoal grey next to Stone's mid-grey, and a good contrast on the
swatch. Every boulder placed anywhere near the outcrop then declined:

```
[decline] DR-KEEP  boulder '' rests on (-30, 55), which is built ground rather than terrain
[decline] DR-KEEP  boulder '' rests on (-37, 43), which is built ground rather than terrain
[decline] DR-KEEP  boulder '' rests on (-33, 59), which is built ground rather than terrain
[decline] DR-KEEP  boulder '' rests on (-37, 60), which is built ground rather than terrain
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

**The one still worth watching: a prop's footprint, not its point.** The `outcrop`-form boulder (the widest of
the four, `size: 4` → a lobe `1.45× as wide as tall`) was first placed at `x: -31`, close enough to the spawn
hall's own approach lane (which reaches to `x: -30`) that its skirt alone crossed the line:

```
[decline] DR-KEEP  boulder '' rests on (-29, 61), which is kept clear as the approach in front of a door
```

A boulder's placement has to clear a keep-out by its *reach*, not by its anchor — the same lesson the road
standoff (`DR-ROAD`) states for a tree or a boulder near a path, here against a door instead.

## What to look at

| Picture | Says |
|---|---|
| `renders/section-crag-x48.png` | the crag alone, `axis=x` at `z=48` — the jagged, near-vertical spire with its dark cap |
| `renders/section-crag-z32.png` | the crag *and* the swell together, `axis=z` at `x=-32` — a grass shoulder cresting into rock, which is the whole idea in one cut |
| `renders/world-ground.png` | the plan view: the grey mass on the west flank of each mirrored island, boulders as small flecks at its foot |
| `renders/world-structure.png` | `?subject=structure` — spawn and wool in solid orange, the boulder claims as the stippled "other (context)" patch at the same coordinates, from the provenance sidecar rather than from a block-colour guess |
| `renders/boulder-round-section.png`, `-angular-`, `-outcrop-`, `-cairn-` | the four forms from `/terrain/prop-preview`, at card size, over the `scree` theme so the moss and the dark fleck read as they will on the board |
| `renders/theme-scree-surface.png` | the swatch: Stone/Coal Ore voronoi speckle, mottled rather than banded, because a domed push has no consistent "inward" to band against |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is `02-theme`'s, untouched |
| `POST …/sketch/relief/read` | island `team`: cells 4125 · low **9** · high **18** (`= 9 base + 6 amount + 3 crown`) · relief 9 · symmetry error **0** |
| crag, near its tallest vertex (anchor 24) | measured **y22**, one cell in from the vertex itself; **y13–14**, one to two cells outside the polygon — a sheer face, `skirt: 0`, exactly as stated |
| boulder heights, centre column above the ground just outside its own reach | round (on scree) **y19** vs **y16** local = 3 blocks proud, camouflaged (see below) · outcrop (on grass) **y10** vs **y8** local = 2 blocks, low and wide as the form promises · cairn **y20** vs **y14–16** local, tallest of the four (three stacked lobes) |
| the round boulder's own column, dead centre | 19 solid blocks, **all `1:0` Stone**, bedrock to crown — its `rock` and the scree's own `beyond` fill are the same block, so a boulder on its own kind of ground is invisible to a column read; only the section (above) shows it is there at all |
| provenance census (`python3 -c "…Counter(o['kind'] for o in owners)…"`) | `boulder: 8`, `roomfloor: 2`, `wool: 2`, `redstoneline: 2`, `spawn: 2` — one row per boulder per orbit image, 4 authored × 2 images, and no boulder has zero rows, which is what the declined fifth would have shown |
| `GET /api/terrain/blocks`, the two rock materials | Stone `#7e7e7e` vs Coal Ore `#373737` — the crag's own bands read apart from each other by the same margin Grass Block (`#79c05a`) reads apart from either, so the rock does not vanish into its own crown the way `02-theme` measured Stone/Andesite/Stone Bricks/Cobblestone vanishing into one grey |
| `GET …/coverage` | 3.3% dead — the same share `07-hill` reads on the same base board; a relief and its dressing move no ground and add no path |
| `GET …/preflight` | export gate **OPEN** — round-trip, mirror, buildability and traversability all pass |

## What this did not reach

A `layered` band pointed inward (§`03-paving`'s own limit) would have given the scree a graded edge — bare
rock at the crest thinning to a scattering of stones at the grass line — rather than the flat mottle it has
now, which is a `voronoi` speckle with no distance term at all. That grading is the same "inset is read once
per island, not per shape" limit `03-paving` already measured, and nothing here works around it; the swell's
edge is a hard cut from grass to rock rather than a taper.
