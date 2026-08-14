# Sonnet — run 2

Three maps, authored entirely by driving `http://localhost:7894/api` directly — the documented six-call
loop (`POST /plan` → `PUT .../plan` → `POST /plan/compile` → `PUT .../sketch` → `POST .../sketch/finish` →
`PUT .../intent/from-plan` → `GET .../export`) — never through `tools/mapgen`, never from a composed board.
No source change anywhere in `pgm-studio`; no new capability anywhere in `pgm-studio-mapgen/tools`. The only
scripts I wrote live in my own scratchpad and do exactly one thing each: assemble a `PlanModel` /
`SketchLayout` / `MapIntent` I had already designed by hand into JSON and `curl` it at a documented
endpoint. None of them compute a placement, a clearance or a validation — every coordinate, every theme
bucket, every prop position is a number I chose.

| Map | Slug | Kind | Size | Goals | Props | What it is |
|---|---|---|---|---|---|---|
| 1 — canonical brief | `corvid-hollow` | DTM | 142×180 | 1 destroyable a team | 36 | a moorland hollow: monument in the open, a forest closing the west, a tilted hill east, a village behind, a 20-block moat forcing the flanks |
| 2 — mine, CTW | `sable-marsh` | CTW | 200×192 | 2 wools a team | 23 | a reed marsh around a ring hub with a pool in its hole; one wool behind a stockade wall, the other open scrub |
| 3 — mine, destroy | `ashfall-scar` | DTC + DTM | 250×190 | 1 core + 1 destroyable a team | 31 | a volcanic ash field: a forward destroyable on a relief-pushed mound, a back core in a relief-carved crater, forest west, a buildable ford east |

Every map has its own theme set (five per board, fifteen total) and its own room styles (one to three per
board) written for that map — none shared, none reused across boards. Full per-map detail, coordinates and
techniques are in `review/corvid-hollow.md`, `review/sable-marsh.md`, `review/ashfall-scar.md`; this
report is the run-level account.

---

## What run 1 found, retested here

Four things the brief named as landed since run 1. I checked all four directly rather than taking the
brief's word for them, because that is exactly the failure mode this run exists to avoid repeating.

**A destroy map now states its own gamemode.** `corvid-hollow`'s `map.xml`: `<gamemode>dtm</gamemode>`,
`<objective>Destroy the enemy's monuments!</objective>`. `ashfall-scar`, which carries both a core and a
destroyable: `<gamemode>dtm dtc</gamemode>`, `<objective>Destroy the enemy's monuments and leak the
enemy's cores!</objective>`. `sable-marsh` (CTW): `<gamemode>ctw</gamemode>`,
`<objective>Capture the enemies' wools!</objective>`. Confirmed on all three of my own maps rather than
assumed from the brief's description.

**A default-obsidian destroyable exports clean, and the kit upgrades to match it.**
`corvid-hollow.plan.json`'s destroyable names no `materials` field at all (the default). Export: `200`.
`corvid-hollow/map.xml`'s spawn kit carries `<item slot="2" material="diamond pickaxe">` — `DestroyKitPairing`
read the obsidian goal and upgraded the corpus-default iron to diamond with no authoring on my part. I did
not have to choose `ender stone` the way run 1's Sonnet report did to route around a refusal that no longer
exists.

**`build.voidEnforcement` fires without a declared build area, and I used it for exactly that case.**
`corvid-hollow` declares no `build.areas` at all — nothing should be bridgeable anywhere on the board — so I
set `voidEnforcement: { exclusions: [] }` explicitly. The exported XML carries
`<apply block-place="deny(void)" region="void-enforcement-area">` over `<everywhere>`, with no
`not-build-area` complement in sight, because there is no build area to take a complement of. This is a
real capability I would not have reached for on the old behaviour, where an undeclared build area meant an
*unenforced* void by accident (`opus-run1.md` finding 2).

**A goal needs no plan piece under it.** Every destroyable and every core on all three maps is placed
`{"piece": "", "at": [...]}` — an absolute board position — riding ground that is an ordinary authored
shape (`corvid-hollow`'s `plaza`, `ashfall-scar`'s `yard`) rather than a piece manufactured to carry a
marker. Confirmed by the compiled intent's `anchor` fields resolving correctly and by every goal marker
appearing exactly where placed in the topdown and section renders across all three maps.

**A malformed dressing document now refuses by name.** I did not have to construct a synthetic test for
this — I hit it for real, mid-build, on `corvid-hollow`. `POST .../sketch/finish` and `PUT .../sketch`
both accepted a room style whose `gableWindows.form` I had written as `"single"`, which is not a
`WindowForm` member; the export answered `422` with
`{"error": "dressing document invalid", "rule": "DR-DOC", "message": "prop 'd2' (#1): field
'style.gableWindows.form' could not be read — expected PgmStudio.Minecraft.WindowForm.", ...}`. That is
exactly the fix the brief describes: named, by prop and field, rather than a `500` (run 1's finding) or a
silently empty `props` list (run 1's other finding). I fixed the field and moved on in under a minute. I
also re-tested run 1 Sonnet's specific enum-casing claim ("every enum must be the PascalCase C# member
name, not camelCase") on a disposable probe map (`enum-probe`, not part of the deliverable): a tree prop
with `"form": "template", "species": "oak"` and a boulder with `"form": "cairn"` — both lower camelCase, as
`docs/tools/sketch.md` shows — exported clean and both stamped correctly (`--column` confirmed a real oak
log-and-leaf column and mossy-cobblestone boulder lobes at the placed coordinates). I could not reproduce
run 1's PascalCase requirement; see the *mistaken* entry below for why I think that finding was itself
confounded by the same-run kind-ordering bug rather than a second real fault.

---

## What I could not say

### Missing from the system

I did not find one. Every wall I hit this run had a mechanism behind it that a closer reading or an extra
probe resolved, and I want to be honest that this is partly a function of what I chose to build rather than
proof the system has no gaps left — see *out of reach*, below, for the things I deliberately did not
attempt.

### Mistaken — the system does this, I read the field wrong or didn't look

These are the most valuable entries in this report and I am listing them in full rather than folding them
into the per-map reviews, because the pattern across five of them is the same one `AGENT-REPORT-2.md`
already named: *I had the information and did not apply it before authoring the next thing.*

**1. `bedrock.relative: true` means "keep only the top `value` blocks as terrain," not "a thin bedrock
floor `value` blocks thick."**
*Reported*: I set `{"relative": true, "value": 1}` on all five of `corvid-hollow`'s themes, reading it as
"one relative block of bedrock" — a thin floor course, the way I'd read the absolute case.
*Checked*: `Minecraft/TerrainTheme.cs`, `BedrockSpec.TerrainRelative(int terrainDepth)`: "Bedrock takes
everything **under** the top `terrainDepth` painted blocks." The word "relative" describes what is being
measured (terrain depth from the top), not what bedrock's own thickness is relative to.
*Verdict*: **mistaken**. Documented in the type's own docstring; I hadn't read the source before authoring
the field, and the surface-only render (`--topdown`, `--heightmap`) cannot show it either way, since both
readings paint the same top block. Caught with `--column` at `(45, -30)`: eighteen courses of solid bedrock
under one grass block, before the fix; a proper stone fill with a one-block bedrock floor after setting
`relative: false`.

**2. A `controls` entry naming both `out` and `in` on the same vertex bends the two edges meeting there,
not one edge twice.**
*Reported*: I wanted to bulge one outer edge of a shape (the hill's east side, the forest's west side on
`corvid-hollow`) and copied `sketch.md`'s worked example, which puts both handles on one vertex — because
in that example the intent *is* to round a corner, which needs both.
*Checked*: `sketch.md`'s own text: `"out"` bends the edge leaving a vertex, `"in"` the edge arriving at
it — for one *edge*, the `out` belongs to its start vertex and the matching `in` to its end vertex, two
different indices. I had put both on the start vertex, which silently also bent the *other* edge sharing
that vertex — on `corvid-hollow`'s hill, that other edge was the seam shared with the village, dragged
thirty-odd blocks sideways until the polygon self-intersected.
*Verdict*: **mistaken**. My own misreading of a documented example, not a gap in it — but worth stating
plainly because the failure mode is silent and total: the plan compiled clean, the sketch saved clean, the
export succeeded, and the only sign was two void columns, `(40, -40)` and `(60, -40)`, found by routinely
column-probing the hill's four corners rather than by any refusal. Fixed on `corvid-hollow` by splitting the
handles onto the edge's own two endpoints; applied correctly from the start on `sable-marsh` and
`ashfall-scar`.

**3. `height_mode: raise`/`sink` reads `anchor_heights` as an offset **added to** the median pre-erection
ground, not as the shape's final absolute height.**
*Reported*: I wrote `anchor_heights: [12, 9, 9, 18]` on `corvid-hollow`'s hill expecting a final height of
9–18 across the shape, the way `level` mode's absolute anchors work.
*Checked*: `SketchRasterizer.Erect`'s own comment: `raise`/`sink` are "read at the **median** of the ground
the shape covers," and `Stated(x, z) = datum + rise * max(1, round(surface(x, z)))` — the anchor value is
added to that datum, not substituted for it. With a pre-erection ground of ≈9 under the hill, `[12, 9, 9,
18]` built a peak at **y27**, seven blocks over the y20 build cap — a player standing there cannot place a
block at all, which defeats the entire point of a hill someone is meant to bridge *from*.
*Verdict*: **mistaken**. The mechanism is documented in the source, not in `sketch.md` or `capabilities.md`
in a way I found before authoring; I hadn't read `SketchRasterizer.cs` itself. Caught by column-probing the
hill's own corners before calling it finished — `(35, -5)` read y25 before the fix, y16 after re-tuning the
anchors to `[4, 1, 1, 9]`.

**4. `skirt` blends toward "the ground just outside the outline," and where that outline meets void there
is nothing sensible to blend toward.**
*Reported*: I gave the hill `skirt: 3` for a soft, grown-looking edge, not expecting it to matter which
side of the shape the skirt was easing toward.
*Checked*: `SketchRasterizer.InwardDepth`'s comment: the skirt reads "the ground height just outside the
outline nearest it," sampled per cell. Where the nearest outside ground is void (the hill's west face
meets `corvid-hollow`'s moat), that sample has nothing real to offer and the blend pulled the whole edge
down — `(32, -2)`, right against the moat, read **y7** with `skirt: 3` against a peak of y16–18 elsewhere on
the same shape, twenty-odd blocks off from what the anchors alone would give.
*Verdict*: **mistaken**, and the least-documented of the five — I found no caveat about a skirt meeting
void anywhere in `sketch.md` or `relief.md`, only the mechanism itself once I went looking. Fixed with
`skirt: 0`, which reads as a legitimate design choice for this shape anyway (a sheer rock face facing the
moat, themed with a `wallDiagonal` strata pattern that suits exactly that).

**5. `PlanValidator`'s SP1 check (a wool must be reachable from a "frontline" piece without crossing a
spawn piece) derives "frontline" from declared build zones, not from role or adjacency.**
*Reported*: `sable-marsh`'s first plan had no `zones` entry — nothing on the board needed bridging, since
every piece I'd drawn touched its neighbour on solid ground — and the compile refused all four wools with
"only reachable through a spawn piece (SP1)." I first suspected my interface graph, since that is what the
message describes.
*Checked*: `POST /plan/inspect` showed every interface I expected, including `hub-ring`↔`approach-a`↔
`wool-a` with no spawn piece anywhere on that path. `PlanValidator.cs`'s `ComputeFrontline`
(`Derive/ContactGraph.cs`) builds the frontline set from `plan.BuildZones` alone — a piece with no declared
zone touching it is never a valid SP1 walk-start, however connected it is. Declaring one `zones` entry over
the hub cleared all eight findings at once.
*Verdict*: **mistaken**, sitting right at the boundary with *unreachable* — `plan.md`'s zones section
documents what a zone is *for* (the buildable mid, the gap-connectivity read) but not that a bare CTW board
with solid ground everywhere still needs one purely to satisfy this specific reachability check. I am
calling it mistaken rather than unreachable because the mechanism is genuinely in the source I could have
read (`ContactGraph.cs` is not hidden), and because the zone I needed to add is also the one the design
wants anyway — the mid band the late-game sky bridge is built across (`match-flow.md` §4.4–4.6) — so the
fix was not a workaround, it was the thing I had left out.

**Bonus, not a bug but worth recording next to the five above: `build.voidEnforcement` and `build.areas`
do not compose safely when both are set with `exclusions: []`.** On `ashfall-scar` I copied
`corvid-hollow`'s `voidEnforcement: { exclusions: [] }` onto a map that already declares a `build.areas`
rectangle over its ford, without re-deriving whether it still applied. It does not:
`ApplyVoidEnforcement` stamps `block-place=deny(void)` over `<everywhere>` with no knowledge of the
declared build area, so the ford would have been just as permanently unbridgeable as the rest of the void —
the opposite of the design, and *silently* so, since the intent JSON looks correct and the export succeeds.
Caught by reading the exported `map.xml` rather than trusting the document that produced it. I am not
calling this a fourth mistaken-field entry because `BuildIntent.VoidEnforcement`'s own docstring says the
two knobs are independent, in plain language — I read "independent" as "safe to combine" when it actually
means "the author must reconcile them." That distinction is worth a sentence in `capabilities.md` or
`plan.md`'s Zones section, since the failure is silent and the two knobs are natural to reach for together
on any destroy map that wants one crossable gap and the rest of its void permanent.

### Out of reach from where I was standing

I did not touch the shared **library** tables (`POST /styles`, `/themes`, `/room-styles`) — every theme
and room style across all three maps is written directly into the layout document. Two other agents were
authoring against the same running database at the same time (`quillon-*`, `sonnet-*` and `haiku-*` slugs
from run 1 are all still rows in `GET /api/maps` alongside a scattering of what look like other sessions'
smoke-test maps), and the library's tables are shared and unscoped by map. That is the same reasoning
run-1 Sonnet gave and I stand by it as a constraint of the exercise, not a claim about whether the library
endpoints work.

I did not author a water lane on any of the three maps. `sable-marsh` places a `water` **prop** (a pool in
the hub's hole) but never a `kind: "water-lane"` **zone** — the mechanism `docs/pgm/water-lanes.md` owns,
opening 45 minutes into a match. I chose the crossable-ford-versus-permanent-moat contrast between Maps 1
and 3 instead, and ran out of time to also demonstrate the lane. This is a scope choice, not a finding.

I did not attempt a multi-wing building (an L or a T footprint). `sketch.md`'s own Limits section already
names this as unreachable from a placed prop (`G172`'s open half — `HouseProp.Points` is exactly two
corners) and I had no reason to test it again; every building on all three maps is a single rectangle.

---

## What I got wrong, once I found out

Covered in full, with the code citation and the coordinate, in the *mistaken* section above — five findings
there, plus the `voidEnforcement`/`build.areas` interaction, are the complete list of things I authored
incorrectly and then caught before shipping. I am not repeating them here; that section *is* the "what I
got wrong" account, written the way the brief asks for it rather than as a separate summary that would
just restate the same five sentences with less evidence attached.

One thing worth adding that is not a field-level mistake: **I initially designed `sable-marsh`'s ring hub
as a plan-level buffer sitting entirely inside the ring piece's own rectangle**, which compiles clean and
does *nothing* — `plan.md` states outright that "a buffer over a generating piece is inert," and I had
read that sentence before drawing the piece, then drew it anyway, because I was thinking "draw the square,
poke a hole in it" rather than "a plan piece can only be a rectangle; the ring is a fact the sketch states,
not the plan." Caught by comparing the compiled shape list against what I'd drawn — the hub's own outline
had no notch — before ever building a world. This is the same shape of mistake as the five above: the rule
was in front of me and I applied a mental model instead of it.

---

## What worked first time

- **All three plans compiled clean on the corrected submission**, with the six-call loop exactly as
  `plan.md` documents it. `sable-marsh` needed two rounds (the SP1 zone, the inert buffer) before it
  compiled and rasterized correctly; `corvid-hollow` and `ashfall-scar` compiled clean on the first plan
  document, and needed sketch-level fixes (bedrock, controls, anchors, skirt) rather than plan-level ones.
- **Absolute goal placement, on all four goals across two maps**, riding ordinary authored ground with no
  piece manufactured to carry it — the exact use case `B128` was built for.
- **Deep material nesting** — a `cell` fabric inside the top layer of a `layered` surface, used on all
  three maps' built tiers (`roost-timber`, `ember-row`) for a patchy top course over measured depth, the
  single most useful technique the run-1 reports named; a `voronoi` with banded depths on `sable-marsh`'s
  hub; `wallRun` and `wallDiagonal` patterns on five different theme walls — all rendered correctly on
  every attempt.
- **Three relief techniques across three maps, each the right tool for its own shape**: `height_mode` +
  `anchor_heights` + `skirt` for `corvid-hollow`'s standalone hill; a subtract ring plus a `push` for
  `sable-marsh`'s hub hole and its hummock; an `area` mark plus a `push` for `ashfall-scar`'s crater and
  mound. All three solved correctly once the parameters were right, and the `sketch/relief/read` numeric
  check caught every one of the height mistakes above before a world was ever built.
- **Bézier curves, four of them across three maps** (the moat's scallop and the forest's and hill's outer
  bulges on `corvid-hollow`; the hub-hole's and the east lane's outer bulges on `sable-marsh`; the forest's
  outer bulge on `ashfall-scar`), all correctly attributed to a single edge once I understood the
  vertex-pair convention. Run 1's own account measured exactly one authored Bézier curve across eleven
  maps; this run alone has four, on top of the anchor-height slant used on two of the three boards.
  Nothing in this run's boards is a straight-edged polygon at one flat height.
- **A defence wall from one `walls` entry**, `sable-marsh`'s `approach-a`/`wool-a` interface — a two-block
  bedrock barrier stamped exactly on the seam, with the chest on the attack-facing side, and read back
  correctly by the traversability check as an intentional foot-level isolation (2 of 4 markers isolated,
  matching the 2 walled wools; the 2 open wools read connected).
  This is the same reading `FINDINGS.md` and `sonnet-run1.md` already validated for other maps: a wall
  meant to be built over, not a fault.
- **Structures read by recorded provenance rather than material, on every render** — every village's houses
  counted individually rather than merged into a blob (`corvid-hollow`: 18 houses + 2 spawn roofs + 2 goal
  markers = 22 findings, matching exactly what was stamped; `sable-marsh` and `ashfall-scar` the same
  shape), and every structures render carries `STRUCTURE READING: RECORDED PROVENANCE` in its scale line
  rather than the material-estimate fallback.
- **The section and column renderers found every mistake in this report.** Not one of the five *mistaken*
  findings above was visible in a top-down or a heightmap — a bedrock-filled column, a self-intersecting
  curve, an over-tall hill and a skirt-dragged edge all look identical from directly above to the correct
  version, because a plan-view render only ever shows the topmost block. `--column` and `--section` are
  what the brief's "look before the next stage consumes it" rule actually means once a shape has a Z axis.

---

## Open gameplay questions, decided without an oracle

Repeated in full, with the reasoning, in each map's own review; listed here together because the pattern
across all three is the same shape of question.

**`corvid-hollow`** — how far "twenty blocks in front" should be measured from. I read it as the width of
the void gap itself (20 blocks deep, from the plaza's edge to the symmetry axis) rather than as the
monument's own setback from the void's near lip (which came out at 10 blocks, since the monument sits
mid-plaza). `approaches.md` gives "roughly twenty blocks" for the gap's width and states no separate
setback figure, so I made the channel's own width the exact number and treated the setback as a free
choice.

**`sable-marsh`** — whether giving one team's own two wools different defensive character (one walled, one
open) is a good CTW shape or just makes one wool the "real" objective and the other a formality.
`approaches.md` says approaches should differ from each other; it does not say whether a team's own pair of
objectives should differ in defensibility, and nothing in the corpus figures `capabilities.md` cites settles
it either. Built it anyway, on the reasoning that a repeated identical wool room reads as one objective
stated twice rather than two objectives.

**`ashfall-scar`** — whether a core and a destroyable on one board should cost roughly the same to break,
or whether a cheap forward goal and an expensive back one is the better shape. The same question
`opus-run1.md` recorded on Quillon Foundry, and I made the same choice for the same reason: two goals of
different cost read as two different fights rather than one fight twice. `approaches.md` settles that goals
belong against each other, not scattered, and stops there.

---

## Findings, with coordinates

| # | Finding | Where to check it | Verdict |
|---|---|---|---|
| 1 | `bedrock.relative: true` reserves the top N blocks as terrain and fills everything below with bedrock | `corvid-hollow` before the fix: `(45, -30)`, y1–19 solid bedrock under one grass block | mistaken |
| 2 | A `controls` entry with `out` **and** `in` on one vertex bends both adjacent edges, self-intersecting a polygon used to bulge only one | `corvid-hollow` before the fix: `(40, -40)` and `(60, -40)`, void | mistaken |
| 3 | `raise`/`sink` add `anchor_heights` to the median pre-erection ground rather than reading it as an absolute height | `corvid-hollow` hill, `(35, -5)`: y25 with anchors `[…,18]`, y16 after re-tuning to `[…,9]` | mistaken |
| 4 | `skirt` blends toward the ground just outside a shape's outline; where that outline meets void, the blend drags the edge down | `corvid-hollow` hill, `(32, -2)`: y7 with `skirt: 3` against void, y16 with `skirt: 0` | mistaken |
| 5 | `PlanValidator`'s SP1 check needs a declared build zone to have any "frontline" pieces to start from, independent of actual reachability | `sable-marsh` first plan, no `zones`: refused all 4 wools; one `zones` entry cleared all 8 findings | mistaken |
| 6 | `build.voidEnforcement` with empty `exclusions` denies the void everywhere, including inside a separately-declared `build.areas` rectangle | `ashfall-scar` first export's `map.xml`: `<everywhere id="void-enforcement-area"/>`, no exclusions, over a board that also declares a build area for its ford | mistaken (docstring says "independent," I read that as "safely additive") |
| 7 | A default-obsidian destroyable exports clean and the kit auto-upgrades to a diamond pickaxe | `corvid-hollow/map.xml`: destroyable `materials="obsidian"`, spawn kit `material="diamond pickaxe"` | confirmed fixed |
| 8 | A destroy map states its own `<gamemode>`/`<objective>`, including a combined DTC+DTM board | `corvid-hollow/map.xml` (`dtm`), `ashfall-scar/map.xml` (`dtm dtc`) | confirmed fixed |
| 9 | `build.voidEnforcement` fires with no declared `build.areas` at all | `corvid-hollow/map.xml`: `block-place=deny(void)` over `everywhere`, no `not-build-area` complement in sight | confirmed fixed |
| 10 | A malformed dressing document refuses by name (prop + field) rather than 500ing or silently emptying `props` | live during `corvid-hollow`'s build: `422 {"rule": "DR-DOC", "message": "prop 'd2' (#1): field 'style.gableWindows.form' could not be read…"}` | confirmed fixed |
| 11 | camelCase enum values (`"template"`, `"cairn"`) parse and stamp correctly | disposable probe map `enum-probe` (not a deliverable): tree + boulder both stamped, confirmed by `--column` | could not reproduce run 1's PascalCase-only claim; likely mistaken there too, confounded by the same run's kind-ordering bug |
| 12 | A walled wool room reads as an isolated traversability marker (foot level); an open one does not | `sable-marsh/renders/06-traversability.png`: 2 of 4 markers isolated, both `stockade`-walled images | confirmed, matches `FINDINGS.md`/`sonnet-run1.md` precedent — intentional, not a fault |
