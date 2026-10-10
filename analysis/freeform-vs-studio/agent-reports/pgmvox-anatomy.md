> Written by a Sonnet 5.5 helper agent on 2026-10-10 and committed as it wrote it. Checked against the code before commit: the door/window finding (build.py:345, :434, :442-450) and the Riftwater house.py lines are correct. The phrase "July-style Python" in §4.1 means the bespoke pre-library scripts; nothing else was changed.

# pgmvox anatomy and board census

Scope: branch `freeform` (142 commits since main, 2026-10-07 19:14 to 2026-10-10 00:34, commit-stamp times). Library `freeform/lib/pgmvox/` v0.18.0, 7,737 lines in 32 modules, 90 tests (`lib/tests/test_pgmvox.py`, 1,012 lines) plus `lib/check.py` (snapshot gate). All paths below are relative to `/home/user/pgm-studio-mapgen/freeform/` unless they start with `lib/pgmvox` (= `lib/pgmvox/`). Where I infer rather than read, it is marked **[inference]**. Two small experiments I ran (door/window adjacency, door facing at oblique headings) are marked **[measured here]**; scripts are in the scratchpad (`wtest2.py`, `dtest.py`, `dtest2.py`).

---

## 1. The process

### 1.1 The pipeline as code

`lib/pgmvox/run.py:21` fixes the order: `STEPS = [plan_check, sketch, gen, write, mapxml, renders, walk]`. `python3 -m pgmvox.run <board-dir>` runs each board script in a subprocess, writes `renders/plan-check.txt`, `renders/00-plan-sketch.png`, `renders/gen.txt`, `world/region` + `level.dat` (through the studio's Anvil writer via `data/write_world.cs`), `scripts/map.xml`, the render set, `renders/walks.txt`, and `renders/build-info.txt` (library version). Every board is therefore re-buildable from one file set in 30 s to 95 s (riftwater port ~30 s; brassmoor ~95 s, "nearly all of it the read-back's four voxel walks"; generation under 1 s on small boards, ~5 s on riftwater).

End to end, as practised on the later boards (claywork, lantern-karst, calcite, trials):

| # | Step | Artifact | Who/what decides |
|---|---|---|---|
| 0 | Read: AGENT-GUIDE, ORDER-OF-WORK, `approaches.md`, `match-flow.md`, lib README | — | (not counted in trial times) |
| 1 | Plan as code | `scripts/plan.py` (+ `PLAN.md` prose) | agent; the numbers carry targets |
| 2 | Plan check | `scripts/plan_check.py` -> `renders/plan-check.txt/.json` | measured walks, jumps, sight, SP/WL/GO rules, widths |
| 3 | Sketch with annotations | `scripts/sketch.py` -> `00-plan-sketch.png` (one sheet) | `pgmvox.sketch` |
| 4 | **Author review of the sketch** | commit message "waiting on a go/review"; `plan_v1.py`, `sketch_v1.py` kept | human; see below |
| 5 | Build | `scripts/gen.py` (+ `dress.py`, board-local builders) | reads plan; adds only what the plan's "look" section said |
| 6 | Write + map.xml | `world/`, `scripts/map.xml` | `objectives.write` + `mapxml.Doc` |
| 7 | Read-back | `scripts/walk.py`: voxel walks, `Objectives.check(w)`, `audit.footing`, `audit.loose_water`, no-stand-above, jump/catch checks | the last check, not the first |
| 8 | Renders | iso (2 corners), elevations, true-scale cutaways, x-ray, annotated top-down | `pgmvox.render`, `sketch.MapPanel.built` |
| 9 | Report | `REPORT.md`, last section a 3-column table | see 1.4 |

The author-review loop is visible in the git log: Lantern Karst (CTW) went through five plan commits in 43 minutes (09:50 -> 10:33: "second plan after review", "third plan - lanes 12-16 wide, steps 12 apart", "fourth plan - Ledges halved, no pools", "plan final") before one block was placed (10:45). Calcite (KOTH) went through three plans, built, then "rebuilt after review" (11:45 -> 12:39). Claywork: v1 layout 11:57, v2 12:27, v3 12:37, v4 12:45, built 13:15, "after review" 13:35. The AGENT-GUIDE phrase for this is "A capture plan was revised four times with the author in seconds each, because the plan was one file and the checker and sketch reran from it."

### 1.2 What the guide makes mandatory, and what it leaves free

`lib/AGENT-GUIDE.md` (176 lines) is mostly "should", with these hard edges:

- "**Four documents before the first line of a plan.**" (guide, ORDER-OF-WORK, `approaches.md`, README) and `match-flow.md` "A plan decided without it is decided on look alone."
- "**A board is decided in its plan, and every expensive failure here was a plan failure.**"
- "**A plan is complete when it states five things, in this order**": identity (one sentence), arrangement, **numbers**, places, **look decided now** (biome, three tone families, material per role).
- "**A number in the plan carries its target.** ... A number without a target is a description; it cannot fail, so it cannot catch anything."
- "**A red row is resolved or explained before the build.** Move the piece, change the target with a reason, or write in `PLAN.md` why the miss stands. A build started over a red row has made the decision without saying so."
- "**The first plan is kept when the plan changes**" (version suffix, plus a "what changed and why" section).
- "**A plan states what the build will add and the plan does not show**" (scenery outside the play area, facade patterns, terrain past the edges).
- Sketch: "**drawn before anything is built**... a sketch carries as much detail as its plan, and no more... A texture or a facade in a sketch looks like a decision and is not one." Required panels: board from above (floor heights written on pieces, places named, team-coloured objective markers, image half paler), routes (arrowed, with jumps and gaps), true-scale sections (kill height/water marked), the check table. "Every panel's title carries its legend."
- "**The read-back is the last check, not the first.**"
- "**What must come from the library**: blocks, orientation/turning, conventions (heights, symmetry, directions, eye height, random streams), writing the world, map.xml through `objectives` and `mapxml`, the read-back. **Should**: plan (`Raster`, `Course`, `Symmetry`), walk graph, sketch, `run`. **Free**: terrain, landforms, routes, buildings, patterns, solids ("A `World` is two numpy arrays; write any geometry straight into it")."
- "**A thing written twice belongs in the library**... Do not change pgmvox in the middle of a board run; write it locally and say in the report what the library should take." `python3 check.py` before any library commit.
- Report: "**ends with a table**: what you wanted, how hard it was, what a studio feature would need" and "Say what the plan missed."

Per-mode plan content (guide table): destroy = goal off the spawn line, exposed, composed ground, goal walks vs studio rules, every underground layer with its own floor and way in; CTW = lane widths, gaps between stones, wool-room doors/entry rules, build zones, void and kill height; attack/defend = stages proved unskippable by walking with later gates shut; payload = the track as PGM traces it; KOTH = equal arrival per team, what a holder sees; arcade = fall model, nothing standable over void.

### 1.3 What plan raster / storeys / plangraph / Course give that a zone plan does not

The studio's plan is "rectangles on a proxy grid" with symmetry fanning (assessment, row M). The freeform plan is:

- **A per-block raster** `lib/pgmvox/plan.py:51 Raster`: `H[x,z]` = y of the floor block (player stands at H+1; one convention written once), `K[x,z]` = kind, plus `stair` directions. Methods `rect`, `poly`, `where`, `flight`, `from_heights` (shaped terrain read as plan), `box`, `mask`. `Symmetry` (plan.py:23) is **applied in the plan**: every rect/poly/flight is drawn twice, stairs turned. Supports `half`, `mirror_x`, `mirror_z`, `cw`/`rot_90` (four teams).
- **Storeys**: `R.storey(n)` (README "Storeys and solids") is a second raster over the same ground, `none` where it has no floor. A cave, a roof, a deck or a tunnel under a plaza is walked and drawn like ground. This is how Claywork's Undercroft, Riftwater's cave/mine/cellar (as storey 1), Hollow Mesa's Throat and Tidewell's gallery were *planned*, not discovered. Plan graph "joins the storeys... ground under a storey is walked only where two blocks of air are left over it."
- **`plangraph`** (`lib/pgmvox/plangraph.py`): `PlanRules` (diagonals -> octile), `jumps` (1-3 block running jumps in any direction, 0.5 s per 374 jumps after 0.8.0), `graph(bridge=zones)` joining every build-zone cell to its 8 neighbours "tagged as built", `measure` ("79, 22 of it bridged"), `dijkstra`, `route`, `path`, `arrivals(spawns_by_team, targets)` and `pad_edges` (jump pads). This is a *capture-board-aware* walk with built-crossing cost; the studio's walk (assessment 0) "is a CTW kit-budget walk with no ladders, jumps, pads, knockback or fall damage".
- **`pieces.Course`** (`lib/pgmvox/pieces.py:73`): a board as an ordered sequence of pieces; a piece off the symmetry axis brings its image, links go step to step; `audit` judges each link with the 1.8 tick model (`move.fall`, `jump_reach`): gap, drop, gentlest way across, landing cell, is-it-water, still-on-piece, damage. `Course.raster()` makes it walkable. Used by Lantern Drop, `examples/drop`.
- **`sight`** (`lib/pgmvox/sight.py`): `line_clear` sampled at 0.25 blocks, `plan_opaque(R, roofs)` / `voxel_opaque(w)`, `visibility(targets, eyes)` and `hidden`. One eye height (`move.EYE = 1.62`), aim 0.9.
- **`move`** (`lib/pgmvox/move.py`): the 1.8 tick model: `fly`, `fall`, `fall_damage`, `jump_reach`, `knockback`, `solve_launch` (pad velocity solver).

The plan check therefore prints every number with its target (e.g. Claywork's sheet: "83 spawn to the band, SP10 at least 55", "75 (7 bridged) band to West Kiln, shortest, WL10e at least 59", "98.7/98.7 red and blue, spawn to their own West Kiln, equal", "0 running jumps between pieces that do not touch", "2 last stone to the flank zone's edge, a jump from a block placed there"). I viewed `lib/boards/claywork/renders/00-plan-sketch.png`: five numbered panels (board with floor heights on every piece and callouts; arrowed routes with dashed over-the-wall variants; two true-scale sections; an Undercroft section; the check table with targets).

### 1.4 What the read-back adds, and what it cannot see

`walk.py` (`lib/pgmvox/walk.py`): `MoveRules(max_drop, jumps, max_gap=3, climb, doors, kill_y, build=(mask,(lo,hi)))`; `standing`; `walk` (exact distance order - fixed in 0.8.0 after a mirrored board read red 81 / blue 83); `nearest`, `unreached`, `no_stand_above`, `catchers`, `gap_cleared`. `audit.py`: `footing` (gravity blocks over air, attachments hanging on nothing), `loose_water` (water with air beside it that is not a fall or the world's edge). `Objectives.check(w)` per objective.

What it cannot see (from the reports' playtest sections): after the author playtested in PGM, Calcite's stairwells ran into 2-high ceilings ("The walk could not have caught it. It counts a place passable with two blocks of air over its floor and does not test a body standing across two columns"); Copperline's spawn-room entry filter was backwards; Lantern Drop's water filter and kill portal (`y="-70"` is an *offset* in PGM, needs `@-150`); Lantern Pass's shooters spawn used a union (PGM cannot draw a point inside one), Speed amplifier is 1-based, steps faced backwards, runners couldn't climb out of the harbour; Saltgate's banner could be lost. None of the new `lib/boards/*` and ports was opened in PGM (their "What was not done" sections say so).

---

## 2. Capability catalogue (mechanism, with file:line)

### 2.1 Terrain

| Capability | Mechanism | Why more expressive than a mark/band stage |
|---|---|---|
| Heightfield landforms as plain numpy ops | `lib/pgmvox/landform.py`: `watercourse` :63 (bed never climbs; reaches and falls; `lowest`, `into`), `lake` :102, `hold` :122 (raises every dry cell beside water to the surface; run last), `canyon` :135 (centreline + cross-section: floor, wall, `ledges`), `spire` :164, `butte` :174 (cliff + talus), `scarp` :202, `terraces` :215, `stage` :226, `grade` :237 (route held to a grade; bridges water; `keep` earlier roads; pins ends), `coast` :288, `blend` :308 | Studio relief is "placed marks; water by height band; no noise heightfields". Here a river is a polyline with a level per reach, a canyon a cross-section profile, a coast an outline. Each op only cuts or only lifts "unless it says otherwise", so the board owns order. |
| Slope as the studio reads it | `terrain.slope_deg` :44 = studio `SurfaceGradient` (Horn over tops 2 cells either side, whole degrees); test holds 21,972 cells equal to a C# export (`data/export_slopes.cs`) | Paint decisions use the same angle the studio's `slope` band axis would |
| Soil by slope, ledge rule | `terrain.lay` :195, `soil_depth` :186 (3/2/1/none; none past 55 deg), `ledge_angle` :174 (a cell level with >=3 of 4 neighbours reads as gentle, <=30 deg) | Cliffs are rock to the face; terrace risers aren't dirt bands; grass holds on ledges |
| Rock beds that dip and fold | `terrain.Strata` :107 (weighted beds, thickest-per-bed, "no bed follows itself", 1-block red bands), `bed_offset` :141, `beds` :152 -> `lay(bands=)`; Riftwater port passes the ground heights as offset so beds follow the surface | Mesa/karst walls show strata dipping across the face; one-block red rule from the paint ruling |
| Scenery mountains outside play | `terrain.mountain_ring` :21 (separate massifs outside a `clear` radius; ridged noise) | Spark/Curio/Copperline: mountains nobody can climb out over |
| Floating islands with real undersides | `terrain.root_depth` :236 (cone * edge-distance**power, roughness, flutes, spires, per-column), `underside` :255 (top_y per column, so islands at many heights in one call; lies wholly inside the floor outline), `forms.skirt` (karst faces under a rim, "never above floor - 2") and `forms.root_vines` | Studio islands "share one plane and one underside profile" (assessment H) |
| Cloud/mist decks | `terrain.cloud_deck` :276 (billows + breaks; fills only air so it wraps mountain feet; glass or wool/snow materials) | Used as the "sea" on 7+ boards; kept above/below gameplay checks |
| Karst towers as stacks of rings | `forms.tower` (`lib/pgmvox/forms.py:29`: rings taper up, ledge every 9 courses, bulge by 3-D noise, beds in courses, crown+pines+vines) | Author singled these out; as a heightfield spire they "came out as plain terrain" (README "Forms") |
| Routes found, graded, paved | `route.find` :45 (48 headings, grade/turn/climb/steep/bridge/avoid/reuse costs; **turn cost is what makes a switchback**: 71 zig-zags -> 5 legs), `network` :185 (trunk sharing at 1/3 cost), `simplify`/`smooth`, `pave` :228 (surface mix, bridge decks, `keep` mask), `steps` :259; `landform.grade` carries the grade into the ground | Studio routes "are strokes an author drags", not found or graded into the ground |
| Terrain checked as a plan | `Raster.from_heights` + the walk graph over shaped heights, before any block | Vale plan check found uplands/canyon rim unreachable before the build |

### 2.2 Underground (`lib/pgmvox/under.py`, 246 lines)

`tunnel` :78 (waypoints (x, floor-y, z, radius); carves a tube but "leaves solid everything under the floor interpolated along it" so a player walks a cave; stays `cover` blocks under the ground; never cuts water), `chamber` :90, `carve` :47, `dress_cave` :96 (floors: gravel/stone/clay/cobble, stalactites, stalagmites against walls, ore glints), `gallery_line` :150 + `gallery` :168 (timbered, rails on level only, stairs on rises, **floor laid after the whole carve** so each rise keeps its stair; timber set only on level), `shaft` :226 (ladder, foot left open where a passage reaches it). Studio has no carve layer ("Pieces are axis-aligned; no carve layer", assessment F). Penstock is the extreme: one block of concrete with rooms cut as boxes of air (`opus55-freeform-penstock/scripts/gen.py`).

### 2.3 Structures (`lib/pgmvox/build.py`, 559 lines)

- **`Frame`** :42 - a building's own axes at any heading. `local`, `world`, `mask(L, W)` (a block belongs when its *centre* is inside), `grid`, `cells`. Walls are the blocks inside with any of **eight** neighbours outside (`shapes.boundary(diagonal=True)`) so a 45-degree wall is closed.
- **`RoofField`** :107 - port of the studio's `PgmStudio.Minecraft.Houses.RoofField`: six forms `FORMS = gable, flat, hip, gambrel, shed, saltbox` (:38), half courses, eave falling to `MAX_EAVE_DROP = 2`, `framed()` :132 measures wall-line distances in the frame. Test runs it against `data/roofs.json.gz` (300 studio roofs, 34,500 cells equal). `lay_roof` :275 lays stairs climbing toward the higher neighbour; **square to the board it is the studio's roof in stairs; turned, laid in cubes and slabs to the half block** (`house` :405-ish "stairs can only face four ways").
- **`House`/`house`** :355/:377 - dataclass (cx, cz, heading, L, W, floor, storeys, jetty, door ±1, chimney, roof form, pitch, overhang, windows fn, style dict). Four styles (`STYLES`: town, plaster, brick, stone) with timber posts at corners and every 4 along long walls, laid log at storey head, jettied joists, gable fill, attic clear, chimney. Returns door cell, footprint, eave, roof.
- `parapet` :485, `site` :495 (level + ease ground under a footprint; **fills down in void columns** - ranked bug #2 in the trials), `stairs` :522, `ladder` :536, `Claims` :542 (named footprint claims by layer, `overlaps`).
- Honest limit (README "What it does not do yet"): "one rectangle per storey, so no wings, porches or dormers"; Riftwater port built the original's wing/lean-to houses as separate houses "their roofs do not meet".

### 2.4 Facade patterns and floor fields (`lib/pgmvox/facade.py`, 376 lines)

A pattern is `f(s, run, t, h, n) -> None | Inset | Accent`: a function of where a block falls on its face (s along the run left-to-right as seen from outside, t up). Library: `band` :71, `band_from_top` :76, `courses` :80, `flutes` :85, `panels` :94, `slits` :103, `checker` :113, `glyph_row`/`word` :140/:154 (3x5 bitmap alphabet `GLYPHS`; a word reads correctly on every side), `windows` :159. `extrude` :197 pours a mass and patterns its faces; `coffer` :246 (coffered undersides with a light in every other); `top_course` :229 ("cornice", "parapet", "parapet-slotted"). **Inset = the face steps back a block** ("a recess and not a paint"), which the studio's wall materials cannot do. Floor fields are `f(Cell)` composed by `first_of` :341 and laid by `carpet` :352: `border`, `medallion`, `corners`, `diamonds`, `steps`, `star`, `stripes`, `tiles`, `cross`. Known limit: `extrude` patterns nothing on a wall one block thick (every cell of a one-block ring is a corner) - hit by Lantern Karst port and Brassmoor, rows 4 of the trials ranking.

### 2.5 Style as geometric grammar (`grammar.py` 321, `brittle.py` 650, `clay.py` 203 lines)

- **`grammar`** (`lib/pgmvox/grammar.py`): `Section` :40 (boxes at one height + `fill` name, `tags`, `motifs`, `tops` for stepped sections), `split` :90 / `tile` :97, `Ground` :107 (every column's top, section and depth-in-section; outline = depth 0), `Face` :179 and `Accent` :161 (courses top-down from the rim; an accent bay every so many along a face, laid **whole or not at all**: every column of it plus `margin` must be face at one height with the needed air - commit 1157a936), `Sunk` :155, `Lot` :228, `Style` :259 (body, faces, seam, fills, motifs; `Style.choose(section, lot)` tries fills in order and a fill may decline), `lay` :281. Rules read only the grid; blocks are the style's, "so one plan can be spoken in more than one style".
- **`brittle`**: five-block cells blueprint (flat, keep, stair, stacked, gap, water); `build(w, cells, only=, grown=)` :301; five-course cap with birch panels framed in black clay; sand fields (sand + upside-down sandstone stairs, cacti on pure sand), grass inside two rings of sandstone stairs; hollows/tunnels under a deck with dark-oak pillars (`_under` :375, `_pillars` :414); `house` :513 (storeys of whole cells, plate overhang in eaves, beacon under glass of the wool colour at the top); `tower` :490; `heart` :636; `fan` :72 turns a unit a quarter 4x.
- **`clay`**: Claywork style (sunk panels with quartz diamonds one per section side, checker/squares/paving/inlay/plate/flight fills, arrow motif).
- **`studioplan`**: reads a plan drawn in the studio's planner (version 2) as a brittle blueprint (Brittlebush III is the studio plan `untitled-plan-8`).

Why it matters: Claywork's visual identity is ~60 lines of style in `clay.py` plus a plan; a second style could re-skin the same plan **[inference]**.

### 2.6 Props, chests, trees

- `props.py` (136 lines): `stall` :18, `stalls` :48 (row of market stalls, awnings in turn), `lamp` :57, **`laid`** :121 (a chest drawn as three rows of nine letters + legend; refuses a row not filled the same from either end; items may carry enchantments written as the chest's tag), `DEFENCE` :71, `ROOM_GEAR` :81, `WOOL_CHEST_LOW/HIGH` :93/:96, `wool_chests` :104 (0.18.0, 2 stacked chests in each inner corner, facing along the door axis away from the wall).
- `trees.py` (152): `library` (the studio's copied trees), `load`, `kinds`, `turned`, **`plant` :95** (seats on the lowest ground under the bottom row as the studio's stamp does; refuses whole if any block lands in anything but air/plants), `scatter` :127 (crowns kept apart by `spacing`).

### 2.7 Objectives (`lib/pgmvox/objectives.py`, 619 lines) - what each stamps and checks

| Class | Stamps | Writes | Checks (`check(w)`) |
|---|---|---|---|
| `Spawn` :175 | nothing | `<spawn>` region, `{team}-spawn` area, `enter` filter `only-X`, `block="never"` or mined-and-regrow (`renewable`) | `_stands` :97 - nowhere to stand |
| `Observer` :222 | — | default spawn point | — |
| `Hill` :232 | border | control point with the studio generator's long attribute names | `check` :264 |
| `Flag` :281 | banner tile entity | flag XML | :303 |
| `Wool` :315 | bedrock pedestal at `slot.y-1`, **air** at slot, **dyed stained glass at slot.y+1** (as the studio stamps a monument), the wool block at `found` | `<wool>`, `{color}-{team}-monument` `<block>`, room `enter` rule, wool spawner into the room | slot is air; something under it; the wool block is at `found` :373-382 |
| `Destroyable` :417 | box of material | `{id}-region`, `<destroyable>` | box blocks are the material |
| `Core` :453 | obsidian shell, lava inside | `{id}-region`, `<core leak=5>` | min dimension >= 2, lava present :475-480 |
| `ScoreBox` :491, `Portal` :525 | — | regions, portals | |

`Objectives.add(obj, mirror=True, **image)` :561 carries a team's objective to the other team(s) through the plan's symmetry (boxes/points turned, yaws turned, team/id swapped, `color=` overrides, one image for `half`/mirror, three for `cw`); `Objectives.check` :597 also lists `{a} and {b} claim the same ground` (ground-claim overlap between objectives). `wool_rooms` :397 writes one union region per keeping team and a block filter (`woolroom-materials`: wood, stained clay, web, plus water an attacker places).

**Is anything above an objective, marking it?** No library call stamps a beacon, floating indicator, banner or sight check on a monument/core/wool. What exists: (a) the Wool monument's **dyed glass cap** over a bedrock pedestal (`Wool.stamp` :347-353); (b) Brittlebush's wool house puts a **beacon under glass of the wool colour** on the top cell (`brittle.house` :612-624, comment :525) - a deliberate beam landmark; (c) board-local: Hoarfrost Reach `monuments_lawn` "a stone ring round each, lamps, so a player finds them" (`lib/trials/sonnet/hoarfrost-reach/scripts/gen.py:162`), Cinderfall's beacon tower on the crest (`.../cinderfall/scripts/gen.py:183`). **`sight` is never used to ask whether an attacker can see an objective.** All 14+ `sight.*` uses in `lib/` run the other way: how much of a *spawn/court/quay floor* is seen from a goal/hill/rooftop (overgrowth: "3% of red's court floor seen from the ziggurat's top, target at most 8%"; whitecliff: "0% of a spawn's floor seen from each hill"; cinder-reach `plan_check.py:105-108` `seen_crag`; lantern-karst port `plan_check.py:65-69` "Ledges seen from the Arms 100%"). The guide's per-mode rows ask for "what a holder sees from the hill and who can see them" - exposure of the holder, not discoverability of the goal.

### 2.8 Walk / physics / sight / sketch / render / audit / mapxml

- `walk.py` and `move.py` as in 1.3/1.4. Walk opens wooden doors and gates (`OPENABLE`), ladders/vines/water lift and catch a fall (fixed 0.8.0), running jumps land on the first floor below the gap down to `max_drop` (0.10.3), `build=(mask,(lo,hi))` lets a player stand in build-zone air "as on a placed block", `kill_y` counts nothing below as a place. Brassmoor: built-walk "building" = 227/232 moves vs plan octile 81-96 (it counts every block climbed).
- `sketch.py` (547 lines): `Panel` :86, `MapPanel` :96 (plan raster or built top-down; heights, places with halo, team-coloured markers mirrored through the plan's symmetry, routes with arrowheads, one jump per piece pair with its gap, zones, ghosts, callouts with leader lines), `SectionPanel` :373 (true scale; `raster` along x/z, `along` unrolled under any polyline, `level` kill height/water), `TablePanel` :474 (checker numbers vs targets, red on a miss), `Sheet` :497 (`row` sets sections side by side).
- `render.py` (198): `iso` :43 (corners "se"/"sw" only - ranked gap), `elevation` :121, `cutaway` :151 along any polyline, `xray_shell` :21, `trim` :190; all in the studio's colours (`data/blocks.json`).
- `mapxml.py` (201): `E`, `Doc` (`region` refuses a duplicate id, `filter`, `apply`, `kit`, `kill_below(how="portal"|"kit")` :124, `blitz`, `time`, `broadcasts`, `itemremove`, ...), `item(... enchant=, unbreakable=, team_color=)`.
- `orient.py` (269) + `data/blocks.json`: turn tables for the families the studio leaves unturned (doors with hinge swap, trapdoors, rails, sign posts, banners, beds, buttons, levers, repeaters, hay, quartz pillars); `turn_world(w, op, keep, axis, recolour=, banners=)` :224 copies a half onto its image **including tile entities** and recolours (team clay/wool/banners).

---

## 3. The author's specific questions

### 3a. Door vs window buffer

**Short answer: there is no rule anywhere. A window can be directly beside a door.** The library's window rhythm and the door are chosen independently; the door is written *after* the walls (so it overwrites whatever was in its two cells) and is never consulted by the window test.

Library (`lib/pgmvox/build.py`):
- `windows(period=3, rows=((2,), (2, 3)), margin=1.5)` :345-352 returns `f(run, span, t, storey)`: on course row t=2 of the ground storey (t=2,3 upper), `margin < run < span - margin` and `abs(run % period - period/2) < 0.6`. It takes only distance along the wall; it has no door argument.
- Called per wall block at :434 (`elif h.windows(run, span, y - y0, s): blk = st["window"]`).
- Door chosen at :442-447 (`cands` = base-wall cells on the door side with `abs(u) < L/2 - 1.5`; `min` of `abs(u)` = the cell nearest the wall middle; ties broken by smallest x then z) and set at :448-450 (`w.set(x, f+1, z, door)`, `f+2` upper half).
- The door's upper half is on t=2 = the window row of the ground storey. So for L=7, 8, 11, 12, 13, 14 the nearest-middle cell lands one cell from a window cell.

**[measured here]** Over 960 houses (4 styles x L 6..15 x W 5/6/7 x headings 0, 90, 180, 270, 20, 45, 70, 135, two storeys, door +1), **468 (49%) had a window pane or iron bar edge-adjacent to the door on the door's own rows** (264/480 axis-aligned, 204/480 turned). By L (axis-aligned, W=6, `town`): L=7: 4/4 doors have an adjacent pane; L=8: 2/4; L=10: 2/4; L=11,12,13: 4/4; L=14: 2/4; L=6, 9, 15: 0/4.

**Where the fix goes:**
1. `build.py:345` - extend `windows` (or the `House.windows` hook, :374) to take the door's `run` and a clearance, e.g. `windows(period, rows, margin, avoid=(door_run, 2))`, and reject when `abs(run - door_run) < avoid`.
2. `build.py:442-447` - the `cands` selection must move **above** the storey loop (before :418) so the door run is known when :434 runs; then pass it into the call at :434. Today the door is resolved only after the walls (the Riftwater port hit the same ordering problem and had to re-derive the door in the plan: PORT-REPORT "House footprints and doors before building", `plan.door_cell`).
3. Board-local copies are the same: `opus55-freeform-riftwater/scripts/house.py:171-184` lays panes every 2 or 3 blocks from `x0+2`/`z0+2` along each wall, then `:195-196` sets the door at the wall's mid cell with no exclusion (fix: skip `x`/`z` within 1 of `door_at`, or place the door before windows at :168-169). Hollowcrown's `house.py` (doors :166-181, windows "wall block on the window rows between posts -> glass" :13) has no exclusion either.

Related defect **[measured here]**: at oblique headings the door can face a wall. `build.house` :448 `facing = fr.across(h.door)` rounds to the nearest cardinal (`Frame.across` :71 via `orient.vec`), but the door cell sits in a staircase wall. Across 200 sampled houses (L 7-11, W 5/6, both door sides), at headings 30, 45, 60 and 135 degrees **10 of 20 doors per heading** had a non-passable block directly outside and directly inside the door's faced axis; headings 0, 90, 12, 20, 70, 200 had none. Printed layer at 45 degrees (door at (-2, 1) facing "s"): wall blocks directly west and south of the door; the gap is diagonal. `build.house` never checks the cell in front of the door; hollowcrown's door facing is `(round(nx), round(nz))` (`house.py:181`). Fix location: after :448, test the outward/inward cardinal cells are passable and otherwise move `cands` to the next cell or carve the outward cell **[inference on fix]**.

### 3b. Objective discoverability

- No marker/indicator API exists (2.7). The only built-in cue is the Wool monument's dyed-glass cap (`objectives.py:347-353`); the Brittlebush wool house beacon; Hoarfrost's lawn ring + braziers; Cinderfall's beacon tower.
- **Checks that exist**: placement (`Wool.check` :373: slot air, support, wool present), material/lava (Destroyable/Core), ground-claim overlap, spawn stands, reachability by walk (`unreached`, "enemy spawn -> monument on foot: not reached" read-backs), exposure of *spawn floors* from goals. **No check** that a monument/core/wool is visible from where an attacker arrives, nor "not hidden".
- Where objectives are underground / enclosed / out of sight (read from PLAN/REPORTs):

| Board | Objective | Placement |
|---|---|---|
| hollow-mesa (DTC) | core | The Throat cavern inside the mesa, on a stub beside a hole to the void; reached by headframe ladder shaft (26 blocks), Bench Adit catwalk, or the Chimney passage (REPORT tour table) |
| hollowcrown (DTM) | monument B | Hall of Echoes, underground temple at y 23 under the town; A on the open Eyrie crown y ~104 (REPORT l.20, :85, :109) |
| riftwater (DTM) | 4 monuments | all floating over open squares/greens (Market Square -66,-44 and Winding Green -66,48); caves *come up beside* them but monuments are in the open (REPORT l.44, :59) |
| frostholm (DTM+DTC) | core in the lighthouse lantern; monument on a rock knoll by a frozen lake | tower-top |
| stratum (DTM+DTC) | core "hung over a shaft into the void" in the Reactor; monument on the Obelisk balcony | |
| saltgate | wool + destroyables in the powder stores and keep | stage-gated interior |
| gullhaven-dtm | gold cubes floating over the harbour and a beach pad | open |
| cinder-reach, cinderfall | cores over a vent / hung in open | "hangs in the open" (REPORT l.3) |
| redwash-mesa | table monument on the Table; wash monument in Arroyo Town's plaza | open; "reached from around, above, below and through" |
| CTW wool rooms (lantern-karst Store/Shrine, claywork Kilns, brassmoor Boiler House/Water Tower, hoarfrost Lighthouse top room at y 94 / Ice Hall) | wool | in a room behind a door or at the top of a ladder; monuments are in front of the *own* spawn |

  Tool-wise, the destroy-board approach law (`approaches.md`) is what keeps goals discoverable: "off the line between spawns, exposed, composed ground round it"; Cinder Reach states "the core sits 39 degrees off the line between the spawns", Redwash "54 and 27 degrees off". Those angles are measured in `plan_check`, not sight lines.
- Practical consequence **[inference]**: if the author finds objectives hard to see, the missing piece is (1) a `Marker` objective part (beacon/glass column/banner) on `Destroyable`/`Core`/`Wool.stamp`, and (2) a `sight.visibility(goal_target, arrival_cells)` row in plan_check; `sight` already has the primitives.

### 3c. Build-zone marking in the world (CTW boards)

PGM's build region here is a **void filter**: `d.filter("not-void", E("not", E("void")))` + `d.apply(block_place="not-void", message="You may not build in the void!")` + `<maxbuildheight>` (claywork `mapxml.py:26-27`; same in brassmoor, hoarfrost, lantern-karst port :27-34, brittlebush-iii, sandreach). PGM's void filter denies placement where the column at y=0 is void/air (`/home/user/pgm-studio/docs/pgm/filter-patterns.md` §2.4). So the "region" is **a per-column mask: block 36 at y 0 under every column a player may build in**. Land columns are buildable too (that is the studio's convention).

| Board | Block 36 at y 0 | Visible outline | Other build marking | Where |
|---|---|---|---|---|
| lantern-karst (freeform) | yes, red's half, turned (`terrain.py:200-205`, `markers`) | yes - the studio's ST5 BuildMarkerStamper: unpowered redstone wire (id 55) at **y 1, two blocks out from every void-facing edge of a build zone**, one air clear of zones/terrain, corners turned (`terrain.py:208-249`, 518 blocks). First attempt put redstone on the island edges "which inverts its meaning" (REPORT row 3) | build zones are polygons (`P.BUILD_ZONES`) | `opus55-freeform-lantern-karst` |
| lantern-karst port | yes `gen.markers` (`ports/.../gen.py:92-97`) | yes `gen.outline` :99-135, 522 blocks | `audit.footing` flags all 522 (redstone over air at y 1) - expected | `lib/ports/lantern-karst` |
| brassmoor-works | yes (`gen.py:268`, `land | zone`) | **no outline** | bedrock line 3 high + cobweb across each lane (`gen.py:158-165`); a 3-row strip kept out of each flats zone so a bridge can't skirt the line; the 22-block band has the crane island | `lib/trials/opus` |
| claywork | yes (grammar `Style.body`; `clay.py:101`; read-back "Land or build zone without block 36, block 36 under plain void: 0, 0") | **no outline** | bedrock wall across each Walk; band drawn as yellow dots on the sketch only | `lib/boards/claywork` |
| brittlebush-iii | yes (`brittle.py:324,395`) | **cobwebs at y 1 on the middle of each edge a gap cell shares with void** (`brittle.py:325-333`); water zones carry none ("PGM holds the water still") | redstone line in front of each wool house's door (a wool-room marker, not a build edge; `gen.py:55-57`) | `lib/boards/brittlebush-iii` |
| sandreach | yes | cobwebs as brittle; "a cell of build zone from both lanes" | redstone line before the wool door (`gen.py:54`) | `lib/boards/sandreach` |
| hoarfrost-reach | yes (`gen.py:350-354`, `~void | zone_mask`) | **no outline** | two named zones (`band`, `gap-w` "the Lighthouse gap", plan.py:78) | `lib/trials/sonnet` |
| brittlebush-koth (KOTH, 4 teams) | yes via brittle | cobwebs at gap cells | — | `lib/boards/brittlebush-koth` |
| riftwater (DTM) | n/a block 36 listed in port: "rift build zone... void filter, max build height" | none | `RIFT_HALF = 10` void x in [-10,9] build zone | `plan.py:10` |

Note: `brittle.py:20` gap cells use block 36 + a cobweb mid-edge. **[inference]** A build zone's outline is a studio convention only the two Lantern Karst boards reproduce exactly; the other three modern CTW boards rely on block 36 with no visual edge. The trials' own friction note: "Block 36 at y 0 under every deck and zone column is one line, but it is the rule every capture board must follow and no library call says so" (asks `objectives.BuildArea(mask)`).

### 3d. Defence chests, bedrock walls, wool-room gear, wool chests

- Library: `props.DEFENCE` :71 (dark-oak planks ends, spruce inside, crafting tables, end stone, a centre column of redstone blocks, two Efficiency II iron pickaxes; rows 9 wide, symmetric), `props.ROOM_GEAR` :81 (iron armour set around two golden apples, beef, arrows, planks), `WOOL_CHEST_LOW/HIGH` :93/96 and `wool_chests(w, box, floor, door)` :104 (the studio's `WoolChests` stamper loot: low = planks/Speed potions/golden apples x16; high = diamond leggings/Power I Infinity bows/planks; two stacked chests in each inner corner of the room). `laid` :121 accepts enchantments (0.11-0.12, "once the library could write enchantments").
- **Use by board** (grep over the repo): `DEFENCE` and `ROOM_GEAR` are used by **Claywork only** (`lib/boards/claywork/scripts/gen.py:213` two defence chests in each bedrock wall's Kiln-facing face; `:297` two ROOM_GEAR chests in each Kiln). **`wool_chests` (0.18.0, the newest commit, 10-10 00:30) is used by no board** - only its test (`tests/test_pgmvox.py:840`). The older CTW boards write ad hoc chests: lantern-karst (freeform and port) iron chestplate/leggings in the Store (`buildings.py:473-477`, `dress.py:401-402`); brassmoor 1 chest with chestplate+32 arrows per room (`gen.py:138,155`); hoarfrost skald's hall golden apples+beef/arrows (`gen.py:158-159`); overgrowth/whitecliff/cinderfall/tamarisk hand-written apple/arrow chests.
- **Bedrock walls**: Claywork - bedrock "to the floor of the world, 3 over the floor" across each Walk (`gen.py:200-206`), ends on the void, so nothing tunnels under; defence chests set into the face with the lid cell left air (`:214`). Brassmoor - "three bedrock and a web" across each lane, four blocks before the room door (`gen.py:158-165`). Lantern Karst - the Store's wall "three bedrock, one cobweb" (`buildings.py:518-524`; port `dress.store_wall` :407-411 "Two thick, the road's width"; plan kind `barrier`). Foundation courses: bedrock 5-6 under every floating island except the rim (lantern-karst `terrain.py:112-121`, hoarfrost `gen.py:72`).
- Spawn kit iron regrows in a mined-and-renewable region (`Spawn(protect=("iron ore",...))` writes `renewable`, `objectives.py:190-209`).

### 3e. Build-region fidelity in map.xml

- Zones are written **not as regions at all**: the XML only contains the void filter and `maxbuildheight`; the "zone" is encoded in the world (block 36 columns). Precision is therefore **per column, whole-height**, exactly as the plan's `zone_mask` (a numpy mask from the plan raster / polygons). Vertical limits are only `maxbuildheight` (claywork `MAX_BUILD`) and kill height `kill_below(y, how="kit")` (instant damage region, `mapxml.py:124`).
- Spawns/rooms/objectives are exact cuboids: `Box` is inclusive blocks written with exclusive max (`objectives.py:39-56`, `Box.cuboid`), points at block centres (x+0.5, y, z+0.5, `centre_el` :92). Region ids refuse duplicates (`Doc.region`). Spawn `area` + `enter="only-red"` + `block="never"`; wool rooms union region + `woolroom-materials` filter (wood, stained clay, web, player-placed water). Wool `location` is floored (`found + 0.5`), monument `<block>` not (matches CLAUDE.md "coordinate flooring is per-field").
- Verification: `data/read_mapxml.cs` runs the studio's own parser + validity check; every trial map.xml "valid, no issues". The studio **refuses** flags, payloads and score boxes, so those boards (riad, copperline, penstock, ...) cannot be round-tripped (assessment cluster A).
- Fidelity gaps: nothing verifies that the block-36 mask equals the plan's zones except the board's own read-back row ("Land or build zone without block 36, block 36 under plain void: 0, 0" in claywork/sandreach/brittlebush-iii); the ST5 outline is replicated by two boards by hand.

### 3f. Houses at different angles, doors, the tower wool on Hoarfrost Reach

- **Angles with roofs following** are not on Hoarfrost. They are `build.Frame/House/RoofField.framed` (above) and, before the library, `opus55-freeform-hollowcrown/scripts/house.py` ("a house is drawn in its own frame and every block asks where its centre falls"; REPORT :28-54: headings on red's half 0, 4, 9, 12, 21, 38, 45, 46, 51, 52, 59, 70, 72, 76, 78, 82; keep at 25 deg; Hall of Echoes an octagon turned 22.5 deg). Roof = height surface `eave + (half-width - |v|)` laid two blocks thick so a 45 deg roof has no gaps, slab where half a block higher, gable ends filled to the underside. Library test: a house at 45 degrees with no wall gap; `examples/parts` lays houses at 0, 20, 45, 90. Library roofs turned off-axis are cubes+slabs to the half block (`build.house` comment at the `RoofField.framed` call).
- **Hoarfrost Reach houses** (`lib/trials/sonnet/hoarfrost-reach/scripts/plan.py:75-80,114-141`): only three, `skald-hall` and two sheds, drawn as rectangles; `spec()` converts them to `House(heading=0 or 90, L, W, door=±1, storeys, style=custom dict, roof="gable", overhang=1)` and `door_cell(spec)` re-derives the door in the plan with the same `cands` formula as build.house (so the plan knows the door before the build); `BLD.house(w, house, ground_at, r)` builds them (`gen.py:130-139`); `skald_interior` adds tables, hearths, carpet, 2 chests.
- **Tower wool (the Lighthouse)** is board-local, not library: `gen.py:202-266 lighthouse()`: 9x9 shaft `P.TOWER = (-82,-59,-74,-51)`, striped clay walls (red/white by 4 courses), iron-bar slits, a glass lantern room under a quartz roof, gallery of slabs+bars, door on the east wall `(-74, -55)` at y 73-74, a ladder up the south wall with a hatch cut in each floor every 5 (`:239-243`), room floor at `ROOM_Y = 94`, and the wool pedestal (a quartz block) at the room centre (`:263-265`; the wool and monument are stamped by `objectives.Wool`). Reached by the "Lighthouse gap" build zone across `West Causeway`; plan walk 121 / built 150 (gap built). Sonnet notes the "strand polygon left out its boundary cell and so left a one-cell gap" and "attack walks started from the wrong side of the build band".

---

## 4. Board census

Lines are `wc -l scripts/*.py` (board-specific; for the 20 originals this includes their copies of `mc.py`, `render_iso.py`, `walk_core.py`, `noise.py`...: SHARED-LIBRARY-ASSESSMENT.md measured 15,800 of ~50,000 lines as copies). "Time" is the commit-stamp span from first plan commit to the last board commit (the agent's clock), not effort; trial times are the SUMMARY's. Sizes are blocks (x by z) from plan bounds or reports; `?` = not found in a quick read.

### 4.1 The 20 freeform originals (bespoke, pre-library, July-style Python copied per board)

| Board | Mode | Size | Symmetry | Code lines | Commit span | Signature features / known defects |
|---|---|---|---|---|---|---|
| riftwater | DTM, 2 monuments/team | 240x176 | mirror x about a rift | 3,379 | 22:37-23:10 (33 min) | river valley split by bottomless rift, falls into void, cave/mine/cellar, hump-back bridge, 29 houses, mill wheel, wheat field. No entities (boat is blocks), no relight |
| hollow-mesa | DTC | 260x200 | half turn | 3,242 | 06:15-06:33 (18 min) | banded mesas, canyon+bench, natural arch, tram + trestle, adobe/false-front town, core in the Throat cavern with a hole to void; the arch "broke the town" until the placement audit |
| frostholm | DTM+DTC | 180x180 | half turn, diagonal band | 2,499 | 06:43-07:07 (24 min) | winter coast, straits frozen in stretches, lighthouse spiral stair + core in lantern; v1 rejected, rebuilt in an evening (generates <1 s, writes ~10 s) |
| cloudhaven | DTM | 264x200 | half turn | 2,046 | 07:10-07:20 (10 min) | 11 islands/side at y 58-92, balloons, airships, rope bridges |
| hollowcrown | DTM, 2 monuments/team | 240x192 | half turn | 3,126 | 08:41-09:03 (22 min) | houses at any angle, serpentine Wend graded road, Underhall cavern city + lake, lifts between two spawns, glass clouds |
| stratum | DTM+DTC | 200x144 | mirror x (land unsymmetric) | 2,418 | 09:22-09:50 (28 min) | brutalist masses with inset/glyph/flute/coffer faces, wool-coloured surfaces, glass cloud sea, kill y 58 |
| lantern-karst | CTW, 2 wools/team | 224x256 | half turn | 2,853 | 09:50-10:55 (65 min, 5 plan rounds) | 26 floating karst pieces, joins, bedrock course 6 under islands, block 36 + ST5 redstone outline, karst towers, Store wall |
| penstock | TDM + score boxes | 140x96 | mirror | 1,530 | one commit 11:20 | station carved from one block, cobweb-guarded score boxes, shops/spawners; studio refuses the mode |
| calcite | KOTH, 3 hills | 120x96 | half turn + per-hill mirror | 4,073 | 11:45-12:39 (54 min; 3 plans+rebuild) | terraced quarry, glass tunnels under lava, jump pads tuned by `solve_launch` against built blocks, true-scale sections; playtest: stair/ceiling headroom, tunnel glass filling a neighbour |
| riad | King of the Flag | 96x121 | mirror z | 3,240 | 12:54-13:33 (39 min) | palace water garden, caged water columns, banner tile entity, spawn terraces left by a drop |
| gullhaven | FFA rage | 136x143 (island + 12 sea) | none | 2,961 | 13:39-14:18 | fishing island, 29 spawns, ravine, sea caves, closed houses, cliffs cut by height-varying noise |
| gullhaven-dtm | DTM | island x2 | half turn about the Skerry | 341 | 14:07-14:18 | composes the FFA island twice; 3x3x3 gold cube monuments over water/beach |
| saltgate | attack/defend, 3 stages | 96x136 | none | 2,866 | 14:43-15:17 (34 min) | harbour stormed from the sea, staged gates and spawns, ships with curved hulls; playtest: banner could be lost |
| copperline | payload | 112x144 | none | 2,832 | 15:17-15:36 | track laid from waypoints and traced as PGM traces it, mine adit, slag heap; playtest: spawn-room entry rule backwards |
| lanternpass | runners & shooters | 68x387 | none | 2,232 | 15:55-16:08; three playtest rounds to 00:32 | 7-section festival road, sight read per cell, bell as control point; playtest: union spawn, Speed amplifier, backward steps, harbour ladders, bamboo thinned twice |
| sunwell | water drop | ? | mirrored ways | 2,286 | 16:20-16:25; **set aside** | plan only (PLAN.md; no REPORT); v1 kept |
| lanterndrop | water drop, 14 hills | ? | mirrored ways | 1,707 | 16:40-16:47 | 30 floating pieces, fall model, hills held through death; playtest: observer point, spreading water, kill portal offset `@-150`, Limbo II's boots |
| loomfall | wool run | 5 carpets | — | 1,329 | 16:54-17:02 | five patterned flying carpets (single sheet of wool), per-cell fall read |
| spark | knockback | ? | 12 rays | 1,715 | 17:27-17:52 (floes plan kept as v1) | the Claude spark in terracotta, knockback model, ridged mountains |
| curio | hide & seek | 48 plots | — | 1,645 (+5302 with plots) | 17:33-18:20 | 16 plots each by Opus/Sonnet/Haiku in a bounded canvas; per-plot climb/sight/footing check; plot kit became `pgmvox.plot` |

### 4.2 Built on the library (pgmvox 0.2 to 0.18)

| Board | Mode | Size | Symmetry | Lib or bespoke | Code lines | Time / date | Signature / defects |
|---|---|---|---|---|---|---|---|
| ports/riftwater | DTM | 240x176 | mirror x | lib (52 refs) + local | 1,885 (original 3,379; ~900 "a library could hold") | 10-08 21:33 -> 21:41+ | whole board came across; not ported: barn, haystacks, rowboat, gardens, wings, interiors; found 3 library bugs (order-dependent walk, no doors in PASSABLE, ladder not entered from top) |
| ports/lantern-karst | CTW | 224x256 | half turn | lib (31) | 1,381 (orig 2,433) | 10-08 21:33; port in ~1 min run, 40 s of it `plangraph.jumps` | same board; roofs are the studio hip not the original stepped one |
| trials/opus/cinder-reach | DTC | 208x144 | half | lib | 1,058 | 29 min (incl `common.py`) | cores over breached cone vents; GO1 3.34 plan vs 2.67 built |
| trials/opus/redwash-mesa | DTM x2 | 192x128 | mirror x | lib | 921 | 12 min | table + canyon-town monuments; cliff house |
| trials/opus/brassmoor-works | CTW, 2 wools | 176x224 | half | lib | 848 | 14 min | ironworks over smog, bedrock lines+web, flats zones, crane in band; 227/232-move build walk |
| trials/opus/vinewatch-ruins | TDM | 96x112 | mirror z | lib | 688 | 10 min | temple ruin, cistern; scoring unread by studio |
| trials/opus/tidewell-canals | KOTH chosen | 160x128 | half + mirror z (2 ways) | lib | 689 | 9 min | Campo worth 2 under a gallery, two markets worth 1 |
| trials/sonnet/cinderfall | DTC | 180x120 | half | lib + `kit.py` | 1,290 | commit 22:35 | floating volcanic island, 5 ways onto each core |
| trials/sonnet/tamarisk-wash | DTM | 200x128 | mirror | lib + kit | 1,593 | 22:52 | desert basin, Obelisk/Sunstone, qanat; water stood a block over banks (fixed by `hold`) |
| trials/sonnet/hoarfrost-reach | CTW | 176x200 | mirror z | lib + kit | 1,221 | 23:00 | ice headlands, Lighthouse wool room y 94, Ice Hall, glacier stair; strand polygon left a 1-cell gap |
| trials/sonnet/overgrowth | TDM | 128x96 | mirror? | lib + kit | 1,133 | 23:10 | walled jungle valley, ziggurat; canopy blanketed board; trees planted after turn left blue half bare |
| trials/sonnet/whitecliff-cistern | KOTH, 3 hills | 120x100 | — | lib + kit | 1,194 | 23:20 | cliff town; built differently each run (Python `hash()` of house name: 5,730 blocks differed) until fixed |
| boards/claywork | CTW, 2 wools | ~? 4 flat levels | mirror | lib (grammar+clay) | 1,229 | 10-09 11:57-14:01 (+19:07), 4 review rounds | bedrock-to-floor walls, DEFENCE+ROOM_GEAR chests, Kilns, Undercroft, stepping stones; first board to use `laid` |
| boards/brittle-study | style study (no mode) | — | — | lib | 384 | 14:15 | Brittlebush signature read and replicated (STYLE.md, GRAMMAR.md) |
| boards/brittlebush-koth (ex Ocotillo) | KOTH, 4 teams, 5 hills | ~? | rot_90 | lib (brittle) | 824 | 14:48-15:51; rebuilt 16:25, house over the keep 17:32 | 3 plan reviews |
| boards/brittlebush-iii | CTW, 4 teams | from studio plan.json | rot_90 | lib (brittle+studioplan) | 364 | 16:25-18:20 | hollow decks, 3 under-sections, every piece its own island so wools reached by building (49 to own, 110-143 to others); not opened in PGM |
| boards/sandreach | CTW, 2 teams x12 | ~? | half | lib (grammar+terrain) | 438 | 10-09 19:21 | made grammar spine + grown meadow/floating island; grown ground rules still in the board's script |
| examples/{islets, drop, parts, vale} | worked examples | — | — | lib | 216/98/74/173 | 10-08 | `check.py` snapshots |

Pattern **[inference from the numbers]**: board-specific code on library boards is 350-1,900 lines versus 1,300-4,100 for the pre-library originals; the five opus trials took 9-29 minutes each on commit stamps (the first includes writing `trials/opus/common.py`, 164 lines).

---

## 5. Evolution of the library (commit stamps, 2026-10-08 unless noted)

| Version (time) | What it added | Friction it removed (from commit bodies / reports) |
|---|---|---|
| assessment 18:54 | `SHARED-LIBRARY-ASSESSMENT.md` | 15,800 of ~50,000 lines were copies; nine colour tables; a `rotate.py` that lost a rail fix; nine walks with a headroom check that could never fire (`if dy == 1 and not st[x,y,z] \| True`) |
| 0.1 part 1+2 (19:09, 19:15) | `blocks` (table exported from the studio's palette), `orient` (families the studio leaves unturned), `world`, `noise`, `shapes`, `move`, `walk` (headroom fixed), `plan`, `plangraph`, `sight`, `sketch`, `terrain`, `render`, `plot`, `mapxml`, `run`; Islets example | one id table, one walk, one physics, one renderer |
| `sketch` annotation layer (19:38) | legends in titles, mirrored markers, one jump per pair, true-scale unrolled sections, checker table | eight section drawers |
| 0.2.0 (19:50) | `build` (Frame, RoofField tested vs 300 studio roofs, house, parapet/site/stairs/ladder/Claims), `facade` | six gable roofs, four `Frame` houses, seven parapets |
| 0.3.0 (19:59) | `pieces.Course` + link audit | water-drop plans (audit caught a landing short of a pool and a fall costing >half health) |
| 0.4.0 (20:18) | `objectives`, storeys, `solid` | 12 boards' hand-written XML regions; `data/read_mapxml.cs` |
| 0.5.0 (20:40) | slope_deg = studio's, `Strata`, `root_depth`, `landform` | a spire that raised the whole board to a plateau (test now bounds it to its radius) |
| 0.6.0 (20:52) | `route` (find/network/pave/steps), `landform.grade` | 71 zig-zags -> 5 legs; Vale uplands/rim found unreachable |
| `check.py` + AGENT-GUIDE (21:22) | snapshot gate, `Raster.from_heights` | |
| 0.7.0 (21:41) | `forms` (karst towers kept), Riftwater rebuild | trial: Riftwater port 2,041 vs 3,379 lines |
| 0.8.0 (21:59) | bucket-queue walk (mirrored board walks the same), doors open, ladder catches fall, `jumps` 38 s -> 0.5 s, `Symmetry.point`, soil by slope, props | trial bugs from ports (red 81 / blue 83) |
| 0.9.0 (22:04) | capture boards: `graph(bridge=)`, octile `PlanRules`, `measure`, `Wool` with room/spawner, mined-and-regrow spawn, kit, kill height | Lantern Karst port's `planwalk.py` became a thin wrapper |
| 0.10.0 (22:16) | `under`, `trees` | Riftwater cave/mine/shaft/woods |
| 0.10.1-0.10.2 (10-09 10:03, 10:29) | `audit.loose_water`, `lake`, `hold`, `watercourse(into=)`, sea runs to void | water standing a block over banks on two sonnet boards |
| 0.10.3 (13:15) | running jump lands lower | Claywork stepping stones read one-way |
| 0.11.0 (15:51) | four teams (`rot_90`, `Teams.next`, wool `keeper`), `brittle` | Brittlebush KOTH/III |
| 0.12.0 (16:25) | `studioplan`, hollow decks | studio plan -> board |
| 0.13.0 (17:24) | one-block outlines, wool houses of whole cells | |
| 0.14.0 (18:06) | sections, fills, panels over a full drop | |
| 0.15.0 (18:28) | `grammar` extracted, Brittlebush spoken in it | |
| 0.16.0 (18:47) | `clay`, sunk course, aligned bays, stepped sections | second style proved the grammar |
| 0.17.0 (19:21) | Sandreach (grammar + grown ground on one board) | |
| 0.18.0 (10-10 00:30) | `props.wool_chests` | the studio's wool loot in each inner corner |

### Ranked gaps in the trials' SUMMARY files

Opus (5 boards, `trials/opus/SUMMARY.md`), "ranked by how much play they can decide without anybody noticing, then by how many boards met them": (1) plan walk octile vs built walk four-way: GO1 3.34/3.08/3.26 plan -> 2.67/2.89/2.94 built, "All five boards met it"; (2) library writes over the void (`build.site` 52 blocks in a 12-block reproduction; `trees.scatter` crowns over void); (3) a plan cannot state a join (4 of them wrong in the first plan on boards 1-4; `plangraph.walkable` drops no-headroom cells silently); (4) `facade.extrude` patterns nothing on a 1-block wall; (5) each mode's rules measured by hand per checker (~120 lines a board: GO1/GO3/GO4, SP10, WL7/9/10e); (6) one symmetry at a time; (7) two stair conventions (`Raster.flight` widens either side, `build.stairs` to the right); (8) a house's door known only after it is built; (9) paint by place / floors in cells; (10) deathmatch scoring unread. Their guide changes: say which walk the goal rules are against; "the plan states its joins"; make sight a standard row; print plan heights as a grid before the sketch ("found more faults than any other single step"); keep the first sketch by tool.

Sonnet (5 boards): (1) octile vs four-way, "built numbers run 15 to 40 percent over the plan's"; (2) `house`/`site` fill to y -1 off an island edge; (3) no tunnel-to-surface helper, plan/world floor convention off by one; (4) plan measures rewritten on every board (routes through a place, bearings, sight runs, dead share, clearance); (5) `Objectives.add` keeps the mirrored objective's name; (6) no TDM score helper; (7) `Raster.flight` width wrong for 3 of 4 headings; (8) `Raster.poly` omits boundary cells; (9) `SectionPanel` axis naming; (10) `plan_opaque` roofs as dict; (11) no shared tower/brazier/lamp props; (12) `render.iso` only two corners.

---

## 6. What the reports asked the studio for (aggregated)

Source: the "What I wanted, how hard it was, what a studio feature would need" tables in 19 originals' REPORT.md (~190 rows per the assessment), the 5 opus trial reports, claywork, and the ports. Assessment's own clustering (§3, rows from boards):

| Rank | Ask (cluster) | Boards asking | Studio today (assessment) |
|---|---|---|---|
| 1 | Objective pieces that write their own regions/XML: hills, posts + flag banner, score boxes, shops, gates by stage, track legs, portals, monuments, kill height, timed region clear, **build-zone marker** (B) | 12 | writes CTW/DTM/DTC goals only |
| 2 | Round-trip validation for the board's gamemode (A): KOTH, KotF, FFA/rage, DTM variant, TDM+scorebox, A/D, payload, blitz/portals, block drops | 11 | refuses flags, payloads, scorebox `<box>` |
| 3 | Structure primitives with guarantees (F): bridges solving their profile, stairs with headroom, tunnels/carves that know the ground | 10 | axis-aligned pieces, no carve layer |
| 4 | Plan-time reads (C): routes on every edit, jump audit, sight from objectives/shooters, arrival times by stage, spawn spacing | 8 | `PlanNav`/`PlanRoutes`, no jumps/sight/stages |
| 5-8 (tied, 7 each) | Physics reads (D: pads, falls, knockback, no-catch, no-stand); team colour a symmetry turn swaps (E); terrain landforms/water courses (G); floating masses/void edges (H); props with a shape rule (I); placement (K: along a polyline, as near as, claims per layer, placement audit) | 7 each | see assessment |
| 9-10 | Patterns (J: insets, glyphs, floor fields) 5; seeing the world (L: iso/x-ray/sections along any line, offline) 5; the plan document itself (M: polygons, relayout, a board as a piece placed twice) 5 | 5 each | |

Concrete asks that recur in individual tables (count of reports naming it, my tally from `asks.txt` + trials **[tally is mine, approximate]**):

- A **sight/exposure read on the plan and world** (calcite, riad, gullhaven, lanternpass, curio, hollow-mesa-style audit, lantern-karst port "new" row, 4 trial boards): ~9.
- A **jump/fall/physics read between pieces with damage** (calcite, lanterndrop, loomfall, spark, lantern-karst, claywork "jump checks on the plan that use the same rules as the built walk"): ~6.
- **Team colour slot swapped by the symmetry turn** (calcite, gullhaven-dtm, stratum, lantern-karst, riad, riftwater, + lanterndrop hills): 7.
- **Objective pieces writing their XML** incl. `objectives.BuildArea` (brassmoor), `Core(vent=)` (cinder-reach), hills (calcite, lanterndrop), score box (penstock, `Doc.score` vinewatch): 9+.
- **A heading on every structure / rotated footprints** (hollowcrown, frostholm, stratum): 3, now partly answered by `Frame`.
- **A plan layer with per-block heights / polygons** (hollowcrown, cloudhaven, lantern-karst "plan view that redraws as a piece is dragged and prints the WL and SP numbers beside it", riftwater, claywork "Storeys on the plan"): 5.
- **Capture-rule table** `plangraph.capture_rows` giving SP10/WL7/WL9/WL10e (brassmoor, lantern-karst port): 2 (+ "width rules per piece kind checked on the plan" lantern-karst).
- **Joins between pieces stated and measured** (brassmoor `plan.joins`, redwash, vinewatch `Raster.opening`, cinder-reach `graph(bridge=)` to any storey, lantern-karst "automatic join stamping with a flight width"): 5.
- **Pattern/inset face treatments and floor fields on a piece** (stratum, loomfall, claywork, lantern-karst, penstock "face-aware paint"): 5.
- **Entities (boats, minecarts, armour stands, item frames) and relight in the writer** (riftwater): 1, blocked.
- **Chest editor / loot presets** (claywork "shows the 27 slots as a grid"): 1 (answered by `laid`, `wool_chests`).

---

## 7. What makes the maps better than the studio's - analysis

Everything in this section is **[inference]** from the code and reports unless it cites a measurement.

1. **The plan is a per-block, multi-storey, checked artifact, not a coarse zone sketch.** `Raster` (H, K per block, symmetry applied in the plan) + storeys + the capture-aware walk means the author reviews numbers with targets (SP10/WL7/WL9/WL10e, equal arrival, widest gap) and a true-scale section on one sheet *before* a block exists, and "the checker and sketch reran from it" in seconds across four-five plan rounds. The studio's pipeline offers coarse rectangles and a CTW kit-budget walk (assessment).
2. **Block-level control with guarantees at the join.** Frame at any heading with eight-neighbour closed walls; the studio's own six roof forms (tested cell-for-cell) plus turned roofs; inset facades, glyph/flute/coffer patterns, floor fields; hand-built props; undersides with flutes/spires/ledges; towers as stacked rings. None of these is a paint on a blocky stamp.
3. **Terrain fidelity**: noise heightfields, `watercourse` that never climbs, `canyon`/`butte`/`scarp`, soil-by-slope with the studio's own gradient definition, bedded rock that dips, undersides. The guide: "A landform is an operation on heights ... cheap, run in seconds."
4. **A read-back vocabulary the studio lacks**: 1.8 physics (`fall_damage`, `knockback`, `solve_launch`), jump audit, no-stand-above, no-catch margin, footing, loose-water, per-spawn arrival, build-walk. Each exists because a board's playtest or plan check found its absence.
5. **Style is data**: grammar + `Style` (brittle, clay) lets a plan be re-spoken; `Strata`, `facade` fields, `props.laid` chests as pictures.
6. **Iteration economics**: whole-board regeneration in 1-30 s and "plan was one file" with a version-suffixed history. Commit stamps show a full board in 10-30 min on the library (opus trials 9-29 min).
7. **Honest caveats**: (a) nothing here is validated by PGM on the new boards; the playtest rounds on older boards found 10+ defects the read-back could not (stair ceiling headroom, filter semantics, entry rules); (b) the plan walk and built walk disagree by 15-40% (opus gap #1), so goal ratios can pass the plan and fail the build; (c) known library defects found above: windows can touch doors (49% of sampled houses), doors at 30/45/60/135 degrees can face a wall, `build.site`/`house` fill over void, `facade.extrude` skips 1-block walls, `wool_chests` and `DEFENCE` unused by almost every CTW board, no objective-visibility check or marker, ST5 redstone outline only on the two Lantern Karst boards; (d) houses are one rectangle per storey (no wings/porches/dormers).
