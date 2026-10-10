# Houses: pgmvox against the studio

**This report compares how the two systems build houses, so studio 2.0 can decide how to model them.** It is written from the code of both, read on 2026-10-10, and from pictures of the built worlds. Paths are relative to `pgm-studio/src/PgmStudio.Minecraft` (studio, `S:`) and `pgm-studio-mapgen/freeform/lib/pgmvox` (pgmvox, `P:`) unless they start with `freeform/`.

**What was and was not verified.** Every claim about code cites a line. Every picture was drawn by pgmvox's own renderer (`P:render.py`): pgmvox worlds were rebuilt with each board's `scripts/gen.py` into a scratch directory, and the studio worlds were read from the stored maps in `maps/*/region` through `tools/anvil.py`, so both sides are drawn by the same code. The local studio did not answer on `:7894`, so no studio code was run and the library-card preview endpoints were not used. Nothing here was checked by stamping a style in the studio.

## Short answer

**The author's read is half right.** The forms are good on both sides and the pgmvox houses do look better, but storeys are not the cause: the studio has the richer storey model (§2). The look difference comes from the data the studio houses are built from and from four stamper features pgmvox has and the studio lacks (§4).

**Four things the pgmvox houses have that the studio houses in the experiment boards do not.**

1. Clay and brick walls in colourways, with stone only as a base course. The studio builder picked stone-wall library rows, and the library holds no yellow, orange or brown clay at all.
2. A roof laid in stairs. None of the 57 seeded library houses names a roof stair, so every studio roof is cubes or half-slabs, although the stamper supports stairs.
3. A timber post every four blocks along upper-storey walls, a chimney through the roof, and real wooden doors.
4. Any heading. A house can stand at 12 degrees or 45 degrees; a studio house is axis-aligned.

**What the studio has that pgmvox lacks, and must keep.** Wings (L, T, U, cross gable, one-storey wing against a two-storey hall), per-storey styling, five window forms, porches, beams, a ladder between storeys, a validated and named library, and the wool-room contract.

## 1. What each system can build

The table states what each side can do today. "Board code" means the capability exists only as hand-written code in one board, not in the library.

| | studio (`HouseStyle` + `HouseStamper`) | pgmvox (`build.House` + `brittle`) |
|---|---|---|
| **Footprint** | One or more touching axis-aligned rectangles ("wings"), 4 blocks across at least, at most 192 cells (`S:Dressing/PlacedProp.cs:454`). L, T and U come from joined wings, checked by `HJ1`-`HJ5` (`S:Houses/WingJoints.cs:40-72`). | One rectangle, `L` by `W` (`P:build.py:354-374`). No wings. `jetty` widens upper storeys by two on the long sides (`build.py:392`). `brittle.house` stacks whole 5-block cells, each storey over part of the one below (`brittle.py:513-625`). |
| **Heading** | None. Placed props are rotated in 90-degree steps by the symmetry fan; `PlacedProp.cs` has no heading. | Any angle. `Frame(cx, cz, heading)` (`build.py:42-97`); a block belongs to a wall when its centre falls in the rectangle (`build.py:87-92`). |
| **Storeys** | A list of `Storey`: own clear height (3 minimum), wall stack, post, windows, deck and zoning (`S:Houses/HouseStyle.cs:176-226`). A wing may stand fewer storeys than the hall (`StoreysHigh`, `BuildingPlan.cs:85-87`). | `storeys` count and one `storey` pitch, default 4, for all (`build.py:366-368`). Ground storey and upper storeys each take a list of wall blocks (`build.py:330-342`). |
| **Setbacks, overhangs, jetties** | Setback only by dropping a whole wing (`BuildingPlan.At(level)`, `BuildingPlan.cs:228-250`). Beams: log ends one block past each corner at every storey seam (`HouseStamper.cs:506-525`). No jetty. | Jetty: upper storeys one block wider each side, joists under them (`build.py:439-441`). `brittle.house`: each storey smaller than the one below and thrown eaves round every plate (`brittle.py:595-611`). |
| **Walls** | Course stacks (`RoomPart`, bands, "repeat" the last band) of any of 13 material kinds: solid, noise, cell, voronoi, checker, log checker, laid log, wall run, wall diagonal, wall frame, team tint (`S:Painting/TerrainTheme.cs:128-141`). Corner post per storey. | A list of blocks; each wall block picks one at random (`build.py:395-437`). Corner posts; on upper storeys also a post every 4 blocks on the long walls (`build.py:426-427`). No inset patterns on houses (`facade.py` insets exist for masses, `facade.py:197-226`). |
| **Base course** | A band at the bottom of the stack, or a `foundation.plate` below the floor (`HouseStyle.cs:242-262`). Many seeded rows have one. | The ground storey and the floor ring take `ground[0]` at floor level (`build.py:410`); the boards add a stone foot course afterwards (`dress.py:131-135`). |
| **Openings** | Window forms: pane, stair lattice, slab band, arched, open; sill, width, height, spacing; optional host block; gable windows (`S:Houses/HouseWindows.cs:9-50`, `Seats` at `:300`). Door: width, height, arched head; the leaf is air, web, stained glass or glass pane only (`S:Domain/DoorMaterials.cs:46-49`). | One flush window rhythm: one pane per 3 blocks, one high on the ground storey, two high above (`build.py:345-351`). A wooden door in the middle of the long wall, a block of wall kept either side (`build.py:443-458`). |
| **Roofs** | Six forms: gable, flat, hip, gambrel, shed, saltbox (`HouseStyle.cs:12-36`). Cross gable and valley from wings, "marching" or "projecting" (`HouseStamper.cs:279-302`). Overhang, ridge cap, verge, wear, roof in cubes, half-slabs or stairs. | The same six forms: `RoofField` is a port, tested against 34,500 answers from the studio's class (`build.py:8-14`, `README.md:385-389`). No wings, so no cross gable. Stairs when square to the board, cubes and slabs when turned (`build.py:462-471`). |
| **Dormers, mansard** | None (grep of both trees). | None. |
| **Interiors** | Floor zoning (border, field, inlay), a deck per storey, one ladder shaft through every slab (`HouseStamper.cs:450-492`). No furniture. | A floor course per storey (`build.py:420-421`). No stairs or ladder inside `house()`; `ladder()` and `stairs()` are separate helpers (`build.py:529-546`). Furnishing is board code (`freeform/opus55-freeform-riftwater/scripts/house.py:236-288`). |
| **Chimney** | None. | A cobble or brick stack through the roof, on by default (`build.py:476-481`). |
| **Towers, rooms** | Wool rooms and spawns are the same stamper: `HouseStamper.Stamp` with a frame (`S:Stamping/WoolStructureStamper.cs:63`, `SpawnStructureStamper.cs:59`). Defaults are flat bedrock shells (`HouseStyle.cs:611-645`). | Wool rooms are `brittle.house` (stepped tiers) or board code. Towers: `brittle.tower` (`brittle.py:490-510`) or hand-written (Hoarfrost, §3). |
| **How a style is chosen** | Data. A `HouseStyle` JSON row in the library (57 seeded in `S:Library/houses/*.json`), bound by name in the dressing document: `{"library": "spruce-roofed-stone-cottage", "kind": "house"}`. Rows are named and validated (`HS1`-`HS21`). | Code. Four presets in `build.STYLES` (`build.py:327-342`), and each board writes its own dict (`clay_style(walls)` in `freeform/lib/boards/exp-abbeymoor-pgmvox/scripts/dress.py:148-152`). |

**The pgmvox version in the repository is 0.21.0**, not 0.20.0 (`P:__init__.py`, `VERSION`). The block of wall either side of every door is in `build.py:453-458` and was in 0.20.0 as the brief says.

**Correction to the brief on roofs.** pgmvox is missing no roof form the studio has. Its six forms are the studio's six, held to the studio's formulas by a test. What it lacks is *wings*, and a cross gable is what two wings make.

## 2. Storeys, in depth

**Both systems build a storey the same way: three or more courses of wall, a laid-log course at the head, the next floor in that same course, and the roof on the last course.** The author's suspicion that storeys are the difference does not survive the code. Where they differ, the studio is the more capable.

**Height.** A pgmvox storey is a fixed pitch for the whole house, default 4: three of wall and "the laid course at its head" (`build.py:367-368`). The eave is `floor + storeys * pitch` (`build.py:390-403`). A studio storey states its *clear*, the air a player stands in, three at least; it spends one more course on the slab when something stands over it, and none when it is the top (`HouseStyle.cs:223-225`). So a three-storey studio house can be 5, 4 and 3 clear (the inline style in `specs/opus5-burgage-terrace/build-spec.py:223`), where pgmvox cannot vary.

**Wall.** pgmvox picks the wall block at random from one list for the ground storey and one for all upper storeys (`build.py:416, 437`). The studio gives each storey its own course stack, corner post and windows, and falls back to the building's where a storey says nothing (`HouseStyle.cs:482-496`).

**Floor.** Both lay the floor of storey *n* in the head course of storey *n-1*, across the interior only (pgmvox `build.py:420-421`; studio `HouseStamper.cs:474-481`, "the perimeter is wall"). The studio adds a zoned surface and a ladder hole at one cell through every slab, so no upper storey is sealed (`HouseStamper.cs:483-488`). pgmvox leaves the way up to the board.

**Transition.** The studio lays beams: log ends one block past each corner at each seam (`HouseStamper.cs:506-525`). pgmvox jetties the upper storey out one block on the long sides, with joists showing under it (`build.py:439-441`), but no experiment board used it; Hollowcrown's three demo houses did (`freeform/opus55-freeform-hollowcrown/scripts/buildings.py:421-423`). `brittle.house` is the only place storeys step back and throw eaves (`brittle.py:513-611`), and the Brittlebush wool houses are built that way (picture `pgmvox-11`).

**Roof base.** Both seat the roof on the course over the top wall: pgmvox at `eave + 1` (`build.py:464`), the studio at `floorY + WallCourses + 1` (`HouseStamper.cs:239-247`). One real difference: pgmvox lays the head log course on the **top** storey too, so a two-storey house has 3 clear plus a log plate under the roof. The studio's top storey has no extra course (`HouseStyle.cs:225`), so the log plate has to be paid for out of the clear height.

**One studio quirk, visible in a picture.** A band stack "repeat" carries the last band on (`S:Painting/BandStack.cs:60-72`), it does not cycle. A non-top storey with clear 4 whose stack is three planks and one log (the shape most seeded rows have) reaches its fifth course, the slab, and repeats the log. The seam is then two courses of log. The minehead's column shows it: y30 and y31 are both spruce log (`img/studio-04-slatefold-minehead.png`, right half, the thick band under the upper floor). Whether that is wanted is the author's call; pgmvox's seam is one course.

| course | pgmvox Cottage B (2 storeys, floor y70) | studio minehead (library `stone-timber-minehead`, floor y21) |
|---|---|---|
| plate | yellow clay (floor ring) | spruce planks (foundation plate) |
| storey 0 wall | stone foot (cobble, andesite, stone brick), yellow/orange clay, clay | stone brick, stone brick, andesite, andesite |
| seam | spruce log, laid along the wall | spruce log, 1 course |
| storey 1 wall | clay x3 (spruce post every 4th block) | planks, window, planks, log |
| seam / eave | spruce log (eave), roof on top | spruce log x2 (see above), then storey 2 |
| roof | stone-brick **stairs** | nether brick **cubes** |

The columns come from `/tmp` scratch reads of the built worlds (`col.py`); the pgmvox side is `freeform/lib/boards/exp-slatefold-pgmvox` rebuilt, the studio side `maps/exp-slatefold-studio`.

## 3. The singled-out structures

### Hoarfrost Reach: the Lighthouse (tower wool room)

**It is hand-written board code, not pgmvox's house model.** `gen.lighthouse()` (`freeform/lib/trials/sonnet/hoarfrost-reach/scripts/gen.py:219-282`) loops over a 9 by 9 box (`plan.py:84`) and sets blocks directly. Only the Skald's Hall and the two sheds go through `BLD.house` (`gen.py:149-158`; `plan.py:138-150`).

**How it is made, in order.**

1. A stone-brick plinth four courses down, then the shaft: edge cells of red clay (data 14) and white clay (data 0) in bands four courses high, `stripe = (t // 4) % 2 == 0` (`gen.py:235-236`); stone-brick corners (`gen.py:237-238`); iron bars every sixth course on alternate cells, `t % 6 == 3 and (x + z) % 2 == 0` (`gen.py:239-240`).
2. A floor of spruce planks across the interior every fifth course, with a hatch of air over the ladder in each (`gen.py:249-253`), and a ladder up the south wall (`gen.py:254-256`).
3. Above the room floor (`ROOM_Y 94`, `plan.py:87`), five courses of stained glass (data 3) with stone-brick corners (`gen.py:242-243`).
4. A quartz lid with a slab rim (`gen.py:259-262`), a glass and sea-lantern column (`gen.py:263-270`), and a gallery of slabs with iron-bar rail at the room floor, one block outside the walls (`gen.py:271-274`).
5. A spruce door on the east face (`gen.py:277-278`), a quartz pedestal for the wool, and the studio's wool-room chests in the four inner corners (`gen.py:282`, `props.wool_chests`).
6. Blue's tower is not built: the whole red half is mirrored and the red clay recoloured to blue clay (`gen.py:394`).

**Could the studio express it today?** Mostly, not entirely, and this is unverified by stamping. The 9 by 9 footprint, the stacked storeys, the ladder shaft, the corner posts and the wool-room chests are all studio features. Red and white bands are explicit bands in a storey stack (a stack does not cycle, so each repeat is written out). What the studio cannot say: the spruce door (a wool-room door is air, web or glass, `DoorMaterials.cs:46-49`), the gallery one block outside the walls (a style writes nothing outside footprint plus overhang, `HouseStamper.cs:21-24`), the lantern column above the roof, hatches at chosen floors (the shaft is one cell, `HouseStamper.cs:457-460`), and bars on alternate cells only (a wall run would need to line up with the arc).

### The grammar boards (Brittlebush III, Sandreach, Claywork, Brittle Study, Brittlebush KOTH)

**The grammar does not build houses; it builds ground.** `grammar.py` states sections, faces and fills over surfaces (`grammar.py:1-26`). The wool houses on these boards are `brittle.house` (`brittle.py:513-625`) and `brittle.tower` (`brittle.py:490-510`): storeys of whole 5-cell blocks, each storey over part of the one below (an L of three cells over a block of four, one cell on top).

**How a `brittle.house` wall is made.** Read bottom up, a wall cell is black clay, an upside-down dark-oak stair, a dark-oak stair, brick (`brittle.py:558-569`); every other cell along a face is a birch-stair panel framed in black clay (`brittle.py:556-566`), with the team's wool tucked under the eave (`brittle.py:570-573`). Each plate overhangs one block in eaves of planks, slab and upside-down stairs (`brittle.py:595-611`); a plate nothing stands on becomes a terrace of sand in a ring of spruce stairs over a sandstone ceiling lit by sea lanterns (`brittle.py:580-594`); a one-cell top storey holds a beacon (`brittle.py:612-625`). Brittlebush III calls it as `house(w, P.WOOL_LAYERS, ...)` (`freeform/lib/boards/brittlebush-iii/scripts/gen.py:50`).

**Claywork's Kilns are a third thing:** hand-written `kiln()` and `hipped()` in the board's `gen.py` (`freeform/lib/boards/claywork/scripts/gen.py:216-281`), a hipped roof of brick stairs written without `RoofField`.

**Could the studio express it?** Not today. Stepped storeys with eaves, birch-stair panels and the terrace roof need a setback and eave per storey and a panel course material; none exists. The ground the houses stand on (five-course cap, bays) is also outside `HouseStyle`.

**Loomfall** is a fourth hand-written case: a 17-line `house()` makes flat-roofed sandstone boxes with a parapet (`freeform/opus55-freeform-loomfall/scripts/gen.py:66-81`).

### Riftwater (DTM) and the two experiment boards

**Riftwater's houses are not pgmvox either.** They are `house.py` in the board (`freeform/opus55-freeform-riftwater/scripts/house.py:1-288`): fixed 4-course storeys, a brick base course and white-clay infill under a spruce frame, spruce posts at the corners and, on upper storeys of the town style, every 4 blocks (`house.py:156-162`), a laid-log seam each storey (`house.py:147-154`), a dark-oak stair roof with a slab ridge (`house.py:83-86`, `roof_gable`), a chimney, and a furnished inside (`furnish`, `house.py:236-288`). The "tall house with a low wing" is two `house()` calls, the second a separate box with its own roof (`freeform/opus55-freeform-riftwater/scripts/buildings.py:239-241`); there is no valley and the two interiors are sealed from each other (`pgmvox-07`). `pgmvox.build.House` descends from the Hollowcrown version of this module (`freeform/opus55-freeform-hollowcrown/scripts/house.py`: same four style names, same `frame_line` post rule).

**Abbeymoor and Slatefold (pgmvox) use `build.House` with a colourway dict.** `clay_style(walls)` sets `ground=walls, upper=walls`, spruce posts, a gable in the wall's first block and a roof by board (`exp-abbeymoor-pgmvox/scripts/dress.py:148-152`). The colourways are lists whose repetition is the weight: `OCHRE = [yellow, yellow, orange]`, `BRICK_RED = [brick, brick, brick, red clay]` (`dress.py:154-166`). The board then replaces the first wall course with stone, `rebase()` (`dress.py:131-135`), and clears windows from the middle of the door wall (`dress.py:100-107`, Slatefold). The author's own review of the first round asked for exactly this: clay walls, stone as the base course (`analysis/freeform-vs-studio/experiment/REVIEW-1.md`, points 1 and 4).

**The studio boards use five library rows by name.** `exp-abbeymoor-studio` binds `spruce-roofed-stone-cottage`, `dark-oak-roofed-stone-cottage`, `rubble-and-spruce-house`, `stone-and-spruce-barn` and `spruce-roofed-stone-longhouse` (`specs/exp-abbeymoor-studio/build-spec.py:372-376`); every house is one wing (`build-spec.py:380-383`). Slatefold's wool rooms bind the room style `brick-townhouse` (`specs/exp-slatefold-studio/build-spec.py:354`), which is the studio's best result here: banded brick and stone, per-storey window rows (`img/studio-05-slatefold-kiln-wool-room.png`).

**Could pgmvox's Abbeymoor and Slatefold houses be expressed in the studio today?** Nearly all of it. The colourway is a `cell` or `noise` material over clay stops, the foot course a first band, the posts `post`, the stair roof `roof.stair`, the gable `roof.gable`. What is missing is the mid-wall posts, the chimney, the wooden door and the heading (§5).

**Studio houses that already look good.** The burgage-terrace row houses are written inline: a brick-and-clay shop of 5 clear, a timber solar of 4 with a laid-log seam, an attic of 3, beams on (`specs/opus5-burgage-terrace/build-spec.py:195-224`). Plot C is an L of two wings and shows the cross gable the studio can make (`img/studio-08-burgage-plot-c-L-wing.png`).

## 4. Why the pgmvox houses read better

Each cause below is a checkable fact. They are ordered by how much of the look they plausibly carry; the ranking is a judgement, not a measurement.

**1. The studio builder chose stone-wall rows, and the library has few alternatives in the colours pgmvox used.** Ten of the 57 seeded rows have stone on every storey (`andesite-gabled-house`, `banded-stone-house`, `dark-oak-roofed-stone-cottage`, `spruce-roofed-stone-cottage` and six more); two of them are in the studio boards, and three more rows the boards bind are mostly stone (`spruce-roofed-stone-longhouse`: three courses of cobble and a stone checker, three of planks). Twelve rows have clay in a wall, in six colours: black, white, light grey, light blue, red and terracotta. No row has yellow, orange or brown clay, which are the colours the pgmvox boards used (`dress.py:154-166`: OCHRE, UMBER). The pictures show it: `studio-02` and `studio-06` are grey walls under a brown roof, `pgmvox-04` and `pgmvox-06` are warm clay under a grey one. This is library data, not a stamper limit.

**2. The pgmvox roof is stairs, the studio's is cubes.** `lay_roof` puts a stair on every slope column when the house is square to the board (`build.py:275-323`, called with `st["stair"]` at `build.py:470`). The studio stamper does the same when `roof.stair` is set (`HouseStamper.cs:564, 624-637`), but **none of the 57 seeded rows sets it** (counted from `Library/houses/*.json`: `stair >= 0` in 0 rows, `slab >= 0` in 17). Counting blocks in the built houses: pgmvox Thorn Cottage 88 stairs, a Slatefold cottage pair 106; the studio longhouse and kiln room 10 each, which are window lattices. A cube roof reads as a staircase of whole blocks; the stair roof reads as a smooth slope. Library data again.

**3. A timber post every four blocks.** On upper storeys of a long wall pgmvox adds a log post at `abs(((run + 1.5) % 4) - 2) < 0.5` (`build.py:426-427`), which is what makes a framed storey read as framed. The studio has corner posts only (`HouseStamper.cs:327-328`). A wall run could draw stripes, but its arc starts wherever the plan's outline starts, so alignment with the corners is not guaranteed (not verified).

**4. A chimney, and a wooden door.** Every pgmvox house gets a stack through the roof by default (`build.py:476-481`) and a spruce or dark-oak door (`build.py:449-450`). The studio has neither: no chimney exists in its source or docs, and the door leaf is air or glass because the wool-room block filter whitelists it (`DoorMaterials.cs:46-53`). A house with a chimney and a door reads as lived in from across a board.

**5. Per-house variation and angle.** Abbeymoor has eleven houses in five colourways, one turned 12 degrees and one 90 (`exp-abbeymoor-pgmvox/scripts/plan.py:98-111`). The studio boards place five identical rows with one wing each, all axis-aligned. Variation is cheap in code and costs a row each in the studio.

**6. Material mix at block level.** pgmvox picks a wall block independently per block from a short list (`build.py:395-437`), which makes plaster. The seeded rows use `noise` with scale 3 over cobble and andesite (e.g. `rubble-and-spruce-house`), which makes grey patches three blocks across. A `cell` material over clay stops could do the pgmvox mix (not verified at cell size 1).

**What does not explain it.** Storeys (§2). Window design: the studio's forms are richer; the lattice is a diamond of open air and the pane form is the same as pgmvox's. The base course: seeded rows already have one. Roof overhang: both are 1.

## 5. Mapping pgmvox's house model onto the studio's JSON

**The shape to extend is `HouseStyle`, serialised by `HouseStyleJson`** (`S:Houses/HouseStyleJson.cs`), and for placement the `HouseProp` in the dressing document. The table says, per pgmvox concept, the existing field or the new one.

| pgmvox concept | studio field today | new field? |
|---|---|---|
| `ground` / `upper` weighted block list (`build.py:416`) | `wall` or `storeys[i].wall` stack with a `cell` / `noise` material over stops; weights by repeating a stop | Maybe a `scatter` material (per-block, weighted) if `cell` size 1 does not hold |
| `post` log species | `post` / `storeys[i].post` | No |
| corner posts only | the same | No |
| mid-wall posts every 4 blocks, upper storeys, long walls (`build.py:426-427`) | none | **`storeys[i].bays`** |
| head log course on every storey (`build.py:432-433`) | a last band `laidLog`; only non-top storeys have the slab course | **`storeys[i].head`**: a ring course over the clear on every storey, the top included |
| `storey` pitch 4, shared | `storeys[i].clear` | No |
| `jetty` (`build.py:392, 439-441`) | `beams` is corner log ends only | **`storeys[i].jetty`** |
| `brittle.house` setback and eaves per storey | `wings[].spec.storeysHigh` drops whole wings | **`storeys[i].setback`, `storeys[i].eave`** |
| `floor` | `foundation.plate`, `storeys[i].deck` | No |
| `windows(period, rows, margin)` | `windows` (`form: pane`, `width: 1`, `height: 1` or `2`, `spacing: 2`) per storey | No |
| a block of wall each side of a door | `MeetsDoor` (`HouseWindows.cs:388`) | No |
| `door` block (spruce, dark oak) | `doorway.door` enum | **wood leaf values**, refused for wool-room styles |
| `roof` form, `pitch`, `overhang` | `roof.form`, `roof.pitch`, `roof.overhang` | No |
| roof `stair`, `slab` | `roof.stair`, `roof.slab` | No (set them in the rows) |
| `gable` | `roof.gable` | No |
| `chimney`, `chimney_cap` (`build.py:476-481`) | none | **`chimney`** |
| `heading` | none; props are axis-aligned | **`heading` on the prop** |
| base foot course (`rebase`) | first band of the wall stack | No |
| wings | `wings[]` with `spec` | pgmvox gains it from the studio |

**A proposed fragment**, extending the current shape. New fields are marked in comments; everything else is the current schema. It describes a two-storey ochre cottage.

```json
{
  "foundation": { "plate": { "stack": { "bands": [{ "material": { "kind": "solid", "id": 5, "data": 1 }, "thickness": 1 }], "ending": "repeat" }, "extent": 1 } },
  "roof": {
    "form": "gable", "pitch": 1, "overhang": 1,
    "stair": 109, "slab": -1,
    "body": { "kind": "solid", "id": 98, "data": 0 },
    "verge": { "kind": "solid", "id": 98, "data": 0 },
    "gable": { "kind": "solid", "id": 159, "data": 4 }
  },
  "post": { "kind": "solid", "id": 17, "data": 1 },
  "storeys": [
    {
      "clear": 3,
      "wall": { "stack": { "bands": [
        { "material": { "kind": "noise", "seed": 3, "scale": 2, "octaves": 1,
          "stops": [ { "kind": "solid", "id": 4, "data": 0 }, { "kind": "solid", "id": 1, "data": 5 }, { "kind": "solid", "id": 98, "data": 0 } ] }, "thickness": 1 },
        { "material": { "kind": "cell", "seed": 11, "cellSize": 1, "jitter": 0, "warp": 0,
          "palette": [ { "kind": "solid", "id": 159, "data": 4 }, { "kind": "solid", "id": 159, "data": 4 }, { "kind": "solid", "id": 159, "data": 1 } ] }, "thickness": 2 }
      ], "ending": "repeat" }, "extent": 3 },
      "windows": { "form": "pane", "block": 102, "width": 1, "height": 1, "sill": 2, "spacing": 2 },
      "head": { "kind": "laidLog", "id": 17, "data": 1 }                      // new
    },
    {
      "clear": 3,
      "wall": { "stack": { "bands": [
        { "material": { "kind": "cell", "seed": 11, "cellSize": 1, "jitter": 0, "warp": 0,
          "palette": [ { "kind": "solid", "id": 159, "data": 4 }, { "kind": "solid", "id": 159, "data": 4 }, { "kind": "solid", "id": 159, "data": 1 } ] }, "thickness": 3 }
      ], "ending": "repeat" }, "extent": 3 },
      "windows": { "form": "pane", "block": 102, "width": 1, "height": 2, "sill": 2, "spacing": 2 },
      "bays": { "period": 4, "post": { "kind": "solid", "id": 17, "data": 1 }, "walls": "long" },   // new
      "head": { "kind": "laidLog", "id": 17, "data": 1 },                                            // new
      "jetty": { "reach": 1, "joists": { "kind": "laidLog", "id": 17, "data": 1 } }                   // new, optional
    }
  ],
  "chimney": { "body": { "kind": "solid", "id": 4, "data": 0 }, "cap": { "kind": "solid", "id": 139, "data": 0 }, "at": "rear", "above": 2 },   // new
  "beams": { "block": -1, "data": 0, "reach": 1 },
  "doorway": { "door": "spruceDoor", "width": 1, "height": 2 }                                        // new value; refused on a wool or spawn room style
}
```

The placed prop gains one field beside `wings`:

```json
{ "id": "mill-cottage", "kind": "house", "style": "ochre-cottage", "heading": 12,
  "wings": [ { "corners": [[36, -91], [44, -85]], "spec": {} } ] }
```

**Three notes on the fragment.** First, the numbers are 1.8 ids (`109` stone-brick stairs, `159` stained clay, `17` log); the `cell` palette repeats a stop for weight, as pgmvox repeats a block in its list. Second, the `//` comments are annotation, not JSON; the fragment is not run against the API (the local studio was down). Third, `head` makes pgmvox's one-course seam and its plate under the roof expressible, and also removes the double-log seam of §2, because the slab course would stop depending on the last band repeating.

**What a heading costs.** `Frame` and the framed `RoofField` are already written and tested against the studio (`build.py:42-97, 131-137`); the studio's stamper is built on rectangles and a ring of walls (`BuildingPlan`, `HouseStamper.Stamp`), so a heading means a second stamper path, not a field. Turned roofs drop to cubes and slabs because a stair faces four ways only (`build.py:462-471`).

**What the studio has that pgmvox lacks, and must keep.**

- **Wings.** Joints (`HJ1`-`HJ5`), marching and projecting roofs, `storeysHigh`, a ridge axis per wing (`BuildingPlan.cs:85-87`, `HouseStamper.cs:279-302`).
- **Window forms:** stair lattice, slab band, arched, open, and gable windows; the arched door head.
- **Porch** taken out of the footprint (`HouseStyle.cs:97-127`), and **beams**.
- **Per-storey wall, post, windows and deck**, and floor zoning.
- **The ladder shaft** so no storey is sealed.
- **The wool-room contract:** the door leaf whitelist, the team-tinted band, the frame's entries, the room kinds that share the stamper (`WoolStructureStamper.cs:63`).
- **The material system, the library, naming and validation** (`HS1`-`HS21`, `HouseNames`), round-tripped JSON with an upgrade path (`HouseStyleJson.Upgrade`).
- **Mirror and rotation by 90 degrees** with handedness, so a fan of a house is its mirror cell for cell (`HouseStamper.cs:122-124`).

## 6. Gaps on each side, ranked by effect on how a map looks

**Studio gaps, largest first.**

1. **No warm clay colourways, and too many stone-only rows.** Data; one afternoon of rows. Largest single effect on the "stone on stone" read.
2. **No stair roof in any seeded row.** Data; set `roof.stair` on the rows. The stamper is ready.
3. **No mid-wall timber bays.** A new storey field (`bays`).
4. **No chimney.** A new style field; changes a roof's silhouette.
5. **No wooden door on placed houses.** A new `DoorMaterial` value, limited to prop houses.
6. **No heading.** A second stamper path; high cost, and mostly valuable for hamlets that should not stand in a row (the author's review of Slatefold: "houses near the spawn stand all in one line").
7. **No jetty, setback or storey eave.** Gives the Brittlebush-style tiered tower and the half-timbered overhang.
8. **No furnishing.** Neither side has it in the library; Riftwater did it in board code.

**pgmvox gaps, largest first.**

1. **No wings.** The silhouette gap: every house is a box with one ridge, and a cross gable cannot be said. Boards fake it with two `house()` calls (`pgmvox-07`).
2. **No per-storey style, no per-storey height.** One pitch, one upper mix.
3. **No window forms beyond one pane rhythm, no gable windows.**
4. **No stair or ladder between storeys in `house()`.** An upper floor is sealed until the board adds a ladder.
5. **No porch, beams, or arched door head.**
6. **Hand-written copies.** Hoarfrost's tower, Claywork's Kilns, Loomfall's boxes and Riftwater's houses each re-implement a house; the library covers the plain rectangle only.
7. **No validation, no names, no preview** of a style until the world is built.

**Where the two meet.** The studio's model is the larger, and the cheapest route to the pgmvox look is data (gaps 1 and 2) plus three small fields (`bays`, `chimney`, a wood door). Heading and stepped tiers are the two items that need new stamper code.

## Pictures

Each panel is an isometric view (left) and a straight-on elevation of the door side (right), drawn by the same renderer. Windows of panes read as sky in the elevation. Files are in `img/`.

- Sheets: `sheet-pgmvox-houses.png`, `sheet-studio-houses.png`.
- pgmvox: `pgmvox-01-abbeymoor-thorn-cottage`, `-02-abbeymoor-mill-cottage-12deg`, `-03-abbeymoor-moorcock-inn`, `-04-slatefold-cottage-b-2storey`, `-05-slatefold-chapel`, `-06-slatefold-kiln-wool-room`, `-07-riftwater-village-house-with-low-wing`, `-09-hoarfrost-lighthouse-wool-room`, `-10-hoarfrost-skald-hall`, `-11-brittlebush-iii-wool-house`, `-12-riftwater-shop-3storey`.
- studio: `studio-01-abbeymoor-farm-longhouse`, `-02-abbeymoor-cottage-a`, `-03-abbeymoor-cottage-b`, `-04-slatefold-minehead`, `-05-slatefold-kiln-wool-room`, `-06-slatefold-cottage`, `-07-burgage-plot-a-3storey`, `-08-burgage-plot-c-L-wing`, `-09-saltwharf-warehouse-L`.

**Not done.** Sandreach and Brittle Study houses were not rendered separately; they use the same `brittle.house` as Brittlebush III. `exp-abbeymoor-studio` and `exp-slatefold-studio` were read from their stored maps, not rebuilt.
