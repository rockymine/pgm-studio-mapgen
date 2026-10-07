# Ember Reach — an autumn river valley

> A destroy-the-monument board for two teams, sixteen a side: a slow river between two banks, a watermill
> on each, one monument a team, valley sides that rise toward the flanks, and a dugout cellar to fight in.

**In one sentence:** a russet valley where a river runs across the middle of the board, each team's
monument stands in an open yard forty-four blocks from its spawn, the valley sides rise ten blocks over the
lane on both flanks, and a roofed dugout beside the yard is the way in from below.

104 × 224 blocks, `rot_180` about the origin, base surface 20, build ceiling 37, y 0..45. Two islands, one a
team, with a 32-block gap between their banks (`z = −16..16`) that holds a river and a build zone.

## How it is meant to play

An attacker leaves the spawn (0, −102) for the enemy monument at (13, 59), walks 51 blocks of own ground
against 165 for an enemy (`GO1` 3.24), and has to cross the river. The crossing is a choice of three: bridge
over the water from the bank, drop in and swim, or go round — and there is no round, because both banks end
in void at `x = ±44`. A swimmer meets a wall 6 above the water on the far
side, so leaving costs the blocks it took to build the way out (the walk read it as four placed).

The monument stands in a flat yard with the west valley side above it, the east valley side across the lane,
a dugout beside it and a granary behind. The approaches differ: around (the lane), above (the two sides,
nine and eight blocks over the yard), below (the cellar), through (the miller's house and the granary).

## What the ground is made of

Three themes. `valley` is the ground and the valley sides: a `layered` stack on the `slope` axis, turf to
46°, dirt and coarse dirt to 58°, stone and andesite beyond, over a stone fill. `bed` is the riverbed —
coarse dirt, sand and sandstone. `yard` is laid ground: granite, polished granite and andesite, on the two
mill yards and in the cellar.

The three tone families are ground (russet turf, podzol, dirt), built (granite, dark oak, grey stone, the
hay roofs' gold) and accent (the hay). The biome is Mesa, which tints grass `#90814d` and leaves `#9e814d`,
so the board reads brown and olive in a game client without a block of it being orange.

## The techniques, and what each bought

**An authored plan of two pieces and a zone.** `hall` (the spawn) and `bank` on one team, the river a build
zone. The first plan had the river as a neutral piece joining both banks, and the studio refused it as `PL12`:
a land connection between two sides it copies. The refusal was the author's ruling stated by the studio.

**The river is ground below the banks.** A 88 × 32 sandstone-and-sand bed with four blocks of ground under a
`pool` fluid prop at level 8. The pool's ring is drawn past the bank's last column, because it stood one
column short and `DR-DRY` named 156 open columns until it was widened.

**Relief by marks and pushes.** Five marks pin the hall, the monument yard, the house pad, the mill pad and
the waterside line; four pushes make the valley sides and the head of the valley; `grain` 1.6 over 16 blocks
brings the share of ground under 10° from 44% to 41% and the largest level field from 22% to 14%.

**A cellar sunk by `sink` shapes.** One floor (10 × 12, five deep) and five one-block steps, roofed by a
turf slab on a `made` layer at y21. The floor is y14 and the roof deck y21..22, six blocks of headroom,
with the stair climbing out to the road at (−11, −80).

## What went wrong

The first pass declined the watermill (`HP3`, 224 blocks over the 192 cap), put two houses on hillsides
(`DR-DIG`, ten blocks of dig), seated two trees past the board's edge, and spelled the biome with a field
that does not exist. The biome one was silent: the store answered 200 with no `RQ3` the driver printed, and
only an anvil read of the world showed byte 1. A second pass added end levees to hold the water, and the
walk then found a land route across them, so they were removed.
