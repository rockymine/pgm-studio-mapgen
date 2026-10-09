# Claywork — the report

**Claywork is built, and the built world reads back as the plan said it would.** It is a capture-the-wool board for
two teams of sixteen, grounded on bedrock, four flat levels joined by broad steps. The layout is in `PLAN.md`,
which went through four reviews before the build. This is what the build made of it.

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

**A face is layered so the bedrock never shows as one slab.** Under the ground lie two blocks of bedrock, then a
stripe of the team's stained clay set flush, then bedrock patterned with obsidian and black wool to the floor.
The mirror recolours the stripe from red to blue on blue's half.

**The floor is a three-by-three checker, and each level has its own pair.** The front is clay and stone, the hub
stone and clay, the Rostrum and the Walks double slab and stone, the spawn double slab and clay, the Kilns smooth
slab and clay. A stone-brick border runs along every edge over the void, so an edge is seen before it is reached.

**Quartz arrows are set into the floor along every way forward.** They run from the Gatehouse to the Grand Steps,
along each Arcade, and up each Walk to its Kiln.

**Arches of stone brick span both flights of the Grand Steps, each Arcade, and each Walk twice.** Each arch has
a beam and upside-down stair corners, and its legs are what narrow a Walk from twelve to ten.

**The Kilns are clay rooms with brick corners, a double-slab roof lit by glowstone, and a red door frame.** Each
holds its wool on the floor and two chests of gear.

**The Undercroft is carved three high under the Court and the Arcades, lit, and reached by the well.** The well
has a shallow pool at its foot, and a ladder at each end climbs the Walk's face.

## Read back from the world

**Every check on the built world comes out clean.** These are from `renders/walks.txt`.

| Read | Value |
|---|---|
| Objectives with a problem | 0 |
| Wools missing from their rooms | 0 |
| Blocks without footing | 0 |
| Water standing against air | 0 |
| Land or build zone without block 36, block 36 under plain void | 0, 0 |
| Spawn to its own monuments, on foot | 14 and 15 |
| Spawn to an enemy Kiln, on foot | not reached: the band and the wall are built over |
| Spawn to an enemy Kiln, building | 214, both Kilns, both teams |
| Court into the well's floor | 9, a drop of four |
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

**A defender cannot walk into their own Kiln either.** The bedrock wall spans the Walk with both ends on the void,
so it stops everyone. That is the defence wall as the gameplay notes describe it: a line the defence holds from
behind, crossed by building. A defender who wants to stand in the room builds over it as an attacker would.

**The palette is grey.** Clay, stone and double slab are all pale grey blocks, and the checker reads mostly as
texture. The team stripe, the quartz arrows and the red door frames carry what colour there is.

## What was not done

- The Gatehouse is plain walls and iron bars, and the Statue Terraces carry a column, not a sculpted statue.
- No cover was placed on the Forecourt or the Court. The plan fixed where it may go, and the board is
  playable without it.
- The board was not opened in PGM. The map.xml is written by the library and the objectives check against the
  world, but no match was played.

## The renders

- `00`: the plan sketches, v1 to v4.
- `05`: the built world from above with the plan's names.
- `10`–`12`: sections along the West Walk, through the Rostrum, and along the Undercroft.
- `30`–`36`: isometric views of the board, red's half, the Gatehouse and Court, a Kiln and its Walk, the front,
  and the Arcade with its stepping stones.
- `40`: the Undercroft in x-ray.
- `50`: the Forecourt's face as seen from the band.

## What I wanted, how hard it was, and what a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| A grounded board with layered faces | Easy: every column gets ground, bedrock, a stripe and a pattern from one function | A face treatment on a piece: the depth of ground, the stripe, and the pattern below |
| Building only over the board | Easy: block 36 at y 0 and a `not void` filter | Build zones drawn on the plan, and the block and filter written from them |
| A checker that tells the levels apart | Easy: a pair of blocks for each kind of piece | A surface pattern per piece, chosen with the theme |
| Arrows and arches | Moderate: each is placed by hand along its way, and the arches must leave the narrowest at ten | Way-marking pieces that follow a route on the plan |
| A second layer under the hub | Moderate: a storey in the raster for the plan's walk, then carved and walked on the blocks | Storeys on the plan, carved from the piece above them |
| Stepping stones that cross both ways | Hard: the plan's walk passed them, and the voxel walk could not land a jump lower until the library was fixed | Jump checks on the plan that use the same rules as the built world's walk |
| A defence wall nobody walks round | Easy: bedrock across the Walk with its ends on the void | The wall as a seam piece, with its effect on both teams' walks shown on the plan |
