# Hoarfire — the plan

## 1. The identity

**Hoarfire is a valley caught on the first night of winter, held by two hunting lodges across a rift: each team's
west lies under the Rimewall glacier's new snow and its east still burns with autumn, and each defends a fire in
the autumn wood and an ice crystal on the snow.** A player remembers the line down the middle of their half where
snow stops at a stream and red maples begin, the lava falling out of the autumn cliff into the void beside the
frozen falls of the winter one, and the crystal of packed ice hanging over a ring of standing stones.

The modes are Destroy the Core and Destroy the Monument together, the ordinary combined board: each team defends a
**Ember Core** (obsidian round lava) forward in the autumn wood and a **Rime Monument** (a crystal of packed ice) on
the snow, and wins by leaking the enemy's core and breaking the enemy's crystal.

## 2. The arrangement

**Two halves of land face each other across the Rift, a void crossed only by building.** Rowan (red) holds the north
half (z < 0); Sloe (blue) holds the south half, Rowan's mirror image across z = -0.5 (`Symmetry("mirror_z")`,
z -> -1 - z). The mirror, and not the half turn, is chosen so that both teams have the snow on the west and the
autumn on the east: the seam between winter and autumn runs the length of the board, and each team owns one
winter flank and one autumn flank of the same shape.

| piece | what it is | where (Rowan's) |
|---|---|---|
| the Hearth Lodge | the spawn: a jettied timber lodge on the Hearth Ridge, its court before it | x -10..10, z -94..-86, floor 56 |
| the Thaw | a stream rising from the court's spring and running down the middle of the half to fall into the Rift; its east bank a step of three and a half over the dell | x -4..2, z -79..-10 |
| the Rimewall | the glacier in the north-west corner, its tongue ending in a snout at 62 | crest (-74,-100) to (-46,-64) |
| the Rime Shelf | level snow, the old tarn bed; the Rime Monument floats over it in a ring of five standing stones | centre (-36,-50), r 10 |
| the Rime Tarn and the Ice Cave | a frozen tarn; a cave from its bank under the snow to a ledge in the Rift's cliff | tarn (-50,-40); cave (-59,-32) to (-50,-12) |
| the Frostwood | snowy spruce on the Frost Knoll and the west knoll | (-22,-30), (-58,-25) |
| Emberstead | a barn and a farmhouse east of the lodge, the harvest field below them | x 22..46, z -85..-78; field x 12..30, z -72..-58 |
| the Ember Pit | a round pit, five deep, in a clearing of charcoal kilns; the Ember Core floats over it | centre (38,-50), r 5 |
| Kiln Hill | a hill on the east edge, its crown at 66, a beacon on its snow | (58,-57), r 14 |
| the Russet Wood | autumn oaks and maples between the core and the Rift | (46,-27), (18,-34), (60,-40) |
| the Hollow Way | a sunken lane, three under the ground, from the Rift's shore into the Ember Pit | (22,-9) to (34,-45) |
| the Rift | void, z -12..11 at its widest, a build zone from edge to edge (z -16..15) | the whole width |
| the Berg and the Cinder | two islets in the Rift, each its own image | (-34,-0.5), (32,-0.5) |

**The objectives stand in front of the spawn and off to each side.** The monument is 36 west and 35 south of the
lodge door, the core 38 east and 36 south of it: neither is on the line between the spawns, and from the court
each is in view down its own path.

## 3. The numbers

Every number is measured by `scripts/plan_check.py` over the plan raster (octile walk, drops over six refused, the
Rift bridged at a block a block) and printed beside its target in `renders/plan-check.txt` and on the sketch.

| number | target | measured |
|---|---|---|
| own spawn to own monument, own core | 40 to 90 | 49, 49 |
| enemy spawn to a goal, over own spawn to it | 2.5 to 4 (the studio asks 3 to 4) | 3.03 (monument), 3.02 (core) |
| a goal to the nearest enemy goal | 85 to 150 | 92 |
| the Rift's narrowest void, shore to shore | 16 or more | 16 (between the two Thaw headlands) |
| void from a shore to an islet | 5 or more, never a jump | 9 |
| the widest jump the plan allows | at most 3 | 3 |
| jumps across the Rift | none | none |
| the core's clearance (trees, buildings within 4) | none | none |
| the monument's float over the shelf | at least 3 | 3 (crystal y 55..59 over the shelf at 51) |
| the core's float over the pit floor | at least 3, leak 5 | 9 of air over the pit floor at 44 |
| the kill height | under every floor | y 30; the lowest floor (the cave's cliff ledge) is 41 |
| players | at most 24 a team | 20 a team |
| the footprint | about 150 by 200 | 144 by 196, of which the Rift is 24 rows |

## 4. The places and their approaches

**Each goal has four ways in, and no two of them are the same walk.** This is the author's law from
`approaches.md`: around, above, below and through.

The **Rime Monument** (a 21-block crystal of packed ice, a bedrock heart) floats over a disc of old ice on the Rime
Shelf, ringed by five standing stones of andesite rimed on their north faces, set 7 to 9 from it so a defender
has cover and an attacker a screen, never within the 4-block clearance.

- **above:** the Rimewall's tongue ends in a snout 11 over the shelf and 16 from the crystal; an attacker climbs
  onto the tongue by the snow drift on its west flank and bridges down onto the crystal from the snout.
- **below:** the Ice Cave opens on a packed-ice ledge in the Rift's cliff at y 41, out of sight of the shelf; an
  attacker bridges to the ledge, walks the cave (lined in packed ice and snow) and comes up on the Rime Tarn's
  bank, 30 from the crystal.
- **around:** the Rime Tarn is frozen and sunk two under the shelf; the way round it or across its ice is the
  west approach.
- **through:** the Frostwood stands between the Rift and the shelf; its spruce give cover to within 11 of the
  crystal.

The **Ember Core** (obsidian 4x4x4 round 2x2x2 lava) floats 9 over the floor of the Ember Pit, whose leak runs
down into the pit. Around it is a charcoal-burners' clearing: four kilns (domes of earth with a smouldering crown)
and log stacks at 8 to 10 from the core.

- **above:** Kiln Hill rises on the east to a crown at 66; its flank is at the core's height (54 to 57) 15
  from it and 6 over it 17 from it, where an attacker stands to bridge across; its crown carries a beacon of
  lava under iron bars.
- **below:** the Hollow Way, a sunken lane from the Rift's shore, comes into the pit under the core; an attacker
  arrives below the defenders' sight line.
- **through:** the Russet Wood covers the ground between the Rift and the clearing.
- **around:** the harvest field and the kiln yard are open ground on the defenders' side; the Cross Road runs from
  the monument over the Thaw Bridge to the pit, the defenders' lateral lane.

**The middle of each half is the Thaw.** Its dell runs from the lodge court to the falls; the Thaw Bridge carries
the Cross Road over it at z -48 and a ford of stepping stones crosses it at z -32. The headlands either side of
the falls are where the two halves are nearest, 16 apart, and the islets offer two longer crossings of 9 and 9.

**Paths go where the players go.** The Rime Path (court to shelf), the Ember Lane (court through Emberstead to the
pit), the Thaw Path (court to the bridge), the Cross Road (shelf to pit), the Frost Track (shelf to the Rift
through the Frostwood) and the Ford Path (bridge to the headland). Each is three wide, in the ground's own set.

## 5. The look

**Biome:** Cold Taiga (30) under the snow and the frost band, Mesa (37) under the autumn, Savanna (35) under
half of the oaks so their crowns go gold. The Mesa tint turns grass and oak leaves russet and the Cold Taiga tint
turns what grass shows through the snow a cold blue-green.

**Three tone families.**

- **Ground:** the snowfield (snow, with packed ice where it is old ice and stone where it is too steep to hold
  snow); autumn grass (with podzol and coarse dirt under the crowns); the rock (stone and andesite in beds, granite
  and coal thin) under both, showing on every face and the Rift's cliffs.
- **Built:** timber over stone: spruce planks, spruce logs as posts and laid beams, cobble and andesite ground
  storeys, brick (the farmhouse, the chimneys), dark oak roofs; stone brick for the made ground (the court, its
  retaining wall and flights, the pit's kerb, the stoop).
- **Accent:** fire and ice. Lava (the falls, the hearth, the kilns' glow, the beacon, the Cinder's eye) and
  jack-o-lanterns; packed ice (the crystal, the falls of the west cliff, the icicles under the snow, the Berg); red
  and orange maple crowns and their fallen leaves; the team's banners at the lodge door.

## 6. What the build adds that the plan does not show

- Ground cover on the autumn grass: tufts, ferns, dead bushes, a few orange tulips and poppies (under 10% of the
  cells, off the paths and clearings); fallen leaves in carpet under the maples.
- Six boulders of one rock on the snow, snow on their crowns.
- The Rift's dressing: three lava falls from vents in the autumn cliff (24, 34 and 18 long), five frozen falls of
  packed ice down the winter cliff, the Thaw falling off its headland; icicles of packed ice under the snow half.
- Nothing grows on the brink a bridger leaves from (z > -18), on a path, within 11 of a goal, or in front of the
  lodge.
