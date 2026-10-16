# Rimeburn: report

## Concept, and how it reads the theme

The board is **one land in two seasons.** Frost (aqua) holds the north in deep winter and Ember (gold) holds the south in the last of autumn. The geometry is identical under the half turn, so the match is fair. Only the season differs, and a player knows which side they stand on from any distance.

The objectives carry the theme as well. **Every team guards a fire and an ice:**
- **The Hearth** is a core of lava in obsidian. It floats over a fire ring in a hollow whose snow has melted to wet leaf litter.
- **The Icestone** is a monument made of packed ice. It floats over a quartz dais on a mesa, ringed by four ice spires.

Frost therefore keeps a fire alive in the snow, and Ember keeps the last ice of the year among its red trees. The theme also shows in smaller places:
- **The Thaw:** in the void between the lands, the snow line wanders across a neutral island, and a fire burns on a deck over it.
- **The burn:** it runs from the Rime Falls to the Tarn. It is frozen on Frost's side and running water on Ember's.
- **Ember's peaks:** they keep the first snow of the winter above y 58.

**Mechanically, the second season is a translation.** Frost's half is laid and built as winter. A copy of it is re-seasoned block by block (`scripts/season.py`) and turned onto the south. The table separates terrain from what was built, and paths from open ground:
- snow becomes Mesa grass;
- packed-ice patches become podzol;
- spruce walls become acacia;
- dark-oak roofs become nether brick;
- ice becomes water.

Each season then gets its own trees and dressing. Frost has spruces with snow on their boughs. Ember has oaks and maples in brown leaves with orange and red wool, and fallen leaves as carpets.

## Modes, and how each objective is approached

This is a Destroy the Core and Monument board (`dtcm`). Each team has one core and one monument and must lose both. Each goal floats (5 air under the core, 3 under the Icestone). Each sits off to one side of its spawn (59° and 60° off the line between the spawns) and has approaches that differ:
- **The Hearth (west):**
  - Around: over the open front, past the March dyke and the knolls.
  - Above: the Anvil, a rock stack with a ledge path whose top stands 8 above the core's top and about 15 away. It is a place to bridge down from.
  - Below: the Vent, a lit passage from the coast's cliff that is reached only by building across the seam. It comes up in the hollow's south wall.
  - Through: the spruces (maples) on the west flank.
- **The Icestone (east):**
  - Up two stair cuts into the mesa: the west one from the Hold and the south-west one from the Tarn.
  - Across the Tarn's open ice.
  - Through Rimecroft's three houses.
  - Around the east coast.

**The lands meet only over void.** The seam (z -26..25) is all build zone. There are three ways across:
- straight across, at least 23 blocks;
- the west and east straits between the headlands;
- the Thaw island in the middle, 11 blocks from each land, with a deck on four legs. This is the fight to hold the middle.

Kit: an iron sword, a bow, and a diamond pickaxe for the core's obsidian, plus an axe, the team's planks, glass, golden apples and food. `doFireTick` is off, so the many fires never spread.

## Layout and proportions

- **Size:** the board is 128 by 192, the spawns stand 156 apart, and there are 18,836 columns of land. The void seam is the only void inside the board, and the land is roughly 75% of the footprint.
- **Teams:** 24 per team at most.
- **Walks:** measured in the plan and in the built world.

| | plan | built world (moves) | target |
|---|---|---|---|
| own spawn to the Hearth / Icestone | 41 / 40 | 38 / 39 to 40 | GO4 40 to 90 |
| enemy spawn to the Hearth / Icestone | 141 / 147 | 131 to 132 / 137 | GO3 85 to 150 |
| ratio | 3.48 / 3.64 | 3.4 / 3.5 | GO1 3 to 4 |

**Heights:**
- spawn terrace 46;
- Rimewall crest 60 to 70;
- hollow floor 34, rim 40;
- mesa 45;
- Anvil 52;
- front 36 to 38;
- Thaw 38, deck 44;
- kill height 20.

## Palette

| role | Frost | Ember |
|---|---|---|
| biome | Ice Plains | Mesa (olive-brown grass, brown leaves) |
| ground | snow, with packed ice inset | grass, with podzol (leaf litter) inset, and leaf carpets under the trees |
| slopes | stone and andesite scree past 32°; rock beds of stone, andesite and cobble past 40° | the same rock, with coarse dirt for the gravel |
| paths | andesite, cobble and polished andesite, a third each | coarse dirt, dirt and spruce planks |
| built | stone-brick foot, spruce walls on spruce posts, dark-oak roof, snow on top | stone-brick foot, acacia walls on dark-oak posts, nether-brick roof |
| water | ice on still water | water, with riffle stones at each fall |
| accent | netherrack fires, nether-brick hearthstones, sea lanterns | the same fires, glowstone, pumpkins, tulips and poppies |
| both | packed-ice spires and Icestone, quartz dais, obsidian core | |

## What was checked

- **`plan_check.py`:** every row passes, including the studio's goal bands GO1, GO3 and GO4, equal walks for both teams, bridge widths, unreached ground (1.7%) and the land count (`renders/plan-check.txt`). The sketch is `renders/00-plan-sketch.png`.
- **`walk.py` on the built world:**
  - every goal is reached from its own spawn on foot and from the enemy spawn with the seam bridged;
  - the Vent walks end to end in 36 moves on both sides;
  - nothing can be stood on over the void outside the lands and the seam;
  - every block has footing;
  - objectives with a problem: 0, so the core holds lava, the floats are right and the columns are marked at y 0.
- **Studio parser** (`read_mapxml.cs`): `valid: true`, no issues.
- **Renders:**
  - Flat-colour reads: `05-topdown-annotated.png`, plus two cutaways.
  - Textured, through the studio's renderer:
    - the board: `20` to `23`;
    - each goal: `30` to `33`;
    - the Thaw: `34`;
    - both Holds: `35`, `36`;
    - both crofts: `37`, `38`;
    - the Anvil: `39`;
    - the Vent: `40`;
    - the ground of each half: `41`, `42`.
  - Several of these were used to fix things:
    - the back of the island was a sheer wall 40 high, because the grid's edge counted as land in the taper;
    - the Vent opened under the island's thin edge;
    - the burn stood as a water column on the ridge;
    - the Hold's yard and the warm hollow were snowed over;
    - the Thaw had a ruled season line;
    - clay crowns read as 2-block cubes, and were replaced by single-block wool clumps.

## What did not work, or is left

- **Two water sources remain against air** at the top of Ember's Rime Falls (21, 58, 92..93). They sit on the back of the ridge, out of play. The rest of the fall is falling water.
- **A few blocks differ between the halves.** The walks are 1 move apart because trees and flowers are placed by each season's own random draws. The geometry and the objectives are exactly symmetric.
- **The renderer draws no fire**, so the braziers read as netherrack knobs in the pictures. In game they burn.
- **The Icestone breaks fast.** It is packed ice, which breaks quickly, so the monument is a fast objective against the slow obsidian core. That is deliberate (the ice is the brittle one), but it is untested in play.
- **Ember's meadow is a muted olive.** The Mesa tint is what makes podzol and grass one floor. The autumn colour comes from the trees, carpets and flowers rather than from the ground itself.
- **The plan raster does not walk the Anvil's top.** Its ramp heads at 52, but the top cells' jagged edge left 1 to 2 cells the plan graph does not reach. The built walk does reach the Anvil.

| wanted | how hard | what a library or studio feature would need to do it |
|---|---|---|
| the same land in two seasons | easy once found: copy, re-season by table, turn | `turn_world(recolour=)` keyed on (terrain/made, column mask) rather than block alone |
| autumn crowns | wool clumps over Mesa-tinted leaves, by hand | a `trees` recolour by clump field |
| a floating island's underside at the board's edge | a 6-cell pad | `island_bottom` treating the grid edge as void |
| riffle stones where a stream steps | written locally (`ground.weirs`) | `watercourse` returning its falls' sills, or `hold` filling to the higher surface |
