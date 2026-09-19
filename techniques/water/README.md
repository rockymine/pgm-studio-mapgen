# Water

Water cannot drape on a slope the way gravel can — laid on the surface it reads as blue paint — so a body of
water is not a finish over the ground but a **shape taken out of it**: a carved bed under a level fill. Ten
panels on one board: five bodies of water in row 1 and five ways of getting one wrong in row 2. Open it in
the studio as `technique-water`, or run `build.py`.

**Two sentences decide almost everything here.** The line a body stands at is the **lowest surface its band
crosses**, and every column over that line inside the band is emptied down to it; and the ground it reads is
**the layer the prop names**, which is why a bridge over a beck stands or does not.

## The document

Ten groups on the `ground` layer, a `deck` layer at `base_y` 25 carrying the two bridges, and the water in
`dressing.props`. Three themes: `moor` for the uplands, `strand` — sand over sandstone — for the shore, and
`plank` for the bridges.

| panel | states | what it built |
|---|---|---|
| `beach` | a `pool` at `level` 16 whose ring is drawn **past the island's edge** | a sea filling to the board's rim, meeting the void |
| `pond` | a `pool`, `form: natural`, **no `level`** | water y19–21 — a line of 21 that no document states |
| `no-shore` | the same pond with `shore` 0 | the same water, and grass at its edge instead of a bank |
| `two-forms` | a `canal` and a `stream` channel, same `radius` and `depth` | one holds its width, one beads along its arc |
| `basin` | a `sink` shape dug 8 deep, filled at `level` 20 | a dock with quay walls — `DROP -8` at the edge |
| `pan-too-big` | an `area` mark at the size of the *hollow* | a small pool in a wide levelled floor |
| `pan-fits` | the same mark at the size of the water | the same pool with the ground rising straight from it |
| `down-a-hill` | one channel down a fall from 30 to 16 | `DR-BANK` — **14 courses** cut away, a trench |
| `no-layer` | a beck under a deck, naming **no layer** | `DR-BANK` — the bridge is bitten through |
| `named-layer` | the same beck with `"layer": "ground"` | planks at y25, water at y19 under them |

```json
{"id": "sea", "kind": "water", "shape": "pool", "form": "natural", "layer": "ground",
 "points": [[-274, -41], [-166, -41], [-166, 3], [-274, 3]],
 "radius": 10, "depth": 6, "level": 16, "shore": 3, "shoreWander": true, "edge": 2,
 "bank": {"kind": "voronoi", "…": "gravel, coarse dirt and sand"}}
```

## A sea is a pool drawn past the edge of the land

**The `beach` panel's ring runs wider than its island on three sides, so the water fills to the board's rim
and meets the void there.** At (−220, −8), the last column before the edge, the read is still water at 16.
A pool drawn inside the land instead stops in a basin with a lip round it, which reads as a tank rather than
as a sea.

**The ground has to shelve under it.** A fell at 30 falls to a sea floor at 11, the water line is stated at
16, and the strand between them carries a **sand theme of its own** — `shore` lays the bank band only where
the water meets the land, so a beach that should read as sand for twenty cells is a surface, not a prop
setting.

**`level` is what makes it a sea rather than a puddle**, because the line is then that Y whatever the column
beneath is doing. What the author owns in exchange is the rim: water rises to the line inside the prop's own
footprint and nowhere else, so the ring has to reach the land's edge or the sea stops short of it.

## What a body of water is drawn as

**`shape` says what the points mean, and it is the first decision.** A `channel` strokes them as a
centreline and takes its width from `radius`; a `pool` closes them into a ring and fills it, and there
`radius` is the **shelf** — how far in from the shore the bed reaches full depth. A harbour and a canal are
one type with two readings of one list.

**`form` is how the band is cut, and the `two-forms` panel is both at once.** The same `radius` 4 and `depth`
3 drawn twice: `canal` holds a clean uniform width the whole way, and `stream` pinches and swells on a fixed
beat down its arc — never wider than nominal, pinching to half — and runs shallower throughout.

**`shore` is how wide a beach the water meets the land through, and 0 means none.** `pond` and `no-shore` are
the same pool with `shore` 3 and `shore` 0: at (−110, −29) the first holds water and at (0, −29) the second
is grass. The bank material is laid on the bed *and* the beach, so one voronoi finishes both.

**With no `level` the line is found, and the `pond` reads y19–21 on flat ground at 21** — a line nothing in
the document states, which is a pond cut into ground that was already there. A `basin` dug out in the sketch
has no surface up at the line for a derived one to find, so it can only be stated.

## A water prop carves against the layer it names

**`no-layer` and `named-layer` are the same beck under the same deck, differing in one field.** Naming no
layer takes the top surface of the stack, which at the bridge is the deck at y25, so the carve empties those
columns down to the line: `DR-BANK`, *cut 6 course(s) … a straight-sided wall from y20 to y25*, and the
bridge is bitten through.

**`"layer": "ground"` is the whole fix.** The same beck reads the ground layer's own surface, carves its bed
in that, and the column at (220, 45) comes back **planks at y25 with water at y19 under them**. Nothing is
declined. A board can have the water and the bridge; the prop has to say which storey it belongs to.

**Every prop kind takes `layer` and `DressingContext.GroundFor` reads it**, so this is not a water rule —
it is the prop rule met where it matters most, because water is the one prop that changes the ground.

## `DR-BANK`: the line is the lowest surface, and everything over it is emptied

**A channel run down a fall takes the foot of the fall as its line and cuts the whole run down to it.**
`down-a-hill` draws one beck from a head at 30 to a foot at 16, and the decline is exact: *is 3 deep and its
carve cut **14 course(s)** of ground away above its own line — a straight-sided wall from y16 to y29*. What
was drawn as a beck is built as a trench.

**So a beck wants level ground, or reaches, or a stated line.** Keep a run within a course or two of level,
break it into reaches that each cross flat ground, or state a `level` and accept the rim — and read
`DR-BANK`'s course count, which is the depth of the trench you did not mean to dig.

## The pan is the size of the pool

**An `area` mark levels ground, and everything it levelled stands at the water line whether it is wet or
not.** `pan-too-big` marks a 68 × 44 floor at 14 and puts a radius-10 pool in the middle of it: a small body
of water in a wide flat expanse at its own height, which reads as a drained lake.

**`pan-fits` is the same water with the mark drawn at the water's own size**, and the ground rises straight
out of it. Neither panel raises anything — a pan drawn too big is not a fault the studio has an opinion
about, and the only way to see it is to look.

**The same fact from the other end is that a water prop fills its own band and no more.** The band **is** the
pond and `radius` is the knob; a canal down the middle of a wide flat hole is a channel with dry ground
either side of it however level the pan under it.

## What the paint makes of it

**A water prop's bank is counted against the theme of the ground it carved, not a theme of its own.**
`census.txt` reports three themes and **eight** distinct surface blocks, with gravel, sand and water turning
up under `moor`, `strand` and `plank` alike, because the bank is a material the prop lays rather than a theme
the document scopes.

**The bands are cut at 35° and 55° here, not at the 15° and 40° the flat-ground cards use.** `incline.txt`
holds 81.6% of this board under 10° and only 4.1% at 40° or steeper, and the shelving fell falls at about
25° — banding under that stripes the whole shore green and brown, row by row.

**The board is nearly all walkable**, 70,936 cells against 836 barrier, and its three faces are the dock's
quay walls — `slopes.txt` puts the largest, 364 cells, at x 189…250, z −62…−29. Water itself is walked: a
bed cut and filled leaves no step at its shore.

## The recipe

**Draw the hollow and the water as one statement, name the layer, and let the ring reach the land's edge
where it is meant to be a sea.**

```json
"dressing": {"props": [
  {"id": "sea", "kind": "water", "layer": "ground", "shape": "pool", "form": "natural",
   "points": "<a ring drawn past the island's own edge>", "radius": 10, "depth": 6, "level": 16,
   "shore": 3, "shoreWander": true, "edge": 2, "seed": 7,
   "bank": "<a voronoi of gravel, coarse dirt and sand>"}]}
```

- **name the `layer`** — a prop with none carves against the top of the stack, and a deck over it is ground.
- **no `level` on ground that is already there**, a stated `level` on ground the sketch dug out.
- **run the ring past the land's edge** for a sea, so the water meets the void instead of a lip.
- **give the shore its own theme** — `shore` lays a bank band a few cells wide, not a beach.
- **`radius` is half the width on a channel and the shelf on a pool** — one number, two meanings.
- **keep a channel's run level**, or `DR-BANK` will trench it by the fall's whole height.
- **a mark drawn bigger than its water is a drained lake**, and nothing reports it.

## What checks it

- `columns.txt` — eleven columns: the sea at the rim, the strand, the tarn with and without a shore, the
  basin at its stated line, the pool in the oversized pan, the beck in its own trench, and the bridge
  bitten through against the bridge standing.
- `transects.txt` — a line through every panel, with the water column beside the ground.
- `dressing.json` — what the pass placed and what it declined: every prop's cell count and line, and the two
  `DR-BANK` complaints with their course counts.
- `slopes.txt` — 70,936 cells walked, 1,188 scrambled, 836 barrier; three faces, the largest 364 cells.
- `census.txt` — three themes and eight surface blocks, which is the bank material showing up under each.
- `water.layout.json` — the one document the board was stored from, posted to `POST /api/map/from-documents`
  with an empty intent and no plan.

Renders: `bodies-row.png` (the sea, the pond, the same pond with no shore, the two forms, the basin),
`traps-row.png` (the two pans, the trench, and the bridge bitten through against the bridge left standing)
and `iso.png`.
