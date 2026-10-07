# Russetford — an autumn river valley, built

> A destroy board for 16 a side: a slow river between two valley sides, a watermill on each bank, one
> monument a team on a shelf partway up its own valley side, and a mine adit under that side.

**In one sentence:** each team holds one side of an autumn valley, its spawn house on the ridge at the top
with a crag at its shoulder, its monument on a shelf below and to the east of it, its mill hamlet on the
bank below that, and a timbered adit running from the strand into the hillside to a chamber under the
shelf's west lip.

128 × 204 blocks of land, `rot_180` about the origin, Mesa biome (grass `#90814d`, leaves `#9e814d`),
ground y21..61, build ceiling y51. The two valley sides are two islands; the river's middle is sixteen
blocks of void with the `ford` build zone over it and reaching both coasts.

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy, two teams, 16 a side | one `<destroyable>` a team, obsidian `pillar-3`, `float` 4 | `red-monument-region` `7,37,-61`..`8,40,-60`; teams `max="16"` |
| a slow river between the sides | a `fluid` pool along each bank at `level` 20, `depth` 4, drawn past the coast into the void | water y19–20 from `z −17` to the coast at `z −8`; void `z −8..8` under the build zone |
| a watermill on each bank | `mill` house, hall `x 27..41, z −31..−24`, wing `x 31..37, z −38..−32`; a made `wheel` layer, radius 5, in a pool bay | paddles at `(34, −22)` y22–26 over water y19–20; a dark-oak axle at `(34, −23)` y22 |
| real relief, valley sides | one relief: strand at 21, ridge at 44, shelf at 33, two pushes | `low 21, high 61, relief 40`; 1.8% of steps further than a player walks |
| three buildings a team | the mill, the miller's cottage `x 50..56, z −40..−34`, the pithead `x −31..−25, z −31..−25` | all three standing in `column` at `(34,−28)`, `(53,−37)`, `(−28,−28)` |
| one place below ground | the adit: an open cutting `x −22..−18, z −20..−31`, then a roofed drive and a chamber `x −12..−2, z −55..−43` | floor y21, air y22–24; `walk (−20,−25,22) → (−7,−50,22)` walked end to end, worst step 0 |
| an authored plan | five pieces and one zone, drawn by hand | `GO1` own 43, enemy 150, ratio 3.49 |

## How it is meant to play

**A defender sees the monument from the spawn door and walks 47 blocks to it, downhill.** The spawn house
stands on the ridge at y44; the monument floats over the shelf at y33, 32 blocks ahead of the spawn and 29
aside of the line to the enemy spawn, 42° off it.

**An attacker has four ways onto the shelf, and they are not the same way twice.** Up the open slope
from the ford is the short way and the exposed one. Round the east through the oak wood on the spur is
cover to within a few blocks. Down from the ridge west of the shelf is height, but that ground is the
defenders' own spawn approach.

**The fourth way is under the slope.** The adit opens on the strand beside the pithead, where a bridge from
the far bank lands, and its chamber ends eleven blocks from the monument's anchor with about six blocks
of ground over it. A player there digs up and comes out on the shelf from below.

**The crossing is a bridge, from the first minute.** The river's middle is void under a build zone that
reaches both coasts, so the enemy's walk to the monument is 168 blocks with 18 placed.

## What the ground is made of

**Three themes, one ground and two patches.** `valley` is the board: grass to 30°, dirt and coarse dirt
half and half to 42°, then stone and andesite with cobblestone patches, over a stone fill with andesite in
it. `strand` is the sand-and-sandstone bank along the river, its inland edge drawn ragged by a bend.
`wood` is the leaf floor of the spur, podzol with grass and coarse dirt inset in it.

**The biome carries the season.** Mesa tints grass `#90814d` and oak leaves `#9e814d`, so the meadow is a
dry tan and the oaks turn brown; the copied oaks carry some birch leaves, which the biome does not tint,
and those stay green.

**The built family is white clay under spruce.** The three houses and the spawn house are one library
style, `spruce-roofed-white-clay-cottage`, at three footprints. The accent is dark oak: the wheel's
paddles, the axle, the adit's posts and lintel, the roofs' verges.

**The lanes are one brown.** Podzol, coarse dirt and spruce planks a third each, `solid`, wandering three
blocks every fourteen: spawn door to the shelf to the ford, the shelf to the mill, the ford to the mill,
and a spur to the pithead.

## The techniques, and what each one bought

| Instrument | Where | What it bought |
|---|---|---|
| six `area` marks, `reach` 0 | strand, ridge, shelf, mill yard, bench, pithead | a valley side that ramps between the flats a player stands on |
| two pushes | the crag behind the spawn, the spur east of the shelf | a rise of 12 within 20 blocks of the spawn; a wooded knoll beside the goal |
| `editShapes` + `bendShapes` on `bank-24` | the bank's coast | thirteen moved or inserted points and a bend `in`, so the island is not the box |
| an override add with a `floor` | `mine-roof` | the valley's own ground lifted off a floor, relief still setting its top |
| a `below` layer | `mine` | the adit's floor under the compiled ground |
| an override add, `relief_scope: exclude` | `mine-cut` | the open cutting, taken out of the solve down to the strand |
| two made layers | `wheel`, `timbering` | the waterwheel and the adit's portal timbers |
| a `fluid` pool past the coast | `river` | water meeting the void, with a bay at the mill |

## What went wrong

**The biome stated as a word stored at 200 and refused the export.** `"biome": "Mesa"` is not a
`BiomeField`; the store took it and `GET …/export` answered `RQ1`. `{"kind": "solid", "id": 37}` is the form.

**The two patch themes painted almost nothing at first.** `strand` read 2.4% and `wood` 0.7% of the ground,
because a shape with no `base_height` is one block at y0 and owns no surface. Stated at the ground's own
thickness, 24, they read 16.5% and 12.7%.

**The adit's first mouth was a floating lid.** An override add's top is never lower than its own `floor`
plus one, so where the relief fell below the roof's floor the shape left one block at y25 over the strand.
The mouth became an `exclude` cutting and the roof starts where the ground stands above it.

**The coast bend opened two-block strips of unbuildable void beside the ford (`EZ2`).** The zone was
widened to `z −12..12` so it reaches both coasts.

## Standing complaints

| Rule | Where | Why it stands |
|---|---|---|
| `EL1`, `SP8` | `spawn-room` against its neighbours | the plan tier walks pieces flat; the ridge mark seats the spawn house level with the ground round it, transect `worst step 0` |
| `DR-PASS` | the mill and the cottage | the mill's river side stands on the water by design |
| `SK18` | `(34, −23)` | the axle meets the mill's wall, which is the point of an axle |
| `SK9`, `SK14` | `mine-roof` | the override is meant to replace the bank there; `column` reads the roof and the air under it |
| `RL5` | group `team` | flats are the strand, ridge, shelf, yard and bench; the rest is valley side |

## Coordinates

| Thing | Red (authored) | Blue (image) |
|---|---|---|
| spawn | `(−32, −80)`, ground y44 | `(31, 79)` |
| monument anchor | `(7, −61)`, shelf y33, obsidian y37–40 | `(−8, 60)` |
| crag summit | `(−56, −86)`, ground y60 | `(55, 85)` |
| mill wheel | `(34, −22)` | `(−35, 21)` |
| adit mouth | `(−20, −31)` | `(19, 30)` |
| adit chamber | `x −12..−2, z −55..−43`, floor y21 | `x 1..11, z 42..54` |
| the ford | build zone `x −64..64, z −12..12` | — |
