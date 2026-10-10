# Freeform against the studio

An analysis of the `opus55-freeform-riftwater` branch (pgmvox and the boards built on it) against pgm-studio, written
2026-10-10, and the case for one tool.

| Path | What it is |
|---|---|
| `pages/report/index.html` | the report, as published: causes, the side-by-side boards, the experiment, the deep dive into terrain, noise, strata, renders, the grammar and houses, the feature table, the author's observations checked, the playtest notes sorted, and studio 2.0 |
| `pages/inspector/index.html` | the Recipe Inspector prototype: the Vale's terrain as steps, a recipe diff, the grammar step by step, a noise playground, the studio's marks for comparison (serve the folder over http; the page reads its heightfields from `data/`) |
| `pages/plan-review/index.html` | the Plan Review prototype: the pgmvox Abbeymoor plan's two versions as a sheet the author notes and approves (serve over http; notes are kept only where it is published as an artifact) |
| `PLAN-REVIEW-DESIGN.md` | how an agent's plan becomes a studio document: the plan of places, its targets, the plan note anchors, the verdict, the API and the loop |
| `pages/studio-2-plan/index.html` | the Studio 2.0 plan of action, in German: the experiments of 10 October (rules off, grain, houses, tunnels), the layer document, play pieces and stamps, the three rule tiers, the order of work and the open decisions |
| `pages/terrain-layers/index.html` | the terrain layer prototype: an island built from ordered, region-bound layers, editable in the browser |
| `boards-as-json/` | Riftwater (its pgmvox port) and Hollow Mesa taken apart by which code writes which blocks, and each written again as one JSON document of ordered layers |
| `houses/HOUSES.md` | the studio's and pgmvox's house models compared, with pictures and a proposed `HouseStyle` extension |
| `experiment/RULES-MINIMAL.md` | the two briefs built a third time with the rules relaxed, and the finished boards checked against every rule |
| `experiment/grain/` | the grain setting tried on a built board |
| `STUDIO-2-DESIGN.md` | the recipe design: four options weighed, the operation families, the API, the model's loop, the order of work, what the studio does better |
| `recipe/` | the Vale as a recipe that reproduces the library's heightfield exactly, a second version to diff against, and the operation catalogue |
| `experiment/` | the two briefs given to both pipelines, what came out, the author's review and the revision round it drove |
| `agent-reports/` | the helper reports as their agents wrote them: pgmvox anatomy, studio inventory, same-brief comparison, grammar walkthrough, objective visibility audit |
| `QUALITY-LEAP-CROSSCHECK.md` | the other session's `freeform/QUALITY-LEAP.md` checked against this folder and the code |
| `playtest-feedback-2026-10-10.md` | the author's playtest notes, sorted by kind and by whether the studio would have caught each |
