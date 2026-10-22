# Chantry Gill: the plan

Destroy the monument, two teams, two monuments a team: one on each landmass. This file grows as the board is decided; the layout comes
first. `scripts/layout.py` is the layout as data, `scripts/sketch_layout.py` draws it (`renders/00-layout.png`),
and `assets/` holds the sheets every piece was designed and looked at on before the board was built.

## 1. The identity

**Two hill towns face each other across the void, each on a fell with a limestone scar beside it across a gill;
one monument stands in the town's square and one on the scar's plateau, and the scar's chimney and the old adit
under the gill are the ways at them that no street leads.**

## 2. The layout

Blue holds the south (z > 0); red is blue's image under the half turn, (x, z) -> (-1 - x, -1 - z). The board is
180 across and about 250 long; no piece of land is a rectangle.

| Land | What it is |
|---|---|
| **Main island**, the fell | about 110 across and 105 deep: the town in its middle, the spawn at its back, fields between the town and the west |
| **Highlands** | one band of high ground along the main island's west coast and back, 18 to 44 blocks deep, cut into pieces that fit together like a puzzle: five heights (the west tor +16, the edge +24, the south pike +28, the knott +20, the high knott +26), scenery fenced off by their faces, and four foothills nested into the notches between them and against the fell (the edge bench +10, the pike knoll +8, the knott foot +6, the spawn knoll +5), played on; the spawn stands under the spawn knoll |
| **Side island**, the Scar | about 45 across and 85 deep, east of the main island, in three storeys: its rim along the gill at the fell's height, a bench at y 50 stepped back where the gill bends away (the second monument on it), and the plateau behind the upper face to y 61, whose line slants to the gill's so face and gorge never run together; the tarn at its front |
| **The Gill** | a gorge winding between the islands, 12 to 18 across, its floor at y 34 and its rims 9 to 10 over it; the brig crosses it near the front and a timber bridge at the back; it opens to the void at both ends |
| **The void** | between the teams, from z -14 to 13, crossed by a build zone the board's whole width |

Under the half turn each team's side island lies opposite the other team's main island, so a team landing from the
build zone comes ashore either on the enemy's fell or on the enemy's Scar.

## 3. The monuments and the ways at them

The **town monument** stands over the market square in the middle of the town, the **Scar monument** on the
Scar's bench, 77 blocks apart: a west and an east across the gill, so a defence holds two places and the
gill between them. The spawn reaches the town's in 41 blocks down the street and the Scar's in 56 over the back
bridge.

| Monument | Way | Length | What it asks |
|---|---|---|---|
| town | **Through** | 45 | ashore on the front coast, the north gate, the street, the square: the town fought through house by house |
| town | **Around** | 66 | ashore on the west coast, past the fields into the town's west, under the west tor |
| town | **Over the brig** | 79 | ashore by the tarn, over the brig and across the town's east into the square |
| town | **Below** | 114 | down into the gill, to the shelter in the brow's foot, the adit under the town's east into the crypt, the ladder up into the chapel, ten blocks from the monument |
| Scar | **Front** | 75 | ashore by the tarn and up the Scar's north slope onto the plateau |
| Scar | **Chimney** | 80 | along the gill floor to the shelter and up the chimney in the rock, coming out on the plateau beside the monument |

The town monument is 153 in a straight line from red's spawn, 3.8 times blue's walk to it; the Scar monument 190,
3.4 times. The brow no longer looks at a monument; it overlooks the brig and the back bridge, and whoever holds it
holds both crossings under fire.

## Open

- The straight lines from a spawn to the enemy's monuments, 153 and 190, are over the band a destroy board is held
  to (85 to 150 of walk); the board is large for two monuments, and the scenery could give back some of its depth.
- The gill's two mouths open to the void. The beck rises at its back and turns east into the tarn before the front,
  so no water runs over an edge.
