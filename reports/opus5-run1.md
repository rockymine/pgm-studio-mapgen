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

Each has a `review/<slug>.md` with its own measurements. This report is only about the surface: what I
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
- **The crossing is 20 blocks, and on Block Realm you pay for it twice.** An attacker on Alderfen and
  Quiverstone places 23–27 blocks; on Block Realm, where the route runs field → midway → field, it is
  **39–42**. Decided **keep it**, because a mid island both sides pay to reach is what the author asked
  for. Whether 40 placed blocks is a crossing or a chore is played, not measured.
