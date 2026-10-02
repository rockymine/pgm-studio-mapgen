# Sonnet 5.5 — Halcyon Cays, a tropical atoll resort driven through the kit

## What I set out to build

**A destroy board for two teams on a tropical atoll, where a resort and the wild cays around it meet along authored edges.** The map is `sonnet55-halcyon-cays`, named **Halcyon Cays**, stored on pgmstudio.de and exported to `maps/sonnet55-halcyon-cays/`. Every document is stated through `from studio_kit import kit` in `specs/sonnet55-halcyon-cays/build-spec.py`.

**The identity sentence, written before the first request.** *A holiday resort on a string of cays in a turquoise lagoon: a white hotel with a pool courtyard on one shore, thatched bungalows on a palm cay, towering rock stacks standing out of the water, and a thatched bar on the sandbar in the middle where the two resorts' routes meet.*

**The overridden ruling.** The middle is joined by terrain, not by a build zone over void: a dry sand spit, a shallow reef ford and an island hop each run across the axis, so the crossing has three ways over. The plan states no zone at all.

## The board

**A lagoon 100 blocks wide and 210 long with the monument 45 blocks of walk from its own spawn and 151 from the enemy's.** The ground runs x −50…49, z −105…104 for team 0 and its mirror (`mirror_z`, the image of block `z` is `−z−1`). The spawn pavilion stands at (0, −95) and the monument at (8, y16–18, −53), both read back from `map.xml` (`<cuboid id="red-monument-region" min="8,16,−53" max="9,19,−52"/>`). The walk read is `45 → 151`, a `GO1` ratio of 3.36, and the plan tier reads 47 and 142.

**The biome is Swampland, chosen because it is the only one that moves the water.** `GET /api/terrain/biomes` answers a water tint of `#ffffff` for every biome but Swampland and Swampland M, both `#e0ffae`. Multiplied into the water texture that reads as a blue-green, which is the nearest the studio has to a turquoise lagoon; Jungle's `#59c93c` grass would have been brighter and left the water the plain blue of the first render.

**The price is the vegetation.** Swampland tints grass and leaves `#6a7039`, so the palms and the lawn read olive and brown instead of holiday green, and the board carries its colour in sand, white quartz and teal roofs instead. I rendered both biomes and kept the teal water; it is a trade the author may want to reverse.

**Three tone families, named before the first theme.** The ground is pale sand and sandstone with olive grass patches; the built family is white quartz, jungle-plank teak and thatch; the accent is turquoise, which appears on every hotel and pavilion roof, the pool tile, the umbrellas, the cabana canopies and the lifeguard roof.

**Three themes, each a place.** `shore` is the map default and the whole of the lagoon floor, beaches and sandbars: sand and sandstone to 28°, sandstone to 46°, stone beyond, over a sandstone fill. `jungle` is the grass patches on the garden, the palm cay and two islets: grass over two dirt to 32°, dirt mix to 46°. `karst` is the rock stacks, in stone, andesite and diorite with cobblestone at 12%. The resort's made ground states a `material` on each shape instead of a fourth theme.

**The relief is one group, `team`, with 14 area marks and one push, stored 25 times on this map.** The lagoon floor is pinned at 7 and every cay is a pad that gives way to it by a bevel, so the pads are drawn a bevel wider than their dry core. Range is 7…15, relief 8, symmetry error 0, and the relief read raised no finding on the final store.

**The water is one basin over the whole lagoon at level 10.** A `basin` fills only the columns under the line and cuts nothing, so islands inside it stay dry and the sea reaches the board's rim, where it meets void. Column reads give water y7–10 over sand at y6 in the channels, a ford top at y9 under one block of water, beach at y11 and the monument's shore at y11.

### Points of interest

**Everything below is stated for team 0; team 1's is the image at z′ = −z−1.** Coordinates are blocks, `y` the top block a player stands on.

| Name | What it is | How it was built | Where (x, y, z) | Why here |
|---|---|---|---|---|
| **Hotel Cay** | The resort island, 56 × 36 blocks of beach | Area mark `hotel-cay` at h12 with bevel 7 | centre (−10, y11, −64) | The ground the whole fight is composed on |
| **The Spit** | A winding dry sand bar, 8 blocks wide, running to the axis | Corridor mark `spit` at h12, bevel 5, and a stone `path-spit` | (−2, −47) → (6, −38) → (−4, −21) → (1, −4), y11 | The fast, exposed crossing, one of three |
| **The East Reef** | A shallow ford 12 wide, one block of water over it | Corridor mark `east-reef` at h10, bevel 4 | (34, −58) → (32, −31) → (17, −9) → (7, −3), top y9 | The wading crossing, slower and under the Needle's eye |
| **Tern Islets I–III** | Three small cays with swim gaps between | Area marks at h12; I carries a jungle patch and a palm | (−38, −40), (−31, −23), (−20, −8), y11 | The island-hop crossing, with cover |
| **Reef Cay and Reef Islet** | Two cays on the reef | Area marks at h12; the cay has a jungle patch and a palm | (28, −27) and (21, −13), y11 | A place to stand on the ford |
| **Palm Cay** | A jungle cay with two thatched bungalows and two palms | Mark `palm-cay`, jungle patch, `FloraProp` lawn | centre (37, −70), crown y13 | The cabana end of the resort, 30 blocks from the monument |
| **Resort terrace** | A white made-ground plinth 2 above the beach | Shape `resort-terrace`, `relief_scope: exclude`, base 14, quartz paving as a `material` | x −40…−3, z −77…−52, top y13 | Made ground set into the grown beach; the meeting is a 2-block face |
| **Stair flight** | A 6-wide ramp from beach to terrace | One polygon, `height_mode: level`, `anchor_heights` 12/14, `skirt` 0 | x −26…−20, z −52…−47 | Where the terrace face opens |
| **The pool** | A 10 × 8 courtyard pool, two blocks deep | A `sink` shape of 3 in prismarine tile, a `basin` at level 12 | x −29…−20, z −63…−55, floor y10, water y11–12 | Between the two hotel wings, where the loungers face it |
| **Pool-deck furniture** | Five loungers and three striped umbrellas | Made things `pool-deck`, 4 layers, 5 beds, 3 poles and canopies | beds x −14…−6, z −57…−54, y14–15; canopies y18 | Human scale on the deck |
| **The Halcyon Hotel** | One made thing: a 3-storey block on an open arcade, a glass lobby, two 2-storey wings, balconies, roof terraces | 15 `made` layers of one `part_of`, a wallRun facade, shared slab layers; see *The hotel, in layers* | x −38…−10, z −74…−57, y14–30 | The resort, stepped down toward the water; ground floor open to the terrace |
| **Bungalows** | Two thatched stilt cabins | House props of `thatched-jungle-plank-stilt-bungalow` | (28…34, −75…−70) and (40…46, −75…−70) | The beach-cabana idea, on the palm cay |
| **Spawn pavilions** | A 16 × 16 hip-roofed pavilion for each team | `roomStyles.spawn` of `cyan-wool-roofed-quartz-pavilion` | footprint x −8…8, z −103…−87 | The team's lobby, in the resort's own materials |
| **Driftwood Bar** | An open thatched pavilion with a counter and eight stools | Made thing, 7 layers, 3 thatch tiers at y17–19, 8 jungle-log posts, `mirrors: false` | x −7…7, z −5…4, deck y12, counter y13–14 | The neutral structure on the axis, the spit running through it |
| **Lifeguard tower** | A stilted white cabin under a cyan roof with a ladder | Made thing, 5 layers, `ring_polygon` walls with a gap | stilts x 9…12, z −36…−33, platform y17, roof y21 | A lookout over the spit, on its own islet at (11, −33) |
| **Palm Walk** | A 3-wide boardwalk over stilts to the palm cay | Corridor polygon at y11 and log stilts at y7–10 | (13, −70) → (19, −72) → (26, −71) | The resort's own route to the bungalows |
| **Sunset Pier** | A boardwalk jetty into the lagoon | The same `jetty` helper | (−14, −46) → (−15, −34) | A standing place over the water west of the spit |
| **Beach cabanas** | Two striped canopies on four posts | Made thing `beach-cabanas`, 2 layers | (−34, −49) and (−17, −49), canopy y16 | Shade on the beach below the terrace |
| **The Needle** | A rock stack of four tiers, the tallest on the board | Four `level` plates, `karst` theme, skirt 6 on the foot | centre (38, −32), top y29 | The perch east of the reef, the approach from above |
| **The Sentinel** | A three-tier stack beside the spit's start | Three `level` plates | centre (19, −43), top y21 | A sightline over the monument's front |
| **The Sisters and the Thumb** | Two stacks and a single stack | Plates of two and three tiers | (−44, −52) top y24, (−34, −47) top y18, (−27, −30) top y23 | The west island chain's silhouettes |

**The monument stands on open sand with the ground round it composed.** The terrace and hotel stand west 15 blocks off, the garden lawn lifts to y13 north, the Sentinel stands east, and the spit leaves south. That is around, through and above, with no approach from below; I did not build one.

**The three crossings differ in what they cost.** The spit is dry and fast and 8 wide, the reef ford is two blocks of wading under the Needle, and the islet hop crosses swim gaps of deeper water. All three meet in the Driftwood Bar's cay, so the contested middle is a structure.

## The hotel, in layers

**The hotel is one made thing, `halcyon-hotel`, of 15 layers and 56 shapes, standing on the resort terrace with no `seat`.** Its footprint is x −38…−10, z −74…−57, the stepped mass rising from the arcade at y14 to a parapet at y30, and team 1 gets its image at z′ = −z−1 because the group keeps `mirrors: true`. The terrace top is y13, so every wall starts at y14; `seat: "ground"` is unused because the facade stack is pinned to world Y and a seat would move its bands off the datum.

**It follows one module: a four-block bay and a five-course storey.** A side of 4n+1 cells puts a quartz-pillar pier on each corner, the facade is a `wallRun` of pier and bay stated as a shape's `material`, and the bay is a `height` stack pinned to y14 (quartz 2, cyan stained glass 2, quartz 1, three storeys, then a two-course cyan-wool cornice). One mass is therefore one layer, and the window bands cost no layer.

**Slabs and doors are shared across masses.** Slabs share one layer per height, a door is a sill override on the mass's layer plus a lintel on the shared one, and the interior is hollow because a one-course override floor sits inside each wall rectangle.

| Layer | What it is | Base y (courses) | Shapes |
|---|---|---|---|
| `halcyon-hotel-lobby` | The glass lobby, set back under the main block | y14–18; floor y13 | 4: walls x −34…−14, z −73…−69; floor override; two door sills at x −29…−27 and −21…−19, z −69 |
| `halcyon-hotel-piers` | The arcade of quartz pillars round the lobby | y14–18 | 16, one every 4 blocks along z −74 and z −66, x −38…−10 |
| `halcyon-hotel-lintels` | The wall left over four doors | y18 (the wing lintels to y25) | 4: the two lobby doors, and the two wing doors at x −30 and x −18, z −64…−62 |
| `halcyon-hotel-main` | The main block, two storeys on the arcade | y19–30; floor y19 | 2: walls x −38…−10, z −74…−66; floor override |
| `halcyon-hotel-wings` | Two 2-storey wings that step down toward the pool | y14–25; floors y13 | 6: walls x −38…−30 and x −18…−10, z −65…−57; two floors; two door sills at x −30 and x −18 |
| `halcyon-hotel-slab-1` | The wings' first-floor slabs | y19 | 2 |
| `halcyon-hotel-slab-2` | The main block's middle slab and both wing roofs | y24 | 3 |
| `halcyon-hotel-slab-3` | The main block's roof terrace | y29 | 1 |
| `halcyon-hotel-balcony-1` and `-2` | A 2-deep balcony on the courtyard face, x −29…−19, z −65…−64 | y19 and y24 | 1 each |
| `halcyon-hotel-rail-1` and `-2` | Jungle-fence rails on those balconies | y20 and y25 | 3 each |
| `halcyon-hotel-roof-loungers` | Six white-wool loungers on the wing roofs | y25 | 6 |
| `halcyon-hotel-roof-poles` and `-canopy` | A striped shade on each wing roof | poles y25–27, canopy y28 | 2 each |

**It reads as a resort hotel from the lagoon.** The isometric shows a white block with turquoise window bands and a cyan cornice, two lower wings, balconies over the courtyard and an open pillared ground floor. `render/eye` from the beach shows the pool between the wings with the lobby doors behind it.

**The ground floor is walkable and the routes are unchanged.** The x-ray reads one open void of 1 535 cells at x −38…−10, y14–18, z −74…−58, which is the arcade, the lobby and both wing ground floors through their doors. Pre-flight still says `export gate OPEN`, and no `OB19`, `DR-PASS` or spawn finding names the hotel, because a made thing is not a prop.

**What the layer system could not express.**

- **The upper storeys are sealed.** The x-ray lists 11 sealed voids, among them the main block's second and third storeys and both wings' second storeys, because a stair is not a made shape and nothing joins one floor to the next.
- **A facade is the same on every face.** The `wallRun` paints the whole perimeter alike, so an open south side on the ground storey needed a separate lobby and a pier arcade.
- **A roof is a slab.** There is no pitched or hip roof as a hollow made shape, so the hotel is flat-roofed with a parapet and a cornice.
- **Height is pinned.** The facade datum is world Y, so the hotel cannot be seated onto a grade, and the build ceiling at y30 caps the main block at three storeys.
- **A shape's `material` applies to every bucket**, so each paving cell needed `size` 2 and a `rise` to pass `PT3` and `PT4`.

## The new house styles

**Two styles were forked from library rows and stated as snapshots, named for what they are; the hotel is not a house style.** Each is stated as `{"library": <base>, "kind": "house", "shell": <the changed parts>}` in `dressing.styles`, and none was saved to the shared library.

| Name | Forks | What changed |
|---|---|---|
| `thatched-jungle-plank-stilt-bungalow` | `jungle-trimmed-stilt-house` | A hay thatch roof; jungle-plank walls; jungle-log posts, beams and laid course; a jungle-stair lattice window; open stilts below |
| `cyan-wool-roofed-quartz-pavilion` | `cyan-roofed-white-clay-house` | One storey, a 2-block overhang, the earlier villa's roof and walls, no storey list |

**Each was looked at in section before the world was built.** `POST /room-styles/preview-snapshot?format=png&view=section` showed a thatched upper room over open stilts and a single storey under a stepped hip. A first hotel was also a style, `cyan-wool-roofed-three-storey-quartz-villa` placed twice, and the author had it rebuilt in layers. No finding named any of them: I saw no `HS` complaint on the store or the export.

## The kit

**Forking a library house is one dict merge, and the kit gives no helper for it.** `kit.Studio().get_room_styles()` and `get_room_styles_json(id)["styleJson"]` give a row's full style, and I replaced whole top-level parts. A fork stated as `{"library": base, "shell": parts}` in `dressing.styles` is honoured.

**`roomStyles.spawn` does not honour that fork wrapper, and nothing says so.** I stated the wrapper there and the spawn halls came out in the base library style, cyan clay over pink-white clay, with a 200 and no finding. Stating the full merged style fixed it, which is why `house_styles()` returns both forms.

**`POST /terrain/prop-preview` cannot preview a house whose style is a name or a snapshot I state.** It answered `DR-DOC` for a name and an empty plan for an inline style, so a multi-wing building is looked at on the board with `render/eye` and `render/section`. Its `HP3` cap of 192 blocks, counted over corners inclusive, is what forced the first hotel into two placements.

**A shape's `material` is held to the theme rules in every bucket.** A `cell` of size 1 answered `PT3`, and one with no `rise` answered `PT4` once for each of rim, surface and fill, about thirty refusals in one dry run. The fix was `size=2, rise=2`.

**The kit's constructors caught nothing in this run because every field was typed.** `kit.Studio()` printed no warning of mine that a constructor could have caught, and every refusal came back from the studio with a rule id and a JSON path.

**Studio write calls took 8 to 10 seconds a drive on the deployed machine.** The `source` store, the report and the picture together ran 8.3 s, and no request was refused 429.

## What went wrong / what I could not say

**The water cannot be turquoise and the grass green at once.** I looked for a biome that tints water and found one, Swampland, so the board has teal water and olive vegetation. A per-column field cannot put one biome over water columns and another over land, because a `cell` or `noise` field is not masked by a shape. Verdict: **missing**, there is no shape-scoped biome.

**A patch's `base_height` above the plan's ground raises a tower.** I stated a jungle patch at 40 over a plan ground of 9 and the column read grass at y39. A taller add wins the column and the relief does not flatten it, so a paint patch must state the ground's own height. I had read the opposite from a card.

**A bevel is paid from inside the ring.** My first spit and cays were drawn at their dry size and came out as a one-block line, 3 wide where I had stated 9. Reading `render/heightmap?format=text&every=1` at the first store showed it; the pads are now drawn a bevel wider.

**A placed tree needs soil, and a lagoon basin claims the shore.** The tree seat mask refused 3 304 cells to `DR-ROOT`, which are sand, and a basin with a default shore claimed the land round it, so my first 12 props were declined `DR-CLAIM` by the lagoon until `shore: 0`. I also lost two trees and two bungalows to the palm cay's size, then enlarged the cay.

**`OB19` named the first hotel the day after `DR-PASS` named its north side.** Moving the villas 4 blocks south fixed `DR-PASS`, which raised `OB19` on the monument's ten-block clearance, so the monument moved to (8, −53). Both gates are right; the order I found them in cost five stores. The layered hotel is outside both gates, which read props.

**Two `DR-PASS` complaints stand on the bungalows.** The palm cay is 26 blocks wide and the two cabins sit 4 apart, so the group has less than 8 blocks of ground on one side; the export carries `Pgm-Warnings: 2 DR-PASS`. The report counts them as "declined 2", but both buildings are in the world.

**The dead share reads 55.3% because most of the board is water.** The two patches are 4 733 cells at (−31, −1) and 4 304 at (29, −1), the open lagoon either side of the spit. One monument a team on a board under 100 wide cannot meet a dead-share band, and a lagoon is the extreme case; I recorded it and left it.

**Things I did not do.** No approach from below was built, no `mirrors=False` landmark except the bar, no `roofStair` roof, and no crops. The stair roofs deployed late in the run; the wool roofs are whole blocks and read as a stepped pyramid. I saved nothing to the library, because no route takes a bare `HouseStyle`, so `HS19` was only tried as the dressing registry's key.

## Open gameplay questions

**Is a bar in the middle of the only dry crossing a funnel or a stall?** I decided it is a landmark with a gap round it: the thatch pavilion is open, the counter is 7 wide, and the spit passes through the pavilion's middle. If the author wants the middle a plain sandbar, the bar belongs on the hotel cay.

**Is a 12-wide wading ford a real route?** Players cross one block of water slowly and exposed. I decided it is the third way over, slower than the spit and covered by the Needle; whether it should be dry is the author's call.

**Is the pool courtyard a place to fight or a place to stand?** The monument is 20 blocks from the pool and the hotel is behind it, so the resort is the "through" approach. I did not decide whether the hotel's upper floors should open onto the terrace.

## What worked first time

**The plan was two pieces and one monument and judged valid on the first dry run.** The `GO1` read was 3.5 and the final walk is 3.36 once the monument moved nearer its spawn. The only plan finding is `G8`, a dead-share the lagoon makes by design.

**The basin water and the pool both stood on the first store.** Column reads gave water at y10 over sand and at y11–12 over prismarine in the pool, and the pool's pit and lip came from one `sink` shape. The export answered 200 with `Pgm-Warnings: 2 DR-PASS` and pre-flight said `export gate OPEN`.

## The instrument count

**One relief with 14 marks and one push, 22 ground shapes, 37 made layers holding 119 shapes, three themes and two house styles.** The zeros are copied trees and `polyline` shapes; the dressing is two flora lawns, two bungalows, three paths and four palms from the library's `jungle-2` and `jungle-5` recipes.

## Timings, on the deployed studio

| What | Time |
|---|---|
| `drive.py` loop, spec to report | 8 s |
| `GET …/report?format=text` | 3 s |
| `render/isometric`, `render/eye` | under 2 s each |

## Where the board is

`specs/sonnet55-halcyon-cays/` holds `build-spec.py`, the plan and refinement it writes, the layout and intent the studio stored, `provenance.json` and the board's picture. `maps/sonnet55-halcyon-cays/` holds `region/`, `level.dat`, `map.xml` and `map.png`. The map is stored with 25 changes.
