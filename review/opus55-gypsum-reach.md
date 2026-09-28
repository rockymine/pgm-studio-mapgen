# Gypsum Reach — a desert lane with three ways in

**A pale desert lane where each team's obsidian monument stands in the open, with a way in from below, one
from above and one through.** The dry wash in front of it is the way from below, the mesa off its outer flank
the way from above, and the two stone houses behind it the way through. That is the sentence the board was
built to, and `docs/gameplay/approaches.md`'s *an objective sits exposed, and the ground around it is composed*
is the rule it follows.

Slug `opus55-gypsum-reach`, map name **Gypsum Reach**, built on the deployed studio. The author's questions on
it are notes 1–5 (`reports/opus55-notes-run.md`).

## How it is meant to play

**A team's monument is a short walk forward of its spawn, and the contest is the ground between the two
monuments.** The spawn stands on a bench at y24 at the back of the lane and grades down to the field. The
monument is 55 blocks from its own spawn and 185 from the enemy's on the plan tier, a ratio of 3.36 against
`GO1`'s 3.0–4.0.

**The two halves are joined by a build zone over void, 32 blocks across the board's whole width.** No land
connects them, per the author's ruling that a crossing a team has to pay to bridge is a decision an attacker
makes.

**Each way in costs something different.** The wash is 9–10 blocks below the shelf, so an attacker drops in
out of sight and has to climb or tunnel out. The mesa is 12 blocks over the shelf, so an attacker on its lip
bridges 18 blocks level onto the goal in view of everyone. The houses give cover up to 11 blocks from the
monument.

## What the ground is made of

**One theme, finished by angle, over sandstone beds that follow the ground.** Sand with small sandstone
patches holds up to 28°, a sandstone shoulder to 45°, and the beds above that. The beds are sandstone and
smooth sandstone with a hardened-clay bed and an orange stained-clay bed every nine blocks, stated once and
used as the fill, the wall and the steepest band. `incline` holds 58% of the ground under 10° and 24% at
10–19°.

**Desert biome, so no tinted block disagrees with the sand.** The houses are stone brick with a brick roof,
the built family; the path is granite, polished granite and brick, the accent.

## Techniques

| Instrument | Where |
|---|---|
| area marks with a bevel | the spawn bench at 24 and the monument's shelf at 22 |
| a line mark | the lip, wandering 16–18 along x −18…−20, and the spawn door's ramp from 24 to 20 |
| a negative push | the wash, −6 over a 7 × 19 ring with roughness |
| a push centred off the coast | the mesa, +13 with falloff 3, its ring half over the void |
| a low push | the north swell, +4 |
| `follow` strata | fill, wall and steep band, from 40 below the ground |
| claiming solid strokes with wander | spawn → monument, and a branch → the lip |

## What went wrong

**The strata came out as plain stone, then as solid orange clay, before they came out as beds.** A `from` of
4 put the whole stack above the ground, and `ending: repeat` does not repeat: the last band claims everything
past the stack. Writing the cycle out bed by bed from 40 below the ground fixed it.

**The first house stood across a path and was declined `DR-CROSS`.** The lip path now branches off the
monument path south of both houses.

**The board is flatter than it should be.** The relief read gives level 0.58 and largest field 0.14, over the
line where ground reads as a table with edges. Note 4 asks the author whether the pan should carry dunes.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−114, 0), bench y24 | transect: worst step 2, walked end to end |
| monument | (−66, −16), shelf y22, obsidian y26–28 | transect: worst step 1 |
| wash floor | x −46…−32 at z −12, y12–13 | near rim at x −48 |
| mesa face | z −34…−36 at x −66, top y34 | 18 blocks south of the monument |
| houses | (−86…−77, −4…4) and (−90…−81, 12…19) | transects: worst step 1 |
| dead patches | (−63, −39) and (−63, 37), about 1 800 cells each | coverage 40.2% dead |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
