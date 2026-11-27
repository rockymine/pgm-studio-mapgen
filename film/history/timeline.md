# Master timeline — the history film

The spine of the film, in date order. Every row is taken from one of the four research files under
`film/history/research/`, named in the last column (`01` origins, `02` studio, `03` maps and models, `04`
hand-built); the table of uploads further down is from `11`. Nothing in the events table was measured or dated afresh, and where a research file marks a fact as uncertain the
row says so. The chapter column refers to `OUTLINE.md`.

Repositories are abbreviated: **CTW** `rockymine/CTW-Layout-Generator`, **MLE** `rockymine/MinecraftLayoutEditor`,
**PMS** `rockymine/pgm-map-studio` (Python), **studio** `rockymine/pgm-studio`, **mapgen** `pgm-studio-mapgen`.
Dates are author dates as the research read them.

## Events

| # | Date | Repo | Commit | Event | Why it matters | Ch. | Src |
|---|---|---|---|---|---|---|---|
| 1 | 2025-09-28 | CTW | `2aed35c` | "Initial commit": the README of a Google AI Studio app | The first trace of the whole project, and it was made in AI Studio, not by hand | 2 | 01 |
| 2 | 2025-10-01 | CTW | `6691417` | A seeded CTW layout generator (`lib/mapGenerator.ts`, 806 lines) with node types `SPAWN`, `WOOL`, `HUB`, `FRONT_LINE`, `CENTER_HUB` | The vocabulary of the later model exists nine months early, and the map is a graph | 2, 3 | 01 |
| 3 | 2025-10-03 | CTW | `3eab815`, `ec9ca62` | A step-wise manual editor; snapping to the symmetry line; the last commit. The only export is "Download JSON" | The repository stops after six days, and it never made a block | 2 | 01 |
| 4 | 2025-10-10/11 | MLE | `d460b47`, `4d132b2` | A self-built C# solution (Blazor WebAssembly, `net10.0`) around a `Graph` of typed nodes; symmetry, mirror and rotate the next day | The C# era begins here, in October 2025; symmetry is the first feature after the canvas | 2, 3 | 01 |
| 5 | 2025-10-12 | MLE | `d961f6a`, `9f978e3` | "add schematic creation and download"; "render edges with bresenham" | **The first downloadable blocks**: a drawn graph becomes a `.schematic`, an edge becomes a line of blocks | 2 | 01 |
| 6 | 2025-11-06 → 11-16 | MLE | `d2c4bc3`, `d23891b`, `f683004` | World import "(claude & grok)"; XML import; the last commit on `master` | The first AI models named in a commit message; the first reading of a real world and a `map.xml` | 2 | 01 |
| 7 | 2026-05-31 | PMS | `915c61c`, `ba9c9b3` | The Python scaffold, co-authored by Claude Sonnet 4.6; island detection over scanned worlds | A second start, five and a half months later, by reading existing maps rather than generating | 2 | 01 |
| 8 | 2026-06-05 | PMS | `12d6395` | The CTW pamphlet: "The ground plane is not just terrain — it is the map's navigational grammar." | The clearest early statement of why the void steers play | 3 | 01 |
| 9 | 2026-06-07 | PMS | `4f095eb` | A browser sketch exports as "a complete, PGM-loadable map folder" | The loop from drawing to loadable world closes, in Python | 2 | 01 |
| 10 | 2026-06-12 | PMS → studio | `490aebe` (03:24), `f499ea88` (17:21) | The last Python commit; fourteen hours later, pgm-studio's first commit, an empty README | The Python studio was worked on until the night before the C# one opened | 2 | 01 |
| 11 | 2026-06-13 | studio | `7b30744a` | "Initial import: ASP.NET Core + Blazor WASM port of pgm-map-studio": 145 files, +18,093 lines, co-authored by Claude Opus 4.8 | A full port in one day, on the stack still used today | 2 | 01 |
| 12 | 2026-06-20 | studio | `f25a9249` | Corpus analysis (N=347): "the generator emits 0 neutral mid pieces but 88% of real maps carry a contested middle" | The corpus becomes the measure, and the middle is named as what is missing | 3 | 01 |
| 13 | 2026-07-02 | studio | `845ccb0a` (14:31), `313ae96b` (14:54) | The map-as-graph written up as an architecture (first Fable 5 commit); 23 minutes later the graph is dropped for areal pieces | The oldest idea in the record, abandoned because "a thinned skeleton cannot represent side contact" | 3 | 01 |
| 14 | 2026-07-02 | studio | `10137274`, `188d61ce` | A layout-rules strawman, numbered "for correction by id"; the author's first correction round the same afternoon | The rules begin as guesses a human corrects: the oracle's first appearance | 6 | 01 |
| 15 | 2026-07-04 | studio | `7b4603cc`, `ec7132d3` | The composer starts; recorded play enters ("105 matches, 510 players, 199 grid nodes" on ingwaz) | The generator and its evaluation instrument begin the same day | 3, 4 | 01, 02 |
| 16 | 2026-07-10 → 07-21 | studio | `9d75d05c`, `d1489f23` | Typed spawn / hub / frontline / mid boxes; "the box pipeline is THE composer" | The hub–approach–frontline–middle model becomes the only generator | 3, 4 | 01 |
| 17 | 2026-07-15 | studio | `5825954d` | The DTM/DTC contract: "DTM is cheaper than the CTW wool we already ship" | Destroy modes arrive a month after CTW, which says CTW came first for its structure, not its ease | 3 | 01 |
| 18 | 2026-08-09 | studio | `b34cf7eb` | How a CTW match is played, read off recorded matches: a void "is uncrossable at every height" | The void as permanent route structure, from play rather than theory | 3 | 01 |
| 19 | 2026-08-11 | studio | `755ab378`, `3c82ff1a` | "A shell became a house — six roofs, a zoned floor, windows, a porch"; a building is a stack of storeys | Houses become a parametric system in a week | 5 | 02 |
| 20 | 2026-08-12 | studio | `c9ea46d6` | 75 hand-built trees measured: "1516 of 4020 never touch their branch" | The generated tree is measured as broken against the author's own | 5 | 02 |
| 21 | 2026-08-12 | studio | `4cf8b107`, `1296cbc7` | The relief solver lands in `Geom`; contours traced on the server | The first terrain design: heights solved from marks | 4 | 02 |
| 22 | 2026-08-11/12 | studio | `5897944a`, `1ffb7728` | `tools/mapgen` builds fifteen boards from one JSON spec each (eleven Opus 5, four Haiku 4.5), Spinebreak among them; the author's fault list MG1–MG13 the same night | The first AI-made boards, and the first review of them | 6 | 03 |
| 23 | 2026-08-13 | mapgen | `7a6c15c1`, `aa429eb3` | pgm-studio-mapgen opens: ClayClay traced from a world; Opus 5's report that `tools/*` "is a reimplementation, not a caller" | The agent tells the author to delete the agent's own shortcut and use the real API | 7 | 03 |
| 24 | 2026-08-13 | studio | `6eec9b8b` | "A floating goal is the design, and gameplay questions have an oracle": the claim that every generated destroy map was unwinnable is withdrawn | The ask-the-author rule is born from a confident, wrong claim | 6 | 02 |
| 25 | 2026-08-14 | mapgen | `7573c380`, `43874f3e`, `78c7e4d2` | Runs 1–2: Haiku, Sonnet and Opus on the same kind of brief; Haiku's two boards "verified working" are 245-byte `map.xml` shells | The first model comparison, and the first false report of success | 6, 7 | 03 |
| 26 | 2026-08-15 | studio | `50caa477`, `f131ee21` | One `Finding` and one refusal envelope; `GET /api/rules` answers 125 rules | A refusal becomes something a caller can ask about by id | 7 | 02 |
| 27 | 2026-08-15 | mapgen | `500f5065` | Grok authors three maps blind, "no .NET 10, no MariaDB"; all three layouts "rasterize to no ground" | A model writing for a tool it cannot run | 7 | 03 |
| 28 | 2026-08-15 | studio | `0d8f68e7` | The model states its own range: the Thunder series cannot be expressed, "a limitation rather than a defect" | What the hub–approach model limits, written in by the author | 3 | 01 |
| 29 | 2026-08-19 | studio | `88bc0baa` | `GET /api/openapi/v1.json` and `/api-docs`: 131 paths; the commit records that `drive.py` "is the seventh driver" | The API describes itself, and says how undrivable it had been | 7 | 02 |
| 30 | 2026-08-20 | studio | `12b364fd` | `tools/mapgen` deleted: "the studio has one front door" | Every model now goes through the same API | 7 | 03 |
| 31 | 2026-09-02 | mapgen | `11d926f1` | rockymine and Ruediger_LP finish Opus 5's Millrace by hand in five hours: "essentially all that was done is theming and some dressing" | The clearest measure of what the tool left undone, and it was the look | 8 | 03 |
| 32 | 2026-09-02 | studio | `0976de79`, `378b2d58` | Text twins of every picture (`?format=text`); a copied tree cut out of a world and planted as a recipe | A model reads numbers instead of images; trees are copied, not grown | 7, 5 | 02 |
| 33 | 2026-09-05 | studio | `1e7d9aa8` | The slope axis: "the only thing in the model that tells a 45-degree hillside from a flat field" | Paint follows the ground's angle | 8 | 02 |
| 34 | 2026-09-09 | studio | `e6e9e231` | "Three rules stop reporting things that are not true": one board from fourteen findings to six | The recorded case of rules raising findings they should not | 6 | 02 |
| 35 | 2026-09-10 | studio | `6b0b3f09` | "Remove the grown tree": 496 lines deleted on the author's ruling | Trees are hard: the procedural tree is given up | 5 | 02 |
| 36 | 2026-09-19 | mapgen | `6c138ecb` | `WHAT-A-BOARD-IS-MADE-OF.md`: "None of it is enforced anywhere" | Taste is written down rather than gated | 8 | 03 |
| 37 | 2026-09-21 | mapgen | `32c77ef7`, `a8ea873e`, `b1c90b8f` | Haiku 4.5, Sonnet 5 and Opus 5 on the same four-objective brief, the same day: no Haiku board builds, all eight others export | The cleanest three-model comparison in the record | 7 | 03 |
| 38 | 2026-09-22 | studio | `c99de32c` | The first commit co-authored by Claude Opus 5.5 | From October it writes almost every commit | 7 | 02 |
| 39 | 2026-09-27 | studio, mapgen | `3be000d5`, `9a973906`, `656bd09f` | `render/eye` draws the world "with Minecraft's 1.8 block sprites"; the author's texturing rulings; nine grey boards painted | **Real textures**: the turning point the brief names | 8 | 02, 03 |
| 40 | 2026-09-26 → 09-28 | studio | `f7587f86`, `de77dc1a`, `71180895`, `31033891` | Discord sign-in, tokens, the build queue, and pgmstudio.de deploying itself from a green `main` | The browser studio goes live, and an agent gets a key | 7 | 02 |
| 41 | 2026-09-30 → 10-04 | studio | `38267335`, `a021d25d`, `c8a67337` | `PUT /map/{slug}/source`; the studio serves `GET /api/kit.py`; `GET /api/glossary` (226 terms) | The tool is something the AI uses: one authoring call, its own client, its own dictionary | 7 | 02 |
| 42 | 2026-10-07/08 | mapgen | `2169c018`, `57da19de` | Riftwater, the first freeform board written as voxels; pgmvox part 1; 86 commits on 8 October | A model stops driving the studio and builds directly | 9 | 03 |
| 43 | 2026-10-10 | mapgen | `0e90bfe6` | Studio against pgmvox, Sonnet 5.5 on both: "the two tools made boards of comparable quality"; the playtest's 30 faults, 9 the studio would have caught | The measurement behind the rethink | 9 | 03, 02 |
| 44 | 2026-10-15 | studio | `2ed975bc` | "The pgmvox port": nine phases, the author's decisions D1–D23 | The rethink of how a map is made | 9 | 02 |
| 45 | 2026-10-16 | mapgen (branch) | `0e7acb64` | Six blind AI entries to a Fire and Ice contest: "All six chose Destroy the Core" | The machines' entries, before the human's | 10 | 04 |
| 46 | 2026-10-18 | studio | `cc4cd3de` | "The plan retires as a level": the rectangle plan and the Plan tool go | The first approach is retired | 9 | 02 |
| 47 | 2026-10-24 | studio | `16864f7f` | "The group relief is retired: the modifier stack is the only terraforming" | Terrain rebuilt as ordered landforms: Hill, Ridge, Canyon, River, Lake | 4, 9 | 02 |
| 48 | 2026-11-02 → 11-07 | mapgen (branch) | `e85cc29a` … `92ee7f55` | The agents compose the author's sketch world into a map, and every version is rejected | "Every one of those failures passed some check that existed at the time" | 10 | 04 |
| 49 | 2026-11-13 | studio | `371e6935` | "The author froze the layout generator: nothing changes what the composer makes" | New capability pauses; bugs first | 9 | 02 |
| 50 | 2026-11-23 → 11-27 | studio (branch), mapgen (branch) | `ed354f43`, `4486636d` | The newest studio rulings (doors, schematics); the fire-and-ice study: reconstruction, viewer, labels, gated variants of the map the author built by hand | Where it stands now: a human-built map the tool can study but could not make | 10 | 02, 04 |

Two dates the record does not hold, and the film must not invent: the day the author built the fire-and-ice half
(somewhere between 2026-11-07 and 2026-11-27, `04` §4) and the day pgmstudio.de first answered publicly (before
2026-09-28, `02` Beat 7).

## Uploads to the public repositories, June to October (research `11`)

Dates the author read off the private repository and Discord, set against the commits of CommunityMaps and
PublicMaps. **Public** is a commit; **his account** is a date only he can give; times are as committed, with UTC where
the day shifts. Every Ruediger commit is `RuedigerLP`, committed through GitHub's web interface.

| Date (2026) | Map and event | Commit | Source | Status |
|---|---|---|---|---|
| 24 Jun 23:47 +0200 | Vauxite, Capture the Wool CTW, Drastic Change II added; the kit, `build-hole-1` and the bare team ids match the studio's export of that week | `caadb19f` | public | confirmed |
| 1 Jul 22:53 +0200 | Vauxite 1.0.1: spawn yaws, two-rectangle spawn unions, a build ceiling; a stray studio-written `region/map.xml` beside it | `7d647015` | public | his "2 July" differs by a day |
| 14 Jul 02:27 +0200 | Bridgid II (not a Brittlebush map; five commits to 02:42, `<created>` 12 July) | `a842b0bd` | public | confirmed |
| 14 Jul | Its side columns gave the wall-run pattern | first `wallRun` is `18d2c8ce`, 1 Aug 16:43 UTC | his account | differs: nothing links them |
| 27 Jul 23:33 +0200 | Kuusepuu CTC, Capture the Cake, credited "Claude Opus 5" | `8df2ca00` | public | confirmed |
| 28 Jul 01:10 +0200 | Hello World Mini / Micro, with a studio plan file (deleted 01:58); removed 12 Aug | `591d21b1` | public | confirmed |
| 6 Aug | Wandering U uploaded | none | his account | unverifiable |
| 7 Aug 20:58 +0200 | No Blocks Placed | `11a15f7d` | public | confirmed |
| 9 Aug 23:00 -0500 (10 Aug 04:00 UTC) | Cedar Crossing by arcadeboss, credited "SuperGrok" for "Map and XML" | `a3de15d2` | public | confirmed on 10 Aug in UTC; not the first model-credited map (Kuusepuu, 13 days earlier) |
| 12 Aug 23:20 +0200 | Viridian and Thornwake | `37bdef57` | public | confirmed |
| 24, 25, 31 Aug | maps uploaded, private | none | his account | unverifiable |
| 2 Sep 02:18 +0200 | Millrace 2.0.0 | `c86226db` | public | confirmed |
| 13, 20 Sep | maps added, private | none | his account | unverifiable |
| 27 Sep 21:55 UTC | Delverdale and Whitstone Weald committed in this project; the PrivateMaps upload is not visible | `d274c0ae` (mapgen) | public / his account | boards confirmed, upload unverifiable |
| 5-8 Oct | Countryside imported into pgmstudio.de (five rows) | listing of 26 Nov | public | recorded |
| 9 Oct | Alphaboy uploads Countryside | `06138ebd`, 14 Oct 23:13 -0300 (15 Oct 02:13 UTC), by Javggg | his account / public | differs by five days |
| 11 Oct | 803 re-made in the browser (`rockymine-5`) | listing of 26 Nov | public | recorded |
| 19 Oct 22:41 +0200 | 803 2.0.1, carrying the studio's pre-11-October XML | `091b378d` | public | confirmed |

## Activity — the data for the on-screen curve

**pgm-studio, commits per ISO week**, all commits reachable from `origin/ccr-875c17a4-2yjgux` (`02`, "Commit
activity per week"). The curve should plot the first column and may mark the four annotated peaks and troughs.

| Week | Dates | Commits | Non-merge | Annotation for the curve |
|---|---|---|---|---|
| W24 | Jun 08–14 | 35 | 35 | the port |
| W25 | Jun 15–21 | 156 | 156 | |
| W26 | Jun 22–28 | 63 | 63 | |
| W27 | Jun 29–Jul 05 | 114 | 114 | graph dropped, composer starts |
| W28 | Jul 06–12 | 60 | 60 | |
| W29 | Jul 13–19 | 174 | 174 | |
| W30 | Jul 20–26 | 105 | 105 | |
| W31 | Jul 27–Aug 02 | 122 | 120 | |
| W32 | Aug 03–09 | 103 | 103 | |
| W33 | Aug 10–16 | 377 | 356 | **peak**: houses, trees, relief, tool docs, one Finding, rules API |
| W34 | Aug 17–23 | 176 | 176 | |
| W35 | Aug 24–30 | 120 | 117 | |
| W36 | Aug 31–Sep 06 | 169 | 168 | |
| W37 | Sep 07–13 | 64 | 64 | |
| W38 | Sep 14–20 | 61 | 60 | |
| W39 | Sep 21–27 | 127 | 109 | textures |
| W40 | Sep 28–Oct 04 | 261 | 215 | **second peak**: deploy, tokens, queue, kit.py, glossary |
| W41 | Oct 05–11 | 95 | 71 | |
| W42 | Oct 12–18 | 142 | 123 | pgmvox port begins, plan retires |
| W43 | Oct 19–25 | 50 | 40 | modifier stack, carves |
| W44 | Oct 26–Nov 01 | 70 | 61 | |
| W45 | Nov 02–08 | 19 | 14 | |
| W46 | Nov 09–15 | 31 | 25 | freeze |
| W47 | Nov 16–22 | 0 | 0 | |
| W48 | Nov 23–29 | 2 | 2 | branch only |

By month (`02`): June 258, July 513, August 861, September 469, October 543, November 52.

**The model behind the commits, per month** (`Co-Authored-By` trailers in pgm-studio, rows of 3 or more, `02`).
This is the data for a stacked band under the curve.

| Month | Trailers |
|---|---|
| 2026-06 | Opus 4.8 255 |
| 2026-07 | Opus 4.8 312 · Fable 5 121 · Opus 5 73 · Opus 5 (1M) 4 |
| 2026-08 | Opus 5 461 · Opus 5 (1M) 187 · Opus 4.8 67 · bare "Claude" 47 · Sonnet 5 30 · Fable 5 26 · none 25 · "Claude Sonnet" 14 |
| 2026-09 | Opus 5 180 · Opus 5.5 176 · Opus 5 (1M) 74 · none 27 · Fable 5.1 9 |
| 2026-10 | Opus 5.5 414 · none 90 · Sonnet 5.5 32 · Sonnet 5.5 + Opus 5.5 7 |
| 2026-11 | Opus 5.5 36 · bare "Claude" 9 · none 7 |

**pgm-studio-mapgen has no weekly table in the research.** What it holds are its busiest days (`03`, end of §1):
8 commits on 2026-08-13, 34 on 08-25, 52 on 09-19, **86 on 10-08** and 92 on 10-10, and 5 commits in total from
10-24 to 11-27. A weekly mapgen curve needs a fresh `git log` count before it is drawn.

**The early repositories, as commit totals only** (`01`): CTW-Layout-Generator 5 commits (2025-09-28 → 10-03);
MinecraftLayoutEditor 112 on `master` (2025-10-10 → 11-16, plus branches); pgm-map-studio 95 on `master`
(2026-05-31 → 06-12). On the curve they are three short bursts before a gap of five and a half months.

**The words a model must read**, for the context visualisation (`03` §3, `wc -w` of the must-read set at each date):
12,620 (08-13) · 11,030 (08-14) · 7,861 (08-16) · 8,643 (08-19) · 3,267 (08-22) · 4,862 (08-26) · 7,099 (09-02) ·
13,773 (09-13) · 10,818 (09-20) · 14,729 (09-30) · 16,378 (10-12) · 16,505 (11-27), and 39,860 on 11-27 with the
skills and the two gameplay documents.
