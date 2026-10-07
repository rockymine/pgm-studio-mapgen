# Haiku 5.5 — Bracken Vale, a destroy valley on the deployed studio

## What I set out to build

A destroy-the-monument board for two teams of sixteen, slug `haiku55-bracken-vale`, map name **Bracken Vale**,
credited to Haiku 5.5. Identity in one sentence: **an autumn river valley in which a monument stands on each
team's hub bench forty-four blocks from its own spawn, one bridged channel runs between them, and the valley's
flanks rise as terraced ground that no route needs.**

The brief's six things, and where each is:

- **Destroy board, 16 a side**: one `cube-4` destroyable a team (ender stone, float 4), `maxPlayers` 16,
  `rot_180` about the origin. Monuments at `(−57, 0)` and `(55, −2)`; spawns at `(−104, 0)` and `(104, 0)`.
- **A slow river between the sides**: one `canal` channel down the valley, `radius` 9, `depth` 4, `level` 9,
  a gravel and sand shore; one central bridge at `x −12..12, z −3..3`.
- **A watermill on each bank**: `mill-a`, an oak stilt house at `(−30,−12)→(−20,−5)` fronting the river.
  **No wheel** — see *What I could not say*.
- **Three buildings a team**: `mill-a`, `cottage-a` at `(−38,6)→(−28,13)`, `barn-a` at `(−72,18)→(−60,26)`,
  plus the spawn room.
- **One place below ground**: `cellar`, a 13 × 13 void under the hub at `(−52..−40, 14..26)` with a grass
  floor at y5, a stone roof over `z 14..22`, open over `z 23..26` so a player drops in.
- **Real relief**: hub bench at 14, two valley-side `raise` pushes; low 14, high 38, relief 24.
- **Palette**: `Savanna` (biome id 35), the autumn-golden grass and foliage tints; `meadow` and `path` themes.

The board's full account, with the coordinates a player can check, is `review/haiku55-bracken-vale.md`.
The three numbers from the final store:

```
ground   12262 walked, 2590 scrambled, 188 barrier — 18.5% steps further than a player walks
props    18 placed, 0 declined
routes   worst step 0, on route spawn-0 to destroyable-0
```

Export gate **OPEN**, no declines, one soft finding (`LN5`, below).

Pictures, by the route that draws each: the overview `render/eye?look=0,0&from=0,156&y=110&width=1280&height=720`
(also `specs/haiku55-bracken-vale/haiku55-bracken-vale.png`); the grid `plan/ascii`; the slope grid
`slopes?format=text`; the incline `incline?format=text`; the flow `plan/flow`; the coverage read `coverage`.

## What I could not say

| # | Wanted | Tried, and where I looked | Verdict |
|---|---|---|---|
| 1 | A water wheel, or a mill race, so the watermill turns a wheel in the channel beside it | `GET /api/openapi/v1.json`, searched for `wheel`, `mill race`, `millrace`, `waterwheel` and `water wheel`: zero hits in any path or schema | **Missing from the system, by name.** Not searched by function (a block that turns in a channel), so a function-level gap is not ruled out. The stilt house stands for the mill; the channel beside it is the water. |
| 2 | A walkable stair or ramp into the cellar, rather than a drop | Read the `ramp-and-stair` card's index; did not build from it; did not search the OpenAPI for a ramp or stair field | **Out of reach within this run, not shown missing.** The card names the instrument. Nothing was built or checked through a transect. The entrance is a nine-block drop. |
| 3 | A way of bringing the valley's flanks onto a route (`coverage` reads 54.4% dead, and `flow` names two stretches, about 4,900 blocks at `(0, −28)` and 4,300 at `(0, 24)`, both on the river's banks) | Narrowed the valley from `z ±52` to `z ±40`, which took the figure from 67% to 44% once; the sides rebuilt on the land's edge brought it back to 54%. Read `GET /api/plan/flow` after each change | **A judgement I could not settle within the brief.** The brief fixes the lane and the river. The only route I can see is moving an objective onto a flank, which is not the board asked for. Open question 4 below. |
| 4 | An autumn biome | `GET /api/terrain/biomes` | **Not a capability gap.** The table has no autumn word. I took `Savanna`, whose grass and foliage tints are golden. |

## What I got wrong, and why the wrong claim looked right

- **A ring over the void lifts nothing, and I had it that the sides were rising.** The first valley-side rings
  sat wholly outside the land after I narrowed the floor, and `slopes` still read as walkable hills. Nothing
  reported the sides as gone; the picture did. The fix was to put the rings on the land's edge and extend the
  land four blocks past them. *Why it looked right:* the rings were drawn where the sides should be, and the
  numbers passed.
- **`rim: {"enabled": false}` needs a material.** I wrote it to switch the rim off. The studio answered RQ1,
  "names no material", on the report and export reads for two stores. *Why it looked right:* a disabled rim is
  off, so I assumed no material was needed.
- **The biome is a `BiomeField`, not a name.** `"biome": "Savanna"` stored at 200 and then the report read
  refused it (RQ1, `BiomeField`). The fix is `{"kind": "solid", "id": 35}`.
- **A cellar's subtract height is read.** The `cutting-a-hole` card says a subtract's own height is never read,
  and that is true of the *cut*: the studio reads the courses the room is, `floor + base_height`, for `SK13`.
  My first ceiling stood above the void's top and was refused (SK13, in the dry run, so no store). The fix was
  to make the void run 6 to 11 and the ceiling 11 to 14.
- **A relief re-tops the floor of a cellar it solves over.** `SK14` (a complaint at the store) named the team
  group's terraform on the same columns as the cellar's override floor. `relief_scope: "exclude"` on that floor
  cleared it, and the cellar's columns read as I intended.
- **Mirror on an on-axis piece is refused.** I first set `mirrors: false` on the middle piece, and `PL12`
  refused the plan: a piece island may not mix copied and uncopied pieces. The middle piece is fanned onto
  itself, and that is valid.
- **Spawn one cell off its hub left the spawn door on void.** The first spawn piece sat three cells west of the
  hub, with one void cell between them, so `SP9` and the walk to the monument were unmeasurable until the
  piece touched the hub.
- **Ground that a wall's falloff reached was not the ground I drew.** Five of the declines (`DR-DIG`, `DR-ROOT`,
  `DR-KEEP`, `OB19`, `DR-SLOPE`) came from placing a prop where I had read the flat hub, and the wall's skirt
  had risen into it. The rule I should have applied is to read the dressing's `claims` and `seats` before
  placing, which I did only after the first declines.
- **Coverage was the number I left out of my first plan.** I wrote the valley at `z ±52`, and `coverage`
  read 67% dead only after the first store. The plan-level `LN5` had said so at evaluate time, and I read it as
  a note rather than as the board's width.

## What worked

These are the things that held without a second attempt, and the things that held after one named fix. The
plan did not evaluate clean the first time, so its line is after the fixes it needed.

- **The dry run before every store.** Twenty stores accepted, and the dry run named every edit each one would
  make, so no store was a surprise. Its refusal (SK13, drive 8) came back as a 422 with the rule id and the
  shape named, before anything was written.
- **Plan evaluation after fixes.** The plan evaluated `valid` after three named fixes: `PL12` (the mirrored
  middle piece), `ST9`/`ST10` (the spawn room too large for its piece), and the spawn's gap cell. The goal ratio
  on the `inspect` after the spawn fix was **3.68** (`own 44`, `enemy 162`), inside the GO1 band.
- **Symmetry on the relief.** `symmetry error 0` on the team group at every store after the walls were
  moved, read back by the driver's own `relief` line.
- **The bridge at ground level, once moved.** A deck at y12 under banks at y14 produced a worst step of 4 on the
  route to the far monument. Moving it to y14 made the worst step 0 on every route, read on the next store.
- **The cellar, after its heights were corrected.** The card's `a-room` recipe built the roofed room once the
  void, floor and ceiling heights were made consistent with `SK13`, and the column read matches the recipe.

## Open gameplay questions

These are questions `approaches.md` and `match-flow.md` do not settle for a destroy board on this shape. I
decided each one and built it, and each is open to the author.

1. **One central crossing.** The only bridge is the channel's central crossing, and every route between the sides
   takes it. *Decided:* one crossing, to make the river a decision rather than a moat. *Open:* whether a destroy
   board on this map needs a second ford for the approach to the far monument.
2. **The monument in the open.** `approaches.md` says an objective sits exposed, and the monument stands on the
   hub bench with no cover inside its ten-block clearance (`OB19` forbids a tree, boulder or building there).
   *Decided:* keep it open. *Open:* whether it should be walled on one side, the way a wool room is.
3. **A drop into the cellar.** The cellar's entrance is a nine-block drop with no way back up, and
   `match-flow.md` §10.5 has one-way ground as capture-board vocabulary. *Decided:* build it as a one-way drop.
   *Open:* whether a destroy board wants a stair back, which would cost the ramp I did not get built.
4. **Flanks off every route.** 54% of the ground is dead and no journey passes it. *Decided:* keep the valley's
   sides as terraced ground that nobody needs to walk, and report the figure. *Open:* the author's view on a
   destroy board's quiet flanks, which `match-flow.md` calls a note rather than a fault.
5. **Ratio 3.68 rather than the midpoint.** The band is 3–4, and I took 3.68 — the monument a few blocks nearer
   the enemy than the middle would be. *Decided:* stay inside the band at the point the arithmetic put it.

## What the run cost

- **Wall time** from the first request (18:48:11) to the final store (19:01:25): **13 minutes 14 seconds**. The
  driver's own runs take about three seconds each; most of the time was reading and deciding between them.
- **Stores.** Twenty accepted, changes 1 to 20 (`change 20` is the final one). One refused: **SK13** at dry-run,
  on the cellar's ceiling standing above the void's top (`drive` run 8), so nothing was written.
- **Times each document was stored**, counted from the driver's edit list on each store:
  - **plan**: stored with every store, changed on two (narrowing the valley, and extending the land past the sides);
  - **relief**: changed on eight stores (the walls, the hub bench and the valley-side rings);
  - **finish** (themes): changed on three stores (the first theme set, the cellar's floor, and the surface's
    slope bands).
- **Rule ids on refused or complained reads and stores**, from the logs: **SK13** (1, the refused store);
  **SK14** (complaints at store, cleared by `relief_scope: exclude`); **RQ1** (four reads refused before the
  material and biome were right, on two stores); **WX14** (two, before the spawn room was stated); **DR-BANK**
  (eight lines, while the river ran into a wall's falloff); **DR-ROOT**, **DR-KEEP**, **DR-DIG**, **DR-PASS**,
  **DR-SLOPE** and **OB19** (the prop placements in *What I got wrong*); **LN5** (the one soft finding that
  stayed, at plan level, and is the open question above). The **GO1** line printed on every run and passed.
- **The three numbers** on the final store: **12262 walked, 2590 scrambled, 188 barrier — 18.5%**; **18 placed,
  0 declined**; **worst step 0**.
- **Tokens.** The session counter read 15,000,000 at the start and about 14,667,000 at the last store, so the
  run used roughly **0.33 M** tokens, most of it in the reads of `ORDER-OF-WORK.md`, the technique cards and
  the OpenAPI schema.
