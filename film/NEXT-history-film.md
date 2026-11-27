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
