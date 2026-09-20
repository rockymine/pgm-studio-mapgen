# Report — opus5-orchard-holm

## What I set out to build

The author's own `example 3` plan with three changes, made to say something the board could not say before:

- **the lane straight out of spawn runs five blocks further into the void**, and the build zone with it. A
  15-block lane takes a building seven blocks across including its eaves — which is a 5×5 wall footprint,
  exactly `DR-SIZE`'s floor — and nothing else, anywhere in it. Twenty blocks take a twelve-block one. That
  is what the widening is for and it is where the buildings went.
- **the terrain either side of the middle is pulled back ten blocks**, which leaves fifty blocks of gap.
- **a holm sits in the middle of it**, 30 × 20, two courses above the team ground, carrying a golden apple
  generator on its own pad at the board's centre.

Capture the wool, one room a side, `rot_180`. Slug `opus5-orchard-holm`.

## Where the buildings went, and why it is not a guess

`POST /map/{slug}/sketch/seats?kind=house&width=&depth=` answers `DR-PASS` forwards over every cell, so
every building here stands on a seat the board offered rather than on one I tried. Asked of the built board:

| footprint | seats | what refused the rest |
|---|---|---|
| 10 × 10 | 120 | 2 776 `DR-KEEP`, 2 297 `DR-SITE`, 1 409 `DR-PASS` |
| 7 × 7 | 218 | 2 662 `DR-KEEP`, 2 110 `DR-SITE`, 1 610 `DR-PASS` |
| 5 × 5 | 625 | 2 538 `DR-KEEP`, 2 329 `DR-PASS`, 1 108 `DR-SITE` |

The 10 × 10 answer in the lane is **two anchors, x −25 and x −24**, and nothing further east. That is the
whole story of the widening in one row of a mask.

**The measured result**, across the lane at the longhouse (`transect -28,-48 → -2,-48`):

```
  x -28 .. -27   void
  x -26 .. -15   house longhouse        12 blocks, the stamp with its eaves
  x -14 ..  -6   ground, y 11            9 blocks, the passage
  x  -5 ..  -2   void
  rises 1, falls 0, worst step 1: 0 barrier, 0 scramble | walked end to end
```

The eave at x −26 oversails the void: the band runs along the walls and the wall is on ground, so the coast
side reads as an edge and the house stands. On the lane the plan drew, it could not have.

**The byre is four blocks off the longhouse's gable** — two blocks between their stamps, one free block
between the byre's stamp and the longhouse's ring. The two are one block of buildings, the passage is owed
round the pair, and neither is complained of. Judged on its own with the longhouse standing, the byre's
north side is a wall.

## What the reads said

```
03-slopes.txt   cells: 6600 walked, 0 scrambled, 0 barrier
06-claims.txt   placed 28, declined 0
coverage        ground 6600, reached 6600, dead 0 — 0.0% over 10 journeys
05-themes.txt   pasture 6000 cells (90.9%), orchard 600 (9.1%), 16 surface blocks
```

`GET /api/map/{slug}/column?at=0,0` and its three neighbours read **Gold Block at y 10**, flush with the
holm's podzol, and `(2, 2)` does not — the pad is the 2 × 2 the board's own centre line asks for, which is
what a whole-number `at` means and a `.5` would not have given.

## Two things I got wrong and the read that said so

**The ground was finished by an angle it does not have.** I wrote the slope stack from the worked example —
bands cutting at 30° and 45° — and the theme census came back with Grass Block and nothing else. `GET
…/incline?format=text` says this board is **77% under 10°, 22.6% in the teens, 0.5% above twenty and
nothing at all past forty**: every cell was in the first band. Recut to 10 / 10 / 80 and the census carries
Coarse Dirt, which is the shoulder of every swell on it. The instrument was in the skill and I reached for
the example's numbers instead of the board's.

**A mark is not a prop.** I stated every relief mark twice, mirrored by hand, and every tree and boulder
twice as well. `RL4` named all four twins as pinning nothing, and `DR-CLAIM` declined ten props against
their own orbit images. A prop is stamped at **every image of its orbit**, so one side is the whole board;
a relief group is one side's ground and the rasterizer mirrors what it solves. Stating either twice is the
same mistake from opposite ends.

Also: `tread` is a **line** mark's field. I put one on a point mark to grade an `RL3` seam and the seam did
not move. Two marks pinning their bands exactly put the whole difference in the one cell where they touch,
so the fix on a point is to state heights that are a block apart, not a shoulder it does not have.

## What I added to the tooling

`tools/drive.py` carried no `spawners` key. It rides on the intent exactly as `controlPoints` and `shops`
do, and for the same reason — the plan states no generator — so `patch_intent` now passes it through and
prints what it drops.
