# Curio Square — the brief for a plot builder

Three builders share this board: Opus, Sonnet and Haiku, sixteen plots each. This page is the whole contract. A
plot that keeps to it goes in the square as it is, and nobody else edits it.

## The game

**Hide and seek, as the community's Hide n' Seek maps play it.** Up to fifty hiders scatter over a square of plots
while a few seekers wait, blinded, for twenty-five seconds. Then the seekers come out in diamond armour with iron
swords, and every hider they kill is out. Hiders have nothing but a compass pointing at the nearest seeker and a
potion of invisibility, with another every couple of rounds.

**Every minute, six plots vanish.** Their blocks are cleared to the grass, and anyone hiding on them drops into the
open. The hiders win if any of them is still alive at seven minutes.

**So a plot is a place to climb and hide, not a place to look at.** A seeker walks the streets round it, and a hider
wants to be somewhere that seeker cannot see, or cannot reach quickly. Good plots have:

- **a way up:** steps of one block, ladders, vines, stairs, slabs, fences to hop on, to somewhere at least six
  blocks over the street;
- **places out of sight:** behind a chimney, under an eave, inside a room, between two parts of a sculpture, on a
  ledge round a corner;
- **more than one way in:** a hider cornered with one way out is caught;
- **one idea, read at once:** a lighthouse, a giant teapot, a windmill, a whale skeleton, a pagoda.

## The theme

**Curio Square is the fair ground of an alpine market town.** Each plot is one curiosity at the fair: a house, a
structure or a sculpture. The subject is free, from a fisherman's hut to a giant stack of books. The square is
paved, ringed by the town and walled, with snow peaks round it.

**Mix the three kinds.** Of a builder's sixteen, about five houses, six structures and five sculptures. Sculptures
are the plots nobody else would think of: giant everyday objects, animals, abstract shapes, a statue.

## The contract

**A plot is a Python module with three names:** `NAME`, `KIND` and `build(c)`.

```python
from mc import B

NAME = "The Lighthouse"              # shown in chat when the plot vanishes
KIND = "structure"                   # house, structure or sculpture


def build(c):
    c.fill(3, 0, 3, 7, 12, 7, B.QUARTZ)
    c.set(5, 13, 5, B.GLOWSTONE)
```

**Plots live in `plots/<builder>/`, one file each,** named for the subject: `plots/sonnet/lighthouse.py`. A
file whose name starts with an underscore is not a plot; `plots/_example.py` is one to read.

**The canvas is the plot's own box: x and z from 0 to 10, y from −1 to 23.** A player on the street stands at y 0.
The ground layer at y −1 is grass when the canvas is handed over and may be repainted, never dug through. Nothing
may be set outside the box: the canvas refuses it, and the check fails.

**The canvas has three methods.**

- `c.set(x, y, z, id, data=0)`: one block.
- `c.fill(x0, y0, z0, x1, y1, z1, id, data=0)`: a box, both corners included.
- `c.get(x, y, z)`: the `(id, data)` there.

**Block ids are Minecraft 1.8's.** `scripts/mc.py` names the common ones in class `B`, with their data values in
its comments. Any other 1.8 id may be used as a number.

**Blocks that face a way take it from their data.** Minecraft 1.8's values, with x east and z south:

| Block | Data |
|---|---|
| stairs (any) | 0 rising toward the east, 1 west, 2 south, 3 north; add 4 for upside down |
| slabs | the lower half; add 8 for the upper half |
| ladder, wall sign | 2 on the north face of the block south of it, 3 the south face of the block north, 4 the west face of the block east, 5 the east face of the block west |
| torch | 1 on the block to its west, 2 to its east, 3 to its north, 4 to its south, 5 standing on the block below |
| log | 0 to 3 upright by wood; add 4 for lying along x, 8 along z |
| wool, stained clay, stained glass, carpet | the 16 colours: 0 white, 1 orange, 2 magenta, 3 light blue, 4 yellow, 5 lime, 6 pink, 7 grey, 8 light grey, 9 cyan, 10 purple, 11 blue, 12 brown, 13 green, 14 red, 15 black |

**A plot is plain, deterministic Python.** It uses no imports but `mc`, `math` and `random` seeded with a constant,
reads no files and finishes in under a second.

**Each plot is placed with x pointing east and z pointing south.** It is never rotated, so a front door at z 10
faces south. The four streets round a plot are all used, so every side is seen.

## What is not allowed

- **Lava, fire, TNT, cobwebs, spawners, barriers and bedrock.** The canvas reports them.
- **Flowing water.** Still water (`B.WATER`) in a basin is fine.
- **Sand, gravel or anvils with air under them.** They fall the moment the world loads.
- **Torches, ladders, signs and other attached blocks with nothing to attach to.** They pop off.
- **Doors.** A door a hider shuts behind them is a wall a seeker opens in a second; a doorway is the same game
  with less to break.
- **A space no one can get into.** A sealed room is wasted. A room a hider can reach is the point.

## The check

**`python3 scripts/plotkit.py plots/<builder>/<plot>.py <out.png>` builds the plot alone and checks it.** It walks
every place a player can stand from the street round the plot, as a player moves with fall damage off: a step of a
block, any drop, ladders and water upward, running jumps over gaps of up to three. It prints three numbers and
draws the plot from two corners.

- **Places to stand:** every cell on the plot a player can reach and stand in.
- **The highest:** how far over the street the highest of them is. It must be at least six.
- **Out of sight:** how many of them no eye on the street round the plot can see. It must be at least twelve.
  A seeker sees through glass, panes, iron bars, fences and walls; leaves and solid blocks hide a player.

**A plot passes when the check prints `pass`.** Then look at the two pictures, since a plot that passes can still
read as nothing from the street.
