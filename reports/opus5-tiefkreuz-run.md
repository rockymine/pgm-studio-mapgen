# Opus 5 — Tiefkreuz: a destroy board on four storeys, and what the surface let me say about a stack

## What I set out to build

A **multi-level transit interchange played on four storeys**, where the whole middle of the board is the
station and the vertical is the point. Written down before any shape was authored:

> A lane 80 × 224 blocks, `rot_180`, cut across its middle by a 32-block chasm. In each half, a terminus
> station buried under the street: two running tracks and three platforms at y8 in cut-and-cover, a
> concourse mezzanine at y18 over them, the street at y29 over that, and a brick viaduct at y41 over the
> street. Two destroyables a team — one on the deepest floor and one on the highest, 34 blocks apart in
> the vertical — so a raid on either has to be climbed or descended and not merely walked. The train
> hall, the platform canopies and the rolling stock drawn, not painted.

That is what was built. `maps/opus5-tiefkreuz` · `specs/opus5-tiefkreuz` · `review/opus5-tiefkreuz.md`.

## The three numbers

```
03-slopes.txt   11 994 walked, 300 scrambled, 1 658 barrier; 10 faces, largest 431 at x -21..20 z -59..-24
06-claims.txt   placed 28, declined 0
04-routes.txt   the worst step on any spawn→goal route is the walk's own 60-block climb onto the
                observer platform, which is a read artefact and not a route (§7)
```

`GET …/preflight`: **export gate OPEN**. `GET …/coverage`: reached 11 521, decorated 936, dead 1 495 —
**10.7% dead**, all of it the corners beside the two head houses. `POST /plan/evaluate`: **score 0,
valid, no violations, no lint.** `POST /plan/inspect`: `GO1` 3.07 and 3.42, `GO4` 55 and 52, `GO2` 38,
`GO3` 127 / 123 / 142, `CT12` 32 — every band met on the first plan that stated `plan: 2`.

---

## What the surface let me say, and what it did not

This run exists to answer that, so it gets the numbers with it. Eight entries: five are places where I
wanted to change one thing and had to reach for something else, and three are capability claims — every
one of them checked against `GET /api/openapi/v1.json` before it was written, which is why two of them
say *mistaken* and only one says *missing*.

### 1. A goal's storey — **it used to be missing and it is not any more**

**Wanted:** to say that one monument stands on the platform level and the other on the viaduct deck.

`opus5-interchange` reported this as *"missing from the system … the field is a string on a record the
compiler already builds"*, and worked round it with a `goalLayers` key in `tools/drive.py` that copies
the word onto every orbit image of the compiled intent.

**Found:** `DestroyablePlacement` now carries `layer` — *"Which layer's surface this stands on, or null
for the top one … Carried straight through to the intent the compiler writes."* Two words in the plan:

```json
{"id": "tief", "piece": "", "at": [-16, 56], "layer": "ground",   "float": 2}
{"id": "hoch", "piece": "", "at": [ 22, 62], "layer": "viadukt",  "float": 3}
```

`POST /plan/compile` answered `"layer": "ground"` and `"layer": "viadukt"` on all four orbit images, and
both monuments landed on the surface they were stated for on the first build — `<cuboid
id="tiefbahnsteig-region" min="-16,11,56" max="-15,13,57"/>` and `<cuboid id="hochbahnsteig-region"
min="22,45,62" max="23,47,63"/>`. **Cost: two fields.** `drive.py`'s `goalLayers` was not needed.

**Verdict: shipped.** The one place a stacked board most obviously needed a word, it has one.

### 2. The walk's storey — **mistaken, and it cost me every route number in the sweep**

**Wanted:** what it costs to walk from a spawn to a monument on the viaduct deck.

**What the sweep said:** `04-routes.txt` reported `spawn-red -> hoch-0: 53 blocks, 0 placed, 0 drops,
walked end to end` — a route that never leaves y30. The monument is at y45, on a deck at y42, twelve
blocks over that route's last step.

**What I nearly wrote:** that `walk` cannot address a storey.

**What is actually there:** `GET …/walk` takes `from` and `to` as *"`x,z`, or `x,z,y` to pick which
storey of a stacked column is meant."* It is in the OpenAPI parameter description. The sweep does not
pass a `y` — `tools/render/textreads.py` derives its endpoints from the spawn point and the goal anchor
as `x,z` — so on any stacked board `04-routes.txt` measures the walk to a *column* and calls it the walk
to the goal.

Re-taken by hand, naming the storey, the board reads:

| From the red spawn (0, 106, 30) | `aim=reach` | `aim=travel` |
|---|---|---|
| own deep monument `(−16, 56, 9)` | 60 blocks, 3 placed, one 21-block drop | the same |
| own high monument `(22, 62, 42)` | **149, 0 placed** — by the ramp | 53, **13 placed** — pillared up |
| enemy deep monument `(15, −57, 9)` | **181, 28 placed** | 169, 78 placed |
| enemy high monument `(−23, −63, 42)` | **370, 25 placed** | 178, 44 placed |

**Verdict: mistaken**, in the brief's sense — it exists, it is documented, and the read that writes the
file does not use it. **Cost: eight `curl` calls**, and one wrong belief I held for two builds (that the
viaduct was somehow reachable for nothing).

### 3. A stroke has no storey — **missing, for one prop kind, and it changed the board**

**Wanted:** one avenue from the head house to the station, running under the viaduct on its way.

**What happened:** a `stroke` seats on the column's top surface, and under the viaduct the top surface is
the deck at y41. A single stroke would have paved the viaduct's ballast instead of the street eleven
blocks below it.

**Checked:** `PlacedProp.layer` is on the abstract prop — *"Which layer's surface this prop rests on"* —
and `DR-LAYER` refuses a prop naming a layer the board has no ground on. Both apply to `stroke` in the
schema; neither reaches the seating. `opus5-interchange` measured the same thing on lane markings
(`"layer": "under"` came back at `y 25`).

**What I did instead:** drew the avenue as **two strokes** that stop at the viaduct's two faces —
`bahnhofstrasse-nord` from `(0,104)` to `(0,78)` and `bahnhofstrasse-sued` from `(0,60)` to `(0,42)`.
**Cost: one extra prop and four lines.** The interruption is legible as a street passing under a bridge,
so this one is arguably better than what I asked for.

**Verdict: missing** for `stroke`, exactly as reported before. Every other prop kind honours the word.

### 4. A layer's paint runs from the bedrock course up — **unreachable, and it cost a whole build**

**Wanted:** the viaduct's iron rails to be iron, and the street under them to be street.

**What the first build gave me**, read at `GET …/column?at=0,66`:

```
y 42..39   Iron Block      the rail on the deck  — correct
y 29..27   Stone Bricks    the street lid        — correct
y 26.. 1   Iron Block      the whole column beneath it
```

`TerrainPainter` walks the layers in order and each pass paints its column from the bedrock course to its
own top; the only thing that stops a pass treading on the one below is the **stone-only invariant** —
it writes over `(Stone, 0)` and nothing else. My ground themes filled in `1:0`. So the viaduct's pass
repainted 26 courses of city as iron, and nothing anywhere said so: the store answered 200, the export
gate answered OPEN, `themes/census` counted the *surface* and was right, and the isometric drew a grey
board because grey is what a top-down of a lit street looks like.

**The fix is one field and it is a field on a different theme**: no ground theme may fill in plain stone.
`stadt.fill` → `1:5` andesite, `bahn.fill` → `1:6`, `schotter.fill` → `1:5`, `ziegel.fill` → brick.

**Verdict: unreachable.** The mechanism is documented — `SCULPTING-WITH-LAYERS.md` §4 states it exactly,
and names `WE56` as the fix that would remove it — but there is no field on a layer that says *paint only
your own span*, no warning when a pass overwrites a lower layer's column, and the cure is stated in terms
of a value in an unrelated document. **Cost: one build (~10 minutes) and one `column` read.** The
`column` read found it in one call; nothing else on the board would have.

### 5. `rimEdges: "drop"` on a two-course slab caps the whole slab — **the rule, working**

**Wanted:** a platform-edge line — a course of a different block along the platform's own lip.

**What I did:** set `bahn.rimEdges = "drop"`, which caps *"wherever the ground falls away, tread edges
included."* A concourse slab two courses thick has a drop on every side of every column, and so does
every tread of a stair; the rim took the top course everywhere, the surface pattern never ran, and
`GET …/column?at=-4,48` read `y25 Quartz / y24..y17 Stone` — a stair with an unpainted body.

**What I did instead:** `rimEdges: "void"` on `bahn` and no platform-edge line at all. `stadt` keeps
`"drop"`, where it is right: it kerbs the street at the chasm and round the trainshed's open bay, which
is what makes the hole read as an edge.

**Verdict: not a gap.** The rule says what it does and I asked for the wrong thing. **Cost: one build to
notice, one word to fix.** Worth writing down because *drop* is the intuitive choice for a built board
and it is wrong for anything thinner than the rim is deep.

### 6. A light — **missing as a fixture, reachable as a block, and I found the second one late**

**Wanted:** to light a station whose two lower storeys are enclosed.

**Checked in `GET /api/openapi/v1.json`:** `glowstone` — 0 hits. `torch` — 3 hits, none of them a
placement (a wool room's entrance redstone line, and a note about headroom). `light` — no field on any
prop, style, theme bucket or layer. **There is no lamp, no light prop and no lit-block bucket.**

**But a theme's material is any `(id, data)` pair**, so a light is a block like any other block, and a
lit floor is an ordinary shape carrying a glowstone theme. The board now has a `licht` theme —
`surface: glowstone` one course deep over an ordinary body — on **18 one-column pavers** down the three
platforms, every six blocks, and **10 two-by-two panels** cut out of the concourse slab and put back at
the same span, so their glowstone reaches both the floor they are in and the platform beneath.
`GET …/column?at=-17,44` reads `y8 Glowstone / y7..y1 Polished Andesite`.

**Verdict: missing** as a *fixture*, **not missing** as a *material* — and the difference is the whole
finding. `opus5-interchange` filed this as "missing from the system, and it is the one gap that would
change what a stacked board can be", built its board dark, and was right about the fixture and wrong
about the capability. **Cost: one build, one theme, 34 shapes generated by two list comprehensions.**

### 7. The observer platform is the only ground in the strait, and every cross-team walk uses it

**Wanted:** `04-routes.txt` to say what crossing the chasm costs.

**What it says:** `spawn-blue -> tief-0 … barrier +60 at (-2, -9); drop -60 at (-2, 10)`. The walk climbs
sixty blocks, crosses the void at y69 and drops sixty. `GET …/column?at=0,0` reads **one block of
bedrock at y68** — the observer platform, which the export writes at `(0, observerY, 0)` whatever the
board is, and which on a board whose middle is void is the only ground in the strait. The walk stands on
any ground, `aim=travel` does not price a climb, and so every cross-team route goes over it.

**What I tried:** `globals.observerY`, the plan's only control over it. Moving it from 58 to 68 put the
pad above `<maxbuildheight>64</maxbuildheight>`, which is worth having — no player can now build to it —
and did not change the read at all, because the walk does not respect the build ceiling either.

**Verdict: in the design.** The platform has to be somewhere and the walk has to stand somewhere. The
honest crossing number is `aim=reach`'s: **28 placed blocks** from the quay at `(28, 15)`. **Cost: one
build, and every `04-routes.txt` cross-team row on this board is unusable.**

### 8. The layout has a fine-grained edit surface, and I did not use it — **mine, not the system's**

Looking for a way to change one shape, I found the whole of it in the OpenAPI document *after* the board
was finished:

```
PATCH  /api/map/{slug}/sketch/shapes/{shapeId}        change one shape without restating the board
POST   /api/map/{slug}/sketch/layers/{layerId}/shapes draw one shape on a layer
DELETE /api/map/{slug}/sketch/shapes/{shapeId}
PUT    /api/map/{slug}/sketch/layers/{layerId}        state one layer of the stack
DELETE /api/map/{slug}/sketch/layers/{layerId}
PUT    /api/map/{slug}/sketch/themes/{themeId}        register one theme, replacing whatever was there
PUT    /api/map/{slug}/sketch/relief/{groupId}
POST   /api/map/{slug}/sketch/props · PATCH · DELETE  one placement at a time
```

Plus three reads that would have saved builds and that I met too late:
`POST …/sketch/seats` (*"where a prop of a stated kind and footprint may stand"* — the placement oracle
`--candidates` approximates by trial), `POST …/sketch/probe-footprint`, and
`POST /api/terrain/theme-map-preview` (*"body is a plan JSON; compiles it, paints the terrain"* — a
whole-board paint without a world, which is exactly the read that would have shown fault 4).

**Verdict: mistaken.** The surface is there, it is per-part, and it is documented. What I did instead is
in the next section, and I would do the same again — but the claim "you can only re-post the whole
document" would have been false.

---

## How I edited the layout while iterating

**I never posted a layout. I edited a constant and re-derived every document from it.**

`specs/opus5-tiefkreuz/build-spec.py` writes the plan and the finish from about forty named constants —
the box's five cross-section strips, the z-bands of the mouth, the open bay and the concourse, the two
stairs' extents, the viaduct's deck and parapets, the ramp's run. `tools/drive.py` then compiles the plan
afresh on every run and applies the finish to the compiled layout, so the layout is **output** and never
input. Seven drives — one refused at the house-style gate before anything was built, six that
exported a world — seven regenerations, and the committed spec is the board.

The reason is not tidiness. It is that on a stacked board **one number is load-bearing in four documents
at once**, and the edit that matters is never one shape:

> The street flight had to move off the board's centre line, because the avenue wanted to run down it.
> `STAIR_STREET = (-8, 0)` → `(-14, -8)`. That one tuple moved the flight's eleven treads, re-cut the
> hole it makes in the concourse slab, re-cut the hole it makes in the street lid, and moved the lid's
> parapet row round it — **34 rectangles across three layers**, all of them derived by a
> `carve(outer, holes)` routine that turns a slab and its openings into the rectangles that remain.

Doing that through `PATCH …/sketch/shapes/{shapeId}` would have been eleven PATCHes for the treads and
then a re-derivation of two slabs by hand anyway, because the API has no *"this slab, minus these
holes"* — a slab with a hole in it is not a shape, it is the rectangles left over, and the arithmetic of
which rectangles those are is the authoring work. The per-shape routes are the right surface for the
Sketch tool's canvas, where a person drags one rectangle at a time; they are the wrong grain for a board
whose geometry is a function.

**What I did use per-part, and it paid every time:** `tools/loop.py`, which posts the compiled-and-patched
layout to `sketch/relief/read` and `sketch/dressing` **without storing anything**. Twenty seconds against
a ten-minute drive. Two of the four faults in this run were found by a full build that `loop.py` would
have caught — and the third, the ramp climbing away from the deck, would have shown in one line of
`loop.py --profile x=-30,z=55..65`, which reads the built columns off a posted document with no map row
touched. **That is the lesson of this run's process: the iteration loop is `build-spec.py` → `loop.py`,
and `drive.py` is the last step, not the first.** I ran it as the first step four times.

One caveat measured afterwards, because it decides which of `loop.py`'s two column reads to use on a
stacked board. `--profile` answers **one height per column and it is the ground layer's** — down the
ramp it reads `54:38 55:38 … 60:41 61:41 62:29 63:29`, where 29 is the street *under* the viaduct and
not the deck at 41. `--column` is the one that keeps the stack: `column (-30,61): ground 41, top 41;
runs top..bottom (41,40,0) (39,30,0) (29,1,0)`. So the read that would have caught the ramp is
`--column`, one call either side of the join, and `--profile` would have agreed with the fault.

---

## What I got wrong

**I drew the viaduct's ramp climbing away from the deck.** Twelve treads, `z0 = RAMP_S_Z[1] - 2*(k+1)`,
so tread 0 (the lowest) sat *nearest* the viaduct and tread 11 (the highest) furthest from it. The ramp
was a perfectly walkable flight that ended twelve blocks below the deck it was drawn to reach, and the
deck was unreachable. Nothing in the drive refused it. What said so was **`SK11`, 1 000 places of
standable ground around `(-36, 62) @43` with open sky over them and no route onto them** — the deck,
named with its coordinates, on a 200. A driver reading status codes would have shipped an elevated
objective nobody could stand on.

The same complaint, in the same build, named the second half of it: **`SK11`, 8 252 places around
`(-14, -54) @7`** — the whole platform level. The street flight's bottom tread landed two blocks short of
the concourse slab and hung over the open bay, so the only way down to the concourse was a fall, and
`SK11`'s walk is a walk *onto* ground. Both were one constant each.

**`WX11` reports the deep monument twenty-one blocks up, and the world says three.** The complaint
reads *"destroyable tief 0 stands 21 blocks above the cell beside it at (−19, 54)"*. Read back:
`GET …/column?at=-16,56` gives obsidian at **y11–y12** over quartz paving at **y8**, and
`?at=-19,54` gives that neighbour's surface at **y8** — three blocks, not twenty-one, and twenty-one is
exactly the drop from the street (y29) to the platform. `map.xml` agrees with the world:
`<cuboid id="tiefbahnsteig-region" min="-16,11,56" max="-15,13,57"/>`. The same complaint on an earlier
build, before the light well moved by one column, said **3**. It is a complaint, nothing was lost, and I
cannot reconcile the number; the export honours the goal's `layer` and this read appears not to.

**I believed a "walked end to end".** Fault 2 above: for two builds I read `spawn-red -> hoch-0: 53
blocks, 0 placed, walked end to end` as *the viaduct is reachable* when what it meant was *the column
under the viaduct is reachable*. The tell was in the same file and I did not look at it: the route's last
row reads `(22, 62) 30`, and the deck is at 42.

**I put the goods shed inside a goal's clearance and did not know until the dressing pass.** `OB19`'s box
is a 10-block square about the anchor tested against the prop's footprint *plus its eaves*; the shed at
`x 24..36, z 44..56` and the monument at `(22, 62)` overlap by four columns. `loop.py` answered it in
twenty seconds — `decline OB19 building 'gueterschuppen' stands on (24, 52), inside a goal's clearance` —
which is the read the skill's table points at and the one thing in this run I did right the first time.

**My first three house styles passed `preview-snapshot` and were refused by the store.** `POST
/room-styles/preview-snapshot?format=png&view=section` answered 200 for all three; `POST
/map/from-documents` refused seven findings — `HS4` (a door head's stairs and its fill cut from two
materials), `HS1` × 4 (a slab-banded window whose block is a glass pane, not a slab), `HS3` × 2 (a bare
log as a roof verge, which stands every log on end). Every one names the field and the fix. **The preview
is a picture, not a gate**, and the gate is at the store — which is early and cheap, but it is not where
the brief's "look at a house in section before building a world" implies it is.

**I wrote a `plan: 1` document out of habit** and the evaluator's `STRUCT` finding named both units:
*"this plan states version 1; this build reads version 2 — marker offsets are blocks from the piece
corner, and version 1 stated them in cells."* Two committed specs in `specs/` still say `1`; they are
dated evidence, as the skill says.

---

## What worked first time

- **The clamp.** Five strips drawn side by side across the box — west platform, west track, island, east
  track, east platform — each at its own height, with the uncut street either side of them as the box
  wall. No `SK9`, no `SK13`, no subtract anywhere on the board.
- **`kind: "made"` and `part_of`.** Six made layers — four slices of a standing train, two of the
  platform canopies on their posts — and neither `SK10`'s pair walk nor `SK11`'s reachability walk said
  a word about any of them. `SCULPTING-WITH-LAYERS.md` §6 proposed both as "what could become a tool";
  they are in the schema and they work.
- **`SK20` silent.** Ten layers ordered ascending by `base_y` including the made ones, which is what both
  the document rule and the painter's bottom-up rule want, and `addLayers` needed no `below`.
- **Every goal band on the first plan that stated `plan: 2`.** `GO1` 3.07 / 3.42, `GO4` 55 / 52, `GO2`
  38, `GO3` 127 / 123 / 142, `CT12` 32. The arithmetic was done before a shape existed: doors 212 apart,
  goals 47–53 along the lane, and the second goal placed by sweeping `POST /plan/inspect` over twenty
  candidate positions — twenty calls, no build, and the band that actually bound was `GO3` on the two
  *high* goals, which pushed the viaduct monument in toward the axis rather than out to the flank.
- **The rectangle-minus-holes routine.** `carve(outer, holes)` written once, used for the lid, the
  concourse slab, the two parapets and the lamp panels; 61 shapes on the ground layer and 34 on the
  concourse, none of them written by hand.
- **`POST /plan/compile` as a units oracle.** One call before anything was stored answered three
  questions at once: that `layer` reaches the intent, that the compiler emits **one** merged polygon and
  **no subtract** for a flat plan whose pieces tile (so `SK13` was never in play), and — from the orbit
  image of a marker at `(-16, 56)` coming back at `(15, -57)` — that `rot_180` maps a block column `c`
  to `-1-c`. That last one is the reason every x-rect on this board is `[-a, a)`: a half-open span is
  its own image only where `min = -max`, and the first cross-section I drew, `[-20, 21)`, would have
  built the two stations one column out of line with each other.

---

## Open gameplay questions

Three, decided without an oracle, built, and recorded here rather than filed as facts.

**Is the inside of a station a corridor the brief rules out?** `AUTHORING-BRIEF.md` §3 says the two
teams' ground is joined by a build zone over void and never by a land connection. This board obeys it at
every height — the chasm is full-depth void, the platforms stop at the tunnel mouths, and the two
viaducts are stubs that do not meet. But the *inside* of each half's station is a 42-block enclosed hall
an attacker walks end to end with two stairs and three light wells as its only doors, and that is a place
a defender stands. I built it because a station with a chasm through it is not a station. A match decides
whether the wells give an attacker enough ways in.

**Is a twelve-block pillar a route?** The free way onto the viaduct is the ramp, 149 blocks; the fast way
is thirteen placed blocks straight up off the street, 53. `aim=travel` takes the pillar and `aim=reach`
takes the ramp, which is exactly the decision the deck is meant to pose. A board that wanted the ramp
contested would put the deck at twenty blocks and lose the headroom under it.

**Is a one-way drop a route?** The light well over the deep monument falls 21 blocks straight onto it —
nine hearts, and the stairs are the only way back. `aim=reach` prefers it to the stairs, because the walk
prices a fall at nothing. `opus5-interchange` asked the same question about its two light wells and kept
them; so did I, for the same reason: a shortcut that costs health and commitment is a real decision.

---

## Rebuilding it

```bash
python3 specs/opus5-tiefkreuz/build-spec.py
python3 tools/drive.py specs/opus5-tiefkreuz "Tiefkreuz" \
        --out maps/opus5-tiefkreuz --renders specs/opus5-tiefkreuz/renders
```

The one ordering that is not obvious: the box is cut into the **compiled ground layer** as override adds,
and the concourse, the street lid and the viaduct are **layers over it**, ordered ascending by `base_y`.
Swap either — make the box a layer, or the lid an override add — and the station is solid rock.
