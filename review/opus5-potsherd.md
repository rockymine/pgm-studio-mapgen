# Potsherd — the pit is the thing in front of the core

> A destroy-the-core board on a terracotta brickfield. Each team's core stands in the open on a baked
> clay terrace with the clay pit cut seven blocks below it and the drying-shed rows behind.

**In one sentence:** the middle-value board of the warm set, where an attacker who wants the core has
to cross an open brickfield, get down into a worked pit, and come up a haul road that the core is
looking straight down.

104 × 208 blocks, `rot_180`, eight plan pieces, maxPlayers 16, ground y17..y28, observer y60.

## Five heights, and the pit is the only one that is a hole

`works` 25 · `terrace` 24 · `rim` 23 · `field` 20 · `pit` 17. The rims are the unquarried clay either
side of the pit, so the pit is a rectangle of low ground with clay on three sides of it and the
brickfield on the fourth — and the frontline where the board's two halves meet is the **field**, which
is flat and open, not the pit.

The relief is eight `area` marks and four pushes, and two of the marks are the whole idea: `pit-pan` at
17 with **bevel 1**, its ring wandering five blocks either side of the plan's straight `z` so the lip
is not a ruled line; and `bench-pan` at 20 inside it, because a worked pit is dug in steps and a single
pan is a hole. `seams 1`, `silentMarks 0`, `symErr 0`, relief range 11, `level 0.615`,
`largestField 0.231` — this is the flattest-measuring of the three boards authored here, and `RL1` said
so until the `landform` was corrected from `rolling` to `plain`, which is what it honestly is.

## Four ways off the pit floor, and every one of them walks

```
haul       (13,-58)→(13,-32)   rises 1, falls 6, worst step 2: 0 barrier, 0 scramble | walked end to end
pit-step   (-18,-42)→(-18,-20) rises 3, falls 0, worst step 1: 0 barrier, 0 scramble | walked end to end
rim-step-w (-43,-40)→(-43,-20) rises 0, falls 3, worst step 1: 0 barrier, 0 scramble | walked end to end
bench-step                     added after RL3 named the bench and the pit floor meeting on a 3-block wall
```

`EL1` complains about six plan seams, two of them seven blocks. It walks the pieces flat and cannot see
a flight. The transects are the answer.

`RL3` still stands: `bench-pan` and `pit-pan` meet on a 3-block step along 31 cells of boundary. That
is a quarry bench and it is meant to be a face; `bench-step` is the one place it is cut through.

## The pit walls are the board's argument

`wallOnTerrainFaces` is on, and the clay theme's `wall` is a five-course `wallRun` — orange over brown
over **white** over yellow over hardened clay. The white is the only pale band anywhere on the board
and it appears on a cut face and nowhere else, which is what makes the pit read as bedded clay rather
than as a hole with a colour change round it.

`column?at=-20,-46` on the lip: `y19 brown · y18 brown · y17 orange · y16..y9 hardened clay`, ground
29° from level.

## What the reads say

| fault | the read | what it says |
|---|---|---|
| objective hidden | `column?at=-34,-60` | ground y23, obsidian y31 and y35 with three courses of lava between, **nothing over it** but its own sky marker at y59–61. Ground 11° from level |
| spawn faces away | intent yaw 0 vs bearings to (-34,-60) and (33,59) | 51° and 14°. Within the bar |
| spawn faces a wall | two transects along the track, spawn → core | both `worst step 0–1, 0 barrier, 0 scramble, walked end to end` |
| stairs that end nowhere | the three transects above | all three walk |
| flat, one theme, empty | `coverage` · `incline` | **9.4% dead**, largest patch 482 cells **1 block** from used ground; angles 56.4 / 29.6 / 8.6 / 3.0 / 1.5 / 0.8 % — 2.3% at 40° or steeper, all of it pit wall |
| straight frontline | the `pit-pan` ring, plus bent `camp-25`/`camp-24`/`camp-20` | the lip wanders; the board's outer edge is a drawn coast |
| stark contrast, no separation | `05-themes.txt` | clay 91.3%, pit 4.9%, works 3.8%; `clay|pit` 516 cells of border, every one of them at the foot of the pit wall, and `clay|works` 242, every one at a one-course built riser |

`03-slopes.txt`: **19 463 walked, 386 scrambled, 123 barrier; 7 faces, largest 35** at x 2..6 z -55..-47
— the haul road's west revetment.

## Two things a picture would not have caught

The core first stood two blocks back from the lip and `column` answered **ground 30° from level**: it
was sitting on the `terrace-pan` mark's own four-cell bevel. A piece's rectangle is not its ground —
the bevel is part of it — so the core moved to (-34,-60) and reads 11°.

The track out of the spawn ran straight through its own kiln: a transect across it read
`BARRIER +15, DROP -15 at (-15,-68)`. The kilns moved four blocks north and the track now runs in front
of their yards rather than into them.

## Limits

- The `swell` push reached the pit-step's head through its falloff and stood two blocks proud of the
  flight it met. Shortening the falloff from 15 to 8 fixed it. A push's `falloff` is a reach, and it is
  easy to place one whose ring is clear of a flight and whose skirt is not.
- Nobody has played it. Whether a seven-block pit in front of a core is a killing ground the attacker
  wants, or a trap that makes the core impossible to defend from below, is a question for the author.
