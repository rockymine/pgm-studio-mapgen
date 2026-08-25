# 03 — paving, and what paint cannot draw

**The technique: scoping a theme to a patch of ground, choosing a pattern that is legible where it lands, and
the one thing an edge cannot be made of.**

This is `02-theme` plus three shapes and three themes: a flagged court in front of the spawn hall, a checkered
threshold at its door, and a small dais beside it. The board, the meadow and the buildings are untouched.

## Scoping a theme to a patch

A compiled board is one polygon a team, so there is nothing for a second theme to attach to. The instrument is
an authored shape that adds no ground:

```json
{ "id": "court", "type": "rectangle", "operation": "add", "override": true,
  "floor": 0, "base_height": 10, "height_mode": "level", "skirt": 0,
  "relief_scope": "exclude", "theme": "court",
  "min_x": -38, "min_z": 60, "max_x": -6, "max_z": 75 }
```

Three fields carry the weight. `override: true` puts the shape after the ordinary algebra, so it overwrites
the column it lands on rather than arguing with it. `relief_scope: "exclude"` keeps it out of the island's
solve, so it holds the height it was drawn at. And **paint resolves smallest-area-wins**, so a 32 × 15 patch
laid over a 6 000-cell island takes the paint of every cell it covers — that is the whole scoping mechanism,
and there is no field named after it.

**An authored shape appended to a mirroring island is fanned by the symmetry.** All three shapes are written
once, for team 0, and both teams have them. Nothing states that; the island's `mirrors` does it.

## Three patterns, each where it is legible

`GET /terrain/patterns` answers fourteen kinds, and the field to read first is **`reads`** — the facts about
a cell each one varies with. It decides where a kind shows anything at all.

| Where | Kind | `reads` | Why there |
|---|---|---|---|
| the court field | `cell` | position | square patches on a jittered grid — flagstones, laid rather than grown |
| the door threshold | `checker` | position, arc, height | a 2 × 2 board, which is a threshold and is nothing in the middle of a field |
| the dais' side | `wallRun` | arc | stripes wrapping the perimeter: legible on a **face**, one flat colour on a top |

The dais exists to carry the third one. A `wallRun` on flat ground is a solid square — it varies along the
perimeter arc, and a plateau's middle has no arc. Raised three courses it has a face, and the face reads as
banded masonry: two of sandstone, one of dark oak, two of end stone, one of dark oak.

```
GET …/column?at=-4,65        the dais' own side
  y 11  Sandstone     ← the rim course, capping the drop
  y 10  Sandstone     ┐
  y  9  Sandstone     │ wallRun, striped along the perimeter
  y  8  Stone Bricks  ← fill
```

## The thing that does not work, measured

**A patch flush with the ground it sits on cannot be given an edge by paint.** Two mechanisms look as though
they should draw one and neither does:

- **`layered` with `axis: "inward"`** draws concentric rings, and its own docstring describes *"a cobble rim
  then two rings of stone brick then a field"* — but the distance it reads is `BucketContext.Inset`, which is
  *"how many steps in from the **landmass's** void-facing edge the column stands"*. It is measured once per
  column over the whole island, not per shape. A court standing 3 blocks in from the coast reads inset 3
  everywhere inside it, so every band is already past and the whole patch paints `beyond`. Measured: the
  intended cobble-then-andesite kerb never appeared, and the two columns that looked like it were flagstones
  the `cell` palette happened to place there.
- **`rimEdges: "boundary"`** caps *"every plateau boundary, including … level ground the paint calls a
  different plateau"* — but a plateau is a **height** grouping, and an override-add at the same height is the
  same plateau. Measured: with `rim.enabled` and `rimEdges: "boundary"`, `column?at=-38,67` answered
  `Andesite`, not the cobble the rim states.

**The kerb is a geometry decision, not a paint one.** Raising the court one course to `base_height: 10` gives
it a real drop, and with `rimEdges: "drop"` the rim course lands:

```
GET …/column?at=-39,67    y 8  Grass Block     the meadow
GET …/column?at=-38,67    y 9  Cobblestone     the kerb — the rim of a patch that is a course higher
GET …/column?at=-37,67    y 9  Andesite        the flagged field
GET …/column?at=-38,66    y 8  Stone           the wall under the kerb, one course of it
```

One block is also the right answer for play: the court is a step up rather than a line drawn on the grass.

Where `axis: "inward"` **is** the right instrument is the island itself — a shore band of gravel round the
whole landmass before the grass starts, which is exactly the distance it measures.

## What to look at

| Picture | Says |
|---|---|
| `renders/theme-court-surface.png` | the flagstones as a swatch — the only view a pattern is legible in |
| `renders/theme-plinth-section.png` | the dais' banded face; the surface view of the same theme is flat |
| `renders/world-ground.png` | the court in place, kerbed, against the meadow |
| `02-theme/renders/world-ground.png` | the same ground with nothing on it |

A theme's **section** and its **surface** answer different questions and neither substitutes: the section is
the column — rim over wall over fill — and the surface is the swatch. A section through a voronoi is one
block wide.

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| shapes | 2 compiled + **3 authored**, fanned to 6 by `rot_180` |
| themes on shapes | `meadow` 2 · `court` 1 · `threshold` 1 · `plinth` 1 |
| court | y9, one course over the meadow's y8; dais top y12 |
