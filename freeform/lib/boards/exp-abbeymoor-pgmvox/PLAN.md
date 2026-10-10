# Abbeymoor — the plan

Destroy the monument, two teams of sixteen, two monuments a team. Built on pgmvox 0.19.0 by Sonnet 5.5 for the pgmvox side of the
experiment (`analysis/freeform-vs-studio/experiment/BRIEFS.md`, brief 2). `scripts/land.py` is the ground, `plan.py` the places,
`plan_check.py` measures them, `sketch.py` draws them (`renders/00-plan-sketch.png`); the generator reads them and decides nothing they state.

## 1. The identity

**A high moor, joined by land, where each team holds the hill of a ruined abbey with an orchard village below it, and the two meet across a
peat bog of dark pools and standing stones; under each abbey a crypt, and a passage from it that comes up in the village.**
What a player remembers: the obsidian cube hung over the ruined nave on its hill, the green with the other cube, the standing stones in the wet.

## 2. The arrangement

Red holds the north, blue is red's image under the half turn, (x, z) -> (-1 - x, -1 - z). The board is 200 by 264; the spawns stand 224 apart
(z -112 and 111); the land is one island of moor, 7,000 columns of void round its ragged edge, no void between the sides.

| Place | Where (red) | What it is, and why a player goes there |
|---|---|---|
| **Hall Farm** (spawn) | (0, -112), floor 68 | The spawn in a hollow, a farmhouse and a hay barn behind it (north), the sheepfold west, the ridge rising 12 behind: the spawn stands in the land at its back |
| **Abbey Hill** | (-42, -72), plateau 80 | A hill of 38 degree slopes with the ruined nave on its top. The Hill Track (north door) and the Monks' Way (east gap) climb it |
| **Monument A** | (-40, -72), pillar y 88 to 90 | Three obsidian blocks over a stepped dais in the open nave; both approaches arrive at it; walls round it are low (2 to 5) so it shows over them |
| **The Crypt** | x -52..-43, z -76..-68, floor 70 | A vaulted hall under the nave; **the Night Stair** (11 cells, three flights of at most four) comes up in the chancel; its south door leads to the passage |
| **The passage** | z -61, x -48 to 10, floor 59 at lowest | 60 blocks under the hill and the valley, lit and timbered; it comes up by **the Tithe Barn's cellar stair** (7 up) in the village, 8 from Monument B |
| **The Village** (Thorncombe) | x 6..52, z -90..-48, floor 66 | Four cottages (headings 0, 0, 12, 90), the Moorcock inn, the Tithe Barn, a north and a south orchard, the green |
| **Monument B** | (30, -70), pillar y 70 to 72 | Three obsidian blocks on the green, in the open, the houses back six or more |
| **The Bog** | across z -31..30 | A basin 4 under the moor; seven pools held at level 61; the Standing Stones (twelve about the middle); a boardwalk two wide down the axis; the peat cuttings (trenches with stacked peat) on its north shore |
| **The Beck** | x 50..72, z -108..-30 | A stream with a reach and a fall into a pool at the bog's edge, along the village's east |
| **Roads** | | The Drove Road (spawn to the green), the Hill Track (spawn to the abbey's north door), the Monks' Way (green to the abbey's east gap), the Peat Track (inn to the boardwalk) |
| The Gatehouse | (-30, -52) | A ruined arch on the way up to the hill: a landmark and a place to hold |

Ways onto each monument, from around, above, below and through (`approaches.md`): **A** is reached over the moor and up the slopes (around), by the
Monks' Way up the east gap (above), through the crypt and the Night Stair from the village's cellar (below), and across the abbey's north door; **B** is
reached across the green (through the village, room by room), along the Peat Track from the bog (around), and from the cellar of the Tithe Barn
(below: a player who tunnels the passage backwards comes up 8 from it).

## 3. The numbers, each with its target

| Number | Target | Plan |
|---|---|---|
| Spawn to its own Abbey / Village monument | GO4: 40 to 90 | 60 / 50 |
| An enemy spawn to red's Abbey / Village monument | GO1: at least three times the own walk (3 to 4) | 202 / 190; ratios 3.37, 3.78 |
| A spawn to the enemy's monuments | GO3: 85 to 150 | 202 / 190: **misses** (the brief sets 200 to 260 between the spawns, and GO1 needs the enemy spawn three times as far as the own one) |
| Degrees off the spawn-to-spawn line | corpus median 42 | 45 / 36 |
| A way from below within 1.4 of the way overland | the crypt route is a real way | 246 against 202 (1.22) |
| The share of the ground 25 to 60 off that sees the monument | at least 25% (lesson 1) | 26% / 40% |
| What stands within five of a cube | no wall or ruin | clear |
| The passage's least cover | at least 3 | 3 |
| The longest climb in a stair or the passage | at most 4 (lesson 5) | 4 |
| Dry ground not reached on foot | at most 5% | 0.2% |

## 4. The look, decided now

Biome swampland (dark water, an olive grass, a podzol it meets). Three tone families: **ground** moor (grass, podzol, coarse dirt, mycelium for the
heather, allium and tall grass), the bog dark (coarse dirt, podzol, the pools); **built** grey stone (cobble, stone brick, andesite, mossy and cracked
in the ruin) with spruce and dark oak timber, thatch of hay and dark roofs on the cottages; **accent** the orchards' leaves and the monuments'
obsidian, the one dark thing on the moor. Rock under the rim is bedded stone, andesite, cobble with flecks.

## 5. What the build adds that the plan does not show

The standing stones, boulders on the hill's skirts, tors, drystone walls round the fold and along the Drove Road, haystacks, the farm's fields, the
well, the village's lamps, barrels, orchard rows (a tree every six), the peat stacks, the abbey's rubble, a pointed arch window every five, the crypt's pillars and
sarcophagi; bedrock at y 1 under the whole island so nothing is dug out of it; block 36 at y 0 and a not-void rule so nobody builds off the edge.
Each stands where a route does not.

## 6. The self-review, before the build, against the brief and the twelve lessons

Read against the first sketch and the first plan check. What it found, and what changed.

| # | Finding | Change |
|---|---|---|
| Brief | Two monuments a team, one at the abbey, one in the village, land across the bog: yes. Crypt under the abbey, a passage that comes up near a monument: yes. Places: eleven. Look: the swampland biome carries bog and moor together | none |
| 1 | The first check said Monument A was seen from **5%** of the ground 25 to 60 off: the hill's own plateau edge hides a cube standing on it, and the ruin's walls were drawn eight high | A stands on a **dais three high** (y 83), the walls are drawn five and built ragged at two to six, and the check now says 26% / 40% |
| 1 | The nave was 11 deep: the cube had walls four from its edge | The nave is 13 deep: five clear on each side. The Tithe Barn moves two west so it stands seven from B |
| 2 | Obsidian needs a diamond pickaxe | the kit carries one, unbreakable, Efficiency II; the cubes are obsidian |
| 3 | A wool room's chests, a wall's chests: no wool, no wall on a destroy board | n/a |
| 4 | Vegetation: orchards are the only dense planting | every orchard tree stands in its own plot, at least four from a road and six from a cube; none in the bog, on the hill or in a lane |
| 5 | The Night Stair is eleven cells in three flights; the check's longest climb was five | the check counted the step onto the landing; it now counts blocks climbed: four, at most. The passage's three descents are three stairs and a landing each |
| 6 | The spawn: farmhouse behind, the fold to the west, the Drove Road and the Hill Track out | nothing in front |
| 7 | No platform: the moor is one mass | bedrock course at y 1 under every column; the edge is a cliff with ledges and moss, not a box |
| 8 | No ladder; water only in the pools, the beck and held by banks (`audit.loose_water`) | none |
| 9 | Joins: the crypt, the stair, the passage, the cellar stair | the walk read-back must reach the crypt from the nave and from the barn, and the nave from the crypt |
| 10 | Scale: the cube 3, the plinth 7, the nave 26 by 13, the ruin walls one thick, houses 8 by 6 | none |
| 11 | Ground in patches and detail on the cliffs | heather and podzol and coarse dirt as patches by shape; the island's cliff faces bedded and mossed |
| 12 | A build zone: none on a destroy board; the land is joined | a not-void rule only |
| Check | The passage's cover read two: the formula was one short | counted from the top of the air; three |
| Check | GO3 misses | accepted: GO1 and the brief's size fix it |

## 7. Versions

`plan.py` v1; the check's first run is the review above.

## 8. Revision 1: the author's first review

Source: `analysis/freeform-vs-studio/experiment/REVIEW-1.md`, "Abbeymoor, pgmvox", and the added point 7. The v1 renders are in `renders-v1/`.
The pipeline (`python3 -m pgmvox.run boards/exp-abbeymoor-pgmvox --build <dir>`) passes: the studio reader reads the map valid, footing 0, loose water 0,
0 windows beside doors, 0 ladders, the crypt joined (spawn to nave 69, to crypt 90, to cellar foot 84), GO1 ratios 3.36 and 3.78 (GO3 still the accepted miss).

| # | Review point | What changed |
|---|---|---|
| 2 | The muddy area is too oval; add smaller patches round the map, especially through the middle | `land.bog_field`: the basin's outline is an ellipse pushed in and out by noise, joined by a fen channel that wanders east and west through the middle on a sine centreline (`dress.surface` paints from the same field, so paint and basin agree). Fifteen irregular peat patches (`dress.PEAT`, tilted ellipses with a wobbling edge) lie across the moor, the densest on the middle band, and three small tarns (-58, -30), (-84, -8), (-6, -48) held at 63. The standing stones, the pools and the boardwalk are unchanged |
| 3 | Something is missing beside the middle | Fenside, a hamlet on the flank at (-68, -17) (its half-turn image at (67, 16) is blue's): Fenside Cottage (-74, -22), Gorse Cottage (-63, -12, turned 90), the Peat Store (-75, -11), a flank orchard (-86..-72, -36..-28), a tarn, and Fen Lane joining it to the bog's north shore at (-17, -31). Not a hill: the author was unsure one fits |
| 4 | Stone houses: clay for the walls, stone for the base course | `dress.clay_style` and `dress.rebase`: every house but the timber Hay Barn has clay or brick walls in a spruce frame and a stone course at the foot. Lime-wash (farmhouse, Brook Cottage, Gorse Cottage), ochre (Thorn Cottage, the Tithe Barn), brick (Mill Cottage), terracotta (Orchard Cottage, Fenside Cottage), umber (the Moorcock, the Peat Store). Roofs stay dark oak, brick for the inn and stone-brick for the Tithe Barn, Orchard Cottage and the Peat Store |
| 5 | Paths more pronounced, in dirt; stone for where rock shows | Roads are coarse dirt, plain dirt and a little gravel (no stone), painted 2.1 blocks either side of the line instead of 1.6. Stone remains on the nave's floor, the Hill Track and Monks' Way steps and the cliffs |
| 6 | More trees and some rocks | `dress.moor_trees`: twelve copses of small oaks, birches, olives and spruces, 31 trees (v1: the orchards' five), none within seven of a road, a green or a cutting, three of water, five of a house or twelve of a monument, none on the hill. `dress.boulders`: 58 boulders and rocks (v1: 20), ten or more apart, never on a road, a green, water, within ten of a monument or four of a house. The read-back still counts 0 trunks on a road, a green, a cutting, the nave or water and 0 columns of canopy over a road |
| 7 | An obsidian monument is at most three blocks | Both monuments are a pillar of three obsidian blocks, `plan.monument_box` one cell wide: A at (-40, 88..90, -72) over the dais (81..83) with the nave's five clear round it, B at (30, 70..72, -70) on the green (blue's: (39, 88..90, 71) and (-31, 70..72, 70)). The regions in `map.xml` are 1 by 3 by 1, the completion is 100% (the studio's default: with three blocks, 50% was two of three), the diamond pickaxe stays in the kit. The sight check now aims at any face of the pillar with air in front of it: voxel sight from 43% (A) and 29% (B) of the ground cells 25 to 60 off (the plan check says 51% and 43%); A floats four above its dais top, B three over the green |

Not done: nothing in points 2 to 7 was left. The library's house window rhythm still ignores the door, which `dress.clear_windows` works round as before.
