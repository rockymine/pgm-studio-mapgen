# 23 — a maze, and the rule that makes both halves the same one

**The technique: a Backrooms lattice under the board — runs on a fixed pitch, links between
neighbours with one in three left out, and a modular rule that is *even under `rot_180`* so the two
teams walk the same maze rather than two different ones.**

This forks `20-undercroft`. The rock, the lift and the flight down are unchanged; the hall is gone and
the lattice is the undercroft.

## The lattice

```python
PITCH, WIDE = 8, 3
runs_x = [-38 + PITCH * k for k in range(10)]
runs_z = [16 + PITCH * m for m in range(8)]

rects = [(x, 16, x + WIDE, 74) for x in runs_x if x + WIDE <= 38]     # every run, whole
for m, z in enumerate(runs_z):
    for k, x in enumerate(runs_x):
        nxt = x + PITCH
        if nxt + WIDE > 38 or (2 * k + 1 + 2 * m) % 3 == 0: continue  # one link in three, missing
        rects.append((x + WIDE, z, nxt, z + WIDE))
```

Ten runs the length of the board, seven rows of links between neighbouring runs, and **one link in
three left out**. The omission is the whole of it: a full lattice is a grid, and what makes a maze is
loops that return and legs that end at rock. Nothing here is random — the same numbers give the same
maze, which is what a board a match is played on has to be.

## The rule has to be even under negation — on the board that needs it

**Not this one, and the difference is worth knowing.** Here the whole `under` layer is authored on one
half of the board and the island fans it, so the two storeys are the same lattice by construction
whatever rule drops the links. `rot_180` does the work.

That stops being true the moment the storey covers **both** halves at once — which is any board
without a strait down the middle. A shape spanning the whole board has its own image lying over it, so
every column would carry two spans (`SK9`), and the answer is an island stated `mirrors: false`,
stamped once. Nothing fans it then: the lattice has to *be* its own image, and that is a property of
the rule that drops the links.

`(k + m) % 3` does not have it. A link is indexed by the run on its **low** side, so under negation it
is indexed by the run on its other side — the index shifts by one and the rule shifts with it, and the
two halves come out different mazes.

`(2k + 1 + 2m) % 3` does. `2k + 1` is the link's own **midpoint** between runs `k` and `k+1`, doubled
to keep it a whole number, and `2m` is its row's. A rule stated on the midpoint is a rule about the
link rather than about one of its ends, and a midpoint negates cleanly where an end does not — so the
image of a dropped link is a dropped link.

`maps/opus5-liminal-dtm-ii` is the board that needs it: its rock covers all 39,680 columns, its island
is `mirrors: false`, and its Backrooms are the same maze from either spawn because of that one
expression.

## It is stated over the land there is

The base board is not a rectangle. It has a strait between its two islands and a void hole in each,
and the rock is stated over neither (`20-undercroft`). The maze is clipped the same way — `minus()` in
the generator returns what is left of a rectangle once a hole is taken out of it, **as rectangles**,
because a subtract would be a claim that the column is empty on every layer.

That clipping is why the lattice here wraps its void rather than crossing it, and it is the honest
shape of a maze on this board. On a board with no void it runs edge to edge.

`minus()` also clips the runs round the **stairwell**, so the maze does not state a second span in the
columns the flight comes down. Over the board's **8,250 columns, none is bare and none carries two
spans** — the same check every stacked board here runs.

## Headroom

Every corridor has the same headroom by construction: the floor is `floor 0` for seven courses and the
rock's underside is at y14, so it is six courses everywhere, without a single number saying so. On a
board that also wants a *ceiling* of its own — smooth sandstone rather than the rock's stone — a
second thin layer between the two is what gives it, and that is what
`maps/opus5-liminal-dtm-ii` does with its `lid` layer: two courses at y16–17, over the maze and
nowhere else, which is also what makes the maze legible in `?layer=lid`.

## What to look at

| | |
|---|---|
| `renders/under-heightmap.png` | the lattice alone — corridors low, rock high |
| `GET …/render/heightmap?layer=under` | the same read, live |

```bash
python3 tools/drive.py showcase/23-maze "Maze" --out showcase/23-maze/world
```
