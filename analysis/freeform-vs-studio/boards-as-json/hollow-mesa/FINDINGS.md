# Hollow Mesa as layers: findings

> Written by a Sonnet 5.5 helper agent on 2026-10-10 and saved by the parent session; the measuring scripts stayed in
> the agent's scratch directory. `ANATOMY.md` and `hollow-mesa.layers.json` beside this file are its other outputs.

## How the board is expressed today

Python, 2,304 pipeline lines. `gen.py` runs `terrain`, `underground`, `buildings`, `dressing` on the red half
(x < 0), `rotate.py` turns it into blue, `write_world.cs` writes region files. No pgmvox import (`house.py` is dead
code). The ground is a numpy heightfield written column by column (97.2% of 1,792,366 blocks); the rest is loops of
`w.set`, one template function per building kind, and tree block lists stamped from `trees.json`. `map.xml` is a
hand-written 71-line file copied by `build.sh:17`; its coordinates are typed a second time, and the blue spawn
rectangle is one block off the half-turn of red's (z -16..9 against -17..8, measured). Blue is `rotate_world`:
reverse the red arrays in x and z, remap data values through a 256 x 16 table. A plain run takes 1.9 s and
reproduces the committed world exactly (0 differing blocks).

## Share of the board

| View | A | B | C |
|---|---|---|---|
| All blocks | 98.76% | 1.21% | 0.03% |
| Without the ground rule | 55.2% | 43.7% | 1.1% |
| Exposed blocks | 88.9% | 10.9% | 0.3% |
| Seen from above (columns) | 88.6% | 11.1% | 0.4% |

Seen from above: terrain 68.8% (all A), dressing 14.2%, canyon town 13.7% (B 7.6, A 5.7, C 0.4), mesa buildings
3.2% (B), underground 0.2%. C is one structure, the tipple (264 blocks a half); counting every single-use structure
as C gives 0.37% of the world.

The 130 layers: 47 existing pgmvox ops as they stand (judged from signatures, not run), 9 existing with one more
parameter, 25 studio concepts, 10 layers of 9 new ops, 38 template placements (13 templates), 1 made.

## Would the agent lose freedom?

**Little, and in one place.** The agent still writes a script; it emits 130 layers (68 KB, 32 KB of parameters,
against 101 KB of Python). What the vocabulary cannot say today:

- **Canyon cross-section** (floor, cliff, bench, cliff, plateau, wandering edges): 598k of the 718k height-blocks the
  heightfield stages move. New op `landform.profile`; `landform.canyon` only cuts.
- **Parameters**: wash floor ramp, scarp gullies, elliptical butte with tier, spire profile, per-point tunnel radius,
  soil patches by noise quantile.
- **New ops**: arch (5,888 blocks), spire field, island outline, falls off the island, vertical bore (hole, well),
  catwalk, rails with corners, team recolour.
- **Templates (13)**: false front, adobe (chapel is a variant), plaza, water tower, trestle, headframe, walled
  compound, fence, windmill, tank, fenced plot, hitching rail, wagon.
- **Made**: the tipple. It moves and turns as a unit; its stair, chute and bin are no longer parameters.

**The real loss is feedback inside the script.** `L.H` is regraded as buildings land and later steps read it
(13 sites, `ANATOMY.md`). A script that only emits JSON has no world: it keeps its own ground model (a second copy
of the system) or reads back from the studio between posts. Every read here is a small query (ground at x,z;
median under a box; first rock face west; first air above), so ops can own them.

## Problems the JSON form brings

- **Order is meaning**: pave after footprints, scatter after pave, scrub last, shaft after the catwalk, arch as a
  storey of its own. Layers need `reads` and a storey flag.
- **Randomness**: four module streams consumed in call order. Seeds per op give a valid but different world.
- **Symmetry**: exact only if every op is clipped to x < 0 and blocks are remapped; plaza and spring are two
  half-discs.
- **Size and speed**: neither matters (terrain 0.4 s); a ground edit re-runs the 1.74M-block step.
- Hand-typed `map.xml` numbers disappear if pieces derive from layers: a gain.

## What removes the escape hatch, by blocks

1. Ground stack (`landform.profile`, `mask.island`, `lay` patches): 1,742,764
2. `false_front`: 10,364
3. Trees (existing): 10,360
4. `adobe`: 6,520
5. `form.arch`: 5,888
6. Greening, scrub, pave (existing): 7,386
7. `walled_compound` 1,597; `water_tower` 1,060
8. `trestle` 580; stair tower (tipple) 528; `headframe` 326; `windmill` 324; rails 230

## The cores and the play pieces

**The core** is a 4 x 4 x 4 obsidian shell with 2 x 2 x 2 lava, written by a triple `w.set` loop
(`underground.py:70-90`), x -67..-64, y 79..82, z -26..-23. Ground there is y73, so it floats five blocks (74..78
air). A 2 x 2 well runs from the Throat's floor (y47) up to the ground, ringed by 12 brown clay blocks. The hole
(r 3.2, centre (-65,-24)) is a cylinder from y47 to y0, about 40 blocks of rock; all four well cells lie inside it.

**The leak is geometry.** By the studio's rule a core leaks when lava reaches y <= 79 - 5 - 1 = 73, the well's
mouth. Lava from the casing's floor falls through the well, the cavern and the hole to the void. Lava from a breach
elsewhere stays at y74 on the plateau until it finds the well (not simulated). `no-void` over `everywhere` stops the
hole being plugged.

**Contract against look.** Contract: two `<core>` lines (`leak="5"`), two cuboids, the `no-void` filter and apply,
spawn protections, and each core's 64 casing and lava blocks. The well and hole are contract by consequence: they are
the leak. Cavern, catwalk, shaft, adit and the 12-block ring are look and route.
