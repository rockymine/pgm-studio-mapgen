# Gypsum Reach — a desert lane with three ways in

**A pale desert lane where each team's obsidian monument stands in the open, with a way in from below, one
from above and one through.** The dry wash in front of it, with a sandstone arch over it, is the way from below;
the mesa off its outer flank, with a ruined tower on it, the way from above; the oasis village on its inner
flank the way through. `docs/gameplay/approaches.md`'s *an objective sits exposed, and the ground around it is
composed* is the rule it follows.

Slug `opus55-gypsum-reach`, map name **Gypsum Reach**, built on the deployed studio. The author's questions on
it are notes 1–5 (`reports/opus55-notes-run.md`).

## The second pass

**The first build was the right shape and empty, and the author said so.** Everything was sand over twenty
blocks of sandstone, two houses stood by a path, the front was bare, and the outline was the plan's rectangle.
The relief and the arrangement were kept; everything laid on them is new.

**Now the rock under the sand is stone.** Sandstone beds lie only in the top ten blocks, with stone and andesite
under them, so a deep face shows beds over grey rock.

**The north flank is an oasis village.** A pool in a hollow, grass round it, acacias and olives, and six
stone-brick houses in one style of two heights round the green, reached by a road that runs on to the lip.

**The wash has an arch over it.** Two piers on its rims carry a sandstone deck at the shelf's height, so a
player crosses the wash dry or drops under the arch into it.

**The rest is smaller.** A ruined drum tower stands on the mesa, a copse of olives grows at the mesa's foot, two
ruined walls stand on the lip where a crossing lands, and stone boulders sit at the wash's head. The field's two
coasts are cut point by point, seventeen points in all.

## How it is meant to play

**A team's monument is a short walk forward of its spawn, and the contest is the ground between the two
monuments.** The monument is 55 blocks from its own spawn and 185 from the enemy's on the plan tier, a ratio of
3.36 against `GO1`'s 3.0–4.0. The halves meet across a 32-block build zone over void the board's whole width.

**Each way in costs something different.** The wash floor is 9–10 below the shelf and its near rim 18 blocks
east of the monument. The mesa's top is 12 over the shelf and its face 18 blocks south. The nearest
house stands 11 blocks from the monument.

## What went wrong

**A bend over the whole field pulled its back edge off the spawn bench.** Pre-flight still read OPEN and the
export refused `EX1`, both spawns unreachable. The coast is now cut only on its two long edges, point by point.

**Houses and trees were placed by eye, and some were declined on every one of six drives.** The causes were a
spawn door's kept lane, the cut coast, a dune's skirt and each other's crowns. The seats raster is the read that
would have saved those drives.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−114, 0), bench y24 | walked end to end to the monument |
| monument | (−66, −16), shelf y22, obsidian y26–28 | — |
| wash arch | deck x −52…−30 at z −13, y15–18, air y13–14 under it | `column` (−41, −13) |
| mesa tower | (−76, −45), stone brick to y41 | `column` (−79, −45) |
| oasis pool | (−63, 31), water y15–17 | `column` (−63, 31) |
| lip ruins | x −32…−29, z 18…34 and x −29…−26, z −44…−30 | `column` (−30, 24) |
| dead ground | 28.4%: the mesa's top and the pool | coverage |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
