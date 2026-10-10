> Written by a Sonnet 5.5 helper agent on 2026-10-10 and committed as it wrote it. Its finding that Riftwater was not built to the Russetford brief stands, and is why analysis/freeform-vs-studio/experiment/ exists. Scripts and extracted worlds it names live in a scratch directory and are not committed.

# Same brief, same plan: studio-built boards against freeform / pgmvox boards

All numbers are read off the committed region files with `tools/anvil.py` plus my own numpy census
(`scratchpad/census.py`, `metrics2.py`, throwaway). Heuristics are named where used. Scratch paths below are
under `/tmp/claude-0/-home-user/9425ba5e-905a-5d7a-87d4-1ee2128563da/scratchpad/` (written `S/`).
Nothing was written to the deployed studio (two GETs of `untitled-plan-8`, one `GET /api/maps?stage=plan`, one
`GET /api/openapi/v1.json`); nothing committed.

---------------------------------------------------------------------------------------------------------------

## PAIR 1 — "an autumn river valley, destroy the monument, 16 a side" (2026-10-07)

### Was Riftwater given the same brief? Verdict: no, not verbatim; it is a sibling task, not the same one

There is no brief text anywhere in `freeform/opus55-freeform-riftwater/`. What the files do say:

| Brief clause (as the studio runs state it) | Riftwater |
|---|---|
| "autumn" | **Not autumn.** PLAN.md's palette is "Plains for the open ground (grass #91bd59)", oak and birch only, wheat gold. The renders are summer green (`05-topdown-annotated.png`, `30-iso-board-se.png`). The word does not occur in PLAN, REPORT or PORT-REPORT. |
| a slow river between the sides, a watermill each bank | River runs down each half and falls into the void; each half has a mill and wheel. The two halves are joined only by a 20-wide **void rift** (build zone), not by a slow river. |
| one monument a team | **Two** a team (4 destroyables): a Market Square and a Winding Green. Objective text: "Destroy both of the enemy's monuments". |
| real relief, 3 buildings a team, one place below ground | Ridge 66-80 over a town at 49-52, **29 houses**, and an entire cave/mine/cellar system. Far beyond. |
| 16 a side | `max="16"`. Same. |

Timeline: the three studio runs started about 20:26 to 20:44 UTC (Russetford first request 20:26, Rustwater 20:44,
Rowan Ford committed 20:37). Riftwater's first commit is 22:37 UTC (PLAN + sketch), i.e. a different session
(`session_01JFykgZF2FRCqGGugXE9LUG`) that began after the author's 21:34 ruling commit ("A board is a small world,
planned before it is built", `WHAT-A-BOARD-IS-MADE-OF.md`, whose worked example is a mining board). Riftwater
therefore got the post-review ruling that Russetford's rebuild (22:06) and Rustwater round two (21:44-21:51) also
got, but Rowan Ford (20:37) never did. Read it as "a river valley, destroy-the-monument DTM, 16 a side, built
freeform", rather than the exact autumn brief. The freeform branch's base is the same `f4c2569b` as the studio
branches.

### Worlds found

| Board | Region files | Notes |
|---|---|---|
| studio `opus55b-russetford` (Opus 5.5) | yes, `S/russet/maps/opus55b-russetford/region` | final = third pass, committed 22:31 |
| studio `sonnet55b-rustwater` (Sonnet 5.5) | yes, `S/rust/maps/sonnet55b-rustwater/region` | round two, committed 21:53 |
| studio `haiku55b-rowanford` (Haiku 5.5) | yes, `S/rowan/maps/haiku55b-rowanford/region` | only build, committed 20:37 |
| freeform `opus55-freeform-riftwater` | yes, `maps/dtcm/riftwater/region` | |
| pgmvox port `lib/ports/riftwater` | **no region files** (`--skip write`); only `world/map.xml`. Numbers below are the port's own report (1,001,926 blocks, 110 trees, 16 tile entities) | |

### World metrics (measured)

| Metric | Riftwater (freeform) | Russetford (Opus, studio) | Rustwater Vale (Sonnet, studio) | Rowan Ford (Haiku, studio) |
|---|---|---|---|---|
| bounding box x by z | 240 x 176 (x -120..119, z -88..87) | 144 x 202 (review says 128 x 192 of land) | 108 x 242 | 168 x 92 |
| occupied columns | 36,664 (87% of box) | 25,200 (87%) | 13,213 (51%) | 13,444 (87%) |
| y range used | 2-94 (floating island, tapered underside) | 0-60 (full-depth to bedrock) | 0-56 | 0-37 |
| top-surface y min..max / std | 35..94 / 11.1 | 20..60 / 9.5 | 1..56 / 10.0 | 1..37 / 4.1 |
| non-air blocks | 1,007,258 | 769,633 | 330,695 | 140,462 |
| distinct block ids | **71** | 37 | 30 | 24 |
| distinct (id, data) pairs | **153** | 75 | 64 | 68 |
| distinct top-surface (id,data) | **83** | 51 | 41 | 15 |
| share of columns topped by built blocks | 19.2% | 11.9% | 17.7% | 7.3% |
| share topped by vegetation | 28.4% | 26.9% | 22.5% | 3.5% |
| share topped by bare ground/water | 52.4% | 61.2% | 59.8% | 89.3% |
| terrain core (stone, dirt, grass, sand, gravel, water) of all blocks | 93.2% | 69.6% (+22.5% are clay / terracotta fill and rock beds, ~8% rest) | 92.2% | 86.7% |
| built blocks (non-natural ids, my list; includes cobble used in rock beds) | 31,882 | 17,062 | 6,124 | 4,218 |
| distinct ids / pairs among the built blocks | **41 / 94** | 19 / 35 | 16 / 35 | 17 / 54 |
| built connected components (26-conn) >= 100 blocks | **50** (26 >= 500) | 31 (11 >= 500) | 16 (2) | 10 (2) |
| water blocks | 5,954 | 5,029 | 1,187 | **0** (void river) |
| roofed air under a built roof (interiors) | **33,178** | 8,938 | 7,227 | 6,314 |
| roofed air under natural roof (caves) | **9,806** (largest connected void 4,336 per side; 4 voids >= 200) | 2,987 (largest 495) | 1,056 (one cellar, 480) | **0** |
| leaf / log blocks | 25,934 / 6,648 | 14,699 / 1,858 | 4,112 / 1,400 | 0 / 946 |
| trees (author report / my trunk heuristic) | 106 / 80 (162 by a looser test) | 14 tree props, ~32 trunks | 7 tree props, ~16 trunks | 0 |
| beds / torches / glowstone / ladders / fences | 76 / 244 / 38 / 284 / 254 | 0 / 0 / 0 / 10 / 1,912 (hedge fences) | 0 / 0 / 0 / 10 / 0 | 0 / 0 / 0 / 16 / 0 |
| tile entities | 16 (8 chests of themed loot, 8 shop/inn signs with text) | 10 | 12 | 10 |
| entities | 0 | 0 | 0 | 0 |

Heuristics: "built" = ids outside {stone family, dirt, grass, sand, gravel, water, bedrock, clay 82, terracotta 172,
ores, obsidian, block 36, leaves, logs, plants, vines, carpet, cobweb}; cobble (4) counts as built, which inflates
the studio boards' number because they use cobble in rock beds and lanes. "Roofed air" = air with a non-vegetation
block above it in its column; "natural roof" = nearest roof block is stone/dirt/grass/ore/etc. Tree counting is
crude; the two author counts are better.

**What the tile entities are.** Every studio tile entity is exporter scaffolding, none is authored: 8 signs at the
observer spawn on the origin (`[DTM] <name>` / `made by <model>`), plus one chest under each monument stamped with
planks (Russetford 2, Rowan Ford 2, Rustwater 2; Rustwater also adds two golden-apple chests it authored). The 16 in
Riftwater are all authored: "Chandler / rope & candles", "Baker / fresh bread", "The Falls Inn / rooms & ale" signs
and eight loot chests (woodcutter, smugglers, gaol cellar, miners' stores).

### map.xml

| | Riftwater | Russetford | Rustwater | Rowan Ford |
|---|---|---|---|---|
| gamemode / objectives | dtm; **4** destroyables (2 a team) | dtm; 2 | dtm; 2 (gold "Millstone") | dtm; 2 |
| regions (all tags) / applies | 18 / 4 | 16 / 4 | 19 / 5 | 19 / 5 |
| build-zone regions | `not-build-area` negative over the rift `rectangle(-16..16, -88..88)` with `no-void` block filter | **none** (river is water, no void zone) | `build-area-1` strip (-52..52, -12..12), void filter on place and break (trees/flora exempt) | `build-area` void gap, full depth, same filter |
| filters | 3 | 2 | 5 | 5 |
| kits | 1 (10 items) | 2 (11 items, enchants, effects) | 2 | 2 |
| modes (monument turns gold, glass) / kill-reward / itemkeep / toolrepair / hunger | **none of these** | modes 15 m gold, 20 m glass; `gapple-kill-reward` include; itemkeep, itemremove, toolrepair, hunger off | same | same |
| maxbuildheight | 90 | 51 | 45 | 30 |
| xml lines | 77 | 149 | 173 | 172 |

The studio's export is the richer **document** (match clock, kill rewards, item keep). The freeform one is a minimal
valid file with 4 destroyables and the void filter, the opposite of its world.

### Objective placement and discoverability

| Board | Monument | Floating marker in the world |
|---|---|---|
| Russetford | obsidian pillar y36-38 on the village green at `(4,-56)`; stamped planks chest at ground y32; three blocks of air between | **Yes**: a 7-block team-coloured wool plus at y56-58 straight above each monument (obsidian top 38, so 18 blocks up). Spawn point has a 2x2 team wool pad at y39. `maxbuildheight 51 + 5 = 56` |
| Rustwater | gold block, bedrock, gold column y29-31 on the Millstone terrace | Same plus at y50-52 (maxbuildheight 45 + 5) |
| Rowan Ford | obsidian y13-15 at `(-61,-38)`, `(60,-38)` | Same plus at y35-37 (maxbuildheight 30 + 5) |
| Riftwater | obsidian pillars two high floating one block above the ground: Market Square `(-66,54-55,-44)`, Winding Green `(-66,52-53,48)`, mirrored | **None.** No beacon, glass or wool column anywhere (0 beacon, 0 glass). Found by the paved square, the town hall behind it and the chapel belfry that looks down on it, and by the objective text in map.xml |

The studio's `WorldBuilder` hangs every goal marker at one altitude (`BuildCeiling`: the ceiling is 20 above the mean
surface and markers five over that), so the studio boards have a sky beacon at the same height over every goal. It is
infrastructure, not design; Riftwater leaves discoverability to the architecture and the annotated top-down.

**Build zone in the world:** unmarked on all four. No cobweb, outline, or lamp marks the zone edge on the studio boards
(`cobweb` 0) or Riftwater (2 in total); the rift's walls are dressed with 726 vine blocks and its
lip is shaped (bays, held straight at bridge heads), which tells a player where the void is, but nothing says where the
zone is. (Brittlebush III in Pair 2 does mark it: 76 cobwebs.)

### Places on each board

| | Places that exist |
|---|---|
| Riftwater | 25 named places in the plan, 29 houses: **Market Town** (16 brick-and-timber buildings on three streets stepping down 52 to 49), market square with stalls and signs, town hall, **chapel with 20-high belfry and ladder**, inn, bakery, **gaol with a 3-cell cellar**, **broken Old Bridge** half-arches over the rift, **hump-backed keystone stone bridge**, **watermill with a dark-oak wheel turning in a cut race and a weir**, **mill pond with spring, jetty, rowboat, reeds, trestle footbridge**, **twin waterfalls pouring into the void**, **Falls Cave** (mouth behind the water on a ledge, lake chamber, pillar hall, smugglers' grotto with chest), **sinkhole**, **Ironhollow mine** (adit, shaft with ladder, galleries with timber sets and rails, ore), **Ironhollow village** (cottages, smithy, well, spoil heap, engine house with brick stack), **headframe**, wheat field with ditches, scarecrow, hay cart, barn, haystacks, hedgerow, **Lone Oak Knoll**, **the Cutting** (stumps, log piles, sawhorse), Watch House spawn on a terrace with a four-storey tower, North Wood, woodcutter's hut with chest |
| Russetford | spawn tower with farmhouse built on, hay yard, orchard on a **cut bank with a cave** under it (mouth at water level, chamber 9 from the monument), monument green on a paved disc, a street of 3 cottages and a well, **stone mill on a leat with a slatted wheel**, miller's house, **market stand with striped wool awning**, **humpback stone bridge** (the one dry crossing), footbridges over the leat, oak **hanger with a ruined castle of two towers and 4 curtain-wall runs**, field with wheat and potatoes, hedges, dry-stone walls, fenced gardens with pumpkins, woodcutter's clearing (log pile, 2 stumps), 10 boulders; autumn colour from a noise biome mosaic (Plains/Savanna/Mesa), banded rock |
| Rustwater Vale | spawn hall on a shelf under a ridge, **the Watch** (ruined round tower with a chest, 26 above the monument), Millstone terrace, Haldenwood and a clearing (4 stumps, 2 log piles), hamlet cottage and root cellar (the one roofed hole), mill with quay, miller's house, orchard and ploughed furrows behind a drystone wall, footbridge to the water, jetty and moored boat, barn; 90 props over 5 themes |
| Rowan Ford | per team: a mill, a store, a lookout (three houses), grass flats and a 4-block step; **no water, no trees, no relief, no below-ground place** (the report says so) |

---------------------------------------------------------------------------------------------------------------

### Author effort (Pair 1)

| | Riftwater (freeform) | Russetford | Rustwater | Rowan Ford |
|---|---|---|---|---|
| authored code | **3,379 lines Python** in 16 scripts (+86 C# writer, 17 sh); every block is placed by code. Port: 2,041 lines on pgmvox 0.6.0 (~900 of them local) | `build-spec.py` **426** lines + `composition.md` 58; the 29k-line `refinement.json` is generated | **319** lines | **118** lines |
| plan before build | PLAN.md (124 lines, 25 places each with reason, how, routes, palette) written before terrain, read from an annotated sketch, 7 changes recorded after viewing renders | first build had none; `composition.md` drawn only after the author's first review | none in round 1; "seven places and eleven lanes" in round two | one identity sentence |
| wall clock (commit stamps) | 22:37 to 23:10 = **33 min** between first and last commit (the session's start is not recorded; upper bound 96 min from its 21:34 base commit) | first request 20:26 to final store 22:30 (124 min incl. two author reviews); the report counts about 19 + 13 + 8 = 40 min of driving | 20:44 to 21:51 (67 min); 14 + 7 = 21 min driving | commit 20:37 (the report says about 8 min and distrusts that figure) |
| iterations | 10 commits, each after a render or walk | **31 stores** (14 + 10 + 7); 2 stores refused (`PT3`/`PT4`), 1 dry `PT4`, 1 export `RQ1` | **16 stores** (7 + 9), 2 dry refusals | **13 stores**, ~16 dry runs, 7 dry refusals |
| author review rounds | none recorded on the studio side. Self-review loop through iso, x-ray, elevations, walk. The pgmvox port the next day had a library review | **2** (first build "a ramp with three houses"; second: 12 asks) | **1** ("the land is a fair start, the rest is unfinished") | **0** |

### What each report says went wrong

- **Russetford:** first build had no composition (dead-ground 37%); the river was "a ruling followed past its sense" (two canals
  with void between); one biome painted everything one brown; a stroke repaints water so footbridges stood over andesite; a fluid's carve emptied the
  wheel's course; a height stack does not cycle (pale clay everywhere above y11); sealed the cave mouth; hedges in decaying leaves;
  `"biome": "Mesa"` stored at 200 but export refused `RQ1`. Could not say: a spoked waterwheel (a layer is one span a column), biome by place, a boat or sheep.
- **Rustwater:** river is two half-rivers (a fluid cannot stand over void); no wheel; no tree within 20 of the spawn (`DR-KEEP`);
  planned a layout and not a world; ground cover everywhere does not make dead ground a place; picked library styles by name and
  most are timber-framed; tuned one relief instead of three; never looked from a player's eye. Stumps, haystacks, pumpkins had to be
  boulder recipes in log, hay or pumpkin blocks, against the author's ruling that boulders are stone. Still missing: a mill wheel, a stair up the Watch.
- **Rowan Ford:** relief "almost flat"; no below-ground place (two attempts either painted as stone or cut columns to void, found only by `column`); a river of void not water;
  spawn two blocks from the edge; four-corner wings (`HP2` x6); explicit mirrored houses collided with the symmetry fan; biome stored as string.
- **Riftwater:** nothing played on a server; **light not done** (every section sky-lit, so the caves are daylight-bright); no entities in the writer
  (a boat is blocks); fields still nearly level; some trees only dice-placed; enemy-spawn-to-monument on foot "not reached" (needs bridging; the 8/20/20
  air gaps are measured). The port dropped barn, haystacks, cart, jetty, rowboat, spring, gardens, benches, hedgerows, worn paths, house furnishing, wing roofs.

### Renders to open (Pair 1)

| Board | Most telling |
|---|---|
| Riftwater | `/home/user/pgm-studio-mapgen/freeform/opus55-freeform-riftwater/renders/05-topdown-annotated.png` (every place named), `30-iso-board-se.png`, `33-iso-town.png`, `38-iso-rift-falls.png`, `40-xray-underground.png`, `35-iso-river-mill.png`, `00-plan-sketch.png`; 54 renders in all (plan sketch, material/height/objective top-downs, 12 sections, 10 isometrics, 2 x-rays, 5 elevations, `walks.txt`) |
| Russetford | `S/russet/specs/opus55b-russetford/opus55b-russetford.png` (1280x720 studio eye render, textured), `S/russet/maps/opus55b-russetford/map.png` (290x246 thumbnail) |
| Rustwater | `S/rust/specs/sonnet55b-rustwater/sonnet55b-rustwater.png`, `S/rust/maps/sonnet55b-rustwater/map.png` |
| Rowan Ford | `S/rowan/specs/haiku55b-rowanford/haiku55b-rowanford.png`, `S/rowan/maps/haiku55b-rowanford/map.png` |
| like-for-like | I re-rendered all four studio worlds with pgmvox's own iso renderer, so they match Riftwater's `30-iso-board-se.png`: `S/renders/studio-russetford-iso-se.png`, `studio-rustwater-iso-se.png`, `studio-rowanford-iso-se.png` |
| port | `/home/user/pgm-studio-mapgen/freeform/lib/ports/riftwater/renders/` (13 renders, same names as the original; PORT-REPORT says the two are "hard to tell apart" from above) |

### The 8 biggest reasons the freeform board is richer (grounded)

1. **It has a below-ground world; two of the three studio boards barely have one.** 9,806 blocks of roofed air under natural rock
   in four connected voids (largest 4,336 per side: falls cave, lake, pillar hall, grotto, sinkhole, mine, cellar), plus gallery/shaft/cellar.
   Russetford 2,987 (largest void 495), Rustwater 1,056, Rowan Ford 0. The studio has no tunnel or gallery shape; the carve `floor` trick
   gave Russetford one cave and Haiku none.
2. **Block vocabulary.** 71 ids / 153 (id,data) pairs against 37/75, 30/64, 24/68, and 83 distinct top-surface kinds against 51/41/15.
   Built blocks alone span 41 ids against 16-19 on the studio boards.
3. **Interiors are made, not stamped.** 33,178 blocks of enclosed built space against 6-9k; 76 bed blocks, 244 torches, 38 glowstone, 284 ladders,
   pews, bars, smithy fittings, 8 loot chests and 4 shop signs with text. Studio houses are shells: 0 beds, 0 torches, 0 glowstone, and every
   tile entity is stamped scaffolding.
4. **Count and kind of set pieces.** 50 connected built structures >= 100 blocks (29 houses, chapel, watch tower, mill + turning wheel, headframe, engine
   stack, two kinds of bridge, a broken bridge, a jetty, a cart, a scarecrow) against 31 / 16 / 10. Each exists because PLAN.md gave a place a reason.
5. **Relief and silhouette are modelled in 3-D.** A floating island with a tapered, bedded underside, a sheer rift wall, ridge at y66-80 over a town at 49-52,
   y span 35-94 (59 on the surface) against 20-60 / 1-56 / 1-37; rivers with water levels (pond 48, river 45, weir), two facing waterfalls into the void.
   Studio boards are full-depth slabs to bedrock (Russetford has 24.7k bedrock + 173k clay/terracotta fill blocks).
6. **The plan was a design document, and the check was a read of the built world.** 25 places each with why / how, routes, walks measured at 63 and 81 blocks
   on the built board, each of 7 revisions made against a render. The studio runs planned the layout in round one and the places only after the author said so.
7. **Seeing was a third of the effort.** Iso, x-ray, elevations, annotated top-down and a voxel walk meant 10 commits in 33 minutes, each fed by a picture.
   The studio runs had `render/eye`, one overview and `column`; Rustwater and Haiku report not looking from a player's eye at all.
8. **No schema stood between the author and the block.** Spoked wheel, stumps, haystacks, pumpkins, a trestle, a spring, a pillared hall were each 5-60 lines of code;
   in the studio each was "missing" or a workaround (boulder recipes, a slatted disc). The cost: 3,379 lines against 118-426, and no gates (nothing
   checked `GO1` ratios, the export, or PGM), no match clock, no light, and the brief itself drifted (green not autumn, 4 monuments not one).

---------------------------------------------------------------------------------------------------------------

## PAIR 2 — Brittlebush III (the planner's plan `untitled-plan-8`)

### What the studio has: plan stage only

`GET /api/map/untitled-plan-8/state`: `stage: plan`, artifacts `{plan: true, sketch: false, world: false, intent: false}`; moves open:
edit plan, `sketch/from-plan`, `intent/from-plan`, state intent. `GET /api/maps?stage=plan` gives `updatedAt 2026-10-09T15:04:11Z`, author rockymine,
no gamemodes, no objective. So **the deployed studio holds a drawing and nothing built**; the pgmvox board is the only world made from it.

Plan content (`GET /api/map/untitled-plan-8/plan`, byte-identical in meaning to `freeform/lib/boards/brittlebush-iii/plan.json`; diff after `json.tool` is empty):
version 2, cell 5, `rot_90`, `maxPlayers 12`, global surface 9; **17 pieces** (surfaces 9 / 12 / 15 / 18), **7 zones** (named `water`, `water-2`, `water-3`, `zone`...), one spawn
(piece `spawn`, facing left) and one wool (piece `wool`, footprint 8x8), no walls, boxes, iron, destroyables. 38 x 38 cells = 190 x 190 blocks, four teams of 12.
The planner's `/plan/flow` reads it: wool at (90,5), attacker walks 130 blocks, defender 53 (ratio 0.41), 3 ways in.

### What the studio would produce from it (I ran the studio's code, locally, unauthored)

I copied `src/` to the scratchpad and ran, through file-based scripts, `PlanCompiler.Compile` then `WorldBuilder.Build` (the pure core of the studio's export: no
database, no themes, no room styles, no dressing, no refinement) and wrote the region with `AnvilRegionWriter`. This is the studio's floor for this plan, not an
authored result.

- **Compile:** one `ground` layer with 24 shapes: 8 flat plateaus (four at 9, two at 12, one at 15, one at 18, fused rectangles), 4 spawn-room shapes, 4 wool-room shapes,
  8 `building` footprint shapes. Intent: 4 teams, 4 spawns, 4 wools with **no monuments placed yet**, 28 build areas, 4 entrance redstone lines, 0 water lanes (a zone named `water` is only
  a build zone; the plan has no water-lane kind), no objectives beyond the wools.
- **Build:** 91,084 blocks, 10 ids / 29 pairs, y 0-40, 7,504 columns; 86.4% of columns topped by plain stone; the only non-stone things are redstone lines (468), wool-room cages (clay, wool, glass panes), 4 floating goal-marker cubes, and 8,820 bedrock.
  No water, no vegetation, no grass. Complaints: `WX14` wool and spawn rooms "have no house of their own" (x4 each), `EX6` no author. `maxbuildheight` 33.
  48 tile entities, all stamped (16 signs, 32 chests).
- Picture of it: `S/renders/studio-bb3-default-iso-se.png`. Stairs, `double-layered` decks and water are just names to the studio, which has no concept of a stair between pieces
  at the plan grain or a hollow deck. To get Brittlebush's cornice, hollow undersides, wool houses of whole cells, hearts and cobweb lines the studio route would need themes, room styles
  and made layers on top (the Pair 1 boards show what that costs: 118-426 spec lines, 13-31 stores).

### pgmvox build vs studio default (measured)

| Metric | pgmvox `brittlebush-iii` | studio default from the same plan | brittle-study (pgmvox swatch of the real map) |
|---|---|---|---|
| mode | **ctw**, 4 teams, 12 wools (each team captures the other 3) | not set (intent holds 4 wools, no monuments) | none, no objectives |
| extent / y | 190 x 190, y 0-36 | 190 x 190, y 0-40 | 72 x 60, y 0-46 |
| columns occupied | 10,244 (28% of the box: islands over void) | 7,504 | 1,794 |
| non-air blocks | 107,727 | 91,084 | 23,447 |
| distinct ids / pairs | **31 / 80** | 10 / 29 | 27 / 50 |
| distinct top-surface kinds | **41** | 13 | 27 |
| top surface: built / vegetation / bare | 69.9% / 7.8% / 22.2% | 13.6% / 0% / 86.4% | 66.4% / 6.2% / 27.4% |
| mass blocks | bedrock 40,364, obsidian 12,800, block 36 10,200, stone 19,740 | stone 81,320, bedrock 8,820 | bedrock 10,441, obsidian 3,482 |
| water | 1,200 (at the zones' floor, no kerb, PGM holds it still) | 0 | 0 |
| cobweb (zone outline) | **76** | 0 | present (dotted bounds line) |
| wool / stained glass / beacon | 313 / 20 / 8 | 252 / 12 / 0 | 165 / 0 / 0 |
| trees | 28 round birches | 0 | 2 |
| roofed air (interior + hollow decks) | 6,683 (4,347 under built roofs: 4 wool towers, 4 spawn houses; 2,336 classed natural by my test: under stone-roofed decks and the tunnel) | 2,044 (cages) | 617 |
| tile entities | 0 (Brittlebush has none) | 48 stamped | 0 |
| objectives marked in sky | 8 beacons (wool house and spawn house per team) shining through team-coloured glass, a floating stack of the team's wool over the spawn house | 4 floating cubes (the studio marker) | none |
| build zone in world | cobweb dotted outline plus water floor | none | |

Authored content in pgmvox's build: per team a **spawn house stacked of whole cells** (3 storeys), a **wool house** 10 blocks square in an L stack with storeys of black
clay / dark-oak stairs / brick, birch panels framed in black clay, eaves, a sand terrace on a sea-lantern ceiling, a beacon on gold in the top cell, **three hollow-deck under-sections**
(a middle island with a pillar, an island with a one-cell tunnel, one before the wool), grass beds with kerb, sand beds with pebbles and cacti, ribbed stone-brick paths, grey stone flights, a redstone line in front of
the wool house, a one-block outline of planks on every piece. Read back: 0 objective problems, 0 blocks without footing, every team's numbers identical (own wool 49 on foot, others 110 / 135 / 143 building).

Effort: `brittlebush-iii/scripts` is **364 lines** (plan 142, walk 78, gen 76, renders 43, mapxml 25) on top of the **7,737-line pgmvox library (1,012 lines of tests)**; of that the Brittlebush-specific
parts are `brittle.py` 650 + `grammar.py` 321 (+ `clay.py` 203, `facade.py` 376, `studioplan.py` 107). Timeline from stamps: plan last saved in the studio 15:04 UTC on 2026-10-09; the study of the real map 14:15; pgmvox 0.12.0 + first build 16:25
(81 min after the plan was saved); further passes 17:04, 17:24, 17:28, 18:06, 18:20 (last). About 2 h of iteration after first build, all of it feeding on a library written
the same afternoon (0.11.0 15:51, 0.12.0 16:25, 0.13.0 17:24, 0.14.0 18:06). Not opened in PGM; not written back to the studio (the report says so).

### Renders to open (Pair 2)

- pgmvox: `/home/user/pgm-studio-mapgen/freeform/lib/boards/brittlebush-iii/renders/` : `05-topdown-annotated.png`, `30-iso-board-se.png`, `40-iso-full-{ne,nw,se,sw}.png`, `34-iso-red-wool-sw.png`, `39-iso-wool-house-se.png`, `36-iso-middle-island-under-se.png`, `37-iso-tunnel-se.png`, `33-iso-red-spawn-se.png`.
- brittle-study: `/home/user/pgm-studio-mapgen/freeform/lib/boards/brittle-study/renders/` : `01-original-and-study.png`, `ref-brittlebush-se.png`, `ref-brittlebush_ii-wool-room-se.png`, `30-iso-se.png`, `32-tower-se.png`, `10-section-x-20.png`.
- studio floor: `S/renders/studio-bb3-default-iso-se.png`. The deployed studio has no render for this map (stage plan); `GET /api/map/untitled-plan-8/plan/ascii` is its only picture, a 38 x 38 letter grid.
- The real Brittlebush world is not present on this machine (CommunityMaps is not under `/media/sf_repos`), so the study's `ref-*` renders are the only view of it.

### Why pgmvox's build is richer than what the studio makes of the plan (and what it is not)

1. The plan carries only rectangles, heights and roles; every visible fact of Brittlebush (cornice, hollow undersides, wool tower, hearts, panels) is **grammar**, which pgmvox encodes and the studio does not have as a plan-level concept.
2. Result: 31 ids / 41 top-surface kinds against 10 / 13; 69.9% of columns topped by built blocks against 13.6%; 1,200 water blocks and 76 cobwebs against none.
3. pgmvox read the plan's **zone names** (`water...` vs bare) and the author's piece names (`stair...`, `double...`); the studio gives those names no meaning.
4. Caveat in the other direction: the studio default is not a fair "studio build" (no themes, room styles or dressing were stated), and pgmvox leans on 7.7k lines of library built for this family of boards the same day.

---------------------------------------------------------------------------------------------------------------

## Scratch files

`S/census.py`, `S/metrics2.py`, `S/xmlsum.py`, `S/te.py`, `S/around.py`, `S/rend.py`, `S/trees2.py` (all throwaway readers); `S/census_*.json`, `S/m2_*.json`;
`S/plan8.json` (the deployed plan), `S/studio-layout.json`, `S/studio-intent.json` (compile output), `S/studio-bb3/region` (the studio-default world),
`S/studio-copy/` (a copy of `src/` used only to run the compile and build).
