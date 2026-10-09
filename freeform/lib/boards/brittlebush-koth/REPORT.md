# Brittlebush KotH — the report

**Brittlebush KotH is built, and every team's walks to the hills read back the same.** It is a king-of-the-hill
board for four teams with five hills, laid on a grid of five-block cells in the Brittlebush style. The layout is
in `PLAN.md`, which went through three reviews. This is what the build made of it.

## What is in the folder

- `scripts/plan.py`, `plan_check.py`, `sketch.py`: the blueprint, its checks and its sketch.
- `scripts/gen.py`: the world, red's quadrant laid by `pgmvox.brittle` and turned a quarter three times.
- `scripts/mapxml.py`: the map.xml, written to `scripts/map.xml` and into `world/`.
- `scripts/walk.py`: the built world read back, written to `renders/walks.txt`.
- `scripts/renders.py`: the pictures.
- `world/`: the Minecraft world, ready for PGM.

The whole board is rebuilt with `python3 -m pgmvox.run boards/brittlebush-koth --build <dir>` from `freeform/lib`.

## How it is built

**Red's quadrant is laid cell by cell, and the other three are its quarter turns.** Each turn moves the team's
colour on a team in the clay, wool, glass and carpet, so blue's quadrant is red's in blue. The hills' pads, the
spawners' marks and the objectives are laid over the whole board after the turns.

**Every cell stands on stone over bedrock to y 3, obsidian under it, and block 36 at y 0.** A cell's edge carries
the cornice where its neighbour lies lower, and every other cell along a face carries the birch panel instead.

**The Keep carries a house of two storeys.** Black clay walls, a band of the team's clay under each plate, a crown
of sandstone round a gold block on the roof, and two doors onto the two stairs out of the Keep.

**Each hill is a pad of white clay ten blocks square, cleared of the beds and trees over it.** Each spawner stands
over a mark of chiseled sandstone.

## Read back from the world

**Every check comes out clean and every team's numbers are the same.** These are from `renders/walks.txt`.

| Read | Value |
|---|---|
| Objectives with a problem | 0 |
| Blocks without footing | 0 |
| Water standing against air, the ponds' floor aside | 0 |
| Water at the ponds' floor against the void, held by PGM | 36 |
| Board without block 36, block 36 under plain void | 0, 0 |
| Spawn to the Dais, on foot | 71 |
| Spawn to the two border hills beside it, on foot | 53 and 53 |
| Spawn to the two border hills beyond, on foot | 143 and 143 |
| Spawn to the golden apples, building | 58 |
| Spawn to the arrows, on foot | 63 |

**The built walks are shorter than the plan's because the voxel walk jumps down where the plan's walks a stair.**
The order is the plan's: the two border hills beside a team come well before the Dais, and the far two are not
worth the walk while the Dais is held.

## What the build found

**A quarter turn needed new pieces of the library.** `Symmetry("rot_90")`, `turn_world(w, "cw")`, `Teams.next`
and objectives fanned four ways are in pgmvox 0.11.0, with tests.

**A cornice reached the floor of the world under the lowest landing.** Every level rose three blocks, and
`pgmvox.brittle.cap` now refuses a cornice that would reach under y 3.

**The original's finish took three reviews to match.** The panel is five wide and framed in black clay down both
sides, the stairs' sides carry the cornice, a bed is ringed twice in sandstone stairs, sand is mixed with
upside-down sandstone stairs, and cacti stand only on pure sand.

## What was not done

- The board was not opened in PGM. The studio's parser reads the map.xml as valid, but no match was played.

## The renders

- `00`: the plan sketches, the first layout and this one.
- `05`: the built world from above with the hills and spawners.
- `10`: a section along red's diagonal.
- `30`–`35`: the board from two corners, red's quadrant, the Keep and its house, the Dais, and an edge.
