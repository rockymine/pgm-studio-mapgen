#!/usr/bin/env python3
"""Core DSP helpers for the synth library. numpy + stdlib only."""
import math
import os
import wave

import numpy as np

SR = 48000
TAU = 2 * np.pi

# ----------------------------------------------------------------- pitch
_N = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
_NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']


def nn(s):
    """Note name ('F#4', 'Bb2') or midi number -> midi number."""
    if not isinstance(s, str):
        return s
    p = _N[s[0]]
    i = 1
    while s[i] in '#b':
        p += 1 if s[i] == '#' else -1
        i += 1
    return p + 12 * (int(s[i:]) + 1)


def hz(m):
    return 440.0 * 2.0 ** ((nn(m) - 69) / 12.0)


def nname(m):
    m = int(round(nn(m)))
    return _NAMES[m % 12] + str(m // 12 - 1)


# ------------------------------------------------------------- envelopes
def adsr(gate, a=0.005, d=0.1, s=0.7, r=0.1, n=None):
    total = int(round((gate + r) * SR)) if n is None else n
    t = np.arange(total) / SR
    a = max(a, 1e-4)
    d = max(d, 1e-4)
    r = max(r, 1e-4)
    held = np.where(t < a, t / a, s + (1 - s) * np.exp(-4.0 * np.maximum(t - a, 0) / d))
    lvl = (gate / a) if gate < a else s + (1 - s) * math.exp(-4.0 * (gate - a) / d)
    tr = np.clip((t - gate) / r, 0, 1)
    rel = lvl * np.exp(-4.0 * tr) * (1 - tr)
    return np.where(t < gate, held, rel)


def fade(x, fin=0.003, fout=0.003):
    """Raised-cosine fade in/out, in place."""
    n = len(x)
    a = min(int(fin * SR), n // 2)
    b = min(int(fout * SR), n // 2)
    if a > 0:
        w = 0.5 - 0.5 * np.cos(np.pi * np.arange(a) / a)
        x[:a] = (x[:a].T * w).T
    if b > 0:
        w = 0.5 + 0.5 * np.cos(np.pi * (np.arange(b) + 1) / b)
        x[n - b:] = (x[n - b:].T * w).T
    return x


# ----------------------------------------------------------- oscillators
def saw(freq, n, phase0=0.0):
    """Band-limited (polyBLEP) sawtooth; freq scalar or per-sample array."""
    dt = np.broadcast_to(np.asarray(freq, float) / SR, (n,))
    p = (phase0 + np.cumsum(dt) - dt) % 1.0
    y = 2 * p - 1
    m = p < dt
    tt = p[m] / dt[m]
    y[m] -= tt + tt - tt * tt - 1
    m = p > 1 - dt
    tt = (p[m] - 1) / dt[m]
    y[m] -= tt * tt + tt + tt + 1
    return y


def square(freq, n, pw=0.5, phase0=0.0):
    return saw(freq, n, phase0) - saw(freq, n, phase0 + pw)


def sine(freq, n, phase0=0.0):
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    return np.sin(TAU * (np.cumsum(f) - f) / SR + phase0)


# --------------------------------------------------------------- filters
def _fftlen(n):
    return 1 << int(math.ceil(math.log2(max(n, 2))))


def _coefs(kind, fc, q, gain_db):
    w0 = TAU * min(max(fc, 5.0), SR * 0.49) / SR
    cw, sw = math.cos(w0), math.sin(w0)
    al = sw / (2 * q)
    A = 10 ** (gain_db / 40.0)
    if kind == 'lp':
        b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == 'hp':
        b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == 'bp':
        b = [al, 0.0, -al]
        a = [1 + al, -2 * cw, 1 - al]
    elif kind == 'peak':
        b = [1 + al * A, -2 * cw, 1 - al * A]
        a = [1 + al / A, -2 * cw, 1 - al / A]
    elif kind == 'hishelf':
        sq = 2 * math.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * cw + sq), -2 * A * ((A - 1) + (A + 1) * cw), A * ((A + 1) + (A - 1) * cw - sq)]
        a = [(A + 1) - (A - 1) * cw + sq, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - sq]
    elif kind == 'loshelf':
        sq = 2 * math.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * cw + sq), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - sq)]
        a = [(A + 1) + (A - 1) * cw + sq, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - sq]
    else:
        raise ValueError(kind)
    return b, a


def filt(x, kind, fc, q=0.7071, gain_db=0.0, passes=1, circular=False):
    """Static biquad applied in the frequency domain (exact causal IIR response)."""
    n = x.shape[0]
    N = n if circular else _fftlen(n + SR // 2)
    b, a = _coefs(kind, fc, q, gain_db)
    X = np.fft.rfft(x, N, axis=0)
    w = TAU * np.arange(N // 2 + 1) / N
    z1 = np.exp(-1j * w)
    z2 = z1 * z1
    H = ((b[0] + b[1] * z1 + b[2] * z2) / (a[0] + a[1] * z1 + a[2] * z2)) ** passes
    if x.ndim == 2:
        H = H[:, None]
    return np.fft.irfft(X * H, N, axis=0)[:n]


def lp(x, fc, q=0.7071, passes=1, **k):
    return filt(x, 'lp', fc, q, passes=passes, **k)


def hp(x, fc, q=0.7071, passes=1, **k):
    return filt(x, 'hp', fc, q, passes=passes, **k)


def bp(x, fc, q=1.0, passes=1, **k):
    return filt(x, 'bp', fc, q, passes=passes, **k)


def peak(x, fc, gain_db, q=1.0):
    return filt(x, 'peak', fc, q, gain_db)


def svf(x, fc, q=0.7071, mode='lp'):
    """Time-varying state-variable filter (TPT form). Mono; fc/q scalar or arrays."""
    n = len(x)
    fc = np.broadcast_to(np.asarray(fc, float), (n,))
    q = np.broadcast_to(np.asarray(q, float), (n,))
    g = np.tan(np.pi * np.clip(fc, 10.0, SR * 0.45) / SR)
    k = 1.0 / q
    a1 = 1.0 / (1.0 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    A1, A2, A3, K, X = a1.tolist(), a2.tolist(), a3.tolist(), k.tolist(), np.asarray(x, float).tolist()
    out = [0.0] * n
    ic1 = ic2 = 0.0
    if mode == 'lp':
        for i in range(n):
            v3 = X[i] - ic2
            v1 = A1[i] * ic1 + A2[i] * v3
            v2 = ic2 + A2[i] * ic1 + A3[i] * v3
            ic1 = 2 * v1 - ic1
            ic2 = 2 * v2 - ic2
            out[i] = v2
    elif mode == 'bp':
        for i in range(n):
            v3 = X[i] - ic2
            v1 = A1[i] * ic1 + A2[i] * v3
            v2 = ic2 + A2[i] * ic1 + A3[i] * v3
            ic1 = 2 * v1 - ic1
            ic2 = 2 * v2 - ic2
            out[i] = K[i] * v1
    else:
        for i in range(n):
            v0 = X[i]
            v3 = v0 - ic2
            v1 = A1[i] * ic1 + A2[i] * v3
            v2 = ic2 + A2[i] * ic1 + A3[i] * v3
            ic1 = 2 * v1 - ic1
            ic2 = 2 * v2 - ic2
            out[i] = v0 - K[i] * v1 - v2
    return np.array(out)


# ----------------------------------------------------- stereo and mixing
def stereo(x):
    if x.ndim == 2:
        return x
    return np.stack([x, x], 1) * 0.7071


def pan(x, p):
    """Constant-power pan of a mono signal, p in [-1, 1]."""
    th = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)], 1)


class Mix:
    def __init__(self, dur):
        self.n = int(round(dur * SR))
        self.b = np.zeros((self.n, 2))

    def add(self, sig, t=0.0, gain=1.0, p=0.0):
        if sig.ndim == 1:
            sig = pan(sig, p)
        elif p != 0.0:
            sig = sig * np.array([min(1.0, 1 - p), min(1.0, 1 + p)])
        i = int(round(t * SR))
        if i < 0:
            sig = sig[-i:]
            i = 0
        if i >= self.n:
            return
        m = min(len(sig), self.n - i)
        self.b[i:i + m] += gain * sig[:m]


def fit(x, n):
    x = stereo(x)
    if len(x) >= n:
        return x[:n].copy()
    out = np.zeros((n, 2))
    out[:len(x)] = x
    return out


# --------------------------------------------------------------- effects
def sat(x, drive=1.5):
    return np.tanh(x * drive) / math.tanh(drive)


def fftconv(x, h):
    n = len(x) + len(h) - 1
    N = _fftlen(n)
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(h, N), N)[:n]


_IR = {}


def make_ir(t60, damp, seed, predelay, lowcut):
    key = (t60, damp, seed, predelay, lowcut)
    if key in _IR:
        return _IR[key]
    n = int(SR * t60 * 1.1)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    pd = int(predelay * SR)
    er = int(0.07 * SR)
    out = np.zeros((n + pd + er, 2))
    for c in range(2):
        w = rng.standard_normal(n)
        lo = lp(w, damp)
        h = lo * np.exp(-6.91 * t / t60) + (w - lo) * np.exp(-6.91 * t / (t60 * 0.3))
        h = hp(h, lowcut)
        h *= np.minimum(1.0, t / 0.012) ** 0.5
        h *= np.clip((n - np.arange(n)) / (0.05 * SR), 0, 1)
        h /= np.sqrt(np.sum(h * h))
        out[pd + er // 3:pd + er // 3 + n, c] += h
        # a few early reflections
        for k in range(5):
            i = pd + int(rng.uniform(0.004, 0.06) * SR)
            out[i, c] += rng.choice([-1, 1]) * 0.22 * (0.8 ** k)
    _IR[key] = out
    return out


def reverb(x, t60=1.5, mix=0.25, damp=5000.0, predelay=0.012, seed=7, lowcut=180.0):
    """Convolution reverb with exponentially decaying filtered noise. Returns n + tail samples."""
    x = stereo(x)
    n = len(x)
    ir = make_ir(t60, damp, seed, predelay, lowcut)
    out = np.zeros((n + len(ir) - 1, 2))
    out[:n] = x
    for c in range(2):
        src = 0.7 * x[:, c] + 0.3 * x[:, 1 - c]
        out[:, c] += mix * fftconv(src, ir[:, c])
    return out


def echo(x, time, fb=0.4, mix=0.3, pingpong=False, damp=None):
    x = stereo(x)
    n = len(x)
    d = int(time * SR)
    reps = max(1, int(math.ceil(math.log(0.002) / math.log(fb))))
    out = np.zeros((n + d * reps, 2))
    out[:n] = x
    cur = x * mix
    for k in range(1, reps + 1):
        if pingpong:
            cur = cur[:, ::-1] if k > 1 else cur * np.array([1.3, 0.3])
        if damp:
            cur = lp(cur, damp)
        out[k * d:k * d + n] += cur
        cur = cur * fb
    return out


def chorus(x, rate=0.6, depth=0.003, base=0.012, mix=0.5):
    x = stereo(x)
    n = len(x)
    idx = np.arange(n, dtype=float)
    t = idx / SR
    out = np.empty_like(x)
    for c in range(2):
        d = (base + depth * np.sin(TAU * rate * t + c * np.pi / 2)) * SR
        out[:, c] = x[:, c] * (1 - 0.4 * mix) + mix * np.interp(idx - d, idx, x[:, c], left=0.0)
    return out


def tremolo_pan(x, rate=4.6, depth=0.3):
    x = stereo(x).copy()
    t = np.arange(len(x)) / SR
    l = np.sin(TAU * rate * t)
    x[:, 0] *= 1 + depth * l
    x[:, 1] *= 1 - depth * l
    return x


# ----------------------------------------------------------- instruments
def piano(m, dur, vel=0.7, rng=None, release=0.3):
    """Additive piano-ish tone: inharmonic partials, two detuned strings, two-stage decay."""
    rng = rng or np.random.default_rng(0)
    f = hz(m)
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    B = 0.00032
    K = int(min(18, max(3, 9000 // f)))
    tau0 = 2.4 * (261.6 / f) ** 0.5
    bright = 0.25 + 0.75 * vel
    keypan = (nn(m) - 62) / 48.0 * 0.6
    out = np.zeros((n, 2))
    for k in range(1, K + 1):
        fk = k * f * math.sqrt(1 + B * k * k)
        if fk > 0.42 * SR:
            break
        amp = (1.0 / k ** 1.2) * math.exp(-(k - 1) * (1 - bright) * 0.45) * (0.25 + abs(math.sin(math.pi * k / 7.3)))
        tau1 = tau0 / (1 + 0.22 * (k - 1))
        nk = min(n, int(tau1 * 1.6 * 9.0 * SR))
        tk = t[:nk]
        env = 0.72 * np.exp(-tk / (tau1 * 0.3)) + 0.28 * np.exp(-tk / (tau1 * 1.6))
        for det, pp in ((-0.8, -0.22), (0.8, 0.22)):
            w = np.sin(TAU * fk * 2 ** (det / 1200.0) * tk + rng.uniform(0, TAU))
            out[:nk] += pan(0.5 * amp * env * w, keypan + pp)
    out *= (1 - np.exp(-t / 0.0012))[:, None]
    # hammer thunk
    hn = int(0.03 * SR)
    th = bp(rng.standard_normal(hn), min(6 * f, 3500), q=0.8) * np.exp(-np.arange(hn) / SR / 0.006)
    out[:hn] += pan(0.05 * vel * th, keypan)
    # damper
    damp = np.where(t < dur, 1.0, np.exp(-(t - dur) / (release * 0.25)) * np.clip(1 - (t - dur) / release, 0, 1))
    return out * damp[:, None] * vel ** 1.3


def pluck(m, dur, decay=0.3, bright=1.0, detune=6.0, even=1.0, attack=0.002):
    """Plucky lead: additive saw whose upper harmonics die faster (no harsh raw saw)."""
    f = hz(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    K = int(max(2, min(26, 11000 // f)))
    k = np.arange(1, K + 1)[:, None]
    amp = (1.0 / k) * np.where(k % 2 == 0, even, 1.0)
    env = np.exp(-t[None, :] * (1.0 / decay) * (1 + 0.6 * (k - 1) / bright))
    out = np.zeros((n, 2))
    for det, pp in ((-detune, -0.35), (detune, 0.35)):
        ph = TAU * f * 2 ** (det / 1200.0) * t[None, :] * k
        out += pan((amp * env * np.sin(ph)).sum(0), pp)
    out *= np.minimum(1.0, t / attack)[:, None]
    fade(out, 0.0, min(0.06, dur / 3))
    return out * 0.5


def bass_note(m, dur, bright=1.0):
    f = hz(m)
    r = 0.04
    n = int((dur + r) * SR)
    t = np.arange(n) / SR
    env = adsr(dur, 0.004, 0.18, 0.6, r, n=n)
    fc = 250 + 900 * bright * np.exp(-t / 0.07)
    K = int(max(2, min(14, 2500 // f)))
    y = 0.5 * np.sin(TAU * f * t)
    for k in range(1, K + 1):
        y += np.sin(TAU * k * f * t) / k / (1 + (k * f / fc) ** 2)
    return sat(y * env, 1.4)


def bass_sus(m, dur, a=0.08, r=0.4):
    f = hz(m)
    n = int((dur + r) * SR)
    t = np.arange(n) / SR
    y = np.sin(TAU * f * t) + 0.3 * np.sin(TAU * 2 * f * t + 0.5) + 0.12 * np.sin(TAU * 3 * f * t)
    return y * adsr(dur, a, 0.3, 0.9, r, n=n)


def epiano(m, dur, vel=0.7, release=0.3):
    """FM electric piano: sine carrier, decaying 1:1 modulator, small tine partial."""
    f = hz(m)
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    idx = 1.3 * vel * np.exp(-t / 0.3) + 0.22 * vel
    body = np.sin(TAU * f * t + idx * np.sin(TAU * f * t))
    tine = np.sin(TAU * f * t + 0.5 * np.exp(-t / 0.05) * np.sin(TAU * 14 * f * t)) * np.exp(-t / 0.2) * 0.22
    amp = np.exp(-t / (1.6 * (261.6 / f) ** 0.3)) * np.minimum(1, t / 0.003)
    damp = np.where(t < dur, 1.0, np.exp(-(t - dur) / (release * 0.25)) * np.clip(1 - (t - dur) / release, 0, 1))
    return (body + tine) * amp * damp * vel


def pad_note(m, dur, a=0.5, r=1.0, cutoff=1800.0, nvoices=5, spread=12.0, rng=None):
    rng = rng or np.random.default_rng(0)
    f = hz(m)
    n = int((dur + r) * SR)
    out = np.zeros((n, 2))
    for det, pp in zip(np.linspace(-spread, spread, nvoices), np.linspace(-0.8, 0.8, nvoices)):
        out += pan(saw(f * 2 ** (det / 1200.0), n, rng.uniform()), pp)
    out = lp(out, cutoff, q=0.7, passes=2)
    return out * adsr(dur, a, 0.3, 0.85, r, n=n)[:, None] / nvoices


def brass(m, dur, vel=0.8, a=0.035, r=0.12, bright=1.0, rng=None, detunes=(-7, 0, 7), vib=0.004):
    """Brass-like saw stack whose low-pass opens with the amplitude envelope."""
    rng = rng or np.random.default_rng(0)
    f = hz(m)
    n = int((dur + r) * SR)
    t = np.arange(n) / SR
    env = adsr(dur, a, 0.2, 0.82, r, n=n)
    fc = f * 1.2 + (900 + 4200 * bright * vel) * env ** 1.5
    vibr = 1 + vib * np.clip((t - 0.18) / 0.25, 0, 1) * np.sin(TAU * 5.6 * t + rng.uniform(0, TAU))
    K = int(min(48, max(4, min(fc.max() * 2.5, 14000) // f)))
    phs = [TAU * np.cumsum(f * 2 ** (det / 1200.0) * vibr) / SR + rng.uniform(0, TAU) for det in detunes]
    ys = [np.zeros(n) for _ in detunes]
    for k in range(1, K + 1):
        ampk = (1.0 / k) / np.sqrt(1 + (k * f / fc) ** 6)
        for y, ph in zip(ys, phs):
            y += np.sin(k * ph) * ampk
    out = np.zeros((n, 2))
    for y, pp in zip(ys, np.linspace(-0.5, 0.5, len(detunes))):
        out += pan(y, pp)
    return out * (env * vel / len(detunes))[:, None]


def bell(f, dur, tau=0.3, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, d in ((1, 1, 1), (2.0, 0.4 * bright, 0.7), (3.01, 0.18 * bright, 0.5), (4.1, 0.1 * bright, 0.35),
                    (5.43, 0.06 * bright, 0.25)):
        if f * r < 0.42 * SR:
            y += a * np.exp(-t / (tau * d)) * np.sin(TAU * f * r * t)
    y *= np.minimum(1, t / 0.0015)
    fade(y, 0.0, 0.01)
    return y


# ----------------------------------------------------------------- drums
def kick(rng, dur=0.32, f0=150.0, f1=47.0, tp=0.03, ta=0.13, click=0.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / tp)
    y = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-t / ta)
    c = hp(rng.standard_normal(n), 2000) * np.exp(-t / 0.003) * click * 0.3
    return fade(sat(y + c, 1.6), 0.0, 0.02)


def snare(rng, dur=0.22, tone=185.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(TAU * np.cumsum(tone * (1 + 0.3 * np.exp(-t / 0.02))) / SR) * np.exp(-t / 0.06)
    nz = lp(hp(rng.standard_normal(n), 1500), 8000) * np.exp(-t / 0.08)
    return fade(0.6 * body + 0.5 * nz, 0.0, 0.02)


def clap(rng, dur=0.3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    w = rng.standard_normal(n)
    w = hp(bp(w, 1300, q=1.4) + 0.4 * bp(w, 2600, q=1.2), 500)
    env = np.zeros(n)
    for d0 in (0.0, 0.011, 0.021):
        env += (t >= d0) * np.exp(-np.maximum(t - d0, 0) / 0.004)
    env += (t >= 0.03) * 0.7 * np.exp(-np.maximum(t - 0.03, 0) / 0.06)
    return fade(w * env, 0.0, 0.03)


def hat(rng, dur=0.06, tau=0.012, fc=7500.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    w = rng.standard_normal(n)
    y = hp(w, fc, q=0.8) + 0.5 * bp(w, 10500, q=2.0)
    return fade(y * np.exp(-t / tau) * np.minimum(1, t / 0.0005), 0.0, 0.01)


def crash(rng, dur=2.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = (1 - np.exp(-t / 0.002)) * (0.6 * np.exp(-t / 0.25) + 0.4 * np.exp(-t / 0.8))
    common = rng.standard_normal(n)
    out = np.zeros((n, 2))
    for c in range(2):
        w = 0.6 * common + 0.6 * rng.standard_normal(n)
        out[:, c] = (hp(w, 3500) + 0.6 * bp(w, 6200, q=1.5)) * env
    return fade(out, 0.0, 0.1)


def rim(rng, dur=0.06):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.sin(TAU * 1750 * t) * np.exp(-t / 0.006) + 0.6 * np.sin(TAU * 820 * t) * np.exp(-t / 0.009)
    y += 0.3 * hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.002)
    return fade(y, 0.0, 0.01)


def shaker(rng, dur=0.09, attack=0.012, tau=0.025):
    n = int(dur * SR)
    t = np.arange(n) / SR
    w = hp(rng.standard_normal(n), 5000)
    return fade(w * np.minimum(1, t / attack) * np.exp(-np.maximum(t - attack, 0) / tau), 0.0, 0.01)


def timpani(m, dur=1.6, vel=1.0, rng=None):
    rng = rng or np.random.default_rng(0)
    f = hz(m)
    n = int(dur * SR)
    t = np.arange(n) / SR
    glide = 1 + 0.025 * np.exp(-t / 0.05)
    ph = TAU * np.cumsum(f * glide) / SR
    y = np.zeros(n)
    for r, a, d in ((1, 1, 0.9), (1.5, 0.55, 0.6), (1.99, 0.4, 0.45), (2.44, 0.22, 0.3), (2.89, 0.12, 0.25)):
        y += a * np.sin(r * ph) * np.exp(-t / (d * 0.9))
    y += 0.8 * lp(rng.standard_normal(n), 500) * np.exp(-t / 0.018)
    return fade(sat(y * vel * 0.6, 1.3), 0.0, 0.05)


# ----------------------------------------------------------------- output
def normalize(x, peak_db):
    return x * (10 ** (peak_db / 20.0) / max(np.max(np.abs(x)), 1e-12))


def master_music(x, peak_db=-4.0, drive=1.2, fin=0.002, fout=0.05, lowcut=25.0, ref=None):
    """High-pass, soft saturation, peak normalise, edge fades. With `ref`, the 99.9th-percentile level is
    set to `ref` before the saturator, so only the rarest transients are rounded off."""
    x = hp(x, lowcut)
    if ref:
        x = x / np.percentile(np.abs(x), 99.9) * ref
    else:
        x = x / np.max(np.abs(x)) * 0.9
    x = sat(x, drive)
    x = normalize(x, peak_db)
    return fade(x, fin, fout)


def write_wav(path, x):
    assert x.ndim == 2 and x.shape[1] == 2
    assert np.max(np.abs(x)) < 1.0, 'would clip'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pcm = np.round(x * 32767.0).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
