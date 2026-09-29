# Sootcombe — a composed capture board on an ash field

**An ash-field combe: each team's hamlet of timber lodges stands on a terrace four blocks over its hub, and the
hub falls to a flat frontline with an archer tower at its back corner.** The arrangement is composed board p12 t2
seed 21, pinned off `GET /api/compose` and taken whole; `composed-p12-seed21.plan.json` is it as pinned. This
board states the elevation, the paint, the made things and the dressing.

Slug `opus55-sootcombe`, map name **Sootcombe**, built on the deployed studio. The notes on it are 6–10 and the
author's own 33–35, 44–50, 61–64, 70, 71 and 75–77 (`reports/opus55-notes-run.md`).

## Seven passes

**The first build was bare ash.** The author's review of the whole run said so, and the second pass cut the outer
coasts point by point and stood a headframe, an engine house, timber stacks, a slag heap and regrowth on it.

**The third pass is the author's notes on the second, taken one by one.** The engine house read as a failed
building and the timber stacks as ugly, and both are gone; the slag heap was too large a rock for a board this
size and is gone too. The headframe was interesting but too tall, and it is now a shorter archer tower on each
frontline with a one-course deck.

**The ground and the rooms changed to the author's words as well.** The ground is the first pass's black clay on
grey stained clay again, at a larger pattern, over granite. The paths are wider and laid in dirt, coarse dirt and
spruce planks. Every room is a timber lodge in the headframe's language rather than the brick house.

**The fourth pass is the author's second round of notes.** The rocks are cyan stained clay, which 1.8 draws
dark grey. The archer tower has a spruce platform at mid-height with a nether-brick fence and a ladder. The
hub's north-west corner rises five blocks where the heap stood.

**The ground and the play changed in the fourth pass too.** The ash is a turbulence field with more black
and some dark oak, and the faces are tilted beds. A second build zone lies east of each hub, and a coast cut
that let players walk round the east wall's end is fixed.

**The fifth pass answered the author's third round.** Every room is now the stone house from Gypsum Reach
under a pitched roof, grey against the brown ash. The boulders are andesite and cobble, and the mid stone
carries two larger ones.

**The ground and the trees changed in the fifth pass too.** The mid stone rises a block in its middle and dips
two at its lips, and each frontline dips along part of its edge. Grass patches and a willow written for the
board replace the birch and the spruce.

**The sixth pass is the author's fourth round.** The doors are three tall, and each wool room's door is
filled with stained-glass panes in its wool's colour. Two more willows and one more grass patch stand on each
team's ground.

**The seventh pass is the author's fifth round.** The mid stone and the frontlines' front corners are
chamfered, the west wool stands a cell further out from the rise, and a channel with lily pads splits the east
wool's lane.

## How it is meant to play

**Two wools a team, each behind a bedrock wall the composer placed.** The west wool is at the end of a spur off
the hub, its wall 11 blocks in front of the room face; the east wool is at the end of the terrace, its wall 15
in front. The defender walks 43 and 46 blocks to them and the attacker 189 and 203.

**The spawn looks down the hub to the band.** The terrace holds the spawn and the east wool's approach, and the
hub grades four blocks down to a frontline pinned flat. The author ruled the relief fine as it is (note 9).

**The archer tower is height at the front.** Its platform is at y14, five over the frontline, reached by a
ladder from the ground, under a roof at y18, at the front's back east corner. Andesite-and-cobble boulders
two and three blocks across are the frontline's cover.

**The mid stone is not flat.** It stands 11 across its body, 12 through its middle and 9 at each lip, and each
frontline's edge dips from 9 to 7 along about half its width, so a bridge lands a little lower than the ground
behind it.

**A player can bridge east of the hub as well as across the band.** The second build zone is x −8…4,
z 40…68: the hub's last eight blocks and four of void, ending seven short of the east wall.

**Every bedrock wall has void past both ends.** The author's ruling (note 48) is that a wall that can be
walked round is not a wall.

## What the ground is made of

**Grey stained clay with black clay in its creases, as a turbulence field at scale 7,** with worn earth
between and a few dark-oak plank patches. The shoulder is grey clay with granite, and the steep band is
granite and polished granite.

**The wall and the fill are tilted beds** — mostly hardened clay, mostly granite, and granite with grey and
black clay — each parted from the next by a line of hardened clay, dipping 1 in 2.

**The built family is grey stone and timber:** the rooms are stone brick and andesite in alternate courses on
polished-andesite posts under jungle-plank roofs with clay gables; the archer towers are dark-oak logs and
planks with a spruce platform and nether-brick fence. The accent is the granite of the rock and one block in
seven of the paths, and the andesite and cobble of the boulders.

## What went wrong

**The stored sketch was found reverted to the second pass after two third-pass drives.** The world read old
headframe planks at (−12, 76) beside the new archer tower, and `GET …/sketch` answered the pre-feedback layers
at ETag "16". A third drive stored the new layout and it held; a Sketch tab open on the board, which saves the
board it holds on entering In game, is the likely cause.

**A coast cut pushed ground two blocks past the east wall's end.** The kit pulled each inserted point toward
the ring's centroid, which on this ring lies across the east approach's south coast. The pull now tests which
side of the edge is inside.

**On the mid stone only the z < 0 half's relief counts.** The stone is one shape on the axis and takes its
relief from that half, fanned; a push stated on its z > 0 lip did nothing until it was stated at the z < 0
lip.

**The tree library has no willow.** The kit writes one as a copied recipe, and it took three drives to read as
a willow rather than a round crown or a block of leaves.

**The mirror turns a layer and not a block's data.** One ladder stated for both teams faced its beam on red
and faced away on blue, so each team's ladder is stated with its own facing.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−10, 92), terrace y13 | spawn → front: falls 4, worst step 1 |
| west wool | (−44, 62), wall x −29…−28, z 56…67 | three courses over the spur |
| east wool | (32, 74), wall x 11…13, z 68…80 | three courses over the terrace |
| archer tower | x 9…13, z 33…37, legs y9–17, platform y13 with fence y14, roof y18 | `column` (11, 37) |
| ladder | (11, 36), y9–13, facing north; blue's (−12, −37) facing south | `column` (11, 36) |
| west rise | x −20…−15, z 68…80, y18 over the terrace's 13 | transect along z 74 |
| second build zone | x −8…4, z 40…68 | `map.xml` `build-area-2` |
| frontline boulders | (−11, 27), (5, 29), (−9, 35), (12, 25), andesite and cobble | `column` (−11, 27) |
| mid stone | 11 across, 12 in the middle, 9 at the lips; rock (5, −4), willow (−9, −5) and their images | transect x −4 |
| willows | (−18, 50) in the regrowth, (−18, 74) on the rise, (2, 79) at the terrace's edge | — |
| orange wool door | x 29, z 72…75, y13–15, orange stained-glass panes | `column` (29, 73) |
| east channel | x 16…18, z 69…79, water at y9–10, coast to coast, four lily pads | `tools/probe.py` face z=74 |
| mid stone rocks | (−6, −3), (5, −5) and their images | — |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
