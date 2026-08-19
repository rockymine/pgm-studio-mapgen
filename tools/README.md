# tools/ — the one driver, and the two probes beside it

## `drive.py` — a plan and a finish, through the API, to a world

```bash
python3 tools/drive.py specs/<slug> "<Map Name>" --out <worlddir> [--force] [--dry]
```

`PGM_STUDIO_API` overrides the endpoint (default `http://localhost:7894/api`).

`specs/<slug>/` holds exactly two authored documents, both named after the directory:

| File | Is |
|---|---|
| `<slug>.plan.json` | a `PlanModel` — the board as cell rectangles, the objectives, the walls |
| `<slug>.finish.json` | everything a plan cannot state, keyed onto the layout the plan compiles to |

The driver writes two more beside them — `<slug>.layout.json` and `<slug>.intent.json`, the documents it
actually posted — so a review reads what was built rather than what was asked for.

### What the finish carries

| Key | Is |
|---|---|
| `themeById` · `themeByHeight` | the theme a compiled shape paints with, by its id or by the height it stands at. The id is the reliable one: compile once, read the ids off `POST /plan/compile`, and key on them. Two pieces at one height fuse into one shape and a height key cannot tell them apart |
| `shapePropsById` · `shapePropsByHeight` | any field merged onto a compiled shape — `relief_scope`, `controls`, `anchor_heights`, `height_mode` |
| `addShapes` | authored `SketchShape`s appended to the first island: the subtracts, the erected shapes, the ramps, the path-shape causeways |
| `relief` | `{"<islandId>": {...}}`, or `{"*": {...}}` for every island. A compiled board's islands are `team` and `neutral` |
| `themes` · `mapTheme` | the theme registry and the map default (the first key unless stated) |
| `roomStyles` | `{"cage": …, "spawn": …}`; a `"@name"` string loads `tools/styles/<name>.json` |
| `dressing` | `{"props": [...]}`; a house prop's `style` takes the same `"@name"` |
| `authors` | `["Opus 5"]`, or `[{"name": …, "uuid": …, "role": …, "contribution": …}]`. PGM takes a person as an **account or a pseudonym**: a bare name writes `<author>Opus 5</author>`, a uuid writes `<author uuid="…"/>` with the name as a sibling comment, and a pseudonym may still carry a `contribution` |
| `voidEnforcement` | `true` patches `intent.build.voidEnforcement`, with `voidExclusions` for the rects to spare |

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

It reads the **stored** plan, so it answers from `PUT …/plan` onward — which is where the driver prints it,
downsampling only when the board comes back wider than a screen. Before a map row exists, `board.py` below is
the same idea off the plan file itself.

### What it prints, and why that is the point

It composes nothing and validates nothing. What it does that the six drivers before it did not is **print
every finding the pipeline raises, with its rule id**, at the four places one can appear:

1. **before a map row exists** — `POST /plan/evaluate` (score, `valid`, the hard/soft terms and the whole lint
   table) and `POST /plan/inspect` (`goalDistances` against `GO1`'s 3.0–4.0 band, `islandGaps` against
   `CT12`'s 15–40, the wall rects, the frontline runs);
2. **at the compile** — `POST /plan/compile`'s `warnings`, and its 422 findings if it refuses;
3. **at the sketch** — `PUT …/sketch/from-plan`'s `SK3`/`SK4`/`SK5`, and `relief/read`'s per-island cells,
   low, high and symmetry error;
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
  carrying a third of its ground unused (`GENERATION-NOTES.md` §18 — run 4's own `wheal-hazel` did). Where a
  board has no two waypoints to join it says so rather than printing nothing, because silence there reads as
  "nothing dead" and means "never measured".

The flow and the coverage are the same question at two ends of the pipeline: flow says *why* ground will go
unused while the board is still rectangles, coverage says *that* it did once a world exists to measure.

A refusal stops the run rather than being skipped. **A refusal is a fault to fix, not a step to work around.**

Two things it deliberately does not do. It never computes a placement, a clearance or a sampler — that is the
capability the run rules keep out of `tools/` — and it never retries a refused call with a different
document. Both of those are the author's.

### The order that matters

`PUT …/intent/from-plan` comes **before** the decline read and **before** the metadata PATCH, and neither is
an accident. The intent is what carries the spawn doors and the goal rings `DR-KEEP` reads, and storing it
projects the map document from the intent's own `meta` — which a compiled intent leaves empty, so an author
name written earlier is overwritten. `GENERATION-NOTES.md` §17 measures both.

### The two escape hatches

`--dry` stops after the evaluator and the inspect feed, so a plan can be iterated with no map row and no
build — which is where most of a board's shape is actually decided. The grid and the flow read the *stored*
plan and so are not in a dry pass; `board.py` covers the grid half of that loop. `--force` passes `?force=true` to
`sketch/from-plan`, accepting the loss of a relief the recompile would orphan (`SK1`).

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

Run 4's own worked example is one line of it. In `maps/opus5-wheal-hazel/renders/00-board.txt`:

```
  -1 |    MMMMMMMMMMMMMMMM    |     M = the neutral bar, sixteen cells
   1 |          NNNN    OOOO  |     N = the build zone that reaches it, four
```

Sixteen against four is the whole of a 60%-dead landform, visible at a glance and invisible in the render
that was actually looked at (`GENERATION-NOTES.md` §18). `maps/opus5-wheal-hazel-v2/renders/00-board.txt` is
the same two rows agreeing.

## `column-probe.cs` and `build.cs` · `world-build.cs`

`column-probe.cs` is the scriptable column read; `pgm-studio`'s
`tools/PgmStudio.RoundTrip --column <regionDir> <x> <z> …` answers the same question and needs no build here.
`build.cs` and `world-build.cs` are the C# drivers two earlier runs wrote, kept as the record of how those
maps were made. **New work uses `drive.py`.** `drive.ps1` was a seventh driver pointed at a port nothing
serves any more and is gone.

## `styles/`

One `HouseStyle` snapshot per file, referenced from a finish as `"@<name>"`. Fork a shipped preset rather
than writing one from nothing: `GET /room-styles/{id}/json` answers the ten presets as the stamper's own JSON
once `dotnet run tools/seed-library.cs` has seeded them. Repaint `storeys[*].wall` as well as `wall`, or the
fork is half applied — except on `Stilts`, whose idiom lives in storey 0's wall.
