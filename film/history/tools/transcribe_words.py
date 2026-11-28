import sys, json, wave
import numpy as np
from faster_whisper import WhisperModel
wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav, "rb"); audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=8)
segs, info = model.transcribe(audio, language="en", vad_filter=True, beam_size=5, word_timestamps=True,
    condition_on_previous_text=False,
    initial_prompt="Ruediger, rockymine, samshaap, TTtie. Minecraft PGM, Overcast, Base 2 Wool, Wool, Map, XML, Claude.")
words = []
for s in segs:
    for wd in s.words:
        words.append([round(wd.start, 2), round(wd.end, 2), wd.word])
    print(int(s.start), flush=True)
json.dump(words, open(out, "w", encoding="utf-8"))
print("done", len(words))
