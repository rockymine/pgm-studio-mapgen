# Opus 5 — Mootgate: a dense walled town, and what a placement can say about it

## What I set out to build

A walled market town on each side of a void crossing, where the buildings *are* the board: a gate, a
street plan a player can read, many buildings of several house styles packed close enough that the
dressing pass has to be argued with, an objective inside a building a player goes into, streets as
routes with the standoff that implies, and a market square that reads as a place. Flat ground on
purpose — everything a player sees inside the walls is a placed thing.

Announced before authoring: **Capture the Wool, two teams, `rot_180`, 80 × 180 blocks, 24 a side.**
Each team's wool sits in the moot hall at the back of its own town; the enemy must cross 28 blocks of
void, come through one of three gates, cross the market square and the Moot Green, and break in.

What shipped: `maps/opus5-mootgate/`, `specs/opus5-mootgate/`, `review/opus5-mootgate.md`.
18 house props a side over five house styles, plus two stamped rooms over two more; 26 authored
terrain shapes; three themes; four routes; 16 trees, 7 boulders, 1 pool and 2 flora overlays a side.

**The three numbers.** `03-slopes.txt`: 9,836 walked, 106 scrambled, 2,218 barrier; 10 faces, largest
808 at x −37..36, z −89..−29 — the two town walls, which is what the barrier count is *for*.
`06-claims.txt`: **placed 93, declined 0**. `04-routes.txt` (taken by hand): the raid costs 154 blocks
and 43 placed straight over the void and the wall, or 177–220 blocks and 20–21 placed round to a gate.
Coverage 6.7% dead. `preflight` — export gate OPEN.

## What the surface let me say, and what it did not

**An objective inside a building I place: no mechanism.** I wanted a destroyable standing inside a
house. `OB19` declines a *tree, boulder or building* that stands inside a goal's clearance — 10 blocks
of the marker, plus the structure grown by four — so a house drawn over a goal is not in the world and
the goal stands in the open. I checked `openapi.json`: `HouseProp` carries `id`, `layer`, `seed`,
`placementOrder`, `wings`, `front`, `style` and nothing else; `DestroyablePlacement` and
`CorePlacement` carry `piece`, `at`, `layer`, `style`, `materials`, `float`, `name` and no reference
to a prop. Nothing ties a goal to a placed building. **Verdict: missing.** What exists instead is the
room stamper — a `wool-room` piece whose shell is a full `HouseStyle` bound at `layout.roomStyles.cage`
— and that is a genuine "objective in a room", which is why the board became a wool board. Cost of the
detour: one design decision, and the loss of `04-routes.txt` (the driver writes none on a wool board).

**The capture point: three documented write paths, none of which reaches the world.** I built a wool
stone on the market square at x 7..9, z 47..49, top y15, so the wool would be carried to the cross.
`POST /map/opus5-mootgate/wools/red/monuments` with `{"team":"blue-team","location":{"x":-8,"y":16,"z":-48}}`
answered 200 and `GET /map/opus5-mootgate` reads the monument back. `PUT /map/opus5-mootgate/intent`
with `wools[].monuments` answered 200 and reads back. `GET .../xml` still writes
`<block id="red-blue-monument">-20,16,-80</block>` and `<wool … monument="red-blue-monument"/>` —
(−20, 16, −80) is inside blue's spawn room (x −30..−18, z −81..−73). Two endpoints, one GET+PUT round
trip, ~15 lines, and nothing moved. `openapi.json` describes `MonumentIntent.location` as "The block
the wool is placed on" and `MonumentWriteRequest.location` as "Where the wool is placed, in block
coordinates"; both read as authoritative. **Verdict: unreachable** — the mechanism is stated in three
places and no path carries it to `map.xml`. The board ships with the derived monument, which is a
working, conventional capture point, so this cost appearance rather than playability.

**A paved street to the moot hall's door: refused, by design.** `DR-KEEP` keeps a 10-block lane clear
off every face of a wool room (20 off a spawn's door face), and a `stroke` is a prop, so a `route`
laid there is declined whole. What I did instead: the avenue is a one-course `add` rectangle carrying
the `cobbles` theme (`sq-moot`, x −31..−15, z 61..73) — one shape instead of one stroke, same picture.
The asymmetry is worth stating: **paint and paving draw the same thing and obey different law.** A
painted avenue is not a route, so trees and boulders keep no standoff from it and I had to keep them
off it by reading `06-claims.txt` instead.

**A terrace: not sayable as separate houses.** Two placements need **four** blocks between footprints
— the roof `overhang` on each (1) plus a block of structure clearance each. Measured: `h-stall-a`
x −10..−5 and `h-stall-b` x −2..3, a two-block gap, declined `DR-CLAIM building 'h-stall-b' stands on
(-3, 51), claimed by the building 'h-stall-a'`; at four blocks both stand. One building may be an L, a
T or a U through `wings`, but `HJ3`/`HJ4` force the two ridges apart and the wing total is capped, so a
row of five 7×6 houses is not one placement either. **Verdict: missing** for a party wall; reachable
as one multi-wing building for two or three bays.

**Street furniture below 5×5: not a prop kind.** `PlacedProp`'s discriminator has exactly six:
`stroke`, `water`, `tree`, `boulder`, `flora`, `house`. `DR-SIZE` floors a building at 5×5 and `HP2`
floors a *wing* at 4×4 — I met that one head on: `HP2 building 'h-inn' makes no building: a wing holds
two walls and an inside, so it is at least 4 blocks each way; this one is 3 × 8`. So a bench, a cart,
a fence, a lamp are all authored as terrain. Mine are: the market cross (4 rectangles), the wool
stone, the town well (a 4-rectangle ring round one open column), two gate towers, two stair flights —
20 of the 26 authored shapes. **Verdict: missing** as a prop kind, and cheap as terrain, because of
one thing I did not expect: **`keepClear` makes an authored shape a real dressing keep-out with no
margin.** `b-berm-e rests on (35, 32), which is kept clear for a stated structure` is a boulder
declined for leaning on the town wall. `GENERATION-NOTES` warns that "a standing stone is terrain, so
`DR-CLAIM` cannot see it" and that a footprint must be tested by hand; with `keepClear` set it does not.

**A `GET` the rule text names does not exist.** `HS1`'s `fix` reads "GET /api/house-parts lists what
each one accepts". `/api/house-parts` answers **404** and is not among `openapi.json`'s 161 paths.
**Verdict: missing** (the route). I read the block-kind requirements off the shipped presets'
`/room-styles/{id}/json` instead, which worked.

**A room's building *is* separable from its piece.** `GENERATION-NOTES` says "A room's building is
sized by its piece, and by nothing else … there is no field that separates the two". That is stale.
`WoolPlacement.footprint` and `SpawnPlacement.footprint` take "[x, z, w, h] in blocks from the piece's
minimum corner"; `WX12` refuses one that reaches outside its piece; `ST9` says the cap is on "the
rectangle the export actually stamps: the one the placement states, or the one `WX1` defaults from".
I stated `[3, 3, 12, 8]` on an 18 × 14 piece and `POST /plan/inspect` answered
`wool-cage minX -29 minZ 73 maxX -17 maxZ 81` before a map row existed. **Verdict on the note:
mistaken** — it exists, it is documented, and the note says otherwise.

**The recipe registry is real and it is what the schema documents.** `DressingDoc.styles` takes
`{"kind":"house","shell":{…HouseStyle…}}`, `{"kind":"tree",…}` and `{"kind":"boulder",…}` under
author-chosen keys, and each placement names a key. Five shells carried eighteen buildings, stored and
built at 200 with no `RQ3`. This repo's `@name` convention in `tools/styles/` inlines a resolved shell
per placement instead, which is eighteen copies of a sixty-line document. Repainting every croft on
the board was one edit.

**What I could not narrow: `WX11` beside a made shape.** Build 3 raised
`WX11 house h-south-d 0 stands 7 blocks above the cell beside it at (11, 33)`. `column?at=11,33` reads
Grass Block at y14 and `column?at=11,34` reads the house's own Cobblestone plate at y14 — the drop is
0, and there is no bedrock face in the world there. Both houses that raised it (`h-south-b` x −17..−11
and `h-south-d` x 11..17) had a footprint column shared with or one block from a stair-flight polygon
whose top is y21–22 there, which is exactly 7 above y14. Moving each two blocks clear of the flight
silenced it. I have not read the code, so this is an observation with coordinates rather than a filed
defect: **`WX11`'s height looks like it is read off the neighbouring made shape rather than off the
terrain.**

## How I edited the layout while iterating

**Whole documents, every time, regenerated from one program.** `specs/opus5-mootgate/build-spec.py`
writes `<slug>.plan.json` and `<slug>.finish.json`; every change was a change to that Python and a
re-run. The plan is 8 pieces; the finish is 26 shapes, 3 themes, 4 relief marks, 10 recipes, 48
placements and 7 house styles, and all of it is re-posted on every pass. I never patched a stored
document.

The reason is the driver's contract, not laziness. `POST /map/from-documents` **replaces** the map at
the slug, so any per-object edit made against the stored map is discarded by the next drive. The spec
is the source and the map is derived; editing the map would have split the truth between two places.

**The per-object surface exists and I deliberately did not use it**: `POST`, `PATCH` and `DELETE` on
`/map/{slug}/sketch/props/{propId}`, `PATCH /map/{slug}/sketch/shapes/{shapeId}`,
`PUT /map/{slug}/sketch/themes/{themeId}`, `PUT /map/{slug}/sketch/room-styles/{part}`. Those are what
a canvas drives. For an agent whose authored truth is a file, they are a second store to keep in sync.

**What made whole-document re-posting cheap was `tools/loop.py`.** It compiles the plan, patches it
with the finish and posts the result to `sketch/relief/read` and `sketch/dressing` without storing
anything — twenty seconds against a six-minute drive. The dressing preview prints every decline with
its rule and its coordinates, so the placement loop was: edit the Python, run `loop.py`, read the
declines, edit again. Six passes took the board from **12 declines to 0** and cost one build.
`--candidates` answered eight trial positions for one prop in a single pass twice; six of eight worked
the second time, which is where four of the trees came from.

The one thing I changed *against the stored map* was the monument, through
`POST /wools/{id}/monuments` — and that is the one change the world did not take.

## What worked first time

- **All seven house styles previewed at 200 in section**, with no `HS` finding, from the shipped
  presets' own JSON shape. `POST /room-styles/preview-snapshot?format=png&view=section&scale=8` is the
  read; the default card at scale 1 is 60 px and unreadable, `scale=8` is legible.
- **The town wall.** Seven rectangles at `override: true`, `height_mode: "level"`, `skirt: 0`,
  `relief_scope: "exclude"`, `keepClear: true`, `base_height: 23`: right height, sheer face, dressing
  keep-out, first build. `column?at=-34,32` reads eight courses of stone brick over cobble fill.
- **The stair flights as single tilted quads**, 16 run for 7 rise, `anchor_heights` [23,23,16,16].
- **The paint-patch form** — `add`, `base_height: 1`, no override — for the square and the yards.
  `column?at=0,36` reads gravel at y14, the town's own level: it never lowered what it was laid on.
- **`footprint` on both room placements**, and `POST /plan/inspect`'s `structures` answering the
  stamped rects before a map row existed.
- **The `styles` registry** in the dressing document.

## What I got wrong

1. **My first L was not an L.** Hall 9×10 and wing 9×5 sharing the same x-span is a 9×15 rectangle.
   `prop-preview`'s plan drew one rectangle and no rule fired, because I had stated the ridges apart
   so `HJ4` could not. Offsetting the wing to 5 wide made it an L. Then `HJ5` caught the second one:
   *the wing reaches no further along the shared edge than the hall reaches across it* — an 8-long
   wing on a 7-wide hall is refused, 7 on 7 stands.
2. **I sized the board for the town and not for the players.** 88 × 196 first, land/team 7,392 blocks;
   `G8`'s table tops out at 5,875 for 32 a side. Cut to 80 × 180, land/team 6,080, and even that is
   253 blocks per player at 24 a side against a ~184 saturation.
3. **I drew four buildings on top of a road and two on top of a pond.** `DR-CROSS × 2`,
   `DR-CLAIM × 2`, and all six were visible in the spec before the build. I did not look; the build
   told me.
4. **I assumed a wool room's door approach was a 21-wide ring** and designed a 32 × 28 dead zone
   round the hall on that basis. `06-claims.txt` says it is a rectangle off *each face, the width of
   the face* — 10 blocks for a wool room, 20 for a spawn's door face. Reading the raster gave back a
   quarter of the town's back half and is the single most useful read of the run.
5. **A rectangle is half-open.** `made("wall-w", -36, 29, -33, 88, …)` owns x −36..−34, and
   `column?at=-33,32` is grass. I had houses touching x=33 and x=−33 and they came back
   `DR-SLOPE … rises 8 block(s) across its own footprint` — the wall was inside the footprint.
6. **Four builds, not one.** Twelve declines, then five, then two `WX11`, then zero.

## Open gameplay questions

1. **`FR6` and the brief disagree, and both are `[author]`.** The brief rules that the two teams'
   ground is joined by "a build zone over void spanning the board's whole width"; `FR6` says a wool
   board's frontline is 6–8 cells and bands it [1, 16]. Mine is 40 cells and the evaluator scores it a
   soft violation of distance 3.2 (of a total 4.976, `valid: true`). I followed the brief, because a
   16-block front is the corridor the brief calls a defender's place, and because three gates only
   mean something if an attacker can choose which to walk to. Recorded, not filed.
2. **`G8`'s fill-ratio is unattainable for a slab board.** 0.844 against [0.201, 0.542].
   `opus5-kiln-row` reads 1.0 and `opus5-quatrefoil` 0.637, so every hand-authored board here is
   outside it. Nothing short of turning the board into an archipelago moves it.
3. **Four doors on a moot hall.** A wool room's entries are every land seam it presents, and it needs
   land on all four sides or its foundation fills that face with bedrock to y0. So a centrally-placed
   room is always open on four sides. I judged that right for a market hall on a green; a room a team
   wants to defend from inside cannot be authored, and a team is barred from its own room anyway.
4. **Where should a wool be carried to?** The exporter puts the monument in the capturing team's own
   spawn, which is safe. I wanted it on the market cross in the open square, so the carry ends
   somewhere contested. The board ships with the exporter's answer.
