# Coldharbour v2 — a second pass, after human review

The first pass (`opus5-coldharbour-authoring.md`) recorded how the studio is driven and produced a board
the author took apart. This is the second pass: what the review said, what reading the **real** plans and
the composer model taught, and the board that came out of starting again from zero.

`pgm-studio` at `14fb4a653f164dfc9a884ec1baa1cf646cae34ab`, working tree clean, untouched. New map, new
documents, nothing carried over from v1 but two terrain themes and the two room shells.

---

## 1. The review, itemised

| # | The review said | What it is in the rule set |
|---|---|---|
| 1 | the water lane is encased by my own pieces; that is not what a lane is | a lane is a gap **between islands** that opens late — mine had no islands either side of it |
| 2 | dead space around the spawn; a spawn alone at the back is normal; it should face mid | **SP2** (near the back of its lane, else the space behind is dead) and **SP3** (faces the enemy) |
| 3 | the wools are not isolated enough and smush into pieces | **WL1** (far end of a *dead-end* lane) and **WL8** (default is a single chokepoint route) |
| 4 | the wall can be walked around; it belongs on an interface in front of the wool, blocking a full lane, void either side; not in the normal flow | **ST4** — walls sit on gentle seams, full seam width; the corpus puts all eleven of them on wool approaches |
| 5 | the large stone area in front of the wall looks random | it was `yard-sill`, a piece that existed to hold a wall I had put in the wrong place |
| 6 | the middle is too wide; players will not meet; three legs reaching mid is not nice | **FR6** — a frontline is **one box**, split (two tips and a gap) or wide. Mine was three pieces spanning the whole front edge |
| 7 | you want a U frontline, a double-hole hub, I and L wool lanes | `model.md` §4.1 and §4.6 — the body and approach taxonomies |
| 8 | one island in the middle | **MD1/MD4** — a stone, inside the band |
| 9 | you made three themes and did not use them | two of three were assigned; the third painted nothing distinguishable |
| 10 | four trees and no boulders, no water; the path ends randomly | **decoration.md** and `approaches.md`'s circulation-first rule, neither of which I followed past the first step |
| 11 | keep the terrain the same or less | v1 was 533 ground cells at fill 0.61 |

Two of those (6 and 7) are the same mistake and it is the one that mattered: **I had not understood that
the frontline is a box rather than an edge.**

## 2. What the real plans measure, and what they are shaped like

I drew every plan as ASCII before reading a line of its JSON (`planview.py`, committed beside the specs).
Numbers first, because they are unarguable:

| plan | symmetry | players | unit extent | ground cells | **fill** |
|---|---|---|---|---|---|
| `ruediger` (hand-authored, built) | rot_180 | 30 | 105 × 125 | 201 | **0.383** |
| `bridgid-ii` (traced) | mirror_z | 12 | 125 × 90 | 194 | **0.431** |
| `kanto` (traced) | rot_180 | 12 | 90 × 155 | 234 | 0.419 |
| `agrostid` (traced) | mirror_z | 12 | 116 × 112 | 245 | 0.302 |
| **coldharbour v1 (mine)** | rot_180 | 24 | 140 × 125 | **533** | **0.614** |
| **coldharbour v2** | rot_180 | 24 | 110 × 140 | **207** | **0.336** |

v1 carried **two and a half times** the ground of a real map of comparable scale. The evaluator had said so
(`fill-ratio 0.68` against a band ending at 0.496) and I recorded it as a stated choice. It was not a
choice; it was the symptom.

Ruediger, drawn out:

```
  24 |WW                   |   wool room: far back-left corner, a dead end
  23 |WWEEEDD4444          |
  22 |FFEEEDD4444          |   the lane to it: a long L climbing 7→8→9→10→11→12→13
  20 |R66    4444          |
  15 |MM     3333   111IHSS|   spawn: far right, at the END of its own lane, nothing behind it
  13 |++  0000000KLG111    |   hub: ONE wide bar. Everything hangs off it
  10 |++  CCC       +++    |
   6 |BBBBBBJ89777AA       |   frontline band
   3 |  TTT    777AA       |   TWO TIPS reach the mid — and only two
   1 |  ++++++++++++       |   the build band docks FLUSH across both tips
```

Three things I had not seen:

**The frontline is local.** Ruediger's front edge is 105 blocks wide and only two tips, 15 and 25 blocks
across, actually reach the mid. Everything else along that edge is void. My v1 put ground along the entire
front, so the two teams faced each other across a 140-block-wide nothing and could cross anywhere.

**The recess between the tips is the point.** `mirror-mid-examples` ex-6 — which FR6 names as the common
form — is exactly `hub-6` with `frontline-6a`/`6b` hung off it and `hole-15b`, **a buffer piece**, between
them. The gap is authored, not left over.

**Everything hangs off one hub.** Ruediger has one 7×3 hub bar; the wool lane, the spawn lane and the
frontline all dock onto it. My v1 had a five-piece back region, a spine, two crests and a knoll, none of
which was a hub — which is why the board had no centre and the spawn had dead ground on both sides.

I also read `model.md` §4 rather than the generator's code, and used it as vocabulary, not as a machine:
the **bodies** (Rectangle · SpineArms · Ring · P · G · DoubleHole · TwoUOnI), the **approach families**
(I · L · Z · Scythe · Clamp · U · H · Donut · Isolated) and their templates (`I = entry · room`,
`L = entry · run · room`), and the rule that a **hub grows wider, not squarer**.

## 3. The board, and which rule each part answers

```
  22 |         SSSS         |   spawn, alone at the end of the spine, facing mid   SP2 SP3
  20 |WWW      SSSS      WWW|   wool rooms: dead ends at the back of two lanes     WL1 WL6
  18 |999     CCCCCC     WWW|   L run west  ·  spine  ·  I lane east — void between
  16 |999     CCCCCC     BBB|        ← the wall crosses the east lane here          ST4
  14 |888877777777777777AAAA|   hub back bar; both lanes dock onto it
  12 |    44   5555   66    |   the two hub holes                          DoubleHole
  10 |    33333333333333    |   hub front bar
   8 |       111..222       |   U frontline: two tips, a BUFFER recess between      FR6
   4 |       ++++++++       |   the band, flush across both tips
   0 |       ++0000++       |   one neutral stone on the axis, inside the band  MD1 MD4
```

**The frontline is one box, 40 blocks wide.** Two tips of 15 blocks with a 10-block buffer recess between
them, hung off the hub's front bar. The rest of the front edge is void. The two teams have exactly one
place to meet and it is 40 blocks across at its widest — against v1's 140.

**The hub is a DoubleHole**, 70 × 30 blocks: two bars, two end pieces, a solid core between two 15 × 10
holes. Every route on the team side docks onto it — both wool lanes, the spine, both frontline tips — so
it is the board's centre in the sense the model means. It is also the only shape left free to the relief,
which is what gives it its swells and its dished front lip.

**The wool lanes are the two families the review named, and they are different on purpose.** West is an
**L** — `wool-w-entry · wool-w-run · wool-w-room`, exactly the template — running out of the hub's west
end and turning north to a dead end. East is an **I** — a straight lane capped by the room. Both rooms have
**one** land seam, to their own run: single chokepoint, WL8's default. Wool↔spawn is 57 and 58 blocks
(WL2 wants ≥ 20, WL9 wants them comparable); wool↔wool is 115 (WL7's band is 46–143).

**The wall is now doing its job.** It sits on `wool-e-lane`–`wool-e-gate`, a seam **15 blocks wide — the
lane's full width — with void on both sides** and Δ = 0 in height, which is ST4's "nobody walls a cliff".
There is no way round it: the only way past is over the bedrock and through the cobweb course. And it is
not on the normal flow — it crosses a dead-end wool lane, where the corpus puts all eleven of its walls,
rather than the artery between the spawn and the middle. `yard-sill`, the random stone area that existed
only to hold the old wall, is gone.

**The spawn stands alone at the end of the spine**, facing `front` — toward the mid. Nothing is behind it,
beside it or under it: the spine is 30 blocks wide, the spawn 20, and the map ends. The iron marker is
**ahead** of the spawn marker rather than beside it (SP7 — players face mid and must see it).

**The mid stone** is a 20 × 20 neutral island on the axis, `mirrors: false`, so it compiles to its own
`neutral` island rather than being fanned. It sits inside the band (MD4), 15 blocks from each team's tips
— a bridgeable hop in G5's 10–20 — and it is the only thing in the middle, which is what makes the
crossing a place rather than a width.

**The water lane is gone.** It had no islands either side of it, so it was a lane in name only. Water is
now what the review said it should be: a **channel cut across the spine** between the spawn and the hub,
so every player leaving spawn crosses it. The spine road paves a 7-block causeway over it, which the
column read confirms — `(±8, 86)` is water over a sand and coarse-dirt bed, `(0, 85)` is the road.

### What the plan does not state, and the sketch does

The review's last note — that plan pieces merging at one height is fine, and that relief and polygon
vertices are where elevation belongs — changed how the two levels were split. The plan states **six flat
surfaces** and nothing else. Everything below is sketch work on the compiled layout:

- **Curved coasts.** Bézier `controls` on four shapes — the mid stone, both wool rooms' ground and the
  spawn pad. The stone's four corners each carry an `in`/`out` pair in absolute board coordinates, which
  turns a 20 × 20 square into a round rock. Applied to coasts only, never to a seam a player walks.
- **A shelving frontline.** `anchor_heights` on both tips: `[10, 10, 12, 12]`, so each tip TIN-interpolates
  from 12 at the hub edge down to 10 at the mid edge and the crossing is a beach rather than a cliff.
- **Relief on the hub alone.** Every other shape carries `relief_scope: "hold"`; the hub is free, with a
  core mark at 14, two shoulder marks at 15, a lip mark at 13 that dishes its front edge toward the
  frontline, and a `rim` mark at 13 so the coast falls a block. `stairs: true`.
- **Three themes, all of them load-bearing.** `chalk-yard` (cobble, gravel, mossy cobble) on the
  **contested** ground — the neutral stone and both frontline tips, which is what makes the crossing read
  as scoured rock from above; `chalk-hanger` (podzol-edged turf) on the two wool runs, the wooded flanks;
  `chalk-down` on everything else. Assignment is by fused-shape height, the only handle a compiled shape
  offers.

### Dressing, drawn from the circulation rather than sprinkled

The routes were drawn first and the props fitted round them, which is `approaches.md`'s order and the one
I skipped in v1. The spine road runs spawn → causeway → hub and forks onto both tips; a drove leaves each
end of the hub for its wool. **Twelve trees** stand on the wool flanks either side of the droves, never on
them; **six boulders** — two on the neutral stone as cover on the one piece of ground both teams want, two
on the tips, two cairns on the hub's face; **four flora rings**, traced as polygons rather than boxed, so
the ground cover has no ruled edge this time; two houses folded into the hub's back corners.

## 4. What it measures

| | v1 | v2 |
|---|---|---|
| ground cells / fill | 533 / 0.614 | **207 / 0.336** |
| navigable columns | 26 818 | **10 898** |
| evaluator | 3.243, two terms fired | **0.0, `valid: true`, nothing fired** |
| frontline | three pieces, 140 blocks of front edge | one box, two tips, 40 blocks |
| mid | a band over empty void | a band over one neutral island |
| traversability | 3 components, 0 isolated | 4 components, **2 isolated** |
| dressing | 4 paths, 16 trees, 4 boulders, 4 flora, 4 houses | 5 paths, 1 water channel, 24 trees, 12 boulders, 8 flora rings, 4 houses |

**Two isolated markers is the wall working.** v1's wall could be walked around, so the read was 0; v2's
seals the east lane, so the east wool reads as its own component. That is the same measurement
`FINDINGS.md` and `review/sable-marsh.md` record — a bedrock line is meant to be built over, and the
traversability read models walking. A 0 there would now mean the wall had failed.

**The evaluator went to zero.** Not chased: the board was drawn to the shapes the model names, and the
score followed. That is the strongest evidence that the v1 fill-ratio complaint was structural rather than
cosmetic — one number, fired twice, describing a board that had no frontline box, no hub and no mid.

## 5. What I got wrong the first time, stated plainly

1. **I read the tool documents and not the model.** `plan.md` tells you what a plan document *is*;
   `docs/generator/model.md` §4 and `docs/generator/rules.md` tell you what a CTW board is *made of*. I had
   read the first and treated the second as generator-internal. It is not: the bodies, the approach
   families and the CT/FR/HB/WL/SP/MD rules describe hand-authored maps too, and `tools/seeds/teaching/`
   exists to demonstrate them.
2. **I treated the evaluator's one number as a matter of taste.** It was reporting the absence of a
   structure, and I answered it by trimming corners.
3. **I never drew the board.** Six lines of Python turn a plan into ASCII, and every fault in v1 —
   the three-legged front, the dead ground round the spawn, the wall on an artery — is visible at a glance
   in that view. I had looked at renders of what I had built and never at a diagram of what I had drawn.
4. **I used features because they existed.** The water lane went in because the format has one, not
   because the board had two islands wanting a late connection. The same for the third theme.

---

## 6. Third pass — the review of the review

Three more notes, and one of them was a question I could answer with a measurement rather than an opinion.

### Did the corner touches fire the evaluator on v1?

I did check v1's score — **3.243, `valid: true`**, two soft terms: `fill-ratio 0.68` (rule `G8`) and
`lane-width 30` (rule `LN1`). Neither was the corner contacts, and v1 had five of them.

The guess is a good one and the rule is real, so I settled it by probe rather than by reading. A two-piece
board whose only link is a corner:

```
POST /plan/evaluate  →  "corner contact between separate areas: 'a' and 'b' touch at a point,
                         not a corridor (no land interface)"        score 2000, valid false
```

Add a third piece joining the same two, leaving the corner exactly where it was:

```
POST /plan/evaluate  →  no corner violation at all
```

So **`PC-C` scores, and hard — but only when the corner is the *only* contact between two otherwise
separate areas.** Every corner in v1 was redundant: the pieces it joined were also joined properly
elsewhere, so nothing fired. The two terms that did fire were the honest ones, and `fill-ratio` was the
structural symptom.

### The mid is a bar now, not a rock

`mid-bar` spans the build zone's full width (`x −20..20`) and is 10 blocks deep, with **15 blocks of void
to each frontline leg** — a 40-block middle crossed as 15 · 10 · 15. The legs each grew a cell forward to
make those numbers land. It reads as one continuous ledge across the crossing rather than a stone in an
open gap, which is what makes the middle a place both teams stand on rather than a width they shoot across.

### The Bézier lobe, and the rule that was missing

The review was right that the room outlines had gone wrong, and diagnosing it needed measuring rather than
squinting. Flattening the old handles and testing every non-adjacent segment pair found **zero
self-intersections** — so it was not topologically a loop. Drawing the curve with its handles showed what it
actually was: a 15-block edge with handles placed 8 blocks past it, bowing into a deep U hanging off the
bottom of a wool room. `renders/09-bezier-lobe-before.png` is that picture and `10-bezier-corner-after.png`
is the same edge under a rule.

**The rule the documentation is missing is which side of the vertex a handle may sit on.** Build every
handle from the edge itself —

```
c1 = p0 + d·t + n·bulge          c2 = p3 − d·t + n·bulge
```

— and hold two constraints: `t·|d| ≥ bulge`, so the handle travels further *along* the edge than *away*
from it, and `bulge ≤ 0.35·|d|`, so a short edge cannot carry a big one. Break the first and the cubic
cusps and then loops; break the second and you get the lobe. `specs/coldharbour_v2/curves.py` is the
generator, and it flattens the finished ring and tests it for self-intersection before anything is posted.

### The organic pass, and the thing it quietly broke

Every coast is now bowed and no seam is: 26 of 38 edges carry a bow, and the 12 that do not are seams a
player walks, edges under 12 blocks, or edges beside the approach wall. West of the axis the amplitude is
0.16 of the edge and east 0.10, so the two wool approaches are not the same walk mirrored.

**The wall veto is the part worth recording, because I did not predict it.** The first organic pass bowed
the east wool lane's coast out to `x 37` and `x 56` either side of a wall running `x 40..55` — and a wall's
width is fixed at compile from the plan's seam, so it no longer spanned the lane. Players could walk round
both ends. Nothing refused it, nothing warned, and the only symptom was a number moving in the opposite
direction from the one I expected: **traversability went from 2 isolated markers to 0**, which on this board
means the wall stopped working rather than started. Vetoing every edge within 10 blocks of a wall rect —
they are in the `POST /plan/inspect` structures feed — put it back to 2.

That is the same class of failure as everything else in these two reports: a change that answers 200 at
every call and is visible only in a read-back you thought to take.
