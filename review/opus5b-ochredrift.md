# Ochre Drift — capture the wool

> A red mesa mining camp over a dry wash, two wools on spurs at the far corners of a team's ground, one
> bedrock line across each spur's mouth, and a T of void through the middle of the hub.

**In one sentence:** a raider on Ochre Drift picks a hand at the wash and cannot change it afterwards,
and a defender holds two prepared lines and cannot hold both.

96 × 208 blocks, `rot_180` about the origin, base surface 9, build ceiling y52, ground y7..y28. Two
teams, two wools each, 32 blocks of void between the two halves.

## What is where

| Thing | Where | Measured |
|---|---|---|
| the west wool | room `x -48..-32, z 80..92`, wool at `(-40, 86)` | three faces on void, one connecting piece |
| the east wool | room `x 32..48, z 80..92`, wool at `(40, 86)` | the same, mirrored across the yard |
| the spawn | `(-5, 94)`, a 10 × 16 hall in a 20 × 20 piece | 38 and 43 blocks from its two wools |
| the walls | `hub-w ↔ w-approach` and `hub-e ↔ e-approach` | 16 blocks of bedrock each, 20 in front of a room's face |
| the notch | `x -12..12, z 16..36` | the gap between the two frontline legs |
| the slot | `x -32..32, z 36..52` (48 in the middle) | the rotation hole; it meets the notch at `z 36` |
| the funnel | `x -48..-32` and `x 32..48` at `z 36` | the only ground joining the wash shelf to the hub |
| the terrace | `x -16..16, z 64..104` at y21, `relief_scope: exclude` | a 6-block face onto the hub, with a flight cut into it |

## The T of void is the board

Two holes are made by arrangement and no piece covers either: a notch between the two frontline legs and
a slot across the hub. They meet, so what the compile declares is one T through the middle of a team's
own ground, and nothing bridges it because no build zone reaches it.

What that buys is the funnel. The only land joining the wash shelf to the hub is sixteen blocks at each
end, and a ramp is cut through each — a `line` mark, `r 5`, `tread 3`, eighteen blocks of run for six of
rise. A transect up the west one reads **rises 6, worst step 1, 0 barrier, walked end to end**.

The frontline is what a build zone touches, and `FR6` caps it at sixteen cells. One piece across the
whole 96-block face read **24**; the two legs read **ten each**, and a raider who has crossed the wash
has committed to a side of the board before meeting anyone.

## Made ground meets grown

The crusher terrace is the one piece of made ground here and it says so with `relief_scope: exclude` on
its compiled shape. `hold` would let the relief bring the hub up to it and there would be no step and no
reason for a flight; `exclude` keeps the raw column and the two tiers meet at a face. `03-slopes.txt`
names that face as the board's largest: **64 cells at `x -16..15, z 64..65`**.

The flight is a made layer of its own, a polygon whose `anchor_heights` are `[15, 15, 21, 21]` over
twelve blocks of run. Read back along `x 0` it is six treads two deep, **rises 6, falls 0, worst step 1,
walked end to end** — which is what `EL1`'s complaint about the same seam cannot see, because the plan
tier walks the pieces flat.

## What the ground is made of

| Theme | Cells | On |
|---|---|---|
| `mesa` | 6 260 (54.1%) | grass and podzol on the flats, red sand on the shoulders, hardened clay and red sandstone on the risers |
| `wash` | 2 904 (25.1%) | the dry wash floor between the frontline legs: red sand and gravel |
| `works` | 2 400 (20.8%) | the crusher terrace: stone brick, polished andesite and cobble |

The slope bands cut at **10°** and **30°**, off `GET …/incline`: 69.8% of the board stands under 10°,
15.8% between 10 and 29 and 7.2% at 40 or steeper. Both cuts land on bucket walls.

The biome is **Mesa**, which tints grass `#90814d`. That is where podzol's brown comes to meet it, so
the pair reads as one dry, leaf-littered floor instead of as two grounds.

The buildings are pale sandstone and birch on a grey plinth, because the ground is red and a building
has to read as built by not being in the ground's family. The stamp mill stands on the wash edge with
one side against the coast, which `DR-PASS` allows; the winding house is on the east arm of the hub.

## What the numbers say

```
03-slopes.txt   11 118 walked, 318 scrambled, 128 barrier; 2 faces, largest 64
06-claims.txt   placed 28, declined 0
coverage        11 564 ground, 0 dead = 0.0%, 21 journeys
```

Zero dead share is not luck. Two wools and a spawn a team make twenty-one journeys between them, and a
board whose ground is four narrow limbs round a hole has nowhere for a journey not to go.

## What went wrong

**`G8` read a fill-ratio of 0.654 against a band of `[0.201, 0.542]`.** The board was one solid slab
with a single hole in it. Splitting the frontline, opening the slot and taking the back band's west
sliver off brought the land from 6 528 blocks a team to 5 360, which is **0.537**.

**The first flight arrived nowhere.** `SK26` read the ground falling fifteen blocks within four cells of
its foot, because the foot stood on the slot's own edge. The slot's north edge moved from `z 52` to
`z 48` in the middle, which leaves four blocks of landing.

**Two acacias were declined `DR-ROAD` at cells the seats raster had marked free.** A copied recipe's
foot is every cell of its lowest course and it is not the anchor: the decline named `(-44, 44)` for a
tree asked for at `(-45, 44)`.

## Limits

**`SK27` stands.** The component compiles to four plateaus and two of them paint differently, which the
complaint calls one landform with a hard line at every riser. Here the second paint is the crusher
terrace, which is excluded from the relief and is made ground rather than a plateau of the same
landform; the complaint is right about the shape of the document and wrong about this board.

**The two wool rooms are mirror-exact.** `match-flow.md` §6.5 says which wool falls first is then decided
by the flank rather than by distance, and that both teams will take the same hand in their own frame.
The T of void is what makes the two hands cost different things; whether it is enough is not something
this repository can answer.
