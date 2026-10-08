# Riftwater on pgmvox — port report

**Riftwater was rebuilt from nothing on pgmvox 0.6.0, and the whole board came across.** The layout, the
places, the four monuments, the terrain, the river, the rift, the town, the village, the cave, the mine and
the cellar are all there. The port is 2,041 lines of scripts against the original's 3,379 lines of Python.
About 900 of those 2,041 are local code that a library could hold, and the friction log below names each piece.

```
cd freeform/lib && python3 -m pgmvox.run ports/riftwater --build /tmp/riftwater-port-build --skip write
```

The run takes about 30 seconds: plan check, sketch, generation (5 s), map.xml, renders and the read-back.
Region files were not written (`--skip write`); `world/map.xml` is the only file under `world/`.

## What the port covers

| Original feature (PLAN.md, REPORT.md) | Status | How |
|---|---|---|
| Board 240 × 176, mirrored across the rift (`x' = -1 - x`) | library | `plan.Symmetry("mirror_x")`, `orient.turn_world` |
| Teams of 16, spawns, observer point, spawn protection | library | `objectives.Spawn`, `Observer`, `Teams` |
| Four monuments, two obsidian blocks floating two over the ground | library | `objectives.Destroyable`, mirrored by `Objectives.add` |
| Blue's wool on the watch tower | library | `turn_world(recolour=...)` |
| Kit, rift build zone, void filter, max build height | library + local XML | `mapxml.Doc`, `E` (no kit or rectangle helper) |
| Rift lip: ragged, bays, held straight at the town, Old Bridge, falls | local | `plan._rift_edge` |
| Town climbing 49 → 52, chapel hill, field slope, ridge, spurs | local + library | noise and smoothstep from `pgmvox.noise`, `landform.terraces` for the ridge steps |
| Square and green levelled into the ground | library | `landform.blend` |
| Lone Oak Knoll | library | `landform.spire` (with an ellipse by stretching z) |
| River valley: bluff on the town side, gentle field bank | local | asymmetric bank formula in `plan.land` |
| River channel, two reaches (pond 48, river 45) and the weir as a fall | library | `landform.watercourse` over a pre-shaped valley |
| Mill pond with its spit and outlet | local | ellipse with noise |
| Spawn shoulder (oval spur levelled at 59) | local | 5 lines in `plan.land` |
| Underside: sheer under the rift, tapering elsewhere | local | per-column bottom clipped after `terrain.lay` |
| Rock in andesite beds following the surface, cobble flecks | library | `terrain.Strata`, `beds` with the heights as the offset |
| Ground painted by slope | library + local | `terrain.lay` with `by_angle`; patches and the sandy river lip local |
| Falls pouring into the void | local | `ground.falls` |
| Biomes (plains, forest, river) | local | 3 lines on `World.biome` |
| Streets, lanes and paths graded into the ground | library | `landform.grade` per route, `keep` the ones laid before |
| Route surfaces (hard, soft, forest) | library | `route.pave` through a local guard (`works.Guarded`) |
| Outlet footbridge on trestles | library + local | `route.pave` lays the deck and rails over water; trestle legs local |
| 29 houses: town, village, stone styles, signs | library | `build.House`, `build.house`, `build.site`, custom style dicts |
| Chapel belfry and spire, watch tower with battlement | local + library | `works.tower`; `build.parapet` for the crenels |
| Spawn terrace and its steps | library | `facade.carpet`, `build.stairs` |
| Market Square floor | library | `facade.carpet` with `first_of(border, tiles)` |
| The gaol over its cellar, ladder down | local | `under.cellar`, `under.gaol_ladder` |
| Stone Bridge: hump-backed, arched, keystoned, stair-stepped | local | `works.stone_bridge` |
| The Old Bridge's broken stub and iron ties | local | `works.old_bridge` |
| The mill, its race, wheel and weir | local | `works.mill` |
| Headframe with winding wheel, shaft and ladder | local + library | `works.headframe`; the shaft is `pgmvox.under.shaft` |
| Engine house stack, smithy, well, spoil heap | local | `works.ironhollow` |
| Falls Cave: gallery, branches, lake chamber, pillar hall, grotto, alcoves | library + local | `pgmvox.under.tunnel` and `chamber`; pillar hall and grotto local |
| Cave mouth ledge, vines, dressing, stalagmites, ores, lake | library + local | `pgmvox.under.dress_cave`; `under.mouth` and `under.lake` local |
| The sinkhole | local | funnel in the plan's heights, rubble in `under.sinkhole` |
| Ironhollow Mine: galleries, sets, rails, stairs, adit, chests | library + local | `pgmvox.under.gallery_line` and `gallery`; adit portal and chest local |
| Trees from the tree showcase, crown spacing, the Cutting's ring, the knoll oak | library | `pgmvox.trees.load`, `plant`, `scatter` (reads the original's `trees.json`) |
| Wheat field, ditches, fence and gate, scarecrow | local | `dress.build` |
| Grass, ferns, flower drifts; vines down the rift face | local | `dress.build` |
| The Cutting's stumps and log piles | local, reduced | stumps and two piles; no sawhorse or sledge |
| Street lamps | local | `works.lamps` |
| Chapel pews and altar, mill sacks, smithy furnishings | local, reduced | a few blocks each |
| Plan sketch, annotated top-down, iso, x-ray, cutaways, elevation | library | `sketch`, `render` |
| Read-back walks, objectives, footing | library | `walk`, `Objectives.check`, `audit.footing` |
| Barn, haystacks, hay cart, jetty and rowboat, spring off the ridge | not ported | — |
| Market stalls on the square's west edge | library | `pgmvox.props.stalls` |
| Village gardens, benches, boulders, fallen logs, hedgerows | not ported | — |
| Worn ground patches, furnishing inside every house, door paths | not ported | — |
| Chapel's tall windows, the wing and lean-to roofs crossing their main ridges | not ported | the library's house is one rectangle |
| Region files (`world/region`) | not written | `--skip write`, as asked |

## How it compares

### Renders side by side

| View | Original | Port |
|---|---|---|
| Plan sketch | `opus55-freeform-riftwater/renders/00-plan-sketch.png` | `renders/00-plan-sketch.png` |
| Annotated top-down | `.../renders/05-topdown-annotated.png` | `renders/05-topdown-annotated.png` |
| Board from the south-east | `.../renders/30-iso-board-se.png` | `renders/30-iso-board-se.png` |
| Board from the other side | `.../renders/31-iso-board-nw.png` | `renders/31-iso-board-sw.png` (the library has no north view) |
| The town | `.../renders/33-iso-town.png` | `renders/33-iso-town.png` |
| Ironhollow | `.../renders/34-iso-village.png` | `renders/34-iso-village.png` |
| River and mill | `.../renders/35-iso-river-mill.png` | `renders/35-iso-river-mill.png` |
| The falls | `.../renders/38-iso-rift-falls.png` | `renders/38-iso-rift-falls.png` |
| Underground x-ray | `.../renders/40-xray-underground.png` | `renders/40-xray-underground.png` |
| Section at z 3 | `.../renders/10-section-falls-cave-z3.png` | `renders/10-section-falls-cave-z3.png` |
| Section through the cellar | `.../renders/12-section-cellar-gaol-x-52.png` | `renders/12-section-cellar-gaol-x-52.png` |
| Section through the shaft | `.../renders/13-section-mine-shaft-z56.png` | `renders/13-section-mine-shaft-z56.png` |
| Rift face elevation | `.../renders/52-elev-rift-face-red-from-rift.png` | `renders/52-elev-rift-face-red-from-rift.png` |

**From above and from the south-east the two boards are hard to tell apart.** The places sit where they did,
the town climbs to its square, and the twin falls face each other across the rift. The port's ridge shows more
bare rock, because `landform.terraces` cuts its steps harder than the original's half-pull toward them did.

### Read-back numbers

From `renders/walks.txt` and `renders/plan-check.txt`. The built walk opens doors and takes no running jumps
(see the friction log for why).

| Walk | Original (built) | Port plan | Port built |
|---|---|---|---|
| Spawn → own north monument (square) | 63 | 65.0 | 65 (red and blue) |
| Spawn → own south monument (green) | 81 | 83.4 | 83 (red and blue) |
| Spawn → mine adit | 23 | 25 | 21 |
| Enemy spawn → either monument, on foot | not reached | not reached | not reached |
| Cave mouth → sinkhole floor | 69 | 76 | 78 |
| Cave mouth → out of the sinkhole onto the field | not measured | — | 90 |
| Cave mouth → gaol cellar | 84 | 94 | 84 |
| Cave mouth → up the ladder into the gaol | not measured | — | 91 |
| Cave mouth → mine breakthrough | 72 | 84 | 75 |
| Cave mouth → spawn, through the mine | not measured | 172 | 103 |
| Cave mouth → up the shaft onto the headframe's collar | not measured | — | 135 |
| Air to bridge: Old Bridge / falls / south fields | 8 / 20 / 20 | 8 / 20 / 22 | as planned |

- `Objectives.check`: no problems (both spawns stand, all four monuments are obsidian, no shared ground).
- `audit.footing`: 0 problems (12 gravel blocks over air on the spoil heap were found and fixed).
- The studio's reader (`data/read_mapxml.cs`) reads `scripts/map.xml` as valid: 2 teams, 2 spawns, 4
  destroyables, 1 kit, 5 apply rules, no issues.
- 1,001,926 blocks (original 1,007,258), 110 trees (106), 16 tile entities (16).

### Line counts

| | Lines |
|---|---|
| Original scripts, Python (`plan`, `terrain`, `underground`, `buildings`, `house`, `dressing`, `mc`, `mirror`, `noise`, renderers, walk ...) | 3,379 |
| Port scripts, all | 2,041 |
| of which plan data (places, routes, houses, cave and mine waypoints) | about 190 |
| of which local code a library could hold | about 900 |

The 900 lines break down as follows.

- Tunnels, galleries, cave dressing, shaft and cellar (`under.py`): about 250.
- Tree planting with crown spacing, ground cover and the crop field (`dress.py`): about 150.
- Bridges, the tower, the mill wheel and the headframe (`works.py`): about 220.
- Terrain helpers: the outline with bays, asymmetric banks, the pond, the per-column underside, per-place paint
  and the falls: about 120.
- Plan glue: house spec, door prediction, tube floor cells, the mine line, the pave guard, the door-open walk:
  about 160.

## Friction log

### What the library could not do, and what was written locally

- **A plan raster for terrain.** `Raster.rect`, `poly`, `where` and `flight` take one height per call; a board
  whose ground is a heightfield has a height per cell. `plan.build` assigns `R.H` and `R.K` directly and mirrors
  the arrays itself (`plan.full`). The library would want `Raster.from_heights(H, K)` that draws the image half.
- **The sketch's heights on a heightfield.** `MapPanel.heights` labels every connected run of one kind at one
  height, which on terrain is thousands of labels. The sketch passes `kinds=[...]` to label built floors only;
  a terrain board wants contour lines (`MapPanel.contours(R, every=5)`).
- **House footprints and doors before building.** `build.house` decides its centre snapping and its door only as
  it builds, so the plan cannot draw a door or check a road against a footprint without copying that logic.
  `plan.spec` and `plan.door_cell` (30 lines) re-derive both, and `works.houses` raises if the two disagree.
  The library wants `House.footprint()` and `House.door_cell()`.
- **A house's door on its short side.** `House.door` is ±v, a long side, and the ridge runs along `L`. A door
  on the gable end needs `L < W` on purpose, which works but reads backwards; a `door="s"` in world terms
  would be clearer.
- **One rectangle per house.** The original's tall house with a low wing, the big house with its lean-to, and
  the watch house with its tower are built as separate houses side by side; their roofs do not meet.
- **Towers.** The chapel belfry and the watch tower are `works.tower` (45 lines): masonry walls, corners, a
  ladder, openings, and a spire or a battlement. Only the battlement is the library's (`build.parapet`).
- **Bridges.** The stone bridge (arch soffit, keystone, stair-stepped deck), the broken Old Bridge and the
  trestle legs are local (95 lines). `route.pave` lays a flat plank deck over water and nothing else.
- **`route.pave` has no mask.** It writes every cell within half its width and clears three blocks over each,
  so a street laid past a house takes its wall out. `works.Guarded` is a ten-line world proxy that refuses
  writes to protected columns. `pave(..., keep=mask)` like `landform.grade` has would remove it.
- **`landform.watercourse` chooses its own levels.** Its bed follows the ground down; a board that names its
  water levels (pond 48, river 45, a weir at x −66) has to shape the valley first so the levels come out. A
  `levels=[(s, y), ...]` argument would say it directly. The bank is also symmetric; the town's bluff and the
  field's gentle bank stay local.
- **`watercourse` interpolates across its falls.** The bed is sampled every block and read back with
  `np.interp`, so the column at a fall gets an in-between level: the weir came out 48, 47, 45.
- **`landform.scarp` is a cliff, not a ridge.** It jumps to half its height at the line; the original's ridge
  rises over fifteen blocks. The ridge stayed local, with `landform.terraces` for its steps.
- **`landform.spire` is round.** The knoll is an ellipse; the port stretches z before calling it.
- **`terrain.lay` paints by slope only.** `top(deg, h)` gets no position, so patches of andesite and coarse dirt
  on a mid slope and the sandy lip by the river are a second pass in `ground.lay_ground`.
- **One floor height for an underside.** `terrain.lay(from_y=...)` and `terrain.underside(top_y=...)` take one y.
  A floating island with relief needs a bottom per column; the port lays from y 3 and clears below its own
  bottom array. `lay(bottom=array)` would do it.
- **No tunnel.** `solid.tube` is round; a walkable cave needs a level floor and must stay under the surface.
  `under.carve` clamps the floor by arc length along the branch and keeps three blocks under the plan's ground.
  The library wants `solid.tunnel(path, radii, floor)` and a `carve(w, solid, below=H - 3)`.
- **No gallery, shaft, cave finish, tree source, field or ground cover.** The mine (timber sets, rails on the
  level, stairs on the rises), the shaft, the cave's floors and stalactites, planting whole trees with crown
  spacing, the crop field and the flower drifts are all local, about 400 lines together.
- **No kit and no rectangle in `mapxml`.** The kit is written with `E` by hand and the build zone as an `E`
  rectangle; both are short, but every PGM board has a kit.
- **`render.iso` has two corners.** `corner` is `"se"` or `"sw"`; the original's north-west view has no
  equivalent, so the port's second board view is from the south-west.
- **The x-ray keeps houses and tree crowns.** `xray_shell` keeps every roofed void, and a house or a crown is
  one. `renders.py` clears everything above the plan's ground in a copy first; an `xray(below=H)` would do it.
- **The plan's jump search takes 80 seconds.** `plangraph.jumps` over the 240 × 176 raster took 80 s and found
  no jump across the rift (it reads the ground storey only, so the Old Bridge stubs on storey 2 are invisible
  to it). `plan_check` measures the rift gaps itself (`rift_gaps`) and runs its graph with `jumps=False`.

### Library bugs, with reproductions

**`walk.walk` gives order-dependent distances when jumps are on.** It is a breadth-first search over a FIFO
queue, but a jump costs `max(|dx|, |dz|)` moves, so a far node can be settled before a nearer one and its
neighbours keep the larger number. On the port, red's walk to its green is 81 and blue's is 83 on a board that
is the exact mirror. A minimal reproduction, a floor with mirrored holes:

```python
import numpy as np
from pgmvox import World, walk, B
rs = np.random.default_rng(1)
w = World(-10, -10, 20, 20, sy=6)
w.fill(-10, 1, -10, 9, 1, 9, B.STONE)
for i, k in np.argwhere(rs.random((10, 20)) < 0.35):
    x, z = -10 + int(i), -10 + int(k)
    w.set(x, 1, z, B.AIR); w.set(-1 - x, 1, z, B.AIR)          # and its mirror
w.set(-8, 1, 0, B.STONE); w.set(7, 1, 0, B.STONE)
a = walk.walk(w.ids, [(-8, 2, 0)], w.x0, w.z0)
b = walk.walk(w.ids, [(7, 2, 0)], w.x0, w.z0)
print((a != b[::-1]).sum())     # 91 cells differ; (-10, 2, -10) is 16 from red, its mirror 17 from blue
```

The fix is a priority queue (Dijkstra) or a 0-1/bucket queue. The port's read-back walks with `jumps=False`,
which is exact and agrees with the plan to the block (65 and 83).

**A ladder is not entered from its top when `max_drop` is set.** Stepping off the collar into the shaft is a
fall, and the fall loop stops only on a standing cell, so it passes every ladder block and gives up after
`max_drop`. Climbing up works. Reproduction:

```python
from pgmvox import World, walk, B
w = World(-3, -3, 6, 6, sy=12)
w.fill(-3, 0, -3, 2, 0, 2, B.STONE); w.fill(-3, 8, -3, 2, 8, 2, B.STONE)
for y in range(1, 9):
    w.set(0, y, 0, B.LADDER, 2); w.set(0, y, 1, B.STONE)
for md in (None, 3):
    d = walk.walk(w.ids, [(-2, 9, 0)], w.x0, w.z0, walk.MoveRules(max_drop=md))
    print(md, d[0 - w.x0, 1, 0 - w.z0])     # None: 2, 3: -1
```

A falling player who passes a climbable block should be caught by it. On the port, the walk down the
headframe's shaft is "not reached" for this reason, and the walk up it is 135.

**Doors are walls to the walk.** `blocks.PASSABLE` holds no door, so `walk.walk` stops at every door; the
spawn is inside the watch house and nothing was reachable without jumps. With jumps on, the walk still found
its way out in 120 moves by a route the port could not account for. `walk.py` opens the doors in a copy of the
ids. The walk wants doors passable (`MoveRules(doors=True)`), and the original board's own walk did that.

**`plangraph.route` and `arrivals` answer `None` for an unreached target, while `dijkstra`'s `D` defaults to
infinity.** Formatting the table with `math.isinf` raised on `None`; `plan_check.cost` maps one to the other.

### Conventions and documents that tripped me

- `Raster.flight` defaults to the kind `"stair"`, which the board's kinds list must contain; the first build
  raised `KeyError: 'stair'` from inside the library.
- The door `facing` that `build.house` returns is a `(dx, dz)` tuple, not one of the letters the README calls
  "one vocabulary everywhere".
- `MapPanel.storey` labels every piece by height and blends; on an underground storey of hundreds of
  little pieces the labels must be turned off (`label=False`).
- The README says routes are found, not drawn. Riftwater's lanes are drawn on purpose (each has a reason
  and a place), so the port used `landform.grade` and `route.pave` and never `route.find` or `network`. That
  works, but the README reads as if drawn routes were not the library's business.
- `plangraph.walkable` and `graph` were written for roofs over the ground. They take a cave under it as
  storey 1 without change, which is worth saying in the docstring: it is how the port planned the cave.
- `terrain.beds(strata, offset)` with the heights as the offset makes beds follow the surface, and `Strata`
  then needs a negative `start`. That works but is not obvious from either docstring.

## Plan and sketch

**The plan was detailed before anything was generated: every height, place, route, building, cave branch and
the mine was data in `plan.py`, read by the checker, the sketch and the generator alike.** That was possible
because the original's coordinates existed; the port reused them. The sketch drew the board, the underground
as storey 1, three sections, red's walks and a check table, and the check table caught five problems before
the first block was laid.

- **Four buildings stood on roads** (the town hall on North Lane, the mill on Mill Lane, two cottages on the
  village paths). The original hid this by paving round built columns. `build.Claims` found them; three routes
  were re-drawn and North Lane narrowed to a lane where it passes between the hall and the next house.
- **The sinkhole was not climbable.** At 1.6 blocks a block its risers were two high; it is now a block a
  block over a 10.5 radius, centred on the cave branch's end so the cave walks into its floor.
- **The lake chamber's floor sat two under the gallery.** It was raised a block.
- **The cave's floor cells took the first sample in reach, not the nearest,** so the north branch met the
  cellar two blocks low; the nearest sample now wins.

Three problems were found only once the world was built and walked.

- **The gaol's ladder stood inside a cell behind an iron door,** as in the original, so nobody came up it. It
  moved to the cellar's guard room, on its east wall.
- **The mine's timber sets put a beam at head height over every stair,** so the gallery was not walkable from
  the cave to the spawn (it was not in the original either). Sets now stand only on level floor.
- **The shaft's ladder went a block past its walls** and hung on nothing; it now stops at the collar.

**What had to be decided while building was mostly about blocks, not places.** The rock beds, the paint
patches, how a tower meets a house, where a sign hangs and which way a ladder faces were decided in gen. The
plan was enough for every place and every walk: the built walks agree with the plan's to the block for both
monuments.

## After review: the board's pieces moved into the library

**The cave, the mine, the shaft and the trees now come from the library.** `pgmvox.under` holds the tunnel,
chamber, cave finish, gallery and shaft this port had written locally, and `pgmvox.trees` plants the original's
cut trees. What stays local is where they go and the pieces only this board has.

**The walks did not move.** Every number in `renders/walks.txt` is the one the local code gave, and the carve
removed the same 5,568 blocks. One tree fewer stands (53), because a tree now rests on the lowest ground under
its whole bottom row, as the studio seats it.

