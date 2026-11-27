# 07 — PublicMaps, the Base maps, the bedrock box, "made by", and the two game-mode experiments

Research for the history. Subject: the last four bullet points of the author's account of 27 November 2026
(`../author-account-2026-11-27.md`), which were added later that day and had not been checked. Read on 2026-11-27
from a full-history blob-less clone of `OvercastCommunity/PublicMaps` (2,079 commits on all refs, head `ebc8b708`
of 25 November, branches `main` and `tdinc`), the CommunityMaps clone of research `06`, `pgm-studio` (all refs,
head of `main` `5df92a35` of 14 November), `pgm-studio-mapgen` (this repository) and the three early repositories
under `rockymine/`. Hashes are marked **(PM)** PublicMaps, **(CM)** CommunityMaps, **(studio)** pgm-studio,
**(mapgen)** this repository. Times are the committers' own.

**The private maps repository the author names could not be read.** No clone, mirror or reference to it exists on
this machine, and nothing below speaks for what it holds.

---

## 1. Did the tests go to PublicMaps?

**How the search was made.** Every PublicMaps commit from 1 June to 27 November 2026 (73) was listed with author,
committer, message and changed files. Authors were searched for Ruediger, RuedigerLP, rockymine, michael, TTtie and
Flamiix; messages for ai, slop, test, studio, generat, claude, opus and mapgen; every `map.xml` at head for opus,
claude, sonnet, haiku, fable, mapgen, pgm-studio, gemini and grok; and the 288 world folder names in this
repository's `maps/INDEX.md` against every directory name PublicMaps has ever held.

**Record.** No AI-made or studio-made map entered PublicMaps between June and November 2026. The searches return
nothing: no message matches except `daca27a3` **(PM)** "Move brady_block (for testing)" by Christopher White on 29
August, a move of BT's Touchdown map; no `map.xml` at head names a model or the studio; no board name of this
repository is a PublicMaps folder.

**Record, who committed.** Fifteen people committed in the window: 3li, Antnecb, BT, Christopher White, Dylan, Javg
/ Javggg, Mitchell Thomas, Pugzy, Sam, TTtie, arcadeboss, jex, limefox3054 and technodono. Ruediger's last commit to
PublicMaps is `bda87b5a` **(PM)** "Aequabilis", 25 February 2025. rockymine and Flamiix never committed there.
TTtie's seven commits in the window are to Ping Bomb II (3 June), Chinatown and Block Runner Classic ("Drop a few
grass patches", Sunday 20 September, `46f7e53f`), Touchdown (2 October), King's Conquest (14 November) and Directrix
(25 November) — none an AI map.

**Record, the maps that did arrive.** The new maps of the window are six by Obelistics moved over by BT (16 June),
Radiant (technodono, 22 June), Nucleus (Sam, 10 July), Outcrop, Cottage and Arch by Dowly_ (limefox3054, 7 August),
Brady Block (BT, 17 August) and Strikezone (Javggg, 3 November). Each credits people.

**Record, 27 September 2026.** PublicMaps has no commit that Sunday. The nearest are `f973e60e` **(PM)** (Hoodoo's
licence file, Saturday 26 September, +0900) and `0be7ca7a` **(PM)** (BT's Touchdown, Wednesday 30 September).

**Batches of about fifteen.** No public repository holds a batch of that size. CommunityMaps' four batches carried
one or two maps each (research `06`). The two batches of this project that come near the number are its own: the
fifteen `tools/mapgen` boards of 11–12 August (eleven Opus 5, four Haiku 4.5; HISTORY chapter 4), and the play test
prepared on 27 September, two large boards beside "the eleven small boards in the same play test", thirteen in all
(`reports/whitstone-weald.md`; research `06` §b).

**Inferred.** The summer tests are in CommunityMaps and the autumn ones are in neither public repository. If the
September test boards were loaded from a repository, it was the private one. The record cannot confirm that.

| Date | Weekday | Committer | Hash | Message | Maps | Removal |
|---|---|---|---|---|---|---|
| — | — | — | — | No AI-made map in PublicMaps, 1 June – 27 November 2026 | — | — |
| 2026-09-26 (+0900) | Sat | limefox3054 | `f973e60e` **(PM)** | Hoodoo: update license file extension (#125) | `dtcm/hoodoo` (not AI) | — |
| 2026-09-27 | Sun | — | — | no commit | — | — |
| 2026-09-30 (−0700) | Wed | BT | `0be7ca7a` **(PM)** | Touchdown: use flag capture actions | `includes/touchdown.xml` (not AI) | — |

## 2. The "Base" maps

**Record.** The three are the studio's `base-*` seeds, committed to `pgm-studio` on Thursday 2 July 2026 by Claude
Opus 4.8. Their map names are **Base 2-Island**, **Base 2-Wool** and **Base 4-Team** (`meta.name` in each
`*.intent.json`). Spoken aloud, "Base 2-Wool" and "Base 4-Team" are close to the "Base to Rule" and "Base for Teams"
the author recalls; that reading is inferred from the sound, and the record holds no other map named Base.

| Date (UTC) | Weekday | Committer | Hash | Message, verbatim | Map | Removed |
|---|---|---|---|---|---|---|
| 2026-07-02 07:43 | Thu | Claude (Opus 4.8) | `c6b0fd89` **(studio)** | Add base 2-island CTW test seed | Base 2-Island: two distorted-H team islands mirrored `rot_180` and a raised centre square, 1 cell = 5 blocks, island heights 9 and 13, observer at y 24, build to 20 | still at head (`tools/seeds/`) |
| 2026-07-02 10:04 | Thu | Claude (Opus 4.8) | `b89cef45` **(studio)** | Test: drive the base 2-island seed through the export pipeline | asserts "bedrock-floored islands, spawn/wool cubes resting on the terrain surface" | — |
| 2026-07-02 11:13 | Thu | Claude (Opus 4.8) | `2770c485` **(studio)** | Add 4-team (rot_90) test seed | Base 4-Team: the same unit fanned by `rot_90` into four arms, each spawn cube holding three monuments | still at head |
| 2026-07-02 11:21 | Thu | Claude (Opus 4.8) | `febb21ce` **(studio)** | Add 2-team x 2-wool test seed (H with centre spine) | Base 2-Wool: an H with the spawn on the crossbar and a wool on each arm, two wools a team | still at head |
| 2026-07-02 22:47 | Thu | Claude | `e09959cb` **(studio)** | G16 + G17: plan schema, validator, compiler + the three seed plans | each seed gains a `*.plan.json` | — |
| 2026-07-15 → 09-01 | — | Claude, rockymine | `7ead71cf` … `b02f58d7` **(studio)** | eight resyncs as the plan and layout schemas changed | all three | — |

**Record, what a Base map was made of.** The seeds were the first boards driven through the sketch world-folder
export, which shipped the same morning (`5d75520d` **(studio)**, "P9 sketch world-folder export shipped"). Its
contract, written the night before, makes the world exactly as the author describes: "y = 0 layer = bedrock (id 7)",
the solid span above "= stone (id 1)", islands at their own heights, and "Both the wool cage and the spawn cube are a
hollow 8×8×8 bedrock shell" (`docs/contracts/sketch-world-export.md` at `08870c54` **(studio)**, 1–2 July). The
first seed's commit records it "Validated end-to-end: the export ZIP decodes to the expected terrain + cages + spawn
cubes + auto-wired monuments + observer boards". The README calls Base 2-Island "The most basic CTW design: two
team islands + a contested centre".

**Record, before the Brittlebush layout.** The Base seeds are of 2 July. Brittlebush's style was read and written
as a grammar on 9 October, and Brittlebush III's layout was drawn on pgmstudio.de, which went public on 28
September (HISTORY chapters 7–8). The author's order holds.

**Record, first of its kind.** No studio world with terrain and structures exists before these: the export they
exercised did not exist until that morning. The Python studio's exports of June (`pgm-map-studio`, 7 June) and
`MinecraftLayoutEditor`'s schematics of October 2025 hold no seed or map named Base; neither early repository, nor
`CTW-Layout-Generator`, contains the word in a map name. Neither CommunityMaps nor PublicMaps holds a Base map: their
only "Base" maps are Research Base, Space Base and Factorio Gridbase, all by other authors and years older.

**Silent.** That the layouts were drawn on squared paper. The record holds coordinates, a five-block cell and the
shapes ("a distorted-H team island"), which fit a drawing on a grid, and a model as the committer; no drawing,
photograph or message from the author. Also silent: whether any Base map was loaded on a server or played.

**Related, and also grey.** Hello World Micro (section 5) is the same kind of world four weeks later: a plan with
pieces at surfaces 9, 11 and 13 on a five-block cell, uploaded as a "grey map for concept test" (`591d21b1`
**(CM)**) and "still rly grey" (`fb0013e1` **(CM)**). Its wool box is a cuboid eight blocks across
(`-49,25,-39` to `-41,30,-31`), which fits the 8×8 shell; that it is the stamped bedrock shell is inferred.

## 3. The bedrock box as the default room

**Record, since when.** The shell was specified on 1 July 2026 in the export contract (`224f6d4b`, `7e98fa84`
**(studio)**, Claude Opus 4.8): eight courses of bedrock, a 4×4 hole in the roof, a coloured band at the fourth
course, glass-pane doors on the wool cage and one open 4×4 door on the spawn cube. It was first built as code at
00:28 UTC on 2 July, "P9d: shared 8x8 cube-shell emitter (wool-cage + spawn-cube variants)" (`638f2136`
**(studio)**). The author's task that asked for it, filed 30 June, named "spawn and wool-room cages" and monument
pedestals of "bedrock block · air block · stained-glass cap" (`a7ef70ab` **(studio)**).

**Record, where it lives now.** `HouseStyle.Wool` and `HouseStyle.Spawn` in
`src/PgmStudio.Minecraft/Houses/HouseStyle.cs` (lines 602–612 at `5df92a35`): "The shipped wool structure: a flat
bedrock shell, a wool band at the fourth course, a light slit at the sixth, and a stained-glass-pane door", and the
spawn "the same shell with a stained-clay band, and an open doorway". `SpawnStructureStamper.Shell` and
`WoolStructureStamper.Shell` default to them. The Theme phase's room select reads "Bedrock box" where nothing is
bound (`SketchThemeInspector.razor.cs`).

**Record, the default and the complaint.** A map's rooms could be bound to a library style from 5 August
(`bd26aaf6`, `bc657e71` **(studio)**). An unbound room still stood in the bedrock box, silently, until Sunday 27
September at 17:53 UTC — the day of the play test's preparation — when `eb53beb7` **(studio)** "WE140: a room left in
the built-in shell is complained of" made every build answer rule `WX14`, "A spawn room or wool room has no house of
its own" (`src/PgmStudio.Domain/RoomFrames.cs`). `docs/world-export/structures.md` states it: "The bedrock box is a
placeholder, and the build says so". It is a complaint, not a refusal, so it still builds.

**Record, the boards whose reviews say the room was left in it.**

| Date (file added) | Board, model | What the review says | Source |
|---|---|---|---|
| 2026-08-14 | Ashen Quarry | "`roomStyles.spawn` was left unbound through every build above, and an unbound room stamps the built-in shell — a bedrock lid" | `review/ashen_quarry.md` (mapgen `644b383f`) |
| 2026-09-12 | Sable Reach, Sonnet 5 | the wrong key `roomStyles.cage` "answered a 200 … and the wool room built in the studio's own default shell rather than mine — a silent miss" | `review/sonnet5-sable-reach.md` (mapgen `f8593017`) |
| 2026-09-12 | Heftfold, Opus 5 | "the board stored at 200, exported at 200 and built its wool rooms as bedrock boxes — `column?at=-45,75` read `y24 Bedrock · y16 Bedrock`"; `showcase/16-forest` carried the same key | `review/opus5-heftfold.md` (mapgen `fc91b3be`) |
| 2026-09-21 | Kilnbrow, Hallowgate and a third board, Opus 5 | "a board can carry a designed house row and still leave those on the default, which is what the first pass of all three did" | `BOARDS-BUILT.md`, "Opus 5 — four boards, one per game mode"; `review/opus5-kilnbrow.md` (mapgen `26215360`) |
| 2026-09-22/23 | five boards, Opus 5.5 | "every one still wears the studio's grey fill and the built-in bedrock box for its rooms, because theming is the next stage" — left on purpose, before paint | `BOARDS-BUILT.md`, "Opus 5.5 — two boards shaped with the author, three nano boards" |

**Inferred.** The author's account holds: the box was the first room the studio built, it stayed the default after
styles existed, and at least three runs between August and September left a spawn or wool room in it without
meaning to. Two of the three were a misnamed key, `cage` for `wool`, which the studio accepted silently; the warning
that names the box came on 27 September.

## 4. "Made by" and nothing

**Record, the uploaded maps all name someone.** Every AI or studio map in CommunityMaps carries an `<authors>`
entry: Hello World Micro rockymine; Kuusepuu CTC rockymine, DerStiv and "Claude Opus 5"; No Blocks Placed rockymine,
Ruediger_LP and Flamiix; Thornwake "mapgen"; Viridian "haiku"; Millrace rockymine, Ruediger_LP and "Opus 5" (each
`map.xml` at its upload commit, **(CM)**). None of those showed "made by" and nothing.

**Record, where "made by" and nothing was.** On the boards built through the studio, the observer platform carries
an info board whose sign begins "made by" in italics over the authors (`ObserverPlatformStamper.cs`, line 109). On
Friday 4 September `4ffd2f1a` **(studio)** recorded the problem and removed it: "The authors sign is left off where
the map names nobody — 69 of those 74 carried 'made by' over three blank lines, which reads as a map whose author is
called nothing. EX6 states the omission rather than leaving it merely visible." The 74 are the boards then under
this repository's `specs/`. Rule `EX6`, "A map has no author", is in `MapExportComposer.cs`.

**Record, the base of it.** The seeds the studio began from state `"authors": []` (all three Base seeds), and this
repository's `tools/README.md` still notes that "a compiled intent leaves it empty". On 12 August `a0c17c8f`
**(studio)** found the writer emitting `<author uuid=""/>` for a person without an account, which PGM refuses to
load.

| Date | Weekday | Hash | What changed |
|---|---|---|---|
| 2026-07-02 | Thu | `c6b0fd89` **(studio)** | the first seed, Base 2-Island, with `"authors": []` |
| 2026-08-12 | Wed | `a0c17c8f` **(studio)** | "An author is an account or a name, and an empty uuid is neither" |
| 2026-08-30 | Sun | `f64d76e1` **(mapgen)** | "A drawn spec states its own authorship" — Millrace's spec carries authors in its intent's meta |
| 2026-09-04 | Fri | `4ffd2f1a` **(studio)** | the "made by" sign is left off a map with no author; `EX6` complains; 69 of 74 specs named nobody |
| 2026-09-27 | Sun | `c8641cd6` **(mapgen)** | "Delverdale and Whitstone Weald credit Opus 5.5" — the two large test boards credited after midnight local |
| 2026-09-28 | Mon | `00e6f179` **(studio)**, `336a30d1` **(mapgen)** | WE145: every export credits "PGM Studio (pgmstudio.de)", and the tree builder; re-driven on 109 boards |
| 2026-10-09 | Fri | `e93de260` **(mapgen)** | the studio's self-credit dropped from 120 boards; on 70 it had been the only contributor |
| 2026-11-27 | Fri | — | 48 of the 276 worlds under `maps/` have no `<author>` element at all: freeform boards, the Thunder reconstructions, Haiku and Grok trials, biome tests and older specs |

**Differs.** The author places the "Made by" in the tab list. The record's "made by" is the sign on the observer
platform, the first thing a player sees on joining. What PGM shows in its tab list for a map with no authors was not
checked: PGM's source is not on this machine.

**Silent.** Which authorless maps were played on the server, and the joke itself; neither appears in any commit or
file.

## 5. Capture the Cake and Hello World Micro

**Record, Capture the Cake.** Kuusepuu CTC, committed by RuedigerLP on Monday 27 July at 23:33 (+0200), message
"Kuusepuu CTC: added", body "Capture the Cake prototype!" (`8df2ca00` **(CM)**). Its objective: "Eat the ENEMY cake,
carry it home, and place it on your own monument." Its header says it is "the DTM map with the destroyables removed
and the cake objective of capture_the_cake_ctw dropped in", credits "CTC conversion" to Claude Opus 5 and "XML" to
Ruediger_LP. It was revised three times that night and the following Friday; 1.0.3's body is "fix respawning with
cake" and its comment "Reported live" (`d73e7040` **(CM)**). It is still in `arcade/standard/kuusepuu_ctc`. The map
`capture_the_cake_ctw` it took its objective from is in no repository on this machine.

**Record, Hello World Micro.** Uploaded the same night as "Hello World Mini: added — grey map for concept test"
(`591d21b1` **(CM)**, Tuesday 28 July 01:10), renamed Micro twenty minutes later. The world came from a studio plan,
`hello-world-mini.plan.json`, `"plan": 1`, `mirror_z` symmetry, a five-block cell and pieces at surfaces 9 to 13; the
plan file was added in 1.0.1 (`04e61f88`) and removed ten minutes after (`b4ef98e9`). Credits name rockymine alone.
The map was deleted on Wednesday 12 August (`067c82cc` **(CM)**). (Research `06` places the plan file in the first
commit; it arrived in the third.)

**Record, the wool room.** The record's wool room does not move; it changes colour. Version 1.0.0 had two wools a
team, "the second appears once you take the first!". Version 1.0.1 rolls 1 or 2 at match start (`floor(random() *
2) + 1`), and when a team takes its first wool, `<fill>` actions recolour the enemy's box, wool and glass panes, to
the second wool and announce "Wool Room Switched". The fills touch only wool and panes, "leaving air and everything
else alone".

**Differs.** The author remembers a moving room that players fell out of. No version in CommunityMaps moves a room
or removes a block a player could stand on. A moving version may have existed elsewhere — the private repository,
the server's own copy — and the record cannot say.

**Silent.** That the layout was AI-made (the plan's piece ids, `piece`, `piece-2` … `piece-8`, are the editor's
defaults, and no credit names a model); that it was tested once; and that players fell out of the world. No commit
reports a Hello World Micro test.

## 6. Summary

| Claim (author, 27 Nov) | Verdict | Where |
|---|---|---|
| Tests may have gone to PublicMaps | **Differs**: none did, June–November | §1 |
| Tests may have gone to the private repository | **Silent**: cannot be read | §1 |
| Last test 27 September | **Holds** as a preparation date, in this repository only | §1; research `06` |
| Batches of about fifteen | **Holds** for this project's own batches (15 on 11–12 Aug, 13 on 27 Sep), not for any public upload | §1 |
| Base maps, about three, stone with heights, bedrock floor, bedrock boxes | **Holds**: Base 2-Island, 2-Wool, 4-Team, 2 July | §2 |
| Drawn on squared paper | **Silent** | §2 |
| Before the Brittlebush layout | **Holds** | §2 |
| The bedrock box stayed the default; agents left spawns unstyled | **Holds**: default since 2 July, complained of from 27 Sept, missed in at least three runs | §3 |
| No AI map had an author; "Made by" and nothing | **Holds** for the studio boards (69 of 74 on 4 Sept), **differs** for the uploaded six, and the "made by" was a sign | §4 |
| Capture the Cake an XML experiment | **Holds**: Kuusepuu CTC, "Capture the Cake prototype!" | §5 |
| Hello World Micro's room moves; players fell out | **Differs**: the room recolours; the fall is in no record | §5 |
