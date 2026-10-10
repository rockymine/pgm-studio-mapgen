# The experiment: what came out

Two briefs (`BRIEFS.md`), each built once through a local studio and once with pgmvox 0.19.0, all four by Sonnet 5.5
from the same reading, the same twelve playtest lessons and no author review. The boards are
`exp-slatefold-studio`, `exp-abbeymoor-studio` (`maps/`, `specs/`, `reports/`) and
`freeform/lib/boards/exp-slatefold-pgmvox/`, `exp-abbeymoor-pgmvox/`.

## The finding

**With the model, the brief, the lessons and about twenty minutes held equal, the two tools made boards of
comparable quality.** Neither pair shows the gap that Riftwater against Russetford suggested. Each tool's boards have
its own strengths, and each builder met almost every lesson. That locates the leap on the freeform branch: it took
the open substrate *and* what was spent on it — Opus, hours per board rather than minutes, rounds of the author's
review, and bespoke code (Riftwater is 3,379 lines; these boards are 1,332 and 1,507). pgmvox raises the ceiling of
what a board can be much more than it raises the floor of what a short run produces.

## Measured from the worlds

The same census over all four region folders.

| | Slatefold, studio | Slatefold, pgmvox | Abbeymoor, studio | Abbeymoor, pgmvox |
|---|---|---|---|---|
| x × z | 102 × 224 | 168 × 216 | 122 × 240 | 186 × 260 |
| y span used | 0–62 | 0–109 | 0–60 | 0–92 |
| distinct block ids / id+data pairs | 33 / 78 | 39 / 75 | 26 / 52 | 40 / 73 |
| distinct top-surface kinds | 36 | 47 | 35 | 49 |
| spread of surface height (std, blocks) | 10.4 | 29.3 | 9.5 | 4.2 |
| air under built roofs | 22,002 | 160,610 | 8,956 | 7,604 |
| tile entities / chests | 44 / 32 | 54 / 40 | 12 / 4 | 16 / 0 |
| ladders / fences | 84 / 0 | 0 / 142 | 112 / 0 | 0 / 132 |
| floating goal markers | yes | no | yes | no |
| build-zone outline | yes (stamped) | yes (by hand) | n/a | n/a |
| defence wall with chests | no | yes | n/a | n/a |
| crypt and passage | n/a | n/a | 8 cuts and 7 lids, a well 6 from a monument | a carved hall, an 11-step stair and a 60-block passage to a barn cellar 14 from a monument |
| authoring code | 355-line spec, 20 stores | 1,332 lines | 404-line spec, 14 stores | 1,507 lines |
| time to the finished build | about 23 min | about 25 min (50 with repairs) | about 20 min | about 21 min |

"Air under built roofs" on the pgmvox Slatefold counts the void under its floating terraces; it is not interior.

## What each pair shows

**Slatefold.** The pgmvox board is the more ambitious arrangement: seven terrace floors and a high bench spread
over 109 blocks of height, bedrock six under every platform, a bedrock defence wall with its chests in the front
face, a headframe, and a building walk that proves no wool room is reached on foot or by a jump. It reads grey and
busy from above. The studio board is two solid hillsides with tidy houses, kilns as brick towers, the quarry pits,
and the studio's stamps doing their work: a floating marker over each wool room, the build zone outlined, wool loot
in the corners. It has no defence wall, because the plan's wall rules did not fit.

**Abbeymoor.** The studio board has the stronger relief (a surface-height spread of 9.5 against 4.2): two abbey
hills with ruins standing on them, a bog with pools, markers floating over both monuments. Its crypt took eight
subtract cuts and seven lids, with ladders and standing stones built as made-layer boxes. The pgmvox board is flatter
but carries more of a place: heather in patches, a beck, peat cuttings and a boardwalk, and a crypt that is a carved
hall with a stair up into the chancel and a passage under the valley to a barn cellar. Its monuments are found by
placement and sight (26–27% visible from the attackers' ground), not by a marker.

**Both builders found the same kind of wall.** The studio builder could not build a crypt, ladders, ruins or
standing stones except as boxes, and had one wool-room shell per map. The pgmvox builder had to write its crypt,
defence wall, build-zone marking and objective-visibility check itself, and worked round the house window and door
defects. Each tool is missing the other's half.

## One round of the author's review

The author reviewed all four boards (`REVIEW-1.md`) and each builder revised its own two, answering every point.
Both finished in minutes, 3 to 8 per board.

**The studio's changes were mostly arrangement.** Slatefold's wool rooms moved behind the front onto a middle
terrace and the stone disc, a pit whose shape had flattened its own hollow, became a lake (water 80 → 1,214 blocks).
Abbeymoor's spawn became the abbey's grange and its outlines irregular. Its friction was a missing unit for a place:
the grange is a room style, cottages, a made-layer wall, paint shapes, strokes, a pond and relief marks, each placed by
hand and refused by a different rule (DR-KEEP alone cost three stores).

**pgmvox's changes added things.** Slatefold got clay-walled houses in five colourways, a creek between two ponds, six
grass hills and fourteen spruces (leaves 654 → 2,074), and its cart rails cut from 100 to 26 (the line the author
read as a fence). Abbeymoor got a noise-warped bog with a fen channel, peat patches and tarns, a hamlet on each flank,
31 trees in copses (leaves 396 → 9,798), 58 boulders, and three-block monuments (obsidian 108 → 12). The one point
pgmvox kept was argued with numbers: the tower wool room at the front would break WL7 and WL10e.

**One round of review closed much of the gap on both tools, and moved pgmvox further**, because on an open substrate
adding what the reviewer asks for is a few lines of code. That is the first round's finding seen again: the leap is
the substrate *and* an eye that asks for things.
