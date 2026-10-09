# Brittlebush KotH — the layout

**Brittlebush KotH is a king-of-the-hill board for four teams with five hills, laid out as a blueprint of five-block
cells in the Brittlebush style.** It began as a capture-the-wool layout; the review found every wool too easy to
reach, with no real middle and gaps too small to make bridging matter, and turned it to capture points. This is
the layout and the map.xml, for review. The sketch is `renders/00-plan-sketch.png`, the checker's table
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
| Flat | level ground at one of six levels: 7, 10, 13, 16, 19, 22 |
| Stair | one cell climbing one level, three blocks in five, slab and block in turn |
| Keep | a team's spawn, three cells by three at 22, a house of two storeys over it |
| Gap | void a player builds over, cobwebs on the floor of the void where it meets the open void |
| Water | void with water at its foot, which marks it without cobwebs |

**A piece's finish follows from its shape.** A piece that is a rectangle two cells or more each way gets a bed of
grass filling it inside its one-block outline, ringed twice in sandstone stairs, one ring rising inward and one
outward, with a birch where the grass is four or more wide. Any other piece is laid in sand mixed with upside-down
sandstone stairs, and cacti and dead bushes stand only on its pure sand.

**Faces alternate their finish cell by cell along a piece's edge.** One cell takes the plain cornice of spruce,
brick, dark oak and black clay; the next takes the birch-stair panel, five wide and framed in black clay down both
sides. The black band so runs unbroken along every edge, at the cornice's foot and round each panel. A stair
cell's sides carry the same cornice.

## The game

**Five hills: the Dais in the middle, worth two points a second, and an island on each border, worth one.** A
border hill lies on the island between two neighbouring spawns, so it is the same walk for both teams beside it.
That is the corpus's own shape: four-team boards carry one point per team and a centre, five in all, and most put
the ring on the diagonals between neighbouring spawns. Each hill is a square pad ten blocks a side, captured in
five seconds.

**Every player spawns with sixteen leaves to bridge with, and every kill pays a leaf and a golden apple.** The
kit is a stone sword, a bow with sixteen arrows, an iron pickaxe, the leaves, steak and team-coloured leather.

**Golden apples grow on the four inner islands, and arrows on the four landings.** An inner island lies between
two neighbours beside their Arbours, across a cell of gap, so the apples are bridged to with the kit's leaves. A
landing lies on the way to the Dais, so the arrows are picked up on the way in. An apple drops every thirty
seconds, one at a time; four arrows every ten seconds, up to eight.

**The first team to 400 points wins, within fifteen minutes.** Building is allowed only over the board and its
gaps, up to y 40.

## The arrangement

**The board is four quadrants, one a team, each its neighbour turned a quarter about the middle.** Red holds the
north-west, blue the north-east, green the south-east and yellow the south-west. The board is 26 cells a side,
130 blocks.

**Each quadrant is its own mirror across its diagonal.** A team's two neighbours meet it in the same way, so its
two border hills are the same walk.

**From each team's corner to the middle, the levels step down one at a time.**

| Level | Floor | Pieces, in red's quadrant |
|---|---|---|
| 5 | 22 | the Keep, the spawn, in the corner, its house over it |
| 4 | 19 | the two Orchards on the wings |
| 3 | 16 | the yard; the two terraces |
| 2 | 13 | the border hills; the two Arbours; the inner islands |
| 1 | 10 | the inner court; the Dais |
| 0 | 7 | the landings on the borders by the middle |

**Every piece is at least two cells deep, and every stair two cells wide.** A stair is ten blocks across and five
long. A cell on a border pairs with the neighbour's cell beside it, so a one-cell island or stair on the border is
two cells, ten blocks, once the two quadrants meet.

**Every hill is reached on foot; the apples are reached by bridging.** A terrace steps down to its border hill by
a stair two cells wide, and the neighbour's terrace does the same from the other side. Beside each Arbour an inner
island faces it across a cell of gap. By the middle, a landing at 7 is shared by two neighbours, with a stair up
from it to each team's inner court and one onto the Dais.

## The places, in red's quadrant

- **The Keep** (22): the spawn, three cells by three, under a house of two storeys of black clay with a band of
  the team's clay under each plate. Its two doors open onto the two stairs, each two cells wide, that lead down
  out of it, one onto each wing.
- **The Orchards** (19): three by three on each wing.
- **The terraces** (16): three by three, down a stair from each Orchard toward the border.
- **The border hills** (13): the islands on the borders, one cell wide and three long, two wide with the
  neighbour's, down a stair from each team's terrace. The hill's pad is the middle ten blocks.
- **The yard** (16): down a stair from the Orchards, with a pond in its inner corner.
- **The Arbours** (13): three by three either side of the pond, down a stair from the yard.
- **The inner islands** (13): beside each Arbour on the border, across a cell of gap: the golden apples.
- **The inner court** (10): by the middle, with a stair up onto each Arbour and one down to each landing.
- **The landings** (7): one cell wide on each border by the middle, two with the neighbour's: the arrows.
- **The Dais** (10): the middle hill, ten blocks square, a quarter of it in each quadrant, a stair up onto it from
  each landing.

## The numbers

**Every rule holds and every team's numbers are the same.** These are red's, from `renders/plan-check.txt`.

| Measure | Value | Target |
|---|---|---|
| Spawn to the Dais, on foot | 82.0 | |
| Spawn to the two border hills beside it, on foot | 53.0 and 53.0 | the same |
| Spawn to the two border hills beyond, on foot | 149.4 and 149.4 | |
| A border hill's distance from the middle, over a spawn's | 0.71 | 0.52 to 0.99 |
| Spawn to the nearest golden apples | 63.5, 6.8 of it bridged | |
| Spawn to the nearest arrows, on foot | 74.2 | |
| Stairs that do not climb one level, or narrower than two cells | 0, 0 | 0 |
| The longest straight run at one level | 3 cells, 15 blocks | 3 cells |
| Floors not reached from a spawn | 0 | 0 |

**A team's two border hills are its own to contest, and the far two belong to the others.** At 53 a team reaches
the hills either side of it well before the Dais at 82, and the far border hills at 149 are not worth the walk
while the Dais is held. So the game is four fights on the borders and one in the middle.

**The studio reads the map.xml as valid.** Its own parser finds the four teams and spawns, the five hills, the
kit and the eight spawners, and its validity check raises nothing.

**No piece is one cell wide, so no piece is sand by the shape rule.** Sand still lies inside the inlay, as the
field round each kerbed bed, as it does in Brittlebush. If whole pieces of sand are wanted, the border hills are
the place: they are the most exposed ground on the board.

## What the build needed from the library

- **A quarter-turn symmetry.** pgmvox mirrored and half-turned a board; four teams needed its world, its
  objectives and its sketch turned a quarter at a time. That is `Symmetry("rot_90")` and `turn_world(w, "cw")`.
- **The Brittlebush pieces as library pieces.** The edge, the panels, the beds and sand, and the stair cell are
  `pgmvox.brittle`, keyed to a cell.

## What changed after the first review

**The first layout had too many pieces one cell wide or one cell deep.** It is kept as
`renders/00-plan-sketch-v1.png`.

- **Every stair is two cells wide.** The keep's two exits, the stairs off the Orchards, into the covered walks,
  onto the decks and to the landings are all ten blocks across.
- **The narrow pieces were widened or folded into others.** The sand walk became a terrace three by three, the
  posts became islands two wide with the neighbour's, the yard became three by three round the Tower, and the
  lookouts went.
- **The Tower moved one cell inward,** onto the yard's corner. The yard met it on two sides and the Arbours'
  decks on the other two.

## What changed after the second review

**The board became king of the hill.** Capture the wool did not work on it: every wool was easy to reach, there
was no real middle, and the gaps were too small to make bridging matter.

- **Five hills:** the Dais, and the island between each pair of neighbouring spawns.
- **Each terrace steps down to its border hill** by a stair two cells wide, where a gap stood before, so every
  hill is reached on foot.
- **The towers keep no wool.** They stay as each team's landmark, with its heart over it.
- **The kit carries sixteen leaves, a kill pays a leaf and a golden apple,** and golden apples and arrows grow on
  the inner islands and the landings.

## What changed after the third review

**The towers and the decks went, and the spawn got a house.** The towers were left over from capture the wool,
and a king-of-the-hill board wants no covered ground.

- **The Tower's cells became the pond,** and the Arbours flat ground at 13.
- **The Keep carries a house** of two storeys, its doors onto the two stairs out of it.
- **Every level rose three blocks,** so the cornice under the lowest landing clears the floor of the world.
- **The finish follows the original more closely:** the five-wide framed panel, the cornice on the stairs' sides,
  the double ring of sandstone stairs round every bed, and the cobwebs off the water.
