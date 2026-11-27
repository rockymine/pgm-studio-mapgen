# Aerie, monument size, and the other faults of the trial-run boards

Research note for the written history. Every claim carries its source: a commit hash with date (UTC unless marked),
a file path, or a world read with the block reader. Quotes are verbatim. Where the record says nothing, this note says so.
Two repositories are meant by "mapgen" (`/home/user/pgm-studio-mapgen`) and "studio" (`/home/user/pgm-studio`).

Short version. The Aerie criticism is **not written down anywhere in either repository**; what the record holds is the
board as built (25 August 2026), the studio fixes made with Aerie as the measured case, and a mechanism that would
explain "nothing editable" (inference, marked). The monument rule is **`DC3`**, shipped in studio commit `cf122593`
(19 August 2026). The other faults were filed by the author's review as `B141`-`B188` in studio commit `705a77c6`
(14 August 2026, 16:17 UTC).

## 1. Aerie (`opus5-aerie`, Opus 5, 25 August 2026)

### 1.1 What the record says about the build

- Built and committed in mapgen `882f75ab`, 2026-08-25 13:54:01 UTC, "Three small boards: a mesa terrace, a chalk
  quarry, and six crags over void" (with Kiln Row and Deepcut); merged in `55e5493d`, 2026-08-25 16:36:16 UTC.
  The session began 2026-08-24 23:48 UTC (`film/history/research/sessions/06-labyrinth-and-aerie.md`).
- The author's brief for it was free: at 13:18 UTC on 25 August he asked for a capture-the-wool map, a destroy map and
  one mixed map, "just go with something you think would be interesting and surprises me" (same write-up, section 1).
  At 13:20 UTC he ordered no water lanes: "Just use the normal build regions."
- Mapgen `review/opus5-aerie.md` (written by the model, added in `882f75ab`) describes the board: 72 x 128, six crags,
  a 24-block strait, "ground from **y26 to y38** over void everywhere else". On the zones: "Four build zones, one per
  gap, and nothing else on the board is buildable - `deny(void)` closes everything outside a build area, so the zone
  list *is* the list of places a bridge may go." The index row in `BOARDS-BUILT.md` (line 202) repeats it: "`deny(void)`
  closes everything outside the four build zones, so the zone list is the map".
- The same review reports "export gate OPEN", "6.1 % dead" and that "Buildability reports **four placements over open
  void** - both spawns and both wools", calling it "the honest reading of a sky board and not a fault".
- The model's own account of its mistakes (`reports/opus5-smallboards-run.md`): it first put the wool on the crag nearest
  the strait ("`WL10` read a wool-front-distance of **8**"), then drew nine crags with six-block gaps ("I drew nine crags
  and eight running jumps") and rebuilt.

### 1.2 The criticism: not in the record

- The author's wording (author account, instalment two or three, quoted in session 06 section 6): "real non-playable xml
  in Aerie due to nothing being really editable and woolrooms appearing on odd islands, bad build zones, etc." Instalment
  ten adds only: "The criticism of the map with unplayable XML (Aerie) and the 27-block monuments is in the logs and
  commits".
- Searches made: `git log --all -i --grep=aerie` in both repositories; every `.md` mentioning Aerie in mapgen
  (`review/`, `reports/`, `BOARDS-BUILT.md`, `maps/INDEX.md`) and studio (`FEATURES.md`, `BACKLOG.md`, `TODO.md`, `docs/`);
  searches for "odd island", "not really editable", "unplayable". **No commit message, review, report or board entry
  contains the author's complaint, a quote of it, or a task filed from it.** Session 06's author-message stretch (13:11-16:20 UTC
  on 25 August) holds no Aerie complaint either; the earlier part of the transcript was not read by that write-up.
- Mapgen commits that name Aerie: `882f75ab`, `55e5493d` (25 Aug) and `49f2467c` (2026-10-10, "maps: one folder per game
  mode") only.

### 1.3 Studio changes that cite Aerie (measured on it, not filed as its criticism)

| Date | Hash | What it says about Aerie |
|---|---|---|
| 2026-08-25 22:27 | studio `d52dc1b1` "WE31 - a foundation seals the ground a cell has, and says when its neighbour has none" | "Measured on opus5-aerie at (20, 28): bedrock from y0 to y24 under a wool room whose crag begins at y16" - a wool room hung a pillar into open sky. Same hour as the build; the nearest thing to a wool-room placement fault on this board. Also adds `WX11`, a complaint where the cell beside a stamped structure is void or "more than a step below the floor". |
| 2026-08-26 09:45 | studio `7a681650` "TN8: the CTW strait is re-read off the drawn board" | "opus5-aerie has six landmasses and fifteen gaps between them, eleven outside the band and all authored water." Used to explain why only passed pairs are re-read. |
| 2026-08-31 11:06 | studio `a12fd725` "G8's fill ratio frames on the ground and not on a build zone past it (B150)" | Aerie's fill ratio moves 0.342 to 0.363 once a build zone no longer counts as ground. |
| 2026-09-02 17:03 | studio `600e8669` "A destroy board's frontline has no width cap, and a zone that overhangs is named (G263)" | Does not name Aerie. Restates `BZ9`: "a stretch of build zone beyond the last ground it docks, which connects nothing and reads as no man's land" - the build-zone rule nearest to "bad build zones". |
| 2026-09-20 22:18 | mapgen `6bc1a2cb` "Drop voidEnforcement, and re-export the 22 worlds that carried its region" | Edits `specs/archive/opus5-aerie/opus5-aerie.intent.json` (removes `"voidEnforcement": null`). Quote on the fault removed: `void-enforcement-area` was "`<everywhere/>` with `block-place="deny(void)"` ruled onto it ... it denied placing over void inside the rectangles the board declared buildable". Aerie's own XML never carried that region (checked: `882f75ab:maps/opus5-aerie/map.xml` has only `<apply block="no-void" region="not-build-area" ...>`). |

### 1.4 What the stored XML shows (read from `maps/mixed/aerie/map.xml`, identical in the 25 August commit for these parts)

- Seven build rectangles, `build-area-1` to `build-area-7`, not four: `8,34..32,44`; `-32,-44..-8,-34`; `-32,28..-8,44`;
  `8,-44..32,-28`; `-8,12..8,34`; `-8,-34..8,-12`; `-34,-12..34,12`. The review's "four build zones" and the XML's seven
  disagree; the record does not explain it.
- The only void rule: `<apply block="no-void" region="not-build-area" message="You may not edit the void!"/>`.
- Wool rooms: `red-wool` `12,22..28,32` and `blue-wool` `-28,-32..-12,-22`, wools at `20,25,28` and `-20,25,-28`; cores at
  `y40-45` in `the-eyrie-region` `-22,40,18..-17,45,23`. These sit on the fold and spire crags exactly as the review says;
  the record gives no instance of a wool room on a wrong island.

### 1.5 A mechanism that would explain "nothing editable" (inference, not stated for Aerie anywhere)

- Studio `e156c366` (2026-08-31 13:38): `ground` is "nothing forbids it, which on a void-enforced board is exactly the
  columns carrying a block at y=0 - the whole of what <void/> tests".
- Mapgen `62dd9b6d` (2026-10-11 14:47): "Hollow Mesa, Riftwater, Cinder Reach and Redwash Mesa float clear of y 0, so PGM's
  void filter read every column as void and refused every block." The fix lays block 36 at y 0 under ground.
- Studio `18a143f8` (2026-10-11 17:03): "A floating goal over columns with nothing at y=0 fails both under the studio's void rule."
- Aerie floats (ground y26-y38). Reading its stored world with the block reader: `eye maps/mixed/aerie find 36` returns
  **0 blocks**; the world spans y 0..65 with 50,245 blocks. Aerie is not in the list of four boards `62dd9b6d` repaired.
  So under the void rule every column outside the seven rectangles would read as void and be refused. That fits the
  author's "nothing being really editable", but **no document says Aerie was judged this way**. PGM itself was not run.

## 2. Monument size

### 2.1 Where the fault was recorded

- The author's review of the 14 August trial boards became studio `BACKLOG.md` entries `B141`-`B188`, filed in studio
  `705a77c6`, 2026-08-14 16:17:25 UTC, "Forty-eight findings filed and bucketed" ("The author's review of twelve of those
  boards - every claim re-measured against the plans, the layouts and the built worlds").
- Entry **`B162`** in that commit: "An obsidian destroyable may carry at most three obsidian blocks, and three maps carry
  27, 27 and 15." Body: "`corvid-hollow` and `basalt-reach` both pair `cube-3` with obsidian - 27 blocks, unhollowed ...
  `tallow-mirefast` pairs `column-plus` with obsidian, five a layer over three layers, 15 blocks, probed at y16-18. Of seven
  destroyable boards only `ashfall-scar` is right with obsidian, on `pillar-3`." Its table also lists, as fine:
  `quillon-barrow` and `sonnet-holdfast` `cube-3` in ender stone (27), `tallow-kilnrow` `cube-4` in ender stone (64),
  `quillon-foundry` `column-plus` in ender stone (15). Signed "author, 2026-08-14 - swept over all 21 folders by parsing
  the intent JSON - probed on all three offending maps."
- The same finding in mapgen's deleted `ART-DIRECTION.md` (commit `7107785c`, 2026-08-14 16:17:40 UTC, "An authoring
  system with art direction, named briefs and a reviewer that is not the author"): "Three maps put obsidian in a
  destroyable over its limit." and the rule row "**Obsidian caps at three** | A destroyable may carry at most **3 obsidian
  blocks**, so only the **pillar** styles may use it. `cube-3` (27), `cube-4` (64) and `column-plus` (15) take **end stone,
  gold or emerald**. | `basalt-reach` 27, `corvid-hollow` 27, `tallow-mirefast` 15 | `B162`". The commit message says:
  "obsidian caps at three blocks and three maps carry 27, 27 and 15".
- These boards were the Opus run 2 and Sonnet run 2 trial boards; commits: `corvid-hollow` mapgen `86f478e6` (2026-08-14
  09:20), `tallow-mirefast` `7764c04e` (09:34), `basalt-reach` `c8ce37f0` (2026-08-14 10:10 +0200).
- Not found: a "13-14 August" review document that records the 27-block monument as a fault before `705a77c6`. Mapgen
  `review/corvid-hollow.md` and `review/basalt-reach.md` were checked only for the other faults in this note.

### 2.2 The rule and the commit that enforces it

- Studio **`cf122593`**, 2026-08-19 07:36:31 UTC, "A core leaks one course lower than it read, and a goal says what it could
  not be built as", item `B162`: "Obsidian is worth three blocks (author), so a cube or a plus-section column carrying it
  is built in ender stone instead, with a complaint naming the size and the cap; the map.xml then declares what was laid."
- In code: `src/PgmStudio.Domain/DestroyableMaterials.cs`: `ObsidianLimit = 3`, `Bulk = "ender stone"`;
  `Resolve(style, materials, columnHeight)` counts `ObjectiveFootprint.BlockCount` and switches obsidian to ender stone
  when the count is over 3. The refusal id is **`DC3`**, a *complaint on a built world* (the goal stands), documented in
  `docs/pgm/destroyables-and-cores.md` ("DC3 - obsidian is worth three blocks, and the studio will not build more") and
  `docs/refusals.md`. Its message: "is a cube-3 of 27 blocks, more than 3 blocks of obsidian, and is built of ender stone"
  (form from the code; the stored dressing report reads "cube-3 is 27 blocks and obsidian is worth at most 3 of them -
  built in ender stone", mapgen `specs/archive/haiku-r5-hollow-crown/dressing-report.json`).
- The rationale in the source: "Obsidian is the slowest block in the game to break, which is what makes it right for the
  pillar every second corpus destroyable is - one to three blocks, a raid rather than a shift - and wrong for anything
  bigger: a 27-block cube of it is a grind nobody performs."
- Same commit also caps float at "the author's twelve" (`OB22`) and the shipped sweep line in studio `FEATURES.md`:
  "Swept over 21 authored folders: `basalt-reach` and `corvid-hollow` carried 27 obsidian on `cube-3`, `tallow-mirefast` 15
  on `column-plus`." Later boards hit the rule and were told: `reports/opus5-overwall-run.md` "I asked for obsidian and got
  told. `DC3`"; `reports/haiku-run5.md`; `review/opus5-swallet-dale.md`.

### 2.3 Real examples from the stored worlds

Block reader: `eye <world> find 49` (obsidian, id 49). The reader splits a cluster across region seams, so the two parts
are added. All three worlds are the stored maps in mapgen `maps/dtcm/`.

| World | Where | Reader output | Blocks |
|---|---|---|---|
| `maps/dtcm/corvid_hollow` | x -1..1, y 13..15, z -31..-29 (and mirror at z 29..31) | 18 + 9 | 27 each (a 3x3x3 cube), 54 obsidian in all |
| `maps/dtcm/basalt_reach` | x -41..-39, y 26..28, z 34..36 (and mirror x 39..41, z -36..-34) | 18 + 9 | 27 each (3x3x3) |
| `maps/dtcm/tallow_mirefast` | x -1..1, y 16..18, z -51..-49 (and mirror z 49..51) | 12 + 3 | 15 each (the plus section, 3 layers) |

`basalt_reach` also holds 5x5x5 obsidian clusters of 98 + 73 + 25 blocks at x -32..-28 / 28..32, y 17..21, z -62..-58 / 58..62;
those are the board's cores, not monuments. The stored worlds are the committed exports (not re-stamped with `DC3`).

### 2.4 The 4-block one on Cedar Crossing

- Not recorded as a fault. Session 03 (`film/history/research/sessions/03-cedar-crossing-analysis.md`) quotes the model:
  "4 obsidian blocks 'sits at p10'" - i.e. unusual but inside the corpus, one of several properties that were each
  "defensible alone". The Cedar world is not under `maps/`, so no block count was taken here; the number 4 is the analysis
  session's. Note that four is over `DC3`'s three; whether the author counted Cedar's monument as a fault is not in the record.

## 3. The other faults of the trial-run boards

All from the same two sources: studio `705a77c6` (14 August 2026, 16:17 UTC) and mapgen `7107785c:ART-DIRECTION.md`
(14 August 2026, 16:17:40 UTC, deleted later). Both are the author's review of boards committed 14 August 2026.

| Fault | Board | Source and quote |
|---|---|---|
| Pitched roofs of slabs one can see through | `tallow-weirgate` (Opus run 2, ctw), six shed houses and its spawn | Studio `BACKLOG.md` `B168` at `705a77c6`: "A slab named as a roof material builds a see-through roof". "Six Weirgate shed houses set `roof: 126` (Wooden Slab) at `pitch: 1` with `roofSlab: -1`; its spawn sets `roof: 44:4` (Brick Slab) on a hip". Quoting `HouseStyle`: at a whole block of rise "a course of slabs leaves an open half between every pair and the roof can be seen straight through". ART-DIRECTION row: "A slab named in `roof` builds a roof you can see straight through." Also `quillon-barrow` roofs three houses in Grass Block (same entry). The one correct slab roof was Saltworks (below). |
| Spawn buildings far too large | `sable-marsh` (Sonnet run 2, ctw) | Studio `B157` at `705a77c6`: "A plan piece has no maximum size, so a wool room came out 30 x 30 and a spawn hall 90 x 15"; "`sable-marsh`'s wool rooms are 6 x 6 cells at cell 5 - 30 x 30 blocks - and its spawn piece is 18 x 3 cells, a 90-block hall." Author's rule: "**20 x 20 blocks maximum** for a wool-room piece and for a spawn piece, for now." |
| Spawn areas (ground under the spawn) far too large | `tallow-weirgate`, `tallow-mirefast` | ART-DIRECTION section 6 item 5: "Weirgate's `yard` is 80 blocks wide for a 20-block spawn; Mirefast's `steading` is 92." Also Mirefast "the 92-block spawn approach" (`B183`). |
| Houses too small | `tallow-weirgate` | `B167`: "eight of fourteen came out four blocks deep" (10x4, 9x4, ...). Rule: at least 5 x 5. |
| A huge hole across the middle that everyone walks round | `tallow-kilnrow` (Opus run 2, dtm/dtc) | Studio `B181` at `705a77c6`: "Kilnrow's `flue` subtracts `x -44...44` - 88 blocks of a 136-block board, 65% of its width - ... leaving two 24-wide side channels. Meanwhile `z -16...16`, where the two sides actually meet, is solid ground. **The hole is where the join belongs and the join is where the hole belongs.**" It led to the amendment of `approaches.md` (hole replaced by "a depression or a pond" on dtm/dtc boards). Note the review `review/tallow-kilnrow.md` calls the flue "bridgeable" ("about fourteen blocks across"), so "unbuildable" is the author's wording, not the review's. A second large hole: `basalt-reach`, "two large void channels cut with `subtract`" and "a void hole through the lower middle" (studio `B150`, `a12fd725`); its `channel` subtract is also described in mapgen `c8ce37f0`. The author's "unbuildable" hole is therefore Kilnrow or Basalt Reach; the record does not say which he meant. |
| Palette faults | `tallow-kilnrow` clashes, `basalt-reach` vanishes, `tallow-mirefast` checkerboards | `B183`: "Tallow Kilnrow clashes: `kiln-stack` is a `cell` over Quartz, Chiselled Quartz, White Clay, Smooth Sandstone and Light Grey Clay, with Red Sandstone two blocks away and a Red Stained Clay boulder in it." |

The author's "grundsätzlich einfach schlechte Maps" and "everything was the problem" (instalment ten) are his summary; the
repository's own summary of the same day is ART-DIRECTION's opening: "Twenty-one boards sit in this repository and the eye reads
most of them as one board."

### 3.1 The quartz board

- **Quillon Saltworks is confirmed as a quartz board**, and it is not Kiln Row: `quillon-saltworks`, Opus run 1, ctw,
  committed in mapgen `78c7e4d2` (2026-08-14 02:25 UTC). `BOARDS-BUILT.md` line 72: "a capture board on a salt pan, quartz
  pans stepping down to the brine". `review/quillon-saltworks.md`: "a working saltworks in white - quartz-and-sandstone pans
  stepping down to the brine, a black spoil bank raked across the flat, and the wool sheds standing at the two far corners
  of the works"; 168 x 168, `rot_180`, "four wools (two a team)", six themes. Its `salt-brine` theme is "white crust - a `cell`
  of white clay/quartz/smooth sandstone/grey clay over two sandstone, quartz rim"; the wool cage is "Quartz and dark-oak
  courses". Its own review's "What went wrong" is mild: "Nothing was dropped this time", "The pans are flatter than the
  heightmap suggests" (y9-11 over 3,169 cells), and the board "still ships as `<gamemode>ctw</gamemode>` ... only by accident".
- Saltworks is **not** the board with the faults above: the author's review names it as the one correct slab roof ("`quillon-saltworks`
  is the one board that builds a slab roof correctly", `B168`), and neither `B162`, `B157` nor `B181` names it. Its flaws in
  the review are the flat pan and the hard-coded gamemode label.
- **Correction to session 04's claim** that Kilnrow holds no quartz: `tallow-kilnrow` does ("quartz rim", `kiln-stack` "a `cell` of
  quartz / chiselled quartz / white clay / smooth red sandstone / light-grey clay", `review/tallow-kilnrow.md` lines 51-55;
  `B183`). Session 04's check read the intent JSON for the word, which the review text shows is not how the palette is stored.
  So both boards have quartz; the author's "probably Quillon Saltworks, not Kiln Row" fits the whiteness, but the faults he
  lists (hole in the middle, see-through slab roofs, oversized spawns) belong to Kilnrow, Weirgate and Sable Marsh, not Saltworks.
  Which one he had in mind is a question for him.

## 4. Not found

- The Aerie complaint itself (non-playable XML, odd-island wool rooms, bad zones): in no commit message, review, report or board entry.
- Any studio task or rule filed because of Aerie: none. The Aerie-citing commits (`d52dc1b1`, `7a681650`, `a12fd725`) fix other
  things and use Aerie as the measured example; none says it was found unplayable.
- A statement that Aerie's void rule makes every column outside the zones unbuildable: this note's inference (section 1.5), not a record.
- An Aerie wool room on "an odd island": none in the XML or review.
- Aerie's four build zones vs seven in the XML: unexplained.
- The Cedar Crossing monument as a fault, and the Cedar world's block count.
- A review document dated 13-14 August that first records the 27-block monuments; the first dated record is `705a77c6` /
  `7107785c` (14 August, 16:17 UTC), and the rule is `cf122593` (19 August).
- The deleted `ART-DIRECTION.md` is reproduced from `git show 7107785c:ART-DIRECTION.md`; `705a77c6` is a studio commit made
  the same minute.
