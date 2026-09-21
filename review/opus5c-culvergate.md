# Culvergate — a works fought room by room, and the middle pays double

> Capture the points. A brick waterworks: the middle point inside a long engine
> hall divided into three rooms by cross-walls whose doors are on opposite hands,
> and the two flank points in settling yards walled on two sides apiece. The
> hall's roof and the gantries out to the yards are a second storey, so two
> players heading for the same point need never meet until one arrives.

## Where the four things are

| The thing | Where | Measured |
|---|---|---|
| The Cistern | `(0, 0)`, inside the hall | pays **2**, no line to either spawn |
| West Settling | `(-44, 0)` | pays **1**, **0.79** of the centre-to-spawn distance |
| East Settling | `(44, 0)` | pays **1**, the same walk from both spawns |
| the hall | `x -32..32, z -10..10` | three rooms, doors at opposite hands |
| the roof / gantries | base_y 15 | reached by one flight a team |
| score limit | — | 750, the corpus's own answer |

## The one decision the board is built on

**The middle pays two against the flanks' one.** A board whose points all pay
alike is a board two teams settle by taking one each and standing on them: each
side holds what is nearest, the score runs level, and nothing on the map is worth
crossing it for. The corpus is narrower than it looks here — 13 of 83 KotH boards
vary the rate at all, and in 10 of those 13 the highest-paying point is the one
named for the middle, at a ratio of roughly two to one.

**And the flanks stand at 0.79 of the centre-to-spawn distance, which is the top
of the corpus's 0.52–0.88 range.** A pair close to the middle is a pair the team
holding the middle also covers, and three points collapse back into one place.

## What the ground is made of

**There is no relief on this board, and that is the decision rather than an
omission.** A capture board is a control game: its ground is built — plazas,
yards, decks, walls — and relief is a blunt instrument beside a wall somebody
placed on purpose. A board that answers the gamemode's name literally and stands
its points on a hill has already lost the game the mode is about, because the
first team onto a high pad keeps it. Every cell here is level and every height on
the board is a course somebody laid.

Three themes: the flags carry 81.5% of the cells, the garth 11.4% and the
settling beds 7.2%. The surface is a **depth** stack rather than a slope one,
because the slope axis answers a landform's question and this board has none.

## The techniques, and what each one bought

**Cover is built, and it comes in two sizes.** Ten boxes two and three courses
tall stand inside the hall's rooms, inside the yards and out on the floor —
small cover is what makes a space survivable, and an open room with nothing in it
is a room nobody crosses. Two brick pillars ten blocks across stand one in each
team's approach: a pillar a player goes round from two sides is not an obstacle,
it is a decision, and it splits one space into two approaches that hide each
other.

**The zigzag is two cross-walls and nothing else.** `bay-w` runs `x -18..-16,
z -10..2` and `bay-e` runs `x 16..18, z -2..10`, which are each other's rot_180
image — so a player crossing the hall goes north to pass the first and south to
pass the second, the same way for both teams, and each of the three rooms is
entered at a door the defence knows.

**A gantry crosses four blocks of open floor on nothing at all.** The painter
writes each layer over its own span only, so the air under a deck stays air.
Dropping from a gantry at y15 into a yard at y8 is seven blocks: it can be left
and not re-entered, which is how a board makes an approach committing.

**The plan states the point COUNT and the finish states the geometry.**
`placements.controlPoints: 3` is what keeps `PL3` quiet — it counts the capture
points a board states a count of — and the three points are written already fanned
into the finish, because a compiled intent carries no symmetry.

## What went wrong

**The works was a rectangle and 727 of its cells were dead — 9.3%, in four
corners behind the yards.** On a capture board that is a fault rather than a note:
every part of the board is there to offer a different way toward a point.

**Two fixes moved it by nothing at all, and the reason is worth keeping.** A
second mouth into each yard and a road round the back made the corners a real
approach and coverage did not shift one cell, because the read measures journeys
between waypoints and a journey takes the short way. Four settling tanks carved
into the corners did not shift it either, because coverage reads the layout's
ground and a water prop is a dressing pass that runs after it.

**What answered was the plan.** The works is a cross rather than a rectangle now
— a middle band 72 × 56 with two 16 × 24 arms that stop where the yards do — and
the board reads **0.9% dead**. The corners had to stop existing.

**`EX5` stands and is the studio being honest.** The observer platform is stated
at y24 and the board builds to y36 over `(0, 0)` — the capture point's own sky
marker — so it stands at y37 instead.

## Coordinates

| Thing | Position | Reading |
|---|---|---|
| The Cistern | `(0, 0)` | `points="2"`, inside the hall, walled on four sides |
| West Settling | `(-44, 0)` | `points="1"`, mouths east and north |
| East Settling | `(44, 0)` | `points="1"`, mouths west and south |
| the zigzag | `(-17, -4)` / `(17, 4)` | two cross-walls, doors on opposite hands |
| the flights | `(-24, 26)` / `(24, -26)` | anchors 9 → 16, arriving at the roof's edge |
| the map.xml | — | `<gamemode>koth</gamemode>`, `<king>`, `<limit>750</limit>` |
| whole board | `104 × 136` | 6 686 walked · 16 scrambled · 100 barrier · 2 faces |
| coverage | — | **0.9% dead** |
| dressing | — | 16 placed, **0 declined**, and no tree or boulder anywhere |
