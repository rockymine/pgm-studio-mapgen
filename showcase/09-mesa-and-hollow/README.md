# 09 — a mesa, a hollow, and stacked rings

**The technique: the `area` mark. It is the only mark that makes a genuinely flat surface of a stated shape —
a bench, a mesa top, a sunken floor — and the only one whose ordering is a design instrument.**

## An area is a ring and a height

```json
{ "id": "mesa",   "kind": "area", "h": 18, "ring": [[-38,-11],[-28,-14],[-26,-1],[-31,9],[-38,7]] }
{ "id": "hollow", "kind": "area", "h":  4, "ring": [[26,-11],[38,-13],[40,1],[34,11],[26,7],[24,-3]] }
```

Every cell inside the ring is pinned to `h`. That is the whole mark, and it is what separates it from the
other four: a `point` makes a disc, a `line` makes a band, a `rim` follows the footprint's own outline, a
`scarp` states a fall. Only an `area` lets an author draw *this shape, at this height, flat*.

Measured: the mesa tops at **y17** and the hollow floors at **y3**, over a base of 9.

**A hollow is an area below the base**, and nothing about the mark changes — `h: 4` where `base: 9` is a
corrie, a quarry floor or a pond basin depending on what goes in it. Watch the bedrock: this board's bedrock
is one course at y0, so a floor at y3 leaves two courses of fill under it. An area written below that would
cut into the bedrock itself.

## Stacked rings, and why order is the whole idea

```json
{ "id": "terrace-outer", "kind": "area", "h": 12, "ring": [[-34,15],[-6,15],[-6,27],[-34,27]] }
{ "id": "terrace-inner", "kind": "area", "h": 10, "ring": [[-28,18],[-12,18],[-12,24],[-28,24]] }
```

**Marks resolve in order and the last one wins a contested cell.** The inner ring sits entirely inside the
outer one and is written after it, so it takes those cells back and the pair reads as a terrace dished in
the middle — an outer step at 12 and a floor at 10.

That is the stacked-hollow idiom, and it is the same mechanism that silently ruins a board: a knoll written
after a bench replaces the bench across their overlap, and what is left is a face nobody authored. On this
board the ordering is deliberate everywhere:

1. `coast` — the rim, first, so nothing later cuts a doorway through the shore
2. `strand` — the frontline bank, level for bridging
3. `mesa`, `hollow` — the two flanks, which do not overlap anything
4. `terrace-outer`, then `terrace-inner` — the pair whose order *is* the terrace

## The trap: a push over a hollow fills the hollow in

A push is not a second kind of mark. **The marks are solved first and the pushes are added to the answer**,
so a push laid across a hollow lifts its floor by the push's own amount.

Measured on this board, with only the push's ring moved from beside the hollow to over it:

| | ring beside the hollow | the same ring over it |
|---|---|---|
| hollow floor at `(32, 46)` | **y3** | **y9** |
| `relief/read` `low` | **4** | **8** |
| `relief` | 14 | 10 |
| complaints | none | **none** |

The hollow was gone and every gate was silent. The relief read-back is the only thing that noticed, and only
if you were looking at `low`.

So the shipped push sits *beside* the hollow, on the ground behind it:

```json
{ "id": "shoulder", "ring": [[6,13],[20,11],[24,23],[14,29],[4,25]],
  "amount": 4, "falloff": 10, "roughness": 0.4, "crown": 2, "seed": 9 }
```

**Where a push and an area genuinely have to share ground, the area has to be the one that wins — and it
cannot be.** A push applies after every constraint, so the only fix is not to overlap them. The exception is
a room floor, which is `Rigid` and which the lift steps over.

## What to look at

| Picture | Says |
|---|---|
| `GET …/render/section?axis=x&at=46&from=-45&to=45&scale=7` | the mesa and the hollow in one cut |
| `renders/world-heightmap.png` | the terrace's two rings, which a section along one axis misses |
| `POST …/sketch/relief/read` | `low` and `high` — the two numbers that catch a mark that did not land |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, no lint |
| `POST …/sketch/relief/read` | cells 10 000 · **low 4** · **high 18** · relief 14 · symmetry error 0 |
| mesa | y17 flat, five-sided |
| hollow | y3 floor, six-sided, six blocks under the base |
| terrace | outer y11 · inner y9 |
| `GET …/preflight` | export gate **OPEN** |
