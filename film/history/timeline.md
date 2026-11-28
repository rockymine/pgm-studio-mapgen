# Timeline, February 2025 to November 2026

One table, in date order. **Kind** says what a row is: **record** (a commit, file, published map, server record,
recording, message or transcript holds it), **account** (the author recalls it, `author-account-2026-11-27.md`,
instalment given as §N), **inference** (a reading made for this history; its basis is the source named). Where a date
is the author's and the record differs, both rows are given. Times are UTC; German summer time is UTC+2 to 25 October.
`r/NN` is `research/NN`, `s/NN` is `research/sessions/NN`; **API** is
`sources/match-status/api-matches-not-in-match-status.csv` (read in r/16), **log** the `#match-status` CSV (r/13);
**pictures** are `sources/early-experiments/`. Match times are starts. Commit times of the early repositories are given
in the committer's zone where marked (+01:00, +02:00). The thread of 20–24 September and the direct messages with four
people carry role labels instead of names, by the author's decision of 28 November (README).

| Date (UTC) | Event | Source | Kind |
|---|---|---|---|
| 2021-01 to 2023-02 | Annealing, II, III, IV and II Short, rockymine with Ruediger_LP and DerStiv | r/08 | record |
| 2022 | The Annealing maps came from his master's thesis on the travelling salesman problem | account §3 | account |
| 2015-04-26 | Agrostid created (rockymine, Matci0B; XML Ruediger_LP), built away from 0,0 in one region file at x −1024 to −513 | r/19 | record |
| 2024-10-14 19:07 | Agrostid 2.0.0 (RuedigerLP): the map moved to 0,0, the old region file kept, the later "stowaway" | r/19 | record |
| 2025-02-11 | To samschaap: "Potential Algorithm steps" (grid nodes, spanning tree favouring straight edges, extra edges for cycles, dissecting for islands, a grid for wave function collapse) and a "Data survey" of his and Ruediger's CTW maps as 1×1 cells | sources/early-experiments/2025-02-11-message-to-samschaap.md; account §20 | record |
| 2025-02-11 | The first v0 prototype, `v0-occ-mapmaking-tools-b63noa.vercel.app`: grid size and node count, spanning trees, shaded cells; "So the earliest v0 prototype made rsts" | the same; account §20; sources/early-experiments/v0-prototype-2025-02 | record (his description; the page, "Random Spanning Tree Visualization", seen as it runs on 28 Nov 2026) |
| 2025-02-11 | samschaap: "so it will be 'trained'"; he: "an educated, rule-based approach is more likely for me to achieve than actual training"; Townside as grid and as a torch graph with a green-carpet cycle edge | the same | record |
| 2025-04-05 | matplotlib figure "Multiple 1-Team PvP Layouts (Improved Graph Connections)": four node-and-edge layouts of one team's half | pictures; account §18 | record (picture); no repository holds it (r/18); the tool is not known, perhaps ChatGPT (account §21) |
| 2025-05-24 01:39 (local) | Claude chat artifact "Interactive Level Design Visualizer", v6 of 6: a "Level Design Generator" with lanes, a void strip, void connections | pictures; account §18 | record (picture) |
| 2025-05-24 | "da gab es noch kein Claude Code, soweit ich mich entsinne" | account §18 | account |
| 2025 | Tools in turn, by the author: ChatGPT and other models in a single chat; v0, the first to make several files and host a prototype; Gemini as an alternative; then Claude, kept | account §21 | account |
| 2025-08-16 21:31–23:11 | v0 chat, 17 messages: "implement this layout generation…" (one attachment); renamed "Capture the Wool Layout Generator" at 21:54; mirror against rotate, random 3×3 grids, row-independent columns | sources/early-experiments/v0-chat-2025-08-16.md | record |
| 2025-09-24 22:10–22:15 | The v0 chat used again; what was asked is not in the page | sources/early-experiments/v0-chat-2025-08-16.md | record |
| 2025-09-26 | Ruediger, to a screenshot of the Gemini tool: "ich frag mich ja wann der erste alle maps eincannt und ne ki anhand der daten eine eigene map erstellen lässt" | r/15; account §18 | record |
| 2025-09-28 00:42 | `CTW-Layout-Generator` opens as an AI Studio app; shown to the contest's map developer: "it was made using gemini" | r/01, r/17, r/18 | record |
| 2025-09-28 → 10-03 | Its generator: 3×3 grid per team, "Standard"/"Row-Independent", "Mirror"/"Rotation"; JSON export; step-wise manual editor; last commit 3 Oct | r/01; the clone's `Documentation.tsx` | record |
| 2025-09-28 | It continues the v0 generator in algorithm and name; no shared code shown | HISTORY ch. 1 | inference |
| 2025-09-29 | To Ruediger: "vielleicht kommt man damit in richtig ki generierung" | r/15 | record |
| 2025-10-07 | AI Studio link to Ruediger, "nur manueller editor. klappt auch ganz gut am telefon": the second AI Studio project, "CTW Smart Map Editor", a graph editor with mirrored nodes, automatic node classes (hub, frontline, scaffold) and an unconnected Gemini analysis he did not know of | account §18, §24; `sources/early-experiments/aistudio-ctw-smart-map-editor-2025/` | record (message; export); author's account (that it was this link) |
| 2025-10-07 | To the contest's map developer: tool moved to his own repository `ctw-layout-editor`, mostly written with Claude's VS Code extension | r/17 | record (no such repository found, r/18; the author thinks it differs from the next row, account §18) |
| 2025-10-10 14:29 (+02:00) | `MinecraftLayoutEditor` (C#): a `Graph` of typed nodes; "with a friend", no WorldEdit (his message) | r/01, r/17 | record |
| 2025-10-11 | Symmetry, mirror, rotate (`4d132b2`); first screenshots to Ruediger | r/18; account §18 | record; account |
| 2025-10-12 | `.schematic` download (00:13), edges as Bresenham lines of blocks (20:05); Ruediger fascinated that blocks need no hands | r/18; account §18 | record; account |
| 2025-11-04 | First okay layout, drawn in the browser, imported on the mapmaker server | pictures; account §18 | account (no commit names it, r/18) |
| 2025-11-06 03:20 | World import "(claude & grok)": the first models named in a commit; no file names the world imported | r/01, r/18, r/19 | record |
| 2025-11-06 | The first world imported was Agrostid, not Annealing | account §25 (corrects §18) | account (the picture's 184 × 267 fits Agrostid's extent, r/19, inference) |
| 2025-11-06 | World import "showing a few XML regions" | account §18 | account (XML regions arrive 10 Nov, r/18) |
| 2025-11-10 00:17–00:40 | XML import and region rendering in the editor | r/18 | record |
| 2025-12-09 | Claude named to Ruediger for the match-logging plugin, "claude hat gut gearbeitet" | r/15 | record |
| 2025-12-20 | Last human commit in `MinecraftLayoutEditor`, "ui improvements (claude)" | r/18 | record |
| 2025-12 → 2026-02 | A small pause, "bis Februar auf jeden Fall" | account §18 | account (no commit in four repositories 21 Dec – 30 Jan, r/18) |
| 2026-01-18 | First day with a logged match in the author's chart (6 matches, a Sunday) | sources/early-experiments/2026-ctw-match-activity.md; account §21 | record (read off a picture) |
| 2026-01-24 | Match logs exist (file names, a Tumbleweed match) | r/18 | record |
| 2026-01-26 (about) | Islands found and cut into polygons by Claude's scripts | account §18 | account (not shown or contradicted, r/18) |
| 2026-01-26 → 02-01 | Mame, I Shrunk the PvPers among the week's longest matches, 1 h 58 min | sources/early-experiments/2026-ctw-match-activity.md | record (read off a picture) |
| 2026-01-31 23:55 (+01:00) | `CTWAnalysis` opens with 67 files: islands, triangulation, skeleton, XML parser, match analysis, "Built with Claude Code" | r/18 | record |
| 2026-02-02 | Inter-island connectivity: the graph returns as a skeleton graph | r/18; account §18 | record |
| 2026-02-02 / 03-08, 03-14 | 689, then 3,000 logged matches; 177 maps "dokumentiert für die ki" | r/15 | record |
| 2026-02-13 | Triangle meshing removed | r/18 | record |
| 2026-03-09 | "Total matches processed 2,452", 177 unique maps | r/18 | record (the author: about 4,000, account §18; the chart's table 2,450, account §21) |
| 2026-03-08 | Last day with a logged match in the chart; the table sums to 2,450 matches on 46 days | sources/early-experiments/2026-ctw-match-activity.md; account §21 | record (read off a picture) |
| 2026-03 | Logging ends | r/17 | record |
| 2026-03-14 04:04 (+01:00) | CTWAnalysis renders every map's layout block by block (`007c157`), after `ctw layout --all` the evening before | r/19 | record |
| 2026-03-14 15:46 / 20:17 | Sam: "Agrostid: remove stowaway", "MIStP: remove stowaway" (Mame, I Shrunk the PvPers) | r/19; #maps-changelog | record |
| 2026-03-14 22:46 (+01:00) | CTWAnalysis: per-map island exclusions, `agrostid` and `mame_i_shrunk_the_pvpers` listed; `exclude_islands`, `playable_bbox` the next day | r/19 | record |
| 2026-03-16 18:26 | Sam: "Wintertime: 1.0.4", "Remove stowaway"; the last of three commits using the word | r/19 | record |
| 2026 (spring) | Sam names the leftover islands "stowaway"; found on very many maps; Mame "practically a complete second copy"; "good opportunity to dev phase that map and forget about it" | account §25 | account (three maps in the record) |
| 2026-03-19 | To Ruediger: "ai maps soon tm" | r/15 | record |
| 2026-03-19 22:05 | CTWAnalysis `a624eb5`: decoration above the build ceiling corrupted terrain heights "for 143 of 177 maps (81%)", the 143 of the next reply | r/19 | record |
| 2026-03-19/20 | Claude Code: "if we simply reverted the pipeline"; Ruediger "just begs for the first ai generated map"; Annealing IV's island a TSP tour; "the 143 contaminated maps" | pictures; r/18 | record (dated by `6cbc9dd`, 20 Mar 00:19 +01:00; "143" in no file) |
| 2026-04-26 | The contest's map developer on another person's AI DTM map: "I don't think any version of that ai map would play well" | r/17 | record |
| 2026-05-13 | He asks whether AI maps are accepted in a contest; the award show's organiser: "no AI for creative stuff" | r/17 | record |
| 2026-05-14 → 24 | CTWAnalysis's browser viewer with XML region overlays (14 May), region drawing (15, 22–24 May) | r/18 | record |
| 2026-05 | PGM Studio began as a view of XML files; regions, then polygons | account §18 | account (the steps are CTWAnalysis's, r/18) |
| 2026-05 | The motive for XML in the browser: XML a hurdle many map makers shy away from, Ruediger wrote many of his; draw regions, answer simple questions, defaults for the standard case | account §25 | account |
| 2026-05-29 | `/concept`: island polygons drawn on a blank canvas; to Ruediger: his polygon drawing is being built; to an administrator: the project is "an offspring from the logging experiment" | r/18, r/15, r/17 | record |
| 2026-05-31 18:41–20:53 | CTWAnalysis's old commands removed, "superseded by map viewer" | r/18 | record |
| 2026-05-31 22:01 | `pgm-map-studio` (Python, Sonnet 4.6 and Opus 4.8) opens, reading worlds for islands | r/01, r/18 | record |
| 2026-06-03 | Seven port documents in CTWAnalysis | r/18 | record |
| 2026-06-10 | To the award show's organiser: "opus is scary good"; the same of Fable 5 | r/17 | record |
| 2026-06-12 03:24 | Last Python commit; `pgm-studio` first commit 17:21 | r/01 | record |
| 2026-06-13 | Port to ASP.NET Core + Blazor, 145 files, Opus 4.8; "zum dritten Mal neu geschrieben" | r/01, r/15 | record |
| 2026-06-17 → 21 | Claude names "Cobalt Crossing" and writes its XML; it becomes Drastic Change II | r/15 | record |
| 2026-06-19/20 | Ruediger proposes the evenings' method: generate many, test the best ten in one evening | r/15 | record |
| 2026-06-20 | Corpus: "88% of real maps carry a contested middle"; organic spline generator starts | r/01, r/08 | record |
| 2026-06-23 | "habe die erste xml geladen und pgm hat sie angenommen" | r/15 | record |
| 2026-06-24 21:47 | Vauxite, Drastic Change II, Capture the Wool CTW to CommunityMaps, with the studio export's traces | r/11 | record |
| 2026-06-24 21:51–22:15 | The three played on server-2 (36, 32, 33 players); not in the log | API, r/16 | record |
| 2026-06-24 | The first maps whose XML he made in the browser; concepts, terrain, colours human | account §5, §8 | account |
| 2026-06-26 17:11 | Sketch tool shape library planned: "Polyomino primitives ("tetris +")", L/U/T/I/scythe | r/19 | record |
| 2026-07-01 20:53 | Vauxite 1.0.1 adds a build ceiling | r/11 | record |
| 2026-07-01 23:21 | The author specifies the 8×8×8 bedrock shell for spawn and wool | r/09 | record |
| 2026-07-02 07:37 | The squared-paper photo, "as a general seed for testing"; misread as a staircase | r/09 | record |
| 2026-07-02 09:09 → 12:08 | Corner coordinates; Base 2-Island right; Base 4-Team 11:13; Base 2-Wool 11:21 | r/09 | record |
| 2026-07-02 | The drawing is the two-team map | account, squared-paper correction | account |
| 2026-07-02 | He had already traced maps into seed files | account, squared-paper correction | account (contradicted, r/09) |
| 2026-07-02 14:31 / 14:54 | Plan-graph design document replaced by areal pieces and interfaces | r/08 | record |
| 2026-07-02 17:10 / 19:26 | To TTtie: "We have a system to auto-generate maps now", "i will not look at them before"; three Base zips sent | r/17 | record |
| 2026-07-02 19:40 | Screen recording begins; the Base maps walked on mapdev by rockymine, Ruediger, TTtie, samschaap | r/16 | record (voices named by the author) |
| 2026-07-02 20:21 | PrivateMaps `711e539` "Irongate Harbor remove dev phase" | r/15, r/16 | record |
| 2026-07-02 20:21 | That commit carried the Base maps; its message is Ruediger's joke about a stalemating map put into the dev phase | account §18 | account (file list unread) |
| 2026-07-02 20:23–20:38 | Base 2-Wool (26), Base 2-Island (28), Base 4-Team (33) on server-2; polls 3 of 4 | API, r/16 | record |
| 2026-07-02 21:21 | Fix `7576a6c4`: exported worlds crashed the 1.8 loader ("Claude had to fix it", in the call) | r/09, r/16 | record |
| 2026-07-02 22:47 | Plan model; `FannedGraph` enters, still in the studio | r/09, r/08 | record |
| 2026-07-04 | Composer starts; first real map traced into a seed; "that's the road to ai maps" to TTtie | r/01, r/09, r/17 | record |
| 2026-07-05 12:34 / 18:12 | `tools/seeds/teaching/` opens (build interface, "only to inform `layout-rules.md`"); frontline and middle teaching sets with labelled ids, nine rule amendments | r/19 | record |
| 2026-07 (beginning) | Teaching files in the plan format, middle zones for example; "Sobald das Planformat dann da gewesen ist, hat es einfach sehr geholfen" | account §25 | account |
| 2026-07-08 06:39–17:20 | Deriver names wool lanes I/L/Z/complex; hand-labelled lane examples and five reference lanes "where the id carries the intent" | r/19 | record |
| 2026-07-08 23:43 (stamp) | Two tablet sketches of wool-lane shapes | sources/july-2026-shapes/ | record (zone of the stamp not recorded) |
| 2026-07-08 | Tetris pieces as the generator's root; unsure whether a generator existed | account §25 | account (the composer existed from 07-04, r/19) |
| 2026-07-09 18:26–18:36 | Ruediger: "was sehe ich?"; the author: shapes of wool lanes, to label and give to Claude | sources/july-2026-shapes/ | record |
| 2026-07-09 20:48 / 21:09 | Single-file offline plan editor in the studio (`tools/mobile/plan-editor.html`), made mobile-friendly | r/19 | record |
| 2026-07-09 21:31–22:45 | `pgm-studio-mobile`: three commits, rockymine with Opus 4.8, a PWA plan editor with three example plans | r/19 | record |
| 2026-07-09 22:28 | Link to Ruediger; "aber nur das planning tool oder?" | sources/july-2026-shapes/ | record |
| 2026-07-10 19:08 → 23:05 | Box partition ("typed spawn/hub/frontline/mid boxes"); wool-approach catalogue: donut, scythe, H, plug; emitted as plans | r/01, r/19 | record |
| 2026-07-11 07:13 / 07:39 | "Ich verwirre die KI"; "er hat sich ein zu statisches system gebaut" | sources/july-2026-shapes/ | record |
| 2026-07-11 11:54 | The piece vocabulary: entry, entry-bar, leg, room-bar, room-run, room | r/19 | record |
| 2026-07-11 13:27 / 16:25 | "eine Box für Frontline, Hub, Spawn und Wool(s)"; three catalogue pictures (Plug, H, Scythe); Ruediger: "ja gute idee lass am abend reden!" | sources/july-2026-shapes/ | record |
| 2026-07-14 00:27 | Bridgid II to CommunityMaps; played 00:31 and 00:53 | r/11, API | record |
| 2026-07-14 | Bridgid II: layout in the browser in a day, skinned in game in an evening; side columns gave the wall run | account §5 (corrected) | account |
| 2026-07-14 | Ruediger: "bridgid 2 nochmal testen?" | r/15 | record |
| 2026-07-15 | Destroy modes; organic generator retired; Bridgid II's first log match | r/01, r/08, r/13 | record |
| 2026-07-17/18 | Capture the Cake designed with Ruediger, loaded the same night | r/15 | record |
| 2026-07-21 | "the box pipeline is THE composer"; TTtie sees a spawn far from its wool | r/01, r/17 | record |
| 2026-07-27 21:33 / 23:10 | Kuusepuu CTC ("CTC conversion: Claude Opus 5"); Hello World Micro, "grey map for concept test" | r/11, r/13 | record |
| 2026-07-27 21:42 → 07-28 00:30 | Kuusepuu CTC three times, Hello World Micro twice (API); Base 4-Team 00:30 (log); "we now have AI maps on occ" | API, r/13, r/17 | record |
| 2026-07-27 | Kuusepuu is not an AI map; Hello World Micro's layout is Hello World's on the grid, drawn by him | account §6, §14 | account |
| 2026-07-31 | Kuusepuu CTC 1.0.3 "Reported live"; moving-room timing by Ruediger | r/06, r/15 | record |
| 2026-07-30 | 19 commits by a Claude session on an unmerged `MinecraftLayoutEditor` branch | r/18 | record |
| 2026-08-01 | Terrain painting "walls, rims, plateaus"; wall run | r/05, r/11 | record |
| 2026-08-02 | Grown tree as Catmull-Rom limbs | r/10 | record |
| 2026-08-06 20:11 / 20:15 / 20:17 | `wandering-u.zip` sent; PrivateMaps "Wandering U: added"; played on server-1, 36 players | r/15, API | record |
| 2026-08-06 | Wandering U: layout his in text, XML Claude's; players fell from the moving room | account §8, §2–§3 | account |
| 2026-08-07 18:58 / 19:01 | No Blocks Placed to CommunityMaps; played, 46 players, 15 min 35 s | r/05, API | record |
| 2026-08-09/10 | Three match-flow commits in CTWAnalysis, the data behind the gameplay documents | r/18 | record |
| 2026-08-10 04:00 / 04:04 | Cedar Crossing (arcadeboss, SuperGrok) uploaded and played: the first match on a map no person laid out | r/11, API | record |
| 2026-08-11/12 | The first fifteen through `tools/mapgen`, 11 Opus 5 and 4 Haiku 4.5; MG1–MG13 | r/03 | record |
| 2026-08-12 21:13 | PrivateMaps deletes the three Base maps and Wandering U | r/15 | record |
| 2026-08-12 21:19 → 21:54 | Thornwake and Viridian on mapdev, to CommunityMaps 21:20, played on server-1 21:43 and 21:54: this project's first composed boards in play | r/15, r/11, API | record |
| 2026-08-13 | Floating-goal claim withdrawn; ask-the-author rule; mapgen repository opens | r/02, r/03 | record |
| 2026-08-13/14 | Trial runs: Haiku's 245-byte shells ("10 lines of xml, no teams" to TTtie); a 27-block obsidian cube | s/04, r/14, r/17 | record |
| 2026-08-14 | His review becomes 48 entries, `B162` obsidian at most three | r/14 | record |
| 2026-08-14 | The quartz board is Quillon Saltworks; Sable Marsh, Cairnmeadow, Cinderreach named as faulty | account §10, §12 | account |
| 2026-08-14 | Ashfall Scar (Sonnet run 2): the flat line-up map, 250 × 190 | r/03; account §12 | record; confirmed by the author |
| 2026-08-15 | One Finding, rules API; "Hab jetzt ein repo für die ganzen slop maps" | r/02, r/15 | record |
| 2026-08-16 | Sunspit by Fable to a specific brief; dead-ground measure | s/05, r/05 | record |
| 2026-08-19 | `DC3` enforces the obsidian cap | r/14 | record |
| 2026-08-22 | Hollow Crown (Haiku 4.5): the monument inside the core | r/05; account §12 | record; account |
| 2026-08-24 18:58 / 19:05 | 6 maps sent; PrivateMaps "Add a few very human maps for testing" | r/15 | record |
| 2026-08-24 19:08–19:50 | First test evening: Hollowbank, Sunspit, Siderite Bowl, Hollowmarch, Cairnmeadow, Elderwold on server-1 | API, r/16 | record |
| 2026-08-24 | To the award show's organiser: "Most of them were just 'Build a map' without any prompting whatsoever"; PrivateMaps commit "reorganize the slop" | r/17, maps-changelog | record |
| 2026-08-24 23:48 | Friend's "Liminal DTM" prompt opens the session of Interchange, Overwall and Aerie | s/06 | record |
| 2026-08-25 20:37 | Tarnfell played | API | record |
| 2026-08-25 | Aerie's XML unplayable | sessions list; account §11, §12 | account (no record; the model reported the gate open) |
| 2026-08-28/29 | Made things named; Slipway's ship and balloons | s/07 | record |
| 2026-08-30 | His basin; Millrace (Opus 5), Cutwater and Fallowmere (Sonnet 4.5) | r/03 | record |
| 2026-08-31 21:00–21:18 | Brackenfold and Millrace (API), then Hollowmarch (log) | API, r/13 | record |
| 2026-08-31 | The Millrace played was the model's, before the hand finish | HISTORY ch. 7 | inference |
| 2026-09-02 00:18 / 00:28 | Millrace 2.0.0 to CommunityMaps; played ten minutes later | r/11, r/13 | record |
| 2026-09-02 | Five hours of hand finishing with Ruediger; Fable 5.1 diffs it; tree world committed 00:53 | r/03, s/02, r/05 | record |
| 2026-09-02 | Fable's tree copying led him to add his tree world | account §1 | account (order contradicted, r/05) |
| 2026-09-02 23:01 | Alderfen Holm from a player's prompt; four cores | s/08 | record |
| 2026-09-04 | "made by" sign left off where nobody is named (69 of 74) | r/07 | record |
| 2026-09-04 22:21–23:51 | Millrace (log); seven event matches 22:36–23:04, Lodestar Yard twice (API); six August boards after (log) | r/13, API | record |
| 2026-09-05 | Sunspit rebuilt, Hollowmarch flattened; slope axis | s/09, r/02 | record |
| 2026-09-09/10 | Ten agents paint his drawn layout | s/10 | record |
| 2026-09-11 23:32 | Sonnet run brief asks for underground passages; Kilnholt Cut's hollow causeway | s/11 | record |
| 2026-09-12 | "slop sunday", Ruediger's name; to TTtie "Opus is better at making maps than Fable" | r/15, r/17 | record |
| 2026-09-12 22:03 | The studio reads, stores and writes shops and shopkeepers (PG9, PG10); Mame's item shop in its documentation | r/19 | record (a feature he asked for, by account §25) |
| 2026-09-13 21:39–22:55 | Eleven matches in Ruediger's order, Kilnholt Cut first; Glassmere 15 min 47 s, the longest destroy match of the project | API, r/15 | record |
| 2026-09-14 | Mirkholt corrected by two messages | s/12 | record |
| 2026-09-18 | TTtie: "those kinda finally start looking like real maps" | r/17 | record |
| 2026-09-19 | `WHAT-A-BOARD-IS-MADE-OF.md`: "None of it is enforced anywhere" | r/03 | record |
| 2026-09-20 21:53–22:45 | Eight matches, Peatgarth twice; Millrace after (log) | API, r/17, r/13 | record |
| 2026-09-20 23:48 → 09-24 | Forum thread "stop AI maps from being played at all", 247 messages kept | r/17 | record |
| 2026-09-21 | Haiku 4.5, Sonnet 5, Opus 5 on one brief | r/03 | record |
| 2026-09-22 | First Opus 5.5 commit | r/02 | record |
| 2026-09-24 | Scarbutte and three more, terrain only | s/13 | record |
| 2026-09-26 → 28 | Discord sign-in, tokens, queue, pgmstudio.de self-deploys on a small Hetzner machine | r/02, r/17 | record |
| 2026-09-27 20:58 | Ruediger's announcement in the event channel, "Slop Sunday … happening now! testing some ai assisted maps", a minute before the first match; a skull 13 times among the reactions (28 Nov) | sources/slop-sunday-announcement; account §19 | record |
| 2026-09-27 | The contest's map developer: going public "concerning" | r/17 | record |
| 2026-09-27 20:59–22:36 | Thirteen matches: eleven from `/event add`, then Delverdale and Whitstone Weald; teams "Claude" and "Anti-Slop" win two | API, r/15, r/16 | record |
| 2026-09-27 22:36 | To an administrator: "that was the prompt for the last two" | r/17 | record |
| 2026-09-27 | The last AI-map test | account §2 | account (no later evening in the log or the API to 27 Nov) |
| 2026-09-28 | Map notes pinned to ground; a player from the event reviews the tool | r/05, r/15 | record |
| 2026-09-29 | Gypsum Reach and Sootcombe worked through notes in five rounds | s/14 | record |
| 2026-10-03 | To a developer of the website: "i wanted a layout editor and then claude was just too good at it and Ruediger wanted ai maps" | r/17 | record |
| 2026-10-05 → 08 | Countryside drawn in the studio | r/11 | record |
| 2026-10-07 22:21 / 22:26 | "what if like an agent didn't need to rely on the current way…"; ingredients and mode | s/00 | record |
| 2026-10-07 | He told a session he did not like the layer model; gave nothing to the first board | account §1, §7 | account (differs in form, s/01) |
| 2026-10-08 05:42 | "Ok. This is a whole different class of map." | s/01 | record |
| 2026-10-08 | Some twenty freeform boards, among them Lantern Pass, Lantern Drop, Spark, Curio Square, Loomfall; `pgmvox` begins | s/01; mapgen log | record |
| 2026-10-09 | Brittlebush read; `pgmvox.grammar`; Brittlebush III built from his plan | r/05 | record |
| 2026-10-09 | Alphaboy uploads Countryside | account §5 | account (repository: 15 Oct UTC) |
| 2026-10-09/10 | Notes sorted: 30 faults, 9 the studio would catch | r/05, r/06 | record |
| 2026-10-09/10 | Viewing of the new pgmvox boards on mapdev, five present (the author, Ruediger, TTtie, mitchiii, wylt): Hollowcrown, Lantern Karst, Hollow Mesa, Riftwater; not a test | account §13, §15, §18 | account |
| 2026-10-09/10 | Observer chat: "are all these ones unmodified from generated state?"; "its over for m*pdevs."; "again, layout is 100% mine" | sources/staff-chat-october | record (the date is the author's) |
| 2026-10-09/10 | They decide to pause; later: a month of weekly testing, the tool needing care | account §13, §14 | account |
| 2026-10-10 | Studio against pgmvox, Sonnet 5.5: comparable; Ruediger proposes finishing the three best | r/03, r/15 | record |
| 2026-10-10/11 | Contest may list the studio "As long as they can't use the opus function" | r/17 | record |
| 2026-10-11 | The award show's organiser on studio XML: "it shouldn't be 'advertised'"; model-made maps hidden in the studio; "AI maps being banned" (a player) | r/17 | record |
| 2026-10-15 | `docs/pgmvox-port.md`; fire-and-ice study forms | r/02, r/04 | record |
| 2026-10-16 | Six blind AI entries to a Fire and Ice contest, all DTC; Viridian in the log | r/04, r/13 | record |
| 2026-10-17 (about) | He begins the hand-built fire-and-ice map | account §14 | account |
| 2026-10-19 | 803 2.0.1 with studio-made XML; "Genug Material haben wir ja." | r/11, r/15 | record |
| 2026-10-22 | Coldstore: "finished and the map.xml a success" | r/03 | record |
| 2026-10-24 → 25 | Modifier stack replaces relief; carves | r/02 | record |
| 2026-11-02 → 07 | Agents compose his sketch world; every version rejected | r/04 | record |
| 2026-11-04 | Port: every phase shipped or parked; grammar has no shipped line | r/02 | record |
| 2026-11-11 | Contest without submissions: "You can't call it a contest if it's me vs you" | r/17 | record |
| 2026-11-11 | That contest is the cancelled fire-and-ice contest | account §18 | account |
| 2026-11-13 / 14 | Layout generator frozen; last commit on `main` | r/02 | record |
| 2026-11-23 / 26 | The award show's organiser asks him to present "best newcomer" at the Mappys; the "Prompt-a-Map Sketch" sent | r/17 | record |
| 2026-11-25 | To the contest's map developer, of the fire-and-ice map: "Note that it still is not AI. Just having claude follow along." | r/17 | record |
| 2026-11-27 | Study of the hand-built map committed; the API read; "which important big ai fails did i miss?" | r/04, r/16, r/17 | record |
| 2026-11-27 21:46 | Lantern Pass played, 49 players, 1 min 8 s | account §15, §16 | record (match page, API) |
| 2026-11-27 23:53 → 11-28 00:13 | Loomfall, Lantern Drop, Spark, Curio Square: the first freeform boards on the public servers | account §16 | record (API, as given) |
| 2026-11-27/28 | Lantern Pass liked but short; Loomfall "a bit bugged"; Lantern Drop "just worked"; Curio Square "okay" | account §14, §16 | account |
| 2026-11-28 | The five voices of 2 July named; the fire-and-ice map is the one Minuyo took for AI | r/16; account §17 | account |
| 2026-11-28 | Early pictures, the message of 11 February 2025 and the v0 link; answers on the viewing, the contest, `711e539`; names withdrawn from the thread and four conversations | account §18–§20 | account |
| 2026-11-28 (planned) | Real gameplay to be recorded on a few maps | account §14 | account (plan) |

## Counts behind the table

These are not events; they are the data a chart of the year would use, kept from research/02, research/03 and
research/16.

- **pgm-studio commits per month** (all commits on the newest branch): June 258, July 513, August 861, September 469,
  October 543, November 52; the busiest week is 10–16 August (377) (r/02).
- **Model trailers per month in pgm-studio**: June Opus 4.8 255; July Opus 4.8 312, Fable 5 121, Opus 5 73; August
  Opus 5 461 (+187 1M), Opus 4.8 67, Sonnet 5 30; September Opus 5 180, Opus 5.5 176; October Opus 5.5 414, Sonnet 5.5
  32; November Opus 5.5 36 (r/02).
- **pgm-studio-mapgen's busiest days**: 8 commits on 13 August, 34 on 25 August, 52 on 19 September, 86 on 8 October,
  92 on 10 October; 5 in total from 24 October to 27 November (r/03).
- **Matches**: the log holds 41,872; the API 388 more on server-1 and server-2 in the same window, and 3,628 on the
  ranked servers (r/16). Players per test evening, by the API: 26–33 (24 Aug), 21–39 (4 Sep), 37–59 (13 Sep), 34–56
  (20 Sep), 44–60 (27 Sep).
