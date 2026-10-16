# Coldbore — the plan

## The board in one sentence

**Two drilling stations cut into opposite cliffs on a frozen plain, split by the glowing fissure their shared
bore tore open: each team's reactor hangs over a pit in a tall hall in the middle of its mountain, and its wool
lies sealed in a quartz vault deep in the mountain's other flank until the reactor leaks.**

What a player remembers: the gate in the west buttress, the core seen from the spawn room's door across the
hall, the long ramps that turn on a landing halfway, the dish on the plateau, and the lava in the fissure seen
from the gallery.

## What happened here

**The bore was drilled from both stations toward a heat pocket under the plain, and it found more than it was
after.** The ground split along the bore's line, the ash it threw up turned the season to a winter that has
not ended, and the derrick fell into the crack it made. Its stump still stands in the lava in the middle of
the board, and the two stations, built by the same company, now fight over what is left of the heat.

## Mode: one core and one wool a team, apart

**The core is the reactor and the wool is in the vault, and the leak is the vault's key.** A core is the
forward objective and a wool the deep one (`WHAT-A-BOARD-IS-MADE-OF.md`). The reactor hangs in the middle of
the mountain; the vault lies 24 blocks east of it, two levels down and under the spawn room, so the two are
fought for in different places and neither stands over the other.

**The leak opens the vault in one trigger.** The core hangs over a pit whose floor is eight blocks under the
hall's, so lava let out of a broken casing falls straight into it, under the leak height (the core's lowest
block, y 62, less five). PGM marks the core leaked, and the trigger fills the core, its cradle and the pit
with air and opens the vault's bedrock blast door.

**Nothing reaches the wool before the leak.** The blast door is bedrock, the vault's shell is a zone nobody may
break, and the room refuses its own team. A player may neither place nor scoop lava, so no bucket can leak a
core from somewhere it should not.

## Arrangement

**Red holds the south half and blue the north, and blue's half is red's turned about (−0.5, −0.5).** The board
is 150 by 200. Red's half runs from the fissure at z 0 to its cliff at z 56, and its plateau runs back to z 99.
The cliff comes forward in two buttresses, a wide one at x −40 for the gate and a narrower one at x 34 for the
generator house, and six gullies cut back into it between them.

| From the middle out | z (red) | top |
|---|---|---|
| the fissure, 24 wide at the surface, narrowing in ledges to the lava | about −12 to 12 | lava at 22 |
| the snowfield: roads, rock through the snow on the west, a crevasse on the west flank, ash along the rim | 12 to 38 | 71, snow over rock |
| the gate's court and the generator house's court | 38 to 49 | 71, paved |
| the cliff, with the two facades as its buttresses' faces | 48 to 60 | rising to 100 |
| the east flank, raised into a hill that climbs to the plateau | x 40 to 74 | 71 rising to 88 |
| the plateau: the yard, the dish, the buildings, boulders in the snow | 60 to 99 | 100 to 108, the yard at 103 |

**The station fills the mountain from the gate on the west to the vault on the east.** Every room and corridor
is a box in `plan.py`, every ramp a run of legs, every deck a floor built inside the hall.

| Level | Feet | Rooms |
|---|---|---|
| 0 | 72 | the gate's vestibule and the entrance hall (14 high), the armoury, the west corridor, the hall's balcony and gantry, the spawn room and the iron room beside it, the generator house and its corridor |
| 1 | 58 | the reactor hall's floor (22 high to its ceiling), the south corridor under the snowfield, the store whose ceiling fell in |
| 2 | 44 | the fissure gallery and the cave west of it, the service corridor, the vault |

**A spiral stair climbs from the generator house's corridor to the yard on the plateau.** It turns two laps round a
solid core lit every six blocks, a block up a step with four blocks of headroom under the lap above, and comes
out through a head house on the yard. It is the only way onto the plateau: nothing climbs the cliff outside.

**Corridors are four wide and seven high, halls fourteen or more.** A hall is fought in, so it is twice a
corridor's height and five or six times its width.

## The ramps

**Every change of level is a ramp of two legs about one in two, turning on a level landing between them.** The
hall's ramp stands as a wedge of stone brick against the hall's west and south walls: down from the balcony
along the west wall, a landing in the corner, then along the south wall to the floor. The ramp to the gallery
is a tunnel: west from the foot of the south corridor, a landing, then south to the gallery's door. Each step is
half a block, a slab or a full block, so nothing on a ramp needs a jump.

## The spawn, in sight of the core

**The spawn room's door opens onto the balcony, and the core is in sight from every cell of it.** A player
leaving the spawn turns once to the door and sees the reactor across the hall. The iron room beside the spawn
has iron blocks set in its walls that grow back once mined, with crafting tables and an anvil to make armour.

## Four ways to a reactor

**Each reactor has an approach from through, above, below and around, and the read-back walks all four.**

| Approach | From | Into |
|---|---|---|
| through the gate | the west court, the vestibule, the entrance hall, the west corridor | the balcony, then the hall's ramp |
| through the generator house | the garage door on the east court, the link and the corridor | the gantry over the hall |
| above | the store's fallen ceiling in the snowfield, a drop onto the rubble | the south corridor and the hall's south door |
| below | the gap between the two galleries over the lava, bridged | the ramp up to the south corridor |

## The numbers

| Measure | Value | Target |
|---|---|---|
| walk from a spawn to its own reactor | 63 on the plan, 57 in the world | 40 to 90 (`GO4`) |
| walk from a spawn to the enemy's reactor | 256 | 85 to 150 (`GO3`): missed |
| the reactor's walks, enemy over own | 4.06 | 3 to 4 (`GO1`): missed |
| cells of the spawn room's door the core is in sight from | 4 of 4 | at least one |
| the narrowest surface crossing of the fissure | 22 | 16 or more |
| the crossing between the galleries at depth | 20 | 8 or more |
| blocks from a core to the nearest lava under its leak height | 40 | over 15 |
| rock over the shallowest room | 3 | at least 3 |
| the wool before the leak | sealed | sealed |
| the wool carried home from the enemy's vault | 258, 20 of it bridged | reached |

**The walk to the enemy's reactor is long because the station is spread.** An attacker leaves through a gate
at the side of the mountain, crosses the plain and the fissure, and enters the other station at its side; the
half turn puts blue's gate on the east flank, so the walk crosses the board from one flank to the other. It is a miss against the band, kept because the spread is what the
second plan was asked for, and it is a question for the author rather than a fault to fix by moving the gates.

**The leak's fifteen blocks are why the cave is where it is.** PGM counts any lava that appears within fifteen
blocks of a core's footprint and under its leak height, so the cave's ponds lie west of x −25 and the
fissure's lava is 40 blocks from the nearest core.

## The look, decided before the build

**The biome is Ice Plains, and the three families are snow and rock, the station's two fronts, and the accent
of hazard bands and lava.** The snowfield is snow with packed ice where the wind has scoured it, and rock breaks
through it in faceted clusters on the plateau and the west front.

**Rock shows wherever the ground is too steep to hold snow, laid in beds that tilt, bend and break.** The beds
are stone, andesite and polished andesite, with cobblestone, blue-grey clay, white mushroom stem and grey acacia
bark between them, two to six blocks thick. They rise a block in ten to the east, fold six blocks over thirty,
step at three faults that run up the gullies, and arch under the mountain by a third of its rise, so they sag
toward the fissure.

**The gullies and the fissure's rim carry their own ground.** In the gullies the runoff has frozen down the face as
ice, and along the fissure the snow has melted to an ash ground of grey and black clay with gravel.

**Everything the station shows above ground is in one dark style.** Its parapets are nether brick and
upside-down nether-brick slabs by turns, one solid line, and its walls nether brick ribbed in stone brick under a
course of stone brick and the team's band. The yard the dish stands on, the head house over the spiral stair, the
operations block and the vent stacks are built this way, so each stands apart from the grey cliff. Inside, the
station is stone and stone brick, and the vault alone is white quartz.

**Both entrance fronts are brought two blocks out from the cliff, in layers.** A plinth of polished andesite, the
stone-brick pilasters with chiseled bases and capitals, and the cornice stand two blocks out; the nether-brick
panels between the pilasters, with the team's band across them, stand one block out. Each door sits in a recess
two deep between chiseled jambs under a polished-andesite lintel, its hazard frame at the recess's back. The gate
has slits of bars under its cornice, the generator house a band of windows and two exhausts up its face.

## The rooms inside

**Every room is dressed with depth, and each in a style of its own.** A wall has a skirting of polished andesite,
pilasters with chiseled bases and capitals every four or five blocks, panels set back a block between them, and a
frieze under the ceiling; a door is framed by jambs and a lintel. From each pilaster a beam of cobblestone wall
crosses the ceiling, so a room is gridded and a corridor ribbed, and the floors are two-block tiles inside a
border. The reactor hall keeps its own dressing of cradle, columns, decks and coolant lines.

| Room | Its panels | Its frieze |
|---|---|---|
| the entrance hall | nether brick, the fronts' dark brought inside | the team's band, set back |
| the gate's vestibule | andesite | the team's band, set back |
| the armoury | spruce planks | a spruce beam |
| the spawn room | polished andesite on stone-brick faces | the team's band, set back |
| the iron room | cobblestone, a workshop | cracked stone brick |
| the generator house | polished andesite, a pipe standing in each | iron |
| the service corridors | none | the hazard band, set back |
| the vault | polished diorite between quartz pilasters, a sea lantern in every other | chiseled quartz, with beams of quartz pillar |

## What the build adds that the plan does not show

**Scenery that changes no route.** The plateau carries the great dish tilted at the southern sky, its feed held
on three struts of iron with a light on its tip and a small satellite hung over the yard on its axis, the
operations block with the signal tower on its roof, the two vent stacks side by side on the yard's east edge, and
boulders cut from the cliff's own beds lying in the snow.

**The snowfield and the fissure carry the rest.** The snowfield has more boulders, two lattice towers on the hill
and one blown over, the broken road bridge and the derrick on the stump, and ten lavafalls run down red's
wall of the fissure, all more than 40 blocks from either core.

**The signal towers follow the author's own on Long Distance.** Each is one block thick: three of the team's clay,
a collar of slabs round an iron hub, two chiseled quartz, repeated, with buttons, a trapdoor and stub antennas of
bars on its faces, and a crown of cobble walls carrying two redstone torches under a whip of bars and fence.

## What changed from the first plan, and why

**The second plan answers the author's reading of the first build.** Each change below is the author's point
and what the plan now does about it.

| The author said | What the plan does now |
|---|---|
| the mountain offers more space; everything was in its centre | the station runs from the armoury at x −62 to the vault at x 44 |
| the entrance should sit to one side, with a second building in the wall | the gate is in a buttress at x −40, the generator house in a second at x 34 |
| the wall reads uniform | six gullies cut it, with talus at their feet and ice down their faces, and the rock is laid in strata |
| the small walls at the board's sides do not fit | they are gone; the east flank rises into a hill instead |
| the core stacked over the vault makes play too vertical | the core is in the middle of the mountain, the vault 24 blocks east and two levels down |
| stairs bridging sixteen blocks | ramps of two legs at one in two, turning on a landing |
| the rock surfacing through the snow was missing | faceted rock breaks through on the plateau and the west front |
| the station on top could be more interesting | a dish, a control house, a radome, a fallen shed, stacks and masts |
| some trees could have survived | four clumps of spruce, taken out again after the second build |
| more lavafalls in the rift | ten on each wall, up from three |
| the spawn within two corners of sight of the core | the spawn room's door opens onto the hall, one corner from the spawn |
| an iron room next to spawn | iron blocks in its walls, regrowing, with benches |
| a secondary entrance where a ceiling fell | the store under the snowfield, its ceiling fallen in front of the generator house |

**The drop, the helix stair, the vent ladder and the culvert are gone.** Each was a way between levels or into
the station that the ramps and the fallen ceiling now make, and a drop of twenty blocks or a ladder twenty high
is the vertical play the author asked away from.

## What changed after the second build, and why

**The author's reading of the second build took four things out and asked for three.** None of it moves a room or
a route between the spawns, and the walk bands were left where they fell: they are for the author to judge in
game, not a number to build toward.

| The author said | What the plan does now |
|---|---|
| the spruces do not fit the place | gone; boulders cut from the cliff's own beds lie in the snow where they stood |
| the stair cut into the hill breaks the landscape and is a long way round | gone; a spiral stair inside the mountain climbs from level 0 to the yard |
| some of the towers float | the pylons and masts stand on the flattest ground near where they were, each leg on a footing; every lattice is joined face to face, and a sweep of the world finds nothing loose but the monuments' glass |
| the board's edge should not be a ruled rectangle | its three outer sides are bitten in by up to five blocks, raggedly, and its back corners are chipped away; across the fissure the edge stays whole, so the lava keeps to the world's edge |

## What changed after the third build, and why

**The author's reading of the third build asked for detail where the board was plain.**

| The author said | What the plan does now |
|---|---|
| the towers want the detail of the signal towers on Long Distance | signal towers built on that pattern, in the team's clay |
| the dish wants the touches of the one on Oumuamua | its feed carries a fence and a redstone torch, and a small satellite hangs over the yard on its axis |
| the round spawn with its cupola on Oumuamua | the radome is a round observatory: a quartz drum, a nether-brick roof ring, a cyan dome with a slit |
| the rock is band on band, dull | the beds tilt, fold, break at three faults and arch under the mountain, through a fault and drape added to `bed_offset` |

## What changed after the fourth build, and why

**The author's reading of the textured renders asked for one style above ground and a quieter cliff.**

| The author said | What the plan does now |
|---|---|
| the rock is noisy, and the pale clay reads pink | the pale clay is gone; white mushroom stem and grey acacia bark take its place, in thicker beds |
| signal towers everywhere is too many | two stand by the dish; the hill keeps the lattice towers |
| both entrances should be dark | the generator house's front is the gate's nether brick, stone-brick ribs, band and parapet |
| the round building was only a pointer to the dish | the observatory is gone |
| the house and the dish's platform do not fit the bunker | the yard is walled, the head house and the operations block built, in the gate's dark style; the shed and the tanks are gone |

## What changed after the fifth build, and why

**The author asked for solid lines and depth where the station had thin ones and flat ones.**

| The author said | What the plan does now |
|---|---|
| the fences in the dish are noise | its struts are iron blocks, each touching the last face to face |
| the slab-and-fence parapet does not connect | every parapet is nether brick and upside-down nether-brick slabs by turns |
| snow on the roofs does not look good, and one signal tower is enough | the roofs are bare nether brick, and one tower stands on the operations block |
| the chimneys are scattered | the two vent stacks stand side by side on the yard's east edge |
| the entrances want depth | both fronts are brought out in layers, the doors recessed with their hazard frames at the back |

## What changed after the sixth build, and why

**The author found the inside plain beside the outside.** Every room is now dressed as the table under *The rooms
inside* says, the floors are tiled in twos instead of threes, and the yellow-and-black band that ran round every
wall is gone, kept only as an inset frieze in the service corridors.

## The first plan

**Kept as it was built, so the two versions can be read side by side.**

### The board in one sentence

**Two drilling stations cut into opposite cliffs on a frozen plain, split by the glowing fissure their shared
bore tore open: each team's reactor burns forward under its forecourt, and the wool lies sealed in the cooling
vault beneath it until the reactor leaks.**

### Mode: one core and one wool a team

**The core is the reactor and the wool is in the vault under it, so the leak is the door.** The vault is the
level under the reactor: concept 8 of the bunker-cores page, the wool beneath the core, with the leak taken from
the side so that no lava ever has to run through the room. A breach runs the lava over the reactor hall's floor
into a well under the core, and the trigger opens the well, a bedrock hatch over the vault's pool and the
vault's blast door; attackers drop through the empty well into the pool.

### Arrangement

**The station went 40 blocks into the mountain on level 0 and turned back under the snowfield on levels 1 and
2.** The gate stood in the middle of red's cliff at x 0 between two blast walls, and a helix stair core of 24
cells a lap joined the levels and the yard on the plateau, where the spawn's shelter stood.

| Level | Feet | Rooms |
|---|---|---|
| 0 | 72 | the vestibule behind the gate, the entrance hall (14 high), the armoury, the link to the stair core, the ramp down into the mountain |
| 1 | 52 | the turn hall at the ramp's foot, the return corridor, the reactor hall (14 high), the barracks, the vent bay, the drop room |
| 2 | 34 | the vault under the reactor, the service corridor, the fissure gallery, and the cave west of it |
| yard | 104 | the spawn's shelter, the monument, the stair core's head house, the drop's mouth, the cutting down the cliff |

### Four ways to a reactor

| Approach | From | Into |
|---|---|---|
| through | the gate, the hall, the ramp, the turn hall, the return corridor | the reactor hall's north end |
| above | a hatch on the forecourt's west side, a ladder 20 blocks down | the vent bay, beside the reactor |
| below | the 11-block gap between the two galleries over the lava | the stair from level 2 up to the hall's south end |
| around | a collapsed culvert from the snow on the west flank | the barracks, beside the reactor |

### The numbers

| Measure | Value | Target |
|---|---|---|
| walk from a spawn to its own reactor | 49 | 40 to 90 (`GO4`) |
| walk from a spawn to the enemy's reactor | 149 | 85 to 150 (`GO3`) |
| the reactor's walks, enemy over own | 3.04 | 3 to 4 (`GO1`) |
| the narrowest surface crossing of the fissure | 22 | 16 or more |
| the crossing between the galleries at depth | 11 | 8 or more |
| blocks from a core to the nearest lava under its leak height | 31 | over 15 |
| the wool before the leak | sealed | sealed |
| the wool carried home from the enemy's vault | 235, 11 of it bridged | reached |
