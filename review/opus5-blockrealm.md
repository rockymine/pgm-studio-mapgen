# Block Realm — a drawn platformer as a DTC board, and every block of height is a plate

> A destroy-the-core board in drawn-level colour: flat green field, brick staircases stepping two at
> a time up each flank, warp pipes at their feet, floating brick-and-question rows, and clouds
> hanging off the coast.

**In one sentence:** the ground is level everywhere a player fights, all of the board's height is
*erected plates* rather than terrain the solver shaped, and every standing thing on it — pipe, hill,
cloud, block row — is a **made** layer, which is what keeps a 100-course cloud out of the build
ceiling.

126 × 206 blocks of rendered extent over a 110 × 200 plan, `rot_180` about the origin, base surface
14, ground y13..y18, plates to y22, clouds to y100. Three landmasses: two team fields (`field`,
x −55..55, z −100..−40) and one mid island (`midway`, x −40..40, z −20..20), joined only by a build
zone over the void (x −50..50, z −40..−20).

## The board

The keep sits at `(0, −90)` on a shelf pinned at y18 with two block houses and two cap houses on it.
Three pinned ramps step down four courses to the field at y14, and two tracks of hardened clay and
brown clay run out to the flanks. The two cores stand at `(±30, −56)` — **42 blocks of walk from
their own keep, 0 placed blocks**, and 155–159 from the enemy's, of which **39–42 are placed**. Read
against its own mirror the board is fair to a block.

Two cores a team rather than one, and this board is where that decision was *measured* rather than
inherited. The first build put the field at 140 wide with the pair at x ±30, and `01-flow.txt`
answered **9 600 of 20 800 blocks (46%) off every route**, in four patches — the outer flanks. The
cause was arithmetic, not decoration: 40 blocks each side that no journey between any two places on
the board passes. Narrowing the field to 110 took it to **33%**, and cleared the standing `LN2`
complaint (*max-chain-length 140 outside [25, 110]*) in the same change.

What the ground round each core does: **open field** on its own pinned flat (nothing within the
clearance of a marker), a **brick staircase** climbing outward on its flank that an attacker holds,
a **dished pit** at the centre-front that a player drops into, a **floating block row** over that
pit, and the four houses on the shelf above to fight back through.

## What the ground is made of

Two grounds, and that is the point rather than an omission.

| Theme | Share | On | Says |
|---|---|---|---|
| `turf` | 93.1% | every landmass | one course of a six-stop `noise` — grass, grass, grass, grass, dirt, coarse dirt — over three of dirt, on a `layered` wall of two courses of brown clay above forty of hardened clay |
| `brickwork` | 6.9% | the eight erected plates | plain brick, `45:0` |

Ten distinct surface blocks over 18 010 ground cells, and one border of 400 cells. The other four
themes on the board — `pipe`, `hillside`, `cloudstuff`, `qblock` — paint **no ground at all**: they
are the materials of made things, so `themes/census` does not count them and should not. A drawn level
has one ground and puts its colour on the things standing on it, and that is what the census reads
back.

## The techniques, and what each one bought

**All height is a plate, and a plate steps by two.** `plate()` is a rectangle with `override: True`,
`height_mode: "level"`, `skirt: 0` and `relief_scope: "exclude"` — sheer on every side, standing at a
stated absolute top and ignoring the relief solve entirely. `staircase()` is three of them in a row at
tops 18, 20, 22. Two is the unit because **a one-block rise walks, a two-block rise costs one placed
block, and three or more is a barrier**: the whole board is climbable at the price of one block a step.
`03-slopes.txt` reads **16 430 walked · 653 scrambled · 927 barrier (5.3%)**, and the barrier is
almost all the plates' own sheer sides — 18 faces, the largest 116 cells at `x -53..-34, z -71..-58`,
which is the west staircase's outer face.

**Everything that stands up is a made layer, for one reason.** The build ceiling is
`BuildCeiling.Of(highestGround)` = *tallest terrain column + 20*. An erected shape **is** a terrain
column, so a cloud authored as erected terrain at y100 would hand the whole board a ceiling at y120.
A `made` layer is out of that reckoning — and out of `BuiltTerrain.Ground`, so nothing seats on one.
So the pipes, hills, clouds and block rows are all `kind: "made"`; the seated ones (`pipe`, `hill`)
carry `seat: "ground"` and a shared `part_of` so their tiers settle as one thing, and the floating
ones (`cloud`, the rows) state a `base_y` instead.

**One recipe is the hill and the cloud both.** `mound()` draws three narrowing tiers of circle lobes.
`seat=True` makes it a hill standing on the ground; `seat=False` with a `base_y` makes it a cloud. Read
at `(46, -92)`: green and lime stained clay banded y18–y24 — the hill. At `(52, -78)`: white clay and
white wool y95–y99 — the cloud. Same eight shapes, two facts changed.

**The clouds hang off the coast, and that is a measurement decision.** Every projective read on this
studio — heightmap, slopes, walk, routes — takes the **topmost solid block**, and a made layer is
solid. A cloud over walkable ground therefore reports a `barrier +60` that no player will ever meet.
The first build had exactly that on a core's own apron (`BARRIER +60 at (41, -56)`). The fix is not
to raise it — height does not help, the read is topmost-solid at any altitude — but to move it **off
every walkable column**. All six clouds are centred at x ±52 or beyond, so most of each one overhangs
the void, and only about fourteen columns of flank sit under one.

**A copied body is how a drawn tree gets a flat top.** A template oak grows a blob and a grown oak
grows a fractal; neither draws the two flat courses a drawn tree has. `block_tree()` is a short bare
trunk under a flat-topped leaf disc with four lower leaves either side, and it is the one recipe that
states its own silhouette.

## What the pass refused, and what it took to clear

Four rounds, and each one was one measurement.

**`GO4` and `GO1`: a goal must be 40–90 blocks from its own spawn, at a 3–4 ratio.** The first plan
put the cores at `(±22, −56)` — 38 and 40 blocks out, ratio 4.079. Moving them out on **x** rather
than forward on **z** cleared both without bringing them nearer the front: at `(±30, −56)` they read
own 42, ratio 3.69 and 3.79, with the pair 60 apart, inside `GO2`'s 35–65 band.

**`OB19` × 4: a prop inside a goal's clearance is declined.** Four trees at `(±38, −64)` and
`(±36, −48)` stood inside the cores' clearance — *the ground its structure covers grown by four
blocks, and never nearer than ten blocks to the marker itself*. The prop is declined rather than the
map refused, because a goal is what the map is for and a prop is removable.

**`DR-CLAIM` × 2: a prop must clear every other prop's own orbit image.** A tree at `(−6, 8)` was
declined by *the prop `tree-7`* at `(2, −10)`, whose `rot_180` image is at `(−2, 10)` — four blocks
away. The same trap `opus5-quiverstone` recorded, and the fix is the same: a landmass 80 × 36 holding
six stated props is holding twelve, and it will not. The midway carries four.

**`SK18`: a made thing shares a column with a building — and a building stamps wider than its stated
corners.** `row-mid` hung at z −8..−6 over a house whose stated `corners` stop at z −9, and drew
*stand in 8 of the same column(s) — first at (-22, -8)*. The house's **stamped** extent — wall
thickness, eave overhang, the structure clearance ring — reaches past its corners, and the only way
to see the stamp is `06-claims.txt`, where a building is `3` and its keep-out is `b`.

**`WX11`: a seated made thing takes the pinned ground out from under itself.** `block-e` drew *stands
5 blocks above the cell beside it at (28, -94) — the ground falling away. Its foundation fills that
face in bedrock, which is a wall a player cannot climb and nobody drew.* The keep pad states
x −34..34 pinned at 18, and the house sits well inside it — so the reading looked impossible. The
transect settles it:

| station | ground | surface | standing |
|---|---|---|---|
| `(27, -94)` | 18 | 18 | house block-e |
| `(28, -94)` | **13** | 17 | storey |
| `(32, -94)` | **13** | 17 | storey |

The columns the seated hill occupies read `standing: storey` with ground at the base rather than the
pad. Widening the pad did not help and dropping `relief_scope` from the hill's shapes did not help —
correctly, because the schema says `relief_scope` is *"not read on a shape that declares a
HeightMode"* and the lobes declare `height_mode: "level"`. What cleared it was moving the hills out
and shrinking them: `(±46, −92)` at `scale=0.55`, inner edge x 38, ten blocks clear of the house's
stamp. **The rule to carry forward: a seated made thing needs the same clearance from a building as
another building does, and it is measured from the made thing's outermost lobe, not its centre.**

## Not a fault

**The red and blue wool three courses high over each core.** `GoalMarkerStamper` puts a small
coloured marker high above a goal so a player can see where it is. At `(30, −56)` it reads Red Wool
y50–52 with the core's own obsidian at y20 and its lava at y21–23. It is also why
`world-surface.png` paints magenta squares labelled *unnamed material*: wool belongs to no
terrain-paint family, and both the markers and the clouds' white wool are wool.

**The magenta dot at board centre** is the observer bedrock.

## Open gameplay questions

- **Two cores a team, 60 apart.** Decided **for**, on the dead-ground measurement above (46% → 33%).
  Whether a 16-a-side team can defend two open-topped cores at once is played rather than measured.
- **A two-block step as the board's unit of height.** Every plate steps by two, so the whole board
  costs one placed block a step to climb. Decided on the reasoning that a drawn platformer's height
  should cost something and not much. Untested in play.
- **Two crossings, and 39–42 placed blocks to reach an enemy core.** The route runs field → midway →
  field, so an attacker pays for the void twice; on the two boards before this one it was 23–27 for
  one crossing. Decided **keep it**, because a mid island both sides pay to reach is the shape asked
  for. Whether forty placed blocks is a crossing or a chore is the author's call.
- **The flanks are deliberately bare.** After the narrowing, the 33% that no journey reaches is the
  outer flank behind each staircase. `01-flow.txt` says decorating dead ground *"only means players
  look at it on the way past"*, so it carries the staircase, a pipe and a hill and nothing else.
  Whether the flank wants a third objective on it is a question about how many goals a team can hold,
  which is the first question again.

## Coordinates

| Thing | At | Reads |
|---|---|---|
| red spawn point | `(0, 18, -90)` | on the pinned keep shelf |
| red cores | `(-30, -56)` and `(30, -56)` | obsidian y20, lava y21–23, `openTop`, `float 6`, `leak 5` |
| the crossings, at `x = 0` | field front z −40 → midway back z −20, and again on the far side | 20 blocks each; build zone z −40..−20 |
| the four staircases | `x -52..-34` and `x 34..52`, `z -70..-58` | erected plates, tops 18 / 20 / 22 |
| the four shelves | `x -52..-40` and `x 40..52`, `z -52..-44` | erected plates, top 18 |
| the two hills | `(-46, -92)` and `(46, -92)` | `made`, `seat: ground`, `scale 0.55`, banded green/lime y18–y24 |
| the six clouds | `(±52, -78)` and `(-52, 4)`, plus images | `made`, `base_y` 82 / 88 / 76, white clay and wool, top y100 |
| the four pipes | `(±44, -76)`, `(-34, 2)`, plus images | `made`, `seat: ground`, lime lip over a green barrel |
| the three block rows | `(-18, -49)` y24 · `(6, -30)` y24 · `(-12, 4)` y28 | `made`, brick and question alternating, five blocks each |
| goal markers (not a fault) | `(±30, -56)` at y50–52 | team wool, `GoalMarkerStamper` |
| largest barrier face | `x -53..-34, z -71..-58` | 116 cells — the west staircase's outer face |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | **score 0**, `valid: true` — no findings of any severity |
| `POST /plan/inspect` | `core-w` own 42 / enemy 155, **ratio 3.69**; `core-e` own 42 / enemy 159, **3.79**. Own pair 60 apart. Island gap **20** |
| `POST …/sketch/relief/read` | `team` 7 224 cells, low 10, high 18, **relief 8**, symErr **0**; `neutral` 3 562 cells, low 14, high 15, relief 1, symErr 0 |
| `03-slopes.txt` | 16 430 walked · 653 scrambled · **927 barrier** (5.3%); 18 faces, largest 116 |
| `06-claims.txt` | **placed 42, declined 0** |
| `04-routes.txt` | own keep → own core 42 blocks, **0 placed**; enemy keep → core 155–159 blocks, **39–42 placed**. All eight routes resolved |
| `05-themes.txt` | 2 ground themes, 10 distinct surface blocks; one border, `brickwork \| turf` 400 cells |
| `GET …/findings` | **empty** — no refusal, no decline, no complaint |
| `GET …/preflight` | export gate **OPEN**; round-trip · mirror · buildability · traversability all pass |
| `GET …/coverage` | reached 11 458 · decorated 1 371 · **dead 5 181 of 18 010 = 28.8%** — the lowest of the three boards, because narrowing the field is what a dead-ground read actually answers to |
| `01-flow.txt` | 5 400 of 16 400 (33%) off every route, in four flank patches |
| provenance | 22 trees · 10 houses · 6 flora · 4 strokes · 4 cores · 2 spawns = 48 owners |
