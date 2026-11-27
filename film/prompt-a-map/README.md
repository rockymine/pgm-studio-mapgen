# Prompt-a-Map — source of the sketch

Everything that produced the video, so a shot can be changed and re-rendered.

## How it is made

1. **Plates.** `eye/eye.cs` is a small file-based .NET script over `pgm-studio`'s own eye renderer
   (`PgmStudio.Minecraft/Render/EyeScene`). It reads a world folder (`region/*.mca`) and draws it from any camera
   with the game's block sprites, as stills or as a frame sequence, with an optional depth picture.
   `film/cams.json` names every camera; `film/plates.py` renders whatever is missing into `film/plates/`.
   The sprites come from the 1.8.9 client jar (set `JAR=`), which the studio downloads only where Mojang's EULA
   is accepted; it is not in this bundle.
2. **Sets.** `sets/sets.py` writes the studio, machine room and awards stage as block lists; the same script
   renders them (`EDITS=<file> eye empty …`).
3. **Animation.** `film/index.html` is the film. `film/lib/engine.js` draws any time `T` with `window.seek(T)`;
   `film/lib/mc.js` is the character rig, a CSS 3D scene whose camera matrix matches the renderer's, so a
   character placed at world coordinates stands in the picture at the right size. Shots are in `film/shots/`,
   in film order. A shot with `depth:` hides its characters behind nearer blocks.
4. **Voices.** `film/script.py` is the script. `film/vo.py` records every line (Piper voices and espeak-ng) and
   solves the timeline from the line lengths into `timeline.json` / `timeline.js`.
5. **Picture and sound.** `film/capture.cjs <dir> <from> <to>` screenshots frames with Playwright;
   `film/mix.py` places voice, music and effects from the film's own cue list and writes the subtitles;
   ffmpeg joins them.

## To replace the voices

Record each line of `dub-sheet.csv`, save them as `film/vo/<line>.wav` (48 kHz mono), put the measured
lengths in `timeline.json`, and re-run `mix.py`. Or simply lay the recordings over
`prompt-a-map_clean_for_dub_1080p.mp4` in an editor: the music already dips where each line falls.

## Paths

The scripts name the session's scratch directory and `/home/user/pgm-studio` literally. Change the constants
at the top of `plates.py`, `vo.py`, `mix.py`, `docs.py` and the `#:project` line of `eye.cs`.
