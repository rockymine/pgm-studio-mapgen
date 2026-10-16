# Rimeburn: the plan

Destroy the Core and the Monument (`dtcm`). There are two teams of up to 24, Ember (gold, south) and Frost (aqua, north), with a half turn between them. `scripts/land.py` is the ground and `scripts/plan.py` holds the places, buildings, routes and objectives. `plan_check.py` measures them, `sketch.py` draws them (`renders/00-plan-sketch.png`), and the generator reads them without deciding anything they state.

## 1. The identity

**One land in two seasons: Frost holds the north in deep winter and Ember the south in the last of autumn, and each team guards one fire and one ice.**
A team's **Hearth** is a core, lava in obsidian, floating over a fire ring in a thawed hollow. Its **Icestone** is a monument of packed ice on a mesa, ringed by ice spires. Frost keeps a fire alive in the snow, and Ember keeps the last ice of the year among red trees. The two lands meet only across the void. In the middle of that gap is the Thaw, an island where the snow line wanders across the grass.

What a player remembers is the two seasons facing each other over the void, the black cube in its ring of braziers, the blue spires on the mesa, and the burn running from the Rime Falls down to the Tarn.

## 2. The arrangement

Frost's half is drawn here, and Ember's is its image under (x, z) -> (-1 - x, -1 - z). The board is 128 by 192 with 18,416 columns of land, and the spawns stand 156 apart.

| Place | Where (Frost) | What it is, and why a player goes there |
|---|---|---|
| **The Hold** (spawn) | yard at (3, -78), floor 46 | A two-storey longhouse cut into the foot of the Rimewall, with a paved yard and two braziers. The ridge rises 15 to 25 behind it, so the spawn sits in the land at its back. |
| **The Rimewall** | z -96..-84 | The ridge behind, crest 60 to 70, falling away behind its crest. It frames the board. Spruces (Frost) and maples (Ember) grow at its foot. |
| **The Rime Falls** | (-21, -88) | The burn's source: a notch down the Rimewall's face, frozen on Frost's side and still water on Ember's. |
| **The burn** | (-21, -87) to the Tarn | A stream three wide, ice on Frost's side and water on Ember's, with riffle stones at each fall. It is bridged twice, on the Hold to Hearth path and on the Hold to front path. |
| **Hearth Hollow** (core) | core (-35, -58), y 40 to 44 | A bowl 6 deep (floor 34) in levelled ground at 40. Its floor has thawed to podzol and coarse dirt, and the hearthstone of nether brick and stone has four fires. Seven braziers stand round the rim. |
| **The Anvil** | (-48, -40), top 52 | A rock stack west of the hollow, with a ledge path winding up its east and north faces. Its top is a stage to bridge from toward the core. |
| **The Vent** | mouth (-24, 32, -22), into the hollow at (-35, -52) | A lit passage cut from the coast's cliff under a low barrow. It comes up in the hollow's south wall and is reached only by building across the seam. |
| **The Rime Shelf** (monument) | Icestone (38, -56), y 50 to 52 | A mesa with its top at 45, a stone-brick and quartz dais at 46, and four packed-ice spires 8 to 11 high at its corners. Flights of stairs rise on the west (from the Hold) and the south-west (from the Tarn). |
| **The Tarn** | (21, -41), level 37 | A frozen lake (water on Ember's side) with a spruce jetty and an ice-fishing hole. |
| **Rimecroft** | (47, -31), floor 38 | A hamlet of a long house, a byre and a smithy, all in the Hold's style. The smithy has a forge fire, an anvil and a trough. There is a woodpile and hay, and pumpkins at Embercroft. |
| **The March** | z -32..-42, x -57..5 | A broken drystone dyke two courses high, with five gaps where paths and the barrow cross. It is cover on the front. |
| **The knolls** | front band | Seven low rock knolls, 3 to 5 high, that a player fights round. |
| **The Thaw** | island on the centre, floor 38 | A deck on four stone legs at 44, with ladders from each side and the meeting fire in a ring of nether brick. The snow line wanders across the island. |

**Ways onto each goal.** The approaches come from around, above, below and through (`approaches.md`).
- **The Hearth.**
  - Around: over the open front, past the March.
  - Above: the Anvil's top, 8 above the core's top and about 15 away, to bridge from.
  - Below: the Vent, from the cliff into the hollow's south wall.
  - Through: the Rimewood spruces on the west flank.
- **The Icestone.**
  - Around: the east coast.
  - Through: Rimecroft's houses.
  - Across: the Tarn's ice, open and exposed.
  - Up a flight: the two stair cuts. The cliff elsewhere is three to six blocks.

## 3. The numbers, each with its target

| Number | Target | Plan |
|---|---|---|
| Own spawn to the Hearth / Icestone (to within 2 of the footprint) | GO4: 40 to 90 | 41 / 40 |
| Enemy spawn to the Hearth / Icestone, seam bridged | GO3: 85 to 150 | 141 / 147 |
| Enemy over own | GO1: 3 to 4 | 3.48 / 3.64 |
| Degrees off the line between the spawns | corpus median 42 | 59 / 60 |
| Narrowest bridge straight across the seam | at least 16 | 23 |
| Narrowest bridge from a land to the Thaw | 8 to 16 | 11 |
| Ground under y 56 that no spawn reaches | at most 2% | 1.7% (the shelf's cliff faces and the Anvil's steep sides) |
| Columns of land | under 20,000 (a void board) | 18,416 |
| Core float | at least 3 air | 5 (floor 34, core 40 to 44); leak 5 reaches the floor |
| Icestone float | at least 3 air | 3 (dais 46, ice 50 to 52) |

## 4. The look, decided now

- **Biomes:** Ice Plains under Frost and Mesa under Ember. Mesa tints grass to an olive brown and oak leaves to a brown, which meets podzol as one leaf-littered floor.
- **Frost:**
  - Ground: snow, with packed ice inset in patches.
  - Slopes: bare stone and andesite scree past 32°, and rock beds past 40°.
  - Built: stone-brick feet, spruce walls on spruce posts, and dark-oak roofs under snow.
  - Accent: the fires, which are netherrack, nether brick and fire.
- **Ember:** the same ground and buildings, re-seasoned block by block (`season.py`).
  - Ground: snow becomes grass, packed-ice patches become podzol, and scree gravel becomes coarse dirt.
  - Paths: dirt, coarse dirt and spruce planks.
  - Built: acacia walls, dark-oak posts and nether-brick roofs.
  - Ridge: snow stays above y 58, the first snow on Ember's peaks.
  - Accent: oaks in brown leaves with clumps of orange wool, and maples in red and orange. Fallen leaves lie as carpets and podzol under them, with tulips and poppies in drifts.
- **Shared:** both halves keep the packed-ice spires and the Icestone, and the rock is the same stone and andesite with cobble flecks.

## 5. What the build adds that the plan does not show

- Trees, two species per board: spruces on Frost's side and oaks on Ember's. They stand at 20 sites per side, at least 10 from either goal's footprint and 5 in from the coast, and none on a path.
- Seven boulders where rock falls: under the Rimewall, round the Anvil and on the Tarn's shore.
- Snow on built tops, but not on yards or in the warm hollow.
- Flowers and ferns kept low.
- `doFireTick` off, so the braziers burn and never spread.
- Block 36 at y 0 under every column, and a build zone over the whole seam (z -26..25) and nowhere else over void. The kill height is y 20.
