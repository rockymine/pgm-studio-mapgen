import sys, wave, numpy as np, torch
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy
wav, out, models = sys.argv[1], sys.argv[2], sys.argv[3]
w = wave.open(wav, "rb"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir=models,
                                     run_opts={"device": "cpu"}, local_strategy=LocalStrategy.COPY)
torch.set_num_threads(6)
sr, win, hop = 16000, 24000, 8000
starts = list(range(0, len(a) - win, hop))
rms = np.array([np.sqrt(np.mean(a[s:s+win]**2)) for s in starts])
keep = [s for s, r in zip(starts, rms) if r > 0.01]
print("windows", len(starts), "kept", len(keep), flush=True)
embs = []
B = 64
for i in range(0, len(keep), B):
    batch = torch.tensor(np.stack([a[s:s+win] for s in keep[i:i+B]]))
    with torch.no_grad():
        e = enc.encode_batch(batch).squeeze(1).numpy()
    embs.append(e)
    if i % (B*20) == 0: print(i, flush=True)
np.savez(out, t=np.array(keep) / sr, e=np.concatenate(embs))
print("done")
