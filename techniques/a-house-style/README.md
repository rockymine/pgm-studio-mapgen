# A house style

**A `HouseStyle` is the other half of a building, and it is the half the plan says nothing about.**
`techniques/a-house-and-its-wings` varies the plan — which rectangles, meeting how — and holds one style
still. This card does the reverse: twelve pads, the same 12 × 8 rectangle at the same place on every one,
and **one field of the style changed** on each. So a form, a pitch, an overhang, a window or a storey reads
as itself rather than as part of a building somebody designed. Open it in the studio as
`technique-a-house-style`, or run `build.py`.

The base is `bothy`, taken whole from `specs/opus5-glassmere` and shared with the wings card, so the two
read against one another.

| Panel | The one field | Ridge | Eaves | What it is |
|---|---|---|---|---|
| `gable` | — the base, unchanged | y24 | y18 | two slopes to a ridge, ends closed by a wall |
| `flat` | `roof.form = "flat"` | y18 | y18 | no ridge: the middle and the eaves are one course |
| `hip` | `roof.form = "hip"` | y24 | y18 | the gable's own section, with its **ends** sloped in too |
| `gambrel` | `roof.form = "gambrel"` | y25 | y18 | a slope that breaks on the way up, so it rises further |
| `shed` | `roof.form = "shed"` | y26 | y32 | one slope: the high edge is at a wall, not in the middle |
| `saltbox` | `roof.form = "saltbox"` | y24 | y18 | a gable with one side carried further down |
| `pitch-1` | `roof.pitch = 1` | y21 | y18 | the gable's shape, three courses shallower |
| `overhang-3` | `roof.overhang = 3` | y24 | y18 | the ridge unmoved; what changes is past the wall |
| `windows-none` | `windows.form = "none"` | y24 | y18 | a knob that removes rather than changes |
| `windows-arched` | `windows.form = "arched"`, `windows.block = 134` | y24 | y18 | **two fields, because they are one decision** |
| `no-beams` | `beams.any = false` | y24 | y18 | no log ends past the corners |
| `one-storey` | `storeys` cut from two to one | y19 | y13 | the whole building five courses shorter |

Every pad solves to the same ground — the yard tops at **y7** on all twelve — so the heights compare.

## A roof form is a height and a material before it is a shape

**`flat` is the one that answers the same course at its middle and at its eaves.** Everything else rises
between the two, and how far is the form: a gable reaches y24 over eaves at y18, a gambrel y25 because its
slope breaks and steepens, a `pitch-1` gable only y21.

**`shed` is the one whose high edge is not in the middle.** It slopes one way, so the column at the house's
centre is partway up the slope and the tall side stands at a wall — which is why its "eaves" figure above
is the largest number in the table rather than the smallest.

**`overhang` changes what stands past the wall and not the ridge.** `overhang-3` reads the same y24 as the
base. It is the one roof knob that cannot be seen in a ridge column at all.

## A hip and a gable are the same cut across, and differ along

**A section across the ridge cannot tell them apart.** Both answer y24 at the middle and y18 at the eaves,
and `sections.txt`'s two cuts are the same picture twice.

**Along the ridge they are not the same building.** `ridges.txt` carries both: a gable closes its ends with
a wall carried straight up to the ridge, and a hip slopes them in the way it slopes its sides. Four courses
of `H` standing vertical against four courses stepping inward.

**So a roof form read from above, or from one cut, is a form half-read.** `gable-along.png` and
`hip-along.png` are the pair, and the plan view of the two is identical.

## What the gate refuses, and it refuses at the door

**All three `HS` rules answer the `PUT`, at 400, naming the JSON path.** Nothing here waits for a finish or
an export — a style is checked when it is stored, which is the cheapest place a refusal has been found in
this repository.

**A window's form and its block are one decision.** `HS1`: *"windows.block (102) is not a stair. The form
turns its corners by a stair's own facing."* `arched` and `stairLattice` are built out of stairs, so
changing the form without changing the block refuses — which is why the `windows-arched` panel is the one
place this card changes two fields.

**A frame is one wood.** `HS4` refuses beams of one timber over posts of another, and it names **every**
site at once: `post`, `storeys[0].post`, `storeys[1].post`, and the wall's laid log. *"A post, the beam
ends docking against it and the course they are the ends of are one frame, so they are cut from one wood."*

**Beams want something to be the ends of.** `HS9`: *"the building lays beams of spruce and no course of any
of its walls is a laid log, so the ends run out of masonry with no timber behind them."* The base style's
laid-log course is in `storeys[1].wall` — not in the roof's verge, which also uses one — so stripping the
verge alone does **not** trip it, and `refusals.txt` had to strip both.

## The recipe

- **change one field at a time and look at a section.** A roof form is invisible from above and every
  shipped roof fault in this repository was visible in a cut.
- **cut along the ridge as well as across it.** A hip and a gable are the same section across.
- **a window's form implies its block.** `arched` and `stairLattice` need a stair; `pane` needs a pane.
- **keep the frame one wood.** Beams, posts, every storey's post and the laid-log course are one timber,
  and `HS4` names all four when they are not.
- **`beams.any` needs a laid log somewhere in the style** — a storey's wall or the roof's verge. Dropping
  the last one and leaving the beams is `HS9`.
- **a storey is the coarsest knob there is.** Cutting one took this building from y24 to y19; nothing about
  the roof changed.
- **read the style back rather than the prop.** The dressing pass placed all twelve of these with no
  decline, so a building that came out wrong is a style question and not a siting one.

## Limits

**One plan, deliberately.** Every pad is the same rectangle, so nothing here says what a style does over
two wings, a lower wing or a projecting one — that is `techniques/a-house-and-its-wings`, which holds the
style still for the same reason.

**No porch and no doorway panel.** `porch` is null on the base style and `doorway` is one more field with
its own vocabulary; both are reachable and neither is worked here.

**The foundation is untouched.** What a building stands on, and what `WX11` says about a stamp standing
proud of its ground, belongs with the structures rather than with the style.

## What checks it

- `sections.txt` — every house cut **across** its own ridge, which is where a form is seen.
- `ridges.txt` — the yard, the ridge and the eaves column of each, and the gable-against-hip pair cut
  **along** the ridge instead.
- `refusals.txt` — `HS1`, `HS4` and `HS9`, each one field off the base, with what the `PUT` said.
- `a-house-style.layout.json` — twelve pads, twelve styles and twelve one-rectangle props.

Renders, off the **built** world: `row1.png`, `row2.png` and `row3.png`, each row cut along x through all
four of its houses; `gable-along.png` and `hip-along.png`, the pair a cut across cannot separate; and
`board.png` from above, where none of it can be told apart at all.
