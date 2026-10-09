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

**The spawn's house is stacked of whole cells over its whole piece too, but otherwise than the wool's.** Its first
storey takes all four cells, the second the two back cells away from the lane, and one cell sits on top at the
north end. Its doors open west onto the lane and south toward the monuments, without cobwebs. Inside lies the
keep's own floor, ringed in the team's clay.

**The team's colour runs under its eaves and in the glass over its beacon.** A stack of the team's wool floats
high over it. From the spawn point the three monuments are 12, 9 and 10 blocks on foot.

**The wool's house takes its whole piece, ten blocks square, as Brittlebush I's do.** Its storeys are whole cells,
five blocks each: two cells by two, then an L of three, then one cell on top. The L leaves open the front cell
toward the centre, where the door is, and the top cell stands behind it.

**Each storey's wall is the ground's edge again.** Read bottom up it is black clay, an upside-down dark-oak stair, a
dark-oak stair and brick. Every other cell along a face carries the birch panel framed in black clay, with the
wool's colour under the eave over it.

**Each plate overhangs by one in eaves of planks, upside-down spruce stairs and a slab.** A plate no storey
stands on is a terrace of sand in a ring of spruce stairs, on a ceiling of sandstone lit by a sea lantern.

**The wool stands on a square of its own colour inside a door three wide, cobwebs just within it.** A beacon on
gold in the top cell shines through glass of the wool's colour. The four wools are yellow, orange, pink and
purple, Brittlebush II's colours. The plan's footprint for the wool was eight blocks square; the house takes the
whole piece instead.

**A piece's outline is one block, as in the original.** Where it falls away it is the rim; where it meets a wall or
a stair it is a line of spruce planks. The bed or the sand starts on the next block in.

## Read back from the world

**Every check comes out clean and every team's numbers are the same.** These are from `renders/walks.txt`.

| Read | Value |
|---|---|
| Objectives with a problem | 0 |
| Blocks without footing | 0 |
| Water standing against air, the zones' floor aside | 0 |
| Water at the zones' floor against the void, held by PGM | 240 |
| Board without block 36, block 36 off the board | 0, 0 |
| Places reached on foot from a spawn | 767 |
| Spawn to its own wool room's door, building | 55 |
| Spawn to the other three wools, building | 111, 136 and 144 |

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
- `39`: the wool's house close, from the south-east and the south-west.
- `40`: the whole board from each of its four corners.
