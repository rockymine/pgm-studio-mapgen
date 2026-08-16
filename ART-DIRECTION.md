# Art direction — the rules, by id

How a board should look, stated as numbered rules an author follows and a reviewer checks. Rule ids are
stable; rules change over time by editing the rule under its id. Where a rule is now enforced by the studio,
the enforcing id is in brackets — the rest are enforced by this document alone. What a map *plays* like is
not here: that is `pgm-studio/docs/gameplay/approaches.md`, which wins any disagreement.

## AD-B — the board

- **AD-B1.** Before any shape: write down the extent, aspect ratio, spawn positions, objective positions,
  and the two routes between them. Five numbers and two lines are the board.
- **AD-B2.** A destroy board is a **lane**, not a square: one dimension meaningfully shorter. On a square
  board every goal is equidistant from both spawns and the ratio flattens.
- **AD-B3.** A destroy goal sits **3.0–4.0×** as far from the enemy spawn as from its own, by walk
  [`GO1`, scored by `goal-spawn-ratio`; `POST /plan/inspect` answers `goalDistances`].
- **AD-B4.** Two goals of one team stand ≥ **35** apart (70–75 good); the nearest enemy goal 95–110.
- **AD-B5.** The identity is one sentence, written before the palette is chosen. If the sentence cannot be
  written, the board is not ready.

## AD-P — the palette

- **AD-P1.** `TerrainPalette.Families` is nineteen hand-ordered tone families; the surface read-back names
  worlds in the same vocabulary. Preview them as pictures: `POST /terrain/material-preview?format=png`.
- **AD-P2.** A pattern takes **two or three members of one family**, never the whole family. Two is a
  texture, three a mottle, five a mistake.
- **AD-P3.** Reach across **two families** for ground that reads as one thing but not one block: `sand` +
  `rust` desert · `cobble` + `grey stone` worked hillside · `loam` + `dirt` fen · `bright` + `ice` snowfield
  (never snow alone — mix ice in, and break large snow with grass patches).
- **AD-P4.** Stained clay, wool and glass are **shade rows**, not ground: use them for a stated colour (team
  accent, roof, marker), never for terrain. Eight stained-clay values belong to no family and render as
  unnamed material in `--surface` (`B147`).
- **AD-P5.** Name three tone families out loud: which is ground, which is built, which is accent. **A
  building is never in the same family as the ground it stands on.** An accent that appears once is not an
  accent.
- **AD-P6.** Match a pattern's cell size to the shape: a 2-block checker is texture at ten blocks, noise at
  ninety.
- **AD-P7.** One material system per role, everywhere it recurs: paths mix paving blocks (`Pave` is a full
  material — cobble + gravel + andesite, not gravel alone); a platform is **not** the path's material; steps
  up to a monument platform take the **platform's** material, not one surface per piece; a boulder's `Rock`
  matches stone, not the sand it sits on.

## AD-R — rim and walls

- **AD-R1.** The rim is **off by default**; on any shape whose ground a relief solves, it is off. A rim over
  relief is contour lines on a hill.
- **AD-R2.** A rim stays where an edge is *made*: the coast over void, a platform lip, a retaining wall's
  top course. `RimEdges`: `void` outer coast only · `drop` every fall · `boundary` every plateau edge.
- **AD-R3.** The wall bucket takes a pattern tied to what the wall **is**: `wallRun` along a face,
  `wallDiagonal` across it, `layered` down a riser. A cliff, a retaining wall and a platform side must not
  read the same.

## AD-L — landforms

- **AD-L1.** A landform meets its neighbour along an authored transition — never a flat pad butted against a
  hill. The four fields: `skirt` (a raise/sink ramps into its surroundings), `anchor_heights` (a surface
  tilts), `height_mode` (level/raise/sink, chosen deliberately), `relief_scope` (`hold` keeps built things
  flat inside a solve).
- **AD-L2.** Do not exclude a piece from the relief and leave its straight edge showing: an excluded
  rectangle meeting solved ground at a ruled corner reads as pasted. Let the relief merge rough ground into
  clean, or author the seam (`B239`'s per-interface read will complain; today this document does).
- **AD-L3.** A depression and the hill beside it are one composition: author the saddle between them.
- **AD-L4.** Elevation: relief for ground that *grew*, `base_height` tiers and shapes for ground that was
  *built*. Adjacent pieces step by **1 level, or take a ramp** — a bare Δ2 seam is un-walkable, and a spawn
  behind one cannot be left (`B239`).
- **AD-L5.** Promote compiled tiers to polygons with Bézier `controls`; a tier can fuse to more than one
  shape, and where land stands higher than a piece the land runs **over** the lower fringe.
- **AD-L6.** A large open area wants level changes, not more trees. If a region is bigger than what fills
  it, shrink the region — the coverage read names the dead patches
  (`GET /map/{slug}/coverage`, `stages/coverage.png`, and the dead-share line every `mapgen` build prints).

## AD-PA — paths

- **AD-PA1.** A path is the circulation diagram, drawn. Author the routes as paths **before** the scenery:
  spawn door → objective, objective → flank, wool → hub.
- **AD-PA2.** A `path` *shape* is terrain (a rasterized band); a `path` *prop* is a finish that repaints the
  surface. Know which you are placing; preview the five band styles at `GET /terrain/path-styles`.
- **AD-PA3.** `tapered` and `rough` edges stop a path reading as a ruled stripe.
- **AD-PA4.** A path never drops a building — the road runs to the porch — but the band refuses the scatter:
  a trunk keeps **3** blocks off the paved edge, a boulder **2** [`DR-ROAD`], measured to the spline, not
  the drawn polyline.

## AD-S — settlements and buildings

- **AD-S1.** A board carries **at least three distinct placement ideas**; a village may be one. The others:
  a single house on a hill, a house in an authored clearing, a mine head / kiln / wellhouse / boathouse
  whose style says its function, a run of buildings as a boundary.
- **AD-S2.** In a village, alignment is authored per prop: vary frontage, aspect ratio and storey count.
  Six footprints in one style is a settlement; one footprint in six materials is a swatch.
- **AD-S3.** Start from a `HousePresets` style and edit; write the style at field level (roof form, pitch,
  slab id, coursed wall, window form, door head). The presets each demonstrate a technique — `Desert`
  (arched head, no sill), `Diorite` (the one correct slab-roof idiom), `Stilts`, `Terrace` (parapet deck),
  `Cottage`/`Longhouse`/`Terrace` (aspect ratio as the variable).
- **AD-S4.** Four idioms beyond "rectangle with a roof": stilts, a parapet-walled flat roof (a storey-stack
  idiom, not a roof form), a porch, per-storey walls and windows. Multi-wing buildings are **one house**: an
  L, T or U is a wing list under one style, marching or projecting where wings meet [`HJ1`–`HJ5`; preview
  refuses what the build would drop].
- **AD-S5.** Placement is bounded and mostly enforced: 20 blocks clear in front of a spawn door and 10 in
  front of a wool entry (trees and buildings; boulders stay legal) [`OB21`]; 10 blocks clear around a goal
  marker [`OB19`]; a building leaves a **5-block passage** on at least one side [`DR-PASS`]; one block
  between buildings, eaves included (`B166`, unenforced); ≥ 5×5 and ≤ 20×20 (`B167`/`B157`, unenforced);
  ground under every column (`B187`, unenforced — check it yourself).
- **AD-S6.** Look at a house before building a world: `/room-styles/preview` (plan, section, isometric,
  cutaway), and `--section` on a built one. Every shipped roof fault was visible in a section and invisible
  from above.

## AD-M — the material laws

- **AD-M1.** Grass is one course, only ever the top layer of a `layered` stack (`B163`).
- **AD-M2.** A destroyable carries ≤ 3 obsidian: only pillar styles may use it; cubes take end stone, gold
  or emerald (`B162`).
- **AD-M3.** Slab in `roofSlab`, whole block in `roof`; a slab-course roof only at a half-course rise
  (`B168`).
- **AD-M4.** Never a log, Grass Block or Podzol in a roof or verge (`B168`).
- **AD-M5.** A block is the kind its role needs — stair in `doorHead.block`, slab in a `slabBanded` window
  [`HS1`]; a spawn door clears 2.5 [`HS2`].
- **AD-M6.** A building seated into terrain names **air** for its sill (`B164`).
- **AD-M7.** Gable at `pitch: 2` loses to its own wall — use `pitch: 1` (`B165`).
- **AD-M8.** A goal name is a name: no `<Team>`, no angle brackets (`B182`).
- **AD-M9.** A tree stands on soil — dirt, grass, sand or snow, never bare stone [`mapgen` complains with
  coordinates].
- **AD-M10.** The map states its author as a bare model name — `"authors": ["Fable 5"]` in the spec becomes
  `<author>Fable 5</author>`; never empty, never a uuid [`mapgen` complains when absent].

## AD-V — void, spawns, zones

- **AD-V1.** Void belongs between the teams, not across an approach; for destroy boards the mid-terrain
  hole is replaced by a depression or a pond. A hole is also what makes a flank worth walking to — do not
  fill every one.
- **AD-V2.** On a CTW board two islands sit 15–40 apart (`B158`); a whole island per team is the right
  shape.
- **AD-V3.** The spawn: door ≥ 15 from void (`B158`) · open ground ahead [`OB21`] · the ground it opens onto
  climbs back (`B180`) · near the back of its lane (`SP2`), iron beside or ahead (`SP7`) · egress steps by
  1 level or a ramp (`B239`).
- **AD-V4.** **One build zone for a compact middle.** Several only where the frontline is legged (one zone
  per leg) or two mid islands each take a flush zone — `frontline-dos-and-donts.plan.json`. Stitched funnels
  are invisible to players (`B238`); a frontline run wants ≥ 15 blocks of width.
- **AD-V5.** A wool stands off its hub behind an approach piece shaped from the approach families (i, l, z,
  scythe, clamp, u, h, donut — `GET /shapes/catalog`); a wool room never docks flush against a hub. The
  bedrock wall sits on the **approach's outer interface**, ~15 blocks from the room — never on the wool's
  own edge [`PL13`].

## AD-C — circulation, then dressing

- **AD-C1.** Routes first, drawn as paths; those runs plus a margin are ground foliage does not get.
- **AD-C2.** Nothing is scattered: every prop answers *why here*. Bare ground you chose beats dressing you
  did not. The coverage read (AD-L6) tells you which ground is dead and undecorated.
- **AD-C3.** Approaches differ: around · above · below · through. Three cover-walks is one approach three
  times.
- **AD-C4.** A forest is canopy share, not leaf count; avoid `whorled: true` (`B174`).

## Open questions go in the report

This document decides nothing about play the author has not. A question `approaches.md` does not settle is
recorded in the run report as an open question with the decision taken — never filed as a fact.
