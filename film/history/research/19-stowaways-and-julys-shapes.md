# 19 — Stowaways, Agrostid, and July's shapes, checked against the record

Research for the history film. Scope: the author's twenty-fifth instalment (28 November 2026,
`../author-account-2026-11-27.md`, cited as account §25) and the six pictures with it (`../sources/july-2026-shapes/`,
whose README transcribes the four chat screenshots), checked on 28 November 2026 against these local clones:
`/home/user/rockymine/MinecraftLayoutEditor` (all branches), `/home/user/rockymine/ctwanalysis` (63 branch refs,
searched on all), `/home/user/rockymine/pgm-studio-mobile` (3 commits), `/home/user/pgm-studio` (all branches) and the
two public map repositories `/home/user/OvercastCommunity/PublicMaps` (2,079 commits) and
`/home/user/OvercastCommunity/CommunityMaps` (4,258 commits; its working tree is not checked out, so it was read
through `git ls-tree` and `git show`). Neither map clone is shallow. The `#maps-changelog` feed
(`../sources/maps-changelog/maps-changelog-2026.csv`) and the match chart note
(`../sources/early-experiments/2026-ctw-match-activity.md`) were read for the same names. All six pictures were looked at.

Times. Commit times are author dates in the zone the commit records; Claude web sessions commit in `+00:00`. The chat
screenshots show the author's clock, German summer time (UTC+2), and are converted where they are set against a commit.
The sketch files carry 8 July 2026, 23:43 in their names; the zone of that stamp is not recorded.

Limits. PrivateMaps is not readable here beyond its feed. No world file was opened: region files are named and sized
from the git trees, and where a map's extent is given it is the extent of the coordinates its `map.xml` states, not of
its blocks.

---

## 1. Agrostid, not Annealing, on 6 November 2025

**The importer's commits name no map, so the record cannot say which world was imported first.** `d2c4bc3` (2025-11-06
03:20 +01:00, `michael`, "working import of .leveldat and .mca files (claude & grok)") adds `WorldImporter.cs` (621
lines) and a `LoadWorldFiles` handler; `9d72ca6` (20:35 the same day, "clean up code") and the merge `084a4ed` follow.
No commit message, file, test world or string in any commit of any branch names Agrostid or Annealing
(`git grep` over `git rev-list --all`). The repository ships no world.

**The picture of that day holds two numbers that fit Agrostid and no Annealing map.** *Record:* the screenshot
(`../sources/early-experiments/2025-11-06-layout-editor-world-import.png`) shows Width 184 and Height 267, mirroring on,
and "5 Dateien ausgewählt" under the world import. In `d2c4bc3` an import sets the layout's width to twice the largest
distance of a block from the blocks' mean x, plus 64, and the height the same way on z. *Inference:* Agrostid's
`map.xml` states coordinates out to |x| = 60 and |z| = 102, which gives 184 by 268; the five Annealing maps state
|x|,|z| of 58/53 (Annealing), 97/139 (II), 85/72 (III), 115/115 (IV) and 101/26 (II Short), none of which gives 184 by 267.
Block extents can differ from the XML's, so this supports the correction without proving it.

**The author's correction stands against his earlier account; the record does not contradict it.** *Account:* "The
first map imported in the browser tool was not Annealing but Agrostid" (account §25), replacing "he tested world import
on Annealing" (account §18).

**Agrostid is in PublicMaps, created 2015, and its region files hold the history he describes.** *Record:*
`PublicMaps/ctw/agrostid/map.xml`, version 3.0.4, `<created>2015-04-26</created>` with the comment "2.0.0 edit
2024-10-03"; authors rockymine and Matci0B, Ruediger_LP credited for XML; a Christmas variant "Agrochion" of
2024-08-15. Its regions sit around 0,0: spawns at z ±72 to ±102, wool rooms at x ±46 to ±60. Until October 2024 the map
lived in a single region file, `r.-2.-1.mca` (x −1024 to −513, z −512 to −1), as the tree before `8c987ed7` shows
(`ctw/standard/agrostid/region/r.-2.-1.mca`). `60c30083` (2024-10-14 21:07 +02:00, RuedigerLP, "Agrostid: 2.0.0")
added the four region files around 0,0 and kept `r.-2.-1.mca` at its old size (278,528 bytes); CommunityMaps
`bc7059e7` "Agrostid: 3.0.0 rework" and `8590fd0f` "Move Agrostid back to Public Maps" followed on 14 and 16 October.
*Account:* he built his worlds of about 2016 inside one map, so Agrostid did not sit at 0,0, and he had rebuilt it
once (account §25). The record agrees on both.

**On 6 November 2025 Agrostid's folder held six world files, the picture says five.** *Record:* level.dat and five
region files, the old copy among them. *Inference:* with the old copy loaded, the importer's mean and extent would
have run to about a thousand blocks, not 184; so either four region files and level.dat were chosen, or the numbers
in the picture are not of an Agrostid import. The record cannot decide which.

## 2. The stowaways

**"Stowaway" is Sam's word in three commit messages, all of 14–16 March 2026.** *Record:*

| Date (+01:00) | Repository | Commit | Map | Message | What went |
|---|---|---|---|---|---|
| 2026-03-14 16:46 | PublicMaps | `79e85196` | Agrostid | "Agrostid: remove stowaway" | `region/r.-2.-1.mca` (278,528 bytes) deleted; version 3.0.3 → 3.0.4 |
| 2026-03-14 21:17 | CommunityMaps | `5f797a5a` | Mame, I Shrunk the PvPers | "MIStP: remove stowaway" | `region/r.-1.1.mca` (20,480) and `r.0.1.mca` (188,416) deleted |
| 2026-03-16 19:26 | CommunityMaps | `a8f47ee0` | Wintertime | "Wintertime: 1.0.4" — "Flip red side / More wool room gear / Remove stowaway" | `r.-1.-1.mca` 368,640 → 196,608 and `r.0.-1.mca` 233,472 → 151,552 bytes |

All three are by `Sam <samschaap@users.noreply.github.com>`, and each is in the `#maps-changelog` feed under samschaap at
the same minute. `git log --all -i --grep=stowaway` over both repositories returns these three and no others; a wider
search (prune, trim, leftover, cleanup, duplicate, copy, unused chunk) finds prunes by others (Mitchell Thomas,
November 2025; TTtie's "Crown: prune" and "Icarus Fortress: prune", 20 September 2026) that do not use the word, and
no other commit of Sam's that deletes region files. So the record shows **three maps cleaned, by Sam, in three days**.

**Mame's stowaway sat where the author says, beside a second copy's worth of world.** *Record:* the two region files
removed lie at z 512 and beyond, while the map's own shopkeepers stand at z ≈ 330–340; they entered with the map's
upload `79841132` (2024-12-08, jack9590). The map credits Cazadorian, Mewzzy and Tundren, created 2023-02-01; it is not
the author's. *Account:* "practically a complete second copy" (account §25). The record holds the files, not their
contents; 208,896 bytes against the kept files' 1.55 MB fits a partial copy at least as well as a complete one.

**Golden Drought VI has no 2026 commit in either public repository.** *Record:* `CommunityMaps/ctw/golden_drought_vi`
was last changed on 2024-12-27 (proto migration); its commits of October 2023 are by "Rachel", and its `map.xml`
credits Lich_of_Flowers and Penuuy, created 2023-10-01. The feed holds no Golden Drought entry in 2026. *Inference:* the
map still carries `r.0.1.mca` (z 512 to 1023, 20,480 bytes), beyond the furthest coordinate its XML states (|z| = 166),
which is what an uncleaned stowaway would look like. *Account:* a stowaway was found on it too and Sam updated "these
maps" piece by piece (account §25). Whether Sam's update of Golden Drought VI exists the record is silent; whether
Rachel is the Reshif the author names, and whether Reshif is either credited account, it does not say.

**Sam's joke is not in the record.** *Account:* "good opportunity to dev phase that map and forget about it" (account
§25), in a message to the author; no commit or feed line carries it.

**CTWAnalysis does not hold the word, as the author said it would not, but its layout renders of all maps come hours
before the first removal.** *Record:* no commit message or file on any of its branches contains "stowaway" or
"contaminat"; "outlier" occurs only as a statistic (`5455eb1`), "duplicate" only for a doubled plot file (`e8a5439`).
On 13 March it gained `ctw layout --all` and a layout audit (22:05–22:54 +01:00), and at 04:04 on 14 March "render layout
plots as block squares instead of scatter dots" (`007c157`); Sam's first removal is 16:46 that day. That evening at 22:46
`ad9a9f4` added `map_layouts.yaml` with per-map island exclusions, listing `agrostid` and `mame_i_shrunk_the_pvpers`,
and on 15 March `81a79f3` generalised them to `exclude_islands` and `playable_bbox` for "any scenery island".
*Inference:* the stowaways surfaced when every map's layout was first drawn block by block, on 13–14 March; this joins
the author's "once he rendered them with the visualisation functions Claude had written" (account §25) to the record
by timing only.

**The "143 contaminated maps" are in a commit message, and they are not stowaways.** *Record:* `a624eb5` (2026-03-19
23:05 +01:00, Sonnet 4.6), "fix(layout): cap top-surface scan at max_build_height from map.xml": "Decorative structures
built above the playable ceiling (birds, giant trees, floating wool markers, observer islands) caused surface_y to
reflect the decoration rather than the genuine navigable terrain, corrupting the height_above_terrain signal for 143
of 177 maps (81%)." `e4f00c4` corrected it at 23:26; the authors command `6cbc9dd` followed at 00:19 on 20 March, the
commit the screenshot's reply asks to make before it "backfill[s] the layout/terrain fixes for the 143 contaminated
maps". research/18 found neither word; "contaminated" is indeed in no commit, but "143" and the corruption it counts
are in `a624eb5`. So the record reads the 143 as maps whose stored terrain heights were spoiled by decoration above
the build ceiling, and it does not support reading "contaminated" as "containing stowaways". The author's guess of the
server's tracking logs (account §21) is not it either.

**Mame's long match is in the chart, and it is not one of the longest.** *Record:* the week of 26 January to 1 February
lists "1h58m 'Mame, I Shrunk t…'", third of that week after Brittlebush II (2 h 46 min) and Desert Country (2 h 19 min);
no other week lists it (`../sources/early-experiments/2026-ctw-match-activity.md`). *Account:* "by the match logs of
the February experiments that map can run very, very long" (account §25). Consistent: two hours, though three other
maps ran past three.

## 3. pgm-studio-mobile

**pgm-studio-mobile is the plan editor cut loose from the studio, made by Claude Opus 4.8 in one evening.** *Record:*
three commits under `rockymine <rockymine.ocn@gmail.com>`, each with `Co-Authored-By: Claude Opus 4.8`:
`cc99471` (2026-07-09 21:31:57 UTC) "Self-contained mobile plan editor (PWA)", 25 files and 3,749 lines; `26dc811`
(22:10) "UX pass: icon tool rail, opt-in left inspector, themed canvas"; `46f472d` (22:45) "Add marquee multi-select for
moving groups". The README calls it "A **self-contained, offline** version of the pgm-studio *plan editor* (the seed
studio)" with "No backend, no database, no map listing, no map compilation — just draw a layout and **import / export
`.plan.json`**", installable as a PWA from `https://rockymine.github.io/pgm-studio-mobile/`, derived from the studio's
`g49` branch (`claude/g49-spawn-wool-rooms-e43i57`). It omits the server's overlays, lint, the Wall tool and compile.
Three sample plans ship in `examples/`: `four-team-wool-two-sided`, `isolated-spawn` (9 pieces each) and
`mirror-big-board` (39).

**It came an hour after a single-file version inside the studio.** *Record:* in `pgm-studio`, `41d380ad` (2026-07-09
20:48 UTC) "Add portable offline plan editor (single-file HTML)", `tools/mobile/plan-editor.html` of 1,533 lines, "so a
plan can be authored offline — on a phone or in a chat artifact — with no server", and `a958b6c9` (21:09) "Make portable
plan editor mobile-friendly"; both Opus 4.8. The separate repository opens 22 minutes later. *Account:* around 10 July he
asked Claude to make the plan tool's state a single HTML application, since nothing was published, so that Ruediger
could draw layouts and they could pass JSON back and forth (account §25). The single HTML file is the studio's; the
published app is the multi-file PWA.

**He sent the link between the second and third commits.** *Record:* "https://rockymine.github.io/pgm-studio-mobile/" at
00:28 German time on 10 July, which is 22:28 UTC on 9 July, after `26dc811` (22:10) and before `46f472d` (22:45).
Ruediger at 00:48: "aber nur das planning tool oder?"; the author at 08:41: "Ja. Ist Absicht. Das konnte man gut
extrahieren und ermöglicht es einfacher schonmal paar Layouts etc unterwegs zu malen ohne die ganze App."
(`../sources/july-2026-shapes/`).

## 4. The teaching files

**The teaching folder opens on 5 July 2026, with middle zones among its first subjects.** *Record:* `959ce486`
(2026-07-05 14:34 +02:00, rockymine with Opus 4.8) moves a "build-interface teaching sketch" into
`tools/seeds/teaching/` (`build-interface-dos-and-donts.plan.json`) and adds `SHOPPING-LIST.md`: "Curated `*.plan.json`
examples that exist **only to inform `layout-rules.md`** — do's and don'ts, like the mid `build-interface-dos-and-donts`
set". The same day `45fd3ab2` (19:11) adds `frontline-dos-and-donts-rot-180-mirror.plan.json`, and `c5d1adbd` (20:12),
"Rules round 3: frontline/mid amendments from the teaching sets", adds `rot-90-mid-example-1` to `-8` and a
`mirror-mid-examples` set whose 66 pieces carry labelled ids (`frontline-1`, `step-1a`, `hub-5`, …), encoding nine rule
amendments (HB4, FR6, FR7, MD6, CT8–CT11, BZ10).

**The labelled lanes of 8 July are the same method for wool approaches.** *Record:* `dbe61ab0` (2026-07-08 06:39 UTC)
"deriver: classify wool-lane SHAPE (I/L/Z/complex) + width"; `f51daee1` (07:06) "wool-lane training set" —
`tools/deriver/lanes/` of "hand-labelled mirror=none single-lane examples + labels.json", a harness that diffs the
classifier against the author's label; `9aba8456` (17:20) `_reference.plan.json`, five verified lanes with ids such as
`i1-dock`, `l1-lane-a`, `z2-lane-c`, `plaza1-wool`, "where the id carries the intent". Later: `tools/compose/wool-lane-study/`
(6 July, six plans), `tools/deriver/shapes/` (10 July, 17 fixtures), six more teaching plans on 14 July (crammed and
double frontlines, middle voids, `a4ff7147`) and the traced real-map corpus `tools/seeds/traced/` (`94be5e7e`, 14 July,
"traced teaching corpus"), in which `agrostid.plan.json` is one of the first files.

**The plan format came three days before the folder.** *Record:* the plan model entered the studio at 22:47 UTC on 2
July (research/09). *Account:* "Around the beginning of July" he began teaching files, middle zones for example, and
"Sobald das Planformat dann da gewesen ist, hat es einfach sehr geholfen" (account §25). The record agrees in date and
subject.

## 5. The shapes, the boxes, and whether a generator existed on 8 July

**A generator existed on 8 July: the composer, four days old.** *Record:* `7b4603cc` (2026-07-04 17:15 +02:00) "G32
first slice: composer envelope + team-unit grower" (research/02); on 7 July `64268a68` "deriver: add a generated-seeds
section from the current composer" and `6eee66d0` expanded it "to ~40 for variance". *Account:* he is not sure whether
a generator existed when he drew (account §25). It did; what did not yet exist was the box grammar.

**The tablet sketches follow a day of lane labelling, and his message says what they were for.** *Record:* the sketch
files are stamped 8 July 23:43; that day the classifier, the training set and the reference examples above were
committed (06:39–17:20 UTC). On 9 July at 20:35 he wrote: "Ich bin am überlegen was für verschiedene shapes von wool
lanes es gibt um die später im Tool zu labeln und claude zu geben um zu schauen ob man die automatisch labeln kann."
The first sketch has seven hatched lanes, each ending in a square with a dot, with red glyphs for zigzag, step and U;
the second a dozen coloured ones each ending in "W", with blue patches.

**"Tetris" is in the record twelve days before the sketches, and "scythe" with it.** *Record:* `206ba341` (2026-06-26
17:11 UTC, Opus 4.8), the sketch tool's shape-library plan: "**Polyomino primitives** ("tetris +")", "L/U/T/I/scythe/
cross/line-with-branch", the Scythe given as a ten-vertex ring; built in `3c243b16` that evening. *Account:* he had long
had the idea that maps partly consist of Tetris pieces, which became the generator's basis (account §25). The word
reaches the record first as drag-in shapes in the sketch tool, not as the generator.

**The wool-approach shapes and the boxes first appear on 10 July, from one Claude web session.** *Record:* all of the
following are by "Claude", Opus 4.8, most with `Claude-Session: …session_01QYwWRxvJbdRqBGUmd3WQv7` (the session of the
8 July lane work too):

| UTC | Commit | First appearance |
|---|---|---|
| 07-10 19:08 | `9d75d05c` | "box-partition + interface-width grammar + wool-approach shape catalog": "typed spawn/hub/frontline/mid boxes as bounding envelopes"; catalog "isolated, straight, side-tuck, corner, flanked, bay/scythe, hole/donut" — first "donut", "side-tuck" |
| 07-10 19:33 | `77cdc57b` | "H/branch + plug approach shapes and the four-way skeleton test" |
| 07-10 19:54 | `449b46b3` | the catalog as 17 plan fixtures in `tools/deriver/shapes/` |
| 07-10 20:23 | `c4cf5324` | `WoolBoxEmitter`: "emit wool-box base shapes (I/L/Z)" |
| 07-10 21:28 | `166f2a07` | "emit all eight base families, verified against WoolApproachShape" |
| 07-10 23:05 | `a8feaf6b` | "add U (flanked) family and donut wool-at-corner" |
| 07-11 06:47 | `7672cfdc` | "variable entry-nub width on Z and scythe (attachment grammar)" |
| 07-11 07:53 | `3ddc51d4` | "classify wool approaches by width-invariant turn count" |
| 07-11 09:13–09:37 | `8516d028`, `6139319e` | backlog G50–G52: shift the wool-box entry off the corner; "wool docking mode (extend vs side-dock)" |
| 07-11 11:54 | `a567b69f` | "the piece vocabulary — families as templates of role-typed segments": first `entry-bar`, `room-bar`, `room-run`, "plug=room", "base case" |
| 07-12 00:48 +02:00 | `d6b5c06e` | "split the two-leg branch into U (flush) and H (stub)" |

**The chat lines fall between those commits.** *Record:* "Ich verwirre die KI" (09:13 German, 07:13 UTC) and "er hat sich
ein zu statisches system gebaut" (07:39 UTC) come between the variable entry width (06:47) and the width-invariant
classification (07:53); "Damit wir I, L, h, U, … Förmige wool approaches haben können" at 08:06 UTC; the long message
at 15:27 German (13:27 UTC), with "Welcher "Wool approach" gesetzt wird hängt am Ende von einer Box-Größe ab" and "Im
Grund ist die Idee eine Box für Frontline, Hub, Spawn und Wool(s) zu platzieren", an hour and a half after the piece
vocabulary. Its three pictures show cards with the role boxes entry, entry-bar, leg, room-bar, room, bar and room-run
and the titles Plug ("base case"), H and Scythe. *Inference:* his complaint of a static system matches the morning's
work of making entry widths and docking variable; the cards' exact texts ("just the wool room docking a box (the hub)",
"three turns — a fold with an open bay") are not in a commit of that day ("a fold with an open bay" first appears on 14
July, `5b5f9448`), so the catalogue pictured was a page or artifact the session rendered.

**The boxes in code came a week later.** *Record:* "Compose: the hub box…" and "the frontline box…" on 18 July, the
first full board off the partition path and "the box pipeline is THE composer" on 21 July (research/01). On 14 July a
Fable 5 review of the generation model (`f58985ab` onward) made "WoolApproachShape's dissolution explicit" and argued
"per-kind shapes via profiles/patterns, no *Shape zoo".

**What is new against HISTORY chapter 6 and research/01, /02.** Those sources date the box partition to 10 July
(`9d75d05c`) and the composer to 4 July, and say the concept was the author's. New here: the lane labelling of 8 July and
the teaching folder of 5 July as the method behind it; the tablet sketches as his drawing of that day; the shape
names (Donut, Scythe, Plug, H, U) and the role pieces dated to 10–11 July; the "tetris +" shape library of 26 June; and
the chat, which records the author describing the box grammar ("eine Box für Frontline, Hub, Spawn und Wool(s)") on the
day the session wrote its vocabulary.

## 6. Villager shops

**The studio first wrote shops and shopkeepers on 12 September 2026.** *Record:* `9db95eaf` (2026-09-12 22:03 UTC,
Claude) "Read, store, emit and author shops and shopkeepers (PG9, PG10)", with `docs/pgm/shops.md`; the ids PG9 and
PG10 appear first in that commit, so no earlier board entry records the request. `shops.md` takes
`ctw/mame_i_shrunk_the_pvpers`' item shop as one of its examples. Shops had already been written by hand outside the
studio: arcadeboss's GrokBuild wrote a whole shop XML from a price list on 27 August (research/15). *Account:* the
feature was a little his request, because he liked maps like Mame (account §25). The record dates it and shows Mame in
its documentation; whose request it was, it does not say.

## 7. Where the record and the account differ

| Account (§25) | Record |
|---|---|
| The first import was Agrostid | No commit names a map; the picture's 184 × 267 fits Agrostid's XML extent and no Annealing map's (inference) |
| Agrostid ten years old, not at 0,0, rebuilt once | Created 2015-04-26; in `r.-2.-1` alone until the 2.0.0 edit of 14 October 2024, which kept the old file |
| Sam named the leftovers "stowaway" | Three commits by Sam, 14–16 March 2026: Agrostid, Mame, Wintertime |
| Found on very many maps | Three removals carry the word; no list of affected maps exists in the record |
| Golden Drought VI cleaned too | No 2026 commit; a region file beyond its XML extent remains (inference) |
| — (the 143 left open, account §21) | `a624eb5`: 143 of 177 maps with decoration above the build ceiling; not stowaways |
| Mame runs very long | 1 h 58 min in the week of 26 January |
| pgm-studio-mobile around 10 July, a single HTML app | Single-file HTML in the studio 9 July 20:48 UTC; the PWA repository 21:31–22:45 UTC |
| Teaching files from the beginning of July, middle zones | `tools/seeds/teaching/` from 5 July, mid examples that evening |
| Unsure whether a generator existed on 8 July | The composer from 4 July; the box grammar from 10 July |
| Shops a feature born of maps like Mame | First written 12 September 2026; Mame cited in `docs/pgm/shops.md` |
