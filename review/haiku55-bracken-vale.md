# Bracken Vale — a destroy valley, built

> A destroy board, two teams of sixteen, a slow river crossing the valley between two wooded banks, one
> monument a team on a hub bench, a watermill on each bank, a roofed cellar a player drops into, and valley
> sides rising from both flanks of the lane.

**In one sentence:** an autumn river valley where a monument stands on each team's hub bench forty-four
blocks from its own spawn, a single bridged channel runs between them, and the valley's flanks rise as
terraced ground that nobody needs to walk.

Two hundred and eight blocks spawn to spawn (`−104,0` to `104,0`), `rot_180` about the origin, base
surface 10, the floor solves to y14 and the flank ridges to y38. Built on the deployed studio, change 20.

## Where the brief's six things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy board, two teams of 16 | one `cube-4` destroyable a team, ender stone, float 4, `maxPlayers` 16 | destroyable-0 at `(−57, 0)`, destroyable-1 at `(55, −2)`; export gate **OPEN** |
| a slow river across the board between the sides | a `canal` channel, `radius` 9, `depth` 4, `level` 9, gravel and sand shore 3 | channel centreline `(−2,−40)`→`(5,−28)`→`(−4,−14)`→`(3,2)`→`(−3,16)`→`(4,28)`→`(−1,40)`; `transect fluid river along x` shows the bed at y5 under water at y9 |
| a watermill on each bank | `mill-a` (oak stilt house) on the west bank, fronting the river | corners `(−30,−12)`→`(−20,−5)`, `front: posX`; the east bank's is its image |
| three or more buildings a team | `mill-a`, `cottage-a`, `barn-a`, and the spawn room (`roomStyles.spawn`) | cottage `(−38,6)`→`(−28,13)`; barn `(−72,18)`→`(−60,26)`; all placed with no declines |
| one place players can use below ground | `cellar`: a subtract, a grass floor and a stone roof on a made layer | void `(−52..−40, 14..26)`; column `(−46,20)` reads roof y11–13, air y6–10, floor y5; open along `z 23..26` |
| real relief, not a flat floor | hub bench at 14, valley sides as two `raise` pushes | low 14, high 38, relief 24; `slopes` reads 2,590 scrambled cells and 188 barrier |
| an autumn palette | `Savanna` biome (id 35): grass tint `#bfb755`, foliage `#aea42a` | oaks and birches under the biome's own foliage |

## The lane

The team unit is four pieces: a spawn box, the hub that carries the monument, the floor between the hub and
the river, and the river's own on-axis piece (`mirrors: false` was refused, `PL12`, so it is fanned onto
itself). `rot_180` makes the lane. The spawn sits four blocks inside its piece with sixteen blocks of ground
ahead of its door, and the monument stands at `(−57, 0)`.

**Goal distance:** own 44, enemy 162, ratio **3.68**, inside the GO1 band of 3–4 and the `L/5`–`L/4` gate
(41–52 blocks). The first placement put the monument at 55 blocks and the ratio at 3.07; moving it to 44
blocks is what the number says the arithmetic wanted.

## The valley sides

The brief asks for real relief, and the valley got it from two `raise` pushes, each a ring standing on the
land's edge: north `x −108..−36, z −36..−20`, south `x 36..108, z 20..36`, both with `amount` 14, `falloff` 12
and `crown` 10. The first version put the rings wholly outside the land, and a ring over the void lifts
nothing, so the sides disappeared from the picture while the numbers still passed. The land had to extend
past the ridges, by four blocks on each side, for them to stand as a slope and not a cliff over the void.

The 188 barrier cells are four faces. The largest, 92 cells at `x 39..52, z −27..−14`, is the rim of the east
cellar, which is the west cellar's image; I did not trace the other three.

The sides are finished by their angle: turf to 40°, coarse dirt to 50°, then stone and andesite with
cobblestone at most a third. The turf cut was raised from 30° once `slopes` showed the north side reading as
a bare grey wall, and the rebuilt picture shows turf on the upper shelves and layered rock below.

## The cellar

A roofed room under the hub, built from the cutting-a-hole card's `a-room` panel: a subtract for the void
(`floor 6`, `base_height 5`), an override floor (`floor 0`, `base_height 6`, `relief_scope: exclude` — without
that, `SK14` reports the relief re-topping the floor's columns), and a ceiling on a made layer (`floor 11`,
`base_height 3`). The roof stops at `z 22`, leaving the last four blocks open, so a player drops in and cannot
climb back. The drop is nine blocks, and that entrance is the one thing on this board I would revisit first.

## What went wrong, and what the numbers say now

- **The valley's flanks are not on any journey.** `coverage` reads 54.4% of the ground dead, and `flow`
  names the two stretches: about 4,900 blocks at `(0, −28)` and 4,300 at `(0, 24)`. These are the river's
  banks north and south of the lane, which no spawn-to-monument walk crosses. The plan-level `LN5` fires at
  62%. Narrowing the valley from `z ±52` to `z ±40` cut the figure from 67%, and I did not find a
  composition that brings the flanks onto a route without moving an objective, which the brief does not allow.
- **The steps are walkable everywhere a player walks.** `routes` worst step 0 on both spawn-to-monument
  walks. Only the sides are steep: 2,590 scrambled cells and 188 barrier, and the largest barrier face is the
  east cellar's rim.
- **Every decline was a placement mistake, not a design one**: a tree on andesite (`DR-ROOT`), a cottage
  on a wall's skirt (`DR-DIG`), a birch in front of a spawn door (`DR-KEEP`), a barn with a narrow passage
  (`DR-PASS`), a cottage inside a monument's clearance (`OB19`). Each moved and re-driven. The export's
  own gates were **OPEN** on the last store with no declines.

## Techniques used

`relief-on-shapes` (the hub bench and two pushes), `ramp-and-stair` (not used — the cellar's entrance is a
drop, see Open questions), `cutting-a-hole` (the cellar's `a-room`), `water` (the `canal` channel with a
gravel shore; the fluid's `bank` is a cell of gravel and sand), `theme-buckets` (the `meadow` theme's five
buckets, the surface laid on the slope axis), `trees-and-boulders` (oak and birch templates), `a-house-style`
(the library's `oak-stilt-house`, `oak-and-spruce-timbered-house` and `hay-gambrel-barn`). Two themes,
`meadow` and `path`, and no third: a `bank` theme I tried was painting nothing and the census said so.

## Open

See `reports/haiku55-bracken-vale.md` for what could not be said, what went wrong in the run, and the
gameplay questions decided without an oracle.
