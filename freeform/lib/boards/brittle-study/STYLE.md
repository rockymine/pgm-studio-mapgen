# Brittlebush — the visual signature, and a study in it

**Brittlebush I and II are read here for their look, and `scripts/style.py` writes that look as functions.** The
two maps are in CommunityMaps, at `ctw/brittlebush` and `ctw/brittlebush_ii`. They were read block by block with
`tools/anvil.py` and rendered with pgmvox's renderer, so the `ref-` renders here and the study's renders compare
like with like. The study, `scripts/gen.py`, is a swatch rather than a map: it has no objectives and no match.

## How the two maps were read

- A census of every block, and of everything above y 20, which is where the wool rooms' towers stand.
- The commonest stack of blocks, top down, at a column on a platform's edge and at a column inside one. A
  column was counted as an edge when one of its neighbours is empty three under its top.
- Letter maps of the top block over a platform, to read how its floor is laid out.
- Isometric close views, sections through a platform and a tower, and one face panel printed course by course.

## The signature

**A platform is a bedrock block with a decorated cap five courses deep.** Under the floor lie four courses of
stone, then bedrock to y 3. An obsidian sheet two thick lies at y 1 and 2 under everything, and bedrock at y 0.
The cap is the only part of a face that is dressed. Below it the face is plain bedrock, which reads as dark mass.

**Every edge carries the same five courses, top down.** An upside-down spruce stair sits at the floor, its full
side inward, so the floor is flush and its underside steps back. Under it lie a course of brick, a dark-oak slab
that leaves a groove, and an upside-down dark-oak stair. A course of black stained clay finishes the cap. Read
from the void, it is a brown cornice, a thin red line, a shadow, a moulding and a black band.

**A long face carries one light panel in its middle.** There the brick, slab and dark-oak stair give way to three
birch stairs under the black clay, two upright and one upside-down. The pale inset stands out against the dark
band like a shuttered window.

**The floor is laid as nested frames.** The spruce-stair rim runs round the edge, and a band of spruce planks one
wide runs inside it. Inside the band are fields of four kinds.

- **Beds.** Grass inside a kerb of sandstone stairs rising toward the middle, with sandstone at the corners. Tall
  grass, alliums and low bushes of birch leaves grow in a bed, and a round birch tree in the larger ones.
- **Sand.** Plain sand with upside-down sandstone stairs lying on it as pebbles, cacti one to three high, and dead
  bushes.
- **Paths.** Stone brick and stone-brick slabs in alternate rows, so the grey path is ribbed.
- **Decks.** Spruce planks.

**Levels are joined by flights of grey stone.** The flights are broad, with plain stone sides, and they are the
only grey faces on the board apart from the bedrock.

**A wool room is the base of a tower of narrow storeys, each stepped back from the one below.** A storey's walls
are black stained clay, with birch-stair panels like the platforms' and a band of the wool's colour under its
roof. Each storey's plate has the platforms' own edge, a spruce-stair rim over dark-oak brackets. The top plate
carries a ring of sandstone stairs round a centre of gold.

**Over each tower floats the wool's heart.** It is a pixel heart in the wool's colour, outlined and backed in
black wool, standing upright high above the roof.

**A dotted line of cobwebs lies on the floor of the void.** Single cobwebs five apart at y 1 trace the board's
bounds and the gaps between platforms.

**The palette is three woods, sandstone and black.** Spruce for the rims and decks, dark oak for the mouldings,
birch for the panels; sandstone and sand for the fields; black clay and bedrock for the mass. Colour comes only
from the grass, the alliums and the wools. Brittlebush I adds water at the floor of the void round the towers'
bases.

## The study

**The study is three platforms at 10, 13 and 16, two flights between them, two islets and one tower.** Each
platform is laid with `style.face`, `style.base`, the frame, and fields of sand with beds and paths over them.
The tower has three storeys over the yellow wool's room, the crown of sandstone and gold, and the heart.

**It reads back clean.** No block falls or hangs on nothing, and no water stands against air.

**`renders/01-original-and-study.png` sets the study beside Brittlebush II.** The faces, the frames and the
tower read as the same hand.

## What it does not copy yet

- The originals' platforms are tall bedrock blocks, often twelve or more high. The study's are lower, so less
  dark mass shows under each cap.
- The originals mark each spawn with a line of the team's wool along its edge and a stack of the team's colour
  floating high over it. The study has no spawn.
- The originals' towers stand on a tall bedrock plinth. The study's tower stands on its yard.
- The trees are a simple round birch, not the originals' darker oak-like crowns.
- There is no water, and nothing about how the maps play was read.

## What a studio feature would need

| What I wanted | How hard it was | What a studio feature would need |
|---|---|---|
| A platform's edge as five dressed courses | Easy once read: one function per column, given the side it faces | An edge profile on a theme: the courses under a piece's rim, top down |
| One panel in each face's middle | Moderate: each face column finds its straight run at one height | Panels placed per face run, centred, from the piece's outline |
| Floors as nested frames with fields | Moderate: depth from the piece's edge, then fields laid over | A floor recipe: rim, band, and named fields drawn on the plan |
| A tiered tower with a floating heart | Moderate: a storey function and a pixel stamp, placed by hand | A tower piece stacking storeys, and a heart stamp for each wool |
| Reading a hand-built map's style | Moderate: a census and edge and inner stacks, then close views | A style read over an imported world: its edge stacks, floor fields and palette |
