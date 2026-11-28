# 16 — The first test, on video, and the server's own match record

Research for the history, written 27 November 2026. Subjects: the author's screen recording of 2 July 2026, the
first time maps made with a model were played on the server; and the Overcast Community match API, which turned out
to hold every match `#match-status` left out. Times are UTC; German time is UTC+2 in this window.

**The recording.** `D:\videos\2026-07-02 21-40-20.mkv`, the author's own capture: 59 min 18 s, one video track and
one stereo audio track holding the game and the voice call together. The file name is the start in German time,
21:40:20, so recording minute 0 is 19:40:20 UTC. The clock is checked against the server twice: Pigland ends at
20:22:46 by the API and the "Cycling to Base 2-Wool in 30 seconds" banner is on screen at minute 42:30.

**In the call** were Ruediger_LP, rockymine (the author), samshaap and TTtie, by the author's word. nuttydragon, a
moderator on the server, joins at about minute 20:40, also by the author's word. The audio was transcribed with
Whisper (`large-v3-turbo`, on the CPU) and read against stills taken every 30 and 90 seconds. The transcript is not
committed, like the direct messages in research `15`; this file quotes it briefly.

**The speakers were told apart by voice and named by what they say.** A speaker model (SpeechBrain ECAPA) grouped
the spoken passages into five voices. The author is the voice that explains the studio for minutes on end. Ruediger
answers "Just do it, Rudiger do it", and samschaap answers "Sam, are you loading them?". nuttydragon is the voice
that is almost silent before minute 20; TTtie is the fifth by elimination.

**Single lines can be in the wrong group.** A quote is named below only where the voice and the content agree.

## 1. The evening, minute by minute

| Recording | UTC | What happens |
|---|---|---|
| 0:00–14:00 | 19:40–19:54 | On `mapdev.oc.tc`, the four of them walk the three Base maps: Base 2-Island (one wool a team), Base 2-Wool (two a team), Base 4-Team ("Base 4-Team by" on the scoreboard, one player a team) |
| 15:00 | 19:55 | Back on `play.oc.tc`, ordinary rotation (Smoke KotH) |
| 17:00–20:00 | 19:57–20:00 | The author cannot set a map; "No new maps found"; the maps are only on mapdev; "throw it in private for now" |
| 20:40–31:10 | 20:01–20:11 | nuttydragon joins the call; the author explains the studio to him |
| 33:00–40:10 | 20:13–20:20 | The commit message is discussed: "remove Iron Gate", "Development phase" |
| 40:41 | 20:21:01 | PrivateMaps `711e539` "Irongate Harbor remove dev phase", by RuedigerLP (`#maps-changelog`) |
| 41:06–42:30 | 20:21–20:23 | "New maps"; Base 2-Wool is set next, without a vote |
| 43:33–47:19 | 20:23:53–20:27:39 | **Base 2-Wool** on server-2, 26 players, Red wins; server poll "Rate the map we just played": 3, 21 votes |
| 48:27–53:39 | 20:28:47–20:33:59 | **Base 2-Island**, 28 players, Red wins; the poll is withdrawn |
| 54:48–58:26 | 20:35:08–20:38:46 | **Base 4-Team**, 33 players, Blue wins; poll 3, 27 votes |
| 59:18 | 20:39:38 | Recording ends on the author's "now back to the normal boring maps"; Java II starts at 20:39:55 |

**The poll scale is one to four.** The screen shows `[1] [2] [3] [4]` under the question and a final result of 3 for
both polls that ran. Of the Base 2-Island poll the chat says only samschaap's "democracy was not giving good results
so it is removed".

**The three matches are the three missing numbers.** Research `13` §3 found match numbers 22 to 24 absent from
`#match-status` between Pigland (20:22) and Java II (20:39). The API gives them: `8d8d57`, `de91ee` and `9e19f3`, the
three Base maps, in that order.

## 2. What the recording settles

**A Base world was played on a server, twice over.** Research `09` left open "whether any Base world was played on a
server". All three were walked on mapdev and then played on the public server-2, each with 26 to 33 players.

**The first load crashed mapdev, by the author's account in the call.** "The first time we loaded it on map dev we
actually crashed the server, because it was in the wrong format, and then Claude had to fix it." The fix in the
studio is `7576a6c4`, committed 23:21:34 +0200, 42 minutes after the recording ends. The fixed worlds were therefore
loaded before the fix was committed; that is an inference from the times, not something said.

**The void in one board was the drawing's, the author said.** On mapdev, about six minutes in, Ruediger asks "why is
that void?"; the author answers "It's void because I drew it exactly like that on the piece of paper. So it's my
fault." He goes on that Claude "wanted to make a simple build region". This is the squared-paper drawing of
research `09`.

**The build height was the improvement named.** "Better than Vauxite, because Vauxite had no build height in the
first test." The voice model puts this with the author, but it follows "Pretty nice, well done", so who said it is
left open. Research `11` dates Vauxite's build ceiling to its 1.0.1 of 1 July.

**The maps went in under another map's commit message.** The commit is discussed for seven minutes (Ruediger: "we'll
try to hide our crimes"), and the only PrivateMaps commit that day is `711e539`, "Irongate Harbor remove dev phase", 40
seconds before "New maps" is said. `#maps-changelog` shows the three Base folders deleted from PrivateMaps on 12 August
(research `15` §3). That `711e539` is the commit that added them is inferred; its file list was not read.

**The authors' line was empty.** The sign at the observer spawn and the map's credit read only "made by", and the
call laughs about it. nuttydragon: "who claims ownership?" and "we need updated OCC AI legislation".

## 3. How the author described the studio that evening

**He gave the layout, the model the format.** "I kind of gave the layout idea to him and then he put it into the
format." Terrain already worked; "the monuments and wool room spawns etc were missing", so he described in words how
a wool room should look and where the monuments go.

**He named three ways a map comes in.** An existing map can be uploaded and its wools and monuments are detected
and written into the XML; a new map takes a wool-room preset where a point is put on the canvas; and "there's also an
API layer behind it, so Claude just basically made a script that creates those things".

**The morning's work and the interview were both that day.** "Today I was on my phone and I told Claude Code to make
some seeds for the generation of the maps. I drew something on paper." And: "I also had like Claude Fable 5 interview
me today for like for an hour, and now we are working on a rule set and more of those AI slop maps."

**He traced the studio back to the logging plugin.** "It all started with this PGM logging plugin that was kind of
controversial a little bit", made with Claude; the movement data it collected led to wanting to generate maps, and
"there's been like three tool iterations that Claude made together with me".

**He described the editor as Figma for islands.** Polygon islands at different heights, layers, holes, elevation,
Bézier splines, rotation modes, cutting islands, aligning on anchor nodes with guidelines; "there's no prompting yet".

**He kept the evening for the grey boxes.** Asked by Ruediger during the mapdev walk to generate "something more
interesting now", he declined: "Because I want to have this moment for myself and appreciate it, and then we can do better
stuff."

**The players saw grey boxes.** A player in chat as Base 4-Team started: "is tihs jus the greybox?". In the call,
during Base 2-Island: "We are witnessing history and it's really boring."

**Ruediger praised them with a straight face.** At minute 20: "You know what I think is so beautiful about your new
maps, Rocky? How they give so much room to the imagination of the player", a canvas where players "build stuff out
of cobblestone and wood planks".

## 4. The match API

**The server keeps a public record of every match.** `api.oc.tc` redirects to its own documentation (`/docs/v2`, an
OpenAPI description inlined in the page). `GET /api/v2/matches/?page=N&size=100` lists matches newest first with
server, map, start, end, status and winner, and `GET /api/v2/matches/{id}` adds every participation and its stats.
The id is the one `oc.tc/matches/<id>` takes. No sign-in is needed.

**Every row of the Discord log is in it.** Pages 1 to 480 were read on 27 November, back to 23 May: 47,998 matches.
Of the 41,872 matches in `match-status-2026-06-01_2026-11-27.csv`, none is missing from the API.

**The API holds 388 matches on the public servers that `#match-status` never posted.** In the log's window, server-1
and server-2 have 41,871 matches in both and 388 only in the API. Another 3,628 are on the ranked servers `bolt-01`
to `bolt-03`, which the channel never reports. The 388 are committed as
`sources/match-status/api-matches-not-in-match-status.csv`.

**The 388 are the test evenings, and more.** Every map of every test evening of research `15` §1 is among them,
with the order it was played in:

| Evening (UTC) | Server | Matches | Maps in order played |
|---|---|---|---|
| 24 Jun 22:00–22:15 | server-2 | 3 | Capture the Wool CTW, Vauxite, Drastic Change II |
| 2 Jul 20:23–20:38 | server-2 | 3 | Base 2-Wool, Base 2-Island, Base 4-Team |
| 24 Aug 19:08–19:50 | server-1 | 6 | Hollowbank, Sunspit, Siderite Bowl, Hollowmarch, Cairnmeadow, Elderwold |
| 25 Aug 20:37 | server-1 | 1 | Tarnfell |
| 31 Aug 21:00–21:18 | server-2 | 2 | Brackenfold, Millrace |
| 4 Sep 22:36–23:04 | server-1 | 7 | Lodestar Yard, Scarrow Delph, Quiverstone Mesa, Lodestar Yard, Mossgill, Weirbank, Alderfen Holm |
| 13 Sep 21:39–22:55 | server-2 | 11 | Kilnholt Cut, Casemate, probe ashfield 1, Lynchet Brow, Goldbank Quarry, Braidwater Ford, Coinfall, Glassmere, Lingbeck, Burgage Terrace, Whinberry Ring |
| 20 Sep 21:53–22:45 | server-1 | 8 | Fallowgate, Orchard Holm, Peatgarth, Grykefell, Mirkholt, Peatgarth, Redmarl, Hushwater |
| 27 Sep 20:59–22:36 | server-1 | 13 | Sedgefall, Cinderhowe, Kelderfell, Scarbutte, Twingill, Reedmere, Copper Wash, Lymedown, Millbank, Clasp, Redcut, Delverdale, Whitstone Weald |

**The counts of research `15` §2 are now exact.** The missing match numbers were 7, 11, 8 and 13 on 4, 13, 20 and
27 September; the API has 7, 11, 8 and 13 unreported matches on those evenings. The extra one of 4 September is
Lodestar Yard played twice; of 20 September, Peatgarth twice.

**Two winning teams were renamed.** Copper Wash was won by a team named "Claude", Delverdale by one named
"Anti-Slop".

**Maps the log called absent were played on the public servers.** Hello World Micro on 27 July (23:29 and 23:45),
Wandering U on 6 August (20:24), Viridian and Thornwake on 12 August (21:53 and 21:59, 44 players each), Delverdale
and Whitstone Weald on 27 September, and Fireball Jump on 20 November (18:21 and 23:58). Research `15` §3 has
Thornwake and Viridian on mapdev, from the conversation with arcadeboss; they were on server-1 as well.

**The model-made maps were played more often than the log shows.** Among the 388 are further matches of Cedar
Crossing, Alligator Charge, Fire on the Mountain, Nether Run, Hot Potato, Xavier's Mansion, Sanctum Veil and Blocker,
and of No Blocks Placed (7 August), Bridgid II (14 July, twice), Kuusepuu CTC (27–28 July, three times) and
Countryside (15 October).

**The participant counts differ from the bot's.** The CSV counts distinct players with any participation; the bot's
"Participants: 17 (4)" for Pigland is 20 distinct players in the API. Compare counts within one source only.
