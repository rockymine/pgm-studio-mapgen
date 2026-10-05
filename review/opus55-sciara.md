# Sciara — two hill towns on a volcano's flank, each defending its core on the threshing floor

> A destroy-the-core board. Each team's core floats over the kerbed threshing floor (the aia) at the top of a
> terraced olive grove. A hill town of fourteen buildings climbs three tiers behind it, and a black lava flow,
> the sciara, runs down the far flank. A ravine over void with a build zone parts the two sides.

**In one sentence:** a Sicilian hillside where every made level — the terraces, the threshing floor, the town's
tiers — is a tilted field held up by a cobbled wall, and the core is fought for through the olives, off the
lava, out of a quarry tunnel or straight up the open slope.

96 × 296 blocks, `rot_180` about the origin, plan surface 22, Savanna biome (grass `#bfb755`). Red's unit is
authored on `z < 0`; every blue coordinate is the image `(−x−1, −z−1)`. Built on the deployed studio as
`opus55-sciara`, revision 2. The author's review of revision 1 — empty, flat, five houses called two villages,
terraces cut as square three-block steps — is what this revision answers.

## The two lines

The spawn hall stands at `(−8, −118)`, y34, in the middle of the town. The core stands at `(10, −68)`, its
casing obsidian at y38 and y42 with lava at y39–41, over a paved threshing floor standing at 32. The plan tier
reads the core's own walk as 59 and the enemy's as 186, so `GO1` is **3.15**. Built, spawn to own core walks
end to end in 57 blocks, by the main street, the piazza and one flight.

## The terraced grove

Nine terraces in four rows fill the west of each side, from the ravine lip at 22 up to the town at 35. A row's
front and back edges are contours shared with the rows either side, so the terraces stack into each other with
no ground between them, and an angled divider splits each row into two or three cells.

| Row | Cells | Standing | Front edge (contour) |
|---|---|---|---|
| a | `a1` `x −36..−22`, `a2` `x −22..−6` | 24, 25 | `z −19..−22` |
| b | `b1` `x −36..−20`, `b2` `x −20..−6` | 27, 28 | `z −33..−37` |
| c | `c1` `x −48..−29`, `c2` `x −29..−14`, `c3` `x −14..−6` | 30, 30, 31 | `z −50..−54` |
| d | `d1` `x −48..−25`, `d2` `x −25..−6` | 33, 32 | `z −67..−71` |

**Each terrace is a plane**, its vertex heights read off a base height and a fall of a few hundredths of a
block per block east and forward, so it dips a block or so across its width. Two cells of one row stand within
a block of each other and merge with no wall between them.

**Every made face is a cobbled retaining wall, with a wall one course high along its top.** The terrace theme
paints its faces in lava stone up to y22 and dry stone (cobblestone with andesite) above. A terrace reaching
the coast therefore shows its wall end-on over the mountain's own rock. The course on top is a thin polygon
strip set 0.15–1.6 blocks in from the edge, its heights the terrace's plus one, broken into runs of eight to
sixteen blocks.

Transect `x −24, z −14..−100`: lip 22, row a 24–25, row b 27, row c 30, row d 32, town 35. The walls stand
one course over their terrace at 33 (`z −72`) and 36 (`z −92`). The transect walks end to end.

## Twelve flights, each in a notch in the wall above it

| Flight | Where | From → to |
|---|---|---|
| `stair-lip` | `x −17..−13` on the front contour | lip 22 → `a2` 25 |
| `stair-a1b1` · `stair-a2b2` | `x −31..−27` · `x −11..−7` | row a → row b |
| `stair-b1c2` | `x −25..−21` | `b1` → `c2` |
| `stair-c1d1` | `x −38..−34` | `c1` 30 → `d1` 33, walked `(−36,−62)→(−36,−78)` end to end |
| `stair-grove` | `x −40..−36` | `d1` → lower town 35 |
| `stair-front` · `stair-piazza` | `x 18..23, z −52..−60` · `x 6..11, z −84..−90` | slope 27 → aia 31 · aia 31 → piazza 34 |
| `stair-upper-w` · `stair-upper-e` | `x −38..−34` · `x 32..36` at `z ≈ −114` | lower town 35 → upper 37 |
| `stair-rear-w` · `stair-rear-e` | `x −24..−20` · `x 16..20`, `z −136..−132` | rear lane 35 → upper 37 |

From the lip at `(−19, −16)` to row c at `(−22, −62)` is walked end to end without a block placed
(`walk … aim=reach`).

## The four ways onto the core

| Approach | Where | Measured |
|---|---|---|
| **through** the olives | the grove, under eleven copied olives | flight to flight, worst step 0 |
| **above**, off the sciara | a push down the east flank, ring centred `(38, −56)`, lift 9 | crest 38 at `(35, −68)`, level with the casing's lowest course and seven over the aia; snout `(30, −18)` to crest walked with one scramble, +2 at `(35, −31)` |
| **below**, out of the cava | a quarry pit at the aia's foot, `x 2..17, z −51..−39`, floor 23 | a tunnel into the aia, `x 8..11, z −58..−51`: column `(9, −55)` is floor y22, air y23–25, roof y26–30; walked `(10,−30)→(9,−56)` end to end |
| **straight up** the open slope | `x −6..26`, pinned at 27 under the aia | a 4-block cobbled wall with `stair-front` in it |

The aia itself is an irregular field at 31. On it the threshing floor is a paved disc of radius 9 standing at
32 inside a dry-stone kerb at 33, with four gaps. Two market stalls stand at `(−2, −56)` and `(21, −78)`,
15–17 blocks from the core.

## The town

Three tiers: the piazza and the spawn's yard at 34, the lower quarters and the rear lane at 35, the upper
quarters at 37, each tier's face a cobbled wall with a course on top. Thirteen houses in the library style
`brick-roofed-quartz-house` stand along paved streets. Five of them carry a second, lower wing with its ridge
running into the hall, so the houses differ in shape rather than in material. The church, the same style two
storeys high with a lower apse, faces the piazza.

The campanile at `(13, −106)` is a quartz shaft to y48, four quartz-pillar posts framing an open belfry to
y52, and a stepped brick cap to y56. The well at `(−19, −96)` is a two-course quartz ring round water under a
brick-slab roof on oak posts. Every house keeps its passage: the quarters stand flush against the straight
back and side coasts and eight blocks clear of the spawn hall.

## Dressing and made things

- **Eleven copied olives** a side (`olive-3`, `olive-7`, `olive-9`, `small-olive-2`), along each terrace and
  two in the town, none within 26 blocks of the core.
- **A wooden lookout** at the grove's front, `(−32, −25)`: four oak posts to a spruce deck at y32, a fence
  rail, and a ladder `(−34, −23)` from y24 up into a hole in the deck.
- **A wayside shrine** at `(−44, −82)`, a quartz pillar under a brick-slab hood, and two stacks of olive crates.
- **A smaller lava lobe** on the west flank, centred `(−43, −36)`.
- **Five angular lava boulders** on grass at the flows' feet: `(19, −34)`, `(22, −25)`, `(30, −23)`,
  `(45, −22)`, `(−40, −17)`. Each column reads coal block on top; none carries moss.
- **Paved streets and farm tracks** from flight to flight, and low ground cover over the whole side.

94 props placed, none declined, no complaint.

## Readings

`ground` 24 429 walked, 1 440 scrambled, 1 225 barrier (9.8%) · `props` 94 placed, 0 declined · relief `level`
0.35, `largestField` 0.17, no seam, no silent mark · coverage **38.6% dead** (48.0% in revision 1), the largest
patches the sciara `(36, −58)` and the lobe `(−38, −51)` · pre-flight `export gate OPEN`.

The report's worst step, 43 on `route spawn-0 to core-1`, is the walk read climbing over the observer platform
at y64, which it cannot pass under. A crossing walked off the centre line places 19 blocks with no step.

## What went wrong in revision 2

- **Every terrace built at the wrong height** (25 where 32 was stated) because the ring's back edge ran the
  wrong way and crossed itself. `GET …/sketch/shapes/{id}?format=text` showed the edge jumping back across the
  ring; the store had said nothing.
- **The first walls stood as black teeth and then as cobble posts down the faces**, because a polyline's band
  spills over a slanting edge. A thin polygon strip inside the terrace is the fix.
- **Back-row houses drew `DR-PASS`** until the tiers stopped a block past the plan's coast, which had moved the
  coast out by that block.
