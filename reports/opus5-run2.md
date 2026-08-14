# B120, run 2 — Opus 5

Two maps, authored by driving `http://localhost:5189/api` directly. Nothing in `pgm-studio` was modified —
it was checked out, run, and read. The only script involved is a 60-line poster (`tools/drive.ps1`) and a
per-map assembler that substitutes a named `HouseStyle` into the houses that name one and concatenates the
authored JSON. Neither computes a coordinate, a placement or a validation.

| Map | Slug | Kind | Size | Goals | Shapes | Themes | Props | What it is |
|---|---|---|---|---|---|---|---|---|
| 1 | `marlstone-steps` | CTW | 152 × 204 | 2 wools a team | 16 | 9 | 57 | a white marl hillside in five terraces, cut by two void ravines |
| 2 | `basalt-reach` | DTM + DTC | 150 × 204 | 1 destroyable + 1 core a team | 11 | 5 | 47 | a black basalt platform, sea stacks, a channel cut with a `subtract` |

**They are built the opposite way round on purpose.** Marlstone is five flat tiers with the relief reaching
one of them (4 294 cells of the solve on a ~19 000-cell board); Basalt is one relief-solved platform with
erected shapes standing out of it (7 184 cells). Every level change on Marlstone above the base tier is a
shape — four `level` ramps, two `sink` basins, a `raise` outcrop, a tilted shelf. That contrast is the point:
the two ways of making ground behave differently and the pair is meant to be read together.

---

## 1. This run's first job: checking the last run's claims

Three models authored nine boards here overnight and their reports disagree with each other. The disagreements
are checkable, and checking them was worth more than a third opinion.

### Claims that were wrong when filed

**Haiku: "per-shape themed materials — missing from the system."** False, and the report's own evidence
contradicts it: it observed that a *compiled* shape's `theme` is not writable and concluded the capability
does not exist. `SketchShape.Theme` is an ordinary field of a hand-authored layout, and the intended route is
to `PUT` your own layout rather than to edit the compiled one. Marlstone carries nine themes over sixteen
shapes and Basalt five over eleven. Not a gap.

**Haiku: "relief marks with area scope — missing from the system."** False. `{"kind": "area", "h": N, "ring":
[...]}` is a relief mark scoped to a polygon, and `point` marks take `at` and `r`. Both my boards use an
`area` mark to hold the mid flat where the two halves meet, and `point` marks for local swells. The previous
Opus run used one too. The report searched the relief block for a *bounding rect* field and, not finding one,
filed the capability as absent.

**Sonnet: "every enum-valued field must be the C# member's literal name; camelCase silently drops the whole
props list."** Not supported by the evidence available in this repository. The previous Opus run's specs are
camelCase throughout (`"form": "template"`, `"stairLattice"`, `"negZ"`, `"worn"`) and its 47 props placed and
were column-probed. Both my maps are camelCase throughout — 104 props between them — and everything placed.
Sonnet's own diagnosis rests on a 53-prop village that shipped zero props at a `200`, which is a real and
serious observation; the attribution is what looks wrong. The likelier cause is the fault the Opus run
documented independently and I reproduced below: **a path claims ground and every building touching it is
dropped, silently.** Sonnet's village was a street with houses along it, which is exactly the arrangement that
trips it.

That distinction matters more than the correction. A wrong *cause* attached to a real *symptom* is the most
durable kind of error, because the symptom keeps confirming it.

**Sonnet: "a destroy goal's material and the map's kit are not automatically paired."** Stale — it was quoting
`capabilities.md`, which the Opus run had already caught and retracted. `DestroyKitPairing.RequiredPickaxe`
upgrades the tier to the hardest material any goal needs. Basalt Reach carries obsidian on both goals and its
`map.xml` ships a **diamond pickaxe**. I chose obsidian specifically to test this rather than designing around
the claim.

### Gaps that were real when filed and have since been closed

Four of the previous run's findings are fixed in the code as it stands today. I exercised each rather than
reading the commit:

| Filed as | Now | Evidence |
|---|---|---|
| a destroy map cannot say it is a destroy map (`<gamemode>ctw</gamemode>` on a wool-less board) | **fixed** | `basalt-reach/map.xml`: `<gamemode>dtm dtc</gamemode>`, *"Destroy the enemy's monuments and leak the enemy's cores!"* |
| no build area ⇒ no `block=no-void` rule at all ⇒ every void bridgeable | **fixed** (`B132`) | `basalt-reach` declares **zero** build areas and gets `<apply block-place="deny(void)" region="void-enforcement-area"/>` |
| a prop's `kind` must be the object's first JSON key or export 500s | **fixed** | `AllowOutOfOrderMetadataProperties` on `DressingJson.Options`; my props are `kind`-last throughout and export cleanly |
| a dressing document that fails to parse silently becomes zero props | **fixed** (`B130`) | `DressingParseException` carries rule `DR-DOC` and names the prop and the field |
| terrain painted in a built-looking block reads orange in `--topdown` | **fixed** (`B133`) | the renderer prints `STRUCTURE READING: RECORDED PROVENANCE`; Marlstone's quartz and stone-brick terraces read as **ground** |

### Gaps that are still live

**A path claims ground and a building touching it is dropped, silently.** Reproduced on `basalt-reach`, four
of five houses, with coordinates in §5. Three commits landed *during* this run about what a *building* claims
— its eaves, its roof ring, two buildings that touch — and none of them touch the path side.

**A spawn shape's interior is not painted by its theme.** `(0, 85)` on Marlstone reads raw `Stone` under the
wool monument, on a board whose crest theme is quartz. Fourth independent report.

---

## 2. What I could not say

### Missing from the system

**A shape's height and its paint resolve an overlap by different rules, and the documented technique puts them
in conflict.** Height takes *the taller* add-shape (`MergeCell`); paint takes *the smallest-area* shape
(`ShapeScopeOwners`, "the most specific scope"). The documented way to give a tier an organic edge is to let
the tier below run **under** it — and where that lower tier is the smaller shape, it keeps the paint over
ground the upper tier owns. Measured on Marlstone at `x = 0`: `(0, 58)` stands at **y21**, the shelf's height,
painted in the orchard's grass-over-sandstone, nine blocks deep across the shelf's own surface. There is no
field that scopes paint to the visible surface rather than to a shape, and nothing warns. Reduced to a two-to-
four-block seam by hand; not removable while the underlap is what stops the join opening a hole.

**A hand-authored shape needs `type`, `operation` and `floor`, and omitting them fails silently at every
stage.** `SketchShape.Type` defaults to `""` and `RingOf` returns `[]` for an unknown type, so the shape
rasterizes to no cells. `PUT …/sketch` answered `{"ok": true}`; `GET …/sketch` returned all sixteen shapes and
the relief intact; `POST …/sketch/relief/read` answered **200 with `{"islands": []}`**. That empty array is
the only symptom the system offers, and it points at the relief rather than at the geometry. Missing: any
refusal, or a required-field validation, on a document whose whole purpose is to describe geometry.

**A prop over void is skipped and nothing counts it out.** A tree authored where no ground stands simply does
not appear — no refusal, no warning. And `--topdown --layer foliage --dressing` reports the count from the
**document**, so it said "34 tree(s)" whether or not one of them stood anywhere. Looked for: a placement
report, a non-zero-crown filter, anything in the export gate. `OB19` refuses a prop inside a goal's clearance
but nothing refuses a prop over nothing.

**The objective line counts objectives across both teams.** One destroyable per team gives
`intent.Destroyables.Count == 2` and therefore "monument**s**". On a board where each team destroys one
monument the line overstates. `MetaGenerator.Objective` reads the flat list; there is no per-team divisor.

### Out of reach from where I was standing

**Standalone void enforcement, from the plan.** `BuildIntent.VoidEnforcement` is exactly the capability a
permanent channel wants, and `PlanModel` has no field for it while `PlanCompiler` never emits one — a compiled
intent always carries `"voidEnforcement": null`. It is one line to patch into the intent before
`PUT …/intent/from-plan`, which is what I did, so the capability is reachable; it is not reachable from the
document that states the board. Looked for: `zones[].kind`, `globals`, `PlanZoneKinds`.

**A stair, a ledge or anything that joins two tiers as a prop.** I wanted to connect five terraces and there
is no prop for it, so the joins are `level` shapes with `anchor_heights` — which works well and is arguably
the better answer, since a ramp is ground rather than scenery. Recording it because "there is no stair" was
my first conclusion and it was the wrong frame, not a gap.

**`species: "dark_oak"` builds a tree of oak blocks.** The wood on Basalt reads `17:12` / `18:4` — oak log and
oak leaves — under a nine-block trunk and a broad crown, so the species is selecting the right *template* and
the wrong *material*. I did not read `docs/world-export/tree-corpus.md` to find out whether that is intended,
so this is a measurement rather than a finding.

**The library.** I never called `POST /styles`, `/themes` or `/room-styles`. Every theme and house style on
both maps is written into the layout document directly. That is a limit of my route, not a claim about those
endpoints.

---

## 3. What I got wrong

**I probed the Bézier at the vertex and concluded `controls` did nothing.** The vertex is a fixed point of the
curve — the extremum sits *between* vertices. Two probe rounds went into "the field is ignored" before I
computed the curve at `t = 0.5` and looked there, where it is unambiguous. The correct method, and the one
that settles it in one shot, is an A/B against a build of the same vertices with `controls` removed:

| column | no `controls` | with `controls` |
|---|---|---|
| `(73, 36)` | void | **solid** |
| `(74, 36)` | void | **solid** |
| `(52, 89)` | void | **solid** |
| `(52, 82)` — *the vertex* | void | void |

**I read "6 roof components" as "eighteen houses are missing", and then explained it away half-correctly.**
All twenty-four houses were standing and had been visible in the top-down I had already rendered. My first
account blamed the `--roof` material filter alone — brick *slabs* (44:4) rather than brick blocks (45) — which
is one of three reasons and not the main one. On being pushed I went back and measured, and the tool is
failing for compounding reasons, all of them because it is built to read worlds the studio did **not** build:

1. the `--roof` filter is exact, and misses a slab-surfaced roof with a quartz-pillar verge;
2. `IsTerrain` includes `1, 4, 13, 24, 98, 155, 159, 172` — so a cottage roofed in `159:14` is classified as
   *ground*, its clearance over terrain is nil, and it is dropped by the `RoofHigh − GroundY` gate.
   `--roof 159:14` on Marlstone returns **0 components**;
3. `CornerStems` requires a vertical **log** at the footprint corners, and Marlstone's styles use
   quartz-pillar posts — so every candidate reads `corners: 0` and is labelled "hangs, unframed".

Relaxing `--min-area`, `--min-side` and `--min-height` changed nothing. Opus run 1's census worked because
`quillon-barrow`'s houses use `post: 17:1` (oak log) and spruce-plank roofs, which satisfy both (2) and (3).

**The instrument I should have used exists and I did not know about it.** `--topdown --layer structure` reads
`region/provenance.json`, which the export writes and which `B139` has just taught to record *which prop*
made each claim. Marlstone's owners list is the census, stated rather than inferred:
`house 24, spawn 2, redstoneline 4, roomfloor 4, wool 4, wall 2` — `h1`…`h12`, twice each. The lesson is not
"read the picture as well as the number"; it is that **a world this studio built carries a record of what it
built, and guessing from blocks is the fallback for worlds that do not.**

**My first diagnosis of the empty relief was the relief block.** It was the shapes. What broke the loop was
posting a *known-good* layout to the same endpoint: it answered normally, which moved the fault from the
endpoint to my document in one call. That step is cheap and I should have taken it first.

**I drew the paths and the buildings at the same time on Basalt.** `approaches.md` says circulation is decided
before dressing and I had written that down; I then authored eleven paths and five houses in one pass and four
of the houses landed on path bands. The rule is not "draw the streets first in the file" — it is that the
streets' *claimed ground* is a constraint the buildings are placed against, and you cannot satisfy a
constraint you have not computed yet.

---

## 4. What worked first time

- **The six-call loop**, unchanged from the previous run's account. Two maps, no surprises.
- **`POST /plan/evaluate` before anything exists.** It named a hard `BZ6` (a build band two cells from a wool
  room) plus three soft terms on Marlstone's first draft, with no map row and no compile. Score went
  1 008 → 3.7 across two edits and **both edits improved the board** — the second was cutting the two ravines,
  which is now the board's main idea. This is the cheapest good advice in the system.
- **`height_mode: "level"` + `anchor_heights` as a ramp.** Four on Marlstone, three on Basalt, all correct on
  the first build. Measured down Marlstone's `ramp-d`: y20 → y22 → y23 → y25 across z66 → z80.
- **`subtract` as the instrument for a hole.** Two organic channels on Basalt, `0 solid blocks` at any height,
  with Bézier controls on the long edges so they read as water-cut.
- **A goal with an empty `piece` and an absolute `at`.** Both Basalt goals; the landform under the monument is
  authored once, as a `raise` polygon, and the height resolved from the terrain actually built.
- **A core.** `float 5, leak 8` → `digDepth 3`, obsidian shell over lava at y18–20, sunk in a `sink` yard.
- **Deep nesting.** A `cell` inside the top layer of a `layered` over two solids, with `wallRun` and
  `wallDiagonal` risers, across fourteen themes. No arity trouble.
- **Turning the rim off on grown ground and on for built tiers.** One boolean, and it is still the single
  theme decision that changes how a board reads most.
- **The refusals name what to change.** `sketch/finish` rejected a malformed `layout.islands` with the
  property path and the line number, which found a PowerShell serialization bug in one read.

---

## 5. Findings, with coordinates

| # | Finding | Where to check it | Verdict |
|---|---|---|---|
| 1 | A shape without `type`/`operation`/`floor` rasterizes to nothing; every stage reports success and `relief/read` answers `{"islands": []}` | reproduce by removing `"type"` from any shape in `specs/marlstone-steps/marlstone-steps.shapes.json` | missing (no validation) |
| 2 | Height takes the taller shape, paint takes the smaller — the documented underlap paints a band of the wrong material | `marlstone-steps` `(0, 58)`: y21 (shelf) painted in the orchard palette; `(0, 70)` and `(0, 50)` both correct | missing (rules conflict, undocumented) |
| 3 | A path's band claims ground; a building touching it is dropped, both orbit images, silently | `basalt-reach` first build: `w2 (−34…−25, 64…71)`, `w3 (−22…−14, 64…73)`, `w4 (−11…−3, 64…70)`, `w5 (0…7, 64…72)` | **still live** (previously filed) |
| 4 | A prop over void is skipped; the foliage read-back counts the document, not the world | `s1` at `(−46, 74)` — 0 solid blocks, still counted in "34 tree(s)" | missing |
| 5 | Bézier `controls` are absolute, keyed by vertex index; `out` bends the next edge, `in` the previous | `(74, 36)` and `(52, 89)` solid with controls, void without | works; semantics undocumented |
| 6 | `voidEnforcement` has no plan field; a compiled intent is always `null` | `specs/basalt-reach/basalt-reach.intent.json` vs `.plan.json` | out of reach from the plan |
| 7 | `G8 fill-ratio` cannot see a layout `subtract` | `basalt-reach` evaluates 0.811 (near-solid); the built board has two large voids | measurement scope, worth knowing |
| 8 | The objective line pluralizes across both teams | `basalt-reach/map.xml`: "monuments" for one destroyable per team | cosmetic |
| 9 | `species: "dark_oak"` builds from oak blocks | `basalt-reach` `(−60, 12)`: `17:12` log, `18:4` leaves | measured, not diagnosed |
| 10 | A spawn shape's interior is unpainted | `marlstone-steps` `(0, 85)`: raw `Stone` under the monument | still live (previously filed) |
| 11 | `--buildings` cannot see a town built from stone and quartz — exact `--roof` match, `IsTerrain` swallowing `159`/`155`/`98`, and `CornerStems` wanting a log | Marlstone: 24 houses standing; `--roof 45:0` → 6 components (all spawn), `--roof 159:14` → 0 | tool scope, not a defect |
| 12 | A provenance sidecar written by an earlier revision **throws** instead of falling back | `--topdown --layer structure` exits 255 with `JsonException` on a world built before `B139` changed the sidecar to `{owners, runs}`; `WorldProvenanceFile.TryRead` guards `File.Exists` but not the deserialize | missing (the doc comment promises the fallback) |

---

## 6. Open gameplay questions, decided without an oracle

**Is a five-tier board too vertical for CTW?** Marlstone falls sixteen blocks from spawn to mid over ninety
blocks of run, in four faces of three to four blocks. I added four ramps because a board that can only be
descended is not one a defence can rotate on. Whether four faces is right, or two, or six, a column probe
cannot say.

**Should a team's two wools be at different difficulties?** I made Marlstone's deliberately unequal — one low,
near and quick; one high, far and slow — reading `approaches.md`'s "the approaches should differ" as extending
to the objectives. The evaluator disagrees mildly: `WL9 spawn-wool-ratio` 1.5 against an authored band of
`[1, 1.231]`, i.e. the corpus keeps a team's wools comparable. Left as authored.

**Are 10-block ravines wide enough to matter?** They cannot be jumped and cost blocks to bridge, but
`approaches.md`'s illustrative figure for a void a player must go around is twenty. Mine are half that because
the hillside they cut has to stay crossable.

**How unequal may two ways round a channel be?** Basalt's isthmuses are 23 blocks west and 37 east, and under
`rot_180` each team's cheap route is the other's expensive one. Designed asymmetry or one team's advantage is
a question about play.

**Is `digDepth 3` a task or a chore?** `float 5, leak 8`. The previous run chose the same number for the same
reason — it feels like real work — and neither of us can say why not two or five. Two runs agreeing on a
number neither can justify is worth flagging as *not* corroboration.

---

## 7. One process note

The rule that paid this run was **posting a known-good document to a failing endpoint**. Twice — once for the
empty relief, once for the malformed islands array — the fault was in my document and the symptom pointed
somewhere else. One call against a layout from `specs/quillon-barrow/` moved the question from "is this
endpoint broken" to "what is different about mine", and the diff was then mechanical. Nine boards' worth of
prior work sitting in this repository is a test fixture, and it is the fastest one available.

The rule that cost this run was the one about pictures. `--buildings` gave me a number that disagreed with a
top-down I had already rendered and I believed the number. The brief's instruction is to look at the picture
and then say what you see in it; the corollary this run adds is that when a measurement and an image disagree,
the image is not automatically wrong — find out which one is answering the question you asked.
