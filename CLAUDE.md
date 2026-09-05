# pgm-studio-mapgen

Maps authored by driving pgm-studio's HTTP API. `AUTHORING-BRIEF.md` is what a board should be;
`README.md` is what is here.

**Building, changing, diagnosing or reading a map: invoke the `pgm-board` skill first.** It carries the
lookup table from question to the read that already answers it, and the two moments to stop at. It is
distilled from 27 run reports and every rule in it cost at least one build.

Three things that are true before the skill loads:

- **Ask the studio whether it is running before doing anything about it, and where it listens is not a
  constant.** It has been a different port on every environment the boards here were built on, so nothing
  states one: set `PGM_STUDIO_API`, or let `tools/drive.py` find it by asking `GET /api/health` at the
  candidates it knows. If you write a port into a document, you have written down the machine you happened
  to be on.

  **A studio that answers is somebody's — leave it alone.** Restarting one takes a board out from under
  whoever is driving it, and two servers on one machine starve each other into route timeouts that read as
  page faults. Drive the one that is there.

  **A studio that does not answer has to be started, and in a fresh cloud container nothing is installed
  at all.** That is not this repository's business — `pgm-studio/docs/cloud-setup.md` is the runbook, and it
  is accurate: the SDK and MariaDB by apt, the database and its user, `--migrate-only`, then the API. Expect
  it to take a while and do it in a background shell, because a sandboxed foreground one has no network.
- **Do not write a second copy of the system.** A `specs/<slug>/build-spec.py` that generates the plan
  and the finish is the authoring work and is expected. A script that reads the *built world* —
  a ground-finder, a section renderer, a walk or clearance check — is not, wherever it lives, including
  a scratch directory. Those reads exist: `column`, `transect`, `slopes`, `walk`, `sketch/dressing`,
  all with `?format=text`. The one exception is a world that is not a stored map (a community map, a
  hand-finished world) — then `tools/anvil.py` and its four siblings.
- **Finish the ground by its angle, not by its height.** A theme hung on plan pieces or on height bands
  paints a board flat from above however much relief is under it. The `slope` band axis is what tells a
  45° hillside from a meadow, `GET …/incline?format=text` is what says where the bands should cut, and the
  `pgm-board` skill carries both with a worked stack. A board finished any other way is the look every
  report here has complained about.
- **Read the text before the pictures.** `tools/drive.py` writes ~25 `?format=text` reads beside every
  render. A picture answers *whether* something came out; a number answers *whether it is right*.
