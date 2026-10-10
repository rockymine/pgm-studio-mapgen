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
| **Monument A** | (-40, -72), cube y 86 to 88 | Over a stepped dais in the open nave; both approaches arrive at it; walls round it are low (2 to 5) so it shows over them |
| **The Crypt** | x -52..-43, z -76..-68, floor 70 | A vaulted hall under the nave; **the Night Stair** (11 cells, three flights of at most four) comes up in the chancel; its south door leads to the passage |
| **The passage** | z -61, x -48 to 10, floor 59 at lowest | 60 blocks under the hill and the valley, lit and timbered; it comes up by **the Tithe Barn's cellar stair** (7 up) in the village, 8 from Monument B |
| **The Village** (Thorncombe) | x 6..52, z -90..-48, floor 66 | Four cottages (headings 0, 0, 12, 90), the Moorcock inn, the Tithe Barn, a north and a south orchard, the green |
| **Monument B** | (30, -70), cube y 69 to 71 | On the green, in the open, the houses back six or more |
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
