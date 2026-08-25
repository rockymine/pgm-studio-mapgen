# 01 — the base board

**The technique: the smallest board the studio will accept, and what "accept" is measured by.**

Every other showcase in this folder forks this plan and changes one thing. It is therefore worth stating
exactly what it is, because everything downstream inherits it.

## What it is

Two teams under `rot_180`, one wool each, and a gap in the middle nobody can walk across. The whole board is
one document — there is no finish worth the name (`{"authors": […]}`) — and it still exports: 2 teams, 2
wools, 16 regions, 20 filters, 11 apply-rules, export gate open.

```
      |         0        |
  -22 |  WWW             |     W  room     the wool room, set back behind the spawn line
  -21 |  W¤W             |     ¤  the wool marker
  -19 |  FFF             |     F  rise     20 blocks of ground between the lane and the room
  -17 |  FFF      SS@S   |     S  spawn    @  the spawn marker
  -15 | EEEEEEEDDDDDDDDD |     D  apron    E  lane
  -12 | CCCooooooooooBBB |     B  flank-w  C  flank-e
   -8 | CCCooooooooooBBB |     o  the hole between the flanks
   -6 | AAAAAAAAAAAAAAAA |     A  shelf    the ground that faces the gap
   -3 | ++++++++++++++++ |     +  the build zone: 30 blocks of void, crossed by bridging
```

Eight pieces a team, one build zone, two markers. `renders/00-board.txt` is the full grid.

## The five decisions

**The gap is 30 blocks and it is void, not ground.** Two teams' islands are joined by a `zones` entry rather
than by land, which is how a capture board is joined at all: `CT12` wants a strait between 15 and 40, and the
build zone over it is what makes the two halves one connected board to every reachability check downstream.
Take the zone away and the wool is refused as unreachable before a world is ever built.

**The zone has to reach the ground either side of it.** The build zone spans `z −20..20` against shelves whose
inner edges stand at `z ±15`, so it overlaps both. A zone that stops short of the land — even by a cell — links
nothing, and the refusal it produces (`wool … is unreachable from team 1's spawn`) names the wool rather than
the zone.

**The frontline is derived from the zone, not stated.** `FannedGraph` calls a piece *frontline* when it
touches a build zone, and `SP1` requires the wool to be reachable from a frontline piece **without crossing a
spawn**. A board with no zone at all has no frontline, so `SP1` fails on a board that looks perfectly
connected. That refusal — `wool on 'room' is only reachable through a spawn piece` — is what a first attempt
here actually hits, and the fix is the zone rather than anything about the wool.

**The island has a hole in it, and the hole is what makes the fill ratio legal.** `G8` wants the plan's
rectangles to cover between 20% and 54% of their own bounding box. A solid slab reads 0.83 and a solid slab
with a mid gap reads 0.63; splitting the middle band into `flank-w` and `flank-e` and leaving 50 blocks of
void between them brings it to 0.47. This is not a formality — over 400 composed boards, 63% of hubs are a
ring or a double hole, and a board with no void in it is a board with one route.

It is also what gives the board its two ways round. An attacker landing on the `shelf` chooses `flank-w` or
`flank-e`, and only the east one reaches the wool without crossing the spawn.

**The wool sits behind the spawn line, at the far end from the gap, with a run of ground in front of it.**
That is what the ratio measures: `renders/01-flow.txt` reads *the attacker walks 194 blocks to it; the
defender 78*. The wool is defended because it is deep, and the attacker's road is long because the board is
long.

`rise` is the twenty blocks between the lane and the room, and it is in the base board on purpose. A wool
room flush against the ground that feeds it has nowhere for a stair, a ramp or a raised keep to go, so every
showcase that lifts the objective would have had to redraw the board first. Here it is a flat strip, and
`05-ramp-and-slant` is the same strip with four anchor heights on it.

## What it deliberately does not have

No theme, no relief, no props. What it does have is **buildings**, because the alternative is not "plain",
it is bedrock:

```json
"roomStyles": { "spawn": "@showcase-hall", "cage": "@showcase-cage" }
```

A spawn or a wool room with no bound style stamps the built-in shell, which is a bedrock box. That is never
what an author wants and it is never worth showing, so the two forked presets in `tools/styles/` are part of
the base board rather than of a later lesson. `15-houses` is about *choosing* a style; this is about not
leaving it unchosen. The `"@name"` form loads `tools/styles/<name>.json`, which is what keeps the finish
short enough to read.

The ground under them is bare, and the build says so:

```
[complaint] SK8  the board is finished carrying no finish: no theme registry, so every column paints the
                 built-in finish; no relief, so the ground is as flat as the shapes stated it; nothing
                 placed on it … it exports as raw stone, and nothing later says so
```

`SK8` is the only complaint this board raises, and it is correct even with the two styles bound — a room
style is not a *finish*, because it dresses a structure rather than the ground. Bare stone is the floor
every other showcase is measured against: `02-theme` is this board with paint on it and nothing else
changed.

## What it compiles to

Six pieces a team fuse into **one polygon a team**, because every piece states the same surface and the
compiler makes one shape per distinct height within a component:

```
s0  polygon  base_height 9      team 0's island — the canvas every later showcase sculpts
s1  polygon                     team 1's island
spawn-red / spawn-blue          role spawn      — projected, not terrain
wool-red-red / wool-blue-blue   role woolRoom   — projected, not terrain
islands: [ team (mirrors) → s0, s1 ]
```

Those two ids are the handle a finish keys on: `themeById: {"s0": …, "s1": …}` paints the ground, and a
`shapePropsById` entry merges relief scope or controls onto it. **Key both.** A finish naming `s0` alone
paints half a symmetric board and nothing complains.

## The block above the objective is deliberate

A column read anywhere over a wool room answers a small block of the team's wool colour around **y 38–40**,
twenty-odd blocks over the cage:

```
GET …/column?at=27,102
  y 40   Red Wool   ┐
  y 39   Red Wool   │ GoalMarkerStamper — a sky marker over the goal
  y 38   Red Wool   ┘
  y 12   Red Wool   ← the room's own floor, in the same colour
```

`GoalMarkerStamper` puts one over every goal — a wool room, a destroyable, a core — so a player can see where
it is from across the board, and it is stamped **above the map's build-height cap** on purpose: a marker
inside build range is a marker a team can dismantle. It is not terrain, so it does not enter the cap's own
derivation. Nothing authored it and nothing needs to.

## What to look at

| Picture | Says |
|---|---|
| `renders/00-board.txt` | the plan as cells — the only view that puts two rectangles on the same rows |
| `renders/01-flow.txt` | the two walks to the wool and the ratio between them, off the plan alone |
| `renders/room-spawn-section.png` · `room-cage-section.png` | the two buildings in section, before a world is built |
| `renders/world-topdown.png` | the built board: two islands, a hole each, the gap between them |
| `renders/world-traversability.png` | that the gap reads as connected, because the build zone opens it |
| `renders/coverage.png` | 3.5% of the ground is off every route — the hole costs nothing |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, no violation, no lint |
| `POST /plan/inspect` | one island gap, **30 blocks** (`CT12` wants 15–40) |
| `GET …/plan/flow` | attacker 194 blocks, defender 78 |
| `GET …/coverage` | 7 979 reached · **271 dead** of 8 250 = 3.3% |
| `GET …/preflight` | export gate **OPEN** |
| extent | 80 × 220 blocks, cell 5, `surface` 9, ground top y8 |
