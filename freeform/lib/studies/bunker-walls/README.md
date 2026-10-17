# Bunker walls

**A bunker's walls and floors stated as one grammar: a face is cut into segments, and a segment is a rectangle
peeled side by side into strips.** The author's segment is six wide and eight tall on a wall two blocks thick.
Two L shapes frame a panel.

**The segment's blocks are the author's, colour by colour.** The outer L is cobblestone fading into cobblestone wall, and the inner L is polished
andesite. Under the inner L's top bar runs a stone-brick top slab with nether brick behind it, and the panel is
andesite fading up into stone. Everything behind the face is cobblestone.

    cd studies/bunker-walls/scripts && MINECRAFT_JAR=/path/to/1.8.9.jar python3 build.py [swatch corners floors stagger interior facade]

**The grammar and the style are library code.** The grammar is `pgmvox.built.segments` and the author's blocks
`pgmvox.grammar.bunker`; this study's `build.py` builds its sheets from them, and `boards/sixes-and-sevens` is
their second user.

## The grammar

**A segment is a list of peels and a core.** Each peel takes one row or column off one side of what is left, in
one material, and the core is the rest. The author's segment is five peels: top in the cobble fade, right in
the cobble fade, top in polished andesite, left in polished andesite, top in the slab-over-nether-brick. The
core is the andesite-to-stone fade. The order is the meaning: the outer L's top bar covers the full width because
it is peeled first, and the inner L's top stops one short because the outer L's right leg was peeled before it.

**A peel's strip has a length, and a fade runs along it.** A top strip runs left to right and a side strip bottom
to top. That is what makes the outer L read as one gradient: its top bar is cobble at the left and wall at the
right, its leg is cobble at the foot and wall at the top, so the elbow is wall and both ends are cobble. A core
fades by its height. `Fade` blends between stops with a fixed per-block noise, 0 cutting sharp and 1 dithering the
whole span.

**A material says what stands in the face and what stands behind it.** `Solid(block, back)` puts `back` one block
in. That is the whole of the slab trick: a top slab at the face shows the nether brick behind it through the
half-block gap. `Nook` is the second design's upside-down stair with its full half at the back, a half-block
nook that runs unbroken along a course.

**A face is every straight run of wall open to the outside, cut into segments as near six as the run allows.**
`cuts` gives the extra columns to the cores from both ends inward, so a run of 14 is two segments of 7 and the
legs stay one wide. Heights are cut the same way into tiers of eight, and tiers stack.

**An outward corner wears the next segment's left leg on both its sides.** This follows the author's corner
drawing. A column open on two sides belongs to the face whose left end it is, read from outside. From the other
face, the corner shows as one more polished-andesite column after that face's last cobble leg. So every outward
corner reads cobble, then polished andesite, whichever way the footprint turns.

**An inward corner needs no rule.** The last segment's cobble right leg meets the next face's polished-andesite
left leg at 90°. That is the same contrast that separates two segments on a straight wall.

**An opening is cut out of the segments, and what stands over it is a segment chosen for it.** The door slot is
three bays by two tiers, 18 by 16. The bays over it are asked for as tier `"over"`, and the facade puts the
obsidian-stripe segment there. An opening names its face's line when two faces look the same way, as a tunnel's
mouth does in the interior.

**A segment may stand out of line with its neighbours.** `staggered` sets bay i forward by i times one shift and
tier j by j times another. One block per bay runs the wall on a diagonal, one block back per tier leans it, and
both together slant it two ways. Every step shows the end of a segment's leg.

**A floor is the same segment laid flat.** It is laid on a four-block grid counted from a tile's corner.

## The sheets

| Sheet | What it shows |
|---|---|
| `swatch-*` | the six segments in a row, two tiers: the author's, an obsidian stripe, a gray-wool stripe, gray wool under cyan clay, the dark segment, the slit |
| `corners-*` | one footprint with two outward and two inward corners, three tiers, and the crown over the front |
| `floors-*` | three floors on a four-block grid, each tile lined on two edges and filled in two pieces: clay and light-gray wool round an andesite L and a stone square; the same lining round an andesite bar and stone; cobblestone and andesite round a cyan-clay L and a gray-wool square |
| `stagger-*` | four bays by three tiers on a diagonal, leaning back, and both |
| `interior-*` | a hall 24 square and two segments tall, a room 24 by 36 and three tall, a dark room 18 square and three tall, tunnels 6, 12 and 18 wide and one tall, every wall in segments |
| `facade-*` | a flat front 42 wide and three tiers tall with the 18-by-16 door, the crown over it, two blast walls, four bays of slanted panels to the west, one lofted wall past them and one beside the east blast wall running out to the south |

**Three light segments take the dark segment's rows.** Their cores are read down from the top through `Courses`.
Two have stone on top, a stripe of obsidian or of gray wool under it, and the andesite-to-stone fade below. The
third has stone on top, a row of cyan clay, and gray wool below.

**The dark segment is the author's peels in the dark family.** Coal is the top row, black wool the right leg and
obsidian the inner L. The slab row is a nether-brick slab with gray wool behind it. The core is bedrock with a row
of cyan clay one under its top, and a taller core stretches at its foot.

**The slit is bedrock and iron bars alone.** A bedrock frame holds columns of iron bars over gray glass, alternating
with bedrock, so there is no field of gray wool round them.

**A floor tile is lined on two edges and filled in two pieces.** It is four a side. Its top edge is one block of
the lining and its left edge the other, so every tile shows an L of two blocks. The three-by-three inside is an L
and a two-by-two square, or a bar one wide and a two-by-three.

**The floors' blocks follow the room.** The light floors line in clay and light-gray wool
and fill in andesite and stone; the dark floor lines in cobblestone and andesite and fills in cyan clay and gray
wool. Each space counts its tiles from its own corner.

**The interior is the facade's grammar turned inward.** The walls are every column within two of a space, the
outside is the spaces themselves, and each wall is as tall as the space it faces. A tunnel's mouth is an opening
in the room's face, so the room's segments stand either side of it and over it.

**The author's segment is the interior's ground, and the others are used sparingly.** Tunnels are the author's
segment alone. The hall puts the gray-wool stripe over it. The room stacks gray wool under cyan at its foot, the
author's segment, and the obsidian stripe under its rim.

**The dark segment has a room of its own,** at the end of
the 6-wide tunnel, where it stands at the foot under gray wool and then the author's segment, over the dark floor.
Nothing is roofed.

**The crown's stone and andesite sit a block back.** The plinth and the stair nook stand in the face, and so does
the black-wool roof, so the roof is the only overhang: over the inset, and a block past each end.

**West of the front, the panels slant two ways.** Four bays stand each a block further back than the one nearer
the door, and each tier a block back from the one under it, so the face runs back on a diagonal and leans.

**A blast wall is four wide for its whole height, painted like the lofted walls.** It stands against the flat
front, 14 long. The face fades from cobble to stone with the loft's noise, and a gray-wool line runs round it ten
blocks up. Its top falls from 19 at the front to 16 at its end.

**A lofted wall is planes spanned the way a loft tool spans them, and its edges may differ in height.** The west
wall runs along the front past the panels: from their end 24 out and 5 forward, then 24 more and 10 forward, its top
falling from 20 to 15 to 8. The east wall starts against the east blast wall and runs out to the south: 24 out
and 5 east, then 24 and 10, falling from 21 to 15 to 7. Both lean back 5.

**Where an edge ends below a height, the plane is cut along its top,** so the wall falls in a slope rather than a
step.

**The lofted face is painted by its own height and marked.** It fades from cobble through polished andesite and
andesite to stone over the height of the wall where it stands, so a low end still reaches stone. Two marks are
inlaid: a gray-wool line, and a number in obsidian.

**The ground behind every wall stays a block under its crest.** The walls are three thick. For three blocks behind
a wall's top edge the ground lies a block below it, so the crest reads as the edge holding the mountain back, and
only then does the ground rise.

## What pgmvox already had, and what this adds

| Need | pgmvox before | Here |
|---|---|---|
| a block in the face and one behind it | `grammar.rules.Course(block, back)` | the same idea as `Solid(block, back)` |
| the upside-down stair facing out | `core.orient.stair(rises, upside_down)` | `Nook` |
| slits, glyphs and words on a face | `built.facade` patterns, `LETTERS` | overlays, `Courses`, the loft's marks |
| floor fields | `built.facade` floor fields, `carpet` | a floor as a flat segment, aligned to the wall |
| a face cut into bays | `Accent`: one bay every so many, top down from a rim, refused at corners | segments that tile the whole face, stack in tiers and stretch to fit |
| nested frames | none | peels |
| a fade along a strip or up a core, with noise | `Mix` (by weight, with no position) | `Fade` |
| corners | a corner keeps the plain courses | the left leg wraps an outward corner |
| a door in a face | none | `Opening`, laid by its own function |
| a band following a stepped roof | none | `crown`, inset under its roof |
| a ruled plane between two edges | `forms.sweep` (a cross-section along a path) | `loft` |

## Limits, as built

- **The crown shows bare ends,** its sides being its stone fill.
- **A blast wall's falling top is steps a player can climb.**
- **A leaning loft steps a block back every three or so,** which is what a loft tool does too. Andesite has no
  stair or slab in 1.8, so smoothing those steps would mean mixing in another material.
- **Andesite and stone are close in tone,** so the light floors' inner L reads faintly; clay and light-gray wool
  likewise.
- **The floors' four-block grid is not the wall's six.** The two meet every twelve blocks, and a 6- or 18-wide
  tunnel or the 18-wide dark room ends in a part tile.
- **A tunnel mouth's reveal is the wall's body,** cobblestone on its inner block.
- **The interior has no roof;** that is still to be decided.
- **Nothing here is held to a hash,** like every study; `check.py` does not build it.
