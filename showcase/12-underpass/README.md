# 12 — a deck, and the floor it cannot have

**The technique: putting ground back over a cut with an `override: true` add, and the measurement that says
what an author gets and does not — a bridge with real headroom under it, never a floor to stand on there.**

This forks `11-channel`, not `02-theme`: the plan and the `gullet-cut` subtract are unchanged, wool still
answers at `(-30, -105)`, the shoulder at `x 20..40` is still open ground. The finish gains one shape — a deck
— and one theme to paint it in, because a deck is built and the ground under it is not.

## The document

```json
"addShapes": [
  { "id": "gullet-cut", "type": "rectangle", "operation": "subtract",
    "floor": 0, "base_height": 40,
    "min_x": -40, "min_z": 60, "max_x": 20, "max_z": 70 },
  { "id": "deck", "type": "rectangle", "operation": "add", "override": true,
    "floor": 13, "base_height": 4, "theme": "deck",
    "min_x": -38, "min_z": 57, "max_x": -12, "max_z": 73 }
]
```

The deck covers the west half of the cut and a little of the shelf and apron either side of it — a real
overhang, not a lid sized exactly to the hole. `x −12..20` of the channel stays open, so the board keeps
three ways across the throat: over the deck, through the remaining gap, or round the shoulder.

## Getting the order right

`gullet-cut` and `deck` occupy the same cells. `SketchRasterizer.RasterGroup` resolves a shape group as
`((adds − subtracts) ∪ override-adds) − override-subtracts` — an **ordinary** add loses to a subtract over
the same column regardless of which was authored first, because the subtract side of the algebra runs before
either shape's `override` is looked at. Dropping `override` from `deck` and rebuilding answers exactly that:

```
GET …/column?at=-25,65   (deck without "override")   0 solid block(s) — void
```

The channel wins; there is no deck. `override: true` is what moves `deck` into the second pass, where it
"overwrites the column it lands on" outright — the third fact `capabilities.md` states about the resolution
order, and the one this board is the worked example of.

## The trap: the first version filled the channel back in

The first `deck` shape stated only `base_height: 17`, on the reasoning that seventeen blocks is where its top
should be. It is not what the field means. `floor` defaults to `0` — the very bottom of the shape's column —
so an override-add with no stated floor spans from the world's floor to its own top, the same as any ordinary
ground. The column it built:

```
GET …/column?at=-25,65   (base_height 17, floor unset)
  y 16   Grass Block
  y 15   Dirt
  y 14   Dirt
  y 13   Stone           ← bedrock and eleven more courses of stone below, unbroken
  ...
  y  0   Bedrock
  17 solid block(s)
```

Seventeen solid blocks, bedrock to grass. The channel is gone — refilled as an ordinary column that happens to
stand tall, not bridged at all. **`floor` is the field that decides**, exactly as the brief warns, and it
decides by setting where the column's own span *starts*, not by any relation to the ground it replaces.

## The fix, and what it actually buys

Setting `floor: 13` alongside `base_height: 4` keeps the same top — `y16` — and starts the span eleven blocks
higher up instead of at the bottom:

```
GET …/column?at=-25,65   (base_height 4, floor 13)
  y 16   Dark Oak Planks
  y 15   Stone Bricks
  y 14   Stone Bricks
  y 13   Stone Bricks
  4 solid block(s)
```

Four blocks of deck, and **nothing recorded below `y13`** — the same "void — no block recorded at any
height" answer the open channel gives. The deck is a slab standing in open air over a real drop, which is
what an overhang is built from: a span that starts high and nothing under it.

## What that costs: there is no floor to stand on underneath

A column is one span. Building the slab higher did not add a second, lower span for a passage floor — it
moved the *only* span this cell has. Asking the walk for a place at `(-25, 65)` and naming the ground height
explicitly proves it:

```
GET …/walk?from=-25,65,8&to=-25,25    reachable, distance 41, blocks 0, drops 1 (worst 8)
```

The request asks for the place at `y8` — where the ground would be if the channel had never been cut — and
the answer snaps to the deck's own top at `y16` anyway and walks from there, dropping 8 blocks free on the far
side. There is no place at `y8` to snap to. A walk crossing the deck's own footprint north–south answers the
same way: it climbs onto the deck (`blocks 7`, the eight-block rise minus one) and crosses on top of it.

```
GET …/walk?from=-25,55&to=-25,80     reachable, distance 29, blocks 7, drops 1 (worst 8)   — climbs onto the deck, crosses it, drops off the far side
```

**"Undercroft Passage" has no undercroft a player can stand in.** Within one sketch layer a rasterized
column carries exactly one vertical span, so a floor at the old ground height and a deck above it, at the
same `(x, z)`, cannot both exist — authoring the deck is authoring away whatever the column held before, all
the way down. (One layer. The next section is the part that changes.) What reads as an underpass from the side is a bridge with a drop under it,
and what is actually walkable is the same set `11-channel` already had: the deck's own top, the open stretch
of channel beside it, and the shoulder round the whole thing. The board keeps its name for what the gap looks
like from a section, not for a route that exists.

## What a column *can* carry two of, and it is not this

The sentence above needs its scope, or it states a limitation the system does not have. **A column carries
one span per sketch layer**, not one span. `SketchRasterizer` groups every rasterized segment by cell and
then compares pairs — and the first thing it does is skip a pair that shares a layer:

```csharp
if (ordered[i].Layer == ordered[j].Layer) continue;   // SK9's ground, not this one
```

That test only means anything because two segments in one cell *can* come from two layers. A genuine
undercroft — a yard at the old ground height with a deck standing over it and a player able to walk under —
is a **second layer**, authored as `addLayers` in the finish (`tools/README.md` documents the key; the
driver moves the compiled ground into `layers` the moment a second slab exists, because the rasterizer reads
`layers` **or** `layout` and never both).

Two boards in this repository already do it. `reports/opus5-undermarket-layers.md` measures a yard with a
terrace over it and two walkways out over open void — *"`topdown-under.png`, `ymax=19`, below the deck: no
grass anywhere, the yard showing through where the terrace was"* — and `opus5-mineshaft` is the other.

So the honest statement is narrower and more useful than "there is no floor underneath": **one layer cannot
stack, and stacking is what layers are for.** This showcase stays inside one layer on purpose, because a
second layer is a different subject with its own two worked examples; what it measures is what an
`override: true` add does to the column it lands on, which is to *replace* it.

## The board still holds together

Nothing about adding the deck weakens the crossing `11-channel` built: the `gullet-bridge` zone still grants
the open half of the cut, the shoulder is untouched, and the deck adds a third, free way across for whoever
does not want to spend the seven blocks a bridge costs or the distance the shoulder does.

```
GET …/preflight                        export gate OPEN — traversability: connected, 1 component
GET …/coverage                         reached 6722 · dead 94 · 1.4% dead
```

## What to look at

| Picture | Says |
|---|---|
| `renders/world-ground.png` | the deck (dark plank/stone) crossing the meadow cut, distinct from both the ground family and `11-channel`'s bare lip |
| `renders/section-deck-x65.png` | `axis=x&at=65` — the deck as a slab hanging in open air, void above **and below** it, the untouched shoulder solid on the right |
| `renders/section-deck-z-25.png` | `axis=z&at=-25` — ground, then the floating deck, then the spawn beyond it, the gap under the deck visible the whole way along |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` |
| `deck` without `override` | column at `(-25,65)` reads **void** — the subtract still wins |
| `deck` with `floor` unset, `base_height: 17` | column reads **17 solid blocks**, bedrock to `y16` — the channel is filled, not bridged |
| `deck` with `floor: 13`, `base_height: 4` | column reads **4 solid blocks**, `y13..16`, nothing below |
| `GET …/walk?from=-25,65,8&to=-25,25` | snaps to the deck's own top (`y16`); no place answers at `y8` |
| `GET …/walk?from=-25,55&to=-25,80` | blocks 7, one drop of 8 — over the deck, not under it |
| `GET …/preflight` | export gate **OPEN**, traversability connected, 1 component |
| `GET …/coverage` | 1.4% dead (11-channel: 1.8%) |
