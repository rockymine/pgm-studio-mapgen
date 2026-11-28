import sys, json, wave, numpy as np, torch
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy
S = sys.argv[1]
words = json.load(open(S + '/video/words.json', encoding='utf-8'))
w = wave.open(S + '/video/audio16k.wav', 'rb'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
# chunks: consecutive words, gap < 0.35 s, length <= 3 s
chunks, cur = [], []
for wd in words:
    if cur and (wd[0] - cur[-1][1] > 0.35 or wd[1] - cur[0][0] > 3.0):
        chunks.append(cur); cur = []
    cur.append(wd)
if cur: chunks.append(cur)
enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir=S + '/models/ecapa', run_opts={"device": "cpu"}, local_strategy=LocalStrategy.COPY)
torch.set_num_threads(6)
out = []
for i, c in enumerate(chunks):
    s, e = c[0][0], c[-1][1]
    if e - s < 0.6:
        mid = (s + e) / 2; s, e = mid - 0.3, mid + 0.3
    seg = a[int(max(0, s) * 16000):int(e * 16000)]
    with torch.no_grad():
        emb = enc.encode_batch(torch.tensor(seg)[None]).squeeze().numpy()
    out.append(emb)
np.savez(S + '/video/chunks.npz', e=np.stack(out), s=np.array([c[0][0] for c in chunks]), t=np.array([c[-1][1] for c in chunks]))
json.dump([' '.join(x[2].strip() for x in c) for c in chunks], open(S + '/video/chunks.json', 'w', encoding='utf-8'))
print('chunks', len(chunks))
