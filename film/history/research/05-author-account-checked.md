# 05 — The author's account, checked against the record

Research for the history. Subject: what rockymine said on 27 November 2026 (`../author-account-2026-11-27.md`),
item by item, set against what the repositories and the published maps hold. Read on 2026-11-27 from five
places: `pgm-studio-mapgen` (branch `mappies-film`, all refs), `pgm-studio` (all refs), the three early
repositories under `/home/user/rockymine/`, a fresh blob-less clone of `OvercastCommunity/CommunityMaps` and
`OvercastCommunity/PublicMaps` (both at their heads of 27 November; CommunityMaps at `5a191d44`), and the deployed
studio's public map list (`GET https://pgmstudio.de/api/maps`, read only, 72 maps).

**How the claims are marked.** *Account* is what the author said, as summarised in the account file; it is his
recollection. *Record* is what a commit, a file or a published map states, with the hash or path beside it.
*Inferred* is a reading of the record made for this document, with the method given. Where the record is silent,
the section says so in those words. Hashes are short and belong to `pgm-studio-mapgen` unless marked **(studio)**
or **(CommunityMaps)**. Dates are author dates.

---

## The five findings that matter most

1. **No Blocks Placed is real, published and older than the record had it, and its third author is not Tttie.**
   It entered CommunityMaps on 7 August 2026, credited as drawn in the studio's browser editor, five days
   before any `tools/mapgen` board went there. Its `map.xml` credits rockymine ("Drawing pieces, shapes, and markers in the browser."),
   Ruediger_LP ("Wisdom.") and Flamiix ("Minimalist."). TTtie's name is on the map's history, as the committer who
   added its creation date on 15 August, and not in its author list. (§b)
2. **Tttie is in the record after all, though not in either studio repository.** TTtie has committed to
   CommunityMaps since at least December 2023 (Watch Your Head, Notre-Daaaaam of Paris), and holds an account
   on pgmstudio.de with one sketch of their own (`untitled-sketch-7`, last changed 28 October). "Slop Sundays"
   appear nowhere. (§f)
3. **The 500-wide map is more probably Hollow Crown than Spinebreak, on every count except size.** Hollow
   Crown has exactly one monument and one core per team, its ground is flat (93% of its columns stand at y 10),
   and each team's core shares its cuboid with the enemy's monument, so enemy objectives stand 0 to 2 blocks apart.
   Spinebreak has four objectives a team, rolling ground from y 9 to 18, and 144 blocks between the nearest enemy
   objectives. Neither is 500 blocks across: Hollow Crown is 100 × 120, Spinebreak 145 × 405. (§h)
4. **The trees came before Fable's rebuild, not after it.** The tree-showcase world was measured in the studio
   on 12 August (75 trees). The commit "Add rockymine's custom trees" landed in this repository at 00:53 UTC on
   2 September, an hour before the hand-finished Millrace and two and a half hours before Fable 5.1's diff of it.
   What Fable did that night was turn those trees into a studio form, the copied tree. The world then grew to 86
   trees on 20 September and 95 on 1 October, which matches "under 100". (§c, §d)
5. **The colouring grammar did arrive with the Python rework, on 9 October, and it was built from his own maps.**
   An Opus 5.5 session read Brittlebush I (2022) and Brittlebush II (2023) block by block, wrote their look as a
   style, then split the rules from the blocks (`pgmvox.grammar`, 779cff79) and spoke a second style, Claywork,
   in the same rules forty minutes later. Brittlebush III's layout was drawn by the author on pgmstudio.de as
   `untitled-plan-8` ("Brittebush III"); the version in this repository is pgmvox's build of that plan. His own
   in-game-coloured Brittlebush III is in no repository and no corpus. (§a, §b)

---

## a. The colouring grammar ("map walls")

**Account.** "Map walls" is how a large shape is coloured. A first prototype set one rule per Y level for a whole
surface, with y 0 as bedrock. Then came the insight that a large block has a top, sides and edges that can be
computed, then surfaces shaded from outside in and patterns stacked. Slope colouring was an important step. Under
the plan model one area had one pattern and another area another, and transitions never worked. A real grammar,
a look defined once for a whole map and transferable, came with the Python attempt, the Brittlebush look first.

**Record, before any paint: stone over bedrock.** The studio's first sketch-to-world path wrote "a synthetic surface
layer (stone, Y=0)" ((studio) `156e77da`, 2026-06-18). The G157 backlog entry of 1 August describes what came out:
"The exported terrain is one flat block of stone" ((studio) `a1b20bca`).

**Record, "one rule per Y level": present, in the authoring specs rather than the painter.** No studio commit
names a per-height rule as a prototype. The nearest thing is the spec key `themeByHeight`, which first appears in
Ashen Quarry on 14 August (`644b383f`): a map from a height to a theme name, applied to every plan tier standing at
that height ("A tier is named by the height it stands at, which is how a theme reaches shapes whose ids the
compiler minted"). Ashen Quarry's spec gives one theme to y 41, another to 51, and "stair" to every height from 42
to 50. Whether this is the prototype he remembers, or something earlier and unrecorded, is a question for him. The
2025 C# editor has only a `Thickness` setting and the comment `// TODO: Stack layers inside schematic`
(MinecraftLayoutEditor `2abc036`, 2025-11-05).

**Record, top, sides and edges: the "walls, rims, plateaus" model, 1 August 2026.** `docs/world-export/terrain-painting.md`
was born that day under the title "Terrain painting — walls, rims, plateaus (G157)" ((studio) `a1b20bca`,
co-authored by Opus 4.8). Its three outputs are exactly his three: "rim = the top-most block of an edge column … wall =
the exposed riser between bedrock and rim; interior = the grass top". The same day added patterns and a theme JSON
(`18d2c8ce`) and scoped per-piece theming with a Theme rail in the UI (`77de36ea`, `2fe215b5`). **This is the most
probable origin of the phrase "map walls"**, which research `02` could not place; the painter's Wall bucket is the
side of a shape.

**Record, outside-in shading: 15 August.** "The inward axis is spendable: a band stack states which way it is
read" ((studio) `cb87fe76`). The doc's example is "a cobble rim, two rings of stone brick, then a field", measured
in from the landmass's void-facing edge. Band stacks became authorable in the Theme phase on 1 September (`7e1c5a47`).

**Record, slope: 5 September.** WE97, "an angle mask: a band stack read by how steep the ground is" ((studio)
`1e7d9aa8`); FEATURES calls it "the only thing in the model that tells a 45-degree hillside from a flat field".
This repository's `CLAUDE.md` still opens its finishing rule with it: "Finish the ground by its angle, not by its
height."

**Record, the transitions that never worked.** The account's complaint, one pattern per area, is the design of
TP10, "scoped per-piece terrain theming" (1 August). The studio later fixed one symptom of it: "a cell's theme is
its own layer's shape's" (TS80, in (studio) `378b2d58`, 2 September). `freeform/QUALITY-LEAP.md` names the same
limit from the other side: "The studio's buckets are chosen by edge and drop", while pgmvox painted "by slope and by
bed, not by shape".

**Record, the grammar: 9 October, in pgmvox, from Brittlebush.** The sequence on one day, all Opus 5.5, one session:

| Time (UTC) | Commit | What |
|---|---|---|
| 14:15 | `51754e2d` | "Brittle study: Brittlebush's visual signature, read and replicated": Brittlebush I and II read "block by block"; `STYLE.md` writes "a bedrock block under a five-course cap (spruce-stair rim, brick, dark-oak slab, dark-oak stair, black clay), one birch panel in each face's middle, floors as nested frames …" |
| 16:25 | `93aed9d0` | Brittlebush III built from the author's studio plan |
| 18:06 | `1daa30da` | "the Brittlebush grammar": sections, fills, panels over a full drop; `GRAMMAR.md` "how to split the style from the grammar" |
| 18:28 | `779cff79` | "pgmvox.grammar holds the rules of a structural board apart from its blocks … lay() speaks a ground in a style" |
| 18:47 | `4f0a3501` | Claywork, a second style "spoken in the grammar" |
| 19:21 | `fb4529a6` | Sandreach: "Brittlebush's grammar and grown ground on one board" |

That is the transfer he describes: the same rules laid in a second style within forty minutes, and the Brittlebush
style on a third board within the hour. The studio's port programme lists the result as Phase 7, "seven styles
(Brittlebush, Claywork, Terra, Marble, Foundry, Segment, Drastic)" (`pgm-studio/docs/pgmvox-port.md`). No FEATURES
line records Phase 7 as shipped (research `02`).

**The Brittlebush look is his, and older than the project.** Brittlebush is rockymine's CTW map of 2022
(CommunityMaps `ctw/brittlebush/map.xml`, `<created>2022-01-04</created>`, Ruediger_LP credited for the XML
template), and Brittlebush II is of 2023 (`<created>2023-01-28</created>`). Both are in PublicMaps too.

**Silent.** The record holds no statement that WorldEdit or a building plugin lacks such a grammar; that is his
judgement. Colour blending is not named as an open task anywhere I found.

---

## b. "No Blocks Placed", and Brittlebush III

**Account.** A CTW map made mainly in the web editor, by rockymine, Ruediger and Tttie, with a few blocks placed by
hand after all, holding the one surviving generated tree. Brittlebush III: layout made in the editor, colouring
entirely in game.

**Record: the map exists, in CommunityMaps, at `ctw/no_blocks_placed`.** Nothing in `pgm-studio-mapgen` holds it;
`maps/` has no such folder and no `map.xml` names it. The studio holds it twice: as the corpus golden
`no_blocks_placed` in `tools/PgmStudio.RoundTrip/corpus-goldens.json` ("31 regions … 4/4 obtainable", first recorded in
(studio) `e8abbef7`, 2026-08-13), and as the worked example of `docs/tools/configure.md`: "The map that goes with this
document is any sketch-origin map in the corpus of built maps. On `no-blocks-placed-verify` — 2 teams, 4 wools —
pre-flight reports 26 regions, 20 filters and 11 apply-rules, all four checks passing, and the gate open" ((studio)
`448b4e03`, 2026-08-13).

| Fact | Value | Source |
|---|---|---|
| Name, version | No Blocks Placed, 1.0.1 on arrival, now 1.0.2 | `map.xml` at (CommunityMaps) `11a15f7d`, `ff115048` |
| Created | 2026-08-07 | `<created>`, added by TTtie in (CommunityMaps) `f17a371a`, 2026-08-15 04:56 +0200 |
| Committed | 2026-08-07 20:58 +0200, by RuedigerLP, "No Blocks Placed: added" | (CommunityMaps) `11a15f7d` |
| Authors | rockymine, "Drawing pieces, shapes, and markers in the browser."; Ruediger_LP, "Wisdom."; Flamiix, "Minimalist." | `<authors>`, unchanged since arrival |
| Mode, teams | CTW, red and blue, 28 a side, two wools a team | `<teams>`, `<wools>` |
| Spawns | red (45, 20, −125), blue (−45, 20, 125) | `<point>`s |
| Wools | red (17.5, 19, −72.5), orange (72.5, 16, −57.5), blue (−17.5, 19, 72.5), light blue (−72.5, 16, 57.5) | `<point>`s |
| World extent | x −80…79, y 0…52, z −130…129 (160 × 260); 222,896 blocks, 115,923 of them bedrock | `tools/anvil.py` census of the published region files |

**The third author is Flamiix, not Tttie.** The `<authors>` element has named the same three since the first
commit. TTtie's only part in the record is the one-line commit adding the creation date. Whether Tttie contributed
to the map without being credited, or whether Flamiix is a name Tttie also uses, the record does not say; the
author should be asked rather than the credit assumed either way.

**The browser origin is stated in the map itself.** "Drawing pieces, shapes, and markers in the browser" is the
studio's Plan tool (pieces), Sketch tool (shapes) and placements (markers) as they stood on 7 August. No earlier
map in CommunityMaps was found whose credits say it was drawn in the studio (only additions since June were
checked); it is five days ahead of the two
`tools/mapgen` boards Ruediger committed on 12 August (Thornwake, credited to "mapgen", and Viridian, to "haiku";
(CommunityMaps) `37bdef57`). **Correction to research `03` §5 question 3:** both of those did reach CommunityMaps.

**"A few blocks placed by hand" is silent in the record.** No commit message or comment says so.

**The surviving tree, inferred.** A connected-component pass over the world's logs and leaves (ids 17, 18, 161, 162,
26-neighbourhood) finds 28 bodies, 14 of them trees standing in mirror pairs about the centre. The two largest are
oak bodies of 320 blocks with 50 logs each, at x −27…−17, y 14…30, z 41…52 and at x 16…26, y 14…30, z −53…−42. A
log count of 50 is limb wood rather than a trunk, which fits the studio's grown tree as it stood on 7 August: the
Catmull-Rom limb tree of 2 August (`de4e2ba1`) built from all-bark logs (`7b661c89`, 6 August). The other pairs carry
7 to 28 logs. **Which body is the generated tree is not stated anywhere; this is a reading of the blocks, and it
wants the author's confirmation in game.**

| Body (pair) | Blocks, logs | Wood | Where (x, y, z) |
|---|---|---|---|
| 1 | 320, 50 | oak, all-bark | −27…−17, 14…30, 41…52 / 16…26, 14…30, −53…−42 |
| 2 | 156, 28 | dark oak | −4…2, 11…20, −27…−21 / −3…3, 11…20, 20…26 |
| 3 | 135, 8 | oak | −44…−38, 18…28, 96…102 / 37…43, 18…28, −103…−97 |
| 4 | 134, 11 | jungle | −27…−21, 9…22, −78…−72 / 20…26, 9…22, 71…77 |
| 5 | 114, 10 | acacia | −55…−47, 15…23, 32…40 / 46…54, 15…23, −41…−33 |
| 6 | 81, 8 | birch | −27…−22, 9…22, −25…−19 / 21…26, 9…22, 18…24 |
| 7 | 57, 7 | spruce | −43…−39, 16…25, 68…72 / 38…42, 16…25, −73…−69 |

**Brittlebush III: the layout is his, drawn on the deployed studio.** The deployed studio lists `untitled-plan-8`,
named "Brittebush III" (sic), CTW, author rockymine, last changed 2026-10-11 (`GET /api/maps`). The pgmvox board's
report says: "The plan is `plan.json`, saved from the studio's map `untitled-plan-8`" (`freeform/lib/boards/brittlebush-iii/REPORT.md`).
The world in `maps/ctw/brittlebush_iii` credits "rockymine" and "Claude (freeform generator, pgmvox)" and is four
teams of twelve; its colouring is pgmvox's Brittlebush style, not his hand.

**Silent.** His in-game-coloured Brittlebush III is not in this repository, the studio, CommunityMaps or PublicMaps
(both heads searched for `brittlebush`; only I and II exist). The film or the history should ask for the world.

---

## c. Millrace in full

**Account.** He drew the layout in the browser; an agent made the landscape, Sonnet and Opus were tried, and Opus's
terrain was kept. He and Ruediger finished it together, five hours side by side, ten person-hours. Fable was then
asked to rebuild it as faithfully as possible and began copying the trees, which led him to tidy his world of custom
trees (under 100) and add it to the repository. The AI's landscape stayed; settlements and houses were redone and
trees added.

**Record, the drawing.** `f956c846`, 2026-08-30 01:07 +0200, "Map Experiment: plan, layout and intent files", git
author `michael`. The world is `maps/dtcm/map_experiment` with rockymine's UUID as sole author. The commit that used
it says the experiment "is drawn in the Sketch tool rather than compiled, so its geometry IS its layout" (`bb7c8a7f`).

**Record, three agents, not two.** `bb7c8a7f` (2026-08-30 16:01 +0200) built three boards off the basin:
`opus5-millrace` (Opus 5, "the basin as a walled water course"), and two by Sonnet 4.5, `sonnet-cutwater` ("floods and
bridges the same basin with its own composition", 260 × 250) and `sonnet-fallowmere` ("the open reading: fewer
things, more ground") (`BOARDS-BUILT.md` lines 242–243). His "Cutwater / Millrace" is right in pairing; the record
adds Fallowmere. The record holds no written judgement by the author on why Opus's was kept; the choice is shown
only by his finishing it.

**Record, the hand finish: five hours for two people.** `review/rockymine-ruediger-millrace.md` opens: "myself
(rockymine) and Ruediger_LP spent 5 hours to complete Millrace." `BOARDS-BUILT.md` line 245: "five hours of WorldEdit
and Arceon over the studio's world". The account's "5 hours side by side, 10 person-hours" agrees with this; the
record does not contradict it, it states the clock time. Committed as `11d926f1`, 2026-09-02 03:40 +0200.

**What was kept and what was redone.** The review: "the terrain, spawn platform, spawn house, objetives, canal walls,
water levels, bridges, boulders, and most house placements were kept intact … essentially all that was done is
theming and some dressing. the redesign of the houses and their interior as well as adding a different ship, statue
and observer spawn play a big part too. but most comes simply down to better theming and using the custom trees."
`BOARDS-BUILT.md` adds that "the eighteen grown trees [were] replaced by sixteen of the author's own showcase trees".
Fable's diff measured "29,954 of 35,610 columns keep their surface height exactly" (`review/fable-millrace-revamp.md`).
The account's "settlements and houses were redone" fits "the redesign of the houses and their interior"; the
review says most house *placements* stayed.

**It went upstream the same day.** CommunityMaps `dtcm/millrace`, "Millrace 2.0.0" and "2.0.1", committed by
RuedigerLP on 2026-09-02 ((CommunityMaps) `c86226db`, `21b6d9b8`). Its credits: rockymine, "layout, terrain, block
palette, beautification"; Ruediger_LP, "interior design, houses, beautification"; Opus 5, "layout composition,
initial draft, sculptures, bridges". `<created>2026-08-30</created>`.

**Record, Fable's rebuild, and the order of the night.** All on 2 September (UTC):

| Time | Commit | What |
|---|---|---|
| 00:53 | `b36147a0` | "Add rockymine's custom trees" (`showcase/tree-showcase`, git author `michael`) |
| 01:40 | `11d926f1` | "Add rockymine's and Ruediger_LP's revamp of Millrace" |
| 03:08 | (studio) `378b2d58` | WE72, Fable 5.1: "a copied tree, cut out of a world and planted as a recipe … Measured on the author's tree-showcase and the Millrace revamp: every tree planted by hand there is one of sixteen showcase trees" |
| 03:23 | `dc2efbd0` | Fable 5.1: "Millrace diffed against its hand revamp, restated as documents"; `specs/fable-millrace-revamp`, "copied tree recipes, the statue, tug, balloon and beacon frames lifted out of the hand-built world" |
| 08:18 | `774b3f22` | Mossgill: "half of Millrace's box, a new layout, the revamp's techniques stated from the start" |

**This contradicts the account's order.** The trees were committed before the revamp and before Fable's work, and the
showcase world had been in the studio since 12 August, when 75 of its trees were measured ((studio) `c9ea46d6`: "one
author-built tree per 19x19 platform, 14 families by platform band plus a wool tree"). What Fable's rebuild did cause
is the copied-tree *form*: "`pgm-studio/tools/seed-trees.cs` cut all 74 standing trees of the showcase into the
library" (`review/fable-millrace-revamp.md`). A tidy-up of the world is recorded later, which may be what he
remembers: 20 September, a jungle row and a willow row and "fourteen feet that hung a course above their platform
now sit on it" (`d44958cb`, 86 trees); 1 October, "rockymine set r13's tenth birch back on its platform and built
three new rows" (`223aaebd`, 95 trees).

**Record, the count.** `pgm-studio/docs/world-export/tree-corpus.md`: "The tree-showcase world holds 95 author-built
trees, one per 19×19 platform, in 20 bands". Under 100, as he says.

**Silent.** How the work was split between the two of them; how many sessions the hand finish took; whether Fable was
asked "as faithfully as possible" (the commit says "restated", the brief behind it is not committed).

---

## d. Trees: every generator, and where a generated one stands

**Account.** A vanilla-like blob or disc is easy for an LLM to code; a real tree generator failed. One generated
tree survives, in No Blocks Placed. Tree building is "a religion".

**Record, in order.** Every tree form the studio has had, with why it went:

| Date | Commit (studio) | Form | Fate |
|---|---|---|---|
| 2026-08-01 | `a3160327` | prototype page, "recursive tree growth" | rebuilt the next day: "The recursive brancher read as a fractal, not a tree" |
| 2026-08-02 | `de4e2ba1`, `20c87902` | the grown tree: limbs as Catmull-Rom splines swept with a disc, then a recursive skeleton with flowing spines | measured as broken on 12 August; deleted 10 September |
| 2026-08-05 | `41b40336` | the vanilla tree, `TreeTemplate`: "a trunk of a known height under a canopy of a known profile … a radius per course" | **still in the studio** as `TreeForm.Template` |
| 2026-08-12 | `c9ea46d6`, `ec91a078` | the grower measured against 75 hand-built trees, then regrown to the corpus | "1516 of 4020 never touch their branch. Below height 12 the crown stops cohering entirely and 42-76% of it floats free" |
| 2026-09-02 | `378b2d58` | the copied tree, the author's tree carried block for block | **the form in use** |
| 2026-09-10 | `6b0b3f09` | the grown tree removed: "they came out broken; the author's ruling is that the form goes rather than gets a knob"; 496 lines of `Geom`, migration `M0035` | — |
| 2026-10-08 | (mapgen) `12675ed9` | pgmvox 0.10.0: "the studio's copied trees, planted whole, turned with their data"; pgmvox's only procedural tree is `dead_tree` | in use on freeform boards |

His "blob or disc is easy" matches the template tree, which is a canopy profile per course and has survived. His
"a real tree generator failed" matches the grown tree's measured failure and removal. The removal commit also deletes
every stored recipe that named the grown form: "a recipe whose shape cannot be built has no second reading as one that
can".

**Where generated trees still stand.** Three places hold them, by the record:

- **No Blocks Placed** (CommunityMaps), built 7 August, between the grown tree's arrival and its removal. §b gives the
  candidate bodies; which one is generated is inferred, not stated.
- **`maps/dtcm/millrace`**, Opus 5's world before the hand finish, with its "eighteen grown trees" (`BOARDS-BUILT.md`
  line 245). The published Millrace replaced them.
- **The worlds of the first fifteen** (`maps/ctw/*`, `maps/dtcm/*` from 11–12 August), built by `tools/mapgen`, whose
  spec "builds a whole map from one spec: … the trees" ((studio) `5897944a`). Which tree form each used is not
  recorded per board.

His claim that one survives in a *played* map is consistent with this: of the three, only No Blocks Placed is
published with its generated tree in place. Thornwake and Viridian in CommunityMaps are of the first fifteen and may
carry grown or template trees too; they were not scanned for this document.

---

## e. The Python rework: freeform, then pgmvox, then the port

**Account.** The layer-based definition hit a hard limit; cavities were very hard because cave walls had to be
defined one by one; noise-based shaping is easier but has its own limits. He told a Claude session he did not like
it and to think. Python came first, in the mapgen repository, usable; then its functions went into the C# studio
and the website. The first board was a floating island with two villages, "Riverside" or similar.

**Record, the first board is Riftwater, 7 October.** `2169c018`, 2026-10-07 22:37 UTC, "Riftwater freeform: the plan,
the sketch, and the writer bridge" (Opus 5.5, session `…01JFykgZF2FRCqGGugXE9LUG`), then nine more commits in 33
minutes. Its report: "one river valley split down the middle by a bottomless rift. On each side a brick-and-timber
market town climbs from the rift to its square, a mining village sits under a wooded ridge … The valley floats from
y 27" (`freeform/lib/boards/riftwater/REPORT.md`). **His "Riverside" is Riftwater**: a floating river valley, and on
each side two settlements, a town and a village. It is 240 × 176 for 16 a side (`PLAN.md`) and "no studio authoring
pipeline was used"; only the studio's region writer.

**Record, what the session was told.** Silent. No commit, report or plan records the instruction "I don't like it,
think". The repository's own account of why the boards improved is `freeform/QUALITY-LEAP.md`: "The leap came from
moving the decisions the studio makes for an author back into the author's hands, and from a loop that checked
them."

**Record, cavities.** The studio's carve was column-wise: "A subtract has no `y` at all — it is a set of `(x, z)`
cells … so it cannot hollow a column out from the middle" (`pgm-studio/docs/tools/sketch.md`). pgmvox could from its
0.10.0, on the day after Riftwater: "under: tunnel, chamber, carve, dress_cave, gallery_line, gallery, shaft"
(`12675ed9`, 2026-10-08). The 10 October playtest sorting records the gap in the studio's own column: "Tamarisk Wash |
well shaft does not open onto its tunnel | … studio cannot carve the tunnel at all"
(`analysis/freeform-vs-studio/playtest-feedback-2026-10-10.md`). The studio gained carves on 25 October: "TS140:
carves — a tunnel, a chamber and a shaft" ((studio) `1e10a4c6`). His "cave walls defined one by one" describes the
layer route of August, where an underground storey was a stack of sketch layers (`under`, `lid`, `ground` in Liminal
DTM II, `BOARDS-BUILT.md` line 281).

**Record, noise.** The studio's terrain since 24 October is the modifier stack, including Roughness, Warp, Lumps and
Shatter ((studio) `16864f7f`, "the modifier stack is the only terraforming"). His remark that the new hand-built map
cannot be expressed in it either agrees with research `04` §3b.

**Record, what moved into C#.** `pgm-studio/docs/pgmvox-port.md` ((studio) `2ed975bc`, 2026-10-15): pgmvox is "the
Python library for freeform boards in `pgm-studio-mapgen` (`freeform/lib/pgmvox`, 0.30.0 on 15 October 2026)", nine
phases, decisions D1–D23. Shipped or parked by 4 November ((studio) `bb53150a`): framed renders and rule tiers,
the sketch as one document with draggable play pieces, the modifier stack, paint rules and slope-thinned soil,
carves and primitives, per-piece stamps, house doors. The grammar (Phase 7) has no shipped line. Before the port, a
controlled run held the model fixed (Sonnet 5.5) and found "the two tools made boards of comparable quality"
(`analysis/freeform-vs-studio/experiment/RESULTS.md`, `0e90bfe6`, 10 October).

---

## f. "Slop Sundays", playtests, and Tttie

**Account.** Tttie is a mapmaker, not an active contributor like Ruediger; they talked often and ran the map tests
together, "Slop Sundays" on the server, about two hours of playing the AI maps. Early maps looked and played alike.

**Record, the phrase.** Silent. "Slop", "Sunday" and "Sonntag" occur in no commit message or file of either studio
repository in that sense (a search for "slop" finds only "slope").

**Record, playtests.** Two are recorded:

- **The 32-a-side test boards, 27 September (a Sunday).** "Delverdale and Whitstone Weald: two large boards for a
  32-a-side play test" (`d274c0ae`, 21:55 UTC). The commit records the boards, not the session or who played.
- **The freeform and trial boards, 9–10 October.** "Playtest fixes: Lantern Pass, Lantern Drop, Calcite, Saltgate"
  (`e9531f6f`, Friday 9 October 22:06 UTC), and the sorted feedback committed at 00:56 UTC on Saturday 10 October
  (`8ce02131`): "The author's notes from playing the freeform and trial boards … The author's wording is
  summarised". It lists faults on 22 boards; the studio "would have caught 9, partly caught 4, and not caught or could
  not have built 17".

Neither record falls on a Sunday by its commit time, and neither names the players. If Slop Sundays are a series,
the record holds at most their results.

**Record, Tttie: three places, none in the studio repositories.** The earlier research found nothing because it
searched only the two studio repositories.

| Where | What | Source |
|---|---|---|
| CommunityMaps, as committer `TTtie` | "No Blocks Placed: add creation date", 2026-08-15 | (CommunityMaps) `f17a371a` |
| CommunityMaps, own and maintained maps | Watch Your Head (1.1.0 in December 2023, pre-releases of 1.2.0 on 31 July and 6 August 2026, hard mode disabled 28 September), Notre-Daaaaam of Paris (2.0.0, April 2024), and maintenance on Bricked N Clayed (24 October 2026), Crown and Icarus Fortress (20 September 2026) | `git log --author=TTtie` on CommunityMaps |
| pgmstudio.de | account `TTtie`, one sketch, `untitled-sketch-7`, CTW, last changed 2026-10-28 | `GET /api/maps`, `GET /api/map/untitled-sketch-7` |

"A mapmaker" is borne out: TTtie maintains maps in the community repository across three years. That TTtie ran
tests with him, and that the two talked often, is his account alone.

---

## g. The review tool, the empty maps, and dead ground

**Account.** Feedback got better with the review tool: early on he described faults in words and the model lacked
coordinates. Two maps were extremely empty; empty, dreary maps remain a problem. Maps got prettier at the end
through texture rules and telling the model where ground is dead, but "dead" is subjective.

**Record, words first.** The first review was a fault list in prose: "Write down where the first fifteen maps fall
short (MG1-MG13)" ((studio) `1ffb7728`, 12 August), now `docs/tools/mapgen-review.md`.

**Record, notes with coordinates: 28 September.** "TS115–TS118: map notes — feedback pinned to the board, answered on
the note" ((studio) `e24eb08b`, 20:30 UTC, Opus 5.5). A note is pinned "to the whole map, to the picture in view, or
to ground on it"; "Point, Box and Lasso … projected onto the ground the picture's own rays hit by GET
…/render/eye/pick". On 2 October the notes could be handed to an agent with one button ("TS146: the author hands the
notes to an agent", `77acee4f`).

**Record, the two empty maps are Gypsum Reach and Sootcombe, 28 September.** `reports/opus55-notes-run.md`, the run
that tested the notes loop: "The author reviewed the first two boards from their pictures and found them empty.
Paraphrased: … there is no dirt or grass for a tree to stand in, two houses stand by a path, the frontlines are bare,
and the outlines were never shaped … Empty is what players dislike about maps like these." That remark itself was
given in chat, "not as a note". Both boards are still on pgmstudio.de (`opus55-gypsum-reach`, last changed 6
October; `opus55-sootcombe`, 30 September).

**Record, dead ground: a measure calibrated on his own reading, then a rule.**

| Date | Commit | What |
|---|---|---|
| 2026-08-16 | (studio) `b493e94a` | `GroundCoverage`: shortest walks between waypoints, widened six blocks, "and everything left is dead ground"; "a measurement, deliberately not a gate" |
| 2026-08-18 | `9520281c` | "The driver never asked whether the ground is used, and Wheal Hazel's bar is 60% dead" |
| (doc) | `pgm-studio/docs/world-scan/ground-coverage.md` | the ten-block ring "is calibrated against the one board known to carry dead ground", piece by piece against "the author's own reading": `works-lo-w` dead / 100%, `bar` "about two thirds" / 62% |
| 2026-09-21 | `32c77ef7` | the dead share's band is `[0, 0.12]`; all four Haiku 4.5 specs fail it (0.766 to 0.854) |
| now | `LayoutRules.cs`, `LN5` | "The share of a layout's ground that lies off every route between waypoints is more than 12 percent", category `Unplayable` |

His point that "dead" is subjective is in the record's own wording on 10 October: "Redwash Mesa | top of the mesa
empty | composition | LN5 counts dead ground, cannot say what belongs" (playtest sorting). The measure began as a
reading of his judgement and became a refusal; the record does not show him ruling on whether that was right.

---

## h. The flat, 500-wide moshpit map: Spinebreak or Hollow Crown

**Account.** Either candidate; one core and one monument per team; flat; nobody walks 250 blocks sideways where
nothing is; enemy objectives about 10 blocks apart, a moshpit with no flanking.

**Measured from the `map.xml` files and the worlds.** Centres are cuboid centres; distances are horizontal. Ground
heights are each column's highest non-bedrock block, read with `tools/anvil.py`.

| | Spinebreak (`maps/dtcm/spinebreak`) | Hollow Crown (`maps/dtcm/hollow_crown`) |
|---|---|---|
| Built | 11–12 August, Opus 5 through `tools/mapgen`; `<author>mapgen</author>` | 22 August, Haiku 4.5, run 5; `<author>Haiku 4.5</author>` |
| Modes declared | `dtm` and `dtc` | `dtm` and `dtc` |
| Objectives a team | **4**: two monuments and two cores | **2**: one monument and one core |
| Red defends | monuments (51, 201), (41, 61); cores (70.5, 200.5), (60.5, 60.5) | monument (−19.5, −24.5); core (20.5, 25.5) |
| Blue defends | monuments (−49, −199), (−39, −59); cores (−69.5, −199.5), (−59.5, −59.5) | monument (19.5, 24.5); core (−20.5, −25.5) |
| Nearest enemy objectives | **144 blocks** (the two second monuments) | **0–2 blocks**: each team's core cuboid overlaps the enemy's monument cuboid (x 18…21, z 23…26 and its turn) |
| Spawns | red (−50, 70), blue (50, −70) | red (0, 50), blue (0, −50) |
| Ground extent | x −72…72, z −202…202: **145 × 405** | x −50…49, z −60…59: **100 × 120** |
| Flatness | tops y 1…26, median 11, 10th–90th percentile 9…18 | tops y 9…51, median 10; **9,702 of 10,400 columns at y 10** |
| Build area | `x −20…20, z −10…10` only | — |
| Described as | "one long 145×420 ridge, an objective at each end" (`BOARDS-BUILT.md` line 51) | "two spawns at opposite ends, one central reach piece containing the objectives, and nothing more" (`review/haiku-r5-hollow-crown.md`) |

**Reading.** Hollow Crown matches the account on objectives, flatness and closeness: it is the map where a team
defends a core standing in the enemy's monument. Spinebreak matches on length and on the line: eight objectives
strung down one axis. The account's "500 wide" fits neither, and Spinebreak's 405 is the nearer. **The memory may
join the two**, which were made ten days apart and are among the four most line-like objective layouts in the repository
(research `03` §4: principal-axis ratios 0.003 for Hollow Crown, the lowest, and 0.144 for Spinebreak, the fourth). A third candidate on pgmstudio.de or in the studio's
local database was not measured.

---

## i. Sonnet against Opus

**Account.** Sonnet's maps were de facto worse, whatever the numbers say; whether because of instructions or the
model is unknown. Late in the year Opus maps are clearly better, through verification steps and model progress.

**Record, the numbers do not say Sonnet was better; on the one controlled day they say the reverse.** On 21
September Sonnet 5 and Opus 5 built four boards each on the same brief. Two of Sonnet's four were outside the
studio's dead-share band (27.4% and 43.0% against `[0, 0.12]`); none of Opus's were (0.0% to 9.6%) (research `03`
§2). All eight exported.

**Record, the reviews are mixed, and the best words for a Sonnet board are the author's.** On the 10 October
experiment, where Sonnet 5.5 built every board in both tools, the author's points as written down by the agent:
Abbeymoor in pgmvox "really looks like a place, with a nice style and a few flaws"; Slatefold pgmvox "The houses near
the spawn stand all in one line", "too much stone in general" (`analysis/freeform-vs-studio/experiment/REVIEW-1.md`).
The experiment's verdict concerned the tools, not the model: "comparable quality".

**Record, what favours Opus.** The board he chose to finish was Opus 5's Millrace over two Sonnet 4.5 boards of the
same basin. The playtest's "essentially perfect" is Riftwater, an Opus 5.5 board, with the repository's caution that
it took "Opus, hours per board rather than minutes, rounds of the author's review, and bespoke code" (`RESULTS.md`).
Of Coldstore, Opus 5.5, 22 October: "The author judged the board finished and the map.xml a success" (`BOARDS-BUILT.md`).

**Silent.** No controlled run compares Opus 5.5 with Sonnet 5.5 on one brief in one tool. "Whatever the numbers say"
has no number against it; the comparison he means is his own.

**Two models the history had not counted.** The deployed studio holds two boards by **Haiku 5.5** (`haiku55-bracken-vale`,
`haiku55b-rowanford`, both 7 October) and two by **Grok** (`grok-hollow`, `peatcut`, 28 September), beside 18 by Opus
5.5 and 8 by Sonnet 5.5 (`GET /api/maps`, `agentMade`). Research `03` knew Grok only from its blind run of 15 August.

---

## Other claims in the account

**"The browser tool is fast for trying layouts."** Consistent with the record and not measured in it. The deployed
studio's list shows 72 maps, 31 of them agent-made, and eleven people besides the agents with a map or sketch of their
own. The account's "the UI is not much used" is his judgement; the list is the only count.

**"Concept maps such as the labyrinth were his ideas, built 1:1."** The labyrinth is Opus 5's Overwall, 25 August, "a
labyrinth of ten-block pillars on a twenty-two block grid, so every passage is twelve wide" (`BOARDS-BUILT.md` line 203;
`df58eb80`). Its row and report do not say whose idea it was. Coldstore is recorded as "the author's concept world",
sent "with signs explaining each piece" (`BOARDS-BUILT.md`).

**"Is the JSON a domain-specific language?"** The record never calls it one. The nearest statements are that a map
"is one JSON file" ((studio) `5897944a`) and that one spec is "the authoring work" (`CLAUDE.md`).

**"His own hand-built map has a dead area that makes sense. Its files come later."** That map is the fire-and-ice
half (research `04`), whose world is in no repository.

## Sources not read

`pgmstudio.de` beyond its public map list and two map documents; the studio's local database; the scanned corpus
output (`/media/sf_repos/pgm-studio-output`, not on this machine); the worlds of Thornwake and Viridian (not scanned
for trees). Throwaway scripts used for the tree bodies and the flatness counts were kept in the session scratchpad and
are not committed.
