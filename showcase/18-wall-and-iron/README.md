# 18 — a wall and iron ore, authored not composed

**The technique: two structures the composer never emits — a defence wall pinned to a piece-pair interface,
and an iron marker whose kind depends only on where it is placed — both reachable only by hand-editing the
plan document.**

The plan is `02-theme`'s eight pieces, untouched, plus one `walls` entry and two `placements.iron` entries.
The finish is `02-theme`'s, untouched.

## The document

```json
"walls": [
  { "a": "lane", "b": "rise" }
],
"placements": {
  "iron": [
    { "id": "iron-armoury", "piece": "spawn", "at": [3.5, 0.5] },
    { "id": "iron-shelf",   "piece": "shelf", "at": [4, 1.5] }
  ]
}
```

Everything else — the theme, the room styles, the shell, the meadow — is `02-theme`'s. The whole technique is
these six lines.

## How the mechanism works

### The wall stands on an interface, and picks its own face

A wall names two pieces, not a rectangle. `ContactGraph.WallInterfaces` turns the marked pair into the
footprint of their shared border — a bedrock barrier two blocks thick across the seam and as wide as the
interface itself — and `PlanCompiler` fans it through the board's symmetry once, for team 0. On this board the
interface is `lane`–`rise`, 15 blocks wide at `z=75`, and the fanned pair is stamped identically at its `rot_180`
image.

Which of the wall's two faces opens for the defence chests is not a field. The wall is two blocks thick, so
exactly one face can be opened without breaching it, and `ContactGraph.ApproachSide` always picks the same one:
the side **further from the wool** — the side both the raiding team and the defence reach the line across.
Carrying it as a piece rather than a compass direction is what survives the orbit: a `rot_180` reflection swaps
which face has the smaller coordinate, but "the `lane` side" is still "the approach side" on both images. A
`side` field used to exist on `PlanWall`; it was removed because the studio never needed an author's opinion on
a question the geometry already answers, and a document that still writes one has it silently ignored.

`/api/plan/inspect` reports the resolved interface before any of this is built:

```json
{"a": "lane", "b": "rise", "kind": "land",
 "x1": 20, "z1": 75, "x2": 35, "z2": 75, "length": 15,
 "woolRoom": false, "wall": true, "wallChest": "lane"}
```

`wallChest: "lane"` is the answer settled before compile — the lane, not the rise, gets the chests, because
the rise sits between the lane and the room.

### Two refusals bound where a wall may stand

A wall pinned to a pair with no shared land border has nothing to divide, and one pinned to the wool room's own
edge would stamp through the room it is meant to defend. Both are structural errors, not lint — they block the
compile.

Posting `{"a": "flank-w", "b": "flank-e"}` — two pieces on opposite sides of the board that never touch —
answers `422` with:

```
PL11  wall 'flank-w'–'flank-e' is not a shared land interface
```

Posting `{"a": "rise", "b": "room"}` — the interface right in front of the wool room, one step closer than the
one this board actually uses — answers `422` with:

```
PL13  bedrock wall 'rise'–'room' may not interface with the wool room piece — place it around 15 blocks
      away from the room
```

`rise`–`room` sits at `z=95`; the wall this board builds sits at `z=75`, twenty blocks further out along the
same approach — inside the band `PL13`'s own message names. A wall pinned to `shelf`–`room` — a pair that is
both non-adjacent and touches the wool room — answers both rules in the same response, which is the first
thing this document got wrong: it looked like a clean `PL11` example and is actually `PL11` **and** `PL13`
together, because `PL13` checks the room role on either named piece regardless of whether the pair touches at
all. `flank-w`–`flank-e` is the pair that isolates `PL11` alone.

### The chest side, measured

The interface is thin across the seam (`z` 74–76) and long along it (`x` 20–35), so `DefenseChest.Stamp` reads
it as one lane 15 blocks wide and sets two chests, evenly spaced at a third and two-thirds along it:

| Column | Block |
|---|---|
| `(25, 74)`, y9 | Chest |
| `(30, 74)`, y9 | Chest |
| `(25, 75)`, y9 | Bedrock — the defence face, one block over, carries no chest |

Both chests sit at `z=74`, the lane-facing column — the approach — and the `z=75` column, one block into the
`rise`, is solid bedrock front to back. The wall does not have two faces with a chest each; it has one face
with two.

### The barrier itself

A column straight through the middle of the footprint, away from either chest:

```
GET …/column?at=27,75
  y 12  Cobweb
  y 11  Bedrock  ┐
  y  9  Bedrock  │ three courses above grade
  ...            │
  y  0  Bedrock  ┘
```

Ground either side sits at y8 (`GET …/column?at=27,70` and `?at=27,80` both top out at y8, grass or coarse
dirt). The wall's bedrock rises to y11 — three blocks above the surrounding grade — and one course of cobweb
caps it at y12: a barrier a team cannot break, topped with a course that costs time to cut through rather than
walk over.

### The iron marker: same field, two different structures

`plan.placements.iron` takes an `id`, a `piece` and an `at` — nothing that names a shape. What comes out of it
is decided entirely by the piece it rides.

`iron-armoury` sits on `spawn`, the piece that also carries `spawn-1`. Because the two share a piece, the iron
never reaches `PlanCompiler`'s standalone-cube loop at all — it rides `SpawnIntent.Iron` and is resolved beside
the framed spawn room (WX8/WX9). Measured, it is a **solid 3×3×3 block of iron** at `x[-14,-12) z[76,78)`,
resting on the meadow at y8 and standing y9–11 — narrower and shorter than the standalone shape, because it is
sized to the slot the room framing carved for it rather than to a fixed cube. That slot is the second effect: the
same board compiled with `iron-armoury` removed frames the spawn cube at `x[-29,-11)` — 18 blocks wide; with it
present, the room narrows to `x[-29,-15)` — 14 blocks — and the 4 blocks given up sit exactly where the armoury
stands. An iron marker beside a spawn does not add to the building; it takes a bite out of it.

`iron-shelf` sits on `shelf`, an ordinary piece with no spawn marker. It falls straight through the standalone
path and stamps a plain **4×4×4 cube** at `x[-22,-18) z[21,24)`, resting on grass at y8 and standing y9–12 —
one course taller and one block wider on a side than the armoury, because nothing here shapes it to a room.

Because the board already has a spawn piece, `PlanValidator`'s `ST2` lint checks every iron marker against it,
and `iron-shelf` fails it:

```
ST2  iron at (-20,23) outside the spawn piece
```

`/api/plan/evaluate` still answers `score 0, valid: true` — `ST2` is a complaint, not a refusal — and the cube
is kept anyway, deliberately: the point of this board is to show the standalone shape and the fact that it
does not renew, and an iron cube that never leaves the spawn piece cannot demonstrate either.

### The renewal, in the map.xml the studio writes

Only one of the two cubes is wired to regrow. `map.xml` carries a single filter pair and a single renewable
region, and the region names only the armoury:

```xml
<material id="only-iron">iron block</material>
...
<union id="iron-cubes">
    <rectangle id="iron-cube-0" min="-14,76" max="-12,78"/>
    <rectangle id="iron-cube-1" min="11,-79" max="13,-77"/>
</union>
...
<renewables>
    <renewable region="iron-cubes" renew-filter="only-iron" replace-filter="only-air" avoid-players="2"/>
</renewables>
```

`iron-cube-0`/`-1` are the two fanned images of `iron-armoury` and nothing else — `x[-14,-12)` is exactly the
3×3 footprint measured above. `iron-shelf`'s cube, at `x[-22,-18)`, appears nowhere in `<renewables>`: it mines
away and stays gone. The mechanism is a standing rule PGM re-evaluates over the region — wherever a block
inside `iron-cubes` matches `only-iron` (an iron block) and has been mined to air, it is replaced back to iron,
skipped only while a player stands in the way (`avoid-players="2"`). Nothing in the XML says "spawn" anywhere
near this rule; the region is what makes it a spawn resource, because it was only ever built where the spawn
marker put it.

## What went wrong first

The first wall pair tried was `shelf`–`room`, meant as a clean example of `PL11` (no shared interface). It
answered both `PL11` and `PL13` in one response, because `PL13` fires on either named piece carrying the
wool-room role independent of whether the pair touches at all — `shelf` and `room` share no border, but `room`
is still the wool room. `flank-w`–`flank-e`, a pair that touches nothing and involves no room, is what isolates
`PL11` alone.

The armoury cube was also expected to come out as a 4×4×4, matching the standalone shape and the finish's
notes in `docs/tools/capabilities.md`. Measured, it is 3×3×3 — a different, smaller shape, sized to the slot
the room framing opens for it rather than stamped as a fixed cube. The column read is what caught this; the
structure-preview box from `/plan/inspect` reports the same footprint and would have been trusted as a 4×4×4
without it.

## What to look at

| Picture | Says |
|---|---|
| `renders/world-ground.png` | the whole board — the wall's chest columns and both iron cubes sit far enough apart to read as separate marks, not a cluster |
| `renders/wall-section.png` | `axis=z at=27 from=60 to=95` — the wall standing above grade between `lane` and `rise`, the only view that shows it is a barrier and not a floor marking |
| `renders/iron-shelf-section.png` | `axis=z at=-20 from=10 to=35` — the standalone cube's full height over the meadow |
| `renders/world-traversability.png` | the spawn↔wool chain still connects around the wall |
| `renders/coverage.png` | dead ground is unchanged from `02-theme` — the wall and the cubes are stamped, not carved |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/compile` — `{a:"flank-w",b:"flank-e"}` | `422` `PL11` "wall 'flank-w'–'flank-e' is not a shared land interface" |
| `POST /plan/compile` — `{a:"rise",b:"room"}` | `422` `PL13` "bedrock wall 'rise'–'room' may not interface with the wool room piece — place it around 15 blocks away from the room" |
| `POST /plan/inspect` — `lane`–`rise` interface | `wall: true`, `wallChest: "lane"`, length 15 |
| `POST /plan/inspect` — wall structure box | `minX 20, minZ 74, maxX 35, maxZ 76, floor 0, top 13` |
| column `(27,75)` — wall centre | Bedrock y0–11, Cobweb y12; ground either side tops at y8 |
| column `(25,74)` / `(30,74)` | Chest, y9 — the approach face |
| column `(25,75)` | Bedrock, y9 — the defence face, one block over |
| column `(-13,77)` — armoury cube | Iron Block y9–11, a solid 3×3 footprint `x[-14,-12) z[76,78)` |
| column `(-20,23)` — standalone cube | Iron Block y9–12, a solid 4×4 footprint `x[-22,-18) z[21,24)` |
| spawn room footprint, with `iron-armoury` | `x[-29,-15)` — 14 blocks |
| spawn room footprint, without it | `x[-29,-11)` — 18 blocks |
| `POST /plan/evaluate` | score **0**, `valid: true`, complaint `ST2` "iron at (-20,23) outside the spawn piece" |
| `map.xml` `<renewables>` | one region, `iron-cubes`, naming only the two armoury images — the standalone cube is absent |
| provenance census | `ironcube: 4` (2 armoury + 2 standalone, fanned) · `wall: 2` (fanned) · `wool: 2` · `spawn: 2` · `roomfloor: 2` · `redstoneline: 2` |
| `GET …/coverage` | 3.3% dead — unchanged from `02-theme`; the wall and the cubes stand on ground that was already used |
| `GET …/preflight` | round-trip, mirror, buildability and traversability all pass; export gate **OPEN** |
