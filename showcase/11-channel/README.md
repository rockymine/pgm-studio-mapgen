# 11 — a hole is not a relief

**The technique: cutting a channel with a `subtract` shape rather than any relief mark, and the second
document a subtract needs to be a real crossing — a build zone that grants the void it opens.**

The plan is `02-theme`'s, plus one zone. The finish gains one `addShapes` entry: a rectangle, `operation:
"subtract"`, cut right across the waist of the board between the two cairns.

## The document

```json
"addShapes": [
  { "id": "gullet-cut", "type": "rectangle", "operation": "subtract",
    "floor": 0, "base_height": 40,
    "min_x": -30, "min_z": -5, "max_x": 30, "max_z": 5 }
]
```

```json
"zones": [
  { "id": "gullet-bridge", "rect": [-6, -1, 12, 2] }
]
```

Two documents, two different things. The **shape** is drawn in blocks and says where the ground is not. The
**zone** is drawn in cells, in the plan, and says where a player may put it back. Cutting a channel is one
line; making it a crossing rather than a wall is the other.

## A subtract does not know how deep it is

`capabilities.md` states it and the rasterizer enforces it: **relief moves a surface, a subtract removes
it.** `SketchRasterizer.RasterGroup` resolves a shape group as `((adds − subtracts) ∪ override-adds) −
override-subtracts`, and the subtract side of that only ever contributes a **set of columns to delete** — the
shape's `floor` and `base_height` never enter the calculation. The shape above states `base_height: 40`,
eleven times the fill it stands over, because the number cannot matter and stating an absurd one is the
proof.

It was checked both ways. `base_height: 999` on the same rectangle answered `SK5` — *"reaches y=999, and the
world is 256 blocks tall — the column is cut to fit"* — a complaint about the shape's own bounds, not about
what it carves. `base_height: 1` on the identical footprint, posted as a second document, carved the same
hole:

```
GET …/column?at=0,0     (999)   0 solid block(s) — void, no block recorded at any height
GET …/column?at=0,0     (1)     0 solid block(s) — void, no block recorded at any height
```

Same depth, two orders of magnitude apart in the field that is supposed to state it.

## What `override` would have changed, and why this shape does not need it

`gullet-cut` is an ordinary subtract, and it is the only shape on the board — `02-theme` is a plain square
with nothing taken out of it. The three-step order — ordinary algebra first, then an override-add
overwriting whatever column it lands on, then an override-subtract removing theirs last — only starts to
matter the moment two shapes contest the same column, and nothing here does. `12-underpass` forks this board
to put a deck back over part of the cut, and that is the shape that needs the word: an ordinary add over a
subtracted cell loses to the subtract regardless of authoring order, so the deck must be an **override-add**
at a `floor` above the subtract's — an override add resting on the subtract's own floor refills the channel
instead of bridging it, which `SK13` refuses. Stated here because the rule the fork leans on is exactly the one
`gullet-cut` did not have to touch.

## Crossable is not a property of the hole — it is a grant

Cutting the channel and stopping there leaves the shoulders at `x ±30..50` untouched but grants nothing, and
the export gate still answers **OPEN** — because a player can already walk round the cut, on ground the shape
never touched. Nothing says the cut itself is uncrossable, so nothing looks. Reading the coverage grid for
the column at `(0, 0)`, in the middle of the cut, answers `0` — the **void** class — with the zone and
without it, which reads as "the zone did nothing." It is not:
`docs/world-scan/ground-coverage.md` states the grid draws a bridgeable void as void regardless, because
*"the route is painted only over cells the read already classed as ground."* The grid was never going to
answer this question; `walk` and `preflight` are.

A controlled pair, built off the map and not part of this one, settles it. Same channel, full width this
time (`x −50..50`, no shoulder), with and without a matching zone:

| | no zone | zone over the cut |
|---|---|---|
| `GET …/preflight` | **BLOCKED** — `traversability: not connected — isolated: blue-team · The Cairn. Add a bridge in Build` | **OPEN** |
| `GET …/walk?from=0,-20&to=0,20` | `reachable: false` | `reachable: true, distance 40, blocks 36` |

**A build zone is a rect in the plan, in cells — `docs/tools/plan.md`'s "a zone is a rect over the void
saying where players may bridge" — and it is the only thing that turns a subtract's hole into a crossing.**
`gullet-bridge` is that rect for this board, sized to the cut exactly: `[-6, -1, 12, 2]` cells is `x
−30..30, z −5..5` in blocks, the same rectangle `gullet-cut` carves. Without it the void is real and
permanent — correct for a chasm at the map's edge, wrong for a gap an attacker is meant to fight across.

## Bridge, or go round

The shoulders were left uncut on purpose: `x ±30..50` carries no subtract, so it is ordinary ground on both
sides of the throat. An attacker crossing the board has two ways — pay thirty-six blocks to bridge the ten-block
gap on a direct line, or take a shoulder round it for nothing:

```
GET …/walk?from=0,-20&to=0,20&aim=travel     reachable, distance 40, blocks 36   (straight through the cut)
GET …/walk?from=40,-20&to=40,20&aim=travel   reachable, distance 40, blocks 0    (the east shoulder)
```

Same distance, thirty-six blocks apart in cost — which is the honest read: the cut adds a choice, not a
requirement, until a defender denies the shoulders. Note what the block count is actually counting: the walk
prices a bridge one block wide with a lip either side, so a ten-block gap is not a ten-block bill.

## The lip is already themed — the rim did it

Nothing was added to `meadow` for this. The theme's `rim` is `rimEdges: "void"` — cap every edge that faces
void — and a subtract's new edge faces void exactly as much as the original coast does. Reading the columns
either side of the cut, and the shoulder's own edge, finds the same cobblestone course the coast wears:

```
GET …/column?at=-30,-6   y8 Cobblestone   (south lip)
GET …/column?at=-30,5    y8 Cobblestone   (north lip)
GET …/column?at=30,0     y8 Cobblestone   (shoulder edge, facing the cut)
GET …/column?at=-30,0    void              (inside the cut)
GET …/column?at=32,0     y8 Grass Block   (two blocks back, off the lip)
```

A cut reads as a cut because the rim policy that caps the coast caps every void it is handed, and cutting one
is all authoring the lip took.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-topdown.png` | the square with a slot right across its waist, and a shoulder either end of it |
| `GET …/render/section?axis=x&at=0&from=-50&to=50&scale=6` | the whole width of the cut in one cut: void from `x −30` to `30`, ground from `32` on |
| `GET …/render/section?axis=z&at=-30&from=-30&to=30&scale=10` | the same gap along the direction of travel, lip on both banks |
| `renders/coverage.png` | the two journeys running straight through the cut; the cut itself is unmarked, being void |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` |
| `GET …/column?at=0,0` | void at `base_height` 999 **and** at `base_height` 1 — identical |
| `GET …/preflight` (no zone, full-width cut) | **BLOCKED** — `EX1`-style refusal, "Add a bridge in Build" |
| `GET …/preflight` (zoned, full-width cut) | **OPEN** |
| `GET …/preflight` (this board — shouldered, zoned) | **OPEN** |
| `GET …/walk?from=0,-20&to=0,20` (full-width cut) | unreachable with no zone; `reachable, distance 40, blocks 36` with one |
| `GET …/walk?from=40,-20&to=40,20` | reachable, distance 40, **blocks 0** — the shoulder, for nothing |
| `GET …/coverage` | reached 2 181 · dead 7 219 of 9 400 · **76.8% dead** |
| lip theme | Cobblestone rim on both banks and the shoulder edge, from the unmodified `meadow` theme |
