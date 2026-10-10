# Lantern Karst on pgmvox — the port

**This folder rebuilds the freeform board Lantern Karst on the shared library, as a trial of the library.** The
original is `freeform/opus55-freeform-lantern-karst/`. The port runs end to end with
`python3 -m pgmvox.run ports/lantern-karst --build /tmp/lantern-karst-port-build --skip write` in about a minute.
Forty seconds of that minute are one library call, `plangraph.jumps`.

**The port is the same board.** It has the same 26 pieces at the same floors, the same four build zones, the
same joins, walls and objectives. The plan check gives the original's numbers to within a block or two. The
studio's own reader accepts the map.xml as valid, with no issues.

## What the port covers

| Feature of the original | How it was ported |
|---|---|
| 26 pieces at their floors, red's half turned onto blue's | library: `plan.Raster` with `Symmetry("half")`, one kind per piece |
| The Store Road's climb, the Drying Floor's ramp, the spawn's two-step exits | library: sub-rectangles in the raster |
| The Tea Court's sinkhole | library: a void rectangle in the raster |
| Joins: slabs for one block, stair flights (or 10 in the middle and retaining walls) for two | local: `plan.joins` finds them and draws `Raster.flight`; `dress.joins` lays them |
| Four build zones, block 36 at y 0 under every buildable column | local: `plan.zone_mask`, `gen.markers` |
| The build outline in redstone at y 1 (ST5) | local: `gen.outline` (522 blocks; the original laid 518) |
| Bedrock course six under every floor, off the rim | local: a pass in `gen.islands` |
| Rock in beds with flecks of cobble and gravel | library: `terrain.Strata`, `bed_offset`, `beds`, `lay` |
| Fluted, spired karst roots down into the mist | library: `terrain.root_depth`, `terrain.underside`, run once per floor height |
| Bulging ledges and undercuts on the island faces, moss on the rim | local: `gen.skirt`, a pass in `gen.islands` |
| Vines on the roots | local: `gen.vines` |
| Mist of white and light grey glass at 24 to 38 | library: `terrain.cloud_deck` with glass materials |
| Sixteen karst towers in the mist with pines | library `landform.spire` and `terrain.lay` for the shape; local placement and pines |
| Paths wandering from both exits to every lane | library: `route.pave` along strokes bent by a local `dress.wander` |
| Paved floors in cells of three, coarse-dirt patches, ferns | local: `dress.paint`, `dress.ferns` |
| Tea rows, drying mats | library: `facade.stripes` laid by `facade.carpet`, wrapped locally |
| Pavilion of Arrival, Store, Shrine, Gate, Bell house, lantern towers | library roofs (`build.RoofField`, `lay_roof`) and walls (`facade.extrude`); local posts, eaves, upturned corners |
| Stone lanterns, pines, the pool, the outcrop, iron cubes, hay | local: `dress.toro`, `dress.pine`, `dress.spawn` |
| Team banners | library: `World.banner`; local recolour after the turn |
| Chests of better gear in the Store | library: `World.chest` |
| The bedrock wall: three bedrock, one cobweb | local: `dress.store_wall`; drawn in the plan as kind `barrier` |
| Entrance lines (ST1) at the Store's door and round the Shrine | local: `dress.entrance_line` |
| Teams, spawns, observer point | library: `objectives.Teams`, `Spawn`, `Observer` |
| Four wools with monuments, mirrored and recoloured | library: `objectives.Wool` with `Objectives.add(..., color=...)` |
| A team kept out of its own wool rooms | library: `Wool(room=...)` writes the rule |
| Wool blocks in the rooms, spawners, room block protection | local: `gen.make`, `mapxml.py` |
| Spawn protection that still lets the iron be mined, renewables | local: `mapxml.py` (`Spawn(protect=False)`) |
| Kit, void filter, item keep, kill rewards, build height | local: `mapxml.py` with `mapxml.E` |
| Kill below y 40 | library: `Doc.kill_below`, a portal to y -64, where the original applied an instant-damage kit |
| The plan check table | library `plangraph` and `sight`; the zones bridged and the amounts read in `plan_check.py` |
| The plan sketch: board, routes, sections, table | library: `sketch.Sheet`, `MapPanel`, `SectionPanel`, `TablePanel` |
| Isometric renders 30 to 37, sections 10 to 13 | library: `render.iso`, `render.cutaway`, `render.trim` |
| Elevations 50 and 52 | library: `render.elevation` |
| Elevations 51, 53 and 60 | not ported |
| Studio top-downs 01 and 03 | replaced by `05-topdown-annotated.png` (library `MapPanel.built`) |
| The walk read-back | library: `walk.walk`, `nearest`, `no_stand_above`, `audit.footing`, `Objectives.check` |
| Region files through the Anvil writer | skipped (`--skip write`), as asked |
| The plan's first versions (`plan_v1`, `plan_v2`, `sketch_v1`) | not ported; they are history |

**Left out on purpose:** the last three elevations, the plan's earlier versions, and the original's fall-kill kit.
The towers have no ledges or vines; a spire from the library is a smooth bullet. The mist has no ragged rim of
plain glass.

## How it compares

**The renders carry the original's names, so a pair is one path apart.**

| View | Original | Port |
|---|---|---|
| plan sketch | `freeform/opus55-freeform-lantern-karst/renders/00-plan-sketch.png` | `renders/00-plan-sketch.png` |
| board, south-east | `.../renders/30-iso-board-se.png` | `renders/30-iso-board-se.png` |
| board, north-west | `.../renders/31-iso-board-nw.png` | `renders/31-iso-board-nw.png` |
| red's half | `.../renders/32-iso-red-half-sw.png` | `renders/32-iso-red-half-sw.png` |
| spawn | `.../renders/33-iso-spawn.png` | `renders/33-iso-spawn.png` |
| Pillar and Arms | `.../renders/34-iso-pillar-and-arms.png` | `renders/34-iso-pillar-and-arms.png` |
| Store and road | `.../renders/35-iso-store-and-road.png` | `renders/35-iso-store-and-road.png` |
| hub and gate | `.../renders/36-iso-hub-and-gate.png` | `renders/36-iso-hub-and-gate.png` |
| middle and steps | `.../renders/37-iso-middle-and-steps.png` | `renders/37-iso-middle-and-steps.png` |
| sections | `.../renders/10-` to `13-*.png` | `renders/10-` to `13-*.png` |
| Store elevation | `.../renders/50-elev-store-from-the-road.png` | `renders/50-elev-store-from-the-road.png` |
| as built from above | `.../renders/01-topdown-material.png` | `renders/05-topdown-annotated.png` |

**From above, the two boards are hard to tell apart.** The islands, roots, paths, pavilions and mist land in the
same places. The port's towers are smoother and more regular, its paths a little denser, and its roofs are the
studio's hip roof rather than the original's own stepped one.

**The plan check reproduces the original's table.** The walk is octile with a step up costing 1.2. The original
walked through the bedrock wall; the port's plan has the wall in it, so its "walked only" rows say "not reached".

| Measured | Original | Port |
|---|---|---|
| spawn to the band | 98 | 98 |
| spawn to the Tea Store | 85 | 86 (3 bridged: over the wall) |
| spawn to the Pillar | 79 (17 bridged) | 79 (22 bridged) |
| their ratio | 1.08 | 1.09 |
| band to the Tea Store, shortest | 86 (27 bridged) | 86 (30 bridged) |
| band to the Pillar, shortest | 80 (64 bridged) | 79 (66 bridged) |
| Pillar to Tea Store, straight | 120 | 120 |
| Pillar to the Arms and the Terrace | 16, 16, 16 | 16, 16, 16 |
| Mist Steps' gaps; Tea Steps' gaps | 12, 12, 12, 12, 16; 12, 11, 11 | the same |
| land on red's half | 7,946 | 7,946 |
| the Ledges seen from the Arms (new, `sight`) | — | 100% |
| red and blue to their own Store, Pillar (new) | — | 86.3 / 86.3, 79.0 / 79.0 |
| running jumps between pieces that do not touch (new) | — | 0 |

**The built world reads back clean, apart from the outline's redstone.** These are `renders/walks.txt`'s numbers.

| Read-back | Port | Original |
|---|---|---|
| `Objectives.check` problems | 0 | — |
| wools missing from their rooms | 0 | — |
| `audit.footing` problems | 522, all the redstone outline at y 1 over air | — |
| places reached on foot from a spawn | 7,460 | 7,599 |
| spawn to its own monuments, on foot | 15 and 15 | 13 |
| on foot into the enemy's rooms, or its own | not reached, as designed | not reached |
| building, to the enemy's Pillar room and Store room | 257 and 262 moves, both teams | not measured |
| columns off the islands standable over the kill height | 3,407: tower crowns and skirts | — |

**The build walk is a stand-in.** The build zones' void and the bedrock wall's cells are filled with water from
the kill height to the build height. The walk swims up and across it the way a player climbs what they build, so
a move counts a block climbed as well as a block crossed. That is why 257 is far above the plan's 79.

**The port is 1,477 lines against the original's 2,433.** The original count leaves out its three superseded plan
files (527 lines) and its hand-written map.xml (164). The port counts every script, map.xml writer included.

| Script | Lines | Of which the library could hold |
|---|---|---|
| `plan.py` | 214 | about 50: `joins` (35), the zone mask (14) |
| `planwalk.py` | 93 | about 65: bridges, diagonals, `reach` |
| `plan_check.py` | 146 | — |
| `sketch.py` | 102 | — |
| `gen.py` | 229 | about 110: `skirt`, `vines`, `markers`, `outline`, tower placement |
| `dress.py` | 465 | about 115: joins, posts, roof with upturn, eave, panel walls, lanterns, pines, entrance line, wander |
| `mapxml.py` | 78 | about 45: kit, spawners, room protection, void filter |
| `renders.py`, `walk.py` | 150 | about 15: the water stand-in for building |
| **total** | **1,477** | **about 400, a quarter** |

**The rest of the port is the board itself.** That is the pieces and their numbers, the places and what stands
on them, and the table's rows. The original spent 211 lines on a world class, 232 on a renderer, 97 on
geometry, 63 on noise and 52 on rotation. The port needs none of those.

## Friction log

**The library fitted the frame of the board and fell short at the capture rules.** Rasters, symmetry, terrain,
roofs, objectives, the sketch and the renders all did their jobs. What a capture-the-wool board adds is build
zones, wool rooms and team-mirrored targets, and every one of those was written locally.

### The plan walk

1. **`plangraph` has no build zones, and a capture board is crossed by building.** Every attack route here
   bridges a zone. `planwalk.graph` (41 lines) adds "bridge" edges from each zone cell to its eight neighbours,
   at any height, and "over the wall" edges across the bedrock wall. The library would want
   `graph(..., bridge=mask, bridge_cost=1)`, with the bridged length reported per route.

2. **`plangraph` walks four ways, so its distances are Manhattan.** The original's targets (SP10 at least 55,
   WL10e at least 59) were set against octile walks. A four-way walk reads 15 to 25% longer, and the targets
   would pass or fail for the wrong reason. `planwalk.graph` adds diagonal steps where both cut corners are
   walkable and the rise is at most one; the library would want a `diagonals=True` rule.

3. **`plangraph.route` returns a route's tags and not how much of it each move was.** "79 (22 bridged)" needs the
   bridged length, so `planwalk.reach` walks `path` back and sums edge costs by tag. A `route` that returned
   `{tag: amount}` would do it.

4. **`plangraph.arrivals` gives every team the same target cells.** That fits a shared hill. On a capture board
   each team's target is its own image (red's Store, blue's Store), so fairness was measured with two calls of
   `dijkstra` and the image cells picked by hand. `arrivals` could take targets per team, or take one team's
   targets and turn them through the raster's symmetry.

5. **`plangraph.jumps` takes forty seconds on this board.** About 16,000 walkable cells, each tried against 81
   offsets in Python, make it the slowest step of the build. It also returns 166 "jumps" that are only corner
   cuts inside one piece or across a join. The port drops those by labelling connected land, the trick
   `MapPanel.jumps` already uses. A box or mask argument, numpy offsets and a between-pieces filter would cover
   both.

### Plan, symmetry and coordinates

6. **Bug: `Symmetry.point` (`orient.turn_xz`) rounds to whole blocks, so it turns anything else wrongly.** It
   is right for a block's own (x, z) and wrong for a block centre or a polygon corner.

   ```
   >>> Symmetry("half").point(0.5, 0.5)      # a block centre; the image is (-1.5, -1.5)
   (-2, -2)
   >>> Symmetry("half").point(1.5, 1.5)      # a different point, the same answer
   (-2, -2)
   >>> Symmetry("half").point(-57.5, -11.5), Symmetry("half").point(56.5, 10.5)
   ((56, 10), (-58, -12))                    # round() to even: one corner moves in, the other out
   ```

   `Raster` only turns cells, so the plan is right. `MapPanel._images` turns routes, polygons and zones with it
   (`both=True`), and those land up to a block off. The port turns its zone rectangles by hand in
   `plan._box_mask`. A float-preserving `point`, beside an integer `cell`, would fix it.

7. **`Raster.rect` takes `(x0, x1, z0, z1)`, and everything else takes `(x0, z0, x1, z1)`.** That includes
   `MapPanel.rect`, `facade.carpet`, the `render.iso` box and the `RoofField` box. The port wraps it in
   `plan.rect`. One order across the library would remove a class of silent mistakes.

8. **A raster keeps one floor and one kind a column.** The Store's walls, the bedrock wall and the stair flights
   are drawn over floors the generator still needs, so `plan.build` copies `R.floor` and `R.piece` before
   drawing them. A per-cell feature layer, or `storey` used for walls, would keep both.

9. **Using the piece key as the raster kind worked well.** Twenty-nine kinds in a dict cost nothing. The checker
   asks `R.mask("pillar")`, the sketch labels each piece's height, and the generator reads which piece a
   column is. The README could suggest it, since a board otherwise keeps a parallel label array.

10. **Scripts must import `plan` before `pgmvox`.** The `sys.path` insert lives in `plan.py`, as in Islets, and
    two scripts failed with `No module named 'pgmvox'` until `import plan` moved to the top. `run` sets
    `PYTHONPATH`, but a script run by hand does not get it. A one-line `_path.py` in the example would say so.

### Objectives and map.xml

11. **A `Wool`'s team is the team that captures it, so the object drawn once straddles both halves.** Red's lime
    lives in red's Pillar room but is `Wool("blue-team", "lime", slot=<blue's monument>, room=<red's room>)`, and
    its image takes `color="magenta"`. It is right once worked out. The docstring's example shows one line and
    no room, and a worked capture board would save the working-out.

12. **`Wool` stamps the monument but not the wool, and its check does not look for it.** `found` names where the
    wool is, yet nothing places a wool block there. The port sets the four blocks after the turn, and `walk.py`
    checks them. `stamp` could place it, and `check` could report a missing one.

13. **`Wool` writes the entry rule but not the rest of a wool room.** Spawners, the room's block protection, a
    union of a team's rooms and the spawner's point are written locally in `mapxml.py` (about 30 lines). They
    are what every capture board writes, and the original's ST1 entrance line belongs with them.

14. **`Spawn(protect=True)` writes `block="never"`, all or nothing.** The original lets players mine the
    spawn's iron and grows it back. The port passes `protect=False` and writes the enter rule, the iron filters
    and `<renewables>` itself. A `protect=` filter or an allowed-materials list would cover it.

15. **`mapxml` has no kit builder and no kill-by-kit.** The 16-line kit is raw `E` calls. The port uses
    `Doc.kill_below`, a portal to y -64. The original applied an instant-damage kit below y 40, so the
    mechanism differs while the outcome matches.

16. **The wool's sketch marker is at its monument, and the room has none.** `Wool.marker` returns the slot, so a
    "W" sits on each Monument Terrace and nothing marks the rooms. The sketch draws the rooms as squares in their
    wool's colour, locally. A second marker for `found` would do it.

### Terrain and the world

17. **`terrain.lay`, `underside` and `root_depth` take one height for the whole mask.** The islands stand at 11
    floor heights, so `gen.islands` loops over them, calling `lay` with `from_y = h - 5` and `underside` with
    `top_y = h - 5`. `root_depth`'s `cap` is a scalar, so the root's floor at y 26 is clamped by hand. Per-column
    arrays for `from_y`, `top_y` and `cap` would make it one call.

18. **`underside`'s paint is told how far down a block is, not its height.** Beds by world height need `h - 5 - k`
    worked out in a closure, and `beds`' flecks are lost because the closure calls `Strata` directly. A
    `paint(y, x, z)` form, or `beds` accepted as the paint, would fix both.

19. **A floating board's skirt is local.** The ledges that bulge out under a rim, never above floor minus two,
    and the undercuts are `gen.skirt` (28 lines). So are the bedrock course and moss on the rim. The README
    names `underside` for floating ground; a `skirt` beside it would finish the island.

20. **Bug: `orient.turn_world`'s `recolour` does not reach a tile entity's colour.** A banner's base colour lives
    in `w.tiles`, so a red banner turned onto blue's half stays red. Reproduce it with `w.banner(0, 70, -5, 1)`,
    then `turn_world(w, "half", lambda x, z: z < 0, recolour={...})`; the image tile still has `base` 1. The
    port sets `base = 4` on every banner tile with z ≥ 0. `recolour` could take a tile hook.

21. **`route.pave` over a plan clears air in void columns.** Given floors with -1 for void, it sets the surface at
    y -1 (ignored) and then clears `clear` blocks above, at y 0 to 2. That would wipe the block 36 markers. The
    port passes `clear=0` and lays the markers after. `pave` could take a mask, or skip columns under 0.

22. **`landform.spire` gives a smooth bullet, not a karst tower.** With a high taper it is a steep column with a
    rounded crown, which places well and lays its beds. A karst tower wants ledges and bulges by height; the
    original drew each course's radius with noise.

23. **`facade.extrude`'s patterns are not told which way their face looks.** `panel_walls` leaves one side
    open by mapping face numbers to normals through `facade.faces`, which relies on its sort order. Passing the
    normal to the pattern would make it plain. Walls of a hollow rectangle also need `fill=False` and a
    catch-all pattern for the base block, which the docstring does not show.

24. **`facade.carpet` lays one course.** The Drying Floor ramps 66 to 68, so its mats are three carpets, and the
    tea rows are a carpet per floor height with a closure that checks each cell's floor. A `y` function would
    do.

25. **`build.house` did not fit the pavilions.** They are open-sided, two-storeyed with a skirt eave between,
    and their hip roofs turn up at the corners. `RoofField` and `lay_roof` fitted exactly and gave the studio's
    hip roof. Upturned corners and a skirt eave are about 20 local lines.

### The read-back

26. **`walk.walk` has no kill height and no build zones.** The original's walk dropped everything under y 41.
    The port sets `d[:, :KILL_Y + 1, :] = -1` after the walk, so a fall into the mist could still have passed
    through it. Building is the water stand-in above. A `floor_y` rule and a `build=mask` rule would give the
    read-back the attack routes the plan check measures.

27. **`audit.footing` flags the studio's own build outline.** All 522 of its problems are the ST5 redstone at
    y 1, which stands over air by design: block 36 at y 0 would mark the column buildable. Either the convention
    or the audit is wrong. A dust that pops on a block update would leave the outline gone in play.

28. **`no_stand_above` cannot tell scenery from a mistake.** It counts 3,407 columns, nearly all the towers'
    crowns and the skirts' ledges, because `allowed` is one mask. An allowance for scenery, or a count by
    connected mass, would make the number readable.

### The sketch

29. **The sketch assumes the image half is x ≥ 0.** `MapPanel.raster` takes `image_half`, but `heights` hardcodes
    `x >= 0` for `both=False`. This board turns north onto south, so the port passes `image_half` everywhere
    and leaves `heights` with `both=True`.

30. **A callout's halo is always white.** On a panel washed by `dim`, light text is invisible, and dark text is
    the only choice. `SectionPanel.callout` turns back at the right edge only, so a label near the left is cut
    off; "shrine at 74" in panel 3a shows it.

### What fitted with no friction

**Much of the library worked first time.** `Objectives.add` mirrored spawns, rooms, monuments and yaws exactly,
and the studio's reader passed the map. `World.chest` and `World.banner` worked, as did `turn_world` on stairs,
chests and logs. `terrain.Strata` and `bed_offset` gave the beds, and `cloud_deck` gave the mist with glass for
material. `RoofField` gave every roof, `sight.hidden` gave a new row for free, and the renders and `Sheet` needed
no workarounds.

## Plan and sketch

**The plan was complete before a block was generated, because it was the original's.** Every piece, height,
zone, wall, wool and monument came across as numbers, and `plan_check.py` reproduced the original's table on the
first full run. The sketch was the original's three panels, plus an unrolled section along the attack route.

**That level was enough for the islands and the objectives.** Nothing about where things stand, or how high,
changed during building.

**Five things were decided only while building:**

- that the joins belong in the plan as flights, since a two-block step stops the library's walk;
- that the Store's walls and the bedrock wall go in the raster, and that the floor under them must be kept;
- how a mirrored `Wool` maps onto rooms and monuments;
- how to stand in for building in the voxel walk;
- the paths' width and the towers' shape, which came from looking at the first renders.

**The pavilions were planned as boxes with a top height and nothing more.** The original's buildings were
written straight into code, and so were the port's. A plan for them would have named the parts the library lacks.

## After review

**The towers were not a simplification; they were the board's look.** The author singled out the original towers
as structural and the port's heightfield spires as plain terrain. The original recipe is a stack of rings with a
ledge every nine courses, faces bulging between them and beds in courses. It is now `pgmvox.forms.tower`, and the
port's towers are built with it.

**The vines hang from the root tips again.** The port hung its vines just under the floor, where they hid against
the faces; the original hangs them from the lower roots, where they trail below the islands. That is now
`pgmvox.forms.root_vines`, and the karst faces under the rims are `pgmvox.forms.skirt`.

**The capture rules are the library's now.** Diagonal steps, bridged build zones and how much of a route was
built are in `plangraph`; the wool's block, spawner and room protection are in `objectives`; the spawn's iron, the
kit and the fall are in `objectives` and `mapxml`. The port's plan check calls them through three helpers and its
`mapxml.py` lost its rules, with the plan check and walks unchanged to the last digit.
