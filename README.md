# pgm-studio-mapgen

Composed worlds and the configuration that produced them. Each map here was authored through
[pgm-studio](https://github.com/rockymine/pgm-studio) and is committed whole — `region/`, `level.dat`
and `map.xml` — so it can be pulled straight onto a machine with Minecraft and loaded without
rebuilding anything.

```
maps/<slug>/region/*.mca   the world
maps/<slug>/region/provenance.json   what each pass placed, and (since B139) which prop placed it
maps/<slug>/level.dat
maps/<slug>/map.xml        what a PGM server loads
maps/<slug>/renders/       the images the map was reviewed from, stage by stage
specs/<slug>/              the documents that were authored — plan, layout, intent, themes, styles, dressing
review/<slug>.md           the measured record for that map
reports/<model>-runN.md    one agent run: what it could not say, what it got wrong, what worked
tools/                     the drivers that post those documents to the API
```

A map's `specs/` are the whole of what was authored; the world is derived from them and is committed as
the artifact rather than as a source. Rebuilding one needs a running pgm-studio API and a migrated
database.

**Start with [GENERATION-NOTES.md](GENERATION-NOTES.md).** It is the errata an author needs beside
`pgm-studio/docs/tools/` — the fields a hand-authored shape needs before it exists at all, the two
different rules height and paint use to resolve an overlap, Bézier control semantics, and the traps that
have each cost a build cycle.

## Maps

Grouped by the run that produced them. Mode is what the map's own `<gamemode>` declares.

### Hand-authored, before the trial runs

| Folder | Mode | What it is |
|---|---|---|
| `clayclay_redux` | ctw | A recreation of `CommunityMaps/ctw/clayclay` — two rot_180 plus-shaped clay islands joined by four void hops. See [FINDINGS.md](FINDINGS.md). |
| `ashen_quarry` | ctw* | Authored from a sketch: a walled town on a raised polygon, a 17-deep quarry the destroyable stands in, a tilted mesa, one interlocking landmass. |

### B120 run 1

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `quillon-barrow` | ctw* | Opus | the canonical brief — a chalk heath, barrow in the open, wood west, crag east, village behind, channel in front |
| `quillon-saltworks` | ctw | Opus | a capture board on a salt pan, quartz pans stepping down to the brine |
| `quillon-foundry` | ctw* | Opus | a core and a stack on a red hillside |
| `sonnet-holdfast` | ctw* | Sonnet | the canonical brief |
| `sonnet-briarlock` | ctw | Sonnet | a CTW map of its own design |
| `sonnet-cinderreach` | ctw* | Sonnet | a destroy-core map of its own design |
| `haiku-canonical-destroy-3` | ctw* | Haiku | the canonical brief |
| `haiku-ctw-rush-2` | ctw | Haiku | a CTW board |
| `haiku-dtm-tower` | ctw* | Haiku | a DTM board with dual objectives |

### Fable run 3

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `firnline` | dtm | Fable | snow-and-mountains lane: a firn valley between built terraces, crevasse pockets, obsidian cairn on a forecourt shelf |
| `kerbstone` | dtm | Fable | cityscape street canyon: multi-storey rows, marching and projecting wings, gold bullion on a civic court |
| `sunspit` | ctw | Fable | summer beach: two shores over an open sea gap, lagoon, walled bluff wool + isolated pier wool, tidal water lane |
| `tanglewold` | ctw | Fable | woodlands: forest belts and brooks, a walled knoll wool + a donut hollow wool, causeway mid over two fords |

### B120 run 2

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `tallow-mirefast` | dtm | Opus | the canonical brief, built |
| `tallow-weirgate` | ctw | Opus | a capture board on a drained reservoir |
| `tallow-kilnrow` | dtm dtc | Opus | a destroy board on a lime works |
| `corvid-hollow` | dtm | Sonnet | the canonical brief |
| `sable-marsh` | ctw | Sonnet | a CTW board |
| `ashfall-scar` | dtm dtc | Sonnet | a DTC + DTM board |
| `marlstone-steps` | ctw | Opus 5 | a white marl hillside in five terraces cut by two void ravines, four tilted ramps joining them |
| `basalt-reach` | dtm dtc | Opus 5 | a black basalt platform with sea stacks, cut by a `subtract` channel; permanent void with no build zones |
| `haiku-r2-canonical-8` | — | Haiku | **not a map** — see below |
| `haiku-r2-ctw-mid` | — | Haiku | **not a map** — see below |

**`*` — the mode is wrong, and the map is not.** Every board marked `ctw*` is a destroy board whose
`map.xml` says `ctw`, because it was built before `MetaGenerator` learned to derive `<gamemode>` and the
objective line from the objective modules the intent actually carries. Boards built after that fix declare
`dtm`, `dtc` or `dtm dtc` correctly. Nothing about those worlds is wrong; only the label is, and rebuilding
them against the current studio would correct it.

**Two folders in run 2 contain no map.** `haiku-r2-canonical-8` and `haiku-r2-ctw-mid` export a 245-byte
`map.xml` with no teams, no spawns and no objectives — `<objective></objective>`, empty `<version>` — over
region files that are largely empty. They are kept because they are evidence, not because they are playable:
they are what `pgm-studio`'s own `d911cefe` names, *"a map with nothing on it satisfies every refusal the
pipeline has"*. Neither is mentioned in `reports/haiku-run2.md`. **Do not load them.**

**A recreation never reuses the original's name.** Both the folder and the `<name>` in `map.xml` carry a
suffix, because a PGM server loading this repo alongside the community corpus would otherwise see two maps
calling themselves the same thing. The name lives in the plan document's `meta.name`, which is what the
compile reads — changing the folder alone is not enough.

## Looking at a map without Minecraft

Every map carries `renders/`. Two of them answer questions no plan view can:

- **`--topdown --layer structure`** reads `region/provenance.json` and draws what the build *recorded* itself
  placing. Its owners list is a literal census of your dressing:

  ```powershell
  $j = Get-Content maps/<slug>/region/provenance.json -Raw | ConvertFrom-Json
  $j.owners | Group-Object { ($_ -split ':')[0] }
  ```

  Prefer it to `--buildings`, which finds buildings by scanning block materials and is built for worlds the
  studio did **not** build — `GENERATION-NOTES.md` §6 has the three ways it misreads one that it did.

- **`--section`** and **`--column`** are the only reads that keep Y. A riser, a ramp's step heights, a
  stamped room's floor and a goal's clearance are none of them visible from above.

## How a report separates a claim from a limitation

**A report says what the model reported, what the code actually allows, and which of the two the reader
should believe.** An agent's account of what it could not do is evidence about the *surface*, not about the
system, and the two have already diverged badly: a run reported five of six brief requirements as impossible
while quoting the documentation that describes two of them, and a later one reported per-shape themes and
area relief marks as missing when both are shipped and in use on maps in this repository.

So every "could not do" entry carries three parts, and an entry missing the third is not finished:

| Part | Is |
|---|---|
| **Reported** | what the model believed, in its own words, including the reasoning that led there |
| **Checked** | what the code and documents actually say — the type, the field, the endpoint, read at the source |
| **Verdict** | **missing** (no mechanism exists) · **unreachable** (it exists and the surface hid it) · **mistaken** (it exists, was documented, and the model did not find it) |

Only **missing** is a capability gap. **Unreachable** is a surface defect and belongs as a task against the
studio. **Mistaken** is the most valuable of the three and the easiest to bury, because it reads as a
limitation and is really a measurement of how legible the system is — and a report that quietly drops its
mistaken entries destroys exactly the signal the run exists to produce.

A verdict is not the model's to award on its own claim. It is settled by reading the code, and the reading is
cited.

## Reports

| File | Is |
|---|---|
| [GENERATION-NOTES.md](GENERATION-NOTES.md) | what an author has to know that is not written down — read before authoring |
| [FINDINGS.md](FINDINGS.md) | the measured record of the ClayClay recreation, per review round |
| [AGENT-REPORT.md](AGENT-REPORT.md) | tracing an existing map: why the `mapgen` spec was the wrong layer, and two claims it got wrong |
| [AGENT-REPORT-2.md](AGENT-REPORT-2.md) | authoring a board from nothing: the height model, the three scripts that should not have needed writing, the void column nothing checked for |
| `reports/opus-run1.md` · `sonnet-run1.md` · `haiku-run1.md` | the three run-1 accounts |
| `reports/opus-run2.md` · `sonnet-run2.md` · `haiku-run2.md` | the three run-2 accounts |
| [reports/opus5-run2.md](reports/opus5-run2.md) | a second, independent run-2 — its §1 audits the earlier runs' claims against the code, and finds three that were wrong when filed and four gaps since closed |
| [reports/fable-run3.md](reports/fable-run3.md) | run 3 — four themed boards; five studio defects found were fixed in the same session, and the fault table separates them from the author's own mistakes |
| `review/` | one measured record per map |

**Two files are both "Opus, run 2" and they are different runs.** `opus-run2.md` is the cloud agent that
authored the `tallow-*` boards; `opus5-run2.md` is a separate local run that authored `marlstone-steps` and
`basalt-reach`. They were written against the same studio revision without knowledge of each other, which
makes the places they agree worth more than either alone — and they do agree, independently, that Haiku's
per-shape-theme and area-relief-mark claims were mistaken.
