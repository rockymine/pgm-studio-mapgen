# 06 — The playtests, and what CommunityMaps holds of them

Research for the history. Subject: the author's statement of 27 November 2026 that the AI maps were tested on the
server in sessions he calls "Slop Sundays", that the last was on 27 September 2026, and that the tests show in the
commit history of `OvercastCommunity/CommunityMaps` because Ruediger always uploaded the maps
(`../author-account-2026-11-27.md`, last line). Read on 2026-11-27 from a full-history blob-less clone of
CommunityMaps (4,253 commits, head `5a191d44` of 27 November, all three remote refs), and from `pgm-studio-mapgen`
and `pgm-studio` (all refs). Hashes are CommunityMaps' unless marked **(mapgen)**. CommunityMaps times are the
committers' own, which for RuedigerLP is +0200 (German summer time); mapgen times are UTC.

**How the search was made.** Every commit from 1 May to 27 November 2026 (281) was listed by author, committer
and message. Messages were searched for ai, slop, test, studio, mapgen, generated and the model names; authors for
Ruediger, rockymine, TTtie and Flamiix; every `map.xml` added, changed or deleted in the window, and every `map.xml`
at head, was searched for opus, claude, sonnet, haiku, fable, grok, mapgen, studio and gemini; every board name in
`maps/INDEX.md` was compared with the folder names. No commit message contains "slop", "AI", "studio" or "mapgen".
rockymine and Flamiix have no commits in the repository in that window; every upload is RuedigerLP's.

---

## a. The uploads

**Record.** Every AI-made or studio-made map that entered CommunityMaps in 2026 was committed by RuedigerLP,
through GitHub's web interface (committer `GitHub`), in four batches between 27 July and 2 September.

| Date (+0200) | Weekday | Hash | Message, verbatim | Map | Made by | Removed |
|---|---|---|---|---|---|---|
| 2026-07-27 23:33 | Mon | `8df2ca00` | Kuusepuu CTC: added | `arcade/standard/kuusepuu_ctc` | rockymine and DerStiv's `dtcm/kuusepuu`, credited "CTC conversion: Claude Opus 5" | still at head |
| 2026-07-28 01:09 | Tue | `7fb35f88` | Kuusepuu CTC: 1.0.1 | same | the time limit replaced by the "Cookie Monster" | — |
| 2026-07-28 01:10 | Tue | `591d21b1` | Hello World Mini: added | `ctw/hello_world_micro` | a studio plan: the folder carried `hello-world-mini.plan.json` with `"plan": 1`, the plan-editor schema of 2 July **(studio `e09959cb`)**; credited to rockymine alone | 2026-08-12 |
| 2026-07-28 01:30 | Tue | `fb0013e1` | Hello World Micro | same | wools moved one block, staggered second wool | — |
| 2026-07-28 01:48 | Tue | `04e61f88` | Hello World Micro: update 1.0.1 | same | "a per-game roll decides whether you need 1 or 2" | — |
| 2026-07-28 01:58 | Tue | `b4ef98e9` | Delete ctw/hello_world_micro/hello-world-mini.plan.json | same | the plan file taken out | — |
| 2026-07-28 02:19 | Tue | `53b38d93` | Kuusepuu CTC: 1.0.2 | Kuusepuu CTC | the delivery is the win; no score, no time limit | — |
| 2026-07-31 23:03 | Fri | `d73e7040` | Kuusepuu CTC: 1.0.3 | Kuusepuu CTC | a respawn fix whose comment says "Reported live: a carrier died, the cake went home, and he still came back holding a usable cake and placed it for the win" | — |
| 2026-08-07 20:58 | Fri | `11a15f7d` | No Blocks Placed: added | `ctw/no_blocks_placed` | the studio, drawn in the browser; credits rockymine, Ruediger_LP, Flamiix | still at head |
| 2026-08-12 23:15 | Wed | `067c82cc` | Delete ctw/hello_world_micro directory | Hello World Micro | — | removed here |
| 2026-08-12 23:20 | Wed | `37bdef57` | Add Viridian and Thornwake | `ctw/thornwake`, `ctw/viridian` | `tools/mapgen`, 11–12 August; Thornwake credited "mapgen" (Opus 5, inferred: it is not one of the batch's four Haiku boards), Viridian credited "haiku" (Haiku 4.5, `hk1_viridian` in `BOARDS-BUILT.md`) | both still at head |
| 2026-08-15 04:56 | Sat | `f17a371a` | No Blocks Placed: add creation date | No Blocks Placed | committed by **TTtie** | — |
| 2026-08-15 13:49 | Sat | `ff115048` | No Blocks Placed 1.0.2 | No Blocks Placed | one `<clear/>` added to a kit | — |
| 2026-09-02 02:18 | Wed | `c86226db` | Millrace 2.0.0 | `dtcm/millrace` | Opus 5's `opus5-millrace`, finished by hand by rockymine and Ruediger_LP; Opus 5 credited | still at head |
| 2026-09-02 02:20 | Wed | `21b6d9b8` | Millrace 2.0.1 | Millrace | an `only-air` material added | — |

**Counts.** Six distinct maps made with a model or the studio were uploaded: Kuusepuu CTC, Hello World Micro, No
Blocks Placed, Thornwake, Viridian and Millrace. Four of them name a model in their credits (Kuusepuu CTC and
Millrace "Opus 5", Viridian "haiku", Thornwake "mapgen"); No Blocks Placed and Hello World Micro are studio plans
credited to people. Four upload batches carry them (27–28 July, 7 August, 12 August, 2 September), with
same-night revisions after the first and later fixes on 31 July and 15 August. One map was removed: Hello World
Micro, on 12 August, five minutes before Thornwake and Viridian arrived. The other five are all still in the
repository on 27 November, in the development phase where they state one.

**No Blocks Placed and Brittlebush III.** No Blocks Placed is there, credited to rockymine ("Drawing pieces, shapes,
and markers in the browser."), Ruediger_LP ("Wisdom.") and Flamiix ("Minimalist."); TTtie's only part in the record
is the creation date of 15 August. Brittlebush III is not in CommunityMaps at all, under any folder or message;
only Brittlebush (2022) and Brittlebush II (2023) are.

**The other uploads of the window are not AI maps.** Ruediger's Vauxite, Capture the Wool CTW and Drastic Change
II (24 June) and Bridgid II (14 July) credit people only and are corpus maps in the studio's goldens; Hello World
(2025) predates the studio. A separate line of AI-made maps runs through the same months from another author,
arcadeboss, credited to "SuperGrok", "GrokBuild" or "GrokBot" (Cedar Crossing on 9 August to Hot Potato and
Xavier's Mansion in November). Its "Play test updates" commits, one of them on Sunday 15 November (`0524662a`), are
that project's and not this one's.

## b. The first and the last test

**Record, the first.** The first AI-made map on the server's repository is Kuusepuu CTC, on the night of Monday 27
July, with Hello World Micro an hour and a half later. Its fix of Friday 31 July is the only commit in the window
whose text reports something seen in play ("Reported live").

**Record, the last upload.** The last is Millrace, in the early hours of Wednesday 2 September. RuedigerLP commits
nothing to CommunityMaps between 2 September and 19 October, and then only to his own map 803. No map of any kind by
this project enters CommunityMaps after 2 September.

**Record, 27 September.** It is a Sunday. CommunityMaps holds nothing for it: the commits on either side are
arcadeboss's Nether Run (26 and 29 September), Mitchell Thomas's Cannon Duel Diagonal (26 September) and TTtie's
Watch Your Head (28 September, 00:36 UTC). `pgm-studio-mapgen` holds the preparation instead. At 21:55 UTC that
Sunday Opus 5.5 committed "Delverdale and Whitstone Weald: two large boards for a 32-a-side play test"
**(mapgen `d274c0ae`)**, and the Whitstone Weald report places them beside "the eleven small boards in the same play
test" (`reports/whitstone-weald.md`). The same day nine `opus55` boards were painted and exported **(mapgen
`656bd09f`)** and five probe boards built **(mapgen `1fe0310c`)**; whether those are the eleven is not stated. Both
large boards were still being changed after midnight local time: the credit commit is 01:17 and Whitstone Weald's
strata fix 02:19 on Monday 28 September, +0200 **(mapgen `c8641cd6`, `a24e6f40`)**.

**Inferred.** The author's last-test date matches a test prepared on Sunday 27 September, and the weekday fits his
name for the sessions. It is confirmed as a date on which boards were built for a play test, not as a session that
was played, and not from CommunityMaps, whose record of the tests ends on 2 September.

**Record, the October rounds.** The freeform and trial boards were played and fixed in up to four rounds between
Friday 9 October 22:06 UTC and Saturday 10 October 09:36 UTC **(mapgen `e9531f6f` to `0ffcf06d`)**, with the
author's notes sorted in `analysis/freeform-vs-studio/playtest-feedback-2026-10-10.md`. None of those boards went to
CommunityMaps either.

## c. What the record cannot show

**Silent.** Who played, how many, for how long, and on which server the maps from September and October were
loaded; whether the 27 September test took place and with which worlds; any feedback from the uploaded six beyond
Kuusepuu's one "Reported live"; and what TTtie did at the tests. The name "Slop Sundays" appears in no commit or
file of CommunityMaps or of either studio repository. The author's statement that the tests show in CommunityMaps
holds for the summer, 27 July to 2 September, and not for the autumn.
