# The match-status log, 1 June to 27 November 2026

**What is here.** Every match the Overcast Community Discord's `#match-status` channel reported as ended between
31 May 14:54 UTC and 27 November 18:37 UTC: 41,872 rows. It was read on 27 November 2026 from the channel itself in
the author's signed-in browser, by stepping through the channel's history in time order, not through Discord's search.
Discord's search turned out not to show every match: the author saw days on which a map was definitely played and the
search returned nothing.

| File | What it holds |
|---|---|
| `match-status-2026-06-01_2026-11-27.csv` | the whole log, one row per ended match |
| `ai-maps-in-match-status.md` | the 114 matches of model-made maps and maps whose XML was made in the browser, by map and one by one, each linked to its match |

**Columns of the CSV.** `posted_utc` (when the bot posted the match message, in UTC; the message is edited when the
match ends, so this is the match's start, not its end), `match_no` (the server's running number, which resets on a
restart), `match_id` (the short id that `oc.tc/matches/<id>` takes), `map`, `length`, `participants` (as the bot
writes it, `players (number in brackets)`), `winner`, `match_url` and `discord_url` (the bot message itself).

**What it leaves out.** A message that never reached "has ended" (a match that was still "starting soon", or a
message in another form) is not a row; there were 271 of those, mostly "starting soon" lines. The reader noted 57
places where the channel showed nothing for 1 to 19 minutes between one window of messages and the next. They are
most likely quiet stretches, but no one has checked that a message was not missed there.

**Times.** UTC throughout. German time is UTC+2 to 25 October and UTC+1 from then on, so a match at 23:00 UTC in
September was played at 01:00 the next morning in Germany.

## What the log shows

**The clearest test session is Friday 4 September, 22:21 to 23:50 UTC.** Seven of this repository's boards were
played back to back: Millrace, Sunspit, Hollowmarch, Brackenfold, Cairnmeadow, Hollowbank and Elderwold, with 27 to 51
participants each.

**This repository's boards were played on more evenings than the uploads show.** Hollowmarch on 31 August; Millrace
on 2 September (00:28 UTC, ten minutes after its 2.0.0 commit), 4, 13 and 20 September; Alderfen Holm on 13 September;
Hushwater and Hollowmarch on 27 September, 02:54 and 03:04 UTC; Viridian on 16 October.

**The record of play runs past 2 September, which research `06` takes as its end.** No map of this repository was
uploaded to CommunityMaps after 2 September, but its boards were played on the server until 16 October, and the
studio's and the other model-made maps until 27 November.

**No Blocks Placed, drawn in the browser studio, was played 14 times**, from 11 August to 27 November.

**Kuusepuu CTC was played on 31 July with 47 participants**, four days after it was added, and again on 29 October.
Its credits name Claude Opus 5 for the conversion, but the author counts it as an ordinary map whose objective was
replaced with a cake, not as an AI map (`../../author-account-2026-11-27.md`, sixth instalment).

**Maps whose XML was made in the browser, first played.** Capture the Wool CTW on 28 June; Bridgid II on 15 July;
Vauxite and Drastic Change II only on 12 October, three and a half months after their upload; 803 on 19 October, the
day of its 2.0.1; Countryside on 4 November.

**arcadeboss's Grok maps are the most played model-made maps.** Cedar Crossing alone has 22 matches, from 10 August
to 20 November; Alligator Charge, Nether Run, Fire on the Mountain, Hot Potato, Xavier's Mansion, Sanctum Veil and
Blocker follow.

**Never in the channel.** Thornwake, Delverdale, Whitstone Weald, Hello World Micro (or Mini), Wandering U and
Fireball Jump have no match in this window. If Delverdale and Whitstone Weald were played on 27 September, it was on
a server that does not report to `#match-status`.

**The "Hello World" of 17 July is not Hello World Micro.** Its winner is Pink, so it had four teams; that is the 2025
map Hello World.
