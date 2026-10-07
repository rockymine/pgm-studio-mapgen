# Opus 5.5 — Russetford, one destroy board on the deployed studio (2026-10-07)

## What I set out to build

**An autumn river valley for two teams of sixteen, one monument a team.** Written before the first request:
*each team holds one side of a valley, its spawn house on the ridge with a crag at its shoulder, its monument
on a shelf below and aside of it, a watermill hamlet on the bank, and a mine adit from the strand into the
hillside — the river between them crossed by a bridge the teams build.*

**The three tone families were named with it.** Ground: tan Mesa-tinted grass over earth and grey rock on the
steep. Built: white clay under spruce. Accent: dark oak — the wheel, the axle, the adit's timbers and the
roofs' verges.

Slug `opus55b-russetford`, map name **Russetford**, credited to Opus 5.5. The board is written up in
`review/opus55b-russetford.md`.

## How the layout was chosen

**Five layouts were weighed against the brief, and the brief had already chosen most of the shape.** A
river between the sides is a seam across the board, so the arrangement is two landmasses facing each other
across it. The `long lane of rolling ground` has a river and villages, but it is a lane with two monuments a
team, and `ORDER-OF-WORK.md` §1 rules the lane out.

**`a box cut by water, walled by mountains` gave the vertical idea.** Its spawn sits high on a massif and its
monument on lower ground in front, reached from the heights or from below. Russetford is that idea turned
into a valley side: spawn on the ridge, monument on a shelf twelve blocks below it, an adit coming at it
from under the slope.

**`a tour widened into land` and `islands in a box` were the outline's lesson.** Both seat the spawn on raised
ground at the outer edge of a landmass that is not a rectangle. The compiled rectangle was reshaped point by
point and bent so the bank reads as a coast rather than a box.

**I departed from the corpus's sea of islands and the rim round a basin.** Both put water or void *inside* a
team's ground, and the brief's river is between the teams. `approaches.md` says void belongs between the
teams and not across an approach, and the author's ruling in `WHAT-A-BOARD-IS-MADE-OF.md` joins the sides
by a build zone over void, so the river's middle is void and its water runs along each bank.

**`ORDER-OF-WORK.md` §1 decided three things.** No lane: the monument is on a shelf off the spawn's line,
not at the end of anything. The spawn stands in its land, not behind it: twenty-one blocks of its own bank
behind it and a crag beside it. The objective stands in front and to one side: 42° off the line between
the spawns, inside the corpus's interquartile range of 18°–76°.

### The spawn's seat, measured

| Measure | Red spawn `(−32, −80)`, ground y44 | How it was read |
|---|---|---|
| land behind | **21 blocks** — ground to `z −101`, void at `z −102` | `column` at `(−32, z)` |
| highest ground within 20 | **12 above** — top y55 at `(−51, −82)`, 19 blocks off | `column`; the crag peaks at y60, 25 blocks off |
| what stands beside | the crag west, an oak at `(−14, −84)` east, the spawn house itself | `transect` along x at `z −80` |
| corpus median / agent boards | 20 behind, 8 above / 10 behind, 0 above | `destroy-layouts.md` |

### The goal against its spawn

| Goal | Straight from the spawn | Ahead | Aside | Off the line | Walk |
|---|---|---|---|---|---|
| red monument `(7, −61)` | 43 | 32 | 29 | 42° | 47 (`route spawn-0 to destroyable-0`) |
| from the enemy spawn | — | — | — | — | 168, 18 placed (`route spawn-1 to destroyable-0`) |

`POST /plan/inspect` read own 43, enemy 150, ratio 3.49 against `GO1`'s 3–4.

## What the run cost

| | |
|---|---|
| wall time, first request to final store | **20:26 → 20:45 UTC, 19½ minutes** |
| stores (`PUT …/source`, not dry) | **14**, every one carrying plan, relief and finish together |
| plan revised in a store | 2 — the first, and the last (the build zone widened) |
| relief revised in a store | 5 |
| finish (themes, shapes, layers, dressing) revised in a store | 13 |
| dry passes besides | 6 `drive.py --dry`, 2 `loop.py` |
| stores refused | **0** at the store |
| refusals elsewhere | 1 dry source `400`, `PT4` ×4 (a pattern on a wall and a fill with no `rise`); 1 export `400`, `RQ1` (the biome) |
| declines met on the way | `HP3` (mill over 192 blocks), `DR-CLAIM` (trees in each other's crowns, the mill on the river's claim), `DR-ROOT` (oaks on rock) |

**The three numbers on the final store:**

```
ground   21188 walked, 346 scrambled, 50 barrier — 1.8% steps further than a player walks
props    32 placed, 2 declined
routes   worst step 0, on route spawn-0 to destroyable-0
```

**The two "declined" are `DR-PASS` on the mill and the cottage, and both buildings are in the world.** The
claims read lists them as declines; `sketch/columns` and the export call them complaints, and `column` at
`(34, −28)` and `(53, −37)` reads their floors and roofs.

**The deployed studio never made me wait.** No `429` reached the driver in fourteen stores; a store with its
report and export took about 35–60 seconds.

## What I could not say

**A waterwheel with spokes.** I wanted a rim, spokes and a hub. A layer holds one span a column, so a wheel
standing in the x–y plane is a solid disc on one layer; `tools/sculpt/solid.py` would compile a ring into
two layers. *Out of reach from where I was standing* — the solid compiler exists; I chose a slatted disc
(a `checker` of two planks) over a second system for one prop.

**A river whose water is continuous across the board.** Water over void cannot stand, and water over a bed
joins the two teams by land, which the author's ruling forbids. *Not a missing capability*: it is the ruling,
and the board follows it. The open question is below.

**A wheel turning, or water flowing.** Nothing in a PGM world turns, and an exported fluid is still water.
*Missing from the system* only in the sense that Minecraft has no such block.

## What I got wrong

**I stated the biome as a name.** `"biome": "Mesa"` stored at 200 and the export refused it `RQ1`. The
schema says `BiomeField` is a discriminated object; I had read the prose, which talks about biomes by name.
The store taking a field the export cannot read is worth the studio's attention.

**I assumed an added shape with a theme and no height would paint the ground under it.** It is one block at
y0 and owned no surface: 0.7% and 2.4% for two of three themes. The warm-up skill says exactly this, and
`themes` in the report is what caught it.

**I assumed an override add would let the relief take its top down as well as up.** Its top is never below
its own floor plus one, so a roof drawn past the point where the hill stood above it left a lid over the
strand. `column` at `(−20, −16)` showed it.

**I spaced the oaks at twelve blocks.** `oak-3`'s crown needs about seventeen, and `DR-CLAIM` declined half the
wood until the spacing was read off the declines.

## What worked first time

**The plan.** Five hand-drawn pieces and one zone evaluated `valid` and inspected inside `GO1` on the second
dry pass, once the build zone was drawn whole across the axis rather than as a half the symmetry fans (`G2`).

**The adit under the compiled ground.** An override add with a `floor`, over a `below` layer stating the
floor, gave three courses of air under relief-solved ground on the first build, and `walk` with a `y`
walked it end to end.

**The fluid pool past the coast.** Water meets the void at the coast exactly as `techniques/water` says, with
a bay drawn into the ring for the mill.

**The band cuts from `incline`.** The ground read 28% under 10° and 13% at 30–39°, so grass to 30° and earth to
42° left grass on the walked slope and rock on the crag and the spur.

## Instruments, counted

One relief, six `area` marks, two pushes, one made-ground shape (the cutting), no polyline, two made layers,
two copied tree styles. **No authored flight and no polyline is the board's weak side**: the valley side is
one ramped field, and its joins are marks rather than walls or stairs.

## Open gameplay questions

1. **Should a river between the teams be swimmable?** I followed the ruling and left the river's middle void
   under a build zone. A river with a bed is the other reading of the brief, and it would make the river a
   land connection a team does not pay to cross.
2. **Is an adit that ends under the defenders' shelf too strong an approach?** It is a covered walk from the
   strand to eleven blocks from the anchor, and the chamber's roof is about six blocks. I kept it on the
   defenders' own side so the attacker still has to cross the river first, and made no wall in it.
3. **Is the coverage acceptable?** The final board reads 37.3% dead, the back of the ridge and the far flank
   of the spur being on no journey. One spawn and one goal a side make two journeys; I took no ground off to
   chase the number.
