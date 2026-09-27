# Delverdale — a thirty-two-a-side capture board with a drift under the fell

## What I set out to build

**One capture-the-wool board for two teams of thirty-two, sized from the corpus and larger than the small
boards it is played beside.** The author asked for two walls, real relief, more trees and more buildings than
the recent destroy boards, and an underground route players can use. The plan was to be my own rather than a
composed one taken as it came.

The sentence, written before the first piece: **a wooded lead-mining dale, where each team's village stands
on a terrace in the middle of its half; one wool is kept up the west side in the mine yard behind a bedrock
wall, and the other in the quarry cut into the east fell, reached over the fell or through the drift driven
under it.**

The three tone families were named before the first theme. The ground is a Forest-biome meadow over pale grey
rock. The built family is dark-oak frames, brick and whitewashed clay under brick or dark-oak roofs. The
accents are the gravel of the workings and the team colours on the wools.

## The board

| | |
|---|---|
| slug and name | `delverdale`, **Delverdale**, credited to Opus 5.5, created 2026-09-27 |
| mode and teams | ctw, red and blue, `max="32"` each (64 players), `rot_180` |
| extent | x −84…83 by z −140…139, **168 × 280 blocks** |
| land | 21 408 ground cells, **about 10 700 a team** with its half of the crossing |
| wools | two a team, four in all |
| build ceiling | y40, set by the studio; the observer platform at y57 |

**The size comes from `G8` and `docs/world-scan/map-size-ladder.md`.** The centi band (32 and up a team) has
a median of 8 732 blocks² of land a team, with the quartiles at 6 966 and 11 356, a board of 161 × 304 at the
median, and four wools in all. This board is 1.23 times the median and inside the upper quartile. It is larger
than the composer's own centi board, which is 168 × 248.

**The distances were held to the envelope terms.** On the plan tier the attacker walks 280 blocks to the ore
house and 268 to the quarry lodge; the defender walks 86 and 98, a ratio of 1.14 against `WL9`'s band of
1.03–1.22. The frontline-to-wool distance sits under `WL10`'s remoteness cap of 130 once the half was shortened.

## How the half is arranged

Red's half is the +z side and blue's is its image; every coordinate below is red's.

**The crossing is a build band x −52…52, z −20…20, with a holm in the middle and a stone either side.** The
holm is 40 × 16 at y14 and carries a roofless engine house with a brick stack at each end, laid out about the
turn's centre so it is its own image. The stones are 16 × 8. Every hop is 12 to 16 blocks.

**The front is two tips, 32 blocks each, with an unbuildable rotation hole between them.** The tips stand at
y14 and hang off the hub's front bar at y16 (x −52…52, z 36…52). The gap between the tips lies outside the
build band, so it can never be bridged and every attacker goes round it.

**Three lanes run north from the front bar, with a hole between each pair.** The west lane is a small dale
rising from 16 to 24 between a knoll and a rim. The middle lane is the village terrace at y20, entered by one
flight at each end. The east lane is the fell, a crest at y28 with the drift under it. A back bar at y24
closes the ring.

**The spawn hall sits on the back bar between the two wools.** Its one door opens south onto an apron, so a
defender leaves it onto the lateral lane and turns east or west.

## The wools and the walls

| wool (captured by) | room | wool block | how it is reached |
|---|---|---|---|
| red (blue) | ore house x −72…−60, z 124…140, floor y23 | (−66, 23, 132) | the mine track up the west side, through the wall, across the yard |
| orange (blue) | quarry lodge x 72…84, z 112…128, floor y15 | (78, 15, 120) | the drift; the quarry stair off the back bar; a drop off the fell top |
| blue (red) | ore house x 60…72, z −140…−124 | (66, 23, −132) | the image of red's |
| light blue (red) | quarry lodge x −84…−72, z −128…−112 | (−78, 15, −120) | the image of red's |

**Each monument stands inside its capturing team's spawn hall.** Red's are at (1, 25, 114) and (−14, 25, 114);
blue's are at (−2, 25, −115) and (13, 25, −115).

**One wall a team, as the author asked, on the ore house's approach.** Red's stands on the seam between the
lane's neck and the mine yard, x −60…−44, z 115…117; blue's is its image at x 44…60, z −117…−115. The column
at (−52, 116) reads bedrock to y26 and cobweb at y27: three courses, y24–26, over the ground pinned at 24. The neck is 16 wide with void past both ends, and the ore house's door is about 20 blocks' walk behind it.

## The underground

**The drift's floor runs 68 blocks from the hub's front bar to the quarry floor, about 48 of them roofed under the east fell.** Its floor stands
at y16 with four courses of air to a roof slab at y20…27, flush with the crest the relief pins either side. The
centreline is (46, 44) → (46, 58) → (49, 72) → (55, 86) → (58, 95) → (58, 110), covered from z 53 to 98.

**It is built as the complement of the space, with no subtract anywhere.** The floor is an override polygon on
the ground layer at a level top of 16, and the roof is the same band on a layer of its own at `base_y` 20. Both
are drawn with one mitred-band helper, so the roof covers exactly the columns the floor cut.

**Each end is a timber-framed portal under a face of the fell's own rock.** The frames stand at z 52 (x 43…48)
and z 99 (x 55…60). Six timber sets stand at z 58, 65, 73, 80, 88 and 95, each a post on the band's outermost
cell either side, a beam at y19 and a glowstone lamp. The passage between posts is three to four blocks.

**Read back:** `walk` at y16 answers *walked end to end* on every stretch, and the section at z 76 shows the
air at x 48…53, y 16…19. The void scan counts 1 032 open cells a side before the timber sets split them.

## The buildings and the made things

| building (red) | footprint | notes |
|---|---|---|
| green-sw | x −24…−16, z 55…61 | two storeys, door to the street |
| green-nw | x −24…−16, z 72…78 | one storey |
| green-se | x 15…23, z 55…61 | one storey |
| green-ne | x 15…23, z 72…78 | two storeys |
| farm | x −49…−41, z 62…68 | the west fell's rim, clear of the knoll |
| fell cottage | x 55…63, z 66…72 | the fell top, beside the drift's roof |
| spawn hall | x −16…4, z 108…128 | the works style |
| ore house, quarry lodge | the two wool rooms | the works style |

**Six houses a side, twelve on the board, in one style.** The cottage is a dark-oak frame with brick to the
sill, whitewashed clay above, a laid-log course under the eaves and a brick roof. The rooms share a second
style, the works: brick walls, the same frame and a dark-oak roof. That is two styles for three kinds of
building.

**The made things are six layers.** The engine house stands on the holm at x −8…8, z −4…4. The two portal
frames and their rock faces are two layers. The village well at x −12…−10, z 64…66 is two more: a stone-brick
kerb round water with two posts, and a windlass bar over it. The timber sets are the sixth.

## The trees and the rest of the dressing

**Eighteen trees a side, thirty-six on the board: oak as the wood and birch as the accent.** All are copied
bodies from the showcase world: `r6` small oaks, one `r12` great oak and `r13` birches, carried in
`specs/delverdale/trees.json`. None stands on the front, the tips, the holm, the approach in front of the wall,
or at a spawn door.

| tree (red) | at | blue image |
|---|---|---|
| great oak on the knoll | (−64, 72) | (63, −73) |
| knoll birch, knoll oak | (−63, 84), (−60, 96) | (62, −85), (59, −97) |
| farmyard birch | (−45, 78) | (44, −79) |
| back-bar rim: oak, birch, oak | (16, 98), (30, 98), (−32, 98) | (−17, −99), (−31, −99), (31, −99) |
| the east wood: birch, oak, birch, birch, birch | (70, 61), (74, 70), (69, 79), (73, 88), (68, 96) | (−71, −62), (−75, −71), (−70, −80), (−74, −89), (−69, −97) |
| cottage oak | (56, 61) | (−57, −62) |
| fell rim over the hole: birch, oak, oak | (41, 62), (41, 76), (42, 88) | (−42, −63), (−42, −77), (−43, −89) |
| quarry lip: two birches | (48, 124), (58, 124) | (−49, −125), (−59, −125) |

**Nine paths a side run where players go.** The street crosses the green from flight to flight, a road leads
to the spawn, and two paths run from the south flight to the tips. The fell road climbs the west lane, the
mine track runs to the ore house door and the quarry tracks run to the lodge; the rake climbs the fell's face.
The village paths are dirt, coarse dirt and spruce planks, and the tracks gravel, andesite and cobble.

**Two boulders a side and one ground-cover pass over the whole board.** The boulders stand at (−61, 77) and
(62, 80). The flora pass is at a coverage of 0.3, with tall grass at 0.08.

## The ground and the paint

**Two reliefs, fourteen marks and three pushes.** The team relief pins the tips at 14 and the hub bar's middle
at 16. It pins the back bar, the spawn, the mine yard and the quarry stair's landing at 24, the quarry at 16,
and the fell crest at 28 along the drift's line. The
pushes are a knoll over the void past the west coast, a rim over the west hole and a low howe on the holm. The
team ground runs 14 to 29 with no seams and no silent marks.

**Three themes: `dale` 76.3%, `green` 14.9% and `mine` 8.8%.** The dale is finished on the slope axis: grass
to 32°, dirt and coarse dirt half and half to 44°, then stone and andesite with cobble at a quarter. The
terrace is a lawn over a stone-brick face with a coping course. The mine theme floors the drift, the quarry
and the mine yard with gravel patches in worked rock.

| read | number |
|---|---|
| slopes | 21 468 walked · 344 scrambled · 598 barrier · 16 faces, the largest the terrace's south face |
| incline | 67.4% under 10°, 7.1% at 40° or steeper |
| relief read, team | level 0.69, largest field 0.149, relief 15 |
| coverage | 1.1% dead |
| dressing | 71 placed, 0 declined |
| pre-flight | export gate OPEN, and the export answered with no warnings |

## The reads that changed the board

| read | what it said | what changed |
|---|---|---|
| `/plan/evaluate`, first plan | `FR6` front 28 cells wide, `LN2` chain 128, `WL10` remoteness 147 | the front split into two tips, the half shortened by 24, both bars cut under 110 |
| `/plan/evaluate`, second plan | `G5` hard: a 58-block hop from a stone to the far tip | the holm widened to 40, so the diagonal spans cross it |
| `/plan/evaluate` | `WL12`: 8 blocks between the quarry lodge and the fell | the lodge moved 4 north |
| `/plan/compile` | the shape ids `a-lane-9` and `a-lane-20` | the finish keyed on them |
| `/map/from-documents` | `PT4` on the stair materials; shapes filed on the `neutral` group | a `rise` on every pattern; every authored shape names `team` |
| `/map/from-documents` | `SK3`: `path` is not a kind; then `SK10` on 4 columns | the drift drawn as polygons from one band helper |
| the compiled outline's vertices | the hub bar ends at x 52, so the portal opened over void | the east fell moved 8 west and the drift re-routed |
| `relief/read` | `RL6` on the knoll's crown | the crown taken off |
| `07-seats.txt` | the house and tree masks | every house site, and the first tree sites |
| the dressing pass | `DR-SITE`, `DR-ROAD`, `DR-CLAIM`, `DR-KEEP`, `DR-CUT`, `DR-ROOT` | four trees removed, others moved, the back-bar tracks moved 3 south |
| `transect` over the quarry stair | scramble +2 at (43, 98) | the stair's landing pinned at 24 |
| `column` down the drift | the first timber sets stood a cell in from the rock | each post seated on the band's own edge cell |
| `relief/read` | level 0.72, largest field 0.297 | the hub bar's west end unpinned and a rim push added: 0.69 and 0.149 |
| `render/eye` at the flights | the terrace's face was dirt | the terrace theme's surface cut to one course, with a coping |
| `render/eye` at the adit | the roof slab's end was turf and dirt | portal frames under a rock face |
| `render/eye` on the green | two trees swallowed the houses | the trees removed and the well put there |
| `render/eye` on the holm | the observer's bedrock pad hung over the engine house | `observerY` 56 |
| `render/eye` in the quarry | the floor was an even speckle | a noise with gravel and cobble patches at its ends |

## What I got wrong

**I wrote `path` as a shape kind because the schema's own description of `type` lists it.** The SketchShape
`type` field in `openapi.json` reads *rectangle, circle, polygon, lasso, path*, while `SK3` answers that the
kinds are *rectangle, circle, polygon, lasso, polyline*. The store answered 200 and drew nothing until `SK3`
was read.

**I wrote `grain` as an array.** The schema shows it as a one-of with a `$ref` inside brackets, which I read as
a list. `RQ1` refused the store and named the path.

**My first `addShapes` landed on the holm's group.** A shape naming no group joins the compiled ground's first
group, which on this board is `neutral`, so the flights and the drift floor would have been built once, on red's
side only. `drive.py` says where each shape went, and naming `team` fixed it.

**I let the drift's portal open over the void.** I placed the east fell by its piece rectangle, not by what the
hub bar reaches. The compiled outline's vertex list showed the bar ending at x 52, about ten blocks short of the
portal. Nothing refused it; the floor polygon simply made a ledge over the void.

**I placed trees by eye and read the declines.** Eleven came back on one build. The seats mask was the read to
start from, and the dressing pass the one to confirm with.

## What worked first time

**The plan tier caught every structural fault before a world existed.** Three evaluate rounds took the plan
through a score of 1000 and an invalid board to 0 and valid, and the first built world pre-flighted OPEN.

**The walled lane held from the first plan.** A 16-wide neck with void past both ends, the room about 20
blocks' walk behind the wall, and `PL13`, `PL17` and `ST8` silent on every evaluate.

**The flights walked on the first build.** Both terrace flights and the rake transect at one block a step.

**The wall stamped where the plan put it,** three courses over the pinned seam, with void past both ends.

## What I could not say

**`tools/loop.py --candidates` cannot answer for a prop near an edited coast.** It compiles the spec afresh and
does not replay `editShapes`, which `drive.py` applies after the store. So it declined sites the built board
seats, with `DR-SITE`. The studio's `POST …/sketch/dressing` answers correctly when handed the *stored* layout.
I used a throwaway script in the scratchpad to post that, so this is **out of reach from the tool**, not missing
from the system.

**The driver draws no preview of a house style named by key.** `drive.py` previews a house prop's style only when
the prop carries it inline, so the cottage had no plan or section among the renders. I drew them myself through
`POST /room-styles/preview-snapshot`. The capability is there; the driver does not reach it.

**`render/eye?look=` on a wool room framed the sky marker, not the room.** Standing the eye with `from`, `yaw` and
`pitch` gave the picture. The read works; the framing is the thing to know.

**`plan/flow` and the theme census cannot see the drift.** The flow reads the plan, which has no storeys, so the
280-block walk to the quarry lodge ignores the drift's shortcut. The census counts the top surface only, so the
drift floor is missing from `mine`'s share. Both are known limits, and `walk` with a `y` is the read that sees
the drift.

## Left in place, and why

**`SK27` on the village terrace.** The terrace is its own place, made ground with its own paint, and a hard line
at its riser is the design.

**`EL1` on the two terrace seams.** The plan states the terrace at 20 against a board surface of 9, so the plan
tier reads an 11-block step. The built flights transect at one block a step, rising 4 each.

**The board shares its tone families with the destroy board built beside it for the same play test.**
`whitstone-weald` is also Forest biome under brick-and-timber buildings, with a drift mine and an engine house.
The two were decided apart and in parallel, so neither could be checked against the other before its first
theme. Across the play test's set they read as one place twice; if both are played, one wants a different
ground or a different built family.

## Open gameplay questions, decided without the author

1. **Two wools a team.** The corpus median at centi is four wools in all, and a third a team would lengthen
   matches the population already makes long.
2. **The wall guards the ore house and not the quarry lodge.** The author asked for one wall a team, so each
   team has a fortress and a cheaper wool. The quarry lodge has three ways in: the drift, the quarry stair and a
   drop off the fell top.
3. **The drift is an attacker's shortcut to the quarry lodge,** about 50 blocks shorter than the surface route
   through the village, by my own reckoning along the drawn lines rather than by a read. I expect the
   quarry lodge to fall first; the defence holds the drift's quarry mouth, about 15 blocks from its door.
4. **The timber sets narrow the drift to three or four blocks every eight.** That is cover inside a firing line,
   which `match-flow.md` §10.3 asks of a tunnel on a control board and which I took to hold here, and it is a
   choke a defender can plug.
5. **The wool rooms have three faces on void.** That is the ordinary composed shape, allowed by `approaches.md`.
6. **The spawn stands between the two wools on the back bar,** so the defenders' lateral lane runs past it. The
   plan's flow reports the attack sharing 43–61% of the defence's ground.
7. **The gap between the tips is unbuildable.** It forces every crossing onto the tips, which are 32 blocks each.
8. **The holm's engine house is the contested middle's large cover,** a ruin with two stacks rather than a deck.
9. **A farmhouse stands beside the west lane on the way to the walled wool,** as cover on the approach; it
   leaves the lane at least ten blocks wide.
10. **The fell top is an approach from above that needs building.** It stands 12 blocks over the quarry floor
    with no stair down, so an attacker arriving there drops or builds down.
11. **The build ceiling is left at y40**, as the studio derived it from the tallest terrain, and the observer
    platform is raised to y57 to keep it off the holm.
