# Brackenfold — the painting rules, built

**What it is, in one sentence.** A grass down falling from each spawn to a peat working, with each team's
monument standing on a cobbled fold on the shoulder above it, and the two workings separated by open air a
team has to bridge.

Destroy the monument, two teams, `rot_180`, 20 players, 68 × 212 blocks. It is the board the *What a board
is painted with* section of `AUTHORING-BRIEF.md` was written for, and this document says which rule bought
which part of it.

## The board

```
      |    1         0         1    |
  -26 |    AAAAAAAAAAAAAAAA        |   A  back, at 20 — the spawn ground
  -25 |    AAAAAASSSSAAAAAA        |   S  camp, the spawn room
  -20 |    BBBBBBBBBBBBBBBB        |   B  moor, at 20 — the down, roads and scars
  -14 |      CCCCCC!CCCCC          |   C  shoulder, at 22 — the fold, and the monument
  -11 |    DDDDDDDDDDDDDDDD        |   D  lower, at 20 — the workings, spoil on the lip
   -6 |    ..................      |   .  void, crossed by one build zone the full width
```

Five pieces on the authored half — four of them ground at one height and one raised shelf — and one build
zone. Everything else about the shape is relief.

## One goal, and a gap that has to be bridged

The monument stands 40 blocks from its own spawn and 142 from the enemy's: **`GO1` ratio 3.55**, inside the
authored band [3.0, 4.0]. The two land masses stand **48 blocks apart** and nothing joins them — the crossing
is a build zone spanning the whole width of the board, so an attacker chooses where to bridge and a defender
cannot know which. `preflight` reads the two masses as one component *bridged by a build region*, and both
markers as connected.

That gap is the map. Everything a defender has is the time it takes to cross open air and climb a shelf; the
attacker's is that the front is 68 blocks wide and the fold is only 48.

## What the ground is made of

**Three themes, and one of them is the map.**

| theme | where | what it is |
|---|---|---|
| `down` | everything | grass over two dirt; a stone lip at the coast; a stone-and-andesite body |
| `fold` | the shoulder | mossy cobble over cobble, a chiselled stone coping, a cobble face |
| `scar` | six drawn patches | coarse dirt over dirt |

**Every pattern carries two blocks.** There are two patterns on the whole board. The **fill** is a voronoi at
`cellSize` 14 in stone and andesite — the body of the rock, seen only where the coast is cut. The **coast
wall** is a noise field at `scale` 20 between the same two blocks, which is a texture in one ground rather
than a border between two. Nothing on the surface is a pattern at all.

**The variation on the surface is drawn.** Three polygons per half carry the `scar` theme — worn ground where
sheep have poached the down — and they are shapes with a theme, not a field sampled over the moor. Six
patches is what a person would put there; a cell pattern of grass and dirt would have put dirt over a third
of the board.

**The three families are named.** Ground is `verdant`. Built is `cobble` — the fold, the tracks, the hut's
plate. The accent is `grey stone` — the coping on the fold, the spawn room, the lip at the coast. The hut
breaks out of all three into `dirt` (spruce) and `loam` (dark oak), which is how it reads as a building from
across the moor rather than as a lump of the ground it stands on.

## The techniques, and what each one bought

- **The shape is relief, not pieces.** Four of the five pieces stand at one height. The moor's swell is a
  `grain` at amplitude 2.2 and **scale 24** — long swells rather than static, which is the whole difference
  between a brush that reads as controlled and one that reads as noise.
- **`relief_scope: "exclude"` on the fold.** The shoulder is a made platform and stays flat while the moor
  rolls around it. Its `rimEdges: "boundary"` puts the chiselled coping round its whole outline — a
  retaining wall's top course, which is the one place a rim belongs.
- **The rim is on at the coast and nowhere else.** `rimEdges: "void"` caps the board's own edge over the gap
  and leaves every fall the relief solved untouched, so the down rolls without contour lines.
- **`bendShapes` on both ground shapes.** The compiler emits the plan's rectangles; the bend resamples the
  long edges and pulls the inserted points inward, so the coast is drawn rather than stamped. 8 compiled
  vertices became 24 on each.
- **A levelled shelf for the hut.** One relief `area` mark at the base height under the hut's site. Without
  it the building stood two blocks over the ground beside it and filled the face in bedrock (`WX11`).
- **Roads before scenery.** Two route strokes run spawn → fold, and every tree and boulder was placed after
  them and moved when the road said so.

## What went wrong

- **Two monuments were too close together.** The first build put two `cube-3` monuments 28 blocks apart on
  one shoulder. On a board this size that is one objective with two health bars. It is now one.
- **The middle was land.** The first build ran ground the whole way through with a peat cutting in the
  relief. A destroy board wants the crossing to be *air* a team pays to cross, and a land connection makes
  the middle a corridor rather than a decision. The land now ends at the spoil heaps and a build zone crosses
  the full width.
- **`obsidian` on a `cube-3` is a grind** (`DC3`): obsidian is worth three blocks, and the studio built the
  goal in ender stone regardless while the XML declared obsidian. The monument is ender stone now, which is
  also the only pale thing on the board and reads as a standing stone.
- **Four prop placements were wrong and the pass said so with coordinates**: a tree on a boulder, a tree on
  the road, a tree three blocks from the pavement, and a tree inside the goal's clearance. The last one was
  dropped rather than moved — a tree on a stone fold has no answer to *why here*.
- **`STRUCT` refused the first plan.** A neutral middle piece touching the mirrored ones mixes fanned and
  non-fanned ground in one landmass. That is what pushed the middle out of the piece list, and the board is
  better for it.

## Coordinates

| thing | at |
|---|---|
| spawn | `(0, ±96)` |
| monument | `(0, ∓50)`, ender stone, `cube-3`, floating 3 |
| the fold | `x −24..24`, `z ∓56..∓44`, surface 22 |
| the gap | `z −24..24`, 48 blocks, build zone `x −36..36` |
| the hut | `x −28..−20`, `z −74..−66` |
| spoil heaps | `(−24, −28) (−8, −29) (10, −28) (26, −29)` and their images |
