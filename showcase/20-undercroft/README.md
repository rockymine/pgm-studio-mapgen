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

The surface does not move — the compiler seats the spawns and the destroyables at y22 and the landmass
still tops out there. What moves is its **floor**. Lift the surface without telling the plan and the
spawns stay at y9 while the ground goes to y22; the buildability check then reports every placement
over open void, because the marker is thirteen courses under the ground it names.

## The rock

```json
{ "id": "under", "name": "Undercroft", "base_y": 0, "below": true,
  "shapes": [
    { "id": "rk1",  "type": "rectangle", "operation": "add", "floor": 0, "base_height": 14,
      "theme": "rock", "min_x": -50, "min_z": -50, "max_x":  50, "max_z": -30 },
    { "id": "rk2",  …  "min_x": -50, "min_z": -30, "max_x": -30, "max_z":  30 },
    { "id": "rk3",  …  "min_x":  30, "min_z": -30, "max_x":  50, "max_z":  30 },
    { "id": "rk4",  …  "min_x": -50, "min_z":  30, "max_x":  50, "max_z":  50 },
    { "id": "hall", "type": "rectangle", "operation": "add", "floor": 0, "base_height": 8,
      "theme": "room", "min_x": -30, "min_z": -30, "max_x": 30, "max_z": 30 }
  ],
  "islands": [ { "id": "under", "mirrors": false, "shapeIds": [ … ] } ] }
```

`below: true` inserts the layer under the compiled ground rather than over it. Its shapes are all
**adds**: the rock is banded round its hole rather than cut with a subtract, which is the first thing
this board measures. Four bands and one hall is the whole storey — a picture frame with a room in it —
and that is what a plain square buys over a board with a complicated outline.

The rock runs `floor 0`, fourteen courses, meeting the landmass's own underside at y14. The hall is a
shorter span in the same columns — `floor 0`, eight courses — so its floor is stood on at y7 and it
has six courses of headroom under the rock's ceiling.

**`mirrors: false`, and that is not a detail.** The storey covers the whole board, so its own `rot_180`
image lies over it; fanning it would put every column's ground back twice. A layer that covers only one
half is fanned and one that covers both is stamped once, and the rule that shapes it then has to be its
own image — which is `23-maze`'s whole subject.

## Three things it measures

**A subtract is a claim about the whole stack, not about one layer.** Cutting the hall out of a slab
with `operation: "subtract"` is the obvious way to write this, and it is refused twice over:

```
POST /map/from-documents   422
SK13  's0' fills 3600 column(s) that 'cut1' takes away — from (-30, -30) — 's0' is on layer 'ground'
      and the subtract on 'under', and a subtract reaches only the layer it is on
SK13  'descent' fills 56 column(s) that 'cut1' takes away — from (-22, 2)
```

The subtract states that the column is *empty*, and the landmass over it then fills what the storey
below said was void — the whole board's worth of it, since the landmass covers every column the hall
does. So the rock is stated as **adds only**, banded round its hole. On a rectangular board with a
rectangular hall that is four rectangles; the general form is to split into z-bands at every hole edge,
split each band in x, and drop the parts that fall inside a hole.

**The tiling is checked, not looked at.** A missing column is invisible in every render — the rock
above and below it hides the gap — so it is counted rather than inspected: over the board's **10,000
columns, none is bare and none carries two spans**. That check is what makes the technique safe to
repeat, and it is the one thing a hand-drawn band set gets wrong.

**A shorter add inside a taller one does nothing at all, and no gate says so.** Writing the rock as one
rectangle over the whole board and the hall as a shorter add in the same columns compiles, builds and
exports with the gate **OPEN** — and there is no hall: a layer holds one span per column and the taller
add wins it outright, so the eight-course hall is simply not there. `SK9` is right to stay silent
(two adds at one floor are ordinary ground, and the taller winning is what "height is the tallest add"
means), which is exactly why the banding is the technique rather than a detail of it.

## The way down

The stairwell is a hole in the rock like any other room, and the flight is **one polygon**, cut into
the landmass as an override add whose anchors fall a course a block:

```json
{ "id": "descent", "type": "polygon", "operation": "add", "override": true, "keepClear": true,
  "floor": 8, "base_height": 14, "theme": "stair", "height_mode": "level", "skirt": 0,
  "vertices":       [[-22,2],[-18,2],[-18,16],[-22,16]],
  "anchor_heights": [   1,     1,      14,      14   ] }
```

Fourteen courses over a fourteen-block run, so the descent is one block a step and walks both ways for
nothing. Measured, `x −20` from the foot to the head:

```
z   2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
y   8  9 10 11 12 13 14 14 15 16 17 18 19 20 21
```

One repeat at `z 8/9` — fourteen courses do not divide fifteen cells — and every other step is exactly
one block. A ramp at one course a cell only rasterizes cleanly because the surface is sampled at the
cell's centre and **floored** into the column; rounding it to nearest puts every sample of a 1:1 grade
on the boundary and the flight comes out as a beat of noughts and twos.

Two numbers matter and both are the same number. The flight's `floor` is **8** — the hall floor's own
top — so it rests on the storey below rather than driving through it (`SK10` is what says otherwise).
And an override add is what cuts the shaft: a subtract there would be `SK13` again. The override
overwrites the column it lands on, floor and all, and the shaft is the air left over the treads.

`keepClear: true` keeps the dressing pass off the flight — see `21-wall-and-stair`.

## What to look at

| | |
|---|---|
| `renders/world-section-z0.png` | the cut across the board: landmass over a band of air over the hall's floor |
| `GET …/render/section?axis=z&at=-20&from=-10&to=30&scale=10` | the flight, in the one view a grade exists in |
| `renders/world-heightmap.png` | the two flights as slots cut into an otherwise flat surface |
| `GET …/column?at=0,0` | quartz floor y7, air 8–13, landmass 14–21, bedrock y0 |

```bash
python3 tools/drive.py showcase/20-undercroft "Undercroft" --out showcase/20-undercroft/world
```
