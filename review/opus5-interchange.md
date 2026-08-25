# Interchange — five rooms you have already been in

> A liminal DTM board, built to a brief from outside this repository: an ordinary theme at the
> centre branching outward into familiar environments made slightly wrong, five obsidian monuments a
> team, each in its own room with its own colour, some of them underground and some in the sky, and
> **repetition** and **exploration** as the two ideas everything else answers to.

**In one sentence:** a municipal transit interchange folded onto itself — one concourse over a
drained swimming pool and under an empty car deck, with a corridor of doors that loops back on
itself, a lawn you can see through glass and cannot walk onto, and the same kiosk standing in all
nine rooms.

124 × 248 blocks, `rot_180` about the origin, **four storeys** (y6 · y18 · y26 · y38), build ceiling
58, one continuous landmass. Ten `<destroyable>`s, obsidian, one or two blocks each.

## The five rooms, and where each monument is

The brief asked for three to five monuments "each in its own area with its own layout and colour
scheme, making the areas easy to tell apart", and for some of them to be somewhere other than the
ground. Five, at five heights, at five depths into the board:

| # | Monument | Room | Storey | Where | Blocks | Own walk | Enemy walk |
|---|---|---|---|---|---|---|---|
| 1 | **The Deep End** | the drained pool | `under`, y6 | `(30, 6, 78)` | 1 | 106 | 248 |
| 2 | **The Catwalk** | a gallery in the stairwell | `catwalk`, y26 | `(-38, 28..29, 68)` | 2 | 126 | 235 |
| 3 | **The Back Office** | the sealed core of the corridor of doors | `ground`, y18 | `(34, 22, 62)` | 1 | 84 | 229 |
| 4 | **Level 4** | the car deck | `deck`, y38 | `(-26, 42..43, 50)` | 2 | 156 | 265 |
| 5 | **The Court** | the garden court | `ground`, y18 | `(24, 22..23, 90)` | 2 | 82 | 227 |

Walks are `GET …/walk?aim=reach` from each team's own spawn, the route that places the fewest
blocks. **Every one of the ten is reachable by both teams placing nothing** — the vertical
circulation is ramps, not pillars. The one exception is a measurement artifact rather than a fault:
the cell *directly under* a floating monument has two blocks of clearance, so `to=-38,68,26` answers
`blocks 3` while `to=-36,68,26`, one step beside it, answers 0.

Both teams' monuments carry the **same five names**, because a stated name is used verbatim on every
orbit image — and on this board that is the point rather than a cost.

## The four storeys, and what makes them possible

A layer is a slab: one span per column, one theme, one surface. Four of them stack here, all at
`base_y 0` with the height carried by each shape's own `floor`, so a course is never counted twice.

| Layer | Blocks | Stood on at | Is |
|---|---|---|---|
| `under` | 0..11 | y3 (basin) · y6 (floor) | the service level: the pool hall, two sealed plant rooms, the ring corridor round them |
| `ground` | 12..17, walls to 25, spine walls to 29 | y18 | the concourse: the spine, the corridor of doors, the stair hall, the garden court |
| `catwalk` | 24..25 | y26 | a twelve-by-four gallery hanging in the stairwell, reached off the up-ramp |
| `roofs` | 26..27 | y28 | the spine's own roof, which turns the only through route into a tunnel |
| `deck` | 34..37 | y38 | the car deck: 36 × 40 of empty slab marked out in sixteen-block bays |

**A wall is not a shape on top of a floor.** A layer keeps one span per column and a taller add
replaces a shorter one outright, floor and all, so every wall on the concourse is the *same slab
carried higher*: floor 12 with a thickness of 14 rather than 6. The pool is the mirror of that rule —
its deck is drawn as four rectangles clamped **around** the basin, because a shorter shape inside a
taller one on one layer is simply not in the world (`SK9`).

**The layers are written bottom-up, and that is load-bearing.** The painter walks the stack in
document order and each pass paints its whole column, so a storey listed after one that stands over
it never sees a stone block again: with the compiled `ground` layer first, the drained pool came out
painted in the corridor-of-doors' brown clay. The undercroft is inserted *before* the compiled layer
for that reason alone.

## The two ways down and the two ways up

Vertical circulation is the whole board, so it is worth stating in numbers.

| Route | Where | Rise | Run | Tread |
|---|---|---|---|---|
| the stairwell, down | `under`, x −40..−32, z 60..80 | 12 | 20 | 1 block, never 2 |
| the ramp, up | `ground`, x −52..−44, z 48..80 | 20 | 32 | 1 block, never 2 |
| the light wells | `ground` subtracts at (−26..−18, 66..74) and (42..48, 60..68) | −12 | — | a drop, one way |
| the pool steps | `under`, x 24..32, z 56..62 | 3 | 6 | 1 block |

**A slope of one course per cell builds as treads of two**, and a two-block rise costs a placed
block to climb: the stairwell at 12-over-12 read `18 16 16 14 14 12 12 10 10 8 8` and could be
walked down but not up. At 12-over-20 it reads one course a cell and walks both ways for nothing.
The up-ramp was right first time at 20-over-32 and is what the correction was measured against.

The light wells are deliberately one-way. Falling twelve blocks into the service level is a shortcut
into the pool that costs health; the stairwell is the way back.

## Repetition, four ways

The brief named the devices. Each one is a measurable thing on the board rather than an intention:

**The same theme in several similar-looking spaces.** The board is one symmetry unit fanned by
`rot_180`, so *the whole complex occurs twice* — the room a player fights through at z +62 is the
room they will fight through again at z −62, in the same colours, with the same monument name over
it. That is the largest instance of the device and it costs nothing, because it is what symmetry
already is.

**Corridors and stairways that loop back into spaces already visited.** The corridor of doors is a
ring: a 10-wide gallery round a sealed core, both legs 28 blocks, so crossing the room west to east
is **56 blocks** against 34 in a straight line. The service level under it is the same shape — a
ring corridor round two solid plant rooms. And the core itself has exactly one door, in its north
face, so leaving the room the monument stands in costs **39 blocks** to get 16 blocks west.

**Glass between spaces, so areas are visible and connected in strange ways.** Four instances:

| Where | Pane | What it shows |
|---|---|---|
| the core's floor, x 26..38 z 58..66 | cyan | the drained pool, sixteen blocks below, and *The Deep End* standing in it |
| the spine's east wall, z 48..54 and 66..72 | yellow | the corridor of doors, from a corridor that does not join it |
| the spine's crossing of the court, z 84..96 both sides | green | both lawns, neither of which can be entered from the spine |
| the car deck and the concourse under it, x −30..−22 z 56..64 | light grey, twice | one shaft through three storeys: the deck, the stair hall floor under it, and the service level under that |

The court crossing is the one that changes play. The spine runs the full length of the complex and
the garden court is the only room it passes *through* without opening onto, so the lawn is sixteen
blocks from the spine and **52 blocks of walking** away: out of the spine, into the corridor loop or
the stair hall, and back in through one of the court's own two gates.

**And it is the one room that grows.** Four oaks, a birch, a kiosk, a cairn and ground cover at 0.55
coverage on the west lawn; an oak, a birch, a kiosk and a cairn on the east, where the monument's own
clearance takes most of the room. Outside the north wall the approach carries two more oaks and a
birch spaced as an avenue rather than a wood, over the unmown verge; the apron and the plaza carry
six oaks and two ground-cover fields between them. Seventeen trees authored, thirty-four fanned, and
the whole of the board's planting is in the four rooms that have a sky.

**One or two small structures repeated as decoration.** A 6 × 6 flat-roofed kiosk in light grey clay
under a quartz slab, and a three-lobed andesite cairn beside it, stand in **nine rooms**: the plaza,
the apron, the approach, the corridor of doors, the pool hall, the stair hall, both lawns of the
garden court, and the car deck. Fanned, that is eighteen kiosks and eighteen cairns on a board that
has no other building. The one in the pool hall stands under a six-block ceiling.

**And the markings, which are the smallest instance of the same idea.** Two dark-prismarine lanes run
the length of the drained basin, `x 22..25` and `x 31..34`, so the pool reads as a pool with the water
taken out of it. A worn track crosses the car deck and another goes round the corridor's ring: both are
`worn` strokes at 0.5 coverage in light grey clay and gravel, laid over floors made of something else,
so what they say is that somebody walked here often enough to wear a line into it.

The lanes are **shapes** and not strokes, and that is not a stylistic choice: a stroke ignores
`layer` and seats on the whole-board top surface, so a lane stated for the basin landed on the corridor
floor sixteen blocks over it. A rectangle of the basin's own thickness carrying only a different theme
is the way to mark a floor that has a roof.

**Spaces that are extremely large or extremely narrow, kept brief.** The car deck is 36 × 40 of
empty slab with one oak on it. The balcony is the other end: a three-wide slot through the east skin
onto a 6 × 9 platform hanging over the void, which goes nowhere.

## What each room is made of

Nine themes, and each one names a structural family and one accent and stops there.

| Room | Floor | Wall | Accent |
|---|---|---|---|
| plaza · apron · approach | grass over dirt, ringed inward with cobble, stone brick and slab from the coast | stone brick banded with andesite | quartz rim |
| the spine | light grey / white clay checker at 4 | white clay | slab coping |
| the stair hall | polished andesite / andesite checker at 8 | grey clay | orange clay band |
| the ramps | polished andesite over andesite over orange | andesite | orange nosing |
| the corridor of doors | oak / dark oak checker at 6 | brown clay | yellow clay band, yellow glass |
| the garden court | **mown in six-block squares**: plain grass against a noise of lime and green clay, over dirt | green clay over mossy cobble | a green-clay rim wherever the lawn meets a wall (`rimEdges: boundary`) |
| the approach outside it | the same three greens unmown — a noise of grass flecked lime, over dirt and podzol | green clay over mossy cobble | mossy rim |
| the car deck | double stone slab / light grey clay checker at **16** | light grey clay | slab band |
| the pool deck | white / light grey clay checker at 2 | cyan clay | prismarine brick rim |
| the basin | light blue clay streaked cyan, over prismarine | prismarine brick, dark prismarine | — |
| the pool's lanes | dark prismarine over prismarine | — | — |
| the service level | a voronoi of cracked brick, stone brick and gravel | grey clay | black clay, cracked brick coping |
| the outer skin | quartz coping | hardened clay banded with stone brick | light grey clay |

The checkerboards are the liminal signature and they are sized to the room: two blocks in a swimming
pool, four in a corridor, **six on the lawn**, sixteen on a car deck, where the squares stop reading
as tiling and start reading as parking bays. Read across the west lawn at `z = 88`, `x −34..−21`:
gravel, gravel, grass, grass, lime clay, green, green, green, green, green, grass, grass, grass,
grass — the road, then a mown square, then an unmown one, six wide. The court is the only room whose
pattern is made of three blocks rather than two, and the third is what stops it reading as a
chessboard: the dark squares are a noise field of lime and green rather than one colour.

**The rim is doing a job here that no shape does.** `rimEdges: boundary` calls a column rim where any
neighbour is a *different plateau* — which inside a room means a wall — so the lawn gets a
single-course green-clay edge everywhere it meets one, and the planted border round a municipal lawn
costs no geometry at all. It is the one place on the board a rim is on, and the reason is that this
is the one room whose edges were built rather than eroded.

## What the reads say

`GET …/preflight`: **export gate OPEN**. Round-trip clean, mirror clean, buildability clean —
all placements on solid ground — and traversability connected for both teams.

`GET …/coverage`: **7.3 % dead** — 1,678 of 22,956 ground cells no journey passes. The five largest
dead patches are all one block from used ground and all on the complex's outer margin between the
skin and the rooms inside it, which is the thickness of a wall rather than a landform nobody visits.

The dressing pass places **90 props and declines none** — 45 authored, fanned.

Eight `SK11` complaints ride on every stage, and all eight are tops: the spine's roof (1,384 places
a side, in a two-block-deep slot between its own parapets), the outer skin's coping (336), the
door-rank walls (272) and one court wall (64). Ground with sky over it and no way onto it is exactly
what the top of a wall is.

## Where it departs from the numbers, and why

**`GO1` — goal-to-spawn walk ratio.** The band is 3.0–4.0; the five goals measure **1.70, 1.87,
2.34, 2.73, 2.77** on the real walk. The cause is the circulation rather than the placement: a maze
lengthens the *defender's* walk as much as the raider's, and adding sixty blocks to both ends of a
ratio pulls it toward 1. `POST /plan/inspect` answers 2.19–5.31 for the same five markers, because a
plan is five rectangles and knows nothing about the walls that make the board — **on a board whose
circulation is authored in the sketch, every plan-level distance is measuring a room that is not
there.**

Taken as a set the five are a front-to-back gradient rather than a flat band: *Level 4* on the deck
is the most exposed (1.70) and *The Court* behind two gates the least (2.77), so a raid has an
order to it. Whether a five-goal board should hold each goal to a band written for a one-goal board
is a gameplay question with no oracle in this session; the numbers are stated so the author can
overrule the decision.

**The walls can be climbed.** Every room wall stands eight courses over the concourse, and
`aim=travel` finds routes over them for 7 to 17 placed blocks against 82 to 156 blocks of free
walking. That is the intended reading — the corridors are the free path and the roofs are a priced
shortcut — but it is a decision rather than a constraint, and a player who wants to bypass the
corridor of doors can.

**The undercroft is dark.** Nothing in the studio places a light source, and the service level and
the pool hall are enclosed. The two light wells and the core's glass floor are the whole of the
daylight down there. On a liminal board that reads as intent; on a playable one it may not be.

## Not stated, deliberately

**No relief.** The board is a building and every floor in it is flat. A relief solves an island's
whole surface, so stating one would have taken the concourse's level away from it; the height model
here is `floor` and `base_height` per shape, which is what a slab wants.

**No water.** The pool is drained. That is the brief's uncanny reading of a familiar place, and it
is also the only way to put a monument in the bottom of one.

**No wool rooms, no cores, no water lanes, no build zones.** One landmass, no strait to bridge;
`build.voidEnforcement` is set with no exclusions instead, which wires
`<apply block-place="deny(void)" region="void-enforcement-area"/>` over everywhere, so the void
around the complex cannot be built out into at any point in the match.
