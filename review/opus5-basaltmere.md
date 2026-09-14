# Basaltmere — the hill has no back to it

> A king-of-the-hill board in a black basalt bowl with one mere in it. The point stands on a stack in
> the middle of the water and can be entered from every quadrant at once.

**In one sentence:** there is exactly one piece of commanding ground on this board, it is an island,
and the four ways onto it — two dry causeways off the benches and two shingle spits off the east and
west flanks — arrive from four different directions, so holding it is holding a place with no back.

90 × 190 blocks, `rot_180`, three surfaces, maxPlayers 20, ground y9..y25, observer y62, score limit
750, one hill paying 1/second on a 6s capture.

## The arrangement

Three surfaces and three shapes: `strand` at 10 (the drowned shelf, crossing the centre and its own
image), `brink`+`bield` at 14 (the benches over the water), `staith` at 15 (the spawn). The board is
one continuous sheet of ground — no void seam — and the `deep` build zone covers the water, so the
one place a player may make ground is the mere.

The relief is four `area` marks and two `push`es. `pan` states the mere floor flat to its own outline,
and its ring **wanders between z 18 and z 34** rather than following the seam between two plan
rectangles — a rim that is a rectangle's own edge reads as a ruler laid across the board. `bench` and
`howe-flat` are the two flats the spawns come out onto; `apron` drops the east bench a hand lower so
the two flanks are not the same ground. The `crag` push raises the west bench seven blocks
(`amount/falloff` 0.44 against `crown`/half-width 0.44).

The stack is a shape with `relief_scope: "exclude"` and `keepClear: true`, so the mere floor and the
stack top meet at a face. A broken ring wall crowns it on a `kind: "made"` layer, with one gate on each
of the four approaches — east, south-east, west, north-west.

## What the reads say

| read | number |
|---|---|
| `03-slopes.txt` | 12 628 walked · 152 scrambled · **720 barrier**; 8 faces, largest 314 at x −45..25, z 2..42 |
| `06-claims.txt` | **placed 42, declined 1** |
| relief read | level **0.651**, largestField **0.461**, 4 faces, 1 cliff, landform *rolling*, **0 seams**, 0 silent marks, symmetry error **0** |
| `GET …/coverage` | **47.2 % dead**, 3 journeys; two patches of 2 858 and 2 729 cells at (−28, 12) and (26, −14), both **1 block** from used ground |
| `GET …/incline` | 47.2 % under 10° · 22.9 % teens · 16.5 % twenties · 5.3 % thirties · 8.1 % at 40°+ |
| `05-themes.txt` | basalt 67.3 % · weed 29.7 % · stack 3.0 % |

## Against the fault catalogue

**Objective hidden — no.** `column (0, 0)` reads the pad (white stained clay) at y15 over six courses
of andesite, and nothing at all above it until the observer platform at y57. The crown wall's inner
face stands at radius 9.5 and the pad is 9 blocks across, so the wall is beside the point and not over
it.

**Spawn faces away — no.** Red spawns at (0, 87) with yaw 180 and the hill is at (0, 0), due −z. Zero
degrees off.

**Spawn faces a wall — no.** The spawn-to-board transect along z reads rises 0, falls 4, worst step 1,
0 barrier, 0 scramble, walked end to end.

**Stairs that end nowhere — no**, and this was measured per flight rather than assumed:
`walk from=40,4 to=0,0` (the east spit) is 47 blocks, **0 placed, 0 drops**; the west spit is 46 blocks,
1 placed, 0 drops. The two causeways run 35 blocks for a rise of 2 and the four beaches 12–16 blocks
for a rise of 4. `EL1` complains that `strand`–`brink` steps 4 blocks and is right about the plan and
silent about the board: the four beaches are authored flights and the plan tier walks the pieces flat.

**A straight frontline — no.** There is no frontline in the plan-rectangle sense; the boundary a player
reads is the waterline, and that is the `pan` mark's own wandering ring plus the pool's `shoreWander`.

**Stark contrast with no area separation — no.** The three grounds meet at things: black stack against
green weed at the stack's own face (74 + 54 border cells), and grit bench against weed at the
waterline (458 cells). Both boundaries are a face or a watercourse, not a colour change on flat ground.

**Flat, one theme, empty — partly.** Three themes, all on the ground, none under 3 %. The relief is the
healthiest of the four boards: 65 % of the ground under ten degrees with 46 % of it in one connected
field, no seams, no silent marks. But **47.2 % dead is the highest figure in this set and the weakest
number on the board.** The two big patches are the east and west lobes of the mere; each is one block
from reached ground, which is the Glassmere condition and not Ruddle Brink's whole-front scarp, and
the board is not split (8 faces, three walkable crossings of the rim a side). It is still the fault's
shape: both spawns and the only objective sit on x = 0, so the walker's journey is one straight line
down the middle and the flanks are on nobody's way anywhere. Moving the spits onto the east and west
flanks was meant to answer it and did not move the number, because the coverage read counts journeys
and not possibilities.

## Limits

- 720 barrier cells (5.3 % of ground) in 8 faces. `RL2` reads 0.6 scrambles per barrier and calls the
  elevation ungraded. That is what a terraced bowl of black rock is, and the crossings are stated
  rather than left to be found — but a reader who wants rolling ground will not find it here.
- The water is `level`-stated and therefore carves: every column inside a pool's outline is emptied
  down to the water line unless the shape under it is marked `keepClear`. `DR-DRY` still reports 162
  open columns of dug ground the pool does not cover, which is a dry grit fringe rather than a trench.
