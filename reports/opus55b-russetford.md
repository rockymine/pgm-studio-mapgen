# Opus 5.5 — Russetford, one destroy board on the deployed studio (2026-10-07)

## What I set out to build

**An autumn river valley for two teams of sixteen, one monument a team.** I built it twice. The first build
followed the brief to the letter and came out a ramp with three houses on it. The author reviewed it, and
the second build starts from a zone plan, `specs/opus55b-russetford/composition.md`.

**What the second build set out to be, written before its first request:** *a meandering river through the
bottom of one valley, each side a working place. The farm under a wooded ridge holds the spawn, an orchard
runs down to a cut bank with a cave in it, and the monument stands on the green where the lanes meet. The
street runs past cottages to a mill on a leat, and a hanger of oaks climbs to a ruined tower.*

**Tone families.** Ground: grass under a mosaic of Plains, Savanna and Mesa tints (green, gold and russet),
over earth, with rock in beds of stone, andesite, pale clay and terracotta on the steep. Built: white clay,
stone under brick, a stone longhouse and a stone-footed tower, none of them timber-framed. Accent: dark oak.

Slug `opus55b-russetford`, map name **Russetford**, credited to Opus 5.5. The board is written up in
`review/opus55b-russetford.md`.

## What was wrong with the first build

**It had no composition.** I chose the "spawn on a hill, monument ahead and aside" layout and added a wood
beside the monument. After that the board was one tilted field with a few houses on it, which is the
emptiness the author described. The dead-ground figure was 37%, and adding trees to lower it would not
have given the ground a purpose.

**The river was a ruling followed past its sense.** I read *the two teams' ground is joined by a build zone
over void* as binding a river too. The result was a straight strip of water along each coast and void in
the middle. A river *is* the middle of the map, and the author said so: it is crossed by swimming, bridging
or the bridge, and it needs no build zone.

**One biome painted the whole board one brown.** Mesa's tint was the autumn idea, but used everywhere it
was monotone. The rebuild uses a noise `BiomeField` of three tints instead.

**The brief was short, and I treated that as permission to stop early.** One sentence of identity is the
header of a board, not the board. What the rebuild did differently was draw the zones first: what each
one is, why a player goes there, and how they get there. The top-down was then checked against that
drawing after each pass.

## How the layout was chosen

**The layout is a valley with the river as its seam.** It is not one of the corpus layouts as it stands.
It takes the vertical idea of `a box cut by water, walled by mountains`: spawn high, monument lower in
front, reached from the heights, from the river and from below. It also takes the villages and the river
of `a long lane of rolling ground` without its lane.

**The meander came from the symmetry.** An S through the origin is its own image under `rot_180`, so each
team gets one outer bend, where its bank is a cut cliff, and one inner bend, where its bank is a gravel
beach and water meadow. The two crossings of the river therefore play differently for each side without
the board being unfair.

**`ORDER-OF-WORK.md` §1 decided three things.** No lane: the monument is on the green where three lanes
meet, at the end of none of them. The spawn stands in its land: the farm is seated on a knoll with twenty
blocks of its own land behind it, the ridge rising behind and the farmhouse built onto it. The objective stands in
front and to one side: 38° off the line between the spawns.

### The spawn's seat, measured

| Measure | Red spawn `(−32, −76)`, ground y40 | How it was read |
|---|---|---|
| land behind | **20 blocks**, ground to `z −96`, void at `z −97` | `column` at `(−32, z)` |
| highest ground within 20 | **8 above**: the ridge at y48 from `z −94` | `transect (−32,−76) → (−32,−96)` |
| what stands beside | the farmhouse built onto the spawn tower, the hay yard east, oaks on the ridge at `(−14, −90)` and `(−2, −86)` | the dressing |
| corpus median / agent boards | 20 behind, 8 above / 10 behind, 0 above | `destroy-layouts.md` |

### The goal against its spawn

| Goal | Straight from the spawn | Ahead | Aside | Off the line | Walk |
|---|---|---|---|---|---|
| red monument `(4, −56)` | 41 | 32 | 26 | 38° | 44 (`route spawn-0 to destroyable-0`) |
| from the enemy spawn | — | — | — | — | 145, 1 placed (`route spawn-1 to destroyable-0`) |

`POST /plan/inspect` read own 44, enemy 138, ratio 3.14 against `GO1`'s 3–4.

## What the run cost

| | first build | rebuild |
|---|---|---|
| wall time, first request to final store | 20:26 → 20:45 UTC, 19 minutes | 21:51 → 22:04 UTC, 13 minutes of driving, after the composition was drawn |
| stores (`PUT …/source`, not dry) | 14 | 10 |
| plan revised in a store | 2 | 1 |
| relief revised in a store | 5 | 6 |
| finish revised in a store | 13 | 9 |
| stores refused | 0 | 2, by `PT3` and `PT4`: a wall pattern with a 1-block period and no `rise` |
| other refusals | 1 dry `PT4`; 1 export `RQ1`, the biome stated as a word | none |

**The three numbers on the final store:**

```
ground   23541 walked, 843 scrambled, 224 barrier — 4.3% steps further than a player walks
props    66 placed, 8 declined
routes   worst step 2, on route spawn-0 to destroyable-1
```

**The eight "declined" are complaints in every other read.** They are five `DR-PASS` on the village's
alleys, two `DR-BANK` (the cut bank and the leat's tail) and one `DR-CUT`. Every building is standing in
`column`. Part of the barrier is the hedges, which are two-block walls of leaves by design.

**The deployed studio never made me wait.** No `429` reached the driver in twenty-four stores.

## The third pass, after the author's second review

**Twelve asks, seven stores, 22:22 → 22:30 UTC, none refused.** The asks and what was built for each are
in the review's *third pass* table. Three of the fixes taught something about the instruments.

**A stroke repaints water.** A lane drawn across the leat paved its surface, so the footbridges stood over a
strip of andesite. A lane now stops at a bank. *Mistaken on my part*: `GENERATION-NOTES.md` says a stroke
reads the surface top of every column it crosses.

**A fluid's carve empties the ground's course above its line, made things included.** The wheel lost the
course between the water and its own lowest block, so it hovered a block over the water. The carve reaches
only as high as the ground the channel crosses, so the mill yard is now at the holm's level and the wheel
stands on the water.

**A height stack does not cycle.** `ending: repeat` carries the last band on for good, so a nine-block set of
beds painted everything above y11 pale clay. The beds are written out seven times.

**The final store's three numbers:**

```
ground   23402 walked, 804 scrambled, 382 barrier — 4.8% steps further than a player walks
props    86 placed, 9 declined
routes   worst step 2, on route spawn-0 to destroyable-1
```

**The nine "declined" are complaints everywhere else.** They are five `DR-PASS` on the village alleys, two
`DR-BANK`, two `DR-CUT`, and an `SK18` where a footbridge meets the mill's eaves. Coverage reads 40.2% dead.

## What I could not say

**A waterwheel with spokes.** A layer holds one span a column, so a wheel standing on edge is a solid disc;
`tools/sculpt/solid.py` would compile a ring into two layers. *Out of reach from where I was standing*: I
chose a slatted `checker` disc.

**Biome by place.** I wanted green water meadows by the river and gold on the hanger. `BiomeField` is
`solid`, `cell` or `noise`, all over the whole board, and no shape or theme carries a biome. *Missing from
the system*: the mosaic is a noise field I looked at and kept, not a placed one.

**A boat on the river, sheep in the pasture.** Neither is in the dressing vocabulary (`GET /api/openapi/v1.json`,
`DressingPropDto.kind`: stroke, fluid, tree, boulder, flora, chest, buildings). *Missing from the system.*

## What I got wrong

**The first build's composition, above.** It is the large one.

**I stated the biome as a name.** `"biome": "Mesa"` stored at 200 and the export refused it `RQ1`. The store
taking a field the export cannot read is worth the studio's attention.

**I assumed an added shape with a theme and no height would paint the ground under it.** It is one block at
y0 and owned no surface: 0.7% and 2.4% for two of three themes until it was given the ground's thickness.

**I built a hill with a push beside a marked village.** A push is added after the marks, so its skirt lifted
the village and steepened every edge to 55–60°. A summit mark that the solver grades down replaced it.

**I sealed the cave's mouth.** The polygon stopped two rows short of the water. `column` at `(−28, −20)` read
solid ground, and the walk read `unreachable`.

**I laid hedges in decayable leaves.** Every read showed them, and the game would have rotted them. `18:4`
is the leaf that never decays.

## What worked first time

**The river as a channel through the origin.** One fluid prop drawn on half the S, with its image
completing it, gave a continuous meander with a cut bank where the ground stood high and a beach where it
stood low. The carve made the cliff by itself.

**The cave under relief-solved ground.** An override add with a `floor`, over a `below` layer stating the
floor, gave three courses of air, and `walk` with a `y` walks it.

**Draped polylines for hedges and walls.** `height_mode: drape` lays a one-wide boundary at a constant height
over a slope, which is what a field boundary is.

**The ruined tower from `tools/sculpt/props.py`, seated on the ground.** `drum_tower` with `seat: "ground"`
landed on the hanger's summit without a height being stated.

## Instruments, counted

One relief, eleven `area` marks and one `line`, no push, one made-ground shape (the cave roof), eight
draped polylines, nineteen made layers, five copied tree styles, two boulder styles, two fluids, five themes. There is still no
authored flight: the farm and the green are reached by graded slopes, not stairs.

## Open gameplay questions

1. **Is a premade bridge on the middle right?** It gives a dry crossing from the first minute. I kept it,
   because the river is swum anywhere else and the middle wants a structure, but it may make the centre too
   easy.
2. **Is the cave too strong?** An attacker who swims to it walks under the orchard to nine blocks from the
   monument's anchor. Its roof is about six blocks.
3. **Are two-block hedges right?** They channel players onto the lanes and are cover. One-block hedges would
   be jumpable and say the same thing more quietly.
4. **Coverage reads 46.5% dead.** The ridge wood, the saddle pasture and the hanger are framing ground off
   the two journeys a one-goal board has. Each has something in it (the woods, the walls, the tower, the
   woodpile), and the hanger is the height beside the monument. I did not cut ground to move the number.
