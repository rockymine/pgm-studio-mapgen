# Rimefire — plan

## 1. The identity

**Rimefire is one island cut by a ravine, the same bones in two skins: the north half is an autumn that is still burning,
the south half is a winter that has already come, and a seam of lava and meltwater runs between them.** A Destroy the
Core board for two teams of 24: each team holds a fortified tor with its core hung in a pit, and the way to the other
tor is over one of three bridges across the seam.

What a player remembers: crossing the Keystone over a stream of lava on one side and a frozen stream on the other, and
the core of the other team hanging in a pit of green stone or black brick.

## 2. The arrangement

One island, 130 by 198 blocks, 22,276 columns of ground in a void. North of the seam (z < 0) is the fire half, south of it
the ice half, and the ice half is the half turn of the fire half about the board's middle: `(x, z) -> (-1 - x, -1 - z)`.
The ground is exactly its own half turn; every built thing is drawn once in the north and turned onto the south in the
south's materials (`echo.py`).

Fire half, north to south:

- **The back ridge** at z -90 to -98, rising to 87–96, with snow on its crests. It is the land behind the spawn.
- **Ashfall Lodge**, the spawn, on a plateau at 64 in front of the ridge: a hall against the ridge and two wings round a
  yard, open to the south. The spawn stands in the yard.
- **The Furnace**, the core, on a tor at 72 to the east and south of the spawn, off the line between the spawns by 55
  degrees: a ring wall with three gates, a ledge, a pit seven blocks deep with a stair down each side, and the core hung
  over its floor.
- **Rustwater**, the hamlet, in a basin to the west at 54–58 round a pond, four houses and a well.
- **The Overlook**, a hill at 77 in the middle lane with a masonry tower on it.
- **The Waystation**, an open shelter on the pass between the hollow and the overlook where the lanes cross.
- **The east scarp**, a wall of ground rising to 85 over the Furnace's east side, with rust-banded needles at its foot.

The seam runs the width of the island at z about -0.5, bending in an S. It is a ravine 15 to 20 blocks wide, its floor at
45, its walls 17 to 25 high. Under the north wall a stream of lava, under the south wall a frozen stream, between them
a walkway with a line of obsidian down its middle where the two would meet. Two stairs climb each wall, and the lava
channel is broken at each stair's foot so the foot can be reached.

Three crossings: the **Keystone** in the middle (6 wide, stone, with a pier standing on the seam's floor and a tunnel
through it) and a **west span** and an **east span** (4 wide, timber trestle). The deck of each is at 63, the level of
the landings. Because the south half is the north half turned, each flank span ends beside one team's hamlet and
in front of the other team's core: the west span's north end is 19 blocks from Rustwater and 72 from the Furnace, its
south end 55 from the Cold Hearth; the east span is the same turned. That is the pinwheel: a flank span is a short way to
the core for one team and a way into a hamlet, a long way from the core, for the other.

Routes: from the lodge three roads leave the yard south — west to the hamlet and the west span, south to the overlook
and the Keystone, east to the foot of the tor and up its flank to the Furnace's west gate; cross roads join the lanes at
the waystation and at the tor's foot. Roads are found over the shaped ground at a grade of 1 in 5 and graded into it.

## 3. The numbers

| Quantity | Target | Plan reads |
|---|---|---|
| Footprint | at most 150 x 200 | 130 x 198 |
| Players | at most 24 a team | 24 |
| Walk, a spawn to its own core's gate | 40 to 90 | 46 (plan graph), 58 (built walk) |
| Walk, a spawn to the enemy core's gate | 85 to 150 | 168 (plan graph), 141 (built walk) |
| Enemy core walk over own core walk | 3 to 4 | 3.66 (plan graph), 2.4 (built walk) |
| Core hung over its pit floor | at least 3 of air; lava has `leak` 5 to fall | 5 of air, leak 5 |
| Seam floor under the landings | 45 vs 63: a fall of 18 | fall damage on; the strip has no lava in it |
| Bridge width | flank 4, Keystone 6 | 4, 6 |
| Stair rise | one block a step | stair blocks on every one-block rise |
| Kill height | under the lowest ground a player can stand on | 26 (the seam floor is 45) |

The plan graph is the stricter reading (it will not climb a slope past 46 degrees and will not jump); the built walk is
the voxel walk over the finished world with jumps of up to 3 and drops of up to 3. Both are in `renders/`.

## 4. The places

Every place has a reason a player goes there.

- **Ashfall Lodge / Rimehold** — the spawn. Players leave south across a yard, through a mouth between two lamp posts.
- **The Furnace / The Cold Hearth** — the objective. Players defend the ring and its gates or climb its wall. The east
  side is solid over a drop; the north and south gates give the flanks a way in; the west gate is the road's.
- **Rustwater / Frostholm** — the nearest ground between a spawn and a flank span. A pond, houses to hold, a well and two
  stalls on its green where a team regroups before the span.
- **The Overlook / Icewatch** — the high ground of the middle lane. A tower whose crown sees the Keystone's landing and the
  road to the hamlet; a chest at its foot holds golden apples, arrows and beef.
- **The Waystation / Rime Shelter** — the crossing of the lanes behind the front: a roof, a table, braziers, a supply chest.
- **The Keystone** — the contested crossing. Wide, a pier in the middle, the seam's floor visible below.
- **The seam's floor** — a flank route under the bridges: down a stair, along the walkway, up the other side. It is where
  a player who falls from a bridge lands.
- **The east scarp** — a high ground over the Furnace reached only from behind: costs time, buys a view of the pit.

## 5. The look, decided now

**Biome: Savanna.** Its grass is `#bfb755` and its oak leaves `#aea42a`: a dry gold that sits beside podzol and coarse
dirt. Snow and ice are blocks and are not tinted, so a cold biome is not needed for the south half.

**Three tone families.**

- *Ground:* the warm skin is dry grass, podzol and coarse dirt over banded brown, orange and yellow clay; the cold skin is
  snow, packed ice and andesite over stone, polished andesite and packed ice beds.
- *Built:* the fire half is stone brick, red sandstone, nether brick and spruce beams under acacia (orange) roofs; the
  ice half, by the same bones, is stone brick, quartz and prismarine bricks under dark oak roofs.
- *Accent:* fire is lava, glowstone and jack-o'-lanterns; ice is sea lanterns, ice and light-blue glass.

**The two skins are one rule.** A column is warm or cold by a cold factor that rises with z and with height and is
broken by a slow noise; so the fire half is cold on its peaks and the ice half is warm in its low hollows. Where the two
meet, warm ground carries a dusting of snow layers. Trees follow the skin, not the half: the ice half has autumn groves
in its valleys, the fire half has spruce on its heights.

**Rules kept from the ruling on what a board is made of:** no snow or ice in a building; no birch log in a building; the
gable is not the overhang's block; a path is three blocks of one tone; two tree species families a half; a building is not
the tone of the ground it stands on.

## 6. What the build adds and the plan does not show

- Trees, shrubs, fallen leaves, fallen logs, boulders, bare spruce trunks and drifts, placed outside every claimed
  footprint, 3 blocks off the roads and 20 off the seam's centre line so no crown overhangs a crossing.
- Lamp posts every 14 blocks along the roads.
- The seam's lava veins: a recess in the north wall with lava held behind a pane of orange glass, three of them (frozen
  veins on the south wall).
- Rust needles of banded clay on the fire half and, turned, ice needles on the ice half.
- Scorched ground round the Furnace thinning out to the grass: coal blocks, netherrack and coarse dirt.
- The underside: a cone hung from the edge with spires, in the banded beds, so a player falling sees rock and not a slab.
