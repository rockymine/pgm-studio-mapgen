# Authoring ClayClay Redux — a report from the agent that did it

Written for whoever works on `tools/mapgen` next. It is deliberately in the first person and full of
opinion, which is not the house doc style — the request was for an honest account rather than a
reference, and the two want different registers. `FINDINGS.md` beside this file is the measured half;
this one is the judgement half, including where the judgement was wrong.

## What was done

The task was to recreate `OvercastCommunity/CommunityMaps/ctw/clayclay` and report what the system
could not express. Five rounds, each driven by the author reviewing the build and naming what was
wrong with it.

1. **Read the original before writing anything.** `--island-sketch` for the outlines, `--surface` for
   the tone census, `--structures` for the rooms, and a column probe for the stacks. That produced the
   board: `rot_180` about world (47, 15), two plus-shaped islands of 13-wide bars, two detached 13×13
   caps, four 21-block void hops.
2. **First build through `tools/mapgen`.** Geometry correct, materials wrong — dark prismarine and
   nether brick on a map made entirely of stained clay. Diagnosed to the spec, not the system.
3. **Switched to driving the studio's API directly** (`tools/build.cs`, six calls), injecting
   `themes` / `mapTheme` / `roomStyles` into the compiled layout. That reached every block.
4. **Four review rounds from the author**, each finding real things: the side pattern was invented
   rather than measured; the houses were in the wrong style; the bedrock wall was in the wool house's
   face rather than fifteen blocks out; the two rooms were sharing one style; the spawn platform was
   17×13 rather than 17×17; a spur ramp was missing entirely; the floor was too organised; the sky
   marker claim was simply false; and the whole dressing layer, which I had twice called impossible.
5. **What it ends as**: 142×158 — the original's dimensions exactly — with the spawn approach
   (15 → 14 four deep → 13 five deep → 12) and the east spur ramp matching block for block, the
   measured layer stack on the risers, a barn over the spawn and a two-storey house over the wool,
   grass, a tree on each middle island, and the hub puddle where the original has it.

The author supplied every correction that mattered about *the map*. The measurements and the code
reading are mine. That division is worth stating because it is exactly the division `CLAUDE.md`
already prescribes — "a rule about the map as it is played is not derivable from this repository" —
and it held: every time I inferred a gameplay fact instead of asking or measuring, I got it wrong.

## The headline: the spec is the wrong layer, and I hit it in the first hour

Yes — I disliked it, and not mildly.

`MapSpec` is a closed vocabulary sitting *above* the plan document, and every one of its fields
narrows something the system underneath can already say:

| The system can say | `MapSpec` can say |
|---|---|
| any block, by id and data | a **palette family** name, resolved to the family's *first* entry |
| fourteen `MaterialKind`s, each nesting inside any other | six, and only on the `surface` bucket |
| any room style in the `room_style` table | one of **ten hardcoded** `HousePresets` names |
| six prop kinds placed where the author puts them | trees and villages as **populations with a count** |

The failure was immediate and total. ClayClay is built out of stained clay. Of the sixteen stained
clays, exactly two — lime `159:5` and cyan `159:9` — are reachable from a spec, because they happen
to sit first in `verdant` and `slate`. The blue that is 23% of the original is third in `azure`,
behind blue *wool*. So the first build came out prismarine and nether brick, and no amount of tuning
the spec would ever have fixed it. That is not a missing knob; it is a layer that cannot express its
own subject.

**The deeper problem is that `tools/*` is a reimplementation, not a caller.** `mapgen`'s `Forest`,
`Village` and `Preset` are a second implementation of placement — a `random.Next` over ground cells
with a keep-out mask — sitting beside a dressing pass that already places props, fans them across the
symmetry orbit, seats them on real ground, and lets an author say *where*. The spec's version is
strictly weaker and structurally different: it scatters where the real one authors. `HousePresets.All`
is a C# array duplicating rows that exist in `room_style`. The theme families duplicate a palette the
library exposes per block through `GET /terrain/blocks`.

So an agent handed `mapgen` is handed a worse model of a system that is sitting right there. The
correct move turned out to be the one I eventually made: **ignore the spec and drive the real
endpoints**, which are documented well enough in `docs/tools/*.md` to do blind. Six calls, no UI, no
guessing. `plan.md`'s "Driving it without the UI" is the single most useful page in the repository,
and it made the whole recreation possible after the spec had failed.

My recommendation, for what it is worth: **`mapgen` should compose the real thing rather than
reimplement a subset of it.** A spec is a fine idea — a terse way to say what a map is about — but it
should expand into a plan document, a theme JSON, room-style JSONs and a dressing list, and then post
those. Every field it cannot expand to should be a field it passes through verbatim. The moment the
spec becomes the ceiling rather than the shorthand, an agent hits it and has to leave anyway.

## Where I was wrong, and it was not the tool

**I said twice, in a committed file, that dressing was unreachable. It was reachable the whole time,
and the evidence was in front of me three separate times.**

- The very first thing I ran on the original, `--island-sketch`, printed the layout's top-level keys.
  `dressing` was one of them. I read that output and moved on.
- I later quoted `SketchLayout.FinishKeys = ["themes", "mapTheme", "roomStyles", "dressing"]`
  *verbatim* into my own notes, as evidence for a different point, and did not notice the fourth key.
- `docs/tools/sketch.md` has a Dressing phase with a table of six prop kinds. I had the file open.

What actually happened is an anchoring failure with a specific shape. I built my model of "what can
be said" out of `MapSpec` first, because that was the tool I was pointed at. `MapSpec` offers trees
as a *population* and houses as *presets*, so "dressing" registered in my head as a closed,
parameterised thing rather than as an authorable document. When I then went looking for a clay tree
and found `DressingPalette.Woods` — six rows, closed — I took that as confirmation of the model I
already had, and generalised from *"a tree's wood is a fixed palette"* to *"the dressing half is not
addressable"*. Those are very different claims and I did not notice I had swapped one for the other.

The tell I should have caught: when I wrote the sentence "the terrain half is block-addressable and
the dressing half is a closed vocabulary", I was describing a **symmetry break in someone else's
design** — and a well-built system rarely has one that stark. That should have sent me back to check
rather than into a commit. `CLAUDE.md` warns about exactly this failure mode in the destroyable/core
story: "the measurement was right and the conclusion was invented". Mine was the same shape.

The same anchoring produced a second false claim — that nothing places a sky marker over a wool —
when `GoalMarkerStamper` had been stamping one over my own builds all along, four blocks above the
build cap. I had not probed high enough, and asserted absence from a failure to look.

Is it prompting? Partly. Being pointed at `mapgen` first framed the whole problem as "what can this
spec say", and I never fully re-framed after abandoning it. But the honest answer is that the
information was in my context and I did not act on it, and a doc that says "read `surface.md` before
writing anything against this tool's spec, which is a reduction of it" told me the spec was a
reduction on line 3 of the README. I read that line and still used the reduction as my model of the
system.

## What I liked

**The documentation is the best I have worked against, and it is not close.** `plan.md`,
`library.md` and `sketch.md` each say what the thing is, what it writes, what it refuses, and how to
drive it without the UI — and the last of those is what turns a studio into something an agent can
use. Being told that `PUT /sketch/from-plan` *merges* while `PUT /sketch` *replaces*, and why, saved
an entire debugging cycle I never had to have.

**The prose-carries-the-claim rule works.** I could not have inferred "a layer stack renders as one
flat colour from above" from a table, and it is the sentence that told me to nest a `cell` inside a
`layered` — the single most useful thing I learned all session, and the fix that got both the patchy
top course and the measured depth at once. Everything nesting inside everything is a genuinely good
design and it is documented as a property rather than as a list of legal combinations.

**The measurement tools are excellent.** `--surface`'s tone census, its "scattered or laid in fields"
table, `--structures`' seat/tall/rough columns, `--island-sketch`'s outlines. I recreated a map's
geometry to the block from those alone. A tool that tells you patch counts and median field size is a
tool built by someone who has actually had to answer "does this read right".

**`CLAUDE.md`'s human-oracle rule is correct and I should have leaned on it harder.** Every single
thing I got wrong about the map — the wall's position, the house styles, the platform size, the spur
ramp — was a gameplay or authorial fact that measurement could have answered but inference did not.
The rule exists because someone already made this mistake; I made it again in a smaller way.

**The refusals are informative rather than obstructive.** A 422 naming rule ids and subjects is
something an agent can act on. The distinction between the compile's refusal and the evaluator's
advice — "read the score as advice about a board's shape and the compile's 422 as the only refusal" —
is exactly the right thing to tell a model.

## What I disliked

Beyond the spec, in rough order of how much they cost:

**No renderer shows a vertical section.** All six are plan-view. `layered` exists precisely to vary
down a riser, and nothing can draw it. `--underground` looks like the exception and is not — it
reports enclosed space, so on a solid map it found only the room interiors. I had to write
`tools/column-probe.cs` to see a stack at all, and it is what verified the wall, the steps, the
rooms and the water. Six renderers and no section is a real hole.

**`--structures` merges a building into the ground when they share a material**, which is the normal
case for a themed map. The original's rooms separate because they are red sandstone on clay; mine
vanished the moment I painted the ground the same clay the shell was. So the check that says "did the
room stamp" silently stops working exactly when a map is well themed.

**The traversability read argues against a legitimate map.** Putting the bedrock wall where the
original has it moves the number from `0 isolated` to `2`. The original measures `2` as well — so the
number is right — but it is *reported as a fault*, and a model authoring a map will remove the wall to
clear it. A full-width wall standing proud is a feature of many CTW maps, built over rather than
walked around. The measurement models walkable ground with headroom and has no way to say "this cut is
intended", so the tool ends up lobbying against the design.

**`BlockPalette.Name` answers "Tall Grass" for `31:1`,** which is the plain one-block grass; tall
grass is `175:2`. Not a loose label — the name of a different block, appearing in every census. A map
that deliberately sets `tallShare: 0` has its own report tell it 374 columns of tall grass landed.

**A spawn-role piece is left unpainted** — raw stone under it, while a plain piece raised to the same
height paints correctly. On an otherwise fully themed map that is a stone cliff under every spawn.

**Undocumented fencepost:** `surface: N` puts the top block at `y = N−1`. Every height in the
recreation was one low until I noticed. Any plan tracing a real map has to match absolute heights, so
this belongs in `plan.md` in a sentence.

**`globals.maxPlayers` lands per team**, which reads as a total.

**The build/lock hazard is real.** The running API holds its own DLLs; rebuilding after a pull fails
with sixteen MSB3027s that look like compile errors and are not. `CLAUDE.md` warns about concurrent
builds; this is the adjacent case and costs the same confusion.

## The one-line version

The system is good and the spec in front of it is not, and the fastest thing anyone could do for an
agent authoring maps here is to delete the reimplementation and point it at
`docs/tools/*.md` and the endpoints those describe. That is what I ended up doing, and everything
that went right went right after it.
