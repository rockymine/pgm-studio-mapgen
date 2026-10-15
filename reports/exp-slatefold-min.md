# exp-slatefold-min: Slatefold, capture the wool, on a studio running `Rules:Mode=minimal`

Built by Sonnet 5.5 from the experiment brief (Brief 1) through `http://localhost:7895/api`; spec in
`specs/exp-slatefold-min/` (`build-spec.py` writes the plan and the refinement), world in
`maps/ctw/slatefold_minimal_rules/`, renders in `specs/exp-slatefold-min/renders/`. The reading was `ORDER-OF-WORK.md`,
`WHAT-A-BOARD-IS-MADE-OF.md`, `approaches.md`, `match-flow.md` §4/§6/§10, `AUTHORING-BRIEF.md` and the `pgm-board`
skill. The earlier builder's spec, report and renders were not opened; `BOARDS-BUILT.md` was opened once, at the end,
to copy the entry format, and its row for the earlier board was read then, after this board's design was fixed.

## What I set out to build

**A slate-quarrying hamlet on two terraced hillsides that face each other across a 32-block void, two wools a team:
a kiln house down on the quarry floor and a winding house on a high bench reached by its own path.** 100 x 232
blocks, `rot_180`, 12 a team, spawn to spawn 216 blocks. Per team (team 0 stands on +z, team 1 is the point image
(x,z) -> (-x,-z)):

| place | where (blocks) | why a player goes there |
|---|---|---|
| spawn hall on the spawn terrace | x -12..12, z 100..116, y16; door at (-1..2, 105) | arrival; the doors face the stair top |
| spawn stair | x -12..12, z 80..92, three treads y13..15 | the one way down to the hamlet, 4 blocks of rise |
| the hamlet and its green | x -32..48, z 36..80, y12; five cottages, worn green at (-4..8, 58), yards at (12..20, 62) and (30..38, 56) | the middle ground, fought through house by house |
| the cart track | stair x 8..24, z 36..48 (y9..11) and the street to the stair head at (16, 53) | the way from hamlet to quarry; the defenders' lane to the kiln |
| the quarry floor and pit | x -16..48, z 16..36, y8; pit centred (8, 25), floor y5 | the lowest ground, the front line, and the place the kiln stands on |
| spoil heaps | on the spoil shelf (x -32..-16, z 16..36, y11) centred (-24, 26) and on the floor at (-10, 30), tops y15 and y11 | cover under the tower and on the kiln approach |
| kiln house (wool) | room x 36..48, z 16..28, y8; wool at (44, 22, y7) | the quick wool, in the front corner, two faces on void |
| high bench and winding house (wool) | bench x -48..-32, z 28..116, y16; tower room x -48..-32, z 16..28; wool at (-40, 22, y15) | the slow wool, 8 blocks above the enemy's quarry |
| bench path | (-14,104) to (-39, 30), wandering, and the bench stair at x -32..-16, z 68..80 (y13..15) | the tower's own way, from the spawn terrace and from the hamlet |
| warden's house | x -44..-34, z 98..108 | the reason to walk the bench's back end; the path ends at its door |
| scree gully | x -32..-16, z 80..96, y12, one boulder at (-22, 88) | the drop between spawn terrace and hamlet |
| crossing | build zone x -48..48, z -16..16; a stone pier 8 wide, 7 long on each shore at x -4..4, z 9..16 (image z -17..-10), bedrock under | where the bridge starts |

Look: grey slate and stone (quarry set: stone, andesite, cobble end patch; cliffs cut as beds of stone, andesite,
cobble and polished andesite), timber (spruce planks, dark oak posts), red brick on the two wool houses, turf with
ferns on the benches. Tone families: ground = grey stone and cool green turf, built = timber with a brick accent.
Biome Extreme hills (#8ab689), the cool grey-green that makes the turf read as moss beside the slate. Three themes:
`hillside` (turf, soil and scree by the slope axis 32/14/44 degrees), `quarry` (bare slate) and `steps` (four
stones in a cell, the same on every flight).

### The review of the plan before building

Done once, from `tools/board.py`, `--dry` and the first isometric, against the brief and the lessons.
It found three things, all changed before the second store. (1) The first grid had a 6 x 4 cell enclosed void in
each back corner between the bench, the spawn stair and the hamlet: a hole by accident, so it became ground at
the hamlet's height (the scree gully). (2) The stairs rose 5 and 6 blocks, over lesson 5's four, so every height was
lowered to 8 / 12 / 16 with three treads between. (3) The spawn terrace's far side and the bench's back end read as
dead on the top-down; the east wing was narrowed from 5 to 3 cells and a warden's house put on the bench back.
The wool rooms stood on the front line on purpose (brief: the kiln is down by the quarry floor), and that is where the
relaxed rules were used.

## What was built, in numbers (final store, change 15, `exp-slatefold-min`)

```
ground   15482 walked, 132 scrambled, 738 barrier, 5.3% steps further than a player walks
props    50 placed, 3 declined   (the three are DR-PASS complaints; the props stand; no decline survives)
routes   worst step 4, on route spawn-0 to wool-0   (a drop into the quarry, 0 placed)
coverage reached 13281, decorated 1794, dead 1385 of 16460 = 8.4% dead
preflight export gate OPEN, traversability one component, mirror check passes
```

The 738 barrier cells are the terrace faces and the bench's eastern cliff (a 4 to 5 block face along x -32,
z 36..68), which are the board's design; every flight a player is meant to walk transects `walked end to end`
(cart stair x16 z28..56 from y5 to y12; bench stair z74 x-38..-8 from y16 to y12; spawn stair x0 z76..100 from y12
to y16, each step 1). Walks: spawn to its own kiln 111 blocks, to its own tower 102; spawn to the enemy kiln
(-44,-22) 148 blocks with 32 placed, to the enemy tower (40,-22) 154 with 37 placed; the flow read gives the
attacker 148 to 150 against a defender's 89 to 92. Each wool room carries the default chests, stacked in pairs at the
inner corners (two of the kiln's four corners checked, at (38,18) and (45,25): chests at y8 and y9). Time to drive: 7 to 12
seconds a store, read-back and export included; no 5xx, no crash, every world built.

## What the relaxed rules did

See section 4. Short version: the board has two wool rooms on the front line, a 96-block front line, terraces
and flights that the plan tier calls 2 to 5-block steps, a tower beside a 5-block climb and three houses with
less than 8 blocks round them, and every one of those answered 200 with a complaint.

---

## 1. Times per phase (from `date`)

| phase | start | end | note |
|---|---|---|---|
| reading (CLAUDE.md, brief, order of work, what a board is made of, approaches, match-flow, authoring brief, skill) | 13:43:46 | 13:46:36 | |
| plan: pieces, grid, evaluate, inspect, first review | 13:46:36 | 13:47:17 | `board.py` grid, one `--dry` |
| first store and look | 13:47:17 | 13:47:24 | 7 s for store, read-back, export, picture |
| ground: three themes, relief pushes, biome, `themeById` | 13:47:24 | 13:48:45 | |
| dressing: house styles forked from the library, paths, props, flora | 13:48:45 | 13:52:14 | |
| revisions: coast edits, heights to four-block flights, piers, trees, plots | 13:52:14 | 13:59:27 | fifteen stores in all |
| final strata fix, drive, read-back | 13:59:27 | 14:01:30 | a `follow` on the strata was a silent no-op |
| a mis-keyed theme (spoil shelf painted as steps), renders, checks, report, `BOARDS-BUILT.md` | 14:01:30 | 14:09 | |

About 25 minutes of building, 20 of it against the studio; one store is under 15 seconds.

## 2. What the brief asked for that the tool could not express, and what I did instead

| asked for | what I looked for | verdict | what I did |
|---|---|---|---|
| a kiln house and a winding house that differ as buildings | `roomStyles` in the refinement: `wool` and `spawn` only (`SketchRoomStyles`); `WoolPlacement` has `id`, `piece`, `at`, `color`, `footprint` and no style | missing: one shell binds every wool room | one forked minehead-style shell (brick over two storeys, timber lookout, slate roof); the rooms differ by footprint (12 x 12 kiln, 16 x 12 tower), by height (y8 against y16) and by position, not by form |
| slate | block ids: no slate in 1.8 | not a studio gap | stone brick roofs, andesite and polished andesite faces |
| moss on the benches | `WHAT-A-BOARD-IS-MADE-OF.md` rules mossy cobble and mossy brick out of ground | by ruling | Extreme hills biome tint plus a `flora` pass at fern share 0.3, coverage 0.28 |
| a winding path to the tower | `stroke` `wander`, `wanderLength` | reachable | wandering stroke; the "winding house" is a name, not a spiral stair |
| a kiln with a chimney, bottle kilns, a headframe | `addLayers` `made` layers | reachable, not built | not built in this run: time. The kiln reads as a brick tower with a slate roof |
| a flooded quarry pit | `fluid` prop | reachable, not built | the pit is a dry hollow (push -3, floor y5) |
| a build zone a player can see | the plan zone writes a region and no marker; `addLayers` | reachable | a stone pier each shore, bedrock under, 4 thick, on the centre line; nothing marks the zone's width, which is the whole 96 blocks |
| a defence wall | `walls` on a shared interface of two pieces | reachable, not used | the brief asks for none, and both rooms are entered from the void side, where no interface exists |
| beds that follow the ground | `follow: 100`, `reach: 16` on a height stack used as `fill` and `wall` | the studio answered 200, no complaint, and painted plain stone | dropped `follow`; beds at fixed world heights |

## 3. The twelve lessons, one by one

1. **An objective is found without a map: met.** Both wool rooms stand on the front line in the open (kiln at x 36..48,
   z 16..28; tower x -48..-32, z 16..28), open on the void side with the door in view, and a wool-coloured cube floats
   about 30 blocks over each room as the signpost (red wool at (42, 22) y39..40). No objective is underground or only at the top.
2. **Made of what the mode needs: met.** Wool blocks that take a colour; no monument on this board.
3. **A wool room holds the standard loot: met by the default.** Chests stacked in pairs at the inner corners (two of four checked in the kiln); I did not open the chests. No defence wall, so no front-face chests.
4. **Vegetation leaves the floor visible: met.** Seven trees a side (five spruce, two oaks), none on the cart track, the
   quarry floor or the spawn terrace's doors; ground cover at coverage 0.28, tall share 0.04.
5. **Every stair is attached and walkable: partly.** The flights are ground treads of one block rise, 4 blocks deep,
   at most four risers (8 to 12, 12 to 16, 12 to 16), no turned stairs, no collisions, a landing at each head, and
   all three walk end to end. Their sides are not railed: they stand beside lower terrace at drops of up to 3 blocks.
6. **A spawn's exit is open: met.** Two doors (`-z` and `-x`), a 4-wide gap at (-1..2, 105) and onto a terrace with
   nothing on it; the walk from the spawn leaves it with 0 placed. One tree that stood in front of a door
   (`DR-KEEP`) was moved.
7. **A floating platform cannot be mined away: met.** The only things off the ground are the piers, which stand
   on bedrock at y3, four blocks thick, one at x -4..4, z 9..16 and its image at z -17..-10.
8. **Ladders only where needed, never in water: met.** There are no ladders, and no water.
9. **Every join is open: met, vacuously.** There are no shafts or tunnels.
10. **Things are at a player's scale: met.** Cottages are 10 x 8 to 12 x 8, the pit 22 x 12, the heaps 10 across, the
    flights 12 to 24 wide, the bench 16 wide; the rim is one course. The tower is four storeys.
11. **Ground varies in patches, bare stone carries detail: partly.** Three worn dirt/coarse dirt patches (the green and two
    yards), a three-stone path set, the slope stack's three bands, a cobble end patch in the quarry floor, and cliff
    faces bedded in stone, andesite, cobble and polished andesite. The hillside is otherwise one meadow.
12. **A build zone shows where to build: partly.** A stone pier each shore on the centre line says where a bridge starts; the zone itself
    is 96 blocks wide and the pier is 8, so the extent of the zone is not drawn.

## 4. The relaxed rules

Every finding that came back as a complaint on a 200 and would have refused or dropped something under the full
rules (category from `GET /api/rules?rule=`). "Final" says whether it is in the stored board's findings.

| rule | category | what it said | kept or changed | why |
|---|---|---|---|---|
| WL10 | unplayable | the kiln wool has a walk of 8 blocks to the crossing, band 22 to 147 | kept (final) | the brief puts the kiln by the quarry floor, which is the front |
| WL18 | unplayable | the same wool, 8 against a band of 25 to 130 | kept (final) | same |
| FR9 | unplayable | the kiln room has 12 blocks of front line, floor 15 | kept (final) | a 12-wide room in the corner |
| FR6 | unplayable | the front line from (-12, 4) to (12, 4) is 24 cells wide, over 16 | kept | the brief's crossing spans the board |
| G8 | unplayable | ground fills 77.6 to 78.7% of its rectangle, band 20 to 54 | kept | two filled hillsides |
| LN5 | unplayable | 15.3 to 15.9% of ground off every route, over 12 | kept | the bench's back end and the spawn wings; coverage later measured 8.4% dead |
| WL11 | unplayable | the tower room sits 4 to 6 blocks above the spoil shelf where they share an edge | kept (5, final) | the tower is the brief's high bench |
| EL1 x 22 (25 first) | unplayable | piece pairs differing 2 to 6 blocks along a shared edge: terrace faces and every tread | kept | EL1 reads treads as flat plan pieces; transects show the flights walk. Offered line marks as the fix; not taken |
| RL3 x 8 | unsatisfiable | marks meeting in steps of 3 to 5 blocks, worst at (-32, 16) and (-32, 36) | kept | the same faces, stated as relief marks |
| SK27 | conflict | the island has 13 plateaus and 3 paints | kept | a theme is a place; the three are quarry, hillside and steps |
| DR-PASS x 3 | unplayable | cottage-east (22..32, 66..74), cottage-yard (27..37, 40..48) and cottage-warden (-44..-34, 98..108) have a side with under 8 blocks | kept (final) | I moved them twice and the terrace is too narrow for 8 on every side |
| DR-TONE | conflict | the boulder at (26, 33) is cut from the ground's own tone family | kept (final); two others cleared by moving them | slate rock on slate floor is the point |
| PL4 x 4 | conflict | spawn-stair treads and the scree gully overlap | changed | my arithmetic: the gully narrowed by one cell |
| HS20 x 4 | conflict | roof slab dark oak against stone brick body | changed | set the slab to the stone brick slab |
| PT1 | conflict | grass fills all three courses of the surface | changed | a grass-over-dirt stack |
| PT4 | conflict | the pier's cell pattern has a rise of 0 | changed | rise 2 |
| WX14 x 2 | unfinished | wool and spawn rooms have no house of their own | changed | bound the two forked styles |
| DR-ROAD x 2 | conflict | a tree 1 to 2 blocks from a road, a boulder 1 block from one | changed | moved |
| DR-KEEP | conflict | a tree on the cell kept clear in front of a door | changed | removed |
| DR-ROOT | conflict | a tree on andesite, not soil | changed | removed |
| DR-CROSS | unplayable | the warden's house overlaps the bench path and splits it | changed | re-routed the path to the door |
| DR-SITE x 2 | unsatisfiable | two trees with no ground, after the east wing narrowed | stayed a decline | nothing to stand on; moved them |
| SR2 | | `themeById` names ids the compile no longer has | answered as complaints on the dry run, fixed before the store | after the heights moved |
| RQ1 x 3 | malformed | the outline of `bench-16` folds across itself after a point is added or moved | changed | this one went to the store as a complaint and stored the folded outline for one run (a 16-corner ring I did not draw); I took the edits out and re-stated them against the clean compile |

**What the relaxed rules let me build that I believe the full rules would have stopped.** (1) Both wool rooms in the
corners of the front line, the kiln 8 blocks of walk from the crossing; `WL10`/`WL18` would have pulled each at
least 14 to 17 blocks back from the edge, which on a quarry floor 20 blocks deep means off the floor. (2) A crossing
96 blocks wide, since `FR6` caps a front line at 16 cells (64 blocks); the board would have been a third narrower or
had a land bridge. (3) A tower room 5 blocks above its neighbour (`WL11`). (4) Terraces with 4 and 5-block faces
and flights of one-block treads between plan pieces (`EL1` x 22). (5) Three cottages that cramp the passage
(`DR-PASS`). Whether any of it plays better I cannot say without the author. The relief seams, the fill and the
three wool-room numbers are the ones I would check in game.

## Open gameplay questions (decided without an oracle)

- **A kiln wool 8 blocks of walk from the crossing.** The attacker's walk to it is 148 against the defender's 89 to
  92, but a player already at the crossing is 16 to 48 blocks from the wool, so it falls to whoever bridges first.
  I left it on the front line because the brief asked for it; an author may want it behind the cart track.
- **The tipped heap beside the tower crests at y15, level with the tower floor, 8 blocks from its wall.** It is a perch to bridge from and shoot from, one of the approaches from above; whether it is too good a one is the author's.
- **The bench has two entries.** The bench stair at z 68..80 and the spawn terrace's wing both reach the tower
  path, so the tower is one queue up a spur of 16 blocks across.
- **The floating cube is the signpost.** Whether two cubes 30 blocks up are enough to find a wool without a map is
  the author's.
