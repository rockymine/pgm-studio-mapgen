# 18 — Before the studio: CTWAnalysis and the early tools, checked against the git record

Research for the history film. Scope: the author's eighteenth instalment ("before the record", 28 November 2026,
`../author-account-2026-11-27.md`) and its eight pictures (`../sources/early-experiments/`), checked against four
local clones read on 28 November 2026: `/home/user/rockymine/ctwanalysis` (773 commits over all branches, 2026-01-31
to 2026-08-10; 748 on `main`; 58 further remote branches, of which 23 are `claude/…`),
`/home/user/rockymine/MinecraftLayoutEditor` (135 commits over all branches), `/home/user/rockymine/CTW-Layout-Generator`
(5 commits) and `/home/user/rockymine/pgm-map-studio` (166 commits over all branches). None is shallow. Dates are
author dates with the committer's timezone as recorded; commits made by Claude web sessions carry `+00:00`.
`research/01-origins.md` and §3 of `research/17-…md` are not repeated except where this record sharpens them.

Limits. The match logger (`pgmlogger`, a Bukkit plugin) is a separate repository that was not cloned; only
references to it were read. The pictures were looked at, but nothing in a picture proves a date that the record
does not. Where the record is silent this file says so. The two committer identities of the early repositories
(`live.de` address and `rockymine`) are treated as in `01-origins.md`: same human account is **[uncertain]**, and
the file does not claim it.

---

## 1. CTWAnalysis (github.com/rockymine/ctwanalysis; the picture sources call it CTWAnalysis)

**The record starts on 31 January 2026 with a finished-looking codebase, not with an empty repository.** The first
commit, `695418f` ("Initial commit", 2026-01-31 23:55 +01:00, `live.de` identity), adds 67 files and 13,971 lines
of Python: `layout_analysis/islands/detection.py` and `triangulation.py` (369 lines), `layout_analysis/skeleton/*`
(skeletonize, prune, nodes, edges, canonicalize, POI annotation), `xml_analysis/` (parser, regions, exporter,
visualizer, tests), `match_analysis/` (life segments, segment classifier, path network) and a `README.md` that says
"Built with Claude Code". So the history before 31 January was developed outside this repository and arrives as one
commit. The record cannot say how long that took.

**The author's "around 26 January" is neither confirmed nor contradicted; it is consistent with what the first commit holds.**
The initial README shows match files named `match_logs/2026-01-24_09-26-48_3.parquet`, and `config.json` names
`2026-01-24_22-24-17_75.parquet` on Tumbleweed; the demo README later says that match was "recorded 2026-01-24".
So match logs existed by 24 January, a week before the first commit. The islands-to-triangles code is in the first
commit; the picture title "Island Triangulation Detail View" appears in the repository exactly once, at
`layout_analysis/islands/visualization.py:447` in `695418f` (31 January), and it was deleted on 13 February (see below).
The string "Simplified Skeleton Detail View" is in no commit on any branch.

**Polygon decomposition is present from the first commit and is removed twelve days later.** `bddea5b` (2026-02-13
22:35 +00:00, Claude): "Remove triangle meshing, rename triangulation → polygon" — "the meshing step … was only used
for visualization". What stays is the exact union-of-blocks island polygon. The two January pictures therefore show a stage
of the tool that the repository carries only between 31 January and 13 February.

**Skeleton/medial graph: in the first commit as a pixel skeleton (scikit-image `skeletonize`, `medial_axis`), and first
developed in the history on 1–2 February.** `88ea4ba` (2026-02-01 16:55) "intra-island POI pathfinding", `02e5bb3`
(1 February) "export of pixel paths from skeleton", `36b64f7` (2 February) "inter-island connectivity analysis",
`9fd3c6c` (2 February) skeleton inside `map_graph.json`. The author's "da sind wir wieder bei der Graph-Idee" fits this:
a graph of islands, skeleton nodes and void links exists from 2 February
(the `docs/demo` "Connectivity Graph" picture shows it for Ingwaz). Claude removed the connectivity module
and the pathfinding from the skeleton package on 13 February (`d0189de`).

**XML reading and display: the parser is in the first commit; showing XML regions on the layout comes on 2 February;
a browser viewer comes on 14 May.** `xml_analysis/parser.py` is in `695418f`. `5698798` (2026-02-02 22:41) "extract and
visualize build regions from xml and parquet data" draws the XML build region over the island picture. The browser
`map_viewer` starts at `0e51971` (2026-05-14 17:20, "add browser-based map visualization package", Flask, SVG, "named
XML region overlays"), with the region tree in the sidebar ten minutes later (`bce9346`).
The author's "in the end the XML display too" is right for the browser viewer, and sharpened for the image output.

**Match data: 2,452 matches processed by 9 March 2026, 177 unique maps; the author's "about 4,000 games" is not in the record.**
`match_analysis/DATABASE_SUMMARY.md` (`85c12bc`, 2026-03-09) lists "Total matches processed 2,452", 49,170
participations, 9,136,355 position records, 4,440 wool captures. The file is touched again on 2026-04-10 and
2026-05-30 and still says 2,452 on `main`, so the number may be stale rather than final. The roadmap
(`docs/analysis_roadmap.md`, 2026-03-18) speaks of 81 maps with at least ten processed matches. The Discord sync
that pulls further match files in is `dd0a743` (2026-03-21, `ingestion/fetch_data.py`). Whether the logger collected
about 4,000 matches in total, with fewer ingested, cannot be told from the repository. A later corpus statement, in
`scripts/match_flow/README.md` (2026-08-09), uses 333 long two-wool matches on 94 maps.

**The logger plugin is named, not contained.** `docs/analysis_overview.md` links
`github.com/rockymine/pgmlogger` as the Bukkit plugin that wrote the match logs; the name first appears in a commit on
2026-03-07 (`cfbfd53`). The raw logs are parquet with columns `timestamp, event_type, player_id, x, y, z, held_item,
inventory_count, wool_id` (initial README). The point cloud picture `2026-player-position-trace.png` is the kind of
output of the `trace` command (`c329722`, 2026-02-03 "support visualizing individual player traces"; `132e0c2`,
2026-02-11 trace from the database). "Map Traces" as a feature that told void from build region is not named in any commit
subject; what the record has instead is a build-region extraction from XML plus parquet data (`5698798`, 2 February)
and the build-region classification fixes of March. **The author's "Map Traces" label is not found; the record is silent on it.**

**Phases, month by month.**

| Month | Commits | What the subjects show |
|---|---|---|
| 2026-01 | 1 | `695418f` (31 Jan 23:55): the 67-file import described above. |
| 2026-02 | 219 (41 Claude-authored) | Skeleton pathfinding and island connectivity (1–2 Feb); build regions from XML (2 Feb); unified `ctw` CLI (2 Feb); DuckDB match analysis, life segments, player traces (3–7 Feb); `matches` pipeline, combat/position/wool tables (5–11 Feb); symmetry analysis as a pipeline step (11 Feb); first Claude-authored commits from a web session (9 Feb); package restructuring and geometry-coordinate cleanup (13–27 Feb), the triangle mesh removal among them. |
| 2026-03 | 256 (28 Claude-authored) | Tumbleweed and wool-dynamics demo images (6–9 Mar); data-driven traffic graph (7–12 Mar); defense-setup analysis (9 Mar); chest/resource classification (12 Mar); kit extraction (13 Mar); `docs/analysis_roadmap.md` with hypotheses (18 Mar); terrain-height table (19 Mar); `authors` command (20 Mar); Discord ingestion and stub maps (21–25 Mar); GridBase and geometry graph (26–27 Mar). |
| 2026-04 | 40 (8 Claude-authored) | Quiet 28 Mar – 8 Apr. Island profiling and the shape classifier (circle, square, L/Z/T, donut, maze) from 9 Apr; Claude's two-axis island classifier (17 Apr); near-symmetry detection (22 Apr). Last commit of the month 22 Apr. |
| 2026-05 | 246 (37 Claude-authored) | Nothing 23 Apr – 13 May. Then 14 May: the browser map viewer and region inspector (14–19 May); draw tools for rectangles (15 May) and points, blocks, cuboids, cylinders, circles (22–24 May); configure page with island exclusions (28 May); Claude-session work on polygon rendering of composite regions and the `/concept` layout concepting tool (28–29 May); the author's follow-up on the concept tool (29–31 May); on 31 May a series of `remove:` commits marked "superseded by map viewer". |
| 2026-06 | 7 (all Claude) | 3 June only, 10:56–18:26 UTC: port-requirements and editor-vision documents. |
| 2026-07 | 0 | |
| 2026-08 | 4 | 6 Aug one Claude housekeeping commit; 9–10 Aug three commits (below). |

**Claude sessions versus the author: 592 of 773 commits carry a Claude mark.** 121 commits are authored by the
identity `Claude` (a web session, timestamps in UTC); 471 more carry a `Co-Authored-By: Claude …` trailer under one of
the two human identities (452 under the `live.de` identity, 18 under `rockymine`; one under `Claude` itself). 181
commits carry neither mark: 140 under the `live.de` identity, 41 under `rockymine`. By trailer the models are Claude
Sonnet 4.6 (443), Claude Opus 4.6 (24, all in February), Claude Opus 4.8 (1, 6 August) and Claude Opus 5 (3, 9–10 August).
The README of the very first commit already says "Built with Claude Code". What a trailer shows is that a Claude
session wrote or helped write the commit; it does not show how much of it. First trailer: `5a50440` (2026-02-09 03:07).
First Claude-authored commit: `34e2dbe` (2026-02-09 03:21 UTC). The 31 January import and the commits of 1–8 February
carry no trailer. **Whether those first commits were written with an assistant is left open by the record**, although the README
says the toolkit was built with Claude Code.

**The author's account says "Claude wrote scripts that find the islands and cut them into polygons": the record
agrees on the code being there on 31 January, and says nothing on who wrote it, because the history before that day is not in the repository.**

**A commit matches the 20 March screenshot's topic, to the hour.** `6cbc9dd` (2026-03-20 00:19 +01:00) "feat(maps): add
authors command to parse map.xml credits and look up Minecraft names", on branch `feat/extract-authors-from-xml`,
merged as PR #40 at 01:06 (`927e6e9`). The screenshot's last line asks "Commit the authors command, then backfill the
layout/terrain fixes for the 143 contaminated maps?" — so the exchange precedes 00:19 on 20 March; the previous merge
was PR #39 (`be444cc`, 2026-03-19 23:35), the terrain-height and `max_build_height` fixes of 19 March
(`7095dd5` … `e4f00c4`, 17:56–23:26). That fits "layout/terrain fixes" and puts the screenshot in the late evening of 19 March
or the first minutes of 20 March. **The words "contaminated" and "143" appear in no commit message and no
file at any point of the history of any branch searched**; what the 143 maps are cannot be read from the record.
Nothing follows on 20 March itself about map generation: the next commits (21 March) are database compaction,
Discord ingestion, stub maps and a debug refactor.

**Map generation and "layout concepting": 28–31 May 2026, in this repository, not before.** Searching the history for
generation work before May finds analysis only: the March roadmap (`docs/analysis_roadmap.md`) states its purpose as understanding how matches play out. The first generative-direction work is the `claude/map-layout-concepting-tool-slYoq`
branch: `1f497b5` (2026-05-29 12:38 UTC, Claude) "Add map layout concepting and sketching tool at /concept" — "designing
map layouts before any pipeline processing … sketch island shapes on a blank canvas, group them into named islands,
and compute the resulting polygon … in the same format that layer extraction delivers"; a lasso tool (`2168ffa`,
12:47 UTC); topology-driven island computation (`30bd248`, 29 May 23:25 +02:00); the merge `9041a04` (30 May 22:03);
Visvalingam-Whyatt simplification in a shape inspector (`1e7119a`, 31 May 02:02). **The 20 March conversation
therefore comes about ten weeks before the first line of layout-drawing code**; the record shows no generation work between them.

**The author's May story is visible inside this repository, in his order, with dates.** Viewer of XML files and maps:
14 May (`0e51971`). Drawing regions: 15 May, draw tool for rectangle regions (`800f902`, 13:48), more region types
22–24 May. Drawing polygons that make islands: 29 May, `/concept` with polygon tool and island computation.
So the three steps the author puts under "PGM Studio" were first taken in CTWAnalysis's `map_viewer`; they move to a
new repository on 31 May (§3).

**What happens after May: one evening of documents and then three commits in August.**
On 31 May, 18:41–20:53, the `rockymine` identity deletes superseded visualisation commands (`f7a5aa9`, `1975200`,
`5c3e253`: "remove: …, superseded by map viewer"; `65e1d3d` removes `notebooks/`). At 22:01 the same
evening `pgm-map-studio` begins (§3). On 3 June Claude writes seven documents ("port requirements document for xml,
symmetry and pipeline refactor", "editor vision", "map viewer design review"; `353fe6c` … `dfc80b6`), which read as the
brief for the port. Nothing then until 6 August. The three August commits are by the `rockymine` identity and one is
Claude-trailed: `77de77f` (2026-08-09 22:11) "match-flow scripts — walls, staircases, sky network, wool order",
`583984c` (2026-08-10 00:02) "approach-route variance, void detection and rotation use", `d34eeaa` (2026-08-10 01:23)
a fix to the excavation measure. All three add `scripts/match_flow/`, "analysis behind testing a written account of how a CTW
map is played against the recorded matches", reading the processed database and the raw `pgmlogger` parquet.
Their message says over "490 bundles on 150 maps, 9% have [a second way in to the objective], 35% [a fork far from the room],
63% a single corridor", i.e. this is the data work behind the gameplay documents of the studio repository.
**Disagreement with the account: the author says he left the match-analysis project in May; the record shows the data
was returned to on 9–10 August 2026, for the match-flow account.**

---

## 2. MinecraftLayoutEditor (github.com/rockymine/MinecraftLayoutEditor)

**The commits the author dates by his chat with Ruediger are all there, to the day.**

| Author's date | What the record has |
|---|---|
| 11 Oct 2025, first screenshots | `4d132b2` 2025-10-11 01:04 "symmetry, mirror, rotate, snap to canvas, etc." |
| 12 Oct 2025, blocks no longer placed by hand | `d961f6a` 2025-10-12 00:13 "add schematic creation and download" (`SchematicWriter.cs`, `Schematic.cs`); `9f978e3` 2025-10-12 20:05 "render edges with bresenham" |
| 4 Nov 2025, first okay layout | No commit says so. `6021b3a` 2025-11-04 00:09 "use skiasharp for rendering" and, that evening, `a3e2a1e` 18:22 "testing: add new layout for performance testing" (a change to `LayoutFactory.cs`). The in-game import on the mapmaker server is outside the repository. |
| 6 Nov 2025, world import | `d2c4bc3` 2025-11-06 03:20 "working import of .leveldat and .mca files (claude & grok)", +740 lines, of which `WorldImporter.cs` 621; merged by PR #2 at 20:40 (`084a4ed`). |

**Dating sharpened: the XML regions the author remembers on 6 November arrive on 10 November.** `d23891b`
(2025-11-10 00:17) "Add XML import" and `054edbb` (00:40) "add missing region types; render regions". On 6 November
the editor imports a world's region files and `level.dat` and draws its blocks; the picture of that day shows blocks and no
region overlay. The branch `17-implement-basic-xml-file-import-for-map-data` has no commit of its own before 10 November. Editing of
regions begins 12 November (`6054970` "add editing mode") and 17–18 November (`a116dc8`, `b936cc3`).

**The UI in `2025-11-06-layout-editor-world-import.png` is this repository's UI at that date, label for label.** At
`d2c4bc3` and at `9d72ca6` (2025-11-06 20:35): `LayoutSettings.razor` has "Width", "Height", "Lane Width", "Thickness",
"Node type"; `Home.razor` has "Generate Schematic" (line 22) and `<label>Import World (Region Files + level.dat)</label>`
with `<InputFile … multiple accept=".mca,.dat">` (line 38), which is what a browser localises as "Durchsuchen … 5 Dateien
ausgewählt"; `MirrorControls.razor` has "Mirror Settings", "Enable mirroring", "Horizontal mirroring", "Rotation (deg)";
`VisualizationControls.razor` has "Show bounding box" and "Show blocks"; `NodeInformation.razor` and
`CanvasControlsHelp.razor` have "Node Information" and "Canvas Controls". The header "Minecraft Layout Editor" and the
Spawn/Wool/Delete Node buttons are the same components. The picture is therefore from 6 November or a few days after, before the
rename of Layout to Map on 9 November (`49cbd9f`) changed the vocabulary of the code, not of the screen.

**Last human commit 20 December 2025; then a Claude session adds 19 commits on 30 July 2026.** Master ends on 2025-11-16
(`f683004`, "introduce edges property for graph"). On branch `24-implement-region-creation-within-editor` there are
`a116dc8` (17 Nov), `b936cc3` (18 Nov) and `de5ee47` (2025-12-20 20:25, "ui improvements (claude)"). Nothing from the two
human identities follows. **The author's "pause from December, until February at least" is consistent: in this
repository, as in all four, no commit falls between 21 December 2025 and 30 January 2026.** But the repository was not
left alone afterwards: branch `claude/minecraft-layout-editor-perf-cspypa` has 19 commits on 2026-07-30 (00:35–02:29 UTC,
author `Claude`, all `Co-Authored-By: Claude Opus 5`, one session), about rendering performance (cache and cull the block
layer, a measuring graph, a write-up of the rendering work) and ending with "Make the map.xml regions pickable and draggable"
(`5828bfa`) and a write-up of hit-testing and dragging (`3fbc6cd`). **That contradicts "he left the MinecraftLayoutEditor
project in May"** unless the author means that he stopped working on it as a tool; the commits are two months after May.
The branch is not merged into `master`.

**`ctw-layout-editor`: the record shows no repository of that name.** The remote is
`https://github.com/rockymine/MinecraftLayoutEditor`; the solution is `MinecraftLayoutEditor.slnx` with projects `…Logic`,
`…Schematics`, `…WebApp`, `…XML`; the README is the single line "# MinecraftLayoutEditor"; the string `ctw-layout-editor` occurs in
no commit searched. The other early repository is `rockymine/CTW-Layout-Generator` (a React/Vite app, 5 commits, 28 Sep – 3 Oct 2025,
first commit "Built with AI Studio"). The record cannot tell whether a third repository, `ctw-layout-editor`, exists;
**the author's "sicherlich wird das ein anderes sein" is not contradicted.** It remains a different name for something
not seen here.

**How much is the author's own, how much assistant-written: the record can say little, and what it says agrees with "größtenteils eigener Code".**
Of 135 commits, 90 are by the `live.de` identity, 26 by `rockymine`, 19 by `Claude`. Every commit before 30 July 2026
is by a human identity. The only explicit assistant marks before that are two commit subjects: `d2c4bc3` "(claude & grok)",
the world importer, and `de5ee47` "(claude)", UI improvements. No commit before July has a `Co-Authored-By` trailer. The
early history reads as hand-made: October 2025 commits are named "Code cleanup", "Refactoring", "Implement command pattern",
"Implement zoom", "Implement panning", one small step at a time. A world-file parser of 621 lines in one commit at 03:20 at night is
the one large block with a named assistant origin. Who wrote the rest cannot be settled by commit text.

---

## 3. pgm-map-studio (github.com/rockymine/pgm-map-studio)

**It begins on 31 May 2026 at 22:01, as an analysis-and-export package, not as a viewer.** `915c61c` ("Initial project
scaffold", 2026-05-31 22:01 +02:00, `rockymine`); `1ad5955` (23:10) "minecraft package with extractors, game data, and map
discovery"; `ba9c9b3` (23:39) "layout package with island detection pipeline". On 3 June: `b4d1333` pgm and symmetry packages
"with full filter/apply rule support", `050b093` "XML roundtrip export (MapXml → map.xml)", `0da8431` the three-step
pipeline "Layout → Symmetry → XML". On 4 June: `3a5dc89` "studio package: Flask editor with Dashboard, Overview, and Teams
activities". On 5 June the data-model and authoring documents; on 6 June "Implement Sketch 1.1 — Overview activity", 1.2
Setup, 1.3 Layout (`dec3cd2`, `8c9b1e9`, `71971a7`); 7 June export of a loadable world. The last commit is on 2026-06-12
(research/01 has the branch `refactor/contract-first` ending 03:24).

**The author's three steps (view XML, draw regions, draw polygons/islands) are dated by the CTWAnalysis log, not by this one.** They are
14 May, 15 May and 29 May in CTWAnalysis (§1). In pgm-map-studio the order is reading and writing XML first (3 June), then a
Flask editor with a region tree (4 June), then a sketch tool with an island layout (6 June). "In May, roughly, PGM Studio began
… first only as a view of the XML files and the maps" is accurate for what was built in May and wrong for the repository
named pgm-map-studio, whose first commit is the last day of May. **The author's "May" is right to the day if the date is
the one on which the viewer's work was finished (31 May).** Authorship: 144 commits `rockymine`, 21 live.de identity,
1 Claude; trailers: 79 Claude Sonnet 4.6, 64 Claude Opus 4.8.

---

## 4. The April, May and August 2025 experiments

**Nothing from April, May or August 2025 is in any of the four repositories.** The earliest commit of any of them is
`2aed35c` (CTW-Layout-Generator, 2025-09-28 02:42, "Initial commit", an AI Studio README). The matplotlib picture of 5 April 2025
("Multiple 1-Team PvP Layouts (Improved Graph Connections)"), the Claude chat artifact of 24 May 2025 and the v0
experiment of 16 August 2025 have no commit, file or message behind them in these clones (a search of commit messages and file
content for "Improved Graph Connections", "Multiple 1-Team", "Interactive Level Design" and "Level Design" found nothing; `networkx` occurs in
CTWAnalysis only in the March 2026 traffic and defense plots, which have nothing to do with that experiment). The
earliest dated traces of generation thinking in the record are therefore the AI Studio repository of 28 September 2025
and the C# editor of 10 October 2025. The AI Studio start fits the author's note that a link to an AI Studio app followed
on 7 October; the repository's own README gives no link.

---

## 5. Where the record and the account differ

| Account | Record |
|---|---|
| "Around 26 January 2026 it began" (islands, polygons) | First commit 31 January 23:55 holds all of it; the 24 January match logs predate it. 26 January is not contradicted but not shown. |
| "20 March, a big turning point" | The topic matches `6cbc9dd` at 00:19 on 20 March (the authors command); the first generative code is 29 May, ten weeks later. |
| "Contaminated maps", 143 | In no commit message or file. |
| About 4,000 games collected | Committed summary: 2,452 matches processed (9 March, unchanged on `main`). |
| "Map Traces" a feature for void versus build region, later dropped | Not named; build-region extraction exists from 2 Feb; the trace command from 3 Feb. |
| 6 Nov 2025: world import "showing a few XML regions" | World import 6 Nov 03:20; XML import and regions 10 Nov 00:17–00:40. |
| Pause from December until February | No commit in any repo 21 Dec – 30 Jan. Consistent. |
| Left the editor and the analysis in May | Analysis repo: removals on 31 May, then three analysis commits on 9–10 Aug. Editor: 19 Claude commits on 30 Jul 2026 (unmerged branch). |
| PGM Studio began in May as an XML viewer | The viewer and drawing tools are in CTWAnalysis from 14 May; pgm-map-studio opens 31 May 22:01. |
| `ctw-layout-editor` probably another repository | No such repository or string in the record. |
| 11–12 Oct 2025 first screenshots, blocks without hand placement | `4d132b2` 11 Oct; `d961f6a` 12 Oct. Confirmed. |
