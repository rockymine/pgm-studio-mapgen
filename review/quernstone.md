# Quernstone — the measured record

> A four-team capture board that pinwheels. Each team is a north-pointing wedge — a **U frontline** of two
> tips straddling the axis, a **double-hole hub** behind it whose two holes are the route fork, an **L**
> wool lane and an **I** wool lane, a spawn alone at the end of the spine — and the four images turn about a
> single neutral millstone at the origin.

`rot_90`, 4 teams, 32 players, 216 × 216 blocks, base surface 12, build ceiling 32, ground y 9..47.
The authored unit is **17 pieces, 151 ground cells**.

## What `rot_90` asked for that `rot_180` did not

**The unit has to clear its own image.** A piece at `(x, z)` has an image at `(z, −x)`, so a wedge that
reaches out along one axis collides with itself a quarter-turn later. Checked before posting: four images,
**no overlapping cells**, closest approach 2 cells (10 blocks). The wedge points north and leans west,
leaving the eastern strip for the next team.

**The frontline sits on the axis, and that is what builds the mid.** `CT11` licenses it and `CT10`'s **plus**
archetype needs it: the frontline box straddles `x = 0`, its four images abut at the axes, and the square
they leave is the middle. The quern sits in it, on the origin, `mirrors: false`, so it compiles to its own
`neutral` island rather than being fanned four times onto itself.

**No destroy objectives exist here.** `PlanCompiler` fans a destroyable or a core only at orbit order 2, so
a four-team board is capture or nothing.

## Measured

| | |
|---|---|
| gamemode | `ctw` |
| teams / spawns | 4 (Red, Blue, Yellow, Green) / 4 |
| wools | 2 rooms a team, 8 rooms, 24 `<wool>` elements — each room a target for the other three teams |
| walls | 4 — one a team, across the east wool lane, full lane width, Δ 0, void both sides |
| dressing | 4 leats, 20 paths, 48 trees, 24 boulders, 16 flora rings, 8 houses (the unit's, fanned) |
| evaluator | **score 0.0, `valid: true`, no term fired on the first compile** |
| traversability | 17 970 navigable columns, 1 072 bridged, 10 components, **12 of 24 markers isolated** |

**Twelve isolated markers is four walls working.** Each team's east wool sits behind a bedrock line that
seals its lane, and three other teams must capture it: 4 × 3 = 12. Each team's west wool is open and reads
connected.

## The two things the mid and the hub actually do

**The hub's holes are a route fork, not decoration.** A player leaving the frontline has three ways to the
wool entrances — round the west hole, through the solid core between them, round the east hole. The spine
road is paved through the **core**, the middle of the three, so the two ways round it are the ones taken
when the road is watched.

**The quern is a diagonal switch.** With two frontline tips, a stone in the middle lets an attacker leave by
one tip and arrive at a different enemy face rather than at the one directly opposite. On a four-team board
that is a choice of *which neighbour to attack*, made at the pivot.

## The finish

Three themes, assigned by fused-shape height: `grit` (gravel and andesite in a voronoi) on the contested
ground — the quern and all eight frontline tips, so the middle reads as bare millstone from every side;
`hag` (dirt and podzol) on the wool runs; `moor` (heather turf, mossy-cobble rim, granite-and-andesite
scarps) on everything else. Coasts bowed by the generated-handle rule, seams and wall surrounds left
straight. The frontline tips shelve 12 → 10 into the mid. Relief on the hub alone. A leat across each
team's spine, forded by its road.

## What is still open

**The quern is small for a four-way pivot** — 20 × 20 with two cairns, 10 blocks off each of eight tips. It
works as a switch and it leaves whoever stands on it exposed from four directions at once.

**The four teams are identical and `rot_90` makes that more visible than `rot_180` does.** Nothing differs
between them but the coast bows. The two wool approaches differ as an L from an I; on a four-team board they
could differ more.

**No build zone spans a hole.** The recess between each pair of tips is a `CT9` buffer hole and the hub's
two are the fork; a hole a build zone spans — a route that opens only when someone bridges it — is the one
form on the menu this board does not use.
