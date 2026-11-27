#!/usr/bin/env python3
# Mix voice, music and effects from the film's cue list; write subtitles.
import json, wave, os, sys, numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__)); A = ROOT + '/../audio/'
info = json.load(open(ROOT + '/filminfo.json')); tl = json.load(open(ROOT + '/timeline.json'))
SR = 48000; N = int((info['total'] + 0.5) * SR)
shot_t0 = {s['id']: s['t0'] for s in info['shots']}
def load(path):
    with wave.open(path) as w:
        n, ch, sr, sw = w.getnframes(), w.getnchannels(), w.getframerate(), w.getsampwidth()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    x = x.reshape(-1, ch)
    if ch == 1: x = np.repeat(x, 2, axis=1)
    assert sr == SR, (path, sr)
    return x
import subprocess
EQ = {'infomercial': 'highpass=f=110,equalizer=f=3500:t=q:w=1:g=2', 'lobby_muzak': 'highpass=f=80,equalizer=f=3000:t=q:w=1:g=3', 'machine': 'highpass=f=90', 'hero': 'highpass=f=60', 'sad_piano': 'highpass=f=60'}
def find(name):
    if name in EQ:
        out = f'{ROOT}/out/eq_{name}.wav'
        if not os.path.exists(out): subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A + 'music/' + name + '.wav', '-af', EQ[name], '-ar', '48000', out], check=True)
        return out
    for d in ('sfx/', 'music/'):
        if os.path.exists(A + d + name + '.wav'): return A + d + name + '.wav'
    raise FileNotFoundError(name)
def place(bus, x, t, gain=1.0):
    i = int(round(t * SR)); 
    if i >= N: return
    x = x[:N - i]; bus[i:i + len(x)] += x * gain
sfx = np.zeros((N, 2), np.float32); music = np.zeros((N, 2), np.float32); vo = np.zeros((N, 2), np.float32)
for c in info['cues']:
    if 'music' in c:
        x = load(find(c['music'])); end = shot_t0.get(c.get('until'), info['total']); length = int((end - c['t']) * SR)
        if length <= 0: continue
        reps = int(np.ceil(length / len(x))); y = np.tile(x, (reps, 1))[:length].copy()
        fi, fo = int(0.05 * SR), int(min(c.get('fade', .5), (end - c['t']) / 2) * SR)
        y[:fi] *= np.linspace(0, 1, fi)[:, None]; y[-fo:] *= np.linspace(1, 0, fo)[:, None]
        place(music, y, c['t'], c['gain'])
    else:
        place(sfx, load(find(c['f'])), c['t'], c['gain'] * 0.8)
tl['lines'] = {k: v for k, v in tl['lines'].items() if v['shot'] in shot_t0}
for lid, l in tl['lines'].items():
    place(vo, load(f'{ROOT}/vo/{lid}.wav'), shot_t0[l['shot']] + l['t0'], 1.0)
# duck music (and a little sfx) under the voice
def smooth(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n - n // 2)])); return (c[n:n + len(x)] - c[:len(x)]) / n
env = np.abs(vo[:, 0]).astype(np.float64); win = int(0.12 * SR); env = smooth(env, win)
env = np.minimum(1, env / 0.05); k = int(0.25 * SR); env = np.maximum.reduce([env, np.roll(env, k // 2), np.roll(env, -k // 2)])
env = smooth(env, k).astype(np.float32)
duck = (1 - 0.62 * env)[:, None]
def master(x):
    x = np.tanh(x * 1.1) ; peak = np.abs(x).max() or 1; return x * (0.89 / peak)
def save(name, x):
    with wave.open(f'{ROOT}/out/{name}', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
bed = music * duck * 0.8 + sfx * (1 - 0.25 * env)[:, None]
save('mix_full.wav', master(bed + vo * 1.25)); save('mix_nodub.wav', master(bed) * 0.8); save('vo_only.wav', master(vo))
# subtitles (.ass styled for burning, .srt plain)
def ts(t, srt=False):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'.replace('.', ',') if srt else f'{h:d}:{m:02d}:{s:05.2f}'
COL = {'MACHINE': '&H00FFFF55&', 'PITCHMAN': '&H001FD2FF&', 'DISCLAIMER': '&H00DDDDDD&'}
ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 0', '', '[V4+ Styles]',
       'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
       'Style: Default,Inter,46,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,-1,0,0,0,100,100,0,0,1,4,2,2,220,220,86,1', '',
       '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
srt = []
items = sorted(tl['lines'].items(), key=lambda kv: shot_t0[kv[1]['shot']] + kv[1]['t0'])
for n, (lid, l) in enumerate(items, 1):
    a = shot_t0[l['shot']] + l['t0']; b = shot_t0[l['shot']] + l['t1'] + 0.25
    if n < len(items): b = min(b, shot_t0[items[n][1]['shot']] + items[n][1]['t0'] - 0.02)
    name = l['name'].upper(); col = COL.get(l['who'], '&H0099E6FF&')
    if l['who'] != 'DISCLAIMER': ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{{\\c{col}}}{name}:{{\\c&HFFFFFF&}} {l['text']}")
    srt.append(f"{n}\n{ts(a, True)} --> {ts(b, True)}\n{l['name']}: {l['text']}\n")
open(ROOT + '/out/subs.ass', 'w').write('\n'.join(ass) + '\n'); open(ROOT + '/out/subs.srt', 'w').write('\n'.join(srt))
print('mixed', round(info['total'], 2), 's;', len(info['cues']), 'cues;', len(items), 'lines')
