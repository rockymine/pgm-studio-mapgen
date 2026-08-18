# Gantry Quarter Works — Gantry Quarter, built

> An industrial yard in three registers that never mix: brick for the buildings, iron and dark stone for
> the machinery and retaining walls, pale gravel for the open yard.

**In one sentence:** a two-team core board where each side defends two cores at opposite heights — a raised
gantry deck and a sunk pit, 75 blocks apart — behind a hand-placed row of six brick workshops that share two
frontage lines and no two of which are the same size.

Board bbox `-60..60 × -115..115` (120×230 blocks) — matches the brief's 120 width but is well past its
"about 160" length; see *Open questions*. `rot_180`, base surface 9, `maxPlayers` 20, gamemode `dtc`.

## Where the brief's things are

| The brief said | Where it is | Measured |
|---|---|---|
| brick for buildings | `sn-gantry-block` (forked from `workshop`, id 10): wall Bricks (45:0) + Hardened Clay (172:0), roof Bricks/Hardened Clay | six houses `h1..h6`, all this one style |
| iron and dark stone for the machinery | `gantry-works` theme: `layered` Stone Bricks/Iron Ore/Stone Bricks, on the two core shapes (`s0` pit, `s3` deck) | `--surface`: the two core platforms read as a distinct dark striped band against the grey yard |
| pale gravel yard | `gantry-yard` theme: Clay/Smooth Stone `cell` mix | `--surface`: the open floor between the buildings |
| a grid, authored by hand, ≥6 buildings, no two the same size | `h1..h6`, footprints (inclusive) `13×12`, `11×15`, `11×10`, `13×8`, `13×14`, `14×12` blocks | six distinct sizes; `h1`,`h3`,`h4`,`h6` share `z=15` as a frontage line, `h2`,`h5` share `z=12` as a second |
| both goals inside the works, different heights | `gantry-deck` piece surface 13 (4 above base), `pit` piece surface 5 (4 below base) | `--column`/`--heightmap`: deck platform raised, pit sunk, both inside the yard's own footprint |
| 35 minimum between the goals, aim 70 | core markers at world `(-37.5, 80)` and `(37.5, 80)` | straight-line 75 blocks; within band, at the "aim" figure |

## What the brief and `GO1` pulled against each other

Getting `GO1`'s 3.0–4.0 band and the brief's "about 120×160" at the same time did not work with this board's
shape. The first draft (a compact yard, cores close to the crossing) measured **2.23–2.83** — too low,
meaning the cores sat too close to the middle relative to spawn. Doubling the yard's depth (the run between
the mid-crossing and the cores) without moving the cores relative to spawn pushed both ratios into band —
**3.46** (deck) and **3.83** (pit) — but it also doubled the board's own length, landing at 230 blocks rather
than something nearer 160. I chose to keep the ratio inside its authored band over the extent figure, since
`GO1` is stated with a number and the extent is stated as "about"; the trade is recorded rather than hidden.

## The technique this board is a test of

**Two goals per team, not one.** `docs/pgm/destroyables-and-cores.md`'s corpus reading puts a second core
on 19% of core-carrying maps; this board deliberately takes that branch, reading "one on a raised gantry
deck, one in a sunk pit... keep 35 minimum between the goals and aim at 70" as `O1`'s same-team spacing rule
applied to two cores rather than a one-goal board with two *positions* described. `POST /plan/inspect`
reports a `goalDistances` entry for each core independently, which is what let both be checked against `GO1`
separately (3.46 and 3.83) rather than as one averaged figure.

**A deliberate grid, not a placed-by-feel row.** Six houses, each its own `house` prop with one wing, laid
out by hand at `z 12`/`z 15` frontage coordinates rather than nudged into place by eye — the two `HP3`
declines (`h5`, `h6` initially over the 192-block footprint cap) were fixed by shrinking the rectangle, not
by moving it off the grid line.

## What the board gets right, measured

- **Two goal heights read distinctly.** `--heightmap` shows the deck platform standing proud of the yard
  and the pit sunk into it, both still inside the same open works rather than dressed on as separate rooms.
- **The three-register rule holds under inspection**, not just by construction: `--surface` shows the
  buildings' brick roofs, the cores' iron/stone-brick platforms and the yard's ash floor as three visually
  distinct bands with no shape borrowing another's material.
- **`GO1` passed on the first build** once the yard was deepened — no further tuning cycle was needed for
  either core.

## The checklist

| # | Check | Measured | Verdict |
|---|---|---|---|
| L1 | one gamemode | `<gamemode>dtc</gamemode>`, once | pass |
| L2/L3 | team/spawn/core present, label matches | 2 `<team>`, 2 `<spawn>`, 4 `<core>` | pass |
| L4 | no `<`/`>` in a goal name | `Gantry Deck Core`, `Pit Core` | pass |
| O1 | same-team goal spacing ≥35, 70–75 good | 75 blocks, straight-line between the two markers | pass |
| O2 | `GO1` 3.0–4.0 | deck 3.46, pit 3.83 | pass |
| P2 | placed building ≥5×5 | smallest is `h3` at 11×10 | pass |
| C0 | extent/aspect | 120×230 — a lane, longer than named | reported |
| C1 | houses by z/x | two frontage lines (`z 12`, `z 15`), six distinct x positions | reported |
| C2 | placement ideas | the six-building grid is the only placement idea on this board — no second village, isolated house or landmark was added | reported |
| C10 | paths | 3: spawn→yard spine, spine→deck, spine→pit | reported |

`GET /map/gantry-quarter-works/traversability` → `connected: true`. No load-blocking or §3.2–§3.5 rule
failed.

## Open questions

**Whether "one on a raised gantry deck, one in a sunk pit" names two goals per team or one goal described
twice.** `docs/gameplay/approaches.md` does not address multi-core boards directly, and the corpus figure
in `capabilities.md` (one core in 77% of core boards) means a two-core reading is the less common shape. I
built two per team because the brief's own spacing numbers (35 minimum, 70 aim) match `O1`'s same-team-goal
language exactly, and a single goal has no second goal to be 70 blocks from. If the intended reading was one
goal whose *shape* has a raised and a sunk face, this board answers a different brief than intended, and
that is worth the author's word rather than my invention.

**Only one placement idea (the building grid) was authored.** `ART-DIRECTION.md` AD-S1 asks for at least
three distinct placement ideas generally; this brief's own text is unusually prescriptive about the grid and
silent about anything else, and I did not add a second idea (a lone landmark, a boundary run) to avoid
diluting the one thing the brief explicitly tests. Recorded as a gap against the general rule rather than
against the brief.
