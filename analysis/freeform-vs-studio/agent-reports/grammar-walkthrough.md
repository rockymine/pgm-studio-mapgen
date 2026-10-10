> Written by a Sonnet 5.5 helper agent on 2026-10-10 from instrumented copies of the two boards' scripts, run in a scratch directory; the images it names are reproduced in the Recipe Inspector prototype.

# How pgmvox's style grammar turns a plan into a board, step by step

Two boards, built cumulatively and rendered after every rule with `pgmvox.render.iso` (same corner `se`, same crop,
same scale and the same pixel frame for every stage of one crop, so the PNGs flip through). All paths are relative
to this folder (`.../scratchpad/grammar-steps/`), images in `img/`. Code is pgmvox 0.19.0 at
`/home/user/pgm-studio-mapgen/freeform/lib/pgmvox`, line numbers from that checkout; "gen" is the board's
`scripts/gen.py`. Nothing in the repository was edited.

**How the stages were produced.** `staged.py` is a line-for-line copy of `grammar.lay` (`grammar.py:281`) with one
switch per rule (`body faces accents seam fill motifs`) and a log of every decision; it replaces `pgmvox.grammar.lay`
at run time (`staged.install()`), so the board scripts and `pgmvox.brittle.build` call it unchanged. `cw_build.py`
and `bb_build.py` run text-edited copies of the two `gen.py` files up to a stage. **Check:** the final stage of each
equals the committed board block for block in count (Claywork 364,698; Brittlebush III 107,727). Stage 2 (depth) is
a debug paint, not a code step. Stage 7 for Brittlebush has no motifs, so it is skipped.

Crops, `se` corner:

| Board | Crop A | Crop B | Crop C |
|---|---|---|---|
| Claywork (scale 8) | the Forecourt, Grand Steps and Rostrum: x -34..26, z -40..-8 | West Kiln, Walk flights, Arcade: x -72..-30, z -100..-52 | the Clay Court and its well: x -36..10, z -70..-40 (plus x-ray) |
| Brittlebush III (scale 10-13) | the wool piece, its house and the island before it: x -16..24, z -95..-50 | the spawn keep and piece-2: x 14..44, z -62..-28 | the tunnel island, the middle island and their hollows: x -20..6, z -62..-8 |

Contact sheets (all stages of one crop on one page): `img/cw-sheet-A|B|C.png`, `img/bb-sheet-A|B|C.png`.

---------------------------------------------------------------------------------------------------------------

## The grammar in one paragraph

A board is a list of `Section`s (boxes at one height, `grammar.py:40`). `Ground(sections)` (`:107`) reads every
column's top, owner and **depth** (chessboard distance in from its section's edge, scipy `distance_transform_cdt`,
`:126`; 0 = the outline). `lay(...)` (`:281`) then visits each section and each of its columns once, doing in this
order: **body** under the column, a **face** where the ground beside falls two or more, otherwise the **seam** on a
depth-0 column; after the columns, the section's **fill** over its depth >= 1 columns and its **motifs**. The blocks
are all in a `Style` (`:259`): `body`, `faces`, `seam`, `fills`, `choose`, `motifs`, `params`. Claywork is
`pgmvox/clay.py` (`style()`, `:61`); Brittlebush is `pgmvox/brittle.py` (`STYLE`, `:263`). What a plan is not
asked to say: any block.

---------------------------------------------------------------------------------------------------------------

# A. Claywork (`boards/claywork`, style `pgmvox/clay.py`)

### Stage 0 - the input: the plan raster
`img/cw-00-plan.png` (red's half; blue is the mirror in z). `plan.py` draws a `Raster` of kinds and floors
(`plan()` at `plan.py:144`; pieces list `PIECES` at `:63`, build zones `BAND`/`FLANK`). Each piece is one kind at
one floor or a stepped rule (1 up per 3 rows). **The plan holds no sections.** `gen.py:77` turns the raster into
`TOP[(x,z)] = (floor, kind)` for red's columns.

### Stage 0b - the cut: plan pieces to sections (code, before the grammar)
`gen.py:64 CUT` says how many sections each piece is cut into, `{"front": (7,2), "hub": (7,3), "rostrum": (4,1) ...}`;
`flat_piece` (`gen.py:115`) cuts the piece's box with `grammar._cuts` (`grammar.py:70`: near-equal runs, the longer
ones in pairs from both ends inward) and names the sections `<kind>-<i>-<j>`; both wings alike (the east copy
mirrors `i`). `gen.py:67 FILLS` gives each piece two fills that alternate like a checker, `(i+j) % 2`, so
neighbours never match. `ARROWS` (`gen.py:70`) drop an `arrow` motif into the section under a point and force
that section's fill to `plate`. Flights (`gen.py:127`) are one stepped section named `<kind>-flight` with `tops`
(per-column height) and the tag `rise-n`. Leftover columns (the well's floor, the landing) become `<kind>-rest`
checker sections (`gen.py:150`). Result: 76 sections, drawn in `img/cw-11-decisions-map.png`.
Names carry meaning: `clay._key(lot)` (`clay.py:34`) is `name.split('-')[0]` and picks the checker pair from
`PAIRS` (`clay.py:27`).

### Stage 1 - sections as plain boxes (body only)
`img/cw-A-01-body.png`, `cw-B-01-body.png`, `cw-C-01-body.png`.
Code: `style.body(w, x, z, h)` called per column, `grammar.py:299` -> `clay.body` (`clay.py:85`).
Rule: twelve courses of stone (12% andesite, 3% gravel) from h-11 to h-1, bedrock from y1 to h-12, and on a column
the plan says is `faced` (next to void) a stripe of the team's clay flush with the face and under it a lattice of
obsidian and black wool; block 36 at y0.
Reads: `DEPTH` (12), `faced(x,z)` (a mask from the plan, `gen.py:63`), the board `rng`. Nothing at the surface
yet (the top block y=h is unset), so the boxes sit one below their floor.

### Stage 2 - the Ground read: depth
`img/cw-A-02-depth.png`, `cw-B-02-depth.png`, `cw-C-02-depth.png` (debug paint, wool at y=h).
Code: `Ground.__init__` computes `owner` and `_depth` (`grammar.py:111-127`); `Ground.depth` (`:132`),
`Ground.falls(x,z,by=2)` (`:137`).
Rule: orange = depth 0 and the ground beside falls >= 2 (a face column); red = depth 0 without a fall (outline that
will get the seam); light blue = depth 1 (the lot's first ring); dark blue = deeper. A fill is only handed
depth >= 1 columns (`Ground.inside`, `:143`).

### Stage 3 - faces: courses read down from the rim
`img/cw-A-03-faces.png`, `cw-B-03-faces.png`, `cw-C-03-faces.png`; close view with caption `img/cw-close-03-faces.png`.
Code: `grammar.py:300-312`: `falls[0]` gives the side and drop; `Face.lay` (`:185`) writes the course stack top-down
from y=h with each course oriented toward `inward`. Style: `clay.style` builds `plain` (`clay.py:71`): brick, eight
courses of brick with 8% wear, three of polished andesite = 12 courses; `face` and `flank` (`:81-83`).
Parameters: `Face.courses`, `Face.floor` (1: a face may not reach below y1), `face_of(x,z)` (gen picks `"flank"`
for flights, `"edge"` elsewhere, `gen.py:165`).
Rule: where the neighbour is 2 or more lower the column gets the plain stack; the depth of the stack is the style's
(12), not the drop.

### Stage 4 - accents: a bay laid whole or not at all
`img/cw-A-04-accents.png`, `cw-B-04-accents.png`, `cw-C-04-accents.png`; refused-bay example
`img/cw-close-04-accents.png` (caption names the reason).
Code: `Face.bay` (`grammar.py:211`) names the bay and the position in it; `Face.open` (`:200`) decides; `Face.lay`
(`:185`) lays pilaster / panel / pilaster only if `along % every == phase` and `air >= min_air`.
Claywork: `G.Accent(PANEL+2 = 8, frame=pilaster, inner=panel, every=1, min_air=9, align="section")`
(`clay.py:81`); `align="section"` centres as many whole 8-wide bays as fit on the section's side, so the panels
answer the floor's cut.
Rule: every column of the bay, plus `margin` either side, must be face at the same height with `min_air` blocks of
air before it, else the whole bay is plain. Log of the run (`cw_log.json`): of 99 accent bays logged, 65 laid and
34 refused; example refused: the Rostrum's south face (rim y23) beside the Forecourt at y20: "only 3 below the
rim; a bay needs 9 of air" (`cw-close-04-accents.png`), while the Forecourt's own faces over void take bays
whole (`cw-A-04-accents.png`, seven panels).

### Stage 5 - seams between sections
`img/cw-A-05-seams.png`, `cw-B-05-seams.png`, `cw-C-05-seams.png`.
Code: `grammar.py:313-314`: a depth-0 column with no fall gets `style.seam`.
Claywork: `seam=ANDESITE` (`clay.py:198`). Rule: the outline wherever a section meets anything but a drop (another
section, a wall, a stair head) is polished andesite, so neighbouring sections read as separate panels.

### Stage 6 - fills chosen by `Style.fill`
`img/cw-A-06-fills.png`, `cw-B-06-fills.png`, `cw-C-06-fills.png`; map of decisions `img/cw-11-decisions-map.png`.
Code: `Lot` (`grammar.py:228`) = the section's depth >= 1 columns; `Style.fill` (`:273`) tries the section's own
`fill` first, then `choose(section, lot)` in order; a fill returns False to decline *before it writes*.
Claywork: `choose = ["squares", "paving", "flat"]` (`clay.py:201`); the section's requested fill comes from
`FILLS` (`gen.py:67`) so in practice it is `requested -> squares -> paving -> flat`.
Fills (`clay.py:103-173`): `checker` (3x3 paces of `PAIRS[kind]`), `squares` (diorite rings round clay in stone
grout inside a double-slab band; declines if min(lot size) < 6), `paving` (bands across the short side; never
declines), `inlay` (diorite / stone / clay rings; declines if not a rectangle or min < 5), `plate`, `flat`, `flight`.
Result for 76 sections (from `cw_log.json`): squares 19, inlay 15, plate 14, paving 12, checker 9, flight 7;
**3 declines**, all in the Court (`hub-2-1`, `hub-3-0`, `hub-4-1`: the well's hole makes the lot a non-rectangle,
so `inlay` and `squares` decline and `paving` lays), red outlines in the decisions map.

### Stage 7 - motifs (arrows)
`img/cw-A-07-motifs.png`, `cw-B-07-motifs.png`, `cw-C-07-motifs.png`.
Code: `grammar.py:319-320` calls `style.motifs[name](w, lot, rng, **params)` after the fill; `clay.arrow`
(`clay.py:175`).
Rule: a head and a shaft in the team's wool on the `plate`, one block in from its frame, pointing `d`; the head
rows widen by two from the tip, the shaft is a third of the width. Parameters: the `Section.motifs` tuple
`(("arrow", (("d","n"),)),)`, `dye`. Eight arrows (`gen.py:70`) point out along the flow of the board.

### Stage 8 - the Undercroft (carved after the ground)
`img/cw-A-08-undercroft.png` (nothing visible here), `cw-C-08-undercroft.png` (the well now has its pool),
x-ray `img/cw-Cx-08-undercroft-xray.png`.
Code: `gen.py:410-433` (run by the walkthrough before the buildings; the order does not change the result): for
every column of the plan's `under` kind it sets three of air at y=UNDER+1.., turns gravel in the roof to stone,
lays a brick/cracked-brick floor in 3x3 checks, a pool in the well, lamps, and ladders up the Walks' faces.
This is hand code over the grammar's output, not a grammar rule.

### Stage 9 - buildings and props
`img/cw-A-09-buildings.png`, `cw-B-09-buildings.png` (the Kiln hall, roof and chimney, arches over the Walk),
`cw-C-09-buildings.png` (the well's canopy), `cw-Cx-09-xray.png`.
Code: arches (`gen.py:172`), parapets (`:192`), bedrock walls and their defence chests (`:200`), the Kilns
(`:216-309`: a brick hall on a plinth, pilasters every four, iron-bar windows, frieze of the team's clay, hipped
roof, chimney), the Gatehouse (`:311-352`), statues (`:354-392`), the well's canopy (`:394-408`). All explicit
`w.set` loops over plan constants (`P.KILN`, `P.ARCHES`, ...). Not grammar.

### Stage 10 - mirror and objectives, whole board
`img/cw-10-final-whole-board-se.png`. `gen.py:434-438`: `turn_world(w, "mirror_z", ...)` with red's clay recoloured
blue; `objectives().stamp(w)`.

---------------------------------------------------------------------------------------------------------------

# B. Brittlebush III (`boards/brittlebush-iii`, style `pgmvox/brittle.py`, plan `studioplan.py`)

### Stage 0 - the input: the studio plan
`img/bb-00a-studio-plan.png` (`plan.json`, identical after JSON normalising to the deployed `untitled-plan-8`): 17 pieces (rect in
cells, role, optional `surface` 9/12/15/18; a later piece lies over an earlier one), 7 zones, one spawn and one wool
placement, `cell: 5`, `symmetry: rot_90`. Nothing says stair direction, deck hollows or any block.

### Stage 0b - the plan read as cells and sections
`img/bb-00b-cells-and-sections.png`.
Code: `studioplan.unit` (`studioplan.py:41`): a piece id beginning `stair` becomes a stair cell whose rise is found
from the neighbour three higher across it (`_stair`, `:71`); `double...` becomes `stacked` (a deck; a cell in the
`under` set is open beneath it); the spawn role becomes `keep`; everything else `flat`; a zone with no piece under
it is a `water` cell if its id begins `water`, else a `gap`. Then the board's `plan.py` adjusts: `RAISE` (`:42`)
lifts two decks 3 blocks, `SPLIT` (`:46`) renames cells to cut `piece-2`, `piece-5`, `piece-8` into rectangles,
`UNDER` (`:30`) lists hollow cells, `FILL` (`:54`) forces a fill per section. `brittle.fan` (`brittle.py:72`)
turns the unit by `rot_90` into four teams.
`brittle.sections` (`:286`) then makes one Section per **piece**: cells joined if same `y`, same `section` string,
same keep-ness (`pieces`, `:109`), each cell = a 5x5 box. 18 sections for red's part.

### Stage 1 - sections as plain boxes (body only)
`img/bb-A-01-body.png`, `bb-B-01-body.png`, `bb-C-01-body.png`.
Code: `brittle.ground` (`brittle.py:135`) through `Style.body`. Rule: four courses of stone under the floor (min y3),
bedrock below to y3, an obsidian sheet at y1-2, block 36 at y0. (Hollow columns get no body: they are laid by
hand in stage 8. Hence the gaps under the decks.)

### Stage 2 - Ground read: depth
`img/bb-A-02-depth.png`, `bb-B-02-depth.png`, `bb-C-02-depth.png`. Same debug paint as Claywork. Because
sections are rectangles of cells, the rim band is one block wide all round, the ring of depth 1 inside it is
where the fill starts.

### Stage 3 - faces
`img/bb-A-03-faces.png`, `bb-B-03-faces.png`, `bb-C-03-faces.png`; `img/bb-close-03-faces.png`.
Code: `EDGE = G.Face([_rim, brick, dark-oak slab, upside-down dark-oak stair, black clay], Accent(...))`
(`brittle.py:235`). The deck faces over a hollow are `DECK_EDGE` (`:238`, the same without the black band, `floor=0`),
chosen by `face_of` in `brittle.build` (`:359`). Rule: the five-course cap top-down from the rim, the rim an
upside-down spruce stair with its full side inward.

### Stage 4 - accents: the birch panel bay
`img/bb-A-04-accents.png`, `bb-B-04-accents.png`, `bb-C-04-accents.png`; `img/bb-close-04-accents.png` (a refused
bay and its reason).
Code: same `Face.bay` / `Face.open` / `Face.lay` as Claywork. Brittlebush: `Accent(module=5, frame=[rim]+4 black
clay, inner=[rim, black clay, birch, birch, upside-down birch], every=2, phase=0, min_air=5)` (`brittle.py:236`),
`align="grid"`: bays are counted from the world origin, so a bay *is* a cell, and every other cell along a face
gets the panel, framed in black clay. Log (`bb_log.json`): 38 accent bays, 34 laid, 4 refused. Example refused
(`bb-close-04-accents.png`): piece-10's south face at z -81: "beside column (0,-81) the ground is at y15, only 3
below the rim at y18; a bay needs 5 of air before it". The other three are likewise short drops (2 or 3
over a lower piece).

### Stage 5 - seams
`img/bb-A-05-seams.png`, `bb-B-05-seams.png`, `bb-C-05-seams.png`. `seam=SPRUCE_PLANKS` (`brittle.py:267`): where two
sections at one height meet, a double line of planks, one from each outline.

### Stage 6 - fills
`img/bb-A-06-fills.png`, `bb-B-06-fills.png`, `bb-C-06-fills.png`; `img/bb-11-decisions-map.png`.
Code: `Style.fill`; `choose = ["keep"] if "keep" in tags else ["bed", "sand"]` (`brittle.py:269`).
Fills (`brittle.py:241-262`): `bed(trees=True)` (grass in two rings of sandstone stairs, birch if the grass is >= 4
across; declines if not a rectangle or min(size) < 6), `grass` (the same, no tree), `sand` (sand with 25% upside-down
sandstone stairs, cacti and dead bushes), `keep` (smooth sandstone with a ring of the team's clay at depth 1).
Result for 18 sections: bed 8, sand 7, grass 2, keep 1; **6 declines** (piece-5, 5b, 7, 10, 11, 12: every section
under 6 across) fall back to sand. `FILL` in `plan.py` forces `grass` on piece-3 and piece-2b (the front toward the
build zones, no tree) and `sand` on piece-9 (the monuments' ground).
Style has no motifs (stage 7 skipped).

### Stage 8 - stairs, hollows, zones (by hand, outside the grammar)
`img/bb-A-08-stairs-hollows-zones.png`, `bb-B-08-...png`, `bb-C-08-...png`.
Code (`brittle.build`, `:318-348` before the grammar and `:360-372` after it): `gap` / `water` cells get block 36 at
y0 and either water at y1 or a cobweb mid-edge toward void; a stair cell is three blocks in five, stone-brick slab and
block in turn, half a block a row (`:336-348`); a `stacked` cell with `under=True` is laid by `_under` (`:375`):
a deck four thick, four blocks of air, a lower floor `DECK = 8` down with the short cap and a sand floor;
a black clay band under decks; and `_pillars` (`:414`): a dark-oak pillar two wide at the middle of an open run of
two cells or more. In the walkthrough these are shown after the grammar; in the source the zones/stairs/hollows are
laid first, the black band and pillars last.

### Stage 9 - houses
`img/bb-A-09-houses.png` (the wool house, three storeys), `bb-B-09-houses.png` (the spawn house).
Code: `gen.py:35-57`: `brittle.house(w, layers, floor, dye, door=...)` (`brittle.py:513`) raises storeys of whole
cells, five blocks each, each over part of the one below (`P.WOOL_LAYERS`, `P.SPAWN_LAYERS` list the cells of each
storey). A storey's wall is the ground's edge read bottom-up; birch panel every other cell; plate overhang by one;
a one-cell top storey gets a beacon on gold under glass in the team's colour. Then the wool square, a redstone
line (`gen.py:55`), air over the monument slots.

### Stage 10 - the other three teams, whole board
`img/bb-10-final-whole-board-se.png`. `gen.py:63-74`: `turn_world(w, "cw", mask, recolour)` three times (each team's
clay and wool colours moved on), then `objectives().stamp(w)`.

---------------------------------------------------------------------------------------------------------------

## What a UI would need to show or set (concrete; inference marked)

### A Style, as the grammar reads it
| Slot | What it holds | Parameters a UI would expose |
|---|---|---|
| `body(w, x, z, h)` | what lies under a surface | Claywork: depth 12, flecks (andesite 12%, gravel 3%), bedrock from y1, a team band at `h-12-2` on faced columns, lattice period 8 (obsidian / black wool), block 36 at y0. Brittlebush: 4 stone courses, bedrock to y3, obsidian y1-2, block 36 at y0 |
| `faces[name]` | a `Face(courses, accent, floor)` | `courses`: top-down list of `(block, data)` or a function of the inward side (stairs and slabs need an orientation; `Sunk(back)` = air at the face with a block behind it); `floor`; Accent: `module`, `frame` (the two end columns), `inner` (list, or a function of position in the bay), `every`, `phase`, `min_air`, `margin`, `align` ("grid" or "section") |
| `seam` | one `(block, data)` | the outline block where a section meets anything but a drop |
| `fills[name]` | recipe `fill(w, lot, rng) -> bool` | the pattern: ring/tile sizes (`squares tile=4`), pair per piece kind (`PAIRS`), band width (`paving` 3), bed rings and tree rule; **minimum size and rectangularity** it needs (it declines otherwise) |
| `choose(section, lot)` | the order of fills to try | an ordered list of names, optionally conditioned on tags (`keep`) |
| `motifs[name]` | marks laid after the fill | arrow: direction; (inference) anything with a name and a parameter dict |
| `params` | free values | `dye` (the team's colour) |

### A plan, as the grammar reads it
- **Cells to sections.** Brittlebush: one `Cell(kind, y, rises, name, under, section)` per 5x5 blocks, sections =
  connected cells of one height and one `section` string. Claywork: columns at one `(floor, kind)` cut into
  `CUT[kind] = (nx, nz)` near-equal pieces named `<kind>-<i>-<j>`.
- **Names that carry meaning.** In the studio plan: id prefix `stair` (stair cell, rise inferred from neighbours three
  apart), `double` (stacked deck), `water` (water zone, else bare gap zone); role `spawn` (keep) / `wool-room`;
  a later piece overwrites an earlier one. In Claywork: the kind prefix of a section name picks the `PAIRS` for
  `checker`; the suffix `-flight` plus tag `rise-<dir>` selects `flight`; `plate` is forced by an arrow.
- **What the plan cannot say today** (so the board's own `plan.py`/`gen.py` says it): which cells are hollow
  (`UNDER`), a deck raised above its drawn height (`RAISE`), a rectangle cut into several sections (`SPLIT` /
  `CUT`), a forced fill (`FILL` / `FILLS`), motif positions (`ARROWS`), stair rises in Claywork (the `("steps", edge,
  lo, hi, dir)` rule), team-colour mapping (`DYES`, `KEEP_DYES`), where houses stand and how many storeys.

### What could be a stored, editable document and what is code (inference)
Data-shaped already, in the code as literals: the section list (`Section(boxes, y, name, fill, tags, motifs, tops)`),
the cut tables, fill requests, the `under`/`raise`/`split` tables, `Accent`/`Face` numbers, the seam block, the
chooser order, the body's depth and percentages, `House` layer lists, the plan's piece/zone rects. A JSON for a
Style would be roughly:
```
{ "name": "claywork", "seam": "stone:6",
  "body": {"depth": 12, "flecks": {"stone:5": 0.12, "gravel": 0.03}, "bedrock_from": 1, "band": "team_clay", "lattice": {"period": 8, "blocks": ["obsidian", "wool:15"]}},
  "faces": {"edge": {"courses": ["stonebrick", "stonebrick:worn(0.08) x8", "stone:6 x3"],
                      "accent": {"module": 8, "align": "section", "every": 1, "phase": 0, "min_air": 9, "margin": 0,
                                 "frame": ["...pilaster courses..."], "inner": "panel(6 wide, sunk 1, diamond)"}}},
  "fills": ["squares", "paving", "flat"], "motifs": ["arrow"] }
```
Parts that resist being data without a small expression language: courses whose block depends on the inward side
(stairs, upside-down stairs), a function `inner(pos)` for the panel (a bitmap would serve), wear drawn from `rng`,
and every fill body (`squares`, `inlay`, `bed`, `sand`, `flight`): ring/tile/grout rules with minimum-size and
rectangle tests. Those are code today and would be a library of named, parameterised recipes; the UI would pick
one and edit its numbers, not write it.
Code, not data: `Ground`/`lay` themselves, `_under`/`_pillars`/stair cells (the hollow logic), `house`/`tower`,
`flight`, `arrow`, the Kilns/Gatehouse/statues, the Undercroft carve, the turn/mirror and recolour.

### What a user would want to see while driving it (inference from the logs above)
- the Ground read: the depth map (stage 2), faces vs seams, because everything else keys on it;
- per section: the fills tried and which declined and why (`min(size) < 6`, not a rectangle): `staged.LOG["sections"]`;
- per face bay: laid or refused with the column and the number that failed (`staged.LOG["bays"]`): refusals are
  the surprising part (34 of 99 in Claywork) and today are silent;
- the map of decisions (`img/cw-11-decisions-map.png`, `img/bb-11-decisions-map.png`);
- the plan-to-section cut (stage 0b), because that is where board-specific tables live.

---------------------------------------------------------------------------------------------------------------

## Files in this folder
`staged.py` (instrumented `lay`), `cw_build.py`, `bb_build.py` (cumulative builders), `make_cw.py`, `make_cw2.py`,
`make_bb.py`, `make_bb2.py` (images), `draw.py`, `common.py`, `sheets.py`, `logs.py`; logs `cw_log.json`, `bb_log.json`.
Rebuild: `PYTHONDONTWRITEBYTECODE=1 python3 make_cw.py && python3 make_cw2.py && python3 make_bb.py && python3 make_bb2.py && python3 sheets.py`.
