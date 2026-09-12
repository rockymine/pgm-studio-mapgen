# Paint this board

*The text below is what an agent is given, verbatim. Nothing else — no examples, no material advice, no
numbers. Substitute `<base>`, `<slug>` and `<place>`.*

---

Board `<slug>` at `<base>` is built and unpainted. It was drawn by hand: ten layers, ground cut by a tunnel,
structures standing over it, two wool rooms and two spawn rooms. It has no theme registry, no map theme and
no room shells — everything about how it *looks* is missing, and that is your job.

**Make it read like `<place>`.**

Three things to author:

1. **The terrain paint.** Register whatever themes the board needs and say which shape wears which. A theme
   states what its rim, surface, wall and fill are made of; a shape with no theme of its own takes the map
   default.
2. **The wool room and spawn room shells.** Each is a room the build stamps — floor, walls, roof, a door.
   Author both so they belong to the place the rest of the board is.
3. **The dressing, if the place wants any.** Trees, boulders, ground cover, paths, water. A tree or a
   boulder is a recipe from the library named on a placement; a path or a channel is traced where it goes.
   A board with nothing on it is a legitimate board, so this is yours to judge.

Work only through the API. It is the whole of what you have and it answers for itself: every route, its
parameters and its response schema are at `<base>/api-docs`, over the document at
`<base>/api/openapi/v1.json`.

The routes you will want:

| | |
|---|---|
| `GET /api/map/<slug>/sketch` | the board — its setup, its layers, its shapes |
| `GET /api/map/<slug>/sketch/layers` | the layers alone, with each one's shapes |
| `GET /api/terrain/blocks` | the blocks a material may be built from |
| `GET /api/terrain/patterns` | every material kind, its fields and its defaults |
| `PUT /api/map/<slug>/sketch/themes/{id}` | register a theme under a name |
| `PUT /api/map/<slug>/sketch/map-theme` | which theme covers every shape that names none |
| `PATCH /api/map/<slug>/sketch/shapes/{shapeId}` | put a theme on one shape |
| `PUT /api/map/<slug>/sketch/room-styles/{part}` | bind a shell — `wool` or `spawn` |
| `GET,POST /api/tree-styles` · `/api/boulder-styles` | the recipe library a placement names |
| `POST /api/map/<slug>/sketch/props` | put one thing on the board |
| `POST /api/map/<slug>/sketch/dressing` | write the placements whole |
| `POST /api/terrain/theme-preview` | render a finish before committing to it |
| `POST /api/room-styles/preview` | render a room shell the same way |
| `POST /api/tree-styles/preview` · `/api/boulder-styles/preview` | render a recipe before saving it |
| `GET /api/map/<slug>/render/surface?format=png` | the board as it now paints |
| `GET /api/map/<slug>/render/section?format=png` | a cut through it |
| `GET /api/map/<slug>/findings` | what the studio makes of the document |
| `GET /api/rules?rule=<id>` | what any rule id means and how to answer it |

**Look at what you have made before you call it done.** The renders above are the board itself, not a
mock-up of it.

When you are finished, say in a sentence or two what you were going for and where you think it fell short.

---

## Running it

`<slug>` must be a copy. Load the three documents beside this file under a slug of the run's own:

```sh
BASE=http://localhost:7894 SLUG=probe-run-1 python3 load.py
```

Run it from this directory. `BASE` is whichever server the run is against and `SLUG` is that run's own.

A freshly loaded board answers `SK8` — no finish — and three `SK11`, which are true of its geometry and not
about paint. Neither is a run's to answer.
