# 08 — a cliff, and the two ways up it

**The technique: a `scarp` mark. It is the only mark that states a *grade* rather than a height, and the
grade is what decides whether ground is walked, climbed with one block, or not crossed on foot at all.**

The plan is `02-theme`'s. The finish puts the back half of each island eleven blocks up and draws the face
between the two halves.

## A scarp is two bands, not one line

Every other mark pins a patch to a height. A scarp pins **two bands, one either side of a drawn line, and
leaves the face between them free** — so what is actually authored is the fall, and the solver puts a face
there because it has no choice.

```json
{ "id": "scarp", "kind": "scarp",
  "points": [[-40,58],[-14,56],[14,57],[40,55]],
  "high": 20, "low": 10, "face": 3, "band": 5 }
```

| Field | Is |
|---|---|
| `points` | the line the face runs along |
| `high` · `low` | the height of the band on each side of it |
| `face` | how wide the unpinned strip between the bands is — **the run the fall happens over** |
| `band` | how wide each pinned band is |

`ScarpMark.Grade` is `|high − low| / face`, and that is the number the mark is really choosing: **10 over 3
is 3.3 blocks of rise per block of run**, which is a cliff. The same ten blocks over a `face` of 10 is a
bank a player walks up, and over 20 it is a slope nobody notices. One field is the difference.

Measured on the built face, five blocks west of the ramp:

```
GET …/column?at=-38,z        z 54  y  9      z 58  y 15
                             z 56  y 11      z 60  y 19      ← 10 blocks in 6, two single steps of 4
```

## The band is what makes the cliff hold

Without `band`, a scarp is two lines and the relaxation is free to slope away from them on both sides — the
cliff becomes a soft step within a few blocks. `band: 5` pins five blocks of level ground at the top and five
at the bottom, so the face has a lip above it and an apron below it and reads as a break of slope rather than
as a fold.

**A band stops where its line stops.** Perpendicular distance alone would wrap a half-disc round each end of
the drawn line, which for a scarp means the cliff closes over the gap beside it — and the gap is usually the
whole reason the line was drawn to end there. `ScarpMark.Pins` skips a cell whose nearest point on the line
is an endpoint, so a scarp can be a wall with a gate in it.

## The two ways up are two line marks

A cliff with no way up is a board in halves, and the export gate will not say so — the walk models a player
who can place blocks (`05-steps`). The ways up are authored, one per flank:

```json
{ "id": "ramp-w", "kind": "line", "points": [[-33,46],[-33,56],[-33,66]], "h": [10,15,20], "r": 3 }
{ "id": "ramp-e", "kind": "line", "points": [[ 33,46],[ 33,56],[ 33,66]], "h": [10,15,20], "r": 3 }
```

A line mark's `h` is **one height per vertex**, interpolated along its arc — so one stroke is a way up that
climbs as it runs. `r` is a **radius**: the band written is six blocks wide, not three.

Five blocks apart, the face and the ramp read completely differently:

```
the face  x=-38   z 44:8  46:9  48:9  50:9  52:9  54:9  56:11  58:15  60:19  62:19
the ramp  x=-33   z 44:9  46:9  48:10 50:11 52:12 54:13 56:14  58:15  60:16  62:17  64:18  66:19
```

Every rise on the ramp is 0 or 1. That is the measurement, and there is no gate that takes it.

## Order is the mechanism, not a detail

Marks resolve in order and **the last one wins a contested cell**. The list is written:

1. `coast` — the rim, first, so nothing later cuts a doorway through the shore
2. `strand` — the frontline bank, held at 9 so both sides of the strait stay at bridging height
3. `upland` — an `area` mark holding the back half at 20
4. `scarp` — the face, drawn across the front of that upland
5. `ramp-w`, `ramp-e` — last, so where a ramp crosses the scarp's own bands the ramp wins

Reorder 4 and 5 and the scarp overwrites the two ramps and the board has no way up. Nothing complains.

## `reach: 0` here, and why

`reach` is how far a statement travels before the field falls back to `base`. On `07-hill` it is 20, which
makes each hill a local landform with plain ground between. Here it is **0 — unlimited** — because the whole
island is one statement: an upland, a face and a shore, with nothing that should be allowed to relax back to
9. A finite reach would have pulled the middle of the upland down toward the base and left the `area` mark
holding only its own ring.

## What to look at

| Picture | Says |
|---|---|
| `GET …/render/section?axis=z&at=-33&from=14&to=112&scale=6` | the ramp, in the one view a grade exists in |
| `GET …/render/section?axis=z&at=-38&from=44&to=72&scale=10` | the face, five blocks away, in the same cut |
| `renders/world-heightmap.png` | the two tiers and the notch each ramp cuts in the face |

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **0**, `valid: true`, no lint |
| `POST …/sketch/relief/read` | cells 4 125 · low 8 · high 20 · relief 12 · symmetry error 0 |
| grade | face **3.3** blocks per block · ramp **0.5** |
| `GET …/preflight` | export gate **OPEN** |

## What went wrong first

The first build wrote the scarp as `{"h": [20, 10], "width": 4}` — the field names a `line` mark uses. A
scarp takes `high`, `low`, `face`, `band`, and the two it did not recognise were simply not read: `High` and
`Low` defaulted to **0**, and the mark pinned the middle of the board to bedrock. The relief read-back said
`low=0 high=20 relief=20` and the export gate stayed **OPEN**.

Nothing named the field. `RQ3` names an unread field on a *posted document's* own path, and a relief mark's
inside is resolved past that walk. **Check a relief against `POST …/sketch/relief/read`'s `low` before
building** — a `low` that is not roughly the `base` is a mark that did not land.
