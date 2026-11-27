# 10. Wandering U, and the tree generator artifact

Written 27 November 2026 after the author's fourth instalment (`author-account-2026-11-27.md`). Two things were
supplied: a zip of the map whose wool room moves, and the link to the page the author says holds the tree generator.
Both are data; nothing in either was run. Research `08` §1 said the moving-wool-room map was not in the record. It is
now, supplied by the author from the private maps repository, and the section below replaces that conclusion.

## 1. Wandering U

### 1.1 What was supplied

The zip is `5f8b7853-wandering-u.zip` (24,535 bytes), uploaded by the author on 27 November 2026. It holds
`wandering-u/level.dat`, `wandering-u/map.xml` (27,715 bytes) and four region files (`r.-1.-1`, `r.-1.0`, `r.0.-1`,
`r.0.0`). It was extracted into an empty directory of its own and read only with `python3 -I` and the render tool; no
script from it was run. The world and the XML are not committed; the pictures are (`renders/wandering-u/`).

Provenance is the author's word: he says it comes from the private maps repository. The record cannot confirm that
(research `08` §1 could not read it) and nothing inside the zip says it.

### 1.2 Identity, as the file states it

| field | in `map.xml` |
|---|---|
| name | `Wandering U` |
| version | `1.0.0` (`proto="1.5.0"`) |
| game mode | `ctw` |
| objective text | "Capture the enemy wool — but its room walks a lap around the U and floats over the void!" |
| teams | `red` and `blue`, `max="12"` each |
| authors, contributors | **none stated**: the file has no `<authors>` and no `<contributors>` element |
| created date | **none stated** in the XML |
| include | `gapple-kill-reward` |

So the question "who are its authors" cannot be answered from the map. The only evidence on who made it is the
author's own account that it is his, built late, tested on 6 August 2026 (`author-account-2026-11-27.md`, second to
fourth instalments).

Dates that are in the zip, with their limits. The `level.dat` field `LastPlayed` reads 1785526980566 ms, which is
Friday 31 July 2026 19:43:00 UTC. The zip's own file times are `level.dat` 31 July 21:43, the region files 1 August
23:06 and `map.xml` 1 August 23:09. The first matches `LastPlayed` two hours later, so the zip times are most likely
local summer time (UTC+2); that is an inference, not stated. If so, the XML was last saved at about 21:09 UTC on 1
August 2026, which is the evening the studio's decoration prototype was first committed (`a3160327`, 23:46 UTC, §2).
These are file dates, not a created date, and a zip can carry changed times. The author's 6 August test date is not
in the file.

### 1.3 The ground and the objectives

The world is 40,612 blocks, x -75..9, y 0..25, z -75..74 (render tool `info`). It is saved with the wool rooms at
their start stop. The layout is a U mirrored over z (the XML's own comment calls it "a comb hanging off one spine"):
each team's spawn building stands at x -75..-65, a five-step staircase drops five blocks to a spine at x -40..-31,
and the two halves meet across a 20 by 20 void gap at x -40..-21, z -10..9 ("the 20x20 contact front"). Every piece
is on bedrock at y 0 with sky below (picture `04`). The spawn points are `-70,15,-40` (red) and `-70,15,40` (blue),
the observer spawn `0,25,0`, and the build height `maxbuildheight` is 30.

Two wools, both `required="true"`: blue captures a red wool at `-5,14,-70` (monument `-68,16,37`), red captures a
blue wool at `-5,14,70` (monument `-68,16,-43`). Each wool is in the enemy half's far corner, in the room that moves.
The wool is also spawned: a `<spawner>` drops a wool every 1.5 s in the room's corridor while that wool is not yet
captured (filter `blue-wool-live` or `red-wool-live`). A team may not enter its own wool room (`enter="not-red"` on
the red room box) and may not edit it except with blocks the `woolrooms-filter` allows. Spawn entry is limited to the
owning team. Outside the contact gap and two short links by the docks, building over void is refused: the `no-void`
filter is applied to everything that is not in `build-area`, "so nobody can chase the island out of the U's mouth".

### 1.4 How the wool room moves

The room is one 10 by 10 chunk, "the entire 10x10 chunk pgm-studio stamps for the wool-room role": a solid bedrock
column from y 0 up to the surface plus an 8 by 8 cage on top, y 0..22. It is a PGM `<structure>` captured from a
source region, then pasted by `<dynamic>` entries at eight stops. The XML (shortened):

```xml
<structure id="red-room" region="red-room-source" air="true" clear="true"/>
<dynamic structure="red-room" trigger="pos-0" offset="0,0,0"/>     <!-- rear dock, start -->
<dynamic structure="red-room" trigger="pos-1" offset="10,0,0"/>
...
<dynamic structure="red-room" trigger="pos-7" offset="20,0,30"/>   <!-- front dock -->
```

`clear="true"` lifts the whole column out at match load, leaving a hole to y 0 at the rear dock. The front dock is
a matching hole the plan leaves at the tip of leg A. So both docks are notches the island plugs into, and the six
stops between are over open void. The route is horizontal only; the island never changes y. From the rear dock it
goes three stops out along x, three across along z, one back in to the front dock, then retraces the eight stops.
The blue room mirrors in z. The red room's corner at stop `pos` is `(-10 + 10*ix, 0, -75 + 10*iz)`.

The clock is two match variables and a pulse:

```xml
<variable id="path_t" scope="match" default="0"/>   <variable id="path_pos" scope="match" default="0"/>
<time id="past-warmup">15s</time>
<pulse id="move-clock" duration="1s" period="5s" filter="past-warmup"/>
<set var="path_t"   value="(path_t + 1) - 26 * floor((path_t + 1) / 26)"/>
<set var="path_pos" value="bound(path_t - 6, 0, 7) - bound(path_t - 19, 0, 7)"/>
```

After a 15 s warm-up one tick passes every 5 s and `path_t` runs 0 to 25. The position is 0 for ticks 0 to 6, climbs
one stop per tick through ticks 7 to 13, holds at stop 7 for ticks 14 to 19, then falls one stop per tick through ticks
20 to 25. From those formulas (my arithmetic) the room sits 7 ticks (35 s) at the rear dock, travels 7 ticks (35 s),
sits 6 ticks (30 s) at the front dock and returns 6 ticks (30 s): a lap of 26 ticks, 130 s. The XML's own comment
says "a full lap is 22 ticks = 110s: 35s docked at A, 30s crossing, 35s docked at B, 10s cutting back", which does not
match its formulas, so the comment is stale or the numbers are; the formulas are what PGM would read. A `rooms-apply`
action, triggered by each of the eight `pos-N` filters, writes the room's box (`red_room_box`, a `<cuboid>` variable)
and spawn point to the new stop. Every protection (`apply enter`, `apply block`) is on that box, so it moves with
the room. The warnings are announced: at the last tick of each halt a title says "Undocking", and "MOVE" and a 3, 2, 1
count in the action bar precede each jump.

What the XML says about people on it: "Riding is not possible: a `<dynamic>` moves BLOCKS, not the players standing on
them, so anyone still inside when the room leaves is left in mid-air over the void. That is the intended tension —
board it while it is docked, take the wool, get out." The depart warning's subtitle reads "Get out or ride it into
the void". So the file shows a player leaving the world by staying in the room when it leaves, which leaves them in the air over
void; the render shows the other way, stepping off any piece, since nothing is under the map but sky. That the room also kills dropped items each tick (`kill-entities` on
`litter-in-red-room`) is only housekeeping.

The author's own account of the test (fall out of the world, room that moves) is consistent with this file, which I
cannot show as a test: nothing here records who played or what happened. This is the first map in the record that
moves a wool room. Hello World and Hello World Micro only recolour theirs (research `08` §2).

### 1.5 How it was built

The XML's comment names the tool: the room is "the entire 10x10 chunk pgm-studio stamps for the wool-room role" and
"the plan is authored at cell=1 — its rects are blocks, not 5-block cells". So it is a studio plan whose `map.xml`
was then extended with a hand-written (or model-written) block of variables, structures, filters and actions. No
commit in `pgm-studio` or `pgm-studio-mapgen` is named for this map: `git log --all -i --grep='wander'` finds only
the history film's own commits and unrelated "wandering steps" in a board, and `-S'<dynamic'` finds no match for a
`<dynamic>` element as a studio feature. This is consistent with the author's statement that test maps lived in the
private repository and not in the two public ones.

### 1.6 The pictures

Five pictures are in `renders/wandering-u/` with their cameras in its README. They show the map saved at stop 0, so
they show where the room starts, not the lap. The best of them for the film is
`03-wool-room-at-rear-dock.jpg` (the bedrock chunk with its cage at the end of the white-and-red leg, the other half
and the front-dock box behind it); `04-wool-room-underside.jpg` shows nothing under the room but sky.

## 2. The tree-generator artifact

### 2.1 What the page is

The artifact `https://claude.ai/artifact/JvGM5hGiW8L3t4Ni8S6Amj` was read with the Artifact tool (the whole 100,475
bytes, 1,409 lines, were read in the saved file in parts). Its title is **"Map Decoration — prototypes"**; the
headline is "Decorating the map, after the paint." It is a single self-contained HTML page with sliders and canvases,
in the studio's dark theme, with a kicker "pgm-studio · layout generation · realize" and chips "Stage realize · a pass
after `TerrainPainter`", "Umbrella G34 · prop stamps", "Builds on G157 terrain paint" and "Determinism hash-from-cell,
never RNG". The page states no date and no author. The tool reported the live version id `1785667613-3ee7`, which read
as a Unix time is 2 August 2026 10:46:53 UTC; I treat that as a likely publish time, not a stated one.

Its content is identical to the studio file `tools/decorate/prototype.html` as committed in `13c00679` ("Migrate
PatternNoise down to Geom/Algorithms; decide dressing placement", 2 August 2026 10:47:11 UTC), apart from the page
wrapper. I checked this by diffing the two. The artifact is thus the published copy of that file, one minute older than
the commit, and the file in the repository is the same page that the model and the author were iterating on.

The page has six numbered sections plus a summary: 1 Flora overlay, 2 Paths, 3 Boulders, 4 Trees, 5 Ponds and
channels, 6 Symmetry and fairness (G162). The author's remark that the decoration "grew out of it" is accurate in a
precise sense: the page is the prototype of the whole dressing stage (plants over soil, paths dragged across it,
boulders, trees, water), and the tree is one of its five tools. It says of its method that the four prototypes "run on
the same four primitives": noise, a mask from the painted surface, a blue-noise scatter and a 3-D stamp seated on the
surface.

### 2.2 The tree generator

Section 4, "Two ways to grow a tree", offers two things.

**Vanilla templates.** Six parametric side-elevation trees, each a trunk height, a canopy radius and a canopy profile:

| species | trunk h | canopy r | profile |
|---|---|---|---|
| oak | 5 | 3.2 | blob |
| birch | 7 | 2.4 | blob |
| spruce | 8 | 3.4 | layered cone |
| acacia | 6 | 4.0 | flat umbrella, lean 3 |
| jungle | 10 | 3.6 | blob |
| dark oak | 5 | 3.6 | blob, 2-wide trunk |

**The grown tree.** The page's text calls it "not a fractal, and not a straight pole". The model, as the page and its
code state it:

- The skeleton is **recursive** in the sense of the "ez-tree" reference: levels of branching, children, a per-level
  taper and an upward pull. Every branch is a stepped path with per-step jitter ("gnarly"), then **smoothed into a
  centripetal Catmull-Rom spline** (the code's `catmull`/`splineOf`, six samples per segment). So the author's
  "spline-based" is right: the limbs are splines, but they are generated, and the page has no dragging of control
  points.
- The trunk is a **leader**: one long swaying, thinning spline that climbs into the crown, with lateral limbs
  staggered up its length, a small fan at the top and a crown cluster on the end. The sway is a slow noise on the
  heading, with a pull toward upright.
- **Stems** sets the base: one stem, a double or a triple (offset and angled apart).
- Wood is a **swept disc** along each spline whose radius tapers from the limb's start to its end; the page notes it
  is the §2 path primitive "lifted one dimension".
- The **crown** is placed the way a hand builder does it: one dense, oblate **disc cluster per branch tip**, pushed up
  and out from the tip and never down, about 92% full, with a **seam of air** between neighbouring clusters (a cell is
  filled only if it clearly belongs to one cluster, nearest-cluster ownership), and a few hanging strands below.
  Clusters shrink with the tree.
- Height couples to the rest: a smaller tree has a thinner base and fewer laterals, and a branch shorter than 3.5
  blocks is terminal, so a sapling is "a few clusters on a thin stalk".

The exposed parameters, from the sliders and `treeParams()` in the page:

| knob | range | default | what it does |
|---|---|---|---|
| height | slider 10 to 100, height in blocks = 12 + 32 x (slider/100), so 15 to 44 | 75, which reads 36 blocks | target tree height; scales base thickness, lateral count, cluster size |
| stems | 1 to 3 | 1 | trunks at the base |
| leader | 0 to 100, used as 0 to 1 | 55 (0.55) | how far the central axis climbs; low is a spreading fork, high a birch or conifer axis; the axis length is height x (0.5 + 0.34 x leader) |
| trunk flow | 0 to 100, used as 0 to 1 | 45 (0.45) | how much the trunk wanders (sway 0.12 + 0.5 x flow) and how gnarly the limbs are (0.14 + 0.28 x flow) |
| branch angle | 15 to 48 degrees | 30 | angle of child limbs off the parent |
| levels | 2 to 3 | 2 | depth of recursive branching |
| leaf size | 20 to 100, used as 0.2 to 1 | 60 (0.60) | crown cluster size |
| seed | 1 to 40 | 5 | the deterministic hash seed |

Fixed in the code, not exposed: child start 0.30, taper 0.62, child scale 0.6, length factor 0.62, trunk radius
0.7 + 1.5 x size. Two views are drawn: the **spine** (centerlines and thickness, each limb in its own colour, "the view
the tree is designed against") and the voxelised blocks. A "parameter sweep" row draws six trees across a height
gradient, then a double and a triple base, and a "forest" figure scatters trees by a low-frequency density field into
groves and clearings.

### 2.3 Other things the page generates

- **Flora:** a density field (fractal value noise with patch scale, octaves, threshold, seed), three scatter kinds
  (white noise, value noise, blue noise), masking by the painted surface so plants land only over soil, and a species
  mix with clustered flower fields (sliders for coverage, fern share, flower fields).
- **Paths:** a dragged centerline buffered by a radius, six variants (solid, worn, rough edge, Voronoi cobble, stepping
  stones, tapered).
- **Boulders:** ellipsoid masks half-buried, four shape families (rounded, angular, outcrop, cairn), four finishes
  (stone, andesite, mossy cobble, blackstone, with moss) and a scatter with exclusion zones.
- **Water:** ponds and channels carved to a bed and filled to one level, with depth, an irregular shoreline, reeds and
  lily pads.
- **Symmetry and fairness (G162):** a real generated board (its data comes from `tools/decorate/dress-map.cs` and
  `Composer.ComposeStages`, rot_180, seed 2) dressed twice, once with free scatter and once with props generated on the
  authored unit and fanned through the symmetry orbit, with unfair cover highlighted. Props that affect play are
  generated once and mirrored; flowers stay free.

It also names the tools it would reuse (`PatternNoise`, `SurfaceTop`, `ObjectiveStamper`, `BlockBox`, `SurfaceYOver`,
the sketch lasso, `SketchShape.Vertices`) and rule families `DR-FL`, `DR-PA`, `DR-SC`, `DR-TR` and `DR-WA`.

### 2.4 How it became the studio's tree code, and how it went

Everything below is from `git -C /home/user/pgm-studio log`. Times are UTC.

| when | commit | what the commit says |
|---|---|---|
| 1 Aug 23:46 | `a3160327` | "Prototype the decoration stage: flora, paths, boulders, trees (G34, G161)": `docs/world-export/decoration.md` and `tools/decorate/prototype.html`, "recursive tree growth" included |
| 2 Aug 00:13 | `de4e2ba1` | "Rebuild the grown tree as Catmull-Rom limb splines, not a fractal": "The recursive brancher read as a fractal, not a tree"; knobs limb count, spread, curve, leaf size |
| 2 Aug 00:20 | `4ab823b1` | trunk slimmed, limbs eased off a single fork |
| 2 Aug 00:35 | `20c87902` | recursive skeleton plus flowing Catmull-Rom spines plus the spine view; the **stems** knob is added; "Combines the two references the way requested: ez-tree recursion for the structure, Catmull-Rom for the flow" |
| 2 Aug 00:51 | `c443ce90` | the crown rebuilt as dense per-tip leaf discs with seams, "not a blob" |
| 2 Aug 01:06 | `7a36f9a9` | the **leader** knob, so "the trunk climbs into the crown" (it "died at the branch point... as if sawn") |
| 2 Aug 01:14 | `771ca1f8` | the **height** parameter, scaling trunk thickness and branch count |
| 2 Aug 01:26 to 07:16 | `b68b2336`, `b9e543df`, `3f3d6d17` | water, then the symmetry and fairness prototype |
| 2 Aug 10:47 | `13c00679` | the file as the artifact shows it |
| 4 Aug 01:17 | `616a3883` | "Grow the dressing stage's algorithms": `Geom/Algorithms/TreeSkeleton.cs` ("the prototype's grower lifted out of its side elevation into three dimensions"), `TreeCrown.cs`, `SweptVolume`, `BlueNoise`, `Blob`, `Polyline`; the decorator and the fairness rule (G161, G162) |
| 5 Aug 08:00 | `41b40336` | "Separate the vanilla tree from the grown one": `TreeTemplate.cs`; the species picker had been "six presets of the grower" that built one silhouette |
| 12 Aug | `c9ea46d6` to `674df496` | 75 hand-built trees measured; the grower retuned to the corpus ("leaves touching wood 14.8% to 54%", "wood in one piece 81% to 100%", then "An author adds crown as a tree grows, not timber") |
| 10 Sep 22:20 | `6b0b3f09` | "Remove the grown tree: a recipe is a species or a body": "`TreeForm.Grown` built its trees from a recursive skeleton and they came out broken; the author's ruling is that the form goes rather than gets a knob"; 496 lines of `TreeSkeleton`, `TreeCrown` and `SweptVolume` deleted, eight `TreeStyle` columns dropped by migration `M0035` |

So the artifact's tree model is exactly the first form of the code the studio later shipped and then removed. The
page's parameters were the grown tree's knobs: stems, leader, trunk flow, branch angle, levels, leaf size and height
(`6b0b3f09` speaks of "the eight fields only it read" and "the seven knob field names"; I did not list the eight). The
author's third instalment said the same: a spline-based editor of "number of main trunks, how branched", removed for
plain typical trees. The record sharpens two points. The "editor" was a generator with sliders, and the first spline
form was written within hours on 2 August, not before the decoration. And the removal came on 10 September, after the
12 August corpus work had spent a week trying to make the generator match hand-built trees.

The 50-log oak on No Blocks Placed is a studio tree "of that week's" (HISTORY §4). The artifact's version of the grower
is the one before the corpus retuning, so whether that oak was made by the 4 August code or a later one is not
decided here.

## 3. What could not be read or settled

- **Wandering U's authors, creation date and any test record.** The XML states none. Only the author says he built it
  and tested it on 6 August 2026. The Discord upload bot and the server log he mentions are not available to me.
- **How the map was made.** No commit names it; whether the long `<variables>`, `<structures>` and `<actions>` blocks
  were typed by him or written by a model is not shown. The XML's own comments are in the style of a model's.
- **Whether it ran.** Nothing shows PGM loading the file. The lap timing in the comment (22 ticks, 110 s) disagrees with
  the formulas (26 ticks, 130 s); I could not check which a server did.
- **The tree page's date and author.** The page states neither. The 2 August time comes from the tool's version id and
  from the identical commit, not from the page.
- **Exact list of the eight removed `TreeStyle` fields.** Not read.
- **The artifact's screenshots.** The page draws its figures with canvas scripts; I read the code, not the figures.
