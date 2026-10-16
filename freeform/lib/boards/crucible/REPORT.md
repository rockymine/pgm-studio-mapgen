# Crucible — the report

## The story and the concept

**Two rival foundries are dug into facing volcanoes across a lava rift.** Each smelts with the mountain's heat: its
crucible (the core, lava in obsidian) hangs on chains from a gantry crane over a casting pit sunk into the slag
plain at the cliff's foot, and its dye stock (the wool) is kept in the cold store, the one cool room, at the
bottom of the foundry's ramps under the mountain's back.

**Destroy the Core and Capture the Wool are two separate goals bound by one place.** A team wins by leaking the
enemy's crucible and placing the enemy's wool on its own monument. The crucible is forward, in the open pit; the
wool is deep, 1.5 times further. The pit is the hinge: its floor opens into the furnace hall, one of the two inside
ways to the store, so a raid on the crucible is a step from the wool route and a defender of one is near the other.

**The casing turns to gold at 15 minutes and to glass at 20**, so a held crucible still ends.

## The layout and the modes

**One island, 140 by 200, turned half round.** From the middle: a lava rift 17 to 23 wide (the whole of it a build
zone, lava at y 6, the kill height at 18), the slag plain from y 45 to 50, and the mountain from a two-tier cliff
at z 58 to a crest near y 95. The foundry has three levels joined by two-leg ramps at one in two (`PLAN.md` §3).

| What | Red's at (x, y, z) | Blue's at |
|---|---|---|
| the spawn (crew hall) | (3, 52, 77) | (−4, 52, −78) |
| the crucible's casing | (20, 46, 43) to (24, 50, 47) | (−25, 46, −48) to (−21, 50, −44) |
| the pit's floor, where its lava lands | top y 39, lava at 40 = the leak line | same |
| the gantry's deck | x 2..46, y 55, z 44..46 | x −47..−3, y 55, z −47..−45 |
| the loggia over the pit | (14..30, 52, 58..61) | (−31..−15, 52, −62..−59) |
| the monument, on the pour room's desk | (21, 53, 67) | (−22, 53, −68) |
| the wool, on the cold store's plinth | (−39, 29, 88) | (38, 29, −89) |
| the cold store | (−46..−32, 28, 84..92) | (31..45, 28, −93..−85) |
| the loading gate | (−33..−28, 52, 58) | (27..32, 52, −59) |
| the sinkhole (the lava tube's mouth) | (−6, 42, 30) | (5, 42, −31) |
| the flank cave's mouth | (−60, 51, 45) | (59, 51, −46) |
| the tip's deck over the rift | (−15..−10, 46, 5..10) | (9..14, 46, −11..−6) |
| the cinder cone's vent | (47, 59, 38) | (−48, 59, −39) |

## How each objective is approached

**The crucible has four ways in, from four directions.** Walked on the built world from red's rim once the rift is
bridged: around, the haul ramp spiralling down the pit's west wall, 36 moves; below, the lava tube from the
sinkhole to the pit floor, 46; above, up the cinder cone onto the gantry and along the girder over the casing, 54;
through, the loading gate, slag run and furnace hall, 99, or the loggia's open end and the furnace ramp, 93.

**The defenders hold the loggia over the pit and the furnace hall behind it.** Red's spawn reaches the floor round
its own crucible in 49 moves on foot, 35 if it drops from the loggia, and the crucible's top is in sight from the
loggia.

**The wool has three ways in.** The loading gate, loading ramp, slag run and deep ramp (132 from the rim); the pit,
the furnace hall and the deep ramp (108); and the flank cave from the west spur's face down through the beds to
the store's west door (77). The store's shell is blast-proof, so those are the ways in.

**The carry home** is 98 moves to red's rim and 93 from blue's rim to blue's monument, with the rift (about 19)
bridged between.

## The palette

**Ground is warm and dark, built is pale, accent is lava and one cold room.** The plain is ash in grey stained clay
(dark brown in the game's textures) with black and brown clay patches; the cone is scoria (netherrack, brown clay);
the black flow is black clay and coal.

**Every cliff and cut shows the same beds**: slate (cyan clay), basalt, tuff, grey andesite and a thin red bed of
netherrack and hardened clay, in long lenses that dip and rise with the land.

**The foundry is stone brick and polished andesite** with smooth double-slab pilasters stepped out, nether brick
panels sunk a block, an orange band sunk under each cornice, and iron for machines. The cold store alone is quartz,
prismarine and sea lanterns.

## What was checked, and the numbers

**The plan check** (`renders/plan-check.txt`, octile walks over the plan): own walk 53 (GO4 40–90, ok), enemy walk
148 (GO3 85–150, ok), ratio 2.79 (GO1 3–4, **missed**), crucible 34° off the spawn line, monument 24 from the
spawn, wool 222 from blue's spawn, every approach reached, the leak landing on its line, the nearest land lava 38
from the crucible, rock over every room 2 or more, the rift 17 at its narrowest, every ramp leg 1 in 2.

**The read-back** (`renders/walks.txt`, the built world): every place the plan names is reached from red's spawn
with no fall over four; every approach reaches its objective; no lava within 15 of a crucible at or under its leak
line; 0 objectives with a problem; 0 blocks that would fall. The four still lava blocks beside air are the sources
in the notches feeding the lavafalls, by design.

**The studio's parser reads the map.xml as valid** with no issue: 2 cores, 2 wools, 2 spawners, 2 modes, 11 apply
rules.

**The textured renders were looked at and acted on.** The first ash was a camouflage of black, brown and coal and
was calmed to one main tone with patches. The rock beds were blotches and became long lenses. The mountain top
showed pale strata wherever its noise turned steep and now shows ash and rubble. A red bed of red stained clay was
recoloured blue on blue's half by the team recolour and is now hardened clay.

## What did not work, or was decided while building

- **GO1 cannot be met with GO3 on a board this long with spawns in the mountain**: keeping the enemy's walk at or
  under 150 leaves the owner's at 53. The spawn was moved five blocks forward to bring GO3 inside its band.
- **The flank cave first carved through the cold store's wall, and its floor painter repaved the store**; it now
  ends at a doorway (`store west door`) and paints only outside the foundry's spaces.
- **The furnace ramp's lower leg runs open along the furnace hall**, so it carries a parapet a block high where it
  stands two or more over the hall's floor; the plan did not say how a ramp meets a hall it runs beside.
- **The black flow's channel steps down with the lobe**, and still lava at a step had air beside it; the step now
  carries flowing lava. The lava sea met the void at the board's edge and is walled in obsidian there.
- **The pit reads small in a top view** against the plain; its floor is 17 across inside the haul ramp and bench.
- **`pgmvox.run` wrote this board's index row as `freeform/lib/freeform/lib/boards/crucible`**, the doubled path;
  the row in `maps/INDEX.md` was corrected by hand.
- **No pgmvox change was needed.** The board writes its own `Modes` part in `mapxml.py`, since `play.rules` has no
  `<modes>` element.

## What a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| a core hung from a crane, not floating | a girder, a trolley and two chains placed by hand over the casing | a core preset "hung" that stamps its own support to an overhead |
| a mode ladder on the core | a hand-written `<modes>` part | `Map(modes=...)` in `play.rules`, as the studio writes its default ladder |
| a spiral haul ramp down a pit | the pit as a polar height function, the ramp an arc of linear height | a pit landform with a ramp stated by its start, end and width |
| rooms with pilasters, sunk panels and bands | a lining pass per box room by wall, rhythm and course | a room style on a box: pilaster period, panel, band, floor set |
| ramps that turn on landings beside a hall | legs and landings by hand, a parapet where one runs open | a ramp stated between two rooms, its open side railed |
| strata that read as beds, not noise | a 3-D noise stretched across the beds | the paint's layered stack with a lens length per bed |
| GO1 against a board's size | measured, missed and explained | the walk bands scaled by the board's spawn-to-spawn walk |
