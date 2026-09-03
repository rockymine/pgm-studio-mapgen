# opus5, run 1 — three boards, and what the surface would and would not say

## What I set out to build

One board was specified by the author, in full, and the rest were mine to choose.

**The specified one.** A destroy-the-core map on a swamp theme. Small-to-medium buildings in spruce
and dark oak. Trees scattered with **vines hanging down at different heights**. A small lake on each
island, surrounded by sand, with **lily pads tested on the water**. Terrain hilly near spawn,
levelling out toward mid, dirt and grass mixed into the hills. A **fairly square** map outline,
nothing extreme. Paths of **coarse dirt and polished andesite** from spawn to mid. **One** mid island.
Rougher, hillier ground toward the edges. A **Mesa-and-swamp biome pattern**. Grass detailed with
specks of podzol and dirt; **fern, brown mushroom and grass** on the surface. **Boulders in a
turbulence pattern** of cobble, mossy cobble and andesite. **Laid log piles** on the ground. **Tiny
huts with a laid-log roof** — if possible a pattern with several laid log types, oak, spruce and dark
oak — and walls in a small **noise pattern of hardened clay, light-grey clay and jungle planks**.
**Tiny 1×1 windows** of light-grey stained clay. And **cumulus-cloud structures in the sky**.

That is `opus5-alderfen`, *Alderfen Reach*.

**Then: "reflect and make some more, completely different themes"**, with a desert-and-Mesa map, a
Mario-inspired map, a space theme and an abstract theme offered as ideas. I took the first two:

- `opus5-quiverstone`, *Quiverstone Mesa* — a destroy-the-monument badlands board, built to answer a
  different question from Alderfen's: whether one `layered` strata stack can be the `wall` bucket of
  every ground theme at once, so that every cut face on the board shows the same beds at the same
  heights.
- `opus5-blockrealm`, *Block Realm* — a destroy-the-core board on a drawn-platformer theme, built to
  invert Alderfen's construction entirely: flat ground with **all** height carried by erected plates
  in two-block steps, and a made-thing vocabulary of warp pipes, drawn hills, floating block rows and
  clouds.
- `opus5-lodestar`, *Lodestar Yard* — a **capture-the-wool** board on a derelict orbital dock. The
  first three are all destroy boards, and a destroy board is not read for routes at all: the flow read
  says so and stops. This one changes the objective family, which changes which rules apply, what the
  flow read can say, and — as it turned out — what shape the board is allowed to be.

Each of the four has a `review/<slug>.md` with its own measurements. This report is only about the surface: what I
could not say to it, what I said wrongly, and what worked without a fight.

## What I could not say

Six things. Each row below states what I wanted, where I looked, and which of the two answers it is —
**missing from the system** (the capability is not there) or **out of reach from where I was standing**
(it is there, and the surface would not tell me, or a rule deliberately forbids it). The difference is
the point, and four of the six turned out to be the second.

### 1 · A multi-wood laid-log roof — *forbidden by a stated rule, on purpose*

**Wanted:** the author asked, in as many words, for a hut roof with "a pattern with multiple laid log
types: oak, spruce, dark oak".

**Looked for:** `HouseStyle.roof` → `RoofStyle.body` and `RoofStyle.verge` in
`GET /api/openapi/v1.json`. Both are declared `oneOf: [TerrainMaterial]` — the same polymorphic base
that carries `noise`, `cell`, `turbulence` and `laidLog`, so from the schema alone a patterned roof
looks expressible. It is not. `GET /api/rules?rule=HS3` says why:

> A roof is not one material. Its body and its verge are each a single block — never a pattern, so
> nothing spreads a voronoi across a roof … A laid log is a roof material, and the distinction is the
> whole rule.

And `LaidLogMaterial` carries exactly two fields, `id` and `data` — one log, not a list.

**Verdict: out of reach, and the rule is the reason rather than an accident.** HS3 states its own case
(a field pattern spread over a sloped roof), so this is a design position, not a gap. The nearest
expressible thing is two woods — body in one, verge in another — which is what shipped: a laid spruce
body with a laid dark-oak verge, and the third wood, oak, in the log piles on the ground beside the
hut. The author asked for three woods on one roof and got two on the roof and the third at its foot.

### 2 · Lily pads on a water prop — *out of reach by claim order, and there is a way round*

**Wanted:** "test placing lilypads on the water."

**Tried:** a copied-tree body of one lily pad, placed on the bed of a `water` prop.

**Refused with `DR-CLAIM`**, twice. `GET /api/rules?rule=DR-CLAIM` explains it exactly:

> The pass places in priority order and the first claimant keeps the cell.

A water prop claims its bed and its beach as `ClaimKind.Water` at **order 0**; a tree places at
**order 4**. So nothing can ever be placed on water a water prop made, by construction — not lily
pads, not reeds, not a boat.

**Verdict: out of reach, with a working detour.** Paint the water as *terrain* instead — a one-course
patch of a marsh theme, pinned a block below the ground around it — and the pond is ground rather
than a claim, so a prop seats on it. Verified at `(-5, -64)` on Alderfen: **Lily Pad y13 / Water y12 /
Sand y9–11**. The lesson generalises: anything that must sit *on* water goes on painted water, never
on a water prop.

### 3 · Brown mushrooms from the cover overlay — *missing, and the substitute is a copied body*

**Wanted:** "some fern, brown Mushroom and grass on the surface."

**Looked for:** a species field on the flora overlay recipe. The recipe takes `coverage`, `scale`,
`octaves`, `fernShare`, `flowerShare`, `flowerScale`, `tallShare` — three named shares, none of them a
mushroom, and no species list. The nearest enum in the whole schema is
`TreeStyleSaveRequest.species`: `oak · birch · spruce · jungle · acacia · dark oak`. No fungus
anywhere.

**Verdict: missing from the overlay.** Delivered another way, and there is a vanilla trap behind it: a
brown mushroom in daylight is dropped by the game unless it stands on podzol or mycelium. So the fix
is two things at once — painted podzol patches (theme `fenbed`) plus one-cell copied bodies on them.
Verified at `(-49, -88)`: **Brown Mushroom y34 / Podzol y33**.

### 4 · Whether a vine's face is turned round the orbit — *the schema cannot say, and the answer is no*

**Wanted:** vines on the correct faces of a copied tree on **both** halves of a `rot_180` board.

**Tried:** vine blocks with a single-face data value (1 = south, 2 = west, …).

**What happens:** `BlockGeometry.Turned` turns a log's axis and a stair's facing round the orbit and
leaves a vine's data nibble alone, so a single-face vine on the mirrored copy hangs off the wrong side
of its own trunk. Nothing in the schema says which data nibbles are turned; the field is an
`integer` called `data`.

**Verdict: out of reach — the surface has no way to express the question.** The workaround is
arithmetic rather than API: use face **pairs**, 5 (north|south) and 10 (west|east), both of which are
invariant under `rot_180`. That is what both boards ship.

### 5 · A `Storey`'s `deck` as a band stack — *out of reach, and the failure mode is the finding*

**Wanted:** a two-material floor plate in a house.

**Tried:** `deck: {stack: [...], extent: 2}`.

**Got: HTTP 500**, with **nothing in the response** and the only diagnostic in the server log:

> the JSON payload for polymorphic … TerrainMaterial must specify a type discriminator.
> Path: `$.shell.storeys[1].deck`

The schema is right and I misread it: `Storey.deck` is `oneOf: [TerrainMaterial]`, a bare material,
and its description says so — *"one course … One plate, one owner."* A `{stack, extent}` is a
`LayeredMaterial`'s *inner* shape, not a `TerrainMaterial`.

**Verdict: out of reach because I read the field wrong** — but the 500 is a real defect in the
surface. Every other malformed document on these three boards came back as a typed finding with a
rule id; this one came back as an unlabelled 500 whose cause was only visible to someone who could
read the server's log. An agent driving over HTTP alone cannot diagnose it. **It cost the same
mistake twice**, once on each of the first two boards, because the first time I worked round it
(`deck: null`) without understanding it.

### 6 · Obsidian for a fifteen-block destroyable — *forbidden, with the fix named in the rule*

**Wanted:** an obsidian `column-plus` monument.

**Got `DC3`:** obsidian is worth at most three blocks, so the studio **built the map anyway** in ender
stone and said so — a complaint, not a refusal, and the `map.xml` declared what was actually laid.
The rule's own `fix` names the pairs: obsidian for a pillar; ender stone, gold or emerald for a cube
or a column.

**Verdict: out of reach by a deliberate rule, and the rule is right.** `pillar-3` in obsidian shipped,
and a slim black spire on white caliche is the better silhouette anyway.

### The finding behind four of those six

**Two of the eight fields of `SketchLayout` carry no schema at all**, and they are the two the author's
brief spent most of its words on:

| `SketchLayout` field | typed in `/api/openapi/v1.json`? |
|---|---|
| `setup`, `layers`, `themes`, `mapTheme`, `roomStyles`, `relief` | yes |
| **`dressing`** | **no — description and `nullable: true`, nothing else** |
| **`biome`** | **no — description and `nullable: true`, nothing else** |

`dressing` is every prop on the board: the trees, the vines, the boulders, the log piles, the huts,
the water, the flora overlay. `biome` is the Mesa-and-swamp pattern. Neither has a single field name
in the published schema, so items 2, 3 and 4 above were **not answerable from the API surface at
all** — I learned them from `docs/`, from the corpus and from refusals. That is not the same as the
capability being absent: the dressing document is rich and does nearly everything asked of it. It is
that the one artifact an agent is told to check before filing a gap cannot answer a question about
half the document it has to write.

### 7 · What a wool board refuses that a destroy board does not

The fourth board is the run's one capture-the-wool map, and it drew four refusals on its **first dry
run** that none of the three destroy boards had ever seen. All four turned out to be **out of reach
from where I was standing** in the most useful sense: the rule said what it wanted and why, and the
"why" was that the board is played for wool.

| Rule | Said | Why the earlier boards never met it |
|---|---|---|
| `FR6` | `frontline-width 20 outside authored band [1, 16]` | its own text: *"On a board played for cores or destroyables there is no width cap at all (amendment 2026-09-02): 6–8 cells is the wool board's figure"* |
| `STRUCT` | `wool room is unreachable: no land seam and no abutting build zone to enter by` | a destroy board has no wool room |
| `G8` | `fill-ratio 0.773 outside authored band [0.201, 0.542]` | not raised on the DTC boards at 0.745 — the band is read against the detected mode |
| `SP2` | `spawn on 'berth' not near the back of its lane` (complaint) | the lane chain here is seven pieces long, and the lint says of itself that it *"approximates 'back' per-piece and misreads spawns placed mid-chain"* |

**This is the run's most transferable finding, and it is not a defect.** A rule id is not a fixed
constraint: `FR6`, `G8` and `CT12` all read **authored bands** whose values depend on what the board
is played for, and three boards of experience on one objective family taught me nothing about the
next. A 100-block frontline and a solid rectangle a side are correct for a core board and refused on
a wool board, and the only way to know is to dry-run the plan and read the band the finding quotes.

What cleared all four was one change of topology rather than four fixes: the deck stopped being a
rectangle and became a **hub with two arms**, each arm ending in a wool bay that abuts it along
fifteen blocks of shared edge, with one 40-block neck as the board's only edge on the void. That is
`FR6`'s own "split frontline hung off a hub", it gives `STRUCT` its seam, and the void between the
arms takes the fill ratio to 0.375.

It also produced the run's best dead-ground number by a wide margin — **1% off every route**, against
28.8%, 36.7% and 40.1% on the three rectangles. A rectangle has corners no journey passes; an arm
is a corridor to somewhere, so every block of it is on the way.

### 8 · A theme's `rim` takes a band, not a material — and the schema will not say

**Wanted:** a chiselled cap course along every cut edge of the hull.

**Tried:** `"rim": solid(STONE_BRICK, CHISELLED_BRICK)` — the same shape `wall` and `fill` take.

**Got `RQ1`**, and the rule states the whole contract in one line: *"'rim' names no material — rim and
surface take a band, `{"material": …, "depth": N}`, and wall and fill take a material directly."*

**Verdict: out of reach because I read the field wrong, and the schema cannot correct me** — the
theme dictionary lives under `SketchLayout.themes`, which *is* typed, but the four buckets' band-vs-
material split is the kind of thing a `oneOf` does not distinguish at a glance. `RQ1` is the good
case for how a refusal should read: it names the field, states both shapes, and says which buckets
take which. One read of the rule and one edit.

### 9 · A voronoi's `bands` are bands, and an ill-formed list stores at 200 and throws at paint time

**Wanted:** a five-colour hull plate — straight-edged convex cells about seven blocks across.

**Tried:** `voronoi(seed, cellSize, [material, material, …])`, by analogy with `noise`, whose `stops`
**is** a bare list of materials.

**Got `RQ2`:** *"the studio failed to answer this request, and the fault is its own rather than the
document's — the detail is in the server log."* The log:

```
unhandled at GET /api/map/opus5-lodestar/export
System.NullReferenceException
   at PgmStudio.Minecraft.Painting.VoronoiMaterial.Resolve(BucketContext& ctx)
      TerrainPatterns.cs:line 64
```

**The schema is right and I read it wrong.** `VoronoiMaterial.bands` is declared
`array of VoronoiBand`, and `VoronoiBand` is documented as *"a material and how many blocks inward
from the cell boundary it runs. The last band's depth is ignored — it takes whatever is left of the
cell."* It even says why it is not a `Band`: a `BandStack` is read along an integer step, a voronoi
along the continuous Worley `F2 − F1` gap. `noise` taking bare materials in `stops` and `voronoi`
taking pairs in `bands` is a real distinction with a real reason, and the field names say so.

**Verdict: out of reach because I read the field wrong — and there is a defect underneath it.** A
`bands` array of bare materials was **accepted by `PUT /sketch` with a 200**, survived the store, and
only failed at `GET /export`, in the painter, on a null `VoronoiBand.Material`. Every other malformed
material on this run was caught at store time by an `RQ` gate that named the field (`RQ1` on the
`rim`, and it named both shapes and which buckets take which). This one was not. The gate that
already exists for `rim` would catch it.

This is the **second** 500 of the run whose only diagnostic was in the server log, after
`Storey.deck`. Both were my misreading of a field, and in both cases an agent driving over HTTP alone
could not have found the cause. `RQ2` at least labels the class honestly — *"the fault is its own
rather than the document's"* — which is more than the bare 500 the `deck` gave.

## What I got wrong

### An ellipse states a box and covers less than half of it

This one caused four repeated `WX11` complaints across two boards before I found it, and it is the
single most useful thing I learned.

`lobed_ring(cx, cz, half_x, half_z, …)` draws an **ellipse** inscribed in the box it names. At 0.8 of
its own half-width it has already fallen to 0.6 of its half-depth. So a relief `area` mark drawn as
`lobed_ring(0, -88, 30, 11)` — which reads exactly like "pin the ground from x −30 to 30, z −99 to
−77" — leaves the **ends of its own stated band unpinned**. A building placed at x −26 on the strength
of that reading stands half on pinned ground and half on the slope beside it, and `WX11` says so:
*"stands 5 blocks above the cell beside it — the ground falling away. Its foundation fills that face
in bedrock, which is a wall a player cannot climb and nobody drew."*

**Why the wrong claim looked right:** the finding points at the *building*, and the building's
coordinates are inside the box the mark named. Everything I could see said the pad covered it. Three
times I moved the building; the fourth time I drew the pad's actual coverage and found the ellipse.

The fix is a `lobed_box` helper — a closed ring with chamfered corners that covers the band it states
— and it is now what every pinned pad on all three boards uses. It is in each `build-spec.py` with
that reasoning in its docstring.

### `maxPlayers` is per team, and its own docstring says otherwise

I set `globals.maxPlayers: 24` reading it as the board's total. `TeamsGenerator` writes it into
**each** team's `max`, so Alderfen's first `map.xml` declared a 48-player map. Both boards ship 16.
The measurement that caught it was reading the exported `map.xml`, not any finding — nothing
complained.

### "Every generated destroy map is unwinnable"

Not this run's mistake, but it is written into `CLAUDE.md` as the worked example of the failure this
repo guards against, and it shaped how I worked. A destroyable and a core **float above the terrain
by design** — a core on the ground cannot leak, a destroyable on the ground is trivially covered.
Measuring the gap and reasoning from first principles produced a confident, filed, committed claim
that was invented. I took the standing lesson literally: every gameplay judgement I made without an
oracle is listed at the bottom of this report rather than asserted as a fact in a doc.

### 46% dead ground read as a theme problem

On Block Realm's first build, `01-flow.txt` reported **9 600 of 20 800 blocks (46%)** off every route,
in four patches — the outer flanks. My first instinct was to decorate them. The read itself says not
to, in as many words: *"Bring an objective to it, put a route through it, or take it off the board —
decorating it only means players look at it on the way past."* The actual cause was arithmetic: a
140-wide field with its two goals at x ±30 leaves 40 blocks each side that no journey between any two
places on the board passes. Narrowing the field to 110 took it to **33%**, and the same change cleared
the `LN2` lane complaint (`max-chain-length 140 outside [25, 110]`) that had been standing since the
first dry run. One measurement, two findings.

### A house stamps wider than the corners it states

`row-mid`, a floating block row at z −8..−6, drew `SK18` against a house whose stated corners stop at
z −9. The house's *stamped* extent — wall thickness, eave overhang and the structure clearance ring —
reaches further than its `corners`. Clearing a made thing against a building means clearing it against
the stamp, and the only way to know the stamp is to read the claims map (`06-claims.txt`, where a
building is `3` and its keep-out ring is `b`) rather than the document you wrote.

## What worked first time

Not padding — this is the half a reader can trust without checking.

- **`?format=text` reads.** `column`, `transect`, `slopes`, `walk`, `themes/census`,
  `sketch/dressing`. Every one of them answered what it says it answers, first time, on all three
  boards. `column?at=x,z&format=text` is the only read that is not a projection, and it settled every
  "did that actually land" question in this run — the lily pad, the mushroom, the strata, the vines.
- **`POST /plan/evaluate` before a map row exists.** Catching `GO1`, `GO4` and `LN2` on a document
  that has never been stored, in about a second, is what made three boards affordable. Block Realm's
  goal geometry was fixed by moving two numbers before anything was built.
- **`layered` as a shared `wall` bucket.** Putting one seven-band strata stack in the `wall` bucket of
  *every* ground theme, and in `fill` as well, gave Quiverstone a badlands where every cut face —
  coast, butte and hoodoo — shows the same beds at the same heights. It worked exactly as reasoned,
  first build, no iteration. Read at `(-52, -86)`: orange clay y42–43, sandstone y40–41, hardened
  clay y35–37, brown clay y33–34.
- **A made layer to dodge the build ceiling.** `BuildCeiling.Of(highestGround)` is *tallest terrain
  column + 20*, so a 20-course pinnacle authored as erected terrain hands the whole board a ceiling 20
  blocks above its own top. Three made slabs with `seat: "ground"` and a shared `part_of` settle onto
  the terrain as one thing and are out of that reckoning. Both the hoodoos and every warp pipe, hill,
  cloud and block row on Block Realm use it. First try, all three boards.
- **Copied tree bodies as the escape hatch for anything the recipes will not say.** A copied body is
  the one recipe that writes arbitrary blocks, and it is how the vines, the dead bushes under an
  acacia, the mushrooms and the flat-topped platformer trees all got built. If a recipe will not say
  it, a copied body will.
- **`bendShapes` for a drawn coast.** Worked as documented; the only correction was magnitude —
  `wander: 2.5` is invisible at map scale and `6` reads as a coast.
- **`teamTint` as a whole board's identity.** One theme, painted on both docks of the wool board, and
  the census reads back `159:14 Red Stained Clay` **and** `159:11 Blue Stained Clay` from that single
  material. It worked exactly as its docstring says, first build. The one thing to know is what its
  `neutral` fallback is for: paint a neutral piece with it and every cell falls back to the fallback,
  so the material has nothing to say there.
- **The studio places a CTW board's monuments itself.** The plan states the wool rooms and their
  markers; `POST /map/from-documents` worked out four wools, four monuments beside the right spawns,
  22 regions, 34 filters and 11 apply-rules, and `preflight`'s mirror check grew a `wool/room ✓` leg
  that the destroy boards never had. No authoring, no correction.

## Open gameplay questions

Decided without an oracle, because the author was not available while these boards were being built.
Each is a judgement about the map **as played**, which `CLAUDE.md` says this repository cannot settle.

- **Two goals a team rather than one, 48–60 apart.** Decided **for**, on a measurement: a single
  central goal put every journey down `x = 0` and left both flanks off every route (83% dead on
  Alderfen's first plan). Splitting the pair took it to 32%. `GO2`'s band (35–65) and
  `docs/gameplay/approaches.md`'s multi-goal arrangement both permit it. **What is not measured** is
  whether a 16-a-side team can defend two objectives at once. If the answer is no, all three boards
  want their pair merged, and the dead-ground problem comes back and needs a different answer.
- **The hills near spawn are deliberately unbuilt.** The author asked for hilly ground near spawn and
  for buildings; `DR-SLOPE` forbids a building on a hillside, so every building stands on a pinned
  pad. Seventy-two blocks of pinned bog already carries two cores with their clearances, two roads and
  a pool, which leaves the hills as terrain and nothing else. Decided **hills over buildings on
  them**. Whether the author wanted a hut *on* a hill — which would need the hill pinned flat at its
  top, i.e. a plateau rather than a hill — is a question I could not answer.
- **A hoodoo is climbable but not bridgeable-from.** Being a made thing it does not raise the build
  ceiling, so a player on top of one cannot build as high as from the butte beside it. Decided
  **accept the asymmetry**, because the alternative raises the whole board's ceiling by twenty. Whether
  two rocks of the same silhouette behaving differently reads as deliberate is the author's call.
- **A two-block step is the unit of height on Block Realm.** A one-block rise walks, a two-block rise
  costs one placed block, and three or more is a barrier. Every plate on that board steps by two, so
  the whole map is climbable at the price of one block per step. Decided **two**, on the reasoning
  that a drawn platformer's height should cost something and not much. Untested in play.
- **A wool at the end of an arm has one way in.** `plan/flow` on the fourth board: *"One way in, end
  to end: nothing forks and nothing merges, so the whole approach is one road to hold."* That is a
  direct consequence of the shape `FR6` and `STRUCT` forced on it, and it is the sharpest gameplay
  finding of the run. Decided **keep it** — the arms are what took dead ground to 1%, and a corridor
  is a real defensive position rather than an open field. But a single approach may simply be too easy
  to hold at 24 a side; if it is, the fix is a bridgeable gap onto each arm's flank, which puts void
  back and raises the fill ratio again. This one wants an oracle more than anything else in the run.
- **Land per player is an input, and I set it from a table rather than from taste.** `G8` couples land
  per team to players per team and saturates near 175–185 blocks a player. The wool board carries
  4 400 blocks of deck a side, so it declares `maxPlayers: 24` — 183 a player, where the corpus curve
  flattens. The three destroy boards all declare 16 and carry more land than that ratio wants, which
  is a thing I did not know to check until the fourth board's plan was refused.
- **The crossing is 20 blocks, and on Block Realm you pay for it twice.** An attacker on Alderfen and
  Quiverstone places 23–27 blocks; on Block Realm, where the route runs field → midway → field, it is
  **39–42**. Decided **keep it**, because a mid island both sides pay to reach is what the author asked
  for. Whether 40 placed blocks is a crossing or a chore is played, not measured.

## What the four boards say together

Four boards, one studio, and the thing worth carrying forward is that **three boards of experience on
one objective family taught me almost nothing about the fourth.**

The three destroy boards converged on a working recipe: a rectangle a team, a rectangle in the middle,
two goals a side, a 20-block crossing, props spaced eight apart and clear of every rot_180 image. Every
one of those is correct for a core or destroyable board. Three of them are refused on a wool board —
`FR6` caps the frontline only when there is wool to carry, `G8` reads a different fill band, and
`STRUCT` will not have a wool room drawn inside another piece. The rules are the same rules; the
**bands** are read against what the board is played for, and a finding quotes the band it used.

So the transferable practice is not a recipe. It is: **dry-run the plan before anything is built, and
read the band the finding quotes rather than the number it rejected.** `POST /plan/evaluate` answers in
about a second on a document that has never been stored, and it is what made four boards affordable.

The second thing the four say together is about **dead ground**, and it is nearly the opposite of what
the first three suggested. Alderfen taught that splitting one central goal into two takes dead ground
from 83% to 32%, and Quiverstone and Block Realm both applied it and landed at 40.1% and 28.8%. All
three are rectangles, and a rectangle has corners no journey passes: past a certain width, adding
board adds dead ground faster than moving goals removes it. Lodestar was not designed for this at all
— its shape was forced by three refusals — and it reads **1%**, because an arm is a corridor to
somewhere and a corner is not. **The shape of the land does more for dead ground than the placement of
the objectives on it.**

| Board | Mode | Land shape | Dead |
|---|---|---|---|
| `opus5-alderfen` | DTC | rectangle | 36.7% |
| `opus5-quiverstone` | DTM | rectangle | 40.1% |
| `opus5-blockrealm` | DTC | rectangle, narrowed 140 → 110 | 28.8% |
| `opus5-lodestar` | CTW | hub and arms | **1.3%** |

And the third: of the nine things in this report I could not say, **five were the schema being right
and me reading it wrong**, three were a deliberate rule saying no and saying why, and one — the
`dressing` and `biome` fields carrying no schema at all — was the surface genuinely unable to answer.
That ratio is the useful number. The system is far more answerable than an agent's first impression of
it, and the check the brief demands — look in `GET /api/openapi/v1.json` before filing a gap — moved
four of my nine from "missing" to "I misread it".
