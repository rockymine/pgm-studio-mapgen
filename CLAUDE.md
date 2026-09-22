# pgm-studio-mapgen

Maps authored by driving pgm-studio's HTTP API. `AUTHORING-BRIEF.md` is what a board should be;
`README.md` is what is here.

**Building a map: read [ORDER-OF-WORK.md](ORDER-OF-WORK.md) first.** One page, the nine decisions a board
is made of and the order they are made in, with the four that cannot be taken back named at the end.

**Then [WHAT-A-BOARD-IS-MADE-OF.md](WHAT-A-BOARD-IS-MADE-OF.md), once, before the first theme is written.**
The author's ruling on how a board should look — the paint, the buildings, the ground cover, where made
ground meets grown. None of it is enforced anywhere, which is the half of authoring every previous run got
wrong.

Those two and `AUTHORING-BRIEF.md` are about 12k tokens together and are the whole of this repository that
is read before the first request. Everything else here is opened at a question, and the brief's §4 says
which question opens what.

**One thing outside this repository is read too, and it is the half nothing here can derive: how a map is
played.** `pgm-studio/docs/gameplay/match-flow.md` is the account of it, read off recorded matches — §4, §6
and §10 if the whole is too much — and `approaches.md` beside it is the author's law on what an objective
needs around it. No card and no endpoint answers what makes a match, so a board decided without them is
decided on look alone.

**Changing, diagnosing or reading a map: invoke the `pgm-board` skill.** It carries the lookup table from
question to the read that already answers it, and the two moments to stop at. It is distilled from 27 run
reports and every rule in it cost at least one build, and it is worth having for an authoring run too.

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

## How an instruction here is written

**One paragraph, one claim. The claim first, the evidence after.**

An instruction is not read the way an essay is read. It is scanned for the sentence that applies right
now, so a paragraph carrying six claims hides five of them. The failure has one shape: a paragraph opens
with a bolded claim and then four more are appended with semicolons and dashes until the opening claim is
the only one anyone sees.

The claim is the first sentence and stays bolded where the document bolds its claims. Everything after it
supports that claim — the mechanism, the number, the failure it prevents, the worked case. Where a
paragraph makes two claims it is two paragraphs.

**An instruction names no board.** A document an agent is handed states the rule and the measurement that
settles it, and a slug in place of a measurement is a citation the reader cannot follow: the board may have
been rebuilt, renamed or retired since, and its coordinates mean nothing without it. Write what was measured —
36 blocks of lane, ten blocks of hill against a wall, twenty-four themes — and leave the board it came off in
`BOARDS-BUILT.md` and the run report, which is what those are for.

**`tools/prose-check.py` is the gate.** It lists every prose paragraph over 110 words or 4 sentences and
exits non-zero while any remain; a table, a fenced block, a list and a heading are none of its business.
Run it over a brief or a skill before the commit that changes one.

**A structural pass may not lose a claim.** `tools/prose-check.py --preserved <before> <after>` compares
the two versions word for word and names anything that disappeared, so splitting a paragraph cannot
quietly drop the clause it was splitting off.

**`tools/boards-check.py` is the other gate.** Every folder under `maps/` and `specs/` is either written up
in `BOARDS-BUILT.md`, named there as not a board, or named there as a debt — and anything else fails. A
board's entry is written by the run that built it, because what a board turned out to be is not derivable
from a folder.
