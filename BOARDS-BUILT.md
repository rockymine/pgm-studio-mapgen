# Every board built here

One entry per board, grouped by the run that produced it, with what the run was for and what each board
turned out to be. Mode is what the map's own `<gamemode>` declares.

**This is a log and it is appended to, which is why it is not in `README.md`.** A board lands here when its
world and its spec are committed, written up by the run that built it (`AUTHORING-BRIEF.md` §6);
`tools/boards-check.py` fails on a folder nobody wrote up. The README says what the repository is and stays
the size a reader will read. Measured on disk: **60 spec folders under `specs/`**, **118 more under `specs/archive/`**, **187
worlds** under `maps/` and **71 reports**.

A spec a report or a review names at `specs/<slug>` and that is not there is at `specs/archive/<slug>`. Those
accounts are dated and were right the day they were written, so their paths are left as they stand. What the
two folders are for, and why most of these specs no longer compile, is `README.md` §Maps.

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

`specs/archive/rockymine-map-experiment` is a basin the author drew in the Sketch tool — a sunken canal between two
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
| `fable-millrace-revamp` | dtm | Fable 5.1 | **the hand revamp restated as documents** over the original's own layout: the six-stone body as one nested cell-and-turbulence pattern, the earth as a depth stack, the author's trees planted as `copied` recipes cut out of `corpus/tree-showcase`, the statue, the tug, the balloon and the beacon frames lifted out of the hand-built world as made things. Every gap between the two is in the review |
| `fable-mossgill` | dtm | Fable 5.1 | **the same techniques on half the box and a new layout** — 130 × 120: one moor split by a beck cut eight courses into it on a shallow diagonal, a crag a team spawns on in each corner, a brow down onto an apron where the monument stands in a quay-walled sheepfold, a plank bridge between two quays at the axis. The six-stone body as a volume of cells wider than tall, three courses of earth as a volume, the author's copied oaks and conifers, granite roads, ferns, four biomes. `review/fable-mossgill.md` |

`corpus/tree-showcase/` is the author's tree corpus: 75 hand-built trees on their own platforms, the measured
ground truth behind `pgm-studio/docs/world-export/tree-corpus.md`, and the world
`pgm-studio/tools/seed-trees.cs` cuts copied tree recipes out of. It is not a board and `corpus/README.md`
says what else it is read by.

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
section cut through one of its houses for the palette `@lk-terrace` forks.

`import-folder` cannot take a map that already carries a `map.xml`; that is the route working as specified,
and it is why the reading was done with the tools rather than through the API.
[reports/opus5-lindenkreuz-run.md](reports/opus5-lindenkreuz-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-lindenkreuz` | dtm | Opus 5 | **90 × 200, and it carries no relief at all** — every height on it is stated, which is what makes it angular and what lets thirty 5 × 3 cars state an absolute floor and land on the tarmac rather than in it. Two city blocks either side of a twenty-block gorge joined by one railway bridge: a car park marked into 36 bays with the monument standing in one of them, a Litfaßsäule and a nether-brick piano on the station forecourt, terrace houses on two raised garden blocks, and an S-Bahn in a **cut-and-cover tunnel** — a trench cut by an override add, a lid that has to be a layer of its own, a switchback stair down to the platform — that comes up a ramp in an open cutting and goes on over the bridge |

### Opus 5 — four boards to a list of things, one per objective shape

One brief was the author's, in full — a swamp DTC with vines hanging at different heights, lily pads on
the water, roads of coarse dirt and polished andesite — and the other three were the run's to choose, one
per objective shape and each on a colour scheme far enough from the last to test the paint rather than
repeat it.

What the four have in common is that three of them are rectangles and the fourth is not, and the fourth is
the one worth reading first: a wool board's rules refuse a rectangle, and the hub-with-two-arms they force
instead came out with **1% dead ground against 28.8%, 36.7% and 40.1%**. A rectangle has corners no journey
passes; an arm is a corridor to somewhere, so every block of it is on the way.
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
exports with 0% dead ground.

And the run found the studio bug that made a four-team board impossible to
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
it from areas thrown together into a place with a plan.

The second pass is the worked example of the sketch's `material` word — one `TerrainMaterial` in place of a
theme, painted over a shape's whole span
— and of why it exists: a theme is a recipe for ground and a shape with no interior column is all edge,
so a kerb, a stilt or a stair tread themed like the floor it serves comes out as rim over wall with the
theme's own surface nowhere on it (`SK23`). 38 shapes on it carry a theme and 367 state a material.
[reports/opus5-tiefkreuz-run.md](reports/opus5-tiefkreuz-run.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-tiefkreuz` | dtm | Opus 5 | **80 × 224 on seventeen layers, and the objectives stand on the rails** — two railways crossing at right angles over one block of city: a north–south **through** station in cut-and-cover with ballast at y5, rails a course proud of it, a concrete cess at each track edge so a track is a trough a player walks through rather than a ditch, an island between two side platforms at y8, a concourse at y18, the street at y29, and the rails running on through a portal into a vaulted bore at the back of the map. Over it, east–west on six brick piers with a 32-block clear span and a masonry soffit, an **elevated station** — platform, canopy, two-car train — with the second monument in its four-foot. Every flight is 45° with a rail two courses over its treads; behind the crossing an avenue with planted verges, an arterial road and six flat-roofed blocks, of which the spawn is the tallest. No relief at all: every height on it is stated |

### Fable 5.1 — four boards to the author's spoken brief, revised to the author's feedback

One sentence each, built through the driver and read back before any picture was opened, then rebuilt
after the author read the first pass; the account of both passes, the numbers and the three questions left
for the author are [reports/fable-four-boards-run.md](reports/fable-four-boards-run.md). The quarry is the
run's attempt at an underground passage, planned from the rock up: a `below` layer of rock slabs with the
tunnels cut through them, the bench's floor lifted over it, and two stairs cut back up through the bench.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `fable-ashcombe-delph` | dtm | Fable 5.1 | a worked quarry on a moor: the monument on the bench above a wandering face, the loading yard below it falling four blocks west to east, a haul ramp round the west end, a crag melted into the bank with the house at its foot, two low stone walls for cover, and **two tunnels** through the face that meet under the bench and come up two stairs, one beside the monument |
| `fable-whinberry-ring` | ctw | Fable 5.1 | composer seed 18 at sixteen players taken over by hand: three levels, a twin frontline with a bay of void between its prongs, a stepping stone on the axis, a bedrock wall on each wool approach, the outline reshaped one vertex at a time, a three-storey wool room over a two-storey spawn, one oak |
| `fable-saltwharf` | dtc · dtm | Fable 5.1 | a stone quay under a grass headland: the core on a stepped stone plinth twelve blocks behind the sea wall, a beacon of end stone on the knoll in the corner, a flat-roofed warehouse of two wings either side, the strand two blocks under the quay, a pier into the sound, the spawn ten blocks up behind with a road down the east flight to the sand |
| `fable-hollin-tarn` | dtm | Fable 5.1 | a snowed valley head under a cold-taiga sky: the monument on a green knoll ten blocks off the axis behind a frozen tarn cut as a level plate, a brook of ice out of it, a crag on the east shore, spruce shoulders either side, a track from the lodge round the shore to the hut and on to the build zone |

### Opus 5 — five boards, one idea each

Five maps authored in one run against one instruction: decide what each board is *about* before deciding
what it is made of, and keep it to one thing. Every one built, every one `export gate OPEN`, every one
`declined 0`. What they share is method rather than subject — the ground on all five is finished on the
**slope** band axis with its cuts read off `GET …/incline?format=text`, the plan on all five is a handful
of rooms and corridors with the board's shape left to the relief, and every way up a face on any of them
is an authored flight measured at worst step 1. [reports/opus5-five-boards.md](reports/opus5-five-boards.md)

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-blackden-sough` | dtm | Opus 5 | **70 × 240, and a drainage sough driven under a gritstone edge** — a twelve-block scarp across each team's ground with one eighteen-wide nick in it, and a six-course passage under it that comes out on the dale floor behind the lot. The storey below is stated as adds banded round the corridor and **clipped out of the moor's own drawn outline**, so nothing of it stands past the coast as a ledge over the void; both flights walk for nothing in both directions (`walk?from=-21,45,18&to=-21,80` — 35 blocks, **0 placed, 0 drops**) |
| `opus5-heftfold` | ctw | Opus 5 | **110 × 170 on the composer's own skeleton, with its three gaps filled** — a walled sheepfold on the saddle as the island the middle otherwise has none of, a team site split into a pasture at y11 and an intake at y16 rather than one rectangle, and the spawn standing **between** its two wools instead of behind both (25 and 32 blocks by walk). The intake is `relief_scope: exclude` so the two tiers meet at a face, its gateway is a rectangular re-entrant cut into the retaining wall, and **0.0% of the board is dead** |
| `opus5-glassmere` | dtc | Opus 5 | **80 × 220 of snowfield where nothing hides you** — two shores of a mere whose middle never freezes, with the coast drawn into three headlands and two bays so the crossing is 24 blocks at one and 40 at the other. The ice is laid **solid** at the water and freckled with a second, wider `worn` stroke over it, because an edge between two grounds is drawn and never sampled. One theme, and its whole variation is the board's own angle: lying snow under 14°, snow and scoured grass to 30°, bare rock past it |
| `opus5-burgage-terrace` | dtm | Opus 5 | **80 × 220 built entirely on one boundary** — a market terrace six courses over a water meadow, its front edge cut into two re-entrants and a salient, with a flight set **into** the wall at each re-entrant. The retaining wall is a `wallDiagonal` whose fourth run is a **`teamTint`**, so the town wears the colour of whoever holds it and you can read from the far bank whose terrace you are looking at. Three burgage plots a side, one style, differing in height and footprint and nothing else |
| `opus5-lingbeck` | ctw | Opus 5 | **110 × 200 split by its own beck** — a six-course gill running the full depth of each team's ground with a wool on each bank, so every rotation between them is a crossing and there are exactly three: round the head, over the brig, or down through the water at the ford (worst step 1, 1 and 0). The gill is an **override add** cut out of one hub piece, because a plan piece at a lower surface enclosed by higher ones is not a cut at all; the brig is a one-course layer at `base_y 11` lapping neither bank. **0.0% dead** |

### Sonnet 5 — five boards, each one its own place

Five maps in one run, each written up on its own before the next was begun: a report and a review a board,
in `reports/sonnet5-*.md` and `review/sonnet5-*.md`, rather than one account of the five. What they share is
that the *place* was decided first and the mechanism second — a quarry, an estuary, a snowbound valley, a
timber yard, an autumn wood — and that each report is asked the same three questions about the studio
(**missing**, **unreachable**, **mistaken**), with the verdict settled by reading the code and the reading
cited. Four of the five dressed with no decline at all.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `sonnet5-emberwood-vale` | ctw | Sonnet 5 | **Two hamlets at opposite ends of an autumn wood, and the wood is the only way across** — each keeps its wool at a shrine behind the village, and three things stand between them: a village-green void through each hamlet, a garden island cut off from the main approach and rejoined by a hand-built footbridge, and a ten-block brook of void across the centre clearing that every crossing must ford. A rougher west-flank trail is the wool's second and harder route. Three themes, and two timber house styles that differ by a roof swap and a repaint. **13 874 walked · 24 scrambled · 0 barrier**, 44 props placed and 1 declined |
| `sonnet5-fellgrave-hollow` | dtm | Sonnet 5 | **Two highland mining camps digging for the same frost-locked relic** — one obsidian destroyable a team, each held in a hollow cut into the hillside at the head of its own dig. Deliberately the quietest of the five: one plan piece of shape decisions and a junction stub, with everything else left to the relief and three themes. The valley is finished on the **slope** axis — snow meadow, rocky shoulder, bare stone — under a cold biome, with one taiga-and-podzol stand kept off the grass, and the mandatory team-to-team void is dressed as a frozen tarn that has cracked through at its centre. Narrowed to 100 wide once, which took dead ground from 71.7% to 61.7%; 28 props placed and none declined |
| `sonnet5-kilnholt-cut` | dtm | Sonnet 5 | **Two stonework guilds cut into opposite flanks of one worked-out quarry** — two buried obsidian monuments a side at the bottom of each cut, and a played-out adit under the west flank that still joins the two sides for anyone bold enough to use it. One landmass a side with the spawn fused to its own excavation, joined on the surface **only** by a permanent void gap spanned by a build zone, so the adit is the one way over that costs nothing placed. The ground is finished by slope angle rather than height — reclaimed floor, worked shoulder, bare cut face — and the tunnel is stacked bottom-up with a stair back to the surface at each end. One edit took the dead share from 30.3% to 9.4%, exactly the flank that was cut away; 16 props placed and none declined |
| `sonnet5-sable-reach` | ctw | Sonnet 5 | **Two trading posts across a tidal river mouth, built past the composer's three known gaps** — each team's site is **two** landmasses (a settlement island and a flanking dock skerry) joined by a short build zone, a build zone sits **inside** the team's own ground as a plaza among the warehouses rather than only at the middle, and the crossing is a real route rather than a gap: one permanent `made`, `keepClear` bridge as the chokepoint with a pair of shallow sand fords as the second way over (`WL8`). The wool is in a dockside warehouse behind a seawall drawn with a diagonal pattern and a team-colour rim. Shore graded sand-then-mud, three themes, two house styles forked from one recipe. **23 636 walked · 12 scrambled**, 41 props placed and none declined, 37.2% dead |
| `sonnet5-talltimber-yard` | dtc | Sonnet 5 | **Two logging outfits, and the core is the ledger** — one obsidian core a team, kept in a tall multi-wing counting-house at the middle of its own timber yard, with the two yards facing each other across the felled ground between them and a build zone spanning the void rather than land. Every house style is a fork of a shipped preset varied by wings and storeys rather than a design of its own, the three-colour paths are solid and drawn before any scenery, and the street trees are sparse. **15 600 walked · 0 scrambled · 0 barrier** — the flattest board of the five — 20 props placed and none declined, 27.7% dead |

### Haiku 4.5 — five specs to one brief, and what stopped each of them

The same brief the three runs above answered, taken in parallel: five specs written at once in about five
minutes, against roughly half an hour a board for the others. **Nothing here built, and the run is kept
because what stopped it is legible in the files.** No world, no render, no review.
[reports/haiku-five-specs.md](reports/haiku-five-specs.md) is the design document it wrote before the first
API call, and it describes all five as though they exist.

Three things stopped them, and only the third is the one the run itself reported. **Four of the five state
`"plan": 1`**, so `POST /plan/compile` refuses them with `PL15` before anything else is read — they were
never drivable. **Four of the five carry no `placements` at all** — no spawn, no wool, no monument, no core
— so they are terrain with nothing on it, and since the studio *derives* `<gamemode>` from the objective
modules an intent carries, those four would declare no game mode whatever they were called.

And **all five
finishes state `themeByHeight`**, which is not one of the driver's keys and is dropped in silence on the
whole-layout write — the same trap `roomStyles` sets, and the reason `tools/README.md` now says so in the
row for each key.

**The unsupported game modes are real but are the least of it, and they exist only in prose.** `quarry-clash`
is called CTF in its docstring, `harbor-district` a mixed destroy-and-capture board and `forgotten-village`
king-of-the-hill — in Python comments and in the design document, never in a document the studio reads,
because there is no field in which a spec may assert a mode. A board names its mode by carrying the
objectives, which four of these do not.

**PGM knows all three words** — `ctf`, `mixed` and `koth` are in the
same closed enum as `ctw` — so what was missing was never the id but the objective the studio builds it
from, and the studio had three: wools, destroyables and cores.

`haiku-riverside-outpost` is the one taken up again after the author's redirect, and it is the interesting
one: **`plan: 2`, with spawns, wool rooms and wools on it**, which is the shape the brief asks for. It still
does not evaluate — `PL4` (the overlapping `river` and `outpost` differ by 4 courses), `PL7` (a spawn at
`[-32, -20]` outside its own piece), `PL5` (a wool naming the empty piece `''`) and `LN2` (a 150-block chain
against an authored band of 25–110). The run's own account names `PL4` and `PL7` correctly and stops before
fixing them.

One of the three invented modes has since become real: **the section that follows authors king-of-the-hill
boards**, because that run read PGM and the corpus first and wrote the contract down before it built
anything. The mode was not the mistake; asserting it in a docstring instead of finding out was.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `haiku-riverside-outpost` | — | Haiku 4.5 | A wool board across a river, and the only one of the five with objectives on it: six pieces, `plan: 2`, two spawns, two wool rooms and two wools. Four refusals stand between it and a compile, two of which its own report names |
| `haiku-mountain-stronghold` | — | Haiku 4.5 | Seven pieces called a monument board in its docstring, carrying no monument and no spawn. `plan: 1` |
| `haiku-quarry-clash` | — | Haiku 4.5 | Seven pieces at three heights — rim, shelf, floor — called CTF, an id PGM knows and the studio has no objective for. No objectives on it either. `plan: 1` |
| `haiku-harbor-district` | — | Haiku 4.5 | Nine pieces grading hinterland to beach to dock, called a mixed destroy-and-capture board. No objectives. `plan: 1` |
| `haiku-forgotten-village` | — | Haiku 4.5 | Five pieces of snowed peak called king-of-the-hill, written when no control point existed. No objectives. `plan: 1` |

### Opus 5 — the first board with a shop in it

The studio grew shops this run: an intent takes a `shops` array, the export writes the `<shops>` menu and a
`<shopkeeper>` at every team's spawn, and a map carrying either now parses, stores and re-emits instead of
losing it. `opus5-coinfall` is two three-step camps facing a neutral holm across a pair of twenty-block
voids, with a villager in each spawn hall, and the menu trades the kit's own wood for what a wool run needs.

**A keeper's position is derived unless it names one** — a keeper that says nothing gets one per shop beside
the point players arrive on at every spawn, and one naming a block or a region stands there once. PGM spawns
the entity itself from the element, so nothing is stamped and the board exports the moment its intent is
stored. [reports/opus5-coinfall-run.md](reports/opus5-coinfall-run.md)

**A generated board minted no currency**, which was the run's finding rather than a fault in the map: the
spawn kit and the kill reward derived from it were its only item sources, so a shop priced in the emerald or
nugget 764 of the corpus's 907 icons use was a menu nobody could open an account with. The studio takes
`spawners` on the intent now — a place, a rate, a cap and what drops — which is what the corpus mints with:
374 of the 429 entries yielding one of the eight commonest shop currencies are a spawner's items.

**A path paints only where it reaches the ground the shapes draw.** The board's two brown ways were authored
as a `polyline` with a theme and nothing else, and painted nothing at all in silence: a stroke with no
`base_height` is one block thick, and a cell's theme goes to the smallest shape that reaches the ground stated
there — never a terrace at 17, 20 or 25. Stating the terrace's own height is the whole fix, and costs the
stroke nothing, because the relief still decides where the way ends up.

### Opus 5 — eight boards by combining relief modes, and a ninth built to the standard they missed

Two agents authored four boards each on one idea: a `push` for the landform, marks for the ground that has to
agree with something, and `height_mode` shapes for what people built. The eight identities were written down
together before a shape was authored and checked across the set, so the run would not come out as eight
greys, and every one exports with the gate open and `symErr 0`.
[reports/opus5-relief-run-a.md](reports/opus5-relief-run-a.md) and
[reports/opus5-relief-run-b.md](reports/opus5-relief-run-b.md) are the two accounts, and each board has its
review.

`opus5-marram-hythe` came after the eight, as the demonstration board: built against the audit the four of
run A did not meet — two reliefs, ten marks of four kinds, four `level` flights, two `made` layers — and
exported with no complaint, no refusal and no decline. The run rewrote `pgm-board-warmup` around what that
board is about, **how two grounds meet**, rather than around predicting a readout.

**A theme patch with no `height_mode` paints nothing, and both agents found it independently.** A one-course
add at bedrock under twelve courses of terrain is never the top of a cell, so it owns no scope, the census
reads one theme at 100%, and nothing warns; `GENERATION-NOTES.md` carries the working form. **Two of the nine
were briefed as capture boards and built as destroy boards**: the studio this run drove answered `RQ3` for
`controlPoints` and `scoreLimit`, and both reports call that a regression. Studio main reads both (`PG5`), so
it is not one there.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-swallet-dale` | dtm | Opus 5 | **80 × 240, and the monument is inside the rock** — each team's monument stands in a chamber inside a limestone crag with three ways in: a drift, an adit and a hole in its roof you drop through and cannot climb back out of. The crag is three `made` layers over the dale, and its rock is computed as the complement of five corridors, so a corridor moved can never leave a wall behind. Finished with no complaint of any kind; 23.2% dead |
| `opus5-ruddle-brink` | dtc | Opus 5 | **104 × 200, one red scarp climbed in exactly three places** — each team holds a low bench under an eleven-block sandstone brink, and the only ways up are a scree the relief was left to solve, a cut road and a long ramp. The two landmasses are joined by a build zone over 24 blocks of void and nothing else. `GO1` 3.24, 19.2% dead |
| `opus5-blindtarn` | dtm | Opus 5 | **80 × 192, and the whole middle is a corrie** — a bowl with a frozen tarn in the bottom, made by a `push` with a negative crown, so every attack is a descent into the open and a climb under the far rim. Briefed as a capture board. `RL5` stands at 26% level against 30%, and whether a bowl is enough to fight in is the author's call; 13.6% dead |
| `opus5-skerry-wick` | ctw | Opus 5 | **110 × 200 of bare skerries, and no land route anywhere** — a team's two wool rooms stand on two islands on two different seas, so every journey is a gap of 10 to 20 blocks somebody bridges under fire. The team unit is the composer's own answer, 105 land cells asked and 104 drawn, offset west so its `rot_180` image interlocks with it. 9.9% dead |
| `opus5-goldbank-quarry` | dtm | Opus 5 | **104 × 224, one worked limestone quarry with both goals on its floor** — the rim at y32 and the pit at y15–22, entered through one notch a side and climbed out of by three-block benches or a haul road that keeps a player in the open its whole length. `GO1` 3.37. A red-wool cross over red's goal at (−32, 70..72, −49) is unexplained and reported with coordinates |
| `opus5-lynchet-brow` | dtc | Opus 5 | **104 × 208, a hillside farmed into four terraces** — every fight is one drystone retaining wall, and the walked way up each is one of two flights staggered in x, so a route zigzags. The core stands on the second lynchet at (−24, −50), backed against the third's wall so a breach has ground to pool on. The highest barrier share of run B |
| `opus5-scoriafell` | dtm | Opus 5 | **104 × 208, one mountain between two valleys, and the pass is the whole map** — one push builds a range coast to coast with its crest at y65–66, a second cuts a defile four blocks wide through it at y34. Briefed as a capture board; it carries one destroyable a side on its dale floor, and the three hills stay in the finish as the authored intent. 13.5% scramble, relief 8–66 |
| `opus5-braidwater-ford` | dtm | Opus 5 | **104 × 224, a braided river crossed at three fords and nowhere else** — 32 blocks of braid round shingle bars between cut banks a player cannot walk up. Under `rot_180` three fords are at most two characters, one on the centre line and a mirrored pair, and the board says so rather than claiming three. 4 props declined (`DR-BANK`) |
| `opus5-marram-hythe` | dtm | Opus 5 | **88 × 224, a shore where the beach meets the dunes two different ways** — by relaxation on the west, walked at worst step 1, and along a cut bank on the east, which is barrier. The monument stands on a built quay, and a fourteen-layer lighthouse stands on the bar at dead centre, the one landmark neither team owns. `GO1` 3.58, 30 props placed |

### Opus 5 — the first two capture boards, and the law the second was built to

The studio grew capture points this run: an intent takes a `controlPoints` array, the export stamps a clay
pad a point and writes the `<king>` block with a `<score>` beside it. These are the first two boards built
through it, and they were built in that order on purpose — the first took the gamemode's name literally and
stood its hills on a hill, the author read that board, and **the reading is now `match-flow.md` §10**:
structural rather than landscape, no point over open ground, no line from a pad to a spawn, path options on
three storeys, cover placed rather than strewn, one-way ground.

The second is built to it.
[reports/opus5-threap-edge-run.md](reports/opus5-threap-edge-run.md) ·
[reports/opus5-casemate-run.md](reports/opus5-casemate-run.md)

**Both boards are read wrongly by three reads that cannot see a capture point**, which is the run's finding
rather than a fault in either map: `POST /plan/evaluate` raises `PL3` — *this plan has no objective* — on a
board that exports as `<gamemode>koth</gamemode>` with three hills and a 750 limit (`TN19`);
`04-routes.txt` prints *no route between a spawn and a goal* while every one of those routes walks (`WS62`);
and `GET …/coverage` prices ground as dead that a capture board is built to contest.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-threap-edge` | koth | Opus 5 | **A gritstone edge across a moor, with the three hills cut into its top** — `The Edge` on the summit at dead centre and `West Nab` and `East Nab` on the shoulders where the crest steps down, 32 blocks either side of it, each paying 1 to a limit of 750. Both teams spawn on the low moor, north and south, 96 blocks apart. Every pad is 64 blocks of white stained clay and every sky marker 7 of white wool at y57–59, and **both are regions the point displays through** — the pad as `progress-display-region`, the marker as `owner-display-region` — so both take the holder's colour on capture and go back to white when the point goes neutral. A wool room's marker and a destroyable's name a team for the whole match; a hill's is the one that moves. **8 420 walked · 908 scrambled · 224 barrier · 8 faces**, 26 props placed and none declined, export gate OPEN |
| `opus5-casemate` | koth | Opus 5 | **A fort rather than a hill, and the middle pays double** — `The Cistern` in a lidded casemate at y13 pays 2, `West Bay` and `East Bay` pay 1 each from three-walled bays with one mouth apiece, to the same 750. Nothing stands over open ground and no pad has a line to a spawn: the terreplein at y20 carries the traverses and the pillars, the rampart rings it, and the ground is one-way. **The cover here is structure, not dressing — 0 props placed** — and the largest of its 20 faces is the casemate's own seven-block wall at x −21..20, z −15..14. **6 364 walked · 360 scrambled · 1 964 barrier**, nine regions, three white wool markers at y53–55, export gate OPEN. The team colour is **stated** rather than sampled, because on a one-island board the tint could not be read (`WE120`) |

### Opus 5 — four boards, one per game mode, to the shortened brief

Four boards asked for together — capture the wool, destroy the monument, destroy the core, and one board
mixing wool with monument — on the run where the technique cards became the way an instrument is learned.
The identities were written down together before the first shape, and the tone families checked **across**
the set rather than within it, because five boards that are each internally coherent still come out five
greys: **warm red clay**, **pale ice**, **dark wet churchyard**, and the fourth board's grey estuary.

**Three of the four are here; the mixed board is not built yet.**

Two findings the run carries rather than either board: `G8`'s `dead-share` is the one hard term with no
technique card behind it, and it is a **journey** measure rather than a size one — narrowing a board or
shortening it moves it the wrong way, and moving the objective off the centre line took Kilnbrow from
**44.6%** to **6.0%**. And `POST …/sketch/seats` read **60 legal cells for a 9 × 7 house** over the whole of
Hallowgate, which is what sent that board's chapel onto made layers instead of into the dressing pass.

**All three boards state `roomStyles`.** A finish that states none stamps the studio's built-in bedrock box
for the spawn and the wool room, which are the two structures a player sees from the inside — and a board
can carry a designed house row and still leave those on the default, which is what the first pass of all
three did. Each room wears its own board's built family under a **pitched** roof — hipped on Kilnbrow, gabled on
the other two. A flat lid with a hole in it is the bedrock box's own shape, and building one in sandstone
is the default again in a different material.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5-kilnbrow` | dtm | Opus 5 | **A red clay firing-ground where the monument stands out on the open pan** — `Kilnbrow Monument` on a pinned shelf at (−20, −70), twenty blocks off the centre line, 63 from its own spawn and 196 from the enemy's for a `GO1` of **3.11**. The four approaches are four instruments: a spoil hill pushed up east to bridge from, a worked clay pit dug west to come up out of, a kiln row of three on the bench to fight through, and the shelf itself pinned flat. The two lands never touch — a build zone spans the whole 70-block width over 40 of void. The kiln bench is `exclude`d and meets the pan at an eight-block face that two flights state; `EL1` complains about that seam and the transect answers `worst step 1, walked end to end`. Bands cut at 30°/50° off its own `incline`. **12 298 walked · 574 scrambled · 528 barrier · 18 faces**, 28 props placed and none declined, 6.0% dead, export gate OPEN |
| `opus5-sluicehead` | dtc | Opus 5 | **A frozen trough where the core stands on the open floor with ground all round its casing** — `Sluicehead Cistern` at (20, −64), fifteen blocks clear of the board's edge so a breach anywhere on it still has terrain under it for the lava. A core is breached where it stands, so nothing is put between it and the middle. Two moraines push up over either shoulder to bridge from, a cut leat runs past it to move along unseen, and a sluice house stands beside it to fight through. Snow over packed ice on **Cold taiga**, because snow and ice are blocks and a snowfield on a summer biome has a meadow running through it. **10 936 walked · 840 scrambled · 224 barrier · 6 faces**, `GO1` **3.19**, 4.0% dead, 26 props placed and none declined, export gate OPEN |
| `opus5-hallowgate` | ctw | Opus 5 | **A composed arrangement taken over into a churchyard** — `composed-seed-3.plan.json` is committed beside the spec, and what it bought is the hub ringing an enclosed grave-pit, the spawn hung off its flank, the L of causeway to a room in a corner and the stepping stones. Everything else is authored: the terrace five courses up as made ground, one defence wall on the causeway's **outer** interface sixteen blocks out from the chapel, two polylines, and four made layers carrying a lychgate over the causeway and the chapel itself. The hole is left as composed because it is the rotation device — the long way round it covers 37% of the defenders' lane against the short way's 76%. **0.0% dead by construction**, 20 props placed and none declined, three themes all painting, export gate OPEN |
| `opus5-tallowfleet` | ctw + dtm | Opus 5 | **A tidal tallow works where each team defends two objectives that ask for opposite things** — the `Tallowfleet Beacon` out on the open quay at (−4, −61) for a `GO1` of **3.54**, and the wool in a cellar at (35, −105) behind a walled spur, 212 blocks from the attacker and 66 from the defender. The beacon stands on the **centre** finger because it straddles the symmetry line: on a flank the pair sits diagonally opposite and `GO3` reads 201 against a band topping out at 150. Widening the flanking fingers to `FR9`'s fifteen blocks took the fill ratio to 0.571, and the answer was the board's own box rather than its ground — the cellar moved five blocks further into its corner, the box went to ninety wide and the ratio to 0.517. The erratics are dark clay, not stone, because `DR-TONE` is right that a grey rock on a grey estuary is a patch of ground standing up. Nothing can stand on the spur — 34 legal house seats on the whole board and none there — so the boiling house is made layers, mirrored, checked with `column` at (24, −92) and at (−25, 91). Bands cut at 20°/32° off its own `incline`. **10 366 walked · 184 scrambled · 150 barrier · 12 faces**, 26 props placed and none declined, 0.0% dead, export gate OPEN |

### Haiku 4.5 — four boards that do not build (2026-09-21)

**The run did not produce a board.** All four specs are on disk under `specs/haiku45-*` and every
one of them is refused by `/plan/evaluate`, so no world matching any of them exists. They are kept
as the run's evidence rather than as boards, and are listed as debts below.

The stale worlds under `maps/` and the three reviews claiming "built and exported successfully,
0 declined props, OPEN export gate" were removed: every world predated its own spec by twenty
minutes, and `placed 0, declined 0` counted nothing attempted rather than nothing refused.

| Slug | Meant to be | What its spec does when driven |
|---|---|---|
| `haiku45-scarp` | dtm | `G8` dead-share **0.766** (band [0, 0.12]) · `GO3` opposing-goal distance **7** (band [85, 150]) · `RQ2`, a studio-side crash |
| `haiku45-moor` | ctw | `G8` dead-share **0.833** · `PL12` landmass [wool-high, lane-b] mixes mirrored and non-mirrored pieces · `PL9` wool unreachable from either spawn |
| `haiku45-bastion` | ctw + dtm | `G8` dead-share **0.806** · `GO3` **7** · `PL4` `wool-platform` and `lane-b` overlap at a surface delta of −5 · `PL9` wool unreachable from either spawn |
| `haiku45-cistern` | dtc | `G8` dead-share **0.854** · `GO3` **7** · `RQ2`, a studio-side crash |

**`GO3` reading 7 on three of the four is one fault, not three.** Under `rot_180` the two images of a
paired goal are 7 blocks apart only if the goal sits essentially on the symmetry line, which means
both teams' objectives are stacked on top of each other in the middle of the board.

**The `RQ2` is the studio's own and is worth fixing.** `RoomPart.At(int step)`
(`src/PgmStudio.Minecraft/Houses/RoomPart.cs:27`) throws a `NullReferenceException` when
`HouseStyleValidation.CheckOres` walks a room style whose parts are not all stated, so an
incomplete `roomStyles` 500s instead of raising a finding.


### Sonnet 5 — four authored boards, one of each objective shape (2026-09-21)

One `dtm`, one `dtc`, one `ctw` and one `ctw + dtm`, decided together so no two are the same board's
arrangement in different blocks: two landscape boards on a flat lane, two built quays on a hub-and-spur.
Every board carries its own tone family — pale chalk, warm peat, grey stone, red earth — checked across
the set rather than within it. All four exported at 0 props declined and export gate OPEN on the drive
that shipped.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `sonnet5b-white-scarp` | dtm | Sonnet 5 | **A wind-scoured chalk down where the beacon monument stands alone on open sward** — `White Scarp Beacon`, 44 blocks from its own spawn and 146 from the enemy's for a `GO1` of **3.32**, 102 between the two monuments (`GO3` 85–150). A quarry cut (an `area` relief mark sunk to y4) closes the south flank, a pine-planted knoll (a `push`) the north; the ground is one theme, slope-banded turf → coarse dirt → sandstone at 20°/40° off its own `incline`. **9644 walked · 12 scrambled · 8 barrier · 2 faces**, 18 props placed and none declined, 27.4% dead (the two flank features, off the spawn↔monument route), export gate OPEN |
| `sonnet5b-turbary-cut` | dtc | Sonnet 5 | **A cut-over peat moor where the core stands on a raised turbary island with ground all round its casing** — `Turbary Core` at the vocabulary's own defaults (`float 6`, `leak 5`, `lava 3`), the same 44/146/3.32 geometry as `white-scarp` because the same lane satisfies `GO1`/`GO3`/`GO4` for either objective kind. A drained cutting (`area`, y2) west, alder scrub on a turbary mound (`push`) east; podzol-over-dirt turf, a coarse-dirt wall bucket so the cut bank reads as turned earth rather than quarried stone, **Swampland** biome set after the drive via `PUT /sketch/biome` and re-exported by hand. **9644 walked · 8 scrambled · 12 barrier · 2 faces**, 18 props placed and none declined, 43.0% dead, export gate OPEN |
| `sonnet5b-ropeworks-quay` | ctw | Sonnet 5 | **A fishing harbour where each wool sits in a stone cellar defended from its corner** — three faces on void, one bedrock wall on the `approach`↔`yard` interface (never the room's own edge, `PL13`), twenty blocks wide and about sixteen in front of the door (`ST8`). Strait 32 blocks (`CT12` 15–40), frontage 64 (`FR9` ≥15). Flat built yard — no relief at all, per `match-flow.md` §10.1's "ground is built, not landscape" — grass/gravel/cobble slope bands, a timber ropewalk shed standing off the quay road. **22688 walked · 0 scrambled · 0 barrier · 0 faces**, 18 props placed and none declined, **3.3% dead**, export gate OPEN |
| `sonnet5b-highgarth-fell` | ctw + dtm | Sonnet 5 | **A red-earth hill-fort where each team holds an exposed beacon and carries a wool out of a buried grain-store** — the same corner-room-and-wall arrangement as `ropeworks-quay`, carrying `Highgarth Beacon` in the yard at 48/174/3.625 (`GO1`/`GO3`/`GO4` all in band) after two rounds of resizing: a CTW-length yard put the beacon's `GO1` at 7.32 and `GO3` at 278 on the first geometry, so the whole spawn-to-strait depth was shrunk from 166 to 94 blocks rather than the beacon moved alone. Red sand and red sandstone, the run's reddest tone family, grass-tinted default biome. **13472 walked · 0 scrambled · 0 barrier · 0 faces**, 16 props placed and none declined, **1.2% dead**, export gate OPEN |

**Open question, recorded rather than filed:** whether a combined wool-and-monument board should prefer a
short strait (the destroy geometry's floor) or a long approach chain (`approaches.md`'s "wool belongs
behind") when the two pull the plan's depth in opposite directions — `sonnet5b-highgarth-fell` answered
it by arithmetic on the numeric bands rather than by asking, and `reports/sonnet5b-run1.md` carries it.

---

### Opus 5 — four boards, one per objective shape, decided together

Four boards written as four sentences before the first shape was drawn, so that no two would be one
arrangement in different blocks: a destroy board that is one wide piece with the relief doing all the
work, a core board that is four height zones with ramps cut through its risers, a wool board that is four
limbs round a T of void, and a mixed board that is a delta with a channel through it.
[reports/opus5b-run1.md](reports/opus5b-run1.md)

**The tone families were checked across the set rather than within it.** The ground is pale chalk, cold
slate, red mesa clay and dark wet carr; what is built is dark timber on cobble, dark timber on brick
under a red roof, pale sandstone and birch, and white plaster framed in dark oak. No two boards share a
ground family and no board's buildings are in its own ground's family.

**`G8` is what shaped three of the four, and it asks two different questions.** On the destroy boards it
reads `dead-share` — ground no journey passes — and Chalkmere went 0.272 → 0.155 → 0.131 → **0.0957** as
the board narrowed from 72 to 48 and the band behind the spawn from 24 deep to 16. On the wool boards it
reads `fill-ratio`, which is land over the fanned bounding box, and it wants a board **less than 54% solid**.

**That second term and `approaches.md` pull opposite ways on a board played for a wool and a monument.**
The capture half wants void inside a team's ground and the destroy half withdraws it, and the only cut
that satisfies both is one that reaches the mid — a channel rather than a hole. Alderquay is built on
that reading and it is a judgement rather than a measurement.

| Folder | Mode | Author | What it is |
|---|---|---|---|
| `opus5b-chalkmere` | dtm | Opus 5 | **A chalk downland split by a dry combe** — one obsidian `pillar-3` a team at `(14, 62)` on an open turf shoulder, own walk 48 against 167, ratio 3.48. The ground round it is composed rather than decorated: a pinned combe five blocks down with a dew pond in it is the way in from below, an eleven-block push east is the way in from above, a five-beech shaw carries cover to within fifteen blocks, and the strand is open. Two halves joined by a build zone over 16 blocks of void across the whole 48-block face. Three themes on a **slope** stack cut at 20° and 38° off its own incline, `Plains` biome, a drystone yard wall drawn as two polylines. **9 324 walked · 382 scrambled · 0 barrier · 0 faces**, 30 props placed and none declined, 9.6% dead, export gate OPEN |
| `opus5b-slakefell` | dtc | Opus 5 | **A slate fell in three benches over a frozen tarn** — the core in a walled fold on the middle bench at `(-14, 48)`, `float 6` and `leak 5`, ground on every side of it, own walk 49 against 151. The benches are pinned flat with three-block gaps, so each riser is a face — 52 barrier cells in four faces and nothing else — and four `line` marks with a height at each end are the ramps cut through them, two to a riser on opposite hands, every one reading worst step 1 on a transect. `Ice plains` so the snow and the grass agree; buildings in dark timber on a brick plinth under a brick roof, the one warm thing on the board. **8 558 walked · 608 scrambled · 52 barrier · 4 faces**, 28 props placed and none declined, 6.7% dead, export gate OPEN |
| `opus5b-ochredrift` | ctw | Opus 5 | **A red mesa mining camp over a dry wash** — two wools a team on spurs at the far corners, each room with three faces on void, each spur's mouth carrying sixteen blocks of bedrock twenty in front of the room's face. A notch between the two frontline legs meets a slot across the hub, so the middle of a team's own ground is one T of void nothing bridges, and the only land joining the wash to the hub is sixteen blocks at each end with a ramp cut through it. The crusher terrace is `relief_scope: exclude` and meets the hub at a 64-cell face, with a twelve-block flight of six two-deep treads cut into it. `Mesa` biome so grass and podzol read as one dry floor. **11 118 walked · 318 scrambled · 128 barrier · 2 faces**, 28 props placed and none declined, **0.0% dead over 21 journeys**, export gate OPEN |
| `opus5b-alderquay` | ctw + dtm | Opus 5 | **A dark alder holt on a delta channel** — one obsidian monument a team in the open on the bank above a timber quay at `(30, 52)`, own walk 53 against 187, and one wool on a spur at the back behind a sixteen-block bedrock line. The map declares both gamemodes. The void here is a channel that reaches the mid rather than a hole inside the team's ground, which is the only cut `approaches.md` and `G8` both allow; a pinned backwater on the west bank is the entrance from below. The quay is two made layers, because one layer holds one span per column and the posts under the deck are simply not in the world otherwise. `Swampland` biome, white-plaster buildings framed in dark oak. **8 440 walked · 90 scrambled · 0 barrier · 0 faces**, 32 props placed and none declined, 1.6% dead, export gate OPEN |

## Not boards

Folders under `maps/` or `specs/` that exist for a reading rather than for a game. They are named
here so `tools/boards-check.py` can tell them from a board nobody wrote up.

| Folder | What it is |
|---|---|
| `band-suite` | a probe suite: one band axis per panel, driven to read the slope bands back |
| `crossing-suite` | a probe suite: one crossing per panel, driven to read what a hop costs |
| `geometry-showcase` | a world built to look at shape geometry, not to be played |
| `probe-ashfield-1` | a biome probe world: ashfield, tint read back off the chunk's biome byte |
| `probe-ashfield-2` | a biome probe world: ashfield, tint read back off the chunk's biome byte |
| `probe-badlands-1` | a biome probe world: badlands, tint read back off the chunk's biome byte |
| `probe-badlands-2` | a biome probe world: badlands, tint read back off the chunk's biome byte |
| `probe-desert-1` | a biome probe world: desert, tint read back off the chunk's biome byte |
| `probe-desert-2` | a biome probe world: desert, tint read back off the chunk's biome byte |
| `probe-plains-1` | a biome probe world: plains, tint read back off the chunk's biome byte |
| `probe-plains-2` | a biome probe world: plains, tint read back off the chunk's biome byte |
| `probe-snowfield-1` | a biome probe world: snowfield, tint read back off the chunk's biome byte |
| `probe-snowfield-2` | a biome probe world: snowfield, tint read back off the chunk's biome byte |
| `rockymine-probe` | the author's own probe spec |

## Not yet written up

A board lands in `maps/` and `specs/` the moment it is driven, and its entry above is written by the
run that built it (`AUTHORING-BRIEF.md` §6). These predate that rule and have no entry yet.

**The list is the debt, carried in the open rather than discovered again later.** A slug leaves it by
getting a row above, written by somebody who knows what the board turned out to be — `reports/` says
what most of these runs were for, and reconstructing the column from a report is how a log comes to
describe boards that were never quite like that.

`opus5-basaltmere` `opus5-birkmire` `opus5-burrowgate` `opus5-clints-scar` `opus5-corbel-scar`
`opus5-crossdyke` `opus5-drystone-ring` `opus5-dustwath` `opus5-eaveswick` `opus5-fallowgate`
`opus5-flintwick` `opus5-gallowsholt` `opus5-garsdale` `opus5-grykefell` `opus5-harrowgate` `opus5-hollowbeck`
`opus5-hushwater` `opus5-kettleshulme` `opus5-longstrand` `opus5-medlock-drift` `opus5-mirkholt`
`opus5-mootgate` `opus5-netherby` `opus5-ochrepans` `opus5-orchard-holm` `opus5-oxenholme` `opus5-peatgarth`
`opus5-portway` `opus5-potsherd` `opus5-quadrangle` `opus5-ravenstone` `opus5-redmarl` `opus5-revetment`
`opus5-sallowmere` `opus5-sallyport` `opus5-scarp-mask` `opus5-scarrow-delph` `opus5-skelwith`
`opus5-slakemoss` `opus5-sparholt` `opus5-stavelbridge` `opus5-thornwaite` `opus5-thrushgate`
`opus5-thwaite-ghyll` `opus5-whitegape` `opus5-widdop`
