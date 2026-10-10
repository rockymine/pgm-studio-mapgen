"""Riftwater's paint stack one layer at a time: where each of the nine top layers won, over the ground in grey; the caption carries the block's own colour."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import sys, json, pickle, numpy as np
from PIL import Image
sys.path.insert(0, D)
from style import up, shade, contours
h = pickle.load(open(f"{OUT}/stack.pkl", "rb")); wd = pickle.load(open(f"{OUT}/world.pkl", "rb"))
land, H = h["land"], h["H"]; S = 2
win = [s for s in wd["snaps"] if s["label"] == "lay"][0]["extra"]["winner"][:land.shape[0]]
LAYERS = [  # the block, its colour, the conditions as ground.py states them
    ("Sand", (219, 207, 163), "Neigung bis 37°, Flussufer, Rauschen über −0,1"),
    ("Kies", (136, 126, 126), "Neigung bis 37°, Flussufer"),
    ("grobe Erde", (119, 85, 59), "Neigung 33–38°, Rauschen über 0,35"),
    ("Andesit", (136, 136, 137), "Neigung 38–55°, Rauschen −0,25 bis 0,15, Zufall bis 0,5"),
    ("Stein", (125, 125, 125), "Neigung 38–55°, Rauschen −0,25 bis 0,15"),
    ("grobe Erde", (119, 85, 59), "Neigung 38–55°, Rauschen unter −0,25"),
    ("Stein", (125, 125, 125), "Neigung über 55°, Zufall bis 0,45"),
    ("Andesit", (136, 136, 137), "Neigung über 55°, Zufall bis 0,8"),
    ("Bruchstein", (100, 100, 100), "Neigung über 55°"),
]
grey = np.where(land[..., None], (np.array([214, 210, 200]) * shade(H)), np.array([24, 26, 34]))
tiles = []
for i, (name, colour, cond) in enumerate(LAYERS):
    m = win == i
    img = up(np.where(m[..., None], np.array([214, 51, 108], float), grey), S)
    nm = f"paint-{i}"; Image.fromarray(np.clip(img, 0, 255).astype(np.uint8).transpose(1, 0, 2)).save(f"{OUT}/img/{nm}.png")
    tiles.append(dict(n=i + 1, name=name, cond=cond, img=nm, cols=int(m.sum())))
rest = (win < 0) & land
tiles.append(dict(n=0, name="keine Schicht", cond="Gras, über 55° Stein: der Block nach Neigung, den lay ohne Schicht legt", img=None, cols=int(rest.sum())))
json.dump(tiles, open(f"{OUT}/paint.json", "w")); print([(t["n"], t["cols"]) for t in tiles])
