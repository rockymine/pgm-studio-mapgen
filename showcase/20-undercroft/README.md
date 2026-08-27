# 20 — an undercroft, and why it is rock with rooms cut out of it

**The technique: a second storey under the landmass. A sketch layer carries one span per column, so a
room drawn on its own leaves every other column of that storey empty — the board's lower half is air
and the ground above it floats. What is stated is the ROCK, over every column the board has, and the
rooms are the holes in it.**

This forks `02-theme`. The plan gains one number and the finish gains a layer.

## The lift

A storey needs somewhere to be, and `02-theme`'s ground stands at y9 with the world floor eight
courses under it. So the plan says its ground stands higher:

```json
"globals": { "surface": 22 }
```

and the finish thins that slab to its top eight courses, leaving the fourteen under it free:

```json
"shapePropsByHeight": { "22": { "floor": 14, "base_height": 8 } }
```

The surface does not move — the compiler seats the spawns and the wool rooms at y22 and the landmass
still tops out there. What moves is its **floor**. Lift the surface without telling the plan and the
spawns stay at y9 while the ground goes to y22; the buildability check then reports every placement
over open void, because the marker is thirteen courses under the ground it names.

## The rock

```json
{ "id": "under", "name": "Undercroft", "base_y": 0, "below": true,
  "shapes": [ … 11 rock rectangles, 2 room floors … ],
  "islands": [ { "id": "under", "mirrors": true, "shapeIds": [ … ] } ] }
```

`below: true` inserts the layer under the compiled ground rather than over it. Its shapes are all
**adds**: the rock is banded round its holes rather than cut with subtracts, which is the first thing
this board measures.

The rock runs `floor 0`, thirteen courses, meeting the landmass's own underside at y14. A room is a
shorter span in the same columns — `floor 0`, seven courses — so its floor is stood on at y8 and it
has six courses of headroom under the rock's ceiling.

## Three things it measures

**A subtract is a claim about the whole stack, not about one layer.** Cutting the rooms out of a slab
with `operation: "subtract"` is the obvious way to write this, and it is refused:

```
SK13  's0' fills 400 column(s) that 'cut1' takes away — from (-38, 20)
      's0' is on layer 'ground' and the subtract on 'under', and a subtract reaches only the layer it is on
```

The subtract states that the column is *empty*, and the landmass over it then fills what the storey
below said was void. The same refusal fires the other way for the board's own void: state rock over
the whole bounding box and the compiler's `s1` — the hole `02-theme` cuts to put its fill ratio in
band — is filled in from below. So the rock is stated as **adds only**, over the rectangles the
board's land decomposes into, banded round every hole. `bands_around` in the generator is the whole of
it: split into z-bands at every hole edge, split each band in x, drop the parts that fall inside a
hole.

**The tiling is checked, not looked at.** A missing column is invisible in every render — the rock
above and below it hides the gap — so the generator counts: over the board's **8,250 columns, none is
bare and none carries two spans**. That check is what makes the technique safe to repeat.

**A structure at the board's edge stands higher for the lift.** Raising the ground thirteen courses
raises everything the plan stamps with it, and `02-theme`'s wool room sits against the void:

```
WX11  roomfloor room 0 stands 22 blocks above the cell beside it at (19, 96) — 43 of them over the void
```

Four of them, one per wool room and its redstone line — the same complaint the base board raises at 9.
It is a complaint and the gate opens; on a real board the answer is to keep a stamped structure off
the void edge, not to stop lifting.

## The way down

The stairwell is a hole in the rock like any other room, and the flight is **one rectangle a course**,
cut into the landmass as an override add:

```json
{ "id": "st1", "type": "rectangle", "operation": "add", "override": true,
  "keepClear": true, "floor": 8, "base_height": 14,
  "min_x": -38, "min_z": 73, "max_x": -30, "max_z": 74 }
```

Fourteen of them, each a course shorter than the last, so the descent is one block a step and walks
both ways for nothing. A ramp at one course a cell rasterizes into treads of two, and a two-block rise
costs a placed block.

Two numbers matter and both are the same number. The treads' `floor` is **8** — the room floor's own
top — so the flight rests on the storey below rather than driving through it (`SK10` is what says
otherwise). And an override add is what cuts the shaft: a subtract there would be `SK13` again, and a
hole left by arrangement is declared a void and emits the same subtract. The override overwrites the
column it lands on, floor and all, and the shaft is the air left over the treads.

`keepClear: true` keeps the dressing pass off the flight — see `21-wall-and-stair`.

## What to look at

| | |
|---|---|
| `renders/section-shaft-x-34.png` | the cut down the shaft: landmass, treads, room, rock |
| `renders/under-heightmap.png` | the storey alone — `?layer=under`, which is how a stacked board is read |
| `GET …/column?at=-33,40` | quartz floor y7, air 8–13, landmass 14–21, bedrock y0 |

```bash
python3 tools/drive.py showcase/20-undercroft "Undercroft" --out showcase/20-undercroft/world
```
