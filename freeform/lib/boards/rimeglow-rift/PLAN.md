# Rimeglow Rift - the plan

**Identity.** One island cut in two by a river of lava: the north half is a glacier country of snow, packed ice and spruce
(Rime), the south half the same ground in autumn - banded red-orange rock, orange and red leaf, dark oak (Ember) - and
where the halves meet fire and ice touch, along a rift three blocks of ledge wide above the lava. A player remembers the rift
and its three bridges. Destroy the Core, two teams of up to 24.

**Arrangement.** One floating island of about 18,900 columns (76% of its 130 x 184 footprint; the rest is void), the
half turn of the north half laid on the south, so the two teams' ground is identical and only its season differs. The
rift runs west to east across the middle, 8 to 14 wide, dammed at both ends so the lava cannot run off the board. Three
crossings span it: the Meltgate causeway (a stone arch, 8 wide, under two gate towers) and, 38 blocks either side, the
Hoarspan and Kindlespan trestle bridges (5 wide, timber). A fourth way is on foot: two ramps cut into the rift's walls take a
player to a ledge three above the lava, and two lines of obsidian pillars carry it across the lava. A team's spawn is the
Hearth Court before its hall at the back of its half; its core is held over a pit in a ring-ruin on a butte to the
east (Rime) or west (Ember) of the court, 44 moves from the spawn and 137 from the enemy's. Between spawn and rift lie a
mere (the flat fighting floor; frozen in the north, a cooled lava crust in the south), a wooded ridge and a pad on
that ridge's foot for a camp.

**Numbers, with their targets** (measured by `scripts/plan_check.py` and `scripts/walk.py`; the output is in
`renders/plan-check.txt` and `renders/walks.txt`)

| What | Value | Target |
|---|---|---|
| ground is its own half turn | exact | exact |
| footprint of the land | 130 x 184 | at most 150 x 200 |
| ground against its footprint | 76% | under 80% |
| rim to rim at the crossings | 28, 33, 33 | 24 to 36 |
| ledge above the lava / width | 3 / 3.6 | 2 to 4 / at least 3 |
| air under a core, over its pit | 7 | at least 3 (leak 6) |
| walk, spawn to own core | 44 moves | 40 to 90 |
| walk, spawn to enemy core, over own | 3.1 | 3 to 4 |
| flat floor of each mere | 721 columns | at least 600 |
| land reached from a spawn | 18,105 of 18,908 | all that is ground |

**The places.**

| Place | What it is | Why a player goes there, how |
|---|---|---|
| Rime Hall and Hearth Court | the spawn: a two-storey hall, gallery, hearth, cupola; a paved court with a fire in the middle | where a team starts; a stair of stone down to the roads |
| Rimewatch | the core: a butte with a ruined ring-wall, the core held over a pit under a timber cage | the objective; two ways up, a road from the court and one from the gate |
| Frostmere / Cinder Mere | the flat floor in front of the court | the middle of the half: a fight over flat ground, with a hut or a kiln, ridges of pressure ice or crust, a ring of standing stones |
| Meltgate | the causeway and its two gate towers (ladders, slits, crenelled crown) | the front: where both teams meet in the middle |
| Hoarspan / Kindlespan | the side bridges and their pylons and plazas | the flank crossings, long and exposed |
| Lava ledge | a shelf along the rift's foot, reached by a ramp at each end, with obsidian pillars across the lava | the low way: slow, but it passes under every bridge |
| Hoarwood / Amberwood | the wooded ridge | cover between the court and the gate; the camp on its foot |
| Woodcutters' Rest / Orchard Keeper's | one flat pad, a cabin each, a fire ring, a woodpile or a pumpkin field | a place to regroup beside the road to the west gate |
| Glacier Tongue / Cooled Flow | a hollow of ice (north) or cooled lava crust (south) running from the highland to the mere | frames the court's west; it is the half's other surface |

**The look, decided now.** Biome: the cold taiga where the winter holds (the north), the mesa elsewhere, so oak leaf and
grass in the south tint toward autumn brown and olive. Three tone families: ground - snow, packed ice and stone in the north,
banded hardened clay and clay in the south; built - stone brick and spruce in the north, nether brick, dark oak, brick and
acacia in the south; accent - sea lantern and clear ice in the north, glowstone, orange clay and lava in the south. The
seasons trade across the rift: a few autumn oaks stand in the snow on the north bank, spruce on the south bank, and
the rock's banding thaws and frosts through noise, so the line between the halves is never ruled. Roads are paved by hue:
cold stone and gravel in the north, dirt, podzol and dark planks in the south.

**What the build adds and the plan does not show.** Spires of ice and clay on the crags behind each hall; frozen falls and ember
seams down the outer cliffs; icicles and ember drips hung under the island; shards of floating rock in the bays (outside
the build area); the lava dams' outer faces carry a fall set in orange clay; signposts at nine decision points; snow drifts
in the lee on gentle ground; carpet litter under each autumn tree.
