# Coldstore: the plan

Capture the wool, two teams of sixteen, two wools a team. A bunker under an ice field: one hall with a bedrock roof
24 blocks over its floors, no floor of its own, islands and pillars standing in the void. `scripts/layout.py` holds
every number below as data.

## 1. The identity

**A bunker drawn as a normal capture-the-wool map turned inside out: where the map would have a void hole the bunker
has a pillar, and where it would have sky it has a roof.** The cold got in through the roof's fans, and its snow lies
in drifts on the islands, thickest under them.

The board is the author's concept quarter, finished. The concept's world held one quarter of it, with signs saying
what each piece is for; every rectangle in `layout.py` is measured off it, and the board's own code builds it. The
dressing is this board's, not the concept's.

## 2. The layout

Blue holds the west (u < 0) and red is its mirror image. Inside a team the south quarter is drawn and the north one
is its mirror across v -0.5, so the board has both mirror symmetries. It is 208 by 112 blocks of bunker.

| Piece | Where, in the drawn quarter | What it is |
|---|---|---|
| **The roof** | y 42 to 48, everywhere | bedrock; the build height is its underside, so nothing is built higher than y 41 |
| **The void** | under every island, between everything | nothing down to the world's floor; a fall is a death |
| **The hub** | a strip u -90 to -62 joined to its image, and a leg south to v 14 | the spawn's island, a T across the team's middle, its two wool monuments by the spawn's door |
| **The south-east island** | u -31 to -11, v 25 to 43 | an L of floor in front of the great door's alcove |
| **The pillars** | three in a quarter, 10 to 20 across | bedrock from the floor to the roof; two of them carry a vent tunnel at y 28 |
| **The wool block** | u -92 to -72, v 25 to 34 | the wool room, and the end stone seal in front of it in its glass case |
| **The walls** | the west, the south, the buttress and the bulk behind the wool block | bedrock under a skin of stone brick |

**The pillars are the concept's core.** A pillar is the negative of a void hole: it stops sight and movement from the
floor to the roof, the way a hole in an open map stops walking. The pillar on the line between the teams is twenty
wide, and its vent tunnel at y 28 is the one way through it.

**Every void between islands is about ten to twelve blocks.** It is crossed by bridging, under fire, with the roof 24
over the floor, so a bridge can climb but not get over anything.

## 3. The wools and their seals

**A wool room has no door: it is reached through its seal.** The room is three by six and four tall, at y 28 in the
wool block. In front of it stand a screen of panes, a gap, and a capsule of end stone ten deep in a glass case whose
faces are on the void.

**An attacker bridges to the case, breaks the glass and blows the end stone out with TNT.** End stone breaks by a
blast and by nothing else. At 90% of the capsule gone the seal is complete, and the map's trigger fills the screen's
middle, two wide and four tall, with air. The seal is a destroyable that does not count to win (`required="false"`).

| Wool | Taken by | From |
|---|---|---|
| Purple, yellow | Blue | red's south and north wool rooms |
| Orange, lime | Red | blue's south and north wool rooms |

**Each wool block carries the concept's arrow on its face toward the spawn**, pointing at the enemy and showing the
colour of the enemy's wool on that side: purple and yellow on blue's blocks, orange and lime on red's.

## 4. What may be broken

**Only what a player brings, the drifts, the cases' glass and, by a blast, the end stone.** The walls are bedrock
under one block of skin, so nobody hides in a wall or tunnels along it, which the concept's two-block walls allowed.
The drifts (snow, packed ice) grow back slowly where nobody stands; the glass and the end stone do not.

The kit carries 16 TNT, which lights as it is placed, and the crafting table is disabled.

**Beside each spawn a team builds nothing.** The pocket between the spawn and its wool block (u -90 to -73, v 5 to
24, in every image) takes no block from the team that spawns there, so it cannot wall its own seal's flank from home.
The concept marked the place with a line of redstone.

## 5. As built

`scripts/walk.py` writes `renders/walks.txt`.

| Walk | Blocks |
|---|---|
| spawn to its own two wool monuments, on foot | 10, 11 |
| spawn to its own seals' cases, bridging | 53, 54 |
| spawn to the enemy's seals' cases, bridging | 192, 193 |
| every seal blown: spawn to the enemy's wool / the wool home | 210 / 198 |

**While a seal stands its wool is not reached in any phase of a match.** Walking blue's spawn to red's south wool:
on the ground, bridged, in the sky and with the drifts dug away, no route gets in. With the seal blown it is 209 in
every phase, because the roof leaves no sky route shorter than a bridge, and walling the seal shuts the room again in
all three.

## Open

- The seal's size is the concept's: 588 blocks of end stone. How much TNT 90% of it takes is a number only a
  played match gives.
- Snow falling from the fans is drawn, not simulated; the drifts are where a fan would put them.
- The ice field over the roof and down the bunker's sides is scenery, so no bedrock shows from outside. No player
  reaches it; a shaft from each fan up through it shows the sky between the fan's blades.
