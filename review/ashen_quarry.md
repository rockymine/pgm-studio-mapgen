# Ashen Quarry — what the system did and did not do

A destroy board authored from scratch through the studio's own endpoints, deliberately reaching for
every capability at once: a plan carrying its own elevation tiers, compiled tiers promoted to authored
polygons, an erected tilted mesa, an area-mark relief, per-shape themes with five-deep nested
materials, a quarry the goal stands in, and fifty hand-placed props.

**The dressing, in one list of fifty.** Nine buildings in three authored house styles — a stone-and-
spruce cottage, a cobble-checkered longhouse under a hip roof, and a two-storey shop whose ground
floor is stone under a timbered flat, written as a `storeys` stack of two. Thirty template oak and
birch, placed one at a time rather than scattered. Four paths: two field tracks paved from a `cell` of
dirt, coarse dirt and spruce planks, and two town ways in stone brick and polished andesite. A
`Natural` stream with a wandering shore over a voronoi bank. Four boulders and two flora meadows.
Every one is authored on the unit and fanned, so both halves match.

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

**A sink shape is how a lower tier gets an organic floor.** The quarry's own outline stays the
rectangle its plan tier fused to, but a `sink` polygon *inside* it — 5 deeper, `skirt: 3`, its floor
tilted by `anchor_heights` — cuts an organic bowl in the flat pan, and the destroyable stands at the
bottom of it. That is the answer to the tension above: a lower tier cannot recede without leaving
void, but it can be dug into.

**Interlocking beats a straight seam.** Under `rot_180` an overhang past x=0 lands on the opposite
side at the mirrored z, so a land polygon that crosses the centre line three times produces two halves
that mesh instead of butting. The one constraint is that an overhang must avoid the z-band where the
*mirrored* quarry lands, or the mirror's land at 41 covers the quarry at 24 — the taller add wins.

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

### A spawn building is sized by its plan piece, and nothing else

There is no size knob. The building the stamper raises fills the spawn-role piece, so a 34×34 piece
gives a 34×34 hall — which on this board read as a bedrock warehouse filling half the town. The fix is
to draw the *piece* small: at 14×14 it is a building, and it can be pushed into a corner of the town
because the piece's position is the building's position. That is workable but backwards — the piece is
a **protection region**, a gameplay contract about where a team is safe, and it is doing double duty as
the footprint of a building. An author who wants a small hut inside a large protected area, or a large
hall in a tight one, cannot say either.

The building itself was also mine to get wrong rather than the tool's. `roomStyles.spawn` was left
unbound through every build above, and an unbound room stamps the **built-in shell — a bedrock lid**,
exactly as `library.md` says it does. It is now a civic hall in the town's own materials: a banded
wall of stone brick with polished andesite courses, andesite posts and verge, spruce hip roof with a
ridge cap and slab eave, arched openings, spruce beams, and a stone-brick floor with an andesite
border and inlay. Zero bedrock above ground anywhere in the footprint.

### A goal needs a plan tier under it, even when the landform is authored

The second destroyable stands on the mesa. A marker must ride a plan piece, and — as the author put
it — the plan has to already carry the high ground for the marker to sit on. So the mesa stopped being
an authored `raise` shape and became a **plan tier at surface 58**, promoted back to a polygon by the
same reshape as the town, with its tilt restored through `anchor_heights` and `relief_scope: hold`.

That works, and the result is the same world, but it inverts the division the tools describe. The plan
is meant to state the *board* and the sketch the *ground*; here a piece of ground had to be pushed back
into the plan purely so a marker had something to ride. Any landform carrying an objective has to exist
twice — once as a plan rectangle for the marker, once as a polygon for the shape it actually is.

### The void column, and the boundary nothing checks

There are **102 void columns along z=29**, a one-row slot at the quarry's mouth. The land polygon
enters its notch on a *diagonal* — `[0,26] → [-70,30]` — so between z=26 and z=30 the land is already
cut away while the quarry rectangle does not start until z=30, and nothing covers the strip.

Two boundaries that must agree, authored in different files in different idioms: one a polygon vertex
list, the other a plan rect. **Nothing validates that they meet.** The build exported clean and the
traversability gate passed. A lint for "shapes leave a hole no tier fills" is the single check that
would have caught the most expensive class of error hit across both maps — this, and ClayClay's
subtract polygons crossing its own spawn.

### The quarry could have been a polygon, and the earlier reasoning here was wrong

An earlier revision of this file said a lower tier "cannot recede without leaving void" and left the
quarry a rectangle on that basis. The rule that actually governs is the one two sections up:

> the tier that recedes must be overlapped by the other one.

For the town the land is lower, so the land runs **under** it. For the quarry the land is higher, so
the land needs to run **over** the quarry's fringe — and then the quarry can be an organic polygon
exactly as the mesa is. Mirrored, not different. The mesa proves the shape works; the quarry is square
because the rule was misapplied, not because the model refuses it.

### Smaller

- **`--structures` cannot see a building whose material matches the ground.** It finds by material, so
  a themed map hides its own rooms from the check that confirms they stamped. Measured here: of nine
  village houses, only the spruce and dark-oak ones are reported — the stone-brick cottages are
  swallowed into the 8,399-cell "structure" that is the stone-brick town they stand on.
- **A stream fragments the navigable read.** Adding the dressing took traversability from 2 components
  to **18**, because water is not walkable and the channel cuts the land. `isolated` stays 0, so the
  objectives are fine and the map is sound — but the component count on its own reads like damage, and
  a board with any water in it will always report a large number.
- **The API holds its own DLLs.** Rebuilding after a pull fails with sixteen `MSB3027`s that read like
  compile errors and are not; the host has to be stopped first. `CLAUDE.md` warns about two concurrent
  builds, which is the adjacent case, not this one.
