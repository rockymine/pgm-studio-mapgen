# pgm-studio-mapgen

Composed worlds and the configuration that produced them. Each map here was authored through
[pgm-studio](https://github.com/rockymine/pgm-studio) and is committed whole — `region/`, `level.dat`
and `map.xml` — so it can be pulled straight onto a machine with Minecraft and loaded without
rebuilding anything.

```
maps/<slug>/region/*.mca              the world
maps/<slug>/region/provenance.json    what each pass placed, and which prop placed it
maps/<slug>/level.dat
maps/<slug>/map.xml                   what a PGM server loads
maps/<slug>/renders/                  the images the map was reviewed from, stage by stage
specs/<slug>/                         the documents that were authored — plan, finish, layout, intent
review/<slug>.md                      the measured record for that map
reports/<model>-runN.md               one agent run: what it could not say, what it got wrong, what worked
tools/                                the driver that posts those documents to the API
```

A map's `specs/` are the whole of what was authored; the world is derived from them and is committed as
the artifact rather than as a source. Rebuilding one needs a running pgm-studio API and a migrated
database.

## Authoring a map here

**Two documents, and the API.** [AUTHORING-BRIEF.md](AUTHORING-BRIEF.md) is what an authoring agent is
given, end to end. [GENERATION-NOTES.md](GENERATION-NOTES.md) is what the API cannot state about itself —
a fact about how two correct mechanisms interact, a number no gate checks, a read-back that lies.

Everything else comes from the studio, which describes itself: `GET /api/openapi/v1.json` is every route
with its request, its answer and the failure codes it declares; `GET /api/rules` is every rule id with what
it means and how to fix it; and every answer carries its own findings — a refusal under `findings`, a
success under `warnings`. A hand-written capability list would be a copy free to disagree with the running
system, so there is not one.

**One agent authors a board.** There is no reviewer agent and no art-direction agent. Feedback on a board
comes from the repository's author.

## Maps

Grouped by the run that produced them. Mode is what the map's own `<gamemode>` declares.

### The first experiment — fifteen boards, worlds only

Fifteen boards were built on 11–12 August 2026, each from a single JSON spec. The spec form itself was a day
old and there was nowhere to commit one, so only the world was saved: none of the fifteen has `specs/`,
`provenance.json`, `renders/` or `review/`, and none is recoverable.

Fourteen are here. The fifteenth, `thornwake`, was accepted into `CommunityMaps/ctw` and lives there instead;
`hk1_viridian` below is the pre-merge draft of the board that went upstream with it as `CommunityMaps/ctw/viridian`.

**What they proved is visible in the files.** Every one of the nine destroy boards declares
`<gamemode>ctw</gamemode>` while carrying no wool at all — the objective kind a board is played for could
not yet be stated. That, and the houses standing inside one another, are what the spec format was written
against. These survive as evidence rather than as examples.

**Capture the wool**

| Folder | Author | What it is |
|---|---|---|
| `emberfall` | Opus 5 | four wools over cinder terraces |
| `ridgeway` | Opus 5 | a cliff splitting each side, a high road and a low one |
| `saltmarch` | Opus 5 | a flat open crossing with nowhere to hide |
| `hk1_viridian` | Haiku 4.5 | a jungle board, two wools — draft of upstream `viridian` |
| `hk2_crystalline_quarry` | Haiku 4.5 | ice caverns, twelve wools, four teams under `rot_90` |

**Destroy the monument, and monument with core** — all nine mis-declare `ctw`

| Folder | Objective | Author | What it is |
|---|---|---|---|
| `cinderreach` | monument | Opus 5 | burnt ground, one monument each |
| `hollowmere` | monument | Opus 5 | each monument over a sunken basin |
| `ironhold` | monument | Opus 5 | one rock, two keeps, no way round |
| `verdigris` | monument | Opus 5 | a copper hall gone green, under `mirror_z` |
| `hk1_glacial` | monument | Haiku 4.5 | frozen monuments on an icy plateau |
| `goldhollow` | monument + core | Opus 5 | two of each, open sand between them |
| `mourncrag` | monument + core | Opus 5 | one of each apiece, on frozen rock |
| `spinebreak` | monument + core | Opus 5 | one long 145×420 ridge, an objective at each end |
| `hk2_obsidian_keep` | monument + core | Haiku 4.5 | one of each, behind the walls of the keep |

Beside them sits one world from the same days that is not one of the fifteen:

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `pattern_test` | — | studio | twenty-five plateaus built to look at terrain patterns, not to be played; superseded by `library_map` from `pgm-studio/tools/library-map.cs` |

### Hand-authored, before the trial runs

| Folder | Mode | What it is |
|---|---|---|
| `clayclay_redux` | ctw | A recreation of `CommunityMaps/ctw/clayclay` — two rot_180 plus-shaped clay islands joined by four void hops |
| `ashen_quarry` | ctw* | Authored from a sketch: a walled town on a raised polygon, a 17-deep quarry the destroyable stands in, a tilted mesa, one interlocking landmass |

### Run 1

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `quillon-barrow` | ctw* | Opus | a chalk heath, barrow in the open, wood west, crag east, village behind, channel in front |
| `quillon-saltworks` | ctw | Opus | a capture board on a salt pan, quartz pans stepping down to the brine |
| `quillon-foundry` | ctw* | Opus | a core and a stack on a red hillside |
| `sonnet-holdfast` | ctw* | Sonnet | a destroy board |
| `sonnet-briarlock` | ctw | Sonnet | a CTW map of its own design |
| `sonnet-cinderreach` | ctw* | Sonnet | a destroy-core map of its own design |
| `haiku-canonical-destroy-3` | ctw* | Haiku | a destroy board |
| `haiku-ctw-rush-2` | ctw | Haiku | a CTW board |
| `haiku-dtm-tower` | ctw* | Haiku | a DTM board with dual objectives |

### Run 3 — Fable

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `firnline` | dtm | Fable | snow-and-mountains lane: a firn valley between built terraces, crevasse pockets, obsidian cairn on a forecourt shelf |
| `kerbstone` | dtm | Fable | cityscape street canyon: multi-storey rows, marching and projecting wings, gold bullion on a civic court |
| `sunspit` | ctw | Fable | summer beach: two shores over an open sea gap, lagoon, walled bluff wool + isolated pier wool, tidal water lane |
| `tanglewold` | ctw | Fable | woodlands: forest belts and brooks, a walled knoll wool + a donut hollow wool, causeway mid over two fords |

### Run 2

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `tallow-mirefast` | dtm | Opus | a destroy board on a mire |
| `tallow-weirgate` | ctw | Opus | a capture board on a drained reservoir |
| `tallow-kilnrow` | dtm · dtc | Opus | a destroy board on a lime works |
| `corvid-hollow` | dtm | Sonnet | a destroy board |
| `sable-marsh` | ctw | Sonnet | a CTW board |
| `ashfall-scar` | dtm · dtc | Sonnet | a DTC + DTM board |
| `marlstone-steps` | ctw | Opus 5 | a white marl hillside in five terraces cut by two void ravines, four tilted ramps joining them |
| `basalt-reach` | dtm · dtc | Opus 5 | a black basalt platform with sea stacks, cut by a `subtract` channel; permanent void with no build zones |
| `haiku-r2-canonical-8` | — | Haiku | **not a map** — see below |
| `haiku-r2-ctw-mid` | — | Haiku | **not a map** — see below |

### Run 4 — Opus 5, four boards, one per objective shape

Authored to record how a model actually drives the studio, so the account of the loop is the deliverable and
the boards are its evidence. All four build with nothing declined.
[reports/opus5-run4.md](reports/opus5-run4.md) is the run.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-wheal-hazel` | ctw | Opus 5 | a granite tin works either side of a shingle bar: a walled wool lane at the head of each valley, a raised leat over a flooded shaft, a tidal lane that opens on the flank at 45 minutes |
| `opus5-wheal-hazel-v2` | ctw | Opus 5 | the same board with its neutral bar cut to the width of the build zone that reaches it. **27.2% dead ground → 0.8%**, on the same four gates passing identically both times |
| `opus5-alabaster-rake` | dtm | Opus 5 | a gypsum badland under a bone-white mesa — three approaches in three dimensions: a weave through a picket of banded hoodoos, a drop into a sunk hollow, a climb up a tilted shelf |
| `opus5-siderite-bowl` | dtc | Opus 5 | an impact crater whose ejecta ring stands **behind** the bowl, so the defence looks down into its own goal and the attack arrives from below |
| `opus5-hollowbank` | ctw · dtm | Opus 5 | a chalk ring-fort carrying **both** objective kinds — the wool in a keep off the enclosure, the beacon out on the inner rampart |

### Run 4 — Sonnet

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `sonnet-compass` | ctw | Sonnet | **the first four-team board here** — `rot_90`, four spawns, twelve wools, a walled yard around a centre nobody owns |
| `sonnet-caravanserai` | dtm | Sonnet | **the first desert here** — a red-rock canyon with a walled caravan stop, `HousePresets.Desert` forked by proportion alone |
| `sonnet-gantry` | dtc | Sonnet | an industrial yard: **two cores a team** on a raised deck and in a sunk pit, and six hand-placed buildings, no two the same size |
| `sonnet-reedcut` | ctw | Sonnet | a worked peat lowland read by height rather than colour, with a water lane confirmed reaching `map.xml` |

### Run 4 — Haiku, four blueprints, honestly labelled

All four load — teams, spawns, objectives and an author over real region files — and **none carries a theme
registry, a placed prop, an authored relief or a single render**. Every shape on all four names a theme the
layout does not carry, which is the silence `SketchLayoutCheck` was extended to report. `haiku-wharf` answers
a capture brief with no wool on it. They are kept as what they are: plan-level blueprints, and the run's own
report lists every one of these under *what could not be done*.

`haiku-chancel` · `haiku-ladder` · `haiku-wharf` · `haiku-winterfold`

### Grok run 1 — authored blind, built afterwards

Three maps written by Grok from the documentation alone, with **no running studio**: nothing it wrote was ever
posted, compiled or exported by its author. They were driven through the endpoints for the first time here.
Two of the three plans were refused for cell arithmetic and fixed with four rect edits; every layout document
rasterized to no ground; the dressing was authored in plan cells rather than blocks.
[reports/grok-run1.md](reports/grok-run1.md) is what each document did, and
[reports/grok-experience.md](reports/grok-experience.md) is Grok's own account, written before any of it was
run. Each map's `specs/<slug>/authored-by-grok/` holds the original documents verbatim.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `grok-ridge` | ctw | Grok | three terraces and a crest, a wool room off each side, a mid build band, one approach wall at the gate seam |
| `sandscar` | dtm | Grok | one plateau a team, two monuments 50 apart, a hollow under one and a hill under the other, a river dragged across as a paved path |
| `sandscar-complex` | dtm | Grok | a height progression from a river front to a dug pit and a climbed hill, both carrying a monument, savanna crest behind |

### Opus 5 — Elderwold and Hoarstone

Two boards authored from a brief rather than a spec, the second after review of the first.
[reports/opus5-elderwold-run.md](reports/opus5-elderwold-run.md) ·
[reports/opus5-hoarstone-run.md](reports/opus5-hoarstone-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-elderwold` | dtm | Opus 5 | a wooded island cut by a river with one paved ford: an endstone cairn on a flat shelf scarped on its attack face, a three-step sunken hollow west, an oak wood east, a cottage on a knoll with a track up to it. **One terrain shape, 24 vertices**; sixteen relief marks and three pushes; one theme, with five wide path props used as a texturing brush |
| `opus5-hoarstone` | dtm | Opus 5 | a frozen archipelago — one island a team, three neutral rocks between them — carrying **thirteen erected monoliths** in three palettes the ground is not made of, six of them a ring on the middle island. Snow over exposed stone, template spruce, and four house plans: an L, a T, a U and a single range, each with its own roof form and storey stack |



### Opus 5 — authored to record the method

Boards authored end to end with the process written down rather than the result:
[reports/opus5-coldharbour-authoring.md](reports/opus5-coldharbour-authoring.md) is every request, which
documents were hand-written and which assembled by script, which previews were looked at before building, and
the two places in the whole build where the source was the only oracle.
[reports/opus5-coldharbour-v2-authoring.md](reports/opus5-coldharbour-v2-authoring.md) is the second pass
after review, and [reports/opus5-quernstone-authoring.md](reports/opus5-quernstone-authoring.md) is the
four-team board built from that vocabulary at `rot_90`.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `coldharbour` | ctw | Opus 5 | a chalk down: two wool rooms a team placed against each other, one behind a cut pit down a sunken lane, one on an open shelf with a water lane that opens late; permanent 20-block channels in the frontline |
| `coldharbour_v2` | ctw | Opus 5 | the same ground rebuilt to the model's own shapes after review: a U frontline off a double-hole hub, an L wool lane and an I wool lane, one neutral stone in the middle, a stream across the spine. 207 ground cells against v1's 533 |
| `quernstone` | ctw | Opus 5 | **four teams**, `rot_90`: the same vocabulary pinwheeled — each team a wedge whose frontline straddles the axis, four images abutting into a plus mid around one neutral millstone. 216 × 216, 8 wool rooms, 4 walls |
| `thunder-series` | — | Opus 5 | see [reports/opus5-thunder-series.md](reports/opus5-thunder-series.md) |

## Three caveats about what is committed here

**`*` — the mode is wrong, and the map is not.** Every board marked `ctw*` is a destroy board whose `map.xml`
says `ctw`, because it was built before `MetaGenerator` learned to derive `<gamemode>` and the objective line
from the objective modules the intent actually carries. Nothing about those worlds is wrong; only the label
is. `ctw` is a valid `Gamemode` id, so these boards load.

**Three boards did not load at all, and are now corrected by hand.** PGM parses `<gamemode>` as a **repeated**
element holding one id each, against a **closed 25-value enum**, with no splitting:
`MapInfoImpl.parseGamemodes` throws `InvalidXMLException("Unknown gamemode")` on `<gamemode>dtm dtc</gamemode>`
and the map does not load. Across ~350 corpus maps every `<gamemode>` holds exactly one id and maps with
several repeat the element (`cacti_the_wool` carries six). `tallow-kilnrow`, `ashfall-scar` and `basalt-reach`
now repeat the element and parse.

**Two folders in run 2 contain no map.** `haiku-r2-canonical-8` and `haiku-r2-ctw-mid` export a 245-byte
`map.xml` with no teams, no spawns and no objectives, over region files that are largely empty. They are kept
because they are evidence, not because they are playable — a map with nothing on it satisfies every refusal
the pipeline had at the time. **Do not load them.**

**A recreation never reuses the original's name.** Both the folder and the `<name>` in `map.xml` carry a
suffix, because a PGM server loading this repository alongside the community corpus would otherwise see two
maps calling themselves the same thing. The name lives in the plan document's `meta.name`, which is what the
compile reads — changing the folder alone is not enough.

## Looking at a map without Minecraft

Every map carries `renders/`. Two reads answer questions no plan view can:

- **`--topdown --layer structure`** reads `region/provenance.json` and draws what the build *recorded* itself
  placing. Its owners list is a literal census of the dressing — every count reads `units × orbit order`, so
  a prop that landed nothing has no row at all:

  ```python
  import json; from collections import Counter
  p = json.load(open('maps/<slug>/region/provenance.json'))
  print(Counter(o['kind'] for o in p['owners']))
  ```

  Beside it, `region/dressing-report.json` answers what did **not** land, and is written only when something
  dropped — so its absence means everything authored stood.

- **`--section`** and **`--column`** are the only reads that keep Y. A riser, a ramp's step heights, a
  stamped room's floor and a goal's clearance are none of them visible from above.

## Reports

`reports/` holds one account per run and `review/` one measured record per board. Both are **dated accounts**:
each describes the studio and the documents as they were on the day it was written, and several name briefs
that have since been retired. They are kept as the record of what was found, not as instruction — an
authoring agent reads `AUTHORING-BRIEF.md` and the API.

**A report separates a claim from a limitation.** An agent's account of what it could not do is evidence about
the *surface*, not about the system, and the two have diverged badly: a run reported five of six requirements
as impossible while quoting the documentation that describes two of them, and a later one reported per-shape
themes and area relief marks as missing when both are shipped and in use on maps here. So every
"could not do" entry carries three parts, and one missing the third is not finished:

| Part | Is |
|---|---|
| **Reported** | what the model believed, in its own words, including the reasoning that led there |
| **Checked** | what the code and the schema actually say — the type, the field, the endpoint, read at the source |
| **Verdict** | **missing** (no mechanism exists) · **unreachable** (it exists and the surface hid it) · **mistaken** (it exists, was documented, and the model did not find it) |

Only **missing** is a capability gap. **Unreachable** is a surface defect and belongs as a task against the
studio. **Mistaken** is the most valuable of the three and the easiest to bury, because it reads as a
limitation and is really a measurement of how legible the system is. A verdict is not the model's to award on
its own claim: it is settled by reading the code, and the reading is cited.
