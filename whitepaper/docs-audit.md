# Documentation audit — pgm-studio at `dae1d45`

Taken while writing `white-paper.md`, by reading the code and the running studio rather than the documents.
Every figure below was measured twice: statically, off the source tree, and live, off `GET
/api/openapi/v1.json` and `GET /api/rules` served by a studio built from this commit.

**The distribution is the finding.** Every documented **endpoint, path and failure code** is correct — 209
distinct `VERB /path` citations across `docs/**/*.md`, zero missing routes — because
`tests/PgmStudio.Api.Tests/EndpointTables.cs` parses the `docs/tools/` endpoint tables and three tests fail
when a row and a route disagree. Every error found is in **ungated prose**. Where a number is generated
(`census.sh` writing `project-structure.md`'s size table) it is right; where it is generated *and* re-typed
130 lines away in the same file, the typed copy is the wrong one.

---

## Applied

Committed on `claude/pgm-studio-mapmaking-whitepaper-raxcr2` in `rockymine/pgm-studio`. No source file was
touched.

### A type and a method that do not exist

| Where | Was | Is |
|---|---|---|
| `docs/refusals.md` — gate table | `SketchRoomStyleGate.Check(layoutJson)` | `SketchMaterialGate.Check(layoutJson)` — `src/PgmStudio.Api/Services/SketchMaterialGate.cs:27`. `SketchRoomStyleGate` appears nowhere in `src/` |
| `docs/refusals.md` — the Edit path | `WriteSupport.RunEditAsync` writes `Refusals.Of` | `MapEdit.RunAsync` writes a `Refusal` — `src/PgmStudio.Api/Services/MapEdit.cs:53`. `WriteSupport` has exactly two members and neither is this. `docs/architecture.md` already named `MapEdit` correctly, so the two root documents disagreed |

### A rule family missing from the table that claims to list them all

`docs/refusals.md`'s *The rule ids* table listed 17 families. **`PT` was absent** — `PT1`
(`SurfaceBlockBuried`) and `PT2` (`MaterialMissing`), owned by
`PgmStudio.Minecraft.Painting.TerrainThemeRules`, both answered by `GET /api/rules?family=PT`. A row has been
added.

### Stale counts

| Where | Was | Is | How measured |
|---|---|---|---|
| `refusals.md`, `architecture.md` | `rules.md` states **92** layout rules | **96** | `grep -cE '^\- \*\*` over `docs/generator/rules.md` |
| `refusals.md`, `architecture.md` | the catalogue answers **34** | **40** | `GET /api/rules`, rows whose owner is `docs/…` |
| `architecture.md` ×4 | **77** rule constants in **14** families | **129** in **18** | `GET /api/rules`, rows whose owner is a type |
| `refusals.md`, `architecture.md` | raised from **97** sites | **178** | `grep -rn "new Finding(" src/` |
| `architecture.md` | **149** endpoint classes over **45** files | **219** over **59** | `grep -hoE '\b(Get\|Post\|Put\|Patch\|Delete)\("' src/PgmStudio.Api/Endpoints/*.cs` |
| `architecture.md` | **118** paths, **149** operations, **291** schemas, **257** described | **165** · **219** · **371** · **337** | live OpenAPI |
| `architecture.md` | **67** POST/PUT/PATCH routes, **64** with a body | **92** · **89** | live OpenAPI |
| `architecture.md` | **seven** routes publish a truthful 204 | **nine** | live OpenAPI |
| `architecture.md` | **six** `image/png` routes, **three** `text/plain` | **fifteen** each | live OpenAPI |
| `architecture.md` | **26** fields publish a word-set enum | **29** | live OpenAPI |
| `architecture.md` | **110** answers carry `warnings`, **151** name the header | **167** · **219** | live OpenAPI |
| `architecture.md` | **1,027 of 1,032** answered fields described | **1,520 of 1,537** schema properties | live OpenAPI |
| `refusals.md`, `architecture.md` | **95 of the 149** operations declare a refusal code | **156 of 219** | live OpenAPI |
| `refusals.md` | **twenty-one** routes answer a list at the root | **twenty-six** | live OpenAPI |
| `refusals.md`, `architecture.md` | the Edit tool's **thirty-six** write routes | **twenty-two** | `grep -rn "MapEdit.RunAsync" src/PgmStudio.Api/` |
| `project-structure.md` | `Export` is **seven** files | **fourteen** — as the census table 120 lines above it in the same document already said | `ls src/PgmStudio.Export/*.cs` |
| `project-structure.md` | `Api` has **41** endpoint files and **21** services | **59** and **45** — likewise | `ls` |
| `project-structure.md` | `tools/` is **70 files, 18,365 lines**; **four** are real `.csproj` projects | **89 files, 21,668 lines**; **one** is. The same section said "One project-based tool" three lines later | `find tools -name '*.csproj'` |
| `project-structure.md` | **"There are seven, and the count is the point"** — the file-based scripts | **eight**. `tools/seed-trees.cs` carries a `#:project` directive, is built by `build-scripts.sh` and is documented in `docs/tools/library.md`, and was in neither the count nor the list | `grep -rl '^#:project' tools/` |
| `project-structure.md` | `*Row` POCOs, **40** tables | **42** | `grep -c "class .*Row\b" src/PgmStudio.Data/Schema/Entities.cs` |
| `client/routing-and-ia.md` | `kind` is `styles\|themes\|roofs\|storeys\|porches\|houses` | eight kinds — `trees` and `boulders` route too. `docs/tools/library.md` said "Eight kinds" correctly, so the two documents disagreed | `LibraryKinds.All` |
| `tools/capabilities.md` ×2 | **forty-eight** worked plans in `tools/seeds/` | **forty-nine** | `find tools/seeds -name '*.plan.json'` |

`./tools/census.sh --check` still passes after the edits.

---

## Reported, not applied

These are in `src/`, and this work left the studio's source untouched. Each is a comment or a UI string, not
behaviour.

| Where | Says | Is |
|---|---|---|
| `src/PgmStudio.Domain/RuleCatalog.cs:44` | *"`rules.md` states 92"* | 96 |
| `src/PgmStudio.Api/Endpoints/Complaints.cs:84` | *"the **seven** rules read off the rasterized spans"* | **eight** — `SketchLayoutCheck.GroundRules` lists `SK9`, `SK10`, `SK11`, `SK13`, `SK14`, `SK15`, `SK16`, `SK23`. `docs/refusals.md` says "eight" correctly; the code comment is the stale one |
| `src/PgmStudio.Client/Features/Library/LibraryChooser.razor:10` and the `LibraryKinds` docstring, `library.css:84`, `TerrainLibraryClient.cs:84` | *"Six libraries, in the order they compose"* | **eight** cards render. Trees and Boulders were added and the heading was not |
| `src/PgmStudio.Client/Features/Configure/ConfigurePhases.cs:12-15` | *"each objective kind gets its own phase and every one of them is offered on every map"* | only `wools` and `cores` have phases; `ObjectiveSlices` names three and `IsObjective` returns true for two. `docs/tools/configure.md` states the truth — here the doc is right and the code comment overstates |
| `src/PgmStudio.Minecraft/Render/WorldReadCatalog.cs:27-32` | the `render/topdown` summary — **published verbatim as the OpenAPI operation summary** — lists `ground`, `structure`, `foliage`, `objectives`, `combined` | the enum has **six** words including `made`, and the endpoint's `QueryWord` publishes all six. The served summary is missing a subject the parameter accepts. `docs/world-scan/read-backs.md` lists `made` correctly |

---

## Left alone, with the reason

| Where | Claim | Why not touched |
|---|---|---|
| `docs/tools/flow.md` | *"349 of 425 in this one"* — maps at `edit` on a development checkout | Explicitly about one machine's database. Unverifiable here, and not wrong in principle |
| `docs/tools/flow.md` | *"Twenty-five of the studio's write endpoints take one shape and fourteen take the other"* | The two sub-populations are not defined in the text, so the claim is not checkable as written. **89** operations publish a request body, which the stated pair does not sum to — worth restating, but a restatement needs the author's intent |
| `docs/world-scan/read-backs.md` | *"Nine renderers sit in …"* | "Renderers" is not a file count. `WorldReadCatalog.All` holds 15 reads; the number corresponds to nothing countable, but which thing it meant to count is a judgement |
| `docs/generator/evaluator.md` | cites `G37`, `G39`, `G40`, `G42`, `G44`, `G45` as rule ids | `docs/generator/rules.md`'s `## G` section states `G1`–`G8`. `G` is the one prefix that is both a rule family and a board prefix, so these read as board ids that no longer exist. **Whether they are rules that were never written or tasks that were done is the author's to say**, and `evaluator.md` is under the generator track's own correction protocol |
| `docs/generator/rules.md` | forward-references `G24`, `G29`, `G36` | Same protocol. `rules.md` is *"amended only by its own correction protocol"* |
| `docs/generator/audit.md`, `vocabulary.md` | cite `B42` as provenance | Provenance citation of an id that is on no board. `CLAUDE.md` permits citing an id for provenance; whether this one existed is the author's to settle |

**One class of error was looked for and not found.** Every task id cited in `docs/` as a *gap* — the
`Limits`-section citations `CLAUDE.md` calls *"a debt with a due date"* — checks out: `B107` is `[~]` in
`TODO.md`, `N12` is `[~]` in `BACKLOG.md` with exactly the destroyables half open that `configure.md` and
`edit.md` claim, `G145`/`G146` are in `docs/generator/ideas.md`. Of 115 doc-cited ids that have shipped, not
one is framed as a gap.
