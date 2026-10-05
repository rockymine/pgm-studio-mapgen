# Sciara — two hill villages on a volcano's flank, each defending its core on the threshing floor

> A destroy-the-core board. Each team's core floats over the paved aia (threshing floor) of its village, in
> the open. Olive terraces lie on one side and a black lava flow, the sciara, stands above it on the other.
> The village with its campanile is behind, and a ravine over void with a build zone parts the two flanks of
> the mountain.

**In one sentence:** a Sicilian hillside where every made thing — the terraces, the yard, the threshing
floor — is held up by walls of the black lava stone the mountain is made of, and the core is fought for from
four directions that are not the same way twice.

96 × 248 blocks, `rot_180` about the origin, plan surface 22, `maxbuildheight` 50, Savanna biome (grass
`#bfb755`). Red's unit is authored on `z < 0`; every blue coordinate below is the image, `(−x−1, −z−1)`.
Built on the deployed studio as `opus55-sciara`, change 11.

## The board, read off the two lines

The spawn stands at the back of the village at `(−9, −106)`, y34. The core stands 50 walked blocks forward
of it on the aia, at `(10, −64)`, its casing obsidian at y37 and y41 with lava at y38–40 over a paved floor
standing at 31.

In front of the aia, open ground falls from 27 to the ravine lip at 22. The ravine is 24 blocks of void with
one build zone across the whole width, `z −12..12`.

The plan tier reads the core's own walk as 52 and the enemy's as 168, so `GO1` is **3.23**. The built board
walks spawn to own core end to end in 50 blocks with no block placed.

## Four ways onto the core, and why each is where it is

| Approach | Where | What it costs | Measured |
|---|---|---|---|
| **through** the olives | the two olive terraces west of the aia, `x −47..−6`, at 25 and 28 | three flights, under cover the whole way | `stair-lip`, `stair-olives`, `stair-olive` each walked end to end, worst step 0 |
| **above**, off the sciara | a push down the east flank, ring centred `(37, −63)` | a climb up the flow's snout, then a 28-block bridge | crest y39 at `(38, −64)`, two over the casing's lowest course; lip `(30, −16)` to crest `(38, −64)` walked end to end |
| **below**, out of the cava | a sunk quarry pit at `(14, −32)` | a tunnel of about 30 blocks under the aia | floor y18–19 against slope y22–27 round it (transect `x 14, z −24..−42`) |
| **straight up** the open slope | `x −6..26`, `z −46..−17` | exposed the whole way, then a 4-block lava-stone wall | one flight in it, `stair-front` at `x 18..23`; the face elsewhere is the defenders' line |

The defenders come down from the piazza by one flight, `stair-piazza` at `x 6..11, z −86..−80`, three
blocks onto the aia.

## Made ground meets grown ground, and every meeting is a flight

**Every terrace is a shape carrying `relief_scope: "exclude"`, so it meets the relief at a face.** The face
is painted as the lava stone through the theme's `wall`, under a one-course grass rim. The rim is what
keeps the surface stack's soil from claiming the top of the face. Every rise a player climbs is a
`height_mode: "level"` polygon with half-riser anchors, two blocks of run a course, `keepClear`, and
polished andesite.

| Flight | Footprint | From → to | Walk |
|---|---|---|---|
| `stair-lip` | `x −22..−17, z −28..−22` | lip 22 → lower terrace 25 | `(−19,−18)→(−19,−34)` end to end |
| `stair-olives` | `x −30..−25, z −54..−48` | lower 25 → upper 28 | `(−27,−44)→(−27,−58)` end to end |
| `stair-olive` | `x −6..0, z −62..−57` | upper 28 → aia 31 | `(−10,−59)→(4,−59)` end to end |
| `stair-front` | `x 18..23, z −56..−48` | slope 27 → aia 31 | `(20,−44)→(20,−60)` end to end |
| `stair-piazza` | `x 6..11, z −86..−80` | aia 31 → piazza 34 | `(8,−76)→(8,−90)` end to end |
| `stair-grove` | `x −40..−35, z −82..−76` | upper 28 → verge 31 | `(−37,−72)→(−37,−86)` end to end |
| `stair-yard` | `x −40..−35, z −96..−90` | verge 31 → yard 34 | `(−37,−86)→(−37,−100)` end to end |

**Each flight is set into a notch cut in the upper terrace's outline**, so the stair sits in the wall rather
than leaning on it. The three that climb onto relief ground stand on a mark that pins that ground first:
`lip` at 22, `slope-top` at 27, `verge` at 31.

## What the ground is made of

Three themes, each a place: **campagna** (76%) — savanna grass to 34°, dirt and coarse dirt half and half
to 48°, the lava stone beyond; **sciara** (15%) — the lava stone as ground, grey stained clay and coal block
patches at the ends of a noise stop list; **borgo** (9%) — granite, polished granite, hardened clay and
brick a quarter each in a three-block cell, on the piazza and the aia's paved circle.

**The lava stone is one rock and it is everywhere a face shows.** Black stained clay, grey stained clay and
coal block, in a two-block cell with a rise of 2, are the wall, the fill and the steepest slope band of
every theme. A terrace wall, the ravine cliff and a tunnel dug toward the core all cut the same rock.

The three tone families are warm ground (savanna grass, soil), built white and red (quartz walls, brick
roofs), and black lava stone as the accent. The accent appears at every wall, the sciara, the cava and the
two boulders.

## The village

Three houses in one library style, `brick-roofed-quartz-house`, which also stamps the spawn hall. They stand
at `x −38..−28, z −114..−108`, `x 12..22, z −114..−107` (two storeys) and `x 30..38, z −112..−104`. A lane
two cells deep behind them, `z −124..−116`, gives every house its 8-block passage to the coast.

The campanile stands on the piazza's corner at `(−29, −104)`. Its quartz shaft runs y34–46, four quartz-pillar
posts frame an open belfry to y50, and a stepped brick cap runs y51–54. It is two `kind: "made"` layers,
because the posts and the cap are two spans of one column.

## Dressing

Eight copied olives (`olive-3`, `olive-7`, `olive-9`) and one young one (`small-olive-2`) stand along the
outside of the two terraces, none within 26 blocks of the core and none on the lip. Two more young olives
stand by the houses, and two angular lava-stone boulders sit on grass at `(24, −22)` by the sciara's snout
and `(−2, −30)` at the grove's corner.

Five solid farm tracks of dirt, coarse dirt and spruce planks run flight to flight. Ground cover runs over the
whole side at coverage 0.22, tall grass 0.03 and dead bush 0.15. 44 props are placed and none declined.

## What went wrong

- **The first store answered 200 and every read of it refused.** Two document faults, both stored silently:
  a biome written `{"name": "Savanna"}` where the wire takes `{"kind": "solid", "id": 35}`, and a `{"use"}`
  nested inside `materials`. `reports/opus55-sciara.md` has the probe.
- **Terrace faces came out as soil.** A surface stack three deep claims the top three courses of an edge
  column, which is the whole of a three-block face. The grass rim one course deep is the fix.
- **The first house sat in the spawn's west door approach (`DR-KEEP` at `(−35, −108)`).** A yard 20 deep
  could not hold a house with 8 blocks of passage front and back (`DR-PASS`), which is what the back lane is
  for.
- **The sciara's crest first stood at 37, level with the casing's bottom course**, which is height over the
  defenders and not over the goal. The lift went from 6 to 8.

## Readings

`ground` 20 796 walked, 840 scrambled, 1 122 barrier (8.6%) · `props` 44 placed, 0 declined · relief
`level` 0.41, `largestField` 0.16 · incline 61% under 10°, 12% at 30–39° · coverage **48.0% dead**, the two
patches centred `(4, −70)` and `(−7, 67)` · pre-flight `export gate OPEN`.

The report's worst step, 39 on `route spawn-0 to core-1`, is not the board's. It is the walk read climbing
over the observer platform at y60, which the read cannot pass under. The same crossing walked at `x −30` is
`28 blocks, 19 placed, worst step 0`.
