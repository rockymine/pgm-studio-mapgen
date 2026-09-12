# Blackden Sough — over the edge, or under it

> A destroy board. A gritstone edge runs right across each team's ground; a drainage sough is driven
> under it. An attacker who bridges the gap lands on the shelf and has three ways at the Stone.

**In one sentence:** a moorland edge with one nick in it and one hole through it, so the ground itself
poses the question the match is about — the gully everybody can see, the twelve-block face somebody has
to pay blocks for, or six courses of headroom in the dark that come out on the dale floor behind the lot.

70 × 240 blocks, `rot_180` about the origin, base surface 28, ground y19..y43, build ceiling y66.
Two plan pieces at one surface, so the board is **one terrain shape** and its shape is the relief's.

## How the board is put together, bottom-up

A stacked board is written from the floor up, because the painter walks the layer stack in document
order and a storey listed after one that stands over it finds no stone left to paint.

| y | what is there | how it is stated |
|---|---|---|
| 0..17 | the sough's floor, and the rock either side of it | layer `under`, `below: true`, five adds |
| 18..23 | the passage's own air — six courses of headroom | the gap between two layers' spans |
| 24.. | the moor | the compiled ground, `floor: 24`, its top from the relief |

The rock is **adds banded round the corridor** and never a subtract: a subtract is a claim about the
whole stack, so the moor over it would fill what the storey below called void (`SK13`, measured in
`showcase/20-undercroft`). Four bands and one corridor tile the footprint exactly.

The bands are clipped out of the **moor's own drawn outline** rather than from the plan's rectangle.
That matters: the coast is drawn by moving into the compiled ring one point at a time — nine inserts,
five of them the coast itself — and a rock band left as a rectangle would have stood out past every bay
as a 24-block ledge over the void. The outline is stated once in `build-spec.py` and the storey below is
cut out of it, so the two can never disagree.

## The three ways at the Stone

| route | what it costs | measured |
|---|---|---|
| **the nick** | eighteen blocks wide, in the middle, overlooked from both shoulders of the crest | `spawn-blue -> destroyable-1-0`: one `scramble +2` at `(7, 30)` and nothing else on the climb |
| **the face** | placed blocks, anywhere along the edge | `03-slopes.txt`: 13 faces, the largest 135 cells at `x 8..33, z -35..-24` — the scarp |
| **the sough** | a six-wide chokepoint, but it arrives behind the edge | `walk?from=-21,45,18&to=-21,80` — **35 blocks, 0 placed, 0 drops, walked end to end** |

Both flights walk both ways for nothing. Into the north mouth: `(-21,16) -> (-21,45)` reads
`28 28 28 28 27 27 26 25 25 24 23 23 22 21 21 20 19 19 18` — one course a block, then level into the
passage. Out of the south mouth: `... 29 30 31 32` and flat onto the pan.

The edge is stated as **two `scarp` marks with the nick between them**, not as a steep relaxation. A
relaxation of 2 blocks a cell builds a staircase of two-block treads and reads as terracing; a scarp
states the drop outright and builds one face. The first build of this board had the terraced version and
the isometric showed it immediately.

## What the ground is made of

One theme over 99.9% of the surface. The board's variation is the **slope band axis**, not a theme per
piece: one `layered` stack on `slope` puts turf over soil under 28°, a coarse-dirt shoulder to 42°, and
bare gritstone past that. The cuts were read off `GET …/incline?format=text`, which answered 43% under
10°, 16% in the teens, 22% in the twenties and 9.6% at 40° or steeper — so the cuts land about
three-quarters turf, a sixth shoulder, a tenth rock, and the worn ground appears exactly where the ground
is actually worn.

The fill is a `cell` nine across with a rise of five — wider than tall, so a cut face reads as blobs
rather than as vertical runs. It is deliberately **not** plain stone: a ground theme filling in `1:0`
hands the whole column to whatever is drawn above it, and this board has two plain layers.

Three families, named before painting: ground is **verdant + grey stone**, built is **dirt** (spruce), the
accent is **brick** (the hall roofs). The hall is therefore not the ground it stands on.

## The three placement ideas

Nothing is scattered; each of the three answers *why here*.

| | where | why |
|---|---|---|
| the edge's broken rock | four at the foot of the face (`z 25..26`), two on the crest (`z 37..38`) | the fallen blocks are cover for whoever is trying to get up the face |
| the holt | five copied birch and dark oak, `x -28..-10, z 77..91` | in the lee of the edge, and 30+ blocks off the Stone so nothing shades it |
| the way | `(0,108) -> (12,62) -> (0,28)`, solid, gravel/andesite/cobble | door to Stone to nick: the circulation diagram, drawn. It is one line, it connects at both ends, and it crosses no building |

26 props placed, **0 declined**. The trees are copied bodies lifted out of `showcase/tree-showcase` with
`tools/trees.py bodies` — the repository author's own trees, not grown ones.

## Numbers

| read | answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, no violation |
| `GET /rules/terms` | goal ratio **3.35** (GO1 wants 3–4); own-spawn walk 54 (GO4 wants 40–90) |
| `GET …/preflight` | **export gate OPEN**, traversability connected per team |
| `GET …/coverage` | reached 9 468 · decorated 528 · dead 2 185 of 12 181 = **17.9% dead** |
| `03-slopes.txt` | 11 297 walked · 265 scrambled · 629 barrier; 13 faces |
| `06-claims.txt` | placed 26, declined 0 |
| the void scan | `x -24..-19, y 18..23, z 34..57` — 864 cells, **open**, six courses of headroom |

## What is deliberately left complained about

`RL2` — *"14 blocks of range and 0.6 scrambles for every barrier — 178 of its steps are taller than a
player can scramble."* That is the scarp, and the scarp is what the board is. 178 barrier steps out of
12 925 is 1.4% of the ground, all of it in the one face `03-slopes.txt` names. Grading it would delete
the board's only question.

## What went wrong on the way

- **The first relief was a table.** Two `area` marks 70 × 64 pinned the dale and the shelf flat, and the
  board came out as two green slabs. An area pins a flat disc and is right only where flat is the point —
  the ground a bridge lands on, the pan a sough discharges into, the shelf a goal stands on. Everything
  else is a `point` at radius 4–6 with the relaxation between them.
- **A push over a pan lowers the pan.** The `slack` push reached the sough's tail and the south flight
  came out landing two blocks proud of the ground it was supposed to arrive on — visible in the walk and
  in nothing else. Pushes are applied to the *solved* surface; marks negotiate with each other. Both
  pushes became marks and the step went away.
- **`HS3`** refused the hall: a bare log on a roof verge stands every block on end and shows a sawn face
  to whoever is looking at the slope. A `laidLog` takes the ridge's own axis.
- **A point mark must not touch a line mark's band.** `rig-w` at `(-30, 52)` overlapped the crest's band
  and `RL3` named a 10-block step along 18 cells. Moving it to `(-32, 68)` was the whole fix.

## Open, and not the author's to settle here

The edge is a twelve-block face with one eighteen-block gully and one six-wide tunnel through it. Whether
that is the right ratio of open route to chokepoint for a twelve-a-side destroy board is a question about
how a map **plays**, and this session has no oracle for it. Built as stated; recorded here rather than
filed as a fact.
