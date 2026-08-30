# tools/ — the one driver, and the two probes beside it

## `drive.py` — a plan and a finish, through the API, to a world

```bash
python3 tools/drive.py specs/<slug> "<Map Name>" --out <worlddir> [--slug <slug>] [--dry]
```

`PGM_STUDIO_API` overrides the endpoint (default `http://localhost:7894/api`).

The directory's own name is the slug the map is stored under unless `--slug` says otherwise, so re-driving a
corrected spec **replaces** the map it had rather than leaving a second one beside it.

`specs/<slug>/` holds exactly two authored documents, both named after the directory:

| File | Is |
|---|---|
| `<slug>.plan.json` | a `PlanModel` — the board as cell rectangles, the objectives, the walls |
| `<slug>.finish.json` | everything a plan cannot state, keyed onto the layout the plan compiles to |

The driver writes two more beside them — `<slug>.layout.json` and `<slug>.intent.json`, the documents it
actually posted — so a review reads what was built rather than what was asked for. **Those two are output
and never input.** A spec carrying a finish is compiled from its plan on every run and the pair is
overwritten; a spec with no finish is a board drawn in the Sketch tool, and then they are the authored
geometry and are read. The finish is what decides which, because `addLayers`, `addShapes` and `bendShapes`
all append — reading back a layout the driver wrote and patching it again gives two storeys called `under`
and a ring bent twice.

### What the finish carries

| Key | Is |
|---|---|
| `themeById` · `themeByHeight` | the theme a compiled shape paints with, by its id or by the height it stands at. The id is the reliable one: compile once, read the ids off `POST /plan/compile`, and key on them. Two pieces at one height fuse into one shape and a height key cannot tell them apart |
| `shapePropsById` · `shapePropsByHeight` | any field merged onto a compiled shape — `relief_scope`, `controls`, `anchor_heights`, `height_mode` |
| `bendShapes` | `{"s0": {"k": 0.22, "wander": 3, "step": 9, "seed": 5}}` — the compiled outline drawn as a coast. The compiler emits a staircase of the plan's rectangles, which is the board's shape and not its coast; redrawing the ring by hand states the coast twice, free to disagree with the plan. This resamples the compiled ring along its long edges, pulls each **inserted** point inward by a deterministic wander and lays Catmull-Rom handles over the result. The plan's own vertices never move, and nothing ever moves outward — a point that did could close the strait a capture board is measured on, or narrow the neck a spur hangs off |
| `addShapes` | authored `SketchShape`s appended to the first group: the subtracts, the erected shapes, the ramps, the path-shape causeways |
| `relief` | `{"<groupId>": {...}}`, or `{"*": {...}}` for every group. A compiled board's groups are `team` and `neutral` |
| `themes` · `mapTheme` | the theme registry and the map default (the first key unless stated) |
| `roomStyles` | `{"cage": …, "spawn": …}`; a `"@name"` string loads `tools/styles/<name>.json` |
| `dressing` | `{"props": [...]}`; a house prop's `style` takes the same `"@name"` |
| `authors` | `["Opus 5"]`, or `[{"name": …, "uuid": …, "role": …, "contribution": …}]`. PGM takes a person as an **account or a pseudonym**: a bare name writes `<author>Opus 5</author>`, a uuid writes `<author uuid="…"/>` with the name as a sibling comment, and a pseudonym may still carry a `contribution` |
| `created` | `"2026-08-25"` — when the map was made, onto `intent.meta.created` and out as `<created>`. The studio derives every other identity field and cannot derive this one, so a finish that states none builds a map with no date and the driver says so |
| `voidEnforcement` | `true` patches `intent.build.voidEnforcement`, with `voidExclusions` for the rects to spare |
| `goalLayers` | `{"destroyable-1": "under"}` — which storey a goal stands on, by its plan marker id, patched onto the compiled intent by `stamp.unit` |
| `addLayers` | `[{id, name, base_y, shapes, groups, below?}]` — the storeys a plan cannot state. `below` inserts one under the compiled ground, where the painter's bottom-up order needs it |

### The grid, before the plan is posted

```bash
curl -s "$PGM_STUDIO_API/map/<slug>/plan/ascii?every=2"
```

`text/plain`, one character per proxy cell, with a key. It is the cheapest check there is and the only render
a caller with no image reader can act on. A plan is a list of rectangles measured in cells and most of what
goes wrong with one is a **relation between two of them**; a rendered world cannot show that, and a grid puts
them on the same rows. `?every=N` draws one character per N cells for a board wider than a terminal.

```
   -1 | MMMMMMMMMMMMMMMM |   M the neutral bar — sixteen cells
    0 | MMMMMMMMMMMMMMMM |
    1 | NNNN     OOOO    |   N the build zone that reaches it — four
```

`GET /plans/{id}/ascii` is the same render for a candidate in the generator pool, by id rather than slug.

It reads the **stored** plan, so it answers from the store onward — which is where the driver prints it,
downsampling only when the board comes back wider than a screen. Before a map row exists, `board.py` below is
the same idea off the plan file itself.

### What it prints, and why that is the point

It composes nothing and validates nothing. What it does is **print every finding the pipeline raises, with
its rule id and the JSON path it is about**.

**Every call prints its own complaints, in `call` rather than at the call sites.** A 2xx is not a promise
that everything posted survived: a `decline` says one piece of the document is not in the world, `RQ3` names
a posted field that went unread, and `SK3`/`SK4` name a shape that drew no ground. The status line carries
the `Pgm-Warnings` header after the code — `200   ! 6 RQ3 SK3 SK4` — wherever the complaint channel
collected anything; the body's own `warnings` array is read either way, because an endpoint answering
`warnings` as its own field, as `/plan/evaluate` does, fills it without the header.
`GET /api/rules?rule=<id>` answers what any id means and how to fix it.

The four places a finding appears:

1. **before a map row exists** — `POST /plan/evaluate` (score, `valid`, the hard/soft terms and the whole lint
   table) and `POST /plan/inspect` (`goalDistances` against `GO1`'s 3.0–4.0 band, `islandGaps` against
   `CT12`'s 15–40, the wall rects, the frontline runs);
2. **at the compile** — `POST /plan/compile`'s `warnings`, and its 422 findings if it refuses;
3. **at the store** — `POST /map/from-documents`'s `SK3`/`SK4`/`SK5`/`SK11`, its `RQ3` over all three
   documents at once (each path named with the member it was posted under — `layout.setupp`, not `setupp`),
   and `relief/read`'s per-group cells, low, high and symmetry error;
4. **at the dressing** — `POST …/sketch/columns`'s `DR-*` declines, read **after** the intent is stored,
   because `DR-KEEP` needs the spawn doors and the goal rings the intent carries.

Then **three reads that raise no finding at all** and are printed anyway. A read that refuses nothing is the
one an author never runs, so the driver runs all three rather than leaving them to be remembered:

- **`GET …/plan/ascii`**, after the plan is stored and before anything is compiled — the board as a grid of
  characters, one per proxy cell. A plan is a list of rectangles and most of what goes wrong with one is a
  *relation between two of them*, which no render of a built world can show, because by then they are terrain.
- **`GET …/plan/flow`**, beside it — what the board asks of the two sides, in prose: each objective's two
  walks and the ratio between them, where the ways in part and meet, whether the defence shares the
  attackers' road, and the ground no journey reaches. Off the plan alone, so it costs no build.
- **`GET …/coverage`**, at the far end — the reached / decorated / dead shares and the five largest dead
  patches with their coordinates. Every gate in the four places above asks whether ground is *reachable*;
  this is the only read that asks whether any journey **goes there**, and a board can pass all four while
  carrying a quarter of its ground unused (`GENERATION-NOTES.md`, *Reachable is not used*). Where a
  board has no two waypoints to join it says so rather than printing nothing, because silence there reads as
  "nothing dead" and means "never measured".

- **`GET …/preflight`**, after the intent and before the export — the export's own verdict, asked before the
  export. It runs the same `Traversability.Check` the export refuses on, **per team**, so a goal a team is
  barred from reaching is named with the team barring it; plus the codec round-trip, the mirror and
  buildability. Its log ends `export gate OPEN` or `export gate BLOCKED`. `EX1` at 409 after a whole world has
  been built and this line are the same answer at two prices.

The flow and the coverage are the same question at two ends of the pipeline: flow says *why* ground will go
unused while the board is still rectangles, coverage says *that* it did once a world exists to measure.

### The pictures, taken rather than remembered

After the export it writes every picture the studio will draw for what was authored, into
`<specdir>/renders` or `--renders <dir>`: the grid and the flow as text, one swatch per theme, a **plan and
a section per house** — the stamped rooms and every distinct house prop style — and the coverage map. That is
21 files on a board carrying six themes and six houses.

Two more it draws itself, because the studio answers columns and not cameras: `world-iso` from two quarters,
and `world-xray` from the same two where the board holds a covered space. The x-ray is the only view anything
underground appears in — `world-iso` draws a gaol under a meadow as a meadow — and it is written only when
the void scan finds a roofed void of at least 200 cells, because below that it draws the board the isometric
already drew, one shade paler. The scan itself runs on every board and prints what it found with the
coordinates: how much covered space, between which blocks, and how much of it is `SEALED`, meaning nothing
can walk into it.

They land beside the documents rather than in `--out`, and so does the provenance sidecar, which the driver
moves out of the exported `region/`. `--out` is what a game server is handed: `region/`, `level.dat`,
`map.xml`, and nothing a match does not read. A CLI read-back pointed at that region directory therefore
finds no provenance and falls back to the material estimate, which it states on its own scale line.

**The sweep is over files, so `renders/close/` is where a hand-taken picture belongs.** A render directory
is one run's output rather than an accumulation of every run's, and the sweep at the end of a run removes
whatever this run did not write — which silently deletes a picture an author took by hand and a README then
points at. A subdirectory is not touched.

The reason they are taken here is the reason the grid and the flow are printed here: **a read nobody is
refused for skipping is the read nobody takes.** Every shipped roof fault was visible in a section and
invisible from above, and no board in this repository had one until an author drew them by hand. Taking a
picture is not the same as looking at one; what this removes is the excuse.

**A style is serialized in the author's own key order.** A material's `kind` is read positionally, so sorting
the keys of a style that previews at 200 turns it into a 400 naming a kind that is right there (`TL2`).

A refusal stops the run rather than being skipped. **A refusal is a fault to fix, not a step to work around.**

Two things it deliberately does not do. It never computes a placement, a clearance or a sampler — that is the
capability the run rules keep out of `tools/` — and it never retries a refused call with a different
document. Both of those are the author's.

### One call stores the map

`POST /map/from-documents` takes the plan, the patched layout and the patched intent together and does the
whole store: the plan to re-plan from, the drawing rasterized into geometry, the intent projected into the map
document, the authors applied over that projection. The compile before it needs no map row, so both documents
are whole before anything is stored — which is what lets the store be one call, and what keeps the slug the
author's rather than one minted per attempt.

Everything after it reads the stored map, and one of those reads has to be there rather than earlier:
`sketch/columns` is asked **after** the store because `DR-KEEP` reads the spawn doors' approaches and the goal
rings, which come off the intent.

### The escape hatches

`--dry` stops after the evaluator and the inspect feed, so a plan can be iterated with no map row and no
build — which is where most of a board's shape is actually decided. The grid and the flow read the *stored*
plan and so are not in a dry pass; `board.py` covers the grid half of that loop. `--slug` overrides the slug
the spec directory's name would give, for a board stored under a name of its own.

## `board.py` — a plan as a grid, before it is a picture

```bash
python3 tools/board.py specs/<slug>/<slug>.plan.json ["<note>"]
```

Renders a plan's pieces and zones as an ASCII cell grid — one character per cell, upper case for a stated
rect and lower case for its symmetry image — with a legend giving each piece's cell rect, its block rect and
its size. **Run it before posting a plan.** A plan is written in cell rectangles, and the faults that matter
are relations between two of those rectangles: a stepping stone wider than the build zone that reaches it, a
wool room touching a piece its wall was meant to guard, a spur that connects to nothing. A grid puts the two
rects on the same rows and a rendered picture does not.

Run 4's own worked example is one line of it. In `specs/opus5-wheal-hazel/renders/00-board.txt`:

```
  -1 |    MMMMMMMMMMMMMMMM    |     M = the neutral bar, sixteen cells
   1 |          NNNN    OOOO  |     N = the build zone that reaches it, four
```

Sixteen against four is the whole of a dead landform, visible at a glance and invisible in the render
that was actually looked at. `specs/opus5-wheal-hazel-v2/renders/00-board.txt` is
the same two rows agreeing.

## `column-probe.cs` and `build.cs` · `world-build.cs`

`column-probe.cs` is the scriptable column read; `pgm-studio`'s
`tools/PgmStudio.RoundTrip --column <regionDir> <x> <z> …` answers the same question and needs no build here.
`build.cs` and `world-build.cs` are the C# drivers two earlier runs wrote, kept as the record of how those
maps were made. **New work uses `drive.py`.** `drive.ps1` was a seventh driver pointed at a port nothing
serves any more and is gone.

## `sculpt/` and `render/` — structures built out of the layer system

`sculpt/` writes sketch documents that hold things which are not terrain, and `render/` takes their picture.
The account of what they are for and what they found is
[SCULPTING-WITH-LAYERS.md](../SCULPTING-WITH-LAYERS.md); this is the file map.

| File | Is |
|---|---|
| `sculpt/props.py` | parametric structures emitted as **sketch shapes** — `ring_wall`, `ellipse_wall`, `dome`, `spire`, `ziggurat`, `arch`, `colonnade`, `tapered_tower`, `bowl`, `crenellated_wall`, `drum_tower`, and `gatehouse` — a composite of five of them, which is the shape a stamper in the tool would have. Eight of the nine are one layer, and what lands in the document is circles and polygons an author can still drag |
| `sculpt/solid.py` | the modelling kit: a solid is a membership test plus its own box. Boxes, ellipsoids, cylinders (upright and laid down), frusta, tori, capsules, half-spaces; plans and side profiles extruded along any axis; revolves about the vertical (`revolve`) **and about the north-south axis** (`revolve_z`, which is what a fuselage or a nacelle is); `tube`, a radius swept along a 3-D polyline, and `sheet`, a plan outline lifted onto a surface — the two a creature needs and nothing else does; union / intersect / difference / shell; translate, mirror, rotate |
| `sculpt/layers.py` | the compiler — a `{(x, y, z): material}` model into layers, by **run index**: per column, maximal runs of one material, and the *n*-th run of every column onto layer *n*. Nothing contests anything, so `SK9` and `SK10` stay silent |
| `sculpt/models.py` | the nine sculptures — robot, droid, Rubik's cube, hooded statue, coupe, walker, dragon, starship, ring station |
| `sculpt/board.py` | the themes (`solid`, `shaded`), the document, the minimal intent an export needs, and the calls that store a board, read its columns back and unzip its world |
| `sculpt/gallery_forms.py` · `gallery_sculpture.py` | the two boards in `sculpture/`, each printing what it cost in layers and shapes and exporting a world into the directory named as its second argument |
| `sculpt/make_board.py` | writes `specs/opus5-automaton`'s plan and finish, props and all, for `drive.py` to build |
| `render/png.py` | a PNG writer, a scanline polygon fill and a 5×7 face, in the standard library alone |
| `render/iso.py` | isometric, **x-ray isometric**, orthographic elevation and one-panel-per-layer renders off `POST …/sketch/columns` — the built world, not the drawing. `drive.py` writes two isometrics per spec, so every board has a picture in the round, and two x-rays where the board holds a covered space. `cavities` beside them is the read on its own: every roofed void, its cell count, the blocks it lies between, and whether anything can walk into it |
| `render/preview.py` | the same isometric taken straight off a model's voxels, for correcting a proportion without a build |

The studio's own 3-D preview is WebGL in the browser, so there is no way to take a picture from it; these
read the column payload the preview meshes and draw it server-side.

## `styles/`

One `HouseStyle` snapshot per file, referenced from a finish as `"@<name>"`. Fork a shipped preset rather
than writing one from nothing: `GET /room-styles/{id}/json` answers the ten presets as the stamper's own JSON
once `dotnet run tools/seed-library.cs` has seeded them. Repaint `storeys[*].wall` as well as `wall`, or the
fork is half applied — except on `Stilts`, whose idiom lives in storey 0's wall.
