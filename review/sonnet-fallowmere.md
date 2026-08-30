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
| `sward` | `s1`, `s2` — both banks, hills included | grown: grass-podzol noise surface, a dirt-over-stone wall, a stone-granite fill |
| `holt` | `s3` and its image — the island, kept its own | grown: coarser, coarse-dirt/podzol surface, stone-mossy-cobble wall and fill |
| `wrought` | the canal wall and the bridge | built: stone-brick/andesite surface, stone-brick/chiseled wall and fill — the one theme that reads as made rather than grown |

Two banks share one ground on purpose — the water is what tells them apart, not a second palette — and
the island keeps the third for the same reason `holt` differs at all: it is a different place, not a
different patch of the same one.

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
- **`SK11`, three patches (11108 + 3634 + 3627 cells).** This is the finding this board spent the most
  time on and did not clear. `relief/read`'s own walk measures the `team` group's solved field with a
  two-block join bound, and it reads the far side of a walled, single-bridge canal as unreached — which
  is close to what a wall is *for*. What it is not measuring is the actual crossing: `GET
  .../render/traversability` shows every marker connected, `main component` on both banks, and
  `preflight`'s own `traversability: spawn ↔ objective chain connected` holds on every run this board was
  driven. Disabling the goal-hollow push entirely left the count unchanged (11108 → 11108), which rules
  the pit out as the cause; the remaining and more likely explanation is that the check is reading the
  relief field the wall was excluded from, not the built column the bridge's own layer stamps over it —
  a question for the studio rather than for this board, and one this run could not settle further without
  changing code outside the brief.
- **`RL2`, 28 blocks of range, 257 barrier steps.** Read together with the heightmap's own contour
  rings — smooth, evenly spaced, no terracing — this is the wall again: a deliberate 15-block masonry
  face reads exactly like an ungraded barrier to a rule that cannot tell a retaining wall from a cliff
  nobody meant. The rolling ground either side of it is graded on purpose (`grain amplitude 0.5`, pushes
  at `falloff 18`) and reads that way in the picture.
- **`WX11` ×2, destroyable-2 two blocks proud of the cell beside it.** The base's own placement,
  untouched; a doorstep rather than a wall, and not worth re-grading a goal the brief says stays where it
  is.

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
| the grounded biplane | `(-64, 3)` | fuselage `y29`, wings at `y30`, the new thing this board tried |
| the yard route | `(-83,26) → (-77,12) → (-70,5) → (-64,3)` | a worn branch off the crossing's own approach, passing east of the croft rather than through it |
| the island knoll | centred `(48, 50)` | `+5` push, `y26..33` read back |

## What to look at

`specs/sonnet-fallowmere/renders/world-iso.png` and `world-iso-turned.png` are the board in the round;
`world-heightmap.png` is the contour read the relief section above is measured against;
`world-traversability.png` is the connectivity claim `SK11` disagrees with;
`specs/sonnet-fallowmere/closeups/bridge-crossing.png` is the arch from the water; `boat-in-canal.png`
and `airplane.png` are the two new props at a scale that reads them; `yard-house-airfield.png` is the
croft, the route and the boulders together.
