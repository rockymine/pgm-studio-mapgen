# Cutwater — the shared basin flooded, walled and bridged

**What I set out to build:** the author's own composition off the same base as `opus5-millrace` and
`sonnet-fallowmere` — a canal walled on both banks, one arched bridge across it, the four flat hint layers
replaced by real relief, and a pit for the near destroyable to sit down inside.

`specs/sonnet-cutwater`, driven 2026-08-30 off `specs/rockymine-map-experiment`. 260 × 250 blocks,
`rot_180`, 12 players, two destroyables a team, the author's own spawns and goals unmoved. `G5` fixed and
verified against `/plan/evaluate` (`piece` widened one cell, `piece-4` shifted the same amount, hop 25 → inside the 10–20 band, `G5` clear);
`GO1`/`GO2`/`GO3` read, weighed and left exactly as the base drew them, per the brief. Plan `valid: true`
at score **6.92**, export gate **OPEN**, and **nothing the dressing pass declined**.

## What it carries

| thing | how it is stated |
|---|---|
| canal wall | two open `path` shapes, radius 1.6, traced along `S0`'s own south and north arcs (one continuous chain from the south lip through the basin's tapered nose to the north lip), `height_mode: level`, sheer `y11..33` |
| bridge | a deck on its own `spans` layer, one slice per block along `z`, flush with the wall top at each shore and opening to the bed at mid-span over one pier founded at `y14` |
| water | one `pool` prop, `S0` densified and pushed outward from its own centroid so the flood reaches the relief's own graded shoreline, `level 24` |
| relief | two pushes replacing the four flat hint layers (`hill-north` +9 at `(-38,120)`, `hill-south` +8 at `(-80,8)`), a scarp cliff on the south bank, an island knoll, and a third, stronger push (-20) that sinks destroyable-1's own pit |
| houses | one `longhouse` preset (id 7) forked into a style and a diorite/jungle-wood repaint, four placements across both banks |
| trees | both forms — grown oak (broadleaf) and grown fir (`whorled: true`, conifer) plus two `template` oaks — conifer on the island's earth, broadleaf on the bank's grass |
| boulders | four erratics, two forms (`outcrop`, `angular`, `cairn`, `round`) and four sizes |
| made things | a balloon and two clouds aloft, a barge moored in the canal, a low-flying plane, a guardian statue at the north bridgehead |

## Three coordinator findings, measured and fixed

### 1. `cloud-0` landed on the terrain in one of its two images

Projecting the built columns into the isometric frame — `u = x - z`, `v = (x+z)/2 - y`, matching
`draw_iso`'s own `px = ox + (x-z)*w`, `py = oy + (x+z)*h - y*k` exactly — an isometric read is antisymmetric
in `v`: a prop off the `x + z = 0` diagonal has its `rot_180` image drawn as far above the board as the
original is drawn into it. `cloud-0` was authored at `(-15, 65)`, `x+z = 50`, nowhere near the diagonal;
`cloud-1` at `(-95, 100)`, `x+z = 5`, was close enough to clear. Rendering `ground` and `cloud-0` alone
(`layers=["ground","cloud-0"]`, full board, no clip) showed it directly: one image a clean white puff in
open sky, the other a white blob sitting on the green bank near the north wall.

**Fixed by moving `cloud-0` to `(-45, 45)`** — `x+z = 0` exactly — at `y80`. Re-rendered the same
`ground`+`cloud-0` isolation afterward: both images now read as sky, confirmed against the real renderer
rather than by eye, and `world-iso.png` shows both puffs floating clear over the spawn hall on either side.
A stateless `POST /sketch/columns` taken between edits does not reliably reflect the very latest document —
one such read produced a centroid nowhere near either authored position — so every number in this review
was taken from a document either freshly written by `build.py` and re-posted, or from `tools/drive.py`'s own
full store-and-read.

### 2. `WX11` at three, four and five blocks was not doorstep scale

The rule's own text: *"a step of one is a doorstep rather than a wall."* Before this pass, five buildings
stood on 3–5 block plinths. The fix is the test itself, not a proxy for it: for a candidate footprint, the
floor is the footprint's own lowest column, and every cell in the **one-block ring around the built
plate** — the wings' corners **plus the `longhouse` style's own 2-block foundation extent**, which is what
the first pass of this search missed and undercounted by — has to sit within the tolerance of that floor.
Searching the built surface with that test:

| house | before | after | site |
|---|---|---|---|
| `house-north-1` | 4 | 3 | `(-63,80)..(-53,88)`, floor `y28` |
| `house-north-2` | 5 | 2 | `(-45,76)..(-35,84)`, floor `y28` |
| `house-south-1` | 4 | 3 | `(-56,6)..(-48,12)`, floor `y34` |

The south bank's own relief — `hill-south`'s push, the scarp, and the grain laid over both — does not carry
a border-ring-flat site under 3 anywhere outside destroyable-1's own excluded pit, at any footprint from
6×5 up; `house-north-2`'s 2 is the one site the search found clean. Three trees (`oak-n0`, `template-oak-a`,
one boat/road check) moved with their houses to stay clear of the new footprints and the expanded water; none
of the moves changed a distance to a goal by enough to matter.

**Destroyable-1 and destroyable-2 stand at 3 and stay at 3 — this is the author's placement, not a fault.**
Destroyable-1 sits inside the pit this board deliberately dug for it (§ below); destroyable-2 sits where the
base intent's own two-goals-a-team layout put it. Neither is a house plot a search can move.

### 3. `SK10` is the bridge's own abutments, not a studio fault

The finding: *"layers 'ground' and 'spans' are driven 9 block(s) into each other over 178 column(s) —
deepest at (-87, 44) — so they build as one solid mass where they meet and the gap between the two layers
is not in the world there."* Read directly off the built columns at the two points that test it:

| column | `ground` top | `spans` (bridge) span |
|---|---|---|
| `(-87, 44)` | `y33` | `y34..34` |
| `(-87, 45)` | `y15` | `y27..34` (several courses, floor 27) |
| `(-87, 43)` | `y32` | `y33..33` |
| `(-87, 46)` | `y15` | `y24..35` |

At `(-87,44)` and `(-87,43)` the wall's own top sits **one course under the deck's own bottom** — flush,
the seam a bridge landing on its own bank is supposed to have, and exactly what `SK10`'s message describes:
solid right up under the deck, no opening. One column further in, at `(-87,45)` and `(-87,46)`, the ground
drops to the carved bed (`y15`) while the deck's floor stays up at `27`/`24` — the water runs freely under
it there. So the finding is real and it is naming the crossing's own abutments: the bridge sits on the wall
where it lands and opens where it doesn't, which is what a bridge does. `opus5-millrace`'s own review
reports the identical shape of finding at its own viaduct's landing, for the identical reason. Nothing here
says the check is wrong; the check is doing exactly its job, on ground that is meant to be solid.

## What it still complains about

| rule | count | what |
|---|---|---|
| `SK10` | 1 | the bridge's own abutments — see above |
| `SK11` | 4, ~9.3k cells total | standable ground around the moat's own graded shoreline with no authored route onto it, plus the detached island; `leave it if a detached group is what this is` covers the island outright, and the shoreline is the one bridge's own cost against a wall run the length of both banks |
| `RL1` | 2 | the `team` and island groups measure `rolling` against a stated `hills`, a label mismatch rather than a shape fault |
| `WX11` | 10 | 5 subjects × 2 mirror images: both destroyables at 3 (the author's placement, above) and all three houses at 2–3 (the search's own limit on the south bank, above) |

Coverage: `reached 21835 · decorated 1043 · dead 9403 of 32281 = 29.1% dead`, against `opus5-slipway`'s
19.3%. Fewer authored routes than a tighter board and a walled moat with a single crossing both push this
figure up; the export gate does not read it, and preflight's own traversability check — spawn ↔ objective,
which coverage does not test — passes.

## What to look at

`specs/sonnet-cutwater/renders/world-iso.png` and `world-iso-turned.png` are the board in the round, and
the ones this review's cloud fix was checked against; `world-heightmap.png` is the relief read, `hill-north`,
`hill-south` and destroyable-1's own pit all visible as real contours rather than steps;
`world-traversability.png` is the walkability read `SK11` is answering; `world-made.png` isolates every made
thing — balloon, clouds, boat, plane, statue — over nothing else, which is the one view that shows all four
mirror pairs at once. `specs/sonnet-cutwater/closeups/pit-destroyable1.png` is the pit in section-like
close-up, and `bridge-crossing.png` is the arch open under the deck at mid-span, the same opening the `SK10`
table above reads at `(-87,45)`.
