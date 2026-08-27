# 03 — paving, and what paint cannot draw

**The technique: scoping a theme to a patch of ground, choosing a pattern that is legible where it lands, and
the one thing an edge cannot be made of.**

This is `02-theme` plus three shapes and three themes: a flagged court across the middle of the board, a
checkered threshold on the way to the spawn hall, and a small dais beside the court. The board, the meadow and
the buildings are untouched.

## Scoping a theme to a patch

A compiled board is one polygon a team, so there is nothing for a second theme to attach to. The instrument is
an authored shape that adds no ground:

```json
{ "id": "court", "type": "rectangle", "operation": "add", "override": true,
  "floor": 0, "base_height": 10, "height_mode": "level", "skirt": 0,
  "relief_scope": "exclude", "theme": "court",
  "min_x": -16, "min_z": 4, "max_x": 16, "max_z": 20 }
```

Three fields carry the weight. `override: true` puts the shape after the ordinary algebra, so it overwrites
the column it lands on rather than arguing with it. `relief_scope: "exclude"` keeps it out of the island's
solve, so it holds the height it was drawn at. And **paint resolves smallest-area-wins**, so a 32 × 16 patch
laid over a 10 000-cell island takes the paint of every cell it covers — that is the whole scoping mechanism,
and there is no field named after it.

**This board is flat, and on ground a relief has solved the safe form is different.** An override-add
overwrites the column outright, and a shape stating no height rasterizes to one course at bedrock
(`HeightFn`: `BaseHeight ?? 1`) — the relief repairs that only where the cell is in a solved footprint. A
patch meant to *follow* solved ground is therefore an **ordinary** add one course thick: the taller add wins
the column, so it can never lower what it paints. `GENERATION-NOTES.md`, *A paint patch on solved ground*,
has the measurement — eleven strokes on `opus5-sandcaster` punched holes twenty courses deep before the form
was corrected.

**An authored shape appended to a mirroring island is fanned by the symmetry.** All three shapes are written
once, for team 0, and both teams have them. Nothing states that; the island's `mirrors` does it.

**Which is why all three are drawn on one half of the board.** A patch has to stay clear of every *other*
patch's reflection as well as of the patches themselves: the dais at `x 20..28, z 4..12` images onto
`x −29..−21, z −13..−5`, and moved a little west it would land inside the court instead. `SK15` reads the
images and says so where the smaller of two contested shapes is also the shorter; where it is the taller, as
here, it simply takes the ground and nothing complains. Drawing on one half is what makes the question easy to
answer by eye.

## Three patterns, each where it is legible

`GET /terrain/patterns` answers fourteen kinds, and the field to read first is **`reads`** — the facts about
a cell each one varies with. It decides where a kind shows anything at all.

| Where | Kind | `reads` | Why there |
|---|---|---|---|
| the court field | `cell` | position | square patches on a jittered grid — flagstones, laid rather than grown |
| the door threshold | `checker` | position, arc, height | a 2 × 2 board, which is a threshold and is nothing in the middle of a field |
| the dais' side | `wallRun` | arc | stripes wrapping the perimeter — of the **island**, and only of the island |

The dais exists to carry the third one, and it is the one that does not work. `wallRun` states four runs —
two of sandstone, one of dark oak, two of end stone, one of dark oak — and the whole face comes out sandstone
on all four sides:

```
GET …/column?at=24,8      y 12  Polished Andesite   the surface, capping the drop
                          y 11  Stone Bricks        fill: the interior is not a face at all
GET …/column?at=20,4      y 11  Sandstone     ┐
GET …/column?at=27,4      y 11  Sandstone     │ the first run, on every column of the perimeter
GET …/column?at=27,11     y 11  Sandstone     │ — sixteen of them, four sides, one colour
GET …/column?at=23,11     y 11  Sandstone     ┘
```

The reason is stated in the type. A `wallRun` reads `BucketContext.PerimeterArc`, which is *"the cell's arc
index along the **outer void-facing wall**"*, and **`-1` — an internal riser — reads as arc 0 and takes the
first run**. The dais is a step up in the middle of an island, not a piece of its coast, so every one of its
columns is arc 0. The pattern needs the landmass's own edge, which is where a run several blocks long has
somewhere to run.

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
  same plateau. Measured: with `rim.enabled` and `rimEdges: "boundary"`, the column at the court's own
  edge answered the flagstone the `cell` palette had placed there, not the cobble the rim states.

**The kerb is a geometry decision, not a paint one.** Raising the court one course to `base_height: 10` gives
it a real drop, and with `rimEdges: "drop"` the rim course lands:

```
GET …/column?at=-17,10    y 8  Coarse Dirt        the meadow's own wall, exposed by the step up beside it
GET …/column?at=-16,10    y 9  Cobblestone        the kerb — the rim of a patch that is a course higher
GET …/column?at=-15,10    y 9  White Stained Clay one flagstone of the court's `cell` palette
GET …/column?at=-16,9     y 8  Stone              the wall under the kerb, one course of it
```

One block is also the right answer for play: the court is a step up rather than a line drawn on the grass.

Where `axis: "inward"` **is** the right instrument is the island itself — a shore band of gravel round the
whole landmass before the grass starts, which is exactly the distance it measures. `wallRun` is the same
answer from the same cause: both read a fact about the **landmass's** edge, so both belong on the map theme
and neither on a patch inside it.

## What to look at

| Picture | Says |
|---|---|
| `renders/theme-court-surface.png` | the flagstones as a swatch — the only view a pattern is legible in |
| `renders/theme-plinth-section.png` | the runs the plinth theme states — which the board does not paint, and why |
| `renders/world-ground.png` | the court in place, kerbed, against the meadow |
| `02-theme/renders/world-ground.png` | the same ground with nothing on it |
| `renders/world-heightmap.png` | the court and the dais as the only two steps on a flat plate |

A theme's **section** and its **surface** answer different questions and neither substitutes: the section is
the column — rim over wall over fill — and the surface is the swatch. A section through a voronoi is one
block wide.

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` — the plan is untouched |
| shapes | 1 compiled + **3 authored**, fanned to 8 by `rot_180` |
| themes on shapes | `meadow` 1 · `court` 1 · `threshold` 1 · `plinth` 1 |
| court | top y9, one course over the meadow's y8; dais top y12 |
| patches | court 32 × 16 · threshold 12 × 6 · dais 8 × 8, all drawn once on the `+z` half |
