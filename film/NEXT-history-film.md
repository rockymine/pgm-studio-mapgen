# Next film: the history of the AI maps (brief from rockymine, 2026-11-27)

A serious, careful documentary — English, synthetic scratch voices again — about a year of AI-made maps and how
the tool changed. Longer than 4–5 minutes is fine; expect several sessions. The orchestrating session only
organizes: research, scouting and any map build go to Opus agents (best results so far), not Sonnet/Haiku.
A new map is optional; maps from about a month ago exist and can stand in. Real names may appear (rockymine,
Ruediger), with their real skins at the end; the models are named (Opus, Sonnet, Haiku, Grok, Fable), logos allowed.

Beats the author named, to find in both histories (pgm-studio from 2026-06-12, pgm-studio-mapgen from 2026-08-13):
- Why capture-the-wool came first: the most structured layout, where the void steers player flow; the first idea
  was to read a map as a graph.
- The model that followed: every map has a hub, wool approaches, a frontline and a middle — and what that limits.
- The generator: how layouts are composed and terrain is built; show it step by step as a time-lapse in a map.
- Trees are hard to generate; houses work well.
- Texturing: early maps were plain; rendering with the real block textures was a turning point; then map walls.
- The API: the tool is something the AI *uses*, and can ask for rules and documentation when it hits a hurdle.
- The pgmvox port and the rethink of how maps are made, because the first approach was limiting.
- Rules and validation: clearly better maps, but which rule causes which gain is not measured; some rules still
  raise findings they should not. A 500-block-wide map with monuments and core in one line is a remembered low.
- Models compared, Haiku and Sonnet still struggle; visualize the context a model must read.
- The browser studio (pgmstudio.de) as where it stands now.
- The newest experiment: a map built by hand on the "fire and ice contest" branch, a DTC+CTW map, partly
  underground and inside a mountain — where a human thinks differently and the tool's gaps show.
- Maps side by side across time; the improvement is visible.
Extra banger for the comedy spot: that 500-wide line-up map.

How the first film was made is `film/prompt-a-map/README.md`; plates, voices and audio are re-rendered from it
(paths in the scripts name a scratch directory and must be changed).

The hand-built "fire and ice" experiment is on branch `claude/compassionate-cerf-fg7m17` (find the repository with `git ls-remote`); another agent is still committing its scripts and scratchpad there, so fetch it fresh.

More from the author (2026-11-27):
- The newest studio branch is `ccr-875c17a4-2yjgux` (partly merged to main): backlog clean-up and UI work, and the
  verification pipeline is not yet where it should be.
- The story starts before `pgm-studio`. First, at the start of the year, a repository with CTW in its name (a
  capture-the-wool layout generator): the realisation, with Claude, that something drawn in the browser could
  become downloadable blocks. Then a Python project that rendered map XML, not yet generation. Then the move to
  C#, a language the author can read. Other repositories whose names contain "pgm-studio" exist; find them with
  `list_repos` and attach them with `add_repo` (this session's scope was only the two).
- Prepare interview questions for rockymine, Ruediger and Tttie. Answers will come later and refine the film;
  an interview is also a possible second way to document the year.

The earlier repositories, all public and readable without attaching (clone with full history, e.g.
`git clone https://github.com/rockymine/<name>`): `CTW-Layout-Generator` (made with Google's AI Studio, the very
first layout test), `MinecraftLayoutEditor` (a small self-built project), `pgm-map-studio` (the Python stage).
The current experiment is illustrated by the artifact https://claude.ai/code/artifact/555b1fbe-f6ae-4b8b-b195-06643ab38297
(read it with the Artifact tool's `read` action).
