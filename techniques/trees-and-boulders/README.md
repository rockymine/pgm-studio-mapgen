# Trees and boulders

**A prop is not drawn, it is asked for.** The dressing pass seats every one against a book of claims and
answers on a **200**: a prop the book refuses is simply not in the world, and the only thing that says so is
the decline beside it. Twelve pads ask for 106 props and get 90. Open it in the studio as
`technique-trees-and-boulders`, or run `build.py`.

**So the numbers in that book are the whole of what an author needs, and every one here is a ladder rather
than a formula.** Each panel states the same prop at a stepping distance from the thing that might refuse
it, and `declines.txt` says which rung the rule cuts at. Nothing on this card is remembered.

**The one fact the ladders turn on: a prop is tested at its own lowest course and claims everything it
covers.** `Seats` walks only the cells a prop rests on, so a tree is judged by its trunk and a boulder by
its footprint — and once placed, each claims its whole canopy or its whole body. Every distance below
follows from that asymmetry.

## The document

Twelve pads on one `ground` layer, one theme, no relief — a plain solved to y7, because a grade would put a
second rule in every measurement. Two pads also carry an authored wall, and one carries a monument.

| panel | asks for | what the book said |
|---|---|---|
| `tree-standoff` | a road, four oaks stepping off it | declined at **2**, placed at 3 (`DR-ROAD`) |
| `boulder-standoff` | the same road, four rocks | declined at **1**, placed at 2 |
| `a-wide-brush` | a radius-8 `rough` brush, four oaks all 11 off it | one of four declined: the band **wanders** |
| `set-back` | a narrow road and nine oaks behind it | nine placed: the road drawn so nothing is lost |
| `two-boulders` | one pair 3 apart, one pair 9 apart | the near pair loses one (`DR-CLAIM`) |
| `kind-decides` | a rock and an oak two apart, twice, order opposite | **both oaks** declined either way |
| `two-trees` | nines at 1–4 and fourteens at 2–5 | nines need **4**, fourteens need **5** |
| `a-wood` | forty-five darts against that rule | forty-five placed |
| `a-kept-clear-wall` | a wall stating `keepClear`, two props on it | both declined (`DR-KEEP`) |
| `an-unmarked-wall` | the same wall without the field | both placed, **standing on its head** |
| `a-goal-clearance` | a monument, oaks at 9, 10, 11, 12 | 9 and 10 declined (`OB19`) |
| `flora-overlay` | a road, a rock, and an overlay over both | 1,591 cells written, nothing declined |

```json
"dressing": {
  "styles": {"oak-9":  {"kind": "tree", "form": "template", "species": "oak", "height": 9},
             "rock-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": true, "rock": "…"}},
  "props":  [{"id": "off-2", "kind": "tree", "seed": 3400, "x": -124, "z": -66, "style": "oak-9"}]}
```

## What paving keeps off

**A tree keeps three blocks from the nearest paved cell and a boulder keeps two.** `off-1` is declined —
*"rests on (−138, −67), nearer than 3 blocks to the road at (−140, −69)"* — and `off-2` one cell further out
is placed. On the rock ladder `rock-off-1` is declined at 1 and `rock-off-2` stands at 2.

**But the boulder's distance is measured from its body, not from the cell it was asked for.** `rock-off-1`
was stated at (−60, −67) and the decline names (−62, −68): a size-3 erratic rests on a footprint seven cells
across, so its *centre* has to stand two plus its own reach away. A tree's trunk is one cell and its centre
is its distance.

**A texture brush is a road, and `DR-ROAD` prices it at the brush's own width plus the standoff.** The
radius-8 `rough` brush claims **1,010** cells and the radius-2 road beside it claims **252** over the same
length of board — four times the paving, and therefore four times the ground nothing can stand on.

**And a `rough` band has no constant edge, so the strip it kills is a range and not a number.** Measured off
the claims map: the brush's band is **11 to 18 cells wide** and reaches **5 to 10** either side of its
centreline, because `rough` spends its knob wandering the half-width over a 7-block scale. The road's
`solid` band is 4 wide at every one of its columns.

**Which is why the ladder for this panel steps along the brush rather than away from it.** Four oaks, all
stated eleven off the centreline, at four places down its length: three stand and the second is refused —
*"rests on (31, −59), nearer than 3 blocks to the road at (33, −61)"*. The same distance is inside the
keep-out at one x and clear of it at the next.

**So brush the ground that is meant to be open and draw the road narrow.** `set-back` is a radius-2 road
with nine oaks thrown south of it, every one placed. A paved forest floor is an empty forest.

## What a prop keeps off another

**`DR-CLAIM` is footprint overlap and nothing else.** Two size-3 rocks three apart contest —
*"rests on (−131, −7), claimed by the prop 'pair-near-a'"* — and the same two nine apart both stand. There
is no standoff between props, only the question of whether one rests where another already is.

**Between two trees that reads as one crown, not two.** A tree is tested at its trunk and claims its canopy,
so the second oak is declined exactly when its trunk falls inside the first one's crown. Measured with one
seed pair down each ladder: a pair of nines is refused at 1, 2 and 3 and stands at **4**; a pair of
fourteens is refused at 2, 3 and 4 and stands at **5**.

**Which means what two trees need is the larger of their two crowns and not the sum of them.** Four blocks
for a nine and five for a fourteen, measured from trunk to trunk — `a-wood` throws forty-five darts against
that rule and the pass takes all forty-five. Thrown points beat a lattice here, which at the same spacing
either reads as a grid or breaks its own minimum.

**And the order between kinds is not the author's to choose.** `kind-decides` states the same rock-and-oak
overlap twice with the document order opposite, and **both oaks are declined**: the pass runs water, then
strokes, then houses, then boulders, then trees, then flora, and the document's order is the order only
*within* a kind. A wood grows round a rock because it cannot do anything else.

## What the ground and the goals keep off

**An authored shape needs two different fields for two different passes, and neither substitutes for the
other.** These walls are override adds on the ground layer: `height_mode: "level"` with `skirt: 0` is what
the relief needs — without it `SK14` fires and the wall comes out level with the meadow — and `keepClear` is
what the dressing pass needs.

**With `keepClear` the wall declines what leans on it, by name.** *"rests on (−128, 69), which is kept clear
for a stated structure"*, for the rock and the oak both, and the column at the wall's middle reads its top
course at y13 with nothing above it.

**Without it the wall is ground like any other and the props stand on its head.** `an-unmarked-wall` places
both: the oak's trunk starts at **y14**, on the wall's own top course, six courses over the meadow, and the
boulder is bedded into the wall head beside it. Nothing refused either, and no read but a column says so.

**A goal's clearance is a 21 × 21 square on the monument's own cell, and it declines a prop from the prop's
end.** `OB19` refuses the oaks at Chebyshev 9 and 10 — *"inside a goal's clearance"* — and passes those at
11 and 12; the claims map counts 441 cells of it. Where `objectives-and-clearances` reads that rule from the
goal's side, this is the same rule seen by the thing it turns away.

**The overlay is the one thing that is never declined.** `flora-overlay` writes 1,591 cells of grass, fern
and flower round a road and a rock without being asked to stand anywhere, because it is paint on whatever
cells the pass left free. A wood's floor belongs to it and to the theme, not to props.

## Also refused, met while building this

**`DR-STEEP` declines a prop standing where the theme calls the ground a face.** A first cut of the wall
panels made the wall five cells deep, so every cell of its head was an edge and the boulder on it came back
*"stands at (−49, 70) on ground inclined 56°, and the theme painting that cell calls the ground a face"*.
The wall is eleven deep here, and its head has flat ground on it.

**`DR-SITE` and `DR-CLAIM` both catch a dart thrown badly.** A wood thrown past the pad's own coast raised
*"has no ground at (131, −41)"*, and one thrown across the road raised *"claimed by the paving"*. The box a
thrower throws into is the author's arithmetic; the pass only reports what it hit.

## The recipe

**Ask for the props, read the declines, and fix the arithmetic — never the other way round.**

- **three blocks off paving for a tree, two for a boulder**, measured from the prop's resting cells: a rock
  of reach `r` wants its centre `2 + r` out.
- **a brush is an exclusion as wide as itself plus the standoff, and a `rough` one has no fixed edge.**
  Radius 8 measured 11–18 wide; budget from the wide end, brush what is meant to be open, and keep the
  wood's floor to the theme.
- **between two trees, the larger crown**: four for a nine, five for a fourteen, trunk to trunk.
- **between anything else, footprint overlap** — there is no standoff, only occupancy.
- **a rock always beats a tree**, whatever the document order says.
- **an authored shape says `height_mode`/`skirt` to the relief and `keepClear` to the dressing.** Both, or
  a prop stands on it and nothing reports the tree growing out of the battlement.
- **keep props eleven blocks off a goal's anchor**, which is the 21 × 21 clearance with one to spare.
- **fill with a flora overlay, not with more props** — it takes what is left and is never refused.

## What checks it

- `declines.txt` — the spine: every prop of every ladder, its stated step, and the rule and coordinate for
  each of the sixteen the book refused. 90 placed, 16 declined, 7,490 cells claimed.
- `dressing.txt` — the same read as text: the claims map a block a character, twelve classes, and the
  declines under it. This is where a keep-out is *seen* rather than inferred.
- `columns.txt` — ten columns: the oak standing on the unmarked wall's head, the boulder bedded into it, the
  marked wall with nothing on it, a placed oak and the road its standoff was measured to, the cell a
  declined oak was asked for, a bedded rock, the wood's floor, a flora cell, and the monument.
- `census.txt` — two themes over 43,008 cells; the walls are 720 of them.
- `incline.txt` — 98% of the ground under 10°, and the 1.9% at 40° or steeper is the two walls' faces. The
  pads are flat on purpose: a grade would put `DR-STEEP` into every other measurement.
- `trees-and-boulders.layout.json` · `.intent.json` — the two documents the board was stored from.

Renders: `row1-standoffs.png`, `row2-claims.png`, `row3-keep-outs.png`; `section-walls.png` — the two walls
cut through at z70, which is the only view a prop standing on a wall head reads in; `iso.png` for all twelve.
