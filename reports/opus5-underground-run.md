# Opus 5 — the underground run

## What I set out to build

**One room under a hill, built properly, on a board that does nothing else.** Not a hole in the rock —
`showcase/20-undercroft` already has that — but a *built* room inside a rock-cut chamber: a floor, a wall
that is masonry rather than the mass around it, a doorway through that wall, a ceiling of its own material,
a way down to it, and props standing on its floor.

The question behind it, in the author's order: how is a hollow space made when a layer holds one span per
column; how is an underground wall drawn; and what actually reaches a room under a hill when the dressing
pass seats things on "the surface".

The board is `showcase/24-underground` — **Gaolstone**, a gaol cut into the meadow of `02-theme`. It forks
`02-theme` through `20-undercroft`: the lift (`globals.surface: 22`, the landmass thinned to `floor 14,
base_height 8`) and the banded rock are `20`'s and unchanged. What is new is the cell block inside the
chamber, its vault, its two doorways, and four props on its floor.

Everything below was measured against the running studio at `localhost:7894`. Every claim carries the
coordinate it was read at.

## What the board is

| | |
|---|---|
| extent | 100 × 100, `rot_180`, one spawn and one destroyable a side (`02-theme`'s, untouched) |
| landmass | `y14..21` |
| the rock | `y0..13`, four bands round the excavation |
| the chamber | `x −24..24`, `z −16..16` — 1,536 columns, floor `y0..5`, **8 courses of headroom** |
| the cell block | `x −8..8`, `z −6..6`, wall **3** thick, `y0..11`, vault `y12..13`, **6 courses inside** |
| the doorways | `x −2..1` through both wall bands: **4 wide, 6 tall** |
| the flight | 15 risers of one course, `y21 → y6`, one per team |
| the dressing | straw in the cell, a rubble boulder, a worn track, a flooded sump — **0 declines** |
| the gates | `GET …/findings` **none**; `GET …/preflight` **export gate OPEN** |

The whole account, with the JSON and the transects, is `showcase/24-underground/README.md`.

## What I could not say

**A light source.** Nothing in the studio places one. `PlacedProp` has six derived types — `stroke`,
`water`, `tree`, `boulder`, `flora`, `house` — and `GET /api/openapi/v1.json` carries no route, prop kind or
document field for a lamp, torch, lantern or glowstone. A cave the studio builds is dark, and the only lit
underground room it can make is one whose floor material glows. **Missing from the system**, and already
recorded as such by `review/opus5-liminal-dtm-ii.md`; this run confirms it against the schema rather than
against a memory of it.

**A prop with a stated Y.** A prop's only vertical control is `layer`; `PlacedProp` carries `Id`, `Layer`,
`Seed` and the kind's own knobs, and there is no `y`, no `floor`, no `elevation`. `DressingContext.GroundFor`
answers the named layer's surface and `SurfaceTop` otherwise. For an underground room that is enough — the
storey *is* the address — but it means a prop cannot be put on a ledge halfway up a shaft, and there is no
document shape for one. **Missing from the system**, and correctly so for a placement model that seats.

**A seated made thing in a cave.** `seat: "ground"` cannot reach a cellar: `SketchRasterizer.Seat` takes the
**maximum** `YTop` over every non-thing layer as the ground, and under a landmass that is always the roof. A
`kind: "prop"`, `seat: "ground"` layer drawn at `floor 30` inside the chamber settled to **y21..23** — on the
meadow — and cut a course out of the grass. **Out of reach from where I was standing rather than missing**:
the same layer without `seat` stays exactly where it is drawn (measured at **y30..32**), which is what a made
thing in a room wants, so the capability is there and the word is simply not for this case.

**A building inside the room.** A `house` prop takes `layer` and stamps like any other prop
(`opus5-interchange` has kiosks under a concourse). Both attempts here died on the symmetry fan —
`DR-CLAIM`, *"building 'h-under' stands on (−21, 3), claimed by the channel 'w-under'"*, where the water
pool's `rot_180` image landed on the house — and a 7 × 7 house plus its structure clearance plus `DR-PASS`'s
five-block passage does not fit beside a cell block in a 48 × 32 chamber. **Out of reach: a placement
problem, not a capability one.** I took it off the board rather than shrink the room around it.

**A tree that fits its room.** Nothing reads a room's headroom. A 12-block oak on the `under` layer at
`(13, 0)` built as a trunk from y6 to y13 with two courses of leaves at y12–13 and nothing above; the rest
of the tree is not in the world and no finding mentions it. **Present but unguarded** — the author has to
size the tree to the ceiling by hand.

**`SK9`, on any response.** This is the one that cost the most and is the most useful. See below.

## What I got wrong, and what an earlier run got wrong

**I expected `SK9` to fire and it did not — because it cannot.** The natural way to write a wall standing on
a floor is `floor 6, base_height 6` over a floor of `floor 0, base_height 6`, and it is wrong: the taller add
wins the column *floor included*, so the floor under the wall is gone and the wall bridges a six-course
trench (`GET …/column?at=-7,0` — brick y6..13, nothing below, not even bedrock). I posted it expecting a
refusal, got **200 with no `Pgm-Warnings` header**, and spent four probe boards convincing myself the gate
was broken before finding that it is raised correctly and thrown away at the boundary:
`Findings.Complaints` keeps only `Severity.Complaint` — on purpose, its docstring says so — and `SK9` is the
only `Severity.Decline` the layout check raises. `GET /api/map/{slug}/findings` names it three times.

The wrong claim looked right because *every other* sketch gate does reach the wire: `SK10`, `SK11`, `SK13`,
`SK3`, `SK4` all appear on `POST /map/from-documents`, so silence there reads as "clean". Filed as `TS68`.

**`GENERATION-NOTES.md` said a stroke ignores `layer`, and it does not.** The entry was measured off
`POST …/sketch/dressing`'s `y` field, which is documented as *"the top of that column in the world this pass
just built"* — the **column's** top, not the prop's. On a stacked board that is always the roof. My own
census answers `"y": 21` for all four of this board's props, including flora that sits at y6, and `"y": 40`
for one image whose column carries the observer platform's bedrock at y40. The world says the opposite of
the census: a `worn` stroke with `"layer": "under"` paves **y5**, the chamber floor's own top course, and
`GET …/column?at=0,10` still answers grass at y21. The entry is rewritten with the column read as its
evidence.

**I marked the wrong thing `keepClear`.** Putting it on the vault — a roof — locked the whole room under it:
the flora ring inside the cell placed **0** cells, silently, because the keep-out mask is `(x, z)` with no
layer while the claim book beside it *is* per layer. Removing the mark from the roof and leaving it on the
wall gives 13 cells and the same protection. Filed as `TS69`.

## What worked first time

- **The whole construction.** The board as designed — banded rock, chamber floor, ring wall from the floor's
  own floor, override-add doorways, a vault layer, a flight — stored at 200, raised nothing anywhere, and
  opened the export gate on the **first** post. Every column read back exactly as stated.
- **The even-odd ring, under a landmass and at every thickness tried.** Stated 1, 2, 3 and 4 all build 1, 2,
  3 and 4 columns of wall, with no gap where the slit runs and no off-by-one. A one-block ring closes.
- **The override-add doorway.** 4 wide and 6 tall, exactly the rectangle stated, on the first attempt.
- **`base_y` against an absolute `floor`.** `base_y: 12, floor: 0` and `base_y: 0, floor: 12` both build at
  y12..13; the two spellings agree to the block.
- **Props on a named storey.** Boulder, tree, flora, stroke and water all seat on the layer they name, and a
  boulder naming none seats on the meadow over the room. `DR-LAYER` names a storey the board does not have.
- **The flight at anchor 17 over a 16-cell run.** Fifteen risers of one course, head flush with the meadow
  and no repeat. The same polygon at anchor 16 gives fourteen risers, one doubled tread and a head one course
  below the grass — the arithmetic `20-undercroft` records for fourteen courses over fifteen cells, met again
  here. **Anchor the head one course above the surface it meets.**
- **`OB19` underground.** A goal's clearance reaching sixteen courses down and naming the cell it stopped at
  is exactly the answer an author can act on.

## Open gameplay questions

No oracle was available, so these are decisions rather than facts.

- **Should a goal's clearance reach into a cellar under it?** `OB19` says yes today, and it is filed as an
  observation rather than a fault: a monument on the surface and a boulder in a room sixteen courses beneath
  it cannot hide each other, so the standoff is arguably measuring nothing there. But a cellar under a
  monument is also a tunnel to it, and clear ground round the approach may be exactly right. **I built to
  the rule** and moved the prop.
- **How much headroom does an underground room want?** I used 8 courses for the chamber and 6 for the cell,
  on the reasoning that 6 is enough to jump and place a block in and 8 reads as a hall. Nothing measures it
  and nothing refuses either number.
- **Should an underground room be reachable from both spawns equally?** This board's two flights are
  `rot_180` images, so they are — but that makes the cellar a *shared* space with two entrances rather than
  either team's ground, which on a real board is a decision about the map and not about the technique.
  Recorded, not settled.

## What a next run should take from this

1. **Ask `GET /api/map/{slug}/findings` after every stacked build.** It is the only read that answers `SK9`,
   and `SK9` is the gate that knows a storey is missing. No driver asks it (`drive.py` included).
2. **State a wall from the floor's own floor, never from its top.** One number, and the difference between a
   room and a wall over a trench.
3. **Mark the wall `keepClear`, never the roof.**
4. **Read a column, never a census `y`.** On a stacked board the census reports the roof.
5. **Rock is adds banded round its holes.** A subtract is a claim about the whole stack and `SK13` refuses
   the landmass over it.
