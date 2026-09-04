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
| How do I reshape a compiled outline? | `PATCH …/sketch/shapes/{id}/vertices/{index}` moves **one** point; `POST …/vertices {"after": n}` adds one at that edge's midpoint; `DELETE …/vertices/{index}` | a second shape added on top to enlarge it, a subtract to eat into it, or a bend to move one corner |
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
