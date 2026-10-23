# Chantry Gill: a destroy board on pgmvox's multi-floor layer document

**Chantry Gill is a two-team destroy-the-monument board, built as one pgmvox layer document, that uses the floors PR
#33 added.** It uses `levels` for the brow, `carve` for the shelter, the chimney shaft, the adit, the crypt and its
hall, and `house` and `blocks` set relative to a house's floor for the nave's hatch. The board lives in
`freeform/lib/boards/chantry-gill`, and its world is `maps/dtcm/chantry_gill`. No studio was driven for it, and the
deployed studio was not written to. The local studio was used only to write the world, render it with the game's
textures and read the map.xml back.

## 1. What the map is

**Two hill towns face each other across 28 blocks of void, each on a fell island with a limestone side island, the
Scar, across a winding gill.** Blue holds the south and red is its image under the half turn, so each team's Scar
lies opposite the other team's town. The floor of every island sits at y 0, and nothing floats.

**Each team defends two obsidian monuments, one on each of its landmasses.** The Chantry Monument floats over the
market square in the middle of the town. The Scar Monument floats over the Scar's bench at y 28, with the plateau
rising behind it to y 39.

**The town is a small settlement read street by street.** It has ten houses in two timber-framed styles, a stone
chapel with a square tower and a churchyard, and a byre with an angled field. Market stalls stand in a paved
square, and a front wall, broken toward the west, has a gate tower. Every piece was designed with the author on
scratch sheets in the game's textures before it went on the board, and the sheets are in the board's `assets/`.

**The land around the town is a band of highlands cut into interlocking pieces.** There are five scenery heights
and four foothills in front of them, played on. The ground is finished by slope, with rock on the steep faces,
scree under them and grass higher up the walls.

## 2. How it plays

**Play has five floors, and each has its own way to the next.** The gill floor is at y 12. The adit and the crypt
are at y 11 under the town's east. The town is at y 20 to 23, with the nave over the crypt. The Scar's bench is at
y 28, and the plateau is at y 39.

**Three caves run under the floors, worn through the rock and never straight.** The Hollin cave opens in the fell's
front cliff, reaches a hall under the fields and forks: east into the adit, west up to a swallow hole by the byre.
The tarn cave opens one block over the tarn at the foot of the plateau's north face and climbs through the Scar
into the open ground under the brow. The side cave opens in the Scar's east cliff and joins it.

| Monument | Way | What it asks |
|---|---|---|
| town | the street | ashore on the front coast, through the gate and up the street into the square, house by house |
| town | around | ashore on the west coast, past the fields and under the west tor |
| town | the brig | over the stone arch across the gill (76 from the east bank to the square), under the brow's fire |
| town | below | down into the gill, along the adit under the town (68) into the crypt, up the ladder through the nave's floor (17), coming up nineteen blocks from the monument |
| Scar | the front | ashore by the tarn and up the Scar's slope onto the bench |
| Scar | the tarn cave | swim the tarn to the mouth in the plateau's face, climb through the Scar (49) and come out under the brow, thirteen blocks from the monument |
| town | the Hollin cave | in at the front cliff (33 to the hall), under the town into the adit (79), then the crypt and the ladder |
| Scar | the chimney | along the gill floor to the shelter in the brow's foot, up the shaft (23) onto the bench nine blocks from the monument |

**The defender's walks are short and the attacker's are long.** The own town monument is 52 blocks from the spawn
and the own Scar monument 59, the Scar reached over the timber back bridge. The enemy's are 172 and 243, bridging
the build zone. Those two are over the band a destroy board is held to. The open point in `PLAN.md` says so, and a
second version would close the void first.

**The build zone is the whole void between the two front coasts, column by column.** Every one of the front
coast's 146 columns has the zone directly in front of it; a fixed band had left gaps of up to six blocks.

**Cover keeps its distance from every monument.** No tree, rock or building stands within four blocks of one,
checked on the built world. The bench carries a broken sheepfold east of its monument as cover for whoever holds
it.

## 3. The read-back

**Every build is read back in text before any picture.** `renders/gen.txt` lists each layer's step, the gill's and
the bench's heights, and the objectives' check (no problem). `renders/walks.txt` has no column standing on air, no
water against air, and every walk and way above. The studio's `read_mapxml.cs` reads the map.xml as valid, with
four destroyables, two spawns and two teams.

**`check.py` passes all 225 unit tests, and every existing board and example builds to its recorded hash.** The
volcanoes study is the one exception, and it failed before this work.

The pictures, all under `freeform/lib/boards/chantry-gill/renders/`:

| Floor | Section | Textured |
|---|---|---|
| the gill floor and the brig | `40-cut-brig.png` | `53-gill.png` |
| the shelter, the chimney, the bench | `41-cut-shelter.png` | `54-scar.png` |
| the adit, the crypt, the ladder into the nave | `42-cut-adit.png` | `52-town.png` |
| the spawn hall and the timber bridge | `43-cut-bridge.png` | `55-spawn.png` |
| the tarn, the brow, the bench, the plateau | `44-cut-scar.png` | `51-blue.png`, `57-tarn-wall.png`, `58-scar-tower.png` |
| the Hollin cave and the swallow hole | `45-cut-hollin.png`, `46-cut-swallow.png` | `56-front-cliff.png` |
| the tarn cave and the side cave | `47-cut-tarn-cave.png` | `59-side-cliff.png` |
| the whole board | `30-iso-se.png`, `31-iso-nw.png`, `33-xray-blue.png` | `50-board.png` |

## 4. Every pgmvox gap

**Each gap this board needed is closed in the library as an opt-in key, with a test and a line in
`analysis/freeform-vs-studio/LAYER-DOCUMENT.md`.** None of them moved a recorded hash.

| Gap | What was added |
|---|---|
| a house could not state its details | style keys for plinth, sills (in the wall or hung), hood, beam ends, chimney stack and top, a window rhythm with a phase, logs, quoins, string course, joists, a slab roof, verges and roof bands, and plain turned houses; even ridges on turned houses now meet |
| a house stood on the highest ground in a square round it | `floor`: `"footprint"` reads only the ground under the walls, and a number sets the plate |
| no door path | a house's `walk`: a one-wide path from its door to a named line, hedged |
| no blocks relative to a house | `blocks` with `rel`, counted from that house's floor |
| no market stall | the `stall` op: fence posts, a striped wool roof, banners front and sides, a counter, goods |
| no tower | the `round_tower` op: round or square, quoins, string course, plinth, crenels as slabs or stairs, openings, slits |
| a wall was one block | `wall` takes `courses` (a gradient from the foot up), `crenel_stair`, `step_stair` and `step_slab`, and `ruin` |
| no garden scenery | `hedge`, `small_trees` (a vanilla-shaped oak), `crops` (angled rows with ditches and a scarecrow), `flowers` (filled rows in a polygon), `boulders` |
| no churchyard or square | `graves` and `paving` |
| a level's ground was one block | a level takes `soil`, its outline a `where`, and its underside a `bottom`, which is how the brow leans |
| laid ground was one block deep | `lay` takes `soil` and `ledges` |
| no gully relief | the `gullies` expression |
| no snow | a `snow` stage: smooth snow after Arceon's `//smoothsnow`, with a mask, an added height and a jitter on it |
| a board could not state a biome | `board.biome` |
| a board could not hand the document a grid it computed | `build(doc, arrays=...)`, read by name in any expression |
| a shaft had no lining | a shaft's `wall` and `post` |
| no ground cover | the `plants` dress op: grass, ferns, their tall kinds and leaf bushes in patches, kept low round a point |
| `pgmvox.run` doubled a board's path in `maps/INDEX.md` when run from `freeform/lib` | `register` is handed the absolute board path |

**Five gaps are open.** Each is named here and left for a later run.

- The studio's renderer draws no banners, so the stalls' banners show only in game.
- `write_world.cs` refuses a fractional spawn in `level.json`. `World.save` takes floats, so the spawn has to be
  whole numbers.
- Nothing in the library checks the four-block cover rule round a monument. It was read off the built world by hand.
- `levels` (the stage) and `level` (the op) collide by name. The stage was used as it is, and `tiers` is the
  likely rename.
- The textured renders need the 1.8.9 client jar, and Mojang's hosts are blocked from this container. A jar holding
  only the block and chest textures was assembled from a public mirror of the 1.8.9 assets, at
  `~/.cache/minecraft/1.8.9-textures.jar`.
