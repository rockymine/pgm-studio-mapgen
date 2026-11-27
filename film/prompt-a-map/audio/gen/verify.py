#!/usr/bin/env python3
"""Check every rendered file against the brief, then print what can be measured about the music."""
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from synth import SR, hz, nn, nname      # noqa: E402
import music                             # noqa: E402
import sfx                               # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# durations the brief states outright; the rest are checked against the generator's own intent
BRIEF = {'whoosh_long': 1.2, 'typing_run': 4, 'card_burst': 3, 'counter_roll': 3, 'fall_whistle': 2, 'crowd_cheer': 3,
         'crowd_aww': 2, 'applause': 4, 'crickets': 4, 'tada': 1.5, 'glitch': 0.6, 'clock_tick': 6, 'power_down': 1.5,
         'tv_static': 1, 'fast_forward': 2, 'heartbeat': 3, 'robot_hum': 6}


def load(rel):
    with wave.open(os.path.join(ROOT, rel), 'rb') as w:
        meta = (w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes())
        x = np.frombuffer(w.readframes(meta[3]), '<i2').astype(float).reshape(-1, meta[1]) / 32768.0
    return meta, x


def db(v):
    return 20 * np.log10(max(v, 1e-9))


def band_split(x):
    m = x.mean(1)
    X = np.abs(np.fft.rfft(m)) ** 2
    f = np.fft.rfftfreq(len(m), 1 / SR)
    tot = X.sum() + 1e-20
    cent = (X * f).sum() / tot
    return [100 * X[(f >= a) & (f < b)].sum() / tot for a, b in ((0, 200), (200, 2000), (2000, 24000))], cent


def pitch_at(x, t0, t1, lo=150, hi=4000):
    seg = x[int(t0 * SR):int(t1 * SR)].mean(1)
    seg = seg * np.hanning(len(seg))
    N = 1 << 17
    X = np.abs(np.fft.rfft(seg, N))
    f = np.fft.rfftfreq(N, 1 / SR)
    m = (f >= lo) & (f <= hi)
    return f[m][np.argmax(X[m])]


def tempo(x, lo=60, hi=180):
    m = np.abs(x.mean(1))
    hop = 240                                    # 5 ms
    env = m[:len(m) // hop * hop].reshape(-1, hop).mean(1)
    on = np.maximum(np.diff(env), 0)
    on -= on.mean()
    ac = np.fft.irfft(np.abs(np.fft.rfft(on, 2 * len(on))) ** 2)[:len(on)]
    best = None
    for bpm in np.arange(lo, hi + 0.01, 0.5):
        lag = 60.0 / bpm * SR / hop
        v = sum(np.interp(lag * k, np.arange(len(ac)), ac) for k in range(1, 9))
        if best is None or v > best[0]:
            best = (v, bpm)
    return best[1]


def main():
    man = {e['file']: e for e in json.load(open(os.path.join(ROOT, 'manifest.json')))['files']}
    spec = [(rel, target, target) for rel, _, target, _ in music.TRACKS]
    spec += [(f'sfx/{n}.wav', BRIEF.get(n, d), d) for n, _, d, _ in sfx.SFX]
    fails = []
    print(f'{"file":30s} {"dur":>7s} {"want":>6s} {"peak":>7s} {"rms":>7s} {"crest":>6s} {"L/R":>5s} {"edge":>7s}  lo/mid/hi %   centroid')
    data = {}
    for rel, want, _ in spec:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            fails.append(f'{rel}: missing')
            continue
        (sr, ch, sw, nf), x = load(rel)
        data[rel] = x
        dur = nf / sr
        pk, rms = np.max(np.abs(x)), np.sqrt(np.mean(x * x))
        corr = float(np.corrcoef(x[:, 0], x[:, 1])[0, 1])
        edge = max(np.max(np.abs(x[0])), np.max(np.abs(x[-1])))
        bands, cent = band_split(x)
        target_pk = -4.0 if rel.startswith('music') else -3.0
        problems = []
        if sr != 48000: problems.append(f'sample rate {sr}')
        if ch != 2: problems.append(f'{ch} channels')
        if sw != 2: problems.append(f'{sw * 8} bit')
        if abs(dur - want) > 0.1 * want: problems.append(f'duration {dur:.2f} vs {want}')
        if db(pk) >= 0: problems.append('clips')
        if abs(db(pk) - target_pk) > 0.6: problems.append(f'peak {db(pk):.2f} not near {target_pk}')
        if db(rms) < -45: problems.append(f'near silent, rms {db(rms):.1f}')
        if db(edge) > -50: problems.append(f'edge sample at {db(edge):.1f} dBFS')
        if abs(x.mean()) > 0.003: problems.append(f'dc {x.mean():.4f}')
        if rel not in man: problems.append('not in manifest')
        elif abs(man[rel]['duration_s'] - dur) > 0.002 or abs(man[rel]['peak_dbfs'] - db(pk)) > 0.02:
            problems.append('manifest disagrees with file')
        print(f'{rel:30s} {dur:7.2f} {want:6.2f} {db(pk):7.2f} {db(rms):7.1f} {db(pk) - db(rms):6.1f} {corr:5.2f} {db(edge):7.1f}'
              f'  {bands[0]:3.0f}/{bands[1]:3.0f}/{bands[2]:3.0f}   {cent:7.0f} Hz' + ('   <-- ' + '; '.join(problems) if problems else ''))
        fails += [f'{rel}: {p}' for p in problems]
    extra = set(man) - {s[0] for s in spec}
    fails += [f'{e}: in manifest but not in the spec' for e in extra]
    print(f'\n{len(spec)} files checked, {len(fails)} problems')
    for f in fails:
        print('  FAIL', f)

    # ---------------- musical checks
    print('\n== note sequences and key membership ==')
    notes = json.load(open(os.path.join(ROOT, 'gen', 'notes.json')))
    scales = {'A minor': 'A B C D E F G G#', 'D major': 'D E F# G A B C#', 'F major': 'F G A Bb C D E',
              'G major': 'G A B C D E F#', 'Eb major': 'Eb F G Ab Bb C D', 'E minor': 'E F# G A B C D'}

    def walk(v):
        if isinstance(v, str):
            for tok in v.replace('+', ' ').replace('|', ' ').replace('/', ' ').split():
                try:
                    yield nn(tok) % 12
                except Exception:
                    pass
        elif isinstance(v, dict):
            for vv in v.values():
                yield from walk(vv)
        elif isinstance(v, list):
            for vv in v:
                yield from walk(vv)

    for rel, info in notes.items():
        print(f'\n{rel}')
        for k, v in info.items():
            if isinstance(v, list):
                print(f'  {k}:')
                for row in v:
                    print(f'      {row}')
            elif isinstance(v, dict):
                print(f'  {k}: ' + ';  '.join(f'{a}: {b}' for a, b in v.items()))
            else:
                print(f'  {k}: {v}')
        key = next((s for s in scales if str(info.get('key', '')).startswith(s)), None)
        if key:
            allowed = {nn(n + '4') % 12 for n in scales[key].split()}
            pcs = [p for k, v in info.items() if k not in ('key', 'chords', 'A chords', 'B chords', 'form') for p in walk(v)]
            out = sorted({nname(p + 60)[:-1] for p in pcs if p not in allowed})
            print(f'  -> {len(pcs)} pitches, outside {key} ({scales[key]}): {out or "none"}')

    print('\n== measured against intent ==')
    for rel, bpm in (('music/infomercial.wav', 128), ('music/machine.wav', 140), ('music/lobby_muzak.wav', 104),
                     ('music/sad_piano.wav', 66)):
        est = tempo(data[rel])
        print(f'  {rel}: onset-autocorrelation tempo {est:.1f} BPM (written at {bpm}; half/double time counts as a match)')
    e8 = 60 / 128 / 2
    x = data['music/infomercial_sting.wav']
    got = []
    for st, nm in zip([0, 1, 2, 4, 5, 6], music.STING_NOTES):
        f = pitch_at(x, 0.02 + st * e8 + 0.02, 0.02 + st * e8 + 0.2, lo=500, hi=1400)
        got.append(f'{nm}={hz(nm):.0f}Hz heard {f:.0f}Hz')
    print('  sting notes: ' + ', '.join(got))
    x = data['sfx/ding.wav']
    print(f'  ding: first tone {pitch_at(x, 0.01, 0.11, 500, 3000):.0f} Hz (B5 = {hz("B5"):.0f}), '
          f'second {pitch_at(x, 0.2, 0.5, 1100, 3000):.0f} Hz (E6 = {hz("E6"):.0f})')
    x = data['sfx/sad_trombone.wav']
    t0, got = 0.004, []
    for nm, ln in (('F4', 0.34), ('D4', 0.34), ('B3', 0.34), ('G#3', 1.1)):
        got.append(f'{nm}={hz(nm):.0f} heard {pitch_at(x, t0 + 0.08, t0 + 0.28, 150, 420):.0f}')
        t0 += ln + 0.07
    print('  sad trombone: ' + ', '.join(got))
    x = data['music/machine.wav']
    q = len(x) // 4
    cents = [band_split(x[i * q:(i + 1) * q])[1] for i in range(4)]
    print('  machine spectral centroid by quarter (should rise): ' + ' -> '.join(f'{c:.0f}' for c in cents))
    x = data['music/hero.wav']
    spb = 60 / 76
    lv = [db(np.sqrt(np.mean(x[int(b * 4 * spb * SR):int((b + 1) * 4 * spb * SR)] ** 2))) for b in range(7)]
    print('  hero RMS by bar (should build, then tail): ' + ' '.join(f'{v:.1f}' for v in lv))
    for rel in ('sfx/robot_hum.wav', 'sfx/clock_tick.wav', 'music/lobby_muzak.wav', 'music/infomercial.wav'):
        x = data[rel]
        k = int(0.05 * SR)
        print(f'  {rel}: last 50 ms rms {db(np.sqrt(np.mean(x[-k:] ** 2))):.1f} dBFS, first 50 ms {db(np.sqrt(np.mean(x[:k] ** 2))):.1f} dBFS')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
