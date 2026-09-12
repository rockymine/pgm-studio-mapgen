# Sable Reach — two trading posts across a tidal mouth

**In one sentence:** two rival trading posts face each other across a tidal river mouth, each holding
its wool in a dockside warehouse behind a seawall, with the mudflats and a single low bridge deciding
who controls the crossing.

200 × 230 blocks, `rot_180` about the origin, 16 players a team, base surface 12 (quay 9, skerry 7),
build ceiling 46. Two landmasses a side — a main settlement island and a flanking dock skerry — joined
by a short build zone; the two teams' islands are joined only by a 30-block tidal channel, crossed by a
permanent causeway and a pair of sand fords. `POST /map/from-documents` → 200, export gate **OPEN**,
dressing pass **0 declines** (41 props placed).

## Where the brief's pieces are

| The brief asked for | Where it is | Measured |
|---|---|---|
| two landmasses a team, joined by a short build zone | `warehouse` (main island, x ±50, z 30–65) and `skerry` (x 65–100, z 30–70), joined by the `skerry-link` zone at x 50–65 | `plan/ascii`: warehouse ends cell 10, `skerry-link` zone cells 10–13, `skerry` starts cell 13 — no gap, no overlap |
| a build zone inside the team's own site | `plaza-yard` zone, x −15..15, z 40..55, laid directly over the warehouse's own solid ground | a normal build region stated on land rather than void (`WL1` allows it: "a build zone may overlap terrain by design") |
| a single bridge, the primary chokepoint | `bridge` shape, x −4..4, z −15..15, `height_mode: level`, `skirt: 0`, `keepClear: true`, flush with the quay at y8 | `render/section?axis=x&at=0` shows one low causeway crossing the void at the centre |
| a secondary, shallower route | `ford-a-sand` (x −25..−15) with `ford-a-mud-w`/`-e` fraying its edges, auto-fanned by `rot_180` to a second ford at x 15..25 | two ford crossings, one near each team's own skerry flank |
| estuary shore, sand then mud | `estuary-shore` theme (sand core) on the ford's centre, a `material`-override mud/gravel `cell` pattern on its edge bands | `05-themes.txt`: `estuary-shore` 960 cells, bordering `sable-town` over 64 cells |
| dockside seawall, diagonal pattern, team accent | `sable-town` theme: `wall` bucket is `wallDiagonal` (cobble/andesite/stone brick), `rim` bucket is `teamTint` (159, stained clay) | `05-themes.txt` lists `159:11 Blue Stained Clay` in the town paint; the quay's south face is the seawall |
| timber warehouse + cottage, one preset forked | `WAREHOUSE_STYLE` (gable, wall extent 8) and `COTTAGE_STYLE` (hip, wall extent 5), both `timber_style(...)`, same wall/roof/post shape | 5 houses stamped, both wing plans and sections rendered in `renders/house-*.png` |
| stony/wood-dirt path triads | `path-quay` (Gravel/Andesite/Cobblestone) on the quay; `path-spine`/`path-wool`/`path-skerry` (Dirt/Coarse Dirt/Spruce Planks) elsewhere | `06-claims.txt` shows the paved spine down the island's centreline |
| one wool a team | `wools: [{"id": "wool-1", ...}]`, no `destroyables`/`cores` | `<gamemode>ctw</gamemode>`, one `<wool>` a team in `map.xml` |
| accessibility check | `GET /plan/flow`: attacker 194 blocks to the enemy wool, defender 32 — a long match, but one connected road, no forks lost | `preflight`: traversability connected, 0 isolated |

## The two ways across are not the same way twice

The bridge sits dead centre and is the short way: flush with both quays at y8, `keepClear` so nothing
repaints or blocks it, 8 blocks wide. The fords sit off to each team's own flank (mirrored, so each side
gets one near its own skerry) and are a course lower — a sandbank you walk onto rather than a built
span, with a narrower mud fringe (a `material`-override `cell` pattern of coarse dirt, gravel and clay)
fraying into the water on both long edges. Defending the bridge does not defend the ford, and the ford
is the harder route to watch because it is not where a defender's eye goes first.

**The channel is genuinely a strait, not a field.** `CT12`'s check on the plan (30 blocks, band 15–40)
still measures the *bare* gap the pieces leave; the bridge and fords are hand-authored on top of it and
the plan gate cannot see them, which is why the stored map answers back with a complaint rather than a
refusal: *"the plan put team islands 30 blocks apart and the drawn board joins them into one landmass —
the strait the plan was checked against is not in the ground."* That is exactly what was intended — a
strait with two built crossings, not an unbridged one — and the complaint is the system correctly saying
so rather than a fault.

## What the ground is made of

Three themes, one per kind of ground:

| Theme | On | Says |
|---|---|---|
| `sable-town` | quay, warehouse, spawn, wool room, rear, the bridge | built: a `cell` mottle of gravel/andesite/cobble, a `wallDiagonal` seawall of cobble→andesite→stone brick, a `teamTint` rim |
| `sable-skerry` | the flanking dock skerry | its own thing: a `cell` mottle of coarse dirt/gravel/gravel/clay, andesite walls, gravel fill |
| `estuary-shore` | the two fords | sand core (`cell` of sand/sand/sandstone), mud-and-gravel edge bands stated as a shape-level `material` override rather than a second theme |

The quay steps down 3 blocks to the water; most of its 100-block frontage is a plain retaining wall
(the seawall), and the one graded way down — a `level` polygon with a per-vertex tilt, `anchor_heights
[9, 9, 12, 12]` over 10 blocks — is `town-stair`, the single stair a defender can watch.

## The buildings

Two styles, one fork: `timber_style(wall_extent, roof_form, ...)` builds both from the same recipe —
Log corner posts, a `laidLog` verge (never a bare standing log, `HS3`), two courses of laid log, one
checker course of two log species (oak/spruce, never the same species twice), then plain spruce planks
up to the eaves. The warehouse is gable-roofed at extent 8; the cottage is the same wall recipe hipped at
extent 5 — a roof-and-proportion variant of one fork, not a second design. Neither states a `footing`.
No `RoofForm.Shed` anywhere. The wool room and the spawn hall are stamped in the warehouse style, so the
wool genuinely reads as sitting inside a dockside warehouse.

## What went wrong, and what it looked like

**`roomStyles.cage` is not a field.** The tools table says `{"cage": …, "spawn": …}`; the DTO
(`SketchRoomStylesDto` in the live `openapi.json`) has `{"wool": …, "spawn": …}`. Posting `"cage"`
answered a 200 with `RQ3` naming `layout.roomStyles.cage` unread, and the wool room built in the studio's
own default shell rather than mine — a silent miss, since a theme/style is a snapshot `RQ3` cannot see
inside further than the top key. Fixed by reading the live schema rather than the doc's table.

**A shape cannot carry both a `theme` and a `material`.** `SK24` refused the ford's mud-edge shapes
outright when they stated both — the two answer the same question (what paints this shape), and stating
both is not "belt and braces," it is a contradiction the studio catches before building anything.

**A bare `Log` verge is refused, not silently accepted.** `HS3`: a verge is the one course that has to
lie along the roof's own ridge, so it wants `laidLog`, not a standing `solid` log — caught before the
first build rather than found as a graphical fault afterward.

**The frontline was 100 blocks wide on the first pass and `FR6` refused it.** A CTW frontline is capped
at 16 cells (80 blocks) unlike a destroy board's, which has none — narrowing the `mid-band` zone to dock
only the centre of the quay (and leaving the quay's own outer flanks facing plain, un-zoned void) fixed
it and also brought `CT12`'s strait into its 15–40 band, which a 50-block first draft had missed by more
than the fix needed to buy back.

**`meta.authors` never landed.** `POST /map/from-documents`'s own schema documents `authors` as a top-
level array, applied *after* the intent projection for exactly the reason it would otherwise be
overwritten, and posting it drew no `RQ3` — yet the stored intent's `meta.authors` reads back `[]`, and
`EX6` still complains the observer's authors board is blank. Filed as an open finding rather than
patched around; see the report for what was checked before calling it a gap.

## Coverage, honestly

`GET /coverage` reads 37.2% dead ground (8 925 of 24 000 cells), concentrated in the flanking filler
pieces that exist only to keep the rectangle contiguous around the wool room and the back band — the
biggest patches are at `(-34, -77)`, `(33, 75)`, `(-40, 87)` and `(39, -89)`, all one block from used
ground rather than stranded. Two path spurs were added late to cut into the worst of it (`path-wool-
flank-w`/`-e`), and it still reads high. This was not chased further than that; the honest reading is
that the flanking bands are backdrop rather than fully worked ground, and a further pass would narrow
them rather than dress them.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| red wool room | `x -30..0, z 95..115`, marker `(-15, 12, 105)` | stamped in the warehouse style, floor y11 |
| red spawn | `x -35..-5, z 65..85`, marker `(-20, 12, 75)`, facing front | door opens toward the warehouse |
| bridge | `x -4..4, z -15..15` | flush y8 with the quay, `keepClear` |
| ford A | `x -28..-12, z -15..15` (auto-fanned to `x 12..28`) | sand core y7, mud edges |
| red skerry | `x 65..100, z 30..70` | its own theme, joined by `skerry-link` zone at `x 50..65` |
| plaza-yard | `x -15..15, z 40..55` | a build zone stated over solid warehouse ground |
| town-stair | `x -6..6, z 25..35` | the one graded way from the quay (y8) to the town (y11) |
| largest barrier face | `x -50..-7, z -31..-30`, 88 cells | the un-ramped stretch of the quay-to-town seawall |
