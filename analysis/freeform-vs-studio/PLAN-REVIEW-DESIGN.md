# The agent's plan, in the studio

**The planning step was the most useful thing the freeform runs added, and the studio has no document for it.**
A pgmvox board starts with a `PLAN.md`: the board's places with what each is for and how it is reached, the
attackers' walks, the numbers set against their targets, two sections, the look, and a version history with the
reason for each change. The author read it and answered it before a block was placed. The studio has three
things a person can see before the build, and none of them carries a reason.

This document proposes where that plan lives, how the studio draws it, how the author answers it, and how an
agent reads the answer. The prototype is `pages/plan-review/index.html`, built over the real Abbeymoor plan in
both its versions (published as the *Plan Review* artifact).

## 1. What each surface says today

**The box plan says what a rectangle is, never why.** A piece has an id, a role (`piece`, `spawn`, `wool-room`,
`buffer`) and a surface. Its `boxes` are annotation the compiler ignores, and the editor shows them to an admin
only. A piece name is the whole of the explanation the plan can hold.

**The sketch says where ground is, never what it is for.** Its shapes make land as soon as they are drawn, so a
sketch is already a build. It is the wrong place to ask "should the abbey be here at all".

**The in-game notes come after the fact.** A note is pinned to a point, box or lasso on an eye picture, has a
thread, and is handed to an agent (`NoteHandoff`). It is the best review surface the studio has, and it can
only be used once there is a world to look at.

**The agent's plan held what none of those does.** Read off `exp-abbeymoor-pgmvox/PLAN.md` and its
`plan-check.json`:

| PLAN.md carries | Studio today |
|---|---|
| the board's identity in two sentences | the map's name |
| eleven places a side, each with *what*, *why* and *how it is reached* | a piece id |
| roads and the attackers' walks A and B as polylines | nothing before the build; `walk` after it |
| twelve numbers, each against a named target (GO1, GO3, GO4, sight, cover, climb) | the GO rules raise on a compiled plan, unseen as a table |
| two sections, each with the reason it was cut there | `transect` after the build |
| the look: materials by role, tone, vegetation | the themes, written into the sketch |
| what the build adds that the plan does not show | nothing |
| a self-review against the lessons | nothing |
| v1 → v2 with what changed and why | the change list, with no reason attached |

## 2. The design: a document the levels are measured against

**The plan of places is a fifth document beside the four levels, not a level of its own.** The four levels are
grains of one map, and each one compiles into the next. A plan of places compiles into nothing. It states what
the map is *for*, and every level is read against it: the box plan, the sketch and the world are each asked
whether they still do what the places say.

**It is stored per map, as `design_json`, and changed by the same numbered changes as the other documents.**
That gives it diff and restore for free. Its versions are the map's changes that touched it, each with the
`because` the agent wrote.

**Its fields, worked on Abbeymoor.** The points are the plan's own (spawn at (0, -112), Monument A at
(-40, -72), the walk's bends from `plan-v2.json`); the hill's ring and the crypt's box are drawn round them for the
example.

```json
{
  "design": 1,
  "identity": "Destroy the monument for two teams of 16. One moor island; each team holds an abbey hill above a village, a peat bog between.",
  "places": [
    { "id": "abbey-hill", "name": "Abbey Hill", "kind": "objective-ground",
      "at": { "ring": [[-58,-88],[-26,-88],[-26,-56],[-58,-56]] }, "floor": 80,
      "what": "A plateau with 38° slopes carrying the ruined nave; Monument A stands on a dais in the chancel.",
      "why": "The defenders hold height over the bog; the attackers have to climb into view.",
      "reach": ["hill-track", "night-stair"] },
    { "id": "monument-a", "name": "Monument A", "kind": "objective",
      "at": { "point": [-40, -72] }, "floor": 88, "objective": "destroyable-1",
      "what": "A pillar of three obsidian blocks, four over its dais.",
      "why": "Seen from the bog edge; reached on foot or from below.",
      "reach": ["hill-track", "night-stair"] },
    { "id": "crypt", "name": "The crypt", "kind": "underground",
      "at": { "box": [-50, -80, 20, 14] }, "floor": 70, "storey": -1,
      "what": "A vaulted hall under the abbey, a passage under the valley to the Tithe Barn's cellar.",
      "why": "A second way to A that is longer but out of sight.",
      "reach": ["cellar-passage"] }
  ],
  "routes": [
    { "id": "walk-a", "team": "blue", "from": "spawn-blue", "to": "monument-a", "purpose": "attack",
      "line": [[-1,111],[-1,65],[-3,18],[-20,-28],[-42,-69]] },
    { "id": "hill-track", "from": "spawn-red", "to": "abbey-hill", "purpose": "defend",
      "line": [[0,-112],[-24,-94],[-40,-80]] }
  ],
  "targets": [
    { "id": "own-walk", "measure": "walk", "from": "spawn-red", "to": "monument-a", "rule": "GO4" },
    { "id": "enemy-ratio", "measure": "ratio", "of": ["walk-a", "own-walk"], "rule": "GO1", "want": [3, 4] },
    { "id": "sight-a", "measure": "sight", "to": "monument-a", "band": [25, 60], "want": [0.25, null],
      "why": "found without a map" },
    { "id": "passage-cover", "measure": "cover", "over": "crypt", "want": [3, null] }
  ],
  "sections": [
    { "id": "sec-hill", "line": [[-110,-72],[110,-72]],
      "why": "Through both monuments' latitude: the hill, the bog and the village in one profile." }
  ],
  "look": { "biome": "moor", "roles": { "house-wall": "clay over a stone course", "path": "coarse dirt and gravel" } },
  "adds": ["58 boulders", "31 trees in copses", "vines on the rim ledges"],
  "review": [ { "lesson": 7, "met": true, "how": "a solid island, bedrock at y 1" } ]
}
```

**A place's geometry is loose by design, and binds to the levels when they exist.** `at` is a point, a box or a
ring in blocks, and that is all an agent knows before a plan is drawn. Once a box plan or a sketch exists, a
place may name what realises it: `"binds": {"pieces": ["plateau"], "shapes": ["sh-12"], "objective":
"destroyable-1"}`. A bound place is drawn from its pieces and shapes, and an unbound one from its own `at`.

**A target is a measurement request, never a number the agent writes.** The agent states *what* to measure and
*what it should be*. The studio measures it on the best level that exists: the compiled plan's cells, the
sketch's ground, or the built world. A target's row therefore carries up to three readings, and the review
sees a number move from plan to build.

**The measures are the studio's own reads, named once.** `walk` and `ratio` are the GO rules' walk; `cover`,
`climb` and `reach` are the `column`, `walk` and `reach` reads; a `section` is `transect`. `sight` is the one
new read: the share of the ground in a distance band from which any face of the objective is visible, which
the visibility audit measured by hand (studio median 55% against freeform 31%).

## 3. How the author answers it

**The note anchors gain five plan kinds, and everything else about a note stays.** `NoteAnchors` today is
`map`, `view`, `point`, `box`, `lasso`. A plan review adds `place`, `route`, `target`, `section` and
`plan-point`, each naming the id it is pinned to and the design version it was written at. The thread, the
statuses, the replies, the pictures and the hand-off are the existing `MapNoteDto` and `NoteHandoffDto`
unchanged.

**An in-game note is tagged with the place its ground falls in.** A point or lasso note already carries the
ground it hit (`Hit`, `Ground`, `Columns`). The studio looks that ground up in the design's places and stores
the place id beside it, so "the cube is too big" on an eye picture reaches the agent as a note on
`monument-a`. That is what joins the two review surfaces into one record.

**The plan carries a verdict, and the build waits on it.** A design version is `proposed`, `changes` or
`approved`. The author sets it from the review sheet. The agent's skill does not build on a version that is not
approved, which is the "waiting on a go" stop the freeform runs used by hand. It is a convention in the loop,
not a refusal in `PUT source`, because a person driving the studio directly should not be blocked by a sheet
they never wrote.

## 4. What the sheet shows

**The review sheet is one page: the map, the places on it, and three tabs beside it.** The map is whatever
exists, drawn underneath: the agent's height raster for a freeform plan, the box plan's cells, the sketch's
shapes or the eye top-down. Over it go the places with their labels, the roads, the attackers' walks, the
storey below, and the section lines, each a layer the author can toggle.

**Clicking a place opens its focus panel.** It shows the kind, *what*, *why* and how it is reached, the targets
that name it, and a section through it if one is cut there. A note written from the panel is pinned to that
place.

**The Numbers tab is the targets as a table, coloured by whether each is met.** Each row is a note anchor of
its own, so "GO3 is a miss you accepted; is it?" is pinned to the GO3 row.

**The version toggle shows what changed.** Places and routes that are new, moved or removed between two design
versions are marked on the map, and the agent's `because` is shown beside each.

The prototype does all of this over the pgmvox Abbeymoor plan's v1 and v2. Its notes and verdicts are kept in
the artifact's own store, where an agent reads them; in the studio they would be `map_note` rows.

## 5. The API

| Endpoint | Does | Fails with |
|---|---|---|
| `PUT /map/{slug}/design` | stores the design as a numbered change, with a `because` | 400 unreadable; 400 a place, route or target naming an id that does not exist |
| `GET /map/{slug}/design[?change=]` | the design at a change, with every target measured on the best level that exists | 404 no design |
| `GET /map/{slug}/design/diff?from=&to=` | places, routes and targets added, moved, removed, each with its `because` | 400 no such change |
| `GET /map/{slug}/design/sheet.png` | the sheet as one picture, for an agent that reads pictures | — |
| `POST /map/{slug}/notes` | unchanged; the anchor may now be a plan kind | 400 an anchor id not in the design |
| `PUT /map/{slug}/design/verdict` | `proposed`, `changes` or `approved` for the current design version | 403 not the map's author |

`PUT /map/{slug}/source` takes `design` as one more member beside `plan`, `layout` and `intent`, so a headless
caller stores everything in one call.

## 6. The model's loop

1. The agent writes the design (identity, places, routes, targets, sections, look) and stores it. No plan or
   sketch need exist yet.
2. The studio measures what it can and draws the sheet.
3. The author reads the sheet, writes notes on places, routes and rows, and sets `changes` or `approved`.
4. The agent reads the notes through the hand-off, answers each one, revises the design with a `because`, and
   stores the next version.
5. On `approved`, the agent builds: the box plan or the sketch, then the world. Each place is bound as its
   pieces and shapes are drawn.
6. The targets are re-measured on the built world, and the in-game notes arrive tagged with their places.

**Every route into a map keeps working.** A box plan drawn by hand needs no design. A generated board can get
one written over it. An uploaded world can be given a design afterwards, to review the map as it is played: the
places are drawn on the eye top-down and the targets measured on the scanned ground.

## 7. Order of work

1. `design_json`, its `PUT` and `GET`, inside `source`, with diff. No measuring yet.
2. The sheet in the client as a read-only tab, drawing places, routes and sections over whatever level exists.
3. The plan note anchors and the verdict.
4. Targets measured on the compiled plan, then on the built world. `sight` is the new read.
5. In-game notes tagged with their place.
6. Recipe steps naming the places they build, so the inspector can show one place's steps
   (`STUDIO-2-DESIGN.md` §5).

## 8. What the prototype is and is not

**It is the sheet and the review, over a plan the studio did not make.** It reads `data/plan-v{1,2}.json` and
three rasters per version, exported from the pgmvox board at commit `869a81d6` (v1) and its revision (v2). The
place descriptions are taken from `PLAN.md`.

**It does not measure anything itself.** Its Numbers tab shows the plan-check rows pgmvox wrote. Notes and the
verdict are written to the artifact's `db` (`notes`, `verdicts/{version}`), and one agent note, on Monument
B's sight, is there to show a thread started from the other side. Opened from this folder over plain http, the
page draws everything and keeps no notes.
