# Sonnet 5.5 — a jungle board and a swamp board on the deployed studio, and the questions left on them

## What I set out to build

**Two boards under the author's one direction, jungle and swamp, made clearly different from each other and from the boards already here.** The direction was split rather than blended: the destroy board is the jungle and the capture board the swamp. The two sentences, written together before either plan:

- **`sonnet55-tanglecleft`, dtm** — a jungle cleft where each team's monument stands on a temple terrace, with a lagoon dell below it, a jungle hill over it, a wood round it and a ziggurat behind it: the four ways in from below, above, around and through.
- **`sonnet55-murkwick`, ctw** — a swamp taken from composed p16 t2 seed 43, where each hub is a village island round a pit, two wools stand at the ends of walled spurs, the frontline is a wading marsh and a thatched stilt platform stands on the mid stone.

**The tone families were checked across the pair.** The jungle's ground is bright green turf over brown earth, its built stone is pale grey brick with a faint mossy vein, and its accent is jungle wood. The swamp's ground is olive turf with podzol, its built timber is dark oak and spruce, and its accent is hay thatch.

**Neither board is a grey one.** Seed 7 and seed 21 at p12 are taken, so the composed board is a different size band (p16, seed 43), and no other board here has a hub ring with two wools on its sides. Four composed cards were pinned to choose it: p12 seeds 8 and 56, and p16 seeds 2 and 43.

## The four stages, and what each read back

**Each board was built in four stages, driven and read back before the next was added, and the pictures reviewed are in `renders/stage-1` to `stage-4`.** The numbers are the three the driver prints last, then the relief read where a relief was stated.

| Stage | Tanglecleft | Murkwick |
|---|---|---|
| 1, plan alone | 15 040 walked · 0 · 0, 10.5% dead, evaluator score 0 | 8 384 walked · 0 · 0, 0.0% dead, score 0 |
| 2, outline and relief | 13 189 walked · 674 scrambled · 0 barrier, level 0.37 | 7 660 walked · 4 · 0, level 0.64 |
| 3, layers and paint | 13 189 · 674 · 0, four themes and a patch | 7 662 · 4 · 0, five themes and four patches |
| 4, dressing | 13 347 · 516 · 0, 46 placed, 0 declined | 7 594 · 56 · 16, 26 placed, 0 declined |

**Stage 1 was driven with no theme, no relief and the studio's built-in rooms.** The plan tier gave Tanglecleft its arithmetic: the monument at (−64, 24) is 58 blocks from its spawn and 183 from the enemy's, a ratio of 3.16. Getting there took the field from 112 to 80 blocks wide and the build band from 32 to 24, because `G8`, `LN2`, `GO1` and `GO3` refused the wider versions; Murkwick's composed plan evaluated clean at the first read, with `FR9` on a 12-block frontline piece that I left.

**The relief was sketched four ways on each board.** The reads and the choice are in each review (`review/sonnet55-tanglecleft.md`, `review/sonnet55-murkwick.md`): the jungle ground took its dell and hill from the first sketch and its cleft from a rejected ravine, and the swamp ground took a hub three over the flat from the second sketch and its hammocks from nothing but the need to leave the table.

**Stage 3 and stage 4 both ran on the shared kit and one small file of mine.** `specs/sonnet55_kit.py` adds block ids by name and `repaint()`, which forks a shipped house style by swapping its woods and stairs; a fork needs its beams stated in the same wood as its posts or `HS4` refuses it.

**The instrument count over each finish is not four zeros.** Tanglecleft states one relief with four marks and five pushes, six made layers, nine copied tree recipes, two waters and a patch; Murkwick states six marks and seven pushes, six made layers, eight copied tree recipes, three waters and four patches. Neither states a `level`, `raise`, `sink` or polyline shape.

## The notes left for the author

**Ten notes, five a board, each written with the token and so standing at `needs-info`.** Every one is pinned by `render/eye/pick` on a picture uploaded to `POST /notes/pictures`, and each says what the board keeps if the author does not mind. Each picture is also copied into the spec's `renders/close/`.

| id | board | tag | pinned to | asks |
|---|---|---|---|---|
| 23 | tanglecleft | gameplay | point (−40, 29, 31), view *Hill over the temple* | is the north hill, 16 over the stone, too strong a perch? |
| 24 | tanglecleft | gameplay | point (−52, 13, 12), view *Below the terrace* | should the way up from the dell be a face instead of a slope? |
| 25 | tanglecleft | gameplay | box of 343 columns, view *Straight down* | should anything bring players to the 9.7% dead corner behind the temple? |
| 26 | tanglecleft | look | box of 665 columns, view *South wood* | does the wood read as jungle, or is it too open? |
| 27 | tanglecleft | terrain | point (−82, 23, 26), view *Temple from the front* | should the temple be a place with a chamber, or stay solid? |
| 28 | murkwick | gameplay | point (−1, 8, 34), view *The marsh* | is a wading frontline the right contested ground? |
| 29 | murkwick | gameplay | point (−2, 12, 2), view *Platform on the mid stone* | is the stilt platform too strong a perch? |
| 30 | murkwick | gameplay | box of 46 columns, view *The hub's pit* | should the pit in each hub be bridged? |
| 31 | murkwick | look | point (−43, 20, 74), view *Thatch on the wool hall* | is the hay thatch on every roof too loud? |
| 32 | murkwick | terrain | point (−1, 11, 94), view *Back bar from the spawn* | does the swamp carry enough water? |

**Nine views are kept so they sit in the author's gallery.** Four on Tanglecleft (*Hill over the temple*, *Below the terrace*, *South wood*, *Temple from the front*) and five on Murkwick (*The marsh*, *Platform on the mid stone*, *The hub's pit*, *Thatch on the wool hall*, *Back bar from the spawn*), besides each board's own straight-down view, which note 25 uses.

**Every pin was checked before it was posted.** The first framing of the hill view stood inside a tree's trunk and its centre pixel hit the trunk, so the view was raised and the mark moved to a pixel that hit the hill at (−40, 29, 31). Note 30's pit view centres on air, so it is a box over the hole's rim and walls rather than a point.

## The deployed studio

**A whole drive took 15 to 20 seconds from the evaluate to the last text read**, on boards of 240 × 80 and 96 × 216. About fifty-five drives and twenty dry evaluations went to the two boards, none was refused 429, and the driver never waited on a `Retry-After`.

**Four composed plans were pinned.** Pinning writes a plan row by content hash, and those rows are left on the studio: p12 seed 8, p12 seed 56, p16 seed 2 and p16 seed 43. Only the last is used.

**Nothing was restarted and the pgm-studio repository was not touched.** Both boards are under `https://pgmstudio.de/maps/{slug}/sketch`, and their worlds are in `maps/`.

## What I could not say

**Nothing was missing from the system in this run.** Every capability reached for was found by its field in `openapi.json` or in a technique card, and two of the three things below are matters of reach rather than of a gap.

**A hub's void could not be filled with water, and I did not try.** I wanted the pit in Murkwick's hub ring to be black water. `WaterProp`'s own description says the carve stops at the surface it crosses and never fills what was already air, and a hole is made by arrangement, so this is out of reach by design and I left the pit a pit.

**The house-style preview picture is too small to judge a hall by.** `POST /room-styles/preview-snapshot?format=png&view=section` answered a 72 × 60 pixel image for every style I sent, the same size as the SVG in the JSON answer. I chose the halls from a shipped style's block list and judged them from the In-game pictures after a build, which is a stage later than a preview should be.

**`at` on a destroyable looked quantised, and I did not isolate it.** In dry evaluations `at` offsets of 40 and 41 blocks gave one identical answer (own 62, enemy 195) and offsets of 24 and 26 another, while 22 differed, so the placement seems to snap to a grid. The card and the schema say blocks; I have not read the compiler to say what the grid is.

## What I got wrong

**I painted a patch at the height the relief solves to, and it added land past the coast.** The cleft's bed patch stated 4 where the ground read 4, and the patch owns paint only at the plan's own 12; at 4 it owned 74 cells that were ground it had itself made outside the outline. `techniques/painting-a-patch` says so and I had not read it before the drive.

**I gave a pond a place in the spawn door's kept-clear lane and it vanished without a decline.** Murkwick's back pond stated at (5, 88) held water only at x 12 and 13; `06-claims.txt` marks the lane as door approach and the pass silently keeps water off it. `column` found it, and the store, the drive and pre-flight had all been quiet.

**I let an unpinned stone float.** Murkwick's mid stone came out at y10 where every other frontline ground is y8, because the relaxation between the two hubs' marks lifted it, and I found it reading `column` at (0, 0) for the platform's floor.

**I read stage 3 by its pictures and missed two declines.** The bridge's posts on the deck's own layer and the platform's legs on its deck's layer each drew `SK9` at the drive, and I found them at stage 4 in the decline list.

**Half-integer rectangle corners built a two-wide bridge, and reversed steps a stair the wrong way.** Both were found by `column` at the coordinates in the reviews, and both were mine.

**A copied tree's stated foot is not where a decline reports it.** Trees declined at coordinates one to four blocks from where I stated them — `o-5` stated at (−97, 13) was `DR-KEEP` at (−93, 15) — because the pass reports the column the tree rests on. I read the first one as a studio fault for a moment and it is not.

## What worked first time

- The composed plan taken whole: Murkwick drove clean at stage 1 with 0.0% dead, and its wool walks read 201 to 208 blocks for the attacker.
- `coast_edits` on both compiled outlines: every insert landed, the vertex count of the Murkwick field went from 24 to 46, and no wall seam, room face or frontline face moved.
- The copied trees and `07-seats.txt`: after the paths were in, every tree site read off the mask seated, and the two declines were both mine.
- `render/eye/pick`: it answered the same block for a pixel on every call, and all ten notes posted on the first try once each pin was checked.
- The made layers on a mirrored board: the ziggurat, pillars, bridge, ponds' walks and hay stacks were each read with `column` at their rot_180 images and matched.

## Open gameplay questions

**None were decided alone.** Every gameplay question this run met is one of notes 23–25, 28–30 and 32, built with the default each note names.

**One decision was mine and is not a note: a board's width against `G8`.** The wide jungle lane read 44% dead at the plan tier and was refused, so I narrowed it to 80 blocks and put the monument 24 off the axis; a wider board with the same monument would want a second goal, which `approaches.md` says a large single-goal board does not.

**One choice was the author's ruling read closely.** A hill in a capture lane is wrong and a hill on a destroy board is right, so the swamp's hummocks are two and three blocks high and the jungle's hill is 16.
