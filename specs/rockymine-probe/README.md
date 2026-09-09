# rockymine-probe

A hand-authored board, finished and **unpainted**. Ten layers over a `rot_180` map: ground cut by a tunnel
whose walls and cover are their own layers, a pillar-and-rim structure standing over it, planters, two wool
rooms, a bedrock approach wall on the seam between two pieces, and a pair of destroyables in cages built for
them. 80 shapes, 10,714 cells, two islands joined by a build zone.

It carries **no theme registry, no map theme and no dressing**, which is the state it was finished in and the
reason it is here: it is the subject of the colouring probe, where an agent is asked to paint a board that is
already built and nothing else. A board that arrives with paint on it cannot pose that question, and a board
drawn to pose it cannot pose it honestly — the heights, adjacencies and rooms here are ones an author made
for a map rather than ones a fixture was built to have.

## How it is put together, and why that matters

It is authored the way a person authors, which is not how the generator does it, and the difference is part
of what a run on it will show.

The **map** is four layers — `ground`, `tunnel-walls`, `tunnel-cover`, `tunnel-top-2`. The other six are
things standing on it: stairs, pillars, a rim, planters, a cover. **None of them is marked `kind: made`**,
and one object is not one layer — the cover repeats the same elements across plan pieces of different height
by leaning on each shape's own `floor`, rather than by giving every object a layer of its own. A generated
board tends to do the opposite on both counts.

That is left exactly as authored. Whether an agent can tell terrain from a thing standing on it without the
`made` marking to help is a question this board asks and a fixture built to be legible would not.

Two things were corrected, neither of which changes the world: the layers are ordered by `base_y` so the
document reads the way the world stands (`SK20`), and the layer ids are the author's own names rather than
the editor's timestamps, so a finding names something a reader recognises. The built heightmap is
byte-identical before and after.

`PROMPT.md` beside this file is the text an agent is given.

Load it with `POST /map/from-documents` under a slug of the run's own, so a run never writes to the board it
was copied from. The harness for that is `mint.py`, outside this repository beside the texture work.

Authored by rockymine, 2026-09-09.
