# Slatefold — the plan

Capture the wool, two teams of twelve, two wools a team. Built on pgmvox 0.19.0 by Sonnet 5.5 for the pgmvox side of the
studio-versus-pgmvox experiment (`analysis/freeform-vs-studio/experiment/BRIEFS.md`, brief 1). `scripts/plan.py` is the plan,
`plan_check.py` measures it, `sketch.py` draws it (`renders/00-plan-sketch.png`); the generator reads `plan.py` and decides nothing it states.

## 1. The identity

**A slate-quarrying hamlet climbs two terraced hills that face each other across 28 blocks of void; each team defends a red
brick kiln down on the quarry floor and an engine house on a high bench, and the middle is crossed by building.**
What a player remembers: the grey stepped hill, the brick kiln with its chimney in the quarry, the winding gear on the skyline.

## 2. The arrangement

Red holds the north (z < 0), blue is red's mirror, z' = -1 - z. The board is 168 by 216 blocks; the spawns stand 186 apart
(z -93 and 92). Each hill steps down toward the band in four terraces, each four blocks below the one behind it, and every
flight is three stair blocks, four blocks of climb.

| Piece (kind) | Floor y | What it is, and why a player goes there |
|---|---|---|
| Quarry Office terrace (spawn) | 74 | The spawn at (0, 93), the two monuments at (±15, 86), the spawn iron, the Quarry Office; three flights down, at x -29, -3 and 8 |
| Terrace Row (row) | 70 | Three slate cottages and the Chapel; the street; the head of the Winding Path at its west end |
| Cart Yard (yard) | 66 | Spoil heaps, the weighbridge, the cart track; the head of the Cart Gantry at its east end |
| Dressing Floor (front) | 62 | The front line: two open sheds, twelve stacks of cut slate as cover, the lip to the band |
| Cart Gantry (landing + 2 flights) | 62 | From the yard east, down two flights and a long landing to the Quarry Floor; **a bedrock wall across the landing**, x 28 to 29 |
| Quarry Floor (quarry) and the Pit | 58 / 54 | An island east of the hill: derrick, slate stacks, beehive ovens, the Pit with a flight in on two sides |
| **The Kiln** (wool room 1) | 58 | A red brick house, 12 by 13, east end of the Quarry Floor, three faces on the void, door on the west, chimney to y 78 |
| Winding Path (flights a, b, c; landings 74 and 78) | 70 to 82 | Row, flight, first landing, flight, second landing with **a bedrock wall across it**, flight, bench |
| High Bench (bench) | 82 | A ledge out to the north-west, void on three faces |
| **The Winding House** (wool room 2) | 82 | An engine house of stone brick, 10 by 11, door on the east, with its headframe to y 98 on the skyline |
| The band (zones) | void | 28 across, z -13 to 12, with a bay either side of the front (x -72 to -53 and 41 to 60, z -40 to -14) |

The two wool rooms are 138 apart. Each team's other half is walked the same way: the kiln beyond the gantry, the winding house beyond the path.

## 3. The numbers, each with its target

| Number | Target | Plan | Why |
|---|---|---|---|
| Spawn to the band's edge | SP10: at least 55 | 80 | the front is far from the spawn |
| Spawn to the Kiln / the Winding House (over the wall) | comparable, ratio at most 1.25 (WL9) | 88 / 95, ratio 1.08 | a defender gets to either in about the same time |
| Band edge to each room | WL10e: at least 59 | 87 / 100 | the wools are deep |
| Room to room, straight | WL7: 46 to 143 | 138 | the rotation runs past the spawn |
| Blue against red, same walks | equal | 88.1 = 88.1, 94.8 = 94.8 | the mirror |
| Band, front line to front line | 20 to 30 | 28 | the corpus band |
| Tallest climb in any flight | at most 4 (lesson 5) | 4 | |
| Walked only, no building | no room reached | not reached | the walls stop it |
| Walked with every running jump | no room reached | not reached | no jump skips a wall |
| Landmarks seen from the monuments' lawn | both | both | lesson 1 |
| Each gap between pieces that do not touch | none a jump can clear onto the Quarry or the path | none | the jump check, 9.5 blocks, drops counted |

## 4. The look, decided now

Biome taiga (a cold green grass and leaf beside grey slate). Three tone families: **ground** grey slate (stone, andesite, polished andesite,
in cells of three) with grass and podzol on the benches; **built** red brick for the kilns and ovens, stone brick and cobble with spruce posts for the
houses, spruce planks for the gantry; **accent** the wool colours on banners and the monuments' glass. Rock is bedded andesite and stone with flecks of coal ore,
cracked brick and cobble; faces between terraces are stone-brick retaining walls, faces to the void are bedded rock with ledges and moss.

## 5. What the build adds that the plan does not show

Rails (spruce fence) along every open edge of a landing and every stair side with a drop; lamps at lane ends and along the front lip (a row of them: where
the bridge begins); signs on the lip ("BUILD HERE"); the build area's block 36 at y 0 and its redstone outline at y 1; a mist of grey glass at y 20 to 25
beneath the hill and not over the zones; knolls of turf, 2 to 3 high, on the lawns off the lanes; spruces in nine chosen places, none on a lane, a flight or a
doorstep. Each is a plan-time decision and not a surprise: none stands where a route runs.

## 6. The self-review, before the build, against the brief and the twelve lessons

Read against the first sketch (`renders/00-plan-sketch.png`, version 1). What it found, and what changed.

| # | Finding | Change |
|---|---|---|
| Brief | Two wools each (kiln by the quarry floor, engine house on a high bench with its own path) yes; spawn on the upper terrace yes; at least five places a side, ten named; size 186 between spawns, inside 150 to 220. The hill's outlines are boxes: terraces read as stacked rectangles | Chamfered corners on the spawn terrace and the front, an island quarry, knolls on the lawns, ragged rock under the rims in the build |
| 1 | The monuments are on the spawn lawn in the open. Neither wool is only underground or at the top of a tower: both are ground-floor rooms. But a room is a house with a door: a stranger has to know which house | A banner of the wool's colour and a sign over each door; the kiln's chimney and the headframe stand above the skyline (the check sees both from the lawn) |
| 2 | Wools and monuments are the library's `Wool`: a wool block, a bedrock pedestal, dyed glass over it | none needed |
| 3 | Wool rooms and walls need the studio's loot | `props.wool_chests` in each room's four inner corners (eight chests a room), `props.defence_chests` in the front face of each wall, two apart so they do not make a double chest |
| 4 | Vegetation | Trees only in places named in `dress.trees_`; none on the Winding Path's landings (one was drawn there and is removed) |
| 5 | Every flight is three stairs; sides over void or a lower terrace need a rail | `gen.flights` lays a cobble wall on every stair side with a drop of one or more; the check prints the tallest climb |
| 6 | The spawn's exit: three flights and a clear lane; nothing walked round | the Office stands behind the spawn, not in front of it |
| 7 | Platforms: each plan floor has a bedrock course six under it, skipped on the rim, and a root | `gen.islands` |
| 8 | No ladders; no water | none |
| 9 | Joins: every flight meets a landing of its own width | the walk read-back reaches every cell of the row, the yard and the front |
| 10 | Scale | houses 8 by 6, the kiln 12 by 13, walls two thick |
| 11 | Ground in patches: lawn, slate flags, podzol and coarse dirt as shapes (the `PATCHES` list), not a field of noise; faces carry strata, cracked brick and moss | `dress.surface`, `gen.retaining_walls`, `forms.skirt` |
| 12 | The build zone must show where to build | `dress.marks`: the studio's redstone outline, signs on the lip, a row of lamps along it; the mist is cut away over the zones so the outline can be seen from above |

## 7. Versions

`plan.py` v1 only; the plan did not change between the sketch and the build (the geometry was corrected by the read-back, see REPORT.md: the wall
moved from x 25 to x 28 once the walk showed the wall's top within a jump of the stair's rail).

## 8. Revision 1: the author's first review

Source: `analysis/freeform-vs-studio/experiment/REVIEW-1.md`, "Slatefold, pgmvox". The v1 renders are kept in `renders-v1/`. Built the same way
(`python3 -m pgmvox.run boards/exp-slatefold-pgmvox --build <dir>`); the plan check, the walks (218 and 257 moves to the enemy's rooms by building,
none on foot or by any running jump), the footing, water, chest and bedrock read-backs and the studio reader all pass as before.

| # | Review point | What changed |
|---|---|---|
| 1 | Stone roofs over stone infill read badly; the clay-walled wool room is the good house | The Kiln's idea is the board's house: `dress.clay_style`, clay or brick walls in a spruce frame under a stone-brick roof, with a stone course at the foot (`dress.rebase`). Four palettes: red brick (cottage A), ochre (cottage B and the weighbridge), lime-wash (cottage D and the chapel), terracotta (the Quarry Office), umber (the Winding House, whose iron-bar windows stay). The Kiln keeps its brick. The old slate style is gone |
| 2 | Houses by the spawn stand in one line | The Terrace Row is a cluster: the chapel (-41, -75), cottage A (-17, -77) set north, the two-storey cottage B (-9, -69) set south, cottage D turned to face the lane (12, -69, heading 90, door west). The street is a dirt lane that bends round them; the Quarry Office stays behind the spawn |
| 3 | The bedrock wall runs to the bottom of the world | `dress.bedrock_walls` now fills each wall column from the foot of that column's own rock (y 49 to 54 under the gantry wall, y 65 to 71 under the path wall) up to the wall's top; nothing hangs below the island |
| 4 | Too much stone; the front should be green and hillier | Lanes and streets are coarse dirt and gravel, not slate flags; spawn terrace, row, front and bench are grass with dirt tracks. Stone stays where the author kept it: the quarry island, the Pit, the Cart Yard (the one stone area) and the retaining walls between terraces. The Dressing Floor has six grass hills (4 to 5 high at (-46, -27) and (34, -27), 3 high at (-22, -24) and (21, -23), two swells at (-40, -42) and (30, -43)) and 14 spruces; its slate stacks go from twelve to four. Grass is 52% of the spawn terrace's top blocks, 38% of the row's, 63% of the front's |
| 5 | Water for contrast, e.g. a river at the front | `dress.river`: a creek across the Dressing Floor from a spring pond at (-35, -35) through seven bends to a pond at (26, -34), three wide, water flush with the ground over a gravel bed in a closed channel (`audit.loose_water` 0), planks where the lane crosses at x -3..3. Mirrored on blue's half |
| 6 | A long fence runs along the map | It was the cart track, 52 rails along the Cart Yard at z -58 and 19 on the Quarry Floor. Now a 12-rail stub by the wagon (x -14..-3) and a 7-rail one by the pit (x 38..44). The longest straight fence in the world is 13 blocks, the safety rail on the Chapel Landing's open edge (-58..-46, 75, -63) |
| 7 | A pine stands on a house roof | The tree at (-76, -97) stood on the Winding House's eave and the one at (-66, -97) inside the headframe. `dress.trees_` refuses a spot inside any house, headframe or kiln box widened by three, and any spot whose ground block is not grass; the bench's trees are at (-74, -82) and (-80, -82). The read-back counts leaf blocks resting on a stone-brick stair: 0. **Library defect worked round locally**: `trees.plant` checks the crown against blocks but takes the trunk's column top as the ground, so a trunk on a roof's overhang is accepted |
| 8 | Should the tower room stand at the front line? | **Kept where it is**, for a reason the plan's numbers state: the front line to each room is 88 and 100 moves against WL10e's floor of 59, and the two rooms are 138 apart against WL7's 46 to 143. A room at the front line would stand about 20 to 30 moves from the band (an estimate, not a measurement), which the corpus rule refuses, and would pull the rotation between the rooms well under WL7's floor. The room is also where the headframe is seen from the spawn terrace |
| 9 | A boulder next to an objective | The nearest boulder-like thing to each objective is now read back (`walk.py`): the beehive ovens stood eight blocks from the Kiln's door, they are now 9.4 and further; the iron cubes stood on the spawn lawn, they are now flat outcrops in the bank behind the spawn at (-21, -104) and (17, -104), 17 blocks from the monuments. Nothing boulder-like is within 9 blocks of any objective |

Not done: the retaining walls between the terraces stay dressed stone (a stepped hill needs a face); they read as stone from above but are the
terraces, not hills of bare rock.
