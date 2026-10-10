# Sandreach — the report

**Sandreach is a capture-the-wool board for two teams of twelve that is made and grown at once.** Its spine is
Brittlebush's grammar on a grid of five-block cells. Beside it lies grown ground, painted by its slope: a meadow
hillside east of each spawn and a floating island off each wool's approach. Red holds the north, and blue's half
is red's turned a half about the middle.

## What is in the folder

- `scripts/plan.py`: the made blueprint in cells and sections, the grown ground's shapes and heights, the
  objectives.
- `scripts/gen.py`: the world: the made through `pgmvox.brittle`, the grown by hand on `pgmvox.terrain`.
- `scripts/mapxml.py`, `scripts/walk.py`, `scripts/renders.py`: the map.xml, the read-back, the pictures.
- `world/`: the Minecraft world, ready for PGM.

The whole board is rebuilt with `python3 -m pgmvox.run boards/sandreach --build <dir>` from `freeform/lib`.

## The arrangement

| Place | Level | What it is |
|---|---|---|
| The plaza | 12 | the middle, six cells by six, three sections a side in grass and sand; neutral, a cell of build zone from both lanes |
| The lane | 15 | two sections from the plaza's edge to the yard's stair |
| The yard and the spawn's house | 18 | sections round a keep; the house two by two, the two back cells, one cell with a beacon |
| The meadow | 11 to 25 | grown: east of the yard, rising north-east, falling away south into hanging rock |
| The spine | 18 | west from the yard to the stair up to the wool's terrace |
| The wool's terrace and house | 21 | the house on its whole piece, the bar before it with the redstone line |
| The landing | 18 | under the terrace toward the middle, up a stair to it: the attackers' way in |
| The island | 12 to 17 | grown, floating between the plaza and the landing |

**The plaza is reached by building from both sides, and the far side by building again.** No made way joins the
two halves, so a team walks its own half and builds across the middle, as Brittlebush's boards do.

## Where the made meets the grown

**The made ground is cut out of the grown, and they meet at a made face.** The meadow is kept out of every made
cell. `brittle.build(grown=...)` reads the meadow's tops, so the yard's and the lane's faces are as deep as the drop
to the meadow under them, and nowhere a slope is graded across the seam.

**The meadow lies three or more under the made faces, so they read as walls and keep their plain courses.** A birch
panel needs five of air; over three, the face shows the rim, brick and dark oak and no cut-off panel.

**The height between them is a stair set into a notch of the yard.** One stair cell climbs from a level foot on the
meadow at the lane's level up into the yard. The meadow runs out from the foot over six blocks to its own slope.

## The grown ground

**The grown ground is painted by its slope.** Grass on the gentle ground; coarse dirt where it steepens or at the
brink; sandstone where it is a face. Under the grass lie two courses of dirt, fewer as the slope steepens, then
sandstone in beds with smooth sandstone every seventh course.

**Every column hangs an underside under it, deepest inland, with flutes and spires.** Its depth is measured from
the void and not from the made ground, so where the meadow meets the yard it is deep and flush against the face.

**Acacias stand to the outside of each grown piece, a handful and no more.** Five on the meadow, on gentle grass
five to ten in from the void and nine or more from any made face, none on the southern brink. Two on the island,
on its side away from the landing and the middle, so no bridger lands in a crown. The board's two species are the
acacia on the grown ground and the birch in the made beds.

## Read back from the world

**Every check comes out clean and both teams' numbers are the same.** These are from `renders/walks.txt`.

| Read | Value |
|---|---|
| Objectives with a problem | 0 |
| Blocks without footing | 0 |
| Water standing against air | 0 |
| Land without block 36, block 36 under neither land nor a zone | 0, 0 |
| Places reached on foot from a spawn | 5141 |
| Spawn to its own wool's door, on foot | 54 |
| Spawn to its monument, on foot | 16 |
| Spawn down the stair onto its meadow, on foot | 26 |
| Spawn to the other wool, on foot | not reached |
| Spawn to the other wool, building | 144 |

## What was not done

- The board was not opened in PGM. The map.xml is written by the library and the objectives check against the
  world, but no match was played.
- The grown ground is laid by the board's own script. The grammar names the made ground's rules; the grown
  ground's are written out here, and they are the next thing to give it.

## The renders

- `05`: the built world from above, with the objectives.
- `30`: the whole board from each of its four corners.
- `32`: red's half.
- `33`: where the yard meets the meadow, the stair in its notch.
- `34`: the island and the landing.
- `35`: the wool's house.

## After the playtest

**Sandreach is now capture the wool and destroy the monument at once, with both modes in its map.xml.** Each
team keeps an emerald monument on its meadow: a cube of emerald three a side with bedrock at its heart, on a plinth
of smooth sandstone. The meadow is levelled to 21 round it and eased back to the hillside over five blocks.

**A team walks to its own emerald in 46 and builds to the other's in 133, the same for both.** Players crossing
the meadow pass it anyway; it gives the ground they run over something to fight for. The other wool is still 143
by building, against 144 before, and the board is still the same for both teams.

**The meadow carries more than grass.** Nine boulders of sandstone, stone and cobble sit into it a dozen blocks
apart, off the made faces, the stair's foot and the emerald's ground; dead bushes grow on the coarse dirt and a few
in the grass. The acacias keep ten blocks from the emerald.

**The wool house carries the studio's wool-room loot.** Two chests stand in each inner corner of its first storey,
as the studio's wool-room stamper lays them.
