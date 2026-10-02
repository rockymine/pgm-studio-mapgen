# Trees and boulders

**A prop is not drawn, it is asked for.** The dressing pass seats every one against a book of claims and
answers on a **200**, so a prop the book refused is simply not in the world and the only thing that says so
is the entry beside it. Sixteen pads ask for 124 props and get 104. Open it in the studio as
`technique-trees-and-boulders`, or run `build.py`.

**So the numbers in that book are the whole of what an author needs, and every one here is a ladder rather
than a formula.** Each panel states the same prop at a stepping distance from the thing that might refuse
it, and `declines.txt` says which rung the rule cuts at. Nothing on this card is remembered.

**And the read gives two answers, not one.** A **decline** means the prop is not in the world; a
**complaint** means it is, minus whatever was cut off it, or standing somewhere it reads wrong. Twenty of this
board's twenty-four entries are declines and four are complaints, and telling them apart is the difference
between a missing tree and a half-written one.

**The one fact the ladders turn on: a prop is tested at its own lowest course and claims more than that.**
`Seats` walks only the cells a prop rests on, so a tree is judged by its trunk and a boulder by its
footprint — and once placed, a boulder claims its whole body and a tree the disc its crown covers, out to its
farthest leaf. Every distance below follows from that asymmetry.

## The document

Sixteen pads on one `ground` layer, one theme, and fifteen of them with no relief — a plain solved to y7,
because a grade would put a second rule in every measurement. Two pads carry an authored wall, one carries
a monument, and the last one is graded on purpose. Five recipes: two template oaks, a boulder, and two
bodies cut out of the `tree-showcase` world, taken from the studio's tree library (`tools/showcase.py`).

| panel | asks for | what the book said |
|---|---|---|
| `tree-standoff` | a road, four oaks stepping off it | declined at **2**, placed at 3 (`DR-ROAD`) |
| `boulder-standoff` | the same road, four rocks | declined at 2 and **3**, placed at 4 — the foot is wider than the cell |
| `a-wide-brush` | a radius-8 `rough` brush, four oaks all 11 off it | all four placed, two at exactly the standoff: the band **wanders** |
| `set-back` | a narrow road and nine oaks behind it | nine placed: the road drawn so nothing is lost |
| `two-boulders` | one pair 3 apart, one pair 9 apart | the near pair loses one (`DR-CLAIM`) |
| `kind-decides` | a rock and an oak two apart, twice, order opposite | **both oaks** declined either way |
| `two-trees` | nines at 2–5 and fourteens at 3–6 | nines need **5**, fourteens need **6** |
| `a-wood` | forty-five darts against that rule | forty-five placed |
| `a-kept-clear-wall` | a wall stating `keepClear`, two props on it | both declined (`DR-KEEP`) |
| `an-unmarked-wall` | the same wall without the field | both placed, **standing on its head**; the oak a `DR-ROOT` complaint |
| `a-goal-clearance` | a monument, oaks at 9, 10, 11, 12 | 9 and 10 declined (`OB19`) |
| `flora-overlay` | a road, a rock, and an overlay over both | 1,592 cells written, nothing declined |
| `a-copied-tree` | `large-pine-1` and `large-pine-4`, and a template | discs of 317 and 377 cells against **81** |
| `a-body-s-foot` | both bodies three off one road | the nine-cell foot declined, the three-cell placed |
| `a-copied-crown` | pairs of `showcase-tall` at 2, 6, 11, 12 | **declined until 12** — the crown's holes decide nothing |
| `props-on-a-grade` | a 63° face with an oak and a rock on it | both placed, both complained about |

```json
"dressing": {
  "styles": {"oak-9":  {"kind": "tree", "form": "template", "species": "oak", "height": 9},
             "rock-3": {"kind": "boulder", "form": "round", "size": 3, "mossy": true, "rock": "…"}},
  "props":  [{"id": "off-2", "kind": "tree", "seed": 3400, "x": -124, "z": -66, "style": "oak-9"}]}
```

## What paving keeps off

**A tree keeps three blocks from the nearest paved cell and a boulder keeps two.** `off-1`, two from the
band, is declined — *"rests on (−138, −102), nearer than 3 blocks to the road at (−140, −104)"* — and `off-2`
one cell further out is placed. On the rock ladder `rock-off-1` and `rock-off-2`, two and three from the
band, are declined, and `rock-off-3` stands at four.

**Because the boulder's distance is measured from its body, not from the cell it was asked for.**
`rock-off-1` was stated at (−60, −102) and the decline names (−62, −103): a size-3 erratic's foot reaches two
cells out from its centre, so the *centre* has to stand two plus that reach away. A tree's trunk is one cell
and its centre is its distance.

**A texture brush is a road, and `DR-ROAD` prices it at the brush's own width plus the standoff.** The
radius-8 `rough` brush claims **1,026** cells and the radius-2 road beside it claims **252** over the same
length of board — four times the paving, and therefore four times the ground nothing can stand on.

**And a `rough` band has no constant edge, so the strip it kills is a range and not a number.** Measured off
the claims map: the brush's band is **13 to 19 cells wide** and reaches **4 to 9** south of its centreline,
because `rough` spends its knob wandering the half-width over a 7-block scale. The road's `solid` band is 4
wide at every one of its columns.

**Which is why the ladder for this panel steps along the brush rather than away from it.** Four oaks, all
stated eleven off the centreline, at four places down its length: within two columns of each, the band
reaches seven, eight, seven and eight south, so all four stand, the second and the fourth at exactly the
three-block standoff. Where it reaches nine, an oak stated eleven off is two from the paving and refused —
the same distance is clear of the keep-out at one x and inside it at another.

**So brush the ground that is meant to be open and draw the road narrow.** `set-back` is a radius-2 road
with nine oaks thrown south of it, every one placed. A paved forest floor is an empty forest.

## What a prop keeps off another

**`DR-CLAIM` is footprint overlap and nothing else.** Two size-3 rocks three apart contest —
*"rests on (−131, −43), claimed by the prop 'pair-near-a'"* — and the same two nine apart both stand. There
is no standoff between props, only the question of whether one rests where another already is.

**Between two trees that reads as one crown, not two.** A tree is tested at its trunk and claims the disc
its crown covers, its radius the farthest leaf of that tree's own build, so the second oak is declined
exactly when its trunk falls inside the first one's disc. Measured with one seed pair down each ladder: a
pair of nines is refused at 2, 3 and 4 and stands at **5**; a pair of fourteens is refused at 3, 4 and 5
and stands at **6**.

**Which means what two trees need is the larger of their two crowns and not the sum of them.** Five blocks
for a nine and six for a fourteen, measured from trunk to trunk — `a-wood` throws forty-five darts against
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

**With `keepClear` the wall declines what leans on it, by name.** *"rests on (−128, 34), which is kept clear
for a stated structure"*, for the rock and the oak both, and the column at the wall's middle reads its top
course at y13 with nothing above it.

**Without it the wall is ground like any other and the props stand on its head.** `an-unmarked-wall` places
both: the oak's trunk starts at **y14**, on the wall's own top course, six courses over the meadow, and the
boulder is bedded into the wall head beside it. Nothing refused either; the oak draws a `DR-ROOT` complaint,
a trunk standing on stone bricks, and the rock nothing at all.

**A goal's clearance is a 21 × 21 square on the monument's own cell, and it declines a prop from the prop's
end.** `OB19` refuses the oaks at Chebyshev 9 and 10 — *"inside a goal's clearance"* — and passes those at
11 and 12; the claims map shows 408 of its 441 cells, the other 33 under the discs of the two oaks that
stand just outside it. Where `objectives-and-clearances` reads that rule from the
goal's side, this is the same rule seen by the thing it turns away.

**The overlay is the one thing that is never declined.** `flora-overlay` writes 1,592 cells of grass, fern
and flower round a road and a rock without being asked to stand anywhere, because it is paint on whatever
cells the pass left free. A wood's floor belongs to it and to the theme, not to props.

## A tree somebody built

**A copied recipe has no species and no nominal anything.** `showcase-tall` and `showcase-giant` are
`large-pine-1` and `large-pine-4` (bands `r2` and `r3`), cut out of that world with `seed-trees.cs` and stated as 311 and
412 blocks of `[x, y, z, id, data]`. What they look like is what was built; the studio's part is to seat
them, turn them round the symmetry and keep their leaves.

**They hold four times the ground a template does.** Their own plan covers 144 and 147 cells, and the read
gives each the disc out to its farthest leaf: **317** cells for `showcase-tall`, a radius of ten, and **377**
for `showcase-giant`, eleven, against **81** for the `oak-14` standing beside them, five — and a template's
whole statement was a species and a number.

**A body's foot is every cell of its lowest course, and that is what the standoff is measured from.**
`showcase-tall` rests on three, its trunk and the two planks laid under it at x −1; `showcase-giant` rests on
**nine**, spanning x 0..3 and z −1..3. Anchored
at the same three blocks off the same road, the slender one stands and the giant is declined — *"rests on
(−26, 108), nearer than 3 blocks to the road at (−28, 106)"*, naming a foot cell rather than the anchor.

**A hand-built crown is not symmetric and not even solid, and neither decides anything.** `showcase-tall`'s
plan footprint across its own trunk row reads `..########..####.`, so the cells at (1, 0) and (2, 0) are
**holes** — but the tree holds the whole disc, holes and all, and a neighbour's foot has to clear it.

**Two apart, six apart and eleven apart are each declined, and twelve apart stands.** The pair at 2 puts its
second tree's foot into the holes and is refused — *"rests on (16, 90), claimed by the prop 'crown-2-a'"* —
a plank laid under that trunk at x −1, which is (1, 0) from the first trunk: a hole in the body and inside the
disc. At 11 that plank lands on (10, 0), the disc's last cell along x; at 12 it lands on (11, 0) and the
pair stands, with nothing cut off either.

**Which is the general shape of it: `DR-CLAIM` refuses and `DR-CUT` reports.** A prop seats on its feet and
is then written wherever it meets air, so standing clear of something is not the same as fitting beside it.
The rock on the graded pad is the case here — *"62 of its 99 blocks are inside something already standing"*
— and for a body of four hundred blocks the difference is worth reading.

## Also refused, met while building this

**`DR-STEEP` is a rock's rule and nobody else's, and it complains rather than refusing.** `PlaceBoulder`
asks it and `PlaceTree` does not, so `props-on-a-grade`'s 63° face takes an oak with only a `DR-ROOT` note
about the stone under its trunk, and keeps the boulder beside it with this one: *"stands at (131, 105) on
ground inclined 63°, and the theme painting that cell calls the ground a face"*. The rock is in the world;
the pass has told you it looks wrong.

**The angle it compares against is the theme's own cliff band, not a constant.** This board's `meadow` puts
grass under 35° and coarse dirt to 55°, so 51° of face raised nothing at all and 63° raised the complaint.
A first cut of the wall panels made the wall five cells deep, every cell of its head an edge, and the
boulder on it came back at 56°; the wall is eleven deep here and its head has flat ground on it.

**`DR-SITE` and `DR-CLAIM` both catch a dart thrown badly.** A wood thrown past the pad's own coast raised
*"has no ground at (131, −41)"*, and one thrown across the road raised *"claimed by the paving"*. The box a
thrower throws into is the author's arithmetic; the pass only reports what it hit.

## Asking forwards instead of hearing a decline

**Every rule on this card can be asked before a prop is placed, and `POST …/sketch/seats` is the ask.**
It answers a raster marking every cell a footprint may seat on, plus a `refused` list of rule → cells,
largest first. `seats.txt` is this card's own board read four ways: a tree seats on 44,056 cells, a boulder
on 52,725, a 9 × 7 house on 19,293 and a 13 × 11 house on 13,609.

**A mark is where the footprint's minimum corner may go, not its centre.** So a house's mask is its own
width and depth narrower than the ground it is read over, and a position taken off the raster is the
building's corner.

**Each kind carries its own standoff from a drawn route** — three blocks for a tree, two for a boulder,
none for a house. That is `DR-ROAD` asked forwards rather than heard as a decline.

**The `refused` list is what answers "why is there nowhere".** On a composed board with a spawn march, a
wool approach and a road, `DR-PASS` and `DR-SITE` between them can take every passable footprint the team
side had — a fact about the board rather than about the siting, and only this read states it.

**The layout goes in the body and the knobs are the query.** `kind`, `width` and `depth` are query words;
posting no body answers **200**, `seats: 0` and `bounds {0, 0, -1, -1}` — an empty board, cleanly, with no
finding of any kind. And `kind` defaults to `tree`, so a house mask asked for without it is a tree mask
that will seat almost anywhere and mean nothing.

## The recipe

**Ask for the props, read the declines, and fix the arithmetic — never the other way round.**

- **ask the mask before placing anything.** `POST …/sketch/seats` with the layout in the body answers
  where a kind may stand at all. Every position taken off it seats; a position chosen by eye is a decline
  waiting on a 200.

- **three blocks off paving for a tree, two for a boulder**, measured from the prop's resting cells: a rock
  whose foot reaches `r` from its centre wants its centre `2 + r` out.
- **a brush is an exclusion as wide as itself plus the standoff, and a `rough` one has no fixed edge.**
  Radius 8 measured 13–19 wide; budget from the wide end, brush what is meant to be open, and keep the
  wood's floor to the theme.
- **between two trees, the larger crown**: five for a nine, six for a fourteen, trunk to trunk.
- **between anything else, footprint overlap** — there is no standoff, only occupancy.
- **a rock always beats a tree**, whatever the document order says.
- **an authored shape says `height_mode`/`skirt` to the relief and `keepClear` to the dressing.** Both, or
  a prop stands on it and nothing reports the tree growing out of the battlement.
- **keep props eleven blocks off a goal's anchor**, which is the 21 × 21 clearance with one to spare.
- **fill with a flora overlay, not with more props** — it takes what is left and is never refused.
- **read a copied recipe's own foot and its own plan before placing two of them.** The body is the whole of
  it: nine cells of foot owe the standoff from all nine, and a crown with holes in it still holds the whole
  disc out to its farthest leaf — `showcase-tall` admits a neighbour at twelve and not before.
- **tell a decline from a complaint.** A `DR-CUT` or a `DR-STEEP` leaves the prop standing and says it is
  wrong; everything else on this card takes it out of the world.

## What checks it

- `declines.txt` — the spine: every prop of every ladder, its stated step, and the rule and coordinate for
  each answer the book gave. 104 placed, 20 declined and 4 complained about, 12,304 cells claimed.
- `dressing.txt` — the same read as text: the claims map a block a character, twelve classes, and the
  declines under it. This is where a keep-out is *seen* rather than inferred.
- `columns.txt` — fourteen columns: the oak standing on the unmarked wall's head, the boulder bedded into
  it, the marked wall with nothing on it, a placed oak and the road its standoff was measured to, the cell a
  declined oak was asked for, a bedded rock, the wood's floor, a flora cell, the monument, a hand-placed
  trunk beside a template one, and the 63° face.
- `seats.txt` — the forwards read: how many cells a tree, a boulder and two house footprints may seat
  on, what refused the rest by rule and cell count, and the two ways the route answers nothing at 200.
- `census.txt` — two themes over 57,344 cells; the walls are 720 of them.
- `incline.txt` — 97.3% of the ground under 10°, and the 2.3% at 40° or steeper is the two walls' faces and
  the one graded pad. Fifteen pads are flat on purpose: a grade puts a second rule into every measurement.
- `trees-and-boulders.layout.json` · `.intent.json` — the two documents the board was stored from.

Renders, each the studio's own route: `iso.png` — all sixteen pads, `render/isometric`;
`section-walls.png` — the two walls cut at z35, the only view a prop standing on a wall head reads in;
`section-grade.png` — the one graded pad cut across its face at x131, fourteen blocks over six cells.
