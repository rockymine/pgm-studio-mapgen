# Art direction — how a board is supposed to look, stated as law

Twenty-one boards sit in this repository and the eye reads most of them as one board. That is the finding the
whole of this document exists to correct, and it is not a matter of taste: it was measured. Ten of twelve
settlements put every house on **two or three z-rows** behind the spawn, all facing the same way, on a "town
square" themed patch — never a watchtower in a field, never a barn away from the town. Twelve of fourteen maps
carrying buildings have **not one building without a footing**. Four maps by three models stacked grass three
courses deep. Three maps put obsidian in a destroyable over its limit. Five maps shipped a literal `<Team>`
placeholder to players.

None of that is a capability gap. Every rule below is expressible today, most of them in one field, and the
worked example for the hardest one is already committed to this repository. What was missing is a document
saying which choice is right, so three models reached for the same default and the boards came out alike.

**Read this before you draw ground, and check a board against it before you build the next stage.** It is
the same list the reviewer agent works from (`REVIEWER-BRIEF.md`), and the reviewer does not read your report,
so a rule broken here is a rule found there.

---

## 1. A board has one visual identity, and you state it in a sentence before you draw

Not "a themed map" — a specific claim about what this ground is and what it is made of, in a sentence you
could tell someone over the phone. *A frozen peat fen, dark and low, with an ice scarp on one flank.* *A
terraced clay hillside in five ochre steps.* *A drained tidal flat, pale sand and tarred timber.* If you
cannot write that sentence, you are not ready to author themes, and every board that skipped it came out
looking like the last one.

**Then the sentence becomes a palette of themes, one per kind of ground, and the pairing of paint to what a
shape is *for* is the whole trick.** A shape carries its own `theme`, and using one theme over the whole board
throws away the only thing the layout already tells you. The minimum that reads as designed is **three**: the
ground that is *grown*, the ground that is *built*, and the ground that is *landform* — a cliff, a scarp, a
cutting. Five is better and the strongest board in the repository uses exactly five.

**Name your three tone families out loud, and say which is ground, which is built, which is the accent.** A
board fails this in one of two opposite directions and both have shipped here:

- **It vanishes.** `basalt-reach`: all five themes sit on Stone (`1:0`) or Andesite (`1:5`), and three of its
  five houses are walled in Stone with an Andesite roof and a Polished Andesite verge — built from the same
  rock as the ground under them. Nothing separates a building from the hill it stands on.
- **It clashes.** `tallow-kilnrow`: `kiln-stack` is a `cell` over Quartz, Chiselled Quartz, White Clay, Smooth
  Sandstone and Light Grey Clay, with Red Sandstone two blocks away and a Red Stained Clay boulder sitting in
  it. Five near-identical whites and then an unrelated red.

The test that catches both: **a building may not be in the same tone family as the ground it stands on**, and a
board may not carry an accent that appears exactly once. A restricted palette is allowed and can be very
strong — but if you choose one, the legibility has to come from somewhere else, and you have to say where
(height, or a single reserved colour, or the built/grown split). Say it in the review.

**A pattern at the wrong scale is the third way to fail.** `tallow-mirefast`'s `mire-timber` puts a
`{"kind":"checker","size":2}` of coarse dirt and gravel over a shape 92 blocks wide. A two-block checker reads
as texture at ten blocks and as noise at ninety. Match a pattern's cell size to the shape it covers, or scope
it to a smaller shape.

---

## 2. The material rules, and they are hard

Every one was broken on a shipped board. Each carries the task id that will eventually enforce it in code;
until that id ships, **this document is the enforcement**, and the reviewer checks it by probing the world.

| Rule | The law | Broken on | Enforced by |
|---|---|---|---|
| **Grass is one course** | A grass course is exactly **1 block** thick and grass never appears below it. A palette containing grass is invalid at any `depth` > 1 unless it is the **top layer of a `layered` stack**. | `corvid-hollow`, `sable-marsh`, `sonnet-briarlock`, `tallow-weirgate` | `B163` |
| **Obsidian caps at three** | A destroyable may carry at most **3 obsidian blocks**, so only the **pillar** styles may use it. `cube-3` (27), `cube-4` (64) and `column-plus` (15) take **end stone, gold or emerald**. | `basalt-reach` 27, `corvid-hollow` 27, `tallow-mirefast` 15 | `B162` |
| **A slab goes in `RoofSlab`** | A slab named in `roof` builds a roof you can see straight through. The slab goes in **`roofSlab`** and a **whole block** in `roof`; a slab-course roof is only right at a **half-course rise**. | 6 Weirgate houses + its spawn | `B168` |
| **No log, no ground material, in a roof or a verge** | A log is never a roof or a verge. Neither is Grass Block, Podzol or any other ground material. | `verge: 162` on 6 Weirgate + Mirefast + Kilnrow houses; `quillon-barrow` roofs three houses in **Grass Block** over a **Podzol** verge | `B168` |
| **A block must be the kind its role needs** | `doorHead.block` must be a **stair**. `doorHead.fillBlock` under `upperSlab` must be a **slab**. A `slabBanded` or `stairLattice` window's `block` must be a slab or a stair respectively. | `sable-marsh` (cobble, cobble, pane), `corvid-hollow` (98/4, then fence and iron bars), `ashfall-scar` (oak fence) | `B160` |
| **A spawn door is 2.5 clear** | At least **2.5 blocks** of clear height. A three-course door leaves two clear courses only if the head's fill is genuinely an upper slab. | `sable-marsh` 2.0, `corvid-hollow` 2.0 | `B161` |
| **A window is plain** | Air, or glass. If it is filled it is filled with a **single block**. No patterned form — `slabBanded` and `stairLattice` are out for these maps whatever blocks they are given. | `sable-marsh`, `corvid-hollow`, `ashfall-scar` | `B161` |
| **A building seated into terrain has no footing** | `HouseStyle.Sill` lays a course one block proud on every side. Turn it off by naming **air** as the sill material. | 12 of 14 maps, 0 opted out | `B164` |
| **Gable at `pitch: 2` is overridden by its own wall** | The wall wins where they disagree, so the roof you asked for is not the roof that stands. Use `pitch: 1` on a gable until the mechanism is traced. | `corvid-hollow` ×2, `ashfall-scar` ×9, `tallow-kilnrow` ×2 | `B165` |
| **A goal name is a name** | No `<Team>`, no `<`, no `>`. PGM prints the attribute verbatim, on both teams, identically. Leave a core's name empty and PGM names it. | 5 boards, all Opus, across 3 runs | `B182` |

**The one correct worked example in the repository is worth copying by hand.** `quillon-saltworks`' `h2` and
`h5` carry `form: "gambrel"`, `pitch: 1`, `roofSlab: 126`, `roof: 5:5` — the slab in `roofSlab`, a whole
block in `roof` — which is exactly what `HousePresets.Diorite` does and exactly the inverse of every other
board's attempt. Read it before you write a roof.

**A technique worth having, since it is the one thing the last runs found that worked.** Nesting a `cell`
inside a `layered` gives a patchy top course over measured depth: a layer stack renders as one flat colour
from above, so putting a `cell` pattern in its top layer breaks that up without stacking anything. It is also
how you satisfy the grass rule while keeping a varied surface — grass at `thickness: 1` on top, a `cell` or a
plain block below.

---

## 3. A settlement is not a street

Ten of twelve boards built the same village: every house on two or three z-rows, spreading freely along the
other axis, one or two orientations, all of it on a "town square" patch directly behind the spawn. Measured:

| Map | Houses | Distinct z | Distinct x | Orientations |
|---|---|---|---|---|
| `tallow-weirgate` | 14 | **2** | 14 | 2 |
| `tallow-mirefast` | 9 | **2** | 9 | 2 |
| `ashfall-scar` | 9 | **2** | 9 | 2 |
| `tallow-kilnrow` | 7 | **2** | 7 | **1** |
| `basalt-reach` | 5 | **2** | 5 | **1** |
| `corvid-hollow` · `marlstone-steps` · `quillon-barrow` | 9 · 12 · 11 | 3 | 9 · 12 · 11 | 2 |

Two boards break it — `sonnet-cinderreach` and `sonnet-holdfast` — and they are the same two that turned the
building footing off, which is worth knowing: one model did notice, twice.

**So: a board carries at least three distinct placement ideas, and "the village" is only one of them.** Pick
three from — a street with a shared frontage line · a square with buildings facing inward · a single isolated
structure with a reason (a watchtower on a rise, a barn away from the town, a shed at a wharf head) · a
building on ground of a different kind or height from the rest · a run of buildings along a board edge acting
as a boundary. The last one is worth knowing a limit about: a building whose interior is filled — a mass
rather than a place — is **`B92` and is not built**, so an edge run today is enterable buildings and you say
so in the review.

**Alignment is authored, one prop at a time.** Houses at unrelated offsets read as debris no matter how good
the individual styles are. If two buildings share a frontage line, they share it because you gave them the
same coordinate, not because the sampler happened to. But **sharing a line is a decision you make three or
four times on a board, not the only thing you do.**

**The difference an eye reads first is aspect ratio and height, not material.** A settlement of six buildings
in one style at six different footprints and storey counts reads as a settlement. Six identical footprints in
six different materials reads as a colour swatch.

**Three placement rules are hard**, and each is somebody's shipped fault:

- **20 × 20 of open ground in front of a spawn** (`B172`). The only props permitted there are a single tree at
  the edge of the area, boulders and fauna. **No houses.** Mirefast's corridor came out 12 wide because two
  houses stood inside the box; `quillon-barrow` has *three* in it.
- **One block of clearance between buildings, eaves included** (`B166`). Corvid Hollow's house stands flush
  against the spawn's face with `"overhang": 2`, so its eaves reach two blocks *inside* the spawn wall.
- **A building is at least 5 × 5 and at most 20 × 20** (`B167`, `B157`). Eight of Weirgate's fourteen came out
  four blocks deep; `sable-marsh`'s spawn came out a **90-block hall** because a stamped building is sized by
  its plan piece and nothing bounds it.

And one that is not about buildings but is found the same way: **a house may be stamped over void and nothing
refuses it** (`B187`). Eight of eleven columns of `quillon-saltworks`' `h1` stand on nothing. Check the ground
under a footprint before you place it, because the export will not.

---

## 4. Ground is the design; elevation is built from shapes

A single relief pass over the whole island is the flattest, most generic answer available, and it is what
every weak run reached for. `tools/seeds/ruediger.plan.json` — hand-authored by this repository's author —
steps its ground with **ten `base_height` tiers and no relief block at all**.

Use relief for the ground that should read as *grown*. Use shapes and tiers for the ground that should read as
*built* or *placed*. Let the two meet, and use `relief_scope: hold` to keep a built thing flat while the
ground rolls around it — without it the relief solves straight through your plateau and the town arrives
covered in contour rings.

**A rim is a choice and it was never chosen.** `Rim` is a `TopBand` with an `Enabled` toggle and `RimEdges`
decides which edges it caps (`void` caps the landmass's true outside only, `drop` caps wherever ground falls
away, `boundary` caps every plateau boundary). On natural terrain solved by a relief, a rim on every drop
terraces rolling ground and reads worse than no rim. **Turn it off where the ground is meant to be grown, and
keep it where an edge is meant to read as an edge.** Every one of the first fifteen generated boards had a rim
because a rim was the default.

**The wall bucket takes a pattern, not just a block.** `wallRun` reads a cell's arc along the outer
void-facing face so a pattern runs *along* a wall; `wallDiagonal` cuts across it; a `layered` stack varies the
material *down* the riser, which is what a real cliff or a coursed retaining wall does. Tie the choice to what
the wall *is* — a cliff face, a built retaining wall and the side of a platform should not read the same.

**Rectangles are where a shape starts, not where it ends.** Promote a compiled tier to a polygon by replacing
its `vertices`; take Bézier `controls`; give a shape `height_mode` (`level`/`raise`/`sink`) with a `skirt`, and
per-vertex `anchor_heights` that **tilt** a surface. A tilted sunken bowl inside a flat pan is four fields and
it works on the first build. Two catches, both documented the hard way: a tier can fuse to **more than one
shape**, and reshaping only the first leaves the others' rectangles showing through; and **where the land is
higher than the piece** — a quarry, a sunken bowl — the land must run **over** the lower tier's fringe, mirrored
from the ordinary case, and then it can pull inward exactly the same way.

**A large open area wants level changes in it, not more trees.** A second mesa, a shelf, a cut. If a region
ends up bigger than what fills it, **shrink the region** rather than scattering props into it.

---

## 5. Scale, and where the void goes

**A destroy board is a lane.** Six of the eight `minuyo` boards — the tightest, most consistent set in the
corpus — have one dimension under 90. Every generated board here is roughly square (240×190, 170×220,
136×190), and on a square board every goal is nearly equidistant from both spawns, which is why the ratios
came out flat. The corpus median board is **118 × 149**.

**The single cheapest number to check a destroy board against**: a goal sits about **three times** as far from
the enemy's spawn as from its own. Corpus median 2.9 over 164 `dtcm` maps, p10 1.4, p90 5.0; only 27 of 164
fall under 2.0. Two spawn points, one goal, one division, no build required.

| | own spawn → goal | enemy spawn → goal | ratio | |
|---|---|---|---|---|
| corpus median | 49.4 | 135.2 | **2.9** | |
| `tallow-mirefast` | 40.0 | 140.0 | 3.50 | good |
| `tallow-kilnrow` | 43.0 | 139.5 | 3.24 | good |
| `quillon-foundry` | 77.8 | 109.8 | 1.41 | corpus p10 |
| `corvid-hollow` · `ashfall-scar` | 80.0 | 100.0 | **1.25** | below p10 |

The three lowest ratios are the three boards the author judged worst on play, arrived at independently.

**Two goals of one team stand at least 35 blocks apart** (`B175`) — Haiku DTM Tower put them **eight** apart on
one piece, with two sky markers ten apart. The two boards judged well spaced give the band to aim at:
same-team **70–75**, nearest enemy goal **95–110**. And the objective set should use the board it is drawn on:
Ashfall Scar is 240 × 190 with every objective on `x = 0` and the whole contest inside a six-block column.

**Void belongs between the teams, not across an approach — and `approaches.md` has been amended to say so.**
The old guidance about cutting a hole in the middle of terrain is **withdrawn for `dtm`/`dtc` boards** and
replaced by a **depression or a pond**: the same interruption of a run, the same reason to go around or drop
through, without removing the ground. A depression is also an entrance from *below*, which a hole does not
offer at all. `tallow-kilnrow` is the counter-example — an 88-block cut across 65% of the board's width sitting
between its own objectives and the middle, while the mid band where the two sides actually meet stayed solid.
The hole was where the join belongs and the join was where the hole belongs.

Do not overcorrect: four small holes around a connected middle draw play into the centre and leave the flanks
unused. **A hole is also what makes a flank worth walking to.** Where void goes is a composition decision about
which ground should be contested.

**On a CTW board, two islands sit 15 to 40 blocks apart** (`B158`), and one whole island belonging to one team
is the *right* shape rather than a defect. A **deliberately shared middle** — a landform crossing the symmetry
axis that neither team owns — is the one composition an agent invented that the author wants kept; it still
needs the 15-to-40 gap on **both** of its sides, which is exactly what Weirgate's `flat` did not have.

---

## 6. Five things about a spawn, because four boards each broke a different one

A spawn is the one place on a board where every player begins, so every fault there is a fault every player
meets. Nothing in the pipeline checks any of this yet.

1. **The door stands at least 15 blocks from the nearest void** (`B158`). Sable Marsh's opens *onto* a
   25-deep void buffer; Weirgate's opens onto a `subtract` sixteen blocks across.
2. **20 × 20 of open ground in front of it** (`B172`), houses excluded — see §3.
3. **The ground it opens onto is climbable back** (`B180`). Kilnrow's spawn steps down three blocks into
   `works` and cannot return; Basalt Reach does the same and puts its stair sixteen blocks off the centre line
   where nobody leaving the door meets it. **Move the route to the door, not the door to the route** — turning
   a spawn to face its stair puts an objective behind the player.
4. **The spawn sits near the back of its lane** (`SP2`) and **the iron goes beside or ahead of it, never
   behind** (`SP7`). Both are written law in `docs/generator/rules.md` and nothing applies them. Haiku CTW
   Rush put its iron five blocks behind the spawn point *and inside its own protection region* — a contested
   resource nobody can contest.
5. **The ground under a spawn carries something or it is not there.** Weirgate's `yard` is 80 blocks wide for
   a 20-block spawn; Mirefast's `steading` is 92. Raw size is not the test — a spawn in a corner that *is* the
   map is fine — but flat dead area around a spawn is dead area, and the fix is to shrink the shape rather
   than to sprinkle it.

---

## 7. Circulation is decided before dressing

State where a player walks from spawn to goal, and where the flanking approach runs, **before** any prop is
placed. Those runs plus a margin are the ground foliage does not get. This is the order the last runs
inverted, and the symptom is a forest that swallows the route it was supposed to shelter.

**Nothing is scattered.** Every prop is placed because there is an answer to *why here*. If you cannot answer
it, leave the ground bare and say so in the review — bare ground you chose is better than dressing you did
not.

**Compose the approaches so they differ.** A void hole makes players go **around**; a hill lets attackers
bridge in from **above**; a forest gives cover **through**, most valuable early; a depression is an entrance
from **below**; a village is fought room by room; open ground exposes, which is what an objective wants around
it. Three approaches that are all "walk through cover" is one approach drawn three times.

**A forest is measured as canopy share, not as a leaf count** — a spruce forest at 17,600 leaves rendered as
one solid mass with the routes buried, while a corpus map at 17,897 leaves over 72 trees renders as a wood a
player walks through. Nearly the same count, opposite maps. And **avoid `whorled: true`**: it builds 46 logs a
tree against a template spruce's 14, at 1.26 leaves per log, which is a trunk farm rather than a grove
(`B174`).

---

## What this document does not cover

It says how a board should look and be composed. It does not say how a map **plays** — that is
`docs/gameplay/approaches.md`, whose claims are the author's and are settled, and `match-flow.md`, which is
the recorded account of CTW matches. Where those two and this one disagree, they are the law and this is the
style guide.

And it does not decide anything the author has not decided. A question about play that `approaches.md` does
not settle is **recorded as an open question in your report**, with what you decided and why — never filed as
a fact. This repository has already committed one confident, wrong, invented gameplay claim derived from a
correct measurement.
