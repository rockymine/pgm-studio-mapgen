# Cinder Reach — destroy the core

**Two grey ash shelves face each other across a smoking fissure, and each team's core hangs in the open over the
vent of a breached cinder cone in front of its lodge.** The core is reached around a hot pond, down off a basalt
ridge, up a lava tube under a scorched wood, or through a quarrymen's hamlet. The board is 208 by 144 blocks,
symmetric by a half turn, one core a team, teams of twenty.

```
cd freeform/lib && python3 -m pgmvox.run trials/opus/cinder-reach --build <scratch>/cinder-reach --skip write
```

The whole run takes about 100 seconds, and 90 of them are the read-back's four voxel walks. Generation takes two
seconds.

## How it plays

**Each team's shelf is one floating island, and the only way across is the fissure, built over.** The fissure is
17 to 26 blocks of void between the lips on the rows a crossing is made on. The build zone is every void column
with |x| at most 24, so a bridge can start anywhere along the lip. Red holds the west, blue the east.

**The spawn is a paved terrace at 57 under the Caldera Wall, at the back.** The lodge stands on the terrace's
north side. The wall rises 13 blocks over the terrace within 20, and 14 blocks of red's own land lie behind the
spawn.

**The core sits 39 degrees off the line between the spawns, forward and to the south.** Its casing (5 x 5 x 5,
y 52 to 56) hangs two blocks over the bowl of a cinder cone, floor 50. Under the casing is a vent eight blocks
deep with an obsidian floor, so the lava falls nine blocks and the core leaks at five. A player beside the casing
stands at 51 with the casing at head height, so nobody walks under it into the vent.

**The cone is a drop in and a walk out.** Its rim stands at 56, a block down for every block outward, so anyone
can climb it from outside. The inner face is a sheer drop of six into the bowl all the way round, except at two
breaches: a ramp west toward the hamlet (the defenders' door) and one east toward the pond.

### The five ways onto a core

| Way | What it is | Blue's walk onto red's core (plan) | Who reaches its mouth first |
|---|---|---|---|
| Around the pond, north | the short road past Steam Pond into the east breach | 138 (the shortest) | red 69, blue 109 |
| Around the pond, south | between the pond and the Spine's foot, over the rim | 146 (x1.06) | red 76, blue 116 |
| Over the Spine's crag | up the basalt ridge to its crag at 64, eight over the casing, then bridge or drop | 168 (x1.22) | red 78, blue 147 |
| Up the lava tube | bridge down seven to the tube's mouth in the fissure face, through the tube to a sinkhole in the wood | 145 (x1.05) | red 68, blue 102 |
| Through Pumice Row | the long flank round behind the core, through the defenders' hamlet | 177 (x1.29) | red 14, blue 153 |

**The ways come from around, above, below and through, as `approaches.md` asks.** The pond splits the front
approach in two. The crag gives height over the casing, the tube comes up under the wood out of sight, and the
hamlet gives cover round the back. Every main way costs at most a quarter more than the shortest, so none is
decorative, and the defenders reach every way's mouth first.

**The shelves meet on opposite flanks.** Red's core is south of the middle and blue's is its image to the north,
so each team attacks across the fissure on its own left. That is the half turn's version of the flank effect in
`match-flow.md` §6.5.

### Walk numbers, both teams

| Walk | Plan (octile, step up 1.2) | Built world (moves, four-way) |
|---|---|---|
| Spawn to its own core, red / blue | 41.2 / 41.2 | 52 / 52 |
| Enemy spawn to the core, bridging | 137.6 / 137.6 (20 of it bridged) | 139 / 139 |
| Core to the enemy spawn over core to its own (GO1) | 3.34 | 2.67 |
| Spawn into the enemy's lava tube | — | 118 / 118 |
| Spawn onto the enemy's crag | — | 158 / 158 |
| Tube mouth to the sinkhole floor, to the wood, to the core | — | 21, 33, 53 |

**The built walk reads the own-core walk a quarter longer than the plan.** The plan walks octile and the voxel
walk counts four-way moves, so a diagonal stretch costs 1.41 in one and 2 in the other. The enemy walk is mostly
bridged in straight lines, so it grows less, and the GO1 ratio falls from 3.34 to 2.67. The friction log takes
this up.

## Renders

| File | What it shows |
|---|---|
| `renders/00-plan-sketch.png` | the plan: the board, the five ways onto red's core, three cuts, blue's shortest attack unrolled, the check |
| `renders/05-topdown-annotated.png` | the built top-down with the plan's names, footprints and markers |
| `renders/30-iso-board-se.png`, `31-iso-board-nw.png` | the board from two corners |
| `renders/32-iso-red-cone-se.png` | red's cone, the pond, the wood and the sinkhole |
| `renders/33-iso-lodge-and-row-se.png` | the lodge terrace, the Caldera Wall and Pumice Row |
| `renders/34-iso-north-flats-sw.png` | the cinder knolls and the Cairn, red's staging ground |
| `renders/10-section-core-z24.png` | a cut through the core, its vent, the cone's rim and the pond |
| `renders/11-section-core-x-51.png` | a cut through the knolls, the core and the crag |
| `renders/12-section-tube-z5.png` | a cut along the tube from the sinkhole to the fissure face |
| `renders/40-xray-tube.png` | the tube in x-ray (small: the tube is 16 blocks long) |
| `renders/50-elev-cone-from-the-pond.png` | the cone as the attackers from the pond see it |

## Read-back

- **`Objectives.check`:** no problems; both spawns stand, both cores have lava.
- **`audit.footing`:** 0 problems.
- **Standable columns over the void:** 0.
- **The leak:** the first block under red's casing is nine down, against a leak of five.
- **The studio's reader** (`data/read_mapxml.cs`): valid, 2 teams, 2 spawns, 2 cores, 1 kit, 5 apply rules, no
  issues.
- **The build:** 574,178 blocks, 8 trees, 8 tile entities (the lodges' banners).

## The plan

**Identity.** Above, in the first paragraph.

**Arrangement.** Two shelves at about 51, the fissure between them, the spawn at the back of each under a wall,
the core forward and to one side, and the five ways onto it. The places on each shelf:

| Place | What it is | Why a player goes there |
|---|---|---|
| The Lodge and its terrace | the spawn, 57, backed by the Caldera Wall | everyone starts here |
| Pumice Row | three brick-and-spruce cottages, a well, a log pile, a wheat plot | the defenders' road to the core runs through it; the attackers' long flank |
| The Breach | the cinder cone and its core | the objective |
| Steam Pond | a pool at 50 in front of the core | splits the front approach in two |
| The Spine | a basalt ridge rising west to a crag at 64 | the way from above |
| The Scorch Wood | acacia and olive over grass | cover to within eleven blocks of the casing |
| The Sinkhole | rings a block apart down to the tube's floor at 43 | the tube's way out |
| The Cairn | a ruined watch tower on the tallest cinder knoll | the staging ground's lookout across the fissure |
| The Landing | the lip where the Flats Road meets the fissure | where the attack across starts |
| Ember Pools | two lava pools in obsidian at the wall's foot by the lodge | the accent; they frame the spawn |

**The look.** The biome is savanna, so the grass inset in the ash reads yellow-green beside it. The ground is an
ash field, grey stained clay with black and pale drifts, over rock of stone and andesite in beds following the
surface, with thin black beds. Building is warm (brick, spruce and dark oak, granite and brick roads and a
granite terrace), so a house never stands in the ground's own family. The accent is lava, glowstone and the team
banners.

**What the build adds that the plan does not show:** the pond's bed, lamps along the roads (kept fifteen from the
core), the hamlet's well, log pile and wheat, and the trees. Trees stand only in the wood and on the Spine's
gentle south side, every block over land, none within four of the casing.

## Decisions, and why

- **One core a team.** The board is wide, and a large board with a single goal is the commonest destroy map there
  is.
- **The core over a vent rather than on a pillar.** A core resting on the ground cannot leak. A vent closed by
  the casing itself keeps players out of it with no barrier block, and its obsidian floor catches the lava.
- **The cone's inner face is one-way.** Dropping in costs a heart and a half; getting out is by a breach, which a
  defender can watch. That makes the rim an attack and the breaches the defence's doors.
- **The flank through the hamlet is allowed to be long.** It is the defenders' own ground and a way round, not a
  way in, so its row in the check has no target.
- **Warm buildings on a grey board.** The ground family is grey ash, so the built family had to be warm.

## What went wrong, and how it was found

- **The lava tube was unreachable in the plan.** Its floor met the sinkhole's rings two blocks under their
  ground, and the plan walk stopped there. The check's "inf" found it. The plan now says what the carve does:
  where the tube passes under the rings, the ground is the tube's floor.
- **The spawn was 37 from its core, under GO4's 40.** The check found it, and the core moved three blocks
  forward.
- **The north half was a plain with nothing on it.** The first sketch showed it. Three cinder knolls went in, the
  Cairn on the tallest, and the far north-west corner was cut back to the void.
- **The ore drift ran out of the island's side.** The read-back found 36 gravel blocks over air and 134 standable
  columns over the void at x -101. The Caldera Wall behind the spawn is only six blocks deep there, so the drift
  was cut rather than moved.
- **Acacia crowns hung over the void and over the fissure.** The read-back's over-the-void count found 48 and
  then 2. `trees.scatter`'s `allowed` now refuses any tree with a block over a column less than two in from the
  edge.
- **The ash reads dark brown from above.** Grey and black stained clay are what the look ruling names for an ash
  field, and the studio's colours for them are brown. Pale drifts went into the set and grass was inset where
  water, shade and the hamlet keep it.
- **The first sketch was overwritten.** The plan changed three times after it (the knolls, the north-west cut, the
  drift) and the earlier sheet was not kept with a version suffix. The later boards keep it.

## What the plan missed

- **Where the drift could run.** The plan put a mine behind the spawn without stating the wall's depth there. A
  plan row "rock over the drift, at least 3" would have caught it.
- **Tree crowns at the edge.** The plan stated the wood's polygon, not that a crown may not hang over the void.
- **The tube's junction with the sinkhole.** The plan stated both, but not how they meet.

## Friction log

### What the library lacked, written locally

- **A raster drawn from a half.** `Raster.from_heights` gives three fixed kinds. A terrain board with its own
  kinds builds `H` and `K` for one half and completes them by the symmetry: `common.full`, used by every board
  here.
- **The fissure's widths.** No measure gives the void between two halves by row; `common.gaps` does.
- **An approach measured by its way.** `plangraph.route` gives the cheapest walk, not the cheapest one through a
  given place. `common.via` walks to a waypoint and on, which is how the five ways were priced.
- **A bridge onto a storey.** `graph(bridge=...)` joins a build zone's cells to ground-storey neighbours only. A
  tube mouth in a cliff face is on storey 1, so its edges to the zone are passed as `extra`.
- **A tunnel meeting a surface hole.** `under.tunnel` and a heightfield sinkhole are separate; where the tunnel
  passes under the hole's rings, the plan and the generator both open them by hand.
- **A core's leak.** `Core.check` asks only for lava inside. Whether the casing can leak (an open drop of more
  than `leak` under it, and room a player cannot walk into) is checked in `walk.py`. `Core` could carry its vent.
- **Paint by place as well as slope.** `terrain.lay` gives the top one block by slope. A set with patches
  (`common.set_paint`), grass inset where water and the hamlet are, and the bowl's cinder floor are a second pass.
- **Paths and floors in cells.** `route.pave` chooses a block per column at random. The look ruling asks for a
  path laid in cells of about three, a third each of three blocks; `common.cell_pick` is that, for the terrace.
- **A door before the house.** `build.house` decides the door only while building, so the plan re-derives it
  (`plan.door_cell`) and the generator raises if they disagree. The same friction is in the Riftwater port's log.

### Bugs and surprises, with reproductions

**The plan walk and the voxel walk disagree by design, and the goal rules do not say which one they mean.** The
plan walks octile; `walk.walk` counts four-way moves. On this board the same own-core walk is 41.2 and 52, and
GO1 is 3.34 in one and 2.67 in the other. A reproduction on an open floor:

```python
from pgmvox import World, walk, B
from pgmvox.plan import Raster
from pgmvox import plangraph as G
w = World(0, 0, 30, 30, sy=8); w.fill(0, 1, 0, 29, 1, 29, B.STONE)
print(walk.walk(w.ids, [(0, 2, 0)], 0, 0)[20, 2, 20])                 # 40
R = Raster((0, 29), (0, 29), ["floor"]); R.H[:] = 1
E = G.graph(R, {"floor"}, rules=G.PlanRules(diagonals=True))
print(round(G.dijkstra(E, [(0, 0)])[0][(20, 20)], 1))                  # 28.3
```

**Crowns over the void pass `trees.scatter` unless `allowed` is given.** `zone` says where a trunk may stand, not
where a crown may reach, so a wood drawn to the island's edge hangs leaves over the void. The default could
refuse any block over a column with no ground.

### What in the guide was unclear

- **Which walk the goal rules are against.** GO1, GO3 and GO4 are quoted in blocks of walk; the plan's octile walk
  and the read-back's four-way walk give different blocks.
- **Where a tunnel's mouth belongs in the plan.** The guide asks for "every layer under the surface, each with its
  own floor height and its own way in", but not how a way in from the void (by bridging) is stated.

### Wanted, how hard, what it would take

| What I wanted | How hard it was | What a library or studio feature would need |
|---|---|---|
| A plan raster from a heightfield half with my own kinds | easy, 10 lines | `Raster.from_half(H, K, kinds, op)` completing both by the symmetry |
| An approach priced by its way | easy, 15 lines | `plangraph.via(edges, starts, waypoint, targets)` |
| A tube reached from a build zone | fiddly, by `extra` edges | `graph(bridge=...)` joining zone cells to any storey's cell beside them |
| A core that is known to leak | 6 lines in the read-back | `Core(vent=...)` stamping the vent, and `check` measuring the open drop against `leak` |
| One number for "the walk" | not solved | the goal rules stated against one walk, and the library's two walks agreeing on diagonals |
| Paths and floors laid in cells | 10 lines | `route.pave(pattern="cell", size=3)` and a `facade.cells` field |

## After the playtest

**The kit now carries a diamond pickaxe, because the core's casing is obsidian.** An iron pickaxe cannot break it. `common.kit` took a `pick` argument that defaults to the iron pickaxe, so the other boards are unchanged, and this board passes `diamond pickaxe` for slot 2.

**The core is raised three blocks, and the obsidian hull under it is gone.** The casing now spans y 55 to 59, written into `red-core-region` as 55 to 60, so it hangs four blocks over the bowl's top. The vent, a five-by-five well seven deep with an obsidian floor and a ring of obsidian walls, is no longer carved: the bowl is ordinary ground down to the platform. The only obsidian left in the cone is the core's own shell.

**A stone brick platform sits under the core in a shallow pit.** A five-by-five pit three deep holds a platform of stone brick, polished andesite and cracked brick at y 47, with a short flight of stone brick stairs up its north row. Lava falls eight blocks onto it against a leak of five, so the core still leaks. The bowl's floor beside the casing is 51, so a player can now walk under the casing, which the walk reads back.

**The crag was raised with the core, so the plan's rule for it still holds.** With the casing's top at 59 the crag stood five over it and none of its top cells saw the casing, where the plan wants 4 to 12 and over 5%. The crag's top is now 67, eight over the casing's top as before, and 6% of its top cells see it. The plan check reports no row missing.

**There are nine more lava pools in the ash, eleven to a half.** Each is two to four blocks in radius with an uneven edge, sunk two blocks deep with obsidian under it and a rim of obsidian, coal block, cobble and black clay at ground level. Sites are flat ash at least 7 blocks off every road and path, 9 off a building, 6 off the pond, 8 off the sinkhole, 6 off the tube and 24 off the core, so none is on a way a team walks.

**The ash is coloured in patches, not noise.** Three blob masks cut from smooth noise, 11 to 17 blocks across, lay six-sided dark oak logs (log data 13), soul sand and coarse dirt with gravel flecks. On the red half the logs cover 6.1% of the top blocks in 9 patches, the largest 314 blocks, soul sand 4.1% in 19 patches and coarse dirt 6.8%, with its largest patch 107 blocks. Roads and paths are paved over them as before.

**Seven dead trees stand on the ash in each half.** Each is a bare trunk of dark oak or spruce six to ten blocks high with three or four limbs of lying logs that turn up at their ends, a twig, and roots lying out at its foot, with no leaves. Three of the seven stand within twelve blocks of a pool and the rest are spread across the flats, at least 14 blocks apart and clear of the paths.

**The island's rock is banded, patched, ore-flecked and hung with stalactites.** Beds three blocks thick dip across the island in stone, andesite, polished andesite and cobble, with a seam of coarse dirt or mossy cobble now and then. Patches of cobble, mossy cobble, andesite, coarse dirt and gravel come from three-dimensional noise, and gravel is laid only over solid rock, with a sweep after the tube's carve for any left over air. The exposed rock faces read back 21% stone, 24% andesite, 9% polished, 19% cobble, 9% mossy, 10% coarse dirt and 2.5% gravel, where they were 53%, 23%, 15%, 5%, none, 0.4% and 0.1%.

**Ore and hanging bits break up the faces and the underside.** The 306 ore faces read 147 coal, 90 iron, 34 gold, 24 redstone, 8 lapis and 3 diamond, in specks of one to three blocks, where there were 5. Stalactites of 4 to 10 blocks with mossy tips hang under the island's rim and 356 vines trail down its faces on the red half, and blue's half is its turn.

**The walks hold.** Spawn to its own core reads 40, to the enemy's core by bridging 131, into the enemy's tube 111 and onto its crag 142, the same as this board built before the change on the current library (the committed 0.10 figures were 52, 139, 118 and 158). The first block under the casing is 8 down against a leak of 5. Objectives with a problem 0, footing problems 0 (a first build had 22 gravel blocks over the tube's air, now swept), map.xml valid with no issues.
