# Chantry Gill: the plan

Destroy the monument, two teams, one monument a team. This file grows as the board is decided; the layout comes
first. `scripts/layout.py` is the layout as data, `scripts/sketch_layout.py` draws it (`renders/00-layout.png`),
and `assets/` holds the sheets every piece was designed and looked at on before the board was built.

## 1. The identity

**Two hill towns face each other across the void, each on a fell with a limestone scar beside it across a gill;
the monument stands on the town's rim over the gill, and the scar's leaning brow and the old adit under the gill
are the two ways at it that no street leads.**

## 2. The layout

Blue holds the south (z > 0); red is blue's image under the half turn, (x, z) -> (-1 - x, -1 - z). The board is
180 across and about 250 long; no piece of land is a rectangle.

| Land | What it is |
|---|---|
| **Main island**, the fell | about 110 across and 105 deep: the town on its east rim, the spawn at its back under the knott, the edge down its west side, fields between the edge and the town |
| **Side island**, the Scar | about 45 across and 85 deep, east of the main island: the tarn at its front, the plateau behind its leaning brow |
| **The Gill** | the gap between the two islands is a gorge, not void: 8 to 12 across, its floor about 9 under the town's rim; the brig crosses it near the front; it opens to the void at both ends |
| **The void** | between the teams, from z -14 to 13, crossed by a build zone the board's whole width |

Under the half turn each team's side island lies opposite the other team's main island, so a team landing from the
build zone comes ashore either on the enemy's fell or on the enemy's Scar.

## 3. The ways at blue's monument

| Way | From the build zone | Length | What it asks |
|---|---|---|---|
| **Through** | the front coast, the north gate, the street, the square | 59 | the town fought through house by house |
| **Around** | the west coast, past the fields, into the town's west | 105 | the long way, under the edge, unseen from the square |
| **Over the brig** | ashore by the tarn, across the brig, up onto the square's north | 56 | the shortest way, and one bridge to hold |
| **Above** | ashore on the Scar, up its north slope to the plateau and out to the brow | 101, then a bridge | the brow stands 14 over the square and 22 off it: a bridge built in the open, from above |
| **Below** | down into the gill, along its floor to the shelter in the brow's foot, the adit under the gill into the crypt, the ladder up into the chapel | 98 | arriving unseen, under the defence, up one ladder ten blocks from the monument |

The defenders walk 48 from the spawn to the monument; blue's monument is 152 in a straight line from red's spawn,
3.1 times that walk.

## Open

- The straight line from a spawn to the enemy monument, 152, is at the top of the band a destroy board is held to
  (85 to 150 of walk); the monument may move a few blocks north once the town is laid.
- The gill's two mouths open to the void. The beck rises at its back and turns east into the tarn before the front,
  so no water runs over an edge.
