# 26 — a lit room, and a floor halfway up it

**The technique: light, and height stated rather than found. A hall twenty-two courses under a meadow, with
a gallery running round it at mid-height, four kinds of emitting block set into its ceiling, its deck and its
floor — and the reason none of them is a prop.**

`24-underground` built a room under a hill and said what it could not do: *"A light source. There is none.
The gaol is dark."* That is half right, and this board is the other half. There is no lamp a **prop** can be —
`PlacedProp`'s six kinds are `stroke`, `water`, `tree`, `boulder`, `flora` and `house`, and none of them emits
(filed as `WE82`). But a **made thing** is drawn shape by shape at an absolute floor, and a shape themed to
glowstone *is* a lamp. So the light on this board is geometry, and it goes exactly where it is put.

The same sentence answers the other thing `24` could not do — *"a prop cannot be put on a ledge halfway up a
shaft"* (`WE83`). The gallery here is a floor at `y14`, and nothing seated it there.

## The board

`02-theme`'s plan with one number, as `20-undercroft` and `24-underground` have it — but deeper, because two
storeys of room need the depth:

```json
"globals": { "surface": 30 }
```

```json
"shapePropsByHeight": { "30": { "floor": 22, "base_height": 8 } }
```

Landmass `y22..29`. Rock `y0..21`. **Twenty-two courses** between the bedrock and the field, against
`24-underground`'s fourteen.

| | |
|---|---|
| extent | 100 × 100, `rot_180`, one spawn and one destroyable a side (`02-theme`'s, untouched) |
| the hall | `x −24..23`, `z −16..15` — floor `y0..5`, air `y6..21`, **16 courses** |
| the gallery | an even-odd ring, deck `y14..15`, band 12 wide east–west and 8 north–south |
| the well | `x −12..11`, `z −8..7` — 24 × 16, open the full 16 courses |
| under the gallery | `y6..13`, **8 courses**; over it `y16..21`, **6** |
| the descents | 14 treads, `y29 → y16`, one per team, landing on the gallery |
| the stairs | 10 treads, `y15 → y6`, one per team, gallery to well |
| the lamps | **128 emitting blocks** in four kinds — see below |
| the gates | `GET …/findings` **none**; `GET …/preflight` **export gate OPEN**; **0** declines |

## The four storeys, and why there are four

A layer keeps one span per column, so the deepest column decides how many layers the board needs. The
column at `(−17, −13)` — a torch standing on the gallery deck under the meadow — holds **four**:

| Layer | Order | Holds | The column at `(−17, −13)` |
|---|---|---|---|
| `under` | first (`below`) | the rock, the hall floor, the piers, the stairs, the brazier plinths | `y0` bedrock · `y1..5` floor |
| `gallery` | second (`below`) | the ring deck and the lanterns let into it | `y14..15` bricks |
| `lamps` | third (`below`) | the ceiling cross, the fires, the torches | `y16` torch `50:5` |
| `ground` | the compiled plan | the landmass, and the two descents cut through it | `y22..29` |

`drive.py`'s `below: true` does `layers.insert(0, …)` per entry, so the finish lists them **top-down** —
`lamps`, `gallery`, `under` — and the posted stack comes out `under, gallery, lamps, ground`, which is the
bottom-up order the painter needs.

## Light is a theme, and a theme is one block

A theme whose every band names one block paints exactly that block wherever a shape wearing it lands:

```json
"glow": {
  "bedrock": { "relative": false, "value": 0 }, "rimEdges": "void",
  "rim":     { "enabled": false, "depth": 1, "material": { "kind": "solid", "id": 89, "data": 0 } },
  "surface": { "enabled": true,  "depth": 1, "material": { "kind": "solid", "id": 89, "data": 0 } },
  "wallEnabled": false,
  "wall": { "kind": "solid", "id": 89, "data": 0 },
  "fill": { "kind": "solid", "id": 89, "data": 0 }
}
```

Four of them, and every one lands. Counted over the built world rather than over the document:

| Theme | Block | Where | Built | Read at |
|---|---|---|---|---|
| `glow` | Glowstone `89:0` | a cross set into the ceiling over the well, `y21` | **60** blocks | `(−8, 21, −1)` |
| `lantern` | Sea Lantern `169:0` | six 2 × 2 insets let into the gallery deck, `y14..15` | **48** blocks | `(−13, 14, −13)` |
| `fire` | Jack o'Lantern `91:0` | the top of each of four braziers, `y9` | **16** blocks | `(−10, 9, −6)` |
| `torch` | Torch `50:5` | four standing on the gallery deck, `y16` | **4** blocks | `(−17, 16, −13)` |

**The data value survives.** `50:5` is a torch standing on the block below it, and that is what
`GET …/column?at=-17,-13` answers:

```
y 16    50:5   Torch
y 15    45:0   Bricks
y 14    45:0   Bricks
```

So the studio can already write a standing torch, a sea lantern and a jack o'lantern; what it cannot do is
place one as a prop, which is the whole of `WE82`.

**A lamp is drawn where it is wanted, and stays there.** The `lamps` layer states no `seat`, and that is
deliberate: `seat: "ground"` reads the **highest** ground at each cell, which under a landmass is the
landmass. A made thing asked to seat inside this hall would land on the meadow at `y30..32`, not on the hall
floor — measured on a probe board and written up in `docs/tools/sketch.md`. **State the floors of anything
indoors absolutely.**

## The gallery: an even-odd ring at a stated height

The deck is one polygon — outer ring, slit inward, inner ring the other way round, closed — the shape
`24-underground`'s cell wall uses, here laid flat:

```json
{ "id": "ring", "type": "polygon", "operation": "add", "floor": 14, "base_height": 2, "theme": "gaol",
  "vertices": [[-24,-16], [24,-16], [24,16], [-24,16], [-24,-16],
               [-12,-8], [-12,8], [12,8], [12,-8], [-12,-8]] }
```

`y14..15`, so the hall reads as **8 courses under the deck and 6 over it**, and the well keeps all 16.
Measured, as air courses:

```
GET …/column?at=-20,-1     ring:       air y6..13   deck y14..15   air y16..21   landmass y22..29
GET …/column?at=0,0        well:       air y6..20   glowstone y21              landmass y22..29
```

Four corner piers carry the deck's inner edge, stated `floor 0, base_height 14` — **from the hall floor's own
floor, never from its top**, which is `24-underground`'s rule and the difference between a pier and a pier
over a trench. The column at `(−14, −10)` is one unbroken brick run `y1..15`: pier and deck met, with nothing
between them.

## Where this board takes the other branch: `kind: "prop"` on the lid

`24-underground` measured a lid repainting the room under it — a terrain layer's bands resolve from the
bedrock course to its own top, so its `fill` claims every stone course beneath — and **kept** the fault,
because the alternative takes the layer out of `SK10`'s pair walk. Here the deck contests nothing (`under`
tops out at `y15` only where the piers and stairs are, and those are the deck's own supports), so the trade
is free and this board takes it. The difference is visible because the insets are a different colour:

| `gallery` layer | `(−4, −12)` deck | `(−4, −12)` under the hall floor |
|---|---|---|
| terrain (no `kind`) | `y14..15` Sea Lantern | `y1..3` **Sea Lantern** — the inset's fill, three courses down |
| `kind: "prop"` | `y14..15` Bricks | `y1..3` **Stone** |

Forty-eight sea lanterns were being buried under the floor. Nothing raised a finding either way.

## The two flights, and the anchor arithmetic generalised

`20-undercroft` and `24-underground` each recorded one worked case of the stair anchor. Three cases is enough
to state the rule.

A `height_mode: level` polygon interpolates its `anchor_heights` across its own extent, samples at each cell's
**centre**, and floors. So for a flight of `n` cells falling one course a cell, from a head tread at `top`:

> **`A = top − floor + 2` at the head, `B = A − n` at the foot.** That gives `n` treads, `n − 1` risers of
> exactly one course, the head flush with the surface it meets and no doubled tread.

Three flights, three checks:

| Flight | `floor` | head `top` | `n` | `A` | `B` | risers |
|---|---|---|---|---|---|---|
| `24-underground`'s descent | 6 | 21 | 16 | 17 | 1 | 15 |
| this board's descent | 16 | 29 | 14 | 15 | 1 | 13 |
| this board's stair | 0 | 15 | 10 | 17 | 7 | 9 |

**The descent** is one polygon in `addShapes`, which lands on the compiled `team` group and is therefore
fanned — one drawn, two built. It is `override: true` on the `ground` layer, so it replaces the landmass
outright in its own columns, and its `floor` is **16**: the gallery deck's own standing course. Starting it
lower would drive it into the deck and `SK10` would say so. Read at `x −20`, `z −16` down to `z −3`:

```
z   −16 −15 −14 −13 −12 −11 −10  −9  −8  −7  −6  −5  −4  −3
y    29  28  27  26  25  24  23  22  21  20  19  18  17  16
```

**Fourteen treads, thirteen risers of exactly one course**, the head flush with the meadow at `y29` and the
foot one course above the deck at `y15`.

**The stair** from the gallery into the well is on the `under` layer, drawn as a `rot_180` pair rather than
fanned — `under` is stamped once — and stated `floor 0` so it is solid to the bedrock rather than bridging a
trench. Read at `z −1`, `x −12` to `x −3`:

```
x   −12 −11 −10  −9  −8  −7  −6  −5  −4  −3
y    15  14  13  12  11  10   9   8   7   6
```

and its image at `z 0`, `x 2..11`, runs `6 7 8 9 10 11 12 13 14 15` — the same flight, turned.

**The `rot_180` rule, stated once.** A cell `(x, z)` maps to `(−1−x, −1−z)`, so a rectangle
`(min_x, min_z)–(max_x, max_z)` maps to `(−max_x, −max_z)–(−min_x, −min_z)`, and a rectangle is its own image
exactly when `min = −max` on both axes. Every pair on this board — the piers, the plinths, the stairs, the
lantern insets, the torches — is emitted from that one line.

Checked rather than trusted, column by column over the whole board at or below `y29`, against
`(−1−x, −1−z)`:

| | |
|---|---|
| every span, placed props and structures included | **104** columns differ, **44** of them in the hall |
| the same with placed props and structures left out | **60** differ, **0** of them in the hall |

**Everything drawn is exact. Everything the dressing pass placed is not.** All 44 in-hall mismatches are
flora, and the reason is the axis: the flora ring is drawn `[[-11,-7],[11,-7],[11,7],[-11,7]]`, whose cells
are `x −11..10, z −7..6` — **exactly its own image**, so the fan has nowhere to stamp a second copy and the
noise inside it is whatever world coordinates give. Grass stands at `(−11, 2)` `y6` and nothing stands at
`(10, −3)`. The remedy is to draw the area **off** the axis so the fan has two places to put it; the case is
recorded against `G162` in `docs/world-export/ideas.md`, which already owns the axis. The 60 outside the hall
are `02-theme`'s own spawn structures and are inherited, not authored here.

## The tree that fits

`24-underground` planted a 12-block oak in an 8-course room and got a trunk to the ceiling with two courses of
leaves and nothing above: *"Nothing reads a room's headroom."* Nothing does here either — but the well is 16
courses, so a 10-block oak has room:

```
GET …/column?at=-6,4
  y 16..14   Oak Leaves
  y 13..6    Oak Log
  y  5..4    Coarse Dirt      the hall floor
```

**Eleven courses used of sixteen, five clear of the ceiling at `y21`.** The canopy is whole. The author sized
it by hand, which is still the only way.

## What to look at

Six of these are taken by hand and live in `renders/close/`. `drive.py` sweeps `renders/` of anything the run
did not write, and the sweep is over **files**, so a subdirectory is where a hand-taken picture belongs.

| | |
|---|---|
| `renders/close/xray-hall.png` · `xray-hall-turned.png` | the x-ray: the meadow washed out, the hall under it. Both quarters, because the veil opens the near side and what it opens differs |
| `renders/close/iso-hall.png` | **the same clip, drawn as an ordinary isometric.** It is a field. That is the whole argument for the mode |
| `renders/close/xray-well.png` | the well at 11 px a block: the ceiling cross, the six lantern insets, the four torches, the braziers, the tree |
| `renders/close/xray-brazier.png` | one brazier at 14 px a block — plinth `y0..8`, fire `y9` |
| `renders/close/layers.png` | one panel a storey: `under` 40,171 blocks, `gallery` 3,391, `lamps` 399, `ground` 15,043. The tree and the flora ride along in every panel — an unattributed run belongs to no storey, so `voxels` hands it to whichever one is asked for |
| `renders/world-xray.png` · `world-xray-turned.png` | what `drive.py` writes for any board holding a roofed void of 200 cells or more |
| `GET …/column?at=-17,-13` | the four-storey column: floor, deck, torch, meadow |
| `GET …/column?at=-20,-1` | the gallery in section: 8 courses under the deck, 6 over it |
| `GET …/findings` | the read that answers `SK9`. `drive.py` asks it on every run |

**A made thing is drawn opaque in the x-ray, and it has to be told.** The sight-line rule washes out whatever
stands between the camera and the room's air, which is right for a ceiling and wrong for a brazier — a lamp
standing on a floor is exactly as much "in the way" as a lid. Nothing in the block set separates them; the
document does, because a layer of `kind: "prop"` *is* a made thing. So `drive.py` passes those layer ids to
`iso.xray(keep=…)`, and here that is `gallery` and `lamps`.

## Numbers

| Read | Answer |
|---|---|
| `POST /plan/evaluate` | score **1.97**, `valid: true` — `02-theme`'s own answer, unmoved by two storeys |
| `POST /plan/inspect` | `destroyable-1` own **20** enemy **67** ratio **3.35** — inside `GO1`'s 3.0–4.0 band |
| the storey's tiling | **10,000** columns: bare **0**, without a span at `y0` **0** |
| the hall | 48 × 32, air `y6..21` = **16** courses; the well 24 × 16 open the full height |
| the void scan | **6** roofed voids. The hall is **20,425** cells at `x −24..23  y 6..21  z −16..15`, open. Two are SEALED — the spawn platforms, 2,176 cells each at `y36..47` |
| the lamps | **128** emitting blocks: 60 glowstone · 48 sea lantern · 16 jack o'lantern · 4 torch |
| the flights | descent **13** risers `y29 → y16`; stair **9** risers `y15 → y6`; no repeat in either |
| `GET …/findings` | **none** |
| `POST …/sketch/dressing` | **0** declines |
| `GET …/preflight` | export gate **OPEN**, traversability connected, both teams |
| `GET …/coverage` | reached 3,878 · dead 6,122 of 10,000 = **61.2 %** dead — `02-theme`'s empty square, and the hall is under the middle of it |

```bash
python3 tools/drive.py showcase/26-lamps-and-gallery "Lanthorn" --out showcase/26-lamps-and-gallery/world
```

## What is still missing

- **A lamp that is a prop** (`WE82`). Everything above is drawn, so every lamp is a rectangle in a document
  rather than a thing clicked once and fanned. Four braziers cost eight shapes, and the dressing pass —
  which keeps props off routes and out of a goal's clearance — never sees them.
- **A prop at a stated height** (`WE83`). Same shape of gap: the gallery is a floor at `y14`, and nothing
  the dressing pass places could stand on it except by naming it as a storey.
- **Anything that reads headroom.** The tree fits because it was measured against the ceiling by hand.
  Nothing would have said so.
- **A fanned area prop on the axis.** The flora above is stamped once and is not mirrored (`G162`).
- **A building inside the room.** Still not attempted — `24-underground` records why, and this board spends
  its floor area on a gallery instead.
