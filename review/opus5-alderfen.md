# Alderfen Holm — a swamp DTC, and the two cores that saved its flanks

> A DTC swamp board: hilly behind the spawn and along the edges, levelling out toward the middle, one
> mid island between the two sides, coarse-dirt-and-polished-andesite roads from spawn to shore, and
> cumulus cloud made out of wool in the sky.

**In one sentence:** a peat holm archipelago where each team's two obsidian cores stand on level bog
in front of a hill-backed island, and the one holm between the sides is reached over sixteen blocks of
void a bridge has to be built across.

162 × 218 blocks of rendered extent over a 150 × 210 plan, `rot_180` about the origin, base surface 14,
ground y11..y41, clouds y80..y96. Three landmasses: two team islands (`holm`, x −75..75, z −105..−41)
and one mid holm (`holm-mid`, x −60..60, z −20..20), joined only by a build zone over the void
(x −65..65, z −40..−20, fanned).

## What the request asked for, and where each thing is

| Asked | Where it is | Measured |
|---|---|---|
| a DTC map | two `<core>` a team, obsidian casing, lava 3×3×3, float 6, leak 5 | `<cuboid id="red-core-region" min="-24,21,-58" max="-19,26,-53"/>` and `red-core-2-region` at x 20..25 |
| swamp theme | biome field `cell`, cellSize 34, palette 4× swampland / 2× mesa | sampled 1 189 columns off the built region: **880 swampland (6), 289 mesa (37)** |
| small-to-medium spruce and dark oak buildings | `croft` (8×8, one storey) ×2 and `stilthouse` (12×10, two storeys on posts) ×2, per island | `croft` walls are two courses of cobble/mossy-cobble noise under four of spruce/dark-oak noise, dark oak log posts, dark oak roof with a laid dark-oak-log verge |
| trees with vines | seven `copied` recipes, each a vanilla-shaped oak with 4–18 vine cells hung in curtains | `(-44, -12)` reads Vines y18–20; `(-43, -17)` reads Vines y17–20; `(-62, -75)` one course. Data 5 and 10 — the two face-pairs a rot_180 image leaves valid |
| small lakes on each island, surrounded by sand | one painted bog pool a team island (`marsh` inside `strand`), two carved pools on the holm | `(-5, -64)`: Lily Pad y13 · Water y12 · Sand y9–11. Holm pool: `~` in `02-heightmap.txt` rows −9..+9 with a sand bank |
| hilly at spawn, levelling toward mid | four pushes behind and beside the spawn shelf; nothing forward of z −76 | `02-heightmap.txt`: bands `p q r s t` (y27–y31) at z −97..−85, band `3`/`4` (y14–15) at z −45..−39 |
| fairly square | 150 × 210 of plan, 1 : 1.4 | — |
| roads of coarse dirt and polished andesite | two `stroke` props, `rough`, radius 2.5, coverage 0.85, `route: true` | `pave` is a `cell` of two blocks at cellSize 3, jitter 60 — coarse dirt with polished andesite laid through it |
| one mid island | `holm-mid`, 120 × 40 | one `neutral` group, relief range **5** — the level half of the board |
| rough terrain to the edges | two `edge` pushes, amounts 10–14, falloff 10, crown 8 | the `brae` theme paints them: grass and dirt in eight-block patches |
| lily pads on the water | on the painted pans, yes; on a water prop, **no** | see *What the pass refused*, below |
| a mesa-and-swamp biome pattern | above | — |
| specks of podzol and dirt in the grass | the `bog` theme's turf is a `noise` at scale 12 whose end stops are podzol and dirt | a fractal field's band areas fall off toward its ends, so the two accents come out as specks and grass is the body |
| fern, brown mushroom and grass | `flora` ×5 at `fernShare` 0.55; mushrooms as three `copied` one-block beds on painted podzol | `(-49, -88)`: Brown Mushroom y34 over **Podzol** y33 |
| boulders of cobble, mossy cobble and andesite | four `erratic`/`shelf` and one `cairn`, rock = `turbulence` scale 3 over those three | `(0, -9)`: Mossy Cobblestone y16–19 over Andesite y15 |
| laid log piles | three `copied` recipes: two courses of logs lying along x with a third on top | `(-37, -92)`: Oak Log **17:4** over Spruce Log **17:5** — data 4 and 5 are the x-axis nibble |
| tiny huts, laid-log roof, clay-noise walls, 1×1 light-grey clay windows | `mirehut`, 6 × 5, three on the holm | `(-46, -4)`: Cobble/Mossy plate y13–14, Hardened Clay y15–19, **Spruce Log y20** (the laid roof). Window is `pane` of `159:8` |
| cumulus cloud structures in the sky | three `made` things of three slabs each, `mirrors: true` → six clouds | `(0, 3)`: White Wool **y84–y92**. `(-52, -90)`: White Wool y80–85 |

## The board, and what it asks of the two sides

The spawn sits at `(0, −95)` on a shelf pinned at y18. Two roads leave its door and swing out and
forward, one to each core, down four pinned one-block steps to the bog at y14. The two cores stand at
`(±22, −56)` — 45 blocks of walk from their own spawn door, **0 placed blocks**, and 158–160 from the
enemy's, of which **40 are placed**: the two sixteen-to-twenty-block bridges the holm crossing costs.
Read against its own mirror the board is fair to a block: red→far 159, blue→far 160.

The two cores are the design decision this board turned on. With **one** central core a team, the plan's
own flow read answered **83% of the ground off every route** — every journey ran down `x = 0` and both
150-block flanks were dead by construction. Splitting the goal into a west and an east, 45 blocks apart
(`GO2`'s own band), pulled the routes diagonally across both flanks and across both shoulders of the
holm: the dead share fell to **32%**, and `reached` more than doubled from 4 348 to 10 780 blocks. It is
also the arrangement `docs/gameplay/approaches.md` states for a multi-goal board — *a west and an east,
placed against each other rather than scattered*.

What the ground round each core does, going out from it: **open** on the apron in front (nothing stands
within 10 blocks of a marker), a **bog pool** on the axis between the two cores that a player drops into
and comes up out of, a **tiny hamlet** on the holm to fight through on the way in, a **wood** on the west
flank giving cover to within 20 blocks of the west core, and **rough hills** on both outer edges that an
attacker climbs to bridge from. Four ways in, arriving from around, below, through and above.

## What the ground is made of

Five ground themes and one sky theme. One ground, one hill, and three splotches — the shares are what
say so.

| Theme | Share | On | Says |
|---|---|---|---|
| `bog` | 82.7% | everything not otherwise stated | grass with podzol and dirt as a `noise` field's two end stops, over three courses of dirt/coarse-dirt at `rise: 8` so a column's soil is one material |
| `brae` | 13.5% | six painted patches over the pushes | grass, dirt and coarse dirt in a `cell` at cellSize 8, jitter 55, warp 2 — the hills wear dirt |
| `fenbed` | 1.9% | three beds beside the tree stands | podzol, which is the one footing a vanilla mushroom keeps in daylight |
| `strand` | 1.3% | the ring round each bog pool | sand and gravel, two blocks |
| `marsh` | 0.7% | inside that ring | one course of standing water, pinned a block under the bog around it |
| `cloud` | — | the six made things | white wool with white stained clay as its shading |

The rim is on `void` edges only, so the coast wears a sand band and no contour of the relief takes a lip.
`wallOnTerrainFaces` is off, so the hillsides stay grass and only the coast and the cut faces show the
rock: a `cell` of turbulences at cellSize 9 with `rise` 5 — wider than tall, which is what stops a cut
face reading as vertical stripes.

## The techniques, and what each one bought

**A copied tree is how a vine gets on a map.** Nothing in the dressing vocabulary places a vine: the
flora overlay's species list is grass, fern and four flowers, and a grown or template tree writes wood
and leaves. A `copied` recipe writes *any* block at any offset, so the seven fen oaks are authored
bodies — a vanilla trunk-and-blob crown, then 2–7 vine cells hung from an outer leaf's face. Two things
make them stand: the drop is clamped so no cell is below the foot's own course + 1, and every vine takes
a **face pair** (5 = north|south, 10 = west|east) rather than a single face, because `BlockGeometry.Turned`
turns a log's axis and a stair's facing round the orbit and leaves a vine's data alone — a single-face
vine would name the wrong side on the mirrored half and drop on the first block update.

**Water painted as terrain carries a lily pad; a water prop does not.** See below.

**A pinned pad is a box, not an ellipse.** The first cut drew the two flat pads as `lobed_ring`
ellipses stated over a box. An ellipse at 0.8 of its own half-width reaches only 0.6 of its half-depth,
so a house placed at the pad's own stated corner found unpinned ground beside it and filled the face in
bedrock — `WX11`, four times over. `lobed_box` walks the box's perimeter instead, rounds the corners and
wobbles every vertex *inward only*, so the ring covers the band it names.

**A push and a pinned area cannot share ground.** A push is applied to the solved surface after every
mark, so a brae whose skirt crosses the spawn pad lifts the pad. Every push ring here stops its own
`falloff` short of the nearest pinned ring, and where they still touch the lift at that distance is
nought. That constraint is also why **no building stands on a hill**: 72 blocks of pinned bog carries two
cores with a 20-block clearance each, two roads and a pool, and nothing six blocks wide was left over —
so the hills are rough ground and the buildings are on the two pads and the holm.

**A coast is drawn, not compiled.** `bendShapes` resamples each compiled rectangle's long edges at 12
blocks and pulls every inserted point inward, then lays Catmull-Rom handles over the result. At
`wander: 2.5` the change is invisible at map scale; at **6** the coast stops reading as the ruled line the
compile emitted. The cost is that everything within `wander + 4` of the old coast has to move inward with
it — the two outcrops, the six spruce along the edges and the paint patches all did.

**A cloud is a made layer and the build ceiling does not see it.** Three slabs at `base_y` 80/83/86 (and
88/91/94, 84/87/90), each a few overlapping circles at `height_mode: level`, `skirt: 0`,
`relief_scope: exclude`, `kind: made`, `part_of` the cloud, `mirrors: true`. Because a made layer's floor
is far above the bedrock course it plates nothing at y0, and because `BuiltTerrain.Ground` takes the made
things out, nothing seats on a cloud.

## What the pass refused, and what it cost

**A lily pad may not stand on a water prop.** Measured twice — a one-cell `copied` recipe of block 111
placed at `(-34, -54)` and at `(-38, -50)`, both inside the `tarn` pool — and declined both times:

```
[decline] DR-CLAIM tree 'lily-tarn' rests on (-38, -50), claimed by the channel 'tarn'
```

A water prop claims every column of its bed and its beach as `ClaimKind.Water` at placement order 0, and
a tree places at order 4, so the claim refuses it. There is no prop kind, no flora species and no field
anywhere in the dressing document that puts a pad on water a `WaterProp` made.

What does work is **water painted as terrain**: a one-course `add` patch whose theme's `surface` is
stationary water (id 9) one course deep, pinned level by an `area` mark a block under the ground round it.
It claims nothing, so a pad seats on the air cell above it, which is exactly where vanilla puts a lily
pad. Three pads a pool, verified: `(-5, -64)`, `(1, -62)`, `(5, -60)` all read `Lily Pad y13 / Water y12`.
The trade is that such a pool is one block deep — a bog puddle rather than a lake — which is why the two
carved pools on the holm are water props with sand banks and the two on the team islands are painted.

**A laid-log roof takes one wood, not a pattern.** `HS3` refuses a roof body that is not a single block:
*a roof's body and its verge are each a single block — never a pattern, so nothing spreads a voronoi
across a roof*. So the mirehut's roof is one laid spruce log with a laid dark-oak verge, and the third
wood the request asked for is in the log piles instead.

**A mushroom in the open does not survive vanilla.** `BlockMushroom.canBlockStay` drops a mushroom at
light 13 or over unless it stands on **podzol or mycelium**. The flora overlay has no mushroom species at
all, so the three beds here are one-cell `copied` recipes, and the ground under each is a painted podzol
patch — which is also what the request's "few specks of podzol" asked for, made deliberate.

## What went wrong

**The clouds broke the read the board is checked with.** The first cut put a cloud over the middle of
the crossing. `walk`, `slopes` and `heightmap` all take the topmost solid block, and a made layer is
solid, so `04-routes.txt` reported the cross-board walk as `barrier +58 at (0, 38) … drop -58 at (0, 19)`
— the route "walked" across the void at y72 over the cloud's own slab. The dressing and seating surface
excludes made things and the projective reads do not, and the projective reads are the ones that lie.
They are placed over the flanks no route runs down now, and their footprints are in *Coordinates* so a
reader can subtract them.

**`SK18` reads a shared column, not a shared span.** A cloud sixty courses above a hut's roof is still
reported as one thing standing inside the other, 141 columns of it. Both holm huts had to move out from
under `cloud-holm` even though nothing anywhere near them interleaves.

**`maxPlayers` is per team, whatever the field says.** `PlanGlobals.MaxPlayers` is documented as *how
many players the board is sized for, across all teams*, and `TeamsGenerator` writes it into each team's
`max`. At 24 this board shipped `max="24"` twice — a 48-player XML on ground sized for half that. It is
16 now.

**Twenty-two placements were declined before they were placed right.** Nothing about this was hard, and
all of it was one read: `POST …/sketch/columns` names every decline with its rule, the prop and the cell,
and eight rounds of read-and-move took it from 22 to 0. The ones worth remembering: a building's claim is
its *stamped* extent grown one block, so two houses need two clear columns between their eaves, not
between their walls; a boulder is 15 blocks across at size 5, so its footprint and not its anchor is what
`OB19` tests; and a road claims a five-wide band that turns a tree away at three more, so a 40-block holm
with a lane down it has no room for a tree at all — which is why the holm carries no road.

## Open gameplay questions

- **Two cores a team on a 150-wide board.** `docs/gameplay/approaches.md` says one goal is the answer
  *on a board a hundred blocks or less across*; this is 150, and one goal left 83% of it off every route.
  Two at 45 apart is `GO2`'s band and the author's stated west-and-east arrangement, but whether a
  12-a-side team can hold two cores 45 apart is a played question, not a measured one.
- **A sixteen-to-twenty-block crossing, twice.** Each team pays 40 placed blocks to reach the enemy's
  cores and 0 to reach its own. Whether that is the right price for a 190-block board is the author's.
- **The bog pool between the two cores.** It is the depression `approaches.md` names as the entrance from
  below, one block deep. Whether one course of water reads as that, or wants a carved basin instead, is
  worth a look in game.

## Coordinates

| Thing | At | Reads |
|---|---|---|
| red spawn point | `(0, 18, -95)` | on the pinned pad, 0 placed blocks to either core |
| red core (west) | anchor `(-22, -56)`, casing `x −24..−19, y21..26, z −58..−53` | obsidian, lava 3 high, float 6 over ground y14 |
| red core (east) | anchor `(22, -56)`, casing `x 20..25, y21..26, z −58..−53` | 45 blocks of walk from its pair |
| the crossing, at `x = 0` | island front z −38, holm back z −22 | 16 blocks of void; build zone z −40..−20 |
| bog pool | `(0, -62)`, pan `x −9..9, z −66..−58` | Lily Pad y13 · Water y12 · Sand y9–11 |
| holm pools | `(-30, 4)` and `(30, -4)` | water props, level 13, sand-and-gravel bank, shore 2.5 |
| west brae crest | `(-58, -76)` | ground y30; oak crown to y37 |
| east brae crest | `(58, -84)` | the largest barrier face on the board, 114 cells at `x 39..68, z −108..−95` |
| cloud footprints (subtract these from `heightmap`/`slopes`/`walk`) | `(-56, -94)` y80–92 · `(-62, -50)` y88–100 · `(0, 0)` y84–96, and their rot_180 images | white wool and white stained clay |
| the three mirehuts | `(-46..-40, -4..1)` · `(40..46, -14..-9)` · `(26..32, 8..13)`, and images | hardened-clay walls, laid spruce roof, 1×1 light-grey clay windows |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0.94**, `valid: true`. One soft term: `LN2 max-chain-length 150 outside [25, 110]` — the lane lint reads a 150-block-wide landmass as a 150-block lane, which is a category mismatch on a landscape board |
| `POST /plan/inspect` | `core-w` own 45 / enemy 158, **ratio 3.51**; `core-e` own 43 / enemy 160, **3.72** (`GO1` wants 3–4). Own pair 45 apart (`GO2` 35–65). Opposing pairs 115 and 133 (`GO3` 85–150). Island gap **20** (`CT12` 15–40) |
| `POST …/sketch/relief/read` | `team` 11 135 cells, low 13, high 41, **relief 28**, symErr **0**; `neutral` 5 534 cells, low 11, high 16, relief 5, symErr 0 |
| `03-slopes.txt` | 22 433 walked · 3 953 scrambled · **1 418 barrier** (5.1%); 20 faces, largest 114 at `x 39..68, z −108..−95` |
| `06-claims.txt` | **placed 110, declined 0** |
| `04-routes.txt` | own spawn → own core 48 blocks, **0 placed**, worst step 0; enemy spawn → core 159/160 blocks, **40 placed**, worst step 0. All eight routes walked end to end |
| `05-themes.txt` | 5 ground themes, 19 distinct surface blocks; largest border `bog | brae` 678 cells |
| `GET …/preflight` | export gate **OPEN** |
| `GET …/coverage` | reached 10 780 · decorated 6 819 · **dead 10 205 of 27 804 = 36.7%**. The five largest dead patches are the four island back-corners (1 400–2 000 cells each) and one holm shoulder |
| biome bytes, sampled off the region | 880 swampland · 289 mesa · 20 void, over 1 189 columns |
| provenance | 66 trees · 14 houses · 10 boulders · 10 flora · 4 strokes · 2 water · 2 spawns · 2 cores |
