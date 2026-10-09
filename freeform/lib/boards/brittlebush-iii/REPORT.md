# Brittlebush III — the report

**Brittlebush III is built from the plan its author drew in the studio's planner, and every team reads back the
same.** It is capture the wool for four teams of twelve: each keeps one wool and captures the other three. The
plan is `plan.json`, saved from the studio's map `untitled-plan-8`. This is what the build made of it.

## What is in the folder

- `plan.json`: the studio's plan, version 2, as the author drew it.
- `scripts/plan.py`: the plan read into cells, the placements, and the objectives.
- `scripts/gen.py`: the world, red's part laid by `pgmvox.brittle` and turned a quarter three times.
- `scripts/mapxml.py`: the map.xml, written to `scripts/map.xml` and into `world/`.
- `scripts/walk.py`: the built world read back, written to `renders/walks.txt`.
- `scripts/renders.py`: the pictures.
- `world/`: the Minecraft world, ready for PGM.

The whole board is rebuilt with `python3 -m pgmvox.run boards/brittlebush-iii --build <dir>` from `freeform/lib`.

## How the plan is read

**`pgmvox.studioplan` reads the planner's pieces as the author used them.** A later piece lies over an earlier
one. A piece named `stair…` is a stair cell climbing from its lower neighbour to its higher, and a piece named
`double…` is a deck.

**A zone where no piece lies is a build zone, and its name says which kind.** A zone named `water…` lays water at
the foot of the void, with no cobwebs and no kerb: PGM holds the water still. Any other zone is bare, with cobwebs
on its outline where it faces the open void.

**The plan's heights are its own.** The lowest decks stand at 9, so their lower floors, eight under them, lie at 1
and run straight into the floor of the world. An earlier build raised every height six blocks to keep a full
cornice under those floors, and the board towered over its void.

## The under-sections

**A double-layered piece is hollow under part of its deck, as Brittlebush I's island beside the middle is.** The
deck's edge over the hollow is the cornice without its black band. Four blocks of air stand under the deck. The
lower floor eight down has no full cornice: its edge is the rim, brick and black clay, as many as fit over y 0,
with sand in its middle and planks along the wall at its back.

**Where the hollow's open side runs two cells, a dark-oak pillar two wide stands at its middle.** Planks, a stair
and an upside-down stair repeat from under the deck down into the lower floor's edge. The wall behind the hollow
carries a line of black clay under the deck and bedrock below it.

**The plan does not draw the hollows, so `plan.py` names them in `UNDER`.**

| Piece | Hollow |
|---|---|
| The middle island, two cells by two | one cell deep and two wide, along its side toward the centre, with a pillar |
| The island two cells by three | a tunnel one cell wide through its middle, open to the zones at both ends |
| The island before the wool, two cells by three | one cell deep and two wide, along its side toward the lane, with a pillar |

## The buildings

**The spawn is a house of two storeys over the spawn's footprint, its door toward the lane.** A stack of the
team's wool floats high over it.

**The wool's room is a tower of three storeys over the wool's footprint, its door onto the ground in front.** The
wool's colour runs in its bands, and the wool's heart floats over it. The four wools are yellow, orange, pink and
purple, Brittlebush II's colours.

## Read back from the world

**Every check comes out clean and every team's numbers are the same.** These are from `renders/walks.txt`.

| Read | Value |
|---|---|
| Objectives with a problem | 0 |
| Blocks without footing | 0 |
| Water standing against air, the zones' floor aside | 0 |
| Water at the zones' floor against the void, held by PGM | 240 |
| Board without block 36, block 36 off the board | 0, 0 |
| Places reached on foot from a spawn | 783 |
| Spawn to its own wool room's door, building | 54 |
| Spawn to the other three wools, building | 110, 136 and 144 |

**Every piece of the plan is its own island, so the wools are reached by building.** The building walk stands in
for blocks placed with water over the zones and four blocks over the board.

## What the build found

**The library could not read a studio plan, nor turn a board a quarter.** The quarter turns came in pgmvox
0.11.0, and `pgmvox.studioplan` with the hollows under a deck in 0.12.0, each with tests.

**A pillar on an even run stands across two cells, so it is laid after every hollow is cut.** Laid with its own
cell, the second cell's hollow cut away its second column.

**The plan's zones gained names during the build.** The first copy had none and every zone was laid as water; the
author's names now tell water from bare zones.

## What was not done

- The board was not opened in PGM. The map.xml is written by the library and the objectives check against the
  world, but no match was played.
- The board was not written back to the deployed studio. Its world and map.xml are in this folder.

## The renders

- `05`: the built world from above with the objectives.
- `30`–`35`: the board from two corners, red's part, its spawn, its wool's tower, and the middle.
- `36`–`38`: the three under-sections: the middle island, the tunnel, and the island before the wool.
