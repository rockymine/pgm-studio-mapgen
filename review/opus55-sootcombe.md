# Sootcombe — a composed capture board on an ash field

**An ash-field combe: each team's hamlet of timber lodges stands on a terrace four blocks over its hub, and the
hub falls to a flat frontline with an archer tower at its back corner.** The arrangement is composed board p12 t2
seed 21, pinned off `GET /api/compose` and taken whole; `composed-p12-seed21.plan.json` is it as pinned. This
board states the elevation, the paint, the made things and the dressing.

Slug `opus55-sootcombe`, map name **Sootcombe**, built on the deployed studio. The notes on it are 6–10 and the
author's own 33–35 (`reports/opus55-notes-run.md`).

## Three passes

**The first build was bare ash.** The author's review of the whole run said so, and the second pass cut the outer
coasts point by point and stood a headframe, an engine house, timber stacks, a slag heap and regrowth on it.

**The third pass is the author's notes on the second, taken one by one.** The engine house read as a failed
building and the timber stacks as ugly, and both are gone; the slag heap was too large a rock for a board this
size and is gone too. The headframe was interesting but too tall, and it is now a shorter archer tower on each
frontline with a one-course deck.

**The ground and the rooms changed to the author's words as well.** The ground is the first pass's black clay on
grey stained clay again, at a larger pattern, over granite. The paths are wider and laid in dirt, coarse dirt and
spruce planks. Every room is a timber lodge in the headframe's language rather than the brick house.

## How it is meant to play

**Two wools a team, each behind a bedrock wall the composer placed.** The west wool is at the end of a spur off
the hub, its wall 11 blocks in front of the room face; the east wool is at the end of the terrace, its wall 15
in front. The defender walks 43 and 46 blocks to them and the attacker 189 and 203.

**The spawn looks down the hub to the band.** The terrace holds the spawn and the east wool's approach, and the
hub grades four blocks down to a frontline pinned flat. The author ruled the relief fine as it is (note 9).

**The archer tower is height at the front.** Its deck is at y18, ten over the frontline, at the front's back
east corner, and it has no ladder. Granite boulders two and three blocks across are the frontline's cover.

## What the ground is made of

**Grey stained clay with black clay and worn earth lying in it, at scale 5,** so the patches come out about a
dozen blocks across. The shoulder is grey clay with granite, and the steep faces, the wall and the fill are
granite and polished granite.

**The built family is timber:** dark-oak logs and spruce planks in the lodges, dark-oak logs and planks in the
archer towers. The accent is the granite of the rock, the boulders and one block in seven of the paths.

## What went wrong

**The stored sketch was found reverted to the second pass after two third-pass drives.** The world read old
headframe planks at (−12, 76) beside the new archer tower, and `GET …/sketch` answered the pre-feedback layers
at ETag "16". A third drive stored the new layout and it held; a Sketch tab open on the board, which saves the
board it holds on entering In game, is the likely cause.

**The granite boulders draw `DR-TONE`**, because the ground's own rock is granite; they are placed, and they
are what the author asked for.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−10, 92), terrace y13 | spawn → front: falls 4, worst step 1 |
| west wool | (−40, 62), wall x −25…−23, z 56…68 | three courses over the spur |
| east wool | (32, 74), wall x 11…13, z 68…80 | three courses over the terrace |
| archer tower | x 9…13, z 33…37, legs y9–17, deck y18 | `column` (9, 33) |
| frontline boulders | (−11, 27), (5, 29), (−9, 35), (12, 25) | `column` (−11, 27) |
| mid stone rocks | (−6, −3), (5, −5) and their images | — |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
