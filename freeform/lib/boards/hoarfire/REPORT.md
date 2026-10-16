# Hoarfire — report

**Hoarfire** is a Destroy the Core and Destroy the Monument board for two teams of twenty, built with pgmvox from
`scripts/`. Its world is `maps/dtcm/hoarfire`; its plan is `PLAN.md`.

```
cd freeform/lib
PGM_STUDIO_ROOT=/home/user/pgm-studio MINECRAFT_JAR=/home/user/mc/client-1.8.9.jar \
  python3 -m pgmvox.run boards/hoarfire --build <build-dir>
```

`PGM_STUDIO_ROOT` is needed by the generator itself (the oaks come from the studio's tree library), not only by
the renders.

## The concept, and how it reads the theme

**Fire and Ice is read as a moment, not as two teams: the first night of winter falling on an autumn valley.**
Each team's half is the same valley caught half-way. The Rimewall glacier has already buried the west under snow,
and the east still burns with autumn: russet oaks, red and orange maples, pumpkins in the harvest field, charcoal
kilns smouldering. The seam between the two is a stream, the Thaw, that rises from the spring in front of each
team's lodge and runs down the middle of its half; west of it lies snow, east of it grass with frost thinning out.

**The two objectives are the two halves of the theme.** A team defends an **Ember Core** (obsidian round lava,
fire held in stone) floating over a charcoal pit in the autumn wood, and a **Rime Monument**, a 21-block crystal
of packed ice floating over a disc of old ice in a ring of standing stones on the snow. To win, a team leaks the
enemy's fire and shatters the enemy's ice.

**Fire and ice meet everywhere the board can make them meet.** The lodge court holds a half-frozen spring beside a
hearth of lava under iron bars. The Rift's autumn cliff pours three lava falls into the void while its winter
cliff hangs five frozen falls of packed ice, with the Thaw's waterfall between them. Kiln Hill carries a beacon of
lava on a crown of first snow. The islets in the Rift are an iceberg (the Berg) and a smouldering cinder cone
(the Cinder) with a lava spill. Under the snow half hang icicles.

**What is new here.** The palette gradient runs along the team axis rather than across it, so the board is
mirrored (`mirror_z`) instead of turned, and both teams own a winter flank and an autumn flank of the same shape.
The board has two fronts that look nothing alike: the fire front (cores facing each other across the east Rift)
and the ice front (monuments facing each other across the west).

## The modes and how each objective is approached

`<gamemode>dtc</gamemode><gamemode>dtm</gamemode>`: two cores and two destroyables. The core is the forward
objective, the monument the deeper one, and both sit a walk of 49 from the spawn (`PLAN.md` §3).

**Each goal has four approaches: around, above, below and through,** the author's law from `approaches.md`.

| goal | above | below | through | around |
|---|---|---|---|---|
| Rime Monument, x -37..-35, y 55..59, z -52..-50 | the glacier's snout at 62, 11 over the shelf and 16 from the crystal, climbed by the snow drift on its west flank | the Ice Cave: a packed-ice ledge in the Rift's cliff at (-50, 41, -12), up under the snow to the Rime Tarn's bank at (-59, 47, -32) | the Frostwood's spruce, to within 11 | the frozen Rime Tarn, sunk two under the shelf |
| Ember Core, x 36..39, y 54..57, z -52..-49 | Kiln Hill's flank, at the core's height 15 from it and 6 over it 17 from it | the Hollow Way, a lane three under the ground from the Rift's shore at (22, -9) into the Ember Pit under the core | the Russet Wood | the kiln yard and the harvest field, open ground on the defenders' side |

**The defenders' lateral lane is the Cross Road**, from the Rime Shelf over the Thaw Bridge to the Ember Pit, so a
team can shift from one goal to the other in about 70 blocks without going back to the lodge.

**The Rift is crossed only by building.** It is a build zone from edge to edge (`Build(areas=[(-72, -16, 71, 15)])`);
the narrowest crossing is 16, between the two headlands where the Thaw falls, and each islet offers a crossing of
two bridges of 9. No running jump crosses anywhere.

## The layout and its proportions

| | |
|---|---|
| footprint | 144 by 196 (x -72..71, z -98..97), of which 24 rows are the Rift's void |
| land | 22,696 columns, both halves and the islets: about 80% of the footprint |
| players | 20 a team |
| spawn to own goals | 49 and 49 (plan walk); 42 and 50 moves (voxel walk) |
| enemy spawn to a goal | 147 to 149 (plan walk, 27 to 31 of it bridged); 135 to 138 moves (voxel walk, building) |
| enemy walk / own walk | 3.03 (monument), 3.02 (core) |
| goal to nearest enemy goal | 92 |
| kill height | y 30; the land's floors run 44 to 66, the cave's cliff ledge 41 |
| build height | 92 |

**The spawn is seated in the land, not hung off it.** The Hearth Lodge stands on the Hearth Ridge with ground
rising behind it to the board's back edge, the glacier on its west shoulder and the hamlet on its east. Its court
is made ground: a paved terrace with a stone-brick retaining wall and a flight down to each of the three paths.

## The palette

| family | blocks | where |
|---|---|---|
| ground: snow | snow; packed ice where it is old ice (the shelf's disc, the glacier in bands of snow); stone and andesite on slopes over 34° | west of the Thaw, the glacier, the Berg |
| ground: autumn | grass under the Mesa tint (russet); podzol and coarse dirt under the crowns; stone showing on slopes over 32° | east of the Thaw |
| ground: rock | stone and andesite in beds, granite and coal thin, cobble flecks; folded and draped over the ground | every face, the Rift's cliffs, the undersides |
| built | spruce planks and spruce logs (posts, laid beams, beam ends), cobble and andesite ground storeys, brick, dark oak roofs; stone brick for the made ground | the lodge, the barn, the farmhouse, the Ice Hut, the court, the bridge |
| accent: fire | lava (falls, hearth, beacon, the Cinder's eye), jack-o-lanterns, netherrack and coal round the vents, red and orange wool clumped in the maple crowns, fallen leaves in carpet | the autumn half, the Rift's east cliff |
| accent: ice | packed ice (the crystal, the frozen falls, the icicles, the standing stones' rime), ice on the tarn and half the spring | the snow half, the Rift's west cliff |

**Biomes are part of the palette.** Cold Taiga (30) under the snow, Mesa (37) under the autumn, Savanna (35) under
half the oaks, so their crowns go gold beside the russet ones. Two species of tree only: spruce (built here, with
snow on every tier) in the cold, oak in the warm.

Paths are the ground's own set laid a third each: gravel, andesite and cobble on the snow; coarse dirt, podzol and
spruce planks on the autumn ground.

## What was checked

**The plan, before a block was written** (`renders/plan-check.txt`, and on `renders/00-plan-sketch.png`): every
row of `PLAN.md` §3 is in range, and both teams' numbers are equal.

**The built world** (`renders/walks.txt`): the voxel walk with doors opened, a step of one, a running jump of three
and no blocks placed, then the same walk building over the Rift. Sloe's column walks to the image (z -> -1 - z).

| read | Rowan | Sloe | at (Rowan's) |
|---|---|---|---|
| objectives with a problem | 0 | | the crystal, the core, both spawns |
| footing problems, loose water | 0, 0 | | the whole world |
| spawn to the Rime Shelf under the crystal | 42 | 42 | (-36, 52, -51) |
| spawn to the Ember Pit's floor | 50 | 50 | (38, 45, -50) |
| spawn to the glacier's snout | 73 | 73 | column (-47, -64) |
| spawn to Kiln Hill's crown | 70 | 70 | column (58, -57) |
| spawn to the Ice Cave's cliff ledge | 86 | 86 | (-50, 42, -11) |
| spawn to the Ice Hut, inside | 84 | 84 | (-62, 52, -40) |
| spawn to the enemy's shelf, building | 138 | 138 | Sloe's (-36, 52, 50) |
| spawn to the enemy's Ember Pit, building | 135 | 135 | Sloe's (38, 45, 49) |
| the enemy's half without building | not reached | not reached | |
| blocks within four of a goal, over the ground | 0 | 0 | |
| logs over a path, the bridge's rails aside | 0 | | |

**The map.xml** is valid to the studio's parser (`data/read_mapxml.cs`): two cores, two destroyables, two spawns,
two teams, no issues.

**The renders.** The library's flat colours (`30-iso-the-board.png`, `31-cutaway-z-50.png`, the annotated
top-down `05-topdown-annotated.png`) and the studio's textured renderer:

| render | what it shows |
|---|---|
| `t01-overview.png` | the whole board |
| `t02-rowan-from-the-rift.png`, `t09-sloe-half.png` | each half, the seam down its middle |
| `t03-rime-monument.png` | the crystal over the shelf, the standing stones, the glacier's snout |
| `t04-ember-core.png` | the core over the Ember Pit, the kilns, Kiln Hill and its beacon |
| `t05-hearth-lodge.png`, `t12-lodge-hall-inside.png` | the spawn, outside and inside (the hearth, the tables) |
| `t06-the-rift.png`, `t10-fire-falls-and-cinder.png`, `t11-across-the-rift.png` | the Rift, its falls and islets |
| `t07-the-seam.png` | the Thaw: snow on one bank, autumn on the other, the bridge |
| `t08-ice-cave-cut.png` | the Ice Cave in section |
| `t13-hollow-way-into-the-pit.png` | the Russet Wood over the Hollow Way |

## What did not work

- **The first monument was invisible.** A 3x3x3 cube of packed ice in front of a packed-ice glacier vanished into
  it in every textured view. It became a crystal (a diamond of 21 blocks), and the ice seracs round it became
  standing stones of andesite, so the only free-floating ice on the shelf is the objective.
- **Autumn has no leaves in 1.8.** Oak leaves take the biome's tint, so the reds come from wool clumped inside the
  crowns (only into leaves with four leaf neighbours, or they stuck out as cubes) and from Savanna patches turning
  half the crowns gold. Speckled wool read as noise; clumps two blocks across read as maple.
- **Fire is not drawn.** The textured renderer draws no fire block, so every flame is lava under iron bars,
  lava in a fall, or a jack-o-lantern. `doFireTick` is off in the map anyway, and the random tick with it, so the
  snow and ice beside the lights keep.
- **Savanna under the whole autumn was tried and dropped.** Its yellow grass read as late summer; Mesa's brown
  reads as autumn.
- **The underside first came out as a slab with walls.** `island_bottom` measures from void inside the array, and
  the land runs to the world's edge; padding the arrays with void gave the taper.
- **The first lodge hung a stone column into the void** where its back wall stood past the land, through the
  house's plate fill; the footprint moved two rows south and the fill is held to four under the floor.
- **The lava falls are straight.** A fall of flowing lava down a sheer face is a column one or two blocks wide; it
  reads as fire from across the board and as a rod close up.
- **The autumn meadow came out the flattest ground on the board.** Between the Thaw and the Russet Wood the grass
  rolled by two or three blocks and nothing else; a bank of three and a half along the Thaw's east side, rock
  showing on its face, was added after the first full build, and the meadow behind it is still gentle.

**What the plan missed, decided while building:**

- The court's edges: the plan levelled the court and said nothing of how a player leaves it, and the built court
  stood five over the ground in front. A retaining wall and three flights were added. The plan should state made
  ground's edges and their stairs.
- The Ice Cave's mouth first opened into the tarn's water; the plan's cave points did not know where the water
  was. Its mouth moved four blocks west.
- The bridge was two wide inside its rails, narrower than the path it carries; the plan's bridge rectangle is now
  four wide.
- A log bench in the court stood on the Rime Path's first cells; the walk's path-clearance read caught it.

## What a library or studio feature would need to do

| what I wanted | how hard it was | what the library or studio would need |
|---|---|---|
| a destroyable with a shape, not a box (the crystal) | a subclass in `plan.py` overriding `stamp` and `check` | `Destroyable(shape=...)`: a list of cells, or a mask in the box, written and checked as the objective |
| autumn colour in 1.8 crowns | a clump pass over each crown, written by hand | `trees.recolour(crown, palette, clump, share)`, clumping into interior leaves |
| a snowy spruce with snow on its tiers | written by hand (`spruce` in `dress.py`) | a tree builder with a snow pass for any library tree: a snow layer on every leaf with sky over it |
| a fall of lava that reads as a fall | lava columns, varied in width and length | a `lavafall` in `surface.terrain` beside `waterfall`, with a vent and a scorched face |
| an island underside that tapers at the world's edge | padding by hand | `island_bottom` padding its own arrays with void |
| a retaining wall and flights for any made ground | written by hand (`flight` in `dress.py`) | `built.build.terrace(cells, y, flights=[...])`: the wall on every open side, a flight where a path leaves |
| a fire block in the textured renders | not possible | the renderer drawing fire, so a brazier can be fire and not lava |
| checking that a goal stands out against what is behind it | found only by looking | a read that measures each goal's contrast against its backdrop from its approaches |
