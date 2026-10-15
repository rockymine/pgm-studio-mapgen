# Frostholm — the plan

Written before any terrain existed. The sections after *As first drawn* record how the plan changed and why.

## The board in one sentence

**A frozen archipelago played corner to corner: each team's home island is a rocky crescent round a bay
of sea ice, its core burning in the lantern of a lighthouse off one horn and its monument on an islet in a
frozen lake on the other, and the teams meet across a lead of open water where three islands stand astride
it.**

What a player remembers: the lighthouse, the ship frozen in the bay, the lake held high with its waterfall
frozen mid-fall.

## Mode: one core and one monument a team

**A combined board, because the crescent has two horns.** The core goes in the lighthouse on the north-east
horn and the monument on the lake islet in the south-west horn: an east and a west, 40° and more off the
line to the enemy. Defending both splits a team across its own bay. The combined board is the ordinary one
in the corpus (`approaches.md`) and neither earlier freeform board tried it.

**The core is in a lantern, and its leak is designed.** It sits in the lighthouse's lantern room on a stone
floor ringed by a gallery. A breach spills lava onto the gallery, which drains through gaps in its parapet
down the tower's face, and that fall is the leak.

## Arrangement

- **Not a floating island.** The islands stand in a frozen sea over a seabed. The board's edge is a frame
  of pack ice heaved up from the seabed, so the world reads as a sea, not a slab in the sky.
- **Corner to corner, by a half-turn.** Red holds the north-west, blue the south-east, and blue's half is
  red's turned 180°. The halves meet along the diagonal `x + z = −1`.
- **The lead.** A strip of open water about ten blocks wide runs along the diagonal: the seam between the
  teams. It is crossed on three islands that stand astride it — Tingholm at the centre and Kraakholm twice,
  at the north-east and south-west — or by bridging and swimming anywhere else.
- **Sea ice everywhere else.** It is walkable and breakable, and pressure ridges heaved up across it are
  the only cover on the open ice. The water around each horn's tip stays open, so the core and the
  monument are both reached across water or by their one land approach.
- **Heights:** sea ice at 47, island shores at 48–50, Jarlshall at 64, the crags to about 80, Kaldvatn held
  at 57, the lantern's core at 82.

## The places (red half; blue's are their half-turn)

![plan sketch](renders/00-plan-sketch.png)

| Place | Where (x, z) | What it is | Why a player goes there | How |
|---|---|---|---|---|
| Jarlshall | −62, −62 | Spawn: a long hall of dark timber on a stone plinth, crags at its back | spawn | its two doors |
| Ulvefjell | −74, −74 | the crags in the corner, snow on their ledges | frames the spawn; lookout | a goat path |
| Ravnsodde | −18, −75 | the north-east horn: a rock ridge out to the Beacon | the way to the core | Ridge Path |
| **The Beacon** | 5, −79 | lighthouse on a sea stack; the core in its lantern | **red core** | its stair; the footbridge; a sea cave in the stack |
| Kaldvatn | −68, −24 | frozen lake high in the south-west horn, a frozen fall from its lip | **red monument** on the islet Holmstein | lake ice; the wood; the crag |
| Granskog | −74, −44 | pine and spruce between the hall and the lake | cover to the monument | Lake Path |
| Skarvik | −46, −46 | fishing village on the bay: boathouses, racks, stave church, smithy, longhouses | cover from the bay to the hall | Shore Road, the pier |
| The Whaler | −26, −36 | a three-master frozen into the bay ice | cover and height on the open bay | over the ice |
| Tingholm | 0, 0 | the centre island: standing stones, a cairn | the middle crossing of the lead | over the ice |
| Kraakholm | 36, −37 | rocky island astride the lead: ruined watchtower one side, sealers' hut the other | the crossing between red's core and blue's monument | over the ice, across the lead |
| Pressure ridges | across the ice | heaved ice | the only cover on the open ice | — |

## Navigation

- **The board is a ring.** Red's core horn faces Kraakholm, and Kraakholm faces blue's monument horn. Red's
  monument horn faces the south-west Kraakholm, which faces blue's core horn. The two bays face each other
  across Tingholm. Every fight at a flank island is one team's core against the other's monument.
- **Spawn to own objectives:** about 68 to the core, 40 to the monument.
- **Approaches to the Beacon:** along the ridge and over the footbridge (*through*); bridging from the
  ridge's high point onto the gallery (*above*); across the open water into the sea cave and up inside the
  stack (*below*); around by the ice to the stack's seaward side.
- **Approaches to Holmstein:** across the lake ice, exposed (and the ice can be broken under you); through
  Granskog to the north shore; down from the crag over the frozen fall.

## Palette, decided now

- **Biome:** Cold Taiga on land and Frozen Ocean on the sea, both tinting grass `#80b497`, so grass and snow
  agree.
- **Ground:** snow on the flats over grass and dirt; stone and andesite with cobblestone where it is steep;
  gravel scree under the crags.
- **Ice:** sea ice of ice blocks; pressure ridges and the frame of packed ice; the frozen fall of packed ice.
- **Built:** dark oak and spruce timber on cobblestone plinths, roofs of dark oak under snow; the Beacon in
  stone brick, whitewashed with diorite courses.
- **Trees:** pine and spruce, cut from rockymine's tree showcase.

## As first drawn

The table and sketch above are the plan as written before building.

## How the plan changed

**The first build was a frozen sea, and the author turned it down.** It was built as drawn: two crescents
round bays of sea ice, the islands small in a lot of white. The author's verdict was that it was too much ice
and not enough land, that the monument sat on a cylindrical island, and that the board should be set in the
winter, not in Antarctica. That version's plan and terrain are kept as `scripts/plan_v1_frozen_sea.py` and
`scripts/terrain_v1_frozen_sea.py`; the sketch above is still that first drawing.

**The second plan is land first.** Rolling snowfields cover most of the board, with rock outcrops standing out
of them, sea crags in the home corner and a lake in a hollow. Two narrow straits a side cut the land across
the line between the spawns: Ravnsund off each home island and Midsund, the lead between the teams, through the
middle. Each strait is frozen in stretches and open in others, so ice is a crossing, not the ground.

**The corners off the diagonal are cut away, as the author suggested mid-build.** The board is the band
`|x − z| < 116`, with a ragged edge, so the play runs corner to corner and nothing is wasted in the two empty
corners. A strip of sea runs round the whole outside, so every landmass is an island with a gravel shore
and the board does not read as a slab.

**The monument moved off its islet onto a knoll on the lake's shore.** Holmstein is now a rock knoll on
Kaldvatn's east shore, reached up its sides from the lake ice, the wood or the road. Kaldvatn itself is a small
frozen lake in a hollow, no longer held high behind a frozen fall.

**The village moved from the bay to the middle island, and the Beacon from a sea stack to a headland.**
Skarvik stands on the middle island over Midsund, with a landing stage onto Tingholm. The Beacon stands on
Ravnsodde, the headland over Ravnsund, on rock all the way under the tower after the first placement left its
east wall hanging over the strait.

**The Old Bridge moved south-west so the whaler fits between it and the Beacon.** On the diagonal, the whaler's
hull claims a string of small boxes along its keel rather than one bounding box. Even so, the stretch of
Ravnsund between the bridge and the Beacon was too short for it until the bridge moved twelve blocks along the
strait and the frozen stretches were moved to match.

### The places as built (red; blue's are the half-turn)

| Place | Where (x, z) | What it is |
|---|---|---|
| Jarlshall | −64, −64 | Red's spawn: a long dark-timber hall, doors east and west, banners at the east door |
| Ulvefjell | −80, −80 | Sea crags in the corner, behind the hall |
| The Beacon | −17, −67 | The lighthouse on Ravnsodde; **red core** in its lantern at y 75–77 |
| Kaldvatn | −70, −26 | A frozen lake in a hollow, two ice-fishing huts on it |
| Holmstein | −58, −20 | A rock knoll on the lake's shore, standing stones round its foot; **red monument** at y 62–63 |
| Granskog, Nordskog | −80, −44; −40, −78 | Pine and spruce woods: to the lake, and to the Beacon |
| The Old Bridge | −48…−29, −26 | A timber trestle over Ravnsund's open water |
| The Whaler | −25, −42 | A three-master frozen into Ravnsund's ice |
| Skarvik | −16, −14 | Stave church, longhouses, smithy, boathouse, drying racks, the landing stage |
| Tingholm | 0, 0 | The rock islet in Midsund, a ring of standing stones and a cairn, shared by both teams |
| Kraakodde | 38, −60 | The middle island's north-east point, a ruined watchtower |
| Sealers' Point | −60, 38 | The middle island's south-west point, a sealers' hut and racks |
