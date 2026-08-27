# 23 — a maze, and the rule that makes both halves the same one

**The technique: a Backrooms lattice under the board — runs on a fixed pitch, links between
neighbours with one in three left out, and a modular rule that is *even under `rot_180`* so the two
teams walk the same maze rather than two different ones.**

This forks `20-undercroft`. The rock, the lift and the flight down are unchanged; the hall is gone and
the lattice is the undercroft. **The square board is the one that needs the rule**, which is why the
maze is here and not on a board with a strait down the middle.

## The lattice

```python
PITCH, WIDE, REACH = 8, 4, 46
CENTRES = sorted(c for j in range(6) for c in (-4 - 8 * j, 4 + 8 * j))   # symmetric about 0

runs = [(c - WIDE // 2, -REACH, c + WIDE // 2, REACH) for c in CENTRES]  # every run, whole
links = [(c + WIDE // 2, r - WIDE // 2, c + PITCH - WIDE // 2, r + WIDE // 2)
         for c in CENTRES if c + PITCH in CENTRES
         for r in CENTRES if (((c + PITCH // 2) // 4) + (r // 4)) % 3 != 0]
```

Twelve runs the length of the board, twelve rows of links between neighbouring runs, **88 of 132 kept**
— one link in three left out. The omission is the whole of it: a full lattice is a grid, and what makes
a maze is loops that return and legs that end at rock. Nothing here is random — the same numbers give
the same maze, which is what a board a match is played on has to be.

**The run centres are `±4, ±12, ±20, ±28, ±36, ±44`, and their symmetry is load-bearing.** A run at `c`
images onto one at `−c`; a run at `−46 + 8k` would image onto no run at all.

## The rule has to be even under negation

A storey covering **both** halves of the board has its own image lying over it, so fanning it would
state every column twice; the island is `mirrors: false` and the lattice is stamped once. Nothing fans
it, which means the lattice has to *be* its own image — and that is a property of the expression that
drops the links, not of the geometry.

A link between the runs at `c` and `c + 8`, on the row at `r`, has its midpoint at `(c + 4, r)`. Under
`rot_180` that midpoint goes to `(−c − 4, −r)`, which is the midpoint of the link between `−c − 8` and
`−c` on row `−r` — another link, because the centres are symmetric. So writing the rule as a function
of `u = (c + 4)/4` and `v = r/4` makes it a statement about the *link* rather than about one of its
ends, and the question becomes whether that function is **even**: `f(u, v) = f(−u, −v)`.

`(u + v) % 3 == 0` is. Negating both arguments negates the sum, and a sum is zero mod three exactly
when its negation is.

**A constant term is what breaks it, and a constant term is the natural thing to add** when the maze
comes out wrong and the obvious fix is to shift which third goes missing. Measured over all 132
candidate links:

| rule | links kept | images that disagree |
|---|---|---|
| `(u + v) % 3` | 88 | **0** |
| `(u + 2v) % 3` | 88 | **0** |
| `(u + v + 1) % 3` | 88 | **88** — every one |

The offset rule keeps the same number of links and gets every single one of them on the wrong side of
the mirror: one team's maze is the exact photographic negative of the other's. It compiles, it builds,
the export gate opens, and nothing anywhere says so.

`maps/opus5-liminal-dtm-ii` is the other board that needs it: its rock covers all 39,680 columns, its
island is `mirrors: false`, and its Backrooms are the same maze from either spawn for this reason.

## The rock is banded round every corridor

The board is a plain square with no void in it, so the lattice runs edge to edge — but the *rock* still
has to be stated as adds banded round each hole, for `20-undercroft`'s reason: a subtract is a claim
about the whole stack, and a shorter add inside a taller one is not a room. One hundred corridors and
links leave **213 rock bands** between them, and that count is why the banding is generated rather than
drawn: over the board's **10,000 columns, none is bare and none carries two spans**, checked rather
than looked at.

That is the honest cost of the technique. A hall is four bands; a maze is two hundred and thirteen.
Nothing about the document is harder — it is the same rectangle repeated — but it is not a document
anyone hand-writes, and the check is what makes generating it safe.

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
| `renders/world-section-z0.png` | the corridors as a row of voids under the landmass, rock pillars between them |
| `renders/world-ground.png` | the lattice in plan — corridors dark, rock pillars light |
| `GET …/render/heightmap?layer=under` | the storey alone, live |

```bash
python3 tools/drive.py showcase/23-maze "Maze" --out showcase/23-maze/world
```
