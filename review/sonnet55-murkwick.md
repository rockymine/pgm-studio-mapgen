# Murkwick — a village island in a swamp

**A capture board on a wet bog where each team's hub is a raised island of ground round a pit, two wools stand at the ends of walled spurs, and the frontline between the sides is a wading marsh.** A thatched stilt platform stands alone on the mid stone. Willows stand on the hubs' rims and the halls wear hay roofs.

Slug `sonnet55-murkwick`, map name **Murkwick**, built on the deployed studio. The arrangement is composed board p16 t2 seed 43, taken whole, and the author's questions on the board are notes 28–32 (`reports/sonnet55-jungle-swamp.md`).

## How it is meant to play

**The arrangement is the composed one and it is balanced by construction.** Each hub is a ring of four pieces round a 16-block void, with a wool spur off the west side and another off the east, each behind a bedrock wall four blocks over the ground. An attacker walks 201 to 208 blocks to a wool and a defender 52 to 56, so neither wool is a raid and the other a walk-in.

**The frontline is the contested ground, and it is flat, wet and covered.** It is pinned level at 9 and the middle of it is drowned one course deep, so an attacker wades, and five hay stacks two and three courses tall give a player something to crouch behind. One willow stands at its back corner and no other tree, and the mid stone carries the one platform.

**The mid stone's stilt platform is the board's one perch.** Its deck course is at y12 over a stone whose top block is y8, on four stilt legs and four roof posts, with a three-step stair up the east side. It sees both frontlines, and note 29 asks whether that is too much.

## What the ground is made of

**Olive turf with podzol and coarse dirt, over peat beds.** Swampland's tint is `#6a7039`, which podzol's brown meets rather than fights, so the turf and the earth read as one dry leaf-littered floor. The bands are cut by angle at 40 degrees for turf and 14 more for earth; the wall and fill are peat beds over rock written out bed by bed.

**The mud is dirt, podzol and coarse dirt, and it is patches with reasons.** The mud flat sits on the frontline round the marsh, and three peat patches cap the hub's hammocks. Mud is 6.1% of the ground and peat 2.9%, and nothing is scattered by a noise field.

**The built family is dark timber under hay thatch, and the thatch is the accent.** The halls are dark oak and spruce over andesite and stone brick with roofs of hay bale, and the platform and the stacks share the thatch. Planked roads on the ground are spruce, dark oak and coarse dirt.

## How the relief was decided

**Four reliefs were sketched and driven unpainted, and the ground is the last.** The board is a third land and its hubs and aprons are flat by design, so the numbers are read against that.

| Sketch | What it states | relief | level | largest field |
|---|---|---|---|---|
| a | the hub two over the flat, nothing else | 2 | 0.88 | 0.412 |
| b | the hub three over, grading up across the front bar | 3 | 0.80 | 0.399 |
| c | the hub at 10 with two basins sunk in its bars | 3 | 0.80 | 0.203 |
| d, shipped | b, plus seven low hammocks | 6 | 0.65 | 0.182 |

**The shipped ground is still over the table line, and on this board that is the arrangement.** A level of 0.65 and a largest field of 0.18 are over 0.45 and 0.13, and the hammocks two and three high are what bring it down from 0.80. The spurs at the wool rooms, the frontline and the mid stone are pinned flat on purpose, since a hill in a wool lane is the fault the rulings name.

## What went wrong

**A pond stated in the spawn's door lane lost its water without a word.** Pond-back first stood at (5, 88), inside the lane the spawn door keeps clear, and the store answered 200 with no decline while `column` read stone at (5, 88) and water only at x 12 and 13. It moved to (−12, 88), west of the lane.

**The mid stone rose two blocks I had not stated.** Nothing pinned it, and the relaxation between the two hubs' marks lifted its top block to y10; `column` at (0, 0) showed it, and a mark at 9 over the stone put it back to y8 and the platform's legs on it.

**The stilt platform's deck and legs stood on one layer, and its steps ran the wrong way.** `SK9` declined the deck's columns under the legs, and the steps rose away from the deck until `column` at (5, 0), (6, 0) and (7, 0) read one, two and three. Deck, legs and posts are now three layers and the steps fall 3, 2, 1 away from the deck.

**The marsh first dug a wall out of a hummock's skirt.** `DR-BANK` said the carve cut three courses at (10, 37), which was the east hummock's skirt inside the pool's ring; both hummocks moved to the prongs and the marsh stands on level ground.

## Coordinates

| Feature | Team 0 (red, z > 0) | Read |
|---|---|---|
| spawn | (4, 104), a dark-oak hall under hay | `column` (4, 104) |
| wool a | room x −48…−40, z 68…80, wall x −29…−27 | walk, `04-routes.txt` |
| wool b | room x 40…48, z 60…72, wall x 27…29 | walk, `04-routes.txt` |
| hub pit | 16 × 16 void at x −8…8, z 64…80 | `column` (0, 72) reads void |
| pond front | 16 × 7, x −12…4, z 52…60, water y10–11 | `column` (−4, 56) |
| pond back | 14 × 7, x −19…−5, z 84…91, water y10–11 | `column` (−12, 88) |
| marsh | x −14…10, z 34…44, one course of water | `column` (0, 39) |
| stilt platform | deck y12, x −7…5, z −4…4, roof y17–20 | `column` (−5, 0), (−7, −4) |
| planked walks | front pond x −6…−3, z 50…62; back pier x −13…−3, z 87…89; deck y12 | `column` (−5, 51), (−12, 88) |
| hay stacks | five on the frontline, tops y9 and y10 | `column` (−14, 28) |
| dead ground | 0.0% | coverage |

Blue's features are the rot_180 images: block `(x, z)` maps to `(−x−1, −z−1)`, and the pond walks and hay stacks were read at their images (4, −52), (11, −89) and (13, −29).
