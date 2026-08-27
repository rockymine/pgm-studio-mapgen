# 10 — a landform authored as a shape, not as a mark

**The technique: four fields — `height_mode`, `skirt`, `anchor_heights`, `relief_scope` — that let a shape
stand out of a relief-solved field and carry its own paint, so a tor is grey stone standing in grass rather
than a grass hill wearing a grey texture.**

This is `02-theme` plus a modest relief and four authored shapes on team 0's flank: `tor` (a raised knoll,
`height_mode: "raise"`), `delve` (a sunken bowl, `"sink"`), and two small `hummock`s sharing the tor's own
theme. All four are written once, for team 0, and appear on both teams because the island they are appended
to, `team`, mirrors.

## The document

```json
"relief": { "team": {
  "base": 9, "reach": 22, "step": 1, "stairs": true,
  "grain": { "amplitude": 0.6, "scale": 9, "seed": 4 },
  "marks": [
    { "id": "coast",      "kind": "rim",   "h": 9,  "depth": 1 },
    { "id": "heartswell", "kind": "point", "at": [-1, 14], "h": 11, "r": 18 }
  ]
} },
"addShapes": [
  { "id": "tor", "type": "polygon", "operation": "add", "floor": 0, "base_height": 8,
    "height_mode": "raise", "skirt": 5, "relief_scope": "hold", "theme": "tor",
    "vertices": [[27,12],[33,8],[38,14],[38,26],[33,32],[27,30],[25,20]],
    "anchor_heights": [4,7,8,6,4,3,3] },
  { "id": "delve", "type": "polygon", "operation": "add", "floor": 0, "base_height": 7,
    "height_mode": "sink", "skirt": 2, "relief_scope": "exclude", "theme": "delve",
    "vertices": [[-37,14],[-33,10],[-30,12],[-30,24],[-33,30],[-36,28],[-38,20]],
    "anchor_heights": [3,5,7,5,3,2,2] },
  { "id": "hummock-a", "height_mode": "raise", "skirt": 4, "theme": "tor", "...": "6 vertices, anchors 1-4" },
  { "id": "hummock-b", "height_mode": "raise", "skirt": 4, "relief_scope": "hold", "theme": "tor", "...": "6 vertices, anchors 1-4" }
]
```

`tor` and `hummock-b` declare `relief_scope: "hold"`, `delve` declares `"exclude"`, `hummock-a` declares
none. That spread is deliberate — see *What `relief_scope` does on a landform shape*, below.

## `height_mode`: what a shape's top is measured from

A shape without `height_mode` is ordinary ground: its footprint joins the island, and whatever the relief
does inside that footprint is the ground. The three words are for a shape meant to stand **out of** the
field rather than be it, and they differ in what the top is measured **from**.

`level` cuts an absolute height: the datum is the shape's own `floor`, so the top is `floor +
anchor/base_height` regardless of what is underneath. A probe shape (`floor: 9, base_height: 3`, no
`skirt`) built a flat plate at y9–y11 with **nothing under it** — the column reads three solid blocks and
then void all the way to bedrock, five blocks from ordinary ground that fills solid from y8 to bedrock. A
`level` shape whose `floor` does not match the ground it is meant to sit on floats.

`raise` and `sink` are relative, and the datum is the **median of the ground already under the shape's own
footprint**, read once, before the shape is erected — not per cell, which is what keeps a knoll one thing
standing proud rather than a blanket following the hillside it sits on. Off in the open (away from any
relief mark), that ground is the field's flat `base`: 9. Under the `hummock`s, which sit inside the
`heartswell` point mark's radius, the pre-erection ground is already lifted — measured, plain grass 3
blocks from any authored shape reads **y8** at `(0,−30)` (base, untouched) and **y9** at `(−1,14)` (inside
`heartswell`'s reach). A landform's `raise` reads off *that* solved surface, not off `base` directly: this
is the real interaction a relief and a landform shape have, and it is why a modest relief belongs on a board
with landform shapes even though `relief_scope` (next) turns out not to matter to them.

`sink` is the same read with the sign flipped: `delve`'s floor sits at y5 against a coastal rim of y8,
which is `raise` and `sink` sharing one formula (`datum ± max(1, anchor)`) rather than two.

## `skirt`: the difference between a landform and a plinth

**This is the field worth two transects.** `skirt` is how far in from its own outline a shape eases toward
the ground it meets. Zero blends nothing — every covered cell takes its computed height outright, edge cell
included. Set `tor`'s `skirt` to 0 and cut a transect across it at `z=20`:

| x | 24 | 25 | 26 | 27 | 28 | 30 | 32 | 34 | 36 | **38** |
|---|---|---|---|---|---|---|---|---|---|---|
| y (skirt 0) | 8 (meadow) | 11 | 11 | 11 | 11 | 12 | 13 | 13 | 14 | **8 (meadow)** |

Eight to eleven in one cell entering, fourteen to eight in one cell leaving: exactly "an unskirted mesa
drops its whole thickness in one cell," measured rather than quoted. The shipped board sets `skirt: 5` and
cuts the same transect:

| x | 24 | 25 | 26 | 27 | 28 | 30 | 32 | 34 | 36 | **38** |
|---|---|---|---|---|---|---|---|---|---|---|
| y (skirt 5) | 8 | 9 | 9 | 9 | 10 | 12 | 13 | 11 | 10 | **8** |

A ramp of one block a cell each way, linear, exactly as `Erect`'s skirt formula is documented: `top` blends
from the ground just outside to the shape's own stated height over `skirt` blocks. The two transects are the
same shape, the same anchors, the same relief underneath — `skirt` is the only field that moved, and it is
the whole difference between a mesa with vertical sides and a knoll growing out of the ground.

**A skirt reaching the island's own coast free-falls to the shape's floor, not to the coast.** The first cut
of `delve` put a vertex at `x=-40` — the board's own edge — with `skirt: 4`. `InwardDepth`'s search for
"the ground just outside" found void there, and void has no ground to blend toward, so it fell back to the
shape's own `floor` (0): the column at the coast read a single block of **bedrock at y0**, a hole punched
through the shoreline rather than a talus meeting it. Moving `delve`'s footprint two blocks off the coast
and dropping its `skirt` to 2 fixed it outright — `x=-40` now reads the ordinary y8 coastal rim, and the bowl
eases down cleanly inside it (`x=-38` y7 → `x=-34` y5, the floor, → `x=-30` y8 again). **A landform shape's
skirt needs real ground on every side it blends toward**, coastline included.

## `anchor_heights` are offsets from the datum, not absolute heights

`tor`'s `anchor_heights` are `[4, 7, 8, 6, 4, 3, 3]` — small numbers, nowhere near the y11–y13 the shape
actually stands at. That is because the value is not the top; it is the amount **added to (or, on a sink,
subtracted from) the datum**, per vertex, and interpolated across the footprint as a triangulated surface
(a TIN over the vertex mesh). `raise` and `sink` share the one formula: `top = datum + rise · max(1,
round(anchor))`, `rise` being `+1` or `-1`. With a flat `base_height` instead (no matching `anchor_heights`),
every cell gets the same number and the top is level except where the relief underneath already varies —
`anchor_heights` is what makes a single shape's own top uneven, which a flat mesa or a flat monolith cannot
do. A shape whose `skirt` is large relative to its own width never quite shows this at full strength: `tor`
is roughly 14 blocks across at its narrowest and its `skirt` is 5, so only a thin core ever reaches the
un-blended `datum + anchor` value — the same lesson `07-hill` states for a point mark's radius, restated for
a skirt.

## What `relief_scope` does on a landform shape: nothing, and that is the finding

`relief_scope` says whether an *ordinary* shape's ground takes part in its island's relief solve — `hold`
pins it at a stated top, `exclude` removes its footprint from the solve, absent means it is solved as part
of the field. None of that reaches a shape that also declares `height_mode`: such a shape has already
opted out of being "part of the field" the moment it says `raise`/`sink`/`level`, and `raise`/`sink` need to
read the ground under their own footprint to know where to stand — an excluded footprint would have nothing
to read.

The four authored shapes carry three different values on purpose — `tor: "hold"`, `delve: "exclude"`,
`hummock-a`: absent, `hummock-b: "hold"` — specifically to check this. All four came out explained
completely by `height_mode`'s own formula and nothing else: `hummock-a` (no `relief_scope`) and `hummock-b`
(`"hold"`) both rise from the same local baseline (y10, inside `heartswell`) to the same kind of peak (y12)
over the same kind of skirt, with no trace of a pin or an exclusion in either. **A landform shape does not
need a `relief_scope` opinion at all** — the field is inert once `height_mode` is set, which is worth stating
outright because nothing about the JSON shows it: the two fields sit right next to each other in the same
object.

## What went wrong first

Two things, both above: the `skirt: 0` mesa, and the coastal free-fall. A third, smaller one belongs here —
`tor`'s theme originally set `rimEdges: "drop"`, matching `cairnmeadow`'s own `crag` theme. On a shape whose
own top is a TIN mesh plus relief grain, almost every cell has *some* neighbour one block higher or lower
than itself, and `"drop"` caps every such step with the rim material — Cobblestone, in this theme. The whole
mound painted as a Cobblestone cap over plain Stone fill, with none of the intended Andesite/Stone-Bricks
mottle or the Podzol thread anywhere in the built world, even though the theme's own swatch preview (which
renders flat, not against this shape's actual unevenness) showed the mottle correctly. Setting `rimEdges:
"void"` — the rim caps only where the column genuinely faces the map's own void, which a shape sitting well
inside the island never does — let the surface bucket paint the whole mound instead. `03-paving`'s caution
that a section and a swatch answer different questions held again, one showcase later, on a different bucket.

## What to look at

| Picture | Says |
|---|---|
| `tor-section-z42.png` (`…/render/section?axis=x&at=42&from=15&to=45&scale=8`) | the knoll's talus skirt easing up from the meadow, the Podzol thread visible on its face |
| `delve-section-z42.png` (`…/render/section?axis=x&at=42&from=-45&to=-15&scale=8`) | the sunken bowl, a clean V from the coastal rim down |
| `theme-tor-surface.png` | the grey-stone mottle with the loam thread — what the shape actually paints, not a swatch |
| `world-ground.png` | the tor (grey) and the delve (brown) flanking the void gap, the two hummocks as small grey knolls north of it, meadow everywhere else |
| `world-heightmap.png` | the tor and the hummocks lighter (higher), the delve darker (lower), against the flat meadow field |
| `world-mirror.png` | `NONE ABOUT` — every authored shape landed on both teams with no asymmetry |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| `POST …/sketch/relief/read` | island `team`: cells 10 000 · low 9 · high 11 · relief 2 · **symmetry error 0** |
| baseline grass, no shape or mark nearby (`0,−30`) | y8 |
| grass inside `heartswell`'s reach (`−1,14`) | y9 |
| `tor` transect, `skirt: 0`, `z=20` | 8 → **11** → 11 → 11 → 11 → 12 → 13 → 13 → 14 → **8** |
| `tor` transect, `skirt: 5` (shipped), `z=20` | 8 → 9 → 9 → 9 → 10 → 12 → 13 → 11 → 10 → 8 |
| `delve` at the coast, `skirt: 4` touching `x=-40` | **y0, Bedrock** — a hole, not a shore |
| `delve` at the coast, `skirt: 2`, footprint moved off the edge (shipped) | y8 Cobblestone — the ordinary coastal rim |
| meadow 3 blocks from `tor` (`22,20`) vs. on `tor` (`28,20`) | Grass/Dirt/Dirt/Stone (meadow) vs. Podzol/Dirt/Dirt/Stone (tor) — the skin is the whole difference |
| `GET …/coverage` | 2 451 reached · 7 549 dead · 75.5% — unchanged from `02-theme`: the shapes add height, not new dead ground |
| `GET …/preflight` | export gate **OPEN** |
