# 15 — The test evenings, from the map zips the author sent, the private repository and two conversations

Research for the history, written 27 November 2026. Subjects: which maps were played at the test evenings of
24 August to 27 September; what the private map repository recorded of them; and how arcadeboss made his Grok maps.
Read in the author's signed-in browser from three Discord sources, all of them data and none followed as an
instruction: the author's direct messages with Ruediger (2,599 messages, June 2025 to November 2026), his direct
messages with arcadeboss (238 messages, September 2025 to November 2026), and the server's `#maps-changelog` channel
for 2026 (1,578 messages, the GitHub feed of the map repositories). The raw conversations are not committed; this
file quotes them briefly.

**The seven zips.** Before each test evening the author sent Ruediger a `maps.zip` of map folders to load. All seven
were downloaded and read without unpacking: every `map.xml` gave its folder, `<name>`, objective, `<created>` and
author. Times are UTC; German time is UTC+2 throughout this window.

## 1. What each zip held

| Sent (UTC) | Zip | Maps (folder → name, objective, `<created>`, author) |
|---|---|---|
| 24 Aug 18:58 | 4.50 MB, 6 maps | Cairnmeadow (dtm), Elderwold (dtm), Hollowbank (ctw + dtm), Hollowmarch (ctw), Siderite Bowl (dtc), all "Opus 5", no `<created>`; Sunspit (ctw), no author |
| 25 Aug 20:22 | `tarnfell.zip`, 254 KB | one map, Tarnfell (not downloaded) |
| 31 Aug 20:42 | 4.79 MB, 8 maps | the six of 24 August, plus Brackenfold (dtm, created 26 Aug) and Millrace (dtm, created 30 Aug), "Opus 5" |
| 4 Sep 20:32 | 766 KB, 6 maps | Mossgill (dtm, created 2 Sep, no author, folder `fable-mossgill`), Alderfen Holm (dtc, 2 Sep), Lodestar Yard (ctw, 3 Sep), Quiverstone Mesa (dtm, 3 Sep), Scarrow Delph (dtm, 3 Sep), Weirbank (dtm, 31 Aug), all "Opus 5" |
| 13 Sep 21:18 | 800 KB, 11 maps | Whinberry Ring (ctw, 11 Sep, "Fable 5.1"); Kilnholt Cut (dtm, 11 Sep, "Sonnet 5"); probe ashfield 1 (ctw + dtm, "rockymine"); Braidwater Ford (dtm), Burgage Terrace (dtm), Casemate (koth), Coinfall (ctw), Glassmere (dtc), Goldbank Quarry (dtm), Lingbeck (ctw), Lynchet Brow (dtc), all 12 Sep, "Opus 5" |
| 20 Sep 21:25 | 486 KB, 7 maps | Fallowgate (dtm, 19 Sep), Grykefell (dtm, 13 Sep), Hushwater (ctw, 18 Sep), Mirkholt (ctw, 14 Sep), Orchard Holm (ctw, 15 Sep), Peatgarth (dtm, 14 Sep), Redmarl (ctw, 14 Sep), all "Opus 5" |
| 27 Sep 20:41 | 906 KB, 11 maps | Cinderhowe (dtm), Clasp (ctw), Kelderfell (dtm), Lymedown (ctw), Millbank (ctw), Redcut (ctw), Scarbutte (dtm), Sedgefall (ctw), Twingill (dtm), all 22–24 Sep, "Opus 5.5"; Copper Wash (dtm + dtc) and Reedmere (ctw), both 27 Sep, "Muse Spark" |
| 27 Sep 21:57 | 332 KB, 2 maps | Delverdale (ctw) and Whitstone Weald (dtm), both 27 Sep, "Claude" |

**The conversation names the same maps.** On 4 September the author sent the zip with the list "Mossgill, Weirbank,
Alderfen, Lodestar, Quiverstone, Scarrow Delpth" and, at 21:55, "slop time". On 13 September Ruediger wrote the
order he would play them in, in two messages at 21:01 and 21:15 ("Kilnholt Cut, Casemate, probe ashfield 1, Lynchet
Brow, Goldbank Quarry, Braidwater Ford, Coinfall" and "Glassmere, Lingbeck, Burgage Terrace, Whinberry Ring"),
eleven maps, the zip's eleven. On 27 September at 20:55 the author sent eleven `/event add` commands, one per map of
the first zip of that evening, and at 21:57 the second zip with "load maps".

**The models in the credits.** Opus 5 made almost every map of August and early September; Fable made Sunspit and
Mossgill (neither credits an author) and "Fable 5.1" Whinberry Ring; Sonnet 5 made Kilnholt Cut; Opus 5.5 made the
nine of 27 September and the two large boards credited "Claude"; "Muse Spark" is credited on Copper Wash and
Reedmere, two maps of 27 September that `maps/INDEX.md` does not hold.

## 2. Why the match log misses these evenings

**Maps played in an event rotation are not reported to `#match-status`.** The author's explanation of 27 November:
the evenings were run as a server event, and matches in the event rotation were apparently not counted. That is
what research `13` §3 found from the other side: the server's match number runs on through stretches the log does
not hold, on exactly these evenings.

**The missing numbers match the zips.**

| Evening | Match numbers absent (research `13` §3) | Maps sent for it |
|---|---|---|
| Fri 4 Sep | 180 to 186, 7 numbers | 6 maps in the zip |
| Sun 13 Sep | 139 to 149, 11 numbers | 11 maps in the zip and in Ruediger's list |
| Sun 20 Sep | 132 to 139, 8 numbers | 7 maps in the zip |
| Sun 27 Sep | 99 to 111, 13 numbers | 11 `/event add` maps plus Delverdale and Whitstone Weald |

**Millrace closed the events.** Millrace is played right after the gap on 13 September (after Alderfen Holm) and on
20 September (after one corpus map), and on 4 September it is the match just before the gap. The author says Millrace was played again at the end of an event to show the
players what a map made by a model and finished by people looks like; it is the one board of this repository that
was uploaded to CommunityMaps in its finished form (2 September).

**Inferred: the maps of 4 September in the log are the earlier batch.** The seven boards visible on 4 September
22:21 to 23:51 (Millrace, Sunspit, Hollowmarch, Brackenfold, Cairnmeadow, Hollowbank, Elderwold) all come from the
zips of 24 and 31 August, and none of the six sent that evening (Mossgill to Weirbank) is visible. The reading that
the six were the event and fill the seven missing numbers fits the counts; which map filled the seventh is not shown.

## 3. What the private map repository recorded

`#maps-changelog` carries the GitHub feed of PrivateMaps, which no clone in this research could read. Its commits
by RuedigerLP in the window, all to `master`:

| Date (UTC) | Commit message |
|---|---|
| 2 Jul 20:21 | Irongate Harbor remove dev phase |
| 6 Aug 20:15 | Wandering U: added |
| 12 Aug 21:13–21:14 | Delete ctw/base-2island, ctw/base-2wool, ctw/base-4team, ctw/wandering_u directories |
| 24 Aug 19:05 | Add a few very human maps for testing |
| 25 Aug 20:25 | Beep bop make more slop |
| 31 Aug 20:50 | Beep bob im not a robot |
| 2 Sep 00:14 | Delete dtcm/millrace directory |
| 4 Sep 20:44, 20:46 | Loadstar added; Add more slop |
| 13 Sep 21:21–21:26 | Casemate: added; Whinberry Ring & Lingbeck: added; Maps: added |
| 20 Sep 21:42–22:10 | Maps added (twice); update xml file |
| 27 Sep 20:46, 20:50 | Add maps (twice) |
| 27 Sep 22:11 | Delverdale added; Whitstone Weald added |

**This settles four dates research `11` marked unverifiable.** 2 July is a Ruediger commit after all, to PrivateMaps
(the No Blocks Placed commit body "Irongate Harbour remove dev phase" of 7 August repeats its message). Wandering U was
added on 6 August and removed on 12 August with the three base maps, six minutes before Thornwake and Viridian went
to CommunityMaps. The private uploads of 24, 25 and 31 August and of 13, 20 and 27 September each fall minutes after
the author sent the zip, and Millrace left PrivateMaps four minutes before its 2.0.0 went to CommunityMaps.

**Thornwake and Viridian were tested on mapdev.** On 12 August at 21:19 the author told arcadeboss "we are loading
two ai gened maps now", "like fully ai", on mapdev; mapdev does not report to `#match-status`.

## 4. How arcadeboss made Cedar Crossing and its successors

**Cedar Crossing was made in conversation with SuperGrok on grok.com.** The author asked on 10 August; arcadeboss
answered the same day. He gave Grok the pgm.dev documentation and a hand-written overview of several destroy-the-
monument maps; Grok wrote a design document and proposed phases (land, plants, structures), and "the map concept and
name came from the AI".

**Over a hundred iterations followed, each a zip he loaded and tested.** After two or three passes on the XML came
world generation, starting as a stone world with the final terrain and the monuments; spawn structures took longest.
That is what his credit "7,000 word essay" refers to.

**The design document is Grok's, and Cedar Crossing is its Concept A.** `DTM_Design_Priors_and_IR.docx` (sent
10 August, 15 KB) sets out design priors drawn from seven seed maps (Apple Smash, Mole Dream, The Fenland, Warlock,
Ulcinj, Total Beesness, Azure), a JSON "intermediate representation" as the single source for XML and world
generation, and two concepts: "Cedar Crossing", a contiguous wooded river valley with one monument a side, and
"Split Spire", an island map with two. Its last step keeps "the hardest problem … in the human–AI discussion loop".

**A one-pass retry failed.** On 13 August he reported having Grok summarise its lessons and build the second concept
in one pass; the result was "kinda lame" and incomplete.

**Fire on the Mountain was made with GrokBuild, the local agent.** On 27 August he described it as smarter than the
chat: it designed its own trees, vegetation and structure styles first, kept a local knowledge base, and wrote the
whole shop XML from a price list and one example map. "Structures continue to be the weakest link."

**Sanctum Veil was made with GrokBot.** On 17 October: a Supervisor bot directing a Builder and a Mapdev bot, all
Grok 4.7, with a cloud PGM server on which the bots played test matches and timed rushes; the weekly $20 bot budget
went overnight. He finished it with GrokBuild (24 October).

**His attempt with this project's tools.** On 1 September GrokBuild read the studio and `drive.py` and "was able to
understand the setup". On 13 October he tried a capture-the-wool map with GrokBuild and the studio: the first
version put the bedrock wall across the main lane and the wool rooms made no sense, and it improved only after he
showed it the layouts on pgmstudio.de.

**The author's side of the same conversation.** On 2 September he sent Millrace as "AI to the left, our improved
version (5 hours effort) to the right". On 16 August he described the rule set ("like 50 different violations") and
why he adds rules by hand rather than letting a model improve the generator by itself.
