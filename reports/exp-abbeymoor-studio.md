# exp-abbeymoor-studio — Abbeymoor, destroy the monument, authored through pgm-studio's HTTP API

Builder: Sonnet 5.5, driving the local studio at `http://localhost:7894/api` (signed in as the local admin; the deployed
studio was not touched). Experiment pair: this board and `freeform/lib/boards/exp-abbeymoor-pgmvox`, same brief, same
lessons. Spec: `specs/exp-abbeymoor-studio/build-spec.py` (writes the plan and the refinement; `tools/drive.py` stores
them). World: `maps/exp-abbeymoor-studio/`. Renders: `specs/exp-abbeymoor-studio/renders/`.

## What I set out to build

**Abbeymoor: a high moor of 112 by 240 blocks where each team of sixteen holds the hill of a ruined abbey, with an orchard
village below it, and a peat bog with standing stones between the two sides, joined by land.** The north team spawns in a
stone longhouse at the top of the board (z -120..-100, ground 38). South of it the moor runs to an abbey hill whose crown is a
flat at y46 (x -42..-6, z -96..-66) carrying a ruin of broken walls, a west gable 14 high and a tower stump, with a
cloister of column stumps to its north. East of the hill, down a 12-block fall, is the village terrace at y34 (x -2..56,
z -90..-56): a longhouse and two cottages in a row, a paved street, and the village monument. South of the village the
land steps down in two orchard terraces (y27, y22) with rows of oaks, to the bog at y20 (z -30..0, fanned to z 30): a
peat floor of podzol and coarse dirt with four hags, two pools, a ring of seven standing stones and a causeway of single
stones. The south team's half is the same turned 180 degrees about the centre.

Under each abbey is a crypt: a pillared hall (x -40..-12, z -88..-72, floor y11, six high), a four-block ladder shaft from its
north-west corner up to the abbey floor, and a corridor east and south that ends in a stone-curbed well at (24,-60) in the
village square, 6 blocks from the village monument. A defender or attacker can take the crypt from the abbey and come up
beside the village monument, or the reverse.

Tone families, named before painting: **ground** is grass over dirt with coarse-dirt patches on the moor, podzol and
coarse dirt on the bog, slate-grey rock from 33 to 35 degrees; **built** is stone brick (plain, mossy, cracked), cobblestone
and polished andesite for the ruins and the crypt, and the library's timber and stone for the village; the **accent** is the
water of two pools and the oaks of the orchard. About 224 blocks between the spawns (z -112 and +112). Biome Swampland.

## Self-review, written before the final build

Written 01:36, after store 11 (the sketch as it stood: relief, crypt, ruins, village row, four pools, bog and heath paint) and before the final store.

**Against the brief**

- Two monuments a team, abbey and village: `abbey-monument` at (-24,-69) on the crown (ground 46, float 3, blocks y49..51) and `village-monument` at (36,-59) on the village terrace (ground 34, float 4, y38..41). Both are obsidian pillars, 3 high, and both stand in the open; the abbey one rises over the ruin walls from the bog approach (seen in `eye-abbey-monument-approach.png`). One flaw found: orchard trees `o4` (34,-45) and `o8` (32,-31) stood in the line from the terrace below to the village monument. Both are removed.
- Land-joined across the bog: the bog piece is z -24..24 at ground 20, with no void anywhere in the plan. Met.
- Crypt under each abbey, passage up near a monument: the hall (-40..-12, -88..-72, y12..19) is a ladder shaft at (-36,-85) from the abbey floor (stair), and a corridor east along z -83..-78 and south along x 22..27 to a well at (24,-60), 12 blocks from the village monument. The north team's crypt therefore comes up beside its own village monument; the south team's crypt, by symmetry, beside the south village monument at (-36,59). The brief's "comes up near one of that team's monuments" is met by the well. The crypt is not reachable from the other team's side in a way that bypasses the monument by more than a short walk. This is the intended flank.
- At least six places a side: spawn longhouse, abbey crown with the ruins, crypt hall, village row (longhouse and two cottages), orchard terraces (two), the well, the standing-stone ring, a tor, a peat pool, the bog causeway. Ten.
- 200 to 260 along the axis: spawns at z -112 and +112, 224 between them.

**Against the twelve lessons**

- 1: monuments are in the open and float; defenders can stand round both. Met.
- 2: obsidian with a kit whose pickaxe is diamond (map.xml line 27). Met.
- 3: no wool room. Not applicable.
- 4: orchard rows are 10 blocks apart on terraces 8 and 6 blocks deep (z -49..-41 and -34..-28), and the lane (ramp-orchard x=8) is kept clear by DR-ROAD. Trees are tiny oaks. Met after the two removals.
- 5: no stairs are built by this board; the hill is climbed by a graded ramp line. Not applicable except that the hill has scrambles of 2.
- 6: spawn door is a 4-wide gap, the road runs out of it. Met (`t4` eye view).
- 7: no floating platform. Not applicable.
- 8: two ladders, at the two shafts, neither in water (the pools are at z -17..-1 and x -40..-10, far from them). Met.
- 9: the stair shaft and the well both reach the crypt floor at y12; column reads at (-36,-85) and (24,-60) show the ladder from y12 to the surface. Met by the read; to be re-checked after the final store.
- 10: ruin walls are 1 block thick, pillars 2x2, the well 3x3 opening. Met.
- 11: bog paint, four peat hags, four heath patches, worn village square. Met.
- 12: no build zone (the sides are joined by land). Not applicable.

**Defects accepted into the final store**

- The abbey hill's south face scrambles over a few columns (about 1000 scrambled of 27000 columns); the graded ramp is the walk.
- A quarter of the ground is on no journey (flow read): the moor flanks and the two ends of the bog. A destroy board has no wool to carry, so the read is advisory; the flanks carry the tor and the tree rows.
- Plan lints EL1 (moor/bog 18 apart where they touch — the orchard terraces take the fall) and WX8 (the iron cube) remain; both are the plan's piece model, not the ground.

After this review one thing moved: `POST /plan/inspect` read the village monument's walk from its own spawn and from the
enemy's at 63 and 185 (2.94; GO1 wants 3 to 4) for the position (32,-62) the review had left, so I set the monument at
(30,-62), which reads 61 and 183 (3.0), and stored it as store 14. The plan evaluator, not the review, found it.

## What the board turned out to be

| Thing | Where | Read |
|---|---|---|
| Spawn longhouse (library style, door gap 4 wide) | x -16..12, z -120..-100, ground 38; the other at z 100..120 | `eye-spawn-doorway.png` |
| Abbey crown, ruins, cloister | x -42..-6, z -96..-66, ground 46; ruin walls 2..16 high | `iso-north-west.png`, `eye-abbey-ruins-from-village.png` |
| Abbey Monument (obsidian pillar, 3 high) | (-24,-69), blocks y49..51 over ground 46; mirror (24,69) | `eye-abbey-monument-from-bog.png` |
| Village Monument (obsidian pillar, 3 high) | (30,-62), blocks y38..40 over ground 34; mirror (-30,62) | `eye-village-monument-from-orchard.png` |
| Crypt hall, pillars and glowstone lamps | x -40..-12, z -88..-72, y12..17, floor y11 | `eye-crypt-hall.png`, `xray-south-east.png` |
| Stair shaft, abbey side | x -37..-33, z -85..-81, ladder at (-36,-85) y12..45 | column `-36,-85` |
| Corridors | x -12..27 at z -83..-78, then x 22..27 at z -78..-62; y12..17 | `eye-crypt-corridor.png` |
| The well, village side | opening x 23..26, z -62..-59, ladder at (24,-60) y12..33, curb around | `eye-well-from-above.png`, `eye-well-from-below.png` |
| Village row | farm longhouse x 12..24, cottages x 29..35 and x 40..46, all z -79..-73 | `iso-south-west.png` |
| Orchard | oaks at z -45 and z -35..-31 on the terraces y27 and y22; road x=8 up to the village | `eye-orchard-terraces.png` |
| Bog, pools, standing stones | pools (-36..-12, -17..-1) and (-10..4, 6..17) and their turns; ring at (24,-10) radius 9 by 7 | `eye-standing-stones.png` |
| Tor, boulders, yews | tor (-50,-50) and (48,-108); yews in the garth at (-34,-94), (-22,-94) | `iso-north-east.png` |

Reads of the stored board: ground 25196 columns walked, 1054 scrambled (3.9%), 580 barrier (2.2%), worst step 4 on the
route from spawn to the abbey monument; export gate OPEN; mirror check clean; 54 props placed, 0 declined; the x-ray finds
28 roofed voids, none sealed, and the crypt as one connected void (4882 cells, x -40..26, y12..19, z -88..-63) joined to the
surface at both shafts. Walk distances `plan/inspect`: abbey monument 48 from its own spawn and 190 from the enemy's (3.96);
village monument 61 and 183 (3.0). 23.4% of the ground is on no journey (the moor flanks and the two ends of the bog).
Remaining complaints: `EL1` (moor and bog differ by 18 where their plan pieces touch; the orchard terraces take the fall),
`WX8` (the iron cube has no 3 by 3 place in the spawn piece), and `SK14` seven times (the lids over the crypt state a top
that the relief also sets; they are the intended override).

---

## 1. Times (`date`, UTC, 2026-10-10)

| Phase | Start | End |
|---|---|---|
| Reading (BRIEFS read once for both boards, the three shared documents, the studio's rules for DR, OB and SK) | 01:18 | 01:19 |
| Plan, relief, crypt, ruins and dressing written; first store (change 1 at 01:25:39) | 01:19 | 01:26 |
| Sketch and dressing iterations (stores 2 to 13: declines cleared, village row, pools, bog paint, orchard thinned) | 01:26 | 01:36 |
| Self-review (written to the scratchpad, then pasted above) | 01:35 | 01:36 |
| Final stores (12 to 14), final world | 01:36 | 01:37 |
| Renders and reads | 01:37 | 01:38 |
| Report | 01:38 | -- |

Stores: **14** (`GET /map/exp-abbeymoor-studio/changes`), every one a whole-source `PUT`. The board stored on the first
try (preflight OPEN) with the crypt in it; the other 13 were: monument style (DC3), the village layout against DR-PASS,
DR-CROSS, OB19 and DR-CLAIM (five stores), pools against DR-DRY (four stores), paint (one), tree sight lines (one), a
goal ratio (one).

## 2. What the brief asked for that the studio could not express, and what I did instead

| The brief asked for | What the studio does | What I did |
|---|---|---|
| A crypt under each abbey | **No underground primitive.** Ground is slabs, one span a column; a void is a `subtract` shape whose declared courses nothing else may overlap (`SK13`), and anything over it is a `lid`, an override add | Eight `subtract` cuts (hall in four pieces round the shaft, two corridors, two shafts) with seven lids over them, and the crypt's own floor, pillars, lamps and ladders as made layers at base y11, y12 and y18 |
| A ladder in the shaft | **No ladder or stair prop.** A block with a data value is a made-layer box | `crypt-ladders`: ladder data 3 at (-36,-85) from y12 to y45 and data 2 at (24,-60) from y12 to y33, each on the solid wall behind it |
| A ruin | No ruin prop; the library has no abbey. Walls are boxes | 37 boxes of stone brick in a made layer: four wall runs of broken heights, a tower stump, ten cloister stumps |
| Standing stones | No stone prop | Twelve single-column boxes of andesite in a made layer, a ring of seven and a causeway of five |
| Two different monuments (abbey and village) | `DC3` caps an obsidian monument at 3 blocks; a cube of 27 is built of ender stone and the kit would then lack the right tool | Both are 3-high obsidian pillars; the abbey's float is 3 (the build ceiling), the village's 4 |
| An abbey and a village as different buildings | **One spawn shell and one set of room styles**; the village is library houses and the abbey is made walls | Library houses (farm longhouse, two cottages) for the village; made walls for the abbey |
| An orchard | No orchard prop; trees are props, one each | Seven oaks on two terraces in rows, kept off the road by `DR-ROAD` |
| Heather | No heather in 1.8 | Heath patches of podzol, grass and coarse dirt, and the flora cover's flowers |
| A peat bog dark and wet | A theme paints a shape; water is a `fluid` prop that stands against a relief hollow and is judged by `DR-DRY` | Bog-paint over the bog band, four peat hags, four pools. **A relief hollow does not fan its fluid:** the rot_180 fold turns the hollows, the fluid props do not, so each pool is written twice. The water polygon is the hollow grown by its bevel, with the lip held at the water's level, found in four stores |
| A passage "near a monument" | A read says where a column is open; **no read says that one place is near another or visible from it** | The well is 6 blocks from the village monument at (30,-62), shown by `eye-well-from-above.png` and column reads; the abbey stair is on the crown |
| Both monuments "visible from the ground an attacker approaches over" | No visibility read | Eye views from the approach: `eye-abbey-monument-from-bog.png` and `eye-village-monument-from-orchard.png`; two trees removed after the first view showed them in the line |
| Houses with interiors | One library house had a sealed loft (the x-ray reads `2 sealed`) | Swapped for a different library longhouse; 0 sealed |
| A build zone | None for a land-joined board | Not applicable |

## 3. The twelve lessons, one by one

| # | Lesson | Met? | Evidence and coordinates |
|---|---|---|---|
| 1 | Objective in the open, never only underground or on a tower, floating a few blocks | **Met** | Abbey monument (-24,-69) blocks y49..51 over crown ground 46; village monument (30,-62) y38..40 over ground 34; both in the open with ground round them, the second 6 blocks from the well. The crypt reaches them, it does not hold them (`eye-abbey-monument-from-bog.png`) |
| 2 | Made of what the mode needs | **Met** | Obsidian goals; the spawn kit carries a diamond pickaxe (`map.xml` line 27) |
| 3 | Wool room loot | **Not applicable** | A destroy board has no wool room |
| 4 | Vegetation leaves the floor visible | **Met** | Seven tiny oaks on two terraces, 10 blocks apart in rows at z -45 and z -35..-31; the lane x=8 (z -58..-26) has none within 3 blocks; two yews at (-34,-94) and (-22,-94) in the garth; none in the crypt, the pools or the bog |
| 5 | Every stair attached and walkable | **Not applicable, one thing to say** | No stairs built. The hill is climbed by a graded ramp line (`ramp-abbey`, (-30,-28) to (-24,-66)); the worst step on a route is 4 (`report`) |
| 6 | Spawn exit open | **Met** | A doorway about 4 wide and 2 high in the longhouse's south wall, with a road beyond (`eye-spawn-doorway.png`) |
| 7 | Floating platform not mineable | **Not applicable** | No floating platform; the crypt floor is ground over bedrock at y0 |
| 8 | Ladders only where needed, never in water | **Met** | Two ladders, at (-36,-85) y12..45 and (24,-60) y12..33; the nearest pool is more than 60 blocks from either |
| 9 | Every join open | **Met** | The shaft's column (-36,-82) is open from y12 to the sky; corridors join the hall at x -12 and each other at (22..27,-78); the shaft meets corridor 2 at z -62 and column (24,-61) is open from y12 to the sky; the x-ray reads the crypt as one void joined at both shafts |
| 10 | Things at a player's scale | **Met** | Ruin walls 1 block thick, 2 to 16 high; pillars 2 by 2, 6 high; shaft opening 3 by 3 with a curb; corridors 5 wide, 6 high |
| 11 | Ground varies in patches, undersides carry detail | **Met** | Bog paint over z -30..0; peat hags at (-44,-18), (-4,-8), (44,-9), (14,-21); heath at (-46,-108), (36,-36), (-26,-48), (20,-104); worn square (36,-66); the board's sides are banded by strata (`iso-south-east.png`) |
| 12 | A build zone shows where to build | **Not applicable** | The two sides are joined by land; there is no void to bridge |

## Where this leaves the board

The map has two monuments a side in the open, two crypts that reach the village beside them, a bog with water and stones
between the sides, and a 112 by 240 footprint. What it does not have: a village that is more than three houses and a row of
trees, an abbey that is more than made walls, and any reading of whether the monuments are seen from where an attacker
comes. Those were stated and checked by eye, not measured.

The files: `specs/exp-abbeymoor-studio/` holds `build-spec.py`, the plan, refinement, layout and intent JSON,
`provenance.json`, `exp-abbeymoor-studio.png` and `renders/` (isometric from four corners, x-ray from two, top-down,
heightmap, surface, traversability and eleven eye views); `maps/exp-abbeymoor-studio/` holds `region/`, `level.dat`,
`map.xml` and `map.png`.

---

# Revision 1 (author's review, `analysis/freeform-vs-studio/experiment/REVIEW-1.md`)

Stores 15 to 19 on the same slug; v1 renders are kept in `specs/exp-abbeymoor-studio/renders-v1/`, v2 in `renders/`.
The crypt, the monuments and the village row are untouched, so the v1 columns and the monument coordinates stand.

## Times (`date`, UTC, 2026-10-10)

| Phase | Start | End |
|---|---|---|
| Reading the review, the v1 heightmap and the spawn's surroundings | 02:06 | 02:08 |
| Grange and terrain written, stores 15 to 18 (declines cleared one at a time) | 02:08 | 02:10 |
| Bog as a basin, store 19, final world | 02:10 | 02:11 |
| Renders, reads, report | 02:11 | 02:14 |

## The review, point by point

| # | The review said | What changed, with coordinates |
|---|---|---|
| 1 | Reads like a place; the layered ruin works, the houses help | Kept as it was: the ruin (37 boxes at x -40..-12, z -96..-72), the village row (x 12..46, z -79..-72) and the crypt |
| 2 | The spawn building is somewhere and nowhere: it does not belong to a place | **The spawn longhouse (x -16..12, z -120..-100) is now the grange of the abbey.** A walled yard stands in front of its door, a garth wall two high (x -24..22, z -100..-90, material cobblestone, mossy cobblestone and stone, gate posts four high at x -5..-3 and 3..5 leaving a 6-wide gate at x -3..3), with a paved forecourt (x -4..4, z -99) and the two roads (`road-spawn`, `road-village`) leaving through the gate. A cottage stands on each side: (23..29, -113..-107) and (-45..-38, -113..-106), two plots of tilled ground (farmland) at x -55..-48, z -112..-94, and a pond at (40,-108) with its hollow, level y36, beside a knoll at (49,-97) with a tor at (50,-113). The south team's grange is the same turned 180 degrees (the pond is written twice, since the fold does not turn fluid props). Seen in `eye-grange-from-east.png`, `eye-grange-from-west.png`, `eye-grange-yard.png`, `iso-north-east.png`. The gate keeps the spawn's exit open (lesson 6): the yard is open to the road and the doorway is 4 wide |
| 3 | The terrain is a little clunky | Read as: every edge was a rectangle and every terrace ran the full width in a straight band (`renders-v1/heightmap.png`). **The relief marks are now irregular outlines and the bands are broken up:** the abbey crown is a 13-point polygon with a wobbling east cliff (`platform`, `cliff-e`, still x -4 where the corridor passes at z -83..-77); the village terrace is a 13-point outline (x -2..56, z -92..-55) with its east edge kept at x 56 for the passage rule; the two orchard terraces have wavy scarps (z -54..-51 and z -39..-37) and wavy flats; the bog is a basin (`bog-edge` polygon, z -33..-22 on its north rim) whose two ends climb to the moor (`rise-w` at (-53,-9) y26, `rise-e` at (53,-10) y25) with two hummocks at (-4,-22) and (44,-18); two shelves break the abbey hill's south flank, at (-38,-48) y36 and (-49,-36) y28; a knoll at (49,-97) y41; and the grain is stronger (amplitude 1.2 at scale 8 where it was 0.8 at 6) |

## Reads after the revision

Export gate OPEN; 60 props placed, two `DR-PASS` complaints (the two grange cottages, both placed); ground 24888 columns
walked, 1120 scrambled (4.4%), 822 barrier (3.1%, of which the yard walls and the ruin's gable are a share); 22.1% of the
ground on no journey (23.4% in v1). The crypt is unchanged and still open at both shafts: column (-36,-82) is open from y12
to the sky and column (24,-61) likewise; the x-ray reads 30 roofed voids and none sealed. The monuments stand where they
did, (-24,-69) y49..51 and (30,-62) y38..40, with walk ratios 3.96 and 3.0.

## What the studio could not do in this round

* A place is a set of things that belong together, and the studio has no unit for it: the grange is a house room style, two
  library cottages, a made-layer wall, two paint shapes, two strokes, a pond and two relief marks, each placed by hand and
  each refused or complained about on its own by a different rule (`DR-KEEP` kept the cottage out of the longhouse's side
  door cells, which run about 16 blocks out; that cost three stores).
* The spawn room is one shell per map: its look could not be changed to suit the grange; the surroundings had to carry it.
* There is no fence prop; the yard wall is a made layer of boxes.
* "Clunky" has no read. The slopes and heightmap say what is steep, not what is rectangular; I judged it from the
  heightmap contours.
