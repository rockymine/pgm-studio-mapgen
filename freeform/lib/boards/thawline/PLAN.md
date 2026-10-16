# Thawline — the plan

Destroy the core and destroy the monument, two teams of twenty, one core and one monument a team. Built on pgmvox
by Claude Opus 5.5. `scripts/land.py` is the ground, `plan.py` the places and the objectives, `checks.py` measures
them, `sketch.py` draws them (`renders/00-plan-sketch.png`), and the generator (`gen.py` with `ground.py`,
`places.py`, `flora.py`, `season.py`) reads them and decides nothing they state.

## 1. The identity

**One valley in one week of the year, split along the line where the winter has reached.** Frost holds the north,
where the winter has already come: a glacier behind the hall, snow on the field, spruce on the slopes. Ember holds
the south, the same ground still in its autumn: rust and flame oaks, golden larches, a charcoal burners' yard and
fire in the hearths. Between them the ground has opened along the Thawline, a gorge with lava at its bottom, and
the Rimefire Stack stands in it, half ice and half fire. What a player remembers: the white half and the burning
half facing each other across the lava, and the spire in the middle that is both.

**The ground is one; the season is per half.** Every place is written once, in Frost's coordinates, and built twice
through a `Side` (`season.py`): Frost's where it is drawn, Ember's at its image under the half turn
(x, z) -> (-1 - x, -1 - z), each block's data turned with it. A material is asked for by its role (`wall`,
`trim`, `light`, `path`, ...) and the palette answers for the season. So the two teams fight over the same ground,
block for block, and only what it is made of differs.

**The season also runs across each half.** `depth` is 0 at the rift and 1 at the board's back. Frost's front is
autumn under the first snow, its back deep winter; Ember's front is plain autumn, its back a burnt and burning
charcoal country. Both lips are autumn, so the two seasons meet in the middle rather than at a line.

## 2. The arrangement

One floating island 128 by 200, cut across its middle by the Thawline: 7 to 24 wide, a gorge 27 deep with lava at
16, crossed only by building. The Stack's island stands in the middle of it, five from either lip. Each half is a
field rising from 40 at the lip to 50 under the spawn, with the Glacier behind the spawn.

| Place | Where (Frost's) | What it is, and why a player goes there |
|---|---|---|
| **Rimehall** (spawn) | terrace at 53 round (0, -86) | Made ground at the back, the hall on its back edge, the Glacier rising behind it; the Hall Stair (53 down to 50) at its front |
| **the Glacier** | z -100 to -90 | The ridge behind the spawn: packed ice on its steep ground and its crest, icefalls between two spurs, three frozen falls down the back cliff. Frames the spawn; nobody fights there |
| **the Kettle** | (-36, -56), floor 40 | A kettle hole 7 deep, 20 across; the **Frost Heart** (core, 5 by 5 by 5) hangs 8 over its floor, four ice spires on its rim |
| **Hoarcrag** | (-55, -64), top 60 | A tor at the coast west of the Kettle; the Crag Path climbs its south side from Rimewood |
| **Coldwater** | (-20, -37) | A tarn between the middle and the Kettle; the **Culvert** runs from its north shore under the rim to the Kettle's floor |
| **Rimewood** | x -62..-35, z -46..-15 | Twelve oaks between the rift and the Kettle, on two drumlins |
| **Lantern Green** | disc at 48 round (31, -55) | A paved terrace, its floor a rose (six arms for Frost, eight for Ember); the **Frost Lantern** (monument, three obsidian) floats 4 over its middle; two flights, west and south |
| **Hoarstead** | x 24..60, z -66..-18 | The hamlet on the Rime Beck: the Reeve's House, the Smithy, the Mill House and its wheel, Beck Cottage, an ice house, the hay yard; two bridges |
| **the Moraine** | z -49..-43 | The low ridge the ice left across the middle field, broken by the Knoll Road's pass |
| **the Knoll** | (10, -30) | A rise in the middle field with the Frostwatch, a ruined tower with a hoarding and a beacon |
| **the middle field** | z -42..-12 | Erratics, two old field walls, drumlins: cover in the open between the lip and the goals |
| **the Thawline** | z about -7..6 | The gorge; icicles down Frost's wall, lava falling down Ember's; the becks fall into it |
| **the Rimefire Stack** | (0, 0), island at 44 | A pillar out of the lava, waisted and ledged, with a 36-high spire: the north half ice, the south half coal and obsidian with fire on its tip |

The roads: the Hall Road (spawn to the junction), the Kettle Road, the Green Road, the Knoll Road through the
Moraine's pass, the Rift Road to the Stack's bridgehead, the Wood Path through Rimewood, the Beck Lane, the Mill Road
and the Reeve's Walk over the beck, the Crag Path up Hoarcrag.

### The approaches

**The Frost Heart** is reached four ways that are not the same way twice (`approaches.md`):

- *through* Rimewood, cover to within twelve of the Kettle's rim, from the west lip;
- *around* Coldwater, which splits the middle into a west and an east way in;
- *above* from Hoarcrag: the Crag Path climbs to 60, eight over the Heart's top, and a bridge of about eleven crosses to it;
- *below* through the Culvert, from Coldwater's shore to the Kettle's floor under the Heart.

**The Frost Lantern** stands on its terrace east of the hall: *through* Hoarstead and over its bridges from the
east, *up* its two flights (west from the Green Road, south from the Moraine's east end), or by towering up the
terrace's three-block face anywhere else.

## 3. The numbers, each with its target

From `renders/plan-check.txt` (the plan raster, octile walks, the rift crossed by building):

| Number | Target | Plan |
|---|---|---|
| Own spawn to the Heart / the Lantern | GO4: 40 to 90 | 44 / 41 |
| Enemy spawn to the Heart / the Lantern | GO3: 85 to 150 | 148 / 148 |
| Enemy walk over own walk | GO1: 3 to 4 | 3.37 / 3.65 |
| Degrees off the line between the spawns | corpus median 42 | 54 / 49 |
| The Thawline's width away from the Stack | at least 7, never jumped | 7 to 24 |
| Gap from a lip to the Stack | 4 to 6: bridged | 5 |
| Dry walkable ground nobody reaches | only the Glacier and spurs behind the spawns | 5.0%, all of it there |
| Land | under 24,000 columns | 20,872 |
| The Heart over the Kettle's floor | its leak (5) reachable | 8 |
| The Lantern over the green | at least 3 | 4 |

## 4. The look, decided now

Biomes: **Ice plains** over Frost's back (cool grass under the snow), **Mesa** over all the autumn (its grass and
leaves olive-brown), **Savanna** under Ember's larch crowns (gold). Three tone families a half:

- *ground*: Frost snow with stone and andesite where steep, the autumn floor (grass with podzol and coarse dirt
  patches) showing through at the front; Ember the autumn floor, leaf litter under every crown, and the cinder
  ridge (coal, black clay, obsidian) at the back.
- *built*: Frost stone brick, polished andesite and spruce, dark roofs stepped in cubes with snow on every step;
  Ember brick, acacia and oak posts under dark oak roofs, a granite floor.
- *accent*: Frost packed ice and sea lanterns; Ember lava, fire, glowstone. Autumn crowns carry orange, red,
  yellow and brown wool among their leaves (rust, flame and copper crowns), the colours no biome tint gives.

## 5. What the build adds that the plan does not show

The underside (a cone with flutes and spires; the gorge sheer to its floor), the beds of rock, the snow drifts, the
crowns' snow, icicles under Frost's coast and down its rift wall, lava falls down Ember's wall and off its back,
the becks' falls into the rift, the ice snout where the beck leaves the Glacier, the lamps, braziers and banners at
the hall, ground cover (bracken, mushrooms under Ember's oaks, dead stalks). None stands on a road, a terrace, the
lip or within four of a goal's ground; trees are planted only where both halves' copies stand whole on land.
