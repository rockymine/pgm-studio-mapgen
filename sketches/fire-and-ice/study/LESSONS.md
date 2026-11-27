# What went wrong, and where the limits were

**This is the study's record of its failures and its limits, written for the documentation that comes after it.**
Each entry states what happened, what it cost, and what now prevents it.

## The composition before the study

**Rebuilding the whole map from its structures' footprints failed on nearly every judgement a player makes.**
`compose.py` in the folder above is that attempt. The author rejected each version, and these are the reasons:

- the surface was not closed;
- stairs stood exposed;
- the mountains broke into separate pieces;
- a "floating island" taper had been added under the terrain without being asked for;
- terrain collided with structures;
- a gorge was cut above the wool room;
- a stone block replaced a facade;
- the map sat 8 blocks too high;
- a ramp led into the void;
- panels were filled in as solid ground;
- the floor was copied block for block, with visible seams.

**The author then built the map themselves, and the study's task became understanding it rather than replacing it.**
The lesson that carried over is that a geometric rule is not a design. Every one of those failures passed some check
that existed at the time.

## The reconstruction

**The first line model overbuilt by up to 14% on some pieces until forks were lofted arm by arm.** Where one line met two,
each arm was joined to the whole of the next line. That twisted the strip across the dip between the arms, 2–5
blocks high over 234 floor blocks. Lofting each arm onto its own stretch of the line it meets brought every piece to
99% or better.

**The lines found are not the author's lines.** They reproduce the surface to within a block, but the author's tool
holds the true lines and their density. Every density comparison in the study measures against this inferred
density, not the author's.

## Briefing the agents

**Agents handed a concept produce that concept, so the author had them sent without one.** The first launch named a
concept for each variant, one of them a ravine the author had liked before. The author stopped it, because the point
was to see what agents find on their own.

**A rule stated too strongly removes whole families of answers.** "Flat ground in the main flow" ruled out any
ravine in the middle. The brief now says the main flow stays walkable and readable, and need not be flat.

**Facts about the map that the agents could not derive had to be stated, or they guessed.**
- Every middle agent read the 2×2 pivot stone at y 18 as the middle's ground height, but it marks the pivot only.
- One agent drew the two team halves as fire against ice in different materials, but both halves are built from the
  same blocks.
- The contest the map was first made for had been cancelled, and the map is an ice map.

**Colour carries meaning, and agents painted it as a blanket.** Yellow is the flatter ground that connects; light
blue is the hillier ground. A cover that is mostly one colour says nothing about its form. The brief states the
meaning, and every piece is coloured by what its ground does.

**A retaining wall does a big job or it is not there.** One middle variant dressed its spoil heaps with small walls.
The author's walls hold back a whole mountain or take up a real step: 19, 13 and 14 blocks tall. The brief now names
those three walls with their coordinates.

## Measuring the middle

**The gap was measured as everything empty between the halves, which counted the bays beside it.** Every middle
variant built into those bays. A rim-closing step added to tidy the measure grew it further. The author's definition
is the span between the two facing edges, closed by straight lines between their outermost points. The east end of
that span sits at the corner where the wool lane runs out of the underground, which the author placed by eye.

**A polygon test on whole blocks is not symmetric under the turn.** Columns on the boundary fell inside on one half
and outside on the other, and a symmetric variant could not fill both. The region now adds the turn of every column
it keeps.

**The author's centre-line markers were read as structure.** The 14 lapis blocks and the pivot stone left one-block
pits in a variant that respected them. The kit now reads the map without them.

## Checks that did not check

**Every check read the blocks, and the viewer draws the lofts.** Agents clipped their blocks to the span, while their
loft lines ran up to 29 blocks past it. The checks reported a pass on variants the author saw as plainly wrong, and
the reports were relayed without being looked at. The gate now refuses any loft point more than 2 blocks outside the
allowed area.

**Checks that only advise get passed over.** Agents reported their numbers and delivered failing variants anyway.
`kit.write` now refuses to write a variant the gate fails, so a wrong variant cannot reach the viewer.

**A loft drawn at the centre of its top block reads half a block low.** A cover that was flush with the checkerboard
roof in blocks looked, in the mesh, as though it ran under the roof. Every loft, the author's and the variants', is
now drawn at the top face of its blocks.

## The cover over the building

**The map is hollow, and agents treated it as solid.** It holds only surfaces and the empty mass between them. The
stairwells and back rooms float in that void, and will be sunk into solid ground later. Three of the first four
covers drew planes low beside the building and left stairwells standing open above them. The author's rules turned
this into checks:
- the surface lies at or above the walk level of the facade's top exit, y 48;
- it is flush with the flat roof and with the light-blue mountain;
- the black-roofed penthouse stands free.

**A rule must count the author's own ground as cover.** Twelve columns in front of the south stair lay under the
author's mountain. The check demanded that the new cover cover them too, and refused a correct variant until it was
fixed.

**Terrain reaching into the roof at roof level reads as pushed in.** One cover filled the slots between the
checkerboard plates with yellow ground, 14 blocks deep into the roof. Another closed them in light grey, as roof,
and was accepted. The gate refuses terrain-coloured blocks inside the roof's outline at roof level.

**Sinking every opening behind the facade sank a real exit.** The brief let openings under the cover go with the
rest. That blocked the south stairwell's west exit, the one way out at the back that connects to the building's
inside. The building's real exits are now named in `kit.DOORS`, and the gate refuses any block in or in front of
them.

## What a person builds by hand

**A shape an agent builds is not a shape the author can set point by point.** The Eismulde's agent laid lines every
3 blocks across the gap: 49 lines and 158 points for one side. Four long lines along the gap carry the same basin in
27 points, 96.6% of it within a block. Lines that follow the feature beat dense cross-sections, and the brief
should ask for the fewest lines that hold the shape.

## Limits of the environment

**The cloud container could not reach the CDNs the published page loads from.** Every check of the viewer ran
against local copies of three.js fetched with `npm pack`. The page itself was only seen through screenshots.

**Agents never saw the viewer.** They judged their work from iso renders of the blocks, and those renders do not
show the lofts. That is half of why the loft overshoot went unseen until the author looked.

**Editing the author's world needs care that a fresh world does not.** The middle lay where the author's world had
no chunks yet. `markers/edit.py` creates empty chunks there and sets `LightPopulated` to 0 so the server relights
them. Its reads and writes are lossless and keep every tile entity.
