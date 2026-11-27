# Brief: missing terrain for the ice map

You design ONE terrain variant for a Minecraft PGM map (a CTW+DTC hybrid) built by its author. It is an ice map: cold
tundra, perhaps with hot springs, or lava caves with lakes underground. The theme plays only a small part in the design
of the middle and the mountain. Your prompt names your variant id and its slot (`middle` or `cover`). **The idea is entirely yours**: no
concept is given, and none is expected. Find what the ground there should be from the map itself — its structures,
its routes, the author's terrain around the gap — and from how the map is played. Several agents work on the same
slots in parallel, each on its own; do not open other folders under `$S/variants/`, and do not open `$S/mid/` or any
earlier design for the middle — for you they do not exist.

## What exists — read it, do not redo it
Study root: `S=sketches/fire-and-ice/study` in pgm-studio-mapgen.

- **`$S/variants/kit.py` — read it first.** The shared toolkit:
  - `kit.existing(full=True)` gives the map as it stands, as `{(x, y, z): (layer name, group)}`.
  - `kit.middle_gap()` gives the missing middle, as columns.
  - `loft_blocks` and `loft_tris` turn lines into lofts.
  - `kit.checks` runs the checks, `kit.render` draws an iso picture, and `kit.symmetric` handles the 180° symmetry.
  - `kit.write` writes the export the viewer reads.

  Do not edit it. Put anything extra in your own folder.
- **`$S/viewer/map.json` holds the author's built half**, every block with its layer; kit loads it for you. The layers come in three groups:
  - **Gelände:**
    - floor, light grey
    - yellow, flatter terrain
    - light blue, mountains
    - lime/green, retaining walls, front and back
  - **Untergrund:**
    - white, the wool lane
    - orange, the underground walls
    - magenta, open rock where the surface turns into the underground
    - pink, the edge between ceiling and wall
    - red, an underground ceiling
    - purple, the ramp under the core
  - **Bauwerke:**
    - stone
    - bedrock
    - clay, plus light-grey wool in the ceiling and in the bunker's checkerboard roof
    - black, a roof
    - glass
    - obsidian and lava, the core
- **`$S/rec/` is a finished reconstruction** of the author's terrain as loft lines. Do not repeat it. It shows how the author builds:
  - A surface is an ordered sequence of lines, each of a few points, with a ruled mesh between each consecutive pair.
  - Separate parts are separate lofts. A layer lying over another is its own "free" loft.
  - Retaining walls (lime front, green back) are tilted plates that hold the terrain at their top edge.
  - The author's story: workers dug out the slope, and retaining walls hold the terrain back.
- **`$S/labels/labels.json` names the building's spaces**: rooms, tunnels, stairwells, the facade and 16 openings,
  each with its air cells, its centre and what it links to.

## Geometry
- **The full map is the built half turned 180°.** The author built one half; it turns about (59.5, 86.5), so (x, z) → (119 − x, 173 − z).
- **`kit.across(x, z)` is the signed distance from the line between the halves**, negative on the built half's side.
- **The 2×2 plain stone at (59–60, 18, 86–87) only marks the pivot, and the lapis blocks only mark the centre line.**
  Their heights mean nothing; they are not a ground level.
- **The middle as uploaded is narrow.** The halves stand 22–26 blocks apart. A ravine there with a floor to fight on
  would need sheer walls, which the author rejects.
- **For the `middle` slot you may move the turned half a few blocks away** with `kit.set_shift(dx, dz)`, called before
  anything else. The built half stays put; the turn becomes (x, z) → (119 + dx − x, 173 + dz − z), and the middle
  widens by about 0.36·dx + 0.93·dz blocks. Keep the widening to about 12 blocks or less, and say in the report what
  you chose and why — or that you kept (0, 0).
- **The middle is exactly the span between the two facing edges, and nothing else.** `kit.span()` gives it as a
  polygon:
  - the built half's front edge where it faces the other half;
  - the turned copy of that edge;
  - two straight lines, each joining the outermost point of one edge to the outermost point of the other. The east
    end of the built half's edge is the corner where the wool lane runs out of the underground, (97, 53).

  `kit.middle_gap()` is every empty column inside that polygon: 1955 at shift (0, 0). Every column of a middle
  variant is one of them, so `outside` in `kit.checks` must be 0. No ground beside the polygon, toward the map's
  left and right edges, and no filled hole in the author's own ground. Along its edges:
  - Existing ground at the gap edge sits mostly at y 15–16, up to about 22.
  - Mountain flanks reach about 36.
  - Edges at y 0 are the wool lane's bedrock.
- **The wool lane stays open on its long side toward the void.** It is white, around x 82–100, z 28–53, and the opening is deliberate. Do not close it.
- **The main building holds the core and the spawn.**
  - Its stone tops span x −15…52, z −22…31, at y 25–60.
  - It has a checkerboard roof of light-grey wool and clay at y 59 (x 12–32, z −22…20) and a black roof at y 66–72 (x 8–30, z 21–47), plus an antenna.
  - Its facade, with the core in it, faces the valley floor.
  - No terrain covers any of it yet.
  - Terrain may cover the checkerboard roof, all of it or in part, but it never runs over the roof's front edge on the
    facade side. The black roof and the antenna stay free.

## The author's rulings
Each of these cost a rebuild before. Obey them.

- **No 100% vertical walls.** `walls` in `kit.checks` must be 0 for ground a player walks on. Sides are slopes, shelves or terraces.
- **A floor everywhere.** Nothing leads into the void: no path or ramp ends at a drop to nothing.
- **The main flow stays walkable and readable; it does not have to be flat.** The flow runs spawn → core → wool. It may
  cross a valley, a ravine with a floor, or a rise, as long as a player can walk it without a jump into nothing. The
  surrounding hills may take freer forms.
- **The author likes flat terrain that flows smoothly from the hills down into the middle**, with no break between
  slope and floor.
- **Smooth and organic.** No noise, no stair-stepped mess, no rectangles as silhouettes, no "floating island" taper under terrain.
- **Meet the existing ground at its height.** `seams` should be mostly 0–1.
- **Never collide with the author's build.** `overlap` must be 0.
- **The map is hollow, and the cover is the surface laid over it.** What exists is only surfaces and the empty mass
  between them. The stairwells, back rooms and slabs behind the facade float in that void, and in the finished map
  they are sunk into solid ground. So the cover is one surface over the whole building, and everything beneath it is
  solid later. A plane drawn low beside the building, leaving a stairwell standing open above it, is wrong.
- **The cover's rules, as `kit.cover_rules(blocks)` measures them:**
  - **No lower than the facade's top exit.** Over every building column behind the facade, the surface lies at y 48
    or above: the walk level of the highest exit in the facade, the opening over the core. No part of the building
    pokes up through it. `below_floor` must be 0. Bare, it is 734.
  - **Flush with the flat roof.** Where the cover meets the checkerboard roof (y 59), it meets it level:
    `roof_seam` 0, or −1 where it tucks under the edge.
  - **Flush with the author's light-blue mountain.** `mountain_seam` 0–1.
  - **Terrain never runs into the roof at roof level.** It covers the checkerboard roof from above, or it stops at
    the roof's edge. The slots between the roof's plates are part of the roof: close one, if at all, as roof (light
    grey), never with terrain reaching in. The gate refuses terrain-coloured blocks inside the roof's outline (x 12–32,
    z −22…20) at y 59 or below.
  - **The black-roofed penthouse stands free.** The cover never wraps it: `penthouse` must be 0. The checkerboard roof
    may be covered, never over its front edge on the facade side.
- **The building's real exits stay open, and the terrain meets them.** `kit.DOORS` names them: the south stair's two
  ways out (one at x −6…7, z 41, floor y 50–54; one at x 8–15, z 43–47, floor y 43–45) and the facade's hall gate,
  core opening and core pit. No cover block stands in a doorway or within 3 blocks in front of it at its height
  (`kit.door_blocks`, enforced by the gate); where the terrain reaches an exit it meets the threshold, so a player
  walks straight out onto it. Other openings behind the facade that lie under the cover are sunk with the rest.
- **Never hide a facade, door, window or entrance behind terrain.** A structure's interior stays air. Think like a player arriving there.
- **Retaining walls are discrete tilted plates** that hold terrain at their top edge. They are never fills.
- **A retaining wall does a big job, or it is not there.** The author's walls hold back a whole mountain or take up a
  real difference in height. Three of them, as measured:
  - x 29–76, y 23–42, z −27…−8: 19 blocks tall, holding the back mountain behind the plaza.
  - x 71–85, y 15–28, z 28–58: 13 blocks tall, taking up the step beside the wool lane.
  - x 20–36, y 22–36, z 56–77: 14 blocks tall, holding the plateau.

  A small wall dropped in to dress a heap or a corner reads wrong and behaves wrong. Do not build one.
- **Use the author's colour semantics:**
  - light grey (8) for flat walkable floor
  - yellow (4) for the flatter terrain that connects: shelves, gentle slopes, the ground that joins one part to another
  - light blue (3) for the hillier ground: mountains, knolls, the steep and rolling parts

  The colour says what the ground does. A piece that is mostly gentle is yellow; a piece that rolls or climbs is light
  blue; a large cover combines both where its ground changes character.
  - lime (5) and green (13) for retaining walls, front and back

  Anything new in meaning takes an unused colour (cyan 9, brown 12, blue 11), named in the piece's note.
- **Both team halves are built from the same blocks.** The map is one design turned 180°, not two materials or two
  themes facing each other. At most the colour of clay or wool may later signal which side belongs to which team.
- **Model at the author's density.** The author's terrain carries about 10–13 loft points per 100 square blocks of
  surface: 10 on the floor, 12–13 on the hills. A surface much coarser than that reads crude, much finer reads busy.
- **How a map plays is the author's call; it cannot be derived from the code.** Read `pgm-studio/docs/gameplay/match-flow.md` §4, §6 and §10, and `approaches.md` beside it, before deciding routes. Keep claims about gameplay modest and turn them into questions for the author.

## Symmetry
- **The `middle` slot is built symmetric, about the pivot of your chosen shift.** Build only the built half's side (`across < 0`), then add the copy with `kit.symmetric(pieces)`. Where a loft meets the cut line, make that boundary line self-symmetric: for every point p on it, `kit.turn(p)` is on it too. The result must be exactly 180° symmetric. Write with `absolute=True`.
- **The `cover` slot is built on the half only**, and the viewer turns it. Keep the shift at (0, 0) and write with
  `absolute=False`.

## The gate
**`kit.write` refuses to write a variant that breaks a hard rule**, and raises an error naming each failure; run
`kit.gate(slot, pieces, absolute)` while you work to see the same list. Only a variant that passes can be delivered.
- **Middle:** `outside`, `overlap`, `walls` and `void` all 0, exactly symmetric, `absolute=True`.
- **Cover:** `overlap`, `walls`, `below_floor` and `penthouse` all 0, no terrain inside the roof at roof level,
  shift (0, 0), `absolute=False`.
- **Both: the lofts themselves stay inside.** The viewer draws the lofts, not only the blocks. A loft whose lines run
  past the allowed area and whose blocks are clipped afterwards still shows outside. Every loft point lies within 2
  blocks of `kit.span()` for the middle, and within 2 blocks of the cover's own blocks for the cover. Build the lines
  so that their ends sit on the boundary; never clip blocks to hide a loft that overshoots.

## Deliver
Work in `$S/variants/<id>/` only. No git, no edits anywhere else.

1. **`build.py`**: the construction, written as lines and lofts, the author's way. It runs with `python3 -I`, uses only the standard library, and finishes in under about two minutes.
2. **`variant.json`**, written with `kit.write(id, slot, <German title, 2–5 words>, <2–3 German sentences: the idea and what a player meets>, pieces, absolute)`.
3. **Two renders made with `kit.render`** from opposite sides. Look at them with the Read tool and fix what looks wrong: one or two passes, not more.
4. **A final reply of under 300 words:**
   - the concept
   - per piece: its name, colour, lofts, lines, points and blocks
   - the full `kit.checks` output: overlap, walls, void, steps, seams
   - the key heights and positions, with coordinates for every claim
   - anything you were unsure about, as a question for the author
