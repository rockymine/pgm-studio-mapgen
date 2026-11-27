#!/usr/bin/env python3
"""The seven music beds. Every function returns (stereo buffer, {voice: note list}) for the build log."""
import os

import numpy as np

from synth import *


def _lv(tag, **buses):
    """LEVELS=1 prints each bus's RMS, peak and low/mid/high energy split, for balancing."""
    if not os.environ.get('LEVELS'):
        return
    for k, v in buses.items():
        v = stereo(v)
        m = v.mean(1)
        X = np.abs(np.fft.rfft(m)) ** 2
        f = np.fft.rfftfreq(len(m), 1 / SR)
        tot = X.sum() + 1e-20
        sh = [100 * X[(f >= a) & (f < b)].sum() / tot for a, b in ((0, 200), (200, 2000), (2000, 24000))]
        print(f'   [{tag}] {k:8s} rms {20 * np.log10(np.sqrt(np.mean(v * v)) + 1e-12):6.1f} dB  peak '
              f'{20 * np.log10(np.max(np.abs(v)) + 1e-12):6.1f} dB   lo/mid/hi {sh[0]:3.0f}/{sh[1]:3.0f}/{sh[2]:3.0f}')


def _drumkit(seed):
    rng = np.random.default_rng(seed)
    return dict(
        kick=[kick(rng, dur=0.26, f0=160, f1=54, tp=0.025, ta=0.095, click=0.45) for _ in range(2)],
        clap=[clap(rng) for _ in range(4)],
        hat=[hat(rng) for _ in range(6)],
        ohat=[hat(rng, dur=0.3, tau=0.09) for _ in range(2)],
        snare=[snare(rng) for _ in range(4)],
        crash=[crash(rng) for _ in range(2)],
    )


def _brass_chord(notes, dur, vel, rng, bright=1.0, a=0.03):
    out = None
    for i, nm in enumerate(notes):
        y = brass(nn(nm), dur, vel, a=a, bright=bright, rng=rng)
        y = y * np.array([1 - 0.25 * (i % 2), 1 - 0.25 * ((i + 1) % 2)])
        out = y if out is None else out + y
    return out / max(1.0, len(notes) ** 0.6)


def _sparkle(mx, t0, notes, spacing, rng, gain=0.3, tau=0.22):
    for i, nm in enumerate(notes):
        mx.add(bell(hz(nm), 0.9, tau=tau), t0 + i * spacing + rng.uniform(0, 0.008), gain * rng.uniform(0.7, 1.0),
               rng.uniform(-0.8, 0.8))


# ------------------------------------------------------------------ 1
def sad_piano():
    bpm = 66.0
    spb = 60 / bpm
    bars = 7
    dur = bars * 4 * spb
    rng = np.random.default_rng(101)
    mx = Mix(dur)
    LH = [
        ['A2', 'E3', 'A3', 'C4', 'E4', 'C4', 'A3', 'E3'],      # Am
        ['F2', 'C3', 'F3', 'A3', 'C4', 'A3', 'F3', 'C3'],      # F
        ['C3', 'G3', 'C4', 'E4', 'G4', 'E4', 'C4', 'G3'],      # C
        ['E2', 'B2', 'E3', 'G#3', 'B3', 'G#3', 'E3', 'B2'],    # E
        ['A2', 'E3', 'A3', 'C4', 'E4', 'C4', 'A3', 'E3'],      # Am
        ['D3', 'A3', 'D4', 'F4', 'E2', 'B2', 'D3', 'G#3'],     # Dm | E7
    ]
    RH = [
        [(0, 1.5, ['E5']), (1.5, 0.5, ['D5']), (2, 1, ['C5']), (3, 1, ['A4'])],
        [(0, 2, ['C5']), (2, 1, ['A4']), (3, 1, ['F5'])],
        [(0, 1.5, ['E5']), (1.5, 0.5, ['D5']), (2, 1, ['E5']), (3, 1, ['G5'])],
        [(0, 1, ['B5']), (1, 1, ['G#5']), (2, 2, ['E5'])],
        [(0, 1.5, ['A5', 'A4']), (1.5, 0.5, ['G5']), (2, 1, ['E5', 'E4']), (3, 1, ['C5'])],
        [(0, 1, ['D5']), (1, 1, ['F5']), (2, 1, ['E5']), (3, 1, ['G#4'])],
        [(0, 4, ['A4']), (2, 2, ['E5']), (3, 1, ['A5'])],
    ]
    vel_bar = [0.50, 0.56, 0.64, 0.74, 0.82, 0.66, 0.46]
    for b, pat in enumerate(LH):
        for e, nm in enumerate(pat):
            beat = e * 0.5
            end = (2.0 if beat < 2 else 4.0) if b == 5 else 4.0
            t0 = max(0.002, (b * 4 + beat) * spb + rng.normal(0, 0.006))
            v = vel_bar[b] * (0.72 if e == 0 else 0.55) * rng.uniform(0.93, 1.06)
            mx.add(piano(nn(nm), (end - beat) * spb + 0.2, v, rng), t0)
    for b, evs in enumerate(RH):
        for beat, ln, notes in evs:
            for j, nm in enumerate(notes):
                t0 = max(0.002, (b * 4 + beat) * spb + rng.normal(0, 0.007) + 0.014 * j)
                v = min(1.0, vel_bar[b] * 1.22) * (1.0 if j == 0 else 0.55)
                if b == 6 and beat > 0:
                    v *= 0.6
                mx.add(piano(nn(nm), ln * spb + 0.9, v, rng), t0)
    final = ['A2', 'E3', 'A3', 'C4', 'E4']
    for j, nm in enumerate(final):
        mx.add(piano(nn(nm), 4 * spb, 0.42, rng), 24 * spb + 0.05 * j)
    out = reverb(mx.b, t60=2.3, mix=0.2, damp=4200, seed=11)[:mx.n]
    out = master_music(out, drive=1.0, fout=1.4)
    notes = {'bpm': bpm, 'bars': bars, 'key': 'A minor',
             'chords': 'Am | F | C | E | Am | Dm E7 | Am',
             'melody': [' '.join('+'.join(n) for _, _, n in bar) for bar in RH],
             'left hand': [' '.join(p) for p in LH] + [' '.join(final) + ' (rolled)']}
    return out, notes


# ------------------------------------------------------------------ 2
INFO_CH = {
    'D': dict(bass='D2', stab=['F#4', 'A4', 'D5']),
    'Bm': dict(bass='B1', stab=['F#4', 'B4', 'D5']),
    'G': dict(bass='G2', stab=['G4', 'B4', 'D5']),
    'A': dict(bass='A1', stab=['E4', 'A4', 'C#5']),
    'Em': dict(bass='E2', stab=['E4', 'G4', 'B4']),
}
INFO_A = ['D', 'Bm', 'G', 'A', 'D', 'Bm', 'G', 'A']
INFO_B = ['G', 'G', 'D', 'D', 'Em', 'Em', 'A', 'A']
A_LEAD = {
    0: [(0, 2, 'F#5'), (2, 2, 'A5'), (4, 4, 'D6'), (10, 2, 'B5'), (12, 4, 'A5')],
    1: [(0, 3, 'D6'), (3, 3, 'B5'), (6, 6, 'F#5')],
    3: [(8, 2, 'A5'), (10, 2, 'B5'), (12, 4, 'C#6')],
    4: [(0, 2, 'D6'), (2, 2, 'A5'), (4, 4, 'F#5'), (10, 2, 'A5'), (12, 4, 'B5')],
    5: [(0, 3, 'D6'), (3, 3, 'B5'), (6, 6, 'F#5')],
    7: [(8, 2, 'C#6'), (10, 2, 'B5'), (12, 4, 'A5')],
}
B_LEAD = {
    0: [(0, 6, 'B5'), (6, 2, 'A5'), (8, 8, 'G5')],
    2: [(0, 6, 'A5'), (6, 2, 'G5'), (8, 8, 'F#5')],
    4: [(0, 6, 'G5'), (6, 2, 'F#5'), (8, 4, 'E5'), (12, 4, 'G5')],
    5: [(0, 8, 'B5')],
    6: [(0, 4, 'A5'), (4, 4, 'B5'), (8, 4, 'C#6'), (12, 4, 'E6')],
    7: [(0, 4, 'E6')],
}
STING_NOTES = ['F#5', 'A5', 'D6', 'B5', 'C#6', 'D6']
# beat within the ending, chord, lead note, held
ENDING = [(0, 'D', 'D6', False), (2, 'G', 'B5', False), (3, 'A', 'C#6', False), (4, 'D', 'D6', True)]


def _lead(nm, steps, s16, bright=1.3, decay=0.33):
    return pluck(nn(nm), min(steps * s16 + 0.35, 1.1), decay=decay, bright=bright, detune=7, even=0.75)


def infomercial():
    bpm = 128.0
    spb = 60 / bpm
    s16 = spb / 4
    bars = 34
    dur = bars * 4 * spb
    rng = np.random.default_rng(202)
    kit = _drumkit(21)
    form = INFO_A + INFO_A + INFO_B + INFO_A + ['D', 'D']
    drums, bassb, stabs, lead, brs, fx = (Mix(dur) for _ in range(6))
    n = drums.n
    duck = np.ones(n)
    tt = np.arange(int(0.3 * SR)) / SR
    dip = 0.4 * np.exp(-tt / 0.07)

    def kick_at(t, g=1.0):
        drums.add(kit['kick'][0], t, 0.62 * g)
        i = int(t * SR)
        m = min(len(dip), n - i)
        duck[i:i + m] = np.minimum(duck[i:i + m], 1 - dip[:m] * g)

    for bar in range(32):
        sec, inb = bar // 8, bar % 8
        isB, last = sec == 2, inb == 7
        tb = bar * 4 * spb
        ch = INFO_CH[form[bar]]
        root = nn(ch['bass'])
        for step in range(16):
            t = tb + step * s16
            beat, on = step // 4, step % 4 == 0
            fill = last and step >= 8
            stop = isB and last and 0 < step < 8
            if fill:
                g = 0.35 + 0.65 * (step - 8) / 7
                drums.add(kit['snare'][step % 4], t, 0.5 * g, 0.1)
                if step in (8, 12):
                    kick_at(t, 0.8)
                continue
            if stop:
                continue
            if on and (not isB or beat in (0, 2)):
                kick_at(t)
            if on and beat in (1, 3):
                drums.add(kit['clap'][(bar + beat) % 4], t, 0.46 if not isB else 0.33, -0.1)
            if isB:
                if step % 2 == 0:
                    drums.add(kit['hat'][step % 6], t, 0.2 if on else 0.28, 0.3)
            else:
                if step % 4 == 2:
                    if inb % 4 == 3 and step == 14:
                        drums.add(kit['ohat'][0], t, 0.24, 0.3)
                    else:
                        drums.add(kit['hat'][step % 6], t, 0.34, 0.3)
                elif step % 2 == 1 and sec in (1, 3):
                    drums.add(kit['hat'][(step + 3) % 6], t, 0.11, -0.3)
        # bass
        if isB:
            pat = [(0, 3, 0), (3, 1, 0), (4, 2, 7), (6, 2, 12)] if not last else [(0, 2, 0)]
            for e, ln, iv in pat:
                bassb.add(bass_note(root + iv, ln * spb / 2 * 0.85, 0.8), tb + e * spb / 2, 0.36)
        else:
            ivs = [0, 12, 0, 12, 0, 12, 7, 12]
            for e, iv in enumerate(ivs):
                if last and e >= 4:
                    iv = [0, 0, 2, 4][e - 4] if form[bar] == 'A' else iv
                bassb.add(bass_note(root + iv, spb / 2 * 0.7, 1.0), tb + e * spb / 2, 0.36)
        # stabs
        steps = ([0, 6, 12] if not last else [0]) if isB else [2, 6, 10, 14]
        for st in steps:
            for i, nm in enumerate(ch['stab']):
                y = pluck(nn(nm), 0.5 if isB else 0.22, decay=0.22 if isB else 0.09, bright=0.8, detune=9)
                stabs.add(y, tb + st * s16, 0.5, (-0.6, 0.0, 0.6)[i])
        # lead
        table = B_LEAD if isB else A_LEAD
        evs = list(table.get(inb, []))
        if bar == 0:
            evs = evs[3:]                      # the ta-daa has the first three notes of the motif
        if bar == 31:
            evs = A_LEAD[3]                    # walk up into the final D
        for st, ln, nm in evs:
            lead.add(_lead(nm, ln, s16, decay=0.45 if isB else 0.33), tb + st * s16, 0.8)
        if inb == 0:
            drums.add(kit['crash'][sec % 2], tb, 0.34 if bar else 0.42)

    # ta-daa on beat 1
    brs.add(_brass_chord(['D4', 'F#4', 'A4', 'D5'], 0.09, 0.9, rng), 0.0, 0.8)
    brs.add(_brass_chord(['D3', 'A3', 'D4', 'F#4', 'A4', 'D5', 'F#5'], 0.72, 1.0, rng), 2 * s16, 0.9)
    brs.add(timpani(nn('D3'), 1.2, 0.8, rng), 2 * s16, 0.5)
    _sparkle(fx, 2 * s16 + 0.05, ['D7', 'F#7', 'A7', 'D8', 'A7', 'F#7', 'D8'], 0.055, rng, 0.2)
    # ending: a three-hit button (D on 1, G and A on 3 and 4) into a final held D on the next downbeat
    te = 32 * 4 * spb
    voic = {'D': ['D3', 'A3', 'D4', 'F#4', 'A4', 'D5', 'F#5'], 'G': ['G3', 'D4', 'G4', 'B4', 'D5'],
            'A': ['A3', 'E4', 'A4', 'C#5', 'E5']}
    for beat, chn, ld, final in ENDING:
        t = te + beat * spb
        kick_at(t)
        brs.add(_brass_chord(voic[chn], 1.0 if final else 0.16, 1.0 if final else 0.85, rng), t, 0.9 if final else 0.7)
        lead.add(_lead(ld, 8 if final else 3, s16), t, 0.8)
        root = nn(INFO_CH[chn]['bass'])
        bassb.add(bass_sus(root, 1.2) if final else bass_note(root + 12, 0.2, 1.0), t, 0.32 if final else 0.36)
        for i, nm in enumerate(INFO_CH[chn]['stab']):
            stabs.add(pluck(nn(nm), 1.2 if final else 0.3, decay=0.5 if final else 0.12, bright=1.0, detune=9), t, 0.5,
                      (-0.6, 0.0, 0.6)[i])
        if final or beat == 0:
            drums.add(kit['crash'][0 if final else 1], t, 0.42 if final else 0.3)
        else:
            drums.add(kit['clap'][beat % 4], t, 0.4, -0.1)
    tf = te + 4 * spb
    brs.add(timpani(nn('D3'), 1.6, 0.9, rng), tf, 0.5)
    _sparkle(fx, tf + 0.08, ['D6', 'F#6', 'A6', 'D7', 'F#7', 'A7', 'D8', 'A7', 'D8'], 0.06, rng, 0.28)

    leadbus = echo(lead.b, 3 * s16, fb=0.3, mix=0.2, pingpong=True, damp=5000)[:n]
    stabbus = hp(stabs.b, 350) * duck[:, None]
    bassbus = lp(bassb.b, 3200) * duck[:, None]
    wet = reverb(leadbus + 0.6 * stabbus + 0.7 * brs.b + fx.b + 0.25 * drums.b, t60=1.1, mix=1.0, seed=5)[:n]
    wet -= leadbus + 0.6 * stabbus + 0.7 * brs.b + fx.b + 0.25 * drums.b      # keep only the wet part
    _lv('infomercial', drums=drums.b, bass=bassbus, stabs=stabbus, lead=leadbus, brass=brs.b, fx=fx.b, wet=0.16 * wet)
    out = drums.b + bassbus + stabbus + leadbus + brs.b + fx.b + 0.2 * wet
    out = peak(out, 1800, -2.5, q=0.8)                                         # leave room for a voice
    out = master_music(out, drive=1.3, fout=0.8, ref=0.62)
    notes = {'bpm': bpm, 'bars': bars, 'key': 'D major', 'form': 'A A B A + 2-bar ending',
             'A chords': ' | '.join(INFO_A), 'B chords': ' | '.join(INFO_B),
             'ending': ' '.join(f'{c}({l})' for _, c, l, _ in ENDING),
             'A lead': {b: ' '.join(n for _, _, n in ev) for b, ev in A_LEAD.items()},
             'B lead': {b: ' '.join(n for _, _, n in ev) for b, ev in B_LEAD.items()},
             'bass roots': {k: v['bass'] for k, v in INFO_CH.items()},
             'stabs': {k: ' '.join(v['stab']) for k, v in INFO_CH.items()}}
    return out, notes


# ------------------------------------------------------------------ 3
def infomercial_sting():
    bpm = 128.0
    e8 = 60 / bpm / 2
    dur = 3.0
    rng = np.random.default_rng(303)
    kit = _drumkit(21)
    mx, fx = Mix(dur), Mix(dur)
    t0 = 0.02
    starts = [0, 1, 2, 4, 5, 6]                 # eighths; the third note is a quarter
    for i, (st, nm) in enumerate(zip(starts, STING_NOTES)):
        ln = 2 if i == 2 else 1
        g = 0.5 if i < 5 else 0.6
        mx.add(pluck(nn(nm), 1.4 if i == 5 else ln * e8 + 0.3, decay=0.6 if i == 5 else 0.3, bright=1.3, detune=7,
                     even=0.75), t0 + st * e8, g)
    tc = t0 + 6 * e8
    for i, nm in enumerate(['D4', 'F#4', 'A4', 'D5', 'F#5']):
        mx.add(pluck(nn(nm), 1.5, decay=0.7, bright=1.1, detune=9), tc, 0.3, (-0.6, -0.3, 0.0, 0.3, 0.6)[i])
    mx.add(_brass_chord(['D3', 'A3', 'D4', 'F#4', 'A4'], 0.6, 0.8, rng), tc, 0.45)
    mx.add(bass_sus(nn('D2'), 0.7), tc, 0.4)
    mx.add(kit['kick'][0], tc, 0.7)
    mx.add(kit['crash'][0], tc, 0.2)
    spark = ['D7', 'A6', 'F#7', 'D7', 'A7', 'F#7', 'D8', 'A7', 'F#8', 'D8', 'A7', 'D8']
    _sparkle(fx, tc + 0.06, spark, 0.07, rng, 0.2, tau=0.25)
    out = reverb(mx.b + fx.b, t60=1.3, mix=0.18, seed=5)[:mx.n]
    out = master_music(out, drive=1.2, fout=0.35, ref=0.6)
    return out, {'key': 'D major', 'jingle': ' '.join(STING_NOTES), 'final chord': 'D3 A3 D4 F#4 A4 D5 F#5',
                 'sparkle': ' '.join(spark)}


# ------------------------------------------------------------------ 4
def machine():
    bpm = 140.0
    spb = 60 / bpm
    s16 = spb / 4
    bars = 14
    dur = bars * 4 * spb
    rng = np.random.default_rng(404)
    n = int(round(dur * SR))
    t = np.arange(n) / SR
    tones = {
        'Esus2': ['E3', 'F#3', 'B3', 'E4', 'F#4', 'B4', 'E5', 'F#5'],
        'Csus2': ['C3', 'D3', 'G3', 'C4', 'D4', 'G4', 'C5', 'D5'],
        'Asus4': ['A3', 'D4', 'E4', 'A4', 'D5', 'E5', 'A5', 'D6'],
        'Bsus4': ['B3', 'E4', 'F#4', 'B4', 'E5', 'F#5', 'B5', 'E6', 'F#6', 'B6'],
    }
    pat = [0, 3, 2, 5, 3, 6, 5, 3, 0, 3, 2, 5, 4, 7, 5, 3]
    rise = [[0, 1, 2, 1, 1, 2, 3, 2, 2, 3, 4, 3, 3, 4, 5, 4], [4, 5, 6, 5, 5, 6, 7, 6, 6, 7, 8, 7, 7, 8, 9, 8]]
    plan = ['Esus2'] * 4 + ['Csus2'] * 4 + ['Asus4'] * 4 + ['Bsus4'] * 2
    roots = {'Esus2': 'E2', 'Csus2': 'C2', 'Asus4': 'A2', 'Bsus4': 'B2'}
    pads = {'Esus2': ['E3', 'B3', 'F#4'], 'Csus2': ['C3', 'G3', 'D4'], 'Asus4': ['A3', 'D4', 'E4'],
            'Bsus4': ['B3', 'E4', 'F#4']}
    arp = np.zeros(n)
    bassb, tick, blp, padb, risb = (Mix(dur) for _ in range(5))
    seqlog = []
    ticks = [hat(rng, dur=0.03, tau=0.004, fc=9000) for _ in range(6)]
    thump = kick(rng, dur=0.2, f0=110, f1=50, tp=0.02, ta=0.07, click=0.05)
    penta = ['E6', 'G6', 'A6', 'B6', 'D7', 'E7']
    bleeps = []
    for bar in range(bars):
        ch = plan[bar]
        idx = rise[bar - 12] if bar >= 12 else pat
        names = [tones[ch][i] for i in idx]
        seqlog.append(f'bar {bar + 1:2d} {ch}: ' + ' '.join(names))
        prog = bar / (bars - 1)
        for step, nm in enumerate(names):
            t0 = (bar * 16 + step) * s16
            m = int((s16 * 0.8 + 0.03) * SR)
            f = hz(nm)
            y = (0.6 * saw(f, m, 0.0) + 0.4 * square(f * 1.003, m, 0.35)) * adsr(s16 * 0.8, 0.002, 0.06, 0.35, 0.03, n=m)
            i = int(t0 * SR)
            mm = min(m, n - i)
            arp[i:i + mm] += y[:mm] * (1.25 if step % 4 == 0 else 1.0)
            # ticking hat
            if step % 2 == 0 or bar >= 4:
                g = (0.5 if step % 4 == 0 else 0.3) if step % 2 == 0 else 0.14 + 0.1 * prog
                tick.add(ticks[step % 6], t0, 1.5 * g * (0.7 + 0.5 * prog), 0.35 if step % 2 == 0 else -0.35)
            if step % 2 == 0 or bar == 13:
                bassb.add(bass_note(nn(roots[ch]) + (12 if step % 8 == 6 else 0), s16 * 1.4, 0.7 + 0.6 * prog), t0, 0.3)
            if bar >= 4 and step % 4 == 0:
                bassb.add(thump, t0, 0.4)
        # bleeps, denser as it goes
        for st in sorted(rng.choice(16, size=2 + bar // 3, replace=False)):
            nm = penta[rng.integers(len(penta))] if bar < 12 else ['F#6', 'B6', 'E7', 'F#7'][rng.integers(4)]
            m = int(0.09 * SR)
            y = (0.7 * sine(hz(nm), m) + 0.3 * square(hz(nm), m)) * adsr(0.045, 0.002, 0.03, 0.4, 0.04, n=m)
            blp.add(lp(y, 6000), (bar * 16 + st) * s16, 0.75, rng.uniform(-0.8, 0.8))
            bleeps.append(nm)
        if bar % 4 == 0 or bar == 12:
            ln = (2 if bar == 12 else 4) * 4 * spb
            for nm in pads[ch]:
                padb.add(pad_note(nn(nm), ln - 0.3, a=0.6, r=0.6, cutoff=1100 + 1500 * prog, rng=rng), bar * 4 * spb,
                         0.22 + 0.12 * prog)
    # the slowly rising filter over the arpeggio
    fc = 650.0 * (9500.0 / 650.0) ** ((t / dur) ** 1.3) * (1 + 0.12 * np.sin(TAU * 0.29 * t))
    arp = sat(svf(arp, fc, q=3.2, mode='lp') * 0.5, 1.4)
    arpbus = echo(pan(arp, -0.15), 3 * s16, fb=0.35, mix=0.28, pingpong=True, damp=4500)[:n]
    # tension: noise riser over the last four bars, pitch riser and roll over the last two
    t10 = 10 * 4 * spb
    m = n - int(t10 * SR)
    u = np.arange(m) / m
    for c, pp in ((0, -0.6), (1, 0.6)):
        nz = svf(rng.standard_normal(m), 300 * (9000 / 300) ** u, q=2.0, mode='bp')
        risb.add(nz * u ** 2 * 0.6, t10, 1.0, pp)
    t12 = 12 * 4 * spb
    m = n - int(t12 * SR)
    u = np.arange(m) / m
    fr = hz('B3') * 2 ** (2 * u)
    trem = 0.6 + 0.4 * np.sin(TAU * np.cumsum(4 + 14 * u) / SR)
    tone = lp(saw(fr, m) + saw(fr * 1.007, m, 0.5), 5000) * u ** 1.5 * trem
    risb.add(tone, t12, 0.38, 0.0)
    t13 = 13 * 4 * spb
    k = 0
    tr = t13
    while tr < dur - 0.02:
        prog = (tr - t13) / (dur - t13)
        risb.add(snare(rng, dur=0.1, tone=210), tr, 0.1 + 0.3 * prog, 0.2 * (-1) ** k)
        tr += s16 if prog < 0.5 else s16 / 2
        k += 1
    _lv('machine', arp=arpbus, bass=bassb.b, tick=tick.b, bleep=blp.b, pad=padb.b, riser=risb.b)
    dry = arpbus + bassb.b + tick.b + blp.b + padb.b + risb.b
    wetsrc = arpbus + echo(blp.b, 3 * s16, fb=0.45, mix=0.5, pingpong=True)[:n] + padb.b + 0.5 * risb.b
    wet = reverb(wetsrc, t60=1.4, mix=1.0, seed=9)[:n] - wetsrc
    out = dry + 0.2 * wet + 0.35 * (echo(blp.b, 3 * s16, fb=0.45, mix=0.5, pingpong=True)[:n] - blp.b)
    out = master_music(out, drive=1.3, fout=0.15, ref=0.6)
    return out, {'bpm': bpm, 'bars': bars, 'key': 'E minor, suspended chords, ends on Bsus4 (V) unresolved',
                 'arpeggio (16ths)': seqlog, 'bass roots': ' '.join(roots[c] for c in plan),
                 'bleeps': ' '.join(bleeps)}


# ------------------------------------------------------------------ 5
def lobby_muzak():
    bpm = 104.0
    spb = 60 / bpm
    e8 = spb / 2
    bars = 20
    dur = bars * 4 * spb
    rng = np.random.default_rng(505)
    CH = {
        'Fmaj7': ('F2', ['A3', 'C4', 'E4', 'G4']),
        'Dm7': ('D2', ['F3', 'A3', 'C4', 'E4']),
        'Gm7': ('G2', ['F3', 'Bb3', 'D4', 'A4']),
        'C7': ('C2', ['E3', 'Bb3', 'D4', 'A4']),
        'Am7': ('A2', ['G3', 'C4', 'E4', 'G4']),
        'Bbmaj7': ('Bb1', ['A3', 'D4', 'F4', 'A4']),
    }
    prog8 = ['Fmaj7', 'Dm7', 'Gm7', 'C7', 'Am7', 'Dm7', 'Gm7', 'C7']
    form = prog8 + prog8 + ['Fmaj7', 'Bbmaj7', 'Fmaj7', 'Fmaj7']
    MEL = {
        2: [(2, 1, 'D5'), (3, 1, 'C5')],
        3: [(0, 2, 'A4')],
        6: [(2, 1, 'Bb4'), (3, 1, 'D5')],
        7: [(0, 2, 'C5')],
        8: [(0, 1.5, 'C5'), (1.5, 0.5, 'A4'), (2, 2, 'G4')],
        9: [(2, 1, 'F4'), (3, 1, 'A4')],
        10: [(0, 1.5, 'Bb4'), (1.5, 0.5, 'A4'), (2, 2, 'G4')],
        11: [(2, 1, 'E4'), (3, 1, 'G4')],
        12: [(0, 1.5, 'C5'), (1.5, 0.5, 'A4'), (2, 2, 'E5')],
        13: [(0, 1.5, 'D5'), (1.5, 0.5, 'C5'), (2, 2, 'A4')],
        14: [(0, 1, 'Bb4'), (1, 1, 'D5'), (2, 2, 'C5')],
        15: [(0, 2, 'Bb4'), (2, 1, 'G4'), (3, 1, 'E4')],
        16: [(0, 3, 'A4')],
        17: [(0, 2, 'D5'), (2, 2, 'C5')],
        18: [(0, 4, 'A4')],
    }
    ep, bassb, perc, mel = (Mix(dur) for _ in range(4))
    rims = [rim(rng) for _ in range(3)]
    shk = [shaker(rng) for _ in range(6)]
    soft = kick(rng, dur=0.2, f0=85, f1=48, tp=0.02, ta=0.07, click=0.03)
    clave = [0, 3, 6, 10, 13]
    for bar in range(bars):
        root, voic = CH[form[bar]]
        tb = bar * 4 * spb
        lastbar = bar == bars - 1
        hits = [0] if lastbar else ([0, 3, 6] if bar % 2 == 0 else [2, 5])
        for h in hits:
            ln = 3.2 * spb if lastbar else (e8 * 2.4 if h in (0, 2, 3) else e8 * 1.6)
            for i, nm in enumerate(voic):
                v = 0.5 * rng.uniform(0.85, 1.0) * (0.9 if h else 1.0)
                ep.add(epiano(nn(nm), ln, v), tb + h * e8 + 0.006 * i + rng.uniform(0, 0.004), 0.5, (-0.3, -0.1, 0.1, 0.3)[i])
        r = nn(root)
        bpat = [(0, 2.6, 0)] if lastbar else [(0, 2.4, 0), (3, 0.8, 0), (4, 2.4, 7), (7, 0.8, 7)]
        for e, ln, iv in bpat:
            bassb.add(lp(bass_note(r + iv, ln * e8 * 0.9, 0.35), 900), tb + e * e8, 0.3)
        if lastbar:
            perc.add(soft, tb, 0.3)
            continue
        for e in range(8):
            t0 = tb + e * e8
            if e in (0, 3, 4, 7):
                perc.add(soft, t0, 0.24 if e in (0, 4) else 0.15)
            perc.add(shk[e % 6], t0 - 0.012, 0.3 if e % 2 else 0.18, 0.4)
            if (bar % 2) * 8 + e in clave and bar >= 2:
                perc.add(rims[e % 3], t0, 0.3, -0.4)
        # brushed swish on every beat
        for b in range(4):
            m = int(0.3 * SR)
            tt = np.arange(m) / SR
            sw = bp(rng.standard_normal(m), 4200, q=0.7) * np.minimum(1, tt / 0.07) * np.exp(-np.maximum(tt - 0.07, 0) / 0.09)
            perc.add(sw, tb + b * spb - 0.03, 0.16 if b % 2 == 0 else 0.24, -0.2)
        for beat, ln, nm in MEL.get(bar, []):
            y = bell(hz(nm), ln * spb + 0.8, tau=0.55, bright=0.35)
            mel.add(y, tb + beat * spb + rng.uniform(0, 0.012), 0.3, 0.15)
    epbus = chorus(tremolo_pan(ep.b, 4.6, 0.28), rate=0.5, depth=0.002, mix=0.3)
    wetsrc = epbus + mel.b + 0.3 * perc.b
    wet = reverb(wetsrc, t60=1.5, mix=1.0, seed=13, damp=3800)[:ep.n] - wetsrc
    _lv('lobby', ep=epbus, bass=bassb.b, perc=perc.b, mel=mel.b, wet=0.2 * wet)
    out = lp(epbus, 7000) + bassb.b + perc.b + mel.b + 0.2 * wet
    out = master_music(out, drive=1.1, fout=1.2, ref=0.55)
    return out, {'bpm': bpm, 'bars': bars, 'key': 'F major', 'chords': ' | '.join(form),
                 'voicings': {k: v[0] + ' / ' + ' '.join(v[1]) for k, v in CH.items()},
                 'melody': {b + 1: ' '.join(n for _, _, n in ev) for b, ev in MEL.items()}}


# ------------------------------------------------------------------ 6
def hero():
    bpm = 76.0
    spb = 60 / bpm
    bars = 7
    dur = bars * 4 * spb
    rng = np.random.default_rng(606)
    chords = [
        (0, 4, ['G3', 'B3', 'D4', 'G4'], 'G2', 'G'),
        (4, 4, ['F#3', 'A3', 'D4', 'F#4'], 'F#2', 'D/F#'),
        (8, 4, ['G3', 'B3', 'E4', 'G4'], 'E2', 'Em'),
        (12, 4, ['G3', 'C4', 'E4', 'G4'], 'C3', 'C'),
        (16, 2, ['A3', 'C4', 'E4', 'G4'], 'A2', 'Am7'),
        (18, 2, ['A3', 'D4', 'F#4', 'A4'], 'D3', 'D'),
        (20, 5.2, ['G3', 'B3', 'D4', 'G4', 'B4', 'D5'], 'G2', 'G'),
    ]
    MEL = [
        (0, 2, 'B4'), (2, 1, 'D5'), (3, 1, 'G5'),
        (4, 2, 'F#5'), (6, 1, 'D5'), (7, 1, 'A5'),
        (8, 2, 'G5'), (10, 1, 'E5'), (11, 1, 'B5'),
        (12, 1.5, 'C6'), (13.5, 0.5, 'B5'), (14, 1, 'G5'), (15, 1, 'E5'),
        (16, 1, 'A5'), (17, 1, 'C6'), (18, 1, 'D6'), (19, 1, 'F#6'),
        (20, 6, 'G6'),
    ]
    padb, bassb, pno, fx = (Mix(dur) for _ in range(4))
    gains = [0.58, 0.66, 0.74, 0.83, 0.9, 0.96, 1.0]
    for i, (b0, ln, voic, root, _) in enumerate(chords):
        final = i == len(chords) - 1
        for nm in voic:
            padb.add(pad_note(nn(nm), ln * spb, a=0.9 if i == 0 else 0.35, r=2.4 if final else 0.9,
                              cutoff=1300 + 250 * i, rng=rng), b0 * spb, 0.5 * gains[i])
            if i >= 2:
                padb.add(pad_note(nn(nm) + 12, ln * spb, a=0.6, r=2.4 if final else 0.9, cutoff=2600, nvoices=3,
                                  rng=rng), b0 * spb, 0.16 * gains[i] * (i - 1) / 5 * 2)
        bassb.add(bass_sus(nn(root), ln * spb, a=0.1, r=1.6 if final else 0.3), b0 * spb, 0.26 * gains[i])
        if final:
            bassb.add(bass_sus(nn(root) - 12, ln * spb, a=0.1, r=1.6), b0 * spb, 0.16)
    for k, (b0, ln, nm) in enumerate(MEL):
        v = 0.58 + 0.34 * min(1.0, b0 / 20.0)
        pno.add(piano(nn(nm), ln * spb + 0.8, v, rng), max(0.002, b0 * spb + rng.normal(0, 0.005)), 1.0)
        if b0 >= 16:
            pno.add(piano(nn(nm) - 12, ln * spb + 0.8, v * 0.7, rng), b0 * spb + 0.012, 1.0)
    roll = ['G2', 'D3', 'G3', 'B3', 'D4', 'G4', 'B4', 'D5']
    for j, nm in enumerate(roll):
        pno.add(piano(nn(nm), 6 * spb, 0.7, rng), 20 * spb + 0.022 * j)
    # swell into the final chord, soft timpani on it
    t17 = 17 * spb
    m = int(3 * spb * SR)
    u = np.arange(m) / m
    for pp in (-0.5, 0.5):
        fx.add(hp(rng.standard_normal(m), 4000) * u ** 3, t17, 0.1, pp)
    fx.add(crash(rng, dur=2.5), 20 * spb, 0.16)
    fx.add(timpani(nn('G2'), 2.2, 1.0, rng), 20 * spb, 0.55)
    padbus = chorus(padb.b, rate=0.35, depth=0.004, base=0.015, mix=0.5)
    src = padbus + pno.b + fx.b
    wet = reverb(src, t60=2.8, mix=1.0, seed=17, damp=4500)[:padb.n] - src
    _lv('hero', pad=padbus, piano=pno.b, fx=fx.b, bass=bassb.b, wet=0.3 * wet)
    out = src + bassb.b + 0.3 * wet
    out = master_music(out, drive=1.1, fout=2.2)
    return out, {'bpm': bpm, 'bars': bars, 'key': 'G major',
                 'chords': ' | '.join(c[4] for c in chords) + ' (held)',
                 'melody': ' '.join(n for _, _, n in MEL), 'final piano roll': ' '.join(roll)}


# ------------------------------------------------------------------ 7
def awards_bumper():
    bpm = 120.0
    spb = 60 / bpm
    dur = 12 * spb
    rng = np.random.default_rng(707)
    th = 1 / 3
    MEL = [(0, th, 'Bb4'), (th, th, 'Eb5'), (2 * th, th, 'G5'), (1, 1.5, 'Bb5'), (2.5, 0.5, 'Ab5'), (3, 1, 'G5'),
           (4, 0.5, 'Ab5'), (4.5, 0.5, 'Bb5'), (5, 1, 'C6'), (6, 1, 'Bb5'),
           (7, th, 'Bb5'), (7 + th, th, 'C6'), (7 + 2 * th, th, 'D6'), (8, 2.7, 'Eb6')]
    SEC = [(1, 1.5, 'G5'), (2.5, 0.5, 'F5'), (3, 1, 'Eb5'), (4, 0.5, 'Eb5'), (4.5, 0.5, 'Eb5'), (5, 1, 'Ab5'),
           (6, 1, 'F5'), (7, th, 'F5'), (7 + th, th, 'Ab5'), (7 + 2 * th, th, 'Bb5'), (8, 2.7, 'Bb5')]
    LOW = [(1, 1.5, ['Eb3', 'Bb3', 'Eb4', 'G4']), (3, 0.9, ['Eb3', 'Bb3', 'Eb4', 'G4']),
           (4, 1, ['Ab2', 'Ab3', 'C4', 'Eb4']), (5, 1, ['Ab2', 'Ab3', 'C4', 'Eb4']),
           (6, 1, ['Bb2', 'Bb3', 'D4', 'F4']),
           (7, th, ['Bb2', 'Bb3', 'D4', 'Ab4']), (7 + th, th, ['Bb2', 'Bb3', 'D4', 'Ab4']),
           (7 + 2 * th, th, ['Bb2', 'Bb3', 'D4', 'Ab4']),
           (8, 2.7, ['Eb2', 'Eb3', 'Bb3', 'Eb4', 'G4', 'Bb4'])]
    TIMP = [(1, 'Eb3', 0.8), (3, 'Bb2', 0.6), (4, 'Eb3', 0.6), (6, 'Bb2', 0.7), (7, 'Bb2', 0.6), (7 + th, 'Bb2', 0.75),
            (7 + 2 * th, 'Bb2', 0.9), (8, 'Eb3', 1.0)]
    brs, prc = Mix(dur), Mix(dur)
    for b0, ln, nm in MEL:
        g = ln * spb * (0.82 if ln < 1 else 0.93)
        brs.add(brass(nn(nm), g, 0.95, a=0.025, bright=1.15, rng=rng), b0 * spb, 0.62, 0.15)
    for b0, ln, nm in SEC:
        g = ln * spb * (0.82 if ln < 1 else 0.93)
        brs.add(brass(nn(nm), g, 0.85, a=0.03, bright=1.0, rng=rng), b0 * spb, 0.42, -0.25)
    for b0, ln, voic in LOW:
        g = ln * spb * (0.8 if ln < 1 else 0.92)
        brs.add(_brass_chord(voic, g, 0.85, rng, bright=0.8, a=0.04), b0 * spb, 0.75)
    for b0, nm, v in TIMP:
        prc.add(timpani(nn(nm), 1.8, v, rng), b0 * spb, 0.5, -0.2)
    prc.add(kick(rng, dur=0.5, f0=90, f1=40, tp=0.04, ta=0.22, click=0.1), 8 * spb, 0.45)
    prc.add(crash(rng, dur=2.2), 8 * spb, 0.42)
    prc.add(crash(rng, dur=1.2), 1 * spb, 0.2)
    tr = 6 * spb
    while tr < 8 * spb - 0.01:
        u = (tr - 6 * spb) / (2 * spb)
        prc.add(snare(rng, dur=0.12, tone=200), tr, 0.1 + 0.32 * u ** 1.5, 0.25)
        tr += spb / 12 * 1.5
    _lv('awards', brass=brs.b, perc=prc.b)
    src = brs.b + prc.b
    wet = reverb(src, t60=1.9, mix=1.0, seed=19, damp=5000)[:brs.n] - src
    out = src + 0.24 * wet
    out = master_music(out, drive=1.3, fout=0.4, ref=0.6)
    return out, {'bpm': bpm, 'bars': 3, 'key': 'Eb major', 'chords': 'Eb | Ab Bb7 | Eb',
                 'lead trumpet': ' '.join(n for _, _, n in MEL), 'second trumpet': ' '.join(n for _, _, n in SEC),
                 'timpani': ' '.join(n for _, n, _ in TIMP)}


# name, function, target seconds from the brief, description
TRACKS = [
    ('music/sad_piano.wav', sad_piano, 24.0,
     'Slow over-sentimental solo piano in A minor, 66 BPM, 7 bars, ends on a held Am that rings out'),
    ('music/infomercial.wav', infomercial, 64.0,
     'Cheesy shopping-channel jingle bed, D major, 128 BPM, ta-daa then A A B A (8 bars each) + 2-bar ending'),
    ('music/infomercial_sting.wav', infomercial_sting, 3.0,
     'Six-note logo jingle in the infomercial key and lead sound, bright D chord with sparkle'),
    ('music/machine.wav', machine, 24.0,
     'Computer-is-thinking bed, 140 BPM, 14 bars: 16th sus-chord arpeggio, bleeps, ticking hat, rising filter, unresolved riser at the end'),
    ('music/lobby_muzak.wav', lobby_muzak, 48.0,
     'Bland bossa-ish lobby muzak, F major, 104 BPM, 20 bars: tremolo electric piano, soft bass, brushes, rim clave'),
    ('music/hero.wav', hero, 22.0,
     'Warm sincere resolution in G major, 76 BPM: pad and piano melody build to a held final chord with a long tail'),
    ('music/awards_bumper.wav', awards_bumper, 6.0,
     'Grand awards-show brass fanfare in Eb major, 120 BPM, 3 bars, timpani, snare roll and crash'),
]
