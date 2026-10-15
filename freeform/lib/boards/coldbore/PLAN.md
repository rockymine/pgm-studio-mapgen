# Coldbore — the plan

## The board in one sentence

**Two drilling stations cut into opposite cliffs on a frozen plain, split by the glowing fissure their shared
bore tore open: each team's reactor burns forward under its forecourt, and the wool lies sealed in the cooling
vault beneath it until the reactor leaks.**

What a player remembers: the gate in the face of the cliff, the reactor hanging over its well, the drop into
the cooling pool once the hatch is gone, and the lava at the bottom of the fissure seen from the gallery.

## What happened here

**The bore was drilled from both stations toward a heat pocket under the plain, and it found more than it was
after.** The ground split along the bore's line, the ash it threw up turned the season to a winter that has
not ended, and the derrick fell into the crack it made. Its stump still stands in the lava in the middle of
the board, and the two stations, built by the same company, now fight over what is left of the heat.

## Mode: one core and one wool a team

**The core is the reactor and the wool is in the vault under it, so the leak is the door.** A core is the
forward objective and a wool the deep one (`WHAT-A-BOARD-IS-MADE-OF.md`), and here deep is literal: the vault
is the level under the reactor. It is concept 8 of the bunker-cores page, the wool beneath the core, with the
leak taken from the side so that no lava ever has to run through the room.

**The leak opens the vault in one trigger.** A breach anywhere on the casing runs the lava over the reactor
hall's floor into the well under the core, whose floor is the leak height (the core's lowest block, y 56, less
five). PGM marks the core leaked, and the trigger fills the core, the spill round it, the well and the bedrock
hatch with air, and opens the vault's blast door. Attackers drop through the empty well into the pool.

**Nothing reaches the wool before the leak.** The hatch and the blast door are bedrock, the vault's shell is a
zone nobody may break, and the room refuses its own team. A player may neither place nor scoop lava, so no
bucket can leak a core from somewhere it should not leak.

## Arrangement

**Red holds the south half and blue the north, and blue's half is red's turned about (−0.5, −0.5).** The board
is 150 by 200. Red's half runs from the fissure at z 0 to its cliff at z 56, a buttress of which comes forward
to z 44 over the station's front, and its plateau runs back to z 99.

| From the middle out | z (red) | top |
|---|---|---|
| the fissure, 24 wide at the surface, narrowing in ledges to the lava | about −12 to 12 | lava at 22 |
| the snowfield: roads, outcrops, crevasses on the flanks, ash along the rim | 12 to 44 | 71, snow over rock |
| the forecourt before the gate, between two blast walls | 34 to 44 | 71, paved |
| the cliff, with the station's facade as the buttress's face | 44 to 56 | rising to 100 |
| the plateau and the station on it | 56 to 99 | 100 to 106, the yard at 103 |

**The station goes 40 blocks into the mountain on level 0 and turns back under the snowfield on levels 1 and
2.** Every room and corridor is a box in `plan.py`, every flight a run of stairs, and the stair core a helix of
24 cells a lap so that each level's door falls where the helix reaches it.

| Level | Feet | Rooms |
|---|---|---|
| 0 | 72 | the vestibule behind the gate, the entrance hall (14 high), the armoury, the link to the stair core, the ramp down into the mountain |
| 1 | 52 | the turn hall at the ramp's foot, the return corridor, the reactor hall (14 high), the barracks, the vent bay, the drop room |
| 2 | 34 | the vault under the reactor, the service corridor, the fissure gallery, and the cave west of it |
| yard | 104 | the spawn's shelter, the monument, the stair core's head house, the drop's mouth, the cutting down the cliff |

**Corridors are four wide and seven high, and halls fourteen.** A hall is fought in, so it is twice a
corridor's height and five or six times its width.

## Four ways to a reactor

**Each reactor has an approach from through, above, below and around, and the read-back walks all four.** An
attacker who has bridged the fissure reaches red's reactor through the gate in 95 moves, down the vent
ladder from the forecourt in 58, up from red's gallery in 39 once the galleries are bridged at depth, and
through the barracks by the culvert from the west flank in 84.

| Approach | From | Into |
|---|---|---|
| through | the gate, the hall, the ramp, the turn hall, the return corridor | the reactor hall's north end |
| above | a hatch on the forecourt's west side, a ladder 20 blocks down | the vent bay, beside the reactor |
| below | the 11-block gap between the two galleries over the lava | the stair from level 2 up to the hall's south end |
| around | a collapsed culvert from the snow on the west flank | the barracks, beside the reactor |

## The numbers

| Measure | Value | Target |
|---|---|---|
| walk from a spawn to its own reactor | 49 | 40 to 90 (`GO4`) |
| walk from a spawn to the enemy's reactor | 149 | 85 to 150 (`GO3`) |
| the reactor's walks, enemy over own | 3.04 | 3 to 4 (`GO1`) |
| the narrowest surface crossing of the fissure | 22 | 16 or more |
| the crossing between the galleries at depth | 11 | 8 or more |
| blocks from a core to the nearest lava under its leak height | 31 | over 15 |
| rock over the shallowest room | 5 | at least 3 |
| the wool before the leak | sealed | sealed |
| the wool carried home from the enemy's vault | 235, 11 of it bridged | reached |

**The leak's fifteen blocks are why the cave is where it is.** PGM counts any lava that appears within fifteen
blocks of a core's footprint and under its leak height, so the cave's ponds stand west of x −20 and south of
z 35, and the fissure's lava is 31 blocks from the nearest core.

## The look, decided before the build

**The biome is Ice Plains, and the three families are snow and rock, the station's nether brick and stone,
and the accent of hazard bands and lava.** The snowfield is snow with packed ice where the wind has scoured it,
rock shows only where the ground is too steep to hold snow, and along the fissure the snow has melted off to
an ash ground of grey and black stained clay with gravel inset. The station's front is nether brick ribbed in
stone brick with the team's band under its parapet, the interior is stone and stone brick, and the vault alone
is white quartz.

## What the build adds that the plan does not show

**Scenery that changes no route.** The outcrops, the crevasses on the flanks, the pylons, the masts, the vent
stacks, the tank, the derrick on the stump and the lavafalls on the fissure's walls are scenery; none stands
on a route the checker walked, and the lavafalls run more than 30 blocks from either core.
