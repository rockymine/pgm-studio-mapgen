# The grown tree and the boulder — what was wrong, and what it builds now

Two props were reported unusable: the **grown** tree ("extremely buggy… elements floating… the trunks are not
very nice"), which no shipped board uses, and the **boulder** ("not very nice" — the author wants glacial
erratics, large, rounded-but-irregular, sitting *on* the ground with weight).

Both are fixed. The grown tree's fault was one measurement everybody had been taking with the wrong
neighbourhood; the boulder's was three shape decisions that each read as the opposite of an erratic.

---

## How this was measured

A probe board was built through the real `WorldBuilder` — a flat plate 688 × 412 with 58 props on it, 56
blocks apart so no two crowns meet: 32 grown trees spanning every height from 6 to 40, one to three stems,
staggered and whorled, at leader 0.1 and 0.9 and levels 2 and 3; 10 vanilla template trees as a control; and
16 boulders, four forms at four sizes. Every prop's blocks were read back out of the built world and filed by
three measures:

- **bodies** — how many pieces the prop's blocks form under **face** adjacency, which is what a player sees.
- **blocks with air on all six faces** — a block joined to the rest at an edge or a corner only. Light passes
  it on every side; it reads as a block hanging in space.
- **pieces resting on nothing** — a face-connected piece none of whose blocks has a solid block beneath it.

Everything below is reproducible from the code as it stands: grow the same shapes at the same seeds, or place
the same props on a flat plate.

---

## Fault 1 — the grown tree was never one body

### What the reading missed

`docs/world-export/tree-corpus.md` scores the grower against 75 hand-built trees, and every one of its
measures is taken over the **3×3×3 neighbourhood**. On that reading the grower was already good: "trees whose
wood is in one piece — 100%".

A 3×3×3 reading counts a corner as a hold. In a world it is not one. A block whose only neighbour is diagonal
has air on all six of its own faces: you see straight past it, and it reads as a floating block beside a tree
rather than part of one. The corpus is nearly free of that by construction — 0.3% of its 4,044 blocks of wood
are held by a corner alone — so the discrepancy never showed.

Read on faces, the grown tree was a haze. Over the 32 grown trees on the probe board:

| | before | after |
|---|---|---|
| blocks placed | 27,228 | 21,638 |
| face-connected bodies | **3,106** | **32** (one per tree) |
| blocks not in the tree's own biggest body | 16,854 | 0 |
| blocks with air on all six faces | **1,912** | **0** |
| pieces resting on nothing | **3,069** | **0** |
| worst single tree | 394 bodies, 235 floating blocks | 1 body, 0 |

The ten **template** trees on the same board were one body each with nothing floating, before and after. That
is why every shipped board uses the vanilla tree.

### Per tree, with coordinates

Each row is one prop on the probe board; the anchor is where it stands, so any of these can be re-placed and
checked in game.

| tree | at | blocks before/after | bodies before/after | six-faces-air before/after | pieces on nothing before/after |
|---|---|---|---|---|---|
| grown h6 stems1 | (−308, −170) | 79 / 41 | 14 / 1 | 7 / 0 | 13 / 0 |
| grown h6 stems2 | (−252, −170) | 56 / 30 | 11 / 1 | 5 / 0 | 10 / 0 |
| grown h6 stems3 | (−196, −170) | 57 / 36 | 10 / 1 | 5 / 0 | 7 / 0 |
| grown h9 stems1 | (−140, −170) | 94 / 73 | 18 / 1 | 15 / 0 | 17 / 0 |
| grown h9 stems2 | (−84, −170) | 106 / 85 | 19 / 1 | 12 / 0 | 18 / 0 |
| grown h9 stems3 | (−28, −170) | 142 / 100 | 30 / 1 | 21 / 0 | 29 / 0 |
| grown h12 stems1 | (28, −170) | 144 / 114 | 20 / 1 | 14 / 0 | 19 / 0 |
| grown h12 stems2 | (84, −170) | 287 / 227 | 35 / 1 | 20 / 0 | 34 / 0 |
| grown h12 stems3 | (140, −170) | 235 / 149 | 35 / 1 | 14 / 0 | 34 / 0 |
| grown h16 stems1 | (196, −170) | 336 / 271 | 27 / 1 | 19 / 0 | 26 / 0 |
| grown h16 stems2 | (252, −170) | 421 / 323 | 43 / 1 | 26 / 0 | 39 / 0 |
| grown h16 stems3 | (308, −170) | 588 / 495 | 65 / 1 | 41 / 0 | 64 / 0 |
| grown h20 stems1 | (−308, −114) | 558 / 471 | 55 / 1 | 30 / 0 | 54 / 0 |
| grown h20 stems2 | (−252, −114) | 883 / 746 | 95 / 1 | 57 / 0 | 94 / 0 |
| grown h20 stems3 | (−196, −114) | 976 / 741 | 109 / 1 | 69 / 0 | 108 / 0 |
| grown h26 stems1 | (−140, −114) | 705 / 552 | 88 / 1 | 59 / 0 | 87 / 0 |
| grown h26 stems2 | (−84, −114) | 1042 / 768 | 163 / 1 | 99 / 0 | 162 / 0 |
| grown h26 stems3 | (−28, −114) | 1590 / 1236 | 159 / 1 | 95 / 0 | 158 / 0 |
| grown h32 stems1 | (28, −114) | 1271 / 1021 | 127 / 1 | 84 / 0 | 126 / 0 |
| grown h32 stems2 | (84, −114) | 1767 / 1359 | 221 / 1 | 140 / 0 | 220 / 0 |
| grown h32 stems3 | (140, −114) | 2507 / 2049 | 284 / 1 | 174 / 0 | 283 / 0 |
| grown h40 stems1 | (196, −114) | 1779 / 1481 | 182 / 1 | 104 / 0 | 181 / 0 |
| grown h40 stems2 | (252, −114) | 2762 / 2196 | 296 / 1 | 194 / 0 | 295 / 0 |
| grown h40 stems3 | (308, −114) | 3629 / 2935 | **394 / 1** | **235 / 0** | **393 / 0** |
| h22 staggered levels2 leader0.1 | (−308, −58) | 395 / 301 | 61 / 1 | 42 / 0 | 60 / 0 |
| h22 staggered levels2 leader0.9 | (−252, −58) | 815 / 654 | 95 / 1 | 67 / 0 | 94 / 0 |
| h22 staggered levels3 leader0.1 | (−196, −58) | 491 / 405 | 49 / 1 | 31 / 0 | 48 / 0 |
| h22 staggered levels3 leader0.9 | (−140, −58) | 1079 / 903 | 113 / 1 | 76 / 0 | 112 / 0 |
| h22 whorled levels2 leader0.1 | (−84, −58) | 565 / 463 | 52 / 1 | 29 / 0 | 51 / 0 |
| h22 whorled levels2 leader0.9 | (−28, −58) | 626 / 500 | 73 / 1 | 41 / 0 | 72 / 0 |
| h22 whorled levels3 leader0.1 | (28, −58) | 604 / 439 | 77 / 1 | 39 / 0 | 76 / 0 |
| h22 whorled levels3 leader0.9 | (84, −58) | 639 / 474 | 86 / 1 | 48 / 0 | 85 / 0 |

The first floating blocks in the worst tree, for a spot check in game: (296, 9, −105), (295, 10, −105),
(296, 11, −105). After the fix that tree has none.

### Cause A — the sweep left edge joins, which severed half the limbs

`SweptVolume.Sweep` stamps a ball at every sample of a limb's spline. A limb thinner than a block selects
exactly one cell per sample — the block the sample sits in — and consecutive samples can cross **two or three
block boundaries at once**, which leaves the cells they stamp touching along an edge or at a corner. Nothing
in the sweep put anything between them.

Over 768 grown trunks and 10,362 branches (8 heights × 2 arrangements × 3 stem counts × 8 seeds):

| | old sweep | new sweep |
|---|---|---|
| trunks severed on a face reading | **396 of 768** | 0 |
| branches severed on a face reading | **5,472 of 10,362** | 0 |

That is "the trunks are not very nice", exactly: a **20-course trunk at height 20, seed 6, came out in two
pieces**, the lower ending at (0, 3, 0) and the upper starting at (−1, 4, 0) — a hole you can see through at
knee height with the rest of the trunk standing above it. At height 32, seed 6, the same trunk was in three
pieces.

**Fix.** `SweptVolume.Sweep` now threads the walk from one sample's cell to the next **one axis at a time** —
`SweptVolume.Between`, a Bresenham staircase that advances whichever axis is furthest behind the straight
line — and stamps every cell of that thread. The run is face-connected by construction, and nothing is taken
away: the new cell set is a superset of the old.

### Cause B — the crown was rooted through corners, so the speckle stayed

`TreeCrown.Rooted` exists precisely to make a floating leaf impossible: it emits only foliage that reaches
wood through a chain of leaves. It walked that chain over the 3×3×3 neighbourhood, so a leaf attached to the
crown at a single corner counted as held — and a crown grown from a 45% white-noise density roll is full of
those.

Measured over 64 grown trees (8 heights × staggered/whorled × 4 seeds), varying only the rooting rule:

| rooting | leaves / tree | blocks with air on all six faces | face bodies / tree | leaves touching wood | occupied neighbours / leaf |
|---|---|---|---|---|---|
| corners (before) | 530 | **8.4%** | **72.6** (worst 221) | 31.8% | 7.3 |
| faces (after) | 368 | **0.0%** | **1.0** | 41.9% | 7.6 |
| corpus | — | 10.6% of leaves hang diagonally | — | 30.3% | 6.2 |

**Fix.** `TreeCrown.Rooted` roots through the six face neighbours. It costs the outer **31%** of the fill,
and that 31% was the haze rather than the crown: density per leaf barely moves (7.3 → 7.6, against a
hand-built 6.2), and wood contact rises to 41.9% because what a face rooting drops is the fringe furthest
from the wood.

Raising the density instead was measured and rejected: 0.55 gets the leaf count back above the old figure but
takes occupied neighbours to 9.0, which is the solid the corpus work spent its effort getting away from.

### Cause C — a clipped prop left the far half hanging

Found while checking the first two. `Decorator.Fan` writes a prop cell only where the world already has air,
so whatever is already standing clips the prop — and a clip can cut it in two. The far half was still being
written, joined to nothing.

A 32-course grown tree beside a 40-course iron tower, tower at the given distance from the trunk:

| tower at | before: blocks / bodies / pieces on nothing | after |
|---|---|---|
| no tower | 731 / 1 / 0 | 731 / 1 / 0 |
| 3 blocks away | 729 / 2 / **1 — 32 blocks from (5, 21, −3)** | 697 / 1 / 0 |
| 2 blocks away | 730 / 2 / **1 — 34 blocks from (5, 21, −3)** | 696 / 1 / 0 |
| 1 block away | 726 / 2 / **1 — 35 blocks from (5, 21, −3)** | 691 / 1 / 0 |
| through the trunk | 710 / 4 / **2 — 584 blocks from (−1, 16, 0)** | 3 / 2 / 0 |

**Fix.** `Decorator.Standing` keeps the cells of a landing prop that rest on a block the world already had,
plus everything reaching one of those through a chain of shared faces, and `Fan` writes nothing else. A prop
places only the part of itself something holds up.

---

## Fault 2 — the boulder was a pebble emerging from the ground

Three separate decisions each read as the opposite of a glacial erratic.

**It was sunk to its middle.** `BoulderShapes` centred every lobe on `y = 0`, so half the ellipsoid was
underground on the stated grounds that "a rock that sits entirely on the ground reads as dropped". An erratic
*is* dropped — that is what the word means — and sinking it halves the rock: what stood was a dome the full
width of the thing and a third of its height, which reads as a knuckle of bedrock.

**It was small.** `size` ran 1 to 7 with a default of 2.5. The default rock was **35 blocks, 3 courses tall
and 5 across** — a stone you step over.

**Its surface was chewed rather than weathered.** `Blob`'s erosion sampled its noise at three times the block
rate, so the field turned over every block: the outline wobbled per cell, which is lumpy rather than eroded,
and at the amplitude an `angular` rock uses it detached chips. An angular rock of size 7 at (−308, 54) came
out in **three pieces with two blocks standing in mid-air, at (−308, 10, 48) and (−312, 11, 51)**; at size 10
(clamped to 7) it was six pieces with three floating blocks.

### What it builds now

`BoulderShapes.Of(form, size, seed)` answers three lobes: a main mass whose middle is lifted so only
`BoulderShapes.Bed` = **30% of the rock's height** is under the surface, plus a haunch at its foot and a
shoulder over it, each thrown out on a bearing hashed from the rock's own seed. `Blob` samples its erosion at
the block rate against a **three-block scale**, which weathers the surface into facets. `size` runs **2 to 10**
with a default of **4**. The `outcrop` is the one form whose middle stays at the surface, because an outcrop
genuinely does emerge.

| form | size | before: blocks / tall / wide / bodies / floating | after |
|---|---|---|---|---|
| round | 2 | 22 / 2 / 5 / 1 / 0 | 28 / 3 / 4 / 1 / 0 |
| round | 4 | 140 / 4 / 9 / 1 / 0 | **212 / 6 / 8** / 1 / 0 |
| round | 7 | 678 / 6 / 15 / 1 / 0 | **1093 / 10 / 15** / 1 / 0 |
| round | 10 | *clamped to 7* — 678 / 6 / 15 | **3101 / 14 / 22** / 1 / 0 |
| angular | 2 | 20 / 2 / 3 / 1 / 0 | 27 / 3 / 4 / 1 / 0 |
| angular | 4 | 143 / 4 / 9 / 1 / 0 | 204 / 6 / 8 / 1 / 0 |
| angular | 7 | 695 / 7 / 15 / **3 / 2** | **1108 / 10 / 15 / 1 / 0** |
| angular | 10 | *clamped* — 687 / 7 / 15 / **6 / 3** | **3077 / 15 / 21 / 1 / 0** |
| outcrop | 7 | 691 / 4 / 21 / 1 / 0 | 850 / 4 / 20 / 1 / 0 |
| cairn | 7 | 636 / 12 / 13 / 1 / 0 | 912 / 14 / 13 / 1 / 0 |

A size-7 erratic in its own frame, seed 11 — 1,342 blocks, 1,091 of them over the ground (19% bedded), foot
128 cells, widest course 15:

```
  9 ......###......
  8 ...#########...
  7 ..###########..
  6 .############..
  5 .#############.
  4 .#############.
  3 ###############
  2 ###############
  1 .##############
  0 .##############
    =============== ground
 -1 ~~#############
 -2 ~~~###########~
 -3 ~~~~#########~~
```

Its widest course sits two above the ground, so the rock overhangs its own foot the way a perched erratic
does; the foot is still nearly the whole width, which is what reads as weight. The same rock at seed 23 has a
different shoulder and a different crest — the lobes are seeded, so a scatter of erratics is a scatter of
shapes.

**On a bank it beds in rather than hangs.** A prop seats on the lowest column of its own footprint, so a
steeper slope buries more of the rock instead of lifting its downhill edge. Measured on a ramp falling 2
courses every 8 blocks with a size-7 rock: 1,229 blocks against 1,342 on the flat, and 14 of 151 footprint
columns over air against 23 — the columns over air being the shoulder overhang, deepest 3 courses at
(3, 15, −6).

---

## What changed

| file | change |
|---|---|
| `src/PgmStudio.Geom/Algorithms/SweptVolume.cs` | `Sweep` threads consecutive sample cells with `Between`, a single-axis Bresenham walk, so a limb is face-connected |
| `src/PgmStudio.Geom/Algorithms/TreeCrown.cs` | `Rooted` walks the six face neighbours instead of the 26 |
| `src/PgmStudio.Geom/Algorithms/Blob.cs` | erosion noise sampled at the block rate against a three-block scale |
| `src/PgmStudio.Minecraft/Dressing/DressingModel.cs` | `BoulderShapes.Of(form, size, seed)` — the erratic's three lobes, `Bed`, seeded bearings |
| `src/PgmStudio.Minecraft/Dressing/PlacedProp.cs` | `BoulderProp.Size` default 4, `Reach` clamped 2–10 |
| `src/PgmStudio.Minecraft/Dressing/Decorator.cs` | `Standing` — a prop places only the part of itself something holds up |
| `src/PgmStudio.Client/…/SketchDressingInspector.razor` | boulder size slider 2–10, default 4 |
| `src/PgmStudio.Client/wwwroot/js/studio/dressing/dressing-doc.js` | a new boulder is size 4 |
| `docs/world-export/decoration.md` | §2 the holding rule, §5 rewritten for the erratic, §6 the face-connected limb and the face rooting |
| `docs/world-export/tree-corpus.md` | a new section on the corner-counting reading, and the grower's scores on it |
| `docs/tools/sketch.md` | the boulder's document model |
| `tests/PgmStudio.Geom.Tests/…/DressingAlgorithmTests.cs` | the sweep bridge, the walk, the tree-is-one-body sweep, the corner-held leaf |
| `tests/PgmStudio.Minecraft.Tests/BoulderShapesTests.cs` | the erratic's proportion, seating, seeded silhouette and one-bodiness |
| `tests/PgmStudio.Minecraft.Tests/DecoratorTests.cs` | the clipped tree, and the boulder's seating |

Every new test was run against the old code first and fails there: 3 of the Geom tests and 7 of the Minecraft
tests. With the fixes in, both suites are green (263 Geom, 909 Minecraft, 405 JS).

---

## What was not fixed

- **A generated crown is still denser than a hand-built one** — 7.6 occupied neighbours per leaf against the
  corpus's 6.2, and a generated tree still carries more wood per leaf than an author's. Already recorded as
  open in `tree-corpus.md`; the face rooting does not move it either way.
- **The whorled tree's bulk sits at mid-height**, not in the bottom third a hand-built conifer puts it in
  (`G173`, already on the board).
- **A prop that is clipped away to nothing says nothing.** `Fan` reports a decline when a prop cannot *seat*;
  a prop that seats and then loses every block to what is already standing places silently. Filed as `WE66`.
- **A grown tree's trunk is one block wide up to about height 26** (`TreeShape.TrunkRadius` = 0.6 + size·0.6,
  reaching a plus-section three wide only near height 40). That is defensible against a corpus whose median
  tree carries 51 blocks of wood, and it is not what the author reported, so it is left alone.
