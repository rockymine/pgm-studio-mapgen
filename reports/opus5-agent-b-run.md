# Agent B — four boards, cold and pale

Four boards driven through pgm-studio's HTTP API in one run: a CTW, a DTM, a DTC and a KotH. The set was
given one ground family — **cold and pale**: chalk, limestone, snow, ice, birch, bleached timber, grey-blue
water, pale quartz — and the work of the run was to make four boards inside that family that do not read as
one board four times. The four identity sentences below were written together, before any shape was
authored, and the hue-and-value column is the check taken **across** the set rather than within it.

## What I set out to build

| slug | mode | in one sentence |
|---|---|---|
| `opus5-flintwick` | CTW | Two chalk headlands facing each other over a grey-blue sound, worked for flint: each team's two wool rooms are cut into the chalk behind its own spawn, and the only way across the sound is a bridge somebody has to build in full view of both cliffs. |
| `opus5-grykefell` | DTM | A limestone pavement fell where the ground itself is the cover — clints, grikes and a shallow gill — carrying one monument in the open on a scoured slab, with a different kind of approach onto it from each quarter: through a birch hag, down off a scar, up out of the gill. |
| `opus5-birkmire` | DTC | A frozen birch mire, white bark on white ground, whose core stands on a low holm in a shallow frozen pan — so the last twenty blocks of every raid are across open ice with nothing standing on it. |
| `opus5-sparholt` | KotH | An alabaster-cutting works on two storeys, where nothing is raised and the objectives are sunk: the centre pad is inside a roofed cutting shed entered only by its four doors, the two flank pads lie in open sawpits two blocks below the yard, and a tramway undercroft joins the two pits without passing the middle. |

### The three tone families, per board, checked across the set

| board | ground | built | accent | where it sits in the pale range |
|---|---|---|---|---|
| `opus5-flintwick` | chalk — white hardened clay, bone-pale stone, quartz | flint-knapped masonry: dark grey cobble and gravel courses | **flint**, near-black, the one dark thing on a white board | brightest, highest contrast |
| `opus5-grykefell` | limestone pavement — stone, andesite, pale grey brick clints | bleached spruce timber over pale stone footings | **straw**: dry grass and hay on the shelves | cool grey with a dry warm note; mid value |
| `opus5-birkmire` | snow, packed ice, ice, frozen podzol peat | birch-framed bothies, white-washed clay | **blue-white**: clear ice and light-blue clay at the water | coldest and bluest, lowest contrast |
| `opus5-sparholt` | alabaster — quartz block, white and light-grey clay, in courses | the works: birch beam and bleached plank over quartz pier | **iron-grey**: the saw frames and tramway | warm pale, wholly built; no landscape in it |

Everything below is written after the boards were built.

---

# What was built

Four boards, four modes, one ground family. All four export, all four gate `OPEN`, and **all four
place every prop they state**.

| slug | mode | board | score | declined | dead | themes | the one thing it is |
|---|---|---|---|---|---|---|---|
| `opus5-flintwick` | CTW | 80 × 200 | 1.48 | 0 of 42 | **0.0%** | chalk 61.9 · sward 18.9 · strand 13.5 · knap 5.7 | flint painted by angle, so the dark is only ever on a face |
| `opus5-grykefell` | DTM | 80 × 200 | 0 | **0** of 36 | 13.1% | fell 70.1 · turf 27.5 · scree 2.4 | the ground is the cover; a coast drawn by sixteen vertex inserts |
| `opus5-birkmire` | DTC | 80 × 200 | 0 | **0** of 44 | 14.7% | mire 61.0 · ice 34.2 · holm 3.0 · garth 1.9 | one place with nothing on it, and the core is on it |
| `opus5-sparholt` | KotH | 80 × 150 | 0 | **0** of 8 | n/a | yard 65.1 · rock 26.1 · bank 6.4 · adit 2.4 | a building with a board in it, on two storeys |

Instruments each board actually used, counted off the finish it generated:

| | reliefs | marks | pushes | level | raise | sink | subtract | excluded ground | polyline | made layers | copied trees |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `flintwick` | 1 | 6 (area · point · scarp) | 2 | 5 | 6 | 0 | 0 | **2** | **4** | 0 | 8 |
| `grykefell` | 1 | 5 (area · line · scarp) | 2 | 1 | 6 | 0 | 0 | **1** | 0 | 0 | 5 |
| `birkmire` | 1 | 8 (area · point) | 2 | 2 | 3 | 0 | 0 | **1** | 0 | 0 | 5 |
| `sparholt` | 1 | 2 (area) | 0 | 1 | 1 | 1 | **2** | 0 | 0 | **4** | 0 |

Every board's ground theme is a `layered` stack on the **slope** axis except `sparholt`, which has no
landscape in it and says so with a bimodal angle distribution (78.6% under 10°, 13.3% at 50–59°, and
almost nothing between).

Per-board reviews with every read in them: `review/opus5-flintwick.md`, `review/opus5-grykefell.md`,
`review/opus5-birkmire.md`, `review/opus5-sparholt.md`.

# Where the boards depart from the sentences above

**`sparholt`'s sawpits are ten courses below the yard, not two.** The sentence said two, and two
cannot carry a tramway: an undercroft needs its own headroom plus the deck over it as a lid, and the
deck alone is four courses. The pits are what is left when the deck is not laid over them, so their
floor is the tramway's floor and the depth is the deck's thickness plus the tramway's headroom. A ramp
cut in the deck beside each pit, fourteen blocks of run for six of fall, and two two-block steps at
its foot, are the way in. Everything else in the sentence holds.

**`flintwick`'s headland is two headlands.** The board is named for a wick — a bay — and it now has
one: thirty-five blocks of open water cut into the land between its two nabs, joined only behind the
bay head. That came out of `G8` (below) and it is the better board: the frontline went from
`profile straight, 80 blocks on one line` to `profile offset`, and a raider who lands on one arm is on
that arm.

# What the system could not do, and what it does that is not obvious

**A `tread` did not grade a `point` mark against an `area` mark.** `RL3`'s fix is a tread on the later
of two marks, narrower than its `r`, so the band past the tread grades into what the earlier mark put
there. On `birkmire`'s `hum-w` — a point mark standing seven courses over the `pan` area mark's pinned
band — `r 9, tread 3` moved the step **not at all** and made the seam longer, 16 cells to 21, because
the wider radius reached further into the pan; `RL2` then appeared on the extra barrier. The same on
`hum-s`: step 3 held, 32 cells became 64. What fixed it was the arrangement — the mark came off the
area mark's ground entirely. *This is one board's reading. The tread may behave as documented between
two `line` or `scarp` marks; what it did not do here was grade a point against a pinned area.*

**A `polyline` states its band as `radius` and its centreline as `vertices`**, like every other shape —
not as `width` and `points`. Stated the other way it stores at 200, pre-flights `OPEN`, and is a path
of width nought that draws no ground. `SK4` says so on the dressing preview and nothing else does.
Two walls on `flintwick` were absent from the world for one build because of it.

**A `sink` cannot open a hole.** It brings the top down and writes ground the whole way to the shape's
floor, which on `sparholt` filled the storey underneath and came back `SEALED` on the void scan. The
instrument for a hole is a `subtract` over exactly the courses to remove; `SK13` then governs what may
stand near it, and its clauses are precise and worth reading in full — *an add whose top stops at or
below the hole's floor is the ground under the void* is what let the two steps at the ramp foot exist.

**An override add cannot put its top below its own layer's floor.** `sparholt`'s ramp is cut to y16
and arrives at y20, because the deck layer's floor is y20. Nothing says so; a transect does.

**A shape's `x1` is exclusive when a polygon rasterizes.** One column of deck stood between the ramp
foot and the pit — a six-block wall across the only way into the lower storey — at 200, `OPEN`, and
invisible to every read but a transect.

**`rot_180` mirrors authored shapes, and two ramps become a V.** A ramp beside the west pit and a ramp
beside the east pit land in each other's columns: the image of one is the other, running the other
way. Measured at x 17: `26 23 22 21 20 21 22 23 26`. State one and let the image be the other.

**`fill-ratio` (`G8`) is measured on wool boards and not on destroy boards.** `grykefell` with a
sixteen-cell back row — geometry identical to `flintwick`'s first plan — evaluates at `score 0` with
no such term; `flintwick` read `0.9 outside [0.201, 0.542]`. The band says a capture board is under
half land. With the wick cut out this one is 0.794 and stays there: getting under the ceiling needs
roughly another 100 cells of void inside the piece bounding box, which at this size means arms under
25 blocks wide. Recorded, not chased.

**Coverage cannot read a capture board.** `controlPoints` ride on the finish into the intent, because
the plan states no capture point; so a KotH plan has no goal, `04-routes.txt` says *no route between a
spawn and a goal*, and `GET …/coverage` reports 72.1% dead in one patch covering all three points.
`01-flow.txt` says the honest thing — *this plan states no objective, so there is no journey to read
and nothing to call dead* — and the coverage number does not. **The empty-board fault cannot be
decided on a KotH board by the read that decides it everywhere else.**

# What I got wrong

- **I believed a rule's fix without measuring it.** Three `RL3` seams, a tread stated as documented,
  and the board came back with a fourth complaint and longer seams. The read was there the whole time
  and I ran it only after the change, not before and after the way it has to be run.
- **I wrote a polyline's band as `width` and its line as `points`** because that is what the words in
  the skill's table look like, instead of reading `SketchShape` in `openapi.json`, where `radius` is
  *"a circle's radius, or a path's half-width"* in as many words.
- **I read a `stack()` helper's own argument order backwards** on `flintwick` and shipped a voronoi
  where a thickness goes. The refusal was `DR-DOC … could not be converted to System.Int32`, which
  names the field and not the cause, and it cost a build.
- **I reasoned about the pits instead of building one.** Two builds went by on the assumption that a
  `sink` through a thinned slab leaves the storey below open. A single `column` at the pit's centre
  after the first build would have said otherwise; I read the void scan instead, saw `SEALED`, and
  still went one more round before taking the column.
- **I nearly shipped `grykefell` with five declined props** because the brief said the board was done
  and I read that as "do not look". The review read said otherwise in its first ten minutes. Two
  `loop.py --candidates` passes of eight positions each found four sites that stand out of fourteen
  tried, and the board now places 36 and declines none.
- **I fixed `SK26` on `flintwick`'s west stair and introduced it on the east ramp.** The west head was
  cut four courses under the ground it arrived on; raising it and lengthening the flight cleared it
  (`worst step 2, 0 barrier, 0 scramble, 0 drop`). The east ramp's head then read `BARRIER +3 at
  (24, 44)` and `DROP −4 at (24, 39)`, because the two arms' downs do not stand at the same height and
  I gave both flights the same number. It is in the review and it is **not** fixed.

# Questions about how these maps play — for the author, not answered here

Each of these is a question about the map as it is played, which neither the corpus nor the code can
settle. None of them is filed as a fault.

1. **`grykefell`'s scar is one-way** — 121 cells of barrier face, approachable from above and not from
   below. On a destroy board with a single monument, does a one-way approach into the objective's
   quarter make the defender's position legible, or halve the attacker's options?
2. **`birkmire`'s holm stands two courses over the pan**, so the last step onto the core's island costs
   a placed block from every direction except the six-block spit. Is that the right price? It makes the
   spit the obvious approach and therefore the obvious place to defend — or it makes the other three
   quarters of the pan decoration.
3. **`flintwick`'s wick is a build zone**, so the bay can be bridged as well as the sound. That gives a
   raider three crossings, and the bay crossing is the only one not overlooked by a cliff. Is that a
   third option worth having, or the one crossing that makes the other two pointless?
4. **`sparholt`'s two pits are joined to each other and not to the middle.** A team holding both pits
   holds two points and can move between them out of sight; a team holding the shed holds two points
   and is surrounded. Is that the right trade on a three-point board?
5. **Four boards in one value range.** The set was built to be cold and pale end to end, and the check
   taken across it was hue and value rather than subject. Does a four-map rotation in one palette read
   as a set, or as one map four times? That is a judgement about a rotation, and nothing in this
   repository measures it.


---

# The author's round: seven readings, and what each one was really about

Every item below arrived as a read with coordinates in it, and every one was closed by taking that
read again on the rebuilt world. Three of the seven turned out to have the same cause.

## A prop seated on the wrong block raises nothing anywhere

**Twelve trees across three boards stood on ground no tree grows in** and not one of them was
declined, complained about or warned. `grykefell`: three birches on bare **Diorite**. `flintwick`:
six on Quartz Block, Cobblestone, stained clay and one on **Coal Block** — because that board's whole
palette was chalk, quartz, gravel, shingle and flint, and it had **no soil in it at all**.
`birkmire`: three on **Packed Ice**, and one whose body began eight courses over the ground, seated in
a neighbour's canopy.

`DR-SITE` asks whether there is ground; `DR-CLAIM` asks whether something else holds it; `DR-ROAD` and
`DR-KEEP` ask about standoffs. **Nothing asks what the block is.** The read that answers it is one
`column` per prop with the leaves and logs filtered out, and it costs a second each.

Two different fixes, and the author named both: *relocate them, or make more grass areas to seat
them.*

- `grykefell` got **two more shelves of turf** — `turf-scarth` west of the gill, `turf-nab` on the
  northern shoulder — placed where soil gathers on a limestone fell, and one tree moved to reach one.
  Turf went 15.4% → **27.5%**, and `fell | turf` 449 → 627 border cells.
- `flintwick` got **a soil theme it did not have**: `sward`, grass over coarse dirt over chalk, in the
  coombe and on each arm's lee — plus the under-12° band's top course mottled so it picks grass one
  cell in five, because chalk downland is grass and the board was painting a white plate. Four themes
  now: chalk **61.9%**, sward **18.9%**, strand 13.5%, knap 5.7%.
- `birkmire` moved four, each to a position read off the built world first. Snow is not the fault ice
  is — `column at (−36, 30)` reads snow over two courses of coarse dirt — so the snowy sites stand.

All twenty-six trees across the three boards now read Grass, Coarse Dirt, Podzol or snow-over-soil.

## A structure sized to one ground level, standing across two

This is the shape the author gave both the barn and the ramp, and it was the right frame for one of
them.

**`grykefell`'s barn** was the only house in twelve boards with terrain inside its footprint: a
transect across the cross wing read `BARRIER +5 at (18, 28)`, y22 west and y27 east. The fix is not a
nudge, it is to give the building one ground level. The shelf right of the spawn stands **level at
y31 from x 21 to x 37** — read at z 72, 78 and 84, every station 31 — and `barn-garth`, a
`relief_scope: "exclude"` pad over x 17..37 z 70..84, holds it there. Across the cross wing now:
`rises 1, falls 0, worst step 1: 0 barrier, 0 scramble, 0 drop`.

**`flintwick`'s east ramp was not that fault at all.** `BARRIER +3 at (24, 44)` came from a plateau at
y28 over z 40..44, and that plateau is `wall-e` — the board's own cliff-top wall standing two courses
proud across the head of the flight. A wall drawn along one line without regard to where the ways come
up. Each arm's wall is now two runs with a **gateway** between them, at the stair on the west and the
ramp on the east, which is also what a drystone wall actually looks like.

**And then the west stair failed a third way.** With the wall off it, it read `DROP −4 at (−29, 40)`
and the stations showed dead-flat y31 from z 41 to 50 — the flight was not in the world. The cause:
**`sward-west`, a `raise 0` paint patch drawn after the flights, sets those columns back to the median
ground.** A later shape wins a contested cell, so paint drawn over a flight deletes it, silently, with
no rule and no warning. The sward now goes down first and the flights are cut into it. Both flights:

```
stair-w  rises 1, falls 11, worst step 2: 0 barrier, 0 scramble, 0 drop | walked end to end
ramp-e   rises 0, falls  8, worst step 3: 0 barrier, 0 scramble, 0 drop | walked end to end
```

`stair-w-hi`'s two anchors are now read off the built world — y24 at (−29, 32) below the face, y31 at
(−29, 48) above it — instead of taken from the plan's `DOWNLAND`. One number for two different grounds
is exactly what put it wrong, twice.

## The Cairn is a cube

`grykefell`'s destroyable is now **`cube-3`** — 27 blocks of end stone round a bedrock core, region
`19,31,53 … 22,34,56` — rather than `pillar-2`'s two. The goal is 42–43 blocks from its own spawn with
20 of lateral offset, and the author's call is that the distance is only survivable if breaking the
monument costs real time. Not a read: a judgement about how the map plays, and it is the author's.

## Kept

`flintwick`'s build zone is still **two stated rectangles** — `sound` across the strait and
`wick-water` up the bay — which `rot_180` makes into a stepped edge rather than one ruler-straight run
across the board. It has not been flattened, and the frontline still reads `profile offset`, (−40, 10)
to (40, 45).

## The correction taken

`GET /coverage` cannot see a control point, so `sparholt`'s 72.1% dead is an artefact of a capture
board having no plan goal — not the empty-board fault. That is now stated as a **studio gap** in
`review/opus5-sparholt.md` rather than as anything the board should answer for.

## Where the boards stand after the round

| slug | props | dead | flights | trees on soil | gate |
|---|---|---|---|---|---|
| `opus5-flintwick` | 42 placed, 0 declined | **0.0%** | both clean | 9 of 9 | OPEN |
| `opus5-grykefell` | 36 placed, 0 declined | **13.1%** | n/a | 6 of 6 | OPEN |
| `opus5-birkmire` | 44 placed, 0 declined | **14.7%** | clean | 11 of 11 | OPEN |
| `opus5-sparholt` | 8 placed, 0 declined | artefact | clean | n/a | OPEN |
