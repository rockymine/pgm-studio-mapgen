# Coldbore — the report

**The second build of a bunker board, made to the author's reading of the first.** The station is spread
across the mountain from the gate in the west buttress to the vault under the spawn room in the east, the
core and the wool are apart, every change of level is a two-leg ramp, and the cliff, the snowfield and the
plateau carry what the author asked for: gullies and strata, rock through the snow, a dish and buildings,
boulders and more lavafalls. A spiral stair inside the mountain is the one way onto the plateau, and the board's
outer edge is ragged.

## What came out

**The read-back finds what the plan states, with two walk bands missed.** Red's spawn reaches its own reactor
in 57 moves with no fall over four blocks, and the core's top is in sight from all four cells of the spawn
room's door. The vault is sealed until the leak, the attacker reaches the reactor through the gate, through the
generator house, down the fallen ceiling and up from the gallery, no lava lies inside a core's leak region,
every objective passes its own check, and nothing falls. The studio's parser reads the map.xml as
valid with no issue.

**The walk to the enemy's reactor is 256 against a band of 85 to 150, and the ratio 4.06 against 3 to 4.**
Both follow from spreading the station: each gate sits on a flank, so an attack crosses the board from one
flank to the other. The plan keeps the miss as a question for the author.

## Where to look in game

| What | Red's at (x, y, z) | Blue's at |
|---|---|---|
| the spawn | (24, 72, 86) | (−25, 72, −87) |
| the spawn room's door, the core in sight | (13, 72, 80 to 83) | (−14, 72, −84 to −81) |
| the core, over its pit | (−4, 62, 69) to (2, 68, 75) | (−3, 62, −76) to (3, 68, −70) |
| the pit's floor, the leak height under the core | y 49, leak at 57 | y 49, leak at 57 |
| the vault's blast door | (25, 44, 76) to (25, 50, 79) | (−26, 44, −80) to (−26, 50, −77) |
| the wool | (40, 44, 84) | (−41, 44, −85) |
| the monument on the balcony | (5, 73, 83) | (−6, 73, −84) |
| the gate | (−43 to −38, 72, 48) | (37 to 42, 72, −49) |
| the generator house's garage door | (31 to 36, 72, 50) | (−37 to −32, 72, −51) |
| the fallen ceiling | (26 to 30, 71, 37 to 41) | (−31 to −27, 71, −42 to −38) |
| the great dish's centre | (5, 111, 78) | (−6, 111, −79) |

## What the plan missed

**Three things were decided only while building, and each is now in the plan or the code.**

- The ramps' legs first met at a corner with a step of a block and a half between them, which a player cannot
  climb. Each ramp now turns on a level landing between its legs.
- The core was first out of sight from the spawn room's door, because the balcony's floor cut the line from the
  door to the core's middle. What a player sees is the core's top, and that is what the read-back now asks.
- The cliff's strata first used grey clay, which renders as a dark brown band across every cliff at one height.
  The beds are now stone, andesite, diorite, cobblestone and pale and blue-grey clay.

**The fallen ceiling is a way in, not a way out.** The rubble under it stands six blocks below the hole's lip,
so an attacker drops onto it and a defender climbs out only with blocks.

## What a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| a station spread through a mountain on three levels | boxes, a lining pass by which way the air lies, two facades the lining leaves alone | a storey that is a room, not a slab: an air box with its floor, walls and ceiling stated |
| ramps that turn halfway | legs in half blocks, a landing between them, a wedge under the solid one | a ramp between two rooms, stated by its legs and its landing |
| a core whose leak opens a vault elsewhere | a trigger of fills on `completed`, a bedrock door, the leak skirt checked by hand | the leak region drawn on the plan, and a door that names the objective that opens it |
| the spawn in sight of the core | a ray from the door to the core's top, through what a player sees past | a sight check between two named points on the plan |
| a cliff of gullies and strata | gullies as grooves in the cliff line, beds by height with a dip | a cliff along a drawn line with gullies stated on it, and strata as a paint band axis |
| a fissure as the build zone between the teams | a heightfield profile in ledges, lava under it | a fissure as a landform along a drawn line (`RP132`) |

## What the library took from this board

**`bed_offset` breaks beds at faults and drapes them over the ground.** A board's beds could only dip and fold, and
at the few blocks every board used they read as level bands down a cliff. A fault is a line with a throw and a
drag either side, and a drape lifts the beds by a share of the ground's smoothed shape; both default to nothing,
so no other board moves.

## The first build

**Kept as it was written, so the two builds can be read side by side.**

The first build put the wool beneath the core, with the leak taken from the side through a well, so the leak
opened the vault. Each spawn reached its own reactor in 44 moves by a drop and 76 by a helix stair, all four
approaches reached the reactor, and the studio's parser read the map.xml as valid.

Four things were decided only while building it: the culvert's mouth first fell inside a flank crevasse; the
rooms' lining first walled up the gallery's mouth; the facade first stood in front of the cliff as a box; and
the first spawn put the walk ratio at 2.92, so nine positions were measured to find one inside all three bands.

**The library took one fix from that board.** `pgmvox.run` registered a new board's world under its path
resolved twice when run from `freeform/lib`, so its row read `freeform/lib/freeform/lib/boards/…`; it now
passes the board's absolute path.
