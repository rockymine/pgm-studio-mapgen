# Hollowstack: a vertical destroy board laid from a segment kit

**Hollowstack is a destroy-the-monument board for two teams of sixteen, built in Python against pgmvox, read like a
side-scrolling game's cross-section.** Two walls of rock riddled with holes face each other across a void chasm,
and each wall is a stack of storeys a team lives in. The board is in `freeform/lib/boards/hollowstack`, its world in
`maps/dtcm/hollowstack`. No studio was driven for it, and nothing was written to the deployed studio; the local
studio wrote the world, rendered it and read its map.xml back.

## 1. What the map is

**Each wall is 84 blocks deep, 52 across and about 100 high, and the chasm between them is 24 blocks of void.**
Blue holds the east and red is its image under the half turn. From top to bottom a wall holds five storeys.

| Storey | Heights | What it is |
|---|---|---|
| The Tops | y 92 to 103 | an oak and birch wood with clearings, the keep at the back with four towers round its yard, a broken watch tower at the brink |
| The Workings | y 82 | a mine laid from the timber kit: galleries with rails, a pithead, two galleries out to the chasm on timber stages |
| The Underwood | y 51 to 63 | a forest in a domed cavern on three terraces, a pond, glowstone stars in the roof, vines down the walls; the Grove Shrine on a spur in its mouth |
| The Undercroft | y 34 and 40 | a dungeon laid from the stone kit: corridors, two stairs, three ladder wells, a library, a prison, a crypt, a hall, the gallery on the chasm and the Vault at the back |
| The Deep | y 13 to 21 | a lava hall with its lake held in obsidian, a pool under the Root Well, a grotto of huge mushrooms |

**The chasm's face is the board's picture.** Every storey opens onto it: the Workings by timber stages on struts,
the Underwood by its whole mouth with the shrine standing in it, the Undercroft by a two-storey arcade and two
balconies, the Deep by a cave mouth. 110 hollows are worn into the face and the walls' sides, never into a laid
passage. Looking across from any mouth a player sees the other team's storeys stacked opposite.

## 2. How it plays

**Each team defends two monuments, and the board was built for wools first.** The author's review turned it: a
wool must always be defensible, and the Shrine's, on the chasm's very edge, was not. The Shrine monument floats over
the altar on the spur in the Underwood's mouth, the front one fought over across the chasm; the Vault monument floats
in the Undercroft's back room by the keep well, reached through the enemy's dungeon.

**Only what a player builds may be broken, with the monuments, and no crafting table can be made.** The rock holds,
so every route to a monument stays a route through its doors; `analysis/late-game/README.md` measures the difference
on the Vault.

| Walk | Blocks |
|---|---|
| spawn to a team's own Shrine monument, on foot / taking the drops into water | 128 / 79 |
| spawn to a team's own Vault monument, on foot / taking the drops into water | 127 / 75 |
| spawn to the enemy's Shrine monument, bridging the chasm | 158 |
| spawn to the enemy's Vault monument, bridging the chasm | 231 |

**The ways between storeys are few and named, so the defence knows where to wait.** The keep well is one ladder from
the yard through the Workings to the Undercroft, with a postern into the Underwood's back. A winding cave runs from
the Workings down into the Underwood, the gatehouse's ladder from the Underwood down into the Undercroft, and a
third well down into the Deep. The fast ways down are falls into water: the light well from the Tops into the pond,
the plunge from the keep's hillside into a pool, and the Root Well from the shrine's spur into the Deep.

**The chasm is crossed by building at the height of the monument a team wants.** At the brink the stumps of a broken
bridge reach out from both walls and leave eight blocks between them, the shortest crossing on the board; lower
down a crossing is longer and under fire from every storey above it.

## 3. The read-back

**Every build is read back in text first.** `renders/walks.txt` reports no block over air and no water against
air, and that each of the 969 places a player reaches in the Undercroft's cells and the 297 in the Workings' has at
least three blocks of air over it. All but eight have four; those eight stand on the crypt's tombs. Every named way
between the storeys walks, and each storey reaches the chasm's face.

**The studio reads the map.xml as valid**, with four destroyables, two spawns and two teams.
`check.py` passes all unit tests, and every board and example builds to its recorded hash. The volcanoes study is
the one exception, and it had no hashes before this work.

The pictures, under `freeform/lib/boards/hollowstack/renders/`:

| What | Section | Textured |
|---|---|---|
| the whole board | `40-cut-middle.png`, `44-cut-chasm.png` | `50-board.png`, `51-section.png` |
| each wall's face across the chasm | — | `52-face-blue.png`, `53-face-red.png` |
| the Tops and the keep | `42-cut-keep-well.png` | `56-tops.png`, `57-keep.png` |
| the Underwood, its wells and its mouth | `41-cut-wells.png` | `54-underwood.png`, `55-underwood-mouth.png` |
| the Undercroft and the Vault | `43-cut-vault.png` | `51-section.png` |
| the Deep | `40-cut-middle.png` | `58-deep.png` |
| the segment kit, each piece in both styles | — | `assets/renders/` |

## 4. pgmvox

**Three capabilities were added, each with a test and a section in `freeform/lib/README.md`, and no recorded hash
moved.**

| Added | What it is |
|---|---|
| `built.segments` | a kit of passage pieces on a grid of cells five across and six high: corridor, corner, junction, dead end, a stair two cells long climbing a storey, a ladder shaft with hatches, rooms of several cells (hall, library, prison, crypt) and ports onto the outside; two kits, `DUNGEON` in stone bricks and `MINE` in rock and timber |
| `segments.network` | the links joining the cells a plan needs by the shortest ways, a turn costing more, then a share of dead ends and rings |
| `under.wander` | a tunnel's waypoints swung sideways and breathing in width between a few stated points, with a wide mouth; Chantry Gill's caves now use it, their hash unchanged |

**The first network was a spanning tree, and it left a maze.** A random depth-first tree pruned back to the needed
cells covered 131 of 224 cells; the shortest-way network covers 53 with the same pieces joined.

**Four gaps are open.**

- A ladder that loses its wall to a later carve is not caught where it is laid; the board removes them at the end.
- Gravel or sand left over a hollow falls in game; the board makes such blocks fast at the end. Both belong in the
  library as a finishing pass.
- The walk counts a fall into water only when any fall is allowed, so a drop into water and a deadly drop read the
  same; the board reports the walks with and without drops.
- The studio's renderer does not darken a cave, so a mouth reads as stone on the pictures and as a dark hole in game.
