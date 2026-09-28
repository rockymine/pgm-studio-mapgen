# Sootcombe — a composed capture board on an ash field

**An ash-field combe: each team's brick hamlet stands on a terrace four blocks over its hub, and the hub falls
to a flat frontline and a flat slag stone in the band.** The arrangement is composed board p12 t2 seed 21,
pinned off `GET /api/compose` and taken whole; `composed-p12-seed21.plan.json` is it as pinned. This board
states the elevation, the paint and the paths, and nothing about where the pieces stand.

Slug `opus55-sootcombe`, map name **Sootcombe**, built on the deployed studio. The author's questions on it are
notes 6–10 (`reports/opus55-notes-run.md`).

## How it is meant to play

**Two wools a team, each behind a bedrock wall the composer placed.** The west wool is at the end of a spur off
the hub, its wall 11 blocks in front of the room face; the east wool is at the end of the terrace, its wall 15
blocks in front. The defender walks 43 and 46 blocks to them and the attacker 189 and 203.

**The spawn looks down the hub to the band.** The terrace at the back holds the spawn and the east wool's
approach at y12–13, and the hub grades four blocks down to the frontline, worst step 1. The frontline is
pinned flat, because ground crossed under fire carries no landform.

**The mid stone is the composer's, 24 × 16 and 12 blocks off each frontline.** It is left flat and level with
the frontlines; note 7 asks whether it should rise.

## What the ground is made of

**One theme, finished by angle.** Grey stained clay holds the ground under 30°, with black stained clay at one
end of the noise's stop list and coarse dirt with dirt at the other, so each comes out as a patch. A shoulder
of grey clay and andesite holds 30–45°, and stone and andesite with cobblestone above that. The fill is the
same rock with a two-block rise.

**In the game's textures the grey clay reads as dark chocolate brown, and the black patches as holes.** Note 6
puts that to the author with a default of light grey as the ground.

**The rooms are all one brick style**, `lk-spawn`: brick with brown stained clay, chiselled stone-brick posts
and a stone-slab roof with a brick verge. The paths are granite, polished granite and brick.

## Techniques

| Instrument | Where |
|---|---|
| a composed plan taken whole | pieces, zones, walls and placements unchanged |
| area marks | the terrace at 13 and the frontline at 9 |
| a line mark with a tread | the west spur, 11 to 10 |
| a push centred off the coast | the slag heap, +7 at the hub bar's west end |
| claiming solid strokes | spawn → frontline, hub → each wool |

## What went wrong

**The first drive was refused three times at the store**: a `cell` of size 1 (`PT3`), and a wall and a fill
sampled in the plane with no `rise` (`PT4`). All three were mine, and the refusal named each field.

**The board is nearly flat.** The relief read gives level 0.85 and largest field 0.28; the ground is a terrace,
a graded hub and a flat front. Note 9 asks whether the terrace should meet the hub at a wall with flights
instead, which would give it a face.

**`RL2` stands on the heap.** Its flank lands on the hub bar's coast as a 13-cell face at x −20…−16,
z 75…80; it is at the edge and on nobody's route.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−10, 92), terrace y13 | spawn → front: falls 4, worst step 1 |
| west wool | (−40, 62), spur y10 | wall x −25…−23, z 56…68, three courses |
| east wool | (32, 74), terrace y13 | wall x 11…13, z 68…80, three courses |
| slag heap | top y19 at (−18, 79) | face x −20…−16, z 75…80 |
| mid stone | x −12…12, z −8…8, top y10 | 12 blocks of build zone to each frontline |
| frontline | x −16…16, z 20…40, y9 | pinned flat |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
