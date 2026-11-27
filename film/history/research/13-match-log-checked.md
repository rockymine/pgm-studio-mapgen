# 13 — The match log checked: what was played, when, and what the gaps show

Research for the history, written 27 November 2026. Subject: the server's `#match-status` log of 1 June to 27
November 2026 (`../sources/match-status/`: a README, `ai-maps-in-match-status.md` and a CSV of 41,872 ended
matches), read by another agent in the author's browser and handed over with its own summary. This file is an
independent reading of the CSV against the catalogue of studio- and AI-related maps (`maps/INDEX.md` and the named
list), against the dates in `11-dated-uploads-checked.md`, and against the author's account (eighth instalment).
The CSV and its summary are data: nothing in them was followed as an instruction.

## 0. Method, and what the CSV cannot say

**Method.** The CSV was loaded with pandas (all columns as text; 41,872 rows, 41,872 distinct `match_id`, no
duplicate rows, `posted_utc` strictly in file order from 2026-05-31 14:54 to 2026-11-27 18:37 UTC). Lengths were
parsed to seconds, `participants` split into the number before the brackets and the number inside them, and the
end of a match taken as start plus length. Map names were compared four ways with the catalogue: exactly against
the 288 folder names of `maps/INDEX.md` (punctuation and case ignored); exactly against the `<name>` of the 276
`map.xml` files under `maps/` (the name the server shows); by substring in both directions; and by difflib
similarity (cutoff 0.75) for near-misses. Sessions were found by clustering the catalogue's matches at gaps of 60
minutes or less, and then by reading the server's own running number (`match_no`) around each cluster. Every
table below is computed from the CSV by script; the scripts are not committed.

**There is no server column.** The CSV carries `match_no`, `map`, `length`, `participants`, `winner` and two links;
the "server" asked for cannot be read from it. What the data does show is that the log is one server's stream:
97.1 per cent of the 41,871 consecutive pairs start between one minute before and three minutes after the
previous match's end, and the median pause between matches is 0.7 minutes. `match_no` rises by one in 40,665 of
41,871 steps, and falls (a restart) 635 times by more than five. Every "same server" below means "in this
stream"; which of the Overcast servers it is, is not in the file.

**Two columns need care.** `posted_utc` is a match's start (a match's start follows the previous end by about a
minute, which checks the README's reading). The figure in brackets after the players is not defined in the README
("players (number in brackets)"); it runs 0 to 7 and is reported as given. Berlin time is UTC+2 to 25 October and
UTC+1 after.

**The log is not complete, and the gaps are part of the finding (section 3).** Between two consecutive rows of one
series `match_no` normally rises by one. Where it rises by more and the clock shows an unexplained pause, matches
were played that the CSV does not hold. Section 3 lists them; they fall on the author's test dates.

## 1. a. Every match on a catalogue map

**Which names were found.** Of the 288 worlds in `maps/INDEX.md`, **ten** appear in the log under their own
name, by folder name and by the `<name>` in their `map.xml` alike: Hollowmarch, Hushwater, Sunspit, Viridian,
Alderfen Holm, Brackenfold, Cairnmeadow, Elderwold, Millrace and Hollowbank, with 15 matches. Of the named list,
found are Base 4-Team (new: 1 match), Bridgid II (8), Vauxite (1), Drastic Change II (1), Kuusepuu CTC (2), No
Blocks Placed (14), Cedar Crossing (22), Countryside (7) and 803 (7). Capture the Wool CTW (6), one of the three maps
of the 24 June upload, is shown too. That is 78 matches on the catalogue's maps (15 + 63) and 84 with Capture the Wool
CTW. The other agent's summary covers 114 matches including 31 on arcadeboss's Grok maps (Alligator Charge, Nether
Run, Fire on the Mountain, Hot Potato, Xavier's Mansion, Sanctum Veil, Blocker), which are outside this catalogue
and are used below only as context for the sessions; the sum of the two is 115.

**Never found.**

| Expected | What the log holds instead | Reading |
|---|---|---|
| Wandering U | no name containing "Wander"; the nearest by spelling are Annealing (24 matches) and Haunted Rings, neither of which is it | never in the stream. The author says it was tested on 6 August. A 26-minute pause with one missing number on Thursday 6 August (19:46 to 20:11 UTC, section 3) is the only trace in the right hour, and is a lead, not a find |
| Hello World Micro (also "Mini") | "Hello World" once, 17 July 19:39 UTC, winner Pink | not the Micro: the Micro came out on 27 July, and Pink means four teams. Two match numbers are missing from 23:13 to 23:30 UTC on 27 July, the hour after the Micro's upload at 23:10 UTC |
| Thornwake | Thornwood (14) | different map |
| Delverdale, Whitstone Weald | Belvedere (20), Wit's End (34) | different maps; the boards of the 27 September test do not appear (section 3) |
| Scarrow Delph | Scareros (1), Cannon Duel (11) | never played in this stream |
| Gypsum Reach, Heftfold, Whinberry Ring, Overwall, Riftwater, Goldhollow, Ridgeway | Rift (3) and Rift II (1) are corpus maps, nothing else is near | never in the stream |
| The other 278 worlds of `maps/INDEX.md` | no exact name | never in the stream (near-misses below) |

**Near-miss names, none of them the catalogue's map.**

| Catalogue name | Appears as | Matches | Why it is not the board |
|---|---|---|---|
| Brittlebush III, Brittlebush KotH | Brittlebush; Brittlebush II | 112; 3 | earlier corpus maps (2022, 2023); Brittlebush III itself does not appear, as the author says |
| Hollowbeck | Hollowbank | 1 | Hollowbank is its own catalogue board and is counted |
| ClayClay Redux | ClayClay | 122 | the original corpus map |
| Tanglewold | Tangled | 2 | different map |
| map experiment (`dtcm/map_experiment`) | Experiment 12 | 176 | different map |
| Thunder / Thunderstorm reconstructions | Thunder; Thunderstorm | 42; 1 | the corpus originals the boards reconstruct |
| Kuusepuu CTC | Kuusepuu | 38 | the original map; the cake conversion has its own name in the log |
| Drastic Change II | Drastic Change | 2 | the earlier map (9 August, 11 September) |
| Base 4-Team | Research Base | 1 (4 Nov, 5 players) | a map of its own name; not a catalogue name, not counted |
| Hello World Micro | Hello World | 1 | the 2025 map, see above |

**Per map.**

| Map | Matches | First (UTC) | Last (UTC) | Median length | Longest |
|---|---|---|---|---|---|
| Hollowmarch | 3 | 2026-08-31 21:18 | 2026-09-27 03:04 | 3m 33s | 3m 39s |
| Hushwater | 1 | 2026-09-27 02:54 | 2026-09-27 02:54 | 9m 23s | 9m 23s |
| Sunspit | 1 | 2026-09-04 23:04 | 2026-09-04 23:04 | 10m 20s | 10m 20s |
| Viridian | 1 | 2026-10-16 02:57 | 2026-10-16 02:57 | 3m 16s | 3m 16s |
| Alderfen Holm | 1 | 2026-09-13 22:56 | 2026-09-13 22:56 | 6m 28s | 6m 28s |
| Brackenfold | 1 | 2026-09-04 23:19 | 2026-09-04 23:19 | 15m 15s | 15m 15s |
| Cairnmeadow | 1 | 2026-09-04 23:36 | 2026-09-04 23:36 | 7m 43s | 7m 43s |
| Elderwold | 1 | 2026-09-04 23:50 | 2026-09-04 23:50 | 1m 08s | 1m 08s |
| Millrace | 4 | 2026-09-02 00:28 | 2026-09-20 22:46 | 9m 32s | 13m 26s |
| Hollowbank | 1 | 2026-09-04 23:45 | 2026-09-04 23:45 | 4m 11s | 4m 11s |
| Base 4-Team | 1 | 2026-07-28 00:30 | 2026-07-28 00:30 | 2m 36s | 2m 36s |
| Bridgid II | 8 | 2026-07-15 22:13 | 2026-11-23 02:02 | 4m 02s | 4m 41s |
| Vauxite | 1 | 2026-10-12 02:28 | 2026-10-12 02:28 | 5m 42s | 5m 42s |
| Drastic Change II | 1 | 2026-10-12 02:35 | 2026-10-12 02:35 | 15m 35s | 15m 35s |
| Kuusepuu CTC | 2 | 2026-07-31 21:20 | 2026-10-29 01:54 | 20m 44s | 22m 57s |
| No Blocks Placed | 14 | 2026-08-11 21:50 | 2026-11-27 03:45 | 4m 39s | 9m 38s |
| Cedar Crossing | 22 | 2026-08-10 23:53 | 2026-11-20 19:12 | 5m 22s | 45m 18s |
| Countryside | 7 | 2026-11-04 17:35 | 2026-11-19 15:20 | 3m 46s | 11m 01s |
| 803 | 7 | 2026-10-19 23:00 | 2026-11-23 21:06 | 8m 52s | 1h 23m 36s |
| Capture the Wool CTW | 6 | 2026-06-28 02:45 | 2026-11-03 18:52 | 8m 12s | 16m 46s |
**Every match, in time order.** Start in UTC; Berlin is the local clock; No. is the server's running match number.

| UTC date | Start UTC | Berlin | No. | Map | Length | Players (bracket) | Winner |
|---|---|---|---|---|---|---|---|
| 2026-06-28 Sun | 02:45 | 04:45 | 131 | Capture the Wool CTW | 16m 46s | 31 (4) | Red |
| 2026-07-15 Wed | 22:13 | 00:13 +1d | 233 | Bridgid II | 4m 25s | 19 (3) | Blue |
| 2026-07-17 Fri | 19:07 | 21:07 | 159 | Bridgid II | 4m 41s | 23 (4) | Blue |
| 2026-07-27 Mon | 20:55 | 22:55 | 119 | Bridgid II | 2m 54s | 31 (6) | Red |
| 2026-07-28 Tue | 00:30 | 02:30 | 153 | Base 4-Team | 2m 36s | 28 (7) | Green |
| 2026-07-31 Fri | 21:20 | 23:20 | 145 | Kuusepuu CTC | 22m 57s | 47 (5) | Red |
| 2026-08-07 Fri | 19:17 | 21:17 | 74 | Bridgid II | 4m 28s | 40 (6) | Blue |
| 2026-08-10 Mon | 23:53 | 01:53 +1d | 167 | Cedar Crossing | 5m 26s | 22 (6) | Red |
| 2026-08-11 Tue | 21:50 | 23:50 | 151 | No Blocks Placed | 3m 46s | 39 (4) | Blue |
| 2026-08-11 Tue | 21:55 | 23:55 | 152 | Bridgid II | 4m 5s | 34 (5) | Blue |
| 2026-08-12 Wed | 03:46 | 05:46 | 203 | Cedar Crossing | 5m 3s | 39 (4) | Red |
| 2026-08-12 Wed | 22:03 | 00:03 +1d | 170 | No Blocks Placed | 4m 44s | 30 (6) | Blue |
| 2026-08-12 Wed | 22:09 | 00:09 +1d | 171 | Cedar Crossing | 15m 20s | 39 (5) | Red |
| 2026-08-12 Wed | 22:25 | 00:25 +1d | 172 | Bridgid II | 2m 39s | 34 (6) | Red |
| 2026-08-14 Fri | 20:16 | 22:16 | 125 | No Blocks Placed | 3m 26s | 22 (1) | Blue |
| 2026-08-15 Sat | 16:11 | 18:11 | 102 | Cedar Crossing | 11m 55s | 28 (2) | Red |
| 2026-08-16 Sun | 02:03 | 04:03 | 154 | No Blocks Placed | 9m 38s | 32 (5) | Red |
| 2026-08-18 Tue | 20:11 | 22:11 | 25 | Cedar Crossing | 1m 8s | 21 (4) | Red |
| 2026-08-21 Fri | 01:59 | 03:59 | 30 | Cedar Crossing | 19m 42s | 32 (2) | Red |
| 2026-08-22 Sat | 19:20 | 21:20 | 56 | No Blocks Placed | 2m 19s | 29 (2) | Red |
| 2026-08-26 Wed | 18:20 | 20:20 | 127 | Cedar Crossing | 1m 7s | 17 (1) | Red |
| 2026-08-28 Fri | 23:39 | 01:39 +1d | 151 | No Blocks Placed | 8m 9s | 30 (3) | Red |
| 2026-08-31 Mon | 21:18 | 23:18 | 143 | Hollowmarch | 3m 39s | 20 (3) | Blue |
| 2026-09-01 Tue | 17:56 | 19:56 | 24 | Cedar Crossing | 45m 18s | 41 (3) | Red |
| 2026-09-02 Wed | 00:28 | 02:28 | 69 | Millrace | 6m 27s | 21 (2) | Blue |
| 2026-09-04 Fri | 22:21 | 00:21 +1d | 179 | Millrace | 13m 26s | 44 (3) | Red |
| 2026-09-04 Fri | 23:04 | 01:04 +1d | 187 | Sunspit | 10m 20s | 30 (5) | Red |
| 2026-09-04 Fri | 23:16 | 01:16 +1d | 188 | Hollowmarch | 2m 49s | 26 (5) | Red |
| 2026-09-04 Fri | 23:19 | 01:19 +1d | 189 | Brackenfold | 15m 15s | 51 (6) | Blue |
| 2026-09-04 Fri | 23:36 | 01:36 +1d | 190 | Cairnmeadow | 7m 43s | 42 (6) | Red |
| 2026-09-04 Fri | 23:45 | 01:45 +1d | 191 | Hollowbank | 4m 11s | 40 (6) | Red |
| 2026-09-04 Fri | 23:50 | 01:50 +1d | 192 | Elderwold | 1m 8s | 27 (6) | Blue |
| 2026-09-06 Sun | 22:05 | 00:05 +1d | 142 | No Blocks Placed | 3m 42s | 32 (4) | Blue |
| 2026-09-07 Mon | 18:13 | 20:13 | 157 | Cedar Crossing | 7m 31s | 27 (2) | Blue |
| 2026-09-11 Fri | 23:56 | 01:56 +1d | 220 | Bridgid II | 3m 59s | 33 (5) | Red |
| 2026-09-13 Sun | 22:56 | 00:56 +1d | 150 | Alderfen Holm | 6m 28s | 40 (6) | Red |
| 2026-09-13 Sun | 23:03 | 01:03 +1d | 151 | Millrace | 4m 28s | 33 (7) | Red |
| 2026-09-20 Sun | 22:46 | 00:46 +1d | 140 | Millrace | 12m 38s | 44 (3) | Blue |
| 2026-09-20 Sun | 23:14 | 01:14 +1d | 143 | No Blocks Placed | 5m 30s | 28 (2) | Red |
| 2026-09-22 Tue | 01:28 | 03:28 | 144 | Cedar Crossing | 4m 10s | 26 (2) | Blue |
| 2026-09-27 Sun | 02:54 | 04:54 | 3 | Hushwater | 9m 23s | 25 (1) | Red |
| 2026-09-27 Sun | 03:04 | 05:04 | 4 | Hollowmarch | 3m 33s | 18 (1) | Red |
| 2026-10-04 Sun | 04:01 | 06:01 | 182 | Cedar Crossing | 1m 7s | 17 (3) | Blue |
| 2026-10-04 Sun | 22:09 | 00:09 +1d | 141 | No Blocks Placed | 6m 29s | 38 (3) | Blue |
| 2026-10-11 Sun | 03:56 | 05:56 | 20 | Cedar Crossing | 5m 19s | 25 (4) | Red |
| 2026-10-12 Mon | 02:28 | 04:28 | 14 | Vauxite | 5m 42s | 27 (2) | Purple |
| 2026-10-12 Mon | 02:35 | 04:35 | 15 | Drastic Change II | 15m 35s | 26 (3) | Blue |
| 2026-10-13 Tue | 01:15 | 03:15 | 32 | Cedar Crossing | 1m 20s | 21 (0) | Blue |
| 2026-10-16 Fri | 02:45 | 04:45 | 155 | Capture the Wool CTW | 10m 39s | 32 (1) | Blue |
| 2026-10-16 Fri | 02:57 | 04:57 | 156 | Viridian | 3m 16s | 28 (1) | Red |
| 2026-10-16 Fri | 03:02 | 05:02 | 157 | Cedar Crossing | 5m 5s | 27 (1) | Blue |
| 2026-10-18 Sun | 16:30 | 18:30 | 64 | Cedar Crossing | 12m 57s | 39 (5) | Blue |
| 2026-10-18 Sun | 21:39 | 23:39 | 89 | No Blocks Placed | 3m 27s | 35 (2) | Blue |
| 2026-10-19 Mon | 23:00 | 01:00 +1d | 183 | 803 | 6m 24s | 25 (2) | Blue |
| 2026-10-20 Tue | 19:57 | 21:57 | 148 | 803 | 1h 23m 36s | 37 (2) | Red |
| 2026-10-24 Sat | 03:04 | 05:04 | 75 | Capture the Wool CTW | 7m 36s | 28 (3) | Red |
| 2026-10-24 Sat | 22:56 | 00:56 +1d | 83 | No Blocks Placed | 4m 28s | 43 (7) | Red |
| 2026-10-25 Sun | 23:13 | 00:13 +1d | 94 | Cedar Crossing | 2m 46s | 26 (3) | Red |
| 2026-10-26 Mon | 00:37 | 01:37 | 108 | Capture the Wool CTW | 8m 49s | 38 (3) | Red |
| 2026-10-27 Tue | 00:20 | 01:20 | 109 | Cedar Crossing | 20m 14s | 33 (0) | Blue |
| 2026-10-27 Tue | 20:00 | 21:00 | 75 | 803 | 10m 42s | 35 (3) | Red |
| 2026-10-29 Thu | 01:54 | 02:54 | 69 | Kuusepuu CTC | 18m 32s | 31 (1) | Red |
| 2026-10-29 Thu | 02:13 | 03:13 | 70 | Capture the Wool CTW | 4m 31s | 24 (1) | Blue |
| 2026-10-30 Fri | 01:03 | 02:03 | 61 | Cedar Crossing | 16m 39s | 26 (3) | Blue |
| 2026-10-30 Fri | 21:09 | 22:09 | 23 | No Blocks Placed | 5m 25s | 40 (1) | Blue |
| 2026-11-03 Tue | 18:52 | 19:52 | 74 | Capture the Wool CTW | 3m 43s | 15 (1) | Red |
| 2026-11-04 Wed | 17:35 | 18:35 | 51 | Countryside | 6m | 12 (1) | Red |
| 2026-11-04 Wed | 22:29 | 23:29 | 87 | 803 | 17m 16s | 27 (0) | Blue |
| 2026-11-05 Thu | 19:09 | 20:09 | 89 | Cedar Crossing | 1m 30s | 22 (2) | Blue |
| 2026-11-08 Sun | 04:46 | 05:46 | 114 | Cedar Crossing | 4m 42s | 23 (3) | Red |
| 2026-11-08 Sun | 10:57 | 11:57 | 169 | Countryside | 5m 43s | 13 (1) | Blue |
| 2026-11-09 Mon | 17:20 | 18:20 | 65 | Countryside | 3m 28s | 14 (1) | Blue |
| 2026-11-10 Tue | 16:38 | 17:38 | 24 | Countryside | 3m 4s | 8 (2) | Blue |
| 2026-11-11 Wed | 17:54 | 18:54 | 46 | Cedar Crossing | 6m 38s | 26 (2) | Red |
| 2026-11-12 Thu | 19:52 | 20:52 | 81 | Countryside | 3m 46s | 14 (1) | Blue |
| 2026-11-16 Mon | 00:08 | 01:08 | 68 | No Blocks Placed | 4m 35s | 29 (2) | Red |
| 2026-11-16 Mon | 15:19 | 16:19 | 22 | Countryside | 2m 19s | 13 (1) | Blue |
| 2026-11-16 Mon | 20:05 | 21:05 | 68 | 803 | 8m 12s | 23 (1) | Blue |
| 2026-11-17 Tue | 20:24 | 21:24 | 77 | 803 | 8m 52s | 25 (3) | Red |
| 2026-11-19 Thu | 15:20 | 16:20 | 69 | Countryside | 11m 1s | 18 (2) | Blue |
| 2026-11-20 Fri | 19:12 | 20:12 | 123 | Cedar Crossing | 21m 33s | 33 (3) | Blue |
| 2026-11-23 Mon | 02:02 | 03:02 | 119 | Bridgid II | 2m 3s | 31 (5) | Blue |
| 2026-11-23 Mon | 21:06 | 22:06 | 146 | 803 | 3m 35s | 22 (1) | Blue |
| 2026-11-27 Fri | 03:45 | 04:45 | 196 | No Blocks Placed | 6m 56s | 19 (3) | Blue |

## 2. b. Test sessions

**What the visible log holds is one clear block and several short ones.** A block is a run of this catalogue's
matches at gaps of an hour or less. Counting only matches the CSV holds, there is one block of more than three
maps, Friday 4 September, and eight shorter ones. Grok maps by arcadeboss that fall inside are named in brackets;
they are not the catalogue's.

| Block | Weekday, UTC date | Start to end UTC (Berlin) | Maps in order (match no.) | Players per match | Length per match |
|---|---|---|---|---|---|
| 1 | Tue 11 Aug | 21:50 to 21:59 (23:50 to 00:00) | No Blocks Placed (151), Bridgid II (152) | 39, 34 | 3m 46s, 4m 05s |
| 2 | Wed 12 Aug | 22:03 to 22:28 (00:03 to 00:28 Thu) | No Blocks Placed (170), [Cedar Crossing] (171), Bridgid II (172) | 30, 39, 34 | 4m 44s, 15m 20s, 2m 39s |
| 3 | Fri 4 Sep | 22:21 to 23:51 (00:21 to 01:51 Sat) | Millrace (179); numbers 180 to 186 absent; Sunspit (187), Hollowmarch (188), Brackenfold (189), Cairnmeadow (190), Hollowbank (191), Elderwold (192) | 44, 30, 26, 51, 42, 40, 27 | 13m 26s, 10m 20s, 2m 49s, 15m 15s, 7m 43s, 4m 11s, 1m 08s |
| 4 | Sun 13 Sep | 22:56 to 23:08 (00:56 to 01:08 Mon) | Alderfen Holm (150), Millrace (151); numbers 139 to 149 absent before them | 40, 33 | 6m 28s, 4m 28s |
| 5 | Sun 20 Sep | 22:46 to 23:19 (00:46 to 01:19 Mon) | Millrace (140), two other maps (141, 142), No Blocks Placed (143); numbers 132 to 139 absent before them | 44, 28 | 12m 38s, 5m 30s |
| 6 | Sun 27 Sep | 02:54 to 03:08 (04:54 to 05:08) | Hushwater (3), Hollowmarch (4), after a server restart at 02:22 | 25, 18 | 9m 23s, 3m 33s |
| 7 | Mon 12 Oct | 02:28 to 02:51 (04:28 to 04:51) | Vauxite (14), Drastic Change II (15) | 27, 26 | 5m 42s, 15m 35s |
| 8 | Fri 16 Oct | 02:45 to 03:07 (04:45 to 05:07) | Capture the Wool CTW (155), Viridian (156), [Cedar Crossing] (157) | 32, 28, 27 | 10m 39s, 3m 16s, 5m 05s |
| 9 | Thu 29 Oct | 01:42 to 02:18 (02:42 to 03:18) | [Nether Run] (67), number 68 absent, Kuusepuu CTC (69), Capture the Wool CTW (70) | 21, 31, 24 | 6m, 18m 32s, 4m 31s |

**Only block 3 is a session in the sense the author describes, and even it is cut.** Six of its seven maps are
consecutive on the server's counter, so they were played one after the other in 1 hour 29 minutes. Millrace, 43
minutes earlier, is not back to back with them: seven match numbers lie between its end (22:35) and the start of
Sunspit (23:04), and the pause between them is 29.7 minutes, about the length of seven short matches. The
Millrace-to-Elderwold stretch is therefore fourteen consecutive numbers, 179 to 192, of which seven are not in the
CSV. Players run from 26 to 51 per match (the other agent's "27 to 51" omits Hollowmarch's 26). Millrace, Sunspit,
Hollowmarch, Cairnmeadow and Hollowbank went to Red, Brackenfold and Elderwold to Blue.

**Blocks 4 and 5 and a 27 September evening are missing their beginnings.** Each of three consecutive Sundays has
a stretch, of 78, 54 and 99 minutes, in which the server's counter advances by 11, 8 and 13 matches that the
CSV does not hold; on 13 and 20 September it ends at the first visible map of the catalogue. They are the matches
that would make these evenings sessions. Section 3 sets them out with the other silent stretches; what they were
is not in the file.

**How many sessions, then.** Three readings, and the third is the one the evidence favours.

| Reading | Count | Dates |
|---|---|---|
| Only what the CSV holds, four or more catalogue maps in one hour | 1 | Fri 4 Sep |
| Silent stretches that end in or beside a catalogue map, in the weeks the author names | 4 | Fri 4 Sep, Sun 13 Sep, Sun 20 Sep, Sun 27 Sep |
| All silent stretches of this kind from 27 July to 27 September | 9 | 27 Jul, 7 Aug, 12 Aug, 24 Aug, 31 Aug, 4 Sep, 13 Sep, 20 Sep, 27 Sep |

**Four sessions, three of them on Sundays, fits the author's recollection of "three or four".** The dates 13, 20
and 27 September are three consecutive Sundays in UTC; read in German time each runs across midnight (23:37 to
00:56 on 13 to 14 September; 23:52 to 00:46 on 20 to 21 September; 22:58 on 27 September to 00:37 on 28
September), so they are Sunday evenings in Germany and Mondays by the time they end. The fourth, Friday 4 September,
runs 00:21 to 01:51 on Saturday in Germany. "One intensive month" fits: 4 to 27 September is 23 days, and with
the 24 and 31 August stretches the activity covers 24 August to 27 September, 35 days. "Sometimes twelve maps in a
row" fits as well: the unbroken counter stretches are 14 numbers on 4 September (179 to 192), 13 on 13 September
(139 to 151, ending with the two visible maps) and 13 on 27 September (99 to 111), of which none is fully visible.
That the last session was on 27 September fits too: the CSV holds no silent stretch of this kind after it, in the
two months to 27 November (section 3 gives the whole list).

**Comparing with the upload dates in `11-dated-uploads-checked.md`.** The author gave 24, 25 and 31 August and 13,
20 and 27 to 28 September; none could be checked in a public repository.

| Upload date he gave | What the log holds | Fit |
|---|---|---|
| 24 Aug (Mon) | silent stretch 19:07 to 19:51 UTC, six matches | same day |
| 25 Aug (Tue) | nothing: no stretch, no catalogue map | no trace |
| 31 Aug (Mon) | Hollowmarch at 21:18 UTC, its first play, after a 19-minute stretch of two matches | same day |
| 13 Sep (Sun) | the 78-minute stretch, then Alderfen Holm and Millrace | same day |
| 20 Sep (Sun) | the 54-minute stretch, then Millrace | same day |
| 27 and 28 Sep | the 99-minute stretch, 20:58 UTC to 22:37 UTC, which is 22:58 to 00:37 in Germany, across both dates | both days, one evening |

**Five of the six dates have a trace on the same day.** The one without a trace, 25
August, is a Tuesday on which the log shows no gap. The agreement of 31 August is the weakest: the stretch is two
matches, and Hollowmarch appears directly after it.

**The 27 September test was prepared and probably played.** The commit "two large boards for a 32-a-side play
test" is at 21:55 UTC (`d274c0ae` **(mapgen)**), 57 minutes into the stretch of 20:58 to 22:37 UTC. The server's
counter runs 98 (a Turf Wars match ending 20:57) to 112 (Rift at 22:37) in one series, so thirteen matches
began on this server in the 99 minutes between, and the CSV holds none of them. A long match cannot have been one
of them: thirteen starts in 99 minutes is about seven minutes each. Whether Delverdale and Whitstone Weald were
among them is not decidable from the file. The other agent's summary offers "a server that does not report";
the counter says it is the same stream, so the matches, if they were the large boards, were played here and lost
from the data, not played elsewhere.

**After 27 September the log shows no more sessions.** Block 8 (16 October) holds the only play of a board of this
project after that date, Viridian, between a Capture the Wool CTW (its first since 28 June) and Cedar Crossing;
blocks 7 and 9 hold the author's own maps and Kuusepuu CTC. None has a silent stretch before it.


## 3. Matches the log does not hold

**Where `match_no` skips and the clock stands still, matches were played that the CSV lacks.** A match number is
given when a match starts and the next match starts about a minute after the last one ends, so a stretch with
absent numbers and a long pause is a run of matches missing from the file. A single skipped number with a short
pause is common (217 forward jumps of 2 to 40 numbers in the whole log, median pause 5.6 minutes) and means
little. A skip of two or more with a pause of 15 minutes or more is rare: **14 in the whole log**. Five fall between
1 June and 26 July, nine between 27 July and 27 September, and none after 27 September. The table lists every
stretch of at least one absent number and 15 minutes between 20 June and 30 September.

| Pause, UTC (Berlin) | Weekday | Absent numbers | Pause | Map before, map after |
|---|---|---|---|---|
| 21 Jun 19:27 to 20:02 | Sun | 19 to 45 (27) | 35.3 min | Dromedary, Keipha CTW (a counter that restarts; not a clean gap) |
| 22 Jun 17:14 to 17:30 | Mon | 34 (1) | 16.8 | Mushroom Kingdoms, Rat Revolution |
| **24 Jun 21:50 to 22:16** | Wed | 72 to 74 (3) | 26.8 | Golden Drought III, Sheep CTW |
| 2 Jul 20:22 to 20:39 | Thu | 22 to 24 (3) | 17.2 | Pigland, Java II |
| 10 Jul 16:42 to 16:58 | Fri | 120 (1) | 15.8 | King Ranch, Fracture DTM |
| 12 Jul 18:36 to 19:10 | Sun | 140 (1) | 34.6 | War of the Acres, Golden Drought VI |
| **27 Jul 23:13 to 23:30** | Mon | 141, 142 (2) | 17.1 | Villa I, The Soup Bowl |
| 6 Aug 19:46 to 20:11 (21:46 to 22:11) | Thu | 88 (1) | 25.8 | Coconut Mald, Spaceship Battles |
| **7 Aug 19:00 to 19:18** | Fri | 73 (1) | 17.9 | Simplicity CTW, Bridgid II |
| 7 Aug 22:04 to 22:41 | Fri | 97 to 99 (3) | 36.9 | AMONG US, Moonlight Summit |
| **12 Aug 21:42 to 21:59** | Wed | 167, 168 (2) | 18.3 | Wholething, Battle of Tenjin II |
| 24 Aug 19:07 to 19:51 (21:07 to 21:51) | Mon | 52 to 57 (6) | 44.2 | Banana Split, Kï |
| 31 Aug 20:59 to 21:18 (22:59 to 23:18) | Mon | 141, 142 (2) | 19.2 | Exit, **Hollowmarch** |
| 4 Sep 22:35 to 23:04 (00:35 to 01:04 Sat) | Fri | 180 to 186 (7) | 29.7 | **Millrace**, **Sunspit** |
| 13 Sep 21:38 to 22:56 (23:38 to 00:56 Mon) | Sun | 139 to 149 (11) | 78.4 | Sanctum Wasser, **Alderfen Holm** |
| 20 Sep 21:52 to 22:46 (23:52 to 00:46 Mon) | Sun | 132 to 139 (8) | 54.1 | Badlands, **Millrace** |
| 27 Sep 20:58 to 22:37 (22:58 to 00:37 Mon) | Sun | 99 to 111 (13) | 99.3 | Turf Wars, Rift |

**The four stretches in bold in the first column open within two to twenty-one minutes of an upload commit.**
24 June 21:50 follows the 21:47 UTC commit of Vauxite, Capture the Wool CTW and Drastic Change II by three minutes;
27 July 23:13 the Hello World Micro commit of 23:10 by three; 7 August 19:00 the No Blocks Placed commit of 18:58
by two, with Bridgid II next; 12 August 21:42 the Viridian and Thornwake commit of 21:20 by twenty-two. Three
other commits, Bridgid II (14 July), Kuusepuu CTC (27 July 21:33 UTC) and Millrace (2 September 00:18 UTC), have no
stretch beside them; Millrace follows its commit by ten minutes in the visible log with no gap.

**Catalogue maps follow such stretches far more often than chance.** Of 84 matches on this catalogue's maps and
Capture the Wool CTW, four (Hollowmarch, Sunspit, Alderfen Holm, Millrace on 20 September) come directly after a
skip of two or more and a pause of 15 minutes or more. Across the whole log that happens before 14 of 41,872
matches, a rate of 0.033 per cent (map names in bold in the table are the catalogue's), so about 0.03 of the 84 would be expected; the chance of four or more is of the
order of 10^-8. None of the 31 Grok-map matches follows one. These are the matches that would account for
the author's "sometimes twelve maps in a row".

**What the stretches are is not decided by the file.** Three explanations fit the numbers. The reader of the channel
may have skipped a window (the README counts 57 stretches of 1 to 19 minutes in which the channel showed nothing,
and these are longer). A match whose end message took another form, as the README says 271 messages did, would be
absent from the CSV and still use a match number; maps added to the server that day are the kind that might. Or the
matches were reported by another server with the same counter. The first two would put the matches on this server;
the stretch of 27 September, with 13 numbers in 99 minutes, matches no single long match. **A re-read of Discord for
the nine stretches from 27 July (UTC times above) would settle it.**


## 4. c. The first match on a map whose layout a person did not draw

**Categories are those of `12-who-decided-what.md`, with the author's answers of the eighth instalment folded in
(section 2 of that file).** A map goes in a category by who decided its layout: 1 a person built everything; 2 a
person drew and the studio filled in; 3 a person's drawing, a model's pen; 4 an algorithm's layout, a model's spec;
5 a model's design inside the studio; 6 a model's own script. Placements marked "mine" are not in file 12; they
come from `BOARDS-BUILT.md` and the specs.

| Category | Map | First match, UTC (Berlin) | Length, players, winner | Note |
|---|---|---|---|---|
| 1 | Capture the Wool CTW | Sun 28 Jun 02:45 (04:45) | 16m 46s, 31 (4), Red | the 24 June upload with Vauxite and Drastic Change II; not itself named by the author |
| 1 | Bridgid II | Wed 15 Jul 22:13 (00:13 Thu) | 4m 25s, 19 (3), Blue | the author: concept, terrain, colour his |
| 1 | Vauxite; Drastic Change II | Mon 12 Oct 02:28; 02:35 | 5m 42s, 27 (2), Purple; 15m 35s, 26 (3), Blue | three and a half months after upload |
| 3 | Base 4-Team | Tue 28 Jul 00:30 (02:30) | 2m 36s, 28 (7), Green | the author's squared-paper unit four times over; four teams (winner Green); the first catalogue map played after the 27 July uploads |
| 3 | Kuusepuu CTC | Fri 31 Jul 21:20 (23:20) | 22m 57s, 47 (5), Red | the author: an ordinary destroy map with a cake as the objective, not an AI map |
| 2 | No Blocks Placed | Tue 11 Aug 21:50 (23:50) | 3m 46s, 39 (4), Blue | |
| 3 | Millrace | Wed 2 Sep 00:28 (02:28) | 6m 27s, 21 (2), Blue | ten minutes after the 2.0.0 commit at 00:18 UTC |
| 4 (as file 12 defines it: the first fifteen) | Viridian | Fri 16 Oct 02:57 (04:57) | 3m 16s, 28 (1), Red | the only one of the fifteen of 11 and 12 August in the log; Goldhollow and Ridgeway are not |
| 4 (mine) | Hollowmarch | Mon 31 Aug 21:18 (23:18) | 3m 39s, 20 (3), Blue | composed board, hub double-hole, seed 1233, 32 players, Opus 5 |
| 5 (mine) | Sunspit | Fri 4 Sep 23:04 (01:04 Sat) | 10m 20s, 30 (5), Red | Fable, run 3 on the live studio (16 August) |
| 6 | Cedar Crossing | Mon 10 Aug 23:53 (01:53 Tue) | 5m 26s, 22 (6), Red | arcadeboss with Grok, credited "Map and XML"; file 12 category 6 |

**The first match on a map whose layout no person drew is Cedar Crossing, on Monday 10 August 2026 at 23:53 UTC,
19 hours 53 minutes after its upload at 04:00 UTC** (22 players, 5 minutes 26 seconds, Red). It is arcadeboss's
map, not this project's, and its layout is the model's by the credits only (file 12, `?` for how it was run).
**The first for this project's own boards is Hollowmarch, Monday 31 August at 21:18 UTC**, a composed layout
(`opus5-hollowmarch`: the composer's hub and front, shifted twenty blocks).

**A caution.** Both dates are the first row in the CSV, and the log lacks matches just before Hollowmarch (31
August, 20:59 to 21:18) and just after the Viridian and Thornwake commit (12 August, 21:42 to 21:59), so an earlier
play of Hollowmarch, Viridian or Thornwake cannot be excluded.

**This corrects an earlier statement.** Kuusepuu CTC, on 31 July, was not the first AI-map test on the server. The
author does not count it as one, and Base 4-Team, which the earlier files had no record of ever being played, was on
the server three days earlier, on 28 July.


## 5. d. Durations

**Longest matches on catalogue maps.**

| Rank | Map | Mode | Start UTC | Length | Players |
|---|---|---|---|---|---|
| 1 | 803 | capture the wool (`ctw/803`) | Tue 20 Oct 19:57 | 1h 23m 36s | 37 (2), Red |
| 2 | Cedar Crossing | not in this repository | Tue 1 Sep 17:56 | 45m 18s | 41 (3), Red |
| 3 | Kuusepuu CTC | cake delivery | Fri 31 Jul 21:20 | 22m 57s | 47 (5), Red |
| 4 | Cedar Crossing | | Fri 20 Nov 19:12 | 21m 33s | 33 (3), Blue |
| 5 | Cedar Crossing | | Tue 27 Oct 00:20 | 20m 14s | 33 (0), Blue |
| 6 | Cedar Crossing | | Fri 21 Aug 01:59 | 19m 42s | 32 (2), Red |
| 7 | Kuusepuu CTC | | Thu 29 Oct 01:54 | 18m 32s | 31 (1), Red |
| 8 | 803 | | Wed 4 Nov 22:29 | 17m 16s | 27 (0), Blue |
| 9 | Capture the Wool CTW | | Sun 28 Jun 02:45 | 16m 46s | 31 (4), Red |
| 10 | Cedar Crossing | | Fri 30 Oct 01:03 | 16m 39s | 26 (3), Blue |

**The destroy-the-monument and destroy-the-core boards of this project, by their `map.xml`, were never long.**

| Board | Mode | Matches | Lengths | Longest |
|---|---|---|---|---|
| Brackenfold | dtm, 3 monuments | 1 | 15m 15s | 15m 15s (4 Sep) |
| Millrace | dtm, 5 monuments | 4 | 6m 27s, 13m 26s, 4m 28s, 12m 38s | 13m 26s (4 Sep) |
| Cairnmeadow | dtm | 1 | 7m 43s | 7m 43s |
| Alderfen Holm | dtc, 5 cores | 1 | 6m 28s | 6m 28s |
| Hollowbank | ctw with monuments | 1 | 4m 11s | 4m 11s |
| Elderwold | dtm | 1 | 1m 08s | 1m 08s |
| Scarrow Delph | dtm | 0 | none in the log | none |
| Whitstone Weald | dtm | 0 | none in the log | none |

**Nothing supports a long match on Scarrow Delph, Alderfen Holm or any destroy board of this project.** Scarrow
Delph and Whitstone Weald are not in the log at all. Alderfen Holm was played once, for 6 minutes 28 seconds,
and Cedar Crossing and 803, the two catalogue maps with a long match, are not destroy boards of this project
(803 is a capture-the-wool map, `ctw/803`; Cedar Crossing's mode is not in this repository). The longest match on a
destroy board of this project is Brackenfold's 15 minutes 15 seconds, and 51 players were in it. The log offers no match to
base a three-hour joke on.

**The silent stretches cannot hide one either.** A three-hour match would need a pause of about 180 minutes; the
longest in the weeks of the tests is 99 minutes (27 September), with 13 absent numbers, so it was thirteen
starts, not one match.

**For scale: long matches exist in the stream.** Of the whole log, 115 matches ran an hour or longer, 19 two hours
or longer, 9 three hours or longer, and the median match is 3 minutes 46 seconds. The longest is Level Up, 6h 28m
54s (4 June, 84 players); the nine of three hours or more are Level Up (five), Wrath of Cthulhu, Xi, Shroom Galaxy and
Chimeric, and none is a catalogue map. The stream's median for the catalogue's non-Grok maps is 5 minutes 22 seconds.


## 6. e. The other agent's summary against this reading

**Every row of `ai-maps-in-match-status.md` is right.** All 114 rows were compared with the CSV by `match_id`:
start minute, map, length, participants and winner agree in every case, and the 26 per-map counts, first and last
dates agree. The disagreements are of omission and interpretation.

| # | What the summary says | This reading |
|---|---|---|
| 1 | 114 matches of model-made and browser maps | **115.** Base 4-Team, played Tuesday 28 July at 00:30 UTC (2m 36s, 28 (7) players, winner Green), is missing; the table has no row for any Base map. Research `09` says nothing read "says a Base world was walked on a server"; the log says one was |
| 2 | Seven boards on 4 September "played back to back", "27 to 51 participants" | Players run **26 to 51** (Hollowmarch had 26). The seven are not all back to back: seven match numbers (180 to 186) and 29.7 minutes fall between Millrace and Sunspit |
| 3 | 57 places where the channel showed nothing for 1 to 19 minutes, "most likely quiet stretches" | the counter shows **17 stretches of 15 to 99 minutes with absent numbers between 20 June and 30 September**; those with two or more absent numbers number nine from 27 July to 27 September and none after (section 3). They are longer than 19 minutes and cluster on the test dates, so they are not quiet stretches; they are runs of matches the file lacks |
| 4 | "Clearest test session is Friday 4 September" | agreed as the clearest *visible* block; but three consecutive Sundays (13, 20, 27 September) have longer stretches of absent matches, and are the sessions the author recalls; the summary does not mention them |
| 5 | "If Delverdale and Whitstone Weald were played on 27 September, it was on a server that does not report" | the counter is one series through that evening (98, then 112, 99 minutes later), so thirteen matches began on this stream and are not in the CSV; the likelier reading is matches lost to the file, not a second server. Not decidable from the CSV |
| 6 | Sunspit: "freeform, Fable" | Sunspit is a Fable board from run 3 on the live studio (16 August; `specs/archive/sunspit` holds a plan and a refinement); "freeform" is the October generation (`freeform/lib/boards/`) |
| 7 | "The record of play runs past 2 September ... boards were played until 16 October" | agreed. 16 October is Viridian, the last board of this project |
| 8 | Millrace played "2 September (00:28 UTC, ten minutes after its 2.0.0 commit)" | agreed: commit 00:18 UTC, match 00:28 |
| 9 | Bridgid II first on 15 July; Vauxite and Drastic Change II on 12 October; 803 on 19 October, the day of 2.0.1; Countryside on 4 November | agreed in every date. 803's 2.0.1 was committed at 20:41 UTC and the match is at 23:00 UTC |
| 10 | Never found: Thornwake, Delverdale, Whitstone Weald, Hello World Micro, Wandering U, Fireball Jump | agreed for all six, and adds Scarrow Delph, Gypsum Reach, Heftfold, Whinberry Ring, Overwall, Riftwater, Goldhollow and Ridgeway |
| 11 | "The 'Hello World' of 17 July is not Hello World Micro" | agreed |
| 12 | Cedar Crossing 22 matches, 10 August to 20 November, the most played model-made map | agreed (22; first 10 Aug 23:53 UTC, last 20 Nov 19:12) |
| 13 | Kuusepuu CTC played 31 July, 47 players, four days after it was added | agreed (47 (5) players; 22m 57s; added 27 July 21:33 UTC) |

**On the other agent's own list of caveats.** It does not mention that the CSV has no server column, nor the
meaning of the bracketed figure; section 0 does.

## 7. Caveats

**Silent stretches are inference.** They rest on `match_no` and the clock. Section 3's explanation (matches the
CSV does not hold) is the reading that fits all the numbers; it is not a record of what was played.

**The weekday of a session depends on the zone.** Sunday evening for a person in Germany is Sunday evening to
Monday night in the UTC column; the table gives both.

**Not found does not mean not played.** Wandering U, Hello World Micro and the 27 September boards have no row, and
the log lacks matches on exactly the days they were played or built. Several explanations remain open.

**The log ends at 27 November 18:37 UTC.** `No Blocks Placed` at 03:45 on 27 November is the last catalogue row.

**Players are the number before the brackets.** The bracketed figure was not interpreted.

**Method is local.** The scripts that took these readings were not committed; the CSV is in `../sources/match-status/`
and the numbers above can be re-derived from it with the method of section 0.
