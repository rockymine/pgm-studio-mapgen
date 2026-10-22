# Chantry Gill: the plan

Destroy the monument, two teams, two monuments a team: one on each landmass. This file grows as the board is decided; the layout comes
first. `scripts/layout.py` is the layout as data, `scripts/sketch_layout.py` draws it (`renders/00-layout.png`),
and `assets/` holds the sheets every piece was designed and looked at on before the board was built.

## 1. The identity

**Two hill towns face each other across the void, each on a fell with a limestone scar beside it across a gill;
one monument stands on the town's rim over the gill and one on the scar's plateau, and the scar's leaning brow,
its chimney and the old adit under the gill are the ways at them that no street leads.**

## 2. The layout

Blue holds the south (z > 0); red is blue's image under the half turn, (x, z) -> (-1 - x, -1 - z). The board is
180 across and about 250 long; no piece of land is a rectangle.

| Land | What it is |
|---|---|
| **Main island**, the fell | about 110 across and 105 deep: the town on its east rim, the spawn at its back, fields between the town and the west |
| **Scenery**, the edge and the knott | the main island's west side and back: a scarp and a crag fenced off from the fell by their own faces, framing the board; nobody fights on them |
| **Side island**, the Scar | about 45 across and 85 deep, east of the main island: the tarn at its front, the plateau behind its leaning brow |
| **The Gill** | the gap between the two islands is a gorge, not void: 8 to 12 across, its floor about 9 under the town's rim; the brig crosses it near the front and a timber bridge behind the brow; it opens to the void at both ends |
| **The void** | between the teams, from z -14 to 13, crossed by a build zone the board's whole width |

Under the half turn each team's side island lies opposite the other team's main island, so a team landing from the
build zone comes ashore either on the enemy's fell or on the enemy's Scar.

## 3. The monuments and the ways at them

The **town monument** stands over the market square on the town's east rim, the **Scar monument** on the plateau
behind the brow. They are an east and a west across the gill, so a defence holds two places and the gill between
them; the spawn reaches the town's in 43 blocks down the street and the Scar's in 56 over the back bridge.

| Monument | Way | Length | What it asks |
|---|---|---|---|
| town | **Through** | 57 | ashore on the front coast, the north gate, the street, the square: the town fought through house by house |
| town | **Around** | 103 | ashore on the west coast, past the fields into the town's west, unseen from the square |
| town | **Over the brig** | 53 | ashore by the tarn, over the brig onto the square: the shortest way, and one bridge to hold |
| town | **From the brow** | 95, then a bridge | over the Scar to its brow, 14 over the square and 22 off it: a bridge built in the open, from above |
| town | **Below** | 97 | down into the gill, to the shelter in the brow's foot, the adit under the gill into the crypt, the ladder up into the chapel, ten blocks from the monument |
| Scar | **Front** | 75 | ashore by the tarn and up the Scar's north slope onto the plateau |
| Scar | **Chimney** | 80 | along the gill floor to the shelter and up the chimney in the rock, coming out on the plateau beside the monument |

The town monument is 153 in a straight line from red's spawn, 3.5 times blue's walk to it; the Scar monument 190,
3.4 times.

## Open

- The straight lines from a spawn to the enemy's monuments, 153 and 190, are over the band a destroy board is held
  to (85 to 150 of walk); the board is large for two monuments, and the scenery could give back some of its depth.
- The gill's two mouths open to the void. The beck rises at its back and turns east into the tarn before the front,
  so no water runs over an edge.
