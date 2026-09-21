# Ropeworks Quay — capture-the-wool

**In one sentence:** a fishing harbour where each team's wool sits in a stone cellar tucked behind the
yard, defended from its corner by three faces of void and one prepared wall about sixteen blocks out on
the yard's own interface, the two teams' quays joined only by a 32-block build zone over the tidal strait.

384 × 144 blocks, `rot_180`, `maxPlayers` 8, base surface 9.

## Where the plan puts things

Four pieces a side: `spawn` (back), `yard` (the hub, reaching the strait), `approach` (a spur off the
yard's own interface), `wool-room` (beyond it, on `approach`'s far edge). The wool room's only land
interface is `approach`'s; its other three sides are void, which is `approaches.md`'s "corner room" —
"three faces on void is the ordinary composed shape, one connecting piece and the rest open."

The defence wall stands on **`approach`↔`yard`**, never on the room's own edge (`PL13`), 20 blocks wide
and about sixteen blocks in front of the cellar door — inside `ST8`'s 10–20-block lane-mouth band and
its own "about 15 in front" reading, both read off `plan/evaluate`'s lint rather than guessed. The
strait is 32 blocks (`CT12`'s 15–40), each team's exposed frontage 64 blocks (`FR9`'s 15 floor).

The first geometry (a 24-block room and wall, no explicit footprint) tripped four complaints —
`ST8` twice, `ST9`, `ST10` — and two soft-scored misses, `WL10`'s `wool-front-distance` and
`-remoteness` at 179 against bands of 22–147 and 25–130 (the room sat far out along the spawn's own
depth, off the yard's forward reach entirely).

Narrowing the room to 20×24 blocks and moving the whole spur onto the yard's mid-depth cleared all four
complaints and both soft terms in one pass; only `LN2`'s `max-chain-length` (156 against 25–110) still
misses, a consequence of the corridor length CT12's strait target imposes, and it does not block a valid
plan.

## The ground

One theme, `quay`: grass-over-dirt on the flat, gravel-over-dirt on the shoulder, cobble-over-stone on
the face, banded on slope. No relief marks at all — the base is flat at y9 throughout, because
`match-flow.md` §10.1 reads a capture-style objective's ground as **built rather than landscape**, and a
quay is the built case: a gravel/andesite/cobble road from spawn to yard, a worn path from yard to
cellar, three masts (template spruce) and two andesite boulders breaking the yard's open flat, one
long timber ropewalk shed (a `HouseProp` on its own footprint, not a room) standing off the road.

Two room styles, both forked from `stonemason`: the wool cellar keeps a hip roof and a chiseled/plain
stone-brick wall; the spawn hall turns the same shell gable and re-bands its wall to cobble-over-oak.

## What checks it

`03-slopes.txt`: 22688 walked, **0 scrambled, 0 barrier**, 0 faces — the flat-quay design has no seam to
scramble at. `06-claims.txt`: 18 props placed, **0 declined** (one early pass declined `HP3`, the
ropewalk's wings covering 273 then 204 blocks against a 192-block cap on one placed building; the
footprint was cut to 14×9 = 126). `preflight`: export gate **OPEN**. `coverage`: **3.3% dead** — the
lowest of the four boards, consistent with `match-flow.md` §10.3's claim that a built capture-style board
should use nearly all its ground.

## What went wrong

The `HouseProp.wings` field is `[{"corners": [[x,z],[x,z]]}]`, not `{"minX","minZ","maxX","maxZ"}`. The
wrong shape did not refuse at the store — it deserialized permissively into a wing with null corners —
and the studio answered 200 at every tier up to and including `plan/compile` and `POST
/map/from-documents`; the fault only surfaced as a 500 `RQ2` ("the studio failed to answer this request,
the fault is its own") on `sketch/columns`, `coverage` and `export`, three calls deep into the drive.

Reading the running studio's own stdout log (`PgmStudio.Api`'s redirected output, found via
`/proc/<pid>/fd/1`) rather than guessing from the refusal text was what actually located the fault: a
`NullReferenceException` in `HouseProp.Check()`, which pointed at the wing corners rather than at
anything the 500's own body named.
