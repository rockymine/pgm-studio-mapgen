# Trees and boulders

**A prop is not drawn, it is asked for.** The dressing pass seats every one against a book of claims and
answers on a **200**, so a prop the book refused is simply not in the world and the only thing that says so
is the entry beside it. Sixteen pads ask for 124 props and get 106. Open it in the studio as
`technique-trees-and-boulders`, or run `build.py`.

**So the numbers in that book are the whole of what an author needs, and every one here is a ladder rather
than a formula.** Each panel states the same prop at a stepping distance from the thing that might refuse
it, and `declines.txt` says which rung the rule cuts at. Nothing on this card is remembered.

**And the read gives two answers, not one.** A **decline** means the prop is not in the world; a
**complaint** means it is, minus whatever was cut off it. Eighteen of this board's twenty-two entries are
declines and four are complaints, and telling them apart is the difference between a missing tree and a
half-written one.

**The one fact the ladders turn on: a prop is tested at its own lowest course and claims everything it
covers.** `Seats` walks only the cells a prop rests on, so a tree is judged by its trunk and a boulder by
its footprint — and once placed, each claims its whole canopy or its whole body. Every distance below
follows from that asymmetry.

## The document

Sixteen pads on one `ground` layer, one theme, and fifteen of them with no relief — a plain solved to y7,
because a grade would put a second rule in every measurement. Two pads carry an authored wall, one carries
a monument, and the last one is graded on purpose. Five recipes: two template oaks, a boulder, and two
bodies cut out of the `tree-showcase` world, which ride in `trees.json` beside this file.

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
| `a-copied-tree` | `tree-showcase-r2-1` and `-r3-1`, and a template | 144 and 147 cells against **67** |
| `a-body-s-foot` | both bodies three off one road | the nine-cell foot declined, the one-cell placed |
| `a-copied-crown` | pairs of `showcase-tall` at 2, 3, 8, 16 | **2 placed, 3 declined** — a hole in the crown |
| `props-on-a-grade` | a 63° face with an oak and a rock on it | both placed, the rock complained about |

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

## A tree somebody built

**A copied recipe has no species and no nominal anything.** `showcase-tall` and `showcase-giant` are
`tree-showcase-r2-1` and `-r3-1`, cut out of that world with `seed-trees.cs` and carried here as 299 and
412 blocks of `[x, y, z, id, data]`. What they look like is what was built; the studio's part is to seat
them, turn them round the symmetry and keep their leaves.

**They cover twice the ground a template does.** The read gives `showcase-tall` 144 plan cells and
`showcase-giant` 147, against **67** for the `oak-14` standing beside them — and a template's whole
statement was a species and a number.

**A body's foot is every cell of its lowest course, and that is what the standoff is measured from.**
`showcase-tall` rests on one cell; `showcase-giant` rests on **nine**, spanning x 0..3 and z −1..3. Anchored
at the same three blocks off the same road, the slender one stands and the giant is declined — *"rests on
(−26, 108), nearer than 3 blocks to the road at (−28, 106)"*, naming a foot cell rather than the anchor.

**And a hand-built crown is not a disc, not symmetric, and not even solid.** `showcase-tall`'s plan
footprint across its own trunk row reads `#######..####`: the cells at (1, 0) and (2, 0) are **holes**. So
which answer a neighbour gets depends on which cell its foot lands in, not on how far away it is.

**Two apart the second tree finds the hole and is placed; three apart it lands on a written cell and is
declined.** The pair at 2 is a `DR-CUT` complaint — *"70 of its 299 blocks are inside something already
standing and were not written, and that cut 51 more off its own footing"*, 229 in the world. The pair at 3
is `DR-CLAIM` and is gone. At 8 the complaint is 17 blocks; at 16 there is none.

**Which is the general shape of it: `DR-CLAIM` refuses and `DR-CUT` reports.** A prop seats on its feet and
is then written wherever it meets air, so standing clear of something is not the same as fitting beside it —
and for a body of four hundred blocks the difference is worth reading.

## Also refused, met while building this

**`DR-STEEP` is a rock's rule and nobody else's, and it complains rather than refusing.** `PlaceBoulder`
asks it and `PlaceTree` does not, so `props-on-a-grade`'s 63° face takes an oak without a word and keeps the
boulder beside it with a note: *"stands at (131, 105) on ground inclined 63°, and the theme painting that
cell calls the ground a face"*. The rock is in the world; the pass has told you it looks wrong.

**The angle it compares against is the theme's own cliff band, not a constant.** This board's `meadow` puts
grass under 35° and coarse dirt to 55°, so 51° of face raised nothing at all and 63° raised the complaint.
A first cut of the wall panels made the wall five cells deep, every cell of its head an edge, and the
boulder on it came back at 56°; the wall is eleven deep here and its head has flat ground on it.

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
- **read a copied recipe's own foot and its own plan before placing two of them.** The body is the whole of
  it: nine cells of foot owe the standoff from all nine, and a crown with holes in it refuses a neighbour
  at three and admits one at two.
- **tell a decline from a complaint.** A `DR-CUT` or a `DR-STEEP` leaves the prop standing and says it is
  wrong; everything else on this card takes it out of the world.

## What checks it

- `declines.txt` — the spine: every prop of every ladder, its stated step, and the rule and coordinate for
  each answer the book gave. 106 placed, 18 declined and 4 complained about, 9,627 cells claimed.
- `dressing.txt` — the same read as text: the claims map a block a character, twelve classes, and the
  declines under it. This is where a keep-out is *seen* rather than inferred.
- `columns.txt` — fourteen columns: the oak standing on the unmarked wall's head, the boulder bedded into
  it, the marked wall with nothing on it, a placed oak and the road its standoff was measured to, the cell a
  declined oak was asked for, a bedded rock, the wood's floor, a flora cell, the monument, a hand-placed
  trunk beside a template one, and the 63° face.
- `census.txt` — two themes over 57,344 cells; the walls are 720 of them.
- `trees.json` — the two hand-built recipes, block for block, with the `tree-showcase` row each came out of.
  A body cannot be re-derived from anything, so it is committed rather than generated.
- `incline.txt` — 97.3% of the ground under 10°, and the 2.3% at 40° or steeper is the two walls' faces and
  the one graded pad. Fifteen pads are flat on purpose: a grade puts a second rule into every measurement.
- `trees-and-boulders.layout.json` · `.intent.json` — the two documents the board was stored from.

Renders: `row1-standoffs.png`, `row2-claims.png`, `row3-keep-outs.png`, `row4-a-body.png`;
`section-walls.png` — the two walls cut at z35, the only view a prop standing on a wall head reads in;
`section-grade.png` — the one graded pad, fourteen blocks over six cells; `iso.png` for all sixteen.
