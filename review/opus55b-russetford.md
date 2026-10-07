# Russetford — an autumn river valley, built twice

> A destroy board for 16 a side: a meandering river through the middle of one valley, a farm, an orchard,
> a mill hamlet and a wooded hill with a ruin on each side, one monument a team on the village green.

**In one sentence:** the Russet winds through the bottom of an autumn valley, and each team holds one side.
Its spawn is a farmhouse under a wooded ridge, with a hay barn across the yard. Below that an orchard
runs down to a cut bank with a cave in it, and the monument stands on the village green where the lanes
meet. The street runs east past cottages and a well to a mill on a leat, and above the village a hanger
of oaks climbs to a ruined tower.

128 × 192 blocks, one landmass, `rot_180` about the origin, ground y21..50, water y20. The biome is a noise
mosaic of Plains, Savanna and Mesa, so the grass and the oaks come out green, gold and russet in broad
regions. `specs/opus55b-russetford/composition.md` is the zone plan the board was built from.

## The first build, and why it was rebuilt

**The first build was a ramp with three houses on it, and the author said so.** The river was two straight
strips of water along the coasts of two islands, with sixteen blocks of void between them under a build
zone. That reads as two canals with a hole in the middle. The rest was one brown slope: a spawn on the hill,
a monument ahead of it, a wood beside the monument and half the board dead.

**The rebuild started from a drawing, not from the relief.** Every zone in `composition.md` states what a
player is doing there or what it frames. The relief, the shapes and the dressing were then authored zone
by zone, and the board was looked at from above and from a player's eye after each pass.

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy, two teams, 16 a side | one obsidian `pillar-3` a team, `float` 4, on the green at `(4, −56)` | teams `max="16"`; `GO1` own 44, enemy 138, ratio 3.14 |
| a slow river between the sides | one `fluid` channel, an S through the origin, radius 6, `level` 20 | water y19–20; the S is its own image under `rot_180`, so each bank has one cut cliff and one gravel beach |
| a watermill on each bank | the mill (`spruce-roofed-stone-longhouse`) on a leat, a slatted wheel in the leat, an axle into the wall | wheel at `(36, −21)` over water y19–20 |
| real relief | ridge 48, farm 40, green 32, orchard 28, village 24, flats 21, hanger summit 42 | `low 21, high 50, relief 29`; 4.3% of steps further than a player walks |
| three buildings a team | farmhouse (spawn), hay barn, mill, miller's house, three cottages, a ruined tower | all standing; `DR-PASS` complaints only, on the village alleys |
| one place below ground | a cave from the cut bank at water level, under the orchard, to a chamber under the green's west lip | `walk (−28,−19,21) → (−7,−55,22)` walked end to end, worst step 0 |
| an authored plan | five pieces, no zone: the valley crosses the axis | one island |

## How it is meant to play

**The river is the front, and it is crossed three ways.** The stone bridge in the middle is the one dry
crossing. Anywhere else it is swum, and the bank the swimmer climbs out on decides the approach.

**At the west bend the attacker lands on the defenders' cliff.** The cut bank stands six to seven blocks
over the water under the orchard. It is bridged up, or the attacker swims into the cave mouth at its foot
and walks under the orchard to a chamber nine blocks from the monument's anchor, then digs up.

**At the east bend the attacker lands on the defenders' water meadow.** The holm is low and open between the
river and the leat, under the village. Two footbridges cross the leat into the mill yard. From there the
village street is cover, house by house, up to the green.

**The hanger is the height beside the monument.** Its oaks give cover to within about twenty blocks of the
green's east side, and its summit with the ruin is ten blocks above the green. It is the place to bridge
down from.

**The defender's walk is 44 blocks, down from the farm past the hay yard to the green.** The monument is 32
blocks ahead of the spawn and 26 aside of the line to the enemy spawn, 38° off it, and the farm looks down
on it.

## What the ground is made of

**Four themes: the valley, the hanger's leaf floor, the gravel bars and the field.** `valley` is grass to
30°, dirt and coarse dirt half and half to 42°, then stone and andesite with cobblestone. `wood` is podzol
with grass and coarse dirt inset, carried to 42° because the hanger's oaks stand on its slope. `beach` is
gravel with sand and andesite patches on the two point bars, and `field` is farmland the flora sows with
wheat and potatoes.

**The built family is three house types, none of them timber-framed.** The cottages are white clay under
spruce, two are stone under brick, the mill is a stone longhouse and the barn has a hay gambrel roof. The
accent is dark oak: the wheel, the axle, the cave's portal timbers. The bridge, the tower and the walls are
stone.

**What is laid over the ground is the farming landscape.** Hedges of non-decaying oak leaves run round the
field and along the bridge lane with gaps for gates, and one crosses the meadow above the cut bank.
Dry-stone walls cross the saddle pasture. The cottage gardens are fenced, with pumpkins in them, and the
farm yard has hay bales. The woodcutter's clearing on the hanger has a log pile and two stumps.

## The techniques, and what each one bought

| Instrument | Where | What it bought |
|---|---|---|
| a plan crossing the axis with no zone | the valley | one landmass; the river is the seam rather than a void |
| a `fluid` channel through the origin | the Russet | a meander whose bends give each team one cliff and one beach |
| a second channel, `form: canal` | the leat | the holm as an island, and the mill's water |
| eleven `area` marks and one `line` | farm, fields, ridge, green, village, mill yard, holm, bridgehead, orchard foot, hanger | each zone at its own height, the slopes between them solved |
| a summit mark instead of a push | the hanger | a hill graded to the village; the push it replaced gave 55–60° at its foot |
| override add with a `floor` over a `below` layer | the cave | three courses of air under relief-solved ground |
| `polyline` shapes, `height_mode: drape` | hedges, walls, fences | field boundaries laid over the slope at a constant height |
| made layers, three of them seated | bridge, wheel, footbridges, well, tower, hay, logs, pumpkins, cave mouth | the made things a valley is lived in with |
| a noise `BiomeField` | the whole board | autumn colour in regions rather than one brown |

## What went wrong in the rebuild

**The hanger's push built 55–60° slopes at its foot.** A push is added after the marks, so its skirt lifted
the village's ground and steepened every edge it met. A summit mark that the solver grades down to the
village's own mark replaced it.

**The cave's mouth was sealed by two rows of bank.** The polygon stopped short of the water, so the river
met solid ground. The polygon now runs into the water's edge.

**The hedges were first stated in decayable leaves.** They would have vanished in game, though every read
showed them. `18:4` is the leaf that never decays.

## Standing complaints

| Rule | Where | Why it stands |
|---|---|---|
| `DR-BANK` | the cut bank at `(−33, −19)`, the leat at `(23, 4)` | the cut bank is the point of the outer bend |
| `DR-PASS` | the village | the alleys between the mill and its neighbours are lanes, deliberately narrower than eight |
| `SK9`, `SK14` | `cave-roof` | the override is meant to replace the ground there; `column` reads the roof and the air under it |
| `DR-CUT` | `ridge-3` | fourteen blocks of root trimmed on the ridge's slope |
| `EL1`, `SP8` | the spawn piece | the plan tier walks pieces flat; the farm's mark seats the house level |

## Coordinates

| Thing | Red (authored) | Blue (image) |
|---|---|---|
| spawn | `(−32, −76)`, ground y40 | `(31, 75)` |
| monument | `(4, −56)`, green y32, obsidian y36–39 | `(−5, 55)` |
| bridge | `x −2..2, z −12..12`, deck y25 | the same |
| cave mouth | `(−28, −20)` | `(27, 19)` |
| cave chamber | `x −11..−3, z −60..−47`, floor y21 | `x 2..10, z 46..59` |
| mill wheel | `(36, −21)` | `(−37, 20)` |
| tower | `(50, −86)` | `(−51, 85)` |
| well | `(43, −50)` | `(−44, 49)` |
