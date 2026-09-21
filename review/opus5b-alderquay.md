# Alderquay — a wool and a monument at once

> A dark alder holt on a delta channel, the monument in the open on the bank above a timber quay, and
> the wool on a spur at the back behind a bedrock line.

**In one sentence:** a team on Alderquay fights for two things at two depths, and the ground that
carries its raid out to the enemy's spur is the same ground its own monument watches.

72 × 224 blocks, `rot_180` about the origin, base surface 9, build ceiling y46, ground y7..y20. Two
halves, 32 blocks of void between them, and a channel running from that void up into each team's ground.

## What is where

| Thing | Where | Measured |
|---|---|---|
| the monument | `(30, 52)`, `pillar-3`, obsidian, `float: 4` | own-spawn walk **53**, enemy walk **187**, ratio **3.53** |
| the wool | room `x -36..-20, z 92..104`, wool at `(-28, 98)` | 47 blocks from its own spawn, three faces on void |
| the spawn | `(19, 102)`, a 10 × 16 hall in a 20 × 20 piece | `<gamemode>ctw</gamemode>` and `<gamemode>dtm</gamemode>` both declared |
| the wall | `holt-w ↔ spur` | 16 blocks, the spur's whole width, 20 in front of the room |
| the channel | `x -20..20` from the mid to `z 44`, then `x -20..12` to `z 60` | closed at the head by `holt-n` |
| the quay | a plank deck `x 13..24, z 46..62` at y11, on spruce posts from y8 | one course proud of the holt |
| the backwater | a pinned pan at y8, ring radius 9 about `(-28, 58)` | water at y9, on the west bank below the wool approach |

## Two topologies on one board

The destroy half puts the thing a team defends in its **own** ground: the monument is a short walk
forward of the spawn and the contested space is everything beyond it. The capture half puts the thing a
team wants in the **enemy's**: the wool a team must fetch is on the other side of the board, behind a
prepared line. So a team's own spur and its own monument are both defences, and its errand is a long
run out and a longer run back.

There is no hole inside a team's own ground, and the destroy half decided that. `approaches.md` withdraws
the middle-of-terrain hole on a destroy board, because a hole between the objectives and the middle
empties the ground the contest happens on. What it endorses instead is a river, and that is what the
channel is — a drop that forces a bridge, which is a chokepoint that has to be built before it is used.

The backwater is the other half of the same ruling: a depression is an entrance from below, which a hole
does not offer at all. It sits on the west bank under the wool approach, so a player who drops into it
comes up where the wall is not.

## The quay, and why the monument is not on it

The quay is two made layers — a plank deck at y11 and a run of spruce posts from y8 under its river
edge. It has to be two, because a layer holds one span per column: drawn on one layer the posts and the
deck stack, `SK9` gives the column to the taller add, and the posts are simply not in the world.

The monument stood on the deck for one build and `SK18` read the made thing and the goal sharing the
courses of **50 columns**. The rasterizer lays a made layer and every stamper writes where it is told,
and neither reads the other. So the monument stands on the open bank four blocks east of the deck's
edge, which is where an objective wants to be anyway.

## What the ground is made of

| Theme | Cells | On |
|---|---|---|
| `carr` | 5 830 (68.3%) | the wood floor: grass and podzol on the flats, coarse dirt and clay on the banks, stone on the faces |
| `works` | 1 852 (21.7%) | the timber works' yard: cobble, andesite and stone brick |
| `reed` | 848 (9.9%) | the backwater's shore: clay and gravel |

The slope bands cut at **20°** and **40°**. `GET …/incline` reads 55.7% of the board under 10°, 20.7%
between 10 and 19, 13% between 20 and 29 and 3.7% at 40 or steeper, so the wood's floor takes three
quarters of the board and bare rock only what is actually a face.

The biome is **Swampland**, which tints grass `#6a7039` — dark enough that grass and podzol read as one
leaf-littered floor. The buildings answer it in white plaster framed in dark oak, which is the palest
thing standing on the darkest of the four boards.

## What the numbers say

```
03-slopes.txt   8 440 walked, 90 scrambled, 0 barrier; 0 faces
06-claims.txt   placed 32, declined 0
coverage        8 530 ground, 132 dead = 1.55%, 21 journeys
```

`EL1` complains at five seams, the largest four blocks. The transect across the holt-to-yard seam at
`x 20`, from `z 64` to `z 82`, reads **rises 4, falls 0, worst step 1, 0 barrier, walked end to end**.

## What went wrong

**The board was solid and `G8` read a fill-ratio of 0.768.** Cutting the front into two eyots with the
channel between them, and carrying that channel up between the two banks, took the land from 6 192
blocks a team to 4 192 — **0.520** — without putting a hole anywhere the destroy half forbids one.

**The quay's deck material was a `cell` pattern with no `rise`.** `PT4` refuses that at the store door:
a sampled field on a bucket read from the side resolves every block of a column alike and comes out as
vertical stripes.

**The house style's verge was a bare log.** `HS3` refuses it — a log has no axis and stands every one of
them on end — and names the laid log as the fix.

**A second building could not be seated.** The works yard holds none, because the spawn hall's own door
apron is kept clear for thirty blocks in front of it; put anywhere the seats raster allowed, the shed
either fell inside the sawmill's claim or left the pair with no eight blocks of passable ground down one
side. `DR-PASS` is asked of a group of buildings rather than of each one.

## Limits

**One building and one quay.** Two dressing ideas is thin for a board this size, and the reason is the
seats raster rather than the author: 80 cells on the whole board will seat a 9 × 6 house.

**The channel reaches the mid, which makes it an inlet rather than an interior hole.** That is the
reading this board is built on and it is a judgement, not a measurement: `approaches.md` bans a hole
between a team's objectives and the middle, and endorses a river, and this is both.
