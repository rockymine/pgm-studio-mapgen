# Ocotillo — the layout

**Ocotillo is a capture-the-wool board for four teams, one wool each, laid out as a blueprint of five-block
cells in the Brittlebush style.** Each team keeps its own wool in a tower beside its spawn and must capture the
other three. This is the layout only, for review. The sketch is `renders/00-plan-sketch.png`, the checker's table
is `renders/plan-check.txt`, and both are drawn from `scripts/plan.py`.

## What Brittlebush was read for this time

**Brittlebush II is laid on a grid of five-block cells.** A census of its top surfaces cell by cell puts its
platform edges on the grid with only 36 of 648 cells partly land, where the trees and the cobwebs fall. It is
mirrored both ways about the middle of the grid.

**Its levels are three blocks apart, and every change of level is one stair cell.** II stands at 4, 7, 10, 13, 16
and 19; Brittlebush I at 8, 11 and 14. A stair cell climbs its three blocks in five rows of half steps, a
stone-brick slab and a stone-brick block in turn.

**No flat piece runs much more than three cells before a stair or a gap.** That is fifteen blocks, and it is
what keeps the boards small and busy.

**The cobwebs mark where a player builds, and where water lies.** In II they trace the void between platforms and
along the board's edge; in I they mark the cells with water at the foot of the void.

## The pieces

**Every cell is one of a handful of pieces.**

| Piece | What it is |
|---|---|
| Flat | level ground at one of five levels: 7, 10, 13, 16, 19 |
| Stair | one cell climbing one level, three blocks in five, slab and block in turn |
| Stacked | a deck one level over an underfloor: covered ground under a deck |
| Keep | a team's spawn, three cells by three at 19 |
| Tower | a team's wool room, two cells by two, a tower of narrow storeys on its yard |
| Gap | void a player builds over, cobwebs on the floor of the void under it |
| Water | void with water at its foot, marked by cobwebs too |

**A piece's finish follows from its shape.** A flat piece only one cell wide is laid in sand, with pebbles of
sandstone stairs, cacti and dead bushes, which stand on sand only. A piece with two cells by two in it gets the
inlay: sandstone kerbs, birch and grass beds. An inlay bed carries one tree for every four cells of grass, so a
two-by-two court has one and a narrow bed none.

**Faces alternate their finish cell by cell along a piece's edge.** One cell takes the plain cornice of spruce,
brick, dark oak and black clay; the next takes the birch-stair panel. The stair details give a wall depth without
insetting it.

## The arrangement

**The board is four quadrants, one a team, each its neighbour turned a quarter about the middle.** Red holds the
north-west, blue the north-east, green the south-east and yellow the south-west. The board is 26 cells a side,
130 blocks.

**Each quadrant is its own mirror across its diagonal.** A team's two neighbours meet it in the same way, so no
team has a near and a far neighbour.

**From each team's corner to the middle, the levels step down one at a time.**

| Level | Floor | Pieces, in red's quadrant |
|---|---|---|
| 5 | 19 | the Keep, the spawn, in the corner |
| 4 | 16 | the two Orchards on the wings; the two Lookouts |
| 3 | 13 | the Tower and its yard; the two Arbours' decks; the sand walks |
| 2 | 10 | the posts on the borders; the Arbours' covered walks; the inner court; the dais |
| 1 | 7 | the landings on the borders by the middle |

**The neighbours meet across gaps, and everyone meets at the dais.** Along each border, a team's post faces its
neighbour's across two cells of gap, and its lookout faces the other lookout across two more. By the middle, a
landing at 7 is shared by two neighbours, with a stair up from it to each team's inner court and one onto the
dais. The dais is ten blocks square at 10, one cell from each quadrant.

## The places, in red's quadrant

- **The Keep** (19): the spawn, three cells by three, with the three monuments for the other teams' wools.
  Two stairs lead down out of it, one onto each wing.
- **The Orchards** (16): three by three on each wing, inlay with two trees.
- **The sand walks** (13): one cell wide and two long, down a stair from each Orchard toward the border.
- **The posts** (10): one cell wide and three long on each border, facing the neighbour's post across a gap.
- **The yard** (13): an L of sand round two sides of the Tower, down a stair from each Orchard.
- **The Tower** (13): the wool room, two cells by two on the diagonal, its door onto the yard. The wool's heart
  floats over it.
- **The Arbours** (13 over 10): stacked pieces three by three either side of the Tower, their decks level with
  the yard and their covered walks open onto the inner court. Two cells of gap lie between each Arbour and the
  sand walk beyond it.
- **The Lookouts** (16): one cell, up a stair from each Arbour's deck, facing the neighbour's across a gap.
- **The inner court** (10): an L of inlay by the middle, with a stair up onto each Arbour's deck and an entry
  into each covered walk.
- **The landings** (7): one cell each, on the borders by the middle, shared with the neighbour.
- **The dais** (10): its quarter of the ten-block square in the middle, a stair up onto it from each landing.

## The numbers

**Every rule holds and every team's numbers are the same.** These are red's, from `renders/plan-check.txt`.

| Measure | Value | Target |
|---|---|---|
| Spawn to its own wool room | 34.7 | short, under 40 |
| Spawn to a neighbour's wool room | 99.7, 11 of it built across a border gap | 46 to 143 |
| Spawn to the opposite team's wool room | 142.5, walked through the middle | 46 to 143 |
| Spawn to the dais | 86.7, walked | |
| Stairs that do not climb one level | 0 | 0 |
| The longest straight run at one level | 3 cells, 15 blocks | 3 cells |
| Flat cells by theme | 76 sand, 112 inlay | |
| Floors not reached from a spawn | 0 | 0 |

**A neighbour is the closer target, and only by building.** A team reaches either neighbour's wool by building
across a border gap, ten blocks, or walks round by the middle. The opposite team's wool is walked, but only
through the dais, where all four teams cross.

**The opposite team's wool is at the top of the corpus's range.** If the board plays long, the first change is
to bring the towers one cell nearer the middle.

## What the build will need from the library

- **A quarter-turn symmetry.** pgmvox mirrors and half-turns a board; four teams need its world, its objectives
  and its sketch turned a quarter at a time.
- **Room protection for more than two teams.** A wool room keeps out every team but the attackers, and the
  library works that out for two teams only.
- **The Brittlebush pieces as library pieces.** The edge, the frame and fields, the stair cell, the stacked cell
  and the tower are in the study's `style.py`. A blueprint board wants them keyed to a cell.
