# Frostvault: the plan

Capture the wool, two teams of twenty-four, two wools a team. A board the studio's generator composed, read as a
bunker the way Coldstore taught: its land islands in the void, its holes pillars, the world outside rock, a roof over
all of it. `scripts/layout.py` holds the numbers, `assets/composed.json` the composed board, and
`renders/plan.txt` the bunker plan a cell a character.

## 1. Where it comes from

**The generator composed it: 24 players a team, mirrored across z, seed 11, at five blocks a cell.** Its deriver
reads a hub with two holes in it, a frontline with two notches, two wool approaches a team and a channelled crossing
with two stepping stones. `pgmvox/data/compose_board.cs` wrote all of it to `assets/composed.json`.

**`plan.bunker.draw` makes four exchanges on it.**

| The generator's | The bunker's |
|---|---|
| land | an island: a slab with its deck at y 17 over the void |
| a build region, the crossing | void, crossed by bridging under the roof |
| an enclosed void: the hub's holes, the frontline's notches | a pillar of bedrock from the floor to the roof, 104 cells of them |
| the world outside | rock, the bunker's walls, with a moat of void two cells wide along every shore |
| a wool room | rock, its seal on the void, the land in front of it cut back two cells |
| a spawn room | a hall cut into the rock, opening onto the hub |
| a defence wall (model.md §5.14) | a seam of rock from the floor to the roof, on 12 seams |

## 2. The islands

**The generator draws one island a team, joined from the spawn to every wool; the concept is islands in the void.**
So the board is cut with the generator's own isolation cut: each wool's approach and the frontline are cut from the
rest of the team's land by two cells, ten blocks, of void. A box is not cut where that would leave it fewer than
twelve cells, so the smaller wool approach stays joined to the hub and only its seal's front is cut.

| Island, each team | Cells |
|---|---|
| the hub, with the spawn's door and the two wool monuments | 147 |
| the far wool's approach | 54 |
| the frontline | 49 |
| the stepping stone in the crossing | 28 |

## 3. The wools, the seals and the rules

**They are Coldstore's.** Each wool room is sealed from its face inward by a glass case, a capsule of 588 end stone,
a gap and a screen; 90% of the capsule broken by TNT opens the screen's middle. Only what a player brings, the snow
on the islands, the cases' glass and, by a blast, the end stone may be broken. Blue keeps orange and lime in the
south and takes purple and yellow from the north; red the reverse.

## 4. As built

`scripts/walk.py` writes `renders/walks.txt`.

| Walk | Blocks |
|---|---|
| spawn to its own two wool monuments, on foot | 11, 10 |
| spawn to its own seals, bridging | 121, 136 |
| spawn to the enemy's seals, bridging | 226, 331 |
| every seal blown: spawn to the enemy's wool / the wool home | 244 / 234, and 349 / 336 |

**While a seal stands its wool is reached in no phase; blown, the walk is the same bridged, in the sky and dug.**
The roof leaves no sky route shorter than a bridge, and walling the seal shuts the room again in every phase.

## Open

- The board is the generator's size for 24 a team, and the farther wool is 331 blocks of bridging from the enemy's
  spawn. A smaller request, or cutting less, would bring it in.
- The hub is still one island of 147 cells; cutting its pieces from each other is a parameter away (`cut`), and
  whether the hub should be one floor is a question for the author.
- The ice field over the roof is Coldstore's alone.
