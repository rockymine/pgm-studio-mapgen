# Lindenkreuz — a city block, a car park, and the S-Bahn out of the ground

> A destroy board asked for by the repository's author: angular the way minuyo's boards are, with a car
> park on it, cars five by three with coal-block wheels and a sponge body and ice windows and a
> stone-slab roof, a Litfaßsäule scaled to them, a piano of nether brick, an S-Bahn tunnel underground
> whose line comes up to the surface and goes on over a bridge, and houses in the style of *Fox Dream*.

**In one sentence:** two rectangular city blocks either side of a twenty-block gorge, joined by one
railway bridge — a car park with the monument standing in a marked bay, a Litfaßsäule and a street piano
on the station forecourt, terrace houses on two raised garden blocks, and the S-Bahn running out of a
cut-and-cover tunnel under the whole quarter, up a ramp in an open cutting and away over the bridge.

90 × 200 blocks of authored ground, `rot_180` about the origin, cell 5, base surface 20, build ceiling
55. The world reads `x −47..46, y 0..65, z −100..99` — the two extra columns each side are tree crowns
and the y65 is the observer pad over the origin; the board itself is y0..y35. Two landmasses, one
crossing. `<gamemode>dtm</gamemode>`, one `<destroyable>` a team, obsidian,
`pillar-3`, named **Parking Meter**.

## Where the brief's eight things are

| The brief said | Where it is | Measured |
|---|---|---|
| destroy the monument | one obsidian pillar a team, in a bay of the car park | `<cuboid id="parking-meter-region" min="-15,22,-51" max="-14,25,-50"/>`, and its `rot_180` image at `(14..15, 50..51)` |
| angular | **no relief at all** — every height is stated, so every face is sheer and every floor flat | four surfaces on the whole board: y8 trackbed, y10 platform, y19 city, y23 terrace |
| a car park | 50 × 30 of tarmac between two raised garden blocks, marked into 36 bays | `x −25..25, z −65..−35`; white markings are **22%** of its surface |
| cars 5 × 3, four courses | 15 a side, 30 on the board, at `y20..y23` | wheels coal `y20`, body sponge `y21`, ice-and-sponge `y22`, stone-slab roof `y23` |
| a Litfaßsäule to their scale | on the plaza at `(−22, −74)`, nine courses over a 3 × 3 plinth | 9 tall against the car's 4 — a real column is about 2.3 × a car |
| a piano of nether brick | an upright on a quartz stage at `(27, −73)` | case `y21..y25`, quartz keyboard cantilevered at `y23` |
| an S-Bahn tunnel that reaches the surface and crosses a bridge | tunnel `z −80..−35`, ramp `z −35..−11`, bridge `z −12..12` | the void scan reads **7 956 cells of open roofed space, x −10..18, y 9..16, z −80..−36, 0 of it sealed** |
| houses like *Fox Dream* | `@lk-terrace`, two storeys, brown clay over brick, jungle roof | six a side plus two kiosks |

## The one crossing, and what it is for

The two halves' ground stops at `z = ∓10` and there is twenty blocks of nothing between them (`CT12`
wants 15–40). One thing crosses it: the railway bridge, `x −10..10`, a deck of three courses at
`y17..y19` with a coping parapet on each edge — level with the city, so it is a bridge in section and a
lane in plan. Everything else is a bridge somebody builds: the plan's single build zone spans the
board's whole width (`x −45..45, z −15..15`), and `<apply block-place="no-void" …>` denies the void
outside it.

**The viaduct is a corridor, and that is the board's one real gameplay question.** The author's brief
rules that the two sides are joined by a build zone over void and never by a land connection, on the
grounds that a corridor is a place a defender stands. This board breaks that rule on purpose, because a
railway that stops at a chasm is not a railway. What it buys instead is a *choice*: the deck is 19 blocks
wide against the frontline's 90, it is not on the line to either monument, and it is the only place on
the board where both teams are in the open at the same height. A team that wants cover bridges at ground
level under fire; a team that wants to arrive now takes the bridge and is seen doing it.

That is an open question rather than a claim. It wants a match to settle.

## The vertical model

Everything on the board is one of four stated heights, and the whole thing is written against them:

```
y23   the two garden terraces          (plan pieces at surface 24)
y19   the city — forecourt, car park, cutting shoulders, the tunnel lid, the bridge deck
y17   the lid's soffit                 (a layer of its own at base_y 17, three courses)
y10   the station platform
y8    the trackbed, eleven courses down
```

The board carries **no `relief` key at all**. That is the single decision the rest of it follows from.
It is what makes the board angular — a relief is a solver, and a solver rounds — and it is also what
makes a 5 × 3 car able to state an absolute floor and land on the tarmac rather than in it. Every
authored shape's `base_height` *is* the height it builds to, and there is nothing downstream that moves
it.

The price is `EL1`: the plan tier walks its pieces flat, so the six seams where a garden terrace meets
the ground at 20 read as four-block steps a player cannot climb, and the evaluator says so six times. The
layout answers all six with an authored flight — `ramp-cp-w/e` out of the car park's aisle, `ramp-fc-w/e`
off the forecourt, `ramp-ct-w/e` down onto the cutting's shoulder — each a tilted quad, four courses over
eight or nine blocks, which is better than the 2:1 that makes a quad a stair rather than a wall. The
transect through `hs-w1` walks its terrace end to end. **The complaint is correct at the tier it reads
and wrong about the world**, and there is no way to tell it so.

## How the tunnel is made

It is cut-and-cover, and the two halves of that are two different mechanisms.

**The trench is an override add.** `x −10..10, z −80..−35`, `base_height 9`, `override: true`,
`height_mode: "level"`, `skirt: 0`. A plain add merges through `MergeCell`, where the *taller* column
wins, so an ordinary shape can never cut into ground another shape has already claimed — the city
polygon at 20 would simply keep the column. An override add does `result[k] = v`: the column becomes its
own, floor and all. That is the only instrument on the board that makes a hole in ground.

**The lid cannot be one.** Among override adds on a single layer the taller still wins, so a lid at
`y17..y19` drawn beside the trench would delete the trench under it. The lid is therefore a layer of its
own — `base_y 17`, `floor 0`, `base_height 3` — whose top block is `y19`, flush with the city, and whose
soffit at `y17` leaves eight blocks of clearance over the trackbed and six over the platform.

**The station box widens the trench east** to `x 18` for `z −80..−62`, and the platform is an override
add fifteen wide at `base_height 11` — taller than the trench, so among the override adds it takes its
own cells. Its edge at `x = 4` carries a yellow line.

**The way down is a switchback, because the forecourt is fifteen blocks deep and the descent is
eighteen.** Nine courses from `y19` to `y10`, one rectangle a course and two blocks of run each, so every
step is a single block a player walks; a ramp polygon over that run would rasterize as treads of two and
charge a placed block to climb. The upper flight comes down a light well cut through the lid
(`x 16..18, z −78..−68`) and the lower one runs back north under it. The break between them is not
arbitrary: the soffit is `y17`, so a step whose top block is 14 or higher has less than three blocks of
headroom, and everything at or above 14 is in the open.

## Two things a stacked board makes the author say twice

**A marking on the ground layer does not appear on the lid.** Paint scope is keyed by `(layer, x, z)` —
a cell covered on two layers is not contested, because each layer shows its own surface — so the bay
markings that fall on the twenty-one blocks of car park standing on the tunnel roof have to be drawn on
the lid as well. `mark()` does both, and **cuts the ground copy out of the lid's footprint** rather than
leaving it under there. That second half was learnt from a column read: a theme owns a whole column, and
a one-course white line that wins a roofed cell paints the tunnel floor and the tunnel wall beneath it
white, thirteen courses down, where nobody drew a line at all.

**An accent is a surface, not a column.** The same fact from the other end. `line`, `warnline`, `coping`,
`stage` and `steel` were first written with one block in all five buckets, which is right for a made
thing — a car is sponge all the way through — and wrong for paint: at `x = 19, z −64..−60` the world
read fifteen courses of white stained clay from `y5` to `y19`. They now state the marking in `surface`
alone and stone in `wall` and `fill`.

## What the world says about the two mistakes that cost a build each

Both were `SK` complaints on a 200, and both would have shipped silently on a driver that read status
codes.

| | What was drawn | What the world did | What it is now |
|---|---|---|---|
| `SK10` | the light well's rail as an override add on the **ground** layer at `floor: 20` | over the trench, the override rule reads the *plain* add under it — the city polygon, top 20 — and keeps "the ground under its floor", so it re-filled the tunnel it stands over: **36 columns**, 4 blocks deep | the rail is on the lid, and it is the deck **plus a course** rather than a course on top of it |
| `SK9` | that rail as a lid shape at `floor: 3` | a layer holds **one span per column**, so the deck under the rail was declined out of the world | one shape, `floor 0`, `base_height 4` — the taller shape simply keeps the column |

## What the ground is painted with

Nine themes over 16 640 ground cells, and only three of them are places:

| Theme | Share | Is |
|---|---|---|
| `city` | 52.2% | the pavement — light gray clay with stone in a 17-scale noise, andesite riser, chiselled coping at the void |
| `garden` | 18.6% | the two raised blocks — grass over dirt over coarse dirt, brick kerb, and a **`layered` wall** of three courses of brick over two of stone brick over andesite, so the retaining face is a coping over rock rather than twenty-four courses of brick |
| `tarmac` | 12.6% | the car park — gray clay with light gray in a 19-scale noise |
| `ballast` · `concrete` | 4.8% · 2.0% | the trackbed, and the station, platform and bridge |
| `line` · `coping` · `stage` · `steel` · `warnline` | 3.9% · 2.9% · 1.1% · 2.0% · — | markings, kerbs, the platform's safety line, the piano's stage, the rails |

**The rim is off everywhere except the lawn.** `rimEdges: "boundary"` caps every shape's outline, and a
board drawn out of a hundred rectangles then wears a chiselled line round each of them — measured at
**16% of the plaza** before the change and **5%** after it. Every ground now states `rimEdges: "void"`,
which caps only the edges that stand over nothing: the gorge and the board's own edge. The kerbs the
board wants elsewhere are shapes, where they can be put exactly. `garden` keeps `boundary`, because a
brick kerb round a lawn is exactly what its outline should wear.

The five accents are not a sixth, seventh and eighth ground. They are paint on the three grounds, and
the census separates them because a theme is the only thing a shape can say about what it is.

## The car, and why it is four layers

The model is 42 blocks and compiles to exactly four sketch layers, one per course, because
`tools/sculpt/layers.py` decomposes a voxel model **by run index**: a column's solid blocks split into
maximal runs of one material, and the *n*-th run of every column goes on layer *n*. A car's worst column
passes through a wheel, the body, a window and the roof — four runs, four layers. That the answer is
four rather than three or five is the model's, not the compiler's.

```
y3   roof     stone slab (44:0)      x −1..1, z 0..2
y2   windows  ice (79:0) round the cabin, hollow in the middle; sponge over the bonnet
y1   body     sponge (19:0)          the whole 3 × 5 footprint
y0   wheels   coal block (173:0)     four, at (±1, ±1)
```

The bonnet is two blocks long and the cabin sits at the back, which is the only thing that says which way
a car is parked; half of them are turned a half-turn so a row is not fifteen of the same object. All
fifteen are compiled together as one made thing — `part_of: "cars"` — so the board carries four layers
for thirty cars rather than sixty.

**The ice does not melt.** Ice melts at a *block* light level over 11, and the nine car-park lamps carry
glowstone at `y25`. Every lamp is at least four blocks and three courses from the nearest windscreen —
the two aisles at `z −56` and `z −45`, against rows at `z −64..−59`, `−53..−48` and `−42..−37` — which
is a path length of seven and a light level of eight.

## Where things stand

| Thing | At | Notes |
|---|---|---|
| red spawn | `(0, 20, −90)` | an 18 × 18 station concourse on a 20 × 20 piece; blue at `(0, 20, 90)` |
| monument | `(−15, −51)` | bay 3 of row 2; blue's at `(15, 51)` |
| Litfaßsäule | `(−22, −74)` | `y20..y28` |
| piano | `(27, −73)` | on a quartz stage `x 22..32, z −78..−70`, one course up |
| light well | `x 16..18, z −78..−68` | the stair down to the platform |
| platform | `x 4..18, z −80..−62`, top `y10` | yellow line at `x = 4` |
| trackbed | `x −10..3`, top `y8` | four rails at `x −9, −6, −2, 1` |
| bridge | `x −10..10, z −12..12`, deck `y17..y19` | parapets at `x = ±10` |
| houses | `hs-w1/w2` `x −37..−28`, `hs-e1/e2` `x 28..37`, `hs-n1/n2` behind the station | plus `ks-w/e` on the plaza |

## The bands

| Rule | Wants | Reads |
|---|---|---|
| `GO1` goal-to-spawn ratio | 3.0–4.0 | **3.51** (own 41, enemy 144) |
| `GO3` opposing goals apart | 85–150 | 102 |
| `GO4` goal from own spawn | 40–90 | 41 |
| `CT12` the strait | 15–40 | 20 |
| `G8` fill ratio at `maxPlayers` 24 | — | score **0**, `valid: true` |
| export gate | — | **OPEN** |

## The rails follow the ramp column by column, and a text read is why

The four rails climb the cutting with the ballast, and getting them to do that took reading
`03-slopes.txt` rather than looking at anything. Drawn in three-block segments at a rounded height they
stood a course proud of the ballast wherever the ramp stepped inside a segment, and a rail one course
proud beside ground one course lower is a **two-block rise**:

| read | said |
|---|---|
| `03-slopes.txt`, `z −27` | `##:..:...:..:........##` — four `:` at `x −9, −6, −2, 1`, and again at `z −21..−20` |
| `02-heightmap.txt`, `z −35` | `c010010001001000000000c` — a different digit under each rail |
| `transect x −9` (the rail) | `rises 8, 2 scramble — +2 at (−9, −26); +2 at (−9, −20)` |
| `transect x −8` (the ballast) | `rises 11, 0 scramble` |

They are now one rectangle per z column at the ramp's own height, **floored rather than rounded** —
`int(TRACK + t·(CITY − TRACK)) − 1`, which matches all 25 stations of that transect. Rebuilt, the
trackbed reads `000000000000000000000` straight across at every z, the rail line transects **11 rises and
0 scramble**, and the board's scramble count falls from **152 cells to 120**. No render on the board
shows any of this: a one-block bump under a rail is one shade in a heightmap and nothing at all in an
isometric.

## What is still wrong with it

**15.9% of the ground is dead**, and the four largest patches say the same thing four times: 238 cells
each at `(±37, ∓18)` and `(±36, ±16)` — the outer corners of the cutting, at the frontline's two flanks.
Every route the coverage read computes crosses at the bridge, so the ninety-block frontline is used over
the twenty blocks in the middle of it. The board's own answer is that the build zone spans the whole
width and a team may cross anywhere; coverage cannot see a bridge nobody has built yet. That is a
measurement, not a verdict — but it is the number a second pass should move.

**`EL1` × 6**, above: correct at the plan tier, answered in the layout, and not silenceable.

**The car park's markings are 22% of its surface.** A block is a block, and a bay divider cannot be
thinner than one; a real bay is 2.5 m wide with a 10 cm line. It reads as a car park from above, which is
what it is for, and it reads as a lot of white from the ground.

**The terraces are 43% house roof and 27% lawn.** Two 10 × 9 houses on a 20 × 30 block is a dense
terrace. That is what a city block is, and it is also why the "garden" in `garden` is mostly a border.

## What to look at

- `specs/opus5-lindenkreuz/renders/world-iso.png` — the board in the round; the cutting and the bridge
  are the whole composition
- `world-xray.png` — the only view the tunnel is in
- `world-ground.png` — the material top-down; the bay markings are what makes the car park read
- `world-section-x0.txt` — the tunnel, the ramp and the bridge in one cut down `x = 0`
- `03-slopes.txt` — where the ground steps, and the only read that found the rail bumps
- `06-claims.txt` — the goal's clearance as a literal 21 × 21 block of `9` with nothing inside it, and
  `placed 60, declined 0`
- `world-section-z0.txt` — the gorge and the bridge in one cut. Its ruler is **z**, not x: `axis=z`
  names the direction the cut runs, so `at` is the other coordinate
- `transect-cars.txt`, `transect-column.txt`, `transect-piano.txt` — what stands where, in numbers
