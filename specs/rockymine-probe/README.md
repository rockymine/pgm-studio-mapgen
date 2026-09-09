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

Load it with `POST /map/from-documents` under a slug of the run's own, so a run never writes to the board it
was copied from. The harness for that is `mint.py`, outside this repository beside the texture work.

Authored by rockymine, 2026-09-09.
