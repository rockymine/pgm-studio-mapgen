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
techniques/<card>/                    one instrument, its variants side by side in one world, with the reads
corpus/                               hand-built worlds nothing can re-derive — the tree corpus
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

## The boards the cards add up to

`maps/opus5-whinnymoor` is the board built out of the techniques one at a time, and
`review/opus5-whinnymoor.md` says which of them each part came from.

`maps/opus5-sandcaster` is the destroy board built on top of that: 110 × 400, three land regions on one hue
axis, a chasm down the middle and a tiled service corridor under the reef — two sketch layers, forty-two
brush strokes and two monuments, one of them twenty blocks underground. `maps/opus5-sandcaster-ii` is the
same brief on one open landmass: a mountain range drawn with pushes round a dale 32 blocks wide, no chasm
anywhere, and the workings moved under the middle of it.

`maps/opus5-ravensmere` is the single-layer one: a mere with a group in the middle of it, a beach thirty
blocks deep round that, rolling downs cut by three crevasses, a wood, a brick-and-granite path with cottages
off it, and a range standing behind each spawn. `maps/opus5-thornfell` is the same technique on a capture
board: void down the middle, two wool rooms hung off the back of each half on spurs a raider walks out along,
and a range behind every one of them.

## The technique cards

`techniques/` is one card per instrument, each a complete world holding its variants **side by side** so the
comparison is the lesson. **Twenty-three exist, which is all of them** — from outlines, overlapping shapes and
Bézier rings through pushes, stacked layers, water and the theme buckets to what a shape must say before it
owns any paint, on to sculpture built out of nothing but shapes and a board somebody else arranged.

**One of them compares the tiers rather than working an instrument.** `raising-a-lane` puts the same L-shaped lane up
eight blocks seven ways — by the plan, by the layout, by the relief and by a storey over it — and measures
what each climb costs a player and what the corner does to it. Each commits the text reads that prove its claims and names no past map.
[techniques/README.md](techniques/README.md) indexes them; a new card is written when a new instrument
lands.

**One world a card, with the variants in it, is what the cards settled on.** A teaching set of one board per
technique was here first and the diff between two boards was meant to be the lesson; putting the variants
side by side in one world made the comparison the lesson instead, and made a card's claims measurable in
reads taken over the same ground. `taking-over-a-composed-board` is the one exception and says why: four
compiles of one plan cannot share a world.

## Sculpting with layers

The sketch tool's layers were built to stack storeys, and they hold rather more than that: a layer is one
arbitrary height field, so a dome is eleven circles on one layer and a thirty-block statue is eight layers
of rectangles. [SCULPTING-WITH-LAYERS.md](SCULPTING-WITH-LAYERS.md) is the account — the six facts that decide
how far it goes, the four limits, and what could become a tool. `sculpture/` holds the two galleries it was
written from and `maps/opus5-automaton` is a played board furnished with them.

`techniques/sculpture-with-layers` is the worked card beside it, and it is the **ladder** rather than a
catalogue: one shape, a polyline, four layers, rings for a field that will not nest, and a solid put through
`tools/sculpt/layers.py` — twenty made things on one board with the columns that measure each rung. The
forms in `sculpture/forms` are what one early exercise reached for and are not a vocabulary to stamp from.

## Authoring a map here

**[ORDER-OF-WORK.md](ORDER-OF-WORK.md) is the one page that is read before anything is posted** — the nine
decisions a board is made of, in the order they are made, and the four that cannot be taken back. It explains
no instrument; it says when each one is reached for and what is unrecoverable if it is reached for late.

**[WHAT-A-BOARD-IS-MADE-OF.md](WHAT-A-BOARD-IS-MADE-OF.md) is the author's ruling on how a board should
look** — the paint, the buildings, the ground cover, the seam where made ground meets grown ground. Nothing
in it is enforced by any gate, which is why it is written down.

**Then the API, and three documents opened at a question.** [AUTHORING-BRIEF.md](AUTHORING-BRIEF.md) is what
an authoring agent is given, end to end.

[GENERATION-NOTES.md](GENERATION-NOTES.md) is what the API cannot state about itself — a fact about how two
correct mechanisms interact, a number no gate checks, a read-back that lies. Where a technique card
demonstrates an instrument, the notes state the claim in a sentence and point at the card rather than
repeating it.
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

**What that agent reads first is being reconsidered.** [CORPUS-DIAGNOSIS.md](CORPUS-DIAGNOSIS.md) measures
the reading list, says what is wrong with it in three parts, and recommends a split. It is a handover for
that work and is not itself an instruction to an authoring agent.

## Maps

Every board built here is logged in **[BOARDS-BUILT.md](BOARDS-BUILT.md)**, grouped by the run that produced
it: what the run was for, what each board turned out to be, and the report that followed it. It is a log and
it is appended to, which is why it is not here.

**Sixty spec folders sit directly under `specs/` and 118 more under `specs/archive/`.** The flat set is the
one worth reading; the archive is a record rather than a catalogue of examples — probes, boards built to find
the limit of one mechanism, early runs, and boards a later one superseded. The split is there because the
cheapest thing a model does is imitate whatever it opens first, so what it opens first should be worth
imitating — and for one technique at a time, `techniques/` is the place rather than either.

**Most of these specs no longer compile, and that is settled rather than pending (author).** 72 of the 127
plans here state `"plan": 1`, whose marker offsets are in cells where version 2 states them in blocks, so
`POST /plan/compile` refuses one with `PL15`. The worlds under `maps/` were built from them and are what
those boards are; migrating the plans would move every marker on 72 boards to rebuild something already
built. **A version 1 spec is the record of a world, not a thing that rebuilds** — read it, do not re-drive
it, and do not file the migration again.

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
