# Emberfrost - plan

## 1. The identity

**Emberfrost is a Destroy the Core board where one gorge divides a frozen lane from a burning one, and every player's walk from spawn runs
ice, autumn, fire.** A glacier with a frozen lake and an ice cave lies in the west; a caldera with a lava moat and a lava tube lies in the east;
the orchard hamlet of Amberford, the colour of October, lies between them. Where water and lava meet in the Thaw, a bar of obsidian stands
under the central bridge.

## 2. The arrangement

One island held in the void, 144 by 192, mirrored across z = -0.5. Red is the north half, blue its image. The island is a rounded slab with a
waist where the gorge crosses it and void bays bitten into the back corners and the flanks.

- **Spawn.** Hearth yard, a level yard at y 66 at the back (z -76), under a ridge of 14 and in front of a lodge, a woodshed and a stable.
- **West, the ice lane.** The Glacier (a mass to y 90 with five spires to 106), the Rime terrace at 72 on its shoulder carrying the **Rime
  Core**, the Mirror (a frozen lake, ice at 62) below it, the Blue Cave under the terrace, Pinewatch lodge, the Aerie on the plateau above.
- **East, the fire lane.** The Caldera (rock to 77 round a floor at 66, open in a west gap and a south gap) carrying the **Forge Core** on a
  plinth inside a lava moat, the Slag Run under it, the Foundry and the Armoury, the Organ (basalt columns) and a burnt cottage by the
  Brimstone Way.
- **Middle.** Amberford, an orchard hamlet on rolling ground at 64, the Drove Road through it, Beacon Hill at 73 over it.
- **The Thaw.** A gorge 21 deep (floor 43, banks 47, rim 64) across the waist: water in the west half, lava in the east, a bar of obsidian at
  the middle. Three spans cross it: Frostspan (x -41, over the water), the Cinder Span (x 0, over the bar, its pier pierced so the bar runs
  through) and Brimstone Bridge (x 40, over the lava). Two scree ways (x -22 and x 23) let a player down to the banks.

Each team keeps two cores, one a lane: a team defends one ice lane core and one fire lane core and attacks the other team's two. Red's Rime Core is
on the west lane north of the gorge and blue's on the same lane south of it; the lanes are pure, west ice and east fire, for both teams.

## 3. The numbers

| Measurement | Target | Plan (checked in `renders/plan-check.txt`) | Built (checked in `renders/walks.txt`) |
|---|---|---|---|
| Board | at most 150 by 200 | 144 by 192 | same |
| Players | at most 24 a team | 24 | 24 |
| Walk, a spawn to its own cores | 40 to 90 | 39 and 40 | 55 and 52 |
| Walk, a spawn to the enemy's cores | 85 to 150 | 138 and 146 | 154 and 171 |
| A core's walk to the enemy spawn / to its own | 3 to 4 | 3.7 and 3.8 | not measured on the built world |
| Gorge crossings | three spans, two ramps | 3, 2 | all reached from spawn |
| A core floats over its floor | 3 | 3 | checked by `Objectives.check`: clean |
| Ground within four blocks of a core | no tree, building or boulder | none | none within four blocks of either footprint (read back); the Rime colonnade stands 9 out |
| Every walkable cell reached from a spawn | all | 21234 of 21960 | 22538 places |

## 4. The places

Each place has a reason to be there and a way in.

| Place | What it is | Why a player goes there | How |
|---|---|---|---|
| Hearth yard | the spawn | where the team starts; two roads leave it east and west and one runs south | its own protected box |
| Rime Keep | the ice core on a terrace of 72, an open ring of columns round a floating obsidian cube | the objective | Frost Road from the north-east, Frost Way from the lake, the glacier above, the Blue Cave below |
| The Mirror | a frozen lake with pressure ridges | the open ground between the keep and the gorge; its ice is a bridge | Frost Way |
| The Blue Cave | an ice cave from the Mirror's north shore to a hall and an undercroft that is the plaza's floor | the way in from below | its mouth on the shore |
| The Aerie | an open pavilion on the plateau at 85 | the way in from above: a view of the whole terrace and a ledge to bridge down from | over the glacier |
| The Forge | the fire core on a plinth at 66 in a moat of lava with two bridges | the objective | Ember Road to the west gap, Cinder Road to the south gap, the rim above, the Slag Run below |
| The Slag Run | a lava tube from the caldera's south slope down to a hall under the plinth | the way in from below | its mouth in the slope |
| Amberford | four houses, a chapel, a mill barn, an orchard in rows, an avenue of maples | the middle ground to fight over and a place to hold | Drove Road |
| Beacon Hill | a crown at 73 with a fire in a ring of pillars | the high ground over the village | by its slopes |
| The Thaw | the gorge with its river bed, banks and three spans | the seam between the teams; the lower route along the banks and over the bar | the spans, the scree ways |
| The Organ and the burnt cottage | basalt columns and a ruin on the ash by the Brimstone Way | cover on the fire lane's approach to the bridge | Brimstone Way |

## 5. The look

- **Biome.** Savanna (a gold grass and foliage), chosen for the autumn middle; snow and ice are blocks and do not change with it.
- **Three tone families.** *Ground*: snow, packed ice and andesite in the west; grass, podzol and coarse dirt in the middle; netherrack, brown
  and orange clay and red sandstone in the east. *Built*: stone brick, quartz and prismarine in the west; spruce, acacia planks and red sandstone
  roofs in the middle; nether brick and black clay in the east. *Accent*: sea lanterns in the west, glowstone and lava in the east.
- **Rock in beds** that follow the ground: packed-ice veins in the west, banded clay in the east, stone, sandstone and clay between; the gorge's
  walls are the lane's rock on each side of the bar.
- **Two species and a burnt one.** Spruce on the ice lane, oak in the orchard with its crown turned by orange, yellow and brown clay laid among
  the leaves, dead oaks on the ash.

## 6. What the build adds that the plan does not show

Snow laid thin on crowns, wall heads and the transition's grass (never on the Rime plaza); leaf litter under the orchard's crowns; ice hung
from the gorge's west rim and glowstone-tipped chains on its east; the Ice Fall and the Magma Fall at the gorge's two ends; embers on the ash,
each on netherrack and three blocks clear of wood; lamp posts on the roads; signposts at the yard's exits and at the three spans; the island's
underside, a cone of the lane's rock.
