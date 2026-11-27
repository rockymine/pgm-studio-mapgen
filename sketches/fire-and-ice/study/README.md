# The fire-and-ice study: the author's terrain as lofts, and agents filling what is missing

**This folder holds a study on the author's hand-built half of an ice map, a CTW and DTC hybrid.** It has four
parts:
- a reconstruction of the author's terrain as loft lines;
- a 3D viewer that shows the map layer by layer, as a low-poly mesh or as blocks;
- a labelling of the building's rooms, tunnels, stairwells and exits;
- terrain variants for the two missing parts (the middle between the halves and the cover over the main building),
  built by agents under rules the author stated.

`LESSONS.md` beside this file records what went wrong on the way and where the limits were.

**The author's world is not in the repository.** It is the author's own download, read as untrusted data with
`python3 -I`. Every script here takes its region folder as an argument, or reads `viewer/map.json`, which is derived
from it.

## The reconstruction

**A surface is rebuilt the way the author's loft tool builds it.** The tool takes ordered lines of a few points each
and joins every consecutive pair with a mesh. `rec/lines.py` reads a terrain piece as stations across it, and one
line per interval at each station. A line starts as its two ends and the author's own markers near it. It takes a
point wherever the curve through those strays more than three quarters of a block from the piece.

**Lines are added in a fixed order.** First come stations at the author's markers. Then come stations where the
outline bends, then stations where the surface between two lines strays more than a block. Where a piece forks, each
arm is lofted onto its own stretch of the line it meets. A layer lying over the main one, such as the cover over the
staircase to the wool bunker, is split off and rebuilt as a free loft.

**Of the author's 18,801 terrain blocks, 3 lie more than a block from the rebuild.** Of the rebuild's 19,771 blocks,
46 lie more than a block from the author's. Exact block identity is 64–80% per piece, because every rasterisation
steps a slope differently, so "within one block" is the measure that means something. A thin-plate spline through
control points, the first approach in `rec/reconstruct.py`, left 146 blocks more than one away.

| piece | blocks | lines | points | free lofts |
|---|---|---|---|---|
| floor (light grey) | 5526 | 81 | 440 | 4 |
| yellow, staircase cover | 2386 | 41 | 228 | 2 |
| yellow | 1550 | 24 | 118 | 1 |
| light blue, largest | 1825 | 23 | 219 | – |
| lime retaining wall | 519 | 5 | 17 | – |
| green retaining wall | 393 | 4 | 13 | – |

**The lines are inferred, not the author's.** They reproduce the surface, but they need not sit where the author
drew them. The point density they imply, 10–13 points per 100 square blocks of surface, is the measure the variants
are held to.

## The viewer

**`viewer/index.html` is the published artifact's page**, with its data beside it:
- `map.json`: every block of the half with its layer, and the loft meshes from `rec/export_viewer.py`;
- `variants.json`: the accepted variants;
- `labels.json`: the labelled spaces;
- `compare.json`: the density and steepness readings from `variants/compare.py`.

**The page has four controls.**

- **Display:** a low-poly mesh, or blocks.
- **Extent:** the half alone, or the whole map turned 180° about the pivot. A middle variant's shift moves the
  turned half with it.
- **Overlays:** the loft lines and their points, or the mesh's triangles.
- **Layers:** each layer can be switched on or off. The groups are Gelände, Untergrund, Bauwerke and the labelled
  spaces, plus one selector for each slot's variant.

**Every loft is drawn at the top face of its blocks.** A loft drawn at the centre of its top block reads half a
block low beside any block structure.

**`viewer/check.js` takes screenshots of the page served locally, before a change is published.** The page loads
three.js from a CDN, and the harness answers those requests from local copies fetched with
`npm pack three@0.128.0`.

## The variants

**Agents design the missing terrain; the kit decides what may be delivered.** `variants/kit.py` gives each agent:
- the map as it stands;
- the middle's region;
- lofts from lines, with their blocks and triangles;
- the checks, an iso renderer, and the 180° symmetry;
- the export the viewer reads.

`variants/BRIEF.md` is the one brief every agent reads: what exists, the geometry, and the author's rulings. An agent
is given a variant id and a slot, and no concept.

**`kit.write` refuses a variant that breaks a hard rule.** It runs `kit.gate` and raises an error naming each
failure, so only a correct variant can reach the viewer. The gate checks the lofts themselves as well as their
blocks.

| rule | how the gate reads it |
|---|---|
| the middle fills exactly the span between the halves | `kit.span()`: both facing edges, closed by straight lines between their outermost points, the east end at the wool lane's corner (97, 53); `outside` and `void` 0 |
| the middle is one design turned 180° | every block's turn is a block; the turned half may move a few blocks away (`kit.set_shift`) |
| no sheer walls, no collisions | `walls` and `overlap` 0 |
| lofts stay inside | no loft point more than 2 blocks outside the span, or away from the cover's own blocks |
| the cover lies over the building | `kit.cover_rules`: every building column behind the facade ends in ground at y 48 or above, the walk level of the facade's top exit |
| the black-roofed penthouse stands free | no cover block at y 61 or above beside it |
| terrain never runs into the roof at roof level | no terrain-coloured block inside the checkerboard roof's outline at y 59 or below |
| the building's real exits stay open | `kit.door_blocks`: nothing in or within 3 blocks in front of the exits in `kit.DOORS` |

**The flush seams are read, not enforced.** `roof_seam` and `mountain_seam` report how the cover meets the flat
roof and the author's light-blue mountain. The gate does not refuse on them.

**Five variants are accepted.** The author judged them, and the gate passes four of their builds as they stand.
Bunker unterm Berg was accepted before the cover rule took its final form, and its build now fails it on 84 columns.

| id | slot | title | shift | readings |
|---|---|---|---|---|
| mid-7 | middle | Die Eismulde | (4, 10) | lens basin at y 11, 4–5 below the rims; 10.5 points per 100 |
| mid-8 | middle | Gletscherzungen am Eissee | (3, 8) | a tongue off each plateau, frozen lake at y 11; 9.7 |
| mid-9 | middle | Pingo-Furt | (3, 8) | shallow trough at y 14, two offset pingos; 6.9 |
| cov-2 | cover | Bunker unterm Berg | – | ridge behind the roof, a yellow shoulder up to it; 5.8; `below_floor` 84 |
| cov-6 | cover | Firnsattel über dem Bunker | – | firn saddle off the north mountain, a shelf flush with the roof; 12.3 |

**`simplify/` turns the Eismulde into something a person can build by hand.** Its agent laid 49 lines across the
gap, which is 158 points for one side. Four long lines along the gap (rim, mid-slope, basin rim and centre line)
carry the same basin in 27 points. Of its 1,421 columns, 96.6% lie within a block of the original and none more
than 2, and 47 edge columns at the two tips are left to close by hand. `markers/edit.py` writes such points into a
copy of the author's world as marker blocks, and leaves everything else in the world as it was.

## Running it

```bash
python3 -I sketches/fire-and-ice/study/rec/run_lines.py <world>/region sketches/fire-and-ice/study/rec arc
```

```bash
python3 -I sketches/fire-and-ice/study/rec/export_viewer.py sketches/fire-and-ice/study/rec sketches/fire-and-ice/study/viewer/map.json
```

```bash
python3 -I sketches/fire-and-ice/study/labels/label.py <world>/region
```

```bash
python3 -I sketches/fire-and-ice/study/variants/mid-7/build.py
```

```bash
python3 -I sketches/fire-and-ice/study/variants/compare.py
```

**`export_viewer.py` reads `rec/half.pkl`: the half's blocks from `load()` in `mid/full.py`, pickled.** A variant's build writes its `variant.json` only if the gate passes. `viewer/variants.json` is the
accepted variants' files joined into one list.

## Files

| path | is |
|---|---|
| `rec/pieces.py` | the author's terrain split into pieces by colour, with their markers |
| `rec/reconstruct.py` | the frame a sheet lies in, the thin-plate approach, and the scoring |
| `rec/lines.py` · `rec/run_lines.py` | the line-loft reconstruction and its run over every piece |
| `rec/export_viewer.py` | the half, its layers and every loft mesh, written as `viewer/map.json` |
| `variants/kit.py` | the agents' toolkit and the gate |
| `variants/BRIEF.md` | the brief, with the author's rulings |
| `variants/compare.py` | density, steepness and reach of the author's terrain and of every variant |
| `variants/<id>/` | an accepted variant: `build.py` and `variant.json`; the Eismulde's loft points as text and CSV |
| `viewer/` | the artifact's page, its data, and `check.js` |
| `labels/label.py` · `labels.json` | rooms, tunnels, stairwells, the facade and the openings, from the geometry |
| `markers/edit.py` | sets single blocks in a copy of a 1.8 world and keeps tile entities, entities and the rest |
| `simplify/` | the Eismulde as four long lines |
| `mid/` | the first-round ravine and centre sketches, superseded by the variants |
