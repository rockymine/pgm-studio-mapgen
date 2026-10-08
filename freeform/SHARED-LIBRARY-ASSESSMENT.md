# Shared library assessment: the twenty freeform generators

What the twenty `opus55-freeform-*` folders share, how the copies have drifted, and what a shared library and
the studio should take from them. Every claim here was read off the code. File references are
`<board>/scripts/<file>:<function>`, with the `opus55-freeform-` prefix dropped.

The analysis is weighted toward the four things the author says freeform adds over the studio: tighter
block-level control, more patterns, terrain fidelity, and the plan phase (sketch and check before building).

## 0. Headline

**About a third of the code is copies.** The 20 folders hold about 50,000 lines of Python and C#. Of these,
15,800 lines are copies of eleven helper modules whose distinct content is about 1,400 lines.

**The copies were copied, not shared, and they drifted.** Fixes reached the boards built after them and never
the boards before. One fix also went missing from later copies of the same file. Nine of the twenty walks
still carry a headroom check that can never fire (§1.3).

**The repeated logic that matters most is in the plan phase.** It is the plan raster with symmetric flights,
the plan-graph walk with a jump audit, the Minecraft 1.8 movement physics, and the sight checks. Each exists
in three to eight parallel copies with different signatures. None of it has a counterpart in the studio:
the studio's walk is a CTW kit-budget walk with no ladders, jumps, pads, knockback or fall damage.

**The REPORT tables say the same thing.** The commonest studio-feature asks are:

- round-trip validation for gamemodes the studio refuses or does not read (11 boards);
- objective pieces that write their own XML regions (12 boards);
- plan-time reads: routes, jumps, sight and arrival times (8 boards);
- physics reads: pads, falls, knockback, no-catch and no-stand (7 boards);
- team colour that a symmetry turn swaps (7 boards).

**Recommended first moves.** First, extract `blocks` plus `orient`, which ends the drift and fixes the bugs.
Second, extract `move` plus `plangraph`, the 1.8 physics and the plan walk. Third, extract `plan` plus
`sketch`, the raster and its true-scale drawing. The studio's matching additions would be an adventure-mode
walk, a physics read (pads, falls, knockback) and its existing reads served over a world that is not a
stored map.

## 1. The copied helpers

### 1.1 Inventory

"Variants" counts distinct file hashes. "Imported by" lists the boards whose own scripts import the module.
A copy no script imports is dead.

| Helper | Copies | Variants | Imported by | Dead copies |
|---|---|---|---|---|
| `noise.py` | 19 | **1** (identical) | 15 boards | calcite, penstock, riad, saltgate |
| `mc.py` | 19 | 4 | all | — |
| `render_iso.py` | 19 | 9 | all 19 with a world | — |
| `write_world.cs` | 20 | 2 | `build.sh` (19 boards; sunwell has none) | — |
| `walk_core.py` | 8 | **1** | copperline, curio, lanterndrop, lanternpass, saltgate, sunwell | **spark, loomfall** (copied, never imported) |
| `cutaway.py` | 9 | 2 | 7 boards | curio |
| `geometry.py` | 8 | **1** | gullhaven, hollowcrown, lantern-karst, stratum | calcite, penstock, riad, saltgate |
| `rotate.py` | 7 | 2 | 6 boards | calcite (its plan rotates itself) |
| `house.py` | 6 | 2 (two unrelated modules, one name) | copperline, gullhaven, hollowcrown, riftwater, saltgate | hollow-mesa |
| `mirror.py` | 3 | 1 | penstock, riftwater, stratum | — |
| `pad.py` | 2 | 1 | calcite (as a script) | riad |

**Twelve copies are dead.** They were copied "in case" and then never imported. A shared package removes the
temptation.

### 1.2 How each one drifted

**`mc.py` grew by appending, one board at a time, and stopped growing at riad.** Its lineage is riftwater
(203 lines) → hollow-mesa (+`RED_SANDSTONE`, `CACTUS`, `ACACIA_STAIRS`, `ACACIA_FENCE`,
`DARK_OAK_FENCE_GATE`) → frostholm and its siblings (+`ICE`, `SNOW`, `PACKED_ICE`) → riad and its successors
(+`World.banner`, 221 lines). The nine boards built before riad cannot place a banner.

Later boards needed ids the table lacked, and defined them locally instead of adding them to `mc.py`:

- `QSTAIRS = 156` and `SLIME = (165, 0)` in `calcite/gen.py`;
- `SEA = (169, 0)` in `penstock/gen.py`;
- `SEA_LANTERN`, `BEACON` in `riad/gen.py`;
- `SEA_LANTERN = 169`, `PRISMARINE = 168` in `stratum/facade.py`;
- raw `134` and `109` stairs in `saltgate/gen.py`.

**`render_iso.py` forked into two lineages, each growing its own colour table.** riftwater → hollow-mesa
added mesa colours, and cloudhaven added ice and snow and made the snow layer (78) transparent. From
cloudhaven it split:

- hollowcrown and stratum each added glass colours, and stratum also added prismarine and sea lantern;
- lantern-karst (copied as-is to penstock) added tea leaves, prismarine, bedrock, glowstone and redstone. It also changed
  the colour of grass (2) from `(130,140,75)` to `(110,150,85)`. And it fixed a real bug: block 36 marks the
  build area at y 0 and is now drawn invisible (`present = (ids > 0) & (ids != 36)`);
- calcite added quartz stairs and slime;
- copperline (copied unchanged to 8 later boards) folded those into the dict and added red sandstone, sandstone stairs,
  beacon and banner;
- curio added about 60 ids in one loop, including huge mushrooms, ores, nether brick, hoppers and quartz
  variants.

**The block-36 and grass fixes never reached the six boards built before lantern-karst.** Curio's 60-id table
reached no other board. Every renderer before curio draws those ids in its fallback magenta.

**`rotate.py` lost a fix on its way forward.** hollow-mesa's copy turns iron trapdoors (167) and powered,
detector and activator rails (27, 28, 157), and swaps all four rail slopes. The later variant, shared by
cloudhaven, frostholm, hollowcrown, lantern-karst, calcite and gullhaven-dtm, generalised the half to a `red`
mask. But it dropped those three rail ids and the iron trapdoor. A powered rail or an iron trapdoor on any of
those boards comes out wrong on blue's half.

**`cutaway.py` in saltgate is a cross-board import.** It puts `../../opus55-freeform-gullhaven/scripts` on
`sys.path`, a line copied from gullhaven-dtm, which does the same in `compose.py`, `renders.py` and
`walk.py`. Saltgate's cutaway therefore draws with gullhaven's `render_iso` colour table, not its own.
`hollowcrown/cut_trees.py` likewise reads `trees.json` out of riftwater and frostholm.

**`write_world.cs` has two versions.** The second adds the `Banner` tile entity. The nine boards on the first
version cannot write a banner even if their `mc.py` placed one.

**`house.py` is two different modules under one name.** riftwater and hollow-mesa have an axis-aligned
house: `site`, `roof_gable`, `house`, `furnish`. hollowcrown, gullhaven, saltgate and copperline have a
rewrite that builds "houses at any angle": `Frame`, `rect_mask`, `boundary`, `axis_of`, `footprint`, `build`.
The second keeps riftwater's style names but not its code.

**`build.sh` carries a fix that never reached the first two boards.** 17 boards run
`(cd /tmp && dotnet run "$here/write_world.cs" …)`. riftwater and hollow-mesa run `dotnet run write_world.cs`
inside `scripts/`. Every `build.sh` hard-codes `/home/user/pgm-studio` and
`tools/PgmStudio.RoundTrip/bin/Debug/net10.0`.

### 1.3 The walk drifted most, and nine boards still carry the old one

**There are three generations of the voxel walk.** `walk_core.py` says in its own header that it came from
gullhaven.

| Generation | Boards | Behaviour |
|---|---|---|
| 1 | riftwater, hollow-mesa, cloudhaven, frostholm, hollowcrown, stratum, lantern-karst, penstock, calcite | Steps of +1..−3 only, so any drop over three blocks reads as a wall. The headroom test is `if dy == 1 and not st[x, y, z] \| True: continue`, which is never true. |
| 2 | gullhaven, riad (own copies in `walk.py`) | Headroom checked (`passable[x, y + 2, z]`); falls of any height; running jumps over 1–3 gaps (`JUMPS`) |
| 3 | `walk_core.py` (8 copies) | Generation 2 as a module, with `push()` and `nearest()` |

**`walk_core.py`'s docstring disagrees with its code.** The docstring says "three blocks at no cost, five at
the price of a heart". The code says `# fall damage is off: any drop`.

### 1.4 Six block-class sets that should be one

Each tool decides "what a player walks through", "what is ground" or "what light passes" with its own set.
The sets disagree at the edges:

| Set | Where | Notes |
|---|---|---|
| `NOT_GROUND` | `mc.py` | what `World.top()` skips |
| `TRANSPARENT` | `render_iso.py` | grows per board (78, then 36 and 55) |
| `PASS` | every `walk.py`, `walk_core.py` | 36 and 55 added at penstock; carpet 171 and banners 176/177 only from gullhaven on |
| `SEE_THROUGH`, `FORBIDDEN`, `GRAVITY`, `TORCH_ON`, `LADDER_ON` | `curio/plotkit.py` | the only attachment table in the corpus |
| `SOLIDISH` | `hollow-mesa/audit.py` (a lambda) | — |
| `WALK`/`WALKK` | each `plan_check.py` | plan kinds, not block ids, but the same idea |

## 2. Repeated logic in the per-board scripts

Similarity is graded: **identical**, **near** (renames and constants only), **parallel** (same algorithm,
different signature or data model), **idea** (same intent, written again).

### 2.1 The plan as rasters

| Pattern | Boards (file:function) | Similarity |
|---|---|---|
| `Raster` with `H` (floor height) and `K` (kind) over `X_MIN..X_MAX × Z_MIN..Z_MAX`, `ix`/`iz`, `KINDS` dict, `WALK` set | calcite, riad, saltgate, copperline, gullhaven, lanternpass `plan.py:Raster` | parallel |
| `rect(x0, x1, z0, z1, h, kind, both=True)` writing a rectangle and its symmetric image | calcite, riad (`both`); saltgate, copperline (no symmetry argument); lanternpass (`top=`) | near |
| stair flights: `flight`, `flight_x`, `flight_z`, `_stair` recording `stair[(x,z)] = "+x"` | calcite `Raster.flight/flight_z/_stair`; riad `flight_x/flight_z`; saltgate `flight_x/flight_z`; copperline `flight_x(xs, z0, z1, h0, step, rises)`; lanternpass `flight(x0, x1, zs, h0, rises)` | parallel: **four different signatures for one idea** |
| an upper storey (`U`, `UK`: roofs and decks over the ground) | riad `Raster.upper`; lanternpass `canopy` | idea |
| gates that open by stage | saltgate, copperline `Raster.gates(…, opens)` | identical |
| plan as pieces instead of a raster | lanterndrop `plan.py:pieces/links/gap`, spark `plan.py:in_ellipse/ray_at/is_floor`, loomfall `plan.py:cells/below/pattern` | idea |
| plan as polygons | lantern-karst, hollowcrown, stratum `plan.py:rect/octagon` + `geometry.py` | near |

A shared signature:

```python
class Raster:
    def __init__(self, xs: tuple[int, int], zs: tuple[int, int], kinds: dict[str, int],
                 base_h: int, base_kind: str, symmetry: Symmetry | None = None, storeys: int = 1): ...
    def rect(self, x0, x1, z0, z1, h, kind, storey=0, sym=True): ...
    def cells(self, cells, h, kind, storey=0, sym=True): ...
    def mask(self, m, h, kind, storey=0): ...                     # gullhaven's Raster.set
    def flight(self, start, rises: Dir, width, steps, h0, step=1, sym=True): ...  # one call for all four
    def gate(self, x0, x1, z0, z1, h, opens: str, sym=True): ...
    walkable: set[str]; stair: dict[tuple[int,int], Dir]; gates: dict[tuple[int,int], str]
```

### 2.2 Walking the plan: graph, Dijkstra, jumps

| Pattern | Boards | Similarity |
|---|---|---|
| `dijkstra(E, start) -> D[, prev]` over `E[u] = [(v, w[, tag])]` | calcite, copperline, gullhaven, lanternpass, riad, saltgate `plan_check.py:dijkstra` | **near** (six copies; return `D` or `(D, prev)`; tagged or not; lanternpass adds multi-source and an exposure weight `w * (1 + k * vis[v])`) |
| `graph(...)` building 4-neighbour edges: step up ≤1, drops one-way, water at half speed, ladders, extras | the same six, `plan_check.py:graph` | parallel: each board's own kinds hard-coded in the body |
| `walkable(i, j)` | calcite, copperline, gullhaven, lanternpass, saltgate | near (saltgate adds team and stage) |
| `jumps()`: every gap 1–3 blocks, `gap = hypot(max(0, |di|-1), max(0, |dj|-1))`, landing ≤1 higher, sampled over `n = max(|di|,|dj|) * 3` points | calcite `plan_check.py:jumps`, riad `plan_check.py:jumps`, and the same rule in voxels in `walk_core.py:JUMPS/bfs` | **near**: the same formula in three places |
| `fall_cost(d, into_water)` | riad `plan_check.py:fall_cost` (free to 3, then 2 a block) | idea; gullhaven and saltgate inline `0.4` per block of climb in route length |
| `landings`, `walk_near`, `path_tags` | calcite, riad, saltgate | near |

A shared signature:

```python
@dataclass
class MoveRules:
    step_up: int = 1; drop_free: int = 3; drop_cost: float = 2.0; water_cost: float = 2.0
    ladder_cost: float = 1.8; jump_max_gap: float = 3.0; jump_max_rise: int = 1; kill_drop: int | None = None
def surfaces(r: Raster) -> dict[Cell, int]
def jumps(r: Raster, rules: MoveRules, top_at=None) -> list[tuple[Cell, Cell, float]]
def graph(r: Raster, rules: MoveRules, extra: Iterable[Edge] = (), team=None, stage=None) -> Graph
def dijkstra(g: Graph, starts, weight=None) -> tuple[dict, dict]
def route(prev, cell) -> list[tuple[Cell, str]]          # the tags: walk, drop 5, jump 2.2, ladder, pad
```

### 2.3 The 1.8 movement physics

**The same tick loop appears five times.** It is `x += vx; y += vy; vy = (vy - 0.08) * 0.98; vx *= 0.91`.

| Function | Where | What it adds |
|---|---|---|
| `fly(p, v, land_y, ticks)` | `calcite/pad.py`, `riad/pad.py` (identical) | apex, path |
| `land_of_pad(pad, v)` | `calcite/plan_check.py` | flies against the plan raster: walls, floors, lava |
| `tune(pad, target)` | `calcite/plan_check.py` | grid search of `vy`, `vh` for a landing within a block; scores `err + 0.05 * apex` |
| `fall(dy, how)`, `LEAVES` = step off / run off / sprint jump (with air acceleration 0.026) | `lanterndrop/plan.py` and inline again in `lanterndrop/sketch.py` | how far out a player lands |
| `damage(dy) = ceil(dy - 3)` | `lanterndrop/plan.py` | fall damage |
| `gentlest(dy, dist)` | `lanterndrop/plan_check.py` | the gentlest way off an edge that clears a gap |
| `knock(level, surf, sprint)` | `spark/plan.py` | horizontal 0.4 + 0.5 per level, 0.4 up, ground friction `SLIP[surf] * 0.91` |
| `below(k, x, z)` | `loomfall/plan.py` | which floor a fall from a cell lands on |

A shared signature:

```python
G, DRAG_Y, DRAG_AIR = 0.08, 0.98, 0.91
SLIP = {"default": 0.6, "ice": 0.98, "slime": 0.8}
def fly(p, v, ticks=200, accel=0.0, land: Callable[[float, float, float, float], Hit | None] = None) -> Flight
def leave_edge(how: Literal["step", "run", "sprint_jump"]) -> tuple[float, float, float]
def fall(dy, how) -> tuple[int, float]                 # ticks, distance out
def fall_damage(dy, into_water=False) -> int
def knockback_reach(level, sprint=True, surface="default") -> float
def solve_launch(origin, target, land, vy=(0.6, 2.0, 0.05), vh=(0.4, 3.0, 0.05)) -> Launch | None
```

### 2.4 Sight and exposure

| Function | Where | Model |
|---|---|---|
| `sight(a, b, eye=1.6)` | `gullhaven/plan_check.py` | eye to eye over raster column tops, 3 samples a block |
| `sight(a, b, eye=1.6)` | `riad/plan_check.py` | eye 1.6 to target +1.0; blocking kinds listed; upper storey blocks; 4 samples a block |
| `sight()` | `lanternpass/plan_check.py` | vectorised: a set of eye positions (eye **1.62**), 90 samples a line, canopy layer, returns a visibility share per cell |
| `sight(ids, x0, z0, reach)` | `lanternpass/walk.py` | the same over the built voxels |
| `_sees(passable, a, b)` + `check` | `curio/plotkit.py` | voxel ray from a ring of street eyes, through `SEE_THROUGH` |
| `openness()` | `gullhaven/plan_check.py` | distance transform to the nearest cover |

A shared signature:

```python
EYE = 1.62
def line_clear(a, b, blocks: Callable[[float, float, float], bool], per_block=4) -> bool
def visibility(targets, eyes, top: ndarray, canopy: ndarray | None = None, rng=None) -> ndarray  # share seen
def voxel_visibility(ids, eyes, targets, see_through: set[int]) -> ndarray
def openness(K, H, blockers: set[int], walk: set[int]) -> ndarray
```

### 2.5 The voxel walk and the post-build checks

| Pattern | Boards | Similarity |
|---|---|---|
| `grid(ids) -> passable, water, ladder, solid`, `standable`, `bfs`, `nearest` | all 20 `walk.py` or `walk_core.py` | three generations (§1.3) |
| `pad_flights` against the built blocks | `calcite/walk.py` | idea, a third copy of `fly` |
| catchers beside a course (blocks that would save a knocked player) | `lanterndrop/walk.py:main` | idea |
| nothing standable above the kill height inside a radius | `spark/walk.py:main`, `loomfall/walk.py:main` | idea |
| a visibility pass over reached cells | `lanternpass/walk.py:sight` | parallel to 2.4 |
| footing: gravity blocks over air, torches, ladders and wall signs hanging on nothing | `curio/plotkit.py:footing` | **only here**. riftwater's history has "fix ladder, torch, vine and reed attachments" done by hand |
| placement audit: floors over air, rock over roofs, claims overlapping | cloudhaven, frostholm, hollow-mesa, hollowcrown, stratum `audit.py` + `buildings.py:claim` | parallel (`claim` keyed on boxes in four, on cells in stratum) |

### 2.6 Terrain

| Pattern | Boards (file:function) | Similarity |
|---|---|---|
| `fbm`, `lattice`, `smoothstep`, `spline`, `polyline_distance` | `noise.py`, 19 identical copies, used in 15 | identical |
| ridged noise as `1 - abs(fbm(...))`, inline | `riftwater/terrain.py` (crag), `frostholm/terrain.py` (crag), `hollowcrown/terrain.py` (ridges), `spark/gen.py:peaks`, `curio/gen.py:ground` | near (five inlines, no function) |
| **mountain ring with a clear radius**: `t = clip((r - clear) / width)`, `ring = smoothstep`, `mass`, `big`, `ridge**2`, `gaussian_filter`, then rock and snow above a line | `spark/gen.py:peaks` (round `r`, seeds 21–24), `curio/gen.py:ground` (`r = 0.6 max(|x|,|z|) + 0.4 hypot`, seeds 31–35) | **near**: same formula, different constants |
| `slope_deg(H, mask)` by central difference with `np.roll` | riftwater, hollow-mesa, frostholm, hollowcrown `terrain.py:slope_deg` | near (hollowcrown drops the mask) |
| paint by angle: rock on steep, soil on flat, the "flat neighbours" clamp | `hollow-mesa/terrain.py:write_land`, `riftwater/terrain.py:write_land`, `frostholm/terrain.py:write`, `hollowcrown/terrain.py:write` | parallel |
| `paint_biomes(w, F)` | cloudhaven, frostholm, hollow-mesa, hollowcrown, riftwater `terrain.py` | parallel |
| rock bands by height | `hollow-mesa/terrain.py:band_table/rock_at` (weighted random beds, red one block thick), `lantern-karst/terrain.py:rock(y, tilt, rng)` (tilted beds), `lanterndrop/gen.py:rock` (`y//6 % 7`), `lanternpass/gen.py:rock` (`y % 9`), `sunwell/gen.py:rock` (`y//5 % 7`), `curio/gen.py:ground` and `spark/gen.py:peaks` (andesite by noise sign) | parallel: **seven banders** |
| snow lines | `curio/gen.py:ground` (`> G+62`, or `> G+52` where noise is positive), `spark/gen.py:peaks` (snow over 112), `frostholm/dressing.py:snow_on_crowns` | idea |
| floating-island undersides | `riftwater/terrain.py:build_underside` and `hollow-mesa/terrain.py:build_underside` (`thick = 4 + 1.1 * edt + 4 * fbm`), `lantern-karst/terrain.py:root_bottom` (cone, flutes, spires), `lanternpass/gen.py:ridge_bottoms`, `lanterndrop/gen.py:underside(w, p, depth_k)`, `spark/gen.py:spark` (banded taper from a BFS edge distance) | parallel: six, three of them on `distance_transform_edt` |
| cloud seas and glass clouds | `spark/gen.py:clouds` (fbm deck with breaks and billows, never into mountains), `stratum/terrain.py:clouds`, `hollowcrown/dressing.py:clouds` | parallel |
| distance-to-edge by BFS or EDT | `spark/gen.py:edge_dist` (BFS), 17 call sites of `distance_transform_edt` in 10 boards | idea |

A shared signature:

```python
def ridged(shape, cell, octaves=4, seed=0, sharpness=2) -> ndarray
def ring_falloff(X, Z, clear, width, squareness=0.0) -> ndarray          # 0 inside clear, smooth to 1
def mountain_ring(X, Z, base, clear, width, height=(45, 45, 80), seeds=(21, 22, 23, 24), blur=2.5) -> ndarray
def slope_deg(H, mask=None, window=1, edge="nearest") -> ndarray        # no wrap-around
def strata(choices: list[tuple[Block, int, float]], length, seed, singles=()) -> list[Block]
def banded(period, pattern: list[Block], jitter=None) -> Callable[[int], Block]
def underside(H, land, base=4, per_edge=1.1, noise=4, floor=5, seed=0) -> ndarray  # bottom y per column
def cloud_deck(w, y, shape, seed, break_below=-0.25, billow=9, mats=..., only_air=True)
def paint_by_angle(w, H, mask, stack: list[tuple[float, Block]], depth=3)
```

### 2.7 Buildings and their parts

| Pattern | Boards (file:function) | Similarity |
|---|---|---|
| gable roof of stair rows, ridge slab, gable wall, attic air | `riftwater/house.py:roof_gable` (= `hollow-mesa/house.py`); `hollow-mesa/buildings.py:gable`; `cloudhaven/buildings.py:gable_house`; `frostholm/buildings.py:steep_roof`; `curio/gen.py:chalet`; `curio/plots/opus/crooked_house.py:main_roof` | parallel: **six gable roofs** |
| roof as a height field in a rotated frame, `r(v) = eave + (half - |v|)` | copperline, gullhaven, hollowcrown, saltgate `house.py:build` | identical |
| hip and skirt roofs, pagoda roofs | `lantern-karst/buildings.py:hip_roof/skirt_roof`, `lanternpass/gen.py:roof` | parallel |
| houses at any heading: `Frame(cx, cz, heading).local/world`, `rect_mask`, 8-neighbour `boundary` so a 45° wall is closed | copperline, gullhaven, hollowcrown, saltgate `house.py` | identical |
| site levelling under a footprint, easing ground over a margin | `riftwater/house.py:site`, `hollow-mesa/buildings.py:site`, `frostholm/buildings.py:site/set_ground`, `cloudhaven/buildings.py:level` | parallel |
| window rhythm `(y - g) % 4 == 2 and (x + z) % 3 == k` | `curio/gen.py:chalet` (k = 1), `loomfall/gen.py:house` (k = 0), a third variant in `curio/gen.py` (`x % 3 == 0`) | near |
| parapet and crenels on a rhythm | `loomfall/gen.py:house` (`(x+z) % 2`), `curio/gen.py:wall`, `riad/gen.py:parapets`, `hollow-mesa/buildings.py:adobe`, `frostholm/buildings.py` lighthouse gallery, `hollowcrown/buildings.py`, `penstock/gen.py` | idea: seven |
| timber framing (posts every four, laid log at a storey's top, infill) | `riftwater/house.py:house`, copperline-lineage `house.py:build` | parallel |
| claims (what stands where, overlaps listed) | cloudhaven, frostholm, hollow-mesa, hollowcrown, stratum `buildings.py:claim` | near |
| tree templates planted by quarter turns, turning a log's axis | cloudhaven, frostholm, hollow-mesa, hollowcrown, riftwater, stratum `dressing.py:plant` | near |

The shared vocabulary is a frame, a footprint, a rhythm predicate and a roof field:

```python
class Frame: cx, cz, heading; def local(x, z); def world(u, v)
def footprint_mask(frame, L, W, box) -> (mask, U, V)
def boundary8(mask) -> mask
Rhythm = Callable[[int, int, int], bool]                    # (s along, t up, run) -> on?
def every(period, phase=0) -> Rhythm; def rows(period, at) -> Rhythm
def roof_field(frame, L, W, eave, kind: Literal["gable", "hip", "shed", "flat"], pitch=1, overhang=1) -> dict[Cell, int]
def lay_roof(w, field, mats: RoofMats, frame)               # stair data from the frame's heading
def house(w, spec: HouseSpec, ground_at, rng) -> Claim
def parapet(w, cells, y, rhythm, mat_low, mat_high)
def site(w, footprint, floor_y, ground_at, margin=2, fill, ease=True)
```

### 2.8 Orientation and symmetry

| Pattern | Boards | Similarity |
|---|---|---|
| `STAIR_DATA = {"+x": 0, "-x": 1, "+z": 2, "-z": 3}` | calcite, copperline, riad, saltgate `gen.py` | identical |
| `stair_dir(dx, dz)` | `gullhaven/gen.py:stair_dir` (per cell from heights), `stratum/buildings.py:stair_dir` | parallel |
| door facing `{"e": 0, "s": 1, "w": 2, "n": 3}` | `riftwater/house.py`, `hollow-mesa/house.py`, `frostholm/buildings.py:door`, `hollow-mesa/buildings.py:door` | identical |
| ladder facing `{"n": 2, "s": 3, "w": 4, "e": 5}` and its inverse | `hollow-mesa/buildings.py:ladder_up`; `curio/plotkit.py:LADDER_ON` | near |
| log axis `4 if |dx| >= |dz| else 8` | `house.py:axis_of` (4 copies) | identical |
| yaw from a direction ("0 faces south, 90 west") | `spark/mapxml.py:spawn_points`, and fixed yaws in `copperline/mapxml.py:YAW` | idea |
| half-turn data table and `rotate_world` | `rotate.py`, 2 variants (§1.2) | near |
| mirror-x data table and `mirror_world` | `mirror.py` (3) | identical |
| per-board recolour of the mirrored team | `penstock/gen.py` (`TEAM = 14`, recoloured to 11), riftwater's blue wool special case | idea |
| symmetry inside the plan instead of on the world | calcite and riad `Raster(both=True)`, lanterndrop `pieces()` (`-x1, -x0`) | parallel |

A shared signature:

```python
Dir = Literal["+x", "-x", "+z", "-z"]
def stair(rises: Dir, upside_down=False) -> int; def door(facing: Dir, upper=False, hinge="left") -> int
def ladder(on_wall: Dir) -> int; def torch(on_wall: Dir | None) -> int; def sign_rot(yaw_deg) -> int
def log_axis(dx, dz) -> int; def yaw(dx, dz) -> float
Op = Literal["mirror_x", "mirror_z", "half", "cw", "ccw"]
def data_table(op: Op) -> ndarray[256, 16]                  # one table, every op, every facing family
def turn_world(w, op, keep: ndarray | None = None, axis=-0.5)
def recolour(w, mask, swaps: dict[Block, Block])            # team colour after a turn
```

### 2.9 Rasterising shapes

| Pattern | Where | Similarity |
|---|---|---|
| polygon `inside` (even-odd, vectorised), `seg_distance`, `edge_distance`, `signed_distance`, `polyline`, `point_at`, `walk_cells`, `centroid` | `geometry.py` (8 identical copies) | identical |
| `polyline_distance` | `noise.py` | **the same function as `geometry.polyline`**, in a second module |
| `disc(c, y, r, bid, d, cx, cz)` and `ring(c, y, r_in, r_out, …)` | 8 and 4 copies in `curio/plots/haiku/*.py` | identical |
| inline circle tests `(x - cx) ** 2 + …` and `hypot` | 26 more in the opus and sonnet plots | idea |
| solids of revolution (`rprof`, `shell_height`, `dome_top`, `arch_top`) | sonnet `snail_shell_house`, `teacup_tower`; opus `viaduct`, `igloo_inn` | idea |
| ellipse and ray shapes | `spark/plan.py:in_ellipse/ray_at/on_spark` | idea |
| `rect_cells`, `poly_cells` | `stratum/facade.py` | near to `geometry.inside` |

The library already exists in part outside `freeform/`: `tools/sculpt/solid.py` is a membership-test solid
with a bounding box, union and intersection. A shared `shapes` module should adopt that design, not grow a
third one.

### 2.10 Patterns

| Pattern | Where | Shape of the code |
|---|---|---|
| facade combinators: `band`, `band_from_top`, `courses`, `flutes`, `panels`, `glyph_row`, `slits`, `checker`, each a function of `(s along, run, t up, h)` answering `None`, `("inset", mat)` or `("accent", mat)`; `build(w, mass, faces=…)`; coffered undersides | `stratum/facade.py` | **the best-designed pattern code in the corpus**; one board |
| floor carpets: border by `edge = min(x - x0, …)`, medallion by `|u|/w + |v|/h`, diamonds by period, kilim steps, star by `0.7 max + 0.3 min` | `loomfall/plan.py:pattern` | five hand-written fields in one `if` chain |
| team stripes and checkers on walls | `penstock/gen.py` (`(x + z) % 4`, `(x // 2 + z // 2) % 2`) | inline |
| paving mixes | `curio/gen.py:PAVE`, `riad/gen.py:ground_block`, `saltgate/gen.py:ground_under` | inline lists with RNG |

### 2.11 map.xml

**Seven boards write map.xml with `mapxml.py`; the rest keep a hand-written `scripts/map.xml`.** Each
`mapxml.py` is `a = o.append` over literal lines.

The lines the seven repeat:

- the header (`<map proto="1.5.0">`, name, version, objective, gamemode);
- regions from plan boxes (`<cuboid min= max=>`, 12 sites);
- spawns with a yaw;
- `itemremove`;
- broadcasts;
- kill heights.

Kits differ by gamemode and are board content: stone sword, bow and arrows in copperline; a knockback stick
by stage in spark; a water bucket in lanterndrop; a seeker and a hider in curio. Objective regions are
derived from the plan: `lanterndrop/mapxml.py:hill_boxes`, `curio/mapxml.py:plot_regions`,
`copperline/mapxml.py:spawn_region`.

### 2.12 Sketches, renders and the pipeline

| Pattern | Where | Similarity |
|---|---|---|
| `px(x, z, oy[, ox]) = ((x - X_MIN) * S, oy + (z - Z_MIN) * S)` | every raster-plan `sketch.py` | identical up to `ox` |
| hillshade `shade()` from `np.gradient` | gullhaven, copperline, lanternpass, stratum `sketch.py:shade` | near |
| true-scale section from `H`, `K`, `U` | `riad/sketch.py:section`, `gullhaven/sketch.py:section`, `saltgate/sketch.py:section`, `hollowcrown/sketch.py:section`, `calcite/sketch.py:sections`, `lantern-karst/sketch.py:sections`, `lanternpass/sketch.py:long_section`, `copperline/sketch.py:unrolled` | parallel: eight |
| routes drawn from the checker's `prev` | calcite, lantern-karst, riad `sketch.py:routes` | near |
| the sketch imports the checker (`R = C.R`) and prints its numbers onto the image | calcite, copperline, gullhaven, lanternpass, riad | identical convention |
| layout: board, a second dimmed board for overlays, two section bands, a text block | gullhaven, riad (`Image.new(W, 2*H + T + 2*band + 12)`) | near |
| `renders.py`: `run(args)` around the round-trip CLI, `o(name)`, then `render_iso.render` calls numbered `01`–`4x` | all 19 | near; only the boxes and titles differ |
| `build.sh`: plan_check → sketch → gen → write_world → mapxml → renders → walk | 19 | near (§1.2) |
| `annotate.py`: labels over the top-down | 6 early boards | parallel |

## 3. What the REPORT tables ask the studio for

The 19 reports hold about 190 rows. Riftwater and hollow-mesa use a four-column variant whose last column is
the same question. Clustered by what the studio would need:

| # | Cluster | Rows from | Boards | Studio today |
|---|---|---|---|---|
| A | **Round-trip validation for the board's gamemode** | calcite (KOTH), riad (KotF), gullhaven (FFA, rage), gullhaven-dtm (DTM), penstock (TDM, scorebox), saltgate (A/D), copperline (payload), lanternpass (blitz, portals, CP), lanterndrop (CP, portals), loomfall (block drops), spark (timed kits, void portals) | 11 | Refuses `flags`, `payloads` and scorebox `<box>` outright (`docs/pgm/supported-maps.md`). |
| B | **Objective pieces that write their own regions and XML** | hills (calcite, lanterndrop), posts and the flag's banner (riad), score boxes, shops, spawners, holes (penstock), gates by stage (saltgate), track legs (copperline), portals (hollowcrown, lanternpass), monuments (gullhaven-dtm), kill height (stratum, penstock), timed region clear (curio), build-zone marker (lantern-karst) | 12 | Writes CTW, DTM and DTC goals from the plan; the rest is new. |
| C | **Reads on the plan, before building** | routes measured on every edit (calcite), jump audit (calcite, riad), sight from objectives and shooters (riad, gullhaven, lanternpass, curio), arrival times by stage (saltgate), spawn spacing (gullhaven), openness (gullhaven), widths per piece kind (lantern-karst), objective placement against both spawns (gullhaven-dtm), exposure-weighted routes (lanternpass) | 8 | Has plan-tier `PlanNav`, `PlanRoutes` and coverage; no jumps, sight or stages. |
| D | **Physics reads** | pad solver (calcite), jump read with damage (lanterndrop), fall per cell (loomfall), knockback reach (spark), drop against the kit (lantern-karst), no-catch margin (lanterndrop, lanternpass), no-stand above kill height (loomfall, spark), a spawn nobody climbs back onto (riad), stairs met head-on (calcite) | 7 | None. The walk treats a drop as free to 3 and counts it beyond; there are no pads, knockback or damage. |
| E | **Symmetry and team colour** | a team-colour slot that a turn swaps (calcite, riad, gullhaven-dtm, stratum, lantern-karst, riftwater), facing blocks after a turn (gullhaven-dtm, riftwater), per-piece symmetry (calcite), masses across the seam (stratum, cloudhaven) | 7 | Turns facing data (FEATURES l. 3603); team colour is per theme, not swapped per piece. |
| F | **Structure primitives with guarantees** | bridges between two points that solve their profile (riftwater, cloudhaven, gullhaven, hollow-mesa trestle), stairs with headroom (frostholm, stratum wound stair, penstock flights, gullhaven ramps, riad sunken stairs, lantern-karst joins), tunnels and carves that know the ground (riftwater, gullhaven, calcite, penstock) | 10 | Pieces are axis-aligned; no carve layer. |
| G | **Terrain landforms and water courses** | watercourse with reaches and falls (riftwater, frostholm, hollowcrown), canyon, wash, spire, butte, scarp (hollow-mesa), terrace stage (hollowcrown), routes that grade the ground (hollowcrown), ridged mountain range with a clear radius (spark), coast to the edge and a non-rectangular outline (frostholm), terrain blending (copperline) | 7 | Relief by placed marks; water by height band; no noise heightfields. |
| H | **Floating masses and void edges** | per-island height and underside (cloudhaven), underside treatments (stratum), void-edge style (lanternpass), cliff skirt never rising into the floor and a bedrock foundation (lantern-karst), overhang as its own storey (hollow-mesa), a sky or cloud stage ignored by gameplay checks (stratum, hollowcrown, lantern-karst) | 7 | Islands share one underside profile. |
| I | **Props and prefabs with a shape rule** | prop library with a facing and a reason to be placed (riftwater), balloons (cloudhaven), ships, palms, smoke (saltgate), headframe and adit (copperline, riftwater), detailed theme pieces (riad), plot pieces (curio), entities (riftwater) | 7 | Has a structure library and trees; no parametric prefabs. |
| J | **Patterns** | face patterns, glyph alphabet (stratum), pattern fills for floors (loomfall), shapes from strokes and discs (spark), face-aware paint (penstock), the author's paint ruling as defaults (lantern-karst) | 5 | Has `WallRunMaterial`, `WallDiagonalMaterial`, `CheckerMaterial`, voronoi and noise ramps (TP13, TP17, TP20); paint only, no insets. |
| K | **Placement** | along a polyline (hollowcrown), as near as possible to a point (frostholm), by reason (riftwater), claims per layer (hollowcrown), placement audit as a report over any world (hollow-mesa), closed buildings the walk honours (gullhaven), a rim band axis (cloudhaven), biome per place (hollow-mesa) | 7 | Placement with clearance exists. |
| L | **Seeing the world** | isometric, x-ray and elevation offline (riftwater), sections along any line (gullhaven-dtm, calcite true scale), per-plot render sheet (curio), a weather pass (frostholm), light (riftwater) | 5 | Has `render/isometric`, `render/xray`, `section`, `transect`, `render/eye`, but only on a stored map. |
| M | **The plan document itself** | a plan in polygons and polylines (hollowcrown), relayout without rewriting (cloudhaven), a board as a piece placed twice (gullhaven-dtm), a course template and a style read from a reference map (lanterndrop), fast whole-board rebuilds (frostholm) | 5 | Plan is coarse-grid rectangles with symmetry fanning. |

**Clusters A–E recur across nearly every board from penstock on.** They are the gameplay half: the boards
that started with a plan checker kept asking for the same five things. F–M are the look half, asked mostly
by the first seven boards, which had no plan checker.

## 4. The proposed library

**One Python package, `freeform/lib/pgmvox/`, imported by path.** New boards import it; the twenty existing
boards are left as they are (§6.4).

Tags: **(a)** near-mechanical extraction of duplicated code; **(b)** generalisation that needs design;
**(c)** a capability the boards kept needing and solved ad hoc.

Studio column: **feature** (becomes or extends a studio feature), **read** (a read the studio could add),
**outside** (should stay in the library).

### 4.1 Foundation

| Module | Key functions | Tag | Studio |
|---|---|---|---|
| `pgmvox.world` | `World(x0, z0, sx, sz, sy)`, `set/get/fill/top`, `chest/sign/banner`, `save(dir, name, spawn)`, `load(dir) -> World` (today `render_iso.load`) | (a) | **outside**: the RWV1 volume is the bridge to `write_world.cs`, which already uses the studio's Anvil writer |
| `pgmvox.blocks` | `B` with every 1.8 id 0–197, data comments; `classes`: `PASSABLE`, `NOT_GROUND`, `SEE_THROUGH`, `TRANSPARENT`, `GRAVITY`, `ATTACHED`, `FORBIDDEN_IN_PLOT`; `colour(id, data)` | (a) ids and sets; (b) colours | **read**: the colours should come from the studio's `BlockPalette` (ids 0–197, parity-checked), exported once as JSON, not grown by hand per board |
| `pgmvox.orient` | `stair(rises)`, `door(facing, upper, hinge)`, `ladder(on_wall)`, `torch(on_wall)`, `sign_rot(yaw)`, `log_axis(dx, dz)`, `yaw(dx, dz)`; `data_table(op)` for `mirror_x`, `mirror_z`, `half`, `cw`, `ccw`; `turn_world(w, op, keep, axis)`; `turn_template(blocks, op)`; `recolour(w, mask, swaps)` | (a) mirror and half; (b) quarter turns, one table for all | **feature overlap**: the studio turns facing data in its own symmetry pass. The library's table should be checked against it, not invented a third time. `recolour` is the studio ask in cluster E |
| `pgmvox.noise` | `lattice`, `fbm`, `ridged`, `smoothstep`, `spline` | (a) | **outside**: the studio's relief is mark-based by design |
| `pgmvox.shapes` | `inside(X, Z, poly)`, `seg_distance`, `edge_distance`, `signed_distance`, `polyline` (one copy; drop `noise.polyline_distance`), `point_at`, `walk_cells`, `disc`, `ring`, `ellipse`, `revolve(profile)`, `Frame`, `footprint_mask`, `boundary8`, `edge_depth(mask)` | (a), plus (b) for `revolve` | **outside**, but it should adopt `tools/sculpt/solid.py`'s solid-with-bounds design |

### 4.2 The plan phase

| Module | Key functions | Tag | Studio |
|---|---|---|---|
| `pgmvox.plan` | `Raster(xs, zs, kinds, base_h, base_kind, symmetry, storeys)` with `rect`, `cells`, `mask`, `flight`, `gate` (§2.1); `Symmetry(op, axis)` applied in the plan, not on the world; `Pieces` for course plans (lanterndrop) | (b) | **feature**: a block-scale plan layer beside the studio's coarse-grid plan. The studio's plan is rectangles on a proxy grid, and the boards' plans are per-block rasters with an upper storey |
| `pgmvox.move` | §2.3: `fly`, `leave_edge`, `fall`, `fall_damage`, `knockback_reach`, `solve_launch` | (a) for `fly`, `fall`, `knock`; (c) for `solve_launch` against any `land` callback | **read**, new: `GET …/physics?pad=…&target=…`, `…/fall?from=…`, `…/knockback?level=…`. Nothing in the studio models a launch, a fall's reach or knockback. `docs/pgm/filter-patterns.md` §4.1 documents velocity pads with no tool to tune them |
| `pgmvox.plangraph` | `MoveRules`, `surfaces`, `jumps`, `graph(r, rules, extra, team, stage)`, `dijkstra(g, starts, weight)`, `route(prev, cell)`, `arrivals(g, spawns_by_team)`, `jump_audit(r, rules, planned)` | (a) for `dijkstra` and `jumps`; (b) for `graph` | **read**, extends `PlanNav`: an adventure-mode rule set (no blocks placed; ladders, water columns, jumps 1–3, pads, fall cost) beside the CTW kit-budget walk |
| `pgmvox.sight` | `line_clear`, `visibility(targets, eyes, top, canopy)`, `voxel_visibility`, `openness`, `EYE = 1.62` | (a) the line; (b) the eye sets | **read**, new: a numeric exposure field (`sight?eyes=…&format=text`) beside `render/eye`, which draws a view but does not count it |
| `pgmvox.sketch` | `Canvas(raster, scale)` with `px`, `hillshade`, `board(colours)`, `section(axis, at, band)` and `section_along(polyline)` at true scale, `routes(prev, tags)`, `jumps`, `table(lines)`; the convention that a sketch draws the checker's own numbers | (a) `px` and `shade`; (b) the section from `H/K/U` | **feature**: the studio's plan view could draw true-scale sections and the checker's numbers (asked in rows C and L) |

### 4.3 Building blocks at block scale

| Module | Key functions | Tag | Studio |
|---|---|---|---|
| `pgmvox.terrain` | `ring_falloff`, `mountain_ring`, `slope_deg` (no wrap), `paint_by_angle(w, H, mask, stack)`, `strata(choices, length, seed, singles)`, `banded(period, pattern)`, `underside(H, land, …)`, `cloud_deck(w, y, …)`, `edge_depth` | (a) `mountain_ring`, `slope_deg`, `underside`; (b) `strata`, `banded`, `cloud_deck` | **feature**, mixed. A scenery mountain ring outside the play area is new (row G, spark). `strata` with "red only ever one block" is a preset for the studio's `layered` stack (hollow-mesa's row). Underside treatments extend the island stage (row H). `paint_by_angle` is what the studio's `slope` band axis already does, so the library version is only for worlds the studio did not build |
| `pgmvox.build` | `Rhythm` predicates (`every`, `rows`, `corners`); `roof_field(frame, L, W, eave, kind)`, `lay_roof`; `house(w, spec)` (the copperline-lineage `Frame` house); `parapet`; `site`; `flight(w, path, block)`, `ladder(w, x, z, y0, y1, wall)`; `claim(registry, name, cells, layer)` | (a) the Frame house and claims; (b) one roof field for six gable roofs | **feature**: a heading on structures. The studio's house stamper is axis-aligned and its `RoofField` already unifies six roofs (G34d), so the library should match its formulas, not diverge. Claims per layer are row K |
| `pgmvox.facade` | `Pattern = f(s, run, t, h) -> None | Inset | Accent`; `band`, `courses`, `flutes`, `panels`, `slits`, `checker`, `glyph_row`; `extrude(w, cells, y0, y1, patterns)`; `coffer(w, mass)`; floor fields `border(k)`, `medallion`, `diamonds(period)`, `steps`, `star`, composed by `first_of(...)` | (b) | **feature**: the studio's wall materials paint. An *inset* (the face steps back a block) and a glyph alphabet are new (row J, stratum). Floor fields extend `CheckerMaterial` to figures (row J, loomfall) |
| `pgmvox.plot` | curio's `Canvas(world, origin, size, y_range, forbidden)`, `draw(module)`, `check(world, …) -> spots, top, hidden`, `footing`, `verdict` | (b) | **feature**: a plot piece, a bounded canvas handed to a contributor (row I, curio) |

### 4.4 Reading the built world

| Module | Key functions | Tag | Studio |
|---|---|---|---|
| `pgmvox.walk` | `grid(ids, classes)`, `standable`, `bfs(st, …, rules: MoveRules)` (generation 3, with the headroom fix, plus pads), `nearest`; checks `no_catch(course, margin)`, `no_stand_above(y, radius)`, `unreached(st, starts)`; `pad_flights(w, pads)` | (a) bfs; (c) the checks | **read**. The studio should serve `walk`, `transect`, `incline`, `reach`, `render/isometric` and `render/xray` over an uploaded region folder, not only a stored map. Until it does, this module is the stopgap the CLAUDE.md exception allows (§6.5) |
| `pgmvox.audit` | `footing(world, box)` (gravity blocks, attachments), `placement(records, world)` (floor over air, rock over roof), `claims_report` | (a) from `plotkit.footing` and the five `audit.py`; (c) footing over a whole board | **read**, new: an attachment and footing check is a world read any studio-built board would benefit from |
| `pgmvox.render` | `iso(ids, dat, x0, z0, out, scale, corner, box, ymin, ymax, xray)`, `elevation`, `xray_shell`, `cutaway(build, out, polyline, …)` | (a) | **read**: `section` along any polyline is row L (gullhaven-dtm). The studio's `section` cuts along x or z, and the round-trip CLI has no isometric over a region folder |
| `pgmvox.mapxml` | `Doc(name, version, objective, gamemode, proto)` with `teams`, `kit(dict)`, `spawn(team, region, yaw)`, `cuboid`, `point`, `filter`, `broadcast`, `kill_height`, `portal(a, b)`; `regions_from(raster, kind)` | (b) | **feature** for rows A and B. For modes the studio supports, emit the studio's intent document and let its codec write XML. Keep string XML only for what it refuses |
| `pgmvox.pipeline` | `python -m pgmvox.run <board>`: plan_check → sketch → gen → write → mapxml → renders → walk; finds the studio by `PGM_STUDIO_ROOT` instead of a hard-coded path; numbered render sets from a list | (a) | **outside** |

## 5. Priorities

Ranked by value against effort, weighted to the four things the author values (control, patterns, terrain,
plan phase):

| Rank | Piece | Value | Effort | Serves | Studio follow-on |
|---|---|---|---|---|---|
| 1 | `blocks` + `orient` (one id table, one class table, one facing and turn table, palette from the studio) | Ends the drift; fixes the dropped rail and trapdoor turns, the missing banner, the local id constants and the six disagreeing block sets | Low | control | export `BlockPalette` as JSON |
| 2 | `move` (the 1.8 tick model, falls, damage, knockback, launch solver) | Five copies become one; every gameplay board after penstock used part of it | Low | plan phase | **physics read**: new |
| 3 | `plangraph` (MoveRules, jumps, graph, Dijkstra, arrivals, jump audit) | Six checkers' cores; the jump audit is the one check every board with jumps wrote | Medium | plan phase | adventure-mode walk on the plan tier |
| 4 | `plan.Raster` with symmetry in the plan and one `flight` | Four flight signatures become one; every raster board starts here | Medium | plan phase, control | block-scale plan layer |
| 5 | `sketch` (true-scale sections, routes, the checker's numbers on the image) | Eight section drawers; the sketch is how the author reviews a plan | Medium | plan phase | sections and numbers in the plan view |
| 6 | `walk` generation 3 + `no_catch`, `no_stand_above`, `footing` | Fixes nine boards' dead headroom check; turns three ad hoc checks into reads | Low | plan phase | studio reads over a raw world |
| 7 | `sight` (one eye height, vectorised visibility, openness) | Five sight models with two eye heights | Medium | plan phase | numeric exposure read |
| 8 | `terrain`: `mountain_ring`, `ridged`, `slope_deg`, `strata`, `underside`, `cloud_deck` | The terrain-fidelity half: seven banders, six undersides, two near-identical mountain rings | Medium | terrain | scenery ring stage; strata preset; underside treatments |
| 9 | `facade` + floor fields | The richest pattern code in the corpus generalised; carpets, flutes, glyphs and insets as parameters | Medium-high | patterns, control | inset patterns and figure fills on studio materials |
| 10 | `build`: `Frame`, `roof_field`, `house`, `Rhythm`, `parapet` | Six gable roofs, four identical `Frame` houses, seven parapets | Medium | control, patterns | heading on structures |
| 11 | `render` (iso, x-ray, polyline cutaway) with the studio palette | Nine renderer variants become one; colours stop forking | Low | (seeing) | `section` along a polyline |
| 12 | `mapxml.Doc` + `regions_from` | Removes boilerplate; less value, because the content is per gamemode | Low | — | objective pieces writing their own regions |

**Do first: ranks 1, 2 and 6.** They are mechanical, they fix live bugs, and everything else imports them.

### 5.1 What not to share

- **Board art.** This covers loomfall's five carpet designs, stratum's glyph words and masses, cloudhaven's
  Albatross and Concord, hollow-mesa's tram and fort, and the 48 curio plots. The library should hold the
  combinators these are written in (`facade`, floor fields, `revolve`, `Rhythm`), not the designs. A design
  in a library becomes a default, and every board starts to look like the first one.
- **Terrain recipes as constants.** spark's `45 + 45 * (big + 0.5)` and curio's `35 + 40 * …` are each a
  look. Share `mountain_ring` with named parameters and keep each board's numbers in its own plan.
- **Plan contents.** `KINDS` per board, `COURSE`, `CARPETS` and `PADS` are the board.
- **Kits and gamemode XML.** They are rules of play, not geometry. The studio's codec owns the modes it
  supports.
- **Tree templates.** They live in the studio's tree library (`tools/trees.py`, `seed-trees.cs`).
  hollowcrown's `cut_trees.py`, which reads two other boards' `trees.json`, is the thing to remove, not to
  share.
- **`annotate.py` and the per-board `renders.py` lists.** Their shape is shared (`pipeline`), but their
  boxes and titles are not.
- **The first-generation walk and the axis-aligned `house.py`.** Both are superseded inside the corpus
  itself.

## 6. Caveats and risks

### 6.1 Coordinate conventions differ

**Height means three different things.** In the raster plans, `H` is the floor block (calcite's flight
lands at `floor = H + 1`). In lanterndrop, `y` is "the top of a piece, the block a player stands on". In
curio, `Y` is where the player's feet are and `G = Y - 1` is the paving. A shared `plan` must name which one
it holds.

**There are two mirror axes.** penstock, riftwater and stratum mirror at `x' = -1 - x`, an axis at
x = −0.5. lanterndrop mirrors pieces at `x' = -x`, an axis through the middle column. The half-turn boards
use `(-1 - x, -1 - z)`. `turn_world` must take the axis as an argument; it cannot assume one.

**Direction words differ by family.** Stairs say `"+x"`; doors and houses say `"e"`; ladders take data 2–5;
and `copperline/plan.py` has `FACE = {(0, -1): "N", …}`. `orient` should accept one vocabulary and convert.

**Arrays are offset differently.** Plans index `[x - X_MIN, z - Z_MIN]`; `World` indexes
`[x - x0, y, z - z0]` with y from 0; curio's plot canvas is local 0..10 with y from −1. Volumes must be
centred for `rotate_world` and `mirror_world` to work (both assert it).

### 6.2 Global state

- **Module-level seeded RNGs.** `RNG = np.random.default_rng(777)` and similar sit in every early board's
  `terrain`, `buildings`, `dressing` and `house` (17 modules). Output depends on the order of calls across
  modules. Moving a function into the library changes which numbers it draws, so **an extracted board will
  not come out block for block the same.** Pass `rng` explicitly in the library and accept the change.
- **Plans built at import.** `R = P.build()` runs at module import in `gen.py` and `plan_check.py` on six
  boards. `sketch.py` imports the checker (`R = C.R`), and `spark/walk.py` imports `gen`. That is convenient
  and makes import order significant. The library should take the raster as an argument.
- **Two seeds called 808 and 2024 on different boards.** This is harmless, but it shows seeds were typed,
  not derived. A `seed(board, name)` helper would make them reproducible and distinct.

### 6.3 Physics and model disagreements to settle once

- **Eye height** is 1.6 (gullhaven, riad, plotkit) or 1.62 (lanternpass). Riad aims at the target's
  y + 1.0, and plotkit at y + 0.9.
- **Fall cost.** Every model makes a drop free to 3, as the studio's walk does. Riad charges 2 a block
  beyond; lanterndrop computes `ceil(dy - 3)` damage against 16 health; `walk_core` charges nothing.
- **`slope_deg` wraps.** `np.roll` makes the board's west edge a neighbour of its east edge. The studio
  reads slope by Horn's 3×3 gradient over a two-cell window (`terrain-painting.md`). A board painted by the
  library's angle and read back by the studio's `incline` can disagree at the edges and on gentle slopes.
- **The plan jump rule and the voxel jump rule** are the same formula in two data models. Unless both call
  one function, the plan check and the built-world check can disagree about the same gap.

### 6.4 Migration risk

**Do not refactor the twenty boards.** They are finished, and their worlds and reports are the record of
what each run did. A library adopted by the next board costs nothing. Retrofitting old boards changes their
output (§6.2) and spends effort where nobody is building.

**Keep the cross-board imports in mind if anything is moved.** saltgate's cutaway and all of
gullhaven-dtm resolve modules from `opus55-freeform-gullhaven/scripts`, and hollowcrown reads two other
boards' `trees.json`. Moving or renaming gullhaven breaks two other boards.

### 6.5 The repository's own rule

**CLAUDE.md forbids "a second copy of the system":** no script that reads a built world, such as a walk, a
section renderer or a clearance check, wherever it lives. The stated exception is a world that is not a
stored map, which is exactly what a freeform world is.

**The exception is why `pgmvox.walk`, `audit` and `render` are a stopgap, not a destination.** The studio
already has `walk`, `transect`, `incline`, `reach`, `render/isometric` and `render/xray`, but only for a map
it built. The durable fix is for the studio to serve those reads over an uploaded region folder. Then the
library's world readers shrink to the checks the studio does not have: no-catch, no-stand, footing, sight.

**The plan-phase modules (`plan`, `plangraph`, `move`, `sight`, `sketch`) do not have this problem.** They
read a plan, not a built world, and the studio has nothing at that grain.

### 6.6 Other risks

- **Python against C#.** Anything promoted into the studio is a port, not a move. The physics and the jump
  audit are small and port cleanly. The facade combinators and the `Frame` house are larger, and their
  rotated-frame rasterisation must agree with the studio's stamper block for block or the two will drift as
  the helpers did.
- **The palette must have one owner.** If the library keeps its own colour table, §1.2 happens again.
  Generate `blocks.colour` from the studio's `BlockPalette` and regenerate on a studio change.
- **`boards-check.py`** gates folders under `maps/` and `specs/`, so a `freeform/lib/` folder is outside
  it. A library under `tools/` would be inside `tools/`' own conventions (`tools/README.md`) and should be
  documented there if it moves.
- **Version pinning.** A board that imports a moving library is no longer reproducible from its own folder.
  Each board's `build.sh` (or `pipeline`) should record the library version it was built with.
