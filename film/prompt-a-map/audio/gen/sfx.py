#!/usr/bin/env python3
"""The sound effects. Every function returns a stereo buffer; build.py trims, normalises and fades it."""
import numpy as np

from synth import *
from music import _brass_chord

OFF = 0.004          # lead-in so the fade-in never touches a transient


def R(seed):
    return np.random.default_rng(seed)


def ts(dur):
    n = int(round(dur * SR))
    return n, np.arange(n) / SR


def damped(f, tau, n, phase=0.0):
    t = np.arange(n) / SR
    return np.sin(TAU * f * t + phase) * np.exp(-t / tau)


def room(x, n, t60=0.3, mix=0.1, seed=31):
    return reverb(x, t60=t60, mix=mix, seed=seed, predelay=0.004)[:n]


# ------------------------------------------------------------ notifications
def ding():
    mx = Mix(0.9)
    mx.add(bell(hz('B5'), 0.8, tau=0.28), OFF, 0.9, -0.2)
    mx.add(bell(hz('E6'), 0.75, tau=0.32), OFF + 0.12, 1.0, 0.2)
    return room(mx.b, mx.n, 0.7, 0.12)


def ding_single():
    mx = Mix(0.8)
    mx.add(bell(hz('E6'), 0.78, tau=0.34), OFF, 1.0, 0.0)
    mx.add(bell(hz('E7'), 0.5, tau=0.12, bright=0.3), OFF, 0.15, 0.0)
    return room(mx.b, mx.n, 0.7, 0.12)


def error_beep():
    mx = Mix(0.5)
    for t0, f in ((OFF, 494.0), (OFF + 0.2, 370.0)):
        m = int(0.19 * SR)
        y = (0.6 * square(f, m) + 0.5 * sine(f, m)) * adsr(0.15, 0.005, 0.05, 0.85, 0.035, n=m)
        mx.add(lp(y, 2600), t0, 1.0, 0.0)
    return room(mx.b, mx.n, 0.25, 0.06)


def buzzer_wrong():
    n, t = ts(0.8)
    y = saw(110.0, n) + saw(112.6, n, 0.3) + 0.6 * square(55.0, n, 0.4)
    y = lp(y, 2200, q=0.9) * (1 + 0.15 * np.sin(TAU * 31 * t))
    y = sat(y * 0.5, 2.0) * adsr(0.7, 0.006, 0.05, 0.95, 0.06, n=n)
    return room(pan(y, 0.0), n, 0.3, 0.12)


def counter_tick():
    rng = R(41)
    n, t = ts(0.08)
    m = n - int(OFF * SR)
    y = np.zeros(n)
    c = damped(2000, 0.008, m) + 0.5 * damped(620, 0.006, m) + 0.4 * hp(rng.standard_normal(m), 3000) * np.exp(
        -np.arange(m) / SR / 0.001)
    y[n - m:] = c
    return pan(y, 0.0)


def counter_roll():
    rng = R(42)
    mx = Mix(3.0)
    t0, k = OFF, 0
    end = 2.36
    while t0 < end:
        u = t0 / end
        m = int(0.06 * SR)
        f = 900 * (2600 / 900) ** u
        c = damped(f, 0.009, m) + 0.4 * damped(f * 0.31, 0.006, m) + 0.3 * hp(rng.standard_normal(m), 3000) * np.exp(
            -np.arange(m) / SR / 0.001)
        mx.add(c, t0, 0.35 + 0.5 * u, 0.25 * (-1) ** k)
        t0 += 0.115 * (0.03 / 0.115) ** u
        k += 1
    mx.add(bell(hz('E6'), 0.6, tau=0.3), 2.42, 1.0, -0.15)
    mx.add(bell(hz('B6'), 0.6, tau=0.25), 2.42, 0.55, 0.15)
    return room(mx.b, mx.n, 0.6, 0.1)


# ------------------------------------------------------------------- impacts
def stamp():
    rng = R(51)
    n, t = ts(0.7)
    m = n - int(OFF * SR)
    tt = np.arange(m) / SR
    boom = np.sin(TAU * np.cumsum(45 + 60 * np.exp(-tt / 0.03)) / SR) * np.exp(-tt / 0.16)
    w = rng.standard_normal(m)
    thwack = lp(bp(w, 520, q=0.8), 2500) * np.exp(-tt / 0.022)
    click = hp(w, 2500) * np.exp(-tt / 0.003) * 0.25
    squish = bp(rng.standard_normal(m), 1300, q=1.2) * np.minimum(1, tt / 0.006) * np.exp(-tt / 0.035) * 0.25
    y = np.zeros(n)
    y[n - m:] = sat(0.7 * boom + 4.5 * thwack + 1.5 * click + 4.0 * squish, 1.6)
    return room(pan(y, 0.0), n, 0.35, 0.12)


def thud():
    rng = R(52)
    n, t = ts(0.5)

    def hit(m):
        tt = np.arange(m) / SR
        body = np.sin(TAU * np.cumsum(50 + 75 * np.exp(-tt / 0.02)) / SR) * np.exp(-tt / 0.09)
        w = rng.standard_normal(m)
        return 0.8 * body + 3.5 * lp(w, 380) * np.exp(-tt / 0.05) + 2.5 * bp(w, 700, q=0.8) * np.exp(-tt / 0.018)

    y = np.zeros(n)
    i = int(OFF * SR)
    y[i:] += hit(n - i)
    j = int(0.14 * SR)
    y[j:] += 0.3 * hit(n - j)
    return room(pan(sat(y, 1.4), 0.0), n, 0.3, 0.08)


def clang():
    rng = R(53)
    n, t = ts(1.2)
    out = np.zeros((n, 2))
    f0 = 523.0
    for r in (1, 1.58, 2.24, 2.76, 3.52, 4.31, 5.40, 6.87, 8.93):
        a = rng.uniform(0.4, 1.0) / r ** 0.5
        tau = 0.55 / r ** 0.6
        y = a * (damped(f0 * r, tau, n) + 0.6 * damped(f0 * r * 1.004, tau * 0.8, n, rng.uniform(0, TAU)))
        out += pan(y, rng.uniform(-0.6, 0.6))
    out += pan(hp(rng.standard_normal(n), 2000) * np.exp(-t / 0.004) * 1.5, 0.0)
    out[:int(OFF * SR)] = 0
    return room(sat(out * 0.4, 1.5), n, 0.9, 0.15)


def explosion_small():
    rng = R(54)
    n, t = ts(1.4)
    out = np.zeros((n, 2))
    boom = np.sin(TAU * np.cumsum(32 + 55 * np.exp(-t / 0.06)) / SR) * np.exp(-t / 0.3)
    for c in range(2):
        nz = svf(rng.standard_normal(n), 250 + 7000 * np.exp(-t / 0.28), 0.8, 'lp')
        nz *= (1 - np.exp(-t / 0.003)) * np.exp(-t / 0.33)
        cr = np.zeros(n)
        idx = rng.integers(0, n, 60)
        cr[idx] = rng.normal(0, 1, 60) * np.exp(-idx / SR / 0.45)
        cr = bp(cr, 2200, q=1.0) * 3
        out[:, c] = sat(0.8 * boom + 1.2 * nz + cr, 3.0)
    out = np.roll(out, int(OFF * SR), axis=0)
    out[:int(OFF * SR)] = 0
    return room(out, n, 1.0, 0.2)


def _break(seed, tone, thunk_f, thunk_g, ngrains, grain_q, tau):
    rng = R(seed)
    n, t = ts(0.35)
    out = np.zeros((n, 2))
    for c in range(3):                      # centre, then a little extra per side
        train = np.zeros(n)
        times = np.clip((rng.exponential(tau, ngrains) * SR).astype(int), 0, n - 1)
        np.add.at(train, times, rng.normal(0, 1, ngrains) * np.exp(-times / SR / (tau * 1.5)))
        y = np.zeros(n)
        for j in range(3):
            m = int(0.02 * SR)
            tt = np.arange(m) / SR
            ker = bp(rng.standard_normal(m), tone * rng.uniform(0.6, 1.6), q=grain_q) * np.exp(-tt / rng.uniform(0.002, 0.006))
            ker /= np.max(np.abs(ker))
            sub = train * (rng.uniform(0, 1, n) < 0.5)
            y += fftconv(sub, ker)[:n]
        if c == 0:
            out += pan(y, 0.0)
        else:
            out[:, c - 1] += 0.45 * y
    mono = bp(rng.standard_normal(n), tone, q=0.7) * np.exp(-t / 0.006) * 2.5
    mono += thunk_g * 0.9 * np.sin(TAU * np.cumsum(thunk_f * (0.7 + 0.5 * np.exp(-t / 0.02))) / SR) * np.exp(-t / 0.04)
    out += pan(mono, 0.0)
    out = np.roll(out, int(OFF * SR), axis=0)
    out[:int(OFF * SR)] = 0
    return room(sat(out * 0.25, 1.6), n, 0.25, 0.08)


def block_break_1():
    return _break(61, 1900, 95, 0.5, 45, 2.5, 0.06)      # stony


def block_break_2():
    return _break(62, 750, 150, 1.0, 30, 3.5, 0.05)       # woody


def block_break_3():
    return _break(63, 3200, 80, 0.3, 90, 1.5, 0.08)       # gravelly


def block_place():
    rng = R(64)
    n, t = ts(0.18)
    m = n - int(OFF * SR)
    tt = np.arange(m) / SR
    y = np.zeros(n)
    c = np.sin(TAU * np.cumsum(210 + 270 * np.exp(-tt / 0.012)) / SR) * np.exp(-tt / 0.03)
    c += 0.3 * bp(rng.standard_normal(m), 1500, q=1.2) * np.exp(-tt / 0.006)
    y[n - m:] = c
    return room(pan(y, 0.0), n, 0.2, 0.06)


def pop():
    n, t = ts(0.15)
    m = n - int(OFF * SR)
    tt = np.arange(m) / SR
    y = np.zeros(n)
    f = 380 + 800 * (1 - np.exp(-tt / 0.012))
    y[n - m:] = np.sin(TAU * np.cumsum(f) / SR) * np.exp(-tt / 0.018) * np.minimum(1, tt / 0.001)
    return room(pan(y, 0.0), n, 0.2, 0.05)


# ------------------------------------------------------------------ movement
def _whoosh(dur, f_lo, f_hi, seed):
    rng = R(seed)
    n, t = ts(dur)
    u = t / dur
    shape = np.sin(np.pi * u ** 1.3)
    fc = f_lo * (f_hi / f_lo) ** shape
    amp = shape ** 2
    y = hp(svf(rng.standard_normal(n), fc, 1.7, 'lp'), 160)
    z = hp(svf(rng.standard_normal(n), fc * 0.8, 1.3, 'lp'), 160)
    th = (-0.8 + 1.6 * u + 1) * np.pi / 4
    out = np.stack([y * np.cos(th) + 0.3 * z, y * np.sin(th) - 0.3 * z], 1) * amp[:, None]
    return out


def whoosh_short():
    return _whoosh(0.35, 300, 3600, 71)


def whoosh_long():
    return _whoosh(1.2, 220, 3000, 72)


def _thwip(seed, pitch=1.0):
    rng = R(seed)
    n, t = ts(0.22)
    sweep = 0.11
    u = np.clip(t / sweep, 0, 1)
    live = t < sweep
    hump = np.where(live, u ** 1.2 * (1 - u) ** 0.25, 0.0) * (1 + 0.3 * np.sin(TAU * 95 * t))
    fc = 550 * pitch * 7 ** u
    y = svf(rng.standard_normal(n), fc, 2.5, 'bp') * hump * 1.6
    y += 0.25 * np.sin(TAU * np.cumsum(500 * pitch * 5 ** u) / SR) * hump
    i = int(sweep * SR)
    m = n - i
    tt = np.arange(m) / SR
    y[i:] += 0.5 * hp(rng.standard_normal(m), 4000) * np.exp(-tt / 0.003) + 0.35 * damped(3200 * pitch, 0.006, m)
    return y


def card_thwip():
    n = int(0.25 * SR)
    mx = Mix(0.25)
    mx.add(_thwip(81), OFF, 1.0, 0.0)
    return room(mx.b, n, 0.2, 0.06)


def card_burst():
    rng = R(82)
    mx = Mix(3.0)
    t0 = OFF
    iv = 0.22
    ratio = (0.04 / 0.22) ** (1 / 23.0)
    for k in range(25):
        mx.add(_thwip(820 + k, 0.9 + 0.45 * k / 24 + rng.uniform(-0.05, 0.05)), t0, rng.uniform(0.75, 1.0),
               rng.uniform(-0.6, 0.6))
        t0 += iv
        iv *= ratio
    return room(mx.b, mx.n, 0.25, 0.07)


def fall_whistle():
    rng = R(73)
    n, t = ts(2.0)
    u = np.clip(t / 1.9, 0, 1)
    f = 2600 * (330 / 2600) ** (u ** 0.85) * (1 + 0.015 * u * np.sin(TAU * 6.2 * t))
    ph = TAU * np.cumsum(f) / SR
    y = np.sin(ph) + 0.1 * np.sin(2 * ph) + 0.04 * np.sin(3 * ph)
    y += 0.18 * svf(rng.standard_normal(n), f, 8.0, 'bp')
    amp = np.minimum(1, t / 0.03) * np.clip((1.95 - t) / 0.5, 0, 1) ** 1.5
    th = (0.5 - 1.0 * u + 1) * np.pi / 4
    out = np.stack([y * np.cos(th), y * np.sin(th)], 1) * amp[:, None]
    return echo(out, 0.09, fb=0.3, mix=0.18)[:n]


def splat_void():
    n, t = ts(1.4)
    m = int(0.6 * SR)
    tt = np.arange(m) / SR
    f = 70 + (330 + 110 * np.exp(-((tt - 0.05) / 0.03) ** 2)) * np.exp(-tt / 0.17)
    ph = TAU * np.cumsum(f) / SR
    y = np.sin(ph + 0.6 * np.sin(ph)) * np.minimum(1, tt / 0.015) * np.clip((0.58 - tt) / 0.25, 0, 1) ** 1.3
    mx = Mix(1.4)
    mx.add(lp(y, 2500), OFF, 1.0, 0.0)
    out = echo(mx.b, 0.13, fb=0.35, mix=0.25, pingpong=True, damp=1500)[:n]
    out = reverb(out, t60=0.9, mix=0.22, damp=2000, seed=33)[:n]
    out *= np.clip((1.15 - t) / 0.5, 0, 1)[:, None]
    return out


def record_scratch():
    rng = R(74)
    n, t = ts(0.6)
    L = 3 * SR
    st = np.arange(L) / SR
    src = sum(saw(f, L, rng.uniform()) for f in (196.0, 247.0, 294.0, 392.0)) * (0.6 + 0.4 * np.sin(TAU * 7 * st))
    src = lp(src, 3000) * 0.3 + bp(rng.standard_normal(L), 2500, q=0.6) * 0.5
    smooth = lambda x: np.clip(x, 0, 1) ** 2 * (3 - 2 * np.clip(x, 0, 1))
    pos = 1.0 + 0.5 * smooth(t / 0.07) - 0.42 * smooth((t - 0.1) / 0.09) + 0.55 * smooth((t - 0.23) / 0.2)
    speed = np.abs(np.gradient(pos) * SR)
    y = np.interp(pos * SR, np.arange(L), src) * np.minimum(1, speed / 2.5) ** 0.8
    y = hp(lp(y, 7000), 250)
    return room(pan(y, 0.0), n, 0.25, 0.1)


def power_down():
    n, t = ts(1.5)
    f = 420 * np.exp(-3.2 * t / 1.4)
    y = saw(f, n) + saw(f * 1.01, n, 0.4) + 1.2 * sine(f, n)
    y = svf(y, 6 * f + 90, 0.9, 'lp')
    trem = 1 - 0.35 * (0.5 + 0.5 * np.sin(TAU * np.cumsum(f / 18) / SR))
    amp = np.minimum(1, t / 0.01) * np.clip((1.46 - t) / 0.7, 0, 1) ** 1.2
    y = sat(y * 0.5, 1.5) * trem * amp
    return room(pan(y, 0.0), n, 0.4, 0.12)


def fast_forward():
    rng = R(75)
    n, t = ts(2.0)
    u = t / 2.0
    spin = np.minimum(1, 0.35 + 0.65 * t / 0.15) * np.minimum(1, 0.3 + 0.7 * (2.0 - t) / 0.2)
    step = 0.022
    ns = int(2.0 / step) + 2
    scale = np.array([0, 2, 4, 7, 9, 12, 14, 16, 19])
    semis = scale[rng.integers(0, len(scale), ns)]
    f = 950 * 2 ** (np.interp(t, np.arange(ns) * step, semis.astype(float)) / 12) * (1 + 0.4 * u) * spin
    gate = np.interp(t, np.arange(ns) * step, (rng.uniform(0, 1, ns) < 0.72).astype(float))
    src = saw(f, n) * 0.6 + sine(f, n) * 0.6
    y = (bp(src, 1900, q=1.2) + 0.7 * bp(src, 3400, q=1.5) + 0.3 * src) * (0.15 + 0.85 * gate)
    y *= 1 + 0.2 * np.sin(TAU * 38 * t)
    whirr = bp(rng.standard_normal(n), 650, q=1.0) * (0.6 + 0.4 * np.sin(TAU * 41 * t * spin)) * 0.12
    hiss = hp(rng.standard_normal(n), 5000) * 0.03
    y = lp(y, 6500) + whirr + hiss
    return room(pan(y, 0.0), n, 0.25, 0.1)


# --------------------------------------------------------------------- keys
def _key(seed, heavy=False):
    rng = R(seed)
    n, t = ts(0.3 if heavy else 0.14)
    y = np.zeros(n)

    def click(t0, amp, bodyf, bodytau, resf):
        i = int(t0 * SR)
        m = n - i
        tt = np.arange(m) / SR
        c = hp(rng.standard_normal(m), 2500) * np.exp(-tt / 0.0012) * 0.5
        for f in resf:
            c += 0.22 * np.sin(TAU * f * tt) * np.exp(-tt / rng.uniform(0.003, 0.007))
        c += 0.8 * np.sin(TAU * bodyf * tt) * np.exp(-tt / bodytau)
        c += 0.3 * bp(rng.standard_normal(m), 900, q=1.0) * np.exp(-tt / 0.008)
        y[i:] += amp * c

    if heavy:
        click(OFF, 1.0, rng.uniform(150, 175), 0.022, rng.uniform(1500, 3500, 3))
        click(OFF + 0.15, 0.4, rng.uniform(230, 280), 0.015, rng.uniform(2500, 5000, 2))
        i = int(OFF * SR)
        y[i:] += 0.06 * damped(2100, 0.06, n - i) + 0.04 * damped(3150, 0.04, n - i)
    else:
        click(OFF, 1.0, rng.uniform(190, 320), rng.uniform(0.012, 0.02), rng.uniform(1800, 4500, 3))
        click(OFF + rng.uniform(0.065, 0.09), 0.33, rng.uniform(300, 420), 0.008, rng.uniform(3000, 5500, 2))
    return y


def _key_file(seed, heavy=False, p=0.0):
    y = _key(seed, heavy)
    return room(pan(y, p), len(y), 0.15, 0.07, seed=30 + seed % 5)


def key_1(): return _key_file(91, p=-0.1)
def key_2(): return _key_file(92, p=0.1)
def key_3(): return _key_file(93, p=-0.05)
def key_4(): return _key_file(94, p=0.05)
def key_5(): return _key_file(95, p=0.0)
def enter_key(): return _key_file(96, heavy=True)


def typing_run():
    rng = R(97)
    mx = Mix(4.0)
    keys = [_key(900 + i) for i in range(9)]
    space = _key(950, heavy=True)[:int(0.2 * SR)]
    t0 = OFF
    count = 0
    while t0 < 3.82:
        if rng.uniform() < 0.12:
            mx.add(space, t0, 0.7, 0.0)
        else:
            mx.add(keys[rng.integers(len(keys))], t0, rng.uniform(0.6, 1.0), rng.uniform(-0.45, 0.45))
        count += 1
        gap = rng.lognormal(np.log(0.105), 0.35)
        if rng.uniform() < 0.09:
            gap += rng.uniform(0.2, 0.4)          # a thinking pause
        t0 += min(max(gap, 0.055), 0.6)
    return room(mx.b, mx.n, 0.15, 0.07)


# ------------------------------------------------------------------- brass
def sad_trombone():
    rng = R(101)
    mx = Mix(2.6)
    notes = [('F4', 0.34, 0.0), ('D4', 0.34, 0.0), ('B3', 0.34, 0.0), ('G#3', 1.1, -2.5)]
    t0 = OFF
    for nm, ln, fall in notes:
        m = int((ln + 0.08) * SR)
        tt = np.arange(m) / SR
        u = tt / ln
        long = ln > 0.5
        semis = -0.5 * np.exp(-tt / 0.03) + fall * np.clip(u - 0.25, 0, 1) ** 1.6
        vib = (0.012 * np.clip(u, 0, 1) * np.sin(TAU * 5.3 * tt)) if long else 0.0
        f = hz(nm) * 2 ** (semis / 12) * (1 + vib)
        ph = TAU * np.cumsum(f) / SR
        fmt = 420 + 760 * np.sin(np.pi * np.clip(u / (0.75 if long else 1.0), 0, 1)) ** (0.7 if not long else 0.5)
        if long:
            fmt = fmt * (1 - 0.45 * np.clip(u - 0.3, 0, 1))
        y = np.zeros(m)
        K = int(4500 // hz(nm))
        for k in range(1, K + 1):
            fk = k * f
            w = (1.0 / k ** 0.8) * (0.18 + np.exp(-0.5 * ((fk - fmt) / (0.45 * fmt + 120)) ** 2)) / (1 + (fk / 3200) ** 4)
            y += w * np.sin(k * ph)
        if long:
            env = np.minimum(1, tt / 0.05) * np.clip((ln + 0.07 - tt) / 0.75, 0, 1)
        else:
            env = np.sin(np.pi * np.clip(tt / ln, 0, 1)) ** 0.55          # each short note swells and closes: 'wah'
        mx.add(y * env, t0, 1.0, 0.0)
        t0 += ln + 0.07
    out = sat(mx.b * 0.6, 1.4)
    return room(out, mx.n, 0.6, 0.12)


def tada():
    rng = R(102)
    mx = Mix(1.5)
    mx.add(_brass_chord(['A4', 'D5', 'F#5'], 0.08, 0.9, rng), OFF, 0.8)
    t1 = OFF + 0.17
    mx.add(_brass_chord(['D4', 'A4', 'D5', 'F#5', 'A5'], 0.75, 1.0, rng, bright=1.1), t1, 1.0)
    mx.add(timpani(nn('D3'), 1.1, 0.8, rng), t1, 0.5)
    mx.add(crash(rng, dur=1.2), t1, 0.3)
    return reverb(mx.b, t60=1.0, mix=0.16, seed=5)[:mx.n]


# ------------------------------------------------------------------- crowds
def _voices(dur, nv, frange, contour, seed, on_spread=0.4, minlen=0.6, rough=0.5):
    rng = R(seed)
    n = int(dur * SR)
    out = np.zeros((n, 2))
    for _ in range(nv):
        f0 = np.exp(rng.uniform(np.log(frange[0]), np.log(frange[1])))
        on = rng.uniform(0, on_spread)
        ln = rng.uniform(min(minlen, dur - on - 0.05), dur - on)
        m = int(ln * SR)
        tt = np.arange(m) / SR
        u = tt / ln
        kn = int(ln * 14) + 2
        jit = np.interp(tt, np.linspace(0, ln, kn), rng.normal(0, 0.012, kn))
        vib = rng.uniform(0.004, 0.02) * np.sin(TAU * rng.uniform(4.5, 7) * tt + rng.uniform(0, TAU))
        f = f0 * 2 ** (contour(u, rng) / 12) * (1 + vib + jit)
        y = saw(f, m, rng.uniform())
        kr = int(ln * 60) + 2
        y *= 1 + rough * np.interp(tt, np.linspace(0, ln, kr), rng.normal(0, 1, kr))
        a, r = rng.uniform(0.05, 0.25), rng.uniform(0.25, 0.6)
        env = np.minimum(1, tt / a) * np.minimum(1, (ln - tt) / r)
        i = int(on * SR)
        out[i:i + m] += pan(y * env * rng.uniform(0.5, 1.0), rng.uniform(-0.9, 0.9))
    return out


def _formants(x, fs):
    return sum(g * bp(x, f, q=q) for f, q, g in fs)


def _applause(dur, rate_fn, seed, nk=10):
    rng = R(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    cdf = np.cumsum(rate_fn(t)) / SR
    total = cdf[-1]
    out = np.zeros((n, 2))
    for _ in range(nk):
        N = rng.poisson(total / nk)
        times = np.clip(np.searchsorted(cdf, rng.uniform(0, total, N)), 0, n - 1)
        amps = rng.lognormal(0, 0.5, N)
        th = (rng.uniform(-1, 1, N) + 1) * np.pi / 4
        tl, tr = np.zeros(n), np.zeros(n)
        np.add.at(tl, times, amps * np.cos(th))
        np.add.at(tr, times, amps * np.sin(th))
        m = int(0.03 * SR)
        tt = np.arange(m) / SR
        ker = bp(rng.standard_normal(m), rng.uniform(900, 2800), q=rng.uniform(1.0, 2.5))
        ker *= np.exp(-tt / 0.0025) + 0.25 * np.exp(-tt / 0.01)
        ker /= np.sqrt(np.sum(ker * ker))
        out[:, 0] += fftconv(tl, ker)[:n]
        out[:, 1] += fftconv(tr, ker)[:n]
    return out


def applause():
    n, t = ts(4.0)
    rate = lambda t: 420 * np.minimum(1, (t + 0.03) / 0.35) * np.clip((4.05 - t) / 1.6, 0, 1) ** 2.2
    out = _applause(4.0, rate, 111)
    # a few near, steady clappers
    rng = R(112)
    m = int(0.03 * SR)
    tt = np.arange(m) / SR
    for _ in range(6):
        ker = bp(rng.standard_normal(m), rng.uniform(1000, 2200), q=1.5) * np.exp(-tt / 0.003)
        ker /= np.sqrt(np.sum(ker * ker))
        per = rng.uniform(0.2, 0.3)
        t0 = rng.uniform(0.05, 0.4)
        stop = rng.uniform(2.6, 3.7)
        p = rng.uniform(-0.8, 0.8)
        mx = Mix(4.0)
        while t0 < stop:
            mx.add(ker, t0, rng.uniform(1.5, 2.5), p)
            t0 += per * rng.uniform(0.92, 1.08)
        out += mx.b
    out = hp(out, 300)
    out = sat(out / np.sqrt(np.mean(out * out)) * 0.22, 1.5)
    return reverb(out, t60=0.9, mix=0.2, seed=35)[:n]


def crowd_cheer():
    n, t = ts(3.0)
    rng = R(121)
    up = lambda u, rng: rng.uniform(1, 5) * np.sin(np.pi * np.clip(u * 1.4, 0, 1)) - 2 * u
    woo = lambda u, rng: rng.uniform(4, 9) * np.minimum(1, u * 3) - 3 * np.clip(u - 0.5, 0, 1)
    a = _formants(_voices(3.0, 34, (180, 420), up, 122), [(800, 4, 1.0), (1250, 5, 0.8), (2700, 5, 0.45)])
    e = _formants(_voices(3.0, 22, (220, 480), up, 123), [(520, 4, 1.0), (1900, 6, 0.7), (2600, 5, 0.4)])
    w = _formants(_voices(3.0, 14, (420, 800), woo, 124, minlen=0.5, rough=0.25), [(420, 3, 1.0), (850, 4, 0.7), (2400, 4, 0.2)])
    bed = np.zeros((n, 2))
    for c in range(2):
        nz = rng.standard_normal(n)
        kn = 3 * 30 + 2
        wob = 1 + 0.35 * np.interp(t, np.linspace(0, 3, kn), rng.normal(0, 1, kn))
        bed[:, c] = (bp(nz, 900, q=1.2) + 0.8 * bp(nz, 1500, q=1.5) + 0.5 * bp(nz, 2800, q=2.0)) * wob
    whistles = Mix(3.0)
    for _ in range(4):
        m = int(rng.uniform(0.3, 0.55) * SR)
        tt = np.arange(m) / m
        f = rng.uniform(2000, 2600) * 2 ** (rng.uniform(2, 6) * tt / 12) * (1 + 0.012 * np.sin(TAU * 9 * tt * m / SR))
        y = sine(f, m) * np.sin(np.pi * tt) ** 0.7
        whistles.add(y, rng.uniform(0.2, 2.0), 0.035, rng.uniform(-0.8, 0.8))
    swell = np.minimum(1, (t + 0.02) / 0.22) ** 0.7 * (0.55 + 0.45 * np.exp(-t / 1.6)) * np.clip((3.02 - t) / 0.9, 0, 1) ** 1.4
    claps = _applause(3.0, lambda t: 260 * np.minimum(1, (t + 0.05) / 0.5) * np.clip((3.05 - t) / 1.2, 0, 1) ** 2, 125)
    rms = lambda x: np.sqrt(np.mean(x * x))
    voices = a / rms(a) + 0.8 * e / rms(e) + 0.55 * w / rms(w)
    out = (voices / rms(voices) + 0.75 * bed / rms(bed)) * swell[:, None] + 0.45 * claps / rms(claps)
    out = lp(hp(out, 180), 6500) / rms(out) * 0.1 + whistles.b * swell[:, None]
    return reverb(out, t60=1.1, mix=0.22, seed=35)[:n]


def crowd_aww():
    n, t = ts(2.0)
    rng = R(131)
    down = lambda u, rng: 1.5 * np.sin(np.pi * np.clip(u * 3, 0, 0.5)) - rng.uniform(3, 6) * np.clip(u - 0.12, 0, 1) ** 0.8
    v = _voices(2.0, 44, (140, 370), down, 132, on_spread=0.18, minlen=1.3, rough=0.25)
    aw = _formants(v, [(620, 4, 1.0), (980, 5, 0.8), (2500, 5, 0.25)])
    oh = _formants(v, [(430, 4, 1.0), (800, 5, 0.6), (2300, 5, 0.12)])
    x = np.clip(t / 1.4, 0, 1)[:, None]
    voices = aw * (1 - x) + oh * x
    bed = np.zeros((n, 2))
    for c in range(2):
        nz = rng.standard_normal(n)
        bed[:, c] = bp(nz, 600, q=1.2) + 0.6 * bp(nz, 1000, q=1.5)
    rms = lambda x: np.sqrt(np.mean(x * x))
    swell = np.minimum(1, (t + 0.02) / 0.25) * np.clip((2.02 - t) / 1.5, 0, 1) ** 1.3
    out = (voices / rms(voices) + 0.35 * bed / rms(bed)) * swell[:, None]
    out = lp(hp(out, 150), 4000)
    return reverb(out, t60=1.0, mix=0.2, seed=35)[:n]


# ---------------------------------------------------------------- ambiences
def crickets():
    rng = R(141)
    n, t = ts(4.0)
    out = np.zeros((n, 2))

    def cricket(f, npulse, pulse, gap, period, start, p, g):
        y = np.zeros(n)
        t0 = start
        while t0 < 4.0 - npulse * (pulse + gap):
            for k in range(npulse):
                i = int((t0 + k * (pulse + gap)) * SR)
                m = int(pulse * SR)
                tt = np.arange(m) / SR
                ff = f * (1 + 0.01 * rng.normal())
                y[i:i + m] += np.sin(TAU * ff * tt) * np.sin(np.pi * tt / pulse) ** 2 * (0.7 + 0.3 * k / npulse)
            t0 += period * rng.uniform(0.96, 1.04)
        return pan(y * g, p)

    out += cricket(4300, 3, 0.014, 0.009, 0.52, 0.05, -0.5, 1.0)
    out += cricket(4750, 4, 0.012, 0.008, 0.66, 0.21, 0.55, 0.7)
    out += cricket(3900, 3, 0.016, 0.010, 0.81, 0.38, 0.1, 0.4)
    trill = np.sin(TAU * 3150 * t) * (0.5 + 0.5 * np.sin(TAU * 46 * t)) ** 2 * (0.7 + 0.3 * np.sin(TAU * 0.25 * t))
    out += pan(trill * 0.07, -0.2)
    for c in range(2):
        out[:, c] += lp(rng.standard_normal(n), 700) * 0.012
    return reverb(out, t60=0.5, mix=0.08, seed=37)[:n]


def clock_tick():
    rng = R(151)
    mx = Mix(6.0)
    for k in range(12):
        tock = k % 2 == 1
        m = int(0.08 * SR)
        tt = np.arange(m) / SR
        fa, fb, fbody = (1700, 2900, 480) if tock else (2400, 3900, 700)
        y = damped(fa, 0.006, m) + 0.6 * damped(fb, 0.004, m) + 0.7 * damped(fbody, 0.011, m)
        y += 0.4 * hp(rng.standard_normal(m), 3000) * np.exp(-tt / 0.001)
        mx.add(y, 0.02 + 0.5 * k, 0.85 if tock else 1.0, -0.12 if tock else 0.12)
    return room(mx.b, mx.n, 0.3, 0.1)


def tv_static():
    rng = R(161)
    n, t = ts(1.0)
    common = rng.standard_normal(n)
    out = np.zeros((n, 2))
    kn = 42
    wob = 1 + 0.15 * np.interp(t, np.linspace(0, 1, kn), rng.normal(0, 1, kn))
    for c in range(2):
        w = 0.6 * common + 0.8 * rng.standard_normal(n)
        w = filt(hp(w, 150), 'hishelf', 4500, 0.7, -9.0)
        pops = np.zeros(n)
        idx = rng.integers(0, n, 25)
        pops[idx] = rng.normal(0, 4, 25)
        out[:, c] = (w + lp(pops, 4000)) * wob * (1 + 0.1 * np.sin(TAU * 50 * t))
    return out


def glitch():
    rng = R(171)
    n, t = ts(0.6)
    out = np.zeros((n, 2))
    i = int(OFF * SR)
    prev = None
    while i < n - int(0.05 * SR):
        m = min(int(rng.uniform(0.012, 0.06) * SR), n - int(0.035 * SR) - i)
        kind = rng.choice(['noise', 'tone', 'stutter', 'gap'], p=[0.35, 0.3, 0.25, 0.1])
        seg = np.zeros((m, 2))
        if kind == 'noise':
            hold = int(SR / rng.uniform(2500, 9000))
            for c in range(2):
                w = np.repeat(rng.uniform(-1, 1, m // hold + 1), hold)[:m]
                seg[:, c] = np.round(w * 4) / 4
        elif kind == 'tone':
            f = rng.choice([220, 311, 440, 622, 880, 1245, 1760, 2489])
            hold = int(SR / rng.uniform(4000, 12000))
            w = np.sign(np.sin(TAU * f * np.arange(m) / SR)) * 0.7
            w = np.repeat(w[::hold], hold)[:m]
            seg[:, 0] = w
            seg[:, 1] = w * rng.uniform(0.3, 1.0)
        elif kind == 'stutter' and prev is not None:
            chunk = prev[:max(64, int(rng.uniform(0.003, 0.009) * SR))]
            reps = m // len(chunk) + 1
            seg = np.tile(chunk, (reps, 1))[:m]
        if kind != 'gap':
            fade(seg, 0.0005, 0.0005)
            prev = seg
        out[i:i + m] = seg * rng.uniform(0.6, 1.0)
        i += m
    return lp(out, 9000)


def heartbeat():
    rng = R(181)
    mx = Mix(3.0)

    def beat(f0, f1, tau, g):
        m = int(0.3 * SR)
        tt = np.arange(m) / SR
        ph = TAU * np.cumsum(f1 + (f0 - f1) * np.exp(-tt / 0.03)) / SR
        y = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph) + 0.2 * np.sin(4 * ph)) * np.exp(-tt / tau) * np.minimum(1, tt / 0.004)
        y += 2.0 * bp(rng.standard_normal(m), 190, q=1.5) * np.exp(-tt / 0.03)
        return fade(sat(y * g, 2.0), 0.0, 0.03)

    for k in range(4):
        t0 = 0.12 + 0.8 * k
        mx.add(beat(95, 52, 0.07, 1.0), t0, 1.0, -0.05)
        mx.add(beat(115, 66, 0.05, 0.8), t0 + 0.27, 0.75, 0.05)
    return lp(mx.b, 1200)


def robot_hum():
    """Exactly periodic over 6 s: every partial and LFO is a multiple of 1/6 Hz, the noise is filtered circularly."""
    rng = R(191)
    n, t = ts(6.0)
    pulse = 0.62 - 0.38 * np.cos(TAU * 0.5 * t)            # minimum at the loop point
    out = np.zeros((n, 2))
    amps = [0.7, 0.7, 0.6, 0.4, 0.42, 0.25, 0.2, 0.15, 0.12, 0.1]
    ph = rng.uniform(0, TAU, (len(amps), 2))
    for c in range(2):
        y = np.zeros(n)
        for k, a in enumerate(amps, 1):
            wide = 0.0 if k <= 3 else 0.9 * c          # only the upper partials differ between channels
            y += a * np.sin(TAU * 54 * k * t + ph[k - 1, 0] + wide)
            y += 0.3 * a * np.sin(TAU * (54 * k + 1 / 6) * t + ph[k - 1, 1] - wide)
        whine = 0.09 * np.sin(TAU * 1188 * t + c) + 0.07 * np.sin(TAU * 1188.5 * t) + 0.03 * np.sin(TAU * 2376 * t + c)
        nz = rng.standard_normal(n)
        fan = bp(nz, 420, q=0.7, circular=True) + 0.5 * bp(nz, 1100, q=1.0, circular=True)
        out[:, c] = y * (0.75 + 0.25 * pulse) + whine * pulse + 0.6 * fan * (0.6 + 0.4 * pulse)
    return sat(out * 0.3, 1.3)


# ------------------------------------------------------------- celebration
def sparkle():
    rng = R(201)
    mx = Mix(1.2)
    scale = ['D6', 'E6', 'F#6', 'A6', 'B6', 'D7', 'E7', 'F#7', 'A7', 'B7', 'D8']
    order = [0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 8, 7, 9, 10]
    names = [scale[i] for i in order]
    for k, nm in enumerate(names):
        mx.add(bell(hz(nm), 0.5, tau=0.16, bright=0.6), OFF + k * 0.045 + rng.uniform(0, 0.008), rng.uniform(0.6, 1.0),
               rng.uniform(-0.8, 0.8))
    n, t = mx.n, np.arange(mx.n) / SR
    for c in range(2):
        mx.b[:, c] += hp(rng.standard_normal(n), 8000) * np.sin(np.pi * np.clip(t / 0.9, 0, 1)) ** 2 * 0.03
    sparkle.notes = names
    return reverb(mx.b, t60=1.0, mix=0.22, seed=5)[:n]


def confetti():
    rng = R(211)
    n, t = ts(1.5)
    out = np.zeros((n, 2))
    i = int(OFF * SR)
    m = n - i
    tt = np.arange(m) / SR
    popm = sat(lp(rng.standard_normal(m), 5000) * np.exp(-tt / 0.009) * 2.5, 2.0)
    popm += 0.5 * np.sin(TAU * np.cumsum(110 + 90 * np.exp(-tt / 0.02)) / SR) * np.exp(-tt / 0.025)
    popm += 0.7 * damped(520, 0.01, m)
    out[i:] += pan(lp(popm, 9000), 0.0)
    for c in range(2):
        fizz = lp(hp(rng.standard_normal(m), 2200), 8000)
        cr = np.zeros(m)
        idx = rng.integers(0, m, 500)
        cr[idx] = rng.normal(0, 1, 500)
        cr = bp(cr, rng.uniform(5000, 7000), q=2.0) * 1.0
        flut = bp(rng.standard_normal(m), 2500, q=1.5) * (0.5 + 0.5 * np.sin(TAU * rng.uniform(22, 28) * tt)) ** 2
        env = np.minimum(1, tt / 0.03) * np.exp(-tt / 0.42)
        out[i:, c] += (0.22 * fizz + 0.6 * cr + 1.6 * flut) * env * 1.3
    return room(out, n, 0.4, 0.1)


# name, function, intended seconds, description
SFX = [
    ('ding', ding, 0.9, 'Chat notification, two bell tones a fourth apart (B5 then E6)'),
    ('ding_single', ding_single, 0.8, 'Single bell ding (E6)'),
    ('stamp', stamp, 0.7, 'Heavy rubber-stamp thud with a low boom'),
    ('whoosh_short', whoosh_short, 0.35, 'Short swept-noise whoosh, left to right'),
    ('whoosh_long', whoosh_long, 1.2, 'Long swept-noise whoosh, left to right'),
    ('key_1', key_1, 0.14, 'Mechanical key click, variant 1'),
    ('key_2', key_2, 0.14, 'Mechanical key click, variant 2'),
    ('key_3', key_3, 0.14, 'Mechanical key click, variant 3'),
    ('key_4', key_4, 0.14, 'Mechanical key click, variant 4'),
    ('key_5', key_5, 0.14, 'Mechanical key click, variant 5'),
    ('typing_run', typing_run, 4.0, 'Irregular typing with pauses and the odd space bar'),
    ('enter_key', enter_key, 0.3, 'Heavier, lower key press with a spring ping and release'),
    ('card_thwip', card_thwip, 0.25, 'One card fired out of a dispenser: rising noise sweep and a flick'),
    ('card_burst', card_burst, 3.0, 'Accelerating burst of 25 card thwips, rising in pitch'),
    ('counter_tick', counter_tick, 0.08, 'Single counter tick'),
    ('counter_roll', counter_roll, 3.0, 'Accelerating, rising tick roll that ends in a ding'),
    ('record_scratch', record_scratch, 0.6, 'Record-scratch stop: forward, back, forward rip'),
    ('sad_trombone', sad_trombone, 2.6, 'Four descending wah notes (F4 D4 B3 G#3), the last one drooping'),
    ('fall_whistle', fall_whistle, 2.0, 'Descending slide whistle with growing vibrato'),
    ('thud', thud, 0.5, 'Body hits the ground: low thump and a small bounce'),
    ('splat_void', splat_void, 1.4, 'Soft descending bwoop that echoes away into silence'),
    ('block_break_1', block_break_1, 0.35, 'Crunchy break, stony'),
    ('block_break_2', block_break_2, 0.35, 'Crunchy break, woody'),
    ('block_break_3', block_break_3, 0.35, 'Crunchy break, gravelly'),
    ('block_place', block_place, 0.18, 'Soft placement pop'),
    ('explosion_small', explosion_small, 1.4, 'Small explosion: boom, closing noise burst, crackle tail'),
    ('crowd_cheer', crowd_cheer, 3.0, 'Crowd cheer from formant-filtered voices, noise bed, whistles and claps'),
    ('crowd_aww', crowd_aww, 2.0, 'Disappointed crowd aww, voices sliding down'),
    ('applause', applause, 4.0, 'Applause that swells and thins out'),
    ('crickets', crickets, 4.0, 'Three chirping crickets over a faint night trill'),
    ('buzzer_wrong', buzzer_wrong, 0.8, 'Low wrong-answer buzzer'),
    ('tada', tada, 1.5, 'Brass ta-daa in D major with timpani and crash'),
    ('glitch', glitch, 0.6, 'Digital static burst: crushed noise, square blips, stutters'),
    ('clock_tick', clock_tick, 6.0, 'Tick-tock loop, twelve beats at 120 per minute, loops at 6 s'),
    ('clang', clang, 1.2, 'Metal clang with inharmonic ringing partials'),
    ('pop', pop, 0.15, 'Short rising pop'),
    ('sparkle', sparkle, 1.2, 'Rising twinkle of bells in D major pentatonic'),
    ('confetti', confetti, 1.5, 'Party-popper pop followed by fizz and paper flutter'),
    ('error_beep', error_beep, 0.5, 'Two-tone descending error beep'),
    ('power_down', power_down, 1.5, 'Machine powering down, pitch dropping to nothing'),
    ('tv_static', tv_static, 1.0, 'TV static with a faint mains roll and pops'),
    ('fast_forward', fast_forward, 2.0, 'Fast-forward tape chirp, accelerating'),
    ('heartbeat', heartbeat, 3.0, 'Four lub-dub heartbeats at 75 per minute'),
    ('robot_hum', robot_hum, 6.0, 'Machine-room hum with a slow pulse, exactly periodic over 6 s'),
]
