# Tiefkreuz — a destroy board played on four storeys

> A multi-level transit interchange whose whole middle is the station: a deep platform level in
> cut-and-cover, a concourse mezzanine over it, the street over that, and an elevated viaduct over the
> street. The objectives stand thirty-four blocks apart in the vertical.

**In one sentence:** two halves of a city are cut apart by a thirty-two-block chasm, and in each half a
terminus station is buried under the street — tracks and platforms at y8, a concourse slab at y18, the
street at y29 and a brick viaduct at y41 — with one monument on the deepest floor and one on the highest,
so a raid on either team has to be climbed or descended before it can be fought.

80 × 224 blocks, `rot_180` about the origin, base surface 30, build ceiling 64, ground y0..y43.
`maps/opus5-tiefkreuz` · `specs/opus5-tiefkreuz` · `reports/opus5-tiefkreuz-run.md`.

## The stack, in world Y

| Storey | Ground top | A player walks at | Drawn by |
|---|---|---|---|
| running tracks (ballast) | y5 | y6 | ground layer, override adds |
| rails, one course proud | y6 | y7 | ground layer |
| platforms — an island between two side platforms | y8 | y9 | ground layer |
| platform canopies | y14 | — | `perron`, a **made** layer on posts from y9 |
| concourse mezzanine | y18 | y19 | `halle`, base_y 17 |
| street — and the box's lid where it crosses it | y29 | y30 | the compiled ground layer, and `deckel` at base_y 27 |
| viaduct deck (parapets y43) | y41 | y42 | `viadukt`, base_y 39 |

Ten layers in all: the compiled `ground` carrying 67 authored shapes, three ground layers over it
(`halle` 41 shapes, `deckel` 7, `viadukt` 8), and six **made** layers — four slices of a standing train
and two of the platform canopies on their posts.

**The board carries no relief at all.** Every height on it is stated: a shape's `floor` and
`base_height`, or a tread's own course. That is what makes a four-storey stack arithmetic rather than a
negotiation with a solver — a relief moves the ground under a slab and a slab does not move with it, and
on a board where a soffit has to clear a platform by exactly eight blocks that is not a trade worth
making. The cost is that every landform on the board is a rectangle, which is right for a city and would
be wrong for anywhere else.

## What the four storeys are for

**The deep level is a terminus.** Two tracks run from the tunnel mouths at `z = ±16` — the chasm face —
north to buffer stops at `z = ±52`, with a west platform, an island and an east platform between them.
At the head of the tracks the three platforms join across a terminus deck (`z ±54..±57`), and the deep
monument stands on it, at `(−16, 11, 56)` and `(15, 11, −57)`.

**The concourse is a slab over the whole box** from `z ±38` to `z ±57`, eight blocks of headroom over the
platforms and eight under the street. It is cut by four openings: the street flight, a light well over
each side platform and one over the island. The well over the west platform runs the whole way up —
street to platform, twenty-one blocks — so the deep monument is visible from the pavement and can be
dropped onto for nine hearts.

**The street is the lid over the station** for `z ±16..±24` and `z ±38..±58`, and is missing between
them: the open bay, 41 × 14, where the trainshed is open to the sky and daylight reaches the platforms.
A player walking the middle of the board meets a hole with a one-course parapet round it and goes round
by either flank, which is what puts traffic on the flanks at all.

**The viaduct crosses the city** at `z ±61..±75`, 88 blocks of deck on eight brick piers, twelve blocks
of headroom over the street. One ramp climbs it — twelve treads of two blocks, at the end furthest from
the goal — and the high monument stands on the deck's south lip at `(22, 45, 62)` and `(−23, 45, −63)`.

## Where the two teams meet

The chasm is `z −16..+16`, 32 blocks, full-depth: void from the sky to y0. It is `CT12`'s strait
measured at **32** and the plan's one build zone (`x −28..28`) covers it exactly, so a stepping stone no
wider than the window that reaches it is not possible here — the window *is* the ground. The export
writes `<apply block-place="…" region="not-build-area" message="You may not edit the void!"/>`, so a
crossing may be built only inside that window.

Three heights face each other across it, and none of them is bridged for you:

| Crossing | Height | Gap | What it arrives at |
|---|---|---|---|
| the tunnel mouths | y9 | 32 | straight onto the enemy platform, at the far end from their monument |
| the quays | y30 | 32 | the enemy street, in the open |
| — | up to y64 | 32 | legal anywhere inside the window, up to the build ceiling |

The viaduct does **not** reach the chasm: each team's is a stub over its own half, so the high monument
cannot be crossed to directly.

## What the walks cost

Measured on the built world with the storey named — `GET …/walk?from=0,106,30&to=x,z,y`. Naming the `y`
matters: without it the walk targets a column, and on a stacked board a route to a goal on the viaduct
ends on the street twelve blocks beneath it.

| From the red spawn point (0, 106, 30) | `aim=reach` | `aim=travel` |
|---|---|---|
| own deep monument `(−16, 56, 9)` | 60 blocks, 3 placed, one 21-block drop | the same |
| own high monument `(22, 62, 42)` | **149 blocks, 0 placed** — by the ramp | 53 blocks, **13 placed** — pillared up |
| enemy deep monument `(15, −57, 9)` | **181 blocks, 28 placed** | 169, 78 placed |
| enemy high monument `(−23, −63, 42)` | **370 blocks, 25 placed** | 178, 44 placed |

The stair chain walks both ways for nothing: street → concourse is 45 blocks and 0 placed, concourse →
platform 25 blocks and 0 placed. The 21-block drop down the light well is the shortcut, and the walk
model prices a fall at nothing, which is why `reach` takes it; in game it costs nine hearts.

Plan tier, off `POST /plan/inspect`: `GO1` **3.07** and **3.42** (band 3–4), `GO4` **55** and **52**
(band 40–90), `GO2` **38** (band 35–65), `GO3` **127 / 123 / 142** (band 85–150), `CT12` **32** (band
15–40). The evaluator scores the plan **0** with no violations and no lint.

## What the ground is made of

Six themes over the ground and three more for the things that are made rather than grown. The families
are three: the city is grey stone, the station is white concrete, the railway is brick and iron — and no
building is walled in the ground's own family.

| Theme | Share | On | Says |
|---|---|---|---|
| `stadt` | 69.5% | the street, the lid, the chasm walls | a `noise` of stone brick and andesite at scale 18 — two blocks, broad patches — kerbed with a smooth-stone rim wherever the ground drops |
| `bahn` | 11.0% | platforms, concourse, canopies, box lining | a 6-block `checker` of quartz and smooth stone: a built floor, light against the city |
| `schotter` | 9.7% | the trackbed and the viaduct's deck | a `noise` of gravel and andesite at scale 9 |
| `ziegel` | 4.7% | the viaduct's piers, parapets and ramp | brick, with a `layered` wall band putting a stone-brick string course every seventh block up the pier faces |
| `gleis` | 4.9% | the rails, four on the deep tracks and four on the deck | iron, one column wide |
| `licht` | 0.1% | 18 pavers down the platforms, 10 panels in the concourse slab | glowstone, one course deep — the only lighting a stacked board can have, since nothing in the API places a fixture |

The train is `zug-rot` / `zug-glas` / `zug-grau` — three solid themes, one block each, because a made
thing wants its geometry read and not its shading. Theme borders: `gleis | schotter` 1360 cells (the
rails in their own ballast), `bahn | stadt` 524, `stadt | ziegel` 380. Nothing is mashed.

## The techniques, and what each one bought

**The clamp, five ways across.** The box is not a floor drawn inside a wall — a layer holds one span per
column and the taller add wins it, so a hall drawn that way builds as its roof alone. The five strips
across the box (platform, track, island, track, platform) are drawn side by side at their own heights,
and the street either side of them *is* the box wall.

**Two flights of treads, not two tilted quads.** A ramp is one polygon with a thickness per vertex, and
that is the shorter statement — but the column where a flight *meets a slab* has to land on that slab's
own top exactly, and an interpolated anchor at the last column does not promise it. Both flights are
per-course rectangles: eleven treads of two blocks from platform to concourse, eleven from concourse to
street, twelve from street to viaduct deck. Every one is a run of two for a rise of one, which is what
makes a flight walk both ways for nothing.

**A goal states its storey.** `DestroyablePlacement` carries `layer`, and it is carried through the
compile onto every orbit image: `{"piece": "", "at": [-16, 56], "layer": "ground"}` resolves against the
ground layer's surface at that column — the terminus deck at y8 — instead of against the lid twenty-one
blocks over it. `{"layer": "viadukt"}` does the same at y41. Neither needed a patch to the intent.

**A rectangle algebra for the slabs.** `carve(outer, holes)` in `build-spec.py` turns a slab and its
openings into the rectangles that remain, banded by z. The lid is seven rectangles round the open bay,
the stair well and two light wells; the concourse is seventeen.

**Made layers for the things that are not ground.** The train is four slices — underframe, body, window
band, roof — because a colour change inside a run splits a layer as surely as air does, and `kind:
"made"` keeps `SK10`'s pair walk and `SK11`'s reachability walk off it. The canopies are two more, on
posts. Six made layers, thirty blocks of statement, and no complaint from either gate.

**A stroke seats on the top surface, so the avenue is drawn in two runs.** The street from the head
house to the station passes *under* the viaduct; a single stroke through it paves the viaduct's deck
instead of the street. `bahnhofstrasse-nord` stops at the viaduct's north face and
`bahnhofstrasse-sued` starts at its south.

## What is wrong with it

**`03-slopes.txt`: 11 994 walked, 300 scrambled, 1 658 barrier, 10 faces, the largest 431 cells at
`x −21..20, z −59..−24`.** That face is the trainshed's own lip — the 21-block drop from the street into
the open bay — and every other face is either the chasm wall or the viaduct's edge. All of them are
drawn, none is a landform that came out wrong; but a board where a sixth of the cells step by three or
more is a board a player falls off, and that is the trade this one makes on purpose.

**The 300 scrambled cells are the trackway.** Ballast at y5, rails at y6, platform at y8: crossing a
track from a platform is a two-block climb out, which costs one placed block. That is deliberate — it is
what makes the concourse the free way between platforms — and it is also the single most likely thing to
annoy a player who does not read it as a railway.

**10.7% of the ground goes unused** (`GET …/coverage`: reached 11 521, decorated 936, dead 1 495). The
five patches are the corners beside each head house — 321 cells at `(−27, −105)`, 288 at `(26, 104)`,
177 at `(−26, 107)`, 177 at `(24, −109)`, 165 at `(−38, 46)`. Bare ground beside a spawn is not a fault
worth dressing over, and nothing was put there to hide it.

**`WX11` on the signal box, twice.** `stellwerk` at `x 31..38, z 40..48` stands 30 blocks above the cell
beside it at `(41, 38)`, fifteen of them over the void, so its foundation fills that face in bedrock.
That face is at the board's own coast, where the street's 30-block cliff already stands; the complaint is
correct and the building is deliberately sited on the railway boundary. Left as it is.

**`WX11` on both monuments**, for the same reason: a goal on a deck or on a terminus platform stands
above the cell beside it by construction. The finding offers an `area` relief mark as its mechanical fix,
which this board has no relief to carry. Its number for the deep monument is also wrong — it reports 21
blocks at `(−19, 54)`, and `GET …/column` reads the obsidian at y11–12 over paving at y8 with that
neighbour's surface also at y8, which is three.

## What a match would decide

Three things were settled without an oracle and are recorded here rather than filed as facts.

**The deep route is a corridor, and the brief rules against one.** `AUTHORING-BRIEF.md` §3 says the two
teams' ground is joined by a build zone over void and never by a land connection. This board obeys that
at every height — the chasm is full-depth and the platforms stop at the mouths — but the *inside* of each
station is a long enclosed hall that an attacker must walk end to end with two stairs as its only doors.
That is a place a defender stands. It is also what a station is, and the alternative was not to build the
board. A match decides whether the twenty-one-block wells and the open bay give an attacker enough ways
in.

**A twelve-block pillar is cheaper than a 149-block walk.** The free route to the viaduct is the ramp;
the fast one is thirteen placed blocks straight up from the street. That is the decision the deck is for,
and a board that wanted the ramp contested would raise the deck to twenty blocks and lose the headroom
under it.

**A one-way drop is a route.** The light well over the deep monument falls twenty-one blocks onto it —
nine hearts, no way back except the stairs. `aim=reach` takes it, and so would a player who is winning.
Closing it would make the deep monument a stair fight and nothing else.
