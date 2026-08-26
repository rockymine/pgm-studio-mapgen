# Whinnymoor — a slate quarry, built out of the showcase library

**What it is, in one sentence.** A slate quarry cut into a moor: the main working runs from the middle of
the board deep into each team's ground as an open chasm, the ground steps down to it in benches joined by
pale haul roads, and each team's two wools sit at opposite ends of its back line — one in a wheelhouse on
the lip above the cut, one in the sump shed at the bottom of the west workings.

Capture the wool, two teams, `rot_180`, 24 players, 110 × 240 blocks. It is the board the `showcase/` folder
was built to make: every technique in it is one of the eighteen, and this document says which.

## The board

```
      |  1         0         1 |
  -24 | VVV                WWW |     V  wheel — the wheelhouse wool, on the lip at surface 22
  -21 | JJJ      SSSS      HHH |     W  sump  — the sump wool, at surface 10
  -18 | GGGGGGGGGGGGGGGGGGGGGG |     S  spawn, in the middle of the back line, at 18
  -15 | FFFFFFFFooooooEEEEEEEE |     E/F moor, at 18 — split around the head of the cut
  -11 |  DDDDDooooooooooCCCCC  |     C/D benches, at 14
   -6 |  BBBBBBooooooooAAAAAA  |     A/B tips, at 10 — the floor of the workings
   -3 |  ++++++++++++++++++++  |     +  the mid band: 30 blocks of void, crossed by building
```

Eleven pieces a team at five surfaces — 10, 14, 18, 22 — and one build zone. The chasm is the void the
pieces leave: no piece covers `x −25..25` between the tips and the moor. It is **not** declared, and should
not be: `PlanVoids.Declare` names an *enclosed* void, and this one opens into the mid band at both ends, so
nothing rings it. The board carries no buffer piece and compiles to no `subtract`.

**A split frontline, because `FR6` says a frontline is either split or 6–8 cells wide.** The first draft ran a
single 28-cell shelf across the front and was refused. Two headlands with the chasm's mouth between them is
the shape the rule was measured off, and it is a better board: an attacker landing on one headland is
committed to that side until the back line.

**Both wools comparably far from the spawn, because `WL9` says so.** The first draft put the spawn at one end
of the back line with one wool beside it and one at the far end — spawn→wool 52 blocks against 110, which
`WL9` refuses at a ratio of 1.76 against a band topping out at 1.232. The spawn moved to the middle and the
wools to the two ends: 73 blocks and 68. What separates them is now their *character* rather than their
distance, which is what the rule is for.

## How it plays

`GET …/plan/flow`, off the plan alone:

```
wool at (-50, -115)   attacker 236 blocks, defender 73
wool at ( 45, -115)   attacker 233 blocks, defender  68
  3 ways in. They part at (0, 90) and meet again 43 blocks short of the objective.
  Going round the merge saves the defender 8 blocks, so the defence arrives from behind the objective
  while the attack arrives at its front.

WHAT NO JOURNEY REACHES
  Every piece of ground is on somebody's way somewhere.
```

**0.0% dead**, 13 200 ground cells. That is not a coincidence and it is not a boast: the board has no ground
that is not either a tier, a road between two tiers, or the back line the two wools hang off. The chasm took
the space a dead landform would have occupied.

The two wools ask different things of an attacker. The **wheelhouse** is up: the last twenty blocks are a
haul road climbing four, and a bedrock wall stands across the approach with its chests on the attackers' own
side of it. The **sump** is down: the last twenty blocks descend eight, into a shed at the bottom of a
working with the moor looking down on it. Holding both means holding two ends of a road, and the road is the
board.

## What the ground is made of

Five themes, three tone families, and the values chosen so the tiers separate from above.

| Theme | On | Made of | Family |
|---|---|---|---|
| `moor` | the moor and the back line | grass over coarse dirt, voronoi at cellSize 17, three courses deep | verdant + dirt |
| `bench` | the workings' benches | stone brick, diorite, polished diorite, cracked brick — the **lightest** grey | grey stone + pale stone |
| `floor` | the tips, at the bottom | cobble, mossy cobble, grey clay, gravel — the **darkest** value | cobble + dark |
| `haul` | the six haul roads | end stone, white clay, birch, gravel — pale and warm | sand |
| `lip` | the wheelhouse platform | stone brick and polished diorite under a sandstone kerb | grey stone + sand |

**The haul roads are pale on purpose.** The first build painted the tips, the benches and the roads all in
the grey-stone family, and the whole quarry came out as one flat grey field — the exact fault `02-theme`
measures, where Stone, Andesite, Stone Bricks and Cobblestone are four names for `#7e7e7e`. Separating them
by *value* rather than by pattern — dark floor, light bench, pale road — is what makes the top-down readable,
and it makes the routes legible from above, which is a design win rather than a cosmetic one.

## The techniques, and where each came from

| Showcase | Used here as |
|---|---|
| `02-theme` | the five-bucket theme; the moor is `meadow` with podzol in its wall |
| `03-paving` | the wheelhouse platform, scoped to its own shape with `override: true` |
| `05-steps` | the tiers themselves — one piece per surface, one compiled shape per height |
| `06-ramp-and-slant` | the six haul roads: polygons with `anchor_heights`, four blocks over seventeen |
| `07-hill` | the two swells on the moor — `point` marks, not pushes, for the reason below |
| `09-mesa-and-hollow` | `back-flat`, an `area` mark holding the back line level under the road and the huts |
| `11-channel` | the chasm — though here it is left by the plan's arrangement rather than cut by a subtract |
| `15-boulder-outcrop` | the spoil: eight boulders grouped where each haul road tops out over a bench lip |
| `16-forest` | the wood, in the hollow between the west bench top and the back line |
| `17-houses` | the engine house at the head of the east haul road, two quarrymen's huts on the back line |
| `18-wall-and-iron` | the bedrock wall across the wheelhouse approach, and the iron in the spawn |

## What went wrong

**Pushes and ramps do not compose, and the ramps lost.** The moor's first relief was three `push` entries.
A push applies to the *already-solved* surface, so it lifted the ground at the head of every haul road by
four or five blocks while the ramps — `relief_scope: "exclude"` — held the height they were drawn at.
Measured: `haul-w2` topped out at y17 against a moor at y21, a four-block wall at the top of a road. Nothing
complained: `evaluate` scored 0, `preflight` said `export gate OPEN`, and `coverage` said 0.0% dead, because
the walk models a player who can place blocks (`05-steps`).

The fix was to state the swells as **`point` marks** instead. A mark is a constraint the ramp can be matched
to; a push is applied afterwards and cannot be. With `reach: 14` and the marks moved clear of the road heads,
the same two hills read the same from above and every road meets the moor flush.

**And then the marks reached further than expected.** `whin-w` at `(-28, 66)`, `h 23`, `r 6` still left a
three-block step at `haul-w2`'s head thirteen blocks away, because `reach` is a decay length rather than a
cutoff. Moving it to `(-24, 68)` and dropping it to `h 22` closed it.

**The proof is a transect, not a picture.** The read that settles the whole question is the top of the solid
mass at every block along each road:

```
haul-w1      y9 → y13     max |step| 1
haul-w2     y13 → y18     max |step| 1
haul-e1      y9 → y13     max |step| 1
haul-e2     y13 → y18     max |step| 1
wheel-ramp  y17 → y21     max |step| 1
sump-ramp   y17 → y10     max |step| 1
```

Sampling every *two* blocks hid the fault: a two-block riser and two one-block risers read the same. A
column read every block is what caught it.

**Two placement faults the dressing pass caught and one it did not.** Four boulders were declined
`DR-SITE has no ground at (…)` — a boulder is placed at a point and grows from it, so one sited four blocks
from a bench lip hangs its own footprint over the void. Two trees were declined `DR-CLAIM … claimed by the
building 'hut-w'`: a building holds the ground it stamps plus a ring beyond it. The one nothing caught was
three trees standing **in the middle of the west haul road** — the wood's first footprint overlapped the
ramp, and no gate has an opinion about a tree in a road. Moving the wood east of the road is the fix, and
looking at the top-down is what found it.

## Coordinates

| Thing | At | Reads |
|---|---|---|
| wheelhouse wool | `(45, 115)` | room floor y21, cage over it, sky marker at y38 |
| sump wool | `(-47, 112)` | room floor y9, at the bottom of the west workings |
| defence wall | `x 40..55, z 89..91` | bedrock over the `back`–`rise` seam, chests on the `back` face |
| iron | inside the spawn at `(-8, 96)` | renews; the spawn building is sized around it |
| settling pond | `(-42, 20)` → `(-26, 21)` | water at y9 on the west tip, gravel bank |
| engine house | `x 21..32, z 58..69` | at the head of the east haul road |
| quarrymen's huts | `x ±22..31, z 78..86` | either side of the spawn, clear of its door |
| the chasm | `x −25..25` between the tips and the moor | void; the mid band crosses it at `z ±20` |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, one `WX4` complaint (the spawn pad shifted for wall clearance) |
| `POST /plan/inspect` | one island gap, **30 blocks** (`CT12` wants 15–40) |
| `POST …/sketch/relief/read` | cells 3 775 · low 18 · high 22 · relief 4 · **symmetry error 0** |
| `GET …/coverage` | 13 200 reached · **0 dead** · 0.0% |
| `GET …/preflight` | export gate **OPEN** |
| provenance census | tree 26 · boulder 16 · house 6 · roomfloor 4 · wool 4 · redstoneline 4 · stroke 4 · spawn 2 · ironcube 2 · wall 2 · flora 2 · water 2 |
| extent | 110 × 240 blocks, cell 5, surfaces 10 / 14 / 18 / 22 |

## Open gameplay questions

Two decisions here had no oracle and were made rather than derived. Both are recorded as questions.

**Is a wool at the bottom of a pit a fair objective?** The sump sits eight blocks below the moor that
overlooks it, so a defender on the lip has a clear shot down into the approach and an attacker in the sump
has nowhere to retreat to. That reads as a strong defensive position; whether it is *too* strong is a
question about how the map plays and belongs to the author.

**Should the chasm be bridgeable along its whole length, or only at the mid band?** It is buildable only
where the mid band covers it, so the two halves of a team's own ground are joined by the back line and not
across the working. That makes the board a horseshoe and gives a defender an interior line. The alternative —
a build region over the whole chasm — would make it a shortcut instead of a wall, and would change the map.
