# Hallowgate — a composed board taken over

A capture-the-wool board on a churchyard. One wool a team in a chapel on a raised terrace,
reached along a walled causeway with a lychgate on it; the hub rings a grave-pit nothing
crosses.

**The sentence it was authored to:** *a churchyard where the wool is fetched from a chapel at
the end of one walled causeway, and the only other way at it is the long way round a hole
nobody can cross.*

## What came from the composer, and what did not

`composed-seed-3.plan.json` is committed beside the spec: the composer's own answer, so the
starting point is reproducible. What it bought is the **arrangement** — a hub ringing an
enclosed hole, a spawn hung off its flank, an L of causeway to a room in a corner, a
frontline bar with two stepping stones, a mid band, and a land budget that keeps a wool board
about a third land. That is the thing that is hard to invent.

**What it does not state, and what is therefore authored here:**

| The composer states none | This board's answer |
|---|---|
| elevation — every piece flat at `surface` | the churchyard terrace five courses up, made ground, `exclude`d |
| defence walls — `"walls": []`, always | one wall on the causeway's outer interface |
| anything but axis-aligned rectangles | two polylines, and the compiled ring bent `side: "in"` |
| layers — no storeys at the plan tier | four: the lychgate's posts and roof, the chapel's walls and roof |
| relief | two groups — the team's ground, and the centre island as its own |
| a spawn yard | one spawn piece where the composer had two, so the iron cube has somewhere to stand |

**The hole in the hub is left exactly as composed, and that is a decision rather than
laziness.** It is the rotation device: `match-flow.md` §4.9 measures that the long way round
a holed hub covers **37%** of the defenders' reinforcement lane against **76%** for the short
way, and it reduces the collision on 74% of the boards that offer one. Bridging it would have
removed the only route on this board that does not spend its whole approach inside that lane.

## The wall

**One wall, on one interface, and not on the room's own.** `PL13` refuses a wall on the wool
room's own interface — *the wall and the room stand through each other and the room can
barely be entered* — so it stands an approach out, on `wool-a-t1` ↔ `hub-t1`, sixteen blocks
from the chapel terrace.

**The wall is meant to be in the way, and it spans the whole of the interface it names.** The
causeway is twelve blocks wide there and nothing else reaches z 76 at that x, so there is no
shoulder beside it to stroll round — which is the thing that turns a prepared line back into
an obstacle for the team that built it.

## What the adaptation had to fix

Four of the composer's own numbers went outside their bands once the board was reshaped, and
each was named rather than guessed at:

- **`SP9`** — the spawn door faced void. The composed `facing: "front"` pointed at the piece's
  back; it faces the hub now.
- **`FR9`** — both stepping stones presented an 8-block front, under the 15 a crossing wants.
  Both were widened to 16 and the mid band widened with them.
- **`WL12`** — the bay between the room and the hub was 12 blocks, under the 16 a gap beside
  a goal wants. Negative space is crossed by jumping long before it is crossed by building,
  and a short bay deletes the approach the board is drawn around. The causeway was
  **lengthened** rather than moved, so it still shares the interface the wall stands on.
- **`WX11`** — the room stood three courses over the terrace behind a bedrock face nobody
  drew, because my churchyard wall ran across the room's own footprint and a room's
  foundation levels its whole footprint at the footprint's highest cell.

## The numbers

| Read | Answer |
|---|---|
| `03-slopes.txt` | 5 688 walked · 82 scrambled · 70 barrier; 4 faces, largest 33 |
| `06-claims.txt` | **20 placed, 0 declined** |
| `GET …/coverage` | reached 6 144 · dead **0** of 6 144 = **0.0% dead** |
| `POST …/sketch/relief/read` | `team` 2 440 cells, 7…19, relief 12, symErr 0 · `neutral` 384 cells |
| `GET …/plan/flow` | attacker 182 blocks to the wool, defender 57 |
| `GET …/preflight` | **export gate OPEN**, per team |

Three themes and all three paint: `mire` 87.9%, `churchyard` 8.0%, `sill` 4.0%.

## The chapel is not a house, and the reason is a read

`POST …/sketch/seats` answers **60 legal cells for a 9 × 7 house over this whole board** —
`DR-KEEP`, `DR-SITE`, `DR-CLAIM` and `DR-PASS` take the rest between them. That is a fact
about a composed board of this size rather than about siting: a spawn march, a wool approach
and a road leave a 64-wide board almost nothing a building can stand on with eight blocks of
passage on a side.

So the chapel is built out of **layers** instead, where the dressing pass has no say: walls
on the terrace's top block plus one, a roof on the walls' top, `kind: "made"` and `part_of`
so `SK10`'s pair walk and `SK11`'s reachability walk stay off it. Seven blocks wide on a
sixteen-block terrace, with five blocks of yard south of it for the route to the room.

## Both rooms are buildings

`roomStyles` takes two members and this board states both, because the default is the
studio's built-in bedrock box standing where the wool is fetched from and where every player
arrives. Both are the chapel's family — birch over stone brick on a dark, wet ground, with a
dark oak frame — under the **steep gable** a chapel wants. The wool room takes the darker
roof and a two-block door; the spawn hall the paler roof and a three-block one.

**Neither is flat with a hole in it, which is what the first pass built.** That shape is the
bedrock box's, and a room reached through its own door has no use for a lid that opens.

## What went wrong

**Both made structures floated a course above what they were meant to rest on.** A layer's
`base_y` is the layer below's **top block** plus one, and a shape of `base_height` N tops out
at N−1 — so the terrace at 14 tops at y13 and the causeway's ground at 9 tops at y8. Written
as `YARD + 1` and `GROUND + 1`, both left a one-block gap that no gate reports.

**The chapel and the flight were built on top of each other**, because both were drawn to the
terrace's middle without either being read against the other. The flight now lands south of
the chapel and the transect proves it:

```
x 7 from z 84 to 95
rises 4, falls 0, worst step 1: 0 barrier, 0 scramble, 0 drop | walked end to end
```

**A theme was registered and never assigned.** `churchyard` sat in the registry painting
nothing until `SK3` named six shapes reaching for a theme the layout did not carry — the
`themes` key itself was missing from the finish. `themes/census` is the only witness to the
milder version of that fault, where the theme exists and simply owns no cell.

**The tarn was drawn across rising ground twice.** A pool takes the lowest surface its band
crosses and empties every column over it down to that line, so the first two placements —
both inside the barrow's falloff — dug a four-course trench and left fourteen dry columns
beside the water.

## Coordinates

| Thing | At |
|---|---|
| wool room (red) | x 16…24, z 92…104 |
| spawn (red) | x −32…−16, z 60…80, door +x |
| defence wall | `wool-a-t1` ↔ `hub-t1`, z 76, x 0…12 |
| grave-pit (enclosed void) | x −4…16, z 52…64 |
| lychgate | posts x 1…3 and 9…11, roof x 0…12, z 78…83 |
| chapel | x 3…10, z 97…103, roof x 2…11, z 96…104 |
| chapel steps | x 3…11, z 86…96 |
| tarn | x −14…−5, z 54…63 |
| barrow crest | ≈ (23, 58) |
| centre island | x −12…12, z −8…8 |
