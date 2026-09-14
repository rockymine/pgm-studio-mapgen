# Slakemoss — the short way is the one where you are wading

> A destroy-the-core board in a hall the moss and the water took back. Each core stands on a dry
> plinth inside a ruined chapter house; between them the nave is roofless and under water.

**In one sentence:** the short way to the enemy's core is straight up the middle of a flooded nave,
in the open, with the arcade standing either side of you and nothing overhead — and the long way is
round the fen on a flank, dry and slow and out of sight.

90 × 200 blocks, `rot_180`, four pieces at four surfaces, maxPlayers 20, ground y12..y24, observer
y62. Cores float 6 and leak at 5, so there are two courses to dig.

## The arrangement

Four surfaces one course apart, and each is a place rather than a hook for a theme: `nave` at 13 (the
drowned floor, crossing the centre and its own image), `fen` at 14, `court` at 15, `frater` at 16.
The `nave-zone` build zone covers the middle 40 blocks of the water, so bridging the nave is what the
short way costs.

The relief is four `area` marks and two pushes. `floor` states the nave flat to its own outline
because a flagged floor is what it was, and its ring is its own `rot_180` image so both groups solve
the same floor and agree across the middle. `reeds` drops the east flank a hand below the fen — the
slow dry way round — and the `bank` push raises the west flank six blocks out of the hall's own
rubble (`amount/falloff` 0.43 against `crown`/half-width 0.43).

## The ruin, written in the sketch's own shapes

Two `kind: "made"` layers, both mirroring:

- **the chapter house** — one annulus polygon at (−14, 56), outer radius 8.5, wall two thick, floor
  17, eight courses high, with three breaches cut as override adds on the three bearings an attacker
  can arrive from: the nave, the west bank and the stair up from the court. An annulus is one even-odd
  polygon, so a round wall costs one shape and no subtract, and `SK13` never sees a negative space.
- **the arcade** — eight piers, three blocks across, ten apart, down both banks of the nave at x ±21,
  floor 13, nine courses. Ten apart matters: the first cut had them six apart and five across, and the
  route read walked the east row as a barrier every six blocks.

The plinth under the core is an ordinary sketch shape carrying `relief_scope: "exclude"` and
`keepClear: true` — a face rather than a ramp — with **two** stated ways up: the processional stair
from the court (18 blocks for a rise of 2) and a broken ramp off the fen on the west (10 blocks for a
rise of 2). A core behind one stair is a core nobody takes.

## What the reads say

| read | number |
|---|---|
| `03-slopes.txt` | 14 292 walked · 182 scrambled · **326 barrier**; 4 faces, largest 86 at x 14..44, z −43..−35 |
| `06-claims.txt` | **placed 38, declined 3** |
| relief read | level **0.713**, largestField **0.486**, 1 face, 1 cliff, landform *plain*, **0 seams**, 0 silent marks, symmetry error **0** |
| `GET …/coverage` | **27.2 % dead**; largest patches 1 842 cells at (35, −2) and 1 823 at (−37, 0), both **1 block** from used ground |
| `GET …/incline` | 62.8 % under 10° · 21.6 % teens · 9 % twenties · 2.5 % thirties · 4 % at 40°+ |
| `05-themes.txt` | slake 40.4 % · fen 31.5 % · garth 28.1 % — the most evenly divided board in this set |
| `GET /plan/evaluate` | score **0**, and the goal term reads own 41 / enemy 154, ratio **3.76** (`GO1` wants 3–4) |

## Against the fault catalogue

**Objective hidden — no.** `column (−14, 56)` reads ground at y16, the core's chest at y17, the
obsidian casing at y23 and y27 with three courses of lava between, and then nothing at all until the
sky marker at y55. The casing stands in open air inside a wall eight courses high with three breaches
in it, so it is visible from the nave, from the west bank and from the head of the stair.

**Spawn faces away — no.** Red spawns at (0, 92) with yaw 180; the bearing to the enemy core at
(13, −57) is 175°. Five degrees.

**Spawn faces a wall — no.** The court is stated flat by `court-flat` with a `tread`, and the first
draft's `howe` push sat over the spawn's own pad and met the room mark on a three-block step —
`RL3` named it at (−15, 79) along 30 cells of boundary. Moving the push east of the court cleared it,
and the relief read now answers zero seams.

**Stairs that end nowhere — no.** Both plinth flights are `height_mode: "level"` with
`anchor_heights`, `skirt: 0` and a material of their own, and both run at five or more times their
rise. The two slipways off the fen into the nave are the same shape.

**A straight frontline — no.** The board has no frontline: the nave crosses the centre as one sheet
and the boundary a player reads is the waterline, which is the pool's own `shoreWander`ed ring inside
the `floor` mark.

**Stark contrast with no area separation — no.** fen meets garth over 300 border cells at the
plinth's and the court's own faces; fen meets slake over 260 at the waterline. Both are a face or a
watercourse.

**Flat, one theme, empty — three themes at 40/32/28 %, and the flattest ground in the set.** The
relief read calls the landform *plain* at level 0.713. That is what a hall's floor and the fen round
it should measure, and the board's verticality is in the ruin — a wall eight courses high, sixteen
piers nine courses high, a plinth with a face — rather than in the terrain. It is the one board of the
four where a reader could reasonably ask for more ground under the buildings.

## Limits

- The route read walks the east pier row and reports `barrier +9 / drop −9` at x ≈ 20–21 repeatedly.
  The transect straight across the nave at z 0 reads **zero barrier over 90 stations**, so the route
  walker is threading the arcade rather than being stopped by it — but a reader of `04-routes.txt`
  alone would think otherwise.
- 27.2 % dead, in the two flank lobes of the fen, each one block from used ground. Two objectives and
  one spawn a side is what keeps it that low; a third journey across a flank would take it lower.
- The `garth` theme census carries `174:0 Packed Ice` from the `hoar-store` shell. It is one building's
  roof and not terrain, but it is the one block on this board that is not dark, wet or green.
