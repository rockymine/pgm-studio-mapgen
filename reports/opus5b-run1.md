# opus5b — four boards, one per objective shape

## What I set out to build

Four boards decided together, each written as one sentence before any shape was drawn, so that no two
would be one solved arrangement in different blocks.

- **`opus5b-chalkmere`, destroy the monument.** A chalk downland split by a dry combe: each team's
  monument alone on a pale turf shoulder above its own steading, the two downs joined only by a build
  zone over the gap between them, so every attack is a crossing made in the open and the combe is the
  one place to drop out of sight once across.
- **`opus5b-slakefell`, destroy the core.** A cold slate fell in three benches over a frozen tarn: the
  core in a walled fold on the middle bench with ground on every side of it, and every way up the fell a
  cut ramp — so the raid is a climb and the defence knows the four places it arrives by.
- **`opus5b-ochredrift`, capture the wool.** A red mesa mining camp over a dry wash: two wools a team on
  spurs at the far corners, one bedrock line across each spur's mouth, and a T of void through the hub
  so a raider picks a hand at the wash and cannot change it afterwards.
- **`opus5b-alderquay`, a wool and a monument at once.** A dark alder holt on a delta channel: the
  monument in the open on the bank above a timber quay, the wool on a spur at the back behind a bedrock
  line, and the same ground carrying the raid out that the monument watches.

The tone families were checked across the set rather than within it. The grounds are **pale chalk**,
**cold slate and snow**, **red mesa clay** and **dark wet carr**; the built families are dark timber on
cobble, dark timber on brick under a red roof, pale sandstone and birch on grey, and white plaster
framed in dark oak. No board's buildings stand in its own ground's family.

## What they came out as

| Board | Mode | Walked / scrambled / barrier | Props | Dead | Gate |
|---|---|---|---|---|---|
| `opus5b-chalkmere` | dtm | 9 324 / 382 / 0, 0 faces | 30 placed, 0 declined | 9.57% | OPEN |
| `opus5b-slakefell` | dtc | 8 558 / 608 / 52, 4 faces | 28 placed, 0 declined | 6.67% | OPEN |
| `opus5b-ochredrift` | ctw | 11 118 / 318 / 128, 2 faces | 28 placed, 0 declined | **0.00%** | OPEN |
| `opus5b-alderquay` | ctw + dtm | 8 440 / 90 / 0, 0 faces | 32 placed, 0 declined | 1.55% | OPEN |

`GET …/coverage` has no gate and no card, so the dead shares are reported rather than designed around.
The one lever that moved them was the arrangement: Chalkmere's monument was already off the centre line
and the share still read 0.272 at 72 blocks wide, because one goal and one spawn a team make two
journeys and the flanks are on neither. Ochre Drift reads 0.0% over 21 journeys by construction — two
wools and a spawn a team, on a board whose ground is four narrow limbs round a hole.

## What I could not say

**A board played for a wool *and* a monument is held to `G8`'s `fill-ratio` while `approaches.md`
forbids the shape that satisfies it.** The term wants a wool board less than 54% solid over its fanned
bounding box; `approaches.md` withdraws the middle-of-terrain hole on a destroy board, because a hole
between the objectives and the middle empties the ground the contest happens on. Alderquay's first cut
read **0.768** and every way of getting it down put void where the destroy half bans it.

What I did is the only cut both allow: a channel that **reaches the mid**, so it reads as an inlet of
the strait rather than as an interior hole, which took the board to 0.520. That is **not a capability
gap** — the mechanism is there and both rules are stated. It is a **rule collision on a mode the rules
were written separately for**, and the answer I chose is a judgement.

**A prop's position is chosen from `POST …/sketch/seats`, and the raster does not know two things the
dressing pass does.** It marks a legal seat and says nothing about the ground's **angle**, so three
boulders taken off it were declined or complained about at 41°, 48° and 54° (`DR-STEEP`). And a **copied
tree's foot is not its anchor**: an acacia asked for at `(-45, 44)` was declined naming `(-44, 44)`.
Both are documented — `techniques/trees-and-boulders` says a body's foot is every cell of its lowest
course — and neither is in the raster. `GET …/column` prints the inclination on its first line, which is
what I used instead.

**`SketchShape.type` is `polyline` and the schema calls it `path`.** `GET /api/openapi/v1.json`
describes the field as *"rectangle, circle, polygon, lasso, path"* and `stroke_edge` as *"how a path's
two long edges are drawn"*; the store answers `SK3` — *"kind 'path' … is not a kind the studio draws —
it has 5 (rectangle, circle, polygon, lasso, polyline)"* — and the shape draws no ground, on a 200. That
is **mistaken rather than missing**: the instrument exists and the surface names it twice, under two
words. It cost one build.

**`HouseProp.front` takes `RoomEdge`, and I guessed `"+x"`.** The answer is a 400 naming the .NET type
rather than the four words, and the four are `negZ`, `posZ`, `negX`, `posX` in the schema. Reachable,
and the refusal does not carry the set.

## What I got wrong

**I drew the combe as a push and its floor came out at y1.** A push is arithmetic applied to the solved
surface, so minus seven under ground that solves to nine is bedrock, and the pool I put in it then cut
three courses of bank away and raised `DR-BANK`. The wrong claim looked right because the card says a
negative push dishes a ring, and it does — but the ring's floor is the solve's answer minus the amount,
and I had not read what the solve answered there. A pinned `area` mark at y7 is level, and water fills
whatever is level.

**I read `EL1` and `SP8` as faults for two builds before transecting them.** They walk the plan's pieces
flat, so a ten-block seam the relief grades over sixty blocks reads to them as a ten-block seam. Every
seam I then transected reads **worst step 1, 0 barrier, walked end to end** — both spawn egresses, all
four of Slakefell's ramps, Ochre Drift's west ramp and its flight, and Alderquay's holt-to-yard seam.

**I put Alderquay's monument on the quay deck.** `SK18` read the made thing and the goal sharing the
courses of 50 columns: the rasterizer lays a made layer and every stamper writes where it is told, and
neither reads the other. And I drew the quay's posts and its deck on **one** layer, which is `SK9` — a
layer holds one span per column, the taller add wins, and the posts were not in the world at all.

## What worked first time

**Every relief built as drawn.** Four boards, 17 `area` marks, six `line` marks and six pushes, and the
only one that came out wrong is the push named above. The `line` mark with a height at each end is the
ramp instrument at the relief tier — the evaluator suggests one itself in `EL1`'s `edit` field — and all
six read worst step 1 on a transect at the first build.

**The `anchor_heights` flight worked first time.** A polygon with `[15, 15, 21, 21]` over twelve blocks,
on a made layer of its own, built six treads two deep and read *rises 6, falls 0, worst step 1, walked
end to end*.

**`relief_scope: exclude` on a compiled shape, keyed by id.** `shapePropsById` reached the terrace the
compile fused out of four pieces at surface 21, and the face it left is the board's largest at 64 cells.
Keying on the id rather than the height is what let four pieces at one surface be addressed as one.

**Every house style stored on its second try or better, and the three refusals were all `HS`.** They
answer the store door, name the JSON path, and say what the fix is — `roofSlab` continues the body's
material, a verge is a laid log rather than a bare one, the frame is one wood.

## Open gameplay questions

**Is a void channel that reaches the mid a hole or an inlet?** `approaches.md` bans a hole between a
team's objectives and the middle and endorses a river, and Alderquay's channel is both by construction.
I built it as an inlet — it opens onto the strait across 40 blocks, so it reads as the delta's own
mouth rather than as a cut in the team's ground. If the author reads it as a hole, the fix is to close
it at `z 16` with a piece and let the water do the interrupting instead.

**Are two mirror-exact wool rooms enough of a decision on Ochre Drift?** `match-flow.md` §6.5 says which
wool falls first is then settled by the flank rather than by distance, and that both teams take the same
hand in their own frame on 68% of matches. The T of void is meant to make the two hands cost different
things — one lane is longer and the other passes the butte — but whether the difference is large enough
to move that 68% is not something this repository can answer.

**Is a building at the frontline cover or clutter?** Ochre Drift's stamp mill stands on the wash edge at
`x -24..-15, z 17..22`, which is the ground a crossing lands on. `WHAT-A-BOARD-IS-MADE-OF.md` says
nothing goes on a contested middle; `match-flow.md` §4.3 says that is exactly where the defence builds
its wall and digs its pit. The seats raster marks 216 cells for that
footprint on the whole board and most of them are on that shelf, and a mill belongs at the water; I
would take it out on the author's word.

**Should a wool room on a combined board be as deep as one on a pure capture board?** Alderquay's wool
sits 47 blocks from its own spawn and the monument 53 from the same spawn, so a team defends two things
at almost the same radius in opposite directions. That may be the point or it may be one defence too
thin; nothing measures it.
