# Sonnet — run 1

Three maps, authored entirely by driving `http://localhost:7894/api` directly (plan → compile →
`sketch/from-plan` → hand-edited layout → `sketch/finish` → `intent/from-plan` → `export`), never
through `tools/mapgen` and never from a composed board. No source change anywhere in `pgm-studio`; no
new capability anywhere in `pgm-studio-mapgen/tools`. Every script I wrote lived in my own scratchpad
and did nothing but post JSON I had authored to documented endpoints and read back the answer — the one
exception, noted below, is a single throwaway diagnostic console app used to get an exact exception
type out of a library call, which never touched a live map and is not part of the deliverable.

- `maps/sonnet-holdfast/`, `maps/sonnet-briarlock/`, `maps/sonnet-cinderreach/` — world, `map.xml`,
  renders at every stage.
- `specs/sonnet-holdfast/`, `specs/sonnet-briarlock/`, `specs/sonnet-cinderreach/` — the plan, the full
  posted layout (shapes, relief, themes, dressing) and the intent for each.
- `review/sonnet-holdfast.md`, `review/sonnet-briarlock.md`, `review/sonnet-cinderreach.md` — what each
  board is, how it plays, the techniques used, coordinates.

## What I could not say

Two are genuine defects — reproducible, minimal, and independent of anything about my own maps'
content. Two more are previously-known gaps this run corroborates rather than discovers. The rest are
choices I made rather than walls I hit, and I have kept the two kinds apart on purpose.

### Missing from the system

**1. `GET /map/{slug}/export` (and `/xml`) requires a dressing prop's `"kind"` to be the *first* JSON
key of the object, and 500s on the whole call otherwise — silently, for every other endpoint.**
`PUT`/`GET /map/{slug}/sketch` and `POST /map/{slug}/sketch/paint` accept and round-trip a prop object
in any field order, including the order `docs/tools/sketch.md`'s own worked dressing example uses
(`{"id": "d1", "kind": "path", …}` — `id` first). I wrote my first attempt following that example
exactly, and it stored cleanly, previewed cleanly, and 500'd at export with
`"The JSON payload for polymorphic interface or abstract type 'PgmStudio.Minecraft.Dressing.PlacedProp'
must specify a type discriminator. Path: $.props[0]"`. I bisected it down to a single minimal
reproduction: one well-formed tree prop, `id` before `kind`, fails; the identical prop with `kind`
first succeeds. Confirmed with `curl` against the live map `sonnet-holdfast`, both directions, several
times.

The mechanism: `DressingJson.Deserialize` (`src/PgmStudio.Minecraft/Dressing/DressingJson.cs`) wraps its
`JsonSerializer.Deserialize<DressingDoc>` call in `catch (JsonException)`, with the comment "a
hand-edited blob must not fail an export." A one-off diagnostic console app referencing
`PgmStudio.Minecraft` directly (not part of the deliverable, run once, deleted with my scratchpad)
called the same method on the same JSON and threw — not a `JsonException`, but an
`InvalidOperationException`/`NotSupportedException`-family error from `System.Text.Json`'s own
polymorphic-type resolution. That family is not caught by the `catch (JsonException)` clause, so it
propagates past the "must not fail" guard straight to `MapExportComposer.Compose`'s outer
`catch (Exception ex)`, which is what turns it into the 500 body I saw. I could not fix this — no
source change is permitted — so every prop in every map I shipped has `"kind"` written first, which is
a workaround in my own JSON, not a fix to the tool.

**2. Every enum-valued field on a dressing prop or a `HouseStyle` must be written as the C# member's
literal name — `Template`, `Worn`, `StairLattice`, `Arched`, `NegX`, `Air` — not the camelCase
`docs/tools/sketch.md` and `docs/world-export/decoration.md` show throughout (`"template"`, `"worn"`,
`"negZ"`). And the failure mode compounds the first one: `DressingJson.Options` declares a
`JsonStringEnumConverter(JsonNamingPolicy.CamelCase)`, so a value that does not parse throws inside the
same deserialize call — caught by the same over-narrow `catch (JsonException)` in some cases, and when
it is caught, the entire `props` list silently becomes empty rather than reporting which prop or field
was wrong.**

I found this by building all 53 props of Sonnet Holdfast's dressing, fixing finding #1, getting a clean
`200` from export with all 53 props stored — and then column-probing a spot I knew should carry a tree,
and finding bare terrain. Nothing anywhere said the dressing pass had done nothing: not the PUT, not the
export status code, not the paint preview (which does not read dressing at all). I confirmed the exact
mechanism by testing single props at a time: `{"form": "template"}` silently drops; `{"form":
"Template"}`, identical otherwise, stamps a real tree. The same held for `PathProp.Style`
(`Worn`, not `worn`), `BoulderProp.Form` (`Round`/`Angular`/`Outcrop`/`Cairn`), `HouseProp.Front`
(`NegX`/`PosX`/`NegZ`/`PosZ`, the `RoomEdge` enum), and every enum inside a `HouseStyle` snapshot —
`RoofForm`, `WindowForm`, `DoorHeadForm`, `DoorHeadFill`, `DoorMaterial`. I confirmed every one of those
names against the C# source (`PlacedProp.cs`, `HouseStyle.cs`, `HouseWindows.cs`,
`RoomFrames.cs`) rather than guessing further after the first two, which is why maps 2 and 3 hit no
further instances of this once I knew to check.

I want to be precise about severity: this is not a cosmetic mismatch. A 53-prop village, forest and
hillside — six house styles, thirty-odd trees, boulders, paths — built, exported, and shipped **zero
of them**, at a `200` status, with the stored document showing all 53 present. An author who does not
column-probe a specific coordinate they already expect a tree at has no way to learn this happened.

### Corroborated, not discovered

**3. A spawn-role structural shape's own terrain paint never applies to its interior — only its edge.**
Column-probed at the true centre of the spawn platform on all three maps: `sonnet-holdfast` (0, −165),
`sonnet-briarlock` (0, −155), `sonnet-cinderreach` (0, −145) all read raw, unpainted `Stone` (id 1)
under a wool-coloured spawn marker block, on three different themes with three different `surface`
buckets, none of which appears. The *edge* of the same platform, where the theme's `wall` bucket
applies (probed at `sonnet-briarlock` (0, −170), the platform's own boundary), **is** painted correctly
— so the fault is specific to the interior/surface classification of a spawn shape, not to spawn shapes
wholesale. This is the same symptom `FINDINGS.md` (this repository, ClayClay Redux) already reported —
I am confirming it is still present on the current build rather than filing it new, with three fresh
coordinates and the edge/interior distinction that file did not have reason to draw.

**4. A destroy goal's material and the map's kit are not automatically paired**, exactly as
`docs/tools/capabilities.md` already documents (`TeamsGenerator` writes one fixed "Standard" kit with an
iron pickaxe, with no branch for a destroyable's material). This is not a bug I found; it is a
documented gap I designed around — see the open question below rather than re-filing it.

### Out of reach from where I was standing, not shown to be missing

I did not use the shared **library** tables (`POST /styles`, `/themes`, `/room-styles`) at all — every
theme and house style in all three maps is written directly into the layout document rather than
composed in the library and pulled in. Two other agents were authoring against the same running
database at the same time, and the library's tables are genuinely shared and unscoped by map
(`docs/tools/library.md`: "no slug, no stage, no map row anywhere in it"), so composing there risked a
name collision or an edit landing between another agent's read and write. That is a constraint of
*this exercise run concurrently*, not a claim that the library endpoints do not work — I simply never
exercised them, and I would not generalise from three maps that never touched `/styles` or `/themes` to
a statement about whether they are sound.

I also never opened `/plan-editor` or called `POST /plans`, so `GET /plans/{id}/png` — the one raster
the plan layer has — was never available to a plan I originated with `POST /plan` directly against a
map row. That is the documented shape of the two routes (`docs/tools/plan.md`: the bare route "has no
map row behind it"), not a gap; I mention it only because it means my "look before the next stage
consumes it" discipline on the plan layer was necessarily `POST /plan/inspect` and `/evaluate` rather
than a picture, and I want that distinction visible rather than implied.

## What I got wrong, once I found out

**I initially assumed a `HouseStyle`'s course `"extent"` field sized the wall to a specific building's
footprint width**, from reading the "desert brick" example in `library.md` where `wall.extent` is 7 and
the preset itself happens to be seven wide, and I nearly wrote one style JSON per house size before
re-reading `docs/world-export/structures.md` §7 closely enough to see `extent` is a **vertical** course
count ("how far the part goes," read from the part's own base outward), independent of the footprint the
prop supplies. Re-reading before acting saved rewriting fifteen-odd style objects; I record it because
the map1/map2 house scripts each define one style shared across footprints of several different sizes
and aspect ratios, and that only works because the assumption was wrong.

**My first hill on Sonnet Holdfast solved to y23 against a build cap of y20** — three blocks *above*
the ceiling a player can place a block up to, which would have made the top of the hill an unreachable
dead zone rather than the bridging launch point the brief asks for. `POST
.../sketch/relief/read` caught it before any world was built (`high: 23`), and I re-tuned the push's
`amount`/`crown` down until the same readback reported 19 — one block of headroom under the cap. I
record this because it is exactly the numeric check `docs/world-export/relief.md` recommends and
`docs/tools/sketch.md`'s "look before the next stage" rule asks for, and it is the one time in three
maps that following it caught something a topdown render would only have shown after the fact.

**I suspected a wall-coloured "riser" seam at a theme boundary on Sonnet Holdfast was a real,
unintended cliff** rather than the documented "structure is decided by block material" render artifact,
before checking the heightmap — which showed a smooth, gradual rise with no such step. I record this as
a wrong suspicion caught before it cost anything, not as a finding, because the correct read was the
one the docs already gave: an image is a check on whether the authored thing came out, not a source of
meaning on its own, and I had to go back to the *document* (the relief numbers) rather than trust the
first *picture* to settle it.

**I chose netherrack (block 87) for two "scorched ground" theme buckets on Sonnet Cinderreach expecting
it to read as natural rock**, and the categorised top-down render came back with the entire knoll one
solid orange mass. `BlockRoles.BuiltSurfaces` (`src/PgmStudio.Minecraft/BlockRoles.cs`) lists netherrack
among sandstone, quartz and stone brick as a "built" surface for render-classification purposes — a
correct and documented mechanism in general (`docs/generator/model.md`'s renderer section states it
plainly), but applied to a specific block I had no way to predict without either reading that table or
rendering and looking, which is what I did. Swapping to plain stone (id 1, not in the table) fixed the
read with no other change. This did not affect the built map at all — it is a render-classification
question, not a world-content one — but it is exactly the "look before the next stage consumes it"
discipline paying for itself, and I record which specific block tripped it since the general caution in
the docs does not name one.

## What worked first time

- **Every plan compiled clean on the first submission**, all three maps: no structural errors, no
  completeness warnings, no lint beyond what I expected.
- **An absolutely-placed goal riding ground with no plan piece under it** (`{"piece": "", "at": [...]}`,
  `docs/tools/plan.md`'s `B128`) worked exactly as documented on both destroy maps — once on an authored
  clearing (Holdfast), once on a relief-solved knoll (Cinderreach) — with no special handling either
  way.
- **The relief model** — marks, an `area` bench holding a pad flat beside a `push` raising a hill beside
  a `scarp` cutting a one-sided shelf, all in one island — solved correctly and matched its own readback
  every time I checked it before building.
- **The traversability gate read exactly as documented in every case**, including the one that looks
  like a fault and is not: Sonnet Briarlock reports 4 isolated points, which are its four wool markers
  behind a three-course defence wall meant to be built over rather than walked through — the identical
  reading `FINDINGS.md` already validated for ClayClay Redux's own wall. I treated the corroboration as
  confirmation the model is doing what it says, not as a new alarm to chase.
- **Deep material nesting** (a `cell` fabric inside a `layered` stack's top course, a `voronoi` with
  banded depths, `wallDiagonal` and `wallRun` patterns) rendered correctly on every attempt, no arity
  limit encountered.
- **Kit-aware goal material choice worked as a substitute for an unreachable kit edit.** Naming Sonnet
  Holdfast's destroyable `"ender stone"` rather than the obsidian default was accepted by the `OB18`
  unwinnable-goal gate at export with no refusal, which is the closest confirmation the pipeline offers
  that the goal is actually breakable by the kit it ships with.
- **The symmetry fan reported zero error on every relief readback across all three maps** (`"symmetryError":
  0`), including on Sonnet Holdfast's Bézier-curved coastline and Sonnet Briarlock's rounded corners.

## Open gameplay questions, decided without an oracle

Each is repeated in full, with the reasoning, in its map's review file; summarised here so they are in
one place.

**Sonnet Holdfast — what material should a destroy goal carry when the kit that ships with it cannot be
changed?** `docs/tools/capabilities.md` already names the gap (no generator path ties a kit to a
destroyable's material); I decided to name the goal `"ender stone"` rather than keep the obsidian
default, since the standard kit's iron pickaxe can mine it and obsidian cannot. I did not attempt to
hand-edit the exported `map.xml`'s kit, because that would ship a deliverable that disagrees with what
the studio itself produced from the authored documents.

**Sonnet Briarlock — how far out from a wool room should its defence wall stand?** `match-flow.md` §6.2
measures a corpus median of 13 blocks out, on a bedrock line the map supplies; I placed both walls at
the corridor's outer mouth (roughly 20 blocks out) rather than at the room's own face, reading it as
closer to that convention than the alternative, but recorded as a judgement rather than a derived
number.

**Sonnet Cinderreach — is a plain river a legitimate sole approach control on a destroy map**, the way a
void channel or a water lane is documented to be on other modes? `approaches.md` names rivers in the
same breath as void holes and hills but every worked example anywhere in the read documents is a
capture-map lane. I built it as a chokepoint on the general claim, and could not verify from the
traversability read alone (0 isolated, 2 components) whether it plays as a commitment or as a shallow
ford nobody notices — that is a question about depth and width under real feet, which is the human
oracle's and not derivable from a column probe.
