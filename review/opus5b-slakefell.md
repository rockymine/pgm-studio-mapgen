# Slakefell — destroy the core

> A cold slate fell in three benches over a frozen tarn, the core in a walled fold on the middle bench,
> and every way up the fell a cut ramp.

**In one sentence:** the raid on Slakefell is a climb, and the defence knows the four places it arrives
by.

48 × 216 blocks, `rot_180` about the origin, base surface 9, build ceiling y59, ground y9..y30. Two
landmasses, 16 blocks of void between them, a build zone over the whole face.

## What is where

| Thing | Where | Measured |
|---|---|---|
| the core | `(-14, 48)`, `lava 3`, `lavaHeight 3`, `float 6`, `leak 5` | own-spawn walk **49**, enemy walk **151**, ratio **3.08** |
| the fold | two drystone arcs on a made layer, `floor 17`, three courses | the casing's lowest course is y24, the wall tops at y20 |
| the spawn | `(-1, 94)`, a 12 × 12 hall in a 20 × 20 piece | two doors, onto the brow and onto the east fold |
| the benches | strand y9, core bench y17, brow y25, lodge apron y29 | pinned `area` marks with three-block gaps, so each riser is a face |
| the ramps | four `line` marks, `r 5`, `tread 3`, 18 blocks of run for 8 of rise | `(-18, 22)→(-18, 40)`, `(16, 22)→(16, 40)`, `(-4, 56)→(-4, 74)`, `(18, 56)→(18, 74)` |
| the crag | a push at `(14, 44)`, `amount 9`, `falloff 10`, `crown 4` | 54 blocks from the casing, clear of it by its whole reach |

## The fell is a face with ramps cut through it

The three benches are pinned flat and the gaps between them are three blocks, so a riser falls eight
blocks over three and is a wall rather than a grade. `03-slopes.txt` counts **52 barrier cells in four
faces**, the largest 18 cells — the risers, and nothing else on the board.

Four `line` marks cut through them, two on each riser and on opposite hands. A line mark pins its band
to a height per vertex, so a mark stating `h: [9, 17]` over eighteen blocks is a ramp; its `tread` keeps
three cells either side of the centreline flat and lofts the rest into the face. Both lower ramps read
**rises 8, worst step 1, 0 barrier, walked end to end** on a transect, and so do both upper ones.

What that buys is the shape of the defence. An attacker who has crossed the tarn has two ways onto the
core's bench and two more onto the brow above it, and a defender on the fold can watch one pair at a
time. The core itself has ground on every side of it, which is what a casing wants: a breach near an
edge ends it at once.

## What the ground is made of

| Theme | Cells | On |
|---|---|---|
| `fell` | 6 442 (69.9%) | snow and turf on the benches, gravel and worn earth on the shoulders, slate on the risers |
| `works` | 2 036 (22.1%) | the fold's floor and the lodge yard: stone brick, andesite and brick |
| `tarn` | 740 (8.0%) | the frozen tarn's shore: gravel and clay |

The slope bands cut at **20°** and **40°**. `GET …/incline` reads 45.5% of this board under 10°, 15.3%
between 10 and 19, 16.6% between 20 and 29 and 11.6% at 40 or steeper, so both cuts sit on bucket walls.

The biome is **Ice plains**, which tints grass, leaves and water `#80b497`. A snowfield on `Plains` has
a summer meadow running through it; here the cell pattern of snow block and grass reads as one patchy
cold ground.

## The buildings

Dark timber on a brick plinth under a brick roof, which is the one warm thing on a slate-and-snow board.
Two of them: a store on the strand by the tarn at `x -2..6, z 18..23`, and a byre on the lodge band at
`x 14..22, z 88..93`, one two storeys and one one.

The bench holds neither, and that is measured rather than chosen. The core's clearance takes the west of
it and the crag's skirt the east, and a byre tried at `x -2..8, z 42..49` was declined `DR-SLOPE` for
ten blocks of rise across its own plan.

## What the numbers say

```
03-slopes.txt   8 558 walked, 608 scrambled, 52 barrier; 4 faces, largest 18
06-claims.txt   placed 28, declined 0
04-routes.txt   spawn -> own core: worst step 0, walked end to end
coverage        9 218 ground, 615 dead = 6.67%
```

## What went wrong

**Three props were placed by eye before the seats raster was read.** A store in the lodge yard was
declined `DR-KEEP` on the spawn's own door apron, a byre beside it complained `DR-PASS`, and a fir was
claimed by a pine six blocks away. Every position on the board now comes off
`POST …/sketch/seats` for its own kind.

**A boulder read 54° at `(10, 28)`.** The seats raster marks a cell as a legal seat and says nothing
about its angle, and `DR-STEEP` is a rock's rule and nobody else's. `GET …/column` prints the
inclination, so the three erratics stand at 0°, 0° and 14°.

## Limits

**The two back corners are dead**, 194 and 92 cells behind the lodge, one block from used ground.

**The fold is decorative, not a region.** It is a made layer and carries no filter, so it slows a player
down and does not keep one out; what defends the core is the four ramps and the ground round the casing.
