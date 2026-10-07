# Rustwater Vale — an autumn river valley, authored plan

> A destroy board for two teams of sixteen: two hillsides face each other across a slow river, each team
> holds the bank and the slope above it, and a gold millstone stands on a terrace below each spawn hall.

**In one sentence:** an olive-brown autumn valley whose two sides run down to a river, with a spawn hall on a
shelf under a ridge, a gold Millstone on a terrace below it and to the east, and a dark-oak watermill at the water.

112 × 232 blocks, `rot_180` about the origin, biome Mesa (`#90814d` grass, `#9e814d` leaves), y 12..43. One
landmass a team, 24 blocks of build zone between the banks (`CT12` band 15 to 40).

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy, 16 a side | one `cube-3` of gold block a team, `maxPlayers` 16 | `<gamemode>dtm</gamemode>`, two teams of 16 in `map.xml` |
| a slow river between the sides | a `stream` fluid on each bank, `level` 13, depth 2, five blocks either side of its line | water at y13 along `z −25..−15`, x −26..24; its mirror at `z 15..25` |
| a watermill a team | the library style `dark-oak-quay-warehouse` at `(−12..−3, −34..−28)`, door to the hill | three blocks from the water; no wheel (see the report) |
| real relief | seven relief marks and one push, a stair of terraces 14, 19, 26, 32 and a ridge at 40 | y12 to y43; 38% of the ground under 10°, 9.5% at 40° or steeper |
| three buildings a team | spawn hall `(−27..−13, −99..−85)`, barn `(−6..3, −102..−95)`, cottage `(−14..−5, −54..−47)`, miller's house `(5..12, −37..−32)`, mill `(−12..−3, −34..−28)` | a row of plain rubble cottages with dark-oak roofs, one gambrel hay barn, one dark-oak quay mill; none is beamed except the mill |
| somewhere to go up to | the Watch, a ruined round tower on the fell's crest at `(29, −92)`, y39 to y46, a chest of two golden apples and sixteen arrows on its floor at y40 | `column (29,−91)`: chest y40 on stone y39; reached by the ridge path from the barn yard and the lane down to the terrace |
| somewhere below ground | a cellar under a lid at `(−1..8, −53..−43)`, floor y11, a six-tread flight rising east to y18 | `column (5,−48)`: lid andesite y20, floor andesite y11, air between |

## The spawn's seat

The spawn at `(−20, −92)` stands on ground y32. `transect` from it to `(−22, −114)` reads y32 for 12 blocks, a
climb of 8 to a ridge top at y40, and void at z −114: **21 blocks of its own land behind it, ground 8 above
within 20.**

The barn stands 14 blocks away at its east. No tree stands within 20 blocks, because the spawn's
own piece is kept clear and the two trees tried at `(7, −79)` and `(−25, −78)` were declined `DR-KEEP`.

## The goal

The Millstone at `(16, −66)` is 44 blocks from the spawn by line, **33 ahead of it and 30 aside, 42° off the
line to the enemy spawn.** The walk is 50 blocks to its own spawn and 172 to the enemy's, a ratio of 3.4
(`GO1`); to the enemy's goal it is 155 (`GO3`). The terrace under it is a flat of radius 15 at y26.

## The ground and its paint

Two themes. `vale` is the ground: a `layered` stack on the `slope` axis, leaf-littered grass (a `noise` of
podzol and grass, podzol at the ends) to 34°, dirt and coarse dirt to 44°, and stone, andesite and cobblestone
past it, over a fill of stone and andesite. `yard` is made ground: a `cell` of stone brick, polished andesite,
andesite and stone on the cellar and its lid.

Three families: ground olive-brown, built dark oak and hay,
accent the gold of the roofs and the monument. Paths are a third each of gravel, andesite and cobblestone, hard ground that reads against the brown turf.

## What went wrong

The relief was never sketched more than one way: it was built once and tuned by `level`, which began at 0.27
under the steep flanks and reached 0.41 after the shelves were widened.

27.5% of the ground is dead because the
spawn's own piece is a keep-out for trees, and the east half of it lies off every journey.

The river is two
half-rivers with the void between them. The paths read faintly on brown ground and no picture from a player's
eye was drawn to check them.

## Revision 2 — a world, not a layout

The author's verdict on the first build was that the land was a fair start and everything on it was unfinished: a
spawn, a terrain and a few houses, with grass over it, and a dead share that falling does not make a place. The
land is untouched in this pass; the plan changes only by splitting the ridge piece in two so the fell is free of
the spawn's keep-out. Everything else is a place with a reason to be visited.

| Place | What is there | Why a player goes |
|---|---|---|
| The Ridge | a crest at y38 to 42 curving east into the fell, a ridge path from the barn yard, boulders, scree, two old oaks | it frames the board and carries the walk to the Watch |
| The Watch | a ruined round tower, doorway south, five merlons, a chest on its floor | the high ground over the Millstone, 26 blocks off, and a reward for the climb |
| Millstone terrace | open flat at y26, a lane from the hall, a lane down from the Watch | the objective, with the wood west, the hill east, the cellar below |
| Haldenwood | oak and birch on the west flank, a leaf-litter clearing with four stumps and two log piles | cover on the way in, and a flank route to the terrace |
| The hamlet | the cottage and the root cellar on the lower shelf, a lane to each | the defenders' ground between the terrace and the mill |
| The mill race | mill, miller's house, an orchard, ploughed furrows with a pumpkin patch behind a dry-stone wall | the valley floor's work, and the way down to the river |
| The river | a footbridge from the mill yard to the water's edge, a jetty and a moored boat | the dry way to the build zone, and a place the water is used |

Every lane joins two of those: hall to terrace, hall to barn, barn to Watch, Watch to terrace, terrace to hamlet,
hamlet to mill, mill to miller, miller to fields, mill to bridge, terrace to clearing, shelf to cellar.

## What was built and how

The Watch is the sculpt toolkit's `ring_wall` with a doorway and a crown of five merlons, as two layers marked
`kind: "made"` and `part_of: "ground"`. A relief pad of radius 5 pins the crest under it, so the tower stands level
without the hill being reshaped.

Stumps, log piles, haystacks and pumpkins are boulder recipes whose rock is a
log, hay or pumpkin block, which follow the ground. The wall round the fields is a `polyline` with
`height_mode: "raise"`, 3 courses of cobblestone, andesite and stone.

The footbridge and the boat are made layers at y14 that name no keep-clear, so the water runs under them. Dressing
now places 90 props over 5 themes; the paint is still three families, olive-brown turf, dark oak and gold hay, and
the added accent is the orange of the pumpkins.

## What is still wrong

27% of the first build's ground was dead and 18.5% still is.

What is left is the spawn's own piece behind the hall,
the Watch's steep outer face and their mirrors, which are ridge and cliff and not ground anyone is meant to cross.

No custom building was designed, so every roof is a library roof. The woodcutter's hut was placed three times and
declined each time by door and building claims, and was dropped.

`DR-PASS` still complains of the hamlet's three
buildings, and a mill wheel is still missing.
