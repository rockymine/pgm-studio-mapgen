# Claywork — the report

**Claywork is built, and the built world reads back as the plan said it would.** It is a capture-the-wool board for
two teams of sixteen, grounded on bedrock, four flat levels joined by broad steps. The layout is in `PLAN.md`,
which went through four reviews before the build and one after it. This is what the build made of it.

## What is in the folder

- `scripts/plan.py`, `plan_check.py`, `sketch.py`: the layout, its checks and its sketch, unchanged by the build.
- `scripts/gen.py`: the world, from the plan's raster.
- `scripts/mapxml.py`: the map.xml, written to `scripts/map.xml` and into `world/`.
- `scripts/walk.py`: the built world read back, written to `renders/walks.txt`.
- `scripts/renders.py`: the pictures.
- `world/`: the Minecraft world, ready for PGM.

The whole board is rebuilt with `python3 -m pgmvox.run boards/claywork --build <dir>` from `freeform/lib`.

## How it is built

**Every piece stands on twelve blocks of ground over bedrock to the world's floor.** Block 36 lies at y 0 under
every piece and every build zone, and the map.xml lets a block be placed only over a column that is not void. The
build height is 44.

**The land is spoken in the grammar: `pgmvox.grammar` gives the rules, `pgmvox.clay` the blocks.** Every piece is
cut into sections about nine blocks a side, and the cut is the same on both wings. Each section is outlined: stone
brick where the ground falls, a line of polished andesite where it meets the next section. Each section is laid in
its own fill.

**A piece's sections alternate between two fills, as the cells of a checker do, so no two neighbours match.**

| Piece | Sections | Fills, in turn |
|---|---|---|
| The Forecourt | seven by two | paving in bands, squares |
| The Clay Court | seven by three, round the well | a checker of three-by-three paces, an inlay of rings |
| The Aprons | two by two | squares, an inlay |
| The Rostrum | four by one | paving |
| The Arcades | three by one | an inlay, squares |
| The Walks' flat run | one by three | squares, paving |
| The Gatehouse | three by two | an inlay, squares |
| A Statue Terrace, a Kiln | one | an inlay; squares |

**The face's bays answer the sections over them.** Under a cornice of stone brick, a panel six wide and five high is
sunk one block between two chiseled pilasters, the team's clay at its back with a diamond of quartz. There is one
bay to each section's side, centred on it, so the Forecourt's front shows seven bays for its seven sections.

**A bay is laid whole or not at all.** All eight columns, the panel and a pilaster either side, must be face at one
height with the panel's depth of air before them. So the short runs at the Court's corners by the stepping stones,
and wherever a lower piece stands before a face, keep their plain stone.

**The bedrock under the ground is layered so it never shows as one slab.** Two blocks of bedrock lie under the
ground, then a stripe of the team's stained clay set flush, then bedrock patterned with obsidian and black wool
to the floor. The mirror recolours every piece of team colour from red to blue on blue's half.

**A flight of steps is a section of its own, stepped.** A smooth stone lip lies behind each rise and the rest is
stone brick. A runner of clay goes up the middle third, in the team's clay where it meets each rise, and a
stone-brick stair at each tread's back edge is its nosing. Its sides are its outline, and its faces over the void
keep the plain courses, since their top changes every tread.

**An arrow is a motif laid into the section it points out of.** The section is laid as a plate of polished diorite
framed in stone brick, and the arrow's head and shaft fill it one block in, in the team's wool. Wool is used
because it is the truer blue. The arrows stand where they stood: up both flights, toward the band, down the Spawn
Steps, out of the Court and the Arcades, up the Walks.

**Arches of stone brick span both flights of the Grand Steps, each Arcade, and each Walk twice.** Each arch has
a beam and upside-down stair corners, and its legs are what narrow a Walk from twelve to ten.

**The Kilns are brick halls with a hipped roof and a chimney.** Each stands on a stone-brick plinth, with
pilasters every four blocks and windows of iron bars on the three faces over the void. A frieze of the team's
clay runs under the cornice. The roof is brick stairs stepping in a course at a time, and the chimney is four by
four with glowstone embers at its top.

**Inside a Kiln, the wool stands on a dais and two chests of gear stand against the back wall.** Glowstone lights
the ceiling and the pilasters. The door is eight wide, framed in the team's clay with stair corners.

**A chest is laid out as a pattern, filled the same from either end.** The Kilns' gear chests hold a set of iron
armour down the middle around two golden apples, food either side, and arrows and planks at the ends. The defence
chests hold dark-oak planks at the ends and spruce inside them. Crafting tables and end stone lie toward the
middle, redstone blocks run down the centre column, and two Efficiency II iron pickaxes sit either side of it.

**The bedrock walls run from the floor of the world to three over the Walk, so nothing tunnels under them.** Each
holds two defence chests set into the face toward the Kiln, at a third and two thirds of the lane. The air over
each chest lets its lid open, and the column behind it is bedrock.

**The Gatehouse is open to the sky, walled on its back and sides.** Its walls stand on a plinth, with
stone-brick pilasters every four blocks lit by sea lanterns, clay between them with iron-bar windows, and a frieze
of the team's clay. A cornice and battlements finish them. Two cubes of iron, three a side, stand in its back
corners, and the spawn point is on a six-by-five carpet in the team's colour.

**The iron grows back.** The spawn's protection keeps every block as it is but iron, which may be mined there and
regrows as a renewable.

**The statues are figures twelve blocks tall.** Each stands on a plinth with sea lanterns at its corners and the
team's clay on its top. The figure is quartz, with the team's clay at its belt and its crest. One stands on each
Statue Terrace and one on the Rostrum.

**A brick roof on four stilts stands over the well.** The stilts are stone brick at the pit's corners, joined by
a beam of slabs seven over the Court with sea lanterns over the stilts. The roof is hipped like a Kiln's. It is open
on every side, so the drop into the well is as it was.

**The Undercroft is carved three high under the Court and the Arcades, with a roof three thick, and reached by the
well.** Its floor is at 17, six under the Court, and the well's whole floor is a pool to land in. A ladder at each
end climbs the Walk's face.

## Read back from the world

**Every check on the built world comes out clean.** These are from `renders/walks.txt`.

| Read | Value |
|---|---|
| Objectives with a problem | 0 |
| Wools missing from their rooms | 0 |
| Blocks without footing | 0 |
| Water standing against air | 0 |
| Land or build zone without block 36, block 36 under plain void | 0, 0 |
| Blocks in a wall's columns that are not bedrock, a chest and its lid aside | 0 |
| Defence chests in the walls, gear chests in the Kilns | 8, 8 |
| Iron blocks, and of them inside a spawn's area | 108, 108 |
| Spawn to its own monuments, on foot | 14 and 15 |
| Spawn to an enemy Kiln, on foot | not reached: the band and the wall are built over |
| Spawn to an enemy Kiln, building | 215, both Kilns, both teams |
| Court into the well's pool | 9, a drop of six into water |
| On through the Undercroft and up the ladder onto the West Walk | 76 |
| Out of the well without a ladder | no |
| The stepping stones, first to last | 16 |
| The stepping stones, last back up onto the Arcade | 20 |

**The building walk floods every build zone and the walls with water from y 10 to the build height.** The walk
swims through water as a player climbs a tower they build, so this is the stand-in for building.

## What the build found

**The library's walk could not jump down onto a lower floor.** A running jump only ever landed one block up or
level, so the stepping stones read as reached going up but not coming down. The walk now lands on the first floor
below the gap, down to the move rules' greatest drop. The library's tests gained a case for it, and every
example's snapshot was unchanged.

**A defender cannot walk into their own Kiln either, and that is intended.** The bedrock wall spans the Walk with
both ends on the void, so it stops everyone. It is the line the defence builds its own wall at, which is why the
defence chests stand at it.

**The floor's palette is grey.** Clay, stone and double slab are all pale grey blocks, and the checker reads mostly
as texture. The team's colour now carries the board: the arrows, the panels, the friezes, the carpet and the
statues. Blue's panels and friezes are blue stained clay, which reads as a dark violet.

## What was not done

- No cover was placed on the Forecourt or the Court. The plan fixed where it may go, and the board is
  playable without it.
- The board was not opened in PGM. The map.xml is written by the library and the objectives check against the
  world, but no match was played.

## The renders

- `00`: the plan sketches, v1 to v4.
- `05`: the built world from above with the plan's names.
- `10`–`12`: sections along the West Walk, through the Rostrum, and along the Undercroft.
- `30`–`36`: isometric views of the board, red's half, the Gatehouse and Court, a Kiln and its Walk, the front,
  the Arcade with its stepping stones, an Apron and its Walk close up for the floors, and the Court and Forecourt with the well's roof.
- `40`: the Undercroft in x-ray.
- `50`: the Forecourt's face as seen from the band.

## What I wanted, how hard it was, and what a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| A grounded board with layered faces | Easy: every column gets ground, bedrock, a stripe and a pattern from one function | A face treatment on a piece: the depth of ground, the stripe, and the pattern below |
| Building only over the board | Easy: block 36 at y 0 and a `not void` filter | Build zones drawn on the plan, and the block and filter written from them |
| Floors that tell the pieces apart | Moderate: a checker for the two broad floors, squares in a rim centred on each piece's box, treads for the steps | A surface pattern per piece, laid out from the piece's own outline and chosen with the theme |
| Arrows and arches | Moderate: each is placed by hand along its way, centred on a lane that may be an even number wide, and the arches must leave the narrowest at ten | Way-marking pieces that follow a route on the plan and centre themselves on it |
| Dressed faces | Moderate: each face cell finds its run along the face at one height, and the bays are centred on it | A face treatment that lays out bays on a piece's edge, with the team's colour in it |
| Chests laid out as patterns | Easy once the library could write enchantments: rows of letters and a legend | A chest editor that shows the 27 slots as a grid |
| A second layer under the hub | Moderate: a storey in the raster for the plan's walk, then carved and walked on the blocks | Storeys on the plan, carved from the piece above them |
| Stepping stones that cross both ways | Hard: the plan's walk passed them, and the voxel walk could not land a jump lower until the library was fixed | Jump checks on the plan that use the same rules as the built world's walk |
| A defence wall nobody walks round or under | Easy: bedrock from the world's floor across the Walk, its ends on the void, chests in its face | The wall as a seam piece, with its effect on both teams' walks shown on the plan |

## After the playtest

**The Kilns carry the studio's wool-room loot, and the walls its defence chests.** Each Kiln's two chests of iron
became two chests in each of its four inner corners, with the planks, Speed potions, golden apples, diamond
leggings and Power bows the studio's wool-room stamper gives. The chests set into the bedrock walls keep their
places and now hold the studio's defence loadout: dark-oak and spruce planks, crafting tables, end stone, redstone
and two Efficiency II pickaxes. The walk counts 32 chests in the Kilns where it counted 8, and every distance is
unchanged.
