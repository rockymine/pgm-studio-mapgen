# Fallowmere — the shared basin, left open

> Sonnet B's reading of `rockymine-map-experiment`: the same canal, the same single bridge, the same
> edgy coast every one of the three boards was asked for — and then less of everything else.

**In one sentence:** a walled canal cut between two quiet grass banks, crossed by one stone bridge a
worn trail actually uses, with a hollow dug under the forward goal, a lone knoll-island either side of
the crossing, and just enough made — a croft, a grounded biplane, a rowboat, a scatter of stone — to
give the ground a reason without covering it.

260 × 250 blocks (`s0`'s own west tip runs two past the stated bbox), `rot_180` about `(0, 0)`, 12
players, `cell: 5`. Driven from `specs/sonnet-fallowmere/build.py`, which loads the shared base fresh
from `specs/rockymine-map-experiment/` on every run and writes the plan, layout and intent beside
itself — no `finish.json`, because the driver now compiles from the plan whenever one exists at all,
and this board's geometry is the hand-authored layout.

## Where the brief's things are

| The brief asked for | Where it is | Measured |
|---|---|---|
| the dip is water | `s0`, the 11-vertex basin, filled to a stated level | `canal-water`, `shape: pool`, `points: s0`, `level: 23`; bed dished by relief to y9–16 |
| the canal walled, sampled never | `wall-n` / `wall-s`, thin paths tracing `s0`'s shared edges with `s1`/`s2` | override, `relief_scope: exclude`, floor 15 → top 30, `keepClear: true` |
| a bridge, a route not scenery | one arch at `x=-70`, and a worn stroke from the spawn door across it to the far goal | deck 33→36→30 (y), water span z 39..70; `route` stroke `radius 2.5`, `route: true` |
| three themes, no more | `sward` (both banks), `holt` (the island), `wrought` (the masonry) | `painted: {'wrought': 5, 'sward': 2, 'holt': 1}` shapes at store time |
| no premade theme | all three authored in `build.py` | none named `grass clay`; every material a `noise`/`solid` pair chosen here |
| one house style, a variation at most | `croft-bank` forked from room-style **6** ("cottage"); `croft-north` the same JSON with oak swapped to ash plank and diorite verge to stone | `GET /room-styles/6/json`, then a recursive block-id swap |
| both tree forms, on the right ground | 5 grown oaks (`whorled: false`) on `sward`; 3 grown spruces (`whorled: true`) on `holt` | oaks `leader 0.5`; firs `leader 0.8`, both `form: grown` |
| four boulder forms, more than one size | round, outcrop, cairn ×2, angular — sizes 3, 4, 5, 6 | `BOULDERS` table in `build.py` |
| a pit under a destroyable, a goal in a dip | `goal-hollow` push, `amount -6 crown -3`, centred on destroyable-1's own anchor | destroyable-1 `(-90, 18)`; ring read `low=10` inside `team`'s relief |
| props placed for a reason | a rowboat in the water it costs nothing extra to sit in; a grounded biplane on the flat the croft's own yard reaches | `boat-*` and `plane-*` prop layers, `kind: "prop"` |
| no sky-writing | none authored | — |
| the outline stays edgy | `s0`/`s1`/`s2`/`s3` carry their drawn vertices unchanged, no `controls` on any outer edge | `S0`/`S1`/`S2` in `build.py` are the base's own arrays, verbatim |

`G5` (`gap-hop-band`, the base's one hard failure) is fixed by the same plan-piece rects the reference
board used — `piece → [-21, 14, 23, 10]`, `piece-4 → [1, 5, 10, 9]` — verified against a live
`POST /plan/evaluate`: `valid: true`, `G5` gone, without moving anything the layout actually draws.
`GO1`, `GO2`, `GO3` read exactly what the brief measured off the untouched base (`2.511`, `111`, `205`
for the far goal), because the two destroyables are the author's and neither was moved.

## The one thing every board here had to answer, and how this one did

**The canal doesn't get a gate cut in it — the bridge rides over the wall instead.** The first attempt
cut a gap in `wall-n`/`wall-s` at the crossing's own width, on the reasoning that a bridge wants an
opening. Read back, that gap bared the raw seam between two flat relief marks — the bank pinned at 30,
the bed pinned at 16, nothing graded between them because both are hard constraints — and the result was
a 16-block sheer drop sitting where neither a wall nor a deck covered it. The fix was to stop cutting the
wall at all: it runs unbroken along both banks, and the bridge's own deck — starting at bank height,
because the wall's top and the bank it retains are one number — simply crosses over it. Short of the
true water the deck is a two-course causeway; over it, an arched soffit springs from a mid-stream pier so
the race runs through the opening rather than against a dam. Measured on the built world at `x=-70`: top
29 → 29 → 30 → 32 → 36 (the crown, over the pier) → 32 → 30 → 29, no step anywhere in that run over two.

## What the ground is made of

| Theme | On | Says |
|---|---|---|
| `sward` | `s1`, `s2` — both banks, hills included | grown: solid grass surface, a dirt-over-stone wall, a stone-granite fill |
| `holt` | `s3` and its image — the island, kept its own | grown: coarser, coarse-dirt/podzol surface, stone-mossy-cobble wall and fill |
| `wrought` | the canal wall and the bridge | built: stone-brick/andesite surface, stone-brick/chiseled wall and fill — the one theme that reads as made rather than grown |

Two banks share one ground on purpose — the water is what tells them apart, not a second palette — and
the island keeps the third for the same reason `holt` differs at all: it is a different place, not a
different patch of the same one.

**`sward`'s surface was first authored as `noise(grass, podzol, scale 22)`, and that was wrong the same
way the author has already ruled against once.** Grass and podzol are two different families — green
against dark brown — not two shades of one, so `world-iso.png` came back a speckle rather than a ground:
the exact "podzol and dirt and grass together clash a lot" the author named on an earlier board. The
reference board's own `moor` answers this by not pairing at all — a solid grass surface, with the noise
kept for the wall and fill, where a mottled reveal is the point rather than the fault. `sward` now does
the same: `theme(GRASS, noise(DIRT, STONE, ...), noise(STONE, GRANITE, ...))`, solid on top. Read back,
both banks are one unbroken green in `world-iso.png` — `holt`'s own pairing (`3:1` coarse dirt against
`3:2` podzol) was never the problem, since both stops are the one dirt family already.

## The relief: two flat marks, then whatever rolls

`TEAM`'s marks are three flat pins — the whole basin at `y16`, the whole of `s1` and the whole of `s2`
at `y30` — laid down first so the wall has a clean, unrolled face to stand on the whole way round. The
pushes come after: two gentle +5 rises well clear of the crossing and the goal (`north-rise` centred
`(-38, 116)`, `south-rise` at `(-32, -6)`, both `falloff 18`), the `goal-hollow` pit under destroyable-1,
and a `canal-dish` push over the basin's own footprint that curves the already-flat bed down toward its
centreline (`crown -3`) rather than leaving it a table. `ISLE` gets one knoll, `+5` over a wide falloff.
Read back: `team` cells 14249, `y10..38` (a relief range of 28 — almost all of it the deliberate 15-block
wall face, not the rolling ground either side of it); `isle` cells 1774, `y26..33` (range 7, a proper
gentle knoll).

## What the driver kept saying, and what was done about each

- **`SK10`, 7 blocks over 164 columns at the bridge's own footing.** The thin causeway that carries the
  deck across the wall shares more than the one course the two layers are allowed to agree on before this
  fires. It is the cost of the causeway being thin (two courses) rather than the alternative — a causeway
  thick enough to duplicate the wall's own mass — and it costs nothing visible: the wall's blocks are
  simply repainted in the bridge's material for two of the fifteen courses under the deck.
- **`SK11`, three patches (11108 + 3634 + 3627 cells).** `render/traversability` and `SK11` answer
  different questions and cannot contradict each other — one asks whether the built world is walkable at
  all, the other whether a relief group's own solved field shows a standable mass with no route drawn
  onto it — so a green traversability read is not by itself a reason to doubt this finding, and an
  earlier pass here reasoned as if it were. What actually settles it is a walk: flooding the built columns
  from spawn over the ground and spans layers together, climb 1 and drop 3, reaches every cell all three
  patches name, including `(-92, 16)`, which the largest is centred on. Disabling the goal-hollow push
  changed nothing (11108 → 11108) either, which had already ruled the pit out as the cause. Read against
  `GET /api/rules?rule=SK11`'s own words — "a second landmass the author meant... or leave it if a
  detached landmass is what the board is" — the finding is the board's two masses either side of the
  middle void: the shared base's own shape, a destroy board's two team territories joined only by the
  build zone at the intent tier and never by land, not a defect introduced here. Left, as the rule says
  to.
- **`RL2`, 28 blocks of range, 257 barrier steps.** Read together with the heightmap's own contour
  rings — smooth, evenly spaced, no terracing — this is the wall again: a deliberate 15-block masonry
  face reads exactly like an ungraded barrier to a rule that cannot tell a retaining wall from a cliff
  nobody meant. The rolling ground either side of it is graded on purpose (`grain amplitude 0.5`, pushes
  at `falloff 18`) and reads that way in the picture.
- **`WX11` ×2, destroyable-2 two blocks proud of the cell beside it.** The base's own placement,
  untouched; a doorstep rather than a wall, and not worth re-grading a goal the brief says stays where it
  is.

**The biplane read as an aircraft from above and as a plank cross from the side.** Its wing was a single
course resting on top of the fuselage rather than a box through it, and the tail fin barely cleared the
fuselage's own height. Both were cheap to change: the wing is now two courses deep, floored level with
the fuselage rather than above it, so it has volume where it crosses rather than sitting on the surface
like a lid; the fin is five courses instead of three. `closeups/airplane.png` shows the wing box plainly
now. A true side elevation still reads it as low and long rather than as a silhouette a player would call
a plane from across the map — the model is eleven blocks long and four tall, which is a scale a wing box
and a taller fin can make readable in plan but not fully in profile — so this is the honest ceiling of a
cheap fix rather than a full one.

## Coverage — the number this board is steering by

`reached 18429 · decorated 1561 · dead 11141 · of 31131 = 35.8% dead`. The dead ground is not scattered —
`coverage.png` shows it as a border, the perimeter strip of every landmass outside the direct
spawn-to-goal line the route actually walks. A board built to breathe is exactly a board where the ground
a player is not on the way to is still there rather than paved or planted, and this is the honest cost of
that: fewer routes drawn than a tighter board would carry, so more of each coastline reads as `dead`
rather than `decorated`. The dead patches themselves are the coastal fringe and the far side of each
island, at `(41,-110)`, `(-43,107)`, `(-104,56)` and their mirrors — shoreline, not unfinished map.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red spawn | `(-90, 105)` | door `-z`, faces the canal |
| destroyable-1, "Red Monument" | `(-90, 18)` | across the canal from spawn; sits in `goal-hollow`'s own dip, `y ≈ 21` at centre |
| destroyable-2, "Red Monument 2" | `(-15, 98)` | same landmass as spawn, no relief mark of its own |
| the bridge | `x = -70`, deck `z 33..76`, water `z 39..70` | crown `y36` over one pier at `z ≈ 55`, `pier_foot y15` |
| the croft | `(-101..-93, -6..1)` | `croft-bank`, forked room-style 6, door `posZ` |
| the second croft | `(-68..-60, 84..90)` | `croft-north`, the same style repainted, door `negZ` |
| the rowboat | `(-100, 52)` | keel `y20`, hull to `y25`, moored west of the crossing |
| the grounded biplane | `(-64, 3)` | fuselage `y29..31`, wing box `y29..31` through it, fin to `y34` |
| the yard route | `(-83,26) → (-77,12) → (-70,5) → (-64,3)` | a worn branch off the crossing's own approach, passing east of the croft rather than through it |
| the island knoll | centred `(48, 50)` | `+5` push, `y26..33` read back |

## What to look at

`specs/sonnet-fallowmere/renders/world-iso.png` and `world-iso-turned.png` are the board in the round;
`world-heightmap.png` is the contour read the relief section above is measured against;
`world-traversability.png` is the walkability read `SK11` is not asking (see above);
`specs/sonnet-fallowmere/closeups/bridge-crossing.png` is the arch from the water; `boat-in-canal.png`
and `airplane.png` are the two new props at a scale that reads them; `yard-house-airfield.png` is the
croft, the route and the boulders together.
