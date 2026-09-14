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
| stark contrast, no separation | `05-themes.txt` | clay 87.8%, pit 4.9%, sward 4.5%, works 2.8%; `clay|pit` 516 cells of border, every one of them at the foot of the pit wall, and `clay|works` at a one-course built riser |

`03-slopes.txt`: **19 377 walked, 472 scrambled, 123 barrier; 7 faces, largest 35** at x 2..6 z -55..-47
— the haul road's west revetment.

## Two things a picture would not have caught

The core first stood two blocks back from the lip and `column` answered **ground 30° from level**: it
was sitting on the `terrace-pan` mark's own four-cell bevel. A piece's rectangle is not its ground —
the bevel is part of it — so the core moved to (-34,-60) and reads 11°.

The track out of the spawn ran straight through its own kiln: a transect across it read
`BARRIER +15, DROP -15 at (-15,-68)`. The kilns moved four blocks north and the track now runs in front
of their yards rather than into them.

## The author's pass: the core was already a cube, and six trees wanted soil

**The goal is a core, and `CorePlacement` carries no `style` at all** — a core's casing size is set by
`lava`, and `lava: 3` is a **5 × 5 × 5** obsidian cube. Measured rather than assumed:
`render/section?axis=x&at=-60` draws the casing five wide and five tall with three courses of lava
inside it, and `column?at=-34,-60` reads obsidian y31, lava y32–34, obsidian y35. That is 98 blocks of
shell against a `cube-3`'s 27, so the *use a cube* item was already satisfied and nothing changed. If a
bigger one is wanted, `lava` is the dial and it goes to 5.

Six of the twelve copied bodies stood on hardened or stained clay — `birk-1` (44, −78), `birk-5`
(44, −64), `birk-6` (−38, −80), `birk-9` (24, −16), `birk-10` (−8, −18), `birk-11` (46, −42). The board
now carries a fourth theme, **`sward`**: grass over two dirt over hardened clay, laid as six seven-point
rings under those six. Its cell carries coarse dirt beside the grass so the patch feathers, and Desert
puts the grass at straw. `05-themes.txt` reads **sward 4.5%, 898 cells, Grass Block first**; columns
confirm soil directly under `birk-5` (`y26 Grass Block · y25 Dirt`), `birk-10` (`y21 Grass Block`) and
`birk-11` (`y23 Coarse Dirt · y22 Dirt`) — the other three sit under 11–13-block birch canopies that a
column reads as leaves whichever cell it is pointed at.

The three `birk` bodies themselves are genuine birch — `17:14` log under `18:14` leaves, 11–13 tall —
and `roundel-1` is oak. Neither is the acacia-trunk-with-birch-leaves conifer the author found on the
two desert boards, so nothing here was replaced.

## Limits

- The `swell` push reached the pit-step's head through its falloff and stood two blocks proud of the
  flight it met. Shortening the falloff from 15 to 8 fixed it. A push's `falloff` is a reach, and it is
  easy to place one whose ring is clear of a flight and whose skirt is not.
- Nobody has played it. Whether a seven-block pit in front of a core is a killing ground the attacker
  wants, or a trap that makes the core impossible to defend from below, is a question for the author.
