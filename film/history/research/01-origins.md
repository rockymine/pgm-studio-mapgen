# 01 — Origins: before pgm-studio, and its first two months

Research for the history film (brief: `film/NEXT-history-film.md`). Scope: the three early public
repositories, and `pgm-studio` from 2026-06-12 to mid-August 2026. Everything below was read from git
history and checked-in files on 2026-11-27. Anything not verified is marked **[uncertain]**.

Clones used (full history, all branches fetched):
`/home/user/rockymine/CTW-Layout-Generator` (5 commits), `/home/user/rockymine/MinecraftLayoutEditor`
(112 commits on `master`, plus 16 remote branches), `/home/user/rockymine/pgm-map-studio` (95 commits on
`master`, plus 4 remote branches), `/home/user/pgm-studio` (2,646 commits on the checked-out branch
`claude/magical-ritchie-3f4e33`; 258 in June, 513 in July, 514 in August 2026 up to the 16th).

**Two corrections to the brief, from the record:**

- The CTW repository is from **autumn 2025, not "the start of the year"**: first commit 2025-09-28, last
  2025-10-03. (It may still feel like "the start" to the author — that is a question for him.)
- **CTW-Layout-Generator does not download blocks.** Its only export is a JSON file ("Download JSON",
  `App.tsx:461–495`). The first *downloadable blocks* in the record are in **MinecraftLayoutEditor**, on
  2025-10-12 ("add schematic creation and download", a `.schematic` file). And that editor is already
  **C#** (Blazor WebAssembly, `net10.0`) — so the C# era begins in October 2025, *before* the Python
  stage of May–June 2026, and `pgm-studio` is a return to C#, not a first move to it.

Committer identities: the early repositories and `pgm-studio` carry two human identities, `michael`
(`michael.g186@live.de`) and `rockymine` (`rockymine.ocn@gmail.com`), interleaved on the same repositories
and the same days. **[uncertain]** whether they are the same person; the brief only names rockymine and
Ruediger.

---

## 1. Timeline

| date | repository | commit | what happened | why it mattered |
|---|---|---|---|---|
| 2025-09-28 | CTW-Layout-Generator | `2aed35c` | "Initial commit" — README of a Google AI Studio app ("Run and deploy your AI Studio app") | The first trace of the project; made in AI Studio, not by hand |
| 2025-10-01 | CTW-Layout-Generator | `6691417` | "initialize project": React/Vite app, 19 files, +3,195 lines; `lib/mapGenerator.ts` (806 lines) generates a seeded CTW layout | The first generator. Its node types are already `SPAWN`, `SPAWN_ENTRY`, `WOOL`, `WOOL_ENTRY`, `HUB`, `FRONT_LINE`, `FRONT_LINE_ENTRY`, `ISLAND`, `CENTER_HUB` (`types.ts`) — the vocabulary of the later model, nine months early |
| 2025-10-03 | CTW-Layout-Generator | `3eab815` | "fix: styling, feat: step-wise manual editor" | Drawing by hand in the browser, in steps (nodes → edges → routes & export) |
| 2025-10-03 | CTW-Layout-Generator | `ec9ca62` | "feat: add snapping to intra-team horizontal symmetry line" — last commit | The repository stops after six days |
| 2025-10-10 | MinecraftLayoutEditor | `d460b47` | "Projektdateien hinzufügen." — a C# solution: Blazor WebAssembly app + `Logic` (Graph, Node, Edge) | The self-built rewrite; the map is literally a `Graph` of typed nodes and edges |
| 2025-10-11 | MinecraftLayoutEditor | `4d132b2` | "symmetry, mirror, rotate, snap to canvas, etc." | Symmetry is the first feature after the canvas — it stays central in every later repo |
| 2025-10-12 | MinecraftLayoutEditor | `d961f6a` | "change node highlight, add schematic creation and download" (`SchematicWriter.cs`, SharpNBT) | **First downloadable blocks**: a drawn graph becomes a `.schematic` file |
| 2025-10-12 | MinecraftLayoutEditor | `9f978e3` | "render edges with bresenham" | An edge between two nodes becomes a line of blocks — graph → ground |
| 2025-10-16 | MinecraftLayoutEditor | `ad2baa0` | "improve rectangle creation, display minecraft blocks on canvas" | The canvas shows blocks, not just a diagram |
| 2025-11-04 | MinecraftLayoutEditor | `6021b3a` | "use skiasharp for rendering" (PR #1 merged 2025-11-05, `a32bf6e`) | Performance work on drawing — a recurring theme |
| 2025-11-06 | MinecraftLayoutEditor | `d2c4bc3` | "working import of .leveldat and .mca files (claude & grok)" (+621 lines `WorldImporter.cs`) | First reading of a real Minecraft world; **first named AI models in a commit message** (Claude and Grok) |
| 2025-11-10 | MinecraftLayoutEditor | `d23891b` | "Add XML import" | First reading of a PGM `map.xml` |
| 2025-11-16 | MinecraftLayoutEditor | `f683004` | "introduce edges property for graph" — last commit on `master` | The editor stops |
| 2025-12-20 | MinecraftLayoutEditor | `de5ee47` (branch `24-implement-region-creation-within-editor`) | "ui improvements (claude)" — last human commit in the repo | Region editing was the open work when it stopped |
| 2026-05-31 | pgm-map-studio | `915c61c` | "Initial project scaffold" (Python), co-authored by **Claude Sonnet 4.6** | The Python stage begins, ~5.5 months after the C# editor stopped |
| 2026-05-31 | pgm-map-studio | `ba9c9b3` | "Add layout package with island detection pipeline" — scans a world, detects islands as polygons | Reading existing maps, not generating them |
| 2026-06-03 | pgm-map-studio | `050b093` | "Add XML roundtrip export (MapXml → map.xml)" | The studio can write the contract it reads |
| 2026-06-04 | pgm-map-studio | `3a5dc89` | "Add studio package: Flask editor with Dashboard, Overview, and Teams activities" | The first "studio" — a browser editor around the analysis |
| 2026-06-05 | pgm-map-studio | `12d6395` | "Add ctw data model and authoring workflow description" (`docs/ctw-map-pamphlet.md`) | The clearest early statement of why the void matters (quote in §2) |
| 2026-06-07 | pgm-map-studio | `4f095eb` | "feat: write Minecraft 1.8 world files on sketch export" — "a complete, PGM-loadable map folder" | A sketch drawn in the browser becomes a loadable world |
| 2026-06-09 | pgm-map-studio | `ad35678` | "feat(objectives): implement wool objectives activity (M1)" | Authoring is CTW-only |
| 2026-06-12 03:24 | pgm-map-studio | `490aebe` (branch `refactor/contract-first`) | "feat(traversability): C15 — objective-chain connectivity (navigability map)" — last commit in the repo | The Python studio was being worked on until the night before the C# repo opened |
| 2026-06-12 17:21 | pgm-studio | `f499ea88` | "add README" (empty file), by `michael` | pgm-studio's first commit |
| 2026-06-13 | pgm-studio | `7b30744a` | "Initial import: ASP.NET Core + Blazor WASM port of pgm-map-studio" — 145 files, +18,093 lines, co-authored by **Claude Opus 4.8** | The move to C#: a full port in one day, with MariaDB and the stack still used today |
| 2026-06-15 | pgm-studio | `ea76f13a` | "Add declarative authoring intent + Teams-slice generator" | A map described as intent, compiled to `map.xml` |
| 2026-06-18 | pgm-studio | `156e77da` | "S2e: finish a sketch → world geometry → Configure (loop closed)" | Draw → world → configure works end to end in C# |
| 2026-06-20 | pgm-studio | `77b47472` | "Sketch generators: lane archetypes (H/Pinwheel/Trident/Organic) + auto-placement, headless" | First layout generator in the studio |
| 2026-06-20 | pgm-studio | `f25a9249` | "G4: Organic-generation demo page + corpus island-count analysis" (N=347): "the generator emits 0 neutral mid pieces but 88% of real maps carry a contested middle" | The corpus as the measure of what was missing — the middle |
| 2026-07-02 | pgm-studio | `8a53c2b6` | "P9e: sketch world-folder export" — a ZIP of `map.xml` + `level.dat` + `region/*.mca` | The C# studio writes a playable world |
| 2026-07-02 | pgm-studio | `c6b0fd89` | "Add base 2-island CTW test seed" — "two distorted-H team islands (rot_180) + a raised central square, 1 cell = 5 blocks" | The hand-made seeds the generator design was argued from (`tools/seeds/`) |
| 2026-07-02 14:31 | pgm-studio | `845ccb0a` | "Add layout-generation design: plan-then-realize architecture" — "Layer A — the plan (topology graph)"; first commit co-authored by **Claude Fable 5** | The map-as-graph idea written down as an architecture |
| 2026-07-02 14:54 | pgm-studio | `313ae96b` | "Rework layout-generation design: piece/interface plans, expert rules, no skeletons" | **23 minutes later the graph is dropped** for areal pieces joined by interfaces |
| 2026-07-02 | pgm-studio | `10137274`, `188d61ce` | "Add layout-rules strawman checklist for expert correction"; "Layout rules v2: fold in the author's first correction round" | The rules start as guesses the author corrects by id — the human oracle |
| 2026-07-03 | pgm-studio | `aabf3500` | "Spec junction-region derivation (hubs as derived overlays)" | The hub becomes a measured thing, not a drawn one |
| 2026-07-04 | pgm-studio | `ec7132d3` | "Design: player-traffic ground truth as the composer's evaluation instrument" — a month of recorded matches; ingwaz sample "105 matches, 510 players, 199 grid nodes" | Real play data enters; players standing in the void reveal the build regions |
| 2026-07-05 | pgm-studio | `bc35f250` | "Composer: middle-out design note" — "the mid is a thin fitted afterthought" | The middle again named as the weak part |
| 2026-07-10 | pgm-studio | `9d75d05c` | "docs: box-partition + interface-width grammar + wool-approach shape catalog" — "typed spawn/hub/frontline/mid boxes" | **The hub / wool approach / frontline / mid model appears as boxes** |
| 2026-07-14 | pgm-studio | `deb62961` | "docs: consolidate map generation into one canonical doc" (`docs/contracts/map-generation.md`), deleting seven drifted docs | One source of truth for the model |
| 2026-07-15 | pgm-studio | `5825954d` | "Destroyables and cores: the DTM/DTC contract" — "DTM is cheaper than the CTW wool we already ship" | DTM/DTC arrive a month after CTW; they "float above the terrain, which is author knowledge" |
| 2026-07-18 | pgm-studio | `5f07842e`, `3d8872a1` | "Compose: the hub box…"; "Compose: the frontline box…" | The model is built in code, box by box |
| 2026-07-21 | pgm-studio | `dec147ee`, `d1489f23` | "map completion v0 — The first full board off the partition-first path"; "the box pipeline is THE composer - retire the old grower path" | The box model becomes the only generator |
| 2026-07-25 | pgm-studio | `40433997` | "Boxes as an authored plan annotation (G126)" — first commit co-authored by **Claude Opus 5** | Model change visible in the trailers |
| 2026-07-27 | pgm-studio | `3686ad38` | "Docs: consolidate the generation cluster into docs/generator, checked against the code" — 11 files / 5,068 lines → 9 files / 3,299 lines; `docs/generator/model.md` is born | The canonical model document in its current home |
| 2026-08-09 | pgm-studio | `b34cf7eb` | "Record how a CTW match is actually played, and the flow reading beside it" (`docs/match-flow.md`, later `docs/gameplay/`) | How the geometry plays, written down; the void as permanent route structure |
| 2026-08-13 | pgm-studio | `a51207d1` | first commit co-authored by **Claude Sonnet 5** ("Grow the handbook…") | Sonnet joins; same day `pgm-studio-mapgen` starts per the brief |
| 2026-08-15 | pgm-studio | `0d8f68e7` | "The model states its own range, so no one invents a body to widen it" | The model's limit written in: the Thunder series cannot be expressed |

Model trailers in pgm-studio, 2026-06-12 to 2026-08-15 (counted from `Co-Authored-By`): June — Opus 4.8 ×255;
July — Opus 4.8 ×312, Fable 5 ×121, Opus 5 ×74 (+4 "1M context"); August to the 15th — Opus 5 ×216
(+137 "1M context"), Opus 4.8 ×67, Sonnet 5 ×29, "Sonnet" ×14, Fable 5 ×11, plain "Claude" ×21. In
pgm-map-studio: Sonnet 4.6 ×79 (all of `master`), Opus 4.8 ×64 (all on branch `refactor/contract-first`,
2026-06-10 to 06-12 — so Opus 4.8 was already in use on the Python code just before the port). In
MinecraftLayoutEditor, the 2025 commits carry no trailers — models appear only in messages ("claude &
grok", "(claude)"); the 19 commits on branch `claude/minecraft-layout-editor-perf-cspypa` (all
2026-07-30) are co-authored by Opus 5.

---

## 2. The origin beats, as the record tells them

### Before the studio: a browser drawing that becomes blocks

The very first test is an AI Studio app whose own description already names the void as the frame:
the generator makes layouts "within a void-based architecture". It places typed nodes on a 3×3 grid per
team, joins them with walkable or bridgeable edges, and mirrors or rotates the half. What it hands back
is JSON, not blocks. The step from drawing to downloadable blocks happens eleven days later in the
self-built C# editor, where an edge is rasterised with Bresenham and saved as a `.schematic`.

> "An automated system to generate balanced, tactically diverse battlefield layouts for Minecraft
> Capture the Wool. It creates randomized yet strategically sound maps with objectives, routes, and
> obstacles within a void-based architecture" — `CTW-Layout-Generator/metadata.json`

> "change node highlight, add schematic creation and download" — MinecraftLayoutEditor `d961f6a`, 2025-10-12

### Why capture-the-wool came first, and the void that steers

The record never states, in one sentence, *why* CTW before DTM/DTC — that is an interview question. What
it does show: every early repository is CTW-only (pgm-map-studio's README: "A tool for creating and
editing PGM Capture the Wool maps"), the first DTM/DTC work in pgm-studio is a month later (2026-07-15),
and that contract calls DTM *simpler* than wool, which suggests CTW was chosen for its structure rather
than its ease. The clearest statement of the void as what shapes play is the Python-era pamphlet, and
the August match-flow commit says the same from recorded matches.

> "This distinction shapes the entire play experience. … The ground plane is not just terrain — it is
> the map's navigational grammar." — pgm-map-studio `docs/ctw-map-pamphlet.md` (`12d6395`, 2026-06-05)

> "a void anywhere else is uncrossable at every height. The routing options a void creates therefore
> last the whole match rather than being flattened by the bridge layer." — pgm-studio `b34cf7eb`, 2026-08-09

### Reading a map as a graph

The graph is the oldest idea in the record. CTW-Layout-Generator's map *is* nodes and edges
(`types.ts`: `Node`, `Edge`, `EdgeType = 'walkable' | 'bridgeable'`); MinecraftLayoutEditor's core type is
`Graph.cs` with `Node.NodeType { Wool, WoolEntry, Spawn, SpawnEntry, Frontline, Hub, Corridor }`. The
Python stage inherited a predecessor, `CTWAnalysisWithClaudeCode`, with "Skeleton Graphs — medial-axis
thinning … to extract a navigation skeleton" (`pgm-map-studio/plans/00_assessment.md`). In pgm-studio the
graph became an architecture on 2026-07-02 at 14:31 — and was abandoned 23 minutes later, because a thin
skeleton cannot represent how a build region touches the long side of land.

> "Layer A — the plan (topology graph) … Edges, typed: `lane` (land — a walkable corridor) or `gap`
> (void — crossable only through a build region)." — `docs/contracts/layout-generation.md` at `845ccb0a`

> "a thinned skeleton cannot represent side contact (a build region touching a wide rectangle's long
> edge maps to no node or labelable edge) and biases generation toward thin maps" — `313ae96b`, 2026-07-02

### The switch to C#

The port is one commit, one day after the last Python commit, and its CLAUDE.md frames the Python
studio as the reference to match. The record gives no reason for choosing C# (the brief's "a language
the author can read" is not written anywhere I found — **[uncertain / interview]**). The stack line
"decided, do not relitigate" is there from the first day.

> "A from-scratch **ASP.NET Core** rewrite of the Python `pgm-map-studio` … which stays in place as the
> **behavioural reference** … Goal: full feature parity in C# with all map data in **MariaDB**." —
> `CLAUDE.md` at `7b30744a`, 2026-06-13

### The model: hub, wool approaches, frontline, middle — and what it limits

The words come from the 2025 generator; the *boxes* come from July 2026. Between 2026-07-02 and
2026-07-21 the plan went from a graph to areal pieces, to rules the author corrected by id, to a box
partition of five kinds (`spawn`, `hub`, `wools`, `frontline`, `mid`), and finally to the only composer.
Twice the corpus said the same thing: the generated middle was missing or thin (0 mid pieces vs 88% of
real maps on 2026-06-20; "a thin fitted afterthought" on 2026-07-05). The limit was written into
`model.md` on 2026-08-15: organic maps like the Thunder series cannot be expressed, by the author's choice.

> "Boxes are a model of how an author works, not a property of maps." — `docs/generator/model.md`
> (since `2ad19e08`, 2026-07-29)

> "It is an **intentional abstraction whose product is a low-fidelity prototype of a layout** … A map
> whose form is organic rather than rectilinear falls outside it: the Thunder series is the worked case …
> **That is a limitation rather than a defect, it is the author's stated position, and it stays.**" —
> `docs/generator/model.md` (since `0d8f68e7`, 2026-08-15)

### The human oracle enters (useful for the rules beat later)

The rules began as a strawman the model extracted from three hand-made seeds, each rule tagged
`[seed]`/`[guess]`/`[?]` "for the author to correct", and the author corrected them the same afternoon.

> "Rules are numbered for correction by id ("WL3: no, 15")." — `docs/contracts/layout-rules.md` at `10137274`

---

## 3. What we could show

**No screenshots, GIFs or worlds are checked into any of the four repositories** (the only images are
icons: `MinecraftLayoutEditor.WebApp/wwwroot/icon-192.png`, `pgm-studio/src/PgmStudio.Client/wwwroot/favicon.*`).
Every picture has to be made by running something. `/media/sf_repos` (corpus, scanned output) is not on
this machine.

**Era 1 — the AI Studio generator (Sep–Oct 2025).**
- Run it: `cd /home/user/rockymine/CTW-Layout-Generator && npm install && npm run dev` (Vite). The Gemini key
  is only injected in `vite.config.ts`; no source file calls Gemini, so it should run without one
  **[uncertain until tried]**. Two modes: generated layout with sliders (`components/Controls.tsx`) and
  the step-wise manual editor (`components/ManualControls.tsx`), "Download JSON".
- On-screen documentation inside the app: `components/Documentation.tsx` ("Layout Generation Process" —
  node types, "Tactical Gaps", islands). Filmable as text.
- The live AI Studio link in `README.md` (`ai.studio/apps/drive/1hrv…`) **[uncertain whether it still opens]**.

**Era 2 — MinecraftLayoutEditor (Oct–Dec 2025).**
- Run it: `dotnet run --project /home/user/rockymine/MinecraftLayoutEditor/MinecraftLayoutEditor.WebApp`
  (ports 5110/7259 in `Properties/launchSettings.json`). It targets `net10.0` with `10.0.0-rc.1` WASM
  packages — **[uncertain]** whether those restore on the installed SDK.
- Filmable moments: place nodes, mirror/rotate, edges drawn as block lines (Bresenham), "download
  schematic" (`Pages/Home.razor.cs:169`), import a `.mca` world and an XML.
- The later Claude branch `origin/claude/minecraft-layout-editor-perf-cspypa` (2026-07-30) revisits the
  old editor's rendering — a small "coming back" moment.

**Era 3 — pgm-map-studio, Python (31 May–12 Jun 2026).**
- Run it: `pip install -e /home/user/rockymine/pgm-map-studio && pgm-map-studio serve` (Flask, port 7892
  per `3a5dc89`). Import needs a world; the concept-first sketch → export path should work without one
  **[uncertain]**. Its `/design` page is the design-system showcase.
- Documents worth a slow pan: `docs/ctw-map-pamphlet.md` (the void as grammar), `plans/00_assessment.md`
  (the inventory of the older `CTWAnalysisWithClaudeCode`), `docs/sketch-workflow.md`.

**Era 4 — pgm-studio's first two months (Jun–mid Aug 2026).**
- The three hand-made seeds: `/home/user/pgm-studio/tools/seeds/base-2island.*`, `base-2wool.*`,
  `base-4team.*` (layout, plan, intent JSON) — loadable into a running studio and exportable as worlds.
- The graph-then-not-graph day, as documents: `git show 845ccb0a:docs/contracts/layout-generation.md` vs
  `git show 313ae96b:docs/contracts/layout-generation.md` — the same file 23 minutes apart.
- The rules strawman and its correction: `git show 10137274:docs/contracts/layout-rules.md` vs `188d61ce`.
- `docs/generator/model.md` — 20 fenced blocks, including ASCII figures checked by
  `dotnet run tools/deriver/figure-check.cs`; the pipeline line in §1 is a ready title card.
- The Organic demo page `/concepts/organic` (noise → anchors → spines → ribbons → mirror, one panel per
  stage) existed at `f25a9249`; it is gone from HEAD, so showing it means checking out that commit and
  building (needs .NET 10 + MariaDB) **[effortful]**. Today's equivalent is the running studio's
  Generator tool, `GET /shapes/catalog` and the compose page.
- Commit-rate and model-trailer counts (§1) as a chart: 258 / 513 / 514 commits per month.

---

## 4. Open questions for the author

1. The brief says the CTW generator was "the start of the year"; git says late September 2025. Was there
   an earlier attempt, or is autumn 2025 the real start?
2. What did you ask AI Studio for, and how much of `mapGenerator.ts` did you change? Did the node types
   (hub, wool entry, front line) come from you or from Gemini?
3. Why did CTW-Layout-Generator stop after six days, and why rebuild it yourself in C# rather than keep the
   TypeScript one?
4. Where did "something drawn in the browser could become downloadable blocks" actually click — the JSON
   export in AI Studio, or the schematic in your own editor?
5. Who is "michael" in the commit history — you, or a collaborator?
6. "claude & grok" (2025-11-06): what did each do on the world importer, and how did you use AI then?
7. The C# editor stops in November 2025 and the Python studio starts on 31 May 2026. What happened in
   those five and a half months? What was `CTWAnalysisWithClaudeCode`, and is it public?
8. Why Python for the second attempt, and why back to C# twelve days later? Is "a language I can read"
   the reason, and what does it mean in practice when the AI writes most of the code?
9. Why CTW before DTM/DTC, in your words? The record says DTM is the simpler objective — was structure the
   reason, the void, or simply what you play?
10. On 2026-07-02 the map-as-graph was written up and dropped within 23 minutes. Was that your call
    in review, or the model's? Do you still think in graphs when you look at a map?
11. The rules were "corrected by id" the same afternoon. How did it feel to be the oracle — and which
    numbers were you least sure of?
12. The recorded matches (a month of play, 105 matches on ingwaz): who recorded them, on which server, and
    how did they change what you believed about flow?
13. The model cannot draw the Thunder series. When did you decide that was acceptable, and which maps you
    love fall outside it?
14. You switched models often in these two months (Opus 4.8 → Fable 5 → Opus 5, Sonnet from August).
    Did you notice the switches in the work, and what made you pick one?
