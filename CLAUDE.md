# pgm-studio-mapgen

Maps authored by driving pgm-studio's HTTP API. `AUTHORING-BRIEF.md` is what a board should be;
`README.md` is what is here.

**Building, changing, diagnosing or reading a map: invoke the `pgm-board` skill first.** It carries the
lookup table from question to the read that already answers it, and the two moments to stop at. It is
distilled from 24 run reports and every rule in it cost at least one build.

Three things that are true before the skill loads:

- **The studio is already running — do not restart it. Where it listens is not a constant.** It has been
  a different port on every environment the boards here were built on, so nothing states one: set
  `PGM_STUDIO_API`, or let `tools/drive.py` find it by asking `GET /api/health` at the candidates it
  knows. If you write a port into a document, you have written down the machine you happened to be on.
- **Do not write a second copy of the system.** A `specs/<slug>/build-spec.py` that generates the plan
  and the finish is the authoring work and is expected. A script that reads the *built world* —
  a ground-finder, a section renderer, a walk or clearance check — is not, wherever it lives, including
  a scratch directory. Those reads exist: `column`, `transect`, `slopes`, `walk`, `sketch/dressing`,
  all with `?format=text`. The one exception is a world that is not a stored map (a community map, a
  hand-finished world) — then `tools/anvil.py` and its four siblings.
- **Read the text before the pictures.** `tools/drive.py` writes ~25 `?format=text` reads beside every
  render. A picture answers *whether* something came out; a number answers *whether it is right*.
