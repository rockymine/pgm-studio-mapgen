# Medlock Drift — a benched tip and a bridge only the defence uses

> Adapted from `GET /api/compose?players=20&symmetry=mirror_z`, **seed 34**, composer
> `markers-in-blocks-1`, cell 5. Composed score 1.548; structure **hub `double-hole` · frontline
> `twin` · wools `l`, `clamp`**.

**In one sentence:** a drift mine in red shale where the only two flat places are the pit floor at the
front and the mine yard at the back, everything between them is a spoil bank benched two blocks at a
time, and the spawn has a second exit that goes nowhere an attacker can follow.

105 × 190 blocks — the smallest of the four — `mirror_z`, base surface 12, observer y 44. One ground
group, 5 480 solved cells.

## What the composer gave and what it became

| The composed board | This board |
|---|---|
| wool-a 134 blocks from the enemy's door, wool-b 104 — **1.28×** straight-line (150/151 by walk, which was already level) | 167 and 164 — **1.02×** straight-line, 182/185 — **1.02×** by walk |
| spawn off the hub's **east flank** | spawn off its **back**, so the two wools can sit at one depth on the two flanks |
| exactly one zone, the mid band, offset east | **two 25-block crossings** with twenty of void between them, and a third zone that is nobody's but this team's |
| both frontline tips 10 blocks wide (`FR9`) | the front drawn out west to 25 and 25, with a scalloped bay between them |
| no elevation anywhere | a spoil bank benched at `step: 2` — 1 854 scrambles, **126 barrier** |
| every piece an axis-aligned rectangle | one 28-vertex compiled ring taken to 30 by hand and bent; all three composed holes redrawn as rounded shafts |

## The defender-egress bridge

`egress` is a 15 × 10 build zone from the spawn piece's west side to `back-pad`, a small apron that
hangs off the west wool's own approach. **Every interfacing component of it touches this team's ground
and no other**, which is what `BZ5` calls the defender-egress bridge — *the spawn's second exit, mainly
for defenders rotating to their wool while attackers push the crossings*. `POST /plan/evaluate` names
it in as many words: `[complaint] BZ5 build zone 'egress' touches spawn piece 'spawn-room'`. The
prohibition is retired; the complaint is the motif being recognised.

It goes to the **west** wool and not the clamp, and that is the whole of the design. Without the
bridge the west wool is 85 blocks from its own door by walk and the clamp is 75 — `WL9`'s
`spawn-wool-ratio` out of band. With it the two read **49 and 52**. A shortcut that shortens the wrong
walk makes a board *less* balanced, and my first version put the bridge on the clamp's side and read
34 against 57.

Zones are not fanned by the plan's symmetry, so `egress-2` is authored by hand as this one's
`mirror_z` image.

## The mid, cut in two

`crossing-e` at `x −5..20` and `crossing-w` at `x −45..−20`, twenty blocks of void between them, both
30 blocks long. The two landings lead to different halves of a double-slotted hub, and the far one
lands on ground from which the only way on is the west flank. The composer's own mid band is offset
east; this keeps the offset rather than centring it, and adds the flank.

## The benched tip

`relief.team` states **no marks** and one push, and the board's character is `step: 2`. `ReliefSpec.Step`
snaps the finished surface to a quantum — the thing that ruins a hillside and the thing a worked spoil
bank is made of. Every stated level is a multiple of it or the knob rounds it away: base 12, `amount`
6, `crown` 6.

Read back: **8 980 walked, 1 854 scrambled, 126 barrier**, 11 faces, largest 25. A scramble is a
two-block step — crossable with a placed block, which is what every player on a wool board is carrying.
`level 0.709`, `largestField 0.264`, `faces 0`, `cliffs 0`, `seams []`. The push reads
`skirt 0.67 · crown 0.46`.

**`GENERATION-NOTES.md` describes a `stairs: true` companion to `step` that *"cuts a way up out of
every place the terracing stranded"*. It is not on the wire on this branch**: `SketchReliefJson`
carries `base`, `reach`, `step`, `landform`, `grain`, `marks` and `pushes` and nothing else, checked in
`GET /api/openapi/v1.json`. The board is authored without it and the benches are scrambles rather than
stairs.

## Where the made ground meets the grown ground

Two excluded floors and a portal between them.

- `pit` — a ten-vertex polygon at `base_height` 12, `relief_scope: "exclude"`, over the whole front:
  the ground this board is fought over, flat to its own edge and out of the solve.
- `yard` — the same at the back, under the spawn.
- `portal` — `base_height` 16, its own `drift` theme, grey polished andesite against the red: the
  adit's mouth where the tramway leaves the pit floor.
- two `incline` flights, twelve blocks of run for four of rise, and two `polyline` revetments along
  the back of the pit, which is what holds a worked face up.

`SK13` refused the first build: `incline-e` reached four columns into the hub's east slot, and a
subtract is the board's statement of its own negative space — an override add beats a subtract on its
own layer, so the hole would simply have been filled. The flight stops at `z 48` and the slot's
redrawn octagon starts at `z 50`.

## What the ground is painted with

Three families: the **ground** is red — red sand, red sandstone, hardened clay, coarse dirt, with coal
in the body of the rock where nobody sees it until a wall is cut; what is **built** is pale birch over
cobblestone, the only light thing on the board; the **accent** is grey andesite, on the portal and the
erratics and nowhere else.

`shale`'s surface is a `layered` material on the **`slope`** axis cut at 24° and 40°. `GET …/incline`
reads 65.9% under 10° — the benching makes a lot of level plate — 6.9% at 10–19°, 15.2% at 20–29%,
6.4% at 30–39° and 5.6% at 40° or steeper.

`themes/census`: `shale` 8 184 cells (74.7%), `working` 2 616 (23.9%), `drift` 160 (1.5%); 456 cells of
drawn border between the shale and the workings and 72 between the drift and the shale. Nothing
registered painted nothing.

The biome is **Mesa** (`#90814d`), chosen because the ground carries podzol and a dry brown grass tint
is what meets it; on `Plains` the pair reads as neither ground.

## The numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, valid; `SP2` and `BZ5` complaints |
| `GET …/preflight` | **export gate OPEN**, per team |
| `GET …/coverage` | reached 8 481, dead 133, **1.5% dead** |
| `03-slopes.txt` | 8 980 walked, 1 854 scrambled, 126 barrier; 11 faces, largest 25 |
| `06-claims.txt` | placed **22**, declined **0** |
| relief `team` | `low 12 · high 24 · level 0.709 · largestField 0.264 · faces 0 · seams 0 · symErr 0` |
| flow, attacker | 182 and 185 — **1.02×** (composed: 150/151 by walk, already level; straight-line 1.28× → 1.02×) |
| flow, defender | 52 and 49 — 1.06× |

## What went wrong

- **The bridge went to the wrong wool.** A shortcut to the *near* objective is what `WL9` is about, and
  my first version read 34 against 57.
- **`SK13` on the east incline** — four columns into the hub's slot.
- **`PT1` on podzol**, the same fault as Kettleshulme's: a surfacing block is exactly one course and
  may not lie under turf.
- **`stairs: true` is not a field**, and I authored it before reading `openapi.json` for it.
- **Three boulder positions were declined in two passes before I stopped picking cells near a run's
  edge.** The dressing pass seats a prop a block or three off the position stated and judges it at
  every image of its orbit, and `sketch/seats` answers for the exact cell: `(24, 48)` reads 1 in the
  mask and the rock was placed at `(26, 46)`, which is over the coast. The board carries three
  erratics rather than four for that reason.

## Open gameplay questions

- **Is a two-block bench across most of a board playable?** 1 854 scrambles and 126 barriers says every
  step is crossable with a placed block and nothing is impassable, which is the right answer for a
  worked tip and the wrong one for a board somebody has to sprint a wool across. I built it because
  the ground is what the board is about; this is the decision I am least sure of.
- **The far crossing lands somewhere the attacker can only go on from by taking the west flank.** I
  meant it as a real choice and not a trap. Whether it reads as one is a question about play.

## Coordinates

| Thing | Where |
|---|---|
| spawn (red) | `(0, 12, 87)`, door `−z` |
| wools (red) | `red` at `(40, 12, 75)` — inside the clamp — and `orange` at `(−45, 12, 70)` |
| the egress bridge | zone `x −20..−5, z 80..90`, fifteen blocks of void |
| the two crossings | `x −5..20` and `x −45..−20`, `z −15..15` |
| the clamp's yard | `x 34..46, z 64..71` |
| the hub's two slots | `x −12..−3` and `x 4..16`, both about `z 50..60` |
| the pit floor | `x −38..18, z 18..38`, top y11 |
| the drift portal | `x −4..6, z 40..48`, top y15 |
