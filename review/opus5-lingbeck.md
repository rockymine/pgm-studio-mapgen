# Lingbeck — one cut, and three ways over it

> A capture-the-wool board split down the middle of each team's own ground by a six-course gill, with
> a wool on each bank. Every rotation between them is a crossing, and there are exactly three.

**In one sentence:** the beck is the map — it runs from the frontline to the spawn's doorstep, so a
defender who commits to one wool has to pay a crossing to reach the other, and the gill itself is the
best covered approach on the board and the worst place to be caught in.

110 × 200 blocks, `rot_180`, the team unit offset west, maxPlayers 24, ground y8..y18 plus the cut.

## The three crossings, measured

| | where | what it is | `transect` across it |
|---|---|---|---|
| the **head** | `z 75..80` | the gill stops short of the spawn's apron and the moss runs round it | rises 0, falls 0, **worst step 0** |
| the **brig** | `z 62..68` | a one-course stone deck on its own layer, flush with both banks, four courses of air under it | rises 1, **worst step 1**, 0 barrier, 0 scramble |
| the **ford** | `z 46..56` | a tilted quad down each bank into the water | rises 5, falls 5, **worst step 1**, 0 barrier, 0 scramble |

All three walk end to end. The gill's own banks are `328` barrier cells in 8 faces — six courses, sheer,
everywhere the crossings are not.

## How the cut is made, and how it is not

**Not as a plan piece.** The first version stated `beck` as a piece at surface 7 enclosed by pieces at
12. The compiler traces **one outline per component**, the taller add wins every column, and the low
piece never appears: a transect across it read `11 11 12 12 13 13 14` straight over the top, with the
water prop sitting on the surface like a puddle. Nothing refused it and the export gate was OPEN.

**As an override add.** `override: true` moves a shape into the second pass, where it overwrites the
column it lands on outright — the one thing that beats a taller ordinary add. The plan then states one
`hub` piece and the gill is cut out of it downstream, with a ramped south mouth so the gill is a route
in as well as a place to fall into.

**The brig is a second layer, not an override.** A layer holds one span per column, so a deck written
onto the ground layer would move that column's only span up and take the bed with it — a lid, not a
bridge (`showcase/12-underpass` measures exactly that). A slab at `base_y 11`, one course thick,
covering exactly the gill's own columns, leaves the bed at y6, four courses of air, and a deck flush
with both banks. Lapping it two blocks onto the banks instead is `SK10`: *"driven 2 blocks into each
other over 24 columns… the gap the layers were drawn to have is not in the world there."*

## Where the wools are, and why

Barn, house, byre in a row across the back — **the spawn between its two wools rather than behind
both**, which is the composer's own arrangement corrected. One wool is on the west bank and one on the
east, so the gill separates them from each other and not from the door.

`WL9` reads the two spawn-wool walks over the **piece graph**, and a void notch between the spawn and a
room is a detour the straight line does not show: the first arrangement read **22 and 38** against a
1.232 cap while both markers were 28 blocks away as the crow flies. Making the three pieces abut and
pushing both markers to the same walk is what fixed it.

## What the ground is made of

Three themes.

- **`ling`**, the moss: a `layered` stack on the **slope** axis — turf, a worn shoulder, stone past 40°.
- **`heugh`**, the gill: its **wall** is where the work goes, because a wall is what a player standing
  in a beck looks at — a cut bank of gravel and coarse earth over the rock it is cut into.
- **`myre`**, peat: two splotches stated on shapes, three close browns and **no grass in the pattern
  with them**, so they read as a different ground rather than as a mottle of this one.

## The beck itself, and what it actually does

Two `water` channels, and only the southern one carries water. A channel reads the **surface top**,
which on a stacked board is the maximum over every layer — so the brig's deck reads as the bed under it
and the water line cannot hold across the jump. Measured: at `(-20, 63)` and `(-20, 67)` the transect
answers ground **12**, which is the deck five courses over the bed.

So the beck runs water from `z 41` to about `z 60` and stands as a dry gravel bed above the bridge.
That is what a beck above a sink looks like, and the northern channel is kept for the bed it paints
rather than for water it does not carry. It is recorded here rather than claimed away.

## The buildings and the trees

One authored house — a **bastle**, a two-storey stone hall with a cross wing, standing on the east bank
where it can watch the brig, because somebody who owned a crossing built a house that watched it. Three
more the rooms stamp. Four to a side and no more.

Four trees. A shaw of three in the lee of the west how and one thorn at the ford. The story wanted them
along the gill, and the gill's banks belong to the road and the two keep-out structures — a tree three
blocks off a road is `DR-ROAD` — so the wood went where there was room for one. Said rather than
pretended.

## Numbers

| read | answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true` |
| `GET …/preflight` | **export gate OPEN** |
| `GET …/coverage` | reached 10 749 · dead **0** of 10 749 = **0.0% dead** |
| `03-slopes.txt` | 10 381 walked · 40 scrambled · 328 barrier; 8 faces, all of them the gill |
| `06-claims.txt` | placed 18, declined **0** |
| the three crossings | worst step 1, 1 and 0; 0 barrier and 0 scramble on all three |

## What went wrong on the way

- **A low piece enclosed by high ones is not a cut** (above). The world built, the gate opened, and the
  gill was simply not there.
- **`SK10`**, above: two courses of lap is one too many.
- **A ramp's top anchor is an absolute height.** Both ford ramps state `MOSS`, and where the relief
  left the bank two blocks above that the crossing arrived at a step — `BARRIER +3 at (-10, 51)`. Two
  `area` marks pinning the banks flat at the ford and at the brig were the fix, and they are the right
  instrument: an area is for where flat is the point, and a crossing is exactly that.
- **`WL9` measures a walk, not a line** (above).

## Open, and not the author's to settle here

The gill runs the full depth of a team's ground, so an attacker who drops into it is in cover the whole
way to the spawn's apron and cannot get out except at the ford. Whether that is a good route or a
death trap is a question about how a map plays, and this session has no oracle for it. Built as stated.
