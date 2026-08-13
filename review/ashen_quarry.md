# Ashen Quarry — what the system did and did not do

A destroy board authored from scratch through the studio's own endpoints, deliberately reaching for
every capability at once: a plan carrying its own elevation tiers, compiled tiers promoted to authored
polygons, an erected tilted mesa, an area-mark relief, per-shape themes with five-deep nested
materials, and a quarry the goal stands in. **Unfinished** — the dressing pass (village, forest, paths,
stream) is not done, and the quarry outline is still a rectangle.

Design sketch: `specs/ashen_quarry/design-sketch.png`.

## The board

360×240, `rot_180`, unit x −180..0 by z −120..120, base surface 41, build ceiling 65.

| Piece | How |
|---|---|
| Town | a plan tier at surface 51 promoted to a 13-vertex polygon, `relief_scope: hold` so its floor stays flat while the field rolls around it |
| Town stair | ten plan pieces, one block per two of run, 42→51 up the wall |
| Quarry | a plan tier at surface 24 — 17 below the field — with the destroyable standing in it |
| Quarry ramp | sixteen plan pieces, 25→40, so the goal is walkable from the front |
| Hill | three `area` relief marks at 56 / 50 / 45 |
| Mesa | an authored polygon, `height_mode: raise` 9 with per-vertex `anchor_heights` so its top tilts, `skirt: 4` |
| Seam | the land polygon crosses x=0 in three places; `rot_180` puts each overhang on the opposite side at the mirrored z, so the halves interlock instead of butting |

## Three techniques worth writing down

**Promote a tier, do not carve it.** A plan draws rectangles; an organic outline comes from replacing
the compiled tier's `vertices`, not from subtracting from its sides. The catch is that a tier can fuse
to **more than one shape**, and reshaping only the first leaves the others' rectangles showing through
wherever the polygon pulled inside them. They have to be dropped.

**A tier can run under a taller one.** The land polygon is drawn *under* the town rather than up to
its edge, so the town's outline can recede organically without opening a gap — the taller add wins
where they overlap. The same trick does **not** work downward, which is why the quarry is still a
rectangle: a lower tier that recedes leaves void, and its ramp is the walkable entry, so a receded
quarry polygon either drops a hole or buries the way in.

**`relief_scope: hold` is what makes a built thing flat.** Without it the relief solves straight
through the town and the plateau arrives covered in contour rings.

## What was hit

### A stranded feature: `bedrockCentre`

The map asks for a 3×3 emerald cube with a bedrock core. `ObjectiveStamper.StampDestroyable` takes
`bool bedrockCentre` and fills the inset for `cube-3`/`cube-4`, and
`ObjectiveStamperTests.cs:89` asserts the bedrock lands in the middle. It is never reachable:
`SketchWorldBuilder.cs:256` calls the method without the argument, and neither `DestroyableIntent` nor
the plan's destroyable marker carries a field for it. One field on the marker, one on the intent, one
argument at the call site. Built, tested, unauthorable.

### A relief mark's `h` is an absolute height, and nothing says so

Read as a lift, `{"kind":"point","h":15}` on a `base: 41` island does not raise 15 — it pulls that
ground to **y15**. The result was terrain at **y4 where it should have been y41**, and the build
**succeeded**: it exported clean, passed the traversability gate, and rendered a plausible map. It was
found by probing columns and noticing the quarry was the only thing at its stated height.

Two things would have caught it. A mark whose height falls far outside `base ± reach` is almost
certainly a unit confusion and is cheap to warn on. And `relief.md` reads against itself here: §2.2
describes a *push*'s amount in relative terms — "one end stands sixteen blocks up, the other six" —
a few paragraphs from the marks table, where `h` is absolute.

### The export's traversability gate refuses while naming nothing

`Traversability.cs:52–68`. `main` is the most common component among points with `Component > 0`. When
**every** point is off-grid, `comps` is empty, `main` stays `0`, and `isolated` — the points where
`Component != main` — comes out **empty**. The refusal is then:

```
409 {"error":"not traversable",
     "message":"0 spawn/wool point(s) are not reachable from the rest",
     "isolated":[]}
```

Zero, and nothing named. The case where an author most needs to know which point failed is the one
case the gate cannot say. It happened here because two subtract polygons crossed the spawn footprint,
so both spawns stood over void — a message reading "no objective point is on navigable ground" would
have said it in a sentence; instead it took reading the analyser's source.

**And a destroyable is never a navigation point.** `NavigationPoints` walks `spawns` and `wools` only,
so on a DTM board the gate checks that the two spawns can see each other and says nothing at all about
whether anyone can reach the goal.

### Smaller

- **`--structures` cannot see a building whose material matches the ground.** It finds by material, so
  a themed map hides its own rooms from the check that confirms they stamped.
- **The API holds its own DLLs.** Rebuilding after a pull fails with sixteen `MSB3027`s that read like
  compile errors and are not; the host has to be stopped first. `CLAUDE.md` warns about two concurrent
  builds, which is the adjacent case, not this one.
