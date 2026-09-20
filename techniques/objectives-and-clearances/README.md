# Objectives and clearances

**An objective is a statement in the intent, not in the layout, and the world gets it at the export.** That
is why this card is a map rather than a grid of panels: one island with five stations along it — red's
spawn, a monument, a core, a wool room, blue's spawn — and a second half that is the same board exported
again with one fault in it at a time. Open it in the studio as `technique-objectives-and-clearances`, or run
`build.py`.

**Two gates judge where a goal may stand and neither is heard before the export.** `OB17` refuses the whole
export at **409** and names which of its three places the goal hit; `OB19` answers **200** and leaves the
offending prop out of the world. `exports.txt` is eight exports of one board, and it is the card.

## The document

The layout is one rectangle 420 × 100 with two `area` marks — a plain at 12 west and a shelf at 22 east —
plus a gravel patch under the monument that paints `OB19`'s keep-out where it can be seen, and five thin
raised walls that make the wool room. The intent is the other file.

| station | at | what it states | what the export built |
|---|---|---|---|
| red spawn | (−180, 0) | a point and a 20 × 20 protection box | the spawn region, and a place no goal may stand |
| monument | (−70, 0) | `pillar-3`, obsidian, `float: 4` | three obsidian from **y16** over ground at y11 |
| core | (30, 0) | `lava: 3`, `float: 6`, `leak: 5` | a five-block box from **y27** over ground at y19 |
| wool room | (130, 0) | a protection box and one entry | the wool at **y25**, inside four walls |
| blue spawn | (180, 0) | the mirror of red's | the same |

```json
{"owner": "blue", "name": "Fold Monument", "style": "pillar-3", "materials": "obsidian",
 "float": 4, "anchor": {"x": -70, "y": 11, "z": 0}}
```

**The wool columns high over every goal are the beacons, and they are not a fault.** `GoalMarkerStamper`
stands three courses of wool at `max_build_height` plus `BuildCeiling.MarkerOver` — five — so the sign is
out of every player's reach by construction. `techniques/destroy-goals` reads the arithmetic back against a
board's own `<maxbuildheight>`.

**An anchor is an absolute point and the studio seats nothing for you.** Every `y` in the intent above was
read off the built world with `column` first. There is no "on the ground" — a goal states the height it
stands at.

**A placement carrying `"stamp": null` voids the whole `PUT /intent`.** The call answers **200** with an
empty body and stores nothing at all, teams and `maxPlayers` included; omit the field instead. It cost this
card an hour, and it is the only way the studio lies about having stored something.

## What `float` builds, and what it is for

**`float` is geometry: the goal's base is the standing level plus the number.** Over ground topping at y11 —
a standing level of y12 — the monument's obsidian starts at **y16** at `float: 4` and at **y20** at
`float: 8`. The same number on the core puts its casing at y27 over a bank topping at y19.

**At `float: 0` a destroyable is not a pillar at all.** The same `pillar-3` comes out as a **single**
obsidian block at y14: the courses that should have been below it are where the goal's chest and the ground
already are. A monument on the ground is not a monument.

**And a core at `float: 0` loses its floor.** At `float: 6` the column reads obsidian, three lava, obsidian —
a closed box. At `float: 0` it reads three lava with a lid and **no obsidian under them**: there is nowhere
for the lava to fall, so the core cannot leak, which is the whole of what a core is.

**So a destroyable and a core float above the terrain by design**, and that is PGM's behaviour rather than
the studio's invention. The four and the six are not clearance from the ground; they are what makes the
goal completable at all.

## What `leak` is, and where to look for it

**`leak` is not geometry.** Exported at `leak: 0`, `leak: 5` and `leak: 10` with `float: 6` held, the core's
column is identical every time: obsidian at y27, lava y28–30, obsidian at y31. Nothing in the world's blocks
carries the number.

**It is an attribute on the `<core>` element, and the studio writes it only when it is not PGM's own
default.** At `leak: 5` the export writes `<core id="bank-core" name="Bank Core" team="red-team"
mode-changes="true" region="bank-core-region"/>` with no `leak` at all; at 10 the same element carries
`leak="10"`. `map-xml.txt` is that half of the document.

**Which means the read that answers a question about a leak is the map.xml, and a column read cannot.**

## `OB17` — the three places a goal may not stand

**It refuses the export at 409, and its message names which of the three it hit.** The same monument moved
three ways, each export in `exports.txt`:

- **past the coast**, to x −230: *"is 1×1 and overhangs the void — the build slice denies breaking blocks
  out there, so the goal could never be completed"*.
- **into red's spawn protection**, at (−180, 0): *"reaches into the spawn on 'red' — spawn protection denies
  breaking blocks to every team, so the goal could never be broken"*.
- **into the wool room**, at (130, 0): *"reaches into the wool room on 'red' — the room's own rules would
  cover the goal"*.

**All three are the same fault in different words: a place the map's own rules make the goal's blocks
unbreakable.** None of them is a geometry check an author can run earlier — the board stores clean, finishes
clean and refuses only when the world has been built and the regions written.

## `OB19` — the ten blocks about a goal

**A tree, a boulder or a building inside a goal's clearance is declined, and the map is built without it.**
The export answers **200** with `Pgm-Warnings: 1 OB19`, because *"a goal is what the map is for, and a prop
is removable, so the map is built without it rather than refused for it"*.

**Measured on one boulder, twice.** An `erratic` six blocks west of the monument comes back as
*"boulder 'rock' rests on (−65, −1), inside a goal's clearance"* and is not in the world; the same boulder
sixteen blocks west is built, and the export is clean.

**The box is the ground the goal's structure covers grown by four blocks, and never nearer than ten to the
marker.** On this board the marker is 1×1, so the keep-out is the ten-block square the gravel patch under it
is painted to — `monument.png` is that square with the pillar standing in it.

## What else the export said

**`EX6` is the one warning an otherwise clean board earns: nobody is named as its author.** *"The board is
the first thing every player who joins reads and it is the only place a map says who built it — the studio
will not invent a name, so the sign is left off rather than stamped blank."* Naming one in `meta.authors`
clears it.

## The recipe

**Place the goals last, and read the ground before you state an anchor.**

```json
{"destroyables": [{"owner": "blue", "style": "pillar-3", "materials": "obsidian",
                   "float": 4, "anchor": {"x": -70, "y": "<the top block, read>", "z": 0}}],
 "cores": [{"owner": "red", "lava": 3, "float": 6, "leak": 5,
            "anchor": {"x": 30, "y": "<the top block, read>", "z": 0}}]}
```

- **never state `"stamp": null`** — omit it, or the whole PUT stores nothing and says 200.
- **leave `float` alone**: 4 on a destroyable and 6 on a core are what make them completable.
- **`leak` lives in the map.xml**, so check it there and not in the world.
- **keep every goal ten blocks clear of the coast, of every spawn protection and of every wool room** — all
  three are `OB17`, and all three are heard only at 409.
- **keep trees, boulders and buildings out of a ten-block square about each marker**, or they are quietly
  left out of the world.
- **name an author.**

## Limits

**The half-block reading of a plan's `at` is not on this board.** `DestroyablePlacement.at` and
`CorePlacement.at` belong to a *plan*, and this card drives the sketch and the intent; the finding that they
are read as blocks rather than half-blocks stands in `GENERATION-NOTES.md` where it was measured.

**Nor is a goal under a deck.** `OB17` asks whether a goal stands over void, in a spawn or in a wool room,
and a monument sealed under a concourse is none of those — it exports at 200 as long as something walks to
it. That claim is the layer cards' ground and not re-measured here.

## What checks it

- `exports.txt` — eight exports of one board: the clean one, three `OB17` refusals with their own messages,
  an `OB19` decline and the same prop moved out of the box, and `float: 0`.
- `columns.txt` — the three goals as built, and the same two numbers swept: the monument at float 0, 4 and 8
  and the core at float 0 and 6 against leak 0, 5 and 10.
- `map-xml.txt` — the teams, spawns, wools, destroyables and cores the export wrote, which is where a leak
  is and where a float is not.
- `objectives-and-clearances.intent.json` — the one intent the board exports at 200 from.
- `objectives-and-clearances.layout.json` — the island, the keep-out patch and the wool room's walls.
- `incline.txt` · `slopes.txt` — the ground the stations stand on.

Renders: `monument.png` — the pillar in its ten-block square; `section-goals.png` — a cut along the island
with both goals floating over it; `iso.png` for the whole board.
