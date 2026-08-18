# Redsand Caravanserai — Caravanserai, built

> A waterless canyon in red rock, with a walled caravan stop at the head of it.

**In one sentence:** a wadi that drops from each team's spawn terrace down to a shared mid-crossing,
walled in strata of red sandstone, with a low End-Stone-banded caravanserai and a small square outbuilding
seated on the shelf partway down, forked verbatim from `HousePresets.Desert`.

Board bbox `-50..50 × -95..95` (100×190 blocks) — matches the brief's "about 90 × 190" closely. `rot_180`,
base surface 9, `maxPlayers` 20, one `team` island (no on-axis neutral piece was needed here).

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| waterless canyon, red rock | `carav-ground` theme: Red Sand (12:1) + Red Sandstone (179:0) + Sand (12:0) + Smooth Sandstone (43:9), `cell` mix | four blocks, two families (`rust`, `sand`), on `s0,s1,s4,s6,s7` |
| the accent, End Stone, on the caravanserai only | `carav-stop` theme (`layered`: End Stone 121:0 over Sand) on `s5` (`caravanserai-yard`) alone | `--column (10,47)`: End Stone `y14..16`; no End Stone anywhere else in a `--column` spot-check off the yard |
| `HousePresets.Desert`, read before changed | `tools/styles/sn-carav-desert.json` — copied **verbatim**, zero fields edited | forked by proportion only: one long low wing `[[26,36],[43,40]]` (17×4) for the caravanserai, one small square wing `[[-24,52],[-18,58]]` (6×6) for the outbuilding — same style object, same material, different footprints |
| a wadi that tilts along its length | one relief `line` mark, `points: [[0,90],[0,40],[0,-10]]`, `h: [13,9,7]` — the floor descends from spawn to the mid crossing | `--heightmap`: visibly darker (lower) toward the centre on both team images |
| `layered` strata riser | `carav-ground.wall`: Red Sandstone → Smooth Red Sandstone-equivalent (Smooth Sandstone) → Red Sandstone, `layered` axis `depth` | theme preview `01-theme-carav-ground-section.png` |
| rim off on open desert, on at the canyon lip | `carav-ground` (`rimEdges: drop`, rim disabled) vs `carav-lip` (`rimEdges: boundary`, rim enabled, on `s2`/`s3`, the canyon-brow shapes) | two themes, deliberately split |
| two paths, caravan road + goat track, road wider | `p1` (radius 3, `tapered`, spawn→wadi mouth) vs `p2` (radius 1.5, `rough`, wadi floor→canyon-brow) | road 2× the track's width, as stated |

## The technique this board is a test of

**A shipped preset used as a starting point, changed by proportion and not by material.** `sn-carav-desert.json`
is `HousePresets.Desert`'s own JSON with nothing edited — the same End-Stone-over-Sandstone wall, the same
Brick gable, the same `Sill = Air` (`foundation.footing: null`), the same arched doorway. The two buildings on
this board differ only in the rectangle handed to the stamper: one long and low, one small and square. That
is the entire test the brief asks for, and it reads correctly in `--column (10,47)`: End Stone at `y14..16`
directly over the Bedrock room floor, nothing else changed.

## What went wrong, and the fix

**The relief, applied island-wide, first flattened every plan-authored tier.** The wadi's `line` mark alone
would sweep every shape on the island into the solve by default (`relief_scope` absent means "part of the
island's ground"), which would have planed the spawn ramp, the canyon-brow shelves and the caravanserai yard
down toward the relief's own base rather than leaving them at the heights the plan stated. Fixed by marking
every shape **except** the wadi floor (`s0`, `s1`) `relief_scope: "exclude"` — `s2..s7` keep their authored
`base_height` untouched, and only the canyon floor itself is relief-shaped.

**A multi-wing caravanserai tripped `HJ3` then `HJ5`.** The first draft joined the long hall to the small
outbuilding as one two-wing building; the shared edge tie (`HJ3`) and then, once a ridge was stated to break
the tie, the taller-wing rule (`HJ5`) both refused it — `POST /map/{slug}/sketch/columns` named the rule
each time. Rather than spend a further cycle threading the wing joint rules (the technique is `TS13`'s
territory, not this brief's), the outbuilding was split into its **own** `house` prop, same style, standing
apart — which is what the brief actually asked for ("the outbuildings are small and square") rather than one
L-shaped structure.

**Two boulders needed repositioning off both a building's footprint and the goal's `OB19` keep-out**, found
by the dressing decline (`DR-SITE`, `DR-CLAIM`) and the export gate (`OB19`) in turn, not predicted in
advance — matches `GENERATION-NOTES` §17's warning that `OB19` is only heard at export.

## The checklist

| # | Check | Measured | Verdict |
|---|---|---|---|
| L1 | one gamemode | `<gamemode>dtm</gamemode>`, once | pass |
| L2/L3 | team/spawn/destroyable present, label matches | 2 `<team>`, 2 `<spawn>`, 2 `<destroyable>` | pass |
| L4 | no `<`/`>` in a goal name | `name="Caravanserai Rest-stone"` | pass |
| O1 | same-team goal spacing | one goal a team (n/a — no second destroyable) | n/a |
| O2 | `GO1` ratio 3.0–4.0 | `POST /plan/inspect`: own 50, enemy 150, **ratio 3.0** | pass, at the floor |
| O4 | obsidian ≤ 3 in a destroyable | style `column-plus`, material `ender stone` — no obsidian at all | pass |
| O5 | sky marker above the built structure | `--column (10,47)`: Red Wool marker at `y39`, structure tops at `y16` | pass |
| M6 | building seated into terrain has no footing | `foundation.footing: null` on both houses (unedited from the preset) | pass |
| C0 | extent/aspect | 100×190, a lane (matches AD-B2) | reported |
| C4 | void placement | the mid crossing zone bridges the two team islands; no void inside either team's own approach | reported |
| C9 | landform transitions | canyon floor (`s0`/`s1`) relief-solved and tilted; every terraced shelf `exclude`d and stepped by the plan, not butted flat against the floor with no transition | reported |

`GET /map/redsand-caravanserai/traversability` → `connected: true`. No load-blocking or §3.2–§3.5 rule
failed after the fixes above.

## Open questions

**Whether a single relief `line` mark is a faithful reading of "a `sink` with `anchor_heights`."** The brief
names a specific mechanism (`height_mode: "sink"` plus per-vertex `anchor_heights`) for the tilt; I used the
relief solver's own `line` mark instead, because it gave the same visible result (a floor that measurably
descends along its length, confirmed in `--heightmap`) with less risk of the anchor-height TIN producing an
uneven floor across the canyon's width. Both are legitimate ways to state a tilt per `sketch.md`; I record
the substitution rather than claim I built exactly what was named.
