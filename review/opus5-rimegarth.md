# Rimegarth — a composed board, and the ring the composer drew once in forty-eight

> A regular capture-the-wool map. The plan under it was **not drawn**: it is
> `GET /api/compose?players=10&symmetry=rot_180&seed=26` pinned verbatim, kept beside this map as
> `specs/opus5-rimegarth/composed.plan.json`. Everything else — the ground it stands on, the four
> themes, the approach wall, the pond and what is planted — is authored on top of it.

**In one sentence:** a snowbound steading at each end of a hundred-block board, hall and solar on the
hub with the gatehouse on its flank, an open green facing a twenty-block gill, and behind it all a
**walled garth** — a ring of yard forty-five blocks long with a pond in the middle of it and the wool
byre closing its far corner.

**100 × 210 blocks**, `rot_180`, one landmass of **2,900 cells** from y9 to y14, plus the pond on a
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
| every piece flat at the global surface | a relief: the garth level, the green two courses under the hall, five low swells and a dip |
| `walls` always empty | one approach wall, across the garth's near gate |
| no themes | four — `heath`, `yard`, `green`, `pool` |
| a hole where the donut's middle is | a pond, five courses down, on a slab of its own |
| nothing standing on it | two houses and a computed scatter |

**The pond took a layer, and that is the finding.** A composed plan does not compile to one shape per
piece: it compiles to **one merged polygon and a `subtract`**, and the subtract is what cuts the
garth's hole out of the merged whole. A subtract beats every add on its layer whatever order they are
written in, so an `addShapes` rectangle over the hole draws *nothing at all* — the first build had a
pool shape, a pool theme and a pool relief mark, and `…/column?at=-8,82` answered *void*. Stated as a
slab of its own with `below: true`, filling exactly the rectangle the subtract took, it builds:

```
y 7  Water   y 6  Water   y 5  Cobblestone   y 4..1  Stone   y 0  Bedrock
```

— five courses under a yard at y12, which is a drop into water rather than a fall.

## The wall, and the way round

`walls` is `[{"a": "wool-a-t4", "b": "wool-a-t2"}]` — a bedrock barrier two thick and three tall
across the garth's **near gate**, stamped on the attack side. Not the wool room's own interface,
which is `PL13`; an approach out, which is what the device is for. It closes the short way into the
ring, so the wool is reached the long way round the yard, past the pond, with the defence looking
down the corridor at you.

| | Built |
|---|---|
| the attacker's walk to the wool | **177** |
| the defender's | **87** |
| the gill between the two greens | **20** blocks, inside `CT12`'s 15–40 |

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
The dressing pass takes 18 prop documents and **declines none**.

`GET …/coverage`: **3.0 % dead** — 196 of 6,550 cells, nearly all of it the pond's own bank.

## Where it departs, and why

**There is almost nothing standing on it, and that is what a composed board is.** Every piece here is
ten blocks wide with a road down the middle of it; once the two doorways' approaches, the buildings
and the roads' own standoffs are taken out, a search over every block of the authored half found
**seven** places a tree or a boulder may stand. They are the seven. A composed CTW plan is corridors
and rooms — the scenery it has room for is paint, which is why the drifts and the tread are strokes.

**The pond is not in the composer's board.** It is the one place this map changes the geometry rather
than dressing it: the hard-term gate rejects a wool ringed by a hole, so the hole is allowed to be
there, and what is in it is the author's.
