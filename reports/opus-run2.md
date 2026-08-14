# B120, run 2 — Opus

Three maps authored by driving the studio's own endpoints. Nothing in `/home/user/pgm-studio` was
modified, no capability was added anywhere in `tools/`, and the only code involved is four files in a
scratchpad: a 90-line transport that posts JSON to documented endpoints and unpacks the answer, a file of
block-id shorthand, and one authoring file per map holding the three documents as literals.

| Map | Slug | Kind | Size | Goals | Themes | House styles | Props | What it is |
|---|---|---|---|---|---|---|---|---|
| 1 — the canonical brief | `tallow-mirefast` | DTM | 138 × 204 | 1 destroyable a team | 5 | 4 | 40 | a frozen peat fen: wardstone in the open, spruce wood west, ice scarp east, timber steading behind, a curved ditch in front |
| 2 — mine, CTW | `tallow-weirgate` | CTW | 142 × 190 | 2 wools a team | 6 | 4 | 34 | a drained reservoir: a brick mill town on a hub cut by a sluice, two wool docks at the board's edges |
| 3 — mine, destroy | `tallow-kilnrow` | DTM + DTC | 134 × 190 | 1 core + 1 destroyable a team | 5 | 4 | 30 | a lime works in red clay: a core sunk in a slake pot, a destroyable on a leaning stack of quicklime |

Sixteen themes and twelve house styles, written for these three boards and nothing else. Across the
three: **sixteen shapes carry Bézier `controls`** (65 control entries), **nine carry per-vertex
`anchor_heights`**, three carry a `subtract`, and the height words are used sixteen times —
`level` ×5, `raise` ×7, `sink` ×4. Fourteen relief marks and five pushes, spread across `rim`, `area`,
`scarp`, `point` and `line`; no board is solved by one relief pass. **Thirty-four images** are committed,
nine of them vertical sections, and about thirty column probes were taken beside them.

---

## 1. What I could not say

Every entry carries **Reported · Checked · Verdict**, and the verdict is settled by reading the code.

### 1.1 A sketch-built map's water lanes never reach `map.xml` — **missing**

**Reported.** Tallow Weirgate's east flank was designed around a water lane: a gap that opens
forty-five minutes in, giving the east wool a second approach late without ever being the thing that
joins the two lands (`approaches.md`). I authored it as `{"id": "lane-e-water", "rect": [9,-4,5,2],
"kind": "water-lane"}`, the compile carried it through, and I expected `<include id="water-lanes"/>`
plus a region in the exported XML. There is neither. My first thought was that I had mis-stated the
zone kind or that a lane over partly-solid ground had been dropped by `WL1`.

**Checked.** The zone is fine and the intent is fine:
`specs/tallow-weirgate/tallow-weirgate.intent.json` carries
`"waterLanes": {"rects": [{"minX":45,"minZ":-20,"maxX":70,"maxZ":-10}, {"minX":-70,"minZ":10,"maxX":-45,"maxZ":20}]}`,
correctly fanned. The loss is downstream, and it is one omitted field.
`SketchWorldBuilder.Build` (`src/PgmStudio.Export/SketchWorldBuilder.cs:238–252`) assembles the resolved
intent it hands back as a fresh object:

```csharp
var resolved = new MapIntent
{
    Teams = intent.Teams, MaxPlayers = intent.MaxPlayers, Spawns = resolvedSpawns,
    Observer = resolvedObserver ?? intent.Observer, Build = intent.Build, Wools = resolvedWools,
    Destroyables = resolvedDestroyables, Cores = resolvedCores, Meta = intent.Meta,
    Symmetry = intent.Symmetry, IslandTeams = intent.IslandTeams, Structures = intent.Structures,
};
```

Eleven properties named, `WaterLanes` not among them. `MapExportComposer.Compose`
(`src/PgmStudio.Export/MapExportComposer.cs:80`) then calls `IntentGenerator.Apply(doc, goals)` with
exactly that copy, and `WaterLaneGenerator.Apply` opens with `Clear(doc)` — so the region a previous
`PUT /map/{slug}/intent` had legitimately written is deleted and never rewritten, and
`WaterLaneGenerator.EnsureInclude` then correctly removes the include because the region is gone. The
two halves stay consistent with each other and both are wrong.

**This failure has already happened once in this tree, was diagnosed, and the fix was applied to a
different file.** `SymmetryExpander.Expand` (`src/PgmStudio.Pgm/Authoring/SymmetryExpander.cs:44–46`)
carries the lesson in a comment: *"`with`, never a fresh `MapIntent`: a rebuild that names its fields
drops every slice added after it was written, which is exactly what happened — destroyables, cores,
island teams and the plan's stamped structures were all deleted here, silently, on any intent carrying a
symmetry."* Its `OrbitBuild` repeats it for `BuildIntent` at line 88. `SketchWorldBuilder` is the one
place on the export path that still names its fields, and `WaterLanes` is the slice added after it was
written. The fix is `intent with { Spawns = …, Observer = …, Wools = …, Destroyables = …, Cores = … }`.

**Verdict: missing.** A water lane is authorable at every layer above the world and cannot survive the
world build, on any sketch-originated map — which is every map an agent authors through the documented
six-call loop. Reproduction is one plan with one `kind: "water-lane"` zone.

*What it cost this board:* Tallow Weirgate ships with its east gap as permanent void and its east wool
on a single door. That is legal and it is 79% of the corpus, so the map plays; it is not the map the
authored documents describe, and `review/tallow-weirgate.md` says so rather than papering over it.

### 1.2 A tone-family reading of a stained-clay board — **missing**, and my first claim about it was **mistaken**

**Reported.** Tallow Kilnrow's `--surface` render came back with most of the board painted magenta —
"unnamed material". I read it as the paint having failed, and started looking for a theme-resolution
fault.

**Checked.** The paint had not failed: `--column` at `(-58, -50)` reads
`159:7 Gray Stained Clay ×3` over stone, which is exactly the `kiln-floor` surface, and
`--topdown --material` draws the whole board correctly (`renders/04-material.png`). What the surface
render cannot do is *sort* those blocks: `TerrainPalette.Families`
(`src/PgmStudio.Minecraft/TerrainPalette.cs:59–75`) names nineteen tone families whose members include
stained clay `159:1, 3, 5, 9, 11, 12, 13, 15` and no others. This board leans on `159:0` (white),
`159:7` (grey), `159:8` (light grey) and `159:14` (red), none of which any family claims, so they fall
through to the unnamed colour.

**Verdict: mistaken** on my own claim — the map is fine and the check I wanted exists one flag away.
The secondary finding stands on its own and is **missing**: there is no tone-family reading of a board
painted in half the stained-clay palette, and `--surface` is the read-back a themed board most wants.
Both renders are committed beside each other, because the failure is the finding.

### 1.3 A grown tree's `branchAngle` is in radians and no tool document says so — **mistaken**

**Reported.** I wrote `"branchAngle": 40` for the neck copse on Tallow Mirefast, reading it as degrees.
The foliage read-back drew five crowns of about fourteen blocks' radius fused into one blanket over a
fifteen-block neck — a mass rather than five trees, which is the exact failure `approaches.md` warns
about under density.

**Checked.** `TreeProp.BranchAngle` (`src/PgmStudio.Minecraft/Dressing/PlacedProp.cs:148–151`) says
plainly: *"how far a branch leaves its parent, **in radians**. A hand-built corpus leaves the trunk at
59° off vertical … so the default is a radian rather than the half one a tighter fan wants."* And
`TreeProp.Shape` clamps it to `[0.2, 1.5]`, so 40 becomes 1.5 — a nearly horizontal fan — with no error
anywhere. `docs/tools/sketch.md:463` lists the field by name inside a sentence of other knobs and gives
no unit; `docs/world-export/decoration.md` does not name it at all.

**Verdict: mistaken.** The unit is stated at the source and I did not read it. Worth recording anyway
because the clamp is what hid it: `leader` and `leafSize` are clamped for the documented reason (cost is
superlinear in reach), and the same clamp turns a unit error into a plausible-looking tree instead of a
refusal. The fix is one word in `sketch.md`.

### 1.4 `build.voidEnforcement` is not reachable from a plan — **mistaken** (about where it lives)

**Reported.** Tallow Mirefast's ditch had to be permanent, and I wanted to say so on the plan. There is
no zone kind for it, no global, and `capabilities.md` and `plan.md` — the two documents the brief pushes
hardest — do not mention void enforcement at all. Run 1 solved the same problem by declaring a decorative
build zone over land purely to switch the void rule on.

**Checked.** It exists, it is documented, and it is not the plan's.
`BuildIntent.VoidEnforcement` (`src/PgmStudio.Pgm/Authoring/MapIntent.cs:178`) is a second, independent
knob; `BuildGenerator.Apply:44` fires it whether or not `Areas` is populated;
`docs/pgm/new-map-authoring.md` §5b is a whole section on it and states outright that *"the plan compiler
does not yet derive a `VoidEnforcement` from anything in the plan model — a hand-authored or
agent-authored intent states it directly"*; and `docs/tools/configure.md:224` carries the worked JSON.
Writing `intent["build"]["voidEnforcement"] = {"exclusions": []}` onto the compiled intent before
`PUT /map/{slug}/intent/from-plan` produced `<everywhere id="void-enforcement-area"/>` and
`<apply block-place="deny(void)" region="void-enforcement-area">` on the first try.

**Verdict: mistaken.** No gap. The measurable is legibility: the field is documented in `configure.md`
and `pgm/new-map-authoring.md`, neither of which is on this brief's reading list, and an agent working
from `plan.md` + `capabilities.md` alone would file it as missing. One sentence in `capabilities.md`'s
set-algebra section — *whether a hole may be bridged is `BuildIntent`, and it does not need an `Areas`
entry* — would close it.

### 1.5 An absolutely-placed goal is invisible in the only picture of a plan — **unreachable**

**Reported.** `GET /plans/{id}/png` for Tallow Mirefast draws five pieces, the ditch buffer, the legend
and both spawns, and **nothing at `(0, −50)`** where the wardstone stands
(`maps/tallow-mirefast/renders/01-plan.png`). The same for both goals on Tallow Kilnrow.

**Checked.** `plan.md` §Coordinates says the canvas *"does not yet offer a way to draw this"* for a
destroyable or core with an empty `piece`; the raster renders the same scene the canvas does, so it
inherits the gap. This is run 1's finding 7, unchanged.

**Verdict: unreachable.** The mechanism (`B128`) is shipped and is the single most useful thing on the
board for an agent — but the one raster the plan layer offers cannot answer "where are the objectives"
for exactly the boards that use it. The objectives layer of the world read-back
(`--topdown --layer objectives`) answers it a whole stage later.

### 1.6 A theme spent on a wool-room piece is spent on nothing — **not a gap, worth knowing**

**Reported.** Tallow Weirgate binds `weir-mill` to both wool docks. A column probe at `(-60, -30)` reads
bedrock y0..11, bricks y12, red wool y13 — no theme anywhere in the column.

**Checked.** `WoolStructureStamper` calls `StampFoundation` unconditionally, filling bedrock from y0 to
the surface under the whole room footprint "so the room cannot be tunnelled into from below"
(already recorded in this repository's `FINDINGS.md`). The dock piece *is* the room, so the whole
platform is foundation.

**Verdict: not a gap** — documented behaviour with a stated reason. Recorded because the consequence is
invisible from above and costs an author a theme: if a wool room is to sit on painted ground, the
painted ground has to be a shape the room does not cover.

### 1.7 The evaluator refuses a motif `rules.md` names as a device — **mistaken** (about what a refusal is)

**Reported.** Tallow Weirgate's first plan came back from `POST /plan/evaluate` with
`valid: false` and a **hard** term: `wool-ringed-hole … "a closure hole is ringed by a wool plateau (two
approaches, WL8)"`. I read `hard` as a refusal and nearly took the void moat out.

**Checked.** `plan.md` §"The evaluator's `valid` is not the compile's" states it exactly: the evaluator
is a critic built to rank composed candidates and promotes some lint to hard terms, *"so a board that
compiles cleanly can come back `valid: false` … and nothing about that stops it being built"*. The
compile returned 200. Separately, the term and the rule text are not saying the same thing:
`ClosureTerms.WoolRingedHole` forbids the motif where *"outside terrain wraps the wool"*, while
`rules.md` §"Function is read from the hole's ring" calls a hole whose ring contains a wool *"the
hole-mediated two-approaches device (the WL8 pattern realized by a hole)"* and names the seeds that use
it.

**Verdict: mistaken** on the refusal. The doc/term tension is real and is a finding for the repository
rather than for me. In the event I redrew the flank anyway, for a reason that was mine and not the
term's: three approaches to one wool and one to the other was an unbalanced board.

### 1.8 What I did not reach

Stated plainly rather than dressed up as limits.

- **A multi-wing footprint** (`G172`'s open half). `HouseProp.Points` is two corners and there is no
  field for a second rectangle. I did not need an L or a T; every building on all three boards is one
  rectangle by the model's choice, not mine.
- **A picture of a sketch.** There is none, by design and by documentation. I built the world and read it
  back, so every geometry decision was checked one stage after it was made. The two faults I found in
  ground (the mid being sixteen blocks deep, the slake pot being two below the floor rather than four)
  were both invisible until then.
- **`POST /map/{slug}/sketch/paint`.** I never called it. It answers the painter's real output as
  palette-indexed runs before a world exists, and it would have caught 1.2 a stage earlier. I used
  `relief/read` on every map and skipped its sibling, which is a hole in my own routine, not the tool's.
- **The shared library** (`/styles`, `/themes`, `/room-styles`). Every theme and house style is written
  into the layout document directly. Two other agents were authoring against the same unscoped library
  tables at the same time; I did not want to leave rows behind in theirs.

---

## 2. What I got wrong

**I read a magenta render as a broken map.** §1.2 above. The rule the repository already states —
*an image is a check, not a source of meaning* — is exactly the rule I broke: I asked a picture *what*
rather than *whether*, and the answer it gave was about its own palette. It cost about fifteen minutes
and it would have cost a redesign if I had acted on it.

**I authored an angle in degrees.** §1.3. The specific lesson is not "read the docstring" but the one
run 1 ends on and I repeated in a new place: the information was in reach and I reasoned from a tool
document that names a field without defining it.

**I put plain stone in a `cell` palette whose theme's fill is plain stone.** Tallow Mirefast's crag read
as unpainted rock in a column probe at `(44, −58)` for one build. A fifth of the crest was drawing the
same block the body is made of. Every cell palette on the later boards is checked against its own fill.

**I sized the first mid at sixteen blocks and could not see it until both halves were drawn.** The
ditch's south edge and its `rot_180` image left the only contested ground on Tallow Mirefast sixteen
blocks deep. Nothing in the plan, the relief readback or the section says this; it is only visible in a
top-down of the fanned board, which is one stage after the decision.

**I assumed a `sink` measures from the ground beside it.** It measures from the **median** of the ground
under its own footprint (`SketchRasterizer.Erect`, and the docstring is explicit). Tallow Kilnrow's
slake pot straddles a terrace at 15 and a floor at 11, so `base_height: 4` cut to 9–10 — two below the
floor, not four. Run 1 recorded the same class of mistake with different numbers; the general form is
that a relative height word reads a datum you have to know the footprint to predict.

---

## 3. What worked first time

This list is the part that says which of the system to trust.

**The six-call loop, exactly as `plan.md` documents it.** `POST /plan` → `PUT …/plan` →
`POST /plan/compile` → `PUT …/sketch` → `POST …/sketch/finish` → `PUT …/intent/from-plan` →
`GET …/export`. Three maps, sub-second exports, no surprises. Authoring the whole `SketchLayout` by hand
and `PUT`ting it verbatim (documented as a verbatim replace) removes the entire class of problem that
comes from addressing compiled tiers by the height they stand at.

**Both goals of Tallow Kilnrow riding authored landforms with no plan piece under them.**
`{"piece": "", "at": [-7, -11]}` and `{"piece": "", "at": [7, -11]}` resolved to `(−35, −55)` and
`(35, −55)` and took their Y from the terrain the rasterizer built — a core at y17..22 in a `sink` pot
and a destroyable at y27..31 on a `raise` stack, ten blocks apart in height because the two landforms
are ten blocks apart. The landform is authored once, in the layout, where it belongs.

**The three run-1 faults are fixed, and I confirmed each rather than assuming it.**

| Fault in run 1 | What run 2 measured |
|---|---|
| a destroy map shipped `<gamemode>ctw</gamemode>` and "Capture the enemies' wools!" | `tallow-mirefast/map.xml:4–5` — `dtm` / "Destroy the enemy's monuments!"; `tallow-kilnrow/map.xml:4–5` — `dtm dtc` / "Destroy the enemy's monuments and leak the enemy's cores!" |
| the export gate refused an obsidian goal against an iron pickaxe as unwinnable | Tallow Mirefast's wardstone **is obsidian**, the export was clean, and `map.xml:17` carries a **diamond pickaxe** because `DestroyKitPairing` upgraded it. Run 1 chose end stone to dodge a refusal that no longer exists |
| a malformed dressing document discarded every prop silently | Not hit: every prop parsed on the first attempt across 104 props and three boards, with `kind` written wherever it fell in the object and enums in camelCase, both of which `DressingJson.Options`' `AllowOutOfOrderMetadataProperties` and camelCase converter now accept |

**A build zone reads as pink and a water lane as hatched blue, and they are unmistakable.**
`maps/tallow-weirgate/renders/01-plan.png` carries both, with the key baked in. The old failure — reading
a blue build zone as water — cannot happen the same way.

**`voidEnforcement` with no build area at all.** One field on the compiled intent produced
`<everywhere id="void-enforcement-area"/>` and `<apply block-place="deny(void)">`, and Tallow Mirefast
declares no build rectangle anywhere. The workaround run 1 needed is gone.

**The vertical read-backs.** `--column` and `--section` settled five things nothing else could: the
ditch is 19 void columns wide with its lip 20 blocks in front of the goal; the neck is walkable at
`(−58,−14)` and `(−50,−14)` and void at `(−44,−14)`; the crag's paint was a palette mistake and not a
theme fault; the slake pot is two below the floor and not four; the destroyable's own column is
unpainted stone under its bedrock plate. Four of those are invisible in every plan view.

**`--structures` reading recorded provenance.** Every render states
`STRUCTURE READING: RECORDED PROVENANCE`, and the counts are exact: 22 on Mirefast (9 × 2 buildings + 2
spawn cubes + 2 goal markers), 47 on Weirgate, 20 on Kilnrow. Run 1 lost buildings silently to a path
band and had no reading that would report it; this one confirms every building asked for was stamped, on
both orbit images, in one line.

**`--topdown --layer foliage --dressing`.** Drawing each tree as a point and a measured crown radius is
what caught the `branchAngle` error. The combined foliage view showed one violet mass; the point-and-
radius view showed five circles of fourteen blocks each, which is a different fact.

**Deep material nesting, on all sixteen themes.** A `cell` inside the top layer of a `layered` over two
solids; a `voronoi` with banded depths; `wallRun`, `wallDiagonal` and `wallFrame` on risers;
`logChecker` and `laidLog` as house posts and gables; `checker` floors. No arity limit, no complaint.
Turning the **rim off** on grown ground and on for built tiers remains the single boolean that changes
how a board reads most.

**A defence wall from one line of JSON.** `walls: [{"a": "dock-w", "b": "front", "side": "a"}]` produced
a two-thick bedrock barrier at `x = −50, z −40..−20` with a cobweb course on top, fanned to both images,
and the traversability read still reports **0 isolated** because the dock's own lane stays open behind
it.

**The `relief/read` numbers.** Every board was tuned against them before a world existed: Mirefast's wood
was solving to y21 against a crag at y22 and the swell was pulled down to 14 so the crag stayed the
board's high point; the walk tier's `places: 1` confirmed one connected surface on two of the three
boards before any picture existed.

---

## 4. Open gameplay questions, decided without an oracle

Each is a decision, not a derivation.

**Which way a channel should be decided, and I decided differently on two boards.** Tallow Mirefast's
ditch is **permanent** — no build area anywhere, `voidEnforcement` over everywhere — so the only thing it
can do is make attackers go round, and the board is built around the two ways round being unequal.
Tallow Kilnrow's flue is **bridgeable from the first tick** under a build zone, so crossing it is a
visible, expensive commitment rather than an impossibility. `approaches.md` says both are legitimate and
that deciding neither is the fault. I have no basis for preferring one, so I built one of each and said
which is which. **Open:** whether a destroy board's *forward* channel — the one twenty blocks in front of
the goal — should ever be bridgeable, or whether that is the one place permanence is the point.

**Asymmetry between a team's own two wools.** Tallow Weirgate's west wool has a walled face and two
approaches; the east has one door and no wall. `approaches.md` says the approaches should differ and
`match-flow.md` §4.8 says one wool always falls first anyway. **Open:** whether making that predictable by
design reads as composition or as an unfair wool. Run 1 asked the same question; I answered it the same
way and I am no more certain.

**A core that is cheap to reach and expensive to break, against a destroyable that is the reverse.**
Kilnrow's slake pot is a bay an attacker walks into with `float 6` / `leak 10` — four blocks of digging
under the casing — while the lime kiln is end stone nineteen blocks up a stack, soft against the diamond
pickaxe the core has already put in the kit. **Open:** whether a defender can actually split attention
across two goals that fail in different ways, or whether the cheap one simply always goes first and the
board is a one-goal board with scenery.

**How far out a defence wall should stand.** `match-flow.md` §6.2 measures a corpus median of thirteen
blocks in front of the room. I put Weirgate's wall **on** the room's own face, because on this board the
attacker arrives at that face off open ground and there is nothing between them to stand a line on.
**Open:** whether a wall flush with the room is a different device from a wall thirteen out, or the same
one badly placed.

**Density, still unmeasurable.** Mirefast carries 21 trees over roughly 45 × 50 blocks of wood plus a
five-tree thicket in the neck; Kilnrow carries nine over a board that was mostly burnt. `approaches.md`
says the measure that would settle it — what share of ground stands under a leaf — is `B96` and unbuilt.
I chose by eye off the point-and-radius foliage render, which at least counts trees.

**Whether sixteen blocks of contested mid is too little.** I decided yes on Mirefast and widened it to
twenty-two. Nothing measured that; the top-down looked pinched.

---

## 5. Findings, with coordinates

| # | Finding | Where to check it | Verdict |
|---|---|---|---|
| 1 | A sketch-built map's `waterLanes` are dropped between the intent and the XML | `specs/tallow-weirgate/…intent.json` has two rects; `maps/tallow-weirgate/map.xml` has no `water-lanes` region and no include. `SketchWorldBuilder.cs:238–252` omits `WaterLanes` from its resolved copy; `MapExportComposer.cs:80` re-projects from it | **missing** |
| 2 | `--surface` paints most of a stained-clay board magenta | `maps/tallow-kilnrow/renders/04-surface.png` against `04-material.png`; `TerrainPalette.cs:59–75` names `159:1,3,5,9,11,12,13,15` only | **missing** (the reading); my "the paint failed" claim was **mistaken** |
| 3 | `branchAngle` is radians, clamped to `[0.2, 1.5]`, and `sketch.md` gives no unit | `PlacedProp.cs:148–151`; `sketch.md:463`. Reproduce with `"branchAngle": 40` and `--topdown --layer foliage --dressing` | **mistaken** (mine), doc gap |
| 4 | `build.voidEnforcement` has no plan-level surface and is unmentioned in `plan.md`/`capabilities.md` | `MapIntent.cs:178`, `BuildGenerator.cs:44`, `new-map-authoring.md` §5b, `configure.md:224`. Works: `tallow-mirefast/map.xml:76,81` | **mistaken** (mine), legibility |
| 5 | An absolutely-placed goal does not appear in `GET /plans/{id}/png` | `maps/tallow-mirefast/renders/01-plan.png` — nothing at `(0, −50)`; `maps/tallow-kilnrow/renders/01-plan.png` — nothing at `(±35, −55)` | **unreachable** |
| 6 | A wool-room piece is bedrock from y0, so a theme on it paints nothing | `(-60, -30)` on `tallow-weirgate`: bedrock y0..11, bricks y12, wool y13 | not a gap; undocumented consequence |
| 7 | `wool-ringed-hole` (WL8) is a **hard** evaluator term over the motif `rules.md` calls the two-approaches device | `ClosureTerms.cs:5–9` against `rules.md` §"Function is read from the hole's ring"; the same plan compiles 200 | doc/term tension |
| 8 | Hay bale (170) and packed ice (174) read as "unnamed material" in `--surface` | `maps/tallow-mirefast/renders/09-surface.png` — the steading roofs and the crag cap | same family as #2 |
| 9 | A destroyable's own column is unpainted stone under its bedrock plate | `(35, -55)` on `tallow-kilnrow`: stone y1..20, bedrock y21, end stone y27..30 | correct by design (paint runs after stamps) |
| 10 | `sink` reads the **median** ground under the whole footprint, so a pit straddling two tiers is shallower than asked | `tallow-kilnrow` pot: `base_height 4` over a footprint straddling 15 and 11 gives a floor at 9–10. `renders/11-section-pot.png` | documented; only visible in section |

---

## 6. One process note

Every board was looked at between stages: `POST /plan/evaluate` → the plan raster → `PUT sketch` →
`POST sketch/relief/read` → finish → export → top-down → heightmap → two or three vertical sections →
column probes → `--structures` → `--traversability-map` → foliage points, and back round. Six of the ten
findings above exist only because of the vertical read-backs or the point-and-radius foliage view, and
four of them are invisible in every plan view of the same map.

The corollary this run adds to run 1's — *a plan view is not a stage image for anything with a height* —
is about the other axis: **a render's palette is part of the render, not part of the map.** Two of my ten
findings are a read-back's own vocabulary running out (`--surface`'s tone families, `BlockPalette`'s
names), and in one case I briefly believed the map was broken because of it. The read-backs state which
reading they used — `STRUCTURE READING: RECORDED PROVENANCE` is printed on every image — and the same
honesty applied to the colour vocabulary ("this board uses N blocks no family claims") would have saved
the detour.
