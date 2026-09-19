# Water

Water cannot drape on a slope the way gravel can — laid on the surface it reads as blue paint — so a body of
water is not a finish over the ground but a **shape taken out of it**: a carved bed under a level fill. Ten
panels, all on one board: five bodies of water in row 1 and five ways of getting one wrong in row 2. Open it
in the studio as `technique-water`, or run `build.py`.

**One sentence decides almost everything on this card.** The line a body stands at is the **lowest surface
its band crosses**, and every column over that line inside the band is emptied down to it — so where a body
is drawn matters more than any of its knobs.

## The document

Ten groups on the `ground` layer and one `deck` layer at `base_y` 25 carrying the two bridges, with the water
in `dressing.props`. A water prop is `kind: "water"` and its fields are the card: `shape`, `form`, `points`,
`radius`, `depth`, `level`, `shore`, `edge` and `bank`.

| panel | states | what it built |
|---|---|---|
| `beach` | a `pool` at `level` 16 with `shore` 5 against a strand at 17 | 1,513 cells of water at y16 and a five-wide strand round it |
| `pond` | a `pool`, `form: natural`, **no `level`** | water y19–21 — a line of 21, which no document states |
| `no-shore` | the same pond with `shore` 0 | the same water, and grass at its edge instead of a bank |
| `two-forms` | a `canal` and a `stream` channel, same `radius` and `depth` | one holds its width, one beads along its arc |
| `basin` | a `sink` shape dug 8 deep, filled at `level` 20 | a dock with quay walls — `DROP -8` at the edge |
| `pan-too-big` | an `area` mark at the size of the *hollow* | a small pool in a wide levelled floor |
| `pan-fits` | the same mark at the size of the water | the same pool with the ground rising straight from it |
| `down-a-hill` | one channel down a fall from 30 to 16 | `DR-BANK` — **14 courses** cut away, a trench |
| `one-channel` | a beck under a deck, drawn the whole way | `DR-BANK` — the bridge is bitten through |
| `two-channels` | the same beck stopped either side of the deck | the bridge stands, and the reach under it is dry |

```json
{"id": "bay", "kind": "water", "shape": "pool", "form": "natural",
 "points": [[-255, -33], [-185, -33], [-185, -11], [-255, -11]],
 "radius": 8, "depth": 4, "level": 16, "shore": 5, "shoreWander": true, "edge": 2,
 "bank": {"kind": "voronoi", "…": "gravel, coarse dirt and sand"}}
```

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
is grass. The bank material is laid on the bed *and* the beach, so one voronoi of gravel, coarse dirt and
sand finishes both.

## A stated line and a found one are different instruments

**With no `level`, the line is the lowest surface the body crosses and the fill never rises past a column's
own surface.** The `pond` reads y19–21 on flat ground at 21 — a line nothing in the document states — which
is a pond cut into ground that was already there.

**With a `level`, the line is that Y whatever the column beneath is doing, and it is the only way to fill dug
ground.** The `basin` panel takes its pool's shape out of the sketch with a `height_mode: "sink"` shape eight
deep and then states `level` 20: the dug floor has no surface up at the line for a derived one to find, so a
dock, a harbour or the water a ship floats on can only be stated.

**What the author owns then is the rim.** Water rises to the line inside the prop's own footprint and nowhere
else, so a line above the surrounding ground stands as a wall of water rather than spilling — which is what
makes the basin's quay a `DROP -8` at its edge rather than a flood.

## The pan is the size of the pool

**An `area` mark levels ground, and everything it levelled stands at the water line whether it is wet or
not.** `pan-too-big` marks a 68 × 44 floor at 14 and puts a radius-10 pool in the middle of it: the result is
a small body of water in a wide flat expanse at its own height, which reads as a drained lake.

**`pan-fits` is the same water with the mark drawn at the water's own size**, and the ground rises straight
out of it. Neither panel raises anything — a pan drawn too big is not a fault the studio has an opinion
about, and the only way to see it is to look.

**The same fact from the other end is that a water prop fills its own band and no more.** The band **is** the
pond and `radius` is the knob; a canal down the middle of a wide flat hole is a channel with dry ground
either side of it however level the pan under it.

## `DR-BANK`: the line is the lowest surface, and everything over it is emptied

**A channel run down a fall takes the foot of the fall as its line and cuts the whole run down to it.**
`down-a-hill` draws one beck from a head at 30 to a foot at 16, and the decline is exact: *is 3 deep and its
carve cut **14 course(s)** of ground away above its own line — a straight-sided wall from y16 to y29*. What
was drawn as a beck is built as a trench.

**The same rule eats a bridge.** `one-channel` runs a beck across level ground at 20 with a plank deck at
y25, and the channel's band crosses the deck's columns: *cut 6 course(s) … a straight-sided wall from y20 to
y25*. The deck is bitten through where the beck passes under it.

**`two-channels` is the remedy and it costs the water.** Two reaches stopped clear of the deck's band raise
nothing at all and the bridge is whole — and the reach under it is dry. A board can have the water under the
bridge or the bridge, not both; where it can afford to, the dry reach still lays its bank materials and reads
as a sink.

**So a beck wants level ground, or reaches.** Keep a run within a course or two of level, or state a `level`
and accept the rim, or break it into reaches that each cross flat ground — and read `DR-BANK`'s course count,
which is the depth of the trench you did not mean to dig.

## What the paint makes of it

**A water prop's bank is counted against the theme of the ground it carved, not a theme of its own.**
`census.txt` reports two themes and **eight** distinct surface blocks: grass, water, coarse dirt, gravel,
cobble, stone and sand all under `moor`, because the bank is a material the prop lays rather than a theme the
document scopes.

**The board is nearly all walkable**, 70,936 cells against 836 barrier, and its three faces are the dock's
quay walls — `slopes.txt` puts the largest, 364 cells, at x 189…250, z −62…−29. Water itself is walked: a
bed cut and filled leaves no step at its shore.

## The recipe

**Draw the hollow and the water as one statement, on ground that is level where the water is.**

```json
"dressing": {"props": [
  {"id": "tarn", "kind": "water", "shape": "pool", "form": "natural",
   "points": "<a lobed ring>", "radius": 6, "depth": 3,
   "shore": 3, "shoreWander": true, "edge": 2, "seed": 7,
   "bank": "<a voronoi of gravel, coarse dirt and sand>"}]}
```

- **no `level` on ground that is already there**, a stated `level` on ground the sketch dug out.
- **`radius` is half the width on a channel and the shelf on a pool** — the same number, two meanings.
- **keep a channel's run level**, or `DR-BANK` will trench it by the fall's whole height.
- **a mark drawn bigger than its water is a drained lake**, and nothing reports it.
- **`shore` 0 is a hard edge**; 3 to 5 is a beach, and `shoreWander` is what stops it reading as a ruled band.
- **a deck over a channel is bitten through** unless the channel stops clear of it.

## What checks it

- `columns.txt` — nine columns: the bay, its strand and the grass past it, the tarn with and without a
  shore, the basin at its stated line, the pool in the oversized pan, and the beck in its own trench.
- `transects.txt` — a line through every panel, with the water column beside the ground.
- `dressing.json` — what the pass placed and what it declined: every prop's cell count and line, and the two
  `DR-BANK` complaints with their course counts.
- `slopes.txt` — 70,936 cells walked, 1,188 scrambled, 836 barrier; three faces, the largest 364 cells.
- `census.txt` — two themes and eight surface blocks, which is the bank material showing up under the
  ground's own theme.
- `water.layout.json` — the one document the board was stored from, posted to `POST /api/map/from-documents`
  with an empty intent and no plan.

Renders: `bodies-row.png` (beach, pond, no shore, the two forms, the basin), `traps-row.png` (the two pans,
the trench, and the bridge bitten through against the bridge left standing) and `iso.png`.
