# Kettleshulme — an island wool and a lane a defender owns

> Adapted from `GET /api/compose?players=20&symmetry=rot_180`, **seed 23**, composer
> `markers-in-blocks-1`, cell 5. Composed score 0.0; structure **hub `double-hole` · frontline `twin`
> · wools `i`, `i`**.

**In one sentence:** a coal-measure clough of dark grit and podzol where each team's near wool is cut
off the hub entirely and reached only over a bridge that team owns, and a mill launder is carried
over the hub's east slot on a deck a raider can run and a defender can shoot from.

110 × 180 blocks, `rot_180` about the origin, base surface 12, observer y 44. One ground group
(`team`, 4 231 solved cells) and one made storey (`launder`, base_y 16).

## What the composer gave and what it became

| The composed board | This board |
|---|---|
| wool-a 123 blocks from the enemy's door, wool-b 83 — **1.48×** straight-line, 139/120 by walk. wool-b was nearer the **enemy** (83) than its own spawn (85) | 138 and 144 — **1.04×** straight-line, 158/167 — **1.06×** by walk |
| both wools hung off the hub, the spawn off its west flank | the spawn moved to the hub's **back**; the far wool takes the flank the spawn had; the near wool is taken off the hub and set on **its own island** |
| exactly one zone, the mid band, 40 blocks of it flush across the front | **two** 15-block crossings with a declared `buffer` between them, and a **third zone that is nobody's but this team's** |
| the east frontline tip 10 blocks wide (`FR9`) | 15 blocks, nose pushed out and broken |
| no storeys at all | a timber launder deck at y16 over the hub's east slot |
| 22 axis-aligned rectangles | one 22-vertex compiled ring taken to 23 by hand, plus a 4-vertex island taken to 6, then both bent |

## The intra-team build zone, which is the board

`wool-b-t1` and `wool-b-room` sit at `x 35..55, z 45..55` — a separate landmass, ten blocks of void
from the hub's east edge, and no other piece touches it. `own-bridge` is a 10 × 10 build zone across
that gap. **Every interfacing component of it touches this team's islands and no other**, which is
what `CT4` calls a team transient-link and `BZ5` the defender-egress bridge; the term that measures it
is `team-stepping-count`, band [0, 2], and the board evaluates at score 0 with one such stone a team.

Zones are **not** fanned by the plan's symmetry — the compile writes back exactly the rects stated —
so the other team's bridge is authored by hand as this one's `rot_180` image. That is one of the two
things on this board I got wrong first and found in `tools/board.py`'s grid rather than in a render:
the enemy's island had no bridge at all and the grid showed it as ten cells of enclosed void.

What it buys in play: the island is a wool an attacker can bridge straight onto from the mid's east
lane — it is the nearest objective on the board to the crossing — but the defender arrives across
ground no attacker can stand on, because the only zone touching the island belongs to him.

## The mid, cut in two

`sike` is a `buffer` piece 10 × 30 blocks on the origin, `mirrors: False`. It makes no terrain; it
states, at the plan tier, that the middle of the crossing is void. Either side of it `crossing-w` and
`crossing-e` are 15 × 30. An attacker commits to a flank before he lays a block, and the two landings
are not the same ground: `walls: [{"a": "front-e", "b": "front-bar"}]` puts a pre-built bedrock
approach wall across the east tip's inland seam, so the east lane lands behind a wall and the west
does not.

## The launder, and what a `made` layer does

`addLayers` with `base_y 16`, `kind: "made"`, `part_of: "launder"`: a deck `x 4..14, z 45..58` one
course thick with two three-block kerbs a course over it. Read back:

```
column (6, 52)   y17 Oak Log · y16 Oak Planks                     over the hub's east slot — void under
column (13, 46)  y17 Oak Log · y16 Oak Planks · y11 Grass · y10 Dirt · y9 Dirt   four courses of air
column (5, 57)   y17 Oak Log · y16 Oak Planks · y15 Bricks        the mill yard, one step down
```

Three things that had to be right and are:

- **`SK13` does not refuse it.** The hub's slot compiles to a subtract and a subtract is the board's
  negative space, but an add *raised* above the ground is a bridge over it rather than a filling of
  it — which is what the rule's own fix text says and what this board measures.
- **`kind: "made"` paints it over its own span.** A plain stacked layer's bands run from the bedrock
  course whatever its `base_y`, which would have handed twenty-six courses of clough to the deck's
  theme. At `(13, 46)` the ground below still reads grass over dirt over dirt.
- **The kerbs are three blocks wide and not one.** At one block every column of a shape touches the
  void, so only the rim and the wall buckets ever paint it and the theme's own surface lands nowhere
  — `SK23`, which fired on the first build and named both kerbs.

It is a way **out** and not a way back: from the mill yard it is a one-block step up, and off its
south end it is a five-block drop onto the hub's front bar.

`05-themes.txt` does not list `launder` at all, and that is not a theme painting nothing: the census
projects to one height per column off the ground layer, so a `made` storey's own paint is invisible to
it. `column` is what sees it.

## Where the made ground meets the grown ground

`yard` is a six-vertex polygon at `base_height` 16 with `relief_scope: "exclude"` — the mill yard, cut
flat into the hub's north bar and out of the relief solve, meeting the hub at a four-block face with a
`wallRun` of brick, cobble and andesite on it. Two flights climb it, one from each end of the bar, ten
blocks of run for four of rise, `height_mode: "level"`, `skirt: 0`, `relief_scope: "exclude"`, a
`material` rather than a theme. A `polyline` runs the brow of the face and a second, the head-dyke,
runs the back of the hub where the moor stops being grazed.

## The relief

No marks and one push — `edge`, a seven-point ring over the frontline whose south lip is the coast
itself, so the front of this board is a gritstone edge that drops into the clough rather than sloping
into it. `amount` 6, `amounts` 6/7/7/6/5/6/6, `crown` **11**, `falloff` 9, `roughness` 2.

The crown is 11 and not 5 because the read said so. `RL6` on the first build: *climbs its skirt at 0.7
and its crown at 0.3 — 2.7× apart*. The half-width a crown is divided by is the ring's own medial
distance, which no arithmetic in the spec predicts; the fix is to read `pushes[].crown` back and set
the number against it. It now reads `skirt 0.78 · crown 0.57`, and the complaint is gone.

`level 0.64`, `largestField 0.537`, `faces 2`, `cliffs 0`, `seams []`, `silentMarks []`, `symErr 0`.

## What the ground is painted with

Three families: the **ground** is dark — millstone grit, podzol, coal in the body of the rock; what is
**built** is red brick, the only warm thing on the board; the **accent** is pale oak, on the launder
and the two stamped shells' posts and beams and nowhere else.

`clough`'s surface is a `layered` material on the **`slope`** axis cut at 26° and 40°. `GET …/incline`
reads 50.3% of this board under 10°, 13.3% at 10–19°, 13.4% at 20–29°, 12.5% at 30–39° and **10.6% at
40° or steeper** — the steepest of the four boards, which is the edge.

`PT1` refused the first build twice: podzol surfaces ground and is exactly one course, so it may not
lie *under* turf. It tops the shoulder band instead.

## The numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, valid; `SP2` and `BZ5` complaints (`BZ5` is the motif being named, not a fault — the prohibition is retired) |
| `GET …/preflight` | **export gate OPEN**, per team |
| `GET …/coverage` | reached 6 174, dead **0**, **0.0% dead** |
| `plan/flow` | *Every piece of ground is on somebody's way somewhere* |
| `03-slopes.txt` | 7 702 walked, 488 scrambled, 276 barrier; 8 faces |
| `06-claims.txt` | placed **16**, declined **0** |
| `05-themes.txt` | `clough` 8 123 cells (95.9%), `yard` 343 (4.1%), 132 cells of drawn border — and the `launder` theme, which `column` sees and the census cannot |
| relief `team` | `low 11 · high 30 · level 0.64 · largestField 0.537 · faces 2 · seams 0 · symErr 0` |
| flow, attacker | 158 and 167 — **1.06×** (composed: 139/120, **1.16×**; straight-line 1.48× → 1.04×) |
| flow, defender | 64 and 58 — 1.10× |

## What is not on this board

**No third building.** A 9 × 7 cottage on the front bar was placed and `DR-PASS` complained: *leaves no
way past it — a side has fewer than 8 blocks of passable ground along its whole run*. The bar is fifteen
blocks deep, so any building on it leaves under eight either side, and the rule is right rather than
awkward: a board already standing a spawn hall, two wool rooms and a launder has nowhere a fourth thing
belongs. The placement ideas that remain are the two stamped shells, the pack road and the wool lane,
five copied birches and one ground-cover pass.

## What went wrong

- **The other team had no bridge.** Zones are not fanned. The grid showed it; no render would have.
- **`RL6` and the crown divisor.** Twice-computed and twice-wrong; the read is the only source.
- **`PT1` on podzol** and **`PT4` on the launder's wall and fill** — a `cell` field with no `rise`
  samples the plane only, so every block of a column resolves alike and a cut face reads as stripes.
- **`SK23` on the one-block kerbs.**

## Open gameplay questions

- **The launder is one-way.** A raider runs it out and drops five blocks off its end; coming back he
  goes round. I judged a one-way high route more interesting than a two-way one, because it costs the
  attacker his retreat and gives the defender the yard above it. This is a question about play and I
  have no oracle for it.
- **The island wool is the nearest objective to the crossing on the board.** It is meant to be the one
  a rush goes for and the one a defence can always reach first. Whether ten blocks of void is enough
  to make an attacker pay for it is not something the plan tier can answer.

## Coordinates

| Thing | Where |
|---|---|
| spawn (red) | `(5, 12, 82)`, door `−z` |
| wools (red) | `red` at `(−45, 12, 50)`, `orange` at `(50, 12, 50)` — the island |
| the island's bridge | zone `x 25..35, z 45..55`, ten blocks of void |
| the two crossings | `x −20..−5` and `x 5..20`, `z −15..15`; the buffer `x −5..5` between them |
| the approach wall | the seam between `front-e` and `front-bar`, `z 25` over `x 5..20` |
| the launder | deck `x 4..14, z 45..58` at y16, kerbs at y17 |
| the mill yard | `x −15..10, z 56..64`, top y15, a 4-block face on the hub |
