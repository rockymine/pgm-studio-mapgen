# pgm-studio-mapgen

Composed worlds and the configuration that produced them. Each map here was authored through
[pgm-studio](https://github.com/rockymine/pgm-studio) and is committed whole — `region/`, `level.dat`
and `map.xml` — so it can be pulled straight onto a machine with Minecraft and loaded without
rebuilding anything.

```
maps/<slug>/region/*.mca              the world
maps/<slug>/level.dat
maps/<slug>/map.xml                   what a PGM server loads
specs/<slug>/                         the documents that were authored — plan, finish, layout, intent
specs/<slug>/renders/                 the images the map was reviewed from, stage by stage
specs/<slug>/provenance.json          what each pass placed, and which prop placed it
review/<slug>.md                      the measured record for that map
reports/<model>-runN.md               one agent run: what it could not say, what it got wrong, what worked
showcase/<nn>-<concept>/              one technique, end to end — documents, world, renders, README
sculpture/                            structures built out of the layer system — the two galleries
tools/                                the driver that posts those documents to the API, the loop beside it, and the world tools
```

**`maps/<slug>/` is what a server is handed and nothing else** — the three things a match reads. Everything
that exists to be *looked at* rather than loaded lives beside the documents in `specs/<slug>/`: the renders,
and the provenance sidecar that says which pass claimed which column. Uploading a map folder to a game server
therefore carries no images and no metadata with it.

A map's `specs/` are the whole of what was authored; the world is derived from them and is committed as
the artifact rather than as a source. Rebuilding one needs a running pgm-studio API and a migrated
database.

## The showcase library

`showcase/` is a teaching set: **one folder per technique**, each a complete map whose
only reason to exist is the one thing its README names. Every one forks the same base board and changes one
thing, so the diff is the lesson — a reader who wants to know how a cliff is stated reads the eleven lines
that state it rather than finding the cliff inside a thousand-line finish. `showcase/README.md` is the index.

`maps/opus5-whinnymoor` is the board they add up to, and `review/opus5-whinnymoor.md` says which showcase
every part of it came from. `maps/opus5-sandcaster` is the destroy board built on top of that: 110 × 400,
three land regions on one hue axis, a chasm down the middle and a tiled service corridor under the reef —
two sketch layers, forty-two brush strokes and two monuments, one of them twenty blocks underground.
`maps/opus5-sandcaster-ii` is the same brief on one open landmass: a mountain range drawn with pushes
round a dale 32 blocks wide, no chasm anywhere, and the workings moved under the middle of it.
`maps/opus5-ravensmere` is the single-layer one: a mere with a group in the middle of it, a beach thirty
blocks deep round that, rolling downs cut by three crevasses, a wood, a brick-and-granite path with
cottages off it, and a range standing behind each spawn. `maps/opus5-thornfell` is the same technique on a
capture board: void down the middle, two wool rooms hung off the back of each half on spurs a raider walks
out along, and a range behind every one of them.

## Sculpting with layers

The sketch tool's layers were built to stack storeys, and they hold rather more than that: a layer is one
arbitrary height field, so a dome is thirteen circles on one layer and a thirty-block statue is eight layers
of rectangles. [SCULPTING-WITH-LAYERS.md](SCULPTING-WITH-LAYERS.md) is the account — the six facts that decide
how far it goes, the four limits, and what could become a tool. `sculpture/` holds the two galleries it was
written from and `maps/opus5-automaton` is a played board furnished with them.

## Authoring a map here

**Two documents, and the API.** [AUTHORING-BRIEF.md](AUTHORING-BRIEF.md) is what an authoring agent is
given, end to end. [GENERATION-NOTES.md](GENERATION-NOTES.md) is what the API cannot state about itself —
a fact about how two correct mechanisms interact, a number no gate checks, a read-back that lies.
[REVAMP-BRIEF.md](REVAMP-BRIEF.md) is the loop after a person has finished a board in game: the two
worlds read against each other, the commands named, the finish restated as documents, and a new board
built with what it taught.

Everything else comes from the studio, which describes itself: `GET /api/openapi/v1.json` is every route
with its request, its answer and the failure codes it declares; `GET /api/rules` is every rule id with what
it means and how to fix it; and every answer carries its own findings — a refusal under `findings`, a
success under `warnings`. A hand-written capability list would be a copy free to disagree with the running
system, so there is not one.

**One agent authors a board.** There is no reviewer agent and no art-direction agent. Feedback on a board
comes from the repository's author.

## Maps

Grouped by the run that produced them. Mode is what the map's own `<gamemode>` declares.

**Most of these specs no longer compile, and that is settled rather than pending (author).** 74 of the 85
plans here state `"plan": 1`, whose marker offsets are in cells where version 2 states them in blocks, so
`POST /plan/compile` refuses one with `PL15`. The worlds under `maps/` were built from them and are what
those boards are; migrating the plans would move every marker on 74 boards to rebuild something already
built. **A version 1 spec is the record of a world, not a thing that rebuilds** — read it, do not re-drive
it, and do not file the migration again.

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
| `clayclay_redux` | ctw | A recreation of `CommunityMaps/ctw/clayclay` — two rot_180 plus-shaped clay groups joined by four void hops |
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

### Run 5 — one board a model, and the brief was a lane rather than a square

Three models, one board each, all three authored to the same instruction the earlier runs had learned:
**a lane, not a square**, because on a square board every goal is equidistant from both spawns and the
walk ratio flattens. Two of the three took the combined destroy shape the corpus calls ordinary — one
destroyable and one core a team, and both boards repeat `<gamemode>` for the pair rather than declaring
one and carrying the other.
[reports/fable-run5.md](reports/fable-run5.md) ·
[reports/haiku-run5.md](reports/haiku-run5.md) ·
[reports/sonnet-run5.md](reports/sonnet-run5.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `fable-r5-whitebarrow` | dtm · dtc | Fable 5.1 | **100 × 190 of chalk down, four stated tiers 9 / 11 / 13 / 15** — the Barrow Stone (obsidian, `pillar-3`) on open turf ringed by sarsens, the Powder Magazine (a default core) sunk in a dell east of it, and the two sides meeting across a saddle that holds a dew pond. Every approach pays a different price: turf and sarsen cover in the open, a beech hanger closing the west flank, and a chalk scarp on the east that is climbed from the mid and bridged from at the top |
| `haiku-r5-hollow-crown` | dtm · dtc | Haiku 4.5 | **100 × 120, and honest about being a test** — two spawns at opposite ends, one central reach piece carrying the objectives, and nothing else. Built to verify that the authoring pipeline and its documentation are followable end to end rather than to be played; its own review names the asymmetric dead ground on the flanks as the cost of that |
| `sonnet-r5-fellgate` | ctw | Sonnet 4.5 | **70 × 350 — the longest lane of the three** — a highland sheep-moor whose two hamlets face each other down a heather track, each guarding a stone bothy behind a **bedrock approach wall**, the banks either side of the mid hollow topped by granite tors. The mid is crossed by a ford at the centre and, forty-five minutes in, by a second flooded lane out on the flank. One connected island: the whole authored half is one landmass fanned whole onto its image |

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

### Opus 5 — a board at a time, each after review of the one before

Twelve boards authored from a brief rather than a spec. The first five are the ground: a drawn
layout, an archipelago, two goals a team, a **composed** layout rather than a drawn one, and an
experiment on the sketch tool's stacked layers. The seven after them push one thing each —
four storeys, a landscape, a composed `donut`, a mesa's strata, a quarry's benches, open sky with
no ground at all, and a labyrinth whose walls are their own slab.
[reports/opus5-elderwold-run.md](reports/opus5-elderwold-run.md) ·
[reports/opus5-hoarstone-run.md](reports/opus5-hoarstone-run.md) ·
[reports/opus5-cairnmeadow-run.md](reports/opus5-cairnmeadow-run.md) ·
[reports/opus5-hollowmarch-run.md](reports/opus5-hollowmarch-run.md) ·
[reports/opus5-undercroft-run.md](reports/opus5-undercroft-run.md) ·
[reports/opus5-interchange-run.md](reports/opus5-interchange-run.md) ·
[reports/opus5-tarnfell-run.md](reports/opus5-tarnfell-run.md) ·
[reports/opus5-rimegarth-run.md](reports/opus5-rimegarth-run.md) ·
[reports/opus5-smallboards-run.md](reports/opus5-smallboards-run.md) ·
[reports/opus5-overwall-run.md](reports/opus5-overwall-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-elderwold` | dtm | Opus 5 | a wooded group cut by a river with one paved ford: an endstone cairn on a flat shelf scarped on its attack face, a three-step sunken hollow west, an oak wood east, a cottage on a knoll with a track up to it. **One terrain shape, 24 vertices**; sixteen relief marks and three pushes; one theme, with five wide path props used as a texturing brush |
| `opus5-hoarstone` | dtm | Opus 5 | a frozen archipelago — one group a team, three neutral rocks between them — carrying **thirteen erected monoliths** in three palettes the ground is not made of, six of them a ring on the middle group. Snow over exposed stone, template spruce, and four house plans: an L, a T, a U and a single range, each with its own roof form and storey stack |
| `opus5-cairnmeadow` | dtm | Opus 5 | an open meadow over three groups, **two destroyables a team**: one on the crown of a stone outcrop, one at the bottom of the cut its stone came out of. Eight irregular crags erected out of the grass at `skirt >= lift`, so they are walked onto rather than climbed, and painted back over with twenty grass brushes so they belong to the ground. One house on the whole board, and it is the spawn's |
| `opus5-hollowmarch` | ctw | Opus 5 | a **composed** board — `hub=double-hole`, `front=twin`, 32 players, seed 1233 — shifted twenty blocks to clear a middle group, then given every height by relief over a flat plan. The spawn and the two wool approaches stand on **`hold` pads pre-raised** so the terrain runs up to meet them; **rim and wall are both off**, so a cliff face is the surface stack and the fill under it. Seven rock crags, each tilted by a **plane through three stated vertices** — flush on its own side, a cliff facing the attack — and a pond on the axis group |
| `opus5-undercroft` | dtm | Opus 5 | a two-level destroy board, and the only one whose subject is a feature: **three sketch layers**, a ground group under a stone terrace twenty blocks over it, and two bridge slabs across the strait. The monument stands on the terrace because a placement snaps to the surface top; the ground it covers survives as a **nine-block hall**, which no 2-D read can see. |
| `opus5-interchange` | dtm | Opus 5 | a liminal board built to an outside brief: a transit interchange on **four storeys** — a drained swimming pool under the concourse, a catwalk in the stairwell, an empty car deck twenty blocks over it — carrying **five obsidian monuments a team**, one to each storey and each in its own colour. A corridor of doors that rings a sealed core, a spine that crosses the garden court behind glass without opening onto it, and the same kiosk in all nine rooms |
| `opus5-tarnfell` | dtm | Opus 5 | a landscape rather than a board: a lobed tarn with a green islet in it, a wide sand shore, rolling fell, a forest, four void crevasses and a mountain backdrop that **runs off all four edges**. Thirty-three relief marks, four of them traced past the coast so the frame cuts a mountainside instead of ground decaying to base; every height above the rock is a **brush stroke** along the crest, and every seam between two grounds is two `worn` strokes freckling into each other. One `cube-4` endstone wardstone a team, 30 right and 50 ahead of spawn, 150 apart |
| `opus5-rimegarth` | ctw | Opus 5 | **the plan was composed, not drawn** — `GET /api/compose?players=10&seed=26` pinned verbatim, picked off two contact sheets of ninety-six seeds for the one shape in nine that comes out a **`donut`**: five pieces enclosing a hole with the wool room closing its far corner. Read as a walled garth, snowbound, with a frozen pond in the middle of it and a hall and solar on the hub. Both ring arms are cut level with the hole so a bedrock wall bars each of the two lanes past it, and every piece states its own height, so the garth climbs a course at a time from the green to the byre |
| `opus5-kiln-row` | ctw | Opus 5 | **72 × 128** — a dry wadi between two banded bluffs, a terrace of three flats on each shelf under **brick roofs**, the wool room at one end of it and the spawn at the other. A mesa's strata are a `layered` stack in the **wall** bucket, so every drop on the board is the same rock in the same order and nowhere else is; the cliffs themselves are `scarp` marks, which draw a fall along a line at a chosen grade. 1.2% dead |
| `opus5-deepcut` | dtm | Opus 5 | **72 × 128** — a chalk quarry worked down in six benches, its floor a Z of two faces joined by a flooded neck, with the monument on a spire of unquarried chalk in each. Four `area` marks and `step: 4` with `stairs: true` do what thirty marks could not: the terracing that ruined `tarnfell` **is** a quarry bench. The spires are `exclude` shapes, which is the only way to a vertical-sided column |
| `opus5-aerie` | ctw · dtc | Opus 5 | **72 × 128** and no ground at all — six crags in open sky, ten to sixteen blocks apart, over a **24-block strait**, with a **core** on the forward spire and the wool in a `teamTint`-walled fold behind it. Every crossing is a bridge somebody builds: `deny(void)` closes everything outside the four build zones, so the zone list is the map |
| `opus5-overwall` | ctw · dtm | Opus 5 | a labyrinth of ten-block pillars on a twenty-two block grid, so **every passage is twelve wide**. Three slabs: a floor with a relief of its own, a wall network with a **second** relief over its crests, and two brick bridges seated on pillar tops held flat for them. A river down the one corridor no wall crosses; a keystone in one 34-square court and a wool room in another; and 32 trees, 14 boulders and four **houses on stilts** on the wall tops, out of everyone's reach |



### Opus 5 — furnished with sculpted props

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `form-gallery` | — | Opus 5 | nine parametric structures on one deck, eight of them circles, polygons and rectangles on a **single layer** — a roundhouse under a conical roof, a hollow dome, a hollow ellipse, a tapered tower, a ziggurat, an arch, a colonnade under a saucer dome and an amphitheatre — plus a **gatehouse** composed of five emitters at once, two crenellated drum towers and an arched gate a visitor walks in through. 19 layers, 157 shapes |
| `sculpture-gallery` | — | Opus 5 | nine solids compiled into layers — a robot, a droid, a **Rubik's cube**, a hooded statue, a coupe, a four-legged **walker**, a **dragon** rearing off a crag, a **starship** and a ring station, the last two flying. 65 layers, 7,423 shapes, and the table that says why: the cube is one run per column and takes seven layers, all of them colour |
| `opus5-automaton` | dtm | Opus 5 | **110 × 110** — a flat green square whose whole finish is *props*: a 45-block brass colossus standing on a stepped granite plinth over the symmetry centre, four hooded sentinels holding lanterns on the spawn approaches, two tile rotundas under clay cones with doorways cut through them, and two tapered slate watchtowers. Every one of them is shapes on layers of the ordinary sketch document, arriving through the finish's `addLayers` with nothing about the studio changed; the four sentinels are two authored on the north half and fanned. Scores **0 with no violation and no lint**. Flat because a prop states an absolute floor and a relief moves the ground under it — [SCULPTING-WITH-LAYERS.md](SCULPTING-WITH-LAYERS.md) §5 |

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

### The author's basin — three boards, a hand revamp, and the revamp restated

`specs/rockymine-map-experiment` is a basin the author drew in the Sketch tool — a sunken canal between two
thirty-high masses, two destroyables a team, the hills hinted as stacked slabs — and its `BRIEF.md` is what
three agents were asked to make of it. Then the author took one of the three onto a build server and finished
it by hand, and that finished world is the first board here that was **not** built by the studio.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-millrace` | dtm | Opus 5 | the basin flooded, walled in stone brick and bridged twice; a quarry pit under one monument, a diorite statue on the moor brow, a lighter moored in the race, clouds in white glass. Two grounds of two-shade noise and the island a third; nine grown oaks and ten grown firs a side |
| `sonnet-cutwater` | dtm | Sonnet 4.5 | the basin **flooded, walled and bridged** — a canal walled on both banks with one arched bridge across it, the four flat hint layers replaced by real relief, and a pit dug for the near destroyable to sit down inside. 260 × 250. The one geometry fault in the base was fixed against the evaluator rather than by eye — a piece widened one cell and its neighbour shifted the same amount took the hop from 25 into `G5`'s 10–20 band — and the author's own spawns and goals were read, weighed and left exactly where they were drawn |
| `sonnet-fallowmere` | dtm | Sonnet 4.5 | the same basin **left open** — the same canal, the same single bridge, the same edgy coast, and then less of everything else: two quiet grass banks, a hollow dug under the forward goal, a lone knoll-island either side of the crossing, and just enough made — a croft, a grounded biplane, a rowboat, a scatter of stone — to give the ground a reason without covering it |
| `opus5-weirbank` | dtm | Opus 5 | half of Millrace's box, the same art direction on a quarter of the area — `review/opus5-weirbank.md` |
| `rockymine-ruediger-millrace` | dtm | rockymine, Ruediger_LP | **Millrace finished by hand**, five hours of WorldEdit and Arceon over the studio's world: the stone body re-laid as a six-stone voronoi, three courses of earth under every surface, the canal walls in double slab and grey wool, granite paths, ferns on every grass block, four biomes, the eighteen grown trees replaced by sixteen of the author's own showcase trees, a team-coloured statue on the small island, a tug in the race, a balloon holding the observer spawn, beacons over the monuments. The terrain, water, walls, bridges and boulders are the studio's, unmoved. `review/rockymine-ruediger-millrace.md` is the author's own account with the commands; `review/fable-millrace-revamp.md` is the measured diff |
| `fable-millrace-revamp` | dtm | Fable 5.1 | **the hand revamp restated as documents** over the original's own layout: the six-stone body as one nested cell-and-turbulence pattern, the earth as a depth stack, the author's trees planted as `copied` recipes cut out of `showcase/tree-showcase`, the statue, the tug, the balloon and the beacon frames lifted out of the hand-built world as made things. Every gap between the two is in the review |
| `fable-mossgill` | dtm | Fable 5.1 | **the same techniques on half the box and a new layout** — 130 × 120: one moor split by a beck cut eight courses into it on a shallow diagonal, a crag a team spawns on in each corner, a brow down onto an apron where the monument stands in a quay-walled sheepfold, a plank bridge between two quays at the axis. The six-stone body as a volume of cells wider than tall, three courses of earth as a volume, the author's copied oaks and conifers, granite roads, ferns, four biomes. `review/fable-mossgill.md` |

`showcase/tree-showcase/` is the author's tree corpus beside the technique showcases: 75 hand-built trees on
their own platforms, the measured ground truth behind `pgm-studio/docs/world-export/tree-corpus.md`, and now
the world `pgm-studio/tools/seed-trees.cs` cuts copied tree recipes out of.

### Boards built to put a rule on live ground

Two boards whose subject is a document rather than a place: each one exists so that a rule written down
somewhere else can be watched deciding a real board, and the review says which sentence bought which part
of the ground. [reports/opus5-run9-brackenfold.md](reports/opus5-run9-brackenfold.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-brackenfold` | dtm | Opus 5 | **68 × 212, and the board the *What a board is painted with* section of `AUTHORING-BRIEF.md` was written for** — a grass down falling from each spawn to a peat working, the monument standing on a cobbled fold on the shoulder above it, and the two workings separated by open air a team has to bridge. **Three themes and one of them is the map**; the variation on the surface is *drawn* — three polygons a half carrying a `scar` theme, worn ground where sheep have poached the down — rather than a field sampled over the moor |
| `sonnet-fellmoor` | dtm | Sonnet 4.5 | **80 × 250, built to put `GO1` and `GO4` on live ground** the week they were wired — a grazing common split by a spring-fed beck, two cairns each on their own barrow behind a fold, a stonemason's hall and a darkwood croft behind each spawn, a mill by the ford, and a turf causeway as the only way across. `POST /plan/inspect` reads the ratio at **3.31** in `[3.0, 4.0]` and the own-spawn walk at **55** in `[40, 90]`. Built a second time over, once the first pass turned out simple to the point of dodging its own findings |

### Opus 5 — the layer track's two fixtures

Neither is a playable map, and both are here because a claim about stacked layers is cheaper to check
against one small world than to argue from a paragraph.
[reports/opus5-mineshaft-layers.md](reports/opus5-mineshaft-layers.md) ·
[reports/opus5-undermarket-layers.md](reports/opus5-undermarket-layers.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-mineshaft` | ctw | Opus 5 | **the smallest board that is genuinely two storeys** — a gallery running under a meadow with an adit climbing out of its east end, and the minimum geometry that answers what a stack of layers actually does. `opus5-undercroft` raised the question; this is the file every claim on the layer track can be measured against |
| `opus5-undermarket` | ctw | Opus 5 | **eighty blocks square, three layers, four shapes, no relief and no dressing** — the smallest board that proves each storey **wears its own finish**. The terrace roofs the middle and the edges are the yard, so one top-down shows both storeys' paint side by side; read at `(0, 0)` the same cell answers two surfaces and two blocks. A player walking off a span meets the void, and `render/topdown?layer=yard` draws one storey by name |

### Opus 5 — two boards to a composition somebody else drew

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-liminal-dtm-ii` | dtm | Opus 5 | **248 × 160 to a brief from outside this repository, and three floors of it played at once** — a walled village as the battlefield, an oval river ringing it, a Desert Pyramid spawn and a Snowy Taiga on each long edge. **Five sketch layers** (`under` · `lid` · `ground` · `bridge` · `sky`): an undercroft holding a swimming pool and a Backrooms maze under the sand, the desert itself at y36, and eight islands hanging over the water to y53 — with one of its six obsidian monuments a team on each of the three levels. [reports/opus5-liminal-dtm-ii-run.md](reports/opus5-liminal-dtm-ii-run.md) |
| `opus5-slipway` | dtm | Opus 5 | **240 × 264 of harbour, sketched by the author at cell scale and scaled up here** — a brigantine on the water, a crane dock west of centre with the first goal's dock beside it, a port east with a car park, the dockside town behind the west dock, a second settlement back and to the east with the other goal in front of it, a terrace row across the middle joining the two, and a field on each arm for a balloon to fly over. Symmetry error **0**, export gate **OPEN**, and **nothing the dressing pass declined** |

### Opus 5 — a board to the author's own brief, with a community map read first

The first board here authored to a list of things rather than to a shape, and the first whose references
are maps this repository does not hold. The brief named minuyo's boards in `CommunityMaps` for their
angularity and *Fox Dream* for its houses, so the run began by **reading a finished community map with the
world tools** — `anvil.py` for a census and a surface read, `probe.py` for what its body is laid in, and a
section cut through one of its houses for the palette `@lk-terrace` forks. `import-folder` cannot take a map
that already carries a `map.xml`; that is the route working as specified, and it is why the reading was done
with the tools rather than through the API. [reports/opus5-lindenkreuz-run.md](reports/opus5-lindenkreuz-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-lindenkreuz` | dtm | Opus 5 | **90 × 200, and it carries no relief at all** — every height on it is stated, which is what makes it angular and what lets thirty 5 × 3 cars state an absolute floor and land on the tarmac rather than in it. Two city blocks either side of a twenty-block gorge joined by one railway bridge: a car park marked into 36 bays with the monument standing in one of them, a Litfaßsäule and a nether-brick piano on the station forecourt, terrace houses on two raised garden blocks, and an S-Bahn in a **cut-and-cover tunnel** — a trench cut by an override add, a lid that has to be a layer of its own, a switchback stair down to the platform — that comes up a ramp in an open cutting and goes on over the bridge |

### Opus 5 — four boards to a list of things, one per objective shape

One brief was the author's, in full — a swamp DTC with vines hanging at different heights, lily pads on
the water, roads of coarse dirt and polished andesite — and the other three were the run's to choose, one
per objective shape and each on a colour scheme far enough from the last to test the paint rather than
repeat it. What the four have in common is that three of them are rectangles and the fourth is not, and
the fourth is the one worth reading first: a wool board's rules refuse a rectangle, and the hub-with-two-
arms they force instead came out with **1% dead ground against 28.8%, 36.7% and 40.1%**. A rectangle has
corners no journey passes; an arm is a corridor to somewhere, so every block of it is on the way.
[reports/opus5-run1.md](reports/opus5-run1.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-alderfen` | dtc | Opus 5 | **150 × 210, a peat holm archipelago, and the board that found out how a vine gets onto a map** — nothing in the dressing vocabulary places one, so the oaks are seven `copied` recipes each carrying 4–18 vine cells hung in curtains. Two obsidian cores a team on level bog in front of a hill-backed island; two team islands and one mid holm, joined only by a build zone over sixteen blocks of void; painted bog pools with lily pads over a sand bank; roads of coarse dirt with polished andesite laid through them; and six cumulus clouds of white wool standing at y80–96 as **made** things |
| `opus5-quiverstone` | dtm | Opus 5 | **140 × 200 of badlands, and a pinnacle that is a made thing on purpose** — a hoodoo tall enough to read as one would otherwise stand inside the build ceiling, so it is a made layer instead. Two obsidian pillars a team at `x ±24` on open caliche, **46 blocks of walk from their own camp and 152–154 from the enemy's, of which 23–27 are placed**; an erected clay butte behind each camp for an attacker to climb and bridge from; a dished wash across the front of each monument; and one sandstone reef in the middle both sides pay twenty blocks of crossing to reach |
| `opus5-blockrealm` | dtc | Opus 5 | **110 × 200 of drawn level, where the ground is flat everywhere a player fights and all of the height is erected plates** — brick staircases stepping two courses at a time up each flank, warp pipes at their feet, floating brick-and-question rows, and clouds to y100. Every standing thing is a **made** layer, which is what keeps a 100-course cloud out of the build ceiling, and four of its themes paint no ground at all because they are the materials of made things. The field was narrowed from 140 to 110 on a dead-ground read — **46% → 33%**, and the standing `LN2` complaint cleared in the same change |
| `opus5-lodestar` | ctw | Opus 5 | **120 × 200 on a derelict orbital dock, and the one board whose shape a rule dictated** — eight pieces a side rather than one, because a wool board's rules will not have a rectangle: a spawn berth, a hub, two arms, a wool bay on the end of each, a neck, and the neutral gantry both sides cross to. Two wool bays a team, each captured by the *other* team and carried to a monument beside its own spawn; the neck is the board's **only** edge on the void, 40 wide with a 20-block crossing; masts to y36 and solar wings to y58. **1% of it is off every route** — the run's best by a wide margin, and the reason is the topology rather than the dressing |

### Opus 5 — a four-team board from a handed-over plan

The first board here authored from a plan somebody else drew: a `rot_90` quatrefoil and a five-colour
palette, given as documents rather than as a brief. Two things it settled. **A scale somebody drew is a
statement, and an evaluator's `"kind": "hard"` is not a gate** — the plan came in at `cell: 1`,
`/plan/evaluate` read it `valid: false` on the composer's `G5` band, that was mistaken for a refusal and
the board was rebuilt at twice the size; driven at the author's own scale it compiles, pre-flights and
exports with 0% dead ground. And the run found the studio bug that made a four-team board impossible to
build fairly: a relief-bearing group read each mirrored copy's heights back through the axis that
*placed* it, which is right for every mirror and the half-turn and wrong for a quarter-turn, so two of
four teams played the shapes' flat base heights while `relief/read` answered `symmetryError 0`. Fixed
upstream as `WE75`. [reports/opus5-quatrefoil-run.md](reports/opus5-quatrefoil-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-quatrefoil` | ctw | Opus 5 | **98 × 98 at the scale it was drawn — nine landmasses, no land route anywhere, and not one step on it a player cannot walk up.** The author's eleven rectangles and their ids untouched: four corner quarters of mossy moor with a spawn hall in the outer corner and a wool room on a ramp in the middle, four pale sand capes on the axes, and a stepped keep in the centre that all four capes meet at. **The shaping is piece heights and four ramps rather than relief** — the relief carries a grain and nothing else — and the board reads back **5 904 walked · 0 scrambled · 0 barrier**, 0% dead, 39 props placed and none declined. The spawn is the shape the model allows and a board rarely uses: a 12 × 12 hall in the corner of a 20 × 20 protected region, so a player walks the whole way round their own building. It is cut with **two doors** — the piece meets the board on both its `+z` and `+x` walls, so both are ways out — and the player looks at the corner between them at yaw `315`, which is the middle of the map. The iron is `POST /plan/room`'s own answer beside the near door, not a hand-placed marker. Every enemy wool costs fifteen placed blocks at least |

### Opus 5 — a four-storey board, and the pass that reworked it

The board with the most storeys in this repository, and the only one here built twice: once as a
terminus station under a viaduct, and once again against a list of measured faults, which is what turned
it from areas thrown together into a place with a plan. The second pass is the worked example of the
sketch's `material` word — one `TerrainMaterial` in place of a theme, painted over a shape's whole span
— and of why it exists: a theme is a recipe for ground and a shape with no interior column is all edge,
so a kerb, a stilt or a stair tread themed like the floor it serves comes out as rim over wall with the
theme's own surface nowhere on it (`SK23`). 38 shapes on it carry a theme and 367 state a material.
[reports/opus5-tiefkreuz-run.md](reports/opus5-tiefkreuz-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-tiefkreuz` | dtm | Opus 5 | **80 × 224 on seventeen layers, and the objectives stand on the rails** — two railways crossing at right angles over one block of city: a north–south **through** station in cut-and-cover with ballast at y5, rails a course proud of it, a concrete cess at each track edge so a track is a trough a player walks through rather than a ditch, an island between two side platforms at y8, a concourse at y18, the street at y29, and the rails running on through a portal into a vaulted bore at the back of the map. Over it, east–west on six brick piers with a 32-block clear span and a masonry soffit, an **elevated station** — platform, canopy, two-car train — with the second monument in its four-foot. Every flight is 45° with a rail two courses over its treads; behind the crossing an avenue with planted verges, an arterial road and six flat-roofed blocks, of which the spawn is the tallest. No relief at all: every height on it is stated |

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

**Three folders under `maps/` are fixtures rather than boards.** `biome-test`, `biome-test-pattern` and
`biome-test-wide` are three worlds built to look at what the biome field does to grass, leaf and water
tint — the same minimal DTM board painted three ways. They carry no `specs/`, no `review/` and no report,
they are in no run, and they are the reason the map tables below do not add up to the folder count. They
load; there is simply nothing on them to play.

**Two folders in run 2 contain no map.** `haiku-r2-canonical-8` and `haiku-r2-ctw-mid` export a 245-byte
`map.xml` with no teams, no spawns and no objectives, over region files that are largely empty. They are kept
because they are evidence, not because they are playable — a map with nothing on it satisfies every refusal
the pipeline had at the time. **Do not load them.**

**A recreation never reuses the original's name.** Both the folder and the `<name>` in `map.xml` carry a
suffix, because a PGM server loading this repository alongside the community corpus would otherwise see two
maps calling themselves the same thing. The name lives in the plan document's `meta.name`, which is what the
compile reads — changing the folder alone is not enough.

## Looking at a map without Minecraft

Every map carries `specs/<slug>/renders/`. Two reads answer questions no plan view can:

- **`--topdown --layer structure`** reads the provenance record and draws what the build *recorded* itself
  placing. Its owners list is a literal census of the dressing — every count reads `units × orbit order`, so
  a prop that landed nothing has no row at all:

  ```python
  import json; from collections import Counter
  p = json.load(open('specs/<slug>/provenance.json'))
  print(Counter(o['kind'] for o in p['owners']))
  ```

  Beside it, `specs/<slug>/dressing-report.json` answers what did **not** land, and is written only when
  something dropped — so its absence means everything authored stood.

  The record is written into the exported world's `region/` and the driver moves it out, so a CLI read-back
  pointed straight at `maps/<slug>/region` falls back to the material estimate and says so on its scale line.
  Copy the sidecar back beside the `.mca` files for the run that needs it.

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
