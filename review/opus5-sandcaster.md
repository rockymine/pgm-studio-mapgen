# Sandcaster — three countries, a chasm, and a corridor nobody built

**What it is, in one sentence.** A long lane split down the middle by a chasm: a rocky reef on one side of it
and a dune field on the other, joined at the front across a wind-scoured pass and at the back through a
wood — and under the reef, reached by two cuttings and lit by two holes in the ground, a tiled service
corridor with a drained pool in it that has no business being there.

Destroy the monument, two teams, `rot_180`, 24 players. **110 × 400 blocks — 100 × 200 a side.** Two
`<destroyable>`s a team: **The Beacon**, obsidian, on a dune in the open; **The Cistern**, end stone, in a
sealed chamber twenty blocks underground.

## The board

```
      | 1         0          |
  -40 |         SSSS         |   S  spawn — 20 × 10, the only role piece
  -38 |     EEEEEEEEEEEE     |   E  apron
  -36 | DDDDDDDDDDDDDDDDDDDD |   D  holt   — forest, surface 24
  -28 | CCCCCCCooooooBBBBBBB |   C  reef   — rock, 22   B  wash — sand, 20   o  the chasm
   -6 | AAAAAAAAAAAAAAAAAAAA |   A  pass   — the seam, 18
    0 | AAAAAAAAAAAAAAAAAAAA |      the axis: one continuous landmass, no strait
```

Six pieces a team at four surfaces, and everything else is the finish. `renders/00-board.txt` is the grid.

**The chasm is left rather than cut.** No piece covers `x −15..15` between `z 30` and `z 140`, and
`PlanVoids.Declare` names it on every compile whether or not anybody drew one. That makes each team's ground
a horseshoe: the reef and the wash meet only across the pass at the front and through the holt at the back,
so a raid commits to a side for 110 blocks.

**The tunnel is the third route**, and it is the only one that crosses under the reef rather than round it.

## The three countries, and the one hue axis

`AUTHORING-BRIEF.md`'s rule is three families named out loud. This board names three *poles* instead and puts
everything on one axis between them, which is what keeps twenty themes from reading as twenty decisions.

| | Family | Made of |
|---|---|---|
| **the reef** — the cool pole | pale stone + ash + grey stone | diorite, polished diorite, mushroom stem, clay, double stone slab, gravel |
| **the wash** — the warm pole | sand + rust | sand, sandstone, end stone, white clay · red sandstone, orange clay, hardened clay |
| **the holt** — what ties them | verdant + loam + dirt | grass over coarse dirt; podzol under the trees |
| **the pass** — where they meet | grey stone with a thread of each | andesite, diorite, stone, gravel, **granite** |
| **the workings** — the same value, gone cold | ash + bright, one accent | clay, double stone slab, quartz, polished andesite · **prismarine**, once |

**Nothing on this board is saturated except two blocks**: the prismarine lanes in the drained pool, and the
obsidian of a goal. The first draft used hardened clay as one of five stops in the pass's cell palette; at a
fifth of the cells a thread stops being a thread and becomes the ground, and the pass came out blotched
red-brown. Granite is the same warmth two steps down.

## The brush, which is most of what the surface is

The regions are painted by **forty-two authored strokes**, not by one pattern each. A stroke is a small
lobed ring carrying a theme, and every one of them answers a *why here*:

| Stroke | Where, and why |
|---|---|
| `br-scree-*` | at the foot of each tower — what fell off it |
| `br-cleft-*` | in each cleft the relief already cut, mossy where water sat |
| `br-pave-*` | four bare patches of pavement between the towers |
| `br-crest-*` | on each dune the relief already raised, scoured to the pale grains |
| `br-hollow-*` | in each swale it already sank, where the red sand collects |
| `br-pan-*` | three gravel patches the dunes have not covered |
| `br-drift-*` | where the wash spills over the chasm's lip — the one place two palettes touch on open ground |
| `br-under-*` | podzol under each copse |
| `br-track-*` | the worn ground between the spawn and the two roads |
| `br-pass-w/e-*` | the reef's stone reaching across the pass from one side and the wash's from the other |

**A stroke is an ordinary add one course thick, and that is not a detail.** The first eleven of them were
override-adds, which is the form that works on flat ground and punches holes in solved ground:
`RasterShape` gives a shape with no `base_height` one course at bedrock, an override-add overwrites the
column outright, and what normally repairs it is the relief writing its solved field back over the cell —
which does not happen on ground a `relief_scope: "exclude"` shape owns. The lid over the workings is
exactly that. Measured at `z 51`: `x −50:0 −47:0 −44:0` against a reef surface of y21 four blocks away.
Re-authored as ordinary adds the same transect reads `−50:21 −47:21 −44:21`, because the taller add wins the
column and a one-course stroke can never lower what it paints. `GENERATION-NOTES.md` carries the correction.

## The relief

One island carrying four regions at four heights, so **each region is held by an `area` mark at its own
height** before anything else is said, and the landforms are written over them. Marks resolve in order and
the last wins:

1. `coast` — the rim, first, so nothing later cuts a doorway through the shore
2. `hold-pass` · `hold-wash` · `hold-reef` · `hold-holt` — the four regions, at 18 / 20 / 22 / 24
3. four `cleft`s cut into the reef's east strip, three knolls beside them
4. five dune summits and two swales on the wash, then the dry `pan` written over them
5. three brows and a dell on the holt
6. two knolls on the pass, then `saddle` — the road across the front, written last

Beside them, **five pushes** — three on the wash, two on the holt — for ground that rolls rather than
stepping between discs. `POST …/sketch/relief/read` answers **cells 13 851 · low 14 · high 37 · relief 23 ·
symmetry error 0**.

**No push touches the reef, and that is a rule rather than a preference.** A push is added to the
*already-solved* surface, so it crosses every constraint under it — including a `relief_scope: "exclude"`
shape, which it cannot move. A push over the lid would leave the lid standing as a step in ground the push
lifted around it. (Whinnymoor's review records the same rule costing it four haul roads.)

The towers are the other half: six **erected** shapes with `height_mode: "raise"`, a skirt of 3 and
per-vertex anchors, so each reads its datum from the ground under it — including the lid, whose top *is* that
ground — and stands out of it as a jagged pinnacle rather than a cone. Highest ground on the board is **y37**,
which is why `<maxbuildheight>` reads **59**.

## The workings

A second sketch layer, `under`, inserted **below** the compiled ground, because the painter walks the stack in
document order and each pass paints its whole column: a storey listed after one that stands over it finds no
stone left. `drive.py`'s `addLayers` takes `"below": true` for exactly this.

| | Blocks | Stood on at |
|---|---|---|
| the corridor floor, the bays, the cistern chamber | 0..6 | y7 |
| the drained basin | 0..3 | y4 |
| the walls | 0..14 | — |
| the lid over all of it (the ground layer, `relief_scope: "exclude"`) | 15..21 | **y22 — the reef's own surface** |

Eight courses of headroom, and the reef above it is ordinary ground with towers standing on it. Read at
`(−38, 80)`: `y0..6` corridor floor · **`y7..14` air** · `y15..21` lid · `y22..25` a tower. Read at
`(−38, 126)`, in the cistern chamber: the same, with black stained clay where the corridor's clay was.

**Two cuttings and two light wells** are the only ways in and the only daylight. Each cutting is a `subtract`
in the ground layer exactly as wide as the ramp under it — the first pair were two blocks wider, and the
strips of pure void that left beside the way down were both an ugly black gash and 7 244 places of standable
wall-top that nothing could reach (`SK11`). Each ramp runs **over twice its rise**: 15 courses over 30 at
the south end, 17 over 35 at the north. A slope of one course a cell builds as treads of two, and a
two-block rise is a placed block to climb.

The uncanny is in the repetition rather than in the colour. **Four identical bays**, five blocks square with
the same bench in each, at even eighteen-block spacing off the west wall. A **drained pool** with two
dark-prismarine lanes marked on its floor — drawn as *shapes* of the basin's own two courses, because a
stroke prop ignores `layer` and would have landed on the reef sixteen blocks above it. And a chamber with one
door in it, holding a goal.

## How it plays

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **1.37**, `valid: true` |
| `POST /plan/inspect` | goal ratios **3.47** and **3.67** — `GO1` wants 3.0–4.0 |
| `GET …/preflight` | round-trip clean · mirror clean · buildability clean · **export gate OPEN** |
| `GET …/render/traversability` | **one component**, all four goal markers connected |
| `GET …/coverage` | 29 982 reached · 351 decorated · **689 dead** of 31 022 = **2.2%** |
| provenance census | tree 44 · boulder 20 · flora 6 · stroke 4 · destroyable 4 · spawn 2 · ironcube 2 — **nothing declined** |
| extent | 110 × 400, cell 5, surfaces 18 / 20 / 22 / 24, `<maxbuildheight>` 59 |

The two goals ask opposite things. **The Beacon** stands on a dune in the open with sightlines the length of
the wash — easy to find, hard to hold. **The Cistern** is twenty blocks down a corridor with two entrances,
both of them cuttings a defender can watch — hard to find the first time, and a killing ground once found.

## Where it departs from the numbers

**`G8` — fill ratio 0.775 against a band of 0.201–0.542.** The band is measured off the authored seed
corpus, whose boards are a third of this one's area, and it is the one term this board deliberately fails.
The alternative was arms twenty blocks wide, which is the thin-lane board this map was asked not to be: at
35 blocks an arm holds a dune field, a tower, a cleft and a road across it; at 20 it holds a corridor. The
soft-term cost is 1.37 of score and nothing else — `valid` stays true and every hard term passes.

**`SK11` on the corridor floor, and a real plug behind part of it.** Most of the complaints are tower
tops, which is what the top of a pinnacle is. The two on the corridor were read as a quirk of the check and
were not: each end wall was drawn as one rectangle **across** the ramp under it, and among the shapes of one
layer the taller override-add wins the column rather than the later one, so the wall did not lose to the
ramp — it plugged it. The end walls are now drawn in halves, clear of the ramp between them, and the south
ramp reads continuous block by block: `21` at `z 36` falling one course every two blocks to `6` at `z 66`,
with the lid over it from `z 62`.

`SK11` still names the workings on this board after the fix, where the same fix cleared it on Sandcaster II.
Both boards answer **one component** on `render/traversability` with all four markers connected, and both
ramps read continuous. What the remaining complaint points at is not something a column read confirms, and
it is recorded as a reading.

**`SK10`, sixteen columns** where the north ramp's high end drives into the holt above it. Two layers
occupying the same solid rock is not a hole; it is one course of double-counting at the mouth of a cutting.

## Coordinates

| Thing | At | Reads |
|---|---|---|
| The Beacon | `(40, 20, 120)` red · `(−40, …, −120)` blue | obsidian `pillar-3`, floating 4 over a dune |
| The Cistern | `(−40, 22, 120)` red | end stone `cube-3`, on layer `under`, floor y7 |
| the corridor | `x −43..−33, z 66..140` | floor y0..6, air y7..14, lid y15..21 |
| the drained pool | `x −41..−35, z 95..109` | basin y0..3, two prismarine lanes |
| the cistern chamber | `x −43..−33, z 118..134` | one door, in its south face |
| the four bays | `x −45..−43`, `z 76 · 94 · 112 · 130` | identical, 5 × 5, one bench each |
| the light wells | `x −40..−36, z 86..90` and `z 116..120` | a 15-block drop, one way |
| the south cutting | `x −42..−34, z 36..62` | y22 → y7 |
| the north cutting | `x −42..−34, z 144..175` | y7 → y24 |

## What was looked at

Beyond the driver's own set: `renders/iso-0.png`, `iso-1.png`, `iso-2.png` — **the studio's own WebGL
isometric preview**, driven in a browser. It is the Sketch tool's 3-D canvas
(`js/studio/render/iso-webgl.js`) and no endpoint exposes it; on a board with a storey under it, it is the
only view that shows the towers, the cuttings and the chasm as solids rather than as colours. It answers
nothing a column read does not, and it is the fastest way to see that a board is a landscape.

## Open gameplay questions

Decided without an oracle and recorded as questions.

**Is a goal in a sealed underground room a fair objective?** The Cistern has one door and two ways to the
corridor, both watchable. That reads as strongly defensible; whether it is *too* strongly is the author's.

**Should the chasm be bridgeable?** It is not — the buildable region is the seam at `z ±10`, so the chasm is
a wall for the whole match and the horseshoe is real. Opening it would make the board a square with a hole
in it rather than a lane with two sides.

**Should a light well be a one-way drop?** Falling fifteen blocks into the corridor costs health and skips
both cuttings. It is a shortcut with a price rather than a route, which is the intent; a player who does not
know the ramps exist will read it as the way in.
