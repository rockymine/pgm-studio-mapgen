#!/usr/bin/env python3
"""Render the library and write manifest.json.  Usage: build.py [name-substring ...]"""
import json
import os
import sys
import time
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synth import SR, fade, fit, hp, normalize, write_wav   # noqa: E402
import music                                            # noqa: E402
import sfx                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_PEAK, SFX_PEAK = -4.0, -3.0
# seamless loops keep the shortest fades; everything else gets a longer tail fade
SFX_FADES = {'robot_hum': (0.004, 0.004), 'tv_static': (0.004, 0.006), 'clock_tick': (0.003, 0.02)}


def measure(path):
    with wave.open(path, 'rb') as w:
        ch, sw, sr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(nf), '<i2').astype(float) / 32768.0
    return {'sample_rate': sr, 'channels': ch, 'bits': sw * 8, 'duration_s': round(nf / sr, 3),
            'peak_dbfs': round(20 * np.log10(max(np.max(np.abs(x)), 1e-9)), 2)}


def main():
    want = sys.argv[1:]
    notes_log = {}
    entries = {}
    mpath = os.path.join(ROOT, 'manifest.json')
    if os.path.exists(mpath):
        entries = {e['file']: e for e in json.load(open(mpath))['files']}
    for rel, fn, target, desc in music.TRACKS:
        if want and not any(w in rel for w in want):
            continue
        t0 = time.time()
        x, notes = fn()
        x = normalize(x, MUSIC_PEAK)
        path = os.path.join(ROOT, rel)
        write_wav(path, x)
        entries[rel] = {'file': rel, **measure(path), 'description': desc}
        notes_log[rel] = notes
        print(f'{rel:32s} {len(x) / SR:7.2f}s  {time.time() - t0:5.1f}s to render', flush=True)
    for name, fn, dur, desc in sfx.SFX:
        rel = f'sfx/{name}.wav'
        if want and not any(w in rel for w in want):
            continue
        x = hp(fit(fn(), int(round(dur * SR))), 20.0, circular=(name == 'robot_hum'))     # no DC
        fin, fout = SFX_FADES.get(name, (0.003, min(0.03, dur * 0.15)))
        x = normalize(fade(x, fin, fout), SFX_PEAK)
        path = os.path.join(ROOT, rel)
        write_wav(path, x)
        entries[rel] = {'file': rel, **measure(path), 'description': desc}
        print(f'{rel:32s} {dur:7.2f}s', flush=True)
    order = [t[0] for t in music.TRACKS] + [f'sfx/{s[0]}.wav' for s in sfx.SFX]
    files = [entries[k] for k in order if k in entries]
    json.dump({'sample_rate': SR, 'channels': 2, 'bits': 16, 'files': files}, open(mpath, 'w'), indent=1)
    if notes_log:
        json.dump(notes_log, open(os.path.join(ROOT, 'gen', 'notes.json'), 'w'), indent=1)
    print(f'manifest: {mpath} ({len(files)} files)')


if __name__ == '__main__':
    main()
