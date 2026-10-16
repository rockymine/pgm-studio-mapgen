# Rimeglow Rift - report

**Concept.** Fire and ice are not two halves of a theme here but one landscape in two seasons, and a river of lava
is where they touch. The north half is a glacier country (snow, packed ice, spruce, a frozen mere); the south half is its
exact half turn, painted and built as an autumn badlands (banded terracotta, orange and red leaf, dark oak, a cooled lava
crust where the mere was). Each half's ground is the other's: the rock under the south half is the banded clay of the mesa
and under the north half the grey beds and ice of a glacier, but the beds trade through noise at the rift, so a bank
of one shows the other's rock in ragged tongues. Autumn oaks stand in the snow on the north bank and spruce on the south bank, the way
a thaw line shows. Lava is the fire; a lava river dammed in a deep rift, with a ledge along its foot, three bridges
over it and lavafalls set solid on the dams' outer faces.

**Mode: Destroy the Core**, 24 a side. Each team has one core: an obsidian shell round lava, held three blocks above a
pit at the middle of a ring-ruin on a butte, 44 moves from its spawn and 137 from the enemy's (3.1 times).
The core stands in front of the spawn and off to one side (the east for Rime, the west for Ember), and the way to it
from the enemy side is a crossing of the rift, a climb of three terraces on a stair, and a ring-wall with two gaps. The three
bridges and the ledge give four routes, each with a different cost and cover: the causeway is short and fought over between
two gate towers; the trestles are long and open; the ledge is hidden below the rim and slow, and its two obsidian lines
cross the lava on pillars a jump apart.

**Layout and proportions.** One island, 130 x 184, 76% land, the rest void. The rift across its middle is 8 to 14 wide,
28 to 33 rim to rim at the crossings. Spawn to own core is 44 moves; spawn to enemy spawn 137. Rim shelves sit at y 57, the
spawn courts at 71, the core's butte at 73, the mere floors at 53, the rift's floor at 35 with lava to 38; the highest
ground is 93. Kill height 10, build height 104. The mere floor is the one large flat on the board and is flat because
it is frozen (or cooled) water; the courts and the plazas are flat because they are paved; the pads are flat because a
building stands on them; everything else is a slope.

**Palette.** Rime: snow, packed ice, ice, stone and andesite, spruce, stone brick, spruce planks, sea lanterns, light blue
glass. Ember: hardened clay and orange, brown and yellow stained clay, red sand-coloured dirt and podzol, dark oak,
nether brick, brick, acacia, glowstone, orange glass. Shared: obsidian, lava, iron bars. The south half's ground is brown
and olive under the mesa biome, which is the autumn: the leaf crowns are dyed clay in orange, red, yellow and brown with
the mesa-tinted oak leaf inside them, and a carpet of fallen leaf in the same colours lies under each.

**What was checked.** (1) `plan_check.py`, before the build: the half turn is exact, the footprint is 130 x 184, the
crossings are 28 to 33, the ledge is three above the lava. (2) `walk.py` on the built world with the 1.8 moves
(max drop 4, running jumps over gaps of 3): both spawns reach their own core in 44 and the enemy's in 137 to 141; 18,105 of
18,908 ground columns are reached from the spawn (the rest are scenery shards, crag tops and tower roofs by ladder);
no footing problem, no loose water, every objective's own check clean. (3) `read_mapxml.cs`, the studio's parser: valid, 2 cores, 2
spawns, 2 teams, no issues. (4) Fire is kept off every flammable block by a pass in `gen.py`, and every lava block has
solid or lava round it or above it. (5) The textured renderer, 18 shots of the outside and of each objective (in
`renders/`); the flat renders and a top-down annotated with the plan's names are beside them.

**What did not work, and what was changed.**
- A first outline put 81% of its footprint in ground; bays were cut and the ellipse narrowed until 76%.
- Trees: 68 sites were all the ridge and mere flanks allowed (the ridge is steep); a fuller forest would need a ridge
  of gentler stone, which would take the ridge's cliff away.
- A cross-checked ladder to the tower crowns was walled in by a floor course; a hatch row was added and the walk now
  reaches both tops.
- Wall banners facing away, signs on a leaf, sand-fall-prone snow layers over air and a fire beside planks were found by
  `audit.footing` and the fire sweep and fixed in `gen.py`.
- The `lava` in the rift's corners spilled sideways through the first cut of the shelves; the banks were raised to one above the
  surface.
- The studio's textured renderer does not tint snow layers, so a drift reads white-grey; the autumn leaf is clay, not
  biome-tinted leaf, because the 1.8 leaf colour in a mesa is a muddy olive.
- Not done: a second objective per team, a mid-board capturable, and water (a frozen mere with no water under it; a hole in the
  ice inside each hut holds a single water block).

| What I wanted | How hard | What a studio feature would need to do it |
|---|---|---|
| One ground in two seasons, rock beds that trade through noise | easy in a script, not stated anywhere | a `season` field a theme can be laid on, with the band axis `slope` and a second axis `winter` |
| A building written once and written twice in two palettes and turned | medium: a `Stamp` of my own | a palette map on a symmetry image, so a placed thing's materials change under the turn |
| A lava canyon with a ledge and ramps | medium | a canyon landform with a shelf and graded ramps down its wall |
| Flat floors that are flat for a reason (a mere) | easy | a `basin` landform that holds a level and paints its own set |
| A core held over a pit in a ring-ruin | medium | a core prefab with its cage and its pit |

**What the plan missed** (decided while building): where the tree sites fall on the ridge (the plan stated the ridge, not its
slope); the hatch in a tower's crown; the dam that closes the rift's ends; the signposts' text; the south half's fire
ring, which the first cabins put beside planks.
