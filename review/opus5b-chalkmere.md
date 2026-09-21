# Chalkmere — destroy the monument

> A chalk downland split by a dry combe, the monument alone on a pale turf shoulder above its own
> steading, and the two downs joined only by a build zone over the gap between them.

**In one sentence:** every attack on Chalkmere is a crossing made in the open, and the combe is the one
place to drop out of sight once across.

48 × 216 blocks, `rot_180` about the origin, base surface 9, build ceiling y50, ground y6..y25. Two
landmasses, 16 blocks of void between them, one build zone spanning the whole 48-block face.

## What is where

| Thing | Where | Measured |
|---|---|---|
| the monument | `(14, 62)`, `pillar-3`, obsidian, `float: 4` | own-spawn walk **48**, enemy walk **167**, ratio **3.48** (GO1 wants 3–4) |
| the spawn | `(-5, 100)`, a 10 × 12 hall in a 20 × 16 piece | iron cube in the six-block strip west of the shell, two blocks clear (WX8) |
| the strait | `z -8..8`, crossed by a build zone `x -24..24` | 16 blocks; frontline run 48 blocks, straight |
| the combe | a pinned pan at y7, ring radius 12 about `(-17, 38)` | a dew pond in it, water at y8 |
| the nab | a push at `(15, 28)`, `amount 11`, `falloff 11`, `crown 4` | the height an attacker climbs to bridge from |
| the fold | two houses, `x -24..-13` at `z 62..70` and `z 76..83` | one two storeys, one one — one style, two plots |

## The four approaches, and why they differ

The monument stands on open turf and the ground round it is composed rather than decorated. The combe
is the way in from **below** — a pinned pan five blocks under the down, with a pond in it and a mouth
that opens onto the landing strand. The nab east of it is the way in from **above**: an eleven-block
push a player climbs and bridges down from. Between the combe and the monument is a beech shaw, which
is the way in **through**, and it carries cover to within fifteen blocks of the anchor.

The fourth is the plain walk across the strand, in the open, which is what an objective wants on at
least one side. Nothing stands within eleven blocks of the marker; `06-claims.txt` reads the goal's
21 × 21 clearance empty.

## What the ground is made of

Three themes, and the two that are not the default are each a shape carrying its own paint.

| Theme | Cells | On |
|---|---|---|
| `down` | 7 740 (79.7%) | the whole board — turf, worn chalk and bare chalk banded on the **slope** axis |
| `combe` | 988 (10.2%) | the dry valley floor: gravel and coarse dirt over earth |
| `yard` | 978 (10.1%) | the steading's made ground: cobble, andesite and stone brick |

The slope bands cut at **20°** and **38°**, off this board's own `GET …/incline`: 45.5% of its ground
stands under 10°, 24.3% between 10 and 19 and 13.1% at 40 or steeper. A cut inside the second population
stripes every gentle flank row by row, which is why the number is read rather than carried over.

The biome is **Plains**. Grass tints `#91bd59` there, which reads fresh against sandstone; the chalk is
sandstone and smooth sandstone in a two-member cell pattern, which is a texture rather than a palette
shown off.

## What the numbers say

```
03-slopes.txt   9 324 walked, 382 scrambled, 0 barrier; 0 faces
06-claims.txt   placed 30, declined 0
04-routes.txt   spawn -> own monument: worst step 0, walked end to end
coverage        9 706 ground, 929 dead = 9.57%, four patches in the back corners
```

`EL1` and `SP8` both complain that the down and the back band step ten blocks. The plan tier walks the
pieces flat and cannot see the relief; the transect down the spawn's own door line, `(-6, 110)` to
`(-6, 76)`, reads **rises 0, falls 2, worst step 1, walked end to end**. The complaint is right about
the plan and says nothing about the board.

## What went wrong

**The board was 72 blocks wide and `G8` read a dead share of 0.272.** One goal and one spawn a team make
two journeys, and the flanks were on neither. Cutting the board to 56 took it to 0.155, taking the back
band from 24 blocks deep to 16 took it to 0.131, and cutting to 48 with the band stopping where the
down's corners did took the built board to **0.0957**.

**The combe was a push and its floor came out at y1.** A push is arithmetic on the solved surface, so
minus seven under ground that solves to nine is bedrock; the pool in it then cut three courses of bank
away and raised `DR-BANK`. A pinned `area` mark at y7 is level, and water fills whatever is level.

**Three boulders were declined `DR-STEEP` at 41°, 48° and 54°.** The seats raster answers where a rock
may stand and says nothing about the angle it would stand at, so the three positions were re-chosen off
`GET …/column`, which prints the ground's inclination on its first line.

## Limits

**The two back corners are still dead**, 334 and 271 cells, each one block from used ground. They are
behind the spawn, which is where SP2 says dead ground lives; taking them off would leave the spawn hall
a promontory with void on three sides.

**One destroyable a team and no second goal.** That is the commonest destroy map there is, and it is
what a 48-block board wants — two goals here would be one objective with two health bars.
