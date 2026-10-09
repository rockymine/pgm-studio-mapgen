# The Brittlebush grammar — what the builds taught, and how to generalize it

**Brittlebush is not a palette but a grammar: a handful of rules applied to a grid of cells.** Every block the
library lays for it follows from three things: the cell's height and kind, the section it belongs to, and how
much air lies beside each face. This note lists the rules as they were found in the original, where each lives in
`pgmvox.brittle` now, and how the same machinery could carry other patterns.

## Three units

**The cell is five blocks, a level is three, and a storey is five.** The five-block storey is the cap's own height,
which is why a house wall and a ground edge can be the same pattern. Every rule below is counted in these units.

| Unit | Blocks | What it sets |
|---|---|---|
| Cell | 5 | where pieces, stairs, panels and storeys begin and end |
| Level | 3 | every change of height; a stair cell climbs one |
| Storey | 5 | a house's floor to floor; the full cap; the air a panel needs |
| Deck | 8 | a stacked piece's deck over its lower floor: four courses of deck, four of air |

## The rules, as found

**A surface is cut into sections, and every section is a rectangle.** The original's broad plazas are rows of
squares two cells by two, each with its own outline, meeting in a double line of planks. A blueprint whose cells
carry a `section` gets this from `pieces()`; without sections every same-height area floods into one piece, and the
large areas read as one convoluted shape.

**A section's outline is one block, and its material says what lies beyond.** It is the rim, an upside-down spruce
stair, where the ground falls away; spruce planks where it meets a wall, a stair or another section. The fill
starts on the next block in. A second ring of wood inside the rim is the mistake that made every shape look
heavy.

**A section is filled by its shape, then by its place.** A rectangle two cells or more each way takes a bed: two
rings of sandstone stairs, one rising each way, round grass. Anything narrower takes sand mixed with upside-down
sandstone stairs, with cacti and dead bushes only on the pure sand. A tree belongs to the back of the board. A
section on the front line, facing a build zone, keeps open grass.

**A face is a stack of courses read down from its edge, and how much of it shows depends on the drop.** The full
stack is five: rim, brick, dark-oak slab, upside-down dark-oak stair, black clay. Every other cell along a face
swaps the middle three for the birch panel, framed in black clay, so the band runs on unbroken. The panel needs
five blocks of air beside it; over a drop of three the face keeps the plain courses, and over a deck the band is
left off.

**A house is the ground's face again, stood on its own plate.** Each storey of whole cells has a wall that is the
cap read upward, and a plate that overhangs one block in eaves. A plate that nothing stands on becomes a section of
its own, a sand terrace. So a house is sections stacked, each smaller than the one under it, and the same outline
and fill rules apply on its roofs.

**A hollow is a deck, four blocks of air, and a lower floor that runs into the world's floor.** The lower floor
keeps only the top of the face: rim, brick, black clay. A run of hollow two cells or longer takes a dark-oak pillar
two wide at its middle. A hollow along one side is an under-section; a line through a piece is a tunnel.

**Water marks itself and a bare zone is marked by cobwebs.** Water lies at the foot of the void with no kerb,
since PGM holds it still. A bare zone carries a cobweb at the middle of each edge that faces the open void.

## Where the rules live now

| Rule | In `pgmvox.brittle` | Fixed in code |
|---|---|---|
| Sections | `pieces()`, `Cell.section` | the double plank line between sections |
| Outline | `build()`, depth 0 of a piece | rim and plank materials |
| Fill | `bed()`, `sand()`, `build(fill=)` | ring order, sand mix, plants, tree size |
| Face | `cap()` and its `panel` | course order, panel geometry, the five-block rule |
| House | `house()` | wall courses, eave pattern, terrace, beacon |
| Hollow | `_under()`, `_pillars()` | deck depth, pillar motif |
| Zones | `build()` | cobweb spacing |

**Every row of that table is a choice of blocks over a rule that would serve any style.** The rules (sections,
exposure, alternation per cell, storeys of cells, roofs as sections) are the reusable part. The blocks and their
order are what makes it Brittlebush, and they are written into the functions.

## How to generalize it

**Split the style from the grammar: a `Style` holds the blocks, and the build reads the blueprint.** The build
already knows, for every column, its section, its depth in the section, its drop on each side and its cell along a
face. A style would answer, for each of those, which block goes there. Brittlebush becomes one `Style`, and the
board scripts pass it in.

| A style names | Brittlebush's answer | Another answer the same build could take |
|---|---|---|
| The face's courses, top down | rim, brick, slab, stair, black clay | a stone cornice over a dyed band |
| The accent and its period | the birch panel, every other cell | a team-coloured inset every third cell |
| The accent's minimum air | five | three, for a shallow inset |
| The outline over a drop, against a section | spruce stair, spruce planks | slab rim, a line of polished stone |
| The fills, by shape | bed with two rings, sand mix | a checker, rings centred in squares, paving |
| The tree rule | back of the board only | none, or one per section |
| The house's walls and eaves | the face read upward, plank eaves | the same face, a slab roof |

**Faces and fills are the two places a new pattern goes.** A face recipe is a list of courses from the top, an
accent with its period and its minimum air, and a corner rule. A fill recipe takes a rectangle and lays it. The
floor patterns built by hand for an earlier capture-the-wool board, squares in a rim and rings round a mark, are
fill recipes waiting to be written as such.

**Sections are what make a pattern readable, so they should come from the plan.** Every override in this board's
`plan.py` is a decision the planner could carry: a split of a piece into sections, a section's fill, the cells
hollow under a deck, a zone's kind, a piece raised a level. With those drawn in the studio, a board script would be
the style and nothing else.

## What to do next

1. Gather the blocks in `pgmvox.brittle` into a `Style` dataclass, with Brittlebush as its first value, and keep
   every board's output the same block for block.
2. Write the earlier board's floors as fill recipes, and its dressed faces as a face recipe, and build one board in
   each style from one blueprint to prove the split.
3. Read section splits, fills and hollow cells from the studio plan, so `SPLIT`, `FILL` and `UNDER` leave the
   board scripts.
