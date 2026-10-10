# What caused the leap in quality

**The leap came from moving the decisions the studio makes for an author back into the author's hands, and from a loop that checked them.** The studio compiles a plan of rectangles into terrain, paints it through a theme of named buckets and stamps a fixed set of structures. The freeform boards wrote voxels directly, from a plan that was drawn, sketched and walked before anything was built. This note separates what the evidence shows from what is plausible, lists what was lost, and ranks what the studio should adopt. Sources are the run reports, `freeform/lib`, the studio's docs and the Stamping folder, read only.

## What the evidence is, and how far it goes

**Nothing here is a controlled comparison.** No board was built both ways, so every attribution below is an inference from what each pipeline can and cannot express. Where a claim rests only on the playtester's reading, it says so. The strongest evidence is a missing capability in the studio paired with a visible feature that needs it.

**The studio-built and freeform boards also differ in author, brief and date.** The studio boards were built from one JSON spec each against `AUTHORING-BRIEF.md`; the freeform boards were written as code with a plan phase and a report. The author's own ruling, in `WHAT-A-BOARD-IS-MADE-OF.md`, is that "every board passed every gate and several look wrong", and that none of it is enforced. That is evidence the studio gates did not measure look.

## What the studio pipeline constrains

**The studio's look is a finish over a shape it has already decided.** `docs/world-export/terrain-painting.md` says the painter "touches only stone", reads terrain the world builder placed, and adds "no new geometry, only materials". A theme sets four buckets (rim, wall, surface, fill), each a material, a depth and a pattern. The terrain under it comes from plan pieces and relief marks, not from the theme.

**The studio's structures are stamped from fixed forms.** `StructureStamper`, `WoolStructureStamper`, `SpawnStructureStamper` and `MonumentStamper` place rooms, shells and objectives from presets. `structures.md` describes a roof as a height field over one rectangle, so a building is axis-aligned, and a wing is its own rectangle. Rules such as WX12 keep a footprint inside the piece it stands on.

**The studio's checks are about validity and play, not appearance.** Its walk is a kit-budget capture walk with no ladders, jumps, pads or fall damage, per `SHARED-LIBRARY-ASSESSMENT.md`. The generator rules (`docs/generator/rules.md`) and the mapgen review gate structure, symmetry and approaches. Nothing asks whether the ground reads as a place.

## What the freeform generators did differently

**They controlled every block, so detail could be chosen where it mattered.** `pgmvox.World` is a voxel array written through the studio's own Anvil writer, so nothing the studio could place is out of reach. Every board's `gen.py` lays its own ground, houses, props and objectives, and the objectives (`pgmvox.objectives`) still write the studio's XML shapes. The studio validates the result with `read_mapxml.cs`.

**Ground was painted by slope and by bed, not by shape.** `terrain.slope_deg` reads the grade as the studio's `SurfaceGradient` does, and `lay` chooses soil depth and top block per column from it, so a cliff is rock to its face and a meadow is grass. `Strata` and `beds` tilt and fold rock beds so a wall shows layers dipping across it. The studio's buckets are chosen by edge and drop; the project's own `CLAUDE.md` names the failure of painting by plan piece or height band as "the look every report here has complained about".

**Floating islands got undersides.** `terrain.underside` and `forms.skirt` hang tapering cones, flutes and ledges below a floor, and `root_vines` trails vines from the roots. The studio emits islands as terrain with a flat cut; the freeform boards built the part a player sees from the side and below. The playtester names "proper floating islands" as one definite cause, and this is the mechanism.

**Houses were rasterised at any heading with the studio's own roofs.** `build.Frame` places a building's axes at any angle, and `RoofField` ports the studio's six roof forms, held to the studio by a test of 34,500 questions. At 0 or 90 degrees the roof is the studio's exactly; turned, it is laid in cubes and slabs. That accounts for "houses at different angles with the roofs properly following".

**A grammar made a style out of a few rules.** `GRAMMAR.md` states Brittlebush as cells of five blocks, sections cut into rectangles, a one-block outline whose material says what lies beyond, and a face read as courses down from its edge with an accent bay. `pgmvox.grammar` and `clay` implement it apart from any blocks. This is the "geometric grammar" the playtester describes, and the studio theme has no counterpart.

**Props and patterns were authored as small objects.** `props.stalls` lays a market row with awnings, `props.lamp` a post and lantern, and `facade` supplies inset bands, courses, windows, glyph rows and floor fields. The playtester liked the market stands; they exist because a prop is a few lines of code, where the studio has no prop seam beyond its stampers.

## The plan, sketch and walk loop

**The freeform boards were planned in a form that could be checked before building.** `pgmvox.plan.Raster` holds the plan with its symmetry drawn in, `sketch` draws it true to scale with its numbers on the sheet, and `plangraph` walks it. Every board's `plan_check.py` measured goal rules against targets before a block was written. The trial reports show the loop catching things: four wrong joins in the first plan of one board.

**The built world was then read back.** Each `walk.py` loads the saved blocks and walks them under the 1.8 movement rules in `pgmvox.move` and `walk`, then runs the footing audit, the void audit and the objective checks. One report found two library bugs only through the count of standable columns over the void. A picture answers whether something came out; the number answers whether it is right, as `CLAUDE.md` says.

**The plan and sketch phases are probably what the playtester felt as "places".** The plan names each place and gives it a reason, as `WHAT-A-BOARD-IS-MADE-OF.md` demands, and the sketch makes the author review it before building. The studio has a sketch tool too (`docs/tools/sketch.md`), so the difference is less the existence of a phase than that here it was measured and drawn at true scale. This attribution is plausible, not shown.

## Which differences plausibly explain which observation

| The playtester saw | Most plausible cause | Standing |
|---|---|---|
| Terrain more detailed | slope-driven soil, tilted beds, per-column control | mechanism shown; effect inferred |
| Proper floating islands | `underside`, `skirt`, `root_vines` | mechanism shown; named by the playtester |
| Houses more detailed, at angles | `Frame`, `RoofField`, `facade` patterns | mechanism shown |
| Props such as stalls | `props`, code-level authoring | mechanism shown |
| Places that look like places | plan phase with named places, sketch review | plausible only |
| A style beyond rim and surface | `grammar`, `brittle`, `clay` | mechanism shown |
| Few gameplay trades | objectives still emit the studio's XML | shown by the validity checker |

**The quality ceiling was the studio's theme model, not its gameplay model.** The freeform boards kept the studio's objective, spawn and kit XML, and the checker reads them as valid, so gameplay barely changed. What changed was everything the studio decides from geometry. That is why the playtester found few gameplay features traded away.

## What was lost relative to the studio

**The stampers' gameplay fixtures were lost first and have since been ported.** The defence chest and the wool-room gear were studio stampers (`DefenseChest.cs`, `WoolChests.cs`). `pgmvox.props` now has `defence_chests` and `wool_chests`, and the playtest batch applied the wool chests to the capture boards. The bedrock wall with its defence chest is the same case, with `props.DEFENCE` in the library.

**Build-region fidelity was lost, and the evidence is in the writers.** The studio writes a zone as a rectangle with no-build holes and marks it. The capture boards write block 36 under every buildable column plus a `not-void` filter, or one negative rectangle, as `brassmoor-works/scripts/mapxml.py` and `common.build_only_over` do. That is coarser than the studio's zones, and a few boards hand-draw the marker line.

**Objective indicators were not ported.** `GoalMarkerStamper.cs` floats a three-block cube or cross above every wool room, destroyable and core, above the build-height cap so nobody can bury it. A search of `pgmvox` finds no equivalent, so the capture boards carry no sky marker. This is a plain gap and the likely reason the playtester found objectives "hard to find".

**Build-zone markings exist on some boards and not others.** `BuildMarkerStamper.cs` lays an unpowered redstone line at y 1, two blocks out from every void-facing zone edge. The Lantern Karst report reproduces it by hand (518 blocks), but the library has no function for it. Boards written without it, the capture boards among them, show no zone edge.

**Some losses are not stampers at all.** The studio's compiler declares enclosed voids, fans objectives across a symmetry orbit and rejects a plan that breaks a rule. The freeform boards redo the symmetry in `Symmetry` and `Objectives.add`, and redo the rules in each checker, about 120 lines a board per the trial summary. Rules a board does not re-state are no longer enforced.

## What to do first, in the library or the studio

**These are ranked by how much play or quality each decides, then by how little it costs.** The first three close gaps the playtester named and land in the library; the rest carry the freeform gain into the studio. Each says where it lands.

1. **Objective sky markers for every pgmvox objective.** Call the existing `GoalMarkerStamper` logic from `pgmvox.objectives` (`Wool`, `Destroyable`, `Core`, `Hill`) so each objective stamps its marker as it stamps its blocks. It lands in `freeform/lib/pgmvox/objectives.py` and reuses `PgmStudio.Minecraft/Stamping/GoalMarkerStamper.cs`.
2. **Build-zone marking and zone fidelity.** Add a `mapxml`/`world` helper that writes the zone rectangles with holes and the y 1 redstone outline, the library's version of `BuildMarkerStamper`. It lands in `pgmvox.mapxml` and `pgmvox.objectives` (`Objectives.write`), so no board hand-draws it.
3. **The defence chest and bedrock wall as one stamp.** `props.defence_chests` exists; pair it with the bedrock wall the capture boards write by hand. It lands in `pgmvox.props` with a plan piece in `plan`.
4. **Slope-banded finish in the theme system.** Add a `slope` axis and bed tilt to `TerrainTheme`, ported from `terrain.lay`, `Strata` and `beds`. It lands in `PgmStudio.Minecraft/TerrainPainter`, and `CLAUDE.md` already names the `slope` band axis.
5. **Floating-island undersides.** Port `terrain.underside` and `forms.skirt` into the world builder's void-edge pass. It lands in `PgmStudio.Minecraft/Stamping/TerrainBuilder.cs` or the relief solver's output stage.
6. **Houses at any heading.** Let `BuildingPlan` carry a heading, using `build.Frame` and the `RoofField` port that the library already tests against the studio. It lands in `StructureStamper.cs` and the roof field.
7. **A style grammar beside the theme.** Offer sections, outlines, faces with accent bays and inset patterns as a second theme kind. It lands beside `TerrainTheme` in the theme JSON and the Sketch tool's Theme phase.
8. **A measured plan walk.** Give the studio an adventure-mode walk with ladders, jumps and fall damage, and one walk unit used by both plan and built reads. It lands in `Geom` and the plan checker, which also settles the octile versus four-way disagreement the trial report ranks first.

## What stays uncertain

**The size of each cause is not measured.** A controlled test would build one spec twice, once through the studio and once with the freeform finish, and ask the playtester to compare. Until then the ranking above rests on mechanism, not on measured effect.

**Discoverability may not be the objective marker alone.** The report evidence says the capture boards have no sky marker and the playtester says objectives were hard to find, which agrees. Whether placement, sight lines or approach law also contributed is not separable from these sources.
