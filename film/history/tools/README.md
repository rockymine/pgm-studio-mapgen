# Tools the history's sources were read with

**These scripts produced the sources of research `15` and `16`; none of them is part of the map tooling.** They
were written in a session's scratch directory on 27 and 28 November 2026 and kept here so the readings can be
repeated. Paths are passed as arguments. The Discord channels themselves were read by JavaScript run in the author's
signed-in browser, which is not kept.

| Script | What it does | Needs |
|---|---|---|
| `ziplist.py <dir>` | lists every `map.xml` in each zip of a folder: name, version, objective, `<created>`, authors | Python |
| `condense_dm.py <txt>` | condenses an exported Discord conversation into one line per message | Python |
| `ocpage.py <dir> <ISO time>` | binary-searches the match list of `api.oc.tc` for the page holding a time | Python |
| `ocharvest.py <dir> <from> <to>` | saves pages of `GET /api/v2/matches/?page=N&size=100`, one JSON file a page | Python |
| `ocdiff.py <match-status csv>` | compares the saved pages with the `#match-status` log by match id; writes the public-server matches the log lacks (run inside the folder holding `pages/`) | Python |
| `ocdetail.py <csv> <dir>` | saves `GET /api/v2/matches/{id}` for every id in a CSV | Python |
| `transcribe.py <wav> <out>` | Whisper transcript with a timestamp per segment | `faster-whisper` |
| `transcribe_words.py <wav> <out.json>` | the same with a timestamp per word | `faster-whisper` |
| `embed.py`, `diarize.py <scratch dir>` | speaker fingerprints (SpeechBrain ECAPA) on fixed windows and on word-aligned chunks, for grouping voices | `torch`, `speechbrain`, `scikit-learn` |

**The audio is prepared with ffmpeg.** `ffmpeg -i <recording>.mkv -vn -ac 1 -ar 16000 audio16k.wav` gives the input
the transcription and speaker scripts read.

**Voices were grouped by spectral clustering of the chunk fingerprints into five groups.** That step was run
inline and is not a script: cosine similarity of chunks of a second or more, `SpectralClustering(n_clusters=5)`,
then every chunk to its nearest group centre. The groups were named by the author from audio samples (research
`16`).

**What the scripts read stays outside the repository.** The recording, the transcripts, the direct messages and
the saved API pages are the author's local copies, not committed (research `15` and `16` say why).
