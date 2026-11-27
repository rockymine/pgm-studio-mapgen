# Research 08: the author's third instalment, checked against the record

Scope: the "Third instalment" in `author-account-2026-11-27.md`, six items. Sources are the local clones of
`pgm-studio` (studio), `pgm-studio-mapgen` (this repository), `rockymine/*` and the two corpora
(`CommunityMaps`, `PublicMaps`), read at their state of 27 November 2026. Every time is UTC; hashes are
abbreviated. Where the record is silent the text says "not in the record". Where the record differs from the
author's memory the difference is marked **differs**. Nothing here was run against a live studio; world readings
were taken with the block reader `eye` (scratchpad tool) and `tools/anvil.py`.

## 1. The late map whose wool room moves, and Hello World

**Not found.** No map in either corpus, at any commit, that rockymine wrote and that moves a wool room. What was
checked:

- Every `map.xml` revision touched since 1 January 2026 on any ref of both repositories was tested for the
  rockymine UUID (`fe3608b7-d105-4029-8800-34b3147065b6`). The maps that carry it as author or contributor in 2026
  are: Segment (1.1.0/1.1.1, 9 and 11 January), Capture the Wool CTW (24 June, author MishM0sh, rockymine
  contributor), Vauxite (24 June, 1 July), Drastic Change II (24 June), Bridgid II (14 July, rockymine and
  Ruediger_LP), Hello World Micro (27 July), Kuusepuu CTC (27 July), No Blocks Placed (7 August), Millrace
  (2 September), 803 (19 October, author minuyo, rockymine "clicking some buttons (XML)"), plus Pillars, Fortress
  Conflict, The Tower of Orthanc (rockymine "Trees and aesthetics"), Strange Dreams I ("Borrowed trees from"),
  Countryside (contributor), Brittlebush (Sam, 4 November, "fix wr filters") and in PublicMaps Rooted
  (`87bf6b84`, 3 April, "Load Rooted by rockymine", staging).
- The ones with wool objectives were read for `<structure>`, `<dynamic>`, `<portal>`, `<move>`, timed or
  variable-driven `<fill>` and actions. Vauxite, Bridgid II, Segment, 803, Rooted, Capture the Wool CTW and
  Drastic Change II contain none: they are ordinary CTW XML. Only Hello World, Hello World Micro, Kuusepuu CTC (the cake map)
  and (a 2024 map, `ctw/outlyne`, Obelistics and rockymine) use `<action>`/`<fill>`.
- A search over all CTW/mixed maps at HEAD for `<fill material="air">` or `<structure>` returned thirteen
  CommunityMaps and five PublicMaps files; none is a rockymine map except Outlyne, whose only fill is
  `<fill material="air" region="floor" filter="stained-glass-filter"/>` on `match-started`, i.e. it clears a
  glass floor that showed the build area. That is not a room moving.
- A scan of every historical `map.xml` revision with the UUID that also contains actions or structures was
  started and stopped unfinished; the 2026 pass above is complete and the older revisions are not in scope.

Conclusion: the moving-wool-room map is **not in the record**. Candidates the author names for it, "probably in
CommunityMaps or PublicMaps", are not there under his authorship. It may be in the private maps repository,
which cannot be read, or unreleased.

### Hello World (the full map): the colour change is here, in 2025

- `CommunityMaps/ctw/hello_world`: authors rockymine and Ruediger_LP (no contributions stated), `<created>`
  2025-01-17, version 1.0.1. Added by RuedigerLP at 2025-02-01 22:56 (`3be98917`, "Add: Hello World"), 1.0.1 on
  2025-02-05 20:11 (`787ca77b`). Still in CommunityMaps.
- Its `<actions>` block recolours wool rooms in the match: `change-orange-to-red-action` fills the pinks' wool
  rooms (`<fill material="stained clay:14" region="pinks-woolrooms" filter="orange-stained-clay-filter"/>`, and
  likewise glass, wool and carpet) triggered by `orange-wool-completed-filter`; a second action turns magenta to
  purple for the yellows' rooms. So the colour change the author remembers on the *Micro* is first the *full*
  Hello World's, **a year and a half earlier** (February 2025). **Differs**: the author said the Micro's room
  changes colour; both do.

### Hello World Micro: authors, dates, what changes

- Folder `ctw/hello_world_micro`, author rockymine alone (no Ruediger credit), committed only by RuedigerLP:
  `591d21b1` 2026-07-27 23:10 "Hello World Mini: added" with the body "grey map for concept test" (the map itself
  is already named Micro inside); `fb0013e1` 23:30 "Hello World Micro", body "add actual map, still rly grey
  though" (adds `map.png`, 98 changed XML lines, the colour `<action>`s); `04e61f88` 23:48 "Hello World Micro:
  update 1.0.1"; `b4ef98e9` 23:58 deletes `hello-world-mini.plan.json`; `067c82cc` 2026-08-12 21:15 deletes the
  whole folder.
- Mechanism in 1.0.1: each team's two wools "share one spot" (`location="-45,25,-35"` for the red room,
  `-45,25,35` for the blue room, two `<wool>` entries each). A variable `wool_count` is rolled at match start
  (`<set var="wool_count" value="floor(random() * 2) + 1"/>`) so a win needs one wool or two. When the lead-in
  wool falls in a two-wool game the box is refilled: `<fill region="blue-box" material="orange wool"
  filter="any-wool"/>` (and the glass panes), and an alert says the wool room "switched to Orange". The fills are
  masked to wool and glass-pane blocks (`any-wool`, `any-pane`), so nothing is removed from under a player.
- **Differs**: nothing in any committed version moves a room or takes a block from under anyone, and no commit
  message reports a test. The "players fell out of the world as the room moved" is the author's account alone.
  The record does say the layout came from the studio's plan tool (the deleted `*.plan.json`); the author's
  third instalment says he made it by hand as a small Hello World, which the record cannot settle.

## 2. The spline tree in pgm-studio

**What it was.** Not an editor in which a person drags splines: a generator with a handful of knobs, previewed
in the studio's Dressing inspector, whose branches were centripetal Catmull-Rom splines swept into blocks. The
author's phrase "number of main trunks, how branched" matches the knobs `stems` and `levels`.

Chronology (studio repository; times UTC):

| When | Commit | What |
|---|---|---|
| 2026-08-01 23:46 | `a3160327` | Decoration stage designed; `tools/decorate/prototype.html` carries "recursive tree growth" |
| 2026-08-02 00:13 | `de4e2ba1` | "Rebuild the grown tree as Catmull-Rom limb splines, not a fractal": "The recursive brancher read as a fractal, not a tree." Limbs are splines swept with a tapering disc; knobs limb count, spread, curve, leaf size |
| 2026-08-02 00:20 | `4ab823b1` | one slim trunk to a fork (base radius about 1.6) |
| 2026-08-02 00:35 | `20c87902` | recursive skeleton with Catmull-Rom spines and a "stems" knob: "one that forks, a double, a triple base"; a spine debug view beside the voxels |
| 2026-08-02 00:51 | `c443ce90` | crown rebuilt as per-tip leaf discs ("not a blob") |
| 2026-08-02 01:06 | `7a36f9a9` | a **central leader**: "The trunk died at the branch point — a single fork, as if sawn."; knob `leader` |
| 2026-08-02 01:14 | `771ca1f8` | `height` parameter scaling trunk thickness and branch count |
| 2026-08-04 01:41 | `ac2f1618` | the dressing pass wired into the Sketch tool; the preview "draws a recipe by growing it" |
| 2026-08-05 08:00 | `41b40336` | the vanilla tree (trunk under a canopy profile) split off: "That offers six silhouettes and builds one" |
| 2026-08-06 18:04 | `7b661c89` | all-bark tree logs |
| 2026-08-12 00:08 | `c9ea46d6` | 75 hand-built trees measured; "the grown crown hangs off nothing": 1516 of 4020 crown clusters (37.7%) never touch their branch; below height 12 42 to 76% of the crown floats free |
| 2026-08-12 01:26, 02:17 | `ec91a078`, `674df496` | regrown to the corpus; a `whorled` conifer form first appears in code here; wood at height 40 cut 456 to 322 against an author's 53 |
| 2026-08-13 01:13 | `e24d2a49` | B78: a taller grown tree was silently dropped because its wide crown clipped protected ground (1545 leaves at height 8, 108 at 12, 0 at 20) |
| 2026-09-10 22:20 | `6b0b3f09` | "Remove the grown tree: a recipe is a species or a body" (WE65): "`TreeForm.Grown` built its trees from a recursive skeleton and they came out broken; the author's ruling is that the form goes rather than gets a knob." 496 lines of `Geom` out |

**Parameters at the end** (from the removed `TreeStyleSaveRequest`): `Height` 5 to 40, `Stems` 1 to 3, `Leader`
0 to 1 ("low spreads, high spires"), `Flow` 0 to 1 (how much the trunk wanders), `BranchAngle` 0.2 to 1.5 rad,
`Levels` ("2 is a tree, 3 a denser one"), `Whorled` (conifer rings), `LeafSize` 0.2 to 1.

**How it degraded.** The record shows two things, not a steady decline. The grower was measured as broken on 12
August and then repaired the same night (stranded leaves 36% to 0%, wood in one piece 81% to 100%, leaves touching
wood 14.8% to 54% against 30.3% by hand). On 13 August a second fault surfaced: height itself made trees vanish
(B78). Even after the repair the document found the crown "a solid mass held on at a few points rather than lace",
more wood for its foliage than an author's, and a conifer whose widest tenth sat mid-height where a hand-built
conifer's sits in the bottom third. "Central trunk got worse" has no commit behind it; the leader was added on the
first night. What replaced it: the vanilla template tree (5 August, still present), the copied tree cut out of a
world (2 September, `378b2d58`) and the author's 95-tree corpus. M0035 dropped the eight knob columns and deleted
the saved recipes that named the form.

**Millrace's first pines.** `specs/opus5-millrace/build.py` (30 August, `bb7c8a7f`) places grown trees only: an
`oak()` helper (`leader=0.5, flow=0.5, branchAngle=1.15, leafSize=0.68, whorled=False`) and a `fir()` helper,
spruce wood, `whorled=True, leader=0.78, flow=0.2, branchAngle=0.8, leafSize=0.58`, on 6 + 4 sites. That is the
author's "meant as pines". The review of that board says "every tree on this board is `form: "template"`", which
contradicts the spec in the same folder, so one of the two is wrong; the spec is what ran. In the stored world
(`maps/dtcm/millrace`) the fir at (-100, -7) stands with logs at x -101..-99, y 37..40 and its leaves in
separate clumps of 36 to 51 blocks at y 45..51 (x -104..-97, z -16..-1). "Leaves only at the sides, every tier
cut off but the lowest" is the author's description of what he saw in game; the world is consistent with sparse,
detached crowns and does not need to be read further here. The hand finish replaced "the generator trees by 9
oak and 9 pine trees of my own collection" (`review/rockymine-ruediger-millrace.md`).

### No Blocks Placed: the larger tree

World read from the repository copy (`CommunityMaps/ctw/no_blocks_placed`, region files unchanged since the first
commit `11a15f7d`, 2026-08-07 18:58, RuedigerLP; `f17a371a` TTtie 15 August adds the creation date; `ff115048`
RuedigerLP 15 August 1.0.2). Ground there is stained clay at y 13. `eye <world> find 17,162` lists these log clusters:

| Logs | Where (x, y, z) | Reading |
|---|---|---|
| 28 + 22 = 50, oak all-bark (17:12) | x -24..-20, y 14..27, z 43..47 and x -23..-20, y 16..25, z 48..50 | **the larger tree**; leaves (18:4) 270 blocks at x -27..-17, y 24..30, z 41..52 |
| 28 + 22 = 50 | x 19..23, y 14..27, z -48..-44 and x 19..22, y 16..25, z -51..-49 | its rot_180 image |
| 14 + 14 per trunk, dark oak (162) | x -1..0, y 11..17, z 22..24 and z -24..-23 | 2 x 2 trunk, 28 logs, 156 blocks |
| 11, 8, 7 | single stems, e.g. x -41, y 18..25, z 99; x -41, y 16..22, z 70 | straight trunks, 7 to 11 logs |

The big tree is the largest by a margin (50 logs against 28 and then 11) and differs in kind: a 2 x 2 base at y 14
(x -23..-22, z 46..47) narrowing to a stem one block wide at y 18, then limbs spreading to z 46..50 at y 22, which is a
tapered swept limb, not a straight trunk under a profile. That is the shape the 2 August grower made. The map's
spawns are at z +-125, the middle at z 0, the blue wool room at x -25..-10, z 65..80; the tree stands at z 41..52,
about 13 blocks short of the wool room edge and 40 to 50 from the centre. **Which tree the author means is still
his to confirm**: the reading is of the blocks, not a statement in the record. The "no other generated tree" claim
was not tested beyond this: the remaining bodies (28 in total, 14 pairs, research `05`) are all smaller.

## 3. The graph idea and the organic layout, June to July 2026

**What was added at 14:31 and dropped at 14:54 on 2 July.** A **design document**, nothing else.
`845ccb0a` (14:31:41, Fable 5, +184 lines `docs/contracts/layout-generation.md`) proposed four layers: "Layer A: the
plan (topology graph)" with typed `lane`/`gap` edges, then a skeleton realizer plus a "roughen" pass, an elevation
grammar and intent wiring. `313ae96b` (14:54:47, 150 added, 182 deleted) replaced it. Its message states why: "a
thinned skeleton cannot represent side contact", it "biases generation toward thin maps", and the corpus
extraction "loses the structure that matters". What was dropped is the **skeleton graph as the plan layer** and the
corpus-mining flywheel; the *roughen* pass was kept "unchanged as the separate final step". What replaced it: areal
pieces (rectangles on a coarse grid with a role and plateau) joined by **edge-interval interfaces**, which is
itself a graph of pieces. No code of the 14:31 design was ever committed; "23 minutes" is exact and describes the
document, so the author's doubt is justified in this sense: the graph *idea* did not die that afternoon.

What existed before:

- 2025: the author's graph editors (research `01`). `MinecraftLayoutEditor` draws edges between nodes; from
  2025-10-14 "thick lines", 2025-11-02 `97e5d01` "lane width configuration" (`Map.LaneWidth`), 2025-11-05
  "map thickness", the edge footprint a rotated rectangle from its two nodes (`Rectangle.FindRectCorners`).
  `Edge` itself has only a type (Walkable, Bridgeable), so the author's "edges with a width and height" is a map-wide
  lane width and thickness, not per-edge. `CTW-Layout-Generator` has a background-image upload, which matches
  "could trace an existing map".
- 20 June 2026: `13087536` 04:00 "Lane-graph island analysis"; `d40a9ab6` 04:48 the **Organic lane generator**
  (on a side branch): hub to wool-tip branches, waypoints bent by noise, smoothed with Catmull-Rom (`829525b6`,
  "centripetal Catmull-Rom"), variable-width ribbons, diamond holes, "the lane-graph reading of real maps turned
  into a generator". It reached `main` at 16:13 in `77b47472` with H, Pinwheel and Trident archetypes. `07f70ff7`
  17:38 added Bezier rounding. A demo page followed (`f25a9249`, 19:23).

What existed after: **`FannedGraph`** (the whole symmetric board as a reachability graph) was added at 22:47 the
same day (`e09959cb`, the plan compiler) and is still in `src/PgmStudio.Pgm/Plan/`; `ContactGraph` entered with the
deriver (`04f627ad`, 14 July) and `PlanFlow` (flow graph, filed as G127) later. So graphs came back as something
**derived from** the plan, never as something authored.

**The organic, spline-based layout attempt lived 25 days:** first commit 2026-06-20 04:48 UTC (`d40a9ab6`), its
design doc deleted 2026-07-14 01:09 (`deb62961`, the documentation consolidation), code removed 2026-07-15 01:10
(`172b6bbc`, "G5: retire the sketch-tool generation-method entry points ... in favour of the plan-then-realize
direction"): `OrganicLane`, `LaneSketchGenerator`, `AutoBridge`, the `POST /api/sketch/generate` endpoints, the
`/concepts/organic` page and the "Generated layout" tab. The author's "not fruitful and the format unappealing"
fits; the record gives no verdict of its own beyond "moot". The roughen operators (jitter, chamfer, subdivision) of
the 14:31 design do not survive as code under that name; whether the composer's later "attachment grammar" is their
heir is not established.

## 4. The "annealing" maps, Race for Victory 2, Two Tier, Outback

All five Annealing maps are in `CommunityMaps`, authors from `map.xml`:

| Map | Mode | `<created>` | Authors |
|---|---|---|---|
| Annealing | DTM, `dtcm/annealing` | 2021-01-20 | rockymine, Ruediger_LP |
| Annealing II | CTW | 2022-01-30 | DerStiv, rockymine, Ruediger_LP (XML) |
| Annealing III | DTC, `dtcm/annealing_iii` | 2022-07-09 | rockymine, Ruediger_LP; DerStiv contributor |
| Annealing IV | CTW | 2023-01-02 | rockymine, Ruediger_LP, DerStiv "master painter"; Mewzzy "squirrel expert" |
| Annealing II Short | CTW | 2023-02-09 | DerStiv; Ruediger_LP (XML) |

**Differs**: the author dates them to 2022; the series spans January 2021 to February 2023, with two of the five
in 2022. The travelling-salesman origin and the thesis are not in the record (no XML text, no commit message
mentions it). Annealing, II and III arrived in the repository by moves (2023-10-18 DTM/DTC, 2024-09-29 CTW); II Short
(2024-10-14) and IV (2024-11-10) were added fresh by RuedigerLP.

- **Outback** is the author's own: `PublicMaps/ctw/outback`, version 3.0.11, author rockymine alone (Pugzy and
  Strangey "Critics"), entered PublicMaps on 2026-03-21 in `46c29857` "Move rockymine's maps to PublicMaps"
  (BT). Related: `Outback Mini` (created 2022-01-25) and `Outback: Outback Edition` (2025-02-04, with Just_ and
  byRobo) in CommunityMaps. The studio's match-flow account calls it "one polygon and an H on the ground: two wide
  bands joined by a bridge fourteen blocks across at the dead centre" (`docs/gameplay/match-flow.md`, line 584).
- **Race for Victory 2** (`PublicMaps/ctw/race_for_victory_2`, 1.3.6): Plastix, IM_A_H0B0, MonsieurApple, Anxuiz;
  no `<created>`; entered the repository 2024-02-03 (`8c987ed7`, a bulk move).
- **Two Tier** (`PublicMaps/ctw/two_tier`, 1.3.2): nixter1029, _IQ, Tywnis; `<created>` 2013-10-31 and 2014-11-30
  (two tags); same move.
- Race for Victory 2 and Two Tier are old community maps, not his. That they are "H-shaped" is the author's
  reading; only Outback's H is stated in the studio's own text, and the other two were not measured here.

## 5. New Life CTW and Old Life CTW (trivia)

Both are in `CommunityMaps/ctw`. **New Life CTW** (1.0.7, `<created>` 2021-07-10) has four teams (blue, red,
yellow, green) and eight wools; its objective reads "Capture both wools, located at the right and left hand side
and place them at the victory monument under the helicopter located at the team's base diagonally opposite from
yours." **Old Life CTW** (1.0.5, `<created>` 2021-08-08) is the same ground with 24 `<wool>` entries and the
objective "Capture all 6 wools!". Both credit rockymine, Ruediger_LP and Just_ as "Executive producer", Strangey
for feedback, Brottweiler as "Map narrator", and Old Life Artdamension as "Head armor stand engineer". The
repository holds only the move (2024-09-29, `9eca3ef6`) and proto migrations (27 and 28 December 2024, Pear). The
contest, the school-children winner, the last place and "the XML was changed to a standard map" are **not in the
record**; the eight-wool, certain-wools-for-each-team design is what the XML shows. Dates match his "2020-21".

## 6. Block-choice faults in the first fifteen tested boards

The fourteen of the fifteen on disk (`BOARDS-BUILT.md`; `thornwake` lives in CommunityMaps) were counted with
`eye` and `tools/anvil.py`: slime block 165, quartz (155, 156, 43/44 data 7), end stone 121. No review or
commit message mentions slime, quartz or end stone for these boards (searched `review/`, `reports/`, studio
history, the MG list); the census is the whole evidence.

| World | Slime | End stone | Quartz | Remark |
|---|---|---|---|---|
| `ctw/viridian` (`hk1_viridian`, Haiku 4.5) | **13,299** of 66,071 non-air blocks (20.1%; 28% of the non-bedrock) | 0 | 0 | the slime is the bright riser along every wall and slope, y 1..11 (viewed in `eye` overview `viri-c0`) |
| `dtcm/verdigris` | 804 | 0 | 0 | |
| `ctw/saltmarch` | 0 | 4,629 (with sandstone 7,249 and sand 4,181) | 0 | an end-stone desert |
| `dtcm/goldhollow` | 0 | 814 | 0 | |
| the other ten | 0 | 0 | 0 | |

- **The slime map is Viridian** (Haiku 4.5, 12 August, spec author `haiku`, committed upstream by RuedigerLP at
  21:20 that day with Thornwake, `37bdef57`; objective "A lush jungle oasis"). The upstream world is identical
  (same 66,071 blocks, 13,299 slime). **Differs** from "mostly slime": a fifth of all blocks, none among the
  commonest surface blocks (the top layer is lime and green clay, prismarine and green wool), but the visible side of every raised
  part.
- **"Every green at once" also fits Viridian**: seven green-family blocks above 200 each (the most of any of the
  288 worlds in `maps/`): lime clay (6,492), green clay (4,608), green wool (3,400), lime wool (648), slime,
  prismarine 168:2 (3,760) and emerald block (1,067). The author names the slime map and the all-greens map
  separately; the record has one board with both.
- **Quartz with end stone as a desert**: not found among the fifteen; Saltmarch has the end stone and the desert
  palette but no quartz. Across all 288 worlds the only boards carrying both in hundreds are `ctw/blastworks`
  (858 quartz, 1,200 end stone) and later pgmvox boards (`frostvault`, `coldstore`, `slipway`, `sandcaster`), so
  that board is probably not in `maps/` or is from the unsaved part of the tests.

## What changes in the history

1. The 23-minute "graph dropped" is a design document rewritten, not a built architecture removed; the graph idea
   persisted as `FannedGraph` (same day, still in the tree) and the spline-based Organic generator ran 25 days.
2. Both Hello World maps recolour wool rooms; the Micro's is not new, and no room moves in any record.
3. The larger No Blocks Placed tree is located (table above); the generated tree is the 50-log oak.
4. Viridian is the slime (and all-greens) board; the quartz board is not identified.
5. Outback is his; Race for Victory 2 and Two Tier are others'; the annealing series runs 2021 to 2023.
