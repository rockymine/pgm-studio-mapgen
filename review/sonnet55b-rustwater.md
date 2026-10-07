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
| three buildings a team | spawn hall `(−27..−13, −99..−85)`, barn `(−6..3, −102..−95)`, cottage `(−14..−5, −54..−47)`, mill | all four in one hay-and-dark-oak family, the mill in its own |
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
accent the gold of the roofs and the monument. Paths are a third each of coarse dirt, spruce planks and gravel.

## What went wrong

The relief was never sketched more than one way: it was built once and tuned by `level`, which began at 0.27
under the steep flanks and reached 0.41 after the shelves were widened.

27.5% of the ground is dead because the
spawn's own piece is a keep-out for trees, and the east half of it lies off every journey.

The river is two
half-rivers with the void between them. The paths read faintly on brown ground and no picture from a player's
eye was drawn to check them.
