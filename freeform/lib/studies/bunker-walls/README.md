# Bunker walls

**A bunker's walls and floors stated as one grammar: a face is cut into segments, and a segment is a rectangle
peeled side by side into strips.** The author's segment is six wide and eight tall on a wall two blocks thick.
Two L shapes frame a panel.

**The segment's blocks are the author's, colour by colour.** The outer L is cobblestone fading into cobblestone wall, and the inner L is polished
andesite. Under the inner L's top bar runs a stone-brick top slab with nether brick behind it, and the panel is
andesite fading up into stone. Everything behind the face is cobblestone.

    cd studies/bunker-walls/scripts && MINECRAFT_JAR=/path/to/1.8.9.jar python3 build.py [swatch corners floors facade]

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
two bays by two tiers, 12 by 16. The bays over it are asked for as tier `"over"`, and the facade puts the dark
segment there.

**A floor is the same segment laid flat.** It aligns to the wall's module, so the tile seams line up with the
segment seams of the face above.

## The sheets

| Sheet | What it shows |
|---|---|
| `swatch-*` | the six segments in a row, two tiers: the author's, a gray-wool cross, two obsidian studs, the dark L's, a bedrock-framed dark slot, bedrock and gray wool with two slits of iron bars over gray glass |
| `corners-*` | one footprint with two outward and two inward corners, three tiers. The crown sits over the front: polished andesite, the stair nook, stone, andesite two under a black-wool roof stepping to the middle |
| `floors-*` | three floors at the wall's module: a stone L, a light-gray-wool L and a clay core; a stone grid with clay and light-gray wool alternating; a double-slab grid with a smooth-slab plate in each tile |
| `facade-*` | a keep 24 wide standing 7 forward of a 48-wide main wall (32 and 24 tall), the door, two dark bays over it, the gable crown, two blast walls 4 thick and 14 long falling 19 to 16, the forecourt paved on the keep's module, two lofted retaining walls each side holding the mountain |

**A lofted wall is two planes spanned the way a loft tool spans them.** Each plane runs 24 along. The first
plane comes forward 5 at its foot, the second plane comes forward 10 more, and both lean back 5 over 16. At every
height the face is the polyline through the edge points at that height, three blocks of wall stand behind it,
and stone fills behind that.

**The lofted face is painted by height and marked.** It fades from cobble through polished andesite and andesite to stone. Two
marks are inlaid: a gray-wool line along both planes, and a number in obsidian.

## What pgmvox already had, and what this adds

| Need | pgmvox before | Here |
|---|---|---|
| a block in the face and one behind it | `grammar.rules.Course(block, back)` | the same idea as `Solid(block, back)` |
| the upside-down stair facing out | `core.orient.stair(rises, upside_down)` | `Nook` |
| slits, glyphs and words on a face | `built.facade` patterns, `LETTERS` | `slit`, `Bitmap`, the loft's marks |
| floor fields | `built.facade` floor fields, `carpet` | a floor as a flat segment, aligned to the wall |
| a face cut into bays | `Accent`: one bay every so many, top down from a rim, refused at corners | segments that tile the whole face, stack in tiers and stretch to fit |
| nested frames | none | peels |
| a fade along a strip or up a core, with noise | `Mix` (by weight, with no position) | `Fade` |
| corners | a corner keeps the plain courses | the left leg wraps an outward corner |
| a door in a face | none | `Opening`, laid by its own function |
| a band following a stepped roof | none | `crown` |
| a ruled plane between two edges | `forms.sweep` (a cross-section along a path) | `loft` |

## Limits, as built

- **The crown and the blast walls show bare ends.** The crown's sides are its stone fill, and the blast walls
  fall in whole-block steps that a player can climb.
- **A leaning loft steps a block back every three or so,** which is what a loft tool does too. Andesite has no
  stair or slab in 1.8, so smoothing those steps would mean mixing in another material.
- **The light-gray-wool L and the clay core of the first floor are close in tone.** The tile reads by its stone L.
- **Nothing here is held to a hash,** like every study; `check.py` does not build it.
