# Opus 5, run 4 — how an agent actually drives the studio, and the one driver

Four boards authored end to end through the live HTTP API in a cloud container, against `pgm-studio` at
`claude/b253-agentic-map-authoring-xbxdd4` (18 Aug 2026). This run's subject is `B253` — *how a model
actually drives the studio* — so the boards are the evidence and the loop is the finding.

**The four are of my own design rather than named briefs**, one per objective shape the system can carry:

| Board | Mode | Is | The thing it was built to test |
|---|---|---|---|
| `opus5-wheal-hazel` | `ctw` | a granite tin works either side of a shingle bar | the `path` **shape** as terrain, and a water lane as a *late* second crossing |
| `opus5-alabaster-rake` | `dtm` | a gypsum badland under a mesa | erected terrain as an obstacle, and a depression as the withdrawn hole's replacement |
| `opus5-siderite-bowl` | `dtc` | an impact crater with its ring behind the bowl | `scarp` marks, a per-vertex `push`, and a flat-roofed building run as a boundary |
| `opus5-hollowbank` | `ctw` · `dtm` | a chalk ring-fort | a board carrying two objective kinds, and `layered` **inward** at board scale |

All four load: two teams, two spawns, real objectives, the right `<gamemode>` label, an `<author>`, no
placeholder in a goal name, `map.xml` 6.3–9.5 KB. All four finish with **nothing declined**.

---

## 1. The loop, as it is actually driven

This is `B253`'s first question — *what every driver had to do itself* — answered by writing the seventh one
and then deleting the need for an eighth. `tools/drive.py` is now the whole of it and `tools/README.md`
documents it; `tools/drive.ps1` is retired.

```
POST  /plan/evaluate      <plan>          score, valid, the hard/soft terms, the WHOLE lint table
POST  /plan/inspect       <plan>          goalDistances (GO1), islandGaps (CT12), the wall rects
POST  /plan               {"name": …}     → {slug}
PUT   /map/{slug}/plan    <plan>
POST  /plan/compile       <plan>          → {layout, intent, warnings}
      ── patch the compiled layout: themes by shape id, relief_scope, controls, addShapes, relief,
         roomStyles, dressing ──
PUT   /map/{slug}/sketch/from-plan  <the patched layout>
POST  /map/{slug}/sketch/relief/read      cells, low, high, symmetry error, per island
POST  /map/{slug}/sketch/finish
PUT   /map/{slug}/intent/from-plan  <intent>
POST  /map/{slug}/sketch/columns    <layout>   the DR-* declines   ← AFTER the intent
PATCH /map/{slug}/metadata  {name, authors}                        ← AFTER the intent
GET   /map/{slug}/export                  → the world
```

**Two of those thirteen calls are new to this run, and both are ordering facts nothing documented.**

`POST …/sketch/columns` is where a driver learns which props the dressing pass will decline, and it must be
asked **after** the intent is stored: `DR-KEEP` reads the spawn doors' approaches and the goal rings, which
do not exist on a map carrying only a sketch. Measured on `firnline`, rebuilt as a smoke test: three declines
asked before, four asked after — and the fourth is a whole house.

`PATCH …/metadata` must also come after, for a different reason. Storing an intent **projects the map
document from the intent's own `meta`**, and a compiled intent's `authors` is empty. `intent/from-plan`
carries authors from a *previously stored intent*, so a first build has nothing to carry and any name written
earlier is silently overwritten. Every board in this run wrote `<author>` only once that was found.

### What every earlier driver had to do itself

Six drivers exist in this repository and none of them is a subset of another. What they all had to invent:

| The thing | Where it lived, six times |
|---|---|
| the call order | hand-written in each, and two point at ports nothing serves |
| the fan of a `@style` reference into a document | `drive.py`, `build.cs` and `world-build.cs` each resolve it differently |
| patching the compiled layout by **height** vs by **id** | `drive.py` by height; the `build.py`s by height with per-map dictionaries; `build.cs` not at all |
| the look-before-you-build step | only `drive.py` had one, and only for `relief/read` |
| what to do with a `warnings[]` | **nothing, in all six.** Every driver read the status code and dropped the findings |

That last row is the finding. The pipeline has been answering with rule ids for several runs and no driver
printed them, which is why the same six declines were re-discovered by hand each run. The new driver prints
every finding at every one of the four places one can appear, and stops on a refusal instead of carrying on.

### One place a driver still cannot reach, and it is not the driver's fault

`OB17` and `OB19` are **refusals raised by the export**, not dressing complaints, so the first time a board
hears about them is `GET …/export` answering 409 — after the whole world has been built. Both fired on this
run, three times between them, at a cost of three full build cycles. Nothing in `sketch/columns` or
`plan/evaluate` predicts either. A pre-flight that answered the export's own objective gates over the
rasterized ground would remove the most expensive round-trip an author has.

---

## 2. How an agent looks at a map

`B253`'s second question. The honest answer is that **an agent looks at four kinds of picture and one kind of
number, and one of the four did not exist when this run started.**

**The theme swatch, before anything is built.** `POST /terrain/theme-preview?format=png&view=surface|section`
answers a raster an agent can open. Three of this run's first-draft themes came back as a *flat colour* and
looked fine as a status code: `noise` takes `stops` and not `palette`, `voronoi` takes `bands` and not
`palette`, `checker` takes `even`/`odd` and not `a`/`b`. A missing required field renders the default at
**200**. Looking at six swatches side by side also caught three things no field check would: a moor that was
one flat green (grass alone, `AD-P3`'s named failure), a works floor whose two greys were indistinguishable,
and a mesa painted the same two tones as the pan below it. All three were fixed at preview cost.

**The building section.** This is the one that did not exist. `AD-S6` and the reviewer's `C14` both say to
look at a house in section before it stands on a map — and the five `*-styles/preview*` routes answered
SVG-inside-JSON only, silently ignoring `?format=png&view=`. Fixed this session. Looking at six sections
immediately caught two rule breaks that would have shipped: every verge was a spruce **log**, which `AD-M4`
forbids, and the style fork was repainting `wall` and leaving `storeys[*].wall` in the preset's material, so
the wool cage came out timber over stone brick. Neither is visible from above.

**The prop preview**, for a multi-wing building, which refuses `HJ*` before a build rather than dropping the
prop during one. Its body is `{propJson, themeJson}` with the documents as **strings** and a house prop's
`style` resolved to a full `HouseStyle` — not the unwrapped document `capabilities.md` describes.

**The world read-backs**, after the build, and the split between them matters. `--topdown` answered *did the
shape come out* — the hoodoo picket as five discs, the shaft as a hole, the inlet as a bay. `--heightmap
--contour` was the most useful single image of the run and answered *is there any three-dimensional design
here*: on `siderite-bowl` it shows the bowl, the ring behind it, the breach through the ring and the ejecta
falling away, which is the entire board in one picture. `--surface` answered *does the paint read* and caught
`hollowbank`'s map theme painting zero cells. `--section` answered what nothing else can — the hoodoos'
strata, the stilts under the picking shed, the sunk shed sitting in its hollow.

`--column` is the only honest read and was used to settle every claim in the four reviews: the core's lava
between its two obsidian courses, the sky markers above the cap, the void inside every subtract, the leat's
solid column proving it is a causeway and not a span.

**And the numbers, which are what actually shape a board.** `POST /plan/evaluate --dry` was run dozens of
times per board with no map row and no build. On `alabaster-rake` it moved the design rather than the
document: the monument was authored on the open pan and `goalDistances` read a ratio of 1.875 against `GO1`'s
3.0–4.0 band, which is not a placement error — it is the board saying the goal is in the contested space
rather than a short walk forward of the spawn. Moving it to the brow gave 3.22 and produced the topology
`approaches.md` describes. **The evaluator taught the composition.** Same story on `siderite-bowl` (2.82 →
3.0) and `hollowbank` (2.38 → 3.5).

---

## 3. How provenance is used

`region/provenance.json` is a **census of what landed**, and since `B252` each owner is `{kind, unit, image}`
rather than a `kind:id` string — the PowerShell census in this repository's `README.md` reads the old shape
and no longer works.

Read as `Counter(o['kind'])`, it is the four-second answer to *did every prop I authored stamp*, because a
unit that landed nothing has no row at all:

| Board | owners |
|---|---|
| `wheal-hazel` | house 8, tree 12, boulder 8, path 6, flora 2, water 2, spawn 2, ironcube 2, roomfloor 2, wool 2, redstoneline 2, wall 2 |
| `alabaster-rake` | house 8, tree 6, boulder 6, path 6, destroyable 2, spawn 2, ironcube 2 |
| `siderite-bowl` | house 8, boulder 10, path 6, core 2, spawn 2, ironcube 2 |
| `hollowbank` | house 6, tree 12, boulder 6, path 6, destroyable 2, wool 2, wall 2, spawn 2, ironcube 2, roomfloor 2, redstoneline 2 |

Every count is exactly `units × orbit order`, which is the check. The smoke rebuild of `firnline` reads
`house 4` for three authored houses — two units × two images — and that missing unit is the `DR-KEEP` decline
above, found from the census before the decline read was written.

The **other half** is `region/dressing-report.json`, which answers what did *not* land. It was written into
the export's temp folder and never added to the zip, so an HTTP caller had never seen one. Fixed this session;
all four of this run's worlds ship without one, which is the correct answer — the file exists only when
something dropped.

---

## 4. What I could not say

| # | What I wanted | What I looked for | Verdict |
|---|---|---|---|
| 1 | a wall of terrain nobody may bridge over | `capabilities.md`'s "an erected cube as a blocker … above the cap". The cap is `BuildCeiling.Of(highestGround)` and `highestGround` is `terrain.SurfaceTop.Values.Max()` (`SketchWorldBuilder.cs:114`) — an erected shape **is** a terrain column. A picket at y43 wrote `<maxbuildheight>64</maxbuildheight>` | **missing** — the composition is unreachable, and `capabilities.md` describes it in the present tense. A gameplay question for the author, filed below |
| 2 | a hole inside one of my own plan pieces | a `buffer` over the piece. It is inert by design ("a buffer over a generating piece is inert") | **missing at the plan layer**, present at the layout layer as a `subtract` — and `/plan/evaluate`'s `G8 fill-ratio` therefore measures a board denser than the one that gets built. Every board here fired `G8` and none of them is as solid as it says |
| 3 | a real span over a hole | an `override: true` add over a `subtract`. It fills its column from `floor` rather than spanning | **out of reach** — the mechanism is `layers[]` with a `base_y`, which the run rules exclude. Not a gap; a documentation gap about which instrument does which |
| 4 | to know which prop the dressing pass would refuse, before building | `sketch/columns` answers `DR-*`; `OB17`/`OB19` are export refusals and appear nowhere earlier | **out of reach** — the mechanism exists at the wrong end of the pipeline |
| 5 | a bare author name | `PATCH …/metadata` `{"authors": ["Opus 5"]}`. An entry with no `uuid` is skipped **silently** (`WriteEndpoints.cs`) | **mistaken, mine** — PGM's contract is a uuid with the name as a comment. `ART-DIRECTION.md` AD-M10's `["Fable 5"]` form is `tools/mapgen`'s spec shorthand and does not exist on the HTTP path |
| 6 | `LN1` satisfied on a plan-authored wool lane | the band is 10–20 blocks; `ST8` wants the wall ~15 in front of the room's entrance, which is three cells of approach at `cell: 5`, and a room is two or three more | **missing** — the two rules cannot both be met. Shortening the lane to satisfy `LN1` fired a hard term instead (score 2 → 1000). Shipped outside `LN1` and said so |
| 7 | to move the observer off my board | no marker, no control — `flow.md` says so. `globals.observerY` is honoured when hand-authored | **out of reach from the canvas, reachable from a document.** Left at the default it stamps a bedrock pad at `surface + 15` over the origin, which on `wheal-hazel` was the middle of the contested bar |

---

## 5. What I got wrong

**I read the traversability map before reading `B99`, and nearly redesigned a correct board.** `hollowbank`
reports 2 isolated markers — both wool rooms — and the obvious reading is that the approach wall seals the
lane. `B99` measures the real cause with numbers: the renderer's ground search steps past decoration and its
headroom test does not, so the **cobweb course** capping every wall reads as impassable. The gate navigates
on `Membership` with no headroom test and passed the board. `wheal-hazel` reads 0 only because its lane has a
second seam. The reviewer brief warns about exactly this and I still had to be caught by it.

**I claimed the leat was an aqueduct before probing under it.** It is a causeway: an override-add fills its
column from `floor`, so the shaft it "spans" is plugged where it crosses. `(−28, 43)` reads solid stone
y1..y8. One `--column` corrected a sentence that had already been written.

**Three of four L-plans were refused the first time, all for the same reason.** A roughly square hall ties
its ridge `AlongX`; a wing meeting it on a vertical shared edge also runs into that edge; both-into-it is
`HJ4`. `GENERATION-NOTES` §13 says the roles are ridge-derived and I still drew three of them wrong before
stating the **hall's** ridge explicitly.

**I invented five material field names out of five.** `palette` for `noise` and for `voronoi`, `a`/`b` for
`checker`, `inset` for a `layered` axis, `{id, data}` for a `teamTint`. `GET /terrain/patterns` names every
field with its type and its `required` flag and answers in one call. Reading the C# type name and guessing
the JSON is the failure mode, and it cost the first build of every board.

---

## 6. What worked first time

- **`anchor_heights` tilts.** Seven on this run — two causeways, two crater ramps, a shelf, a leat tail, a
  breach ramp — every one right first time and every one visible in a section. Four numbers per shape.
- **`relief_scope: hold` on the built tiers, one tier free.** Crisp terraces against solved ground, on all
  four boards, with no seam to author.
- **The `scarp` mark.** `siderite-bowl`'s crater face is a *grade* — `high 9, low 6, face 2, band 6` — and
  the ground arrives at the lip through six blocks of fall rather than stepping off it. First try.
- **A `push` with per-vertex `amounts`.** The ejecta blanket sits on top of the scarp's solved surface
  instead of arguing with it, which is the whole difference between a push and a mark, and it behaved
  exactly as `capabilities.md` says.
- **Bézier `controls` under GENERATION-NOTES §11's rule.** Fourteen bowed outlines across four boards, zero
  self-intersections, zero lobes, because the rule (`t·|d| ≥ bulge`, `bulge ≤ 0.35·|d|`) was applied
  mechanically and the flattened ring was tested for crossings before anything was posted.
- **The two-file spec.** A `PlanModel` plus a finish keyed onto the compiled layout by **shape id** is a
  complete map in about 25 KB of JSON, and the id key is strictly better than the height key the earlier
  drivers used — two pieces at one height fuse into one shape and a height cannot tell them apart.
- **`prop-preview` refusing an uncomposable building.** Once the request shape was right it answered every
  `HJ*` before a world was built, which is `fable-run3`'s fix #2 doing exactly what it was for.

---

## 7. Open gameplay questions

Recorded, not filed as facts. This session had no human oracle.

1. **Should erected terrain count toward the build ceiling?** Today it does, which makes a wall of terrain
   raise the cap twenty blocks above itself and hands the whole board a ceiling it did not ask for. If the
   answer is no, `SketchWorldBuilder` should measure the ceiling over terrain that is *not* `height_mode`-
   erected and `capabilities.md`'s blocker composition becomes real. If the answer is yes, `capabilities.md`
   should stop describing it. I built at a bridgeable height and said so.
2. **Should a late-opening water lane share the frontline the early crossing uses, or a different one?**
   `wheal-hazel` puts them 40 blocks apart so the endgame is fought on new ground. Unverified.
3. **Is a hole inside a team's own land legitimate on a capture board?** The withdrawal is stated for
   `dtm`/`dtc` only. `wheal-hazel`'s flooded shaft is a rotation device inside the works rather than a
   barrier across an approach; if the withdrawal generalises, it is wrong.
4. **Should the defence's route to its own goal be the one the attack uses?** `siderite-bowl` gives them
   different ones — a breach behind the ring for the defence, a shelf on the flank for the attack.
5. **On a board carrying two objective kinds, should the two jobs compete for the same players?**
   `hollowbank` is built so they do. It may simply play as two half-maps.
6. **How deep and how close should a depression near a goal be?** `approaches.md` names the instrument and
   gives no numbers. `alabaster-rake`'s is 22 × 14 and about 4 deep, 10 blocks off the goal's brow.

---

## 8. Five defects found and fixed in the studio this session

Each was hit while authoring, each is small, and each mislabelled a document fault as the studio's own or hid
an answer an agent is told to look for. The last two were found by measuring another model's run rather than
my own, which is worth saying: a board that looks built and is not is exactly what a silent gate produces.

| # | Found | Checked | Verdict |
|---|---|---|---|
| 1 | a theme carrying a material with no `kind`, a `layered` with no `stack`, a `checker` with no `even`/`odd`, or a `teamTint` with no `neutral` answered **500 `RQ2` — "the fault is its own rather than the document's"** | `DeserializeMaterial` already translated the missing-discriminator `NotSupportedException` into a named `JsonException`; the *theme* and *style* readers did not, so a nested one escaped. The three patterns null-dereferenced at paint time, which is per column, so a whole request died. `flow.md`: *"A body that cannot be read is refused, never crashed"* | **missing** — **fixed**: the translation is written once and shared by the theme and style readers; the three records fall through the way `VoronoiMaterial` already did, so the reader's `unread` walk names the field that was written instead. All four now answer 400 by name |
| 2 | `GET /map/{slug}/export` never shipped `region/dressing-report.json` | `MapExportEndpoint.BuildWorldZip` calls `DressingReportFile.Write` into the temp region dir and then adds only `provenance.json` to the archive. `tools/mapgen` writes into a real directory so it survives there; the HTTP path deleted it with the temp folder. The decline record is the only account an HTTP caller gets of a dropped prop | **missing** — **fixed**: both sidecars travel |
| 3 | `/room-styles/preview`, `preview-snapshot`, `/roof-styles/`, `/storey-styles/`, `/porch-styles/preview` ignored `?format=png&view=` and answered SVG-in-JSON, dropping the query rather than refusing it | `PngAnswer` is already shared by the three terrain previews. `WorldViews.Plan`/`Section` were `SvgRaster.Raster` calls that could have been `CellRaster`s, which carry both encodings by construction — the type's own docstring says that is what it is for. The one preview family that draws a **building** was the one an agent could not open | **unreachable** — **fixed**: `Plan`/`Section` return a `CellRaster` and the string methods delegate; `?format=png&view=plan\|section` answers raw PNG and `isometric`/`cutaway` are refused by name, since both draw a block as its own shape and have no raster to encode |

| 4 | A shape naming a theme the layout's registry does not carry produced **no warning at all**, on either write path | `SketchLayoutCheck` reports a shape kind nobody has, a mirror mode nobody has, an island listing a shape id the layout does not carry, and a relief keyed to an island that does not exist — a **theme** name matching nothing is the same class and was not in the list. Those cells silently take the map default, so the board looks built | **missing** — **fixed**: reported as `SK3`, once per name rather than once per shape, and the map default is checked the same way |
| 5 | `PUT …/sketch/from-plan` answered `{ok, orphaned}` and ran no document gate, while the plain `PUT …/sketch` ran one and returned its `warnings` | The merge path is the road every headless driver takes — all six of them, and `tools/mapgen` besides. So the one road nothing was reported on was the only road anybody drove | **missing** — **fixed**: the same gate now runs over the **merged** document, which is the one actually stored, and its complaints ride back with `orphaned` |

**How fault 4 was found is the part worth keeping.** Not by reading the code — by measuring the delegated
Haiku run's four boards against its own report. Every shape on all four names a theme like `t0`, and the
layout carries no `themes` registry at all. The run believed its boards were themed; the pipeline had every
opportunity to say otherwise and said nothing, on both write paths and on the columns read. Four boards
shipped unpainted for want of one complaint.

And one **documentation** defect left for the author because its resolution is a design call, not a fix:
`capabilities.md` describes a shape erected above the build cap as an obstacle nobody bridges, and the
ceiling rule in `plan.md` (`G6` amendment 14 — twenty blocks over the highest ground the world builds) makes
that unreachable for anything made of terrain. Both documents are internally correct; together they promise
something that cannot be built. Open question 1 above is the decision that settles which one changes.
