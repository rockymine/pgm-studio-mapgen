# Gypsum Reach — a desert lane with three ways in

**A pale desert lane where each team's emerald monument stands in the open, with a way in from below, one from
above and one through.** The dry wash in front of it, crossed by a timber bridge, is the way from below; the
grassed mesa off its outer flank is the way from above; the sunken oasis and its hamlet on the inner flank are
the way through. `docs/gameplay/approaches.md`'s *an objective sits exposed, and the ground around it is
composed* is the rule it follows.

Slug `opus55-gypsum-reach`, map name **Gypsum Reach**, built on the deployed studio. The run's questions on it
are notes 1–5, and the author's own notes are 36–43 (`reports/opus55-notes-run.md`).

## Three passes

**The first build was the right shape and empty, and the author said so.** Everything was sand over twenty
blocks of sandstone, two houses stood by a path, the front was bare, and the outline was the plan's rectangle.

**The second pass laid a board on that shape.** Stone went under the sand, with sandstone beds only in the top
ten blocks. An oasis with a pool, grass, acacias and olives went on the north flank, with a hamlet round it.
The wash got a sandstone arch, the mesa a ruined tower and the lip two ruins, and the two long coasts were cut
point by point.

**The third pass is the author's notes 36–43 on the second, taken one by one.** The frontline is pushed out on
one side and pulled in on the other, with a middle island. The spawn is in a corner beside the oasis, and the
oasis floor sits four under the field.

**The made things changed to the author's words as well.** The houses are stone brick with no cobble or clay,
and the rocks are all the larger angular boulder.

**The arch is a timber bridge now, and the mesa's tower is gone.** The mesa carries grass, a tree and two rocks
instead, and the monument is an emerald cube.

## How it is meant to play

**A team's monument is a short walk forward of its spawn, and the contest is the ground between the two
monuments.** The monument is 50 blocks from its own spawn and 179 from the enemy's on the plan tier, a ratio of
3.58 against `GO1`'s 3.0–4.0.

**The spawn stands inside its corner, not against it.** Players leave it facing −z with the oasis on their
right, run along it on the path, and turn right onto the road south of the pool to the front (note 37).

**The halves meet across a 32-block build zone over void, with an island on the axis.** The island is 8 × 32
blocks at y18, 12 blocks from each frontline, with a rock at each end. The frontline is pushed out toward it
south of the middle and pulled back 4 to 8 blocks north of it (note 36).

**Each way in costs something different.** The wash floor is 7–8 below the field and the bridge crosses it at
field height. The mesa's grassed top is 10 over the field, south of the monument. The oasis floor is 4 under
the field and holds the pool.

## What the ground is made of

**Sand over sandstone beds over stone and andesite, finished by angle.** The beds carry one bed of hardened clay
and a thin orange one, and they follow the ground, so the wash and the mesa show them. The oasis, the spring
and the mesa top are grass over dirt, which the desert biome tints yellow-green.

**The built family is grey:** stone-brick houses with cracked stone brick and polished andesite through their
middle courses under brick roofs, and stone-brick ruins. The bridge is spruce planks on dark-oak posts behind
oak-fence rails. The accent is the granite and brick of the paths and the orange bed in the rock.

## What went wrong

**A bend over the whole field once pulled its back edge off the spawn bench.** Pre-flight still read OPEN and
the export refused `EX1`, both spawns unreachable. The coasts are now cut point by point, and the spawn's seams
are left as the plan cut them.

**A made layer's rectangle covers `x0 … x1 − 1`.** A one-block post written as `x, x` has no area and draws
nothing (`SK4`). The bridge's first drive laid a deck without rails or posts until the column read said so.

**Houses placed by eye were declined for `DR-PASS` on three drives.** A group of buildings needs eight blocks of
passable ground on every side that is not the ground's edge, and the spawn room counts as a building. The house
seats read put them where they fit.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−96, 38), yaw 180, y21 | walked end to end to the monument |
| monument | (−70, −2), shelf y22, emerald cube y26–28 with a bedrock centre | `column` (−70, −2) |
| bridge | deck x −54…−35, z −4…0 at y18, step x −34…−33 at y17, posts x −50/−44/−38 | `column` (−44, −4) |
| mesa top | (−70, −40), grass at y29, acacia (−72, −40) | `column` (−72, −40) |
| oasis pool | (−63, 31), water at y15, grass y15–16 against the field's y19 | `column` (−63, 31) |
| island | x −4…3, z −16…15, y18, rocks (−1, −9) and (0, 8) | `column` (−1, −9) |
| lip ruins | x −32…−29, z 18…34 and x −29…−26, z −44…−30 | — |
| dead ground | 17.0%: round the two houses behind the monument, at (−86, −22) | coverage |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
