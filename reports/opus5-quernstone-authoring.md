# Quernstone — a four-team board, authored from the concepts rather than from scratch

Third map in this sequence and the first that did not begin by getting the structure wrong. `coldharbour`
was rebuilt after review into `coldharbour_v2`; this one starts from the vocabulary that rebuild taught and
applies it at `rot_90`, where the fan is four images instead of two.

`pgm-studio` at `14fb4a653f164dfc9a884ec1baa1cf646cae34ab`, working tree clean, untouched.

---

## 1. Two corrections carried in from the review

Both of these were claims I had written into `review/coldharbour_v2.md` as open problems. Both were wrong,
and the corrections are what the mid and the hub of this board are built on.

**The hub's holes were never decoration.** I had written that "no route passes between them that a player
would choose over the bar". That misreads what a hole does: a double-hole hub gives a player leaving the
frontline **three ways** to the wool entrances — round the west hole, through the solid core between them,
or round the east hole. It is a route fork, and the fork is the point. On this board the spine road
deliberately takes the **middle** of the three, so the two ways round it are the ones a player chooses when
the road is watched.

**The mid stone was never one crossing.** I had written that "every route over it is the same route". With
a frontline that has two tips, a stone in the middle is what lets an attacker leave by one tip and arrive at
a *different* enemy face — the diagonal switch. Straight across is only the cheapest of the routes it
offers, not the only one. On a four-team board that matters twice over: the quern is the pivot at which a
player can change which neighbour they are attacking.

## 2. What `rot_90` changes

Everything in `coldharbour_v2` applies, and three things do not.

**The unit is a quadrant wedge and it must clear its own image.** Under `rot_180` a piece and its image are
far apart by construction. Under `rot_90` a piece at `(x, z)` has an image at `(z, −x)`, so a unit that
reaches out along one axis collides with itself a quarter-turn later. The check is four lines and I ran it
before posting anything:

```
unit ground cells: 151
orbit-image overlaps: none — the four images are disjoint
closest unit cell to an image cell: 2 cells = 10 blocks
```

The board is therefore authored as a **north-pointing wedge leaning west**: the frontline straddles `x = 0`,
and everything behind it is kept west of `x = 2` and north of `z = 4`, which leaves the eastern strip free
for the next team's image to occupy.

**A frontline may sit on the axis, and that is what makes the mid.** `CT11` grants exactly this licence —
*"a frontline may straddle the x=0 / z=0 axis, and its four fanned images abut cleanly at the axis"* — and
it is the only way to build `CT10`'s **plus** archetype. The frontline box here spans `x −20..10` across
`z 20..35`; its four images make the plus, and the square they leave in the middle is the mid.

**Destroy objectives are unavailable.** `PlanCompiler` fans a destroyable or a core only at orbit order 2,
so a four-team board is a capture board or nothing. That is a hard constraint, not a preference, and it
decided the gamemode before the first rectangle was drawn.

## 3. The board

```
  20 |               SSSS         |   spawn, alone at the end of the spine, facing the mid
  17 |         WWW   SSSS         |   L wool lane west (dead end)
  14 |         999   CCCC   WWW   |   I wool lane east — the wall crosses it at z 11
  12 |         88887777777777 BBB |   hub back bar; both lanes and the spine dock onto it
  10 |             44  55  66AAAA |   two holes, solid core between them — the route fork
   8 |             3333333333     |   hub front bar
   6 |                 11..22     |   U frontline: two tips, buffer recess between
   3 |                 ++++++++   |   the band
   1 |                 ++0000++   |   the quern — one neutral stone, on the axis
```

and fanned, the four images pinwheel around it. Team **Red** is that wedge; **Blue**, **Yellow** and
**Green** are the same wedge at 90°, 180° and 270°.

| | |
|---|---|
| symmetry / teams | `rot_90`, 4 — Red, Blue, Yellow, Green |
| extent | 216 × 216 blocks, ground y 9..47 |
| unit | 17 pieces, **151 ground cells**; 604 fanned plus the 16-cell quern |
| wools | 2 rooms a team, 8 rooms, 24 `<wool>` elements — each room is a target for the three other teams |
| spawns | 4, one a team, each alone at the end of its own spine |
| walls | 4 — one a team, across the east wool lane |
| evaluator | **score 0.0, `valid: true`, nothing fired** |
| traversability | 17 970 navigable columns, 1 072 bridged, 10 components, **12 of 24 markers isolated** |

**Twelve isolated markers is the wall working, four times.** Each team's east wool sits behind a bedrock
line that seals its lane; three other teams have to capture it; 4 × 3 = 12. The west wool of each team is
open, and reads connected.

**The evaluator fired nothing on the first compile.** Not iterated to: the board was drawn to the shapes
`model.md` names, and `rot_90` was checked for self-collision before the plan was posted.

## 4. What the sketch does with four images

The same passes as `coldharbour_v2`, and one of them behaves differently at `rot_90`.

- **Three themes, assigned by fused-shape height.** `grit` — gravel and andesite banded by a voronoi — on
  the contested ground: the quern and both frontline tips, so the middle of the map reads as bare
  millstone rock from any of the four sides. `hag` — dirt and podzol — on the two wool runs, the peat
  flanks. `moor` — heather turf over coarse dirt, mossy-cobble rim, granite-and-andesite scarps — on
  everything else.
- **Curves on the coasts only**, generated from each edge (`curves.py`), with the two constraints that keep
  a handle a corner rather than a lobe, seams left straight, and **every edge within 10 blocks of a wall
  left straight** — the veto that `coldharbour_v2` learned by breaking its own wall. Here it matters four
  times: `POST /plan/inspect` returns all four wall rects, and the veto reads them all.
- **The frontline tips shelve** from 12 at the hub edge to 10 at the mid edge, found by vertex `z` rather
  than by a hand-written id list, so the rule survives a recompile renumbering the shapes.
- **Relief on the hub alone**; every other shape `relief_scope: "hold"`.
- **A leat across the spine**, forded by the spine road on a causeway — the same device as v2's stream,
  and on a four-team board it appears four times, once on each team's walk out of spawn.

**The dressing follows the fork rather than ignoring it.** The spine road drops through the hub's **solid
core**, which is the middle of the three ways past the holes; the two ways round are left unpaved. That is
the difference between a route a map has and a route a map *shows*, and it is the direct consequence of the
first correction above.

## 5. What I would look at next

**The quern is small for a four-way pivot.** 20 × 20 blocks with two cairns on it, 10 blocks off each of
eight frontline tips. It works as a switch, but a player standing on it is exposed from four directions at
once, which may be more than the diagonal is worth.

**The four teams are identical, which `rot_90` makes stronger than `rot_180` does.** Under a half-turn a
player sees the enemy board upside down; under a quarter-turn they see it rotated, and the wool that is
"west" for one team is "north" for the next. The board reads fair, but nothing about it is asymmetric except
the coast bows, and a four-team map may want the two wool approaches to differ more than an L and an I do.

**Nothing exercises `CT8`'s rotation device at the frontline.** The recess between each pair of tips is a
buffer hole, which is `CT9`; the holes in the hub are the fork. A hole that a *build zone* spans — so the
route through it opens only when someone bridges — is the one form on the menu this board does not use.
