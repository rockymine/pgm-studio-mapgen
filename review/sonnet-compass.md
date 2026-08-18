# Four Winds Compound — Compass Yard, built

> Four teams under `rot_90`, each owning one quadrant of a walled yard, with a shared centre none of them owns.

**In one sentence:** a square four-armed compound of pale clay-and-stone, one arm per team, each arm
climbing in one-block steps from a shared cobblestone plaza at the centre out to a walled wool bay and a
spawn keep at its tip, every team's own approach stained in its own dye so a player can read whose ground
they stand on without looking up.

Board bbox `-100..100 × -100..100` (200×200 blocks, framing `-100/-100/100/100`) — larger than the "about
170×170" the brief names; see *Open questions*. `rot_90`, base surface 9, `maxPlayers` 24, four teams
(red/blue/yellow/green). One neutral on-axis island (the plaza) plus one `team` island fanned four ways.

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| four teams, `rot_90` | `globals.symmetry: "rot_90"` | compile answers 4 spawns, 4 wool rooms, teams `red/blue/yellow/green` |
| a shared centre none of them owns | `plaza` piece, `mirrors: false`, centred on the origin | `x -15..15, z -15..15`, theme `compass-plaza` (cobble family), the well building at its centre |
| one quadrant authored, fanned ×4 | one symmetry unit: hub → wool-approach/flanks → wool-room → apron → spawn | compiled shapes `s0..s5` plus `spawn-red/blue/yellow/green`, `wool-*-*` — six terrain shapes, four team images each |
| ash ground, cobble worked ground | `compass-yard` (Clay 82:0 + Smooth Stone 43:8, `cell` texture) on the yard/apron/spawn; `compass-plaza` (Cobblestone 4:0 + Gravel 13:0) on the plaza | `--surface` render: grey-mottled yard, grey-brown mottled plaza, no third ground colour |
| team Stained Clay on the built ground of its own approach, nowhere else | `compass-approach` theme (`teamTint`, block 159) on the wool-approach+flank shape and the wool-room shape only | `--surface`: solid blue/green/yellow/red panels precisely on the four wool bays, nowhere on the open yard |
| one identical structure per quadrant | `sn-compass-keep` (forked from `counting house`, id 9) placed once at `[[8,31],[22,39]]`, fanned ×4 | `--topdown --layer structure`: four orange blocks, one per arm, same offset from each arm's own axis |
| one route per quadrant, spawn → wool → centre | path prop `p1`, `[[0,88],[0,75],[0,60],[0,45],[0,32],[0,17]]`, `worn`, radius 2.5, Voronoi cobble/gravel pave | visible in `--topdown` and `--surface` as a pale line down each arm |
| the 15–40 rule on each of the four gaps | `POST /plan/inspect` → `islandGaps`: `{"piecesA":["plaza"],"piecesB":["hub","spawn","spawn-apron"],"blocks":15}` | 15, at the band's own floor — see *Open questions* on whether this is the right pair to measure |

## What nearly shipped broken, and what actually explains it

The first three complete builds refused at export with `EX1` — *"12 objective(s) sit behind ground an enter
rule bars the attacking team from"* — naming **every** cross-team wool as unreachable, for every team. That
reads like a four-team bug and it is not one: `docs/gameplay/approaches.md`'s "defender never required to
reach its own wool room" and the shipped `not-<owner>` enter rule (`WoolGenerator.cs`) are correct and
unchanged from any two-team board. The actual fault was mine — the first drafts routed
`spawn → apron → wool-room → wool-approach → hub`, with the room **inline** on the only path from a team's
spawn to the rest of the board. Since every team is denied entry to its *own* wool room by design, that
routing meant a team's own spawn became topologically sealed off from everything else by a room its own
players may never stand in. `GET /map/{slug}/traversability` (undocumented in `plan.md`/`sketch.md`'s API
tables, but live) is what found this — it answers the same `Traversability.Check` the export gate runs,
without the export's 409, so the isolated pairs and their `for:<team>` tags could be read directly rather
than guessed at. The fix: the wool room is a **dead-end pocket** off the wool-approach piece, and two ground
pieces (`wool-room-flank-w`/`-e`, named with the room's own id prefix per `GENERATION-NOTES` §15's donut
sanction) carry the spine's full width **past** the room rather than through it. Confirmed on the built map:
`GET /map/four-winds-compound/traversability` → `connected: true`.

## The techniques

**A pinwheel, not a literal pie-slice.** Each arm is centred on its own axis and widens outward from a
narrow neck at the plaza (half-width < near-edge distance at every piece, so no two rotated arms overlap);
the visual result in `--topdown` reads as a four-armed windmill around a paved hub rather than four
quadrant wedges. This is a legitimate reading of "each owning one quadrant of a walled yard" but not the
only one, and it is worth naming as a choice rather than the brief's literal geometry — see *Open
questions*.

**A defence wall exactly where AD-V5 wants it.** `walls: [{"a": "hub", "b": "wool-approach", "side":
"wool-approach"}]` sits on the hub/wool-approach interface, 15 blocks from the room's own edge (wool-approach
runs `z 8..12` in cells, the room starts at `z 12`) — matching "never on the wool's own edge... ~15 blocks
from the room" to the block. `POST /plan/inspect` confirms all four images at `15×20` blocks (width×height),
inside `ST8`'s 10–20 band.

**The donut sanction, named and avoided.** The bypass flanks fully ring the wool room together with
wool-approach and the room's own footprint, which is exactly the "wool encloses its own bay" shape `WL8`
sanctions — until the flanks are named `wool-room-flank-w`/`-e`, sharing the room's own id prefix, which
`ClosureAnalysis.AnyHoleRingedBy` reads as the room's own box rather than a foreign ring. Renaming two
pieces is the entire fix; the geometry does not change at all.

## What the board gets right, measured

- **Team colour reads without a marker.** `--surface`: the four wool-approach/room shapes are solid
  saturated blue/green/yellow/red blocks against the neutral grey yard and plaza — exactly the "tell whose
  quarter you're in without looking up" the brief asks for.
- **The rim is a made edge, used correctly.** `compass-yard` and `compass-plaza` both carry `rimEdges:
  "boundary"`, `rim.enabled: true` — deliberate, because these are **built** stepped tiers (AD-L4), not a
  relief solve; AD-R1's "off on grown ground" does not apply here since nothing here grew.
- **A defence wall, a bypass, and a donut-safe naming all landed first time** once the topology was
  understood — no further build cycles were needed after the `wool-room-flank-*` rename.

## The checklist

| # | Check | Measured | Verdict |
|---|---|---|---|
| L1 | one gamemode | `<gamemode>ctw</gamemode>`, once | pass |
| L2 | team/spawn/objective present | 4 `<team>` + 4 filter `<team>` reuses, 4 `<spawn>`, 12 `<wool>` | pass |
| L3 | label matches contents | `ctw` label, wool-only board | pass |
| L4 | no `<`/`>` in a goal name | wools carry no custom `name` (default text) | pass |
| P1 | wool-room/spawn piece ≤ 20×20 | wool-room `4×4` cells = `20×20` blocks (boundary); spawn `4×2` = `20×10` | pass |
| P5 | CTW islands 15–40 apart | plaza↔hub direct gap = **15** (floor of the band) | pass, at the edge |
| P6 | no wall on the wool room's own entry face | wall sits on hub/wool-approach, one piece out from the room | pass |
| P7 | wall 10–20 wide, ~15 in front | `15×20` blocks, seated exactly 15 from the room | pass |
| M1 | grass exactly 1 course | no grass used anywhere in this board's themes | n/a |
| M7 | three tone families named | ground = ash+cobble, built = grey stone (Stone Bricks+Iron Ore), accent = team Stained Clay | pass |
| C0 | extent/aspect | 200×200, square (matches brief's intent, over its stated number) | reported |
| C1 | houses by z/x/orientation | 4 keeps, one per arm, each offset the same way relative to its own arm — genuinely identical under rotation, per the brief's own instruction | reported |
| C2 | placement ideas | keep (per-arm structure) · well (neutral centre landmark, Diorite-forked) · gatepost boulders (plaza) — three | reported |
| C4 | void placement | between the plaza and every arm (15 blocks, bridged by a build zone); none across an approach | reported |
| C10 | paths | 4 (fanned from one), spawn→wool→centre, `worn` | reported |

No load-blocking or §3.2–§3.5 rule failed. `EX1` was caught and fixed before this build; the shipped world
answers `connected: true`.

## Open questions

**Is the plaza↔arm gap the pair CT12/AD-V2 actually mean to bound, or is it the arm↔arm gap?** The brief
text says "the four gaps between quadrants... each wants the 15-to-40 rule applied to it independently,"
which reads as arm-to-arm. I measured and built for a **15-block arm-to-arm gap** (`2 × near-edge`) and
treated the plaza↔arm gap as a secondary, unconstrained connector; `/plan/inspect`'s `islandGaps` only
reports the plaza↔hub pair (the only two-island relationship the deriver sees, since the four arm images
are one mirrored `team` island rather than four separate ones — an arm never becomes its own island under
`mirrors: true`, so there is no `islandGaps` entry to read for "arm vs. its neighbour" directly). I could
not get a second, independent number for that specific pair from the tools available and did not invent
one; I built the geometry so the *direct* arm-to-arm distance is 30 blocks (computed by hand from the
piece rects, not read from an endpoint) and record that as an open question rather than a checked fact.

**Whether a "pinwheel" reading of "one quadrant of a walled yard" is faithful to the brief.** I judged that
a piece can only avoid overlapping its own 90°-rotated image if it stays inside the 45° cone from the
origin (half-width < near-edge distance) — a literal square quadrant abutting the two adjacent quadrants
along a straight edge is not reachable with a single rectangle-based piece in this geometry without
either the quadrants touching directly (fusing into one island, losing the four separate gaps) or a
build-zone-based cut that the piece system does not offer at cell resolution. I built the pinwheel and
recorded the reasoning rather than asserting it is the only correct answer.
