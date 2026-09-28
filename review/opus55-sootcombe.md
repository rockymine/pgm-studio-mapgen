# Sootcombe — a composed capture board on an ash field

**An ash-field combe: each team's brick hamlet stands on a terrace four blocks over its hub, and the hub falls
to a flat frontline and a slag stone in the band with a ruined engine house on it.** The arrangement is composed
board p12 t2 seed 21, pinned off `GET /api/compose` and taken whole; `composed-p12-seed21.plan.json` is it as
pinned. This board states the elevation, the paint, the made things and the dressing.

Slug `opus55-sootcombe`, map name **Sootcombe**, built on the deployed studio. The author's questions on it are
notes 6–10 (`reports/opus55-notes-run.md`).

## The second pass

**The first build was bare ash, and the author's review of the run said so.** The arrangement and the relief
were kept; the ground's paint, the coasts and everything standing on the board are new.

**The ash is gravel, andesite and stone.** Grey stained clay read as dark chocolate in the game's textures and
light grey stained clay as pink terracotta, so neither is ash on a board. Note 6's thread carries both pictures.

**The mid stone carries a ruined engine house.** It is a roofless brick shell with a doorway in each long side,
stated once for the board, and a brick stack at one corner fanned to the opposite one.

**A timber headframe stands over the shaft at the hub bar's west end,** beside the slag heap the shaft threw
up, which now wears a slag theme of its own.

**Timber stacks stand on the frontline as cover, two and three courses tall.** Birch and tiny spruce stand on
regrowth along the hub's west rim and the terrace's north coast, and the outer coasts are cut point by point. The
frontline's face to the band, the two wall seams and the rooms' faces stay as the composer cut them.

## How it is meant to play

**Two wools a team, each behind a bedrock wall the composer placed.** The west wool is at the end of a spur off
the hub, its wall 11 blocks in front of the room face; the east wool is at the end of the terrace, its wall 15
in front. The defender walks 43 and 46 blocks to them and the attacker 189 and 203.

**The spawn looks down the hub to the band.** The terrace holds the spawn and the east wool's approach, and the
hub grades four blocks down to a frontline pinned flat.

## What went wrong

**The first finish was refused three times at the store**: a `cell` of size one (`PT3`), and a wall and a fill
sampled in the plane with no `rise` (`PT4`).

**Two stacks stated off the mirror each drew `SK28`.** One stack stated once and fanned is the same building
without the complaint.

**Boulders of stone and andesite drew `DR-TONE` on this ground**, which already carries every tone they are cut
from, and were taken out.

## Coordinates

| Feature | Team 0 (red) | Read |
|---|---|---|
| spawn | (−10, 92), terrace y13 | spawn → front: falls 4, worst step 1 |
| west wool | (−40, 62), wall x −25…−23, z 56…68 | three courses over the spur |
| east wool | (32, 74), wall x 11…13, z 68…80 | three courses over the terrace |
| headframe | x −17…−12, z 71…76, logs to y26, cap y27–28 | `column` (−17, 71) |
| engine house | x −6…6, z −4…4, walls to y16; stack to y25 | `column` (0, −4), (4, −6) |
| frontline cover | four stacks, e.g. x −12…−9, z 26…28, y8–10 | `column` (−10, 27) |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`.
