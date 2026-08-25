# Opus 5 — Rimegarth: browsing the composer, and the subtract under a generated board

## What I set out to build

A regular capture-the-wool map — the kind the studio's own generator makes — and the brief was to
**look at composer output and pick a brand-new design** rather than draw one. So the board's plan is
not mine: `specs/opus5-rimegarth/composed.plan.json` is `GET /api/compose?players=10&seed=26` pinned
verbatim, and everything else is authored on top of it.

`maps/opus5-rimegarth`, 100 × 210, one landmass of 2,900 cells plus a pond on its own slab, zero
declines, export gate open, `review/opus5-rimegarth.md`.

## Browsing is a real agent workflow, and this is what it costs

`GET /compose?players=&symmetry=&seedStart=&count=` returns cards: each carries the descriptor that
reproduces it, its score against the seven hard terms, a structural read, and a board SVG. `POST
/compose/pin` stores one from the descriptor and `GET /plans/{id}/png` renders it as an image an
image reader can open. Ninety-six seeds scanned, eleven pinned, two contact sheets, one pick — about
four minutes of API time.

What ninety-six seeds say the composer's vocabulary is:

| | at 16 players, 48 seeds |
|---|---|
| hub | `bar` 14 · `ring` 16 · `single` 9 · `twin` 5 · `g` 2 · `double-hole` 1 · `p` 1 |
| frontline | `bar` 28 · `single` 10 · `none` 6 · `twin` 4 |
| wool | `i` · `l` · **`donut`** 5 |

Two things a scan tells you that no document does. **Cell 5 is the only scale it works at**: at cell
4 it produced nothing in ninety-six seeds and at cell 3 nothing in twelve, both `exhausted`. And **10
and 12 players give byte-identical boards**, so the land budget buckets rather than scaling.

The pick was the `donut` wool at ten players, seed 26 — five pieces enclosing a hole with the wool
room closing the far corner, paired with a `twin` hub, scoring 0. Read as a place it is a walled
garth, and that is the map.

## The finding this run is for

**A composed plan does not compile to one shape per piece. It compiles to one merged polygon and a
`subtract`, and the subtract beats every add on its layer.**

Twelve pieces went in and eleven shapes came out: `s0`, one merged `add` polygon over the whole
footprint; `s1`, a `subtract` polygon cutting everything the pieces do not cover — including the
donut's hole; four structural room annotations; and my five added rectangles.

So the obvious way to fill the hole does not work, and it fails *silently*. The first build stated a
`pool` rectangle over the hole, a `pool` theme for it and a `pool` relief mark holding it flat, all
three accepted with no finding, and `…/column?at=-8,82` answered **void**: `s1` had removed those
cells from the layer's set algebra before anything else was asked. The relief read even reported the
right total, because the cells were never in the footprint to be missing from it.

What works is a **slab of its own**: an `addLayers` entry with `below: true`, one rectangle filling
exactly what the subtract took. No overlap with the compiled ground, so no `SK10`; the painter reaches
it first; and a prop with no `layer` seats on `SurfaceTop`, which over the hole is the pond. It builds
water at y6–7 over a bed at y5, five courses under a yard at y12.

**Fill a composed hole on its own layer. An `addShapes` rectangle over one draws nothing and says
nothing.**

## What I could not say

**How much room a composed board has for scenery — until I measured it.** Every piece on this plan is
ten blocks wide with a road down the middle. Placing props by eye gave **fourteen declines** on the
first pass and eleven on the second, half of them `DR-SITE — has no ground`, because a composed board
*is* its pieces and there is no landscape around them.

The fix was to make the spec compute it. Given the piece rectangles, the roads with their radii, the
buildings and the two doorways, a search over every block of the authored half returns the places a
prop may stand: **seven**. That is the honest number for a hundred-block CTW board, and the answer to
"why is it so bare" is that a composed plan is corridors and rooms.

Two rules came out of getting there. **A road's standoff is measured to its paved cells, not its
centreline**, so what a prop must clear is the stroke's radius plus its kind's standoff — three for a
tree, two for a boulder. And **an approach wall's interface is kept clear the way a doorway is**, so
the seam a `walls` entry names has to go in the keep-out list beside the rooms.

## What I got wrong

**I assumed water spreads to fill a level pan.** It did on `deepcut`, where an oversized flat `area`
mark became an oversized square lake — and on that board the lesson was *make the pan the size of the
pool*. Here the pond is a flat slab and a `canal` water prop filled only its own stated band, leaving
a channel down the middle of a hole fifteen blocks wide. The band **is** the pond; the radius is the
knob. Both boards are consistent once you stop thinking of a water prop as a fluid and start thinking
of it as a stroke that carves.

**I put three byres inside the ring.** A corridor ten blocks wide with a route down it has no room
for a seven-wide house, and the dressing pass said so twice over — `DR-CLAIM` against the channel and
`DR-KEEP` against the wool room's door. The garth gets its pond, its paving and its drifts; the
buildings are on the hub.

## What worked first time

- **The board itself.** A composed plan compiles, evaluates and exports without a hand on it; every
  refusal in this run was about something I added.
- **The approach wall.** One line — `{"a": "wool-a-t4", "b": "wool-a-t2"}` — and the near gate into
  the garth is barred with bedrock two thick and three tall, so the wool is reached the long way
  round the yard. `walls` is the one thing a composed board never carries and the cheapest thing to
  add to it.
- **`teamTint` on the green's rim.** The only colour on a white board, on the one edge that matters:
  the lip a team defends, seen from across the gill.

## Open gameplay questions

**Is 177 to 87 the right ratio for a ring?** The wall makes the attacker go the long way round the
garth, which is most of the difference. A ring wool room is a defender's shape by construction — you
can be met at either end of the corridor — and whether that wants the wall as well is a question
about how the map plays rather than how it builds.

**Should the garth's pond be reachable back out of?** It is five courses down with a yard wall all
round; you climb out at the bank the water prop left, or you place a block. On a capture board that
is a real cost for a carrier who gets knocked in, and it may be one too many.
