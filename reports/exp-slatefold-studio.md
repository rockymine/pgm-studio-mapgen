# exp-slatefold-studio — Slatefold, capture the wool, authored through pgm-studio's HTTP API

Builder: Sonnet 5.5, driving the local studio at `http://localhost:7894/api` (signed in as the local admin; the deployed
studio was not touched). Experiment pair: this board and `freeform/lib/boards/exp-slatefold-pgmvox`, same brief, same
lessons. Spec: `specs/exp-slatefold-studio/build-spec.py` (writes the plan and the refinement; `tools/drive.py` stores
them). World: `maps/exp-slatefold-studio/`. Renders: `specs/exp-slatefold-studio/renders/`.

## What I set out to build

**Slatefold: a slate-quarrying hamlet on two terraced hillsides that face each other across 32 blocks of void, for two
teams of twelve, two wools a team.** Each side is one hillside in three terraces — a quarry yard at y14 nearest the void,
a cottage terrace at y22, an upper terrace at y30 with the spawn hall — and, east of them, a grown hillside that a
switchback cart track climbs to a high bench at y40. The kiln house is the wool at the quarry floor; the winding house
is the wool on the bench, reached by the track and by nothing else on foot. The middle is crossed by building, from a
landing pier on each shore that stands between two lamp-topped posts.

Grey slate and stone in the ground, timber and brick in the buildings, grass and moss on the benches. About 208 blocks
between the spawns (z −104 and +104), 96 wide. Biome Extreme hills.

Tone families, named before painting: **ground** is grass over dirt on the flat and slate (stone, andesite, polished
andesite, a little cobblestone) from 50 degrees; **built** is red brick with timber and stone-brick trim; the **accent**
is the moss (mossy cobblestone inside grass) and the one pool of water.

## Self-review, written before the final build (01:10–01:12)

I read the plan, the relief and the report of the fifth store against the brief and the twelve lessons, and changed four
things. Each change is a store (`change` 11 to 20 on the slug).

1. **The winding wool was 28 blocks from its own spawn and 212 from the attacker** (`GET /map/{slug}/plan/flow`, ratio
   0.13), because the upper terrace ran straight into the bench. That is a fortress rather than a path of its own. I cut
   the ramp between the upper terrace and the bench and put a 10-block face on the line x=16, z −112…−86 (mark
   `s-upper-bench`, bench raised from 34 to 40), so the bench is reached by the switchback and the track only. After it
   the spawn-to-wool walk is 43 blocks through a face (14 placed) and 65 blocks along the track (0 placed).
2. **The two wool rooms were the same 14×14 brick block.** The studio binds one shell per kind of room and cannot give two
   rooms two styles, so I made the footprints differ (kiln 14×14, winding house 10×10, a tower by proportion) and put a
   made thing beside each: two bottle kilns and a stack by the kiln, a timber headframe by the winding house.
3. **Dead ground.** The coverage read put 976 cells at (−36, −96) on the upper-west terrace. I gave it a reason to be
   walked: a slate-dressing shed (`hall`), a pool (`tarn`) and a path to both (`road-tarn`). Dead share 9.7% → 6.5%.
4. **The terrace banks were 8 high over 8 across: 45 degrees of grass and dirt in stripes.** They read as ploughed
   fields, not as quarried terraces. I narrowed the faces to 4 across (63 degrees), which the slope axis paints slate and
   which transects as scrambles (steps of 2), not barriers. The ramps (`ramp-yard-mid`, `ramp-mid-upper-w/-e`) are the
   walkable ways up.

Not changed: a defence wall (see below), and the plan-tier `EL1`/`WL11` complaints, which walk the plan's pieces flat and
cannot see the relief that grades the terraces (transects read `worst step 1` on every ramp).

## What the board turned out to be

Three numbers, as the driver prints them after the last store: **ground 16486 walked, 1780 scrambled, 252 barrier (the
scrambles are the 63-degree banks, the barriers are the bench face and the track's turns); props 40 placed, 0
declined; routes worst step 9 on route spawn-0 to wool-1 (the straight line through the bench face, which the track
avoids).** Pre-flight: `export gate OPEN`; coverage 6.5% dead; editability finds no unreachable-but-standing ground
(`findings []`).

| What | Where (team 0, north; the south is the rot_180 image `(x,z) → (−x,−z)`) |
|---|---|
| Spawn hall (red) | pad (0, 30, −104), hall x −9…11, z −111…−96, door south onto the upper terrace |
| Wool, kiln house | pad (−38, 13, −38) — red wool, captured by blue; 14×14 brick hall in the quarry-yard corner, two doors (east and south) |
| Wool, winding house | pad (38, 39, −93) — orange wool; 10×10 brick tower on the bench, doors west and south, headframe at x 34…40, z −110…−104 |
| Quarry pit | floor y8 at x −14…8, z −38…−24, painted as quarry floor; the yard around it is y14 |
| Spoil tips | `tip-1` (−26, −22), `tip-2` (20, −42), `tip-3` (38, −44) — raised 4–6, painted bare slate |
| Cart road | pier (0, −13) → (13, −26) → (8, −44) → ramp at x=−4 to the cottage terrace; branch to the kiln door at (−27, −40) |
| Cottage terrace | `cot-1` x −39…−31, `cot-2` x −22…−12, minehead x −8…4, all z −71…−65, lane z=−62 |
| Sheds, bottle kilns | `shed-1` x 26…38, z −34…−26; bottle kilns at (−43, −22) and (−35, −21) |
| Upper-west | dressing hall x −47…−37, z −111…−103; tarn at (−36, −94) |
| Switchback | `road-track` through (44,−52) (22,−52) (22,−66) (44,−66) (44,−80) (22,−80) (22,−88); y14 → y40 over 26 blocks of rise |
| Crossing | pier x −4…4, z −17…−11 on each shore; posts at x −42…−40 and 40…42, z −19…−17, 7 high, lamp on top |

Places a player goes to, and why (team 0's half): the quarry pit (the fighting floor in front of the kiln, with the tips
as cover), the kiln and its bottle kilns, the cart road (the one flat way from the pier to the terraces), the cottage
row and minehead (a firing gallery over the yard), the sheds (cover at the east front), the switchback (the long climb to
the winding house, shot at from the terrace above it), the winding house and headframe, the tarn and dressing hall (the
upper terrace's back yard, behind the spawn), the spoil tips. Nine.

## Where the studio answered, in numbers

* **Terraces**: every ramp walks end to end — transect `-4,-42;-4,-62` rises 9, worst step 1; `-27,-76;-27,-96` rises 8,
  worst 1; `6,-76;6,-96` rises 8, worst 1; the whole switchback `44,-50 … 22,-90` rises 26, worst step 1,
  `walked end to end`.
* **Walks** (`GET …/walk`, no team, aim travel): spawn → kiln 82 blocks, 0 placed; spawn → winding 43 blocks, 14 placed
  (through the face), but 65 blocks and 0 placed along the track from (44, −44) to (33, −98). An attacker from the other
  spawn reaches the kiln in 158 blocks (32 placed, the bridge) and the winding house in 213 (35 placed).
* **Ground by angle** (`incline`): 59.6% under 10°, 12.7% 10–19°, 7.3% 20–29°, 7.4% 30–39°, 4.5% 40–49°, 6.4% 50–59°,
  1.9% 60–69°. 13% at 40° or steeper, which is the slate.
* **Themes** (`themes/census`): hill 86.5%, quarry floor 8.5%, spoil 2.7%, moss 2.3%; 17 distinct surface blocks.
* **Build ceiling** the studio derived: `maxbuildheight` 43 (mean ground + 20). The goal markers hang at y48.

## What worked first time

* One `PUT /map/{slug}/source` per pass, ten seconds a pass with the world exported; the dry run's edit list is how I saw
  what a pass changed. 20 stores in about 14 minutes by the wall clock.
* `relief`: `area` marks for the terraces, `scarp` for the banks, `line` marks with `tread` for the ramps and the
  switchback, with no seams: `RL3` fired only where I put the 10-block bench face on purpose.
* The slope axis in the `hill` theme: grass to 32°, a thin dirt shoulder to 40°, slate beyond. The terraces read as
  quarried the moment the faces were narrowed.
* Rooms: `roomStyles` bound `brick-townhouse` (wool) and `spruce-roofed-stone-longhouse` (spawn) from the library by name;
  the four chests a corner and the doors came out as the lesson asks (column `-44,-44`: two stacked chests at y14 and y15).
* The dressing pass's own rules (`DR-PASS`, `DR-KEEP`, `DR-CLAIM`, `DR-ROAD`) said where a house or a tree could not
  stand; `loop.py --candidates` answered five placements in one pass.

## What I got wrong

* I read `face` on a `scarp` as the slope's run and set 8 across for an 8 drop. That is 45 degrees and a slope painted in
  stripes of dirt and grass. The faces I wanted were 4 across.
* A made thing is one span a column per layer: a post and the beam on its top written as two shapes on one layer both
  stored at 200 and `SK9` declined the overlap. Every part of the headframe is a layer of its own.
* `scarp` direction: the shelf is on the +z hand of the travel direction, so a line drawn west to east puts the high side
  south; I drew every bank east to west.

## Open gameplay questions decided without an oracle

1. **Is a wool 43 blocks from its own spawn a fortress or a path of its own?** I judged the first and cut the ramp
   (self-review item 1). The defenders still reach it in 65 blocks by the track; an attacker needs 213.
2. **Are the terrace banks walls or slopes?** I let them be scrambles (2 per block): a rush is slowed, nobody is stopped.
3. **Should the kiln wool, the near one, be the first to fall?** It is 158 blocks and one bridge from the enemy spawn
   against 213 for the winding house; I left that asymmetry in (match-flow §4.8: the first wool falls, the defence shifts).

---

## 1. Times (`date`, UTC, 2026-10-10)

| Phase | Start | End |
|---|---|---|
| Reading (BRIEFS, ORDER-OF-WORK, WHAT-A-BOARD-IS-MADE-OF, AUTHORING-BRIEF, pgm-board skill, approaches, match-flow §4/§6/§10, cards) | 00:55 | 01:00 |
| Plan and relief written, first store, first look | 01:00 | 01:05 |
| Sketch and dressing iterations (stores 2–10: made things, pier, moss, sheds, houses cleared of declines) | 01:05 | 01:11 |
| Self-review and the changes it caused (stores 11–19) | 01:11 | 01:16 |
| Retaining-wall faces (store 20), final world, renders | 01:16 | 01:18 |
| Report | 01:18 | — |

Stores: **20** (`GET /map/exp-slatefold-studio/changes`), every one a whole-source `PUT`.

## 2. What the brief asked for that the studio could not express, and what I did instead

| The brief asked for | What the studio does | What I did |
|---|---|---|
| A kiln house and a winding house or watchtower as two different wool buildings | **Missing.** A map binds one wool shell and one spawn shell (`structures.md` §9: "there is no per-room override"), so every wool room is the same style | Different footprints (14×14 against 10×10) and made things beside each: bottle kilns and a stack by the kiln, a timber headframe by the winding house |
| A kiln that is built of red brick and a cart track with rails | Walls come from a style (brick is in the library); there is **no rail, fence-post or prop stamper** — the seven dressing props are stroke, fluid, flora, house, tree, boulder, chest | The cart track is a paved `stroke`; the kiln is brick by the wool style |
| Slate: a bedded, dark rock | Strata exist as a `height`-axis layered material with `follow`; there is no slate block in 1.8, so slate is stone, andesite and polished andesite in beds | `strata()` in the theme's wall and fill, and the rock band of the slope stack |
| Terraces with retaining walls and stairs | Terraces are relief marks and scarps; a wall is the face of a scarp, a stair is a tilted polygon with `anchor_heights`. **No wall-as-prop** | 63-degree scarp faces painted slate by the slope axis; ramps as `line` marks with `tread`; no authored flights |
| A visible build zone | The zone is a rectangle in the intent; the only mark the studio writes is an unpowered redstone line at y=1, two blocks out from the void edge, which no player sees from the ground | A landing pier on each shore (ground out over the void, quarry floor paint) and two lamp-topped posts at each end of the zone, as made-thing layers |
| Defence walls with chests in the front face | **Present but not usable here.** A plan wall needs a seam of 10–20 blocks between two ground pieces at 10–20 blocks from the room's entrance (`ST8`, `ST11`); the kiln sits at a corner of a wide yard and the winding house on a 12-block bench strip with a 4-block margin | None. The wool rooms stand without a wall; the corner chests are the studio's own (lesson 3's first half) |
| A pit with water or a flooded quarry on the east hill | A fluid pool needs level ground; between the switchback's passes the ground is a bank | A pool on the flat upper-west terrace instead |
| Moss on the benches | Only mossy cobblestone as a block; I painted it as three patches inside grass on shapes of their own (`theme: moss`), 2.3% of the ground | As said |
| Different heights of one team's two halves of the board | Not asked, but worth saying: rot_180 gives the south hill the same terraces turned, so the two hillsides are one design | Accepted |

## 3. The twelve lessons, one by one

| # | Lesson | Met? | Evidence and coordinates |
|---|---|---|---|
| 1 | An objective is found without a map | **Met** | Wool pads (−38, 13, −38) and (38, 39, −93), and their images (38, 13, 38) and (−38, 39, 93). Each is in a 10–14 block building standing in the open, a sky marker (a 3×3×3 wool cube at y48) hangs over each, and defenders stand round them on the yard and the bench. Neither is underground or on a tower top |
| 2 | An objective is made of what the mode needs | **Met, trivially** | Capture the wool: the pad is wool in the room's colour, the monument a bedrock pedestal with a stained-glass cap in the capturing team's spawn |
| 3 | A wool room holds the standard loot; a wall's chests are in its front face | **Half met** | Chests: column `-44,-44` reads two chests, y14 and y15, in the kiln's north-west interior corner; the other three corners likewise (`renders/column-kiln-corners.txt`). **No defence wall**, so no front-face chests; see §2 |
| 4 | Vegetation leaves the floor visible | **Met** | 4 trees a side (spruce at (−45,−90), birch at (20,−108), spruce at (46,−34), birch at (42,−22)), none within 3 blocks of a road (`DR-ROAD`), none on the pier, in the pit or on a lane; ground cover `coverage` 0.22 with `tallShare` 0.04, so two-block grass is 1% of the ground |
| 5 | Every stair is attached and walkable | **Met by having none** | No stair is authored. The ramps are full-block slopes, each transected: `-4,-42;-4,-62` worst step 1; `-27,-76;-27,-96` worst 1; `6,-76;6,-96` worst 1; the switchback worst 1. The bench face (x 15…18, z −112…−86, 10 high) is a wall by intent, not a stair |
| 6 | A spawn's exit is open | **Met** | Hall x −9…11, z −111…−96, door south, 8 blocks of level ground ahead (z −96…−88) and then the ramp at x=6 and the bank, no step greater than 1 (transect `6,-76;6,-96`); route spawn → kiln 82 blocks with 0 placed; the spawn keep-out holds the door's approach clear of trees and boulders (`claims` digit 7 and 8) |
| 7 | A floating platform cannot be mined away | **Met** | There is none: both hillsides are solid to bedrock (column `-44,-44` bedrock at y0), and the piers are ground, 14 thick, on the same slab |
| 8 | Ladders only where needed, never in water | **Met** | The only ladders are the studio's inside the multi-storey buildings; the pool at (−36, −94) has no ladder in or by it |
| 9 | Every join is open | **Met, nothing to join** | No shaft, tunnel or well on this board. The ramps and the track were each walked end to end by a transect |
| 10 | Things are at a player's scale | **Met** | Cottages 8×6 to 12×6, the wool halls 14×14 and 10×10 with 1-block walls, headframe posts 2×2, bottle kilns r3.5, stack 3×3, pier 8 wide; nothing is a speck, nothing a field |
| 11 | Ground varies in patches; edges and undersides carry detail | **Met** | Worn quarry floor (1568 cells), spoil tips (508), moss patches (420) are shapes with a theme of their own, not noise; the coast cliffs and banks are strata beds that follow the land (`strata()`), the rim off on relief ground |
| 12 | A build zone shows where to build | **Met, with made things** | Pier x −4…4, z −17…−11 on both shores, a paved road ending on it, and a dark-oak post with a glowstone lamp at x −42…−40 and 40…42, z −19…−17 (y7 lamp), which bracket the zone's x −40…40; seen in `renders/eye-buildzone-posts.png`. The studio's own marker, a redstone line at y=1, is visible in that picture far below and is not what a player steers by |

## Files

* `specs/exp-slatefold-studio/`: `build-spec.py`, `exp-slatefold-studio.plan.json`, `…refinement.json`, the stored `…layout.json`
  and `…intent.json`, `provenance.json`, `exp-slatefold-studio.png` (the board from its long side), `renders/`.
* `maps/exp-slatefold-studio/`: `region/`, `level.dat`, `map.xml`, `map.png`.
* `renders/`: isometric from all four corners, top-down combined and ground, heightmap, surface, traversability, the
  x-ray, and eye views of both wool rooms of each team, the spawn, the crossing, the pit and the build-zone posts.
