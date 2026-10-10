> Written by two Sonnet 5.5 helper agents on 2026-10-10: started by one, which stopped at the coordinator's priority change, and finished by another. Its scripts and per-objective JSON live in a scratch directory and are not committed; the versions it measured are named in the method.

# Findability audit: where the goals are, and how visible they are

**Question.** The author's complaint is that freeform monuments and cores are sometimes hidden or hard to reach, while the studio floats a marker over every goal. This audit gives every objective measured, comparable numbers with coordinates: how much of the ground within 30 and 60 blocks, in front of it and reachable by the attackers' walk, can see it; where on the attackers' walk it is first seen; what it stands on and under; and whether anything marks it. Code, JSON and logs are in this folder (`audit.py`, `common.py`, `build_audit.py`, `hand.py`, `out/*.json`, `rows.json`).

**What was run.** 19 board versions, 65 objectives (58 reached by the attackers' walk, 7 not): 10 freeform board versions (8 boards; Hollow Mesa and Frostholm twice, before and after the core moves), 4 library trials, the 2 experiment boards of the pgmvox side, and 3 studio boards.

## Method (exact wording of AUDIT-PARTIAL.md; changes marked **[amended]** or **[added]**)
- World: Anvil regions read to a voxel array. Objective blocks = blocks inside the map.xml region whose id is the objective material
  (destroyable `materials`, core default obsidian); a cuboid max is exclusive (PGM). If none, any non-air non-liquid block.
  Exposed faces = faces whose neighbour cell is not opaque (pgmvox `sight.voxel_opaque`: leaves, solids opaque; glass, fences, water clear).
  **[added]** A capture-the-wool objective is the wool block inside a 3x3x3 box round the `<wool location>` (its taker is the attacker, the other team defends); a flat `<wool>` outside `<wools>` is not an objective.
- Sight: `sight.line_clear` (quarter-block steps) from the eye `(x+.5, feet_y+1.62, z+.5)` to a point 0.05 out of any exposed face centre,
  only for faces whose normal points to the eye (exact, a back face is hidden by its own block).
- Eyes: standable cells (`walk.standing`, doors passable) reached by the attackers' walk, within 3D distance of the objective centre,
  in the front half-plane: `(cell - objective) . axis >= 0` or past halfway between spawns (axis = owner spawn to attacker spawn).
  Columns: `v30` (<=30), `v60` (<=60, the headline), `vfar` (60 to 120), `v60all` (<=60, all directions, reached), `v60standable` (front, not reached-filtered).
  At most 3000 cells sampled per band (seed 20261010); the sampled count and cell count are in the JSON (`out/<slug>.json`). **[added]** A share over 3000 sampled cells carries about +-1.8 points of sampling error (95%); a band with fewer than 3000 cells is exact.
- Walk: `pgmvox.walk.walk`, MoveRules(max_drop=6, running jumps gap<=3, doors, ladders, kill_y from a `<below>` region else none), from the
  spawn point's nearest standing cell. If the objective is not reached on foot and the map allows building over void, a second walk
  with `rules.build` = pure-void columns (inside the map's build rectangle where the map restricts it: riftwater x -16..16 z -88..88,
  cinder-reach x -24..24 z -72..72, redwash-mesa x -22..22 z -64..64 **[added]** exp-slatefold-studio x -40..40 z -16..16; everywhere where the map has no void rule; nowhere for
  hollow-mesa, cinderfall, tamarisk-wash, exp-abbeymoor-pgmvox **[added]** exp-slatefold-pgmvox) over y 1..maxbuildheight-1. Walk mode is recorded per objective.
  **[amended]** A column is "pure void" when it holds no solid block at or above the kill height (was: no solid block at all). It changes only Stratum, whose pylons and land under the clouds made every column non-void, so it was unreachable under the old rule; with `<below y=58>` its sky above y 58 is void. Stratum's bridging walk therefore lets a player build anywhere above y 58 (1.67 million cells reached); its rows are the least restricted reading in the table.
  Portals (hollowcrown lifts) are modelled: a reached source cell at distance d0 starts a second walk offset by d0 (`combined_walk`).
- Access cell: the reached standing cell with the least walk distance within 3 blocks (then 4.5, 6, 9) of an exposed face centre.
- Float: air blocks between the objective's lowest block and the first non-passable block under its nearest footprint column.
  Setting: sky = nothing non-passable within 20 above; otherwise roof (<= 6 thick, not much over it) or underground. `sky_rays` = clear rays
  (straight up plus 8 at 45 degrees, 40 blocks) out of 9. `prominence` = objective top minus the highest solid within 10 blocks.
  **[amended]** Free-floating components (below) are ignored for setting and prominence, so a floating marker is not read as a roof or a hill.

### Path trace and "first seen" (the fix to known defect 1)
- **[amended]** The trace walks back from the access cell along predecessors (distance minus the step's cost, 4-neighbour, ladder, running-jump and fall steps) to the spawn; each step is confirmed by a walk over a crop of the world. The crop walk now carries the build mask (cropped, y shifted) and the kill height, so a step through bridged air is confirmed (it was rejected before, which left `first_seen` and `held_from` empty for every bridging objective). Where no candidate step confirms, the cheapest candidate is taken anyway and counted (`trace_unverified`): 1 step in each of the four Hollowcrown objectives (its lift walk), 0 elsewhere.
- **First seen** = the first cell of that path from which any exposed face of the objective is visible within 128 blocks (vanilla view distance, `CONFIG.RENDER`); `distance` is the eye-to-centre distance there and `walk` its walk distance from the spawn. 128 or so means "from the start of the walk, across open ground". **Held from** = the distance from which the objective stays visible to the end of the path (in the JSON; not tabled).
- "never on path" = no cell of the traced path sees it within 128 blocks.

### Markers (the fix to known defect 2)
- **[amended]** `floaters` lists every free-floating component (26-neighbour connected, at most 400 blocks, touching nothing on the sides or floor of a window 14 blocks round the objective, from its top-2 to top+64) with its block census, bbox, height above the objective's top and horizontal offset. The old census of beacon/glowstone/lantern ids stays in the JSON (`markers_near`) but is not used. Every row's marker cell was then **judged by hand** from the floater list plus a column read (blocks over the footprint +-3 up 70, and marker-like ids within 10: `hand.py`). A marker is a free-floating wool or beacon mass over the goal; a gold cap on a roof or a banner on a wall is not.

### Boards read, versions
- **[added]** All freeform and library boards are the committed worlds of commit **b970fcb2** (`git archive`, folder `snap-b970fcb2/`); `hollow-mesa-after` and `frostholm-after` are `origin/opus55-freeform-riftwater` at **53fbe2e2** (`snap-origin/`), measured with the same code, so each pair is a before/after of one core move.
- **[added]** The four experiment boards are the working-tree worlds copied at **02:24 UTC on 2026-10-10** (`snap-exp/`, md5 list `snap-exp/md5-snap-v2.txt`). An earlier copy at 02:05 UTC had different Abbeymoor (both) and Slatefold-pgmvox worlds; those results are in `out-exp-v1/` and are not used. The working tree was re-hashed at 02:26 and 02:28 UTC after the runs: unchanged. Slatefold-studio did not change between the two copies.
- `opus55b-russetford` is the world of origin/opus55b-russetford (the third pass, committed 22:31 on 2026-10-07).

### What is estimated or approximate
- Every share is a sample (above). `first seen` is capped at 128. `float` counts air under the nearest footprint column's lowest block, so a core over a pit counts the pit (Frostholm-after: 8, over a stone-brick floor at y 48 with ground at y 56 beside it).
- Setting `underground` / `roof` is the heuristic; non-sky rows were checked by hand (below).
- Rows marked "not reached" have no v30/v60 (the attackers' walk, with the modelled bridging, does not get within 9 blocks of a face); the estimate shown is `v60standable` (every standable front-half cell within 60, reached or not), which is an upper bound.
- Stratum's rows come from the permissive bridging; Hollowcrown's from the lift model; Saltgate (attack/defend, three stages with filter-keyed spawns) is audited from the stage-1 attackers' spawn only.

### Hand checks of every non-"sky" setting
| board, objective | heuristic | by hand |
|---|---|---|
| hollow-mesa red-core / blue-core | underground | right: over the footprint +-3, y 53..73 holds planks, hardened clay (516), stained clay (991) and the mesa top at y 73: the core hangs in the Throat cavern under 20 blocks of mesa |
| frostholm red-core / blue-core | roof | right: pane y78, stone brick y79, planks y80..83 and a fence y84 over the lantern: a lighthouse lantern roof |
| cloudhaven red-lantern / blue-lantern | roof | right: quartz y83..88 over the lantern, one gold block at y 89 on top (7 above the objective, part of the roof: not a marker) |
| hollowcrown red-echoes / blue-echoes | underground | right: stone y40..81 over the column (1568 blocks) |
| stratum red-obelisk / blue-obelisk | underground | wrong word, right fact: a niche cut two blocks into the obelisk shaft (quartz from y102 to 120 above; the shaft is open on the east face balcony); "enclosed by tower" |
| saltgate west-store / east-store / purple-attackers | roof / roof / underground | stone-brick roof 32..33 over the west store; 36..37 over the east store; the wool at (0,35,54) sits under stone brick y41..50 and fence y51..60 |
| exp-slatefold-pgmvox (all four wools) | roof | right: stone brick and stair roofs 8 to 16 above each wool room |
| exp-slatefold-studio (all four wools) | roof | right: a plank roof 5 to 27 above; wool cube marker above it |

## Rows (one per objective)

Columns: **float** = air blocks under the lowest block. **v30 / v60 / far** = share of the attackers' reached cells in the front half, within 30 / 60 / 60-120 blocks, that can see the objective (headline: v60). **prom.** = objective top minus the highest solid within 10 blocks (negative: the objective sits below its surroundings). **first seen** = eye-to-centre distance in blocks, the cell, and the walk distance from the attackers' spawn, on the traced path to the access cell. **marker** judged by hand. `[bridging]` = reached only by the modelled bridging walk; `[foot+lift]` = Hollowcrown's lifts. Box is x, y, z of the objective blocks (inclusive).

### freeform

**riftwater**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-square [bridging] | -66..-66, 54..55, -44..-44 | 1 | sky | (-63,53,-44) walk 165 | 48% | 21% | 13% | -10 | 45 at (-21,55,-41), walk 123 | no |
| red-green [bridging] | -66..-66, 52..53, 48..48 | 1 | sky | (-63,51,47) walk 167 | 73% | 59% | 29% | -16 | 128 at (58,47,18), walk 44 | no |
| blue-square [bridging] | 65..65, 54..55, -44..-44 | 1 | sky | (62,53,-44) walk 165 | 48% | 22% | 14% | -10 | 45 at (20,55,-41), walk 123 | no |
| blue-green [bridging] | 65..65, 52..53, 48..48 | 1 | sky | (62,51,47) walk 167 | 73% | 60% | 30% | -16 | 128 at (-59,47,18), walk 44 | no |

**hollow-mesa**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core | -73..-70, 49..52, -26..-23 | 0 | underground | (-70,47,-20) walk 173 | 24% | 4% | 0% | -41 | 19 at (-56,44,-15), walk 157 | no |
| blue-core | 69..72, 49..52, 22..25 | 0 | underground | (67,47,21) walk 173 | 24% | 4% | 0% | -41 | 16 at (57,45,15), walk 159 | no |

**hollow-mesa-after** (after the core move, origin/opus55-freeform-riftwater 53fbe2e2)

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core | -67..-64, 79..82, -26..-23 | 5 | sky | (-64,74,-21) walk 173 | 83% | 42% | 34% | -11 | 129 at (62,75,-3), walk 39 | no |
| blue-core | 63..66, 79..82, 22..25 | 5 | sky | (63,74,20) walk 173 | 83% | 42% | 35% | -11 | 129 at (-63,75,2), walk 39 | no |

**frostholm**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core | -18..-16, 75..77, -68..-66 | 0 | roof | (-20,71,-67) walk 193 | 22% | 9% | 13% | -7 | 85 at (35,52,-4), walk 75 | no |
| blue-core | 15..17, 75..77, 65..67 | 0 | roof | (19,71,66) walk 193 | 22% | 10% | 12% | -7 | 85 at (-36,52,3), walk 75 | no |
| red-holmstein | -58..-58, 62..63, -20..-20 | 2 | sky | (-59,60,-18) walk 151 | 49% | 25% | 7% | -5 | 72 at (-8,56,32), walk 73 | no |
| blue-holmstein | 57..57, 62..63, 19..19 | 2 | sky | (57,60,17) walk 151 | 49% | 27% | 7% | -5 | 72 at (7,56,-33), walk 73 | no |

**frostholm-after** (after the core move, origin/opus55-freeform-riftwater 53fbe2e2)

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core | -29..-27, 57..59, -59..-57 | 8 | sky | (-24,56,-59) walk 161 | 43% | 30% | 6% | -25 | 40 at (5,63,-37), walk 125 | no |
| blue-core | 26..28, 57..59, 56..58 | 8 | sky | (23,56,58) walk 161 | 43% | 31% | 7% | -25 | 40 at (-6,63,36), walk 125 | no |
| red-holmstein | -58..-58, 62..63, -20..-20 | 2 | sky | (-59,60,-18) walk 150 | 56% | 30% | 8% | 4 | 72 at (-9,57,32), walk 75 | no |
| blue-holmstein | 57..57, 62..63, 19..19 | 2 | sky | (57,60,17) walk 150 | 56% | 29% | 9% | 4 | 72 at (8,57,-33), walk 75 | no |

**cloudhaven**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-lantern | -72..-72, 81..82, -60..-60 | 0 | roof | (-73,80,-57) walk 260 | 73% | 31% | 16% | -11 | 123 at (34,75,2), walk 76 | no (gold block cap y89 on the roof, 7 above) |
| red-gardens | -71..-71, 61..62, 59..59 | 0 | sky | (-72,60,56) walk 223 | 52% | 35% | 10% | -14 | 111 at (23,76,2), walk 87 | no |
| blue-lantern | 71..71, 81..82, 59..59 | 0 | roof | (72,80,56) walk 260 | 74% | 31% | 16% | -11 | 123 at (-35,75,-3), walk 76 | no (gold block cap y89 on the roof, 7 above) |
| blue-gardens | 70..70, 61..62, -60..-60 | 0 | sky | (69,60,-57) walk 223 | 53% | 35% | 10% | -14 | 111 at (-24,76,-3), walk 87 | no |

**hollowcrown**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-eyrie [foot+lift] | -54..-54, 106..107, -70..-70 | 0 | sky | (-51,102,-69) walk 216 | 5% | 2% | 1% | 1 | never on path | no |
| red-echoes [foot+lift] | -66..-66, 23..24, 16..16 | 0 | underground | (-65,22,13) walk 194 | 21% | 2% | 0% | -84 | 16 at (-65,21,0), walk 181 | no |
| blue-eyrie [foot+lift] | 53..53, 106..107, 69..69 | 0 | sky | (50,102,68) walk 216 | 4% | 2% | 1% | 1 | never on path | no |
| blue-echoes [foot+lift] | 65..65, 23..24, -17..-17 | 0 | underground | (64,22,-14) walk 194 | 21% | 2% | 0% | -84 | 16 at (64,21,-1), walk 181 | no |

**stratum**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core [bridging] | -57..-55, 81..83, 47..49 | 29 | sky | (-52,81,47) walk 159 | 53% | 30% | 9% | -14 | 29 at (-27,81,52), walk 134 | no |
| blue-core [bridging] | 54..56, 81..83, 47..49 | 60 | sky | (51,81,47) walk 159 | 53% | 30% | 9% | -14 | 29 at (26,81,52), walk 134 | no |
| red-obelisk [bridging] | -55..-55, 100..101, -50..-50 | 0 | underground | (-53,99,-52) walk 180 | 6% | 17% | 23% | -20 | 125 at (65,80,-21), walk 29 | no (gold cap y121 on the shaft) |
| blue-obelisk [bridging] | 54..54, 100..101, -50..-50 | 0 | underground | (52,99,-52) walk 180 | 6% | 17% | 23% | -20 | 125 at (-66,80,-21), walk 29 | no (gold cap y121 on the shaft) |

**gullhaven-dtm**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-harbour | 30..32, 22..24, 24..26 | 3 | sky | (28,19,25) walk 161 | 79% | 68% | 41% | -4 | 27 at (7,27,37), walk 139 | no |
| red-beach | -52..-50, 25..27, 7..9 | 3 | sky | (-51,22,9) walk 149 | 81% | 78% | 34% | -5 | 96 at (-44,30,104), walk 52 | no |
| blue-harbour | -70..-68, 22..24, 89..91 | 3 | sky | (-66,19,88) walk 161 | 78% | 68% | 42% | -4 | 27 at (-45,27,78), walk 139 | no |
| blue-beach | 12..14, 25..27, 106..108 | 3 | sky | (13,22,106) walk 149 | 82% | 78% | 36% | -5 | 96 at (6,30,11), walk 52 | no |

**saltgate**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| west-store | -18..-18, 27..28, 0..0 | 0 | roof | - | not reached | not reached (est. 1% from standable cells) | not reached | -10 | - | no |
| east-store | 18..18, 31..32, 15..15 | 0 | roof | - | not reached | not reached (est. 5% from standable cells) | not reached | -17 | - | no |
| purple-attackers | 0, 35, 54 | 0 | underground | - | not reached | not reached (est. 5% from standable cells) | not reached | -25 | - | no |

### library trials (pgmvox library, Opus / Sonnet)

**cinder-reach**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core [bridging] | -53..-49, 52..56, 22..26 | 8 | sky | (-46,51,21) walk 130 | 45% | 27% | 35% | 0 | 121 at (69,53,12), walk 14 | no |
| blue-core [bridging] | 48..52, 52..56, -27..-23 | 8 | sky | (45,51,-28) walk 130 | 45% | 27% | 35% | 0 | 121 at (-70,53,-13), walk 14 | no |

**redwash-mesa**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-table [bridging] | -56..-56, 64..65, -24..-24 | 1 | sky | (-55,63,-21) walk 153 | 68% | 58% | 38% | -4 | 112 at (52,63,7), walk 32 | no |
| blue-table [bridging] | 55..55, 64..65, -24..-24 | 1 | sky | (52,63,-25) walk 153 | 68% | 58% | 36% | -4 | 112 at (-53,63,7), walk 32 | no |
| red-wash [bridging] | -47..-47, 43..44, 28..28 | 1 | sky | (-44,42,27) walk 125 | 58% | 35% | 21% | -15 | 128 at (80,53,12), walk 1 | no |
| blue-wash [bridging] | 46..46, 43..44, 28..28 | 1 | sky | (43,42,27) walk 125 | 58% | 34% | 22% | -15 | 128 at (-81,53,12), walk 1 | no |

**cinderfall**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-core | -50..-46, 65..69, -12..-8 | 6 | sky | (-43,59,-13) walk 118 | 87% | 56% | 51% | 1 | 107 at (59,61,-9), walk 15 | no |
| blue-core | 45..49, 65..69, 7..11 | 6 | sky | (42,59,6) walk 118 | 87% | 56% | 50% | 1 | 107 at (-60,61,8), walk 15 | no |

**tamarisk-wash**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-obelisk | -58..-58, 74..76, -28..-28 | 2 | sky | (-57,71,-26) walk 161 | 67% | 57% | 38% | 0 | 105 at (46,64,-18), walk 41 | no |
| blue-obelisk | 57..57, 74..76, -28..-28 | 2 | sky | (56,71,-26) walk 161 | 67% | 56% | 37% | 0 | 105 at (-47,64,-18), walk 41 | no |
| red-sunstone | -63..-63, 65..66, 21..21 | 2 | sky | (-60,63,21) walk 154 | 39% | 20% | 2% | -5 | 15 at (-49,68,16), walk 143 | no |
| blue-sunstone | 62..62, 65..66, 21..21 | 2 | sky | (59,63,21) walk 154 | 39% | 20% | 2% | -5 | 15 at (48,68,16), walk 143 | no |

### experiment boards, pgmvox side

**exp-abbeymoor-pgmvox**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-abbey | -40..-40, 88..90, -72..-72 | 4 | sky | (-40,84,-72) walk 191 | 37% | 38% | 53% | -2 | 128 at (-6,67,50), walk 61 | no |
| blue-abbey | 39..39, 88..90, 71..71 | 4 | sky | (39,84,71) walk 191 | 37% | 39% | 55% | -2 | 128 at (5,67,-51), walk 61 | no |
| red-village | 30..30, 70..72, -70..-70 | 3 | sky | (28,67,-69) walk 182 | 44% | 22% | 5% | -10 | 16 at (26,67,-55), walk 166 | no |
| blue-village | -31..-31, 70..72, 69..69 | 3 | sky | (-30,67,67) walk 182 | 44% | 22% | 5% | -10 | 16 at (-27,67,54), walk 166 | no |

**exp-slatefold-pgmvox**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| orange-blue-team | 60, 59, -68 | 0 | roof | - | not reached | not reached (est. 4% from standable cells) | not reached | -20 | - | no |
| magenta-red-team | 60, 59, 67 | 0 | roof | - | not reached | not reached (est. 4% from standable cells) | not reached | -20 | - | no |
| cyan-blue-team | -76, 83, -91 | 0 | roof | - | not reached | not reached (est. 3% from standable cells) | not reached | -18 | - | no |
| yellow-red-team | -76, 83, 90 | 0 | roof | - | not reached | not reached (est. 3% from standable cells) | not reached | -18 | - | no |

### studio boards (STUDIO)

**opus55b-russetford**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-monument | 4..4, 36..38, -56..-56 | 3 | sky | (4,33,-56) walk 132 | 78% | 55% | 54% | 4 | 128 at (32,40,69), walk 7 | YES wool plus y56-58 (18 above top) |
| blue-monument | -5..-5, 36..38, 55..55 | 3 | sky | (-5,33,55) walk 131 | 78% | 56% | 54% | 4 | 128 at (-32,40,-70), walk 6 | YES wool plus y56-58 (18 above top) |

**exp-abbeymoor-studio**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| abbey-monument | -24..-24, 49..51, -69..-69 | 2 | sky | (-23,46,-67) walk 184 | 84% | 64% | 82% | -9 | 128 at (-2,34,56), walk 56 | YES wool plus y57-59 (6 above top) |
| village-monument | 30..30, 38..40, -62..-62 | 3 | sky | (30,35,-62) walk 186 | 78% | 59% | 58% | 0 | 127 at (1,34,62), walk 50 | YES wool plus y57-59 (17 above top) |
| abbey-monument-2 | 23..23, 49..51, 68..68 | 2 | sky | (21,46,67) walk 183 | 84% | 65% | 81% | -9 | 128 at (1,34,-57), walk 55 | YES wool plus y57-59 (6 above top) |
| village-monument-2 | -31..-31, 38..40, 61..61 | 3 | sky | (-31,35,61) walk 185 | 79% | 58% | 59% | 0 | 127 at (-2,34,-63), walk 49 | YES wool plus y57-59 (17 above top) |

**exp-slatefold-studio**

| objective | box x, y, z | float | setting | access cell (walk) | v30 | v60 | far 60-120 | prom. | first seen on the attackers' walk: distance, cell, walk | marker |
|---|---|---|---|---|---|---|---|---|---|---|
| red-blue-team [bridging] | -39..-38, 21..21, -71..-70 | 0 | roof | (-36,22,-69) walk 200 | 15% | 4% | 2% | -27 | 34 at (-7,21,-59), walk 164 | YES wool cube 3x3x3 y46-48 (25 above) |
| orange-blue-team [bridging] | 39..40, 21..21, -69..-68 | 0 | roof | (37,22,-67) walk 185 | 34% | 18% | 1% | -23 | 13 at (28,22,-63), walk 172 | YES wool cube 3x3x3 y46-48 (25 above) |
| blue-red-team [bridging] | 37..38, 21..21, 69..70 | 0 | roof | (35,22,68) walk 199 | 15% | 4% | 2% | -27 | 34 at (6,21,58), walk 163 | YES wool cube 3x3x3 y46-48 (25 above) |
| light_blue-red-team [bridging] | -41..-40, 21..21, 67..68 | 0 | roof | (-39,22,65) walk 184 | 34% | 18% | 1% | -23 | 13 at (-29,22,62), walk 171 | YES wool cube 3x3x3 y46-48 (25 above) |

## One paragraph per board: the worst objective

**riftwater.** The worst is the Market Square monument, red at (-66, 54..55, -44) (blue is the mirror at 65): v60 21% (v30 48%), floating one block over a paved square among houses on a bluff, prominence -10, no marker. The attackers (bridging; 165 moves) first see it 45 blocks away at (-21, 55, -41) after 123 moves, at the Old Bridge's foot; the Winding Green monuments (-66, 52..53, 48) are the opposite case, seen from 128 blocks from move 44 (v60 59%).

**hollow-mesa (before the move).** The worst is both cores: blue at (69..72, 49..52, 22..25), red at (-73..-70, 49..52, -26..-23): v60 **4%**, v30 24%, far 0%, setting underground (20 blocks of mesa over it), prominence -41, no marker. First seen at 16 to 19 blocks, at (57, 45, 15) after 159 of the 173 moves to the access cell (67, 47, 21). **After the move** (cores now at (63..66, 79..82, 22..25) and (-67..-64, 79..82, -26..-23), 5 above the headframe floor, sky): v60 **42%**, v30 83%, far 34%, prominence -11, first seen at 129 blocks at move 39 (from the near start of the walk). v60 up by 38 points, first sight 120 moves earlier; still no marker, and still sunk 11 below its surroundings.

**frostholm (before the move).** The worst is the core, red at (-18..-16, 75..77, -68..-66) (blue at 15..17, 75..77, 65..67), inside the glass lantern of the lighthouse under a roof of planks y80..83: v60 **9%** (10% blue), v30 22%, setting roof, first seen from 85 blocks at (35, 52, -4) at move 75 but not held to the end. **After the move** (core at (-29..-27, 57..59, -59..-57), over a stone-brick pit floor at y 48, open sky): v60 **30%**, v30 43%, prominence -25, first seen at 40 blocks at (5, 63, -37) after 125 of 161 moves. Better in v60 (+21) and v30 (+21) but the new place is 25 below its surroundings and is first seen late. After the move the worst objective is the Holmstein monument, blue at (57, 62..63, 19): v60 29% (v30 56%, prominence +4, 72 blocks first-seen at move 75).

**cloudhaven.** The worst is the lantern, red at (-72, 81..82, -60) (blue at 71, 81..82, 59): v60 31%, v30 73%, under a quartz roof y83..88 with a gold cap at y89 (not a marker), prominence -11, first seen at 123 blocks (move 76) but only held from 33. The Gardens objectives are v60 35%.

**hollowcrown.** The worst by far: all four are at 2% v60. The Echoes, red at (-66, 23..24, 16) and blue at (65, 23..24, -17), are underground (1568 blocks of stone over them), prominence -84, v30 21%, first seen only at 16 blocks at move 181 of 194. The Eyries at (-54, 106..107, -70) and (53, 106..107, 69) are on a crag in the open (sky, prominence +1) yet seen from 2% of the reached cells (v30 5%, 13% of all standable cells but few of them reached), and on the traced path never within 128 blocks. Walks use the lift model; the trace took one unverified step in each.

**stratum.** The worst is the Obelisk monument, blue at (54, 100..101, -50) (red -55): v60 **17%**, v30 6%, in a niche two blocks into the tower shaft at y 100 (a gold cap at y 121 on the shaft top, not a marker), prominence -20, first seen from 125 blocks at move 29 but held only from 3. The cores at (-57..-55, 81..83, 47..49) and (54..56, 81..83, 47..49) hang 29 and 60 blocks over a shaft (float): v60 30%, first seen at 29 blocks at move 134. All four are reached only by building.

**gullhaven-dtm.** The best board in the table: the worst objective is the harbour monument, red at (30..32, 22..24, 24..26) (a 3x3x3 gold block, 3 above the ground): v60 68%, v30 79%, first seen at 27 blocks (move 139); the beach monuments (-52..-50, 25..27, 7..9) are v60 78%.

**saltgate** (attack/defend, three stages). Not reached from the stage-1 attackers' spawn (0, 25, -62) by the modelled walk, even bridging: the West Powder Store at (-18, 27..28, 0), the East at (18, 31..32, 15) and the purple wool at (0, 35, 54) are all under stone-brick roofs; the audit has no number for them (upper bound from the standable cells: 1%, 5%, 5%). Not comparable with the others.

**cinder-reach.** The worst is both cores, blue at (48..52, 52..56, -27..-23): v60 27%, v30 45%, floating 8 over the fissure's lip in the open (sky), prominence 0, first seen at 121 blocks at move 14, held all the way; reached by bridging.

**redwash-mesa.** The worst is the wash monument, blue at (46, 43..44, 28) (red -47): v60 34%, v30 58%, 1 above the ground, prominence -15 (in a hollow), first seen from 128 blocks at move 1 but held only from 90; the table monuments (55, 64..65, -24) are v60 58%.

**cinderfall.** The worst is the core, red at (-50..-46, 65..69, -12..-8): v60 56%, v30 87%, 6 above the ground in the open, prominence +1, first seen at 107 blocks at move 15, held from 32. The most visible of the cores.

**tamarisk-wash.** The worst is the sunstone, blue at (62, 65..66, 21) (red -63): v60 20%, v30 39%, 2 above the ground, no hill, first seen only at 15 blocks at move 143 of 154; the obelisks (57, 74..76, -28) are v60 56%.

**exp-abbeymoor-pgmvox.** The worst is the village monument, red at (30, 70..72, -70) (blue -31, 70..72, 69): v60 22%, v30 44%, 3 above the ground in the open, prominence -10, first seen at 16 blocks at move 166 of 182, no marker. The abbey monuments (-40, 88..90, -72) are v60 38%, seen from 128 blocks at the start. (World measured at 02:24 UTC; the 02:05 version had different monument boxes.)

**exp-slatefold-pgmvox** (CTW). Not reached: the four wools at (60, 59, -68), (60, 59, 67), (-76, 83, -91), (-76, 83, 90) are not reached on foot or by any jump, and the map allows building over no void (`not-void` everywhere), so no v60 exists; the upper bound from standable front cells is 3 to 4%. The wool rooms are under stone-brick roofs 8 to 16 above. No marker.

**opus55b-russetford** (STUDIO). The worst is the monument, red at (4, 36..38, -56) (blue -5, 36..38, 55): v60 **55%**, v30 78%, 3 above the green, prominence +4, first seen at 128 blocks at move 7, **marker: yes**, a 7-block wool plus at y 56..58, 18 above the top.

**exp-abbeymoor-studio** (STUDIO). The worst is the village monument, blue at (-31, 38..40, 61) (red 30, 38..40, -62): v60 58%, v30 79%, 3 above the ground, first seen at 127 blocks at move 49; **marker: yes**, wool plus at y 57..59 (6 above the abbey monument, 17 above the village one). The abbey monument at (-24, 49..51, -69) is v60 64%.

**exp-slatefold-studio** (STUDIO, CTW). The worst is the wool in the blue-red room at (37..38, 21, 69..70) (red-blue at (-39..-38, 21, -71..-70)): v60 **4%**, v30 15%, a wool room under a plank roof, prominence -27, first seen at 34 blocks at move 163 of 199; reached by bridging over the build zone. **Marker: yes**, a 3x3x3 wool cube at y 46..48, 25 above each wool. The other two wools are v60 18%. A marker does not make the room visible from the ground; it makes it findable from the air.

## Before and after the two moves
| core | box before | v30 / v60 / far | setting, prom. | first seen | box after | v30 / v60 / far | setting, prom. | first seen |
|---|---|---|---|---|---|---|---|---|
| hollow-mesa red | -73..-70, 49..52, -26..-23 | 24% / 4% / 0% | underground, -41 | 19 at (-56,44,-15), walk 157 of 173 | -67..-64, 79..82, -26..-23 | 83% / 42% / 34% | sky, -11 | 129 at (62,75,-3), walk 39 |
| hollow-mesa blue | 69..72, 49..52, 22..25 | 24% / 4% / 0% | underground, -41 | 16 at (57,45,15), walk 159 of 173 | 63..66, 79..82, 22..25 | 83% / 42% / 35% | sky, -11 | 129 at (-63,75,2), walk 39 |
| frostholm red | -18..-16, 75..77, -68..-66 | 22% / 9% / 13% | roof, -7 | 85 at (35,52,-4), walk 75 of 193; not held | -29..-27, 57..59, -59..-57 | 43% / 30% / 6% | sky, -25 | 40 at (5,63,-37), walk 125 of 161 |
| frostholm blue | 15..17, 75..77, 65..67 | 22% / 10% / 12% | roof, -7 | 85 at (-36,52,3), walk 75 of 193 | 26..28, 57..59, 56..58 | 43% / 31% / 7% | sky, -25 | 40 at (-6,63,36), walk 125 of 161 |

The Hollow Mesa move took the cores from the least findable freeform objectives bar Hollowcrown (4%) to the middle of the table (42%); Frostholm's from 9% to 30%. Both still have no marker, and Frostholm's new core is the lowest-lying core in the table next to the Hollow Mesa one (prominence -25).

## Ranking of all objectives that the attackers' walk reaches, by v60 (lowest first)
| rank | board | objective | v60 | v30 | float | setting | marker |
|---|---|---|---|---|---|---|---|
| 1 | hollowcrown | red-echoes | 2% | 21% | 0 | underground | no |
| 2 | hollowcrown | blue-echoes | 2% | 21% | 0 | underground | no |
| 3 | hollowcrown | blue-eyrie | 2% | 4% | 0 | sky | no |
| 4 | hollowcrown | red-eyrie | 2% | 5% | 0 | sky | no |
| 5 | hollow-mesa | blue-core | 4% | 24% | 0 | underground | no |
| 6 | exp-slatefold-studio **(STUDIO)** | blue-red-team | 4% | 15% | 0 | roof | YES |
| 7 | hollow-mesa | red-core | 4% | 24% | 0 | underground | no |
| 8 | exp-slatefold-studio **(STUDIO)** | red-blue-team | 4% | 15% | 0 | roof | YES |
| 9 | frostholm | red-core | 9% | 22% | 0 | roof | no |
| 10 | frostholm | blue-core | 10% | 22% | 0 | roof | no |
| 11 | stratum | blue-obelisk | 17% | 6% | 0 | underground | no |
| 12 | stratum | red-obelisk | 17% | 6% | 0 | underground | no |
| 13 | exp-slatefold-studio **(STUDIO)** | light_blue-red-team | 18% | 34% | 0 | roof | YES |
| 14 | exp-slatefold-studio **(STUDIO)** | orange-blue-team | 18% | 34% | 0 | roof | YES |
| 15 | tamarisk-wash | blue-sunstone | 20% | 39% | 2 | sky | no |
| 16 | tamarisk-wash | red-sunstone | 20% | 39% | 2 | sky | no |
| 17 | riftwater | red-square | 21% | 48% | 1 | sky | no |
| 18 | riftwater | blue-square | 22% | 48% | 1 | sky | no |
| 19 | exp-abbeymoor-pgmvox | red-village | 22% | 44% | 3 | sky | no |
| 20 | exp-abbeymoor-pgmvox | blue-village | 22% | 44% | 3 | sky | no |
| 21 | frostholm | red-holmstein | 25% | 49% | 2 | sky | no |
| 22 | cinder-reach | blue-core | 27% | 45% | 8 | sky | no |
| 23 | frostholm | blue-holmstein | 27% | 49% | 2 | sky | no |
| 24 | cinder-reach | red-core | 27% | 45% | 8 | sky | no |
| 25 | frostholm-after | blue-holmstein | 29% | 56% | 2 | sky | no |
| 26 | stratum | red-core | 30% | 53% | 29 | sky | no |
| 27 | stratum | blue-core | 30% | 53% | 60 | sky | no |
| 28 | frostholm-after | red-holmstein | 30% | 56% | 2 | sky | no |
| 29 | frostholm-after | red-core | 30% | 43% | 8 | sky | no |
| 30 | frostholm-after | blue-core | 31% | 43% | 8 | sky | no |
| 31 | cloudhaven | red-lantern | 31% | 73% | 0 | roof | no |
| 32 | cloudhaven | blue-lantern | 31% | 74% | 0 | roof | no |
| 33 | redwash-mesa | blue-wash | 34% | 58% | 1 | sky | no |
| 34 | cloudhaven | red-gardens | 35% | 52% | 0 | sky | no |
| 35 | redwash-mesa | red-wash | 35% | 58% | 1 | sky | no |
| 36 | cloudhaven | blue-gardens | 35% | 53% | 0 | sky | no |
| 37 | exp-abbeymoor-pgmvox | red-abbey | 38% | 37% | 4 | sky | no |
| 38 | exp-abbeymoor-pgmvox | blue-abbey | 39% | 37% | 4 | sky | no |
| 39 | hollow-mesa-after | red-core | 42% | 83% | 5 | sky | no |
| 40 | hollow-mesa-after | blue-core | 42% | 83% | 5 | sky | no |
| 41 | opus55b-russetford **(STUDIO)** | red-monument | 55% | 78% | 3 | sky | YES |
| 42 | opus55b-russetford **(STUDIO)** | blue-monument | 56% | 78% | 3 | sky | YES |
| 43 | cinderfall | red-core | 56% | 87% | 6 | sky | no |
| 44 | cinderfall | blue-core | 56% | 87% | 6 | sky | no |
| 45 | tamarisk-wash | blue-obelisk | 56% | 67% | 2 | sky | no |
| 46 | tamarisk-wash | red-obelisk | 57% | 67% | 2 | sky | no |
| 47 | redwash-mesa | red-table | 58% | 68% | 1 | sky | no |
| 48 | redwash-mesa | blue-table | 58% | 68% | 1 | sky | no |
| 49 | exp-abbeymoor-studio **(STUDIO)** | village-monument-2 | 58% | 79% | 3 | sky | YES |
| 50 | exp-abbeymoor-studio **(STUDIO)** | village-monument | 59% | 78% | 3 | sky | YES |
| 51 | riftwater | red-green | 59% | 73% | 1 | sky | no |
| 52 | riftwater | blue-green | 60% | 73% | 1 | sky | no |
| 53 | exp-abbeymoor-studio **(STUDIO)** | abbey-monument | 64% | 84% | 2 | sky | YES |
| 54 | exp-abbeymoor-studio **(STUDIO)** | abbey-monument-2 | 65% | 84% | 2 | sky | YES |
| 55 | gullhaven-dtm | red-harbour | 68% | 79% | 3 | sky | no |
| 56 | gullhaven-dtm | blue-harbour | 68% | 78% | 3 | sky | no |
| 57 | gullhaven-dtm | red-beach | 78% | 81% | 3 | sky | no |
| 58 | gullhaven-dtm | blue-beach | 78% | 82% | 3 | sky | no |

Not reached by the attackers' walk (no v60; estimate from all standable cells in the front half within 60, not reached-filtered): saltgate west-store (est. 1%); saltgate east-store (est. 5%); saltgate purple-attackers (est. 5%); exp-slatefold-pgmvox orange-blue-team (est. 4%); exp-slatefold-pgmvox magenta-red-team (est. 4%); exp-slatefold-pgmvox cyan-blue-team (est. 3%); exp-slatefold-pgmvox yellow-red-team (est. 3%).

Reading (final versions of the boards, i.e. Hollow Mesa and Frostholm after their moves; 52 reached objectives: 42 non-studio, 10 studio):
- Median v60 is **55% for the studio boards** (10 objectives) and **31% for all the others** (42). 6 of 10 studio objectives and 12 of 42 others are at 50% or more.
- The studio marker is a sky beacon, not a line of sight: Slatefold-studio's four wool rooms carry a 3x3x3 wool cube and are still at v60 4% (two) and 18% (two), ranks 6, 8, 13 and 14 of 58. The studio boards with an open monument on a green or terrace (Russetford 55 to 56%, Abbeymoor-studio 58 to 65%) are near the freeform ones with the same layout.
- Freeform objectives at or above Russetford's 55%: Cinderfall's cores (56%), Tamarisk's obelisks (56 to 57%), Redwash's tables (58%), Riftwater's Winding Greens (59 to 60%), Gullhaven's harbours (68%) and beaches (78%). All stand on open ground, 1 to 6 blocks above it, with prominence of about -4 to +1.
- Below 20%: Hollowcrown's four (2%: two crag tops, two underground chambers), Stratum's two obelisk niches (17%), Tamarisk's sunstones (20%, a hollow with the viewer cells far), Slatefold-studio's four wool rooms. Before their moves, Hollow Mesa's cores were 4% and Frostholm's 9 to 10%.
- The two settings that produce the lowest numbers are the same on both sides of the comparison: a goal enclosed under a roof or in rock (Hollow Mesa before, Frostholm before, Hollowcrown's chambers, Slatefold's wool rooms) and a goal on a crag far from walkable ground (Hollowcrown's eyries).
