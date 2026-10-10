> Written by a Sonnet 5.5 helper agent on 2026-10-10 and committed as it wrote it. Checked against the code before commit: the window/door rule (HouseWindows.cs), the goal markers (GoalMarkerStamper.cs, BuildCeiling.OverGround = 20) and the kit pickaxe pairing hold. GET /api/rules on a local studio answers 266 rules, against the "about 262" counted here.

# pgm-studio inventory (for "studio 2.0" planning)

Scope: what the studio (`/home/user/pgm-studio`, branch content of `main`) does and does not have. Written from
the docs under `docs/` and, where it mattered, from the code in `src/`. Evidence tags: **[C]** read in code,
**[D]** stated in a doc, **[I]** inferred by me. Paths are relative to `/home/user/pgm-studio` unless noted.
Size context: ~135k lines of C# in `src/`, 484 test files / ~4,100 `[Test]` methods, 149 HTTP operations
(`docs/refusals.md` "How a gate is called") [D].

---

## 0. One-paragraph shape of the thing

The studio is a **declarative, rule-gated, symmetric-board authoring system**. Its centre of gravity is a
*plan* (rectangles on a coarse grid, authored as one symmetry unit and fanned across the orbit), which compiles
into a *sketch layout* (block-resolution shapes + relief + paint + dressing) and a *MapIntent* (teams, spawns,
objectives, build zones). A world is rasterised from the layout, stamped with objective structures, painted,
dressed, and written as Anvil + `map.xml`. Everything is stored in MariaDB with a change history, exposed over
HTTP (149 operations), self-described by generated schema/glossary/rules, and edited by a Blazor WASM UI. It is
strong on **gameplay contracts, validation, and PGM-correct XML**; it is weak on **free-form 3-D geometry**
(its ground is a stack of heightfield "slabs", not a voxel volume) and on **parametric props**.

---

## 1. The authoring model

### 1.1 The four levels (flow.md)

`docs/tools/flow.md:7-17` [D]:

| Level | Document | Tool | Grain |
|---|---|---|---|
| Board | `PlanModel` (`*.plan.json`) | Plan | coarse grid cells (default 5 blocks), axis-aligned rects |
| Ground | `SketchLayout` | Sketch | block-resolution shapes, relief, paint, dressing |
| Play | `MapIntent` | Configure | teams, spawns, objectives, build areas, shops, spawners, capture points |
| Map | `VoxelWorld` + `MapXml` | built | the Anvil world and `map.xml` |

Plus a fifth, **kept** document: the *refinement* (flow.md:155-178, 238-242), the statements a plan cannot make,
stored beside the plan/layout/intent. And a non-level: the **Library** (materials, themes, house parts, room
styles, biomes, trees, boulders) which is *copied* into maps, never referenced (flow.md:31-34; library.md "A map
takes a copy, never a key").

The flow is one-way (flow.md:25-29): plan -> (layout, intent) -> world/`map.xml`. Nothing is read back up; a
finished `map.xml` cannot become an intent (flow.md:307-310 explains `PUT /source` as the only road back in, and
it takes a plan/layout/intent, not XML).

### 1.2 The plan document (plan.md:60-420)

- `globals`: `cell` (blocks/cell, default 5), `symmetry` (`rot_180`, `rot_90`, `mirror_x`, `mirror_z`, `none`),
  `maxPlayers`, `surface` (base height 9), `observerY` (plan.md:142-176).
- `pieces[]`: `{id, role, rect:[x,z,w,h] in cells, surface?, mirrors?}`. Roles: `piece`, `spawn`, `wool-room`,
  `buffer` (negative space) (plan.md:181-220). Each distinct height in a connected component becomes its own
  shape; abutting same-height pieces fuse (plan.md:430-440).
- `zones[]`: rect over void where players may bridge (`kind` absent = build zone; `water-lane` = opens ~45 min in)
  (plan.md:221-235).
- `placements`: `spawns` (facing, footprint), `wools` (colour, footprint), `iron` cubes, `destroyables` (style
  `pillar-1/2/3`, `cube-3/4`, `column-plus`; material; `float` <=12), `cores` (lava size/height, `float`+`leak`),
  all positioned in **blocks** relative to a piece on a half-block lattice; `layer` names the storey
  (plan.md:237-361). `controlPoints` is a count (1, N, or N+1) not a position (plan.md:333-347).
- `walls[]`: a bedrock approach wall (2 thick, 3 courses) on a piece-pair interface (plan.md:363-392).
- `boxes[]`: composer annotation only (plan.md:394-413).
- Refuses at compile (422): `PL*`, `OB*`, `WX*`, `DC*`; lints come back on `/plan/evaluate` (plan.md:645-736).
- **Plan authors no paint, no dressing, no stack**: "flat by decision" (plan.md:960-995). One team's unit only.

### 1.3 Sketch layout (sketch.md:94-607)

`SketchLayout` keys: `setup` (mirror mode/centre/bbox), `layers[]` (slabs), `themes`/`themeSources`/`mapTheme`,
`roomStyles` (`wool`,`spawn`), `dressing`, `biome`, `relief` (keyed by group id) (sketch.md:122-130).
Shape types: `rectangle`, `circle` (64-gon), `polygon` (Bezier `controls`, per-vertex `anchor_heights`), `lasso`,
`polyline` (centripetal Catmull-Rom centreline with `stroke_edge` solid/rough/tapered) [C]
`src/PgmStudio.Pgm/Sketch/SketchLayout.cs:476-649`. Each carries `operation` add/subtract, `override`, `floor`,
`base_height`, `height_mode` (`level`/`raise`/`sink`/`drape`), `skirt`, `relief_scope` (`follow`/`hold`/`exclude`),
`keepClear`, `theme` **or** `material` (never both, SK23/SK24), `layer`/`group`.

Set algebra per layer: `((adds - subtracts) U override-adds) - override-subtracts` (sketch.md:468).

### 1.4 What an agent sends (HTTP)

The one-call authoring road is **`PUT /api/map/{slug}/source`** (flow.md:142-362) [D]: a `plan` (or a
`layout`+`intent` pair) plus a `refinement`, an `origin` (repo/commit/path), a `note`, `after`/`discard`. The
server compiles, applies the refinement, rasterises, projects the intent, and stores it all as **one numbered
change**; `?dry=true` decides everything and stores nothing. Refinement members (flow.md:163-178): `materials`,
`themeByHeight`, `themeById`, `shapePropsBy{Height,Id}`, `addLayers`, `addShapes`, `editShapes` (insert/move/remove
point, `pulls`), `bendShapes` (coast), `outlines` (lobed ellipse -> ring), `relief`, `themes`/`mapTheme`, `biome`,
`roomStyles`, `dressing`, `created`/`authors`, `controlPoints`, `scoreLimit`, `spawners`, `shops`.
Note what is **not** a refinement member: `build` areas, kits, objectives other than via the plan. A driver wanting
block-exact build rects supplies a full `layout`+`intent` base instead.

Other agent-facing endpoints (all [D] unless stated):
- Self-description: `GET /api/openapi/v1.json`, `/api/glossary`, `/api/rules[?rule=|family=]`, `/api/rules/terms`,
  `/api/terrain/patterns`, `GET /kit.py` (a generated Python client; flow.md:77).
- Plan reads: `POST /plan/compile|evaluate|inspect|ascii|columns|feasibility|room`, `GET /map/{slug}/plan/ascii`,
  `/plan/flow`, `/state`, `/findings` (plan.md API table).
- Sketch granular edits: layers, groups, shapes (+`/bend`, `/vertices`), `relief/{groupId}`, `themes`, `props`,
  `room-styles/{part}`, `biome`, `paint`, `columns`, `dressing`, `seats`, `probe-footprint` (sketch.md:2158+).
- Configure/play: `PUT /map/{slug}/intent`, `GET /map/{slug}/preflight|traversability|editability|kit-reach|
  wool-availability|coverage|xml|export` (configure.md:574-668).
- Read-backs: `render/{topdown,section,heightmap,surface,traversability,structures,mirror,isometric,xray,walk,eye,
  picture}`, `slopes`, `incline`, `reach`, `walk`, `column`, `transect`, `stroke`, `themes/census`, `report`, `diff`
  (read-backs.md:38-63).
- History: `GET /map/{slug}/changes`, `/diff`, `POST /changes/{n}/restore`; notes + hand-edit handoff (`SR1`)
  (flow.md:371-420; sketch.md Notes).
- Already-finished maps: entity routes (`PATCH /map/{slug}/regions/{id}` etc.), flow.md:509-578.
- Auth: Discord sign-in + invitation, whitelisted `member`/`admin`, bearer **tokens** for headless callers;
  429 + `Retry-After` when the 3-at-once build queue is full (`docs/access.md`, CLAUDE.md of mapgen).

### 1.5 The generator / composer (generator.md, shapes.md, docs/generator/*)

A pre-computed library of whole boards: **500 per size band and symmetry**, composed from size band + symmetry +
seed, browsed at `/generator`; "keep" -> plan row -> author -> Plan tool (generator.md:1-23). Vocabulary: nine
approach families (`i`, `l`, `z`, `scythe`, `clamp`, `u`, `h`, `donut`, `isolated`), hub bodies (`bar`, `single`,
`twin`, `ring`, `p`, `double-hole`, `g`), frontline bodies (shapes.md:23-72). Limits (generator.md:424-470): only
two-team `rot_180`/`mirror_z`; boards are "flat, unpainted and CTW"; some families unreachable by the sampler
(G145/G146); no on-request composition. 1,616 corpus maps were measured to calibrate it (supported-maps.md).
`docs/generator/model.md` (21k words) governs; `rules.md` (18k words) argues each layout rule.

### 1.6 What cannot be expressed (or only awkwardly)

| Wish | Verdict | Evidence |
|---|---|---|
| Underground passages | **Partly.** A *roofed void*: subtract (hole) + an override-add lid above the subtract's floor is legal and silent; or a second layer (storey) with `base_y`. A tunnel through ground that *keeps* relief over it is **not** expressible: a subtract empties the whole column, so tunnels are straight-walled shafts. Open task TS140 "A carve" | sketch.md:204-220; BACKLOG.md:312 |
| Caves, 3-D carved bores, arches in rock | **No** (no 3-D carve, no ellipsoid cut). Only via many stacked layers/slices (sculpture "made things") | BACKLOG.md:312 (TS140), :250 (TS63) |
| Overhangs / cantilevers | **Via layers.** One layer = one `(floor,top)` span per column; a deck over a void is a second layer or a `floor>0` shape. Within one layer the *taller add wins, floor included* | sketch.md:438-450 |
| Floating islands | **Yes**, flat underside per shape (`floor`). A shaped underside (cone/roots) needs stacked tiers (taller wins, floor included) **[I]** or made-thing layers; no underside-profile field. Bedrock is only written at y=0 under columns whose ground reaches it | sketch.md:236-239; sketch-world-export.md:36-40 |
| Buildings at arbitrary angles | **No.** Houses are rectangles (and touching-rectangle wings: L/T/U) on the block grid; no heading/yaw on `HouseProp`; the orbit can only turn them by 90 degrees | [C] `src/PgmStudio.Minecraft/Dressing/PlacedProp.cs:409-470`; decoration.md:871-880 |
| Curved/round buildings | Only as "made thing" layers of circles/polygons (hollow dome = N circles); form library TS63 unbuilt | BACKLOG.md:250 |
| Multi-storey interiors | **Yes for shells**: storeys with clear heights, decks, ladder through the deck, roof terrace via parapet storey. **No** interior partitions, rooms-within-rooms, furniture **[I]** (none in structures.md) | structures.md:914-1036 |
| Arbitrary props / prefabs / schematics | **No by design.** Seven prop kinds only (below). Hand-built bodies are refused for library trees (`DR-COPY`); inline `copied` bodies in a map's registry are an open question (WE134) | decoration.md:~1280; BACKLOG.md:734 |
| Wells, market stands, lamps, fences, banners, furniture, ships, signs | **No stamper.** Fences/lanterns appear only as block choices inside a wall/roof/made-layer material. Market stalls are small houses with porches (structures.md:731-748) | [C] `PlacedProp` derived types list: stroke, fluid, tree, boulder, flora, house, chest |
| Roads to a grade | **Yes, in two parts:** a relief `line` mark with `tread`/`batter` grades the ground; a `stroke` prop (or `polyline` shape) paves it. A switchback/spiral road is covered. The stroke *drapes*, it does not grade | relief.md:114-165; decoration.md §4 |
| Kits / starting gear | **No.** One fixed "Standard" kit per team; no kit statement in the intent | configure.md:724-728; TeamsGenerator.cs |
| Gamemodes beyond CTW/DTM/DTC/capture-point/(TDM score) | **No authoring** for CTF flags, payloads, scoreboxes (parser *refuses* such maps); FFA/rage/blitz are not authored | supported-maps.md |
| Portals, kill heights, timed regions, gates by stage, custom filters | **No intent slice.** (pgmvox needs these for 11 of 20 boards, per SHARED-LIBRARY-ASSESSMENT cluster A/B) | /home/user/pgm-studio-mapgen/freeform/SHARED-LIBRARY-ASSESSMENT.md:409-420 |
| Entities (armor stands, mobs other than shopkeepers) | **No** | (absent from docs) |
| Per-team different boards | **No.** A plan is one symmetry unit; `none` symmetry needs every team's units stated | plan.md:11-13 |
| Set build height by hand | **No.** `maxbuildheight` is derived = mean terrain top + 20 and overwrites whatever the intent says | [C] WorldBuilder.cs:141-150 |

---

## 2. Terrain

### 2.1 Relief model (relief.md)

- **Heightfield per group per layer**, solved by a screened-Poisson relaxation between *placed marks*; the group
  (a fused connected landmass) is the unit; one relief per group id (relief.md:2, 31-76; sketch.md:382-385).
- **Marks** (constraints, honoured exactly): `point` (disc), `line` (band around a polyline, per-vertex heights,
  `tread`, `batter`), `area` (ring at one height or per-vertex tilt, optional `bevel`), `rim` (footprint edge),
  `scarp` (two heights + a free face = the break-of-slope instrument) (relief.md:58-66).
- **Push** (a landform on top of the solved surface): drawn ring + amount + `falloff` measured from the ring across
  the land + `roughness`; "top is a field" (ridge crest falls along length, hollow, centre pull) (relief.md:231-330).
- Extras: `reach` (0 = unlimited!), grain, block-step repair, symmetry fold (solved on the folded surface),
  `landform` word, `height_mode`/`relief_scope` per shape to leave the solve (sketch.md:286-296, 387-409).
- Reads: `POST .../sketch/relief/read` raises `RL1-RL6`: RL2 (never graded), RL3 (seam taller than scramble),
  RL4 (mark pinned nothing), RL5 (graded everywhere, level nowhere; bar 30%) (relief.md:78-112) [D];
  `slopes`, `incline`, `reach`, `transect`, `column`.
- Not heightmap noise: **no procedural noise terrain** (the pgmvox `fbm`/ridged-mountain approach has no
  counterpart; SHARED-LIBRARY-ASSESSMENT cluster G says "no noise heightfields"). A `noise` *material* exists for
  paint only.
- Open: carve/graded road should fold under symmetry (S42), water ignores relief (S46), relief key should be
  layer+group (WE28) (BACKLOG.md:149-212).

### 2.2 Shapes catalogue (two meanings of "shape")

1. **Sketch shapes** (above): rectangle/circle/polygon/lasso/polyline + add/subtract/override + height modes.
2. **Composer shapes** (shapes.md): the plan-tier families/bodies; read-only vocabulary for the generator.
3. **Forms** for made things (round walls, domes, ziggurat...) are *not* a library yet (TS63).

### 2.3 Terrain painting (terrain-painting.md, library.md)

- A **theme** = four paint buckets plus bedrock: `rim` (top block of an edge column, depth stated), `wall`
  (exposed riser down to the shallowest neighbour drop), `surface` (stack on interior tops, depth stated), `fill`
  (everything else) [C] `src/PgmStudio.Minecraft/Painting/TerrainTheme.cs:10,483-502`. `RimEdges` = `void`/`drop`/
  `boundary` (TP3).
- Painter touches **only stone**, runs last-but-one (after stamps, before dressing); a stamped block is never
  repainted (TP6).
- **Fourteen material kinds**, all nestable: `solid`, `layered` (band stack with `axis`), `teamTint`, plus area
  patterns (`voronoi`, `cell`, `noise`, `turbulence`, `electric`), wall patterns (`wallRun`, `wallDiagonal`,
  `checker`, ...) (library.md:159-324).
- **Band-stack axes**: `depth`, `inward` (rings from the void edge), `height` (world Y, optionally `follow`ing the
  smoothed ground 0-100%, TP26), **`slope`** (degrees of inclination from Horn's 3x3 gradient, 2 cells either
  side) (terrain-painting.md:186-257). This is the "paint by angle" tool pgmvox hand-codes.
- Per-shape scoping: `theme` (ground) vs `material` (what a thing is made of), smallest-area themed shape wins at a
  column, one theme per layer (sketch.md:189-196, 486-491).
- **Biome**: `BiomeField` = `solid` / `cell` (jittered regions from a palette) / `noise` (banded fractal);
  written as the per-column biome byte, folded through symmetry (library.md:445-475; WorldBuilder biome step).
- Pattern field seeds sampled at the *folded* cell so mirrored boards paint alike (TP21).
- Open: `repeat` band ending named wrongly (WE60) and no cycling ending (WE143); "family on display" judge for
  patterns parked (WE41) (BACKLOG.md:92-147).

### 2.4 Water

- **Fluid prop** (`DR-WA`): `channel`, `pool`, `basin`; forms `canal`/`natural`/`stream`; water or lava; cuts the
  bed into built terrain and fills to a derived or stated `level` (decoration.md §7; sketch.md:1160-1185).
- **Water lanes** (plan zones): void rects filled by PGM's shared fragment 45 min in, re-filled each 15 (plan.md:226-235).
- No relief-aware routing, no per-pool levels, no falls (S46). pgmvox needs "watercourse with reaches and falls".

### 2.5 Void and build zones

Void is simply absence of ground. Holes are made by arrangement (pieces ring a gap) or subtract shapes. A *hole is
never papered over with an add* (SK13). Buildable rects over void come from plan `zones` (cell resolution) or
`intent.build.areas` (block resolution). See section 6.

### 2.6 Trees

- 7 template species (rows: wood + canopy profile radius per course) + **84 copied trees cut from a hand-built
  world** (`tools/seed-trees.cs` over `corpus/tree-showcase`) [C] `src/PgmStudio.Minecraft/Library/trees.json`
  (dict keys `world`,`trees`); 4 boulders (`erratic`, `shattered`, `outcrop`, `cairn`) [C] `boulders.json`.
- Foliage scored against the 75-tree measured corpus (tree-corpus.md); a copied tree carries a `cut` provenance and
  the map credits its builder in `<contributors>` (sketch-world-export.md:212-242).
- Trees are *clicked into place* (position = point, recipe = library row); no scatter; no forest brush
  (decoration.md "Dressing is placed, not sprinkled"; WE107 affinity placement is an unbuilt idea).

---

## 3. Structures and dressing

### 3.1 Houses (`HouseStamper` + `HouseStyle`) — the richest block-level system

[C] `src/PgmStudio.Minecraft/Houses/` (~4.5k lines); doc `structures.md` §7-8; 57 seeded houses in
`src/PgmStudio.Minecraft/Library/houses/`, 8 seeded themes.

- **Footprint**: rectangle, or touching rectangles as **wings** (L/T/U) with joint rules `HJ1-HJ5`; max 192 covered
  cells (`HP3`); min 5 (`DR-SIZE`); axis-aligned only.
- **Roof forms** (height-field `RoofField`): `Flat`, `Gable`, `Hip`, `Gambrel`, `Shed`, `Saltbox`; pitch, overhang,
  slab/stair finish, ridge cap, wear; a house wears no shed (`HS14`, complaint) (structures.md:379-420).
  Rise is always measured over each wing's *shorter* side.
- **Storeys**: a stack with per-storey `clear` (>=3), wall stack, windows, posts, deck/floor zoning; stilts
  (a floor of air); ladder through the deck on the door wall; roof terrace/parapet (structures.md:914-1036).
- **Wall parts** = course stacks of any of the 14 material kinds (wall runs, laid logs, checkered logs, diagonal runs).
- **Beams**: log ends run out past the corners at storey seams (8 ends), requiring a laid-log course and log posts
  (`HS9`, `HS11`, `HS13`).
- **Porch**: strip taken *inward* from the footprint with deck, posts, rail (breaks at the door), own canopy
  (never shed) (structures.md:730-780).
- **Doors**: closed set `air` / `cobweb` / `stained glass` / `glass panes` (`Domain.DoorMaterials`), because a wool
  room's block rule is a whitelist — a door outside it would seal the cage (structures.md:838-850). Door head can
  be `Arched` (two upside-down stairs, optional span).
- **Windows**: five forms — stair `lattice` (2x2), `slab band`, `panes`, `open`, `arched`. **Is there a window/door
  keep-apart rule? Yes.** Each wall is seated on the run *between its two corners*; windows are spread evenly and
  centred; *"any seat that would meet a doorway, or the block of wall either side of it, is dropped rather than
  shifted"* (structures.md:803-807, repeated :875; [C] `src/PgmStudio.Minecraft/Houses/HouseWindows.cs:281-283`).
  Also every opening keeps >=1 block of wall clear of each corner (structures.md:854-860); a window may be bound to
  a *host block* so it only seats inside a banded panel of that material (structures.md:810-822); an opening that
  does not fit between sill and the last wall course is not cut.
- **Foundation**: plate + surface zoning (border/field/inlay); footing absent by default and `HS7` complains of one.
- **Blocks refused**: ore anywhere (`HS5`), surfacing soil in a wall (`HS16`), snow/ice (`HS17`), a wall checkered in
  its posts' own log (`HS15`) (structures.md:1077-1105). 22 `HS*` rules in total.
- Library: a house is composed from *roof_style*, *storey_style*, *porch_style* rows bound by a `room_style`
  (structures.md:1152-1200); previews are stamped by the real stamper (isometric, plan, section, cutaway).
- **Siting rules** as a placed prop (`DR-*`): seats on the *lowest* footprint column, digs out above (`DR-DIG` >3
  blocks complaint), `DR-SLOPE`, `DR-SITE` (ground under every cell), `DR-PASS` (**8 blocks of passable ground on
  every side**, counted from what the building stamps; a group of near buildings is one block of buildings),
  `DR-SPAN` (not across the whole land), `DR-CLAIM` (3 blocks between walls), `DR-CROSS`, `DR-WAY`, `OB19`
  (>=4 blocks from a goal's structure) (decoration.md:862-1000).

### 3.2 Dressing props: exactly seven kinds

[C] `PlacedProp.cs:27-34`: `stroke`, `fluid`, `tree`, `boulder`, `flora`, `house`, `chest`.

| Kind | Placed by | Notes |
|---|---|---|
| `stroke` | trace a line | repaints top course only (a finish, not terrain); styles `solid/worn/rough/stones/tapered`; `pave` = any of the 14 materials; `claimsGround` for routes vs paint; `wander` bend |
| `fluid` | trace/ring | carves bed, fills water/lava |
| `flora` | trace a ring | noise field of tall grass/fern/flowers; coverage, scale |
| `house` | drag rectangle(s) | above |
| `tree` | click | template or copied |
| `boulder` | click | 4 forms; may moss |
| `chest` | click | up to 27 stacks, enchantments by PGM name; `y` for a deck; no refill (WE154) |

Every prop is fanned over the symmetry orbit (turning facing data), seeded for reproducibility, and held to
the claim book (`DR-CLAIM`, `DR-KEEP`, `DR-ROAD` 3 blocks tree / 2 boulder off a claiming road). Declines come
back as `DR-*` findings and in `region/dressing-report.json` inside the export zip.

**There is no stamper for wells, market stands, lamps/posts, fences, walls (as props), statues, ships, signs,
banners, furniture.** Such things are either houses, or are *drawn* as "made thing" layers (shape sets with
materials) — expensive: measured 5 layers for a robot, 16 if banded by geometry; the gatehouse is 8 layers / 74
shapes (BACKLOG.md:250-256). A form library (TS63) is open. This is where pgmvox's `props.py`/`pieces.py`/`facade.py`
have an advantage.

### 3.3 Made things (`kind: made` layers) (sketch.md:509-575)

Layers can hold ship/balloon/statue/gatehouse sculpture: out of the stacking rules (`SK10/SK11`), painted before
ground (TP25), `part_of` groups slices, `seat: ground` seats the whole thing with one drop number and cuts the bank
out of its footprint. Block data with direction (ladder, stair, log axis, torch, chest) is **turned per orbit image**.
Open: one row in the layer strip (TS64), team-colour per image (WE74).

---

## 4. Objective and gameplay stampers (every automatic stamp the export applies)

Orchestrator: `PgmStudio.Export.WorldBuilder.Build` [C] `src/PgmStudio.Export/WorldBuilder.cs:118+`. Pass order:
rasterise -> terrain -> wool rooms -> spawn rooms (+ monuments, iron) -> plan structures (entrance line, iron cubes,
approach walls) -> build-region marker -> destroyables -> cores -> control-point pads -> **terrain paint** -> dressing
-> **sky markers** -> biome -> observer platform -> level.dat/pictures.

| # | Stamp | What is written | Where (code) | Notes / rule |
|---|---|---|---|---|
| 1 | **Sky marker above each goal** | 3x3x3 **wool** shape hung at `buildCeiling + 5` (so mean ground + 25): a **solid cube over each wool room** in the wool colour; a **3-D asterisk ("Cross")** over each **destroyable and core** in the owner team's colour; a Cross in the neutral colour over each **capture point** (the point's display region covers it so PGM recolours it) | `Stamping/GoalMarkerStamper.cs:23-76`; stamped late at `WorldBuilder.cs:441-443`; CP marker `WorldBuilder.cs:828-838`; constants `Domain/BuildCeiling.cs:25,35` | Clamped under the world ceiling; "nobody can reach or grief it"; `OB23` complains if a goal tops out above the ceiling |
| 2 | **Build-region marker** | **Unpowered redstone wire at y=1**, one air block clear of the build region and of terrain (so 2 blocks out from the edge), only along edges that face void, corners turned into rings | `Stamping/BuildMarkerStamper.cs:5-105`; call `WorldBuilder.cs:295` | rule `ST5`; no signs, no fences, nothing at play height |
| 3 | **Bedrock approach wall + defence chests** | Bedrock from y=0 to **3 courses over the highest solved ground** along the seam, 2 thick; 1 or 2 (lane >10 wide) **defence chests** set into the approach face, lid-air above; the far face stays full bedrock | `Stamping/StructureStamper.cs:207-270`; `DefenseChest.cs`; `WorldBuilder.cs:565-566` | `ST4` (<=4 courses proud), `ST8` (10-20 long), `ST11` (10-20 from the wool room), `PL11/13/17` |
| 4 | **Defence chest (27 slots)** | 32 per slot: 12 slots dark-oak planks, 7 spruce planks, 4 crafting tables, 1 end stone, 1 redstone block, plus **2x Efficiency II iron pickaxes** (= 27 slots) | `Stamping/DefenseChest.cs:35-110` | At walls **and** at every destroyable/core |
| 5 | **Destroyable plate** | one-block **5x5 bedrock plate 3 courses beneath** the ground the goal resolved on, centred on the anchor; **a core takes none** (you dig to a core) | `StructureStamper.cs:143-175`; `WorldBuilder.cs:673-675` | author's ruling |
| 6 | **Goal-side defence chest** | the same 27-slot chest set into the ground at the anchor column, course over it carved to air | `StructureStamper.cs:185-206`; `WorldBuilder.cs:675,869` | destroyables and cores |
| 7 | **Destroyable / core structure** | styles `pillar-1/2/3`, `cube-3/4` (hollow bedrock centre), `column-plus` in obsidian/emerald/gold/ender stone; core = obsidian casing + lava interior, optional open top; both **float** over the highest ground their footprint spans | `Stamping/ObjectiveStamper.cs`; `WorldBuilder.cs:660,860` | float default 4 (D) / 6 (core), <=12 (`OB22`) |
| 8 | **Wool room** | foundation (levels ground upward), shell from the bound room style (default placeholder, `WX14`), wool **pad** (2x2/3x3, the wool colour = exported point), **4 interior corners x 2 stacked chests** (A: planks x16, Speed I 3:00 potions, golden apples x16; B: diamond leggings, Power I+Infinity bows, planks x16), doors = stained glass panes in the wool colour, **lit redstone entrance line with torches at the ends** along every entry seam | `Stamping/WoolStructureStamper.cs`; `WoolChests.cs:28-60`; `StructureStamper.cs:96-115` | `WX1-WX14`, `ST1`, `ST9/ST10`, `WL11` |
| 9 | **Spawn room** | foundation, shell (default spawn style) with an **always-open air door** on one or two walls, **pad in the team colour** (exported spawn point = pad centre), **wool monuments** inside, renewable **3x3x3 iron cubes** beside the door | `Stamping/SpawnStructureStamper.cs`; `WorldBuilder.cs:216-237` | `SP*`, `WX*`, `ST2`, `WX8/9` |
| 10 | **Monument** | bedrock pedestal one above the floor, **air placement cell**, stained-glass cap in the wool colour, **wall sign** "Place the / **<Colour>** / Wool / here!"; positions derived from the capturing team's spawn (authored location is replaced, `OB25`) | `Stamping/MonumentStamper.cs`; `RoomFrames.MonumentSlots` | author's ruling: monument = standalone stamp near the spawn |
| 11 | **Capture-point pad** | clay pad (neutral colour) cut *into* the ground at the highest footprint ground with a skirt (<=8) so no air beneath, plus a cleared capture volume | `Stamping/ControlPointStamper.cs`; `WorldBuilder.cs:715-719` | pad is flat so PGM's progress pie is centred |
| 12 | **Observer platform** | solid **6x6 bedrock** at the observer's floating authored Y (lifted above anything under it, `EX5`), **four 1x2 bedrock info boards with 2-sign pairs** (map name + `[CTW/DTM]` gamemode, and "made by" + authors); omitted authors -> `EX6` | `Stamping/ObserverPlatformStamper.cs`; `WorldBuilder.cs:462-476` | |
| 13 | **Iron cubes** (standalone) | 3x3x3 iron block, resting on the ground its footprint spans | `StructureStamper.cs:128-141` | renews only in a spawn piece (`ST2`) |
| 14 | **Biome byte** | per-chunk/column biome from the map's `BiomeField` | `Export/BiomeScope.cs` | runs after every pass that can add a chunk |
| 15 | **`map.png`**, `level.dat` | 290x246 picture in block sprites; world spawn at the observer | sketch-world-export.md:25-30, 203 | needs textures (`RQ10` otherwise) |

**map.xml standards written at export** (not stored): `itemkeep`, `toolrepair`, `itemremove` (kit armour + terrain
drops + every objective material), block-drop chance 0 for kit blocks, a per-kill building-block reward,
`gapple-kill-reward` include, hunger off [C] `src/PgmStudio.Pgm/Authoring/MapStandards.cs:1-130`. **Kits:** one
fixed "Standard" preset (iron tier + infinity bow, planks + team clay, golden apple + water bucket, team leather
armour) [C] `TeamsGenerator.cs:40-60`.

---

## 5. Rules, gates, read-backs

### 5.1 Counts

Declared rule constants carrying `[Rule(RuleCategory...)]` in `src/`: **262** (my regex count over all projects;
`docs/refusals.md`/briefs say "about two hundred rows" [D]; the discrepancy is probably because several are
internal). By family [C]:

- **`LayoutRules`** (`src/PgmStudio.Domain/LayoutRules.cs`, 387 lines): **58** ids — `G2,G5,G8` (3), `LN1,2,5,6` (4),
  `CT1,4,5,8,9,12,13,14` (8), `SP1,2,8,9,10,11` (6), `WL2,7,9-20` (14), `FR4,6,8,9` (4), `MD7,8` (2), `EL1` (1),
  `BZ5,6,9,11,12` (5), `GO1-4` (4), `ST1,2,4,8,9,10,11` (7). **`HB1-HB4` and `PC*` exist in `rules.md` but are not
  served as raised rules** (HB is argued only) [D rules.md:252-266].
- Objective: `OB*` (16), `DC*` (3). Room frames `WX*` (10 declared + more in docs). Sketch `SK*` (31), refinement
  `SR*` (8), plan `PL*` (17) + `PC-C`, relief `RL*` (6), edit zones `EZ*` (2), export `EX*` (6), house `HS*` (22),
  `HJ*` (5), `HP*` (3), painting `PT*` (5), `DR-*` (~25 dressing rules), request `RQ*` (19), library `LB*` (6),
  import `IM*` (7), edit `ED*` (4), shop `SH1`, box `BX*` (10).
- Categories (`RuleCategory`): Unplayable 87, Conflict 66, Unsatisfiable 58, Malformed 21, Unknown 14, Unavailable 7,
  Forbidden 4, Internal 3, Unfinished 2.
- Severity: `refusal` (stops), `decline` (work done, one piece not in the world), `complaint`. Finding record =
  `{rule, message with numbers, severity, field?, subjects?, edit?, cites?}`; `edit` states the mechanical fix
  in the document's own vocabulary (refusals.md:1-97). Rules are served from `GET /api/rules` with `meaning` and
  `fix` text.

### 5.2 What the numbers protect (gameplay)

| Group | Representative limits (blocks) | Protects |
|---|---|---|
| Objective distances `GO1-4` | enemy:own spawn walk ratio 3-4x; goals of one team 35-65 apart; enemy goals 85-150 apart; goal to own spawn 40-90 | destroy-map fairness (from the ratio `(L-d)/d`) |
| Wool timing `WL2/7/9-19` | spawn->nearest wool 29-176 (and >=20); wool<->wool 50-227; farthest <=1.22x nearest; wool->crossing 22-147 | pacing of captures |
| Spawn `SP1,2,8-11` | spawn near the back half; door egress step <2; >=15 of ground ahead of the door; spawn->crossing >=55 | spawn safety, no spawn-kill pocket |
| Lanes `LN1/2/5/6`, `G2/G5` | lane width 10-30; run 25-110; hop gap 10-20; ground off routes <=12%; hole >=12 | readable circulation, bridgeable gaps |
| Crossing `CT1,4,5,8,12-14`, `FR*`, `MD*`, `BZ*` | strait 15-40; <=3 build regions joining sides; attackers' route <=87.5% of defenders'; frontline >=15 blocks (`FR9`) and <=16 cells wide (`FR6`) | no turtle/sealed halves, fair crossing |
| Elevation `EL1`, `SP8`, `WL11`, `WX11`, `RL3` | step >=2 between pieces/at doors is a complaint | stepping out of a spawn |
| Rooms `WX*`,`ST9/10` | footprint >=4 across, spawn/wool room <=20x20 building, protection <=20x30; door 2/3/4 wide | stamped rooms that actually fit |
| Objectives `OB*` | not over void (OB17), not in a spawn/wool room (OB30), float <=12, <=20 over mean ground (OB23), no tree/boulder/house within 4 of a goal (OB19), `OB24` overlap | winnable, uncovered goals |
| Walls `ST4/8/11`, `PL11/13/17` | wall <=4 proud, 10-20 long, 10-20 from the room, no open shoulder | a "line, not a barricade" (approaches.md) |
| Dressing `DR-PASS` etc. | 8 blocks of passage each side of a house group | a building must not cork a lane |

Gameplay oracle: `docs/gameplay/approaches.md` (all claims author-confirmed) says what composed objectives are
(approaches from around/above/below/through), void belongs between teams not across a destroy approach, a bay
>=16 at a goal, wool room in a corner (two faces on void), etc.

### 5.3 Export gate

`GET /xml` and `/export` refuse with the one envelope: `OB20` (unknown gamemode), `EX1` (not traversable), `OB17/OB30/OB31`,
`OB24`, `EX2` (nobody can enter), `EX3` (a kind stated went missing), `EX4` (objective with no team), `SH1`,
`DR-DOC` (dressing document will not parse at all -> 422, never partially read). Preflight (`/preflight`) runs
round-trip (blocks), mirror, buildability, build-zone reach (`EZ2`), traversability (blocks) (configure.md:423-445).
The world build behind read-backs runs **no gate** on purpose (read-backs.md:22-24).

### 5.4 The walk (movement model) [C] `src/PgmStudio.Geom/Walk.cs:210-283`; [D] read-backs.md:72-233

Node = a **place** `(x, z, y)` (a cell and its storey); needs **2 clear blocks** of headroom; 8-connected
(diagonal 141/100, refused if a squeezed cell is a drop). Costs, each in its own unit and never weighed against
each other: `reachable`, `distance` (blocks), `blocks` placed, `drops`/`worstDrop`.
- Climb of delta costs **delta-1 blocks placed** (`FreeRise=1`); `ScrambleStep=2`; `WallRise=5` (>5 is a face);
  `FreeDrop=3` (4 = fall damage; every kit carries a water bucket so a fall never walls a route off, but it is
  counted); void inside a build zone costs 1 block/cell; **water costs no blocks, doubles distance**.
- `aim`: `travel` (shortest, reports blocks) / `reach` (fewest blocks) / `comfort` (<=10 blocks longer, max edge
  clearance). `team` narrows by `enter` rules (spawn protections, own wool room); door of glass/pane is open where
  breaking is allowed.
- Props: a tree/boulder is solid to headroom but never somewhere to stand.
- **No ladders, no jump arcs/gap jumps, no pads, no knockback, no fall-damage model, no sight/exposure.** Confirmed by
  grep: no `ladder|jump|trampoline|knockback` in `Walk.cs`; also stated in
  `/home/user/pgm-studio-mapgen/freeform/SHARED-LIBRARY-ASSESSMENT.md:10-20, 411-420` (the pgmvox side's own
  inventory of this gap).

### 5.5 Read-backs (read-backs.md; all HTTP, mostly `?format=text`)

`render/topdown` (subjects ground/structure/made/foliage/objectives; `layer`, `ymax`), `section` (+text), `heightmap`
(+text), `surface`, `traversability`, `structures`, `mirror`, `isometric`, `xray` (roofed-void scan),
`render/walk` (cost field + route picture) and `walk` (numbers: `places`, `steps`, `beside`), `column` (bedrock to sky, text), `transect`,
`slopes` (`. : #` tiers), `incline` (tens of degrees), `reach` (stranded ground patches), `editability`,
`coverage` (reached/decorated/dead cells), `kit-reach` (blocks needed vs kit), `wool-availability`, `themes/census`,
`stroke`, `render/eye` (+`/pick`, 1.8 block sprites), `render/picture`, `report` (one document with the three
headline numbers), `diff` (edits + changed columns, PNG). **Only on a stored map** (read-backs.md:15-20;
SHARED-LIBRARY-ASSESSMENT cluster L).

---

## 6. Build regions: how they reach `map.xml`, and how precise

- **Substrate is the terrain, not a region.** PGM's void filter `block = not(void)` applied to the negative of the
  build group makes any column with a block at y=0 editable, so islands need no region (new-map-authoring.md:161-170).
- `BuildIntent` = `maxHeight` + `areas` (over-void extensions) + `holes` (no-build cutouts). `BuildGenerator` emits
  a single apply over `not-build-area` with `block-place="block-place-void-filter"` and
  `block-break="block-break-void-filter"` (break additionally allows what dressing leaves hanging over void —
  tree logs, leaves, flora); a map that declares no `areas` writes no void rule (configure.md:285-325;
  new-map-authoring.md §5b). Spawn and wool-room protections are emitted *before* the build rule because PGM stops at the
  first deciding apply (configure.md:147-155).
- **Precision.** Areas/holes are **axis-aligned rectangles**, unions thereof, stated in blocks on the intent but
  at **cell resolution** (`cell` x n) when they come from a plan `zone` (plan.md:221-235). `holes` become a PGM
  `complement`. There is no polygonal or per-column build region, and no way to make a floating island buildable
  via the y=0 rule (a floating island has no block at y=0, so it reads as void **[I]**; basis: `editability` defines `ground` on a void-enforced map as "exactly the
  columns with a block at y=0", configure.md:645 and read-backs.md:48).
- **Build height cannot be stated:** derived as mean terrain top + 20 (`G6`) and overwritten onto the intent
  (`WorldBuilder.cs:141-150`); erected terrain raises the mean it is measured over, so a tall wall cannot sit
  above the cap (plan.md:163-176).
- In-world marker: redstone wire at y=1 (section 4 #2).
- Checks: `EZ1` (a patch of standing ground nobody can edit), `EZ2` (void between a coast and a build zone nobody can
  bridge), `BZ5/6/9/11/12` at plan level, mirror check on build zones.

---

## 7. Strengths a pgmvox-style generator would lose if it replaced the studio wholesale

1. **A multi-user, authenticated web app with a real DB.** MariaDB + FluentMigrator (~64 migrations), Discord
   sign-in with whitelist/invites/roles, bearer tokens that act as the person (`docs/access.md`), deployed at
   pgmstudio.de on 4 GB / 2 cores with a 3-at-once build queue (`docs/deployment.md`).
2. **Every map is four+ versioned documents.** Numbered change history per slug with writer/token/origin/note,
   `diff` between any two changes (edits + changed columns + PNG), `restore`, optimistic concurrency (`ETag` / `If-Match`
   -> `RQ13`), and the *hand-edit handoff* (`SR1`): an author's UI edit is handed to the agent's next round instead
   of overwritten (flow.md:243-273, 371-420).
3. **Human review loop in the product:** Sketch Review phase with named camera views, notes pinned to ground with
   pictures and replies, `GET /notes/handoff` fires an agent routine (sketch.md Notes) — the author's feedback channel.
4. **One validation envelope and a generated rule catalogue** (`GET /api/rules`, `/glossary`, `/rules/terms`), each rule
   with meaning + fix text, `edit` proposals, `Pgm-Warnings` header, `RQ3` naming every unread field of a posted
   document (typo detection), generated Python kit with word-set checking (`/kit.py`).
5. **Playability gates built on a measured corpus:** 58 layout rules calibrated on 350 corpus maps / 1,616 scanned
   map dirs; the export gate and preflight; `--goldens` regression net over every corpus map
   (`tools/PgmStudio.RoundTrip --goldens`) so a derivation change reports which maps moved.
6. **A real `map.xml` codec and parser:** `MapParser` (with the supported-maps gates), id-keyed regions/filters,
   include resolution, round-trip check, `template.xml`, the intent -> 19-region/20-filter/11-apply-rule projection,
   shops/shopkeepers/spawners/kill rewards/standard item rules, control points and score. pgmvox's `mapxml.py` is
   201 lines of literal XML lines (SHARED-LIBRARY-ASSESSMENT §2.11).
7. **Symmetry as a first-class citizen:** the canonical `Geom.Symmetry` fan applied to shapes, relief (solved on the
   folded surface), paint (sampled at the canonical image), props (turning direction-carrying blocks), rooms (hands:
   left/right swap on reflected images), plus the `mirror` read-back. pgmvox has `orient.py`/`mirror` in places.
8. **A painting system with 14 nestable material kinds, slope/height/depth/inward axes, team tinting and biome fields,
   previewed server-side** through the real painter; theme library; per-shape scoping.
9. **A house system with 57 seeded styles, 22 style rules, wings, storeys, roofs, porches, beams, windows and a
   composable parts library**, with siting rules (`DR-*`) and an interactive editor. This is the strongest
   block-level asset the studio has.
10. **UI tools:** Plan/Sketch/Configure/Library/Generator/Shape catalog, undo, 3-D (WebGL) preview, history,
    keyboard-driven canvas; 257 client files / 31k lines. None of this exists on the pgmvox side.
11. **Operational tooling:** e2e gate (`tools/e2e.sh all`), CI on PRs, build gate with warnings as errors, JS suite,
    census, figure-check, ~4,100 tests.
12. **Corpus knowledge:** block palette, terrain ground truth, monument suggestion, 75-tree measured corpus, the
    `docs/gameplay/` match-flow account — see `docs/world-scan/*` (some of these inform rules but are not runtime).

---

## 8. Known limits and open backlog relevant to richness, underground, structures, props, discoverability

### 8.1 From each tool document's Limits

- **Plan** (plan.md:960-995): rectangles only, no polygon/curve/lasso; one flat surface per piece; no stack; no paint
  or dressing; observer not placeable; destroy objectives only at symmetry order 2.
- **Sketch** (sketch.md:2555+): only *Draw* edits geometry (Theme/Relief/Dressing select only); symmetry is a
  preview/mirror flag, not a constraint (nothing checks the two halves agree); "almost nothing validates a sketch";
  `circle` cannot be drawn in the UI; a *picked piece* can move but not resize.
- **Configure** (configure.md:724-770): kits not editable; water lanes not authorable here; buildings not choosable;
  a corpus map has no intent and cannot gain one; "nothing here judges how a map plays".
- **Generator** (generator.md:424-470): library only; no on-request boards; only two-team rot_180/mirror_z reachable;
  boards are flat, unpainted, CTW-only; census inflates over a session.
- **Library** (library.md:1040-1070): library edits never reach maps that copied a row; windows/rails are single
  blocks (no patterns).
- **Walk**: no ladders/jumps/pads/knockback (5.4).
- **World scan** `WS74`: 169 of 911 corpus maps read "not connected" under traversability and are baseline-parked.

### 8.2 Open items by theme (BACKLOG.md / TODO.md / ideas)

TODO.md holds exactly one entry: **TS130** — point edits and bends should reach relief rings and prop points
(TODO.md:19-27). Everything else is in BACKLOG.md (779 lines).

| Theme | Task | State |
|---|---|---|
| Underground/caves | **TS140** carve (3-D bore with radii, negative boulder) | open (BACKLOG.md:312) |
| Underground objectives | **B264** Configure cannot address a storey; only `PUT /intent` can place a below-top objective | open (:224) |
| Relief | **WE28** relief key = layer+group; **S42** carve/road must fold under symmetry; **WE148/149** mark/push diagnostics | open (:149-197) |
| Water | **S46** water reads relief, per-pool levels, river-on-axis is a canal | open (:199) |
| Painting | **WE60/WE143** band ending names + cycling strata; **WE41** pattern-as-family judge (parked); **WE46** building must not wear the ground's tone family | open (:92-147) |
| Made things / structures | **TS63** form library (arch, ziggurat, ellipse wall, tapered tower, dome); **TS64** one row per made thing; **WE74** colour per orbit image | open (:233-260) |
| Houses | **WE162** two seeded houses' doorways land on different columns in a mirror image; **WE152** door width by style | open (:263-310, 702-713) |
| Dressing | **WE104** vertical-surface dressing (moss, vines, scree); **WE107** affinity placement (a brush); **WE106** biome/season driver; **WE108** dressing budget; **WE109** border/POI framing; **WE154** refilling chests; **WE134** inline copied tree bodies | idea pool / open (ideas.md:50-99; BACKLOG.md:261-295) |
| Objectives/shops | **TC7** hill step, **TC9** shop step (API-only today); **PG15** spawner ramps; **PG16** spawner height | open (:66-83, 335-355) |
| Plan model | **B213** lock a wall's interface in the sketch (a re-bowed coast can walk round it); **G268-G270**; **G285-G289** one measure for crossings, 3-block steps | open (:436-531) |
| Walk | G285 straight bridge from the nearest land; G286 3-block step | open (:491-531) |
| Discoverability | **RP99** terms defined where they appear (`Term` component); **RP100** map authors on the list; **TN25** plan undo; **C69/C70** UI direction (parked) | open (:532-640) |
| Coast bend | **TS156** a bend control on the canvas (only via API now) | open (:295) |

### 8.3 Discoverability

The system is explicit that capability lives in generated reads (`GET /api/openapi/v1.json`, `/glossary`, `/rules`,
`/kit.py`), because hand-written lists drift (ORDER-OF-WORK.md "Where the detail is"). The first-time-reader backlog
(BACKLOG.md:532-596) admits the UI itself lacks term help and uses monospace for everything. The mapgen CLAUDE.md
says "None of it (look/tone rules) is enforced anywhere" — gates measure play, not appearance (WHAT-A-BOARD-IS-MADE-OF.md).

---

## 9. Quick matrix: pgmvox-side asks (SHARED-LIBRARY-ASSESSMENT.md section 3) vs. the studio today

(The studio-side column below is *this inventory's* reading; the "Studio today" column in that assessment is the
pgmvox author's reading and agrees on every row I checked.)

| Cluster | Studio status |
|---|---|
| A. Round-trip for other gamemodes (KOTH/FFA/TDM/CTF/payload/scorebox/portals) | KOTH (control-points/king) + TDM-score parse and author; `flags`, `payloads`, `<score><box>` refused by the parser; no portals, kill heights, timed clear |
| B. Objective pieces writing their own regions | wool/destroyable/core/control-point/shop/spawner write regions; nothing else |
| C. Plan-time reads (jumps, sight, stages, arrival times) | plan-tier `PlanNav`/`PlanRoutes`/coverage/flow text exist; no jump, sight, or stage model |
| D. Physics reads (pads, fall damage, knockback, no-catch) | none |
| E. Team colour swapped by symmetry turn | `teamTint` is per-theme-cell via territory; facing blocks turn; no per-piece colour slot swap |
| F. Bridges/stairs/tunnels that know the ground | stairs via tilted quad (`anchor_heights`, SK26 landing check), bridges = build-zone over void; no carve layer |
| G. Landforms, watercourses | relief marks/pushes; no noise heightfields, no falls |
| H. Floating masses/undersides | per-shape flat underside; cloud/sky stage not gameplay-ignored (made layers are) |
| I. Props with a shape rule | seven prop kinds + made layers; no parametric prefab library |
| J. Patterns | strong (14 kinds), paint only |
| K. Placement | claims/clearances exist; no polyline-distributed placement or affinity brush |
| L. Seeing the world | rich but only on stored maps (no free-standing world input except `tools/anvil.py` on the mapgen side) |
| M. Plan in polygons | no: plan is cell rects; polygons are sketch-tier |
