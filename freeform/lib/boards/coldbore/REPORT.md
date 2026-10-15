# Coldbore — the report

**A bunker board built to the author's spoken brief: a station in a cliff, a cold plain with roads to it, a
fissure down the middle, three levels, a cave with lava, and one of the core-and-wool concepts.** The concept
is the wool beneath the core, with the leak taken from the side through a well, so the leak opens the vault.

## What came out

**Everything the plan states, the read-back finds in the world.** Both reads come back with no miss: each
spawn reaches its own reactor in 44 moves by the drop and 76 by the stair, the vault is sealed until the
leak, all four approaches reach the reactor, no lava lies inside a core's leak region, every objective
passes its own check, and nothing falls. The studio's parser reads the map.xml as valid with no issue.

**The board is deterministic, and `check.py --boards` holds it to its hash.**

## What the plan missed

**Four things were decided only while building, and each is now a line in the plan.**

- The culvert's mouth first fell inside a flank crevasse, thirteen blocks down a crack instead of on the snow.
  The plan names both now and the crevasse moved west; a plan check of each entrance's ground would have
  caught it.
- The rooms' lining first walled up the gallery's mouth, because the shell was laid on every cell next to a
  room, open air included. It is laid on rock alone now.
- The facade first stood in front of the cliff as a box. The cliff's foot is now a buttress over the
  station's front, and the facade is its face.
- The first spawn put the walk ratio at 2.92. Nine positions were measured and the one at (13, 104, 74)
  meets all three walk bands.

## What a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| a bunker of rooms, corridors and flights on three levels under the ground | the most work on the board: boxes, a lining pass by which way the air lies, a helix stair whose doors follow it | a storey that is a room, not a slab: an air box with its floor, walls and ceiling stated, and a stair between two of them |
| a core whose leak opens a room under it | a trigger of fills on `completed`, a bedrock hatch and door, and the fifteen-block skirt checked by hand | the leak region drawn on the plan, and a door that names the objective that opens it |
| a cave off a room, with ponds that cannot leak a core | `volume.under` tunnels and chambers; ponds sunk flush with rims, kept out of the skirt | caves as a layer, with the leak skirt as a keep-out every lava placement asks |
| the mountain coming forward over the gate | a cliff line with a bay in it | a facade a cliff is told to wrap |
| a fissure as the build zone between the teams | a heightfield profile in ledges, lava under it | a fissure as a landform along a drawn line (`RP132`) |
| snow that melts off near the fissure | a ragged band by distance from the rim | a paint band by distance from a named landform |

**The library took one fix from this board.** `pgmvox.run` registered a new board's world under its path
resolved twice when run from `freeform/lib`, so its row read `freeform/lib/freeform/lib/boards/…`; it now
passes the board's absolute path.
