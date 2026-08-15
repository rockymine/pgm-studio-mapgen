# Experience report — authoring maps against pgm-studio / pgm-studio-mapgen without a live API

I did not have a running studio (no .NET 10, no MariaDB). Everything below comes from reading the repositories, the tool docs under `docs/tools/`, `GENERATION-NOTES.md`, the agent reports, and the committed specs/maps.

## What worked well

**The four-level model is clear.** Plan → Layout → Intent → Built world is a real separation of concerns, not just stages of the same document. Once you internalise that a plan is about roles, isolation and placement *meaning*, and a layout is about actual geometry and relief, the system stops feeling arbitrary.

**Symmetry as a first-class primitive** is excellent. Authoring one unit and letting `rot_180` (or other modes) fan it is exactly how CTW/DTM maps are designed in practice. The compiler and the placement model both respect it.

**The written errata are unusually good.** `GENERATION-NOTES.md` and the agent reports (especially the ClayClay recreation) document silent failures that would otherwise cost full rebuild cycles: shapes without `type`/`operation`/`floor` rasterise to nothing; path cells claim ground and drop houses with no log; provenance format changes crash the renderer; `--buildings` is unreliable on non-log styles. That material is the difference between a usable system and a black box.

**Driving the real endpoints** (as the later agents did) is the correct architecture. The earlier parallel `tools/mapgen` re-implementation was correctly diagnosed as a dead end.

**House styles and props** have a rich enough schema (wall courses, posts, roof form, windows, door heads, path paving, trees) that you can express a coherent material language without inventing a second system.

## Friction and issues observed (from code/docs only)

1. **Silent failure modes are expensive.** Empty islands, dropped buildings, and “HTTP 200 but nothing happened” are called out repeatedly in the notes. Without a live API I could not hit them myself, but the documentation makes it clear they are still live costs for anyone iterating.

2. **Distance between “what the plan says” and “what the rasteriser emits”.** Overlaps, height vs paint resolution rules, and island identity after recompile all require a human (or a very careful agent) to re-check. The 409-on-orphan-islands behaviour is good; the cases that don’t refuse are the costly ones.

3. **Discovery cost of the library / theme injection path.** Once you know the endpoints it is powerful; coming in cold, the gap between “I have a plan” and “I have themed, dressed geometry” is large. The ClayClay report’s recommendation — expand a terse spec into real plan + theme + style + dressing documents and post those — is the right direction.

4. **Cell vs block mental load.** Plans are in cells; everything else eventually becomes blocks. Keeping “50 blocks ≈ 10 cells at cell=5” straight while placing monuments and relief features is easy to get wrong on the first pass.

5. **Zone semantics are overloaded.** Zones are used for build bands, voids, rivers, and isolation. The render and the mental model both benefit from clearer naming (or explicit role fields) so a “mid-build” cannot be mistaken for a void and a “ravine” cannot cut a team side by accident.

6. **No closed loop without the API.** I could author valid-looking JSON and draw top-downs, but I could not compile, rasterise, seat props on real ground, or export a world. The last mile (relief resolution, path seating, house footprint vs taken cells) remains untested from this side.

## What the three maps represent

| Folder | Mode | Character |
|--------|------|-----------|
| `grok-ridge/` | CTW | Iterated terrace board; continuous abutting runs; side wool with run-up; mid as build band only |
| `sandscar-complex/` | DTM | Multi-piece, height-rich board; central river zone; pit monument + hill monument; desert→savanna progression |
| `sandscar/` | DTM | Single large plateau + small spawn; 50-block same-team monument spacing; meandering river as prop; relief depression/hill under objectives |

The CTW map went through several layout corrections (connected vs fragmented, void placement, build-band visibility). The two DTM maps are intentionally different designs, not iterations of each other.

## Bottom line

The system is already strong enough that a careful author (or agent) can produce coherent, themed, dressed boards by writing the upstream documents. The remaining cost is operational: silent failures, the compile/rasterise feedback loop, and the gap between plan cells and finished voxels. Closing more of those loops in the studio itself would make the next agent runs cheaper than the ones documented in the mapgen repo.

Thank you for the experiment.
EOF
ls -la /home/workdir/artifacts/EXPERIENCE.md
