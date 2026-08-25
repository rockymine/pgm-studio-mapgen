# Rimegarth — a composed board, and the ring the composer drew once in forty-eight

> A regular capture-the-wool map. The plan under it was **not drawn**: it is
> `GET /api/compose?players=10&symmetry=rot_180&seed=26` pinned verbatim, kept beside this map as
> `specs/opus5-rimegarth/composed.plan.json`. Everything else — the height each piece stands at, the
> five themes, the two approach walls, the pond and what is planted — is authored on top of it.

**In one sentence:** a snowbound steading at each end of a hundred-block board, hall and solar on the
hub with the gatehouse on its flank, an open green facing a twenty-block gill, and behind it all a
**walled garth** — a ring of yard forty-five blocks long, climbing a course at a time from the green
to the byre, with a frozen pond in the middle of it and a bedrock wall barring each of the two lanes
that run past it.

**100 × 210 blocks**, `rot_180`, one landmass of **2,900 cells** from y8 to y14, plus the pond on a
slab of its own. Symmetry error **0**.

## What the composer gave, and how it was picked

Forty-eight seeds at ten players and forty-eight at sixteen, read as cards — each carries its
descriptor, its score against the seven hard terms, and a board SVG. What the scan says the composer
can build:

| | Forms seen in 48 seeds at 16 players |
|---|---|
| hub | `bar` ×14 · `ring` ×16 · `single` ×9 · `twin` ×5 · `g` ×2 · `double-hole` ×1 · `p` ×1 |
| frontline | `bar` ×28 · `single` ×10 · `none` ×6 · `twin` ×4 |
| wool | `i` · `l` · **`donut`** ×5 of 48 |

**The donut is why seed 26 was picked.** A composed wool box is usually a bar or an L; once in nine
it comes out as five pieces enclosing a hole, with the wool room closing the far corner. Read as a
place, that is a walled garth — a yard you can only go *round*, the wool in the byre at the far side
of it, and the middle of it open. Seed 26 pairs it with a `twin` hub, which is a hall with a solar
stepped off one end, and scores **0** — clean on every hard term.

Cell 5 is effectively the only scale the composer works at: at cell 4 it produced nothing in ninety-six
seeds and at cell 3 nothing in twelve, both exhausted. Ten players and twelve give the same boards.

## What a composed plan does not carry, and what was added

| The composer leaves | Added here |
|---|---|
| every piece flat at the global surface | a `surface` per piece — a seven-step stair, 9 to 15, rising exactly one at every seam |
| each ring arm one long piece | both arms cut in two at the middle of the hole, 12 pieces to 14 |
| `walls` always empty | **two** approach walls, one across each lane, at the cuts |
| no themes | five — `heath`, `yard`, `garth`, `green`, `pool`, bound by height |
| a hole where the donut's middle is | a pond, five courses down, on a slab of its own |
| nothing standing on it | two houses and a computed scatter |

**The pond took a layer, and how the plan compiles is why.** Left flat — every piece at one global
surface, which is how the composer hands it over — a composed plan does **not** compile to one shape
per piece. It compiles to **one merged polygon and a `subtract`**, and the subtract is what cuts the
garth's hole out of the merged whole. A subtract beats every add on its layer whatever order they are
written in, so an `addShapes` rectangle over the hole drew *nothing at all*: the first build had a
pool shape, a pool theme and a pool relief mark, all three accepted with no finding, and
`…/column?at=-8,82` answered *void*.

Giving each piece its own `surface` changes that. There is nothing left to merge, so the ground layer
now compiles to **nine polygons and no subtract at all** — one per height, `s0` at 9 through `s8` at
15 — which is also what lets `themeByHeight` bind, since a theme is stated on a shape and there are
now shapes to state it on. The hole is simply a place no polygon covers.

The pond stays on the slab it was moved to, `below: true`, filling exactly the hole's rectangle:

```
y 7  Water   y 6  Water   y 5  Cobblestone   y 4..1  Stone   y 0  Bedrock
```

— frozen at the edges, five courses under a yard at y12, which is a drop into water rather than a fall.

## The two walls, and the lanes they close

The donut's hole has a lane down each side of it and the wool byre beyond both, so **one wall closes
nothing** — a barrier on the ring's near gate is walked round by anyone who takes the other lane. The
composer does not draw a seam to hang a second one on, so the arms were cut: `wool-a-t1` and
`wool-a-t5` each split in two at cell z16, block **z80**, level with the middle of the hole. Twelve
pieces become fourteen and two new interfaces appear, one per lane, facing each other across the yard.

`walls` is then

```json
[{"a": "wool-a-t1a", "b": "wool-a-t1b"}, {"a": "wool-a-t5a", "b": "wool-a-t5b"}]
```

and each entry stamps bedrock two thick and three tall across the **full** width of its lane, on the
attack side. Read back off the built world at z80:

```
x  -27 -26 -25 …………………… -16 -15 -14 -13        x   -2  -1   0 ……………………  9  10  11  12
      .   .   # (ten) #    _   _   _                 _   _   # (ten) #   .   .   .
                          └ pond ┘                └ pond ┘
```

— ten columns of bedrock in the west lane (x −25..−16) and ten in the east (x 0..9), each spanning
its lane edge to edge, the pond between them. Neither is the wool room's own interface, which is
`PL13`; both are approaches out, which is what the device is for.

## The stair

Every piece states its own `surface`, and no relief is stated at all — a relief solves a height for
every cell and replaces the per-piece values, which is the whole reason there is none here. The
values were chosen so that **every seam on the board is a step of exactly one**:

| | green | hub | gatehouse · neck · ring gate | south arm · west lane low | west lane high · east lane low | north arm · east lane high | byre |
|---|---|---|---|---|---|---|---|
| `surface` | 9 | 10 | 11 | 12 | 13 | 14 | 15 |

Read off the built world along the west arm: y11 at z65, z72 and z78, y12 from z82 north. Along the
east arm: y12 south of the cut, y13 north of it. The step falls at z80 — **on the wall**, so the
barrier is also the lip, and getting over one is getting up the other.

Climbing the garth is therefore a climb, not a walk on the flat: the wool sits six courses above the
green the attacker starts from, and each course is paid for at a seam.

## Winter, and the one colour on it

Snow lying on frozen ground, the hill's own stone under it, spruce for what was cut. The board is all
edges — every piece falls into void — so the **wall** bucket is where the material goes: one section
of snow, coarse dirt, podzol, stone, andesite, a stone-cobble-gravel noise and granite, shared by
every theme, so the whole board is cut out of one hill.

**The green's rim is `teamTint`.** It is the only colour on the map, and it is on the one edge that
matters: the lip a team defends, seen from the other side of the gill. The wool byre's top wall course
and the gatehouse's carry the same material, so the two things worth attacking say whose they are.

## What it costs

`GET …/preflight`: **export gate OPEN**. Round-trip, mirror, buildability and traversability clean.
The dressing pass takes 20 prop documents and **declines none**.

`GET …/coverage`: **3.1 % dead** — 196 of 6,350 cells, nearly all of it the pond's own bank.

## Where it departs, and why

**There is almost nothing standing on it, and that is what a composed board is.** Every piece here is
ten blocks wide with a road down the middle of it; once the two doorways' approaches, the two wall
seams, the buildings and the roads' own standoffs are taken out, a search over every block of the
authored half found **nine** places a tree or a boulder may stand. They are the nine. A composed CTW plan is corridors
and rooms — the scenery it has room for is paint, which is why the drifts and the tread are strokes.

**The pond is not in the composer's board.** It is the one place this map changes the geometry rather
than dressing it: the hard-term gate rejects a wool ringed by a hole, so the hole is allowed to be
there, and what is in it is the author's.

**A hundred blocks of the ring's far corner are on the way to nothing.** `renders/01-flow.txt` names
them — 75 in `wool-a-t1b` and 25 in `wool-a-t3`, the outside of the last bend. Both routes into the
byre cut the corner, which is what a corner is; the ground is there to be fought over rather than
walked, and it is 5 % of a board whose whole shape is a loop.
