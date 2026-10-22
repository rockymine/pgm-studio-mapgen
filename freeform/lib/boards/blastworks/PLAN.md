# Blastworks: the plan

Capture the wool, two teams of sixteen, one wool a team. The author's second concept, the one without a roof: a box
of bedrock holding the wool, blown open with TNT from the top and from the side. `scripts/layout.py` holds every
number below as data.

## 1. The identity

**A wool sealed in a bedrock box behind two doors of end stone, reached over and under a bridge, with TNT to open
it.** The concept's box, its bridge, its stairs and its slits are kept where the concept put them. What it left open
was laid out with the author over five plans, and the last one was approved.

**Two kinds of ground, never floating.** The spawn and the front are natural: solid rock to the world's floor, soil
and grass on top, spruces, boulders and ferns. Everything made is one grammar, polished diorite and stone brick under
a spruce rim, a cyan band a storey, spruce posts with quartz heads, windows of iron bars on quartz sills.

## 2. The layout

Blue holds the west (x < 0) and red is its image under the half turn about (-0.5, -0.5). The board runs 230 blocks
east to west and 42 north to south, z -21 to 20.

| Piece | Where (blue) | What it is |
|---|---|---|
| **The spawn** | x -110 to -69, z 7 to 20, y 12 | natural ground at the map's end; nothing behind it |
| **The hall** | x -106 to -96, z 10 to 17 | a piece of the grammar set into the ground, hollow; the spawn on a 2x2 wool pad and the monument inside |
| **The stairs** | up x -82 to -77, down x -76 to -69 | from the spawn up to the box's deck at y 18 and down to y 6 |
| **The box** | x -96 to -77, z -21 to -8 | the concept's: bedrock walls to y 13 with slits, the wool room inside, deck at y 18 |
| **The bridge** | x -76 to -60, z -21 to -8 | the Steg: a bedrock slab at y 14 and 15 under three courses of deck, void under it |
| **The east block** | x -59 to -41, z -14 to -8, y 26 | raised eight over the Steg; a tunnel through it at y 21, an arm on top over the Steg |
| **The descent** | x -59 to -41, z -21 to -15 | the main artery, from the front at y 14 down to the Steg's end |
| **The front** | x -40 to -27, z -21 to 20, y 14 | natural ground facing the middle |
| **The exit** | two lanes at z 14 to 20 | from the spawn to the front, a gap of eight between them |
| **The middle** | two stones 14 by 14 and the pedestal | each stone 15 blocks before its own front, the TNT spawner on the axis |

**Three ways from the front to the enemy's box.** Down the descent onto the Steg; up the stair at x -40 to -34 into
the tunnel, which comes out three blocks over the Steg; or tower onto the east block, along the arm and jump to the
Steg, or bridge eight blocks from the arm's end to the box and drop TNT.

## 3. The wool and its doors

**The wool lies in the box's room on a 2x2 pad of its own colour, on a checkerboard floor that falls toward the
side door.** The room is seen and shot into through the slits at y 5, 8 and 11, but no player walks through them.
Its chests are the studio's: two stacked in each inner corner, the lower with planks, Speed I potions and golden
apples, the upper with diamond leggings, Power I Infinity bows and planks. The team keeping the room may not open
them.

| Door | Where | How it is blown |
|---|---|---|
| **Roof door** | x -94 to -85, y 15 to 17, a block under the deck | from the box's top, by the enemy alone |
| **Side door** | x -79 to -77, y 2 to 11, flush in the east wall | from the build zone under the bridge |

**End stone breaks by a blast and by nothing else.** Each door is a destroyable that does not count to win. While
both stand the wool is reached in no phase of a match.

**Over its own box, inside the bedrock line at x -83, a team may not go.** It defends the roof door from in front of
it, as the concept's line of bedrock said.

**The monument stands in the spawn's hall against the quartz post beside its door, open on two sides.** Its column
is left out of the spawn's protection, which refuses every block, so the wool can be placed. The spawn stands on a
2x2 pad of the wool it is to fetch: orange in blue's hall, lime in red's.

## 4. Building

**Over the void a player builds only in the build zones, and a line of redstone at y 1 rings each.** The zones are
the whole underside of the bridge, a strip in line with the down stair from its foot to the bridge, the hole from
that stair's edge to the front, the exit's gap, and the middle from front to front. The build height is y 32.

**Only what a player brings breaks, and the doors' end stone by a blast.** The kit carries 12 TNT, which lights as
it is placed, and the pedestal at the middle drops two more every 20 seconds.

## 5. The concept's bedrock

| Where | As the concept had it |
|---|---|
| the box's walls | bedrock from y 0 to 13, the slits through it |
| across the box's top | a line at x -83, the edge the defenders keep outside |
| the bridge | a slab at y 14 and 15 |
| the east block's face over the void | bedrock up to y 15 |
| y 0 under every piece | the floor PGM's void rule reads |

## 6. As built

`scripts/walk.py` writes `renders/walks.txt`.

| Walk | Blocks |
|---|---|
| spawn to its own monument, on foot | 3 |
| spawn to its own roof door, on foot | 51 |
| spawn to the enemy's side door, bridging | 173 |
| spawn to the enemy's roof door, bridging | 187 |
| spawn to the middle's TNT, bridging | 110 |
| a door blown: spawn to the enemy's wool and home | 187 to 196 |

## Open

- How much TNT a door takes, and whether 12 in the kit and two every 20 seconds is the right supply, are numbers
  for a played match.
- The redstone rings hang over the void at y 1, as the studio stamps them; a block update beside one pops it off.
