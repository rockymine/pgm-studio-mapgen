# Hushwater — the composed board against the board it became

The descriptor that reproduces the starting point, byte for byte:

```
GET /api/compose?players=18&teams=2&symmetry=rot_180&seedStart=5&count=1
POST /api/compose/pin  { players: 18, teams: 2, symmetry: "rot_180", cell: 4,
                         seed: 5, composerVersion: "body-first-1", schema: 1, index: 0 }
```

Every number in the *composed* column is off that card, read back through `POST /compose/pin` and
written to `specs/opus5-hushwater/composed.json` by the build script before anything was changed.
Every number in the *adapted* column is a read off the built board, named beside it.

---

## 1. The descriptor and the card

| | composed | adapted |
|---|---|---|
| players · teams | 18 · 2 | unchanged — the count names the micro band (14–21 give byte-identical boards) |
| symmetry · cell | `rot_180` · 4 | unchanged |
| seed · composer version | 5 · `body-first-1` | unchanged |
| evaluator score | **0.000**, no hard term, no top soft term | **0**, `valid: true`, no violation |
| plan-tier lint | 1 complaint: `WL12`, a 12-block bay between `wool-a-room` and `hub-t1` | 1 complaint: `EL1`, the bank↔yard seam reading 3 blocks flat — answered by transect, below |

## 2. The spend block

| | composed | adapted |
|---|---|---|
| band | micro | micro |
| unit land | **250** cells against a **226.4** budget | **265** cells — 15 added, all of it the two room aprons, the bing and the re-cut wool approaches |
| mid land | **0** cells against a **50.3** budget | **24** cells — two shoal legs of 6 × 2 cells, each the other's image |
| footprint | 280 cells | 289 cells |
| hub | 1 box, 128 land cells / 144 footprint | 116 land cells — three arms re-cut, the yard hole kept at 4 × 4 cells |
| frontline | 1 box, 64 / 72 | unchanged rects, 64 / 72 |
| wool | 2 boxes, 42 / 48 | 2 boxes, 57 land cells — an apron added to each room, and both approaches re-cut |
| spawn | 1 box, 16 / 16 | 16 cells, moved 16 blocks west onto the centre line |
| pieces · zones · walls | **12 · 1 · 0** | **17 · 3 · 1** |
| distinct piece surfaces | **1** (`globals.surface` 9; no piece states one) | **7** — 12, 13, 14, 16, 17, 18, 19 |

## 3. The structure block

| | composed | adapted |
|---|---|---|
| hub body | `ring` | `ring`, kept — four arms round a 16 × 16 yard, two of them shortened so the east arm makes a nose |
| wool families | `i`, `i` | `i`, `i` — same family, opposite characters: the west one open across moor, the east one a lane behind a bedrock wall |
| frontline form | `single` | `single`, untouched: one 32-block run, `/plan/inspect` reads `widthBlocks 32, profile straight` on both teams |
| mid | none emitted | a Z of two neutral legs, each the other's `rot_180` image, meeting at the origin |
| enclosed holes | 2 (one yard a side, 16 cells each) | 2, unchanged, narrowest crossing **16 blocks** — the adaptation did not fill or narrow either |
| defence walls | `[]` | 1, on `hub-t4`↔`wool-b-t1`: bedrock `x 35..37, z 60..76`, 16 blocks of interface, five courses above the lane |
| build zones | 1 (the mid band) | 3 — the mid band widened to the new strait, plus two team-only planks onto the bing |

## 4. What the crossing became

| | composed | adapted |
|---|---|---|
| strait | 32 blocks, one hop, nothing in it | 40 blocks with a bank in it |
| hops | one | **two**, and they are different: 12 blocks on one hand, 20 on the other, and `rot_180` gives each team the short one on the opposite hand |
| `islandGaps` | `team ↔ team, 32 blocks` | `team ↔ shoal, 12 blocks`; `team ↔ bing, 12 blocks` |
| `CT12` | in band (15–40) | out of the rule's reach by construction — a mid island makes the crossing indirect; `G5` governs each hop at 10–20 and both are inside it |

## 5. The lopsided wool, measured before and after

The brief's §2 is the thing this board was watched for. `GET …/plan/flow` reads it off the plan, and
`GET …/walk` reads it off the built world.

| read | composed (straight line off the pinned rects) | adapted (`plan/flow` and `walk`, built) |
|---|---|---|
| enemy spawn → wool-a | 180.9 blocks | **210** blocks walked, **30 placed** |
| enemy spawn → wool-b | 179.4 blocks | **213** blocks walked, **30 placed** |
| worst ratio | **1.008** | **1.014** |
| own spawn → wool-a | 54 blocks | **59** walked, **4 placed** |
| own spawn → wool-b | 50 blocks | **66** walked, **3 placed** — the wall is the difference, and the bing is the way round it |

**Seed 5 was not lopsided, and that is worth saying plainly.** The brief measured 1.29×–1.53× on p20 and
p30 boards at seeds 0–3; this one came off the composer at about 1.01 and the adaptation kept it there
while moving both rooms, moving the spawn and adding 39 cells of land (15 to the unit, 24 to the mid). The adaptation's job here was to
*not break* a balance the composer had already found.

## 6. What the ground became

The composed board is flat at `globals.surface` 9 and carries no relief, no theme and no prop. There is
therefore nothing to compare the finish against — every number below is the adaptation's.

| read | value |
|---|---|
| `relief/read`, team group | 2768 cells solved, low 11, high 21, range 10, symmetry error 0 |
| `relief/read`, neutral group | 384 cells, low 12, high 15, range 3 |
| `incline`, first finish (bands cut at 14° / 26°) | `00-09° 71% · 10-19° 20.5% · 20-29° 4.6% · 30-39° 2.3% · 40-49° 1% · 50-59° 0.5%` |
| `incline`, shipped (bands cut at 12° / 26°) | `00-09° 62.6% · 10-19° 27.4% · 20-29° 6.7% · 30-39° 2.4% · 40-49° 0.5% · 50-59° 0.3%` |
| `themes/census`, first finish | floor **50.5%** · moor 35.6% · hush 13.8% |
| `themes/census`, shipped | moor **56.8%** · floor 24.5% · hush 18.7%; borders floor\|moor 372 cells, hush\|moor 284 |
| `slopes`, first finish | 8598 walked · 134 scrambled · 132 barrier; 8 faces, largest 44 |
| `slopes`, shipped | 8559 walked · **251 scrambled** · **54 barrier**; 6 faces, largest **16** |
| `coverage` | reached 8718 · dead 146 of 8864 = **1.6%** |
| ground cells with the chimney | 8920 stored, 8864 walkable |
| `plan/flow` dead ground | 368 of 8864 (4%), 144 of it the bing — a pad no *land* route passes, which is what a team transient-link is |
| `preflight` | `export gate OPEN`, per team |
| `sketch/dressing` | 28 placed, **0 declined** |
| `04-routes.txt`, the four raids | 206 · 211 · 204 · 211 blocks, **30 placed each** |
| `04-routes.txt`, the four defence walks | 73 · 73 · 68 · 72 blocks, 4 · 3 · 4 · 3 placed |
| storeys | 1 made layer (the chimney), 5 shapes, `mirrors: true` |

## 7. Every gap the reshaping opened, in blocks

`POST /plan/inspect` → `spaces`, which measures the narrowest straight crossing over each bay and hole.
The floor is **16 blocks** where a space touches a wool-room or spawn piece and **12** where it does not;
a space a build zone covers is not asked, because building over it is what the zone states.

| space | kind | cells | narrowest | touches a room? | covered by a zone? | verdict |
|---|---|---|---|---|---|---|
| the yard, `hub-t3`↔`hub-t4` (×2, one a side) | hole | 16 | **16** | no | no | 16 ≥ 12 ✓ — and it is the composer's own hole, unchanged |
| the gill, `frontline-t2`↔`shoal-s` | bay | 882 | **12** | yes | yes, `mid-band` | a stated crossing, not a bay to jump: 12 blocks is four times a sprint jump |
| `bing`↔`wool-b-t1` (×2) | bay | 76 | **12** | yes | yes, `bing-plank-s` | the one gap geometry would not let me widen — see below |
| `bing`↔`hub-t1` | — | — | **16** | yes | yes, `bing-plank-w` | widened from 12 to 16 on purpose |

The `bing`↔`wool-b-t1` hop stays at 12 because the two edges it must reach are 16 blocks apart in z: a pad
16 blocks clear of the lane leaves only 4 blocks of facing for the mine head, and `G2` then refuses the
plank at *corridor width 4 < 10*. Twelve is the studio's floor on that plank, not a number I preferred.

## 8. Every refusal hit, by rule id

| id | what it said | what I did |
|---|---|---|
| `G2` | `zone 'staithe-link-e' corridor width 8 < 10` — **hard**, score 2000 | widened every build zone to 12 blocks or more |
| `G5` | `gap hop 8 outside 10..20 between 'hub-t1' and 'staithe'` — **hard** | moved the pad so both hops are 12–16 |
| `ST2` | the iron cube does not stand inside a spawn piece | moved it onto the spawn-role piece |
| `WX8` | the cube needs 3×3 inside the piece and 2 blocks clear of the shell | dropped the iron: `WX1` makes the shell the piece inset one block, so the three cannot hold together on a plan-compiled spawn |
| `DR-DOC` | `field 'pave.jitter' could not be read` | `jitter` is an integer percentage 0–100, not a fraction — fixed everywhere, including inside the themes, where `RQ3` would never have told me |
| `PT4` | a shape's `material` sampled in the plane reads as vertical stripes | gave the stair and lane materials a `rise` |
| `HS4` | `beams are dark oak and post is spruce` | cut the beams from the same wood as the posts |
| `SK14` | two override adds stating a top the relief solves through | gave the launder and the tramway the same `relief_scope: "exclude"` as the floor they lie in |
| `SK13` | `'spill-yard' draws nothing over 130 columns — 'void-1-cut' takes them away` | moved the brush off the composer's yard hole. A hole is never scenery |
| `DR-KEEP`, `DR-PASS`, `DR-STEEP`, `DR-SITE`, `DR-ROAD`, `DR-CLAIM` | 7 declines on the first dressing pass | every one moved by reading `sketch/seats` and then `loop.py --candidates`, to 26 placed / 0 declined |

Two complaints ship standing, and both are answered by a read rather than by a change:

- **`EL1`** — `'frontline-t1'–'hub-t2' steps 3 blocks`. The plan tier walks pieces flat and cannot see the
  relief. The built crossing transects `rises 6, falls 1, worst step 1, 0 barrier, 0 scramble, walked end
  to end` at x −2 and `rises 5, falls 2, worst step 1` at x 8.
- **`SK27`** — the component compiles to 7 plateaus carrying 3 paints. Two of the three boundaries are the
  thing the board is about (the mine's made floor ends where the fell begins), and the third is broken on
  purpose by four brushes drawn to cross the risers rather than to sit inside a plateau.
