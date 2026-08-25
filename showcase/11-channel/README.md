# 11 — a hole is not a relief

**The technique: cutting a channel with a `subtract` shape rather than any relief mark, and the second
document a subtract needs to be a real crossing — a build zone that grants the void it opens.**

The plan is `02-theme`'s, plus one zone. The finish gains one `addShapes` entry: a rectangle, `operation:
"subtract"`, laid across the throat between the spawn approach and the wool room.

## The document

```json
"addShapes": [
  { "id": "gullet-cut", "type": "rectangle", "operation": "subtract",
    "floor": 0, "base_height": 40,
    "min_x": -40, "min_z": 60, "max_x": 20, "max_z": 70 }
]
```

```json
"zones": [
  { "id": "mid", "rect": [-8, -4, 16, 8] },
  { "id": "gullet-bridge", "rect": [-8, 12, 12, 2] }
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
GET …/column?at=0,65     (999)   0 solid block(s) — void, no block recorded at any height
GET …/column?at=0,65     (1)     0 solid block(s) — void, no block recorded at any height
```

Same depth, two orders of magnitude apart in the field that is supposed to state it.

## What `override` would have changed, and why this shape does not need it

`gullet-cut` is an ordinary subtract, the same operation `02-theme`'s own `s1` hole already carries — the
notch nothing put a piece over. The three-step order — ordinary algebra first, then an override-add
overwriting whatever column it lands on, then an override-subtract removing theirs last — only starts to
matter the moment two shapes contest the same column, and nothing here does. `12-underpass` forks this board
to put a deck back over part of the cut, and that is the shape that needs the word: an ordinary add over a
subtracted cell loses to the subtract regardless of authoring order, so the deck must be an **override-add**
or the channel wins and there is no deck. Stated here because the rule the fork leans on is exactly the one
`gullet-cut` did not have to touch.

## Crossable is not a property of the hole — it is a grant

The first build cut the channel and stopped there, leaving the shoulder at `x 20..40` untouched (below) but
granting nothing. It compiled, evaluated at 0, and the export gate answered **OPEN** — because a player could
already walk around the cut, on the ground the shape never touched. Nothing said the cut itself was
uncrossable, so nothing looked. Reading the coverage grid for the column at `(0, 65)` (in the middle of the
cut) answered `0` — the **void** class — before *and after* granting the zone, which briefly read as "the
zone did nothing." It is not: `docs/world-scan/ground-coverage.md` states the grid draws a bridgeable void as
void regardless, because *"the route is painted only over cells the read already classed as ground."* The
grid was never going to answer this question; `walk` and `preflight` are.

A controlled pair, built off the map and not part of this one, settles it. Same channel, full width this
time (`x −40..40`, no shoulder), with and without a matching zone:

| | no zone | zone over the cut |
|---|---|---|
| `GET …/preflight` | **BLOCKED** — `traversability: not connected — isolated: blue-team · blue. Add a bridge in Build` | **OPEN** |
| `GET …/walk?from=30,55&to=30,80` | `reachable: false` | `reachable: true, distance 25, blocks 10` |

**A build zone is a rect in the plan, in cells — `docs/tools/plan.md`'s "a zone is a rect over the void
saying where players may bridge" — and it is the only thing that turns a subtract's hole into a crossing.**
`gullet-bridge` is that rect for this board, sized to the cut exactly: `[-8, 12, 12, 2]` cells is `x
−40..20, z 60..70` in blocks, the same rectangle `gullet-cut` carves. Without it the void is real and
permanent — correct for a chasm at the map's edge, wrong for a gap an attacker is meant to fight across.

## Bridge, or go round

The shoulder was left uncut on purpose: `x 20..40` at `z 60..70` carries no subtract, so it is ordinary
ground on both sides of the throat. An attacker has two ways up from the shelf to the wool room — pay ten
blocks and a few seconds to bridge the fourteen-cell gap on a direct line, or take the eighteen-block
shoulder round it for nothing. Ten blocks placed under fire is not a small ask on a capture board; the
shoulder is what keeps the cut from simply walling off the objective for anyone without a kit to spend.

```
GET …/walk?from=-30,25&to=-30,72&aim=travel     reachable, distance 47, blocks 10   (straight through the cut)
GET …/walk?from=-20,80&to=-30,-105&aim=travel   reachable, distance 245, blocks 55  (the shoulder, both islands)
```

The second number is the whole cross-board walk `travel` actually prefers — free ground beats ten placed
blocks whichever aim is asked — which is the honest read: the cut adds a choice, not a requirement, until a
defender denies the shoulder.

## The lip is already themed — the rim did it

Nothing was added to `meadow` for this. The theme's `rim` is `rimEdges: "void"` — cap every edge that faces
void — and a subtract's new edge faces void exactly as much as the original coast does. Reading the columns
either side of the cut, and the shoulder's own edge, finds the same cobblestone course the coast wears:

```
GET …/column?at=-30,59   y8 Cobblestone   (south lip)
GET …/column?at=-30,70   y8 Cobblestone   (north lip)
GET …/column?at=20,65    y8 Cobblestone   (shoulder edge, facing the cut)
GET …/column?at=-30,65   void              (inside the cut)
GET …/column?at=22,65    y8 Grass Block   (two blocks back, off the lip)
```

A cut reads as a cut because the rim policy that caps the coast caps every void it is handed, and cutting one
is all authoring the lip took.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-ground.png` | the U-shaped island with two holes now — `02-theme`'s original notch, and the new horizontal cut just below the throat |
| `renders/section-channel-x65.png` | `axis=x&at=65` — the whole width of the cut in one cut: void from `x −40` to `20`, solid ground from `22` on, the shoulder in one picture |
| `renders/section-channel-z-30.png` | `axis=z&at=-30` — the same gap along the direction of travel, shelf on one side and apron on the other |
| `renders/coverage.png` | the diagonal corridor through the shoulder on both islands; the cut itself is unmarked, being void |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` |
| `GET …/column?at=0,65` | void at `base_height` 999 **and** at `base_height` 1 — identical |
| `GET …/preflight` (no zone, full-width cut) | **BLOCKED** — `EX1`-style refusal, "Add a bridge in Build" |
| `GET …/preflight` (zoned, full-width cut) | **OPEN** |
| `GET …/preflight` (this board — shouldered, zoned) | **OPEN** |
| `GET …/walk?from=30,55&to=30,80` | unreachable with no zone; `reachable, blocks 10` with one |
| `GET …/walk?from=-30,25&to=-30,72` | reachable, distance 47, blocks 10 — straight through the cut |
| `GET …/coverage` | reached 6923 · dead 127 · **1.8% dead** (34.0% before the zone was added) |
| lip theme | Cobblestone rim on both banks and the shoulder edge, from the unmodified `meadow` theme |
