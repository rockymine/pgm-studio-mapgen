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

Then one read that raises no finding at all and is printed anyway: **`GET …/coverage`**, the reached /
decorated / dead shares and the five largest dead patches with their coordinates. Every gate in the four
places above asks whether ground is *reachable*; this is the only read that asks whether any journey
**goes there**, and a board can pass all four while carrying a third of its ground unused
(`GENERATION-NOTES.md` §18 — run 4's own `wheal-hazel` did). It refuses nothing, so it is on the driver to
put the number where an author sees it.

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
build — which is where most of a board's shape is actually decided. `--force` passes `?force=true` to
`sketch/from-plan`, accepting the loss of a relief the recompile would orphan (`SK1`).

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
