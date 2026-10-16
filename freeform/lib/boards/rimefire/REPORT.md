# Rimefire — report

A Destroy the Core board for two teams of 24, built with pgmvox. The board is `freeform/lib/boards/rimefire`, its world
`maps/dtcm/rimefire`. `python3 -m pgmvox.run boards/rimefire --build <dir>` rebuilds it in about two minutes, with
`PGM_STUDIO_ROOT` set for the trees and the world writer.

## Concept: how it reads Fire and Ice

**One island, one ground, two skins.** The land is a single heightfield drawn for the north half and made exactly its own
half turn, so the two halves are the same hills, the same ravine, the same lanes. What differs is what lies on them. The
north half is an autumn that is still burning: dry gold grass, podzol, banded clay cliffs in browns, oranges and
yellows, oaks and birches whose crowns have turned orange, yellow, red and rust, fallen leaves, nether brick and lava. The
south half is a winter that has already come: snow, packed ice, andesite cliffs veined with ice, spruce with snow lying on
the boughs, quartz and prismarine, sea lanterns.

**The two halves are not clean.** A column is warm or cold by a factor that rises with z and with height and is broken by a
slow noise, so the fire half is white on its peaks, the ice half is autumn in its low hollows, and where they meet warm
ground carries a dusting of snow layers. Trees follow the skin, not the half: there are birch groves in the ice half's
valleys and spruce on the fire half's heights.

**The seam is where they touch.** A ravine across the whole island, bending in an S: a stream of lava under the north
wall, a frozen stream under the south wall, an obsidian line down the middle where the two would meet, veins of lava
behind orange glass in the north wall and frozen veins in the south one. Three bridges cross it, and each bridge changes
skin at its middle: dark oak and jack-o'-lanterns, then spruce and sea lanterns.

**The same bones, drawn once.** Every built thing is drawn once in the fire half and carried by `echo.py` to the ice half
through the half turn with its materials swapped: acacia roofs to dark oak, red sandstone to quartz, nether brick to
prismarine, glowstone and jack-o'-lanterns to sea lanterns, netherrack to packed ice, lava to ice, hay to snow. The
Furnace's nether-brick ring is the Cold Hearth's prismarine ring; both cores are lava in obsidian.

## The modes

**Destroy the Core only**, two cores (`fire-core`, the Furnace; `ice-core`, the Cold Hearth), `leak` 5, each core a 5 x 5 x 5
obsidian shell round a 3 x 3 x 3 of lava.

**Each core stands on a tor off to one side of its spawn and in front of it.** The Furnace is 55 degrees off the line
between the spawns and 46 blocks of plan walk (58 of built walk) from the Ashfall Lodge's yard; the Cold Hearth is its
half turn. It is not at the end of a lane.

**A core hangs over a pit rather than standing on a floor.** The ring wall (5 courses and a parapet, three gates: west
for the road, north and south for flanks, the east side solid over a drop) encloses a ledge, then a pit seven blocks
deep with a stair down each of four sides. The core's lowest block is five blocks over the pit's floor, so the lava has the
`leak` of 5 to fall; the author's rule that a core floats is kept (5 of air under every column). Four small lava
basins in the pit floor's corners (ice in the other half) and a chimney stack on the east give each ring a
silhouette from across the board. Towers flank the west gate; the ground round the ring is scorched.

**The approaches differ.** The west gate is the road's and the main assault. The north and south gates give a way in from the
flanks. The east scarp, a wall of ground rising to 85, overlooks the ring from behind and is reachable only from the
rear. The Overlook (a hill at 77 with a tower) stands in the middle lane in front of the tor's road.

**Why a team crosses where it does.** Because the south half is the north half turned, each flank span ends beside one
team's hamlet and in front of the other team's core. The west span's north end is 19 blocks from Rustwater and 72 from the
Furnace, its south end 55 from the Cold Hearth: for the fire team a short way to the ice core, for the ice team a way into
a hamlet. The east span is the same turned. The Keystone in the middle is the contested way, equal for both.

## Layout and proportions

The island is 130 by 198 blocks (22,276 columns of ground), with a void all round it and below. The land's underside is a
cone with spires hung from the edge in banded beds. The kill height is y 26.

| Piece | Height | Notes |
|---|---|---|
| Back ridge | up to 96 | behind each spawn, with snow on its crests |
| Spawn plateau | 64 | Ashfall Lodge: a hall and two wings round a yard 14 wide |
| Tor and Furnace | 72 | ring wall to 78, chimney to 94, core 71–75 over a pit floor at 65 |
| The Overlook | 77 | tower on the top, 15 courses, ladder, chest of food and arrows |
| Rustwater basin | 54–58 | pond, four houses, a well, two stalls |
| Landings and bridge decks | 63 | |
| The seam's floor | 45 | walls 17–25 high, two stairs each wall at one block a step |
| East scarp | 85 | |

Walks (the voxel walk over the finished world, drops to 3, jumps to 3): a spawn to its own core's ledge 58 and to its
pit floor 56; to the enemy core's ledge 141 and its pit floor 139; spawn to spawn 149–151. On the plan graph over the
shaped ground and the bridge decks (no jumps, slopes past 46 degrees not climbed): 46 to its own core's gate, 168 to the
enemy's, 197 spawn to spawn, ratio 3.66. 21,817 of 22,276 columns are reached from the fire spawn on the built walk.

## The palette

Biome Savanna: grass `#bfb755`, oak leaves `#aea42a`, a dry gold that sits beside podzol.

| | Fire (warm) | Ice (cold) |
|---|---|---|
| Ground | dry grass, podzol, coarse dirt | snow, packed ice patches, andesite on the steeps |
| Cliff beds | brown, orange, yellow stained clay, hardened clay, red sandstone | andesite, stone, polished andesite, packed ice |
| Paths | granite, coarse dirt, gravel, a little brick | andesite, gravel, cobble |
| Built | stone brick, red sandstone, nether brick, spruce beams, acacia roofs | stone brick, quartz, prismarine brick, spruce beams, dark oak roofs |
| Accent | lava, glowstone, jack-o'-lanterns | ice, sea lanterns, light-blue glass |
| Crowns | gold, orange, yellow, red, rust; real leaves 16% | spruce and pine under snow layers |

Nothing in a building is snow, ice or birch log; no building wall is the ground's tone.

## What was checked

- **map.xml** read by the studio's parser (`read_mapxml.cs`): valid, no issues; two cores, two spawns, two teams of 24.
- **Walks** (`renders/walks.txt`): both spawns reach both cores' ledges and pit floors and each other; `audit.footing`
  reports 0 and `loose_water` 0; `Objectives.check` reports 0 (the cores float and stand on ground).
- **Plan check** (`renders/plan-check.txt`) and the **plan sketch** (`renders/00-plan-sketch.png`) before the build; the
  annotated top-down (`19-topdown-annotated.png`) after it.
- **Renders**: flat colour (`30`, `31`) and textured (`01`-`18`, the studio's renderer, 1.8.9 textures). Every place was
  looked at in the textured renderer, not only the flat one: the pink of the paths, the orange of smooth red sandstone and
  the teal of prismarine were chosen by looking.
- The ground is checked to be its own half turn in `land.py` (`python3 land.py` prints it).

## What did not work, and what was changed

- **The first plateaus were circles.** The spawn plateau and the tor were levelled in a disc and read as craters from above;
  they are now levelled in a bent frame (`noise.warp`) with a long reach, and the lodge and ring wall are what make
  their outline.
- **The island had a notch of void behind the spawn.** The outline's north edge stood too close, so the yard's back
  corner was over nothing; the outline was moved out and the levelling skips void columns.
- **A core with a pit five blocks deep and a leak of 5 cannot be leaked.** Lava can only fall as far as the floor, 4 blocks;
  the pit is seven deep, with the floor five under the core.
- **Trees planted over the ice half's buildings.** The claims were recorded only for the fire half; they are now turned
  with the places. Trees also grew over the bridge heads; the seam's rims are kept clear to 20 blocks.
- **Snow layers stacked on snow layers and over air** popped off at load (`audit.footing` found ten). A pass removes them.
- **Lava falls as flowing lava** would decay; they are lava held in a recess behind orange glass, which shows and holds.
- **Banners** on the lodge's gate posts are written as tiles but the studio's textured renderer does not draw them, so the
  posts look bare in the renders. They are in the world.
- **The goal ratio reads 3.66 on the plan graph and 2.4 on the built walk.** The built walk lets a player jump and drop,
  which shortens the enemy's way by more than it shortens the own way. Moving the cores nearer the spawns would lift the
  ratio and take the own walk under its 40; it was left.
- **The lodge hall's roof is one large plane.** A gambrel over a 17 by 8 hall still hides most of the hall's wall; a
  cross-gabled hall would give more depth and was not built.

## What the plan missed

| Decided while building | What in the plan would have decided it |
|---|---|
| The core pit's depth | the leak against the float: depth = leak + the pit's floor stand |
| Which things the trees keep off | a claims list in `plan.py` as data, turned with the places |
| How wide a path is | a width per road class with its colour |
| Where a tree's crown may overhang | a clearance in blocks per place, not only a footprint |
| Where the stairs of the ravine start | the stair's foot against the lava channel, stated as a ford |

## What a studio feature would need to do it

| What I wanted | How hard it was | What a studio feature would need to do |
|---|---|---|
| Build one half and carry it onto the other with another palette | A helper (`echo.py`): diff the world before and after the north's builders and turn the changes; `turn_world` turns whole columns and would overwrite the south's differently painted ground | `orient.turn_changes(w, before, palette)`: carry only the blocks changed since a snapshot, through any symmetry, with a palette map keyed on (id, data) and its tiles |
| A ground exactly its own half turn though roads, ramps and a seam are cut into it | The blend `t*F + (1-t)*F_turned` covers the field; roads graded one at a time are not symmetric, so the last step takes the north's rows and turns them | `Symmetry.make_whole(H, keep=...)` as one call at the end of a ground, and `grade` taking `symmetry=` to lay both images at once |
| A planting that knows the cold from the warm | Own planting loop (`plant_wood`) with a hue per crown and snow on the boughs; `scatter` takes one zone and one kind table | `trees.scatter` with a per-tree recolour and a post hook, and snow on the boughs as a library step |
| A crossing's clear zone, both ways | Excluded by hand as a distance from the seam's centre line | a named keep-clear mask on `Raster` that placements and trees both read |
| A recess held behind glass as a vein in a wall | Searched the wall's face course by course by hand | `volume.under.vein(w, wall_cells, fill, pane)` |
| A shot that frames what a place is | Boxes tried by hand until the foreground tree was outside them | `render.textured` taking a place and a radius and choosing the box and the eye with a clear-sight test |
