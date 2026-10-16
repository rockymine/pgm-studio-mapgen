# Thawline — report

A destroy-the-core and destroy-the-monument board for two teams of twenty, built on pgmvox by Claude Opus 5.5 for
the Fire and Ice competition. `PLAN.md` is the plan; this is what came of it. The world is `maps/dtcm/thawline`.

## The concept, and how it reads the theme

**Fire and Ice is read as one valley in one week of the year, split where the winter has reached.** The two teams
are the two seasons: **Frost** holds the north, already in winter (a glacier behind the hall, snow on the field,
spruce, ice in the becks), and **Ember** holds the south, still in autumn (rust, flame and copper oaks, golden
larches, a charcoal burners' country, fire in the hearths and lava running off the cinder ridge). The ground split
between them along the Thawline, a gorge with lava at its bottom, and the Rimefire Stack stands in it: a pillar out
of the lava with a spire whose north half is ice and south half is coal and obsidian with fire on its tip.

**The halves are the same board, only their season differs.** Every place is written once and built twice through
a `Side` (`scripts/season.py`) that turns each block and its data through the half turn and asks the season's
palette for each material by its role. The ground, every building, every tree's cut and every boulder stand in the
same place on both halves; the trees use the same cut turned half round, so cover is equal. The walk read-back
reaches each team's own Heart in 38 moves from its spawn and the enemy's in 133 to 134.

**The meeting is a gradient, not a line.** Each half's season runs from its back to the rift: Frost's back is deep
winter and its front autumn under the first snow, with snow lying on brown and orange crowns; Ember's front is
plain autumn and its back burns. So the two sides meet at the lips as two versions of late autumn, and the theme's
"snow meeting the reds and oranges" is on the board at every scale: across it, inside each half, on single trees.

## The modes, and how each objective is approached

Each team has one core (the **Heart**, a 5 by 5 by 5 obsidian shell of lava, leak 5) and one monument (the
**Lantern**, three obsidian). Following the author's rulings, the core is the board's forward, contested
objective in the open and the monument stands back by the spawn; neither is at the end of a lane, both are off the
line between the spawns (54 and 49 degrees), and they are a west and an east.

- **The Heart** hangs 8 over the floor of the Kettle, a kettle hole 7 deep and 20 across, four spires on its rim.
  Its approaches are four different kinds: *through* Rimewood (twelve oaks to within twelve of the rim), *around*
  Coldwater (the tarn that splits the middle into a west and an east way in), *above* from Hoarcrag (the Crag
  Path climbs to 60, eight over the Heart's top, a bridge of about eleven across), and *below* through the
  Culvert, a passage from the tarn's shore under the rim that comes out on the Kettle's floor under the Heart.
  The Kettle is also why the core can leak: its lava falls to a floor 7 under the shell.
- **The Lantern** floats 4 over Lantern Green, a paved terrace three over the field east of the hall: *through*
  the hamlet and over its two bridges, *up* the terrace's two flights, or by towering its face.
- **The middle** is the Thawline. Nobody walks across it: the lips are 7 to 24 apart, and the Stack's island
  stands 5 from each lip, so the shortest crossing is two bridges of five by the Stack and the longest a long
  bridge at the flanks. The Knoll's ruined tower with its hoarding is each team's forward watch over the lip; the
  Moraine, the drumlins, the erratics and two broken field walls are the cover between the lip and the goals.

## The layout and its proportions

The board is 128 by 200 with 20,872 columns of land (the rift and the void not counted), a floating island whose
underside tapers to a cone with flutes and spires and drops sheer into the gorge. Twenty a team. The spawn's
terrace is at 53, the field from 40 at the lip to 50, the Glacier to about 75. The goal rules the studio holds a
destroy board to all pass on the plan (`renders/plan-check.txt`): own spawn to the Heart 44 and to the Lantern 41
(GO4 40–90), the enemy's spawn to each 148 (GO3 85–150), enemy over own 3.37 and 3.65 (GO1 3–4).

## The palette

Biomes: Ice plains over Frost's back, Mesa over all the autumn (olive-brown grass, brown leaves), Savanna under
Ember's larch crowns (gold). Built: Frost stone brick, polished andesite and spruce, dark plank roofs stepped in
cubes so every step carries snow, sea lanterns; Ember brick and acacia with oak posts, dark oak roofs, granite
floors, glowstone and fire. Ground: snow with stone and andesite where steep; the autumn floor (grass with podzol
and coarse dirt patches, litter under every crown); the cinder ridge of coal, black clay and obsidian with lava in
its gutters. Accents: packed ice and ice (Glacier, icicles, Kettle spires, the Stack's north half), lava and fire
(the gorge, the cinder falls, the Stack's south half, the braziers, the kilns' vents). Autumn crowns carry orange,
red, yellow and brown wool among their leaves, in three recipes (rust, flame, copper), because no biome tints a
leaf orange or red; the swatch that decided it compared tinted leaves, wool and stained clay side by side.

## What was checked

- **The plan**, before any block: `checks.py` measures the walks with the rift crossed by building, the goal rules,
  the angles, the gorge's widths, the Stack's gaps and the unreachable ground (5.0%, all of it the Glacier and its
  spurs behind the spawns), and draws them on `renders/00-plan-sketch.png`.
- **The built world** (`renders/walks.txt`): both spawns walked over the blocks (the rift as a build zone, nothing
  below the kill height); every objective's ground reached; `objectives.check` clean (the cores have lava, both
  goals float, every column under them is marked ground); nothing standable over the kill height off the land;
  no block that falls or pops off; no water standing against air.
- **The map.xml** through the studio's parser: valid, two teams, two cores, two destroyables, no issues. Fire
  spread is off (`doFireTick` false) so the board's fires and the wool in the crowns stay as laid.
- **The renders**: the studio's textured renderer for every place (`renders/01` to `62`), and pgmvox's flat
  cutaway across the rift (`10`).

## What did not work, or is not done

- The first underside cut the whole island down to y 1 beside the rift and showed a flat grey wall forty high;
  the rift is now part of one tapered island with its floor at 13.
- The rift ran past the coast as a lava trough hanging in the void until it was clipped to the board's outline and
  dammed below the kill height at both mouths.
- Tree cuts overlapped each other's branches and refused on one half only; trees are now chosen so both halves'
  copies fit before either is planted, and every crown stays over land.
- Grass was left on cliff faces because the lay's top is grass whatever the slope; steep tops now take the rock of
  their bed.
- A first frost on Ember's north-facing slopes by the rift read as white scraps on the grass and was removed.
- The banners at the halls are in the world but the textured renderer draws no tile entities, so no picture shows
  them.
- The walk to the Lantern is 36 moves for Frost and 34 for Ember, two moves apart where everything else matches to
  the move; the difference is in what the season lays (snow layers and ice) rather than in the ground, and was not
  traced further.
- The houses are the library's houses (one rectangle a storey); the hall wants a porch and a wing.

## What was wanted, how hard it was, and what the library would need

| Wanted | How hard | What the library or studio would need |
|---|---|---|
| One board built twice in two materials | Easy once written: a `Side` mapping coordinates, data and palette roles | `pgmvox.core.orient` could carry a `Side` (image + data turn + palette lookup) so a board writes each place once |
| Autumn colour in the crowns | A swatch and a crown recipe per tree | `trees.remap(tree, wood, crown_recipe)` in `scenery.trees`; a tree planted only where its image also fits |
| Seasons as a gradient | A depth field and thresholds in the paint | A `Paint` value axis for distance from a line (the rift), as the slope axis is |
| Floating island with a gorge | The rift had to join the body before the underside cone | `terrain.root_depth` over a body mask and `island_bottom` that both know a gorge floor |
| Water held at banks after everything is built | A pass that reads `loose_water` and fixes it | `audit.loose_water` returning the fix (bank or fall) as well as the fault |
| Gravel and snow left hanging | A settle pass | a `settle(w)` in the library, run before save |
| Flights in the plan raster | Moved the terraces and flights into `plan.py` | `Raster` support for a flight cut out of made ground, shared by the plan and the builder |
| Pictures of banners | — | tile entities in `render_world.cs` |
