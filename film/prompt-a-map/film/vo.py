# Synthesize every line, measure it, and solve the timeline.
import json, os, subprocess, wave, hashlib, sys
import numpy as np
from script import CAST, SHOTS
TTS = '/tmp/claude-0/-home-user/5b5a763a-8f02-5e92-a825-a8c273c7b88d/scratchpad/tts/'
voices = {}
def piper(cfg, text, out):
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    m = cfg['model']
    if m not in voices: voices[m] = PiperVoice.load(TTS + m)
    sc = SynthesisConfig(speaker_id=cfg.get('speaker'), length_scale=cfg.get('length', 1.0), noise_scale=cfg.get('noise', 0.667), noise_w_scale=cfg.get('noise_w', 0.8))
    chunks = list(voices[m].synthesize(text, sc))
    audio = np.concatenate([c.audio_int16_array for c in chunks]); sr = chunks[0].sample_rate
    with wave.open(out, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(audio.tobytes())
FX = {
    None: 'highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80:makeup=3',
    'robot': 'highpass=f=120,aecho=0.8:0.7:9|17:0.45|0.3,flanger=delay=2:depth=3:speed=0.4,acompressor=threshold=-20dB:ratio=4:makeup=4',
    'kid': 'asetrate=22050*1.22,aresample=48000,atempo=0.9,highpass=f=150,acompressor=threshold=-18dB:ratio=3:makeup=3',
    'fast': 'atempo=1.28,highpass=f=90,acompressor=threshold=-16dB:ratio=5:attack=3:release=50:makeup=4',
}
def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]).decode())
lines, shots = {}, {}
for s in SHOTS:
    t = s.get('pre', 0.5); last = 0
    for n, ln in enumerate(s['lines'], 1):
        who, text = ln[0], ln[1]; opt = ln[2] if len(ln) > 2 else {}
        say = opt.get('say', text); cfg = CAST[who]; lid = f"{s['id']}.{n}"
        key = hashlib.md5(json.dumps([cfg, say], sort_keys=True).encode()).hexdigest()[:10]
        raw, out = f'vo/raw-{key}.wav', f'vo/{lid}.wav'
        if not os.path.exists(raw):
            if cfg['engine'] == 'espeak':
                subprocess.run(['espeak-ng', '-v', cfg['voice'], '-s', str(cfg['speed']), '-p', str(cfg['pitch']), '-w', raw, say], check=True)
            else: piper(cfg, say, raw)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-af', FX[cfg.get('fx')] + ',silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '1', out], check=True)
        d = dur(out)
        if n > 1: t += opt.get('gap', 0.25)
        t = max(t, opt.get('at', 0))
        lines[lid] = dict(t0=round(t, 3), t1=round(t + d, 3), who=who, name=cfg['name'], text=text, shot=s['id'])
        t += d; last = t
    shots[s['id']] = dict(dur=round(max(s.get('min', 0), last + s.get('post', 0.5)), 3))
tl = dict(shots=shots, lines=lines)
json.dump(tl, open('timeline.json', 'w'), indent=1)
open('timeline.js', 'w').write('window.TIMELINE = ' + json.dumps(tl) + ';\n')
tot = 0
for s in SHOTS:
    print(f"{s['id']}  t0={tot:6.2f}  dur={shots[s['id']]['dur']:5.2f}"); tot += shots[s['id']]['dur']
    for lid, l in lines.items():
        if l['shot'] == s['id']: print(f"     {lid:7} {l['t0']:5.2f}-{l['t1']:5.2f} {l['who']:10} {l['text'][:60]}")
print('TOTAL', round(tot, 2))
