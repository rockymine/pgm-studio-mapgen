# 07 — a hill, stated and sculpted

**The technique: a relief. The two halves of its vocabulary — a mark is a *constraint*, a push is
*sculpting* — put side by side on one board so the difference is visible in one section.**

The plan is `02-theme`'s, untouched. The finish gains a `relief` block keyed on the island id, which for a
compiled board is `team`.

## The document

```json
"relief": { "team": {
  "base": 9, "reach": 20, "step": 1, "stairs": true,
  "grain": { "amplitude": 1.0, "scale": 11, "seed": 3 },
  "marks": [
    { "id": "coast",  "kind": "rim",   "h": 9, "depth": 1 },
    { "id": "brow-w", "kind": "point", "at": [-32, 6], "h": 17, "r": 4 },
    { "id": "strand", "kind": "line",  "points": [[-40,-21],[0,-21],[40,-21]], "h": [9,9,9], "width": 5 }
  ],
  "pushes": [
    { "id": "spur-e", "ring": [[27,-7],[38,-3],[40,11],[33,21],[26,17],[24,5]],
      "amount": 7, "falloff": 12, "roughness": 0.45, "crown": 3, "seed": 5 }
  ] } }
```

The west flank is a **mark** and the east flank is a **push**, and they make the same kind of landform two
different ways.

## Mark against push

A **mark** is a constraint: the ground here *is* seventeen, and the solver honours it exactly. Everything
between the marks is a relaxation — the surface of least curvature subject to them — which has the property
an author needs and a weighted fill does not: **its extremes can only sit where a mark put one**. No bump
appears that nobody asked for.

A **push** applies to the already-solved surface. It takes a drawn ring, lifts the ground inside it and falls
away outside over `falloff`, so the landform's *plan* is whatever was drawn — a crescent, a spur, a lobe.
Two pushes over the same ground add; two constraints over the same ground would have to argue.

| | `brow-w` — a mark | `spur-e` — a push |
|---|---|---|
| shape in plan | a disc, and only a disc | the ring that was drawn |
| height | exactly `h` | `amount` over whatever was solved there |
| composes with a neighbour | later one **wins** the contested cell | they **add** |
| top | flat at `h` across the whole radius | domed by `crown` along the shape's own medial axis |
| edge | the relaxation slopes it away | `falloff` blocks of skirt, wobbled by `roughness` |

`crown` is worth stating on its own, because it is the field that stops a push being a plateau. It says how
much higher the middle stands than the edge, and *the middle is not authored* — it is the deepest point of
the outline measured inward, the shape's own medial axis. On a round push that is a point and the crown makes
a dome; on a long push it is a line and the crown makes a ridge whose crest follows the spine. `crown: 3` on
a lobed ring gives a lobed hill for free.

## The radius is the whole of a point mark, and it is easy to get wrong

The first build stated `"r": 10` on a flank fifteen blocks wide. A point mark **pins a disc flat**, so the
disc swallowed the flank and the hill came out as a mesa with vertical sides — visible in one section and in
nothing else. `"r": 4` leaves ten blocks between the pin and the coast for the relaxation to slope through,
and the same mark reads as a knoll.

**A point mark's radius must be small against the ground it stands on**, or a hill is a plateau. There is no
gate for this; the section is the read.

## Three knobs that turn a field into ground

**`reach`** is how far a statement travels before the field falls back to `base`, in blocks. Zero is
unlimited — the marks decide the whole surface, which is what a room-sized island wants. **20** here makes
each hill a local landform with plain ground between, which is the difference between two summits joined by a
broad saddle and two hills standing in a field.

**`grain`** is deterministic value noise added after the solve — the wobble that stops a solved surface
reading as machined. It is hashed from the cell rather than drawn from a generator, so the map re-exports
identically, and **it is never allowed to override a mark**.

**`step`** is the block quantum. `1` follows the field. `2` reads as deliberate terracing and is *the one knob
that can break a map*: every riser becomes a two-block wall. `stairs: true` is the repair that ships with it —
one stair cut through each stranded place's cheapest riser. This board steps at 1 and still says `stairs`,
because the cost of saying so is nothing and the cost of forgetting is a board in halves.

## Two marks that are there for a reason and look like padding

**`coast`, the rim, is written first.** Marks resolve in order and the last one wins a contested cell — so a
rim written *after* a summit cuts a doorway through the high ground wherever the two meet, and hands anyone
walking a free way round it. Written first, it holds the shore at the base level and everything else is
solved inside it.

**`strand`, the line right across the board at `z −21`, holds a band of it at 9.** It runs two blocks north
of the far cairn, so the ground the objective stands on and the ground in front of it stay level whatever the
hills either side do — a summit rising under an objective moves the objective. A line mark's `h` is per
vertex and interpolated along its arc, so one stroke can also be a shoulder that falls as it runs; here all
three are 9 because level is the whole point. Note that a line's `width` is its **radius** — the band it
writes is twice it.

**And, like every authored shape on a `rot_180` board, the marks are solved on one half and mirrored.** The
relief is solved on the island's primary half and the answer reflected, so a mark stated on the far half is a
mark that does nothing. Both hills here are written at `z ≥ −21` for that reason, and `symmetryError: 0` is
what says the reflection took.

## What the relief read answers, and what it does not

```
POST …/sketch/relief/read
  island team: cells=10000  low=8  high=18  relief=10  symErr=0
```

`symmetryError: 0` is the one number here that no picture gives and that a hand-authored relief can silently
lose: nothing prevents an author drawing across the axis, and this says the two halves agree.

## The limit: paint cannot follow elevation

The hills are grass to their tops, because **a relief moves the surface inside one shape and a theme is
scoped to a shape.** There is no bucket keyed on height: `layered`'s axis is `depth` or `inward`, and a
pattern's `rise` makes its field three-dimensional rather than selecting by altitude.

Rock above a treeline is therefore not a paint decision — it is a second shape, with `relief_scope: "hold"`
and its own theme, standing where the high ground is. That is the `cairnmeadow` idiom and it is
`10-landform-shapes`.

## What to look at

| Picture | Says |
|---|---|
| `GET …/render/section?axis=x&at=6&from=-45&to=45&scale=7` | both hills in one cut — the only view that separates a mark from a push |
| `renders/world-heightmap.png` | the two landforms in plan, contoured, and their two images |
| `renders/world-ground.png` | almost nothing: paint is flat and relief is not a paint question |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — a relief is not a plan question |
| `POST …/sketch/relief/read` | cells 10 000 · low 8 · high 18 · relief 10 · **symmetry error 0** |
| `GET …/coverage` | 75.5% dead — unchanged from `02-theme`; relief moves ground, it does not add or remove any |
| `GET …/preflight` | export gate **OPEN** |
