# The Thunder series — read out of the worlds, rebuilt in the studio, and extended

Four maps: `thunder` (2014, v2.1.6), `thundershock` (v1.0.5) and `thunderstorm` (v1.1.3) from `PublicMaps/ctw`,
and `thunderbolt` (v1.0.4) from `CommunityMaps/ctw`. All four are rockymine's. The first three are four-team
`rot_90` boards and are rebuilt here; the fourth is six-team and is looked at only, because the studio's
symmetry vocabulary has no sixth-turn.

`pgm-studio` at `14fb4a653f164dfc9a884ec1baa1cf646cae34ab`, working tree clean, untouched.

---

## 1. What the series is, measured

Nothing below is read off a picture. The land comes from
`PgmStudio.RoundTrip --island-sketch <map>`, which walks the world's cleaned base, runs the island detector
over it, and pushes every island's outline through Douglas-Peucker (`IslandSimplifier`). The rectangles come
from each map's own `map.xml`. The rotation centre is the point the four spawns actually turn about.

| | thunder | thundershock | thunderstorm | thunderbolt |
|---|---|---|---|---|
| teams · wools | 4 · 12 | 4 · 12 | 4 · 12 | 6 · 30 |
| rotation centre | `0.5, 0.5` | `−55.5, −239.5` | `−48.5, 30.5` | sixth-turn |
| islands, whole board | **17** | **13** | **9** | 25 |
| islands per team | 4 | 3 | 2 | — |
| board | 239² | 279² | 231² | 235² |
| ground y · maxbuildheight | 7 · 25 | 13 · 18 | 10 · 22 | — |
| fill (ground ÷ board) | 0.193 | 0.177 | 0.323 | — |

**The island counts are the shape of the series.** A team does not own *an* island; it owns a handful, with
void between them, and the void is what the map is played across. Thunder gives each team four separate
islands and puts one small quad on the axis: 4 × 4 + 1 = 17.

**A Thunder island is a ribbon, not a set of rooms.** Eroding each main island layer by layer gives its width
directly:

| | area | vertices | compactness | ribbon width |
|---|---|---|---|---|
| thunder main | 1878 | 29 | 0.240 | 8 – 24 |
| thundershock main | 2967 | 33 | 0.236 | 10 – 28 |
| thunderstorm main | 3754 | 30 | 0.286 | 12 – 40 |
| **centre island, all three** | **85 – 113** | **4 – 5** | **0.79 – 0.82** | 4 – 16 |

A compactness of 0.24 is a band that wanders, not a body with limbs. The centre island of every one of the
three is a **near-square quad of about a hundred blocks** — four vertices, and that is the whole form.

**Each map's signature is what its ribbon does.** Thunder zig-zags — a lightning bolt, which is the name.
Thundershock hooks: out, round, and back to a spit. Thunderstorm spirals into a C and hides the wool room in
the crook. That is the design language, and it has no vocabulary in common with the generator's — **there is
no hub anywhere in the series, no crossbar, no lane grammar, no U frontline.** The route structure is which
island you can reach from where you are standing.

**One wool room per team, raided by the other three.** Twelve `<wool>` elements on each of the three: four
rooms, each a target for three teams. The studio reproduces this from a single wool marker on a
`wool-room` piece.

**A wool is isolated by water, never by bedrock.** Thunder hangs two further islands out past its wool tip;
Thundershock runs a narrow spit to it; Thunderstorm puts a chamfered chamber at the far end of a C. No map
in the series uses a wall.

## 2. How each was rebuilt

One path, four boards — `trace.py`, `plan_from_unit.py`, `reconstruct.py`.

**The plan is authored at one block per cell, not five.** The two rectangles the original *declares* — the
spawn-protect box and the wool room — have to land exactly where the XML puts them, and a five-block grid
cannot hold `min="-119,2" max="-105,19"`. So `globals.cell = 1` and the plan's rectangles are block
rectangles.

**The plan and the sketch describe the same ground in two languages, and only one of them is the shape.**
The plan states what a rectangle can state: the spawn, the wool room, a rectangle *cover* found inside each
traced island — largest inscribed rectangle, then the next largest, seeded from the two declared rects so the
component that survives is the one holding them — the build zones, and the maximum build height. It compiles
to the intent. Then the sketch **throws the compiler's rectangles away** and puts the traced polygons in
their place, keeping only the role shapes (the spawn rooms, the wool cages), because the shape of this land
is the entire point and a rectangle cover is not it.

**A light Bezier pass afterwards, and only light.** The traced polygon is already the right shape, so the
softening runs at amplitude 0.14 with the bulge capped at four blocks — a fraction of what an invented coast
gets — purely to take the Douglas-Peucker corners off. The corner rule holds: a handle runs along the edge it
leaves and never past its far end, and every polygon is checked for self-intersection rather than assumed.

**The one liberty taken.** Thunder turns about `(0.5, 0.5)`; a cell grid cannot hold a half block, so the
board is shifted by the rounded centre and every rotational image lands one block off true. Over 240 blocks
it is invisible, and it is the only coordinate that is not the original's.

## 3. What the studio said about a hand-built map

Running `POST /plan/evaluate` on a faithful transcription of a 2014 map is the useful part of this exercise,
because the generator's envelopes were fitted to a different corpus. Every one of the three fires:

| rule | thunder | thundershock | thunderstorm | band |
|---|---|---|---|---|
| `G8` fill-ratio | 0.145 | 0.153 | — | 0.201 – 0.496 |
| `LN1` lane-width | 2 | 6 | 6 | 10 – 20 |
| `WL10` wool-front-distance | 7 | 8 | 6 | 24 – 165 |
| `G5` gap-hop | 9 | — | 8 | 10 – 20 |

Two of these are the transcription's fault and two are the maps'. `LN1` and `WL10` read the **rectangle
cover**, which contains slivers no player will ever see — a cover is not a decomposition and the numbers it
produces are not the map's. `G8` and `G5` are real: the series is genuinely emptier than the generator's
fill band allows, and it genuinely hops eight or nine blocks where the band starts at ten. A void map at
0.15–0.19 fill is not a defective map; it is a kind of map the band does not describe.

## 4. Thunderhead — the next one

Authored in the series' language and nothing else's, by `author_unit.py`. An island is stated as **strokes**:
a centreline with a half-width at each point, swept at one block, carved along a value-noise field so the
coast is bays and headlands rather than offsets, its boundary walked, and the ring reduced by
Douglas-Peucker at the same tolerance the tracer uses. What comes out is a simplified polygon of the same
kind `--island-sketch` returns for a real map, and it goes down the identical path afterwards.

**Its signature is the fork.** Thunder zig-zags, Thundershock hooks, Thunderstorm spirals; Thunderhead's
ribbon leaves the spawn as one band, narrows to a nine-block waist at the middle of the island — the one
place a defender can stand and mean it — then splits into two prongs reaching for the centre quad. That is
the whole of its route structure: two ways at the mid, chosen forty blocks before you arrive, and no way to
swap once committed except back through the waist.

| | thunderhead | series |
|---|---|---|
| islands per team + axis | 3 + 1 | 2 – 4 + 1 |
| main island | 2007 blocks, 31v, compactness 0.352 | 1878 – 3754, 29 – 33v, 0.236 – 0.286 |
| centre quad | 104 blocks, 4v, 0.785 | 85 – 113, 4 – 5v, 0.79 – 0.82 |
| board | 248² | 231² – 279² |
| wools | 12 | 12 |
| wool isolated by | its own island, 17 blocks of void | island / spit / crook |

**The unit has to fit inside one ninety-degree sector.** Under `rot_90` a cell at `(x, z)` has an image at
`(z, −x)`, so anything the unit reaches outside its sector meets its own quarter-turn image. Two drafts of
this board collided — the second prong's image landed on the first prong, then on a fourth islet — and the
islet was cut rather than shrunk, which is why Thunderhead carries three islands and not four. The check
runs on the cells, not the bounding boxes, and it runs on every build:
`rot_90 self-collision: none`.

**Every building on all four boards is `desert brick`**, the seeded preset from `HousePresets.cs:166` — two
courses of end stone under five of sandstone, brick roof and verge, birch stair-lattice windows, birch arched
door head — fetched from the room-style library at build time rather than copied, so the house is the one the
code defines. It is also the right one: the material top-downs of the originals are sand and sandstone with
brick-roofed buildings, and the series is a desert.

## 5. Where I had to read the code rather than the API

- **`PlanCompiler.cs:118`** — a buffer becomes a subtract shape only after
  `RectilinearUnion.Difference(bufferRect, terrain)`, so a hole stated *inside* a single piece is clipped to
  nothing and silently dropped. A ring has to be drawn as bars with the hole between them. No error, no
  warning: the plan compiles and the hole is simply not there.
- **`HousePresets.cs:166`** — which preset the user's description named. `LibrarySeed` reports `desert brick`
  as one of the five that "round-trip whole"; five of the ten lose fields the room-style row has no column
  for.
- **`IslandSimplifier` / `RunIslandSketch`** — the whole reconstruction hangs on `--island-sketch`, which is
  documented nowhere I found from the outside; the flag list in `tools/PgmStudio.RoundTrip/Program.cs` is
  where it exists.

## 6. What I got wrong first, and what corrected it

**The first three reconstructions were drawn from the top-down renders.** I read the pictures, assembled
plan rectangles at five blocks per cell that looked like the arrangement, and built four boards that were
recognisably my own previous map with the furniture moved. Being told to use the tooling instead is what
produced everything above; the island detector had the real answer the entire time.

**The first Thunderhead had a double-hole hub and a U frontline.** Those are the *generator's* words, learned
from `docs/generator/model.md` and from the previous two maps in this repo. No map in the Thunder series
contains either, and importing them produced a board in the wrong dialect however organic its coastline was.
The series had to be measured before it could be extended.

**Two coasts closed a void hop.** The Bezier pass on an invented board spent more than the free space in
front of it and welded islands together — first across a wall, then across the anvil's moat, and the second
time the clearance test was blind to the *rotational images*, which are where the neighbour actually is. Both
are fixed in `reconstruct.py`, and the softening on the traced boards is deliberately small enough that
neither can happen.

## 7. Limits

- **Thunderbolt is not rebuilt.** Six teams need a sixth-turn and `Symmetry` has `rot_90` and `rot_180`.
- **The rectangle cover is not a decomposition**, so `LN1` and `WL10` report slivers rather than lanes on all
  four boards. A cover that merged its slivers, or an evaluator that read the sketch polygons instead of the
  plan rectangles, would fix both.
- **The reconstructions carry the originals' *shape*, not their contents.** No monuments, no team-coloured
  roads, no interiors, no `<variant>` — Thunder's Christmas worlds are not touched. The relief is flat
  because the originals are close to flat, and the dressing is one road, one house and a scrub patch per
  island, placed from the traced land rather than by hand.
