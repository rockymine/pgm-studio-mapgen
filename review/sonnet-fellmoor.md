# Fellmoor Common — a GO1/GO4 test board, built

> A grazing common split by a spring-fed beck: two cairns stand on their own barrow behind a fold, a
> stonemason's hall and a darkwood croft close behind each spawn, a sandy-mushroom mill stands by the
> ford, and a turf causeway is the only way across the beck to the enemy's ground.

80 × 250 blocks, `rot_180` about the origin, base surface 9, one destroyable a team. Built specifically to
put the two just-wired distance rules — `GO1` (a goal's spawn ratio) and `GO4` (a goal's own-spawn
distance) — on live ground and watch `POST /plan/inspect` and `POST /plan/evaluate` score them, then built
a second time over, once the first pass turned out simple to the point of dodging its own findings.

## The two rules, live

| Rule | Reads | Band | Verdict |
|---|---|---|---|
| `GO1` | enemy÷own spawn walk | `[3.0, 4.0]` | **3.31** — `POST /plan/inspect` |
| `GO4` | own-spawn walk | `[40, 90]` blocks | **55** — `POST /plan/inspect` |

`POST /plan/evaluate` scores the plan **0**, `valid: true`, empty lint. `GO4` shipped today with only
synthetic TUnit fixtures behind it; this is the first real board it has ever scored. The own-spawn walk
(55) sits close to the band's centre and the pgm-studio corpus sweep's own median (55.5, cited in `GO4`'s
own `rules.md` entry) — not tuned to that number on purpose, but a reassuring coincidence. Neither number
moved between the two passes: everything added in the second belongs to the finish, not the plan, and the
walk is measured over plan geometry alone.

## The second pass — what the first one dodged

The first build hit `SP8` (a raised spawn's egress steps 4 blocks to the lane) and answered it by dropping
the spawn flush instead of carving the ramp the rule was pointing at. That was the easy way out of a
finding built to be worked, not routed around, and the board was left looking exactly like what it was: a
lane, a spawn, a goal, nothing else. Second pass:

- **The ramp got built.** Spawn back up to `surface 13`; a `spawn-ramp` shape (`height_mode: level`,
  `anchor_heights [13, 9, 9, 13]`, `relief_scope: exclude`) climbs it over `z 95..105` — 10 blocks of run
  for 4 of rise, a 2.5:1 grade, painted `worn` so it reads as a trodden approach rather than a floating
  ledge.
- **The cairn got a barrow.** Where the first pass held its ground flat with one `area` mark, this one adds
  a `push` — `ring` 28×28 about the goal, `amount 3`, `falloff 8`, `crown 2` — so the plinth rises into an
  actual mound rather than a plateau with square corners. `relief/read`'s high climbed `10 → 14`.
- **A worn track runs the map.** One `path` prop (`route: true`, `style: worn`, the same `terracotta with
  dirt` pattern as the cairn's ring) follows the lane's own centreline from the spawn door through the
  ring and down to the causeway — drawn, per the authoring brief, before the scenery went in around it.
- **A short stream.** `beck-water`, a 3-point `stream` channel over the relief line's low stretch
  (`z 34→14`), the one place the terrain was already heading that way.
- **Sixteen trees and two boulders**, eight oak/birch a flank, on two new `worn` verge strips either side
  of the lane (`x -20..-11` and `11..20`) — not decoration alone. `clay grassland`'s fill palette carries
  **green wool** as one of three cell materials, and wool is on `DressingPalette.IsStamp`'s list (with
  bedrock, obsidian, the metal blocks, glass and air) — a column topped in it reads to the dressing pass as
  a *stamp*, not terrain, and every tree and boulder first placed straight onto the grassland declined with
  `DR-KEEP` naming it "built ground rather than terrain". The verge strips are wool-free by construction
  (dirt/stone/terracotta only), which is what let anything root there at all — worth knowing before
  scattering flora on this theme again.
- **A third house.** `sandy mushroom` (`HousePresets.Authored`, the one preset the first pass left unused)
  stands at the ford, `(10..16, 18..24)` — all three authored houses are now in the board: `stonemason` as
  the spawn hall itself, `darkwood` as the croft, `sandy mushroom` as the mill.

## What went wrong, both passes

1. **`ST9`** — the first spawn piece was 50×15; the cap on a role piece is 20×20. Shrunk to 20×20.
2. **`DR-SITE`**, twice — the croft's footprint first poked past the lane's void edge, then sat under the
   spawn door's kept-clear approach. Walked it inward and down the lane.
3. **`DR-KEEP` (Built)**, ten times over — every tree and one boulder, landing on a wool-topped cell of
   `clay grassland`'s own fill (above). Fixed by painting their ground `worn` instead of moving them one by
   one; the last boulder needed its `outcrop` form swapped for `round` — outcrop's mask perturbs wider than
   its stated `size` states, and was the one shape still catching a wool cell at a stated size and position
   that should have cleared it.
4. **`WX11`**, twice, left as-is — the croft stands a few blocks proud of the ground just north of it,
   where the cairn's new mound and the spawn's approach margin meet and the relief solve grades unevenly
   between them. A complaint, not a decline; the building is in the exported world.

## What is not settled

Dead ground fell from **27.2% to 13.6%** (`GET /map/sonnet-fellmoor/coverage`) once the flanks carried
trees, boulders and a worn margin — closer to reached than not now, though still short of the wheal-hazel
v2 answer (narrow the lane to the route's own width) if that share ever needs to hit zero. The two `WX11`
complaints above are the other open item: moving the croft another few blocks off the mound's falloff, or
levelling a small verge under its foundation with its own `area` mark, would clear them.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red spawn | `(0, 115)`, protection `-10..10, 105..125` | stamped `stonemason`, y13, ramp down to the lane |
| red cairn | `(0, 63)` | obsidian, `pillar-3`, floats 4, on a pushed barrow (crown ~y14) |
| red croft | `(8..14, 78..84)` | `darkwood`, fronts `-z` |
| red mill | `(10..16, 18..24)` | `sandy mushroom`, fronts `-x`, by the ford |
| worn track | `(0, 103) → (0, 12)` | `route: true`, radius 3, follows the beck's own line |
| beck (water) | `(2, 34) → (-1, 14)` | stream, radius 2, depth 2 |
| tree verges | `x -20..-11` and `11..20`, `z 15..100` | 8 oak/birch a flank, `worn` ground beneath them |
| causeway | `x -40..40, z -10..10` | build zone over the beck's low point, 20-block strait (`CT12`: 15–40) |
| blue spawn / cairn / croft / mill / trees | the `rot_180` image of each of the above | symmetry error `0` (`relief/read`) |

Built via `tools/drive.py` against a freshly migrated local database; nothing here changed anything the
API didn't already expose. Full documents in `specs/sonnet-fellmoor/`, renders in
`specs/sonnet-fellmoor/renders/`.
