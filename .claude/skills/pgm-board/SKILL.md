---
name: pgm-board
description: Author, revise or read a PGM map in this repository through the pgm-studio API — a destroy/capture/core board, a spec under specs/, a world under maps/. Use whenever the task is to build a map, change one, diagnose one that built wrong, or read an existing PGM world. Carries the read-before-you-believe procedure and the lookup table from question to the read that answers it, distilled from 27 Opus 5 runs.
---

# Authoring a board here

`AUTHORING-BRIEF.md` is what the board should be. This is how not to lose a build finding out.

Everything below is measured off the run reports in `reports/opus5-*.md`. Each rule cost at least one
build, most of them more than one, and several were paid twice by different runs.

---

## 1. The lookup table — the question, and the read that already answers it

**Reach for a row before you write anything that computes an answer.** The single most-repeated
sentence in the reports is a variant of *"the instrument I should have used exists and I did not know
about it."*

| The question | The read | Not |
|---|---|---|
| What is actually at this coordinate? | `GET /map/{slug}/column?at=x,z` | any render — every other read is a projection |
| Does this climb? Is that step walkable? | `GET …/transect?points=x,z;x,z&beside=2&format=text`, or `03-slopes.txt` | eyeballing a heightmap shade |
| Where does the ground step, over the whole board? | `03-slopes.txt` — `. walked · : scramble · # barrier`, plus a per-face summary | — |
| How high is the ground along this line? | `tools/loop.py --profile x=<x>,z=<a>..<b>,step=1` | your own arithmetic over the anchors |
| How **steep** is the ground, and where? | `GET …/incline?format=text` — the glyph is the tens of degrees, and under the grid, how much ground stands in each ten | `03-slopes.txt`, which answers a *step* (can it be walked) and not an *angle* (how should it be finished) |
| Which two **marks** built that wall? | `POST …/sketch/relief/read` → `seams`, worst first, each naming the pair and the cell; `RL3` fires above a scramble | a face in `03-slopes.txt` or the relief read, which report the wall as terrain and attribute it to nothing |
| What does a column hold, layer by layer? | `tools/loop.py --column x,z` | reading a world file yourself |
| May a prop stand here? | `06-claims.txt` (`POST …/sketch/dressing?format=text`), then `tools/loop.py --candidates <propId> x,z …` | placing it and reading the decline |
| What did the route actually cost? | `GET …/walk?from=&to=&aim=&format=text`, or `04-routes.txt` | assuming the shortest line is the route |
| …and on a **stacked** board? | the same read, with **`from=x,z,y`** — the `y` picks which storey of the column is meant | `x,z` alone, which walks to the column *under* an elevated goal and calls it walked end to end |
| Is a lower storey still made of what I painted it? | `GET …/column?at=x,z` | the isometric, the census, or the 200 — none of the three sees it |
| Is the board joined up, per team? | `GET …/preflight` | the export, at 409, after a whole world is built |
| Is any ground unused? | `GET …/coverage` (after) · `GET …/plan/flow` (before) | nothing — no gate asks this |
| What is the board made of, and what borders what? | `05-themes.txt` (`themes/census?format=text`) | counting your own theme dict |
| What is the plan's shape, before a map row exists? | `tools/board.py specs/<slug>/<slug>.plan.json` | a render of a built world |
| Is this section of the world what I think? | `GET …/render/section?axis=&at=&from=&to=&format=text` — **`axis` names the direction the cut runs, so `at` is the other coordinate** | a PNG section, which blends renderer gridlines over it |
| What fields does this pattern take? | `GET /api/terrain/patterns` — fourteen kinds with exact field names | guessing. One run invented **five field names out of five** |
| What does this refusal mean? | `GET /api/rules?rule=<id>` | inferring from the sentence |
| What does the house style build? | `POST /room-styles/preview-snapshot?format=png&view=section` (and `plan`; other views 400) | a top-down — every shipped roof fault was visible in a section and invisible from above |
| What does a whole multi-wing house build? | `POST /terrain/prop-preview` — the prop plus a theme | `preview-snapshot`, which draws a default box |
| How do I reshape a compiled outline? | `PATCH …/sketch/shapes/{id}/vertices/{index}` moves **one** point; `POST …/vertices {"after": n}` adds one at that edge's midpoint; `DELETE …/vertices/{index}`. A spec states them as `editShapes`, replayed before any bend | a second shape added on top to enlarge it, a subtract to eat into it, or a bend to move one corner |
| How do I make a whole edge read rougher? | `POST …/sketch/shapes/{id}/bend` with `side: out\|in\|both` (`out` is the default and is the bloat that reads as land) | restating the whole `vertices` array, which is a second copy of the coast |
| How do I get a flowing wall, lane or watercourse? | a `polyline` **shape** — the rasterizer splines its points (centripetal Catmull-Rom, 8 samples a segment) before offsetting the band, so 4 clicked points draw as a curve. `stroke_edge`: `solid` \| `rough` \| `tapered` | a chain of rectangles, or hand-authored `controls` |

**A world that is not a stored map** — a community map, a hand-finished world, anything with a
`map.xml` the studio did not write — is the one case none of the above reaches. `import-folder`
takes an **xml-less** folder under a configured `MapsRoots` only. Use `tools/anvil.py`, `probe.py`,
`trees.py`, `lift.py`, `world-diff.py`; they read Anvil in the standard library alone.

---

## 2. The two moments

A rule in a document does not fire. These are the two places to stop, and they are cheap.

**After `--dry`, before the first build.** Run `tools/board.py` on the plan and read the grid. A plan
is a list of rectangles and most of what goes wrong with one is a *relation between two of them*;
no render of a built world can show that, because by then they are terrain.

**After every drive, before you open a single PNG.** Open these three and say the numbers out loud:

```
03-slopes.txt   -> cells: N walked, N scrambled, N barrier; faces: N, largest N at …
06-claims.txt   -> placed N, declined N      (and: is the goal's clearance block empty?)
04-routes.txt   -> each team's walk: rises, falls, worst step, and what stands within two blocks
```

Then look at the pictures. The order is not taste: **a picture answers whether a thing came out, a
number answers whether it is right.** A one-block bump under a rail is one shade in a heightmap and
nothing at all in an isometric — `03-slopes.txt` names it with its coordinates, and it shipped in five
consecutive builds of `opus5-lindenkreuz` because nobody opened the file.

---

## 3. What you may write, and what you may not

**Write a `build-spec.py`.** A spec's plan and finish are large structured documents with arithmetic in
them — bay grids, per-course stairs, voxel models, ramp anchors. Generating them from a script *is* the
authoring work, it is what every run here has done, and it is what makes a board re-buildable. Keep it
in `specs/<slug>/` beside the documents it writes.

**Do not write anything that reads the built world.** No ground-finder, no section renderer, no walk
checker, no clearance test, no site filter. Every one of those exists, and the home-made version has
been wrong every time it has been tried here:

> *"Then I wrote three ground-finders and two of them were wrong. 'The topmost solid block' reads a
> roof."* — `opus5-run6-7`
> *"I measured a stair every two blocks and called it walkable."* — `opus5-run6-7`
> *"I believed a 200 for two rounds. My scratch loop posted the layout with `PUT …/sketch/from-plan`"*
> — `opus5-elderwold` (a home-made driver silently lost every edit)

**The run rules say "no capability is added in `tools/`", and that wording has a hole in it.**
`opus5-lindenkreuz` complied with it exactly — nothing was added to `tools/` — while writing a section
renderer, a surface census and a column probe in a scratch directory instead. The rule is about
**second copies of the system**, wherever they live.

The one legitimate exception is §1's last row: a world that is not a stored map.

---

## 4. Seven failures that have each cost more than one run

### A picture that looks plausible is not a read

`opus5-thunder-series` reconstructed three boards from top-down renders and had to redo them.
`opus5-tarnfell` read `world-material.png`, saw sand, and concluded the lake was missing — the material
top-down draws the top **solid** block, so water reads as its own bed. `opus5-run4` read the
traversability map and nearly redesigned a correct board (`B99`: an approach wall's cobweb reads as
impassable). `opus5-undercroft` read a transect through a filter capped at y22 and concluded a causeway
was six blocks low.

> *"`GET /api/map/{slug}/column` is the read that settled every disagreement."* — `opus5-interchange`

**When two reads disagree, `column` is the one that is not a projection.**

### Assumed instead of measured

> *"I drew a stair for a fall I had assumed rather than measured."*
> *"I assumed the river's 8-block drop was the same on both banks. It is not."* — `opus5-liminal-dtm-ii`
> *"I assumed water spreads to fill a level pan."* — `opus5-rimegarth` (water fills its own band; the
> pan is the size of the pool)
> *"I read `maxPlayers` as the board's cap and shipped a 48 v 48 map."* — `opus5-liminal-dtm-ii`

The tell is always the same: a number you derived yourself, used as if it had been read back. If you
computed it, **transect the thing you computed** before building on it.

### A spec in this repository is dated evidence, not the current contract

`opus5-lindenkreuz` copied `"plan": 1` and the marker offsets in cells from the specs it read first, and
the compile refused: *version 2 states marker offsets in blocks from the piece corner.* Two spec
documents in `specs/` disagree with the API by exactly one cell size.

The same applies to `GENERATION-NOTES.md`, which is headed *"Measured against pgm-studio at b45b154"*.
Its claim that theme scope is cross-layer is **stale** — `ShapeScopeOwners` keys on `(layer, x, z)`.

**Order of authority: the API's own answer › the schema in `openapi.json` › the notes › a committed
spec.** Read source only where two of those disagree, and then read the narrowest thing that settles it.

### "Missing from the system" is a claim about the surface until you check

`opus5-run2` had to correct two earlier reports: *"per-shape themed materials — missing from the
system"* — **false**; *"relief marks with area scope — missing"* — **false**. `opus5-run8` shipped a
wrong explanation of `SK11` and filed a wrong bug against the 3-D preview that the author caught.

Before writing that something is missing, look for it in `GET /api/openapi/v1.json` and say what you
found. **missing** (no mechanism) · **unreachable** (exists, the surface hid it) · **mistaken** (exists,
documented, not found) are three different verdicts and only the first is a capability gap.

### The plan was cut up so a theme would have somewhere to hang

A plan states the board's **arrangement** — which ground is where, at what height, next to what. It is not
the board's shape, and adding pieces to get a shape is the failure. `firnline` is the worked example:
**13 plan pieces at 6 surface heights**, then `themeByHeight` mapping each height to a theme, so the theme
partition is the piece partition and the board's look was decided by how it happened to be cut up. It reads
chopped rather than coherent, and no amount of dressing repairs it.

The same board is **one terrain shape plus two platforms**: author the ground the map is played on as one
shape (or as few as the arrangement genuinely needs), reshape it per vertex until it reads as ground, then
put the monument shelf and the middle plateau on `addLayers` slabs over it, each with its own `base_y` and
its own theme. A piece earns its place by stating something the arrangement needs — a height a lane climbs, a
room a building is seated in, a footprint the symmetry fans. A piece that exists only so a theme can be hung
on it should have been a shape scope.

**Construction comes before dressing, and a bad construction cannot be dressed out of.**

### The ground was finished by its height instead of its angle

A board painted one material per plan piece, or one per height band, comes out a flat sheet from above however
much relief is under it: the quarry, the graded terrace and the cut banks are all in the picture and none of
them is visible. Nothing in the geometry tells a 45° hillside from a meadow — such a surface has no exposed
riser, so the `wall` bucket never sees it and every other band axis paints the two alike.

**Give the ground theme's surface a `layered` material on the `slope` axis.** A thickness on that axis is a
span of **degrees**, so one stack finishes the flat, the shoulder and the face of the same hill, and each band
takes a depth stack of its own so grass stays one course over its soil:

```json
{"kind": "layered", "axis": "slope", "stack": {"ending": "repeat", "bands": [
  {"material": <grass over two dirt>,       "thickness": 30},
  {"material": <coarse dirt over two dirt>, "thickness": 15},
  {"material": <stone/cobble cells>,        "thickness": 45}]}}
```

**Read `incline` before choosing where the bands cut.** It answers how much ground stands in each ten degrees,
which is the only thing that says whether a cut lands where you think it does — and a distribution with a
*spike* in it is a board reporting its own `step` quantum rather than its shape. `opus5-scarp-mask` is the
worked example: 68% moor, 8% shoulder, 11% rock on ground that was 86% grass and nothing else.

### A mark's band ends on a wall, and `tread` is the answer to both ways it happens

**A road drawn as a line walls itself.** A `line` mark pins every cell to whichever pass of the line is
nearest, so a serpentine, a switchback or a spiral haul road puts the cells either side of the midline between
two passes a whole winding apart in height. State a **`tread`** narrower than `r` and the rest of the band
lofts — a ramp between the two treads' edges. Left alone it spreads over the whole run,
`atan(drop / (pitch − 2·tread))`, and for a spiral the pitch is `(r0 − r1) / turns`; **`batter`**, in degrees,
makes it steeper and puts a flat bench at the toe, which is what a worked quarry looks like. Work the pitch out
before building — under `2·tread` there is no run to grade in, whatever is stated.

**Two different marks whose bands touch do the same thing**, and this one is easy to miss because neither mark
looks wrong on its own. The later one wins its cells outright and the seam is one cell carrying the whole
difference. A `tread` on the later mark grades it: the shoulder states its height softly and blends into
whatever the earlier mark put there. The shoulder's **width** sets the grade — 22 blocks over a 4-cell shoulder
is 5.5 a cell, over 10 cells it is 2 — so a gentler seam means a narrower tread or a longer reach.

**Do not go looking for these in a render.** `POST …/sketch/relief/read` answers `seams` per group — every
pair of marks whose ground meets on a step of more than a block, worst first, each with the coordinate to
stand at — and raises `RL3` where one is taller than a scramble. It also answers `silentMarks`, the marks that
pinned nothing at all because they were placed off their group's ground (`RL4`). A seam that grades reports
nothing, so the list is the fault and not the arrangement.

*`opus5-scarp-mask` at (14, −78): `crest` (r 18, h 33) and `terrace` (r 13, h 24) overlap, and the transect read
`33 33 33 DROP −9 24`. The read named it `crest | terrace, step 10 at (7, −80), 43 cells`. With `tread: 7` on
the terrace the transect reads `33 33 32 31 29 28 26 25 24` and the seam is gone. Board-wide, 1,006 barrier
cells became 480.*

### A layer's paint reaches further down than the layer does

A **plain** stacked layer's bands run from the **bedrock course**, whatever its `base_y`; only a made
layer (`kind: "made"`) is painted over its own span. The one thing keeping a pass off the layer below
is the stone-only invariant — it writes over `(1, 0)` and nothing else — so a ground theme filling in
plain stone hands the whole column to whatever is drawn above it.

> *"`y 42..39 Iron Block` the viaduct rail, `y 29..27 Stone Bricks` the street lid, `y 26..1 Iron
> Block` — twenty-six courses of city painted as rail."* — `opus5-tiefkreuz`

Nothing says so. The store answers 200, the export gate answers OPEN, `themes/census` counts the
**surface** and is right, and a top-down of a lit street is grey either way. **On any board of more than
one plain layer, `column` a cell where two of them overlap before you believe the render** — and give
every ground theme a `fill` that is not `1:0`.

### Dressing placed by eye is dressing declined

`opus5-hoarstone`: *"My site filter ignored the fan"* — a prop is judged at **every image of its orbit**;
and *"I tested footprints against the authored polygon instead of the built coast"* — a Bézier edge
bulges outside the vertex ring on a convex stretch and inside it on a concave one. `opus5-hollowmarch`:
*"My keep-out model for the dressing was the wrong shape twice"*. `opus5-smallboards`: four buildings
declined `DR-KEEP` at once.

`06-claims.txt` is the whole board as one raster of what claims each cell — free, route, structure,
tree, goal clearance, spawn keep-out. **The raster says where to try; `loop.py --candidates` says
whether the try lands**, eight candidates for one pass. Neither costs a build.

---

## 5. The order a board is built in

```
build-spec.py            write the plan and the finish
tools/board.py           the grid — relations between rectangles
drive.py --dry           evaluate + inspect: score, GO1/GO3/GO4, CT12, the lint table
                         ── iterate here; this is where the board's shape is decided ──
drive.py --out …         compile, store, read back, pre-flight, export, render, text
03/06/04-*.txt           the numbers, before the pictures
loop.py                  every placement question after the first drive — twenty seconds, not ten minutes
```

**A refusal is a fault to fix, not a step to work around.** Do not re-post a refused document with
different numbers until you have read why it was refused.

**Every 2xx carries `warnings`, and a `decline` means a piece of what you posted is not in the world.**
`SK9`, `SK10`, `SK15`, `WX11`, `HS7`, `DR-*` all arrive on a 200. The status code is half the answer.
