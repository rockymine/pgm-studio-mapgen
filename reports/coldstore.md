# Coldstore: the author's bunker concept, finished

**Coldstore is a capture-the-wool board for two teams of sixteen, built in Python against pgmvox from a quarter the
author sent as a concept world.** The board is in `freeform/lib/boards/coldstore`, its world in `maps/ctw/coldstore`.
No studio was driven for it and nothing was written to the deployed studio. The concept world itself is not in the
repository.

## 1. What the concept world held

**The world held two concepts, and the one with a roof is the more complete.** It is one quarter of a bunker, 92 by
55 blocks, with a bedrock roof at y 42 to 48 and nothing under it. The concept without a roof, a spawn and two
monuments over wool, was read and left.

**Its 44 signs say what each piece is for, and four of them are the concept.**

| Sign | What it says |
|---|---|
| the pillars | the core of the map: the negatives of what a void hole would be in a normal map, some with shafts to rotate through |
| the platforms | the islands of a normal capture-the-wool layout |
| the wool room | Hot Dive's room behind Ender Blast's monument: blow the monument with TNT, and at 90% the room's middle segment opens |
| the walls | two blocks thick, so a player could hide and tunnel in them: make them thicker or not breakable at all |

The rest name the dressing (pipes, vents, screens, graffiti, a fire extinguisher, a great door and a blade fan in the
roof), say the terrain should grow back slowly except glass and end stone, and wish for an ice field over the roof
that tells the bunker's story.

## 2. How the board finishes it

**The quarter is measured into rectangles and built by the board's own code.** `layout.py` holds its walls, islands,
pillars, wool block and alcoves; `shell.py` builds rock, island and void, `rooms.py` the wool block and spawn,
`dress.py` everything a player only looks at. The drawn quarter is mirrored inside the team and then between the
teams.

**What the concept left open, the board decides.** The arrow on the wool block points east, so the teams split
there. The spawn is cut into the west wall at the team's middle, beside the two wool monuments. Every wall is bedrock
under one block of skin, which answers the wall sign. The drifts are snow and packed ice, the only ground that
breaks.

**The author's review added four things, and the board has them.** Each wool block's arrow shows the colour of the
enemy wool it points to. Beside each spawn its own team may not build, which is what the concept's line of redstone
there meant. The ice field is higher and runs down the bunker's sides to the world's floor, so no bedrock shows from
outside. And each fan has a shaft through the ice, so between its blades a player looks up at the sky.

## 3. What was measured

| Reading | Value |
|---|---|
| spawn to its own wool monuments, on foot | 10 and 11 |
| spawn to its own seals, bridging | 53 and 54 |
| spawn to the enemy's seals, bridging | 192 and 193 |
| every seal blown: to the enemy's wool and home | 210 and 198 |
| blue to red's south wool, seal standing: ground, bridged, sky, dug | not reached in any |
| the same, seal blown | 209 in every phase but the ground; walling the seal shuts it in all three |

**The roof is what makes the late game the early game.** The sky phase builds on every column to the build height,
and here that height is the roof's underside, 24 over the floors: no route over it is shorter than a bridge.

The studio reads the map.xml as valid: four wools, four seals, two spawns.

## 4. pgmvox

**Two capabilities were added, each with a test and a line in `freeform/lib/README.md`, and no recorded hash
moved.**

| Added | What it is |
|---|---|
| `Destroyable(required=False)` | a monument the match is not won by, for a seal whose breaking opens something |
| `play.rules.Tnt` | how TNT behaves: lit as placed, its blast breaking blocks, its yield, power and fuse |

## 5. Open

- How much TNT the seal's 90% takes is a number for a played match; the capsule is the concept's size, 588 blocks.
- Whether PGM's block-break rules hold a blast to them is taken from how PGM files explosions; it is not tested here.
- The concept's second drawing, the open one, was not built.
