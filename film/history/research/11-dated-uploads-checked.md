# 11 — The dated uploads of June to October, checked against the public record

Research for the history. Subject: the fifth instalment of the author's account of 27 November 2026
(`../author-account-2026-11-27.md`, "dates the author read off the private repository and Discord"), a voice-transcribed
list of uploads from 24 June to 9 October. Read on 27 November 2026 from full-history clones of
`OvercastCommunity/CommunityMaps` (head `5a191d44`) and `OvercastCommunity/PublicMaps` (head `ebc8b708`), from
`pgm-studio` (head `5df92a35`, 14 November; 2,646 commits) and from `pgm-studio-mapgen` (its first commit is of
13 August, so it holds nothing before that), and from the saved listing of pgmstudio.de's maps of 26 November
(72 maps). Hashes are the first eight characters and are CommunityMaps' unless marked **(studio)** or
**(mapgen)**. Times are as committed, with the UTC equivalent where the day could shift. Every Ruediger commit below
has author `RuedigerLP` and committer `GitHub`, which is the web interface.

**How the search was made.** Every commit from 1 June to 31 October in both corpora was listed (202 in
CommunityMaps, 68 in PublicMaps) and every map the instalment names was read at the commit that added it and at head.
Head `map.xml` files were searched for model and tool names (`grok`, `claude`, `opus`, `gemini`, `haiku`, `mapgen`);
region and kit ids in the 24 June files were searched across both heads; the studio's history was searched for
`wallRun`, `wall run`, `bridgid` and `brittlebush`. Pull-request bodies could not be read (the session has no GitHub
API access to the repository), so what a pull request said is unverifiable here.

---

## The table

Status: **confirmed** (the public record holds the event on that day), **differs** (it holds it, on another day or in
another form), **unverifiable** (the public record cannot show it, so it stands on the author's account alone).

| Date (2026) | Event | Source | Status |
|---|---|---|---|
| 24 Jun 23:47 +0200 (21:47 UTC) | RuedigerLP adds three maps, `caadb19f` "Add: Vauxite, Capture the Wool CTW, Drastic Change II": `ctw/vauxite`, `ctw/capture_the_wool_ctw`, `ctw/drastic_change_ii` | public commit | **confirmed**; names resolved (§1) |
| 24 Jun | Their XML was made in the browser, the first maps on which he tried it | public traces + author's account | **traces found**, not proof (§1) |
| 1 Jul 22:53 +0200 (20:53 UTC) | `7d647015` "Vauxite: 1.0.1", the only Ruediger commit of 30 June to 3 July | public commit | **differs**: 1 July, not 2 July, and one map (§1) |
| 12 Jul | `<created>` of Bridgid II | public `map.xml` | recorded |
| 14 Jul 02:27 +0200 (00:27 UTC) | Bridgid II added: `a842b0bd`, five commits to 02:42, `ctw/bridgid_ii` | public commit | **confirmed**; the map is Bridgid II, not a Brittlebush map (§2) |
| 14 Jul 20:55 +0200 | `94be5e7e` **(studio)** adds `tools/seeds/traced/bridgid-ii.plan.json`, a plan traced from the map's world | public commit | extra: the studio traced it the same evening (§2) |
| 14 Jul | Its repeating side columns gave the wall-run pattern | author's account | **differs**: first `wallRun` is of 1 August; nothing links the two (§2) |
| 27 Jul 23:33 +0200 (21:33 UTC) | Kuusepuu CTC, "Capture the Cake prototype!", `8df2ca00` | public commit | **confirmed** (§3) |
| 28 Jul 01:10 +0200 (27 Jul 23:10 UTC) | Hello World Mini / Micro added, `591d21b1`; three revisions to 02:19; removed 12 Aug | public commit | **confirmed** (§3) |
| 6 Aug | Wandering U uploaded | author's account | **unverifiable**: in neither repository (§3) |
| 7 Aug 20:58 +0200 (18:58 UTC) | No Blocks Placed, `11a15f7d` | public commit | **confirmed** (§3) |
| 9 Aug 23:00 -0500 (10 Aug 04:00 UTC) | Cedar Crossing by arcadeboss, `a3de15d2` (#1366) | public commit | **confirmed** on 10 Aug in UTC; "AI map" confirmed by its credits, "first" **differs** (§3) |
| 12 Aug 23:20 +0200 (21:20 UTC) | Viridian and Thornwake, `37bdef57` | public commit | **confirmed** (§3) |
| 24, 25, 31 Aug | maps uploaded, private | author's account | **unverifiable**: no RuedigerLP commit in either repository between 12 Aug and 2 Sep |
| 2 Sep 02:18 +0200 (00:18 UTC) | Millrace 2.0.0, `c86226db`, and 2.0.1 two minutes later | public commit | **confirmed** (§4) |
| 13, 20 Sep | maps added, private | author's account | **unverifiable**: no RuedigerLP commit in either repository between 2 Sep and 19 Oct |
| 27 Sep 21:55 UTC | Delverdale and Whitstone Weald committed in this project, `d274c0ae` **(mapgen)** | public commit | the same boards the author names; the PrivateMaps upload of 27 and 28 Sep is **unverifiable** (§5) |
| 5-8 Oct | Four Countryside rows on pgmstudio.de (`rockymine-4`, `alphaboy98yt`, `-2`, `-3`, `-4`) | studio listing | recorded (§4) |
| 9 Oct | Alphaboy uploads Countryside | author's account | **differs**: loaded into CommunityMaps on 14 Oct 23:13 -0300 (15 Oct 02:13 UTC), `06138ebd` by Javggg (§4) |
| 11 Oct | "803" re-made in the browser (`rockymine-5`) | studio listing | recorded (§4) |
| 19 Oct 22:41 +0200 (20:41 UTC) | 803 2.0.1, `091b378d`, then 2.0.2 at 00:55 | public commit | **confirmed**: "later" is ten days after Countryside's studio rows (§4) |

---

## 1. 24 June and 1 July: three maps, and what the XML shows

**Resolved names.** The commit subject lists three maps, so "Walkside" and "Vauxite" are one map, **Vauxite**, and the
capture-the-wool map is **Capture the Wool CTW**, which is its title. The garbled "Drastic Change 2" is **Drastic
Change II**. Authors and contributors, read from the `map.xml` added in `caadb19f`:

| Map | Folder | Authors and contributors | `<created>` |
|---|---|---|---|
| Vauxite 1.0.0 | `ctw/vauxite` | author rockymine | none, then or since |
| Capture the Wool CTW 1.0.0 | `ctw/capture_the_wool_ctw` | author MishM0sh; contributor rockymine | none, then or since |
| Drastic Change II 1.0.0 | `ctw/drastic_change_ii` | author rockymine | none then; `2026-06-24` added by limefox3054 on 12 Sep (`e9a5ee8a`, "Drastic Change II: 1.0.1 (#1378)", who is credited "Remastered XML") |

**Record, the traces of browser-made XML.** Nothing in the three files says so in words: no comment, no generator
mark. Four things in them match what the studio's export wrote that week and match little else.

- **The kit.** All three carry a spawn kit with an arrow in slot 9, 32 stained clay in slot 10 and leather armour
  with `projectile_protection`. That is `TeamsGenerator.cs` **(studio)** as it stood on 24 June (`Item(9, "arrow")`,
  `Item(10, "stained clay", …)`). The studio moved the slots on 1 July (`f4ddf8b5`, task B18, "fix kit item slot
  placement"). `slot="10" material="stained clay"` occurs in no other `map.xml` at the head of either corpus.
- **Region ids.** Capture the Wool CTW and Vauxite name the rectangles of their build area `build-area-1`…`5` and
  its holes `build-hole-1` (four in Capture the Wool CTW, one in Vauxite). The studio's build-hole generator is of 15 June (`4421499d` **(studio)**, "Apply map symmetry by default: orbit-fill,
  team synthesis, build holes"). `build-hole-1` occurs in no other `map.xml` at the head of either corpus.
- **Plain ids.** Teams are `red` and `blue`, not `red-team` and `blue-team`, which the studio changed on 1 July
  (`f4ddf8b5`, B10; the board entry `f0284e08` says the bare ids were wrong against its template).
- **The numbered children.** Vauxite 1.0.1 has `blue-spawn-1`, `blue-spawn-2` unioned into `blue-spawn`.
  Numbered children of a union are what `44be1f44` **(studio)** (24 June, 23:27 +0200, "N10: multi-rectangle wool
  rooms + spawn protection (union)") made the generators emit, twenty minutes before the upload. The 24 June copy
  has a single `red-spawn` rectangle.

**Record, one file holds the export itself.** Vauxite's 1.0.1 commit also added `ctw/vauxite/region/map.xml`, a stray
copy still at head. It begins with `<?xml version="1.0"?>`, puts `<!-- rockymine -->` on a line of its own under the
author, and uses two-space indentation: exactly the `XmlWriter` output of `2a55eb06` **(studio)** (21 June, "a uuid
-> username comment under each author … on its own line"), before 1 July's `9fd6d6da` dropped the declaration and
moved to four spaces. It is labelled version 1.0.0, has the N10 unions and the new yaws, and its content matches the
root `map.xml` of 1.0.1 line for line. The root file is the same document reformatted by hand, with the comments back
on the author line.

**Record, what the second commit changed, which is the best evidence of "some errors".** `7d647015` has the message
"Vauxite: 1.0.1" and no more. Its diff (whitespace ignored) gives both teams a spawn yaw (the blue spawn had none; the
red had `180`, now `152.7`), replaces each single spawn rectangle with a two-rectangle union, adds
`<maxbuildheight>24</maxbuildheight>` and removes `<phase>development</phase>`. Capture the Wool CTW was never revised in the public
repository.

**Differs, 2 July.** The only Ruediger commit between 30 June and 3 July is `7d647015` of 1 July, 22:53 +0200. No
commit on 2 July by anyone adds a map. The author's "more maps added by Ruediger" may be a Discord date or a private
repository; the public record shows one.

**The studio that week.** 21 June: the XML export (`4463ca0a`, N06). 24 June, 00:46: "Configure export: protection
ordering, fractional points, spawn-anchored renewables, monument subtraction" (`129ad09b`). 1 July, 22:59: the board's
"XML conventions become the focus" (`f0284e08`), and the serialiser changes at 23:16 and 23:55.

## 2. 14 July: Bridgid II, and where the wall run came from

**Resolved.** The 14 July map is **Bridgid II** (`ctw/bridgid_ii`), as the author typed it and as the existing
correction in his account says. It is not a Brittlebush map. The commits, all RuedigerLP, committer `GitHub`, on the
night of 13 to 14 July: `a842b0bd` 02:27 "Bridgid II: added" (a lone `map.xml`), `fe035adf` 02:33 "Bridgid II: add
all files?", `ce45916a` 02:39 "Delete ctw/bridgid_ii directory", `5701b66d` 02:40 "Bridgit II: upload all files for
real this time i swear", `ae4d8f9e` 02:42 "Bridgit II: add dev-phase". The first upload put the folder in a
sub-folder; the author's "added" is the night of 14 July in Germany and the evening of 13 July in the Americas.
`map.xml`: authors rockymine and Ruediger_LP, `<created>2026-07-12</created>`, version 1.0.0, 64 players, includes
`water-lanes` and `iron-bulkcrafting`, four-space indentation with the author comments on the same line. Its XML has
no browser trace: the `red-team` ids and 4-space indent are the 1 July conventions, but those are also what hand-made
XML looks like in the corpus.

**Record, the map's picture.** The `map.png` uploaded with it (290 by 246 pixels) shows island sides in alternating
dark purple and grey vertical bands and a white-and-dark panelled tower. At that size nothing finer can be read.

**Record, what the studio did that week.** `8d898076` **(studio)** (12 July, 19:43 +0200, `<created>` day) added a
reference backdrop to the plan editor: "trace over a real map's top-down render". `94be5e7e` (14 July, 20:55 +0200)
added `tools/seeds/traced/bridgid-ii.plan.json`, 36 pieces over sixteen height tiers, as one of twelve traced real
maps. `docs/generator/rules.md` calls it "hand-carved". The studio names Bridgid II nowhere else except a corpus
golden and a test fixture (`AuthorIntentJsonTests.cs`: `"authors":["rockymine","Ruediger_LP"]`). Whether the map's
layout was made in the plan editor, as the account says, is not shown: the studio's traced plan is a trace *of* the
map, made after it was uploaded.

**Differs, the wall run.** The first mention of a wall run in the studio is `492d20d4` **(studio)** (1 August, 12:17
UTC, "Note surface layering, bucket toggles, and patterns (G157)": "layered or map-wrapping vertical wall runs"). The
first identifier is `WallRun` in the design commit `e2c6b688` (13:18 UTC) and the first code is `WallRunMaterial` in
`18d2c8ce` (16:43 UTC, "Build terrain-paint patterns and the theme JSON (G157, TP13)"): "N stripes of any widths
that repeat along the void-facing perimeter". That is eighteen days after Bridgid II. No commit message, document or
test names Bridgid II or Brittlebush in connection with it, and none of the three says where the idea came from.
`wallRun` never occurs in this repository (`pgm-studio-mapgen` opens on 13 August). The link to Bridgid II's side
columns is the author's account alone, and not contradicted by the picture above.

## 3. 27 July to 12 August

**Capture the Cake.** `8df2ca00`, Monday 27 July 23:33 +0200, "Kuusepuu CTC: added", body "Capture the Cake
prototype!", `arcade/standard/kuusepuu_ctc`. Authors rockymine, DerStiv and "Claude Opus 5" ("CTC conversion");
contributor Ruediger_LP ("XML"); `<created>2026-07-27</created>`. Revised at 01:09 and 02:19 on 28 July and on 31 July.

**Hello World Micro.** The author's "tested briefly" cannot be read. `591d21b1`, 28 July 01:10 +0200, subject "Hello
World Mini: added", body "grey map for concept test", folder `ctw/hello_world_micro`; `fb0013e1` 01:30 "Hello World
Micro", body "add actual map, still rly grey though"; `04e61f88` 01:48 "Hello World Micro: update 1.0.1", which also
added `hello-world-mini.plan.json`; `b4ef98e9` deleted that file at 01:58; the folder went on 12 August at 23:15
(`067c82cc`). Author rockymine alone; no `<created>`. **The plan file is a trace of the browser tool**: it opens
`{"plan": 1, "meta": {"name": "Hello World Mini"}, "globals": {"cell": 5, "symmetry": "mirror_z", …}, "pieces": […]}`,
the studio's plan format. The 1.0.1 XML is the map in which "a per-game roll decides whether you need 1 or 2" wools and
the wool box is recoloured, so the wool room that changes colour is Hello World Micro, as the instalment says.

**6 August, Wandering U.** In neither repository, at any commit, under any folder. The author's account alone, and
research `10` read the file he supplied.

**7 August, No Blocks Placed.** `11a15f7d`, 20:58 +0200 (18:58 UTC), "No Blocks Placed: added", folder
`ctw/no_blocks_placed`. The commit body reads "Irongate Harbour remove dev phase", which names no map in this
history. Authors: rockymine "Drawing pieces, shapes, and markers in the browser.", Ruediger_LP "Wisdom.", Flamiix
"Minimalist." There was no `<created>` in the first commit; TTtie added `2026-08-07` on 15 August
(`f17a371a`, 04:56 +0200), and `ff115048` (Ruediger, 13:49) added `<clear/>` to the spawn kit. It is the first
`map.xml` of the window that says its pieces were drawn in the browser.

**10 August, Cedar Crossing.** `a3de15d2`, committer `GitHub`, author **arcadeboss**, pull request #1366, "Cedar
Crossing - Initial Version", Sunday 9 August 23:00:13 -0500 (10 August 04:00:13 UTC, 06:00 in Germany): the author's
10 August holds in UTC. Folder `dtcm/cedar_crossing`, destroy the monument, version 1.0.0. Credits: arcadeboss
("7,000 word essay"), **"SuperGrok" ("Map and XML")**, and a second human uuid ("Map suggestions"); `<created>`
`2026-07-27`. That credit is the only place the map is described as AI-made: the commit messages (`#1366`,
"Updates from play testing" `75d4eab1` of 13 August) say nothing, and the pull-request text could not be read.
**Differs, "the first AI map there":** Kuusepuu CTC, credited "Claude Opus 5", is thirteen days earlier. What holds is
that Cedar Crossing is the first map by an uploader other than Ruediger that credits a model, and the first that
credits Grok.

**Other 2026 maps by the same author.** arcadeboss has committed to CommunityMaps since May 2023 (192 commits to
27 November 2026, 28 of them from August on, among them Black Betty, Bed Rush, Tom Brady and Battleline), so he is no
newcomer. In 2026 he added:

| Date | Map | Credit to a model in head `map.xml` |
|---|---|---|
| 25 Apr | Badger Dream, `db703b08` | none; author minuyo |
| 9 Aug | Cedar Crossing | "SuperGrok" |
| 27 Aug | Fire on the Mountain, `279c06e2` | "GrokBuild", author |
| 8 Sep | Alligator Charge, `cf87a560` | "GrokBuild" (XML), "Grok Imagine" (logo), "Gemini" (swimming speed matrix) |
| 25 Sep | Nether Run, `48e2dc3e` | "GrokBuild" (world generation) |
| 24 Oct | Sanctum Veil, `0bbfcc6c` | "GrokBot", author |
| 7 Nov | Blocker, `a081ce5e` | "GrokBot", author |
| 13 Nov | Xavier's Estate (now Xavier's Mansion), `a4ffc13a` | a model name present at head |
| 15 Nov | Hot Potato, `42a11bb1` | "Grok Bot", "Grok Build" |
| 19 Nov | Fireball Jump, `1090dc32` | none in the credits |

Twelve head `map.xml` files in CommunityMaps credit a model; the earliest is Kuusepuu CTC; eight are arcadeboss's
(Cedar Crossing to Hot Potato) and four this project's (Kuusepuu CTC, Millrace, Thornwake, Viridian). Research `06` says that
every AI-made map was committed by Ruediger; it holds for this project's maps and not for these.

**12 August, Viridian.** `37bdef57`, 23:20:57 +0200 (21:20 UTC), "Add Viridian and Thornwake", body "Two new maps made
by fellow human humans, for great enjoyment of humanity!" Folders `ctw/viridian` (author "haiku") and `ctw/thornwake`
(author "mapgen"), both `development`, neither with a `<created>`. The author's "a lot happened" holds: five minutes
earlier Hello World Micro was deleted, and 13 August brought Cedar Crossing's update. The author calls Viridian "in
CommunityMaps"; it is in `ctw/`.

## 4. 2 September to 19 October

**2 September, Millrace.** `c86226db`, 02:18:07 +0200 (00:18 UTC), "Millrace 2.0.0", body "Human improved version
:robot:"; `21b6d9b8` 02:20 "Millrace 2.0.1". Folder `dtcm/millrace`, destroy the monument; authors rockymine ("layout,
terrain, block palette, beautification"), Ruediger_LP ("interior design, houses, beautification"), "Opus 5"
("layout composition, initial draft, sculptures, bridges"); `<created>2026-08-30</created>`. No earlier version is in
the repository: the "reworked" Millrace came into it as 2.0.0.

**Countryside.** The public commit is `06138ebd`, **14 October 23:13:48 -0300** (15 October 02:13 UTC), author and
committer Javggg, message "load countryside by alphaboy", folder `ctw/countryside`. `<created>2026-10-06</created>`,
phase `staging`, author **Alphaboy98yt** (the author's "Alphaboy"), contributors rockymine and limefox3054 ("Remastered
XML"). A later commit by Sam (`da94a699`, 9 November) changes its buildable area. The record has nothing on 9 October:
the date differs by five days, and the upload to Discord or to a maintainer is not in a repository. The committed
XML is `proto 1.5.1` with a five-second spawn resistance and `<half>` regions, the maintainer's remaster; the
browser-made XML is not what was committed.

**Record, what the studio holds of it.** The saved listing of 26 November has Countryside five times, all with author
Alphaboy98yt, `agentMade` false: `rockymine-4` (5 Oct 21:35 UTC), `alphaboy98yt` (22:42), `-2` (22:56), `-3` (23:13),
`alphaboy98yt-4` (8 Oct 19:22), and two rows by "Claude Code" that traced it (`countryside-plan`, `countryside-props`,
6 Oct 01:03 and 01:27 UTC). A slug is the last segment of the link a world was fetched from, suffixed past one taken
(`WorldUrlImport.NewAsync`), so the slug names a download link, not a person; the listing's `youWroteAt` is relative to
whoever fetched it and is set on `rockymine-4`, `alphaboy98yt-4` and `rockymine-5` and not on the three others. That
is consistent with Alphaboy having imported and configured it himself on 5 October and with the author having
imported it too; it does not decide who did. The date `<created>2026-10-06` is the day on which the `alphaboy98yt` row was last
updated, counted in German time (22:42 UTC on 5 October is 00:42 CEST on 6 October).

**803.** `091b378d`, 19 October 22:41:06 +0200 (20:41 UTC), "803: 2.0.1", and `d9cf9c6d` at 00:55 on 20 October;
Sam added `maintain dev phase` on 21 October. Folder `ctw/803`; author minuyo, contributors rockymine ("clicking some
buttons (XML)") and Ruediger_LP ("XML"); no `<created>`. The map is old: `44241314`, 29 September 2024, added by
Ruediger. The listing has it as `rockymine-5`, "803", minuyo author, rockymine contributor "clicking some buttons",
last updated 11 October 20:33 UTC. **The XML bears the studio's mark of that date**: 2.0.1 contains `reset-resistance-kit`
(`force="true"`), a `not-spawns` region and `only-red`/`only-blue` filters, which `31274925` **(studio)** (11 October,
23:06 UTC, "Configure's map.xml follows the reviewer") removed three hours after the listing's last write. The map was
exported from the browser before that commit and uploaded eight days later. "Two maps by others so far" holds in the
public record: Countryside, and 803, which is minuyo's.

**The feature.** What lets a person bring a world and draw regions on it is the Configure tool's import. Its history:
`09951fb7` **(studio)** (17 June, "B8: import-from-url endpoint with SSRF + zip safeguards"), the `/maps/new` landing
(`ae2038b0`, 17 June), URL import wired into Configure on 23 June (`36529987`, which also made slugs unique), and
"Re-import a world into the map it was imported from" (`29f96303`, 6 October 01:45 UTC), the day after Countryside's
rows. Its document is `docs/tools/configure.md`, "Import — phase zero": a download link fetched server-side from an
allowlisted host and extracted `region/*.mca` only. It is **a link, not an upload from the browser**. Public sign-in
began 26 to 28 September (`f7587f86`, `31033891`), so Countryside's rows of 5 October come about a week after the site opened. The
export stopped crediting the studio as a contributor on 9 October (`a4417f4e`).

## 5. What the public record cannot show

- 24, 25 and 31 August; 13 and 20 September: maps "uploaded", private. No RuedigerLP commit to either corpus falls
  between 12 August and 2 September, or between 2 September and 19 October.
- 27 and 28 September: Ruediger adding to PrivateMaps. **Whitstone is Whitstone Weald**, a destroy-the-monument board
  by Opus 5.5; Delverdale is Opus 5.5's capture-the-wool board. Both were committed in `pgm-studio-mapgen` at 21:55 UTC
  on 27 September (`d274c0ae` **(mapgen)**, "two large boards for a 32-a-side play test") and are on the deployed
  studio (`whitstone-weald` last updated 28 September 08:05 UTC, `delverdale` 2 October). Neither is in a public map
  repository.
- 6 August (Wandering U), the test of any of these maps, who played, and what any pull request said.

## Corrections this makes

- The account's "Bridget": Bridgid II, as already corrected.
- "Hello World Micro (the wool room that changes colour)": holds.
- Research `06`: "every AI- or studio-made map … was committed by RuedigerLP" holds for this project's maps, not for
  arcadeboss's Grok maps, the first of which is Cedar Crossing.
- 2 July: 1 July, one map. 9 October: 14 October in the repository.
