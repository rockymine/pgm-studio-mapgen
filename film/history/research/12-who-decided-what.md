# 12 — Who decided what: a spectrum from hand-made to model-made

Research for the history, written 27 November 2026 to answer the author's seventh instalment
(`../author-account-2026-11-27.md`, "what makes a map an 'AI map'"). Nothing here was measured afresh. Every cell is
taken from research `01`–`11`, from the reports and specs in this repository, or, for two cells, from the `pgm-studio`
history (named where used). **"unknown" means the record is silent; it is not a guess in either direction.** Cells
the author answered in the eighth instalment (`../author-account-2026-11-27.md`, same day) are marked **(his account)**:
they are his statement, not something the record shows.

## 1. How to read it

The author's point is that one studio executes everything, so the useful question is who decided. Each map is split
into seven decisions, and each cell says **who decided** and **what executed**.

| Who decided | Means |
|---|---|
| **person** | a named human (the author, rockymine, unless another is named) |
| **model** | a named model, as the credits, the trailer or the report name it |
| **algorithm** | the composer, the relief solver, the placement pass, a theme or the tree grower, fed by a seed or by defaults a person or model chose |

| What executed | Means |
|---|---|
| **studio** | pgm-studio, deterministically: its export, solver, painter, placement, refusals |
| **model script** | a script the model wrote itself (`build-spec.py`, pgmvox Python, a Grok script) |
| **browser** | the studio's browser editor driven by a person |
| **hands** | a person building in game (WorldEdit and similar) |

A decision is not "the model's" because a model typed the file. The cells below mark **model** only where the record
shows the model choosing the content, and **person** where the record shows a person stating the content and a model
only writing it down. Where both are true of one decision, the cell says so.

## 2. The spectrum in one table

Each cell is *decider / executor*. P person, M model, A algorithm; st studio, br browser, ms model script, ha hands,
? unknown. The per-map tables in §3 carry the evidence; this table is the index.

| # | Map (date) | concept | layout | terrain | colour | structures, decoration | objectives, XML | finishing | Category |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Author's ice map (Nov) | P / ha | P / ha | P / ha | P / ha (his account: snow, stone, ice or grass, undecided) | P / ha | P / ha, XML none | P / ha (his account: he builds it to the end) | 1 |
| 2 | Vauxite, Drastic Change II (24 Jun) | P (his account) | ? | P (his account) | P (his account) | ? | P / br then ha | P / ha | 1 |
| 3 | Bridgid II (14 Jul) | P (his account) | P / br | P (his account) | P / ha | ? | P (Ruediger, his account) / br, then ha for the water lane | P / ha | 1 |
| 4 | No Blocks Placed (7 Aug) | ? | P / br | P / br, st | ? / st | A / st, P / ha | P / br, st | P / ha | 2 |
| 5 | Wandering U (6 Aug, his account) | P / ? | P (described in text, his account) / ? | A / st | A / st | A / st | M (his account: Claude wrote the XML) / ? | ? | 3 |
| 6 | Base 2-Island (2 Jul) | P / – | P / M-writes, st | P / st | A defaults / st | P / st | P / st, XML ? | none | 3 |
| 7 | Capture the Cake (27 Jul) | ? | P (old map) | P (old map) | P (old map) | P (old map) | M, P / ? | P / ? | 3 |
| 8 | Millrace (30 Aug – 2 Sep) | P / br | P / br | M, A / st; P kept | M, A / st then P / ha | M then P / ha | M / st, then P (Ruediger, his account, as far as he remembers) | P / ha | 3 |
| 9 | Goldhollow (12 Aug) | M, spec | A / st (seed 41) | A / st | M words / st | A / st | A retarget / st | none; review in words | 4 |
| 10 | Gypsum Reach (28 Sep –) | M / ? | M / st | M / st | M / st, P notes | M / st | M / st | P notes, M / st | 5 |
| 11 | Whinberry Ring (12 Sep) | ? | A seed 18, M edits / ms, st | M / ms, st | M / ms, st | M / ms, st | A, M / ms, st | P feedback, M / ms, st | 5 |
| 12 | Overwall (25 Aug) | P (account) | M / ms, st | M / ms, st | M / ms, st | M / ms, st | M / ms, st | none (his account: no hand finishing) | 5 |
| 13 | Riftwater (7 Oct) | M (account: P nothing) | M / ms | M / ms | M / ms | M / ms | M / ms | P review, M / ms | 6 |
| 14 | Cedar Crossing (10 Aug) | P essay | M ("Map") / ms | M / ms | M / ms | M / ms | M ("XML") / ms | ? | 6 |

The spectrum has six categories (§5). Row 7 is placed provisionally, for the reason in its table.

## 3. The maps, one at a time

### 3.1 The author's hand-built ice map (2026, branch `claude/compassionate-cerf-fg7m17`)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person: a CTW and DTC hybrid, a bunker set into a mountain with the core in its face, an underground wool lane, a valley floor between; first made for a contest that was cancelled, so "the map is an ice map" | hands |
| Layout | person: one half, turned 180 degrees about a pivot. His account: "the map grew around the bunker facade", the lookout and stairwell added as he went | hands, with a loft tool in game that the record does not name |
| Terrain shape | person: 23 lofts, 299 lines, 1,578 points; ground median tilt 36 degrees | hands (loft tool) |
| Colouring, materials | person **(his account)**: the final material is not yet chosen, between snow, stone, ice and grass; a cold map. He builds in colour-coded wool whose colours carry meaning (grey flat floor, yellow connecting ground, light blue hills, lime retaining walls) | hands |
| Structures, decoration | person: main building, great hall, spiral stair, three retaining walls of 19, 13 and 14 blocks | hands |
| Objectives, XML | person: a core in the east facade and a wool room, as built; no `map.xml` for it is in the record | hands; XML none |
| Finishing | person **(his account)**: he will build the map to the end himself, middle included. The middle between the halves is missing in his build so far; five middle and cover variants were written by agents as scripts and he "judged them" | hands; agent scripts for the variants (not the studio) |

What the agents did is the contrast: they were asked to compose the map from his sketch world on 2 to 7 November,
and "every version was rejected". They then rebuilt his terrain as loft lines (3 blocks of 18,801 more than a block
off) and drew the variants. The studio was not used at any step.
Sources: research `04` §§1, 2, 3a, 4; `film/history/research/05` ("his own hand-built map");
`author-account-2026-11-27.md` (third instalment, the paragraph on routes).

### 3.2 Vauxite and Drastic Change II (24 June; Vauxite 1.0.1 on 1 July)

| Decision | Who decided | What executed |
|---|---|---|
| Concept, terrain, colour | person **(his account)**: "all concepts, terrain and colours are human" for Vauxite, Drastic Change II and Bridgid II | the record holds nothing on how the blocks were made; the commissioning brief says hands |
| Layout, structures | unknown from the record; the commissioning brief calls them hand-built and the record credits rockymine as author | the brief says hands; not in the record |
| Objectives, XML | person drew the regions in the browser (his account: the first maps he tried that on); the kit, `build-hole-1` ids and bare team ids are the studio export of that week | studio export, then hand editing: Vauxite 1.0.1 fixes spawn yaws, two-rectangle spawns and a build ceiling of 24, and the root `map.xml` is a hand-reformatted copy of a stray studio-written one |
| Finishing | person (the 1.0.1 revision is the "some errors" he recalls); who found each error: unknown. Vauxite and Drastic Change II were first played on 12 October, three and a half months after upload (research `13`) | hands on the XML |

Sources: research `11` §1; author's account, fifth instalment.

### 3.3 Bridgid II (14 July)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person **(his account)**; he calls it "as wild as Hello World"; credited rockymine and Ruediger_LP | |
| Layout | person: "built in practically one day … in the browser it was quick" | browser |
| Terrain shape | person **(his account)**. The studio holds a traced plan of it (16 height tiers) but made after the upload | unknown |
| Colouring | person: "skinned" from stone "in one long evening" in game; the repeating colour columns on its sides are where he dates the wall-run idea | hands |
| Structures, decoration | unknown | |
| Objectives, XML | person **(his account)**: Ruediger made the XML, much of it with the browser tool, which placed things automatically from the plan model; only adjustments such as the water lane were added by hand, and he believes the water lane was the only one. The record finds no browser trace in its XML (research `11` §2) | browser, then hands for the water lane |
| Finishing | person (the skinning above) | hands |

Sources: author's account, fifth instalment and its correction; research `11` §2.

### 3.4 No Blocks Placed (7 August)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | unknown. Credits: rockymine "Drawing pieces, shapes, and markers in the browser.", Ruediger_LP "Wisdom.", Flamiix "Minimalist." | |
| Layout | person (rockymine), pieces | browser (Plan tool) |
| Terrain shape | person, shapes | browser (Sketch tool) |
| Colouring | unknown who chose the theme; the ground is stained clay at y 13 | studio terrain painting |
| Structures, decoration | algorithm: the studio's grown-tree generator and decoration (the 50-log oak is the author's reading of the one surviving generated tree, not yet confirmed in game); person (Flamiix, his account): wool room and spawn building interiors | studio for trees; hands for the interiors |
| Objectives, XML | person, markers in the browser | studio Configure export (the map became that tool's worked example on 13 August) |
| Finishing | person: "a few blocks were placed by hand after all"; how many: unknown. TTtie added only the creation date; Ruediger added `<clear/>` | hands |

Sources: research `05` §b, `08` ("the larger tree"), `11` §3; author's account (third instalment).

### 3.5 Wandering U (tested 6 August, his account; not in either public repository)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person, his account: "wild concepts they wanted to try", a wool room that walks a lap around the U. The file names no author | |
| Layout | person **(his account)**: he described it in text; the XML's own comment says the plan was "authored at cell=1" in the studio | browser (studio plan), by whom: unknown |
| Terrain, colour, structures | algorithm: the 10 by 10 chunk of bedrock is "the entire 10x10 chunk pgm-studio stamps for the wool-room role" | studio |
| Objectives, XML | model **(his account)**: Claude wrote the XML from his text. The base is the studio's export; the variables, eight `<dynamic>` stops and countdown actions are the part the file shows as hand-written or model-written | model |
| Finishing | unknown. His account: players fell out of the world as the room moved | |

Category 3: a person states the content in text and a model writes it down. Sources: research `10` §1; `11` §3.

### 3.6 Base 2-Island (2 July, session `session_014BYG9EwhkDRUmRP1FYLBk2`)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person: "the most basic map design out there"; a test seed. The name Base is the model's | |
| Layout | person: his squared-paper drawing. Opus 4.8 misread the photo and committed a staircase; he typed the corner coordinates in five-block cells ("1,5 3,5 3,11 …") and it came out right at 09:14 | model wrote the seed JSON; studio exports it |
| Terrain shape | person: "island height for the large island would be 9, for the small island 13", build height 20, observer at 24 | studio |
| Colouring | nobody chose: bedrock floor at y 0, stone to height, the export's defaults | studio |
| Structures | person: the 8 by 8 by 8 bedrock shell for spawn and wool, specified at 23:21 on 1 July | Opus 4.8 wrote it; studio builds it |
| Objectives, XML | person placed the spawn and wool markers; whether a `map.xml` was part of the export: not recorded in research `09` | studio |
| Finishing | none: the first export crashed the 1.8 loader and the fix was his own commit. Base 4-Team was played on the server on 28 July 2026 at 00:30 UTC (2m 36s, 28 players, winner Green; research `13`); no play of Base 2-Island or Base 2-Wool is in the log | |

Sources: research `09` throughout; `13` §4; `07` §2; `../sources/base-map-squared-paper-drawing.jpg`.

### 3.7 Capture the Cake, Kuusepuu CTC (27 July)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | unknown. The header says "the DTM map with the destroyables removed and the cake objective of capture_the_cake_ctw dropped in", a map in no repository here; the author calls it a game-mode experiment | |
| Layout, terrain, colour, structures | person: an existing map by rockymine and DerStiv, unchanged by this step | the earlier map |
| Objectives, XML | model: credits "CTC conversion: Claude Opus 5"; Ruediger_LP credited for "XML" | how the conversion was run: unknown |
| Finishing | person: three revisions on 28 and 31 July; 1.0.3's comment "Reported live: a carrier died, the cake went home" is the one commit that reports play | hands on the XML |

The author says it is not an AI map. It sits here because its credit puts a model on exactly one decision.
Sources: research `06` §1, `07` §5, `11` §3; author's account (sixth instalment).

### 3.8 Millrace (30 August to 2 September)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person: he drew a basin ("Map Experiment") and had it built out | browser (Sketch tool) |
| Layout | person: the sketch's geometry is the layout | browser |
| Terrain shape | model: Opus 5's terrain was kept over two Sonnet 4.5 boards of the same basin (the record holds no written judgement of why); person: kept it, 29,954 of 35,610 columns at exactly their height after the hand finish | studio relief solver (Opus's spec) |
| Colouring | model first (studio themes); person after: "most comes simply down to better theming" | studio, then WorldEdit and Arceon |
| Structures, decoration | model first: houses, bridges, sculptures, eighteen grown trees; person after: houses and interiors redesigned (Ruediger_LP credited), a tug for the ship, sixteen showcase trees replaced the grown ones | studio, then hands |
| Objectives, XML | model: objectives kept intact by the hand finish; person **(his account, as far as he remembers)**: Ruediger reworked the XML of the published version | studio export, then hands on the XML |
| Finishing | person: rockymine and Ruediger_LP, 5 hours side by side, 10 person-hours | hands |

Fable 5.1 then diffed the two worlds and restated the revamp as documents (`specs/fable-millrace-revamp`), which
decided nothing on the published map; it also produced the studio's copied-tree form. Credits on the upload: rockymine
"layout, terrain, block palette, beautification", Ruediger_LP "interior design, houses, beautification", Opus 5
"layout composition, initial draft, sculptures, bridges". The credits give "terrain" to rockymine and "initial draft" to Opus 5; what he means by terrain is not recorded.
Sources: research `05` §c, `03` §1, `11` §4.

### 3.9 Goldhollow, one of the first fifteen (11 to 12 August; Ridgeway beside it)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | model: the spec's objective sentence is "Two monuments, two cores, and a lot of open sand between them"; who asked Opus 5 for it: unknown | |
| Layout | algorithm: the composer, seed 41, 15 a side, `rot_180`, cell 9. Whether Opus 5 walked other seeds first: unknown | studio (`tools/mapgen`) |
| Terrain shape | algorithm: relief base 6, step 1, grain amplitude 1.1 at scale 14, eight scattered rises, all seed 41; the numbers are the model's | studio |
| Colouring | model, in words: surface gold, wall sand, rim ash, fill pale stone, pattern cell | studio terrain painting |
| Structures, decoration | model states counts (150 trees of three woods, five village presets); algorithm places them with seed 41 | studio placement |
| Objectives, XML | algorithm: `objective_mode: dtcm` turns the composed capture board's wool markers into a monument and a core; the author's authors field is "mapgen". The retarget put goals "at the back of a corridor it never wanted" and was deleted on 14 August | studio export |
| Finishing | none recorded. The author's review that night is a fault list in prose, MG1 to MG13 | |

Ridgeway (seed 89, capture the wool, cell 10) has no retarget; otherwise the same. Caveat: the specs are readable at
(studio) `f7b8cb82^`; that they are exactly what produced the committed worlds is not established (research `03` §1).
Sources: research `03` §§1, 4; (studio) `tools/mapgen/specs/goldhollow.json`, `ridgeway.json`;
`BOARDS-BUILT.md`; `../../docs/tools/mapgen-review.md` as cited in `03`.

### 3.10 Gypsum Reach (28 September, Opus 5.5 on the deployed studio)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | model: the sentence "a pale desert lane where each team's monument stands in the open" was written in the run; who set the run: unknown | |
| Layout | model: a plan on the deployed studio; whether it came from the composer is not stated for this board (its pair, Sootcombe, used composed seed 21) | studio |
| Terrain shape | model states relief and the wash, mesa and oasis; person: ruled on it by notes ("flat pan, or low dunes?", note 4) | studio (relief) |
| Colouring | model chose the tone families; person: notes 56 and 65 to 69 (e.g. two broken hardened-clay lines, no orange) changed it | studio painting |
| Structures, decoration | model stated them and placed them by eye; the placement pass declined what did not fit | studio placement and refusals |
| Objectives, XML | model: obsidian monuments, `DestroyablePlacement`; XML from the export | studio |
| Finishing | person: notes and rulings in rounds (8, 10, 5 and 3 new notes on this board across four rounds, rulings in rounds one and two), each worked and answered by the model at a named revision; the author's first verdict was "empty" | model through the studio |

Sources: `reports/opus55-notes-run.md` (second, fourth, sixth, eighth and tenth passes); research `05` §"Feedback".

### 3.11 Whinberry Ring (12 September; Fable 5.1, and Heftfold by Opus 5)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | unknown who wrote the one-sentence brief; the run was held to the author's spoken brief (think first, keep it simple, one ground, few houses of one family, no grown trees) | |
| Layout | algorithm: `GET /compose?players=16&symmetry=rot_180` walked for 24 seeds, seed 18 pinned "for its shape" by the model; model: three levels, a twin frontline with a bay, a stepping stone, bedrock walls on the wool approaches, the outline reshaped vertex by vertex | `build-spec.py` through the driver, studio |
| Terrain, colour, structures | model, to the stated brief; one oak copied from the author's tree showcase | model script, studio |
| Objectives, XML | algorithm (composer's wools and spawn), model (kept) | studio export; "gate OPEN, nothing declined" |
| Finishing | person: he read the first build of each board and said what was wrong ("cute and had too many trees"); the model changed it | model script, studio |

Heftfold (Opus 5) is the same arrangement with different edits: the composer's skeleton kept, with a walled island in
the middle, a team site in three levels and the spawn between its two wools; who briefed it: unknown.
Sources: `reports/fable-four-boards-run.md`; `review/opus5-heftfold.md`; `BOARDS-BUILT.md` (rows 367 and 383).

### 3.12 Overwall, the labyrinth (25 August, Opus 5)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person, his account: "concept maps such as the labyrinth were his ideas, built 1:1 to probe limits". The report says only "a third brief from the same person outside this repository"; it does not name him | |
| Layout, terrain, colour, structures, objectives | model: pillars on a 22-block grid so every passage is 12 wide, three slabs, a river down the one open corridor, a keystone and a wool room, 32 trees, 14 boulders, four houses on stilts; the brief fixed the 12-wide passages, the river, the third-layer bridge and the houses on the walls | model script (`specs/archive/opus5-overwall`), studio |
| Objectives, XML | studio export, gate open | studio |
| Finishing | none **(his account)**: no hand finishing | |

Coldstore (22 October, pgmvox) is the same kind with a better record: the author sent a concept world of one bunker
quarter with 44 explanatory signs, and the model built the rest by Python scripts; two author reviews changed four and
five things; no studio was driven (category 6).
Sources: `reports/opus5-overwall-run.md`; `reports/coldstore.md`; research `05` §"Other claims".

### 3.13 Riftwater, the first freeform board (7 October, Opus 5.5)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | model; the author (seventh instalment): he contributed nothing. The record is silent on the instruction that started it | |
| Layout | model: one valley mirrored across a rift 20 blocks wide, two settlements a side, DTM rather than DTC, because a core's lava would pour into the cave the board is built around | model scripts (`plan.py`, `gen.py`) |
| Terrain shape | model | model scripts (3,379 lines in all) |
| Colouring, structures, decoration | model, including a cave system under the valley | model scripts; the studio's region writer only |
| Objectives, XML | model: four monuments, the rift as the only place to build; `mapxml.py` wrote the `map.xml` | model script |
| Finishing | person: review rounds and his playtest verdict "essentially perfect"; model: fixes | model scripts |

"No studio authoring pipeline was used." The cost the repository states: "Opus, hours per board rather than minutes,
rounds of the author's review, and bespoke code".
Sources: research `05` §"The rework", `03` §§1, 2; `freeform/lib/boards/riftwater/REPORT.md`.

### 3.14 Cedar Crossing (10 August UTC, arcadeboss with Grok)

| Decision | Who decided | What executed |
|---|---|---|
| Concept | person: credits "7,000 word essay" to arcadeboss and "Map suggestions" to a second human | |
| Layout, terrain, colour, structures, objectives | model, by the credit "SuperGrok: Map and XML"; which decisions the essay fixed and which Grok made: unknown | the author's account: a script Grok wrote and a zip; the record holds only the credits, so how it ran is unknown |
| XML | model, same credit | unknown |
| Finishing | unknown. "Updates from play testing" on 13 August; who made them: unknown | |

No shared tool is in the record. Sources: research `11` §3, `06`; author's account (fifth and seventh instalments).

## 4. What the table shows

The studio is an executor in 9 of the 14 rows, and the decider in none: where it decides, the cell reads
"algorithm" and names the seed or default. The column most often "unknown" is concept, and the one most often
"person" is finishing. The author's own map is the only row in which no model decided anything and the studio
executed nothing.

## 5. The six categories

| # | Name | What is true of it | Maps |
|---|---|---|---|
| 1 | **Hand-made** | a person decides all seven and builds them; a tool at most writes the XML he drew | ice map, Vauxite and Drastic Change II, Bridgid II |
| 2 | **Person's design, algorithm's detail** | a person draws and states; the studio solves, paints and grows what he did not state | No Blocks Placed |
| 3 | **Person's drawing, model's pen** | a person supplies the drawing, the numbers or the object; a model writes it down, or builds on it, and a person finishes | Base 2-Island, Capture the Cake, Millrace, Wandering U (his text, Claude's XML) |
| 4 | **Algorithm's layout, model's spec** | a model states words and numbers; a seeded algorithm lays out and fills | first fifteen (Goldhollow, Ridgeway) |
| 5 | **Model's design inside the studio, person's rulings** | a model decides content through the studio's vocabulary; a person steers by brief, notes and rulings | Gypsum Reach, Whinberry Ring, Heftfold, Overwall |
| 6 | **Model's own script** | a model decides and writes the program that writes the world; the person gives a concept, a review or nothing | Riftwater, Coldstore, Cedar Crossing |

## 6. The argument

**"AI map" has meant a different thing at each stage.** In June and July it meant a person's map whose XML a tool
wrote. In July it meant a person's drawing that a model turned into blocks (Base), and a model's credit on one
conversion (Kuusepuu). In August it meant a model's spec to which a seeded composer gave the shape. From September it
meant a model deciding content through the studio while a person ruled by notes. In October it meant a model writing
the whole world as a program. In November the newest map went back to the first category, built by the author, and the
models were put to reading it. The phrase covers every point on that line, so "AI-made" alone says almost nothing.

**The human stayed in five places.** He drew (the squared paper, the basin, the labyrinth's rules), he briefed (the
spoken brief, the essay behind Cedar Crossing, the Coldstore world with its signs), he left notes (26 on one desert
board over four rounds), he ruled (the grown tree went "rather than gets a knob"), and he finished (ten person-hours
on Millrace). Where the record has no one in any of those places, the cell says unknown; it is not read as the model.

**The algorithmic part is real and smaller than it sounds.** The composer decided a layout from a seed, the relief
solver the heights, the placement pass where a tree could stand, a theme which block a wall was. But a seed is a
decision in waiting: Goldhollow's seed 41 and Whinberry Ring's seed 18 were chosen by someone, and the second was
pinned from 24 walked by looking at their shape. An algorithm decides what nobody stated, which is its value and its
limit: his account of the ice map says agents never think about routes beforehand and that the path is only computed
afterwards, and a layout composer is the same thing done once at the start.

**The composer's concept is the author's, and by his account the agents mostly took its layout unchanged.** He says
the layout generator's concept is his, devised to reproduce existing maps as far as possible; what it emits is
generic, as limited as it is, but a base to work on, and the agents mostly took that base and did nothing with it,
not even adjusting other aspects of the layout **(his account)**. The record agrees for the first fifteen
(Goldhollow, Ridgeway: the layout cell is the composer's seed) and shows the opposite in two places: Whinberry Ring's outline
was reshaped vertex by vertex from seed 18, and Heftfold's composed skeleton was given a walled island. So the layout
cells of categories 4 and 5 read "algorithm" where the board is the composer's output unedited, and "model" only
where the record names the edit.

**The tool's part is execution and refusal, and neither is authorship.** The studio turned a typed list of corners
into a world, and it executed a model's `build-spec.py` for Whinberry Ring by the same code; Riftwater's scripts wrote
theirs through nothing but its region writer. Its gates say no (a dead-ground band, a board with no author) but a
refusal removes options; it never supplies content. The branch where the author built his map states the limit in one
line: "a geometric rule is not a design. Every one of those failures passed some check that existed at the time."

**The model's own decisions are the ones the record shows it making against no stated content.** It chose a valley, a
rift and a cave for Riftwater, three levels and a bay for Whinberry Ring, the wash and the mesa for Gypsum Reach. The
record also shows it deciding wrongly: a staircase where the drawing had an H, and two boards reported "verified
working" that were 245-byte `map.xml` shells. A model's decision can be real and bad, and a person's can be a
selection (Opus's terrain over two Sonnet boards of the same basin) rather than an act of drawing.

**Determinism of execution does not settle authorship, because authorship is a property of the inputs.** The same
studio returns the same world for the same input, whether a person typed the corners or a model wrote the spec; that
shows the function is pure and says nothing of who wrote its argument. A compiler is deterministic and does not
author the program. A map the studio never executed, such as the author's ice map, shows the converse: nothing
deterministic ran, and it still has one author. What the spectrum measures is how much of each of the seven decisions
someone stated before the executor ran, and who that someone was.

## 7. Open cells

Unknown after this pass: who set the briefs for the first fifteen, Gypsum Reach, Heftfold and Whinberry's sentence
(he offers to find the sessions from their dates: the first fifteen were built on 11 and 12 August 2026, the first
commit of `tools/mapgen` is 12 August 20:05 UTC (`5897944a` **(studio)**), Heftfold was first committed on 12
September at 06:41 UTC (`fc91b3be`) and Gypsum Reach on 28 September at 23:00 UTC (`ae025473`)); the layout and
structures of Vauxite, Drastic Change II and Bridgid II; who drew Wandering U's layout in the studio, as against
describing it in text; how Cedar Crossing was run (he may be able to answer from his chat history); whose idea the
labyrinth was beyond his account. Answered by him on 27 November and folded into the cells above: the concept,
terrain and colour of Vauxite, Drastic Change II and Bridgid II; Bridgid II's XML; Wandering U's XML; the XML of the
published Millrace; the ice map's materials and finishing; Overwall's finishing.
The interview questions after this file ask the five that matter most.
