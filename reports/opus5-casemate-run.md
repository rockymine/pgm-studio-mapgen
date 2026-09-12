# Casemate — a capture board built to the control law

`opus5-threap-edge` took the gamemode's name literally and stood its hills on a hill. The author's reading
of that board is now `match-flow.md` §10, and this is the board built to it: **structural, not landscape;
no point over open ground; no line from any pad to a spawn; path options on three storeys; cover placed
rather than strewn; and one-way ground.** Everything below is measured off the built world.

## The board

```
                    z −44   ▲ red gate house
        ┌──────────────────────────────────────────────┐
        │   ■ pillar      ═══ traverse ═══   ■ pillar  │   the terreplein, y20
        │                   ╷ ramp                     │
   ╔════╡  ▓ West Bay  ┌────┴────────┐  East Bay ▓  ╞══╡   bays: three walls, one mouth
   rampart             │ ░ THE SLOT ░│              rampart
        │              └──── CISTERN ┘                 │   the casemate, y13, under a lid
        │   ■ pillar      ═══ traverse ═══   ■ pillar  │
        └──────────────────────────────────────────────┘
                    z +43   ▼ blue gate house
```

**The Cistern** sits in a vaulted casemate under the middle of the works — floor y13, ceiling y19, **seven
blocks clear**, two aisles of 1 680 cells each. One slot of open sky runs straight over the pad; everything
either side of it is roofed. **West Bay** and **East Bay** sit on the terreplein at x ±29 (0.66 of the
44-block centre-to-spawn distance, the corpus median), each in a bay walled on three sides with one mouth
facing the middle.

Three ways into the vault, and they are not the same kind of way:

| route | what it costs |
|---|---|
| the north and south ramps | walked, both directions — `walk` from the pad to a spawn is *walked end to end* |
| the slot | an **8-block drop** onto the pad; one way |
| the two holes in the roof plates | a **7-block drop** into an aisle; one way |

The bays each take a walked route from the middle and a **one-way port at the back**: a rampart walk two
blocks above the terreplein enters the bay through a gap in its outer wall and drops two into it. Two blocks
is a step nobody climbs back up, so the back door only opens inward.

## The sightline, measured

The fault the author named on Threap Edge — *a raised point looks straight into a spawn* — is the one thing
here that had to be checked rather than argued. `GET …/transect` along the line from the West Bay pad to the
red spawn:

```
(-30,  -1)  20   the pad
(-21, -14)  21
(-18, -18)  28   ← the pillar, eight blocks over the pad, on the line
(-15, -22)  19
( -1, -42)  20   the spawn
```

A ten-wide pillar stands squarely between them. The Cistern needs no such check: it is at y13 under a lid.

## What the build taught

**A layer's plate and the ground it is laid into are settled in `SK10`/`SK11`, and the two pull opposite
ways.** Sizing the casemate roof to the pit's own ring left a slot round it and made the plates an island
nobody could step onto (`SK11`, 48 cells). Reaching them two blocks past the ring drove them into the ground
instead (`SK10`, 152 columns). What settles it is the rule's own fix — *raise the base_y of the lid* — so the
plate sits **one course over** the terreplein and is stepped onto rather than butted against. The cause under
both is worth writing down: **the relief solves on the cell grid, two blocks to a cell**, so the hole an
`area` mark cuts is the cells its ring covers and not the blocks its corners name.

**A pad takes the highest ground its own footprint spans.** The first ramps ran along x into the vault's
ends — straight through the flank bays — so each bay pad straddled a ramp trench and the stamper built it as
a plinth two blocks over the works. Moving the ramps to the vault's north and south ends fixed both bays at
once. The tell was `walk` answering `(-30, -1) 22` where the terreplein is 20.

**A ramp needs three points, not two.** A two-point line mark's head lands wherever the cell grid rounds it,
and the first version's head was a six-block drop with a slope at the bottom of it. A level first segment
puts the head flush.

**Two complaints are left standing on purpose.** `SK11` reports 100 standable cells on each pillar top with
no route onto them, and says outright to leave it where a detached group is what the thing is — a pillar is
cover, and a pillar a team can stand on is a firing platform in the middle of the works. `RL3` reports the
casemate wall and the ramp cuts as steps two marks meet on; they are walls, and a fort's walls are what the
board is read off.

## The second pass: colour, symmetry, and what the middle is worth

Six corrections from the author, and four of them changed the board's shape rather than its look.

**The middle pays double.** All three points paid one a second, which is a board two teams settle by taking
one each and standing on them. The Cistern pays **2** now and the bays **1**, and the flanks moved from 29
blocks out to **38** — 0.86 of the centre-to-spawn distance, the top of the corpus's 0.52–0.88 range rather
than its median — so that a team holding the middle does not also cover them. The corpus backs both:
13 of 83 KotH boards vary the rate, 10 of those pay the most for the point named for the middle, and
`koth/catre_koth` and `koth/abaddon_koth` are literally 1 / 2 / 1. It is written up as `match-flow.md` §10.6.

**The board is symmetric across both axes now, not only under the half-turn.** Every structure is authored
in the **north-west quadrant alone** and fanned four ways; a shape that straddles an axis is drawn up to it
and its mirror completes it. rot_180 alone sends a wall on red's west to blue's east, so the two halves of
the board differed in a way neither team's play could be compared across. The ramps moved onto the x axis
for the same reason — one from each end, in line with the pad — and each aisle roof now carries a mirrored
**pair** of drop holes instead of one hole off to a side.

**The fill was the green block.** Eighteen courses of andesite under every exposed face and every pit wall,
on a board otherwise made of cobblestone and stone brick. The fill is cobblestone now, and both mossy
variants are out of every palette — they were the only other green in it.

**The team's colour is in the works.** `teamTint` stamps stained clay in the owning team's colour and falls
back to a neutral where no team owns the cell, which is exactly the right instrument here: the ground says
whose end you are at, and says nothing where the answer is the thing being fought over. It runs as a course
through the terrain's wall run and as a band and a parapet in the gate house. Read back: the vault's west
face carries `159:14` at y14 under its chiselled string course, red's gate carries `159:14` at y23 and y25,
blue's carries `159:11` at the same courses.

**The roof plates read as masonry, not timber.** They were spruce-rimmed, which made the vault's lid look
like a platform somebody left there rather than the ceiling of the room under it — and a lid nobody can
name is a lid nobody knows to look under. Stone, with a chiselled rim so the edge a player drops past is
legible.

**The cover near the spawns is gone.** Cover in front of a door breaks nothing, because the ground there is
where a team already stands. Five boxes per quadrant now, each on a line that needs breaking: the lane out
of the traverse, the run down the ramp head, the bay's mouth, the vault rim, the outer lane before the
rampart stair.

## What the studio still cannot see on a capture board

Unchanged from the last board and now measured twice. `POST /plan/evaluate` raises `PL3` — *this plan has no
objective* — on a board that exports as `<gamemode>koth</gamemode>` with three hills and a 750 limit
(`TN19`). `GET …/coverage` calls it 71.5% dead with its two largest dead patches centred on the two bays,
and `04-routes.txt` prints *no route between a spawn and a goal* while every one of those routes walks
(`WS62`). On a capture board **dead space is a fault rather than a note** (`match-flow.md` §10.3), so the one
read that would price this board's own law is the one that cannot see its objectives.

Final reads: 6 364 walked · 360 scrambled · 1 964 barrier · 20 faces, the largest of them the casemate's own
seven-block wall at x −21..20 z −15..14; 0 props placed and none declined — the cover here is structure, not
dressing; three hills paying 2 / 1 / 1, nine regions, three white wool markers at y53–55; export gate OPEN.
