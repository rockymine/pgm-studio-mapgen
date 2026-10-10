# exp-abbeymoor-min — Abbeymoor on a studio running `Rules:Mode=minimal`

Sonnet 5.5, 2026-10-10, against `http://localhost:7895/api`. The board is `maps/exp-abbeymoor-min/`, its spec
`specs/exp-abbeymoor-min/` (`build-spec.py` writes the plan and the refinement; the driver stored them), its
renders `specs/exp-abbeymoor-min/renders/`. Brief 2 of `analysis/freeform-vs-studio/experiment/BRIEFS.md`.
Nothing under `specs/exp-abbeymoor-studio`, its report or its renders was opened.

## What I set out to build

**Abbeymoor: a heather moor pinched in the middle by a black peat bog, where each team holds the hill of a
ruined abbey with a crypt under it and an orchard village in the hollow below, and the way across is a pair of
stone causeways crossing inside a ring of standing stones.** A player remembers the stone ring in the bog, the
obsidian pillar standing over the ruined nave against the sky, and that the crypt is a second road under the hill.

The arrangement is one hourglass-shaped island, 286 by 102 blocks (x −143..143, z −51..51), spawn point to spawn
point 228 blocks, joined by land across the bog (no void between the teams, no build zone). The red half is
authored at x < 0 and `rot_180` draws blue; the image of a block `(x, z)` is `(−x−1, −z−1)`.

**Per side, eight places, each with a reason a player goes there:**

| place | where (red; blue is the image) | why a player goes |
|---|---|---|
| spawn hall and ridge | hall x −124..−104, z −8..16, point (−114, 4), doors +x and −z; ridge push at (−134, 2) | where the team starts; 16 blocks of heath and a 7-block ridge with two hawthorns behind it (x −140..−124) |
| abbey ruin | nave floor x −104..−68, z −36..−22 at y34; walls to y39, tower stump to y44 at (−106..−100, −26..−20) | holds the **Abbey Stone** |
| crypt | chamber x −98..−82, z −35..−24, floor y26, air y27..31, roof y32..34; four pillars, two tombs, four glowstone lamps | the second road to the Abbey Stone |
| village green | green at (−60, 28), hollow at y19; cottages (−80..−72, 22..28), (−74..−66, 8..13), (−50..−42, 10..15), (−74..−66, 38..43), (−54..−49, 32..36) | holds the **Market Cross**; fought through room by room |
| orchard | 3 × 3 lattice of small oaks 8 apart at x −100, −92, −84 × z 32, 40, 47, and (−62, 47), (−54, 47) | cover on the south flank, a way round the green |
| tor | push at (−50, −44), 9 high, two boulders (−54, −45), (−45, −41) | a lookout over the bog and the north approach |
| peat yard | stacks x −46..−35, z −46..−41; a cottage (−46..−38, −36..−31) dug into the tor's foot | forward post at the bog edge where the abbey causeway starts |
| sheepfold | ring wall x −126..−113, z −38..−29, path from the spawn's north door | north flank cover, the way the −z door leads |

**Shared:** a ring of eight standing stones, radius 15 about (0, 0), three blocks square and 8 to 12 tall (red
side authored at (14, 6), (5, 14), (−6, 14), (−14, 5), the rest are their images); two causeways from (−46, 34) and
(−54, −28) to the origin and out the far side, crossing in the ring; three tarns on the red side at (−14, −18),
(−24, 33), (−6, 20); three hummocks with a hawthorn on two of them.

**The objectives**, one at the abbey and one by the village, a team each:

| monument | at | made of | floor under it | float |
|---|---|---|---|---|
| red Abbey Stone | (−74, −30) | obsidian `pillar-3`, y39..41 | nave roof, top block y34 | 4 |
| red Market Cross | (−60, 28) | gold `cube-3`, y24..26, bedrock centre | village green, top block y19 | 4 |
| blue Abbey Stone | (73, 29) | as red | | 4 |
| blue Market Cross | (59, −29) | as red | | 4 |

Walks (`plan/inspect`): Abbey Stone own spawn 55, enemy spawn 198 (ratio 3.60); Market Cross 66 and 187 (2.83).

## The plan review, once, before the first store

I reviewed the plan against the brief and the twelve lessons after the compile and before the first drive, and I
am writing it down here from what I decided then; it was not written to a file at the time.

- **Land and routes.** One island, land across the bog, two ways across (the causeways) and the open peat between
  them. The attackers' view of both monuments is from the east, over the bog. Kept.
- **Monuments.** Both off the spawn–spawn line (abbey 40 forward and 34 to the side of the spawn, village 54 and
  24), both on open ground with no tree within ten blocks. The Abbey Stone is in the open east end of the nave and
  not on a tower top. Kept.
- **Crypt.** Needs a second entrance or it is a defenders' cellar. Decided: a stair well from the nave beside the
  Abbey Stone, and a lane from the hill's east flank at (−52, −29) running under the monument into the chamber.
- **Dead ground.** The compile's `plan/flow` read 46% dead on a 120-wide board. Cut to 102 wide and added the
  fold, the tor and the peat yard so the north moor has something in it; 38.9% fell to 24.4%.
- **Lesson 6** (spawn exit) and **lesson 4** (trees) checked against the plan: trees stay off the hall's doors and
  off every causeway; the orchard is a lattice off the street.

After the top-down I changed three things: the spawn hall's west door (a west neighbour piece gave it one) went by
deleting that piece, the paved nave floor read as a grey slab so the nave went back to turf with a paved aisle
over the lane, and the first orchard (6 apart) was declined by tree crowns until it went to 8 apart.

## The numbers

```
ground   25102 walked, 404 scrambled, 1108 barrier — 5.7% steps further than a player walks
props    75 placed, 8 declined   (every one of the eight is a kept complaint: dressing-report.json drops none)
routes   worst step 7, on route spawn-0 to destroyable-0   (it is the spawn hall's own wall on the straight line)
coverage 24.4% dead — two patches of about 2 900 cells, (−118, −11) and its image (116, 9), the heath behind each spawn
preflight export gate OPEN; export 200 with Pgm-Warnings: DR-DIG DR-KEEP DR-PASS DR-ROAD OB19 WX13
relief    team: 16 204 cells, low y17, high y38, symmetry error 0
```

The 1108 barrier cells are the ruin's own walls (largest face 155 cells at x −107..−92, z −39..−20), the standing
stones and the cliff face of the hill's south flank. Nothing is a barrier on a spawn → monument line except the
hall wall and the nave wall at (−74, −22).

**Verified with `column` and `transect`, not with a picture.**

| claim | read | answer |
|---|---|---|
| crypt exists | `column (−90, −29)` | solid y0..26, air y27..31, andesite y32..34 |
| the image has one | `column (89, 28)` | the same |
| lane is open to the sky past x −68 | `column (−58, −29)` and `(−55, −29)` | floor y26, nothing above |
| stair well walks | `transect (−82, −33) → (−62, −33)` | 28, 28, 29, 29, 30, 30, 31, 31, 31, 31, 32, 32, 33, 33, 34, 34, 35, 35; worst step +1, walked end to end |
| spawn exits | `walk (−114, 4) → (−96, 4)` and `→ (−114, −14)` | both walked end to end, no step over 1 |
| monument float | `column (−74, −30)`, `(−60, 28)` | obsidian y39..41 over top block y34; gold y24..26 over y19 |

## Times per phase

From `date`, 2026-10-10 UTC.

| phase | start | end | minutes |
|---|---|---|---|
| read the briefs, the three documents, `approaches.md`, `match-flow.md`, the skill, the technique cards, the API's schemas | 13:43:45 | 13:46:43 | 3 |
| identity, places, arrangement, the plan compiled and read (`plan/compile`, ASCII of pieces) | 13:46:43 | 13:50:15 | 3.5 |
| first spec, first store and export (`drive.py`, 16 s) | 13:50:15 | 13:50:40 | 0.5 |
| revisions: narrower board, crypt and its two entrances, orchard lattice, patches (five further drives) | 13:50:40 | 13:59:40 | 9 |
| strata, lamps, final drive and export (two drives) | 13:59:40 | 14:03:37 | 4 |
| renders (30 pictures) and read-backs | 14:01:19 | 14:04:51 | 3.5, overlapping the above |
| report | 14:04:51 | 14:08:03 | |

Building, first drive to last: about 13 minutes of wall-clock, which is less than the 20 to 30 the brief allowed.
Eight drives in all, every one 200; a drive takes 15 to 25 seconds.

## What the brief asked for that the tool could not express

Each was searched for by the name, by what it would do, and in the term list; the verdicts use the skill's three
words.

| asked for | what I did | verdict |
|---|---|---|
| **heather**, purple moorland | a grass / podzol / coarse-dirt ground, four `heath` patch shapes, and a `flora` field with flowers; Swampland biome so the grass is olive | **missing**: no purple ground block exists in the palette the themes allow; wool and clay are shade rows, not ground |
| **an orchard's greens against a dark bog**, two colours of grass | one solid Swampland biome for the whole board, so orchard leaves and moor grass are the same olive | **missing**: `biome` is a solid, cell or noise field (`GET /api/openapi/v1.json`, `BiomeField`), never a shape, so a biome cannot be put on the village and not the bog |
| **a standing stone** | erected 3 × 3 shapes, `height_mode: level`, `skirt: 0`, ruin theme, `keepClear` | **mistaken**, in the sense that no prop exists and shapes do the job; they are square columns, never leaning or tapered |
| **a ruined arch, a window, a broken vault** | rectangular wall courses at ragged heights and piers | **missing**: shapes are prisms; there is no stair-block or slab course in a shape's material, so no arch |
| **a stair** (crypt well, lane apron) | eight rectangles each one block higher than the last, on the crypt layer, inside a ground-layer `subtract` | **out of reach**: the stair instrument in `techniques/ramp-and-stair` is a tilted polygon; the well is a straight run, and a turn or a landing is built by hand with an extra long step |
| **a crypt under the hill** | a layer `crypt` (`below: true`, `base_y` 0) holding the floor, pillars, tombs, steps and lamps, and an override add on the ground layer at `floor: 32` for the roof | **works**, but nothing says "chamber": `SK13` complains of the steps because they fill what the subtract takes away |
| **light in the crypt** | four 1 × 1 shapes whose `material` is glowstone (id 89) | **missing** as a prop: `torch`, `lantern` and `glowstone` are not in the schema except the wool room's redstone torches |
| **a bog dark and wet** | peat as podzol / coarse dirt, three shallow pools at level 17, Swampland water | **partly missing**: there is no mud or soul-sand-slow ground that I was willing to use, and the render draws the pools plain blue |
| **dense peat**, hummocks in water | three hummock marks at y20 and a line mark under each causeway | works |

## The twelve lessons, one by one

1. **An objective is found without a map. Met, with one caveat.** The Abbey Stone is on the nave's open east end
   at (−74, −30), seen from the causeway at (−30, −12) as a black pillar over the skyline
   (`eye-abbey-stone-approach-causeway.png`) and from the hillside at (−66, −4). The Market Cross at (−60, 28) is
   in the open green and seen from the causeway at (−24, 14), but two cottages stand across the line and show it in
   a gap (`eye-market-cross-approach-causeway.png`); the green's east side is open. Neither is underground or on a
   tower. The crypt lane passes under the Abbey Stone and does not carry it.
2. **Made of what the mode needs. Met.** Obsidian `pillar-3` (three blocks, `DC3` quiet) and a gold `cube-3`; the
   kit's `diamond pickaxe` breaks both (`maps/exp-abbeymoor-min/map.xml` slot 2).
3. **A wool room holds the standard loot.** Not applicable: a destroy board has no wool room. The studio puts one
   defence chest a course over the ground under each goal, which the render of the nave shows.
4. **Vegetation leaves the floor visible. Met.** Trees: a 3 × 3 orchard lattice 8 apart off the village street,
   two more beside it, a hawthorn on two hummocks and two behind the spawn; none on a causeway or in the bog. The
   `DR-CLAIM` declines on my first orchard (6 apart) were the crowns saying the same thing.
5. **Every stair is attached and walkable. Met for the one I built.** The stair well (x −82..−64, z −35..−32)
   has trench walls of ground on both sides, rises 8 in two flights of 4 with a four-block landing at y30 (x −76..−72),
   and no turned stair is anywhere. The lane's mouth has two apron steps (x −54..−50). Two stairways do not collide.
   The ruin's steps and the hill are slopes of one-block terraces; I did not build a diagonal ramp.
6. **A spawn's exit is open. Met.** Both doors (+x, −z) walk end to end with no step over 1; the hall's west
   door went with the piece that gave it one, and the street begins at (−103, 4).
7. **A floating platform cannot be mined away.** No platform floats over void on this board. The crypt roof is
   three courses of stone over five of air; the lane roof under the Abbey Stone carries a bedrock course at y31
   under the monument's footprint (x −76..−72) that appears with the goal.
8. **Ladders only where players need them, never in water. Met.** None: the stair well is steps.
9. **Every join is open. Met, read with `column`.** The lane meets the chamber at x −82 (floor y26 both sides), the
   stair well's first step (y27, x −82..−80) is one above the chamber floor, its last step (y34) equals the nave
   floor, and the apron at x −50 meets ground at y23..24.
10. **Things are at a player's scale. Mostly met.** Ruin walls two thick, stones 3 square, houses 9 × 7, tarns
    10 to 16 across, a 3-wide lane and well. The spawn hall is 18 × 22, the largest thing on the board, and `ST9` and
    `WX13` both complain it is over 20.
11. **Ground varies in patches, bare stone carries detail. Half met.** Four patch shapes with their own `heath`
    theme (at (−108, −26), (−131, 18), (−102, 36), (−64, −50)), the slope stack's three bands, `flora` flowers
    in fields; the cliff faces and underside are laid in strata (`layered`, `height` axis, `follow: 100`, `reach:
    16`), but I did not look at the strata in the game's textures, and in the isometric they read one grey.
12. **A build zone shows where to build.** Not applicable: the sides are joined by land and the board has no
    build zone.

## The relaxed rules

**How I sorted them.** A finding that arrives as a complaint is either one the rule raises as a complaint in every
mode, or a refusal or decline that `RulePolicy` (`pgm-studio/src/PgmStudio.Vocabulary/RulePolicy.cs`) turned into a
complaint because the rule is not in `MinimalRules`. The two look the same on the wire, so I read the severity
each finding is constructed with in the source (`new Finding(rule, message, Severity.X)`; the default is
`Refusal`) and a dressing site's `TurnsAway`. I did not run these documents against the rules-on studio; each
"would have" below is that reading, not a test.

### A. Complaints that exist only because the rules are relaxed

| rule | what it said (this board) | would have, under the full rules | kept or changed, and why |
|---|---|---|---|
| `SK13` ×11 | the nine stair steps, the lane floor and the two apron steps on layer `crypt` *fill* columns the ground layer's `stair-well` and `lane-cut` subtracts take away | **refused**: `SketchLayoutCheck` writes `survives ? Refusal : Complaint`, and these all survive | **kept.** It is the crypt's two ways in: the subtract opens the sky over the stair well and the lane, the add on the lower layer is the step. This is the one finding that changed the board |
| `OB19` | cottage `cott-5` at (−54, 32..36) stands inside the clearance of the Market Cross | **declined** by the dressing pass, and the export refuses a building inside a goal's clearance (409) | **kept**, on purpose: 6 blocks from the cross (the four-block cover rule holds), a building defenders hold at the green |
| `DR-ROAD` ×2 | the tor boulders at (−55, −44) and (−45, −42) stand one block off a path | **declined**, both boulders dropped | **kept.** Both are in the world at their stated cells; `edit` offered a one-block move |
| `DR-KEEP` ×1 | boulder (−45, −43) on a cell kept clear for the peat cottage; first drive: two hawthorns at (−137, −4), (−136, 14) and one at (−120, −26) in front of a door | **declined** | the boulder **kept**; the trees **changed** (the west door went with the piece beside the hall, the one at (−120, −26) was removed) |
| `DR-CROSS` (first drive) | `cott-2` overlapped `hill-path` and cut it in two runs | **declined**, the cottage dropped | **changed**: path moved to x −62..−61 |
| `DR-DRY` ×3, `DR-HELD` (first drive) | the tarns stood against open columns at level 18, one over a kept-clear cell | **declined** | **changed**: level 17 and moved off a hummock and the causeway |
| `DR-STEEP` (second drive) | boulder on 53° ground | **declined** | **changed**: boulder moved |
| `PT4` ×6 (first dry run) | wall and fill patterns with a rise of 0 | **refused** (`new Finding` with the default severity) | **changed**: `rise` 2 on every cell pattern; the strata replaced them |

**Declines that still dropped something under minimal rules** (the rules that keep one prop off another prop and
a prop off nothing): six orchard trees whose crowns met at 6 apart (`DR-CLAIM`) and the tor boulder at (−53, −50),
which had no ground (`DR-SITE`). All were fixed by moving them; none is in the final world.

### B. Complaints in every mode (shown, not a relaxation)

| rule | what it said | kept or changed |
|---|---|---|
| `GO1` | Market Cross 2.83 times as far from the enemy spawn as from its own, under 3 | kept; moving it back 5 blocks makes the ratio and loses the village's green |
| `GO2` | the two monuments of one team 67 apart, over 65 | kept, by 2 blocks |
| `GO3` | 173 between the two Abbey Stones, over 150 | kept: 228 between spawns and a monument forward of its spawn cannot be inside 150 |
| `LN5` | 34% of the ground off every route, over 12% | kept; 46% before the board was narrowed |
| `LN2` (first drive) | longest straight run 120, over 110 | did not return after the plan lost its west piece |
| `EL1` ×3 | `moor-n`, `moor-s`, `moor-m` each 4 above the bog piece where they share an edge, over 1 | kept: the relief grades 4 over 36 blocks; each carried an `edit` for a six-wide ramp mark that I did not take |
| `ST9`, `WX13` ×2 | spawn hall 18 by 22, over 20 on a side | kept; the first footprint (10 by 22) was a door gap eating the hall |
| `ST10` (first drive) | the spawn piece 24 by 24, over 20 by 30 | changed to a 20 by 24 piece |
| `SK27` | the island has two plateaus (18, 22) with two paints | kept: the bog and the moor |
| `RL6` ×3 (first drive) | the abbey hill, spawn ridge and tor climb skirt and crown 4.1, 5.7 and 2.1 times apart | changed: falloff 18 → 26 and crowns 2 → 4; none on the last drive |
| `DR-PASS` ×3 | cottages `cott-1`, `cott-2`, `cott-4` leave a passage under 8 | kept: a village street, 5 to 7 between two cottages |
| `DR-DIG` | cottage `cott-6` at (−46, −36) digs 5 into the tor's foot, over 3 | kept: a peat cutter's cottage cut into a bank (40 columns, 75 blocks removed) |

**What the relaxed rules let me build that I believe the full rules would have stopped:**

1. **The crypt's two openings** (`SK13`): a stair well cut through the nave floor and an open lane cut into the
   hill's flank, each with the step or floor on a lower layer under a ground-layer subtract. I believe this is the
   one that matters. Under the full rules the crypt would need another way up, a stair under a roof with no opening
   to the sky, or a hole by arrangement (ground shapes ringing a gap), and the lane's open cutting would not exist.
2. **A cottage inside a monument's clearance** (`OB19`), which is the dressing pass's decline and the export's 409.
3. **Two boulders on a path and on a kept-clear cell** (`DR-ROAD`, `DR-KEEP`).
4. Nothing else. `GO1` to `GO3`, `EL1`, `ST9`, `WX13`, `LN5`, `SK27`, `RL6`, `DR-PASS` and `DR-DIG` are complaints
   under the full rules as well, so the board's outside-the-band walks, its 4-block seam and its oversize hall are
   not results of the relaxation. A full-rules builder with the same plan would have met the same complaints.

**What the relaxed rules did not touch:** `RQ1` refused my first plan (*a component mixes mirrored and
non-mirrored pieces*: a bog piece stated `mirrors: false` beside mirrored ones). It is a readability refusal and
fires in both modes.

## What went wrong

- **The first plan stated `mirrors: false` on the bog piece and was refused `RQ1`.** A piece centred on the origin
  is its own image, so the default `mirrors` is the right word; I had read the field from the schema and taken it
  to mean "do not double it".
- **`drive.py` clears `renders/` on every run**, so every drive wiped the pictures I had taken; the thirty in the
  folder now are from the last drive. Taking pictures after the last store is the order the driver wants.
- **The head of the report says `props 75 placed, 8 declined` and `claims` prints each of the eight as
  `decline`**, while `region/dressing-report.json` carries them with `severity: complaint` and drops none, and
  every one of the eight is in the world. Under `Rules:Mode=minimal` the head number is therefore a count of kept
  complaints, which reads as a loss. It is a labelling fault in the read-back, not a build fault.
- **A report render of the spawn from `from=` stands in the hall's eaves**, which is how I first read the hall as
  having no door; the `walk` read said otherwise and is the one that settles it.

## What worked first time

The compile, the store and the export, from the first drive: a 286 by 102 board with a crypt layer, a lane cut
and a well cut, 22 crypt shapes, 35 ground shapes and 38 props was 200 and exported with the gate OPEN in 16 seconds.
`column`, `transect` and `walk` settled every question; the `look=` camera of `render/eye` frames a thing without
my working out a pitch. The `bendShapes` and `shapePropsById` ring gave the hourglass without a second shape.

## Open gameplay questions decided without an oracle

- **Is a crypt lane that lets attackers walk under a monument a second approach or a shortcut?** It enters the hill
  at (−52, −29), 22 blocks from the causeway's end, and arrives beside the Abbey Stone through the well, so an
  attacker who finds it is in the nave in about 40 blocks. I built it and did not measure what it does to the walk.
- **Is a 3-block roof over a 5-block chamber too thin for a defence?** Three courses of andesite is mined through in
  seconds from the nave; a monument over the lane is open to a player digging up from the lane. I left the roof, as
  the clarification asked for building up a few blocks under a monument, and the lane roof at y31 under the monument
  is the studio's bedrock.
- **Is a Market Cross of 27 gold blocks too slow to break against a one-block pillar of obsidian?** The two
  monuments of a team are not the same task by design; I did not weigh it.
- **Does a cottage 6 blocks from a goal read as cover (approaches.md) or as a covered goal?** Kept as cover.

## The files

`specs/exp-abbeymoor-min/build-spec.py` writes `exp-abbeymoor-min.plan.json` and `.refinement.json`; the driver
wrote `.layout.json`, `.intent.json`, `exp-abbeymoor-min.png` and `provenance.json`. Renders, each by the camera
that drew it:

- the four isometrics `iso-south-east|north-east|north-west|south-west.png`, `topdown.png`, `topdown-material.png`,
  `xray-south-east.png`, `xray-north-west.png`;
- the crypt cut along x at z −29 and along z at x −90: `section-crypt-lane.png`, `section-crypt-chamber.png`;
- the Abbey Stone from the causeway `eye-abbey-stone-approach-causeway.png`, from the hillside, from inside the nave;
- the Market Cross from the causeway and from the green; the red spawn's exit and the hall from the street; the
  village street and the orchard;
- underground: the chamber both ways, the stair well from the nave and from the crypt, and the lane's mouth from
  outside; the bog stones from both sides; the blue Abbey Stone; the tor and the peat yard.
