# 09 — The session that made the Base maps

Research for the history. Subject: the Claude Code session in which the first three "Base" maps were made from a
layout the author drew on squared paper (`../author-account-2026-11-27.md`, last sections; research `07` §2 and §3).
Read on 27 November 2026 from the session's own transcript, with the `pgm-studio` history beside it. Hashes are
`pgm-studio` commits. All times are UTC, as the transcript stamps them; the author's local time that summer was
CEST (UTC+2), which is an inference about where he was and is used only where marked.

**The session.** `session_014BYG9EwhkDRUmRP1FYLBk2`, titled "P9 backlog task breakdown", created 1 July 2026 at
22:10:32 from an Android client, Opus 4.8, repository `rockymine/pgm-studio`, branch `claude/p9-task-breakdown-ufx0s9`.
Its last event is 2 July at 12:16:54. Every message the author typed is English, so no gloss is needed.

## What was read, and what was not

**Read in full: every message the author typed.** The transcript was paged backwards from its end to its first event
and every user-typed message was taken out of it; the tool results that carry no typing were not read, except where
quoted. Between 1 July 22:10 and 2 July 12:16 the author typed 28 messages (a hook notice and the model's own prompt to a helper agent are not his); nearly all are quoted or cited below.

**Read in part: the model's own words.** Its text was read for 2 July 07:21–07:43 (the photo), 08:41–09:12 (the
render and the rebuild) and 11:09–11:19 (the four-team seed). The rest of the model's text, and all its tool calls,
were not read; the commits stand in for them.

**Not readable: the model's reasoning.** Every thinking block in the transcript is empty (a signature and no text),
so why the model drew the photo as it did is known only from what it said afterwards. The photo itself is not in the
transcript either; only its note "[Image: original 4624x2604, displayed at 2000x1126 …]" and the file name the model
opened. The author's own copy is `../sources/base-map-squared-paper-drawing.jpg`.

## 1. What the session was first about, and when the drawing came in

**It was about P9, not about maps.** The first message, 1 July 22:10:33:

> the task Board is empty. I would like to work on p9 from the backlog next. it needs splitting into it's own tasks
> and Lots of clarification by me.

P9 was the backlog item for a world-folder export of a sketch: `.mca` region files and a `level.dat` for a map that so
far existed only as a drawn layout. The first commit of the session, 22:31, is "Split P9 into P9a-P9g sub-tasks in
backlog" (`6eba4251`). The next two hours are specification, and the author does the specifying in long messages.

**The author, not the model, designed the bedrock box.** At 23:21:13 he typed:

> wool cages should be hollow bedrock 8x8x8 cages. the 3rd layer from the top should be missing to show some light.
> the roof should be missing a 4x4 center. the 5th layer from the top should be wool blocks. to let players enter
> the cube from all sides they need four 2 wide 3 tall doors made from stained glass on top of the floor level.

He goes on for a paragraph: a 2×2 wool marker in the floor, two stacked chests in each corner with stated loadouts, a
spawn cube "except that it has a single door that will be 4x4", the monuments in the cube's corners with a bedrock
pedestal and a sign. At 23:31 and 23:40 he adds layer numbers and "x and z also need to be full integer coords as
otherwise the structure won't place properly, it has a 2x2 center". The contract document followed at 23:24
(`224f6d4b`), refined at 23:32 (`7e98fa84`). Research `07` §3 says "the 8×8×8 bedrock shell was specified by Opus 4.8";
the transcript says the dimensions, the layers and the doors were his and the model wrote them down.

**The build started at 00:11 on 2 July.** "you may start building now … you can essentially build the whole thing now.
test and commit after each task." (00:11:40). The model had to install the .NET SDK and MariaDB first (the cloud
container had neither; 00:12–00:18), then wrote `P9a` to `P9l` from 00:19 to 07:13 (`ef56874c` … `bb634545`), and
moved the cluster to FEATURES at 07:14 (`5d75520d`). The export endpoint `GET /map/{slug}/export` is `8a53c2b6`,
07:06:59.

**The word "seed" enters at 07:19.** The author typed, 2 July 07:19:48: "you should end-to-end test with a seeded
sketch map". The model built a throwaway map in the running studio: two plain rectangles, 40 by 40 blocks, height 3,
posted through `POST /sketch`, `PUT …/sketch`, `…/finish`, `PUT …/intent` and `GET …/export` (07:22–07:27). It
found MariaDB stopped and the schema never migrated (the app does not migrate itself; only tests do), fixed both, and
decoded the `.mca` back: 6400 stone, 4166 bedrock, 72 wool, 16 chests, 10 signs, "End-to-end validation is
**conclusive**" (07:27:24). That throwaway was never committed.

**The drawing came in at 07:37.** The model woke at 07:37:38 and opened an uploaded file named
`20260702_0929191607934470108003284.jpg`. The first line of the author's message is stamped 07:37:15 and the image
note 07:37:40. By the file name the photo was taken at 09:29:19 on 2 July; if that is the phone's local clock it is
07:29 UTC, eight minutes before he sent it. That is an inference; the transcript holds only the name.

## 2. The photo, the misreading, the coordinates, the builds

**What he asked for, in his words.** 07:37:15, in full:

> please make this layout as a general seed for testing. green is the build area. red are where the team spawns
> are. blue is where the wool spawns. middle line is at 0 with center at 0,0. we have the team's main island as a
> distorted H shape (different spine lengths) and one square island. the observer spawn would be positioned dead
> center at 0,0 but raised to something like 24. max build height would be something like 20. island height for the
> large island would be 9, for the small island 13. one cell on the raster paper is 5x5 blocks. the total bbox
> therefore is 30x(28×5). what's good about this layout in particular is that we can use the general 2 island setup
> also with rotate 90 symmetry mode to make a 4 team map to test 3 wool monuments. we could also mirror the layout
> to the right along the spawn axis to have a H with a center spine that would give us a test for the common 2 teams
> need to capture 2 wools each setup. it's pretty much the most basic map design out there.

Three things in it. The drawing was made "as a general seed for testing", so the Base maps were conceived as
fixtures to exercise the export, not as maps to play. The author named in advance all three variants that were built
(two teams, four teams by `rot_90`, two wools each). And "red" are the dots the author's account calls orange.

**What the model saw.** After three minutes and forty-three seconds (07:37:38 to 07:41:21) it wrote, at 07:41:24:

> That's a clean 2-island CTW base — distorted-H team islands (rot_180) plus a central square, wide and shallow.

It then wrote the layout without asking anything: a team island of three rectangles, `top_arm` (x −70..−30, z 5..15),
`bottom_arm` (x −70..−45, z −15..−5) and `spine` (x −45..−30, z −5..5), mirrored by `rot_180`, and one centre
square (x and z −10..10) at height 13. The bounding box was 140 by 30. The seed was committed at 07:43:42 as `c6b0fd89`,
"Add base 2-island CTW test seed", whose message says "Validated end-to-end".

**What went wrong, in the model's own words.** The author asked at 08:38:04: "please output the traversability image
from the ui into this chat so that I can judge the look of the map." The model rendered a top-down picture of the
seed from the studio's own island, traversability and intent data (08:42–08:45) and added, at 08:45:38:

> **The thing worth your eye:** the team islands read as a **staircase/bracket**, not a clean "H". My reconstruction
> placed both arms on the same (outer) side of the spine, so the union comes out as a Z/L rather than an H with
> arms on both sides. If you want a truer distorted-H (arms extending both directions off a central spine), give me
> the arm cell-lengths from your drawing and I'll retune `base-2island.layout.json`

So the fault was the shape: the two bars of the H stood on one side of the crossbar, and the drawing's two small
squares became one square in the middle. The model's own check had found it "fully connected" (08:42:05), which asks whether spawn
and wool join, not whether the layout is the drawing; the seed was connected and wrong. The transcript gives no other
cause. One more difference stands out from a look at the photo: it is wider than tall, the model laid the long axis
along x (140 by 30), and the author's later coordinates put it along z (40 by 140). Which frame is turned against the
paper is not discussed anywhere in the transcript.

**How the layout was then given: as corner coordinates.** The author did not send a second photo. At 09:09:10, 24
minutes after the model's offer, he typed:

> I'll give you the anchor coords scaled down (need to be multiplied by grid resolution). we have center at 0,0.
> the small square island (not the observer spawn) has it's anchors at 1,1 1,3 3,3 3,1. the h structure has anchors
> at 1,5 3,5 3,11 1,11 1,9 -1,9 -1,13 -3,13 -3,4 -1,4 -1,7 1,7. you can follow these points and connect the first
> and the last. that should give the 2 hulls. Spawn is positioned at 2,10 and wool at -2,12. obs spawn is no
> island inside the sketch. it gets created from setting the obs point at 0,24,0 in configure.

The model multiplied by five and wrote the H as a twelve-vertex polygon (09:11:35: "those H anchors make a **proper
distorted H** (two vertical bars of different lengths joined by a crossbar), not my staircase"): right bar x 5..15,
z 25..55; left bar x −15..−5, z 20..65; crossbar x −5..5, z 35..45; the square x 5..15, z 5..15. It is
`cca91571`, 09:14:50. Spawn (10, 50), wool (−10, 60), observer (0, 24, 0), both teams by `rot_180`.

**Two corrections to the build region followed.** 09:17:57: "that's great. the build region isna bit too extreme.
make it from -3,-5 to 3,5 but scaled with the grid factor. that should produce the intended build region." The
model's first build region had been the whole bounding box; it became x −15..15, z −25..25 (`47d2e20c`, 09:20:01).

**The order of what was built.**

| UTC, 2 July | What the author asked | What the model made | Commit |
|---|---|---|---|
| 07:37 | the drawing as "a general seed" | wrong H, one centre square, 140 by 30 | `c6b0fd89` 07:43 |
| 09:09 | the corner coordinates above | the drawn H and two squares, 40 by 140 | `cca91571` 09:14 |
| 09:17 | build region −3,−5 to 3,5, ×5 | a central band | `47d2e20c` 09:20 |
| 10:00 | "are there any Tests for the seed" | a test that runs the seed through the export | `b89cef45` 10:04 |
| 10:39 | spawn protection and wool room should "encase the cubes" | both derived from the cube footprint | `2743c895` 10:44 |
| 11:05 | "can you make a 4 team seed? … we just rotate the 2 islands around the center" | four H arms, eight islands, three monuments a cube | `2770c485` 11:13 |
| 11:15 | "build that one next" | first 2-wool seed: an H with the spawn on the crossbar | `febb21ce` 11:21 |
| 11:59 | the 2-wool layout is not an H any more (below) | the H plus an L-shaped wool island and a bridge | `270768ff` 12:04 |
| 12:05 | "the layout dropped the small islands near the middle" | the squares put back, six islands | `69e911e6` 12:08 |

**The 4-team seed.** 11:05:37: "perfect. now that you understand the seed and intent strucure. can you make a 4 team
seed? center is still the same. we just rotate the 2 islands around the center. what has to change is the build
region. here we would just do it cheap and have four build regions in the intent. spanning from -3,0 to 3,5
(multiplied with the grid factor again)." The model rotated every coordinate 90° per team, checked "12 monuments = 3
per spawn cube" (11:10:31) and committed at 11:13. Colours red, blue, yellow, green.

**The 2-wool seed was built twice.** The model had written "I left it as a documented "still to come" rather than
guess the geometry. Want me to build that one next, or is the 4-team enough for now?" (11:13:33); the author answered "build that one next" (11:15:18).
Its first version took the author's 07:37 phrase, "mirror the layout to the right … to have a H with a center
spine", and made exactly that. At 11:59:07 the author gave the layout he meant:

> for the 2 wool setup we can reuse the large island and add a new island for the second wool as well as a new
> bridge region. it's not a h anymore but still a common layout. the new island to be added has the following
> coordinates inside the non-scaled grid: 5,9 9,9 9,5 7,5 7,7 5,7. the wool spawn is placed at 8,6. the island is
> the identical height as the tiny square island. we need to add a new build region rectangle from 3,9 to 5,7 to
> connect the new wool island to the h structure. then scale the whole thing. we can use mirror or rotate 180 for
> this. does not matter. obs spawn stays in the same place. build height also identical.

The model rebuilt it at 12:04 ("a small L-shaped wool island for wool2, linked by a new bridge build region"). The
author saw the picture and typed, 12:05:46, "the layout dropped the small islands near the middle. we will integrate
it in this layout too!", and at 12:08 the model put the squares back. The model's closing table (12:08:40):
`base-2island` 4 islands, 2×1 teams and wools, 1 monument a cube; `base-4team` 8, 4×1, 3; `base-2wool` 6, 2×2, 2.

## 3. What a "seed" was, and whether maps had already been traced

**A seed was a pair of JSON files for a test.** The model's answer to the author's 12:12:54 question, "may I ask
where the seeds live in the code?", is 12:13:14: they are in `tools/seeds/`, each "a **pair of JSON files**:
`*.layout.json` is the *sketch* (the polygon shapes, islands, and `mirror_mode` symmetry …), and `*.intent.json` is
the *authoring intent* (teams, spawn/wool/observer points, build regions)", posted by `seed.sh` to a running studio
and guarded by `BaseSeedWorldTests`. The layout holds shapes with a `base_height` (the first version rectangles, the
second polygons), so "rectangles and heights" describes it in part. It is not the plan model.

**The plan model came ten and a half hours after this session ended.** `e09959cb`, 2 July 22:47: "G16 + G17: plan
schema, validator, compiler + the three seed plans … The three seeds are re-expressed as `tools/seeds/*.plan.json`".
The first seed file in the repository's history is `c6b0fd89`, this session's; the first real map traced into one is
`aca45ae1`, 4 July, "real-map trace at 30/team"; "Trace four maps into the plan model" is `ced41d86`, 10 August.

**Maps had been traced before, but not into seeds.** From 20 to 22 June the studio had a Decompose surface that read
a map's islands and stored them "→ sketch format, stored per map" (`1ab1a82d`, `13087536`,
`f94b97f5`). The transcript lists its route (`/maps/{Slug}/decompose`, 08:39) without using it, and the board entries
for it were struck on 2 July at 18:59 as the plan-then-realize direction replaced "the decompose->corpus-mining
flywheel" (`12a57b8b`, `87ed78f9`).

**What the author said about tracing other maps' islands: nothing, in this session.** None of his 28 messages
mentions tracing, a corpus map or another map's layout; the only named map is `outback_outback_edition`, to copy
sign patterns and a `level.dat` from (00:11:40).

## 4. The first playable maps, and what the world looked like

**They were the first worlds the studio wrote from a sketch.** The model's pull-request text (12:16:42) says why:
"Sketch-originated maps had no real voxel world (their "world" was a synthetic `layer.parquet`), so they couldn't
ship a playable PGM map." The export that gives them one was finished that morning (`8a53c2b6`). That makes the Base
seeds the first sketches to leave the studio as a world, and the throwaway of 07:22 the first world made before them,
uncommitted.

**Playable was the model's word, and the first load failed.** The model "validated" by decoding its own `.mca` files
with the studio's own reader. The commit that follows, 2 July 21:21 UTC, is by rockymine: `7576a6c4`, "AnvilRegionWriter:
emit the light + heightmap tags the 1.8 loader requires — Exported worlds crashed on load ('heightmap array length
is 0 instead of 256'; 'ChunkNibbleArrays should be 2048 bytes not: 0')". It does not name which world he loaded, and
the transcript ends nine hours before it. Nothing read says a Base world was walked on a server.

**The world, in the model's check.** The 09:23 verifier, run on the corrected seed, passed all 17 tests; among them:
"H island bedrock@y0", "H island stone@y1..8", "H island surface=9 (air@y9 on bare terrain)", "square bedrock@y0",
"square stone up to y12", "spawn cube floor 2x2 wool@y9 (marker)", "spawn cube roof bedrock@y17", "observer
platform bedrock@(0,24,0)", "observer floats (air just below @y23)". So: a bedrock floor at y 0, stone to the island's
height (9 for the H, 13 for the square), an 8×8×8 bedrock shell for a spawn and a wool
cage standing on the ground with a 2×2 wool marker, and a 6×6 bedrock observer platform floating at y 24.

**The author's own words for it** are his specification, 23:21 on 1 July, quoted in §1, and, on 2 July at 09:21:39,
a question that lists what he expected: "did you validate the position of the spawn and wool boxes to sit on the
terrain, the layout having bedrock at the bottom of the islands, the observer spawn being in the correct place
etc." At 09:54:51 he settles the anchor: "this sounds correct. no nerf to change Single block. the Box and wool and
obs spawn all have a 2x2 center."

## 5. Other things that belong in the history

**The author's reactions are short and warm.** 09:17:57 "that's great"; 09:21:39 "amazing"; 11:04:00 "prioritizing
the users authored regions and falling back to the cube is the perfect choice"; 11:05:37 "perfect"; 12:12:54 "I am
fascinated. this is awesome." At 12:15:42 he asked for a pull request ("can you create a pull request for this"),
and PR #1 was opened at 12:16:44, "P9: sketch world-folder export (playable .mca + level.dat) + CTW test seeds".

**He kept deciding what the model's rules should be.** 09:46:18 asks whether the spawn points sit at the centre of
the 2×2 markers; 11:04:00 settles that authored regions come before the cube and asks that the build height of 20
be confirmed in the intent. 10:00:39: "are there any Tests for the seed / commands that drive it straight through
the full pipeline / loadable from the ui?"; the test is `b89cef45`, four minutes later.

**The surprises were environmental.** The container had no .NET and no working MariaDB at 00:15; MariaDB had died by 07:22;
the app does not migrate its schema, only the tests do. The model noted it could add that to the cloud runbook
(07:27:43). Nothing in the session concerns trees, terrain painting, models or the Python rework.

**The name "Base" is the model's.** The author's messages never use it. He wrote "the most basic map design out
there" (07:37:15); the model called the first seed "a clean 2-island CTW base" (07:41:24), named the files
`base-2island.*` and the map "Base 2-Island". "Base 4-Team" and "Base 2-Wool" follow from that. "Base to Rule" and
"Base for Teams" appear in none of his messages.

**The maps had no authors.** The seed intent says `"authors": []`, and the observer platform's right-hand sign, which the
author specified at 23:56 on 1 July as "made by" in italics over the authors' names, would then carry no names
(inferred from the empty list; research `07` §4 follows the sign).

## What the transcript confirms and contradicts in the author's account

| The author's recollection (27 Nov) | The transcript |
|---|---|
| He drew the layout on squared paper and gave it to the model | Confirmed. 07:37:15 and the photo, 2 July |
| The model did not read the photo well | Confirmed, and in the model's own words, 08:45:38 |
| He then gave the corner coordinates and that worked | Confirmed. 09:09:10; the model's 09:11:35 "not my staircase" |
| The drawing is the two-team map; the 2-wool map had an island pushed on | Confirmed, and refined: the 2-wool map reused the H and added an L-shaped island and a bridge (11:59:07) |
| Orange dots spawns, blue wools, "or the other way round" | Settled: red (his word) are spawns, blue wools, 07:37:15 |
| Bedrock floor, stone to a height, bedrock boxes for wool and spawn | Confirmed, in his spec (23:21:13) and the model's checks (09:23) |
| Probably the first maps made this way | Confirmed as the first worlds from a sketch; the author's purpose was "a general seed for testing" |
| Three Base maps, "Base to Rule" and "Base for Teams" | Three maps; the names are the model's, Base 2-Island, 4-Team, 2-Wool |
| He had already traced existing maps and stored them as seed files; the seed was the plan model | **Contradicted for this session.** Seeds are born here, as test fixtures; the plan model follows at 22:47 the same day; the first traced real map is 4 July. What predates it is the June Decompose surface |
| Tracing other maps' islands into one format proved too varied | Not in the transcript. The Decompose entries were struck on 2 July, but the reason given there is a change of direction, not a failed format |
| The drawing was the very first before Brittlebush | Holds (Brittlebush is October; research `07` §2) |

## Open points the record cannot settle

Whether any Base world was played on a server. Whether the first crash on load of 2 July 21:21 UTC was on a Base
world. Which axis of the paper is x. Whether the 11:21 centre-spine version of the 2-wool seed was drawn or only
described. Why the 8×8×8 shell has the layers it has: the layers are the author's, and the transcript does not say
where he took them from.
