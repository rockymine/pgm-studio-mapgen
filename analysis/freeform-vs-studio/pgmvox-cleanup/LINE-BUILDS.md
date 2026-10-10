# Line builds and path steps: hand-built sites in board scripts

Measured over the board scripts at commit `968c71f8`, before any board moved onto `build.line_wall` or `route.halfsteps` (Tamarisk Wash aside). Line numbers are as of that commit.

All paths are relative to `freeform/`.
Boards named by directory. `lib/` = `freeform/lib`. Old copies (`gen_v1.py`, `gen_v3.py`) are folded into the row of the current file.

Shorthand: "plan raster" = the board's `R.K` / `R.H` / `R.stair` cell arrays; "ground per column" = height read per column (`P.g`, `H(L,x,z)`, `w.top`);
"fixed y" = one constant or a plan level for the whole run.

---------------------------------------------------------------------------------------------------------------------------------------------

## 1. Library call sites (functions that already exist)

| function | call site | what it is used for | arguments worth noting |
|---|---|---|---|
| `build.parapet` (build.py:492) | lib/trials/sonnet/cinderfall/scripts/gen.py:206 (in `houses`) | roof-edge parapet of foundry/hold footprint | y = eave+1; STONEBRICK or NETHER_BRICK; `crenel=COBBLE_WALL` for "hold", default rhythm `(x+z)%2==0` |
| `build.parapet` | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:133 (in `houses`) | roof-edge parapet of adobe/kasbah | y = eave+1; SANDSTONE data 2; `crenel=(SANDSTONE,1)` for kasbah only |
| `build.parapet` | lib/trials/sonnet/hoarfrost-reach/scripts/gen.py:201 (in `strand`) | a fence rail along a breakwater, abusing parapet with two 73-cell straight lines | fixed y 71, SPRUCE_FENCE, no crenel; both lines are 1 thick so `edge_cells` returns all of them |
| `build.parapet` | lib/ports/riftwater/scripts/works.py:107 (in `tower`) | battlement on a masonry tower roof | cells pre-filtered with `BLD.edge_cells`; STONEBRICK + `crenel=(SLAB,5)` |
| `build.edge_cells` (build.py:486) | lib/trials/opus/redwash-mesa/scripts/gen.py:131, :136; lib/ports/riftwater/scripts/works.py:107 | edge of a footprint (vigas, window frames; tower battlement) | not a line build |
| `route.pave` (route.py:230) | lib/examples/vale/scripts/gen.py:23 (bridges over `river.mask|sea.mask`), :25 (footpath, width 2) | roads | `water=` makes a plank deck with `rail=B.FENCE` each side |
| `route.pave` | lib/trials/sonnet/cinderfall/scripts/gen.py:173 | roads | `keep=lava|X>=0` |
| `route.pave` | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:92 (in `roads`) | roads; steep ghats are skipped here and rebuilt by `halfsteps` | water masked out of H, `keep=(X>=0)|water` |
| `route.pave` | lib/trials/opus/cinder-reach/scripts/gen.py:262 | roads | module level |
| `route.pave` | lib/trials/opus/redwash-mesa/scripts/gen.py:118 | trails | module level |
| `route.pave` | lib/ports/riftwater/scripts/works.py:385 (in `roads`) | every route; over the pond outlet a plank deck with `rail=(SPRUCE_FENCE,0)`, graded `level=` lambda, trestle legs added by the board after (works.py:389-394) | uses `Guarded` world wrapper to protect built columns |
| `route.pave` | lib/ports/lantern-karst/scripts/dress.py:107 | paths, `clear=0`, `wander(pts)` | |
| `route.steps` (route.py:261) | lib/examples/vale/scripts/gen.py:26 | footpath steps, width 2 | |
| `route.steps` | lib/boards/exp-abbeymoor-pgmvox/scripts/dress.py:568 (in `steps_on_slopes`) | Hill Track and Monks' Way, width 2 | |
| `route.steps` | lib/trials/sonnet/cinderfall/scripts/gen.py:176 | only when `kind == "road"` and `grade > 0.4`, width `min(width,3)` | |
| `route.halfstep_levels` / `route.halfsteps` | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:104, :117; test lib/tests/test_pgmvox.py:695, :704 | the two ghats in half blocks (slab on odd level), no stair blocks | `GHAT_BLOCKS` = 2 sandstone data, `GHAT_SLAB=(SLAB,1)`, fill sandstone |
| `props.crop_field` fence (props.py:216, fence at the end of the z loop) | lib/ports/riftwater/scripts/dress.py:74 | `fence="w"`, gate in the middle row (default) | fence y follows the field's tilted plane (`yz+1`); one side only; gate = FENCE_GATE |
| `build.stairs` (build.py:529) | lib/trials/opus/redwash-mesa/scripts/gen.py:103; lib/ports/riftwater/scripts/works.py:160 | straight flight, width 3, `under=` fill | |
| `forms.masonry_tower` crown `crenel=` (forms.py:133) | lib/trials/sonnet/overgrowth/scripts/gen.py:214 (COBBLE_WALL data 1); lib/trials/sonnet/tamarisk-wash/scripts/gen.py:166 (SANDSTONE 2); lib/trials/sonnet/cinderfall/scripts/gen.py:268 (default) | tower crown crenel | |
| facade `top="parapet"` / `"parapet-slotted"` (`Fa.build` / `F.extrude`, facade.py `top_course`) | opus55-freeform-stratum/scripts/buildings.py:195, :266, :355, :404, :452; lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:116; lib/trials/sonnet/tamarisk-wash/scripts/gen.py:198 (serai); lib/examples/parts/scripts/gen.py:41 | parapet on a polygon mass; slotted = every third cell open | |
| `under.gallery` (under.py:157) | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:337; lib/trials/opus/redwash-mesa/scripts/gen.py:151; lib/ports/riftwater/scripts/under.py:112 | tunnel with a stair at every rise, fence rail posts | the 3D path-stairs case underground |
| `props.lamps` | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:421 | posts every 13 cells at side 3.2 along a route | a "posts along a line" cousin |
| `forms.skirt` | lib/boards/exp-slatefold-pgmvox/scripts/gen.py:62; lib/boards/exp-abbeymoor-pgmvox/scripts/gen.py:58 | rock skirt under an island edge | not a line build; listed only because the task named it |

No board outside `lib/pgmvox` calls `build.parapet` with a polyline; every use passes a cell set.

---------------------------------------------------------------------------------------------------------------------------------------------

## 2. Hand-built line builds (wall / hedge / fence / parapet / railing / kerb)

### 2a. Walls, hedges and fences laid on polylines or polygon edges over the ground

| board | file:line | function | kind | follows ground | laid along | materials | height & width | gaps/gates | notes |
|---|---|---|---|---|---|---|---|---|---|
| exp-abbeymoor-pgmvox | lib/boards/exp-abbeymoor-pgmvox/scripts/dress.py:329 (loop :333-339; callers :347, :350) | `walls_along` | wall | ground per column: `P.g(x,z)+1`; skips non-land, wet and occupied cells | polyline, walked cell by cell (`shapes.walk_cells`); callers pass a 60-point circle ring and two copies of Drove Road offset +-5 | COBBLE_WALL; data 1 (mossy) with p=0.2 from `r` | 1 high, 1 wide | gap list: each gap point opens a 3x3 (Chebyshev 1); ring has one gate, each road wall two | random mossy mix; wall blocks join themselves, no corner code; the only polyline wall helper in any board |
| exp-slatefold-pgmvox | lib/boards/exp-slatefold-pgmvox/scripts/gen.py:67 (loop :73-84) | `retaining_walls` | wall (retaining) | fills from the lower neighbour's floor+1 up to h-1; face height = plan floor drop (>=2) | raster cells whose 4-neighbour is walkable and >=2 lower | STONEBRICK data 0 (80%), 2 (15%), 1 (5%) random | drop-1 high (>=1), 1 wide | none | returns a count; one pass per direction |
| exp-slatefold-pgmvox | lib/boards/exp-slatefold-pgmvox/scripts/gen.py:88 (rail loop :103-112) | `flights` | railing | y of stair cell +1 | raster: stair cells whose across-climb neighbour is lower by >=1 or void | COBBLE_WALL | 1 high | none | wall only on the lower side; breaks after first hit |
| exp-slatefold-pgmvox | lib/boards/exp-slatefold-pgmvox/scripts/dress.py:301 | `rails` | railing | plan height of landing cell +1 | raster edge: landing cells with a void neighbour | SPRUCE_FENCE | 1 high | none | only if the cell above is air |
| exp-slatefold-pgmvox | lib/boards/exp-slatefold-pgmvox/scripts/dress.py:360-371 (in `cover_and_dressing` :349) | (inline) | wall (3 cells) | fixed y YARD_H+1 | straight x range, hard-coded | COBBLE_WALL, STONEBRICK | 1-2 high | none | weighbridge hut, minor |
| claywork | lib/boards/claywork/scripts/gen.py:192-198 (module level) | (none) | parapet | plan floor per column (`R.floor[i,k]`) | raster mask "parapet" | BRICK at floor+1, SLAB data 5 at floor+2 | 2 high, 1 wide | none | red half only, turn copies it |
| curio | opus55-freeform-curio/scripts/gen.py:133 (loop :136-158) | `wall` | wall (curtain, crenellated) + gates | flat board: y from G (const) to Y+8 | square ring `+-P.WALL`, four sides by `for k` | STONEBRICK; data 2 where `(3x+y+5z)%9==0` | 8 high, 1 thick (+ a 2-wide inner walk to Y+6 outside) | gates: 5 wide at the midpoint of each side, iron bars Y..Y+4, brick above, towers at k=+-3 up to Y+13 | crenel at Y+8 where `k%2==0`; walk block placed in a loop over `t in (1,2)` |
| curio | opus55-freeform-curio/scripts/gen.py:79-83 (in `square` :70) | `square` | kerb | fixed y G | rectangle ring around each plot (`P.plots()`) | DSLAB data 0 | 1 high, 1 wide | none | a per-plot kerb, ring includes corners |
| hollowcrown | opus55-freeform-hollowcrown/scripts/buildings.py:188 (loop :195-218) | `crownhold` | wall (curtain) | wall column fill from `H-3` up to y+8, y=98 fixed crown | polygon `inset(P.CROWN,2.5)`, each edge rasterised with `thick_line_cells(width 1.0)` | STONEBRICK, 15% data 1, 10% data 2; course at y+4 is STONE data 6 | to y+8, thickness 1 | gates = cells within 1.6 of the wall cell nearest each route end (two gates); air y+1..y+4, iron bars y+5 | crenel at y+8 where `(x+z)%2==0` and not a gate; round tower at every vertex (`round_tower`), banner fences atop |
| hollowcrown | opus55-freeform-hollowcrown/scripts/buildings.py:439 (loop :480-491) | `wendholm` | parapet (low road-edge wall) | ground per column: `H(F,x,z)+1` | raster: road cells with a neighbour >=3 lower and not occupied | COBBLE_WALL | 1 high | none | one block per cell, `break` after first neighbour |
| hollowcrown | opus55-freeform-hollowcrown/scripts/buildings.py:534 (:548-549) | `kingsbridge` | parapet | arched deck: `deck = 44+2 sin(...)`, wall at deck+1 | two straight edge lines z=-3 and z=2 for x in x0..-1 | COBBLE_WALL | 1 high | none | deck, arch and wall in one loop over x |
| hollowcrown | opus55-freeform-hollowcrown/scripts/buildings.py:601 (:620-622) | `fields` | fence | field level y (median of its cells) | edge cells of a rotated polygon mask (cell with a missing 4-neighbour) | FENCE on GRASS | 1 high | none (the "gate" is a farmhouse, not a gap) | field rotated to the polygon's first edge |
| hollowcrown | opus55-freeform-hollowcrown/scripts/terrain.py:299 (in `write`) | `write` | wall (retaining) | column fill from `top-down+1` to top | raster: town cells where `H - min(4-neighbour) >= 3` | STONEBRICK, data 1 (25%), 2 (15%), else 0 | drop high | none | hand-rolled in a per-column painter |
| hollowcrown | opus55-freeform-hollowcrown/scripts/buildings.py:783 | `mine_road` | other: posts across a path every 4 cells | `route_y` per cell | walked path cells, perpendicular posts at +-2 | FENCE x3 high at both sides + PLANKS beam at y+4 | 3 high | skipped where the cell is tunnel floor | not a continuous line |
| gullhaven | opus55-freeform-gullhaven/scripts/gen.py:403 (loop :406-436); old copy gen_v1.py:323 | `cover` | hedge AND wall | ground per column `g(x,z)`; height = plan `R.H - g` (plan states each cell's height) | raster: cells within 0.75 of a polyline from `P.HEDGES` and `P.WALLS` where plan kind is "cover" | hedge LEAVES data 4; wall COBBLE 60% / MOSSY_COBBLE 40% random | plan-stated, hedge/wall 1 wide (+-0.75) | none in the code (gaps are in the plan lines) | the same loop also builds stones, crates, driftwood by kind |
| gullhaven | opus55-freeform-gullhaven/scripts/gen.py:94 (:127-132); old copy gen_v1.py:94 | `columns` | wall (retaining / sea wall) | from the lowest non-sea 4-neighbour to h-1 (`low`); sea wall 6 courses deep when next to sea and h-SEA>4 | raster street/quay/ramp cells | SBRICK with MOSSY_BRICK where `y<low+2` or 15% random; sea wall mossy where `y<h-4` or 20% | drop high | none | face is a column fill, not a separate pass |
| riad | opus55-freeform-riad/scripts/gen.py:189-192 (in `columns` :128) | `columns` | hedge | `floor_h` (G or LOW) | raster cells of plan kind "hedge" | HEDGE = LEAVES data 4 | 2 high, 1 wide | none | one cell wide strip rasterised from the plan |
| riad | opus55-freeform-riad/scripts/gen.py:209 | `parapets` | parapet | plan height h per column, +1 and +2 | raster: floor/hedge/tree cells with an outer-void 4-neighbour; excludes three zones by coordinates | RED_SMOOTH or team wool where `(x+z)%4==0 and \|z\|>16`; QUARTZ_SLAB on top | 2 high | zone exclusions only | crenel `(x+z)%2==0`; wool inlay every 4th. gen_v1.py:168 `edges` is the older fence-on-coping variant |
| cloudhaven | opus55-freeform-cloudhaven/scripts/buildings.py:286 (hedge :308-311) | `sunken_garden` | hedge | flat (levelled) y+1 | square ring at Chebyshev radius 6 around the monument | LEAVES data 4 | 1 high | 3 wide gap at each side's middle (`min(\|dx\|,\|dz\|) > 1` only) with a stair flight in it (:312-321) | stairs: 3 steps, STONEBRICK_STAIRS, data per side 1/0/3/2 |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/dressing.py:463 | `hedgerows` | hedge | ground per column `H(L,X,Z)`; only on GRASS with air/grass above | spline of the Farm Track, offset +2, sampled per spline point | LEAVES data 4; second block when `i%3==0` | 1-2 high | skips spline index `i%13 in (0,1)` (a 2-cell gap every 13) | gap rhythm by index, random-free |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/dressing.py:145 (fence :178-184) | `wheat_field` | fence | `L.H` per column (already tilted by the field loop) | straight line along the field's west edge, z0..z1 | FENCE; FENCE_GATE data 1 | 1 high | gate at `(z0+z1)//2` | the library `props.crop_field` does the same (port uses it) |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/dressing.py:380 (:393-399) | `gardens` | fence | `H+1`, only if `abs(g - floor) <= 1` | rectangle ring around a 4-wide plot behind each cottage | SPRUCE_FENCE | 1 high | none | farmland+crops inside; water source |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/buildings.py:368 (:386-390) | `watch_house` | wall (terrace) | fixed y 60 | three rectangle sides, west side open at z -8..-6 | COBBLE_WALL | 1 high | 3-cell gap where the stairs come up | lib/ports/riftwater/scripts/works.py:151-155 repeats it |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/buildings.py:472 (:481-483) | `footbridge` | railing | deck y per z (eases down south) | straight, both x edges | SPRUCE_FENCE (+ torch every 8) | 1 high | none | deck LOG edges |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/buildings.py:560 (:585-589) | `old_bridge` | parapet | deck fixed per bridge | two straight edge lines z=zc+-3 | STONEBRICK + SLAB data 5 on top | 2 high | ragged: broken with p=0.6 in the last 2 cells | port: lib/ports/riftwater/scripts/works.py:249 (:265-268) |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/buildings.py:500 (:540-546) | `stone_bridge` | parapet | deck + 1 / +2 following the stepped crown | two straight edge lines x0 and x1 for z in zN..zS | STONEBRICK + SLAB 5 | 2 high | none | port: works.py:206 (:230-236) |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:709 (walls :718-724; walk :734-738; tower rail :761-766) | `fort` | wall (curtain) + railing | fixed y `floor_of(...)` | rectangle ring -113..-97 x -8..16 | SANDSTONE data 0 at y+1, data 2 y+2..y+4; WOOD_SLAB (1\|8) inner walk at y+3; SPRUCE_FENCE ring at tower y+10 | 4 high + crenel, 1 thick | gate 5 wide on the east side (z 2..6), LOG lintel and jambs | crenel y+5 where `(x+z)%2==0` |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:786 (:795-799) | `rancho` | fence (corral) | `H(L,x,z)+1` per column | rectangle ring | FENCE | 1 high | 3-cell gap on the east side (`abs(z-mid)<=1`) | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/dressing.py:173 (:178-182) | `cemetery` | fence | `H+1` per column | rectangle ring 8x7 | SPRUCE_FENCE | 1 high | gate cell at east middle | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/dressing.py:191 (:203-208) | `hitching` | fence (rail) | `H(L,X,z)+1` | straight 6-cell line in front of doors | FENCE | 1 high | skips the door row | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:695 | `tank` | wall (ring) | `g+1` | circle, band `r <= d < r+1` | COBBLE_WALL | 1 high | none | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:370 (:380-390) | `spring` | kerb | fixed y FLOOR_Y+1 | circle band `5.2 <= d < 6.3` | SLAB data 1 | half block | skipped where the creek / canyon is within 2.2 | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:498 (:504-505) | `trestle` | railing | fixed y BENCH_Y+1 | per tram cell, posts at x+-2 | DARK_OAK_FENCE on LOG2 | 1 high | none | plus deck 3 wide of PLANKS; bents every 4th cell |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/underground.py:93 (rail :108-113) | `catwalk` | railing | fixed y 50 | two straight runs (N and E walls) | DARK_OAK_FENCE | 1 high | on the open side only (when the cell below is air) | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:220 (:241-243, in nested `box`) | `adobe` | parapet | flat roof | rectangle ring | SANDSTONE 2 | 1 high | gaps "for the rain": absent where `(x+z)%5 == 0` | the only parapet with a gap rhythm |
| calcite | opus55-freeform-calcite/scripts/gen.py:308 (loop :310-313); old copy gen_v3.py:280 | `rails` | railing | fixed y 14 | straight, hard-coded x -23..-12, z=-3 and z=2, plus `P.rot` copy | IRON_BARS | 1 high | none | |
| copperline | opus55-freeform-copperline/scripts/gen.py:381 (:387-389; footbridge :402-407) | `trestle` | railing | fixed y+1 | straight, both edges x0 / x1 of the deck | SPRUCE_FENCE | 1 high | none | footbridge uses FENCE one block outside the deck |
| copperline | opus55-freeform-copperline/scripts/gen.py:553 (walkway :577-583) | `gantry` | railing | fixed y+1 | straight z -49..-33, both edges x=2 and x=6 | SPRUCE_FENCE over DARK_OAK edge beams | 1 high | none | |
| frostholm | opus55-freeform-frostholm/scripts/buildings.py:425 (:445-447) | `bridge` | railing | deck = `y0 + (y1-y0)t + 2.2 sin(pi t)` per x | straight along x at dz=+-2 | SPRUCE_FENCE on LOG | 1 high | none | arched deck; bents every 4th |
| frostholm | opus55-freeform-frostholm/scripts/buildings.py:264 (:285-292) | `beacon` | parapet | fixed gallery top | circle band `5.6 < d <= 6.4` | STONEBRICK + SLAB 5 | 2 high | gaps where `angle mod 45 <= 6` | rhythm by angle, round tower |
| frostholm | opus55-freeform-frostholm/scripts/buildings.py:592 (:611-613) | `landing_stage` | railing | deck y per z | straight, only on water cells at x+-2 | SPRUCE_FENCE | 1 high | none | |
| lanternpass | opus55-freeform-lanternpass/scripts/gen.py:538 (:541-547) | `walkways` | wall (gallery wall) | height table `HW[z]`, +1..+5 | straight in z at `outer +- 1` | RED_CLAY post every 8, WHITE_CLAY / BLACK_CLAY cap | 5 high | ends closed by a wall across | lantern every 16; stairs in same loop (section 3) |
| lanternpass | opus55-freeform-lanternpass/scripts/gen.py:254 (:279-289) | `harbour` | railing | fixed y 21 / 21 | straight z 5..60 at x=-12 and x=11 | SPRUCE_FENCE every 4th; COBBLE_WALL every 3rd | 1 high | by index only | posts, not a continuous line |
| lanternpass | opus55-freeform-lanternpass/scripts/gen.py:421 (:426-427) | `gorge` | railing | per-z `h(x,z)` | straight rope edges | FENCE at plank level | 1 | none | "ropes" |
| lanterndrop | opus55-freeform-lanterndrop/scripts/gen.py:236 (:255-259) | `harbour` | kerb (quay rim) | fixed `hy+1` | ellipse band `1 < v <= 1+2.6/min(rx,rz)` | SBRICK; COBBLE_WALL + GLOWSTONE lamp where `(x+z)%7==0` | 1 high (lamp 3) | none | lamp rhythm by `(x+z)%7` |
| penstock | opus55-freeform-penstock/scripts/gen.py:245 | `rails` | railing | fixed y 28 | raster edge of every deck cell with a drop, minus flights and joins | IRON_BARS | 1 high | cleared where a flight meets (:268-281) | mirrors the west half (`deck[::-1]`) |
| penstock | opus55-freeform-penstock/scripts/gen.py:326 (nested in `cover` :318) | `low_wall` | wall | fixed y 21 | axis-aligned rectangles, 16 calls | STONEBRICK, SLAB 5 cap | 2-3 high | none | |
| saltgate | opus55-freeform-saltgate/scripts/gen.py:266 (:269-272, :283-287); old copy gen_v1.py:170 | `sea_wall` | parapet (crenels only) | fixed y 29 | straight at z=-31 where kind is rampart; tower edges via raster | SBRICK | 1 | gate passage -3..2 | crenel `x%2==0` or `(x+z)%2==0` |
| saltgate | opus55-freeform-saltgate/scripts/gen.py:359 (:362-364); 379 (:388-393) | `citadel`, `keep` | parapet (crenels) | fixed y 45; fixed y 51 / 55 | straight line z=23; rectangle ring | SBRICK | 1 | | `x%2==0`; `(x+z)%2==0` |
| saltgate | opus55-freeform-saltgate/scripts/gen.py:244 (:254-258) | `landing` | railing | fixed y 22 | straight z=-50 and the two ends | SPRUCE_FENCE | 1 | gaps at each ship's cx-1..cx+1 (gangplanks) | |
| sunwell | opus55-freeform-sunwell/scripts/gen.py:184 | `rims` | wall (low) | fixed y per shelf | straight z=+-EDGE, x -R..R | MOSSY_WALL | 1 high | per-shelf gap list `P.gaps(k)` | the cleanest "wall with named gaps" |
| stratum | opus55-freeform-stratum/scripts/facade.py:201 | `top_course` | parapet | mass top y1+1 | edge cells of a mass | SMOOTH | 1 | "slotted": `(x+z)%3 == 0` open | library-like |
| stratum | opus55-freeform-stratum/scripts/buildings.py:164 (:183-184) | `skyway` | parapet | deck graded linearly y0..y1 along the polyline | 5-wide beam along a polyline (`G.polyline`), edge = `d > half-0.5` | SLAB data 0 on edge cells | 1 high | absent at both ends (`0.04 < t < 0.96`) | deck is a graded path surface, see section 3 |
| loomfall | opus55-freeform-loomfall/scripts/gen.py:66 (:78-79) | `house` | parapet | `g+hgt+1` | rectangle edge | SMOOTH | 1 | crenel `(x+z)%2==0` | |
| brittle-study | lib/boards/brittle-study/scripts/style.py:50 (called gen.py:115-118) | `kerbed_bed` | kerb | fixed y | rectangle ring (box) | SANDSTONE_STAIRS facing inward on edges, SANDSTONE at corners | 1 | none | stair facing = toward the box centre (:61) |
| brittle-study | lib/boards/brittle-study/scripts/style.py:22 (called gen.py:104) | `face` | other: platform edge trim | per column, 5 courses down | raster edge columns | upside-down SPRUCE_STAIRS, BRICK, DARK_OAK_SLAB, ... | 5 down | | stair facing `S.OPP[out]` |
| hoarfrost-reach | lib/trials/sonnet/hoarfrost-reach/scripts/gen.py:68 (:83-91) | `surface` | railing | plan floor | raster: deck cells with a non-land neighbour | SPRUCE_FENCE | 1 | | `break` after first |
| hoarfrost-reach | lib/trials/sonnet/hoarfrost-reach/scripts/gen.py:113 (:126-127) | `glacier_bridge` | railing | fixed HALL_Y+1 | straight z -51..-66, x0 and x1 | COBBLE_WALL | 1 | | |
| overgrowth | lib/trials/sonnet/overgrowth/scripts/gen.py:169 (:181-189) | `courts` | wall (court wall) + crenel | fixed COURT_Y | rectangle ring | `stonework(r)` mix | 6 high + slab on `(x+z)%2` | gate cell set `gate_cells` | |
| overgrowth | lib/trials/sonnet/overgrowth/scripts/gen.py:241 | `perimeter` | wall (board edge) | per-column `L.H-2 .. +6` | raster board-edge ring, 2 thick | `stonework` mix; COBBLE_WALL data 1 at top | 9 | none | crenel `(i+k)%2==0` |
| overgrowth | lib/trials/sonnet/overgrowth/scripts/gen.py:220 | `bridges` | railing | plan H | raster: bridge cells with a non-bridge x neighbour | JUNGLE_FENCE; second block where `z%6==0` | 1-2 | | |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:281 (:284-296) | `quay` | wall | fixed QUAY | rectangle ring | WHITE / BLUE every third course; SLAB 7 | 6 high + slab | gate cells (plan kind "gate") | |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:303 (:306-315) | `garden_and_dock` | wall | fixed GARDEN | rectangle ring | same as quay | 6 | gate cells | |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:356 | `rim` | parapet/rail | plan `R.h` | `shapes.boundary(plate)` | SLAB 7; IRON_BARS where `(x+z)%3==0` | 1-2 | | |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:139 (:152-156) | `court` | parapet | fixed TOWN | edge ring of the court | SLAB 7 | 1 | open on kind != "ring" | |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:168 (:172-203) | `cover` | hedge/barricade/low wall | plan rect heights | plan rectangles | hedge LEAVES data 7; barricade PLANKS + SPRUCE_FENCE top; lowwall STONE | per-plan height | | rectangles, not lines |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:106 (:121-131) | `blocks` | railing | fixed 74 | straight lines x=-36 and x=-32, z -3..2 | SPRUCE_FENCE | 1 | ends open | |
| tamarisk-wash | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:285 (:292-295) | `aqueduct` | parapet | fixed DECK_Y+1 | two straight edge lines z0, z1 | COBBLE_WALL | 1 | every second x only (`x%2==0`), none near the ragged end | |
| tamarisk-wash | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:190 (:197-198, :221-223) | `serai` | parapet (library `F.extrude top="parapet-slotted"`) + hand gap | roof of the ring | ring cells of the serai | SANDSTONE data 1 | 1 | 4 cells cleared by hand where the stair meets the roof (:222-223) | the only place a library parapet is opened by a board |
| cinder-reach | lib/trials/opus/cinder-reach/scripts/gen.py:268-275 (module level) | (none) | railing/parapet | fixed TERRACE_Y+1 | rectangle edge on 3 sides (z0, z1, x0) | BRICK; FENCE where `(x+z)%4 == 0` | 1 | | alternating blocks |
| cinder-reach | lib/trials/opus/cinder-reach/scripts/gen.py:313-320 | (none) | fence | `hwall(x,z)+1` per column | edge of a 4x5 plot | DARK_OAK_FENCE | 1 | none | |
| redwash-mesa | lib/trials/opus/redwash-mesa/scripts/gen.py:104-108 | (none) | railing | `y0+kk` per step | beside the stairs, x = fx+-2 | SANDSTONE data 2 | 1 | only where the cut is open | stair-side wall |
| brassmoor-works | lib/trials/opus/brassmoor-works/scripts/gen.py:200-203 | (none) | wall | fixed 67 | rectangle ring around the pit, only on kind "yard" | COBBLE_WALL | 1 | | |
| tidewell-canals | lib/trials/opus/tidewell-canals/scripts/gen.py:86-91 | (none) | kerb (coping) | fixed S | raster: street/campo cells with a canal / lagoon neighbour | ISTRIAN = (STONE,4) | 0 (replaces the surface course) | | |
| tidewell-canals | lib/trials/opus/tidewell-canals/scripts/gen.py:150-158 | (none) | railing | fixed GALLERY+1 | straight x range along the front edge | SPRUCE_FENCE | 1 | | |

### 2b. Prepared-line walls (bedrock + cobweb capture lines), the same recurring structure

| board | file:line | function | follows ground | laid along | materials | height | notes |
|---|---|---|---|---|---|---|---|
| claywork | lib/boards/claywork/scripts/gen.py:204-206 | (module) | from y=1 to `floor + WALL.height` | raster "barrier" | BEDROCK | to floor+height | down to world floor |
| exp-slatefold-pgmvox | lib/boards/exp-slatefold-pgmvox/scripts/dress.py:270 (`bedrock_walls`) | | column's rock foot to plan top | raster "barrier" | BEDROCK | | |
| lantern-karst (opus55) | opus55-freeform-lantern-karst/scripts/buildings.py:518 (`store_wall`) | | `floor_y(F,x,z)` per column | rectangle x0..x1, z and z-1 | BEDROCK x3, COBWEB at +4 | 4 | |
| lantern-karst (port) | lib/ports/lantern-karst/scripts/dress.py:407 (`store_wall`) | | `g.at(x,z)` per column | box | BEDROCK `height` courses + COBWEB | `height`+1 | |
| brassmoor-works | lib/trials/opus/brassmoor-works/scripts/gen.py:162-168 | (module) | plan floor of the piece | boxes `P.WALLS` | BEDROCK x3 + COBWEB | 4 | |

---------------------------------------------------------------------------------------------------------------------------------------------

## 3. Path surfaces with steps: stairs / slabs where a path climbs, and flights

### 3a. Along a path or route (the "route.steps / route.pave" family)

| board | file:line | function | kind | follows ground | laid along | materials | width | gaps | notes (facing, diagonals, special) |
|---|---|---|---|---|---|---|---|---|---|
| hollowcrown | opus55-freeform-hollowcrown/scripts/buildings.py:847 (calls :885, :886) | `path_steps` | path stairs | ground per cell `H(F,cx,cz)` | `walk_cells` of a 3D route | COBBLE_STAIRS | 1 | skips cx>=0 and cells already air/water | facing from the step vector `{(1,0):0,(-1,0):1,(0,1):2,(0,-1):3}` of **travel direction**; only ascending steps (`y == prev+1`) get a stair; diagonals are not in the table so they get none; it replaces the ground block at y |
| exp-abbeymoor | lib/boards/exp-abbeymoor-pgmvox/scripts/dress.py:564 | `steps_on_slopes` | path stairs (library call) | | | | 2 | | route.steps, shown in section 1 |
| gullhaven | opus55-freeform-gullhaven/scripts/gen.py:375 (:385-395) | `bridges` | path stairs on a bridge deck (+ fence rail :396-400) | plan deck level `R.U` per cell | raster cells within `half+1` of the polyline | stair id 134 (spruce stairs) data `sd` toward the lower neighbour, else SPRUCE planks | 2*half+1 | | stair facing = direction of the neighbour with `U == u-1`; trestle logs every 4th along-index |
| lanternpass | opus55-freeform-lanternpass/scripts/gen.py:538 (:549-556) | `walkways` | path stairs | height table `HW[z]` | straight in z, full width x0..x1 except the wall cell | STONEBRICK_STAIRS data 2 (rising +z) or data 3 | walkway width | | up-step: stair at hh on this z; down-step: stair at prev height on z-1, data 3 |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/buildings.py:500 (:529-535) | `stone_bridge` | path stairs on deck | stepped crown `deck_y(z)` | straight in z, 5 wide (x -38..-34) | STONEBRICK_STAIRS data 2 / 3 over STONEBRICK | 5 | | stair at dy+1 where `nxt > dy` (z<1) or `prev > dy` (z>1); parapets lifted one block there |
| riftwater (port) | lib/ports/riftwater/scripts/works.py:206 (:225-227) | `stone_bridge` | same, via `stair("s"/"n")` | | | | | | |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/buildings.py:368 (:391-405) | `watch_house` | flight, under-filled | `top(w,-78,-7)` to floor | straight 3 wide, going west | STONEBRICK_STAIRS data 1 over STONE | 3 | | the port replaces it with `BLD.stairs` (works.py:160) |
| riftwater (opus55) | opus55-freeform-riftwater/scripts/underground.py:183 (:210-222) | `mine` | path stairs in a tunnel | 3D path, floor changes by +-1 | clean 3D polyline, 3 wide | COBBLE_STAIRS | 3 | | facing from the step to the neighbour along x or z; library `under.gallery` is the same code, port uses it |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/underground.py:134 (:160-166) | `gallery` | path stairs in a tunnel | | | COBBLE_STAIRS | `width` | | same as above, hand-written duplicate |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/underground.py:93 (:117-123) | `catwalk` | flight down | | straight, 2 wide | SPRUCE_STAIRS data 0 | 2 | | |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:599 (inner `flight` :602-620) | `mule_trail` | path stairs on a cliff | y rises 1 per cell along z | `x_of(z)` curve, 2 wide, with air above and clay fill below | RED_SANDSTONE_STAIRS data 3 or 2 (by `dirz`) over RED_SANDSTONE | 2 | | rail: DARK_OAK_FENCE at x+1,y+2 if open; every cell rises by one |
| hollow-mesa | opus55-freeform-hollow-mesa/scripts/buildings.py:518 (:546-560) | `tipple` | switchback flight | | inside a tower, back and forth | SPRUCE_STAIRS data 0 / 1 | 2 | | |
| stratum | opus55-freeform-stratum/scripts/buildings.py:62 | `wound_stair` | path steps on a ring | y rises 1 per non-corner cell | ring path of a rectangle shaft | `mat=(DSLAB,8)`, STONEBRICK_STAIRS via `stair_dir(next-cur)` on non-corners | 1 | | corners are landings; air cleared 3 above; the "path" is a closed ring |
| stratum | opus55-freeform-stratum/scripts/buildings.py:164 | `skyway` | graded path surface (no steps) | linear y0..y1 | polyline beam 5 wide | | 5 | | the deck's height is the continuous `along/L`, rounded |
| tamarisk-wash | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:102-120 (ghats) | `ghat_levels`, `ghats` | path slabs (half block steps) | graded profile `rt["profile"]` relaxed to <= 1 half block between 4-neighbours | route band `d <= width/2`, minus earlier ghats | SANDSTONE data 0/2 random + SLAB data 1 on odd levels, fill SANDSTONE | route width | | no stair blocks, so no diagonal facing problem. The library route.halfsteps (route.py:333) now holds the loop |
| lantern-karst | opus55-freeform-lantern-karst/scripts/terrain.py:160 (`joins`); port lib/ports/lantern-karst/scripts/dress.py:118 | `joins` | steps between raster pieces: 1 block = SLAB 5; 2 blocks = two STONEBRICK_STAIRS (y+1 and next cell y+2); more = wall | | runs of cells along each join, grouped `along` | STONEBRICK_STAIRS data by direction `(1,0):0,(-1,0):1,(0,1):2,(0,-1):3` | run, but max 10 stairs per run longer than 14 (middle only) | | opus55: handles d==1, 2 only; port: plan stair cells + slab on low side of 1-block steps |
| exp-abbeymoor | lib/boards/exp-abbeymoor-pgmvox/scripts/crypt.py:63, :90 | `night_stair`, `passage` | tunnel steps | floor per x | x runs, 3 wide | STONEBRICK_STAIRS `stair_data("e"/"w")` at floor changes | 3 | | stair where `y != prev` |
| tidewell-canals | lib/trials/opus/tidewell-canals/scripts/gen.py:76-84 | (module) | stairs onto a bridge | raster H | cells where a neighbour is h+1 and kind bridge | STONEBRICK_STAIRS facing the neighbour | 1 | | |

### 3b. Flights laid on the plan's stair cells (one stair block per cell, facing read from `R.stair`)

| board | file:line | function | materials | notes |
|---|---|---|---|---|
| exp-slatefold-pgmvox | lib/boards/exp-slatefold-pgmvox/scripts/gen.py:88 | `flights` | STONEBRICK_STAIRS over a 6-deep mass, air 4 above | side wall rail (see 2a) |
| hoarfrost-reach | lib/trials/sonnet/hoarfrost-reach/scripts/gen.py:94 | `flights` | QUARTZ_STAIRS / STONEBRICK_STAIRS over ice/brick | |
| overgrowth | lib/trials/sonnet/overgrowth/scripts/gen.py:160-166 (tiers); :199-205 (courts) | `tiers`, `courts` | STONEBRICK_STAIRS over BRICK / MOSS | |
| whitecliff-cistern | lib/trials/sonnet/whitecliff-cistern/scripts/gen.py:226 | `stairs` | SANDSTONE_STAIRS over PALE | two storeys |
| brassmoor-works | lib/trials/opus/brassmoor-works/scripts/gen.py:77-82 | (module) | STONEBRICK_STAIRS, deck fill below, bedrock at the bottom | |
| tidewell-canals | lib/trials/opus/tidewell-canals/scripts/gen.py:63-66 | (module) | STONEBRICK_STAIRS, always data "e" | |
| vinewatch-ruins | lib/trials/opus/vinewatch-ruins/scripts/gen.py:107-108, :163-164, :199-204 | (module) | QUARTZ_STAIRS / STONEBRICK_STAIRS | three flights |
| calcite | opus55-freeform-calcite/scripts/gen.py:86-87 (`columns`), :136 (`stairs_on`), gen_v3.py:116 (`stair_run`) | | QSTAIRS | `stairs_on` takes cells + axis + half width |
| riad | opus55-freeform-riad/scripts/gen.py:183-184 (`columns`) | | SANDSTONE_STAIRS | |
| lanternpass | opus55-freeform-lanternpass/scripts/gen.py:117-119 (`columns`) | | STONEBRICK_STAIRS / OAK_STAIRS / COBBLE_STAIRS by height | |
| gullhaven | opus55-freeform-gullhaven/scripts/gen.py:141-143 (`columns`) | | BRICK_STAIRS / COBBLE_STAIRS on "ramp" cells that step up | `stair_dir` :85 |
| copperline | opus55-freeform-copperline/scripts/gen.py:238 (`columns`) | | COBBLE_STAIRS | |
| penstock | opus55-freeform-penstock/scripts/gen.py:89 (`flights`), :109 (`tunnels`) | | SB_STAIRS over CONCRETE | rows of full width |
| lantern-karst port | lib/ports/lantern-karst/scripts/dress.py:121-123 | `joins` | STONEBRICK_STAIRS | |
| tamarisk-wash | lib/trials/sonnet/tamarisk-wash/scripts/gen.py:212-220 (serai), :246-254 (`table_rock`) | | SANDSTONE_STAIRS data `e` / `n` over SANDSTONE 2 | |
| redwash-mesa | lib/trials/opus/redwash-mesa/scripts/gen.py:88-107 | (module) | `BLD.stairs` + side wall | library call |

---------------------------------------------------------------------------------------------------------------------------------------------

## 4. What a generic line build would need

Parameters the sites together require, with the sites that need each.

| parameter | values seen | sites |
|---|---|---|
| geometry source | polyline (walked cells); closed polyline / polygon edge; rectangle edge (box); circle band; raster mask edge (cell with a missing 4-neighbour); raster mask cells; straight line segment | polyline: abbeymoor walls_along, gullhaven cover, riftwater hedgerows, hoarfrost strand (via parapet); polygon: hollowcrown crownhold; rectangle: curio wall, hollow-mesa fort/rancho/cemetery, overgrowth courts, whitecliff quay/garden, cinder-reach plot; circle: hollow-mesa tank/spring, frostholm beacon, lanterndrop harbour; raster edge: riad parapets, penstock rails, slatefold rails, hollowcrown fields, hoarfrost surface, whitecliff rim |
| y mode: follows ground per column | `top = ground(x,z)+1`, skip if occupied / wet / not land | abbeymoor, gullhaven cover, riftwater hedgerows/gardens/wheat, hollow-mesa rancho/cemetery/hitching/tank, hollowcrown wendholm/fields, cinder-reach plot |
| y mode: fixed y | one constant or a plan level | curio, calcite rails, copperline railings, saltgate, sunwell rims, penstock, whitecliff, brassmoor, redwash |
| y mode: plan-stated height | wall height from `R.H - ground` | gullhaven cover, claywork parapet, slatefold retaining |
| y mode: level crown in steps | deck / wall following a stepped crown | riftwater stone_bridge parapets, hollowcrown kingsbridge, frostholm bridge (arched), lanternpass walkways (table) |
| y mode: graded along a route | deck graded by distance along the line | stratum skyway, riftwater footbridge |
| fill below to a foot | wall as a column from the lower neighbour's floor | slatefold/hollowcrown/gullhaven retaining walls, hollowcrown crownhold (ground-3 up) |
| height | 1 (rail/wall block), 2 (hedge, parapet+cap), N (curtain wall 4-9), plan-stated | all |
| thickness / width | 1 (almost all), 2 (curtain wall in hollowcrown thick_line_cells, overgrowth perimeter), 3 (stair side) | |
| material mix | single; random weights (retaining 80/15/5; cobble 60 / mossy 40; mossy 20% of walls); hashed (curio `(3x+y+5z)%9`); height-banded (hollowcrown y+4 band, whitecliff WHITE/BLUE every third course) | abbeymoor, gullhaven, curio, slatefold, hollowcrown, whitecliff |
| alternating blocks along the line | two blocks by `(x+z)%n` or index | cinder-reach (BRICK / FENCE every 4), riad (wool every 4th), lanternpass (post every 8) |
| top cap | slab on top (parapet + slab), second block (hedge), crenel | claywork, riftwater bridges, riad, frostholm beacon, whitecliff (SLAB 7) |
| crenel rhythm | every other cell by `(x+z)%2`; by x index; every third/fifth (slotted); by angle on a circle; gap rhythm (open every 5th) | curio, hollow-mesa fort/adobe, saltgate, loomfall, riad, stratum, frostholm beacon |
| gaps / gates | explicit point list with radius (abbeymoor), named intervals (sunwell), plan cells (overgrowth/whitecliff `gate_cells`), cells within r of route ends (hollowcrown), side midpoints (cloudhaven, curio), index modulus (riftwater hedgerows every 13) | |
| gate content | air + lintel; iron bars; stair flight in the gap; fence gate | curio, hollowcrown, cloudhaven, riftwater wheat (FENCE_GATE) |
| which side of the line | outer side offset (hedgerows +2, abbeymoor +-5), both sides (bridges), one side (crop field west) | |
| corner handling | wall/fence blocks self-connect; stairs/kerb at corners use a different block (brittle kerbed_bed); curio/hollowcrown add towers at vertices | |
| skip rules | skip occupied, wet, non-land, protected columns; skip where the tile above is not air; skip near ends (skyway 0.04-0.96) | abbeymoor, riftwater hedgerows, stratum |
| side-rail "only where there is a drop" | add the rail where a neighbour is lower by >=1/>=3 or void | slatefold flights/rails, hollowcrown wendholm parapets, penstock rails, riad parapets, hollow-mesa catwalk |
| ends | clear the rail where a flight meets it | penstock, redwash (open cut), tamarisk serai |
| result | count of cells written / list of cells for claims | abbeymoor, slatefold |

Specific facts a design can rely on:
- `build.parapet` is a cell-set function: it has no polyline input, no ground-follow, no gaps, and one rhythm `(x+z)%2`.
- Every ground-following site reads the height itself (`P.g`, `H(L,..)`, `w.top`) and skips non-air tops; there is no shared helper.
- Gap handling is the most varied part: four different encodings.

---------------------------------------------------------------------------------------------------------------------------------------------

## 5. What a generic path-steps option would need

| aspect | what the sites do | sites |
|---|---|---|
| stairs vs slabs | stairs when the ground rises 1 per cell (`route.steps`); half-block slab steps for a graded, steep route (route.halfsteps / Tamarisk ghats); slab on the low side of a 1-block join (lantern-karst joins) | stairs: abbeymoor, cinderfall, vale, hollowcrown path_steps, gullhaven bridges; slabs: tamarisk, lantern-karst |
| when a step is laid | `abs(dh) == 1` and orthogonal move (route.steps); `y == prev+1` ascending only (hollowcrown); rise detected by next/prev cell in a 3D polyline (galleries); plan height changes (`HW[z]`, `U` neighbour) | |
| facing | ascending direction of travel (route.steps: `up = (dx,dz)` or reversed if descending); explicit table keyed on step vector (hollowcrown, lantern-karst); toward the lower neighbour (gullhaven); fixed per flight (lanternpass walkways 2/3, riftwater bridge 2/3, mule_trail 3/2) | |
| diagonal runs | route.steps skips non-orthogonal moves (so a diagonal climb has no stair); hollowcrown's table has no diagonals; tamarisk avoids stairs for exactly this reason ("no stair faces the wrong way across a diagonal run") | steps, path_steps, ghats |
| width | route.steps widens across the climb; hollowcrown 1; bridges 3-5 across the deck; galleries 3; mule_trail 2; ghats = route width via the band | |
| what is under / over | fill under (STONE, clay, mass) and air above 3-4 blocks; hollowcrown and route.steps do neither | flights, mule_trail, serai, redwash |
| side rails | stair-side wall / fence on the open side only | slatefold flights, mule_trail, redwash, penstock tunnels |
| grade source | the actual heightmap (route.steps), the route's graded profile (`rt["profile"]`, tamarisk), a plan table (`HW[z]`, `U`) | |
| returns | a count of steps (route.steps), a joined flag (halfstep_levels) | |
| conditional on grade | cinderfall calls steps only if `grade > 0.4` and kind road; tamarisk excludes ghats from pave and rebuilds them | |

---------------------------------------------------------------------------------------------------------------------------------------------

## 6. Minor or borderline sites (fence posts, ship rails, interior)

- Ship and balloon rails: cloudhaven buildings.py:443, :474, :555, :617; saltgate `ships` (gen.py:122); riftwater footbridge torch posts.
- Fence posts in a line without being a continuous barrier: lanternpass `harbour` posts (gen.py:279), copperline `lamps` (gen.py:823), hollowcrown `mine_road` (buildings.py:783), tamarisk/hoarfrost `props.lamps`.
- Interior rails: hollow-mesa `catwalk`/`gallery` (underground.py:93, :134), copperline `adit` (gen.py:644), riftwater `mine`.
- Fort-style compounds that are building walls: hollow-mesa `fort` (listed), curio `wall` (listed). `masonry_tower` and `F.extrude` are library.
- Not found: no board script builds a palisade, a levee, a balustrade or a colonnade as a line; stratum `forum` (buildings.py:323) has 2x2 piers every six along two long edges (`# the colonnades` at :347) which is a pier row, not a wall.
- `lib/boards/brittlebush-iii`, `brittlebush-koth`, `sandreach`, `lib/examples/drop`, `islets`: only plan-level stairs (`R.flight`), no hand-built line geometry in gen.
