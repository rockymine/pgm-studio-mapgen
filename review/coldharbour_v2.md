# Coldharbour v2 — the measured record

> A capture board built to the shapes the model names: a **U frontline** of two tips off a **double-hole
> hub**, an **L** wool lane west and an **I** wool lane east, a spawn alone at the end of the spine facing
> mid, and one neutral stone in the middle of the only crossing there is. The stream across the spine is
> the first thing a player leaving spawn walks over.

The second pass on `coldharbour`, after the author took the first apart.
`reports/opus5-coldharbour-v2-authoring.md` is the review, what the real plans taught, and the rebuild.

110 × 140 blocks per unit, 240 blocks end to end, `rot_180`, base surface 12, build ceiling 32, ground
y 9..45. **17 pieces, 207 ground cells, fill 0.336** — against `ruediger`'s 0.383 and `bridgid-ii`'s 0.431,
and against v1's 533 cells at 0.614.

## The shape, and the rule each part answers

```
  22 |         SSSS         |   spawn — alone at the end of the spine, facing mid    SP2 SP3 SP7
  20 |WWW      SSSS      WWW|   both wool rooms are dead ends                        WL1 WL6 WL8
  18 |999     CCCCCC     WWW|   L run west · spine · I lane east, void between them
  16 |999     CCCCCC     BBB|        the wall crosses the east lane here             ST4
  14 |888877777777777777AAAA|   hub back bar — every route docks onto it             HB1
  12 |    44   5555   66    |   two holes, solid core between                        DoubleHole
  10 |    33333333333333    |   hub front bar
   8 |       111..222       |   U frontline: two tips, buffer recess between          FR6 CT9
   4 |       ++++++++       |   band, flush across both tips
   0 |       ++0000++       |   one neutral stone, on the axis, inside the band       MD1 MD4
```

| | |
|---|---|
| gamemode | `ctw`, "Capture the enemies' wools!" |
| teams / spawns | 2 / 2, `rot_180`, 24 players |
| wools | 4 — `red` `(-48, 15, 102)`, `orange` `(47, 15, 97)`, mirrored for blue |
| islands | two — `neutral` (the mid stone alone) and `team` |
| walls | one, `wool-e-lane`–`wool-e-gate`: 15 blocks, the lane's full width, Δ 0, void both sides |
| dressing | 5 paths, 1 water channel, 24 trees, 12 boulders, 8 flora rings, 4 houses |
| evaluator | **score 0.0, `valid: true`, no term fired** |
| traversability | 11 065 navigable columns, 1 368 bridged, 4 components, **2 of 4 markers isolated** |

**Two isolated markers is the wall working**, not a fault. v1's wall could be walked round, so the read was
0; this one seals the east wool lane and the room behind it reads as its own component — the measurement
`FINDINGS.md` and `review/sable-marsh.md` both record for a bedrock line that is meant to be built over.

**The evaluator scoring zero was not chased.** v1 fired `fill-ratio 0.68` and `lane-width 30` and I recorded
the first as a stated choice. It was not: it was reporting that the board had no frontline box, no hub and
no mid. Drawing those three things took the score to zero on its own.

## What the mid does

One crossing, 40 blocks wide at the frontline and narrowing to the stone. The two tips shelve from y12 at
the hub edge down to y10 at the mid edge — `anchor_heights` on the compiled polygons, so each tip is a
beach rather than a cliff — and the stone sits 15 blocks off each of them, inside G5's bridgeable band. The
recess between the tips is an authored **buffer**, the CT9 hole, so a player who enters it is in a pocket
rather than on a route.

Everything else along both front edges is void. That is the whole of the difference from v1, where ground
ran the full 140-block width and the two teams could cross anywhere and therefore met nowhere.

## What the sketch states that the plan cannot

The plan states six flat surfaces. The rest is sketch work on the compiled layout:

- **Curved coasts** — Bézier `controls` on the mid stone, both wool rooms' ground and the spawn pad. The
  stone's four corners each carry an `in`/`out` pair, which is what turns a 20 × 20 square into a rock.
- **Relief on the hub alone** — every other shape is `relief_scope: "hold"`. The hub carries a core mark at
  14, two shoulders at 15, a lip at 13 dishing its front edge toward the frontline, and a `rim` at 13.
- **Three themes, all load-bearing** — `chalk-yard` on the contested ground (the neutral stone and both
  frontline tips, so the crossing reads as scoured rock), `chalk-hanger` on the two wooded wool runs,
  `chalk-down` on the rest.
- **A stream across the spine** — a `water` prop, carved bed and all, between spawn and hub, with the spine
  road paving a 7-block causeway over it. `(±8, 86)` reads water over sand; `(0, 85)` reads road.

## What is still open

**The two wool lanes are more alike than the design says.** West is an L and east an I, which differ in
plan, but both are a walk down a corridor to a dead end and only the wall tells them apart. A climb on one
(WL5's stepped approach) or a second entry on the other (WL8's alternative route) would make them two
decisions rather than two corridors.

**The hub's holes are decoration so far.** They are the right body and they read from above, but nothing
uses them: no route passes between them that a player would choose over the bar, and no build zone spans
them. CT8 calls an internal hole the rotation device; here it is a hole.

**The neutral stone is small for what it has to carry.** 20 × 20 with two boulders on it is a stepping
stone, and the crossing might want it either bigger and shaped, or paired with a second one so the hop has
a choice in it (MD6 puts stones in a grid of two lateral columns, never a chain).
