# B120, run 1 — Opus

Three maps authored by driving the studio's own endpoints. No capability was added to `tools/`, nothing in
`/home/user/pgm-studio` was modified, and the only script involved is a 110-line thing in a scratchpad that
posts JSON to documented endpoints and unzips the answer.

| Map | Slug | Kind | Size | Goals | Props | What it is |
|---|---|---|---|---|---|---|
| 1 — the canonical brief | `quillon-barrow` | DTM | 148 × 228 | 1 destroyable a team | 47 | a chalk heath: barrow in the open, wood west, crag east, village behind, channel in front |
| 2 — mine, CTW | `quillon-saltworks` | CTW | 168 × 168 | 2 wools a team | 24 | a saltworks: quartz pans stepping down to the brine, a black spoil bank, sheds at the corners |
| 3 — mine, destroy | `quillon-foundry` | DTC + DTM | 148 × 184 | 1 core + 1 destroyable a team | 23 | a hillside foundry in red rock: furnace on a black casting floor, stack on a slag ridge |

Each map has its own themes (four, six and six), its own room shells, and its own house styles — sixteen
themes and eight buildings written for these three boards and nothing else.

---

## 1. What I could not say

Split as the brief asks: **missing from the system** means no path to it exists at any layer;
**out of reach from where I was standing** means the path exists and I could not take it, or did not.

### Missing from the system

**A destroy map cannot say it is a destroy map.** All three boards ship
`<gamemode>ctw</gamemode>` and `<objective>Capture the enemies' wools!</objective>`, including the one
carrying a core and a destroyable and no wool anywhere.
`MetaGenerator` (`src/PgmStudio.Pgm/Authoring/MetaGenerator.cs:16, 24, 29`) writes `gamemode` from a
`const string Gamemode = "ctw"` and derives the objective line from `intent.Wools.Count` alone, so a
wool-less map falls to the plural branch. There is no field for either on `PlanModel.Meta`, on
`MapIntent.Meta`, or anywhere the intent endpoint reads; the map row's own `gamemode` column is
explicitly not writable (`WriteEndpoints.cs:43`). Every projection of the intent rewrites it. Looked for:
`meta` on both documents, `PATCH /map/{slug}/metadata` (name and authors only), `GET /objectives/vocabulary`.

**A relief landform cannot carry its own paint.** Terrain paint scopes to a **shape**
(`SketchShape.Theme`) or to the map. A hill made of relief marks lives inside some other shape's
footprint, so it can only ever wear that shape's theme, and there is no elevation band, no per-mark theme
and no second axis on `TerrainTheme` to hang one on. This is why Quillon Barrow's crag and Quillon
Foundry's slag ridge are `height_mode: raise` **shapes** rather than relief pushes: a shape can be grey
while the ground around it is green. The consequence is that the two ways of making terrain are not
interchangeable — one of them cannot be painted — and nothing says so.

**A stepped board can carry relief on exactly one tier.** A relief is one field per island against one
`base`, and every cell it covers takes its height from the solve. So every tier that is not at the base
must be `hold` or `exclude`, and neither can then carry any relief of its own. Measured: Quillon
Saltworks' readback reports **3 169 cells** for an island whose footprint is about 11 000 — the pan alone,
because the flat, the works and the stage are excluded. `sketch.md` states the mechanism ("there is no way
to give two parts of a landmass a relief each"); what it does not say is the design consequence, which is
that on a four-tier board three quarters of the ground is outside the elevation model and every landform
up there has to be an erected shape.

**A dressing prop's `kind` must be the JSON object's first key, and the documented example puts it
second.** `sketch.md`'s Dressing example is `{ "id": "d1", "kind": "path", … }`. Posted verbatim through
`PUT /map/{slug}/sketch` that stores fine, `POST .../sketch/finish` succeeds, and then
`GET /map/{slug}/export` answers **500**:

```
The JSON payload for polymorphic interface or abstract type
'PgmStudio.Minecraft.Dressing.PlacedProp' must specify a type discriminator. Path: $.props[0]
```

System.Text.Json requires the discriminator first. Moving `kind` to the front of every prop fixed all 47
in one go. Two things make this worth writing down beyond the typo: the failure surfaces **two stages
after the write that caused it**, and the one worked example in the document is the shape that fails.

**A path claims ground, and a building that touches it is dropped silently.**
`Decorator.PlacePath` adds every band cell to the `taken` set (`Decorator.cs:124`), and `PlaceHouse`
returns 0 — for **every orbit image**, not just the colliding one — if any footprint cell is taken
(`Decorator.cs:325`). Nothing is logged, nothing is refused, the export is clean. The brief's own
instruction is to line a settlement's buildings up along a street, which is precisely the arrangement that
trips it. Measured on the first Quillon Barrow village:

| House | footprint | street band at that x | stamped |
|---|---|---|---|
| `h1` | `x −38..−31, z −81..−77` | `z −76..−72` | yes |
| `h2` | `x −27..−16, z −82..−77` | `z −76.8..−72.8` | **no** |
| `h3` | `x −12..−4, z −81..−77` | `z −77..−73` | **no** |
| `h6` | `x 29..40, z −82..−77` | `z −77..−73` | **no** |

Found by probing `(−22, −79)` and reading terrace where a longhouse should be; `--buildings` reported
"10 roof components" and gave no hint that eleven had been asked for. The fix is authorial (move the
frontage line two blocks clear), but the diagnosis cost an hour and there is no reading that offers it.

**A wing, an L or a T.** `HouseProp.Points` is exactly two corners and `Footprint`'s multi-wing
constructor is unreachable from a document. `G172`'s open half; I did not need it, but a village of
rectangles is what the model permits.

**A goal placed with an empty `piece` is invisible in the only picture of a plan.** `GET /plans/{id}/png`
drew Quillon Barrow's board with its spawns and its four pieces and nothing at `(0, −50)`. `plan.md` says
the canvas cannot draw an absolute goal; the render inherits that. So the one raster the plan layer offers
cannot answer "where are the objectives" for exactly the boards that use the new placement.

### Out of reach from where I was standing

**A picture of a sketch.** There is none, by design and by documentation: the three sketch reads answer in
palette runs, contour polylines and numbers. I chose to build the world and read it back rather than
render the data myself — which works, and it means every geometry decision is checked one whole stage
after it is made. Everything I got wrong about the ground (the six-deep tail race, the dropped houses) was
found in a world read-back that a sketch-level picture would have shown sooner.

**Observer placement, walls in world coordinates, and anything else Configure owns.** I drove
`PUT /map/{slug}/intent/from-plan` with the compiled intent verbatim, which puts the observer at
`(0, observerY, 0)` — on Quillon Barrow that is a platform over the mid causeway. `PUT /map/{slug}/intent`
takes a whole `MapIntent` and would have let me move it, add `structures.walls` in absolute coordinates,
or hand-place iron. I did not use it. That is a limit of my route, not of the system, and I am naming it
because the honest form of "I could not" is often "I did not".

**A tree that is not one of six woods, and a second concentric rim band.** Both are previous runs'
findings, both still true, and neither bit me — my palettes were chosen inside what the model offers
rather than against it.

---

## 2. What I got wrong

**The one that nearly shipped: I wrote that a core cannot be broken by the kit this studio writes.** The
reasoning was clean and every step of it was sourced. `capabilities.md` says, in the present tense:
"Nothing in the generator ties the two together yet: `TeamsGenerator.GenerateKits` writes one fixed
'Standard' kit for every map with spawns, an iron pickaxe among its tools, with no branch for a destroy
objective or its material… until `B81` lands, pairing the kit to the goal is the author's job". A core's
casing is obsidian with no knob. An iron pickaxe does not mine obsidian. Therefore every DTC board the
studio builds is unwinnable — a striking finding, filed, written into a review.

It is false. `B81` has landed. `DestroyKitPairing.RequiredPickaxe` takes the hardest material any
destroyable or core on the map needs and upgrades the tier — cores force diamond outright —
and `TeamsGenerator.GenerateKits` calls it. Quillon Foundry's `map.xml` carries a **diamond pickaxe**
because it has a core; Quillon Barrow's carries an **iron** one because its only goal is end stone. The
pairing is exact.

I caught it because I went to the source for a line number to cite. That is the whole lesson, and it is
the same lesson both previous reports end on: *the information was in reach and I reasoned from prose
instead*. The specific trap here is the one `CLAUDE.md` names — "a task id in a document is a promise to
come back", and citing `B81` as a gap became false the moment it shipped. **A stale gap claim is more
dangerous than a stale feature claim**, because it reads as a warning and warnings do not get checked.

Downstream of the same stale paragraph: I chose `ender stone` for both destroyables specifically so an
iron pickaxe could break them. That is a legitimate choice and the maps are fine, but the *reason* was
wrong — obsidian would have upgraded the kit by itself.

**I assumed "no build zone" meant "no bridging".** `approaches.md` says a void gap with no build region
over it is permanent. It is not, if the map declares no build area at all:
`BuildGenerator.Apply` returns early when `Build.Areas` is empty (`BuildGenerator.cs:35`), so
`not-build-area` and the `block=no-void` rule are never written, and PGM then permits building anywhere —
void included. Quillon Barrow's first export had no such rule and its channel was bridgeable from the first
tick, which is the exact opposite of the design. Verified by reading the emitted `map.xml`, not by
reasoning: there was no `<apply block="no-void">` element in it. The remedy is to declare a zone somewhere
harmless — I put a 90 × 10 build zone over the mid causeway, which is land end to end and changes nothing
except switching the void rule on. Both destroy maps needed the same trick.

**I mis-sized a `sink`.** `sink` measures from the median ground under the footprint, so the foundry's
tail race at `base_height 4, skirt 1` came out with its floor at **y9** against a field top of **y15** — a
six-block one-way drop nobody could climb out of, rather than the covered route it was drawn to be. At
`base_height 3, skirt 2` it reads y11 with ramped ends. Both numbers came from probing `(−30, −20)`;
neither is visible in any plan view, and the first build looked correct in the top-down and the heightmap.

**I read the top-down's void holes as bigger than they are.** I measured the channel off the picture at
about 50 blocks deep and was about to redesign around it; `--section` reported **43 void columns** along
`x = 0` across both channels, which is the 22 + 22 I authored. The picture answers *whether*, and I asked
it *how much*.

---

## 3. What worked first time

This list is longer than the two above, and it is the part that says which of the system to trust.

**The six-call loop, exactly as `plan.md` documents it.** `POST /plan` → `PUT …/plan` → `POST /plan/compile`
→ `PUT …/sketch` → `POST …/sketch/finish` → `PUT …/intent/from-plan` → `GET …/export`. Three maps, no
surprises, sub-second exports. The one deviation I made — authoring the whole `SketchLayout` by hand and
`PUT`ting it verbatim instead of merging a finish into the compiled layout — is documented behaviour
(`PUT /map/{slug}/sketch` is a verbatim replace) and it removed the entire class of problem the previous
run built `world-build.cs` for. Compiled tiers never have to be addressed by the height they stand at,
because they are thrown away. Role-tagged shapes are skipped by the rasterizer, so nothing of the plan's
geometry needs carrying across.

**A goal with an empty `piece`.** `{"piece": "", "at": [0, -10]}` → anchor `(0, 12, −50)`, resolved to
`y16..18` against the terrain the rasterizer actually built. Same for the core at `(−25, −37.5)` and the
destroyable at `(55, −20)` riding an authored `raise` polygon that has no plan piece anywhere near it.
This is the single most valuable thing that landed before this run: the landform is authored once, in the
layout, where it belongs.

**`height_mode` and `skirt`, in every combination I tried.** `raise` with per-vertex `anchor_heights` and
`skirt 3` gave the barrow's crag a tilted crest and a climbable face; `level` with
`anchor_heights [12,12,23,23]` gave its ramp a clean tilted plane; `sink` gave two salt basins and a
brick-lined tail race. `relief.md` says the word is orthogonal to the height function and it is.

**`hold` against `exclude`, and the difference is visible.** Quillon Foundry uses both on one board — the
casting floor `hold` so the ash field ramps up to meet it, the yard and stage `exclude` so they meet the
tier below at a face. `05-section-core.png` shows the two joins side by side.

**The refusals are worth their weight.** `POST /plan/evaluate` answered a hard `STRUCT`/`WX3` term —
"marker parity differs between axes; the pad is always square" — before I had a map row, and the compile's
422 repeated it with the same sentence. The overlapping-piece refusal named both pieces and the delta.
Every refusal I hit told me what to change.

**Nesting.** A `cell` inside the top layer of a `layered` over two solids, with `wallRun` and
`wallDiagonal` on the risers, resolved without complaint on all sixteen themes. Turning the **rim off** on
grown ground and on for built tiers is the one theme decision that changed how the boards read most, and
it is one boolean.

**The defence wall, which nothing generated has ever asked for.** One `walls` entry naming
`lane-w`/`hub` produced a two-thick bedrock barrier at `x −65..−55, z −56..−54`, `topY 14` — three courses
proud of the attack side, one proud of the lane behind it, with a cobweb course on top. `topY` is derived
from the *approach* piece's surface, which is why it is three proud where it matters. That is the corpus
behaviour `match-flow.md` §6.2 measures, and it came out of one line of JSON.

**The section renderer.** `--column` and `--section` answered every question a plan view cannot: the
layer stacks, the goal floats, the bedrock platform under a destroyable, the trench depth, the missing
houses, the void count. The previous report asked for this first; it is the difference between checking
and guessing, and it is now there.

**Water lanes over void only.** Two flank lanes at `x ±(45..75), z −10..10` compiled into
`waterLanes.rects` and stayed out of the build intent, exactly as documented.

---

## 4. Open gameplay questions, decided without an oracle

Each of these is a decision I made, not a fact I derived. `approaches.md` settles the frame and not the
number.

**"A void channel twenty blocks in front" — twenty of what?** The brief's phrase can mean twenty blocks
in front of the monument or twenty blocks across. `approaches.md` gives "roughly twenty blocks, though
that number is illustrative" for the width. I made both true: the near lip sits at `z = −30` against a
goal at `z = −50` (twenty in front) and the gap is 22 blocks across at `x = 0`. If only one was meant, the
map still satisfies it.

**I made every channel permanent rather than bridgeable.** `approaches.md` says both are legitimate and
that a channel cut without deciding which has had half of it decided by accident. A channel that can be
bridged in minute one does not make anyone go around, so on both destroy boards the only build area is a
strip of the mid that is land end to end. **Open question:** whether a destroy board's forward channel
should instead be build-zoned so that bridging it is a visible, expensive commitment rather than an
impossibility.

**A core with `leak` above `float`.** Defaults are `float 6, leak 5`, which is a dig depth of zero. I set
`float 6, leak 9` so `digDepth` is 3 — attackers must break the casing *and* open the ground under it.
Nothing says what the right number is. Three felt like a real task and not a chore; I have no basis for
preferring it to two or five.

**Two goals of different kinds, one low and one high.** `approaches.md` says several goals are placed
against each other rather than scattered and that the spacing decides whether the defence is one line or
three. I put the foundry's core deep in the works and its destroyable out on a ridge thirty blocks
forward, so the two are unlike in depth, in height and in what breaks them. **Open question:** whether a
core and a destroyable on one board should be at comparable difficulty, or whether the cheap forward goal
and the expensive back one is the point.

**One walled lane and one open lane on the capture board.** `approaches.md` says the approaches should
differ; `match-flow.md` says the wall is where the defence forms. So one wool is behind a prepared bedrock
line and the other is not. **Open question:** whether asymmetry between a team's *own* two objectives is
good design or just an unfair wool.

**The forest's density.** 21 trees over roughly 40 × 50 blocks, in two stands either side of a four-block
clear run. `approaches.md` says density is a design decision and that the measure that would settle it —
what share of ground stands under a leaf — is `B96` and unbuilt. I chose "walkable woodland, sightlines
broken at about fifteen blocks" by eye off the top-down.

**Whether a full-width bedrock wall should worry me.** It takes the traversability read from 0 isolated to
some isolated, as the previous run documented. My saltworks reports 0 isolated with the wall in, because
the lane is ten wide and the wall spans it — the wool markers still connect through the room's own
interior. I did not tune anything to make that number look good.

---

## 5. Findings, with coordinates

| # | Finding | Where to check it | Verdict |
|---|---|---|---|
| 1 | `<gamemode>ctw</gamemode>` + "Capture the enemies' wools!" on a destroy map | `maps/quillon-foundry/map.xml` lines 4–5, beside `<cores>` and `<destroyables>` | missing from the system |
| 2 | No build area ⇒ no `block=no-void` rule at all ⇒ every void is bridgeable | `BuildGenerator.cs:35`; reproduce by compiling a plan with `zones: []` | missing (and it inverts `approaches.md`'s claim) |
| 3 | A path's band claims ground; a building touching it is dropped, both orbit images, silently | `Decorator.cs:124` and `:325`; `h2`/`h3`/`h6` at `z −82..−77` against a street band reaching `z −77` | missing (no reading reports it) |
| 4 | `kind` must be a prop's first JSON key; the documented example is `id`-first | `docs/tools/sketch.md` §Dressing example → `GET /map/{slug}/export` 500 | doc + serializer |
| 5 | `capabilities.md` says the kit is not paired to the goal material; it is | `DestroyKitPairing.RequiredPickaxe`; `maps/quillon-foundry/map.xml:17` = diamond pickaxe, `maps/quillon-barrow/map.xml:17` = iron | stale doc — **my wrong claim, retracted** |
| 6 | A 5×5 bedrock plate is buried one course under every destroyable | `(−2..2, 10, −52..−48)` in `quillon-barrow`; `StructureStamper.PlatformSize`, called at `SketchWorldBuilder.cs:267` | undocumented outside `rules.md`; correct and useful |
| 7 | An absolutely-placed goal does not appear in `GET /plans/{id}/png` | `maps/quillon-barrow/renders/01-plan.png` — nothing at `(0, −50)` | out of reach (canvas parity) |
| 8 | Excluded tiers leave the relief field entirely | `quillon-saltworks` readback: 3 169 cells for an ~11 000-cell island | mechanism documented, consequence not |
| 9 | Terrain painted in a built-looking block reads orange in `--topdown` | the whole salt pan and both village terraces | known limit, correctly warned about in the brief |
| 10 | Water props fragment the traversability component count | `quillon-barrow`: 8 components with two pools, 0 isolated | known; the isolated count is the one to read |

---

## 6. One process note

Every map was looked at between stages: plan render → relief readback → build → top-down → heightmap →
section → column probe → buildings census, and back round. Three of the ten findings above only exist
because of the two vertical read-backs, and two of them (the dropped houses, the six-deep trench) were
invisible in every plan view I had already drawn. The rule in `capabilities.md` — *a stage that produced
something should be looked at before the next stage consumes it* — is right, and the corollary this run
adds is that **a plan view is not a stage image for anything with a height**.
