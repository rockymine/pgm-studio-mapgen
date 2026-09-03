# Lodestar Yard — a capture-the-wool station, and the one board whose shape a rule dictated

> A CTW board on a derelict orbital dock: two wool bays a team on the ends of two arms, one gantry
> between the sides, and every ground on it a plate somebody welded rather than a soil that grew.

**In one sentence:** the fourth board of the run and the only wool one, and the deck is a **hub with
two arms** rather than a rectangle because a wool board's rules will not have a rectangle — which
turned out to be the shape with almost no dead ground in it.

126 × 210 blocks of rendered extent over a 120 × 200 plan, `rot_180` about the origin, base surface
20, ground y19..y24, masts to y36, solar wings to y58. Eight pieces a side rather than one: a spawn
berth, a hub, two arms, two wool bays, one neck, and the neutral gantry both sides cross to.

## The board

The berth sits at `(0, −90)` on a shelf pinned at y24, with its door facing the hub. Three ramps step
down four courses to the deck at y20. Two walkways run out along the arms to a wool bay at each end;
one runs down the middle to the neck, which is the board's **only** edge on the void — 40 blocks wide,
with a 20-block crossing to the gantry.

The four wools sit at `(±52, 19, ∓62)`, one pair in each dock's two bays, and each is captured by the
*other* team and carried to a monument beside that team's own spawn at `(∓6, 24, ±86)` and
`(±5, 24, ±86)`. The studio placed the monuments itself from the plan's wool placements; the plan
states only the rooms.

| Journey | Blocks | Placed |
|---|---|---|
| defender, out the berth door | 12 | **0** |
| defender, door → either of its own bays | 56 | **0** |
| attacker, spawn → west wool | 185 | 35 |
| attacker, spawn → east wool | 186 | 36 |
| attacker, spawn → its own monument | 8 | 2 (the monument's own pedestal) |

Read against its own mirror the board is fair to a block. `plan/flow` puts the attacker at 182–184
blocks against the defender's 62–67, a ratio of 0.34–0.36, and says of each bay: *"Neither side is
obviously first to it."*

## Why the board is this shape

Three refusals on the **first dry run**, none of which the three destroy boards in this run had ever
seen, and all three because this one is played for wool.

**`FR6`: `frontline-width 20 outside authored band [1, 16]`.** The rule says why in its own text:
*"On a board played for cores or destroyables there is no width cap at all (amendment 2026-09-02):
6–8 cells is the wool board's figure."* A solid rectangle a side meets the void along its whole
width, which is 24 cells. So the deck cannot be a rectangle: it meets the void at one **neck**, eight
cells across, hung off a hub — the split frontline the rule itself describes.

**`STRUCT`: `wool room is unreachable: no land seam and no abutting build zone to enter by`.** A
piece's rect is what it claims, so a wool room drawn *inside* the deck is a hole with nothing to enter
it by. Each vault therefore **abuts** its own arm along 25 blocks of shared edge, out where the arm
ends.

**`G8`: `fill-ratio 0.773 outside authored band [0.201, 0.542]`.** Not raised on the DTC board in this
run at 0.745, so the band is read against the detected mode. A yard built of arms with void between
them is **0.375**.

One change of topology cleared all three, and it is also what a dock looks like.

**And it produced the run's best dead-ground number by a wide margin.** `01-flow.txt`:

> 150 of 10600 blocks (1%) sit off every route between the places this board has. … None of it is a
> place — every stretch is under 100 blocks, which is a sliver between corridors rather than ground
> anyone would notice.

Against 28.8%, 36.7% and 40.1% on the three rectangles. A rectangle has corners no journey passes; an
arm is a corridor to somewhere, so every block of it is on the way. That is worth more than the
rules that forced it.

## What the ground is made of

Nothing here grew, so no ground here is a soil. Five grounds, and each is a different way of stating
a made surface — and four of the five patterns are ones the other three boards had no use for.

| Theme | Share | Pattern | Says |
|---|---|---|---|
| `plate` | 64.0% | **`voronoi`**, cellSize 7, five bands | straight-edged convex cells: a plate somebody welded, not a stone somebody weathered |
| `seam` | 12.4% | **`electric`**, scale 11, five stops | thin branching filaments with everything fallen away from them — glowstone and sea lantern at the core of a ramp of pale clay |
| `grating` | 9.3% | **`checker`**, size 2 | a grating, and nothing anyone would mistake for ground |
| `livery` | 7.8% | **`teamTint`** inside a `checker` | one material that reads its own cell's owner |
| `scorch` | 6.5% | `noise`, scale 8 | nether brick, coal and cracked brick: the only ground here that is not a colour somebody chose |

19 distinct surface blocks over 11 425 ground cells, against Block Realm's 10 over 18 010.

**The `teamTint` is the thing this board was built to prove, and the census is the proof.** `livery`
is *one* theme, painted on *both* docks, and its block list reads **`159:14 Red Stained Clay` and
`159:11 Blue Stained Clay`** — plus `35:14 Red Wool` and `35:11 Blue Wool` in the rim. The neutral
fallback is light-grey clay, which is why the gantry is never painted with it: a neutral cell would
fall back to the grey and the point of the material would be lost.

**One `layered` stack is the `wall` bucket of all five, and `fill` too** — the same trick
`opus5-quiverstone` used for its strata. Quartz, iron, chiselled brick, grey clay, stone brick, coal,
then obsidian beyond. So every cut face on the board shows the same beds at the same courses, which is
what a hull section looks like, and putting it in `fill` is what makes the docks banded all the way
down rather than banded in their top two courses. It is the most visible thing in the isometric.

## The techniques, and what each one bought

**No pushes at all — the first board of the run with none.** A push is applied *after* the marks, so a
dish inside a pinned pad drops whatever is pinned there, and on a deck this densely built there is
nowhere a dish can go that nothing stands in. Five area marks and three ramp lines pin every flat, and
`relief/read` answers `team` relief **5** (the berth's four courses plus one of grain) and `neutral`
relief **1**, both with symErr **0**. A hull is machined, not weathered.

**A high catwalk is an erected plate; a mast is a made layer.** The catwalks are `plate()` — a
rectangle with `override`, `height_mode: level`, `skirt: 0` and `relief_scope: exclude` — standing at
y26 over each arm's back half, six courses above the deck: a drop taken freely and a climb that has to
be placed for, which is the whole point of a high approach to a wool. The masts are `made` layers with
`seat: "ground"` and a shared `part_of`, because the build ceiling is *tallest terrain column + 20* and
a 36-course mast authored as terrain would hand the yard a ceiling above its own head.

**The solar wings hang over the void on purpose, and it is a measurement decision.** Every projective
read takes the topmost solid block and a made layer is solid, so a panel over walkable deck reports a
barrier no player will meet. Height does not help at any altitude — being off every walkable column
does. All four wings sit in the void between an arm and the gantry, and `03-slopes.txt` reads
**10 845 walked · 92 scrambled · 488 barrier (4.3%)** with 12 faces, the largest 68 cells at
`x -39..-26, z -73..-66` — the west catwalk's own sheer side.

**Every prop is a copied body, because nothing on a station grows.** Crates, dishes, conduits and
torn plate: a copied body is the one recipe that writes an arbitrary block, and it is the same escape
hatch the vines and the flat-topped platformer trees used. They are `tree`-kind props because the tree
recipes are the ones that place a thing on the ground.

## What the pass refused, and what it took to clear

Five rounds. The first three refusals are above; these are the rest.

**`RQ1`: a theme's `rim` takes a band, not a material.** The rule states the whole contract in a line:
*"'rim' names no material — rim and surface take a band, `{"material": …, "depth": N}`, and wall and
fill take a material directly."* This is how a refusal should read: it names the field, gives both
shapes, and says which buckets take which.

**`RQ2`: a voronoi's `bands` are bands, and an ill-formed list stores at 200 and throws at paint
time.** I passed `bands` a bare list of materials, by analogy with `noise`, whose `stops` is exactly
that. The document was **accepted by `PUT /sketch` with a 200**, survived the store, and died at
`GET /export`:

```
System.NullReferenceException
   at PgmStudio.Minecraft.Painting.VoronoiMaterial.Resolve(BucketContext& ctx)
      TerrainPatterns.cs:line 64
```

The schema is right and I read it wrong — `VoronoiMaterial.bands` is declared `array of VoronoiBand`,
documented as *"a material and how many blocks inward from the cell boundary it runs"*, and it even
says why it is not a `Band`. But the store gate that catches a malformed `rim` does not catch a
malformed `bands`, and `RQ2`'s own text — *"the fault is its own rather than the document's — the
detail is in the server log"* — is not reachable by an agent driving over HTTP.

**`DR-KEEP`, `DR-SITE` and `DR-ROAD`: a deck this densely walked has six places for a thing to
stand.** Two crates were declined off the berth (*"kept clear for a spawn"* — a spawn piece is
nothing but that ground), then off the hub's back corners (*"nearer than 3 blocks to the road at
(−18, −77)"* — the walkway's Catmull-Rom overshoots the outside of its first turn), and the debris
piles were declined off the arm's front edge (*"has no ground at (−23, −50)"* — the coast bend had
already cut that corner away). The crates are gone. **Eight stated props became six, and the answer to
the seventh was not to move it again.**

**`WX11`: a house stamps wider than its stated corners.** An 8 × 7 shed on a neck 15 blocks deep stood
*"20 blocks above the cell beside it at (19, −49) — 3 of them over the void"*, because its stamp
reached past the neck's bent corner. Both sheds are 6 × 5 now, with two blocks clear on every side.

## Not a fault

**The magenta in `world-surface.png`, labelled *unnamed material (3 blocks no family claims)*.** Three
block types on this board belong to no terrain-paint family: **wool** (the `livery` rim is
`teamTint(WOOL, …)`, so it is literally team wool), **sea lantern** and **glowstone** (the `seam`'s lit
core). All three are deliberate.

**28 roofed voids, 0 of them sealed.** The six large ones are the interiors of the four wool bays and
the two berths — `x -59..-47, y 20..26, z -72..-54` and its three images, and `x -8..7, y 23..29,
z -96..-85` and its mirror. A wool room is supposed to be a room, and *none is sealed*, which is the
half that matters.

**The masts read as solid columns rather than lattice.** `wall_frame` inks an edge along the top and
bottom courses and down the corners; on a 4 × 4 shaft every column is a corner, so there is no panel
left to fill. It is the material behaving exactly as documented on a shape too small for it.

## Open gameplay questions

- **`plan/flow` says of every bay: "One way in, end to end: nothing forks and nothing merges, so the
  whole approach is one road to hold."** That is the sharpest gameplay finding of the whole run, and
  it is a direct consequence of the shape `FR6` and `STRUCT` forced: an arm is a corridor, and a
  corridor has one mouth. **Decided: keep it**, because the arms are what took the dead ground to 1%
  and because a wool an attacker must fight down a corridor for is a real defensive position rather
  than an open field. But a single approach to an objective may simply be too easy to hold with 24 a
  side, and if it is, the fix is a second way onto each arm — a bridgeable gap from the neck to the
  arm's flank — which would put some void back and raise the fill ratio again.
- **Two wools a team rather than three.** Two, on opposite arms, so an attacker cannot cover both from
  one position. Whether a team can defend two corridors while attacking two others is played.
- **The crossing is 20 blocks and the neck is 40 wide.** `CT12` permits 15–40 and `FR6` wants 6–8
  cells, so both are in band, but 40 blocks of frontline for a 24-a-side team is a narrow front by the
  standards of the three destroy boards in this run, which had 100–120. Decided **narrow**, on `FR6`'s
  own reading of what a wool board is. Whether it plays as a chokepoint or a crush is the author's.
- **`decorated 0`.** There is no flora on this board — no overlay, no plants, nothing that grows,
  because a station has none. `coverage` counts `decorated` from the flora overlay, so a station
  decorates nothing by that measure while carrying six copied-body props, six houses and seven
  walkways. The number is honest and the board is not bare; they are just measuring different things.

## Coordinates

| Thing | At | Reads |
|---|---|---|
| red spawn point | `(0, 23, -90)` | inside the berth bay, door facing the hub |
| the four wools | `(±52, 19, -62)` and `(±52, 19, 62)` | in the bays at each arm's end; blue captures red's pair |
| the four monuments | `(-6, 24, ±86)` and `(5, 24, ±86)` | beside each team's own spawn |
| the crossing, at `x = 0` | neck front z −35 → gantry back z −15 | 20 blocks; build zone `x -20..20, z -35..-15` |
| the frontline | `x -20..20`, z −35 | 40 blocks — 8 cells, `FR6`'s own figure for a wool board |
| the two catwalks | `x -38..-26` and `x 26..38`, `z -72..-66` | erected plates, top y26, six courses over the deck |
| the three masts | `(±32, -70)` on the catwalks, `(-24, -10)` on the gantry | `made`, `seat: ground`, heads at y26 / y30 / y34 |
| the four solar wings | `(±40, -34)` and `(±48, -20)`, plus images | `made`, `base_y` 42 / 48 / 52 / 56, out over the void |
| the wool-bay interiors (not a fault) | `x -59..-47, y 20..26, z -72..-54` + 3 images | roofed void, **not sealed** |
| largest barrier face | `x -39..-26, z -73..-66` | 68 cells — the west catwalk's sheer side |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | **score 0**, `valid: true` — no findings of any severity |
| `POST /plan/compile` | 15 authored shapes onto `team`; 10 made layers; themes on shapes `plate 2 · grating 5 · scorch 5 · livery 3 · seam 2` |
| `POST …/sketch/relief/read` | `team` 5 406 cells, low 19, high 24, **relief 5**, symErr **0**; `neutral` 1 985 cells, low 19, high 20, relief 1, symErr 0 |
| `03-slopes.txt` | 10 845 walked · 92 scrambled · **488 barrier** (4.3%); 12 faces, largest 68 — the best of the four boards |
| `06-claims.txt` | **placed 30, declined 0** |
| walks | defender 12 + 56 blocks, **0 placed**; attacker 185–186, 35–36 placed. Symmetric to a block |
| `plan/flow` | attacker 182–184 vs defender 62–67, ratio **0.34–0.36**; one way in to each bay |
| `01-flow.txt` | **150 of 10 600 (1%)** off every route, none of it a place |
| `05-themes.txt` | 5 ground themes, **19 distinct surface blocks**; largest border `plate \| scorch` 359 cells |
| `GET …/findings` | **nothing** |
| `GET …/preflight` | export gate **OPEN**; 2 teams · 4 wools · 22 regions · 34 filters · 11 apply-rules; round-trip · mirror (`wool/room ✓`) · buildability · traversability all pass |
| `GET …/coverage` | reached 11 279 · decorated **0** · dead **146 of 11 425 = 1.3%**; largest dead patch 35 cells, 1 block from used ground |
| provenance | 16 copied bodies · 7 strokes · 6 houses · 4 wools · 4 redstone lines · 2 spawns = 39 owners |
