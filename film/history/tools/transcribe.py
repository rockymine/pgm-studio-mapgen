import sys, time, wave
import numpy as np
from faster_whisper import WhisperModel

wav, out = sys.argv[1], sys.argv[2]
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=10)
t0 = time.time()
w = wave.open(wav, "rb"); audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
segs, info = model.transcribe(audio, language=None, vad_filter=True, beam_size=5,
                              condition_on_previous_text=False,
                              initial_prompt="Ruediger, rockymine, samshaap, TTtie. Minecraft PGM, Overcast, Base 2 Wool, Wool, Map, XML, Claude.")
print("lang", info.language, info.language_probability, flush=True)
with open(out, "w", encoding="utf-8") as f:
    for s in segs:
        m, sec = divmod(int(s.start), 60)
        line = f"[{m:02d}:{sec:02d}] {s.text.strip()}"
        f.write(line + "\n"); f.flush()
        print(line, flush=True)
print("done", round(time.time() - t0), "s", flush=True)
