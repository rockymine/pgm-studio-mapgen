# Coinfall — the first board with a shop in it

The studio grew shops this run: `PUT /map/{slug}/intent` takes a `shops` array, the export writes the
`<shops>` menu and a `<shopkeeper>` at every team's spawn, and a map that carries either now parses, stores
and re-emits instead of losing it. Coinfall is the first board built through that. The report is about the
three things it taught — one about where a keeper goes, one about what a shop board needs that this one
cannot state, and one about a room that is a block out of true.

## What the board is

Two camps face each other across a ten-block gap. Each has an apron behind it, a vault off one shoulder
holding the wool, and a crossing reaching out to the middle — and the middle is **void**, with a build zone
over it. Nothing on this board bridges that gap except blocks a player is carrying.

```
       z −60  ┌────────┐            camp (spawn), y16
              │  camp  │
       z −40  ├──┬─────┴───────────┐ apron, y15   · vault (wool) at the −x end
              │V │     apron       │
       z −25  └──┴──┬──────────┬───┘
                    │ crossing │     y14
       z −10        └──────────┘
                   ─ ─ ─ void ─ ─ ─  the ford: 20 blocks, buildable from the first tick
       z  10        ┌──────────┐
                    │ crossing │
```

`rot_180` fans the lot. 120 × 120 blocks, 12 a side, `cell: 5`. `CT12` measures the strait at **20 blocks**,
inside the 15–40 the rule wants, and the frontline is a straight 60-block run at `z = ±10`.

The ground is deliberately plain — `incline` reads it flat, 0–1 tens of degrees everywhere, and
`03-slopes.txt` says **5600 cells walked, 0 scrambled, 0 barrier, 0 faces**. This board is not about its
terrain; it is about what a player can buy standing in their own spawn.

## The keeper carries no position, and that is the whole placement rule

The finish states the menu and says nothing at all about where the villager stands:

```json
"shops": [{
  "id": "quartermaster",
  "keeper": {"name": "`6`lQuartermaster", "mob": "Villager"},
  "categories": [{"id": "kit", "material": "gold ingot", "name": "`6Supplies", "items": [ … ]}]
}]
```

A shop is a catalogue rather than a place. The studio puts one keeper per shop at **every team's spawn**, on
the spawn's own floor, beside the point players arrive on and turned to face them, with blocks counted from
the block the spawn point stands in. The two it emitted:

| keeper | spawn point | stands at | faces |
|---|---|---|---|
| red | `0,16,-50`, yaw 0 (+z) | `2.5,16,-49.5` | yaw 90 (−x) |
| blue | `0,16,50`, yaw 180 (−z) | `-1.5,16,50.5` | yaw −90 (+x) |

Both are two blocks across the way the team faces, on a block centre, at the spawn's own height — and
`column?at=2,-50` and `column?at=-2,50` both answer a solid floor at `y 15` with air above it, which is the
same course the spawn marker stands on. Nothing is stamped for either: PGM spawns the entity itself at match
load and freezes it, so a shop board exports the moment its intent is stored, with no world build to wait for.

## The board mints no currency, so the shop is priced in wood

This is the finding worth carrying forward. Everything a player holds on a generated board comes from two
places — the spawn kit `TeamsGenerator` writes, and the kill reward `MapStandards` derives from that kit's own
blocks — and **neither pays in anything a shop would normally charge**. Of the corpus's 907 shop icons, 764
are priced in a material no spawn kit carries: emerald 225, nether star 126, gold ingot 118, gold nugget 86.
A first draft of this board priced its menu in gold nuggets and would have shipped a villager nobody could
open an account with.

So Coinfall prices everything in **wood**: 64 in the kit, 16 more a kill, and the menu trades it for the
things a wool run actually needs — a gapple at 16, arrows at 8, ladders at 8, the team's own stained clay at
12, iron bars at 24. That is a real economy rather than a workaround (the corpus prices a third of its upgrade
ladders in the tool they replace), but it is a narrow one, and the reason it is narrow is filed as `PG14`:
the intent has no way to say what a kill pays or what a block drops.

## A room's door bay is a block out of place on its mirror image

Read while checking the keepers were under cover. The shell's roof course is `y = 23`; red's opening spans
`z −54…−51` at `x = 0` and blue's spans `z 50…53`. Under `rot_180` the image of red's is `51…54`, so the two
differ by a block and blue's keeper at `(-1.5, 16, 50.5)` stands under open sky where red's stands under a
roof. `column?at=0,-54` answers no roof block; `column?at=0,54` answers one. Filed against the studio as
`WE121` — the bay is cut from the piece's corner rather than from the frame's centre.

The mirror check does not see it: it compares regions, and both rooms' regions are exact images. Only the
blocks disagree.

## The reads

```
03-slopes.txt   5600 walked, 0 scrambled, 0 barrier; faces: 0
06-claims.txt   placed 0, declined 0            (nothing dressed — the board states no props)
04-routes.txt   spawn → wool walks end to end both ways; the worst steps are the room shells' own walls
coverage        reached 5428, dead 172 of 5600 = 3.1% dead, in two 86-cell patches one block off used ground
preflight       2 teams · 2 wools · 16 regions · 34 filters · 11 apply-rules — export gate OPEN
```

The two dead patches are the far corners of each apron, past the vault. One objective and one spawn a side
make two journeys and those corners are on neither; at 3.1% it is not worth cutting the board down for.

## Rebuilding it

```bash
python3 specs/opus5-coinfall/build-spec.py
tools/drive.py specs/opus5-coinfall "Coinfall" --out maps/opus5-coinfall --renders specs/opus5-coinfall/renders
```
