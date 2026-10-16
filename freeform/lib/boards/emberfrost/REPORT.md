# Emberfrost - report

Board: `freeform/lib/boards/emberfrost`, world `maps/dtcm/emberfrost`. Built with pgmvox, 2,029 lines of board scripts, a build of about four
seconds, and the whole pipeline (plan check, build, write, map.xml, flat and textured renders, walk) in about ninety.

## Concept and how it reads the theme

**Fire and ice are two lanes of one island, and autumn is what stands between them.** A frozen lane in the west (glacier, spruce, a frozen
lake, ice caves, quartz columns) and a burning lane in the east (a caldera, nether brick, lava moats and tubes, banded clay cliffs) meet at a
gorge, the Thaw, where meltwater runs in the west half and lava in the east, with a bar of obsidian between them under the central bridge.
Autumn is the colour of the ground where they meet: gold grass, podzol, acacia-plank houses under red sandstone roofs, an orchard whose oaks have
orange, yellow and brown clay worked into their crowns, and snow dusted on the orange crowns where the cold lane begins. A player's walk from
spawn runs ice, autumn, fire, and every core is itself a fire in ice or a fire in fire: lava inside obsidian, standing in snow on one lane and in
a moat of lava on the other.

## Modes and the objectives

**Destroy the Core, two cores a team, one a lane.** Red's Rime Core stands on the west lane in an open ring of columns on a terrace of 72, and
its Forge Core on the east lane on a plinth of 66 inside a lava moat in a caldera. Blue's are their mirror images. A core is a five-cube of
obsidian round three cubes of lava, floating three over a solid floor, exposed in the open: not one block stands over the floor within four blocks of its footprint (read back from the world).
Each core is approached four ways that differ.

| | Rime Core (ice) | Forge Core (fire) |
|---|---|---|
| Around, on the level | across the open terrace from the Frost Gate; spruce stands round it | across two bridges over the moat from the west and south gaps |
| From above | the glacier's plateau at 85 with the Aerie, a ledge to bridge down from | the caldera's rim at 77 |
| From below | the Blue Cave: a mouth on the Mirror's shore, a hall, an undercroft whose roof is the plaza's floor | the Slag Run: a lava tube down from the south slope to a hall under the plinth, with lava pools sunk in its floor |
| Water or a drop | the Mirror, a frozen lake whose ice is a road | the lava moat; from the north and east it has to be bridged |
| What to hold | Pinewatch lodge, the colonnade, the glacier's cover | the Foundry and the Armoury inside the rim, the chimneys |

The middle is Amberford and Beacon Hill: four houses, a chapel and a mill barn in a village, an orchard in rows, an avenue of maples on the Drove Road, a hill
with a fire on its crown. The seam between the teams is the Thaw, crossed by Frostspan, the Cinder Span and Brimstone Bridge, with a lower
route along the banks and over the bar under the Cinder Span's pierced pier, and two scree ways down the walls.

## Layout and proportions

A single island in the void, 144 by 192, mirrored across z = -0.5; land is 79% of the box. Red's spawn at (0, 68, -76) in the Hearth yard at the
back, the lodge behind it and a ridge of 14 behind that. The land is deeper than it is wide, with a waist at the gorge and void bays in the back
corners and the flanks.

- Walk from a spawn to its own cores: 55 and 52 blocks (plan 39 and 40). To the enemy's: 154 and 171 (plan 138 and 146).
- The island rises from 64 in the middle to 77 at the caldera's rim, 90 on the glacier and 106 on its highest spire; the gorge floor is 43.
- Every core is reached on foot from either spawn, and 22,538 places are reached from a spawn on foot (31,286 with every running jump).
- The build height is 118, the kill height 4, and the island's underside bottoms out at 9.

## Palette

| Role | West, ice | Middle, autumn | East, fire |
|---|---|---|---|
| Ground | snow, packed ice, andesite | grass, podzol, coarse dirt, a little gravel | netherrack, brown and orange clay, red sandstone, soul sand |
| Rock in beds | packed ice, andesite, stone, snow | stone, sandstone, brown clay, hardened clay | brown, orange and hardened clay, red sandstone, netherrack |
| Built | stone brick, quartz, prismarine, spruce, sea lanterns | spruce, acacia planks, red sandstone roofs, brick, glowstone | nether brick, black clay, stone brick, glowstone |
| Trees | spruce, snow on every crown | oak, orange, yellow and brown clay worked into the crown | dead oaks |

The biome is Savanna, whose gold grass and foliage carry the middle; roads are granite with brick strips in the warm lanes and andesite with
gravel in the cold one.

## What was checked

- **The studio's parser** reads `maps/dtcm/emberfrost/map.xml` as valid: four cores, two spawns, two teams of twenty-four, no issues.
- **`walk.py`**: `Objectives.check` clean, `audit.footing` 0 problems, `audit.loose_water` 0, every core reached from both spawns, both caves, the
  three spans, the bar, the banks and the lake shore reached on foot from the red spawn (results in `renders/walks.txt`).
- **`plan_check.py`**: the walk over the planned ground against its targets, before any block was built (`renders/plan-check.txt`).
- **Renders**: pgmvox's flat colour (`30` to `33`, three sections `10` to `12` and the annotated top-down `05`), and eighteen textured pictures
  from the studio's renderer (`t01` to `t18`), looked at one by one.

## What did not work

- **The first outline was a blob.** The first island was a rounded block at 80% land with a pad as big as a plaza under each core; the pads
  became ring terraces, the corners were cut into bays, and the land fraction is still 79%. A map that uses void is meant to have less ground
  and this one is mostly ground with its void on the edge.
- **The gorge opened into the void.** The first waist was narrower than the gorge, so its water and lava stood against air. The waist was
  widened and liquids now stay 2.5 blocks from the edge (`audit.loose_water` went from 14 to 0).
- **The Slag Run ran under the moat.** The tube's ceiling was cut by the moat's bed and left a one-block passage; the tube now dives to 54
  before it reaches the moat's radius.
- **Trees would not fit.** The library's oaks reach eleven to fifteen blocks and refuse to plant across a house's posts or another trunk, so a
  hamlet has room for few. The orchard is small oaks in rows, a few great maples and an avenue of two; the first scatter planted four.
  `trees.scatter` takes no ground that gives way, so `wood.py` carries its own.
- **Snow hid the plaza.** The first frost pass covered the Rime plaza's pattern; it now stops ten blocks from the core.
- **Nothing was run on a server.** The lava and the water are held by solid banks a block under their rims, which is what keeps them still; a
  PGM match was not played on it, and the leak of a core into the pit under it, which is solid here by design, was not tried.
- **The ratios on the built world run long.** The walks to the enemy's cores are 154 and 171 against the target of 85 to 150, because the roads
  wind and the gorge is crossed by a span; the plan's own walk is 138 and 146.
- **Gameplay is read from walks and pictures only.** Whether the four approaches to each core balance against one another is a judgement made
  from the geometry.

## What the plan missed

| Decided while building | What in the plan would have decided it |
|---|---|
| Houses stood on slopes, so a pad under each was added to the ground | each house's footprint and level stated in the plan |
| Trees colliding with houses | a tree claim map stated beside the road and building claims |
| The Slag Run's depth against the moat | the tube's floor heights as numbers with a clearance target under the moat |
| The gorge's liquid against the island's edge | a distance-from-edge target for every liquid |

## What I wanted, how hard it was, and what a studio feature would need

| What I wanted | How hard it was | What a studio feature would need to do it |
|---|---|---|
| Rings of one tone round a core, the plinth patterned by distance | easy: a disc, a Chebyshev ring and a pick table | a floor-field instrument that takes a centre and a ring list |
| A tree species with its crown turned autumn (clay worked among the leaves) | easy once a tree was a value; `dataclasses.replace` on its blocks | a theme stating a crown's recolour on a tree kind, not a hand-built variant |
| A tunnel that opens in a hillside and ends under a floor | medium: the carve refuses to come within `cover` of the surface, so the mouth needed `ground=None` and a hand-checked clearance under the moat | `volume.under.tunnel` taking a mouth that is allowed to break the surface, and a read of the clearance under it |
| Trees that know the buildings, the roads and the objectives' ground | hard: every pass kept its own claims and the scatter refuses whole on a log | one claims layer in the library, which `trees.scatter` reads and `built.build.house` and `routes` write |
| Mirror symmetry for a board of two pure lanes | easy: `Symmetry("mirror_z")` and `turn_world` | none |
| Lava and water held still beside a void | medium: the edge test was a read after the build | `fill_water` refusing to place a liquid within a distance of the land's edge |
| Snow laid on whatever stands in the cold | medium: a pass over every column with a frostable list | a weather instrument in the library: a layer on tops by exposure |
