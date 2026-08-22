# Whitebarrow Down — a combined destroy board on chalk

> One destroyable and one core per team — the ordinary combined board — on a high chalk down:
> a standing stone on an open barrow lawn, a powder magazine sunk in a dell behind it, the two
> sides meeting across a saddle holding a dew pond, a beech hanger closing the west flank and a
> chalk scarp on the east that is climbed from the mid and bridged from at the top.

**In one sentence:** a chalk downland lane where each team defends the Barrow Stone (obsidian,
`pillar-3`) on open turf ringed by sarsens, and the Powder Magazine (a default core) in a
sunken dell east of it, with every approach paying a different price — turf and sarsen cover in
the open, trees on the west, height on the east, and a Δ2 lip wherever no ramp was cut.

100 × 190 blocks, `rot_180` about the origin, cell 5, four stated tiers 9 / 11 / 13 / 15,
16 players, build ceiling 37, observer at `(0, 56, 0)`. One landmass: the saddle piece crosses
the axis and fuses with its own image, so nothing on the board is bridged and
`voidEnforcement` seals the outside edge instead of a build-region list.

## Where the design's pieces are

| The board says | Where it is | Measured |
|---|---|---|
| combined destroy board | one `<destroyable>` + one `<core>` a team | `barrow-stone-region` min `-8,21,53` max `-7,24,54`, obsidian; `powder-magazine-region` min `23,17,53` max `28,22,58`; `<gamemode>dtm</gamemode>` + `<gamemode>dtc</gamemode>`, objective "Destroy the enemy's monument and leak the enemy's core!" |
| GO1 band kept | both goals at ratio 3.0 | destroyable own 50 / enemy 150; core own 60 / enemy 180 (`/plan/inspect`) |
| the stone in the open | area mark pins the lawn at 13; a push raises a 2-block tumulus under the stone | column `(-8,53)`: grass top y16, obsidian y21..23, red wool sky marker y42..44; nearest sarsen 12 blocks, nearest tree x ≤ −28, nearest building z ≥ 58 at x ≥ 5 |
| the magazine sunk behind | dell piece at 11 against down 13 and scarp 15 | core casing y17..21, lava y18..20 inside the shell; dell entered at grade from the apron (z=30 seam, both h11), by a Δ2 drop from the down, Δ4 from the scarp |
| dew pond in the mid | a point mark (h6 r7) dished the saddle; a water prop cut and filled it | column `(0,0)`: water y4..5 over a gravel bed, shore of clay/sand; pond ~16 × 10 |
| west flank = cover | 10 trees per side on the hanger tier (13) with a fern floor and a worn track | tree anchors x −45..−24, z 20..62; flank path `pa4` (−16,2)→(−38,28) |
| east flank = height | the scarp (15) reached only by the earthwork ramp `ramp-s` (x 34..40, 11→15) | scarp crest top y14 at `(45,40)`; its Δ4 west face overlooks the dell and the core |
| kit agrees with obsidian | `DestroyKitPairing` upgraded the pickaxe | `<item slot="2" material="diamond pickaxe">` |

## The tier model, and where the ways up are

Tiers are plan surfaces (9 saddle, 11 apron+dell, 13 down+hanger, 15 back+scarp), all odd, so
every seam is Δ2 — a lip that costs a placed block — except where a ramp was authored. Five
`level` + `anchor_heights` + `relief_scope: exclude` shapes are the ways up, each painted
`barrow-track`: `ramp-w` (west flank 11→13), `ramp-c1`/`ramp-c2` (the two frontal ramps
11→13, the funnel of the board), `ramp-b` (the defenders' road 13→15, paved by the main
track), `ramp-s` (the scarp climb 11→15, entered from the mid side — so the scarp is a
platform both sides fight for, not a defenders' balcony). The relief solves only the saddle
and the down/hanger tier: apron and dell are `hold` (the solved ground arrives at their
level), back and scarp are `exclude` (clean faces). Read back: island low 6, high 17,
symmetry error 0.

## What the ground is made of

Five themes, every `fill` diorite, so anything cut anywhere shows chalk.

| Theme | On | Says |
|---|---|---|
| `barrow-turf` (default) | saddle, apron, back | grown: rim off, a `cell` of grass with a sixth of coarse dirt over dirt, chalk-noise faces |
| `barrow-down` | the high down | worn turf: a `noise` run grass → coarse dirt → clay, thin soil (1+1 courses) straight onto chalk |
| `barrow-scar` | the scarp | bare: a `cell` of diorite/clay/polished diorite with a seventh of coal block — flint in the chalk — and a `layered` strata wall |
| `barrow-dell` | a same-height paint shape over the dell | worked ground: coarse dirt/podzol/gravel with a coal accent |
| `barrow-track` | the five ramps | a fine `cell` of gravel/clay/diorite, one course |

The flint accent appears in the scar, the dell and every building's walls, so it reads as the
board's material rather than a one-off. Buildings are flint-and-timber (cobble noise with coal
nodules, spruce, hay thatch): two `wb-cott` cottages, a `wb-barn`, a flat-roofed `wb-hut`
powder store by the dell track, and the `wb-spawn` hall bound as the spawn room style — all
forks of shipped presets with `wall` repainted (all have empty storey stacks, so the
half-fork trap does not arise). Structures read-back: **18 structures** over terrain
(2 spawn halls, 8 cottages+barns, 2 powder huts, 2 destroyable platforms, 2 core casings,
2 iron cubes), all seated within 1 of level ground except the hut (+1 over ground uneven by 3).

## How it is meant to play

The contested field is the saddle and apron — 60 blocks of open turf between the two Δ2 down
lips, interrupted only by the pond. A rush crosses it exposed; the ways around it are bought:
west under the hanger (cover, no height, the long way), east up `ramp-s` onto the scarp
(height over the enemy dell, no cover, and the same platform the defenders want). The
destroyable is defended from the brow above it (`m-brow`, h14) and from the back tier; the
core is defended by dropping into the dell from the down — the attacker enters it at grade
from the front through a 20-block mouth, or bridges down from the scarp. The two goals split
the defence laterally: stone west, magazine east, 33 blocks apart.

## What went wrong, and what it cost

- **A flora field can land zero blades and nothing says so.** `f2` (the saddle meadow,
  coverage 0.3, scale 10) produced no blades on either image at seed 32 — no decline, no
  warning; the only witness was a missing row in `region/provenance.json`. Changing the seed
  landed 13 blades; raising coverage to 0.5 landed the meadow. Coverage under ~0.4 at these
  scales is a lottery.
- **A building's claim is its footprint plus about two blocks.** The barn was declined three
  times (`DR-CLAIM` naming the neighbour) before it stood: a shared row, then a one-block gap,
  then a two-block gap against a cottage still collided; buildings need ~4 blocks between
  footprints, and the spawn shell claims ~2 outside itself too.
- **Two sarsens and a boulder stood in the road and the pond's shore** — `DR-ROAD`/`DR-CLAIM`
  declines, each naming the colliding cell; moved.
- **`axis: "down"` is not a word** — a layered wall's axis is `depth`/`inward`
  (`/terrain/patterns` carries the choices; the refusal named only the path).
- **Coverage reads the open field as dead** (48.7%; the two symmetric patches at (±23,∓3) are
  the saddle/apron flanks). Recorded as an open question in the run report rather than
  designed away: on a destroy board that ground is the fight front, and `approaches.md` wants
  it larger and emptier than a capture board's — but no oracle was available to settle whether
  48% is too much of it.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red Barrow Stone | `(-8..-7, 21..24, 53..54)` | obsidian `pillar-3`, floats 4 over mound top y16 |
| red Powder Magazine | `(23..28, 17..22, 53..58)` | obsidian shell, lava y18..20, ground y10, floats 6, leak 5 |
| dew pond | `(0,0)` ± 8 | water y4..5, gravel bed, clay/sand shore |
| observer perch | `(0, 55, 0)` | bedrock pad over the pond (the plan's only observer control) |
| scarp crest | `(45, 40)` | top y14, clay/diorite; Δ4 faces west and south |
| scarp ramp foot | `(37, 12)` | h≈12 rising to 15 at z 28..30 |
| barrow lawn | `x -18..2, z 44..62` | held flat at 13 by an area mark, +2 tumulus push |
| west neck path | `(-16,2) → (-38,28)` | worn gravel/clay track under the hanger edge |
| village street | `z ≈ 68, x -22..10` | worn track; cottages at (5..12, 58..64), (13..19, 68..74), (-24..-18, 64..70); barn (-19..-10, 76..82) |
| spawn hall | `(0, 90)` | flint walls, dark oak roof y23, red wool pad y14 |
| main track | `(0,84) → (2,10)` | spawn door → defenders' ramp → east of the lawn → frontal ramp → pond edge |
