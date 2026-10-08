"""The station's plan, one slice per level, read from the built volume: the tunnels (y 16), the floor (21),
the spawns' floor (25) and the decks (28). Solid at the slice in its block colour, open floor below it dimmed,
void black. This is the plan picture: a TDM board is a stack of floors, and a slice shows each.

    python3 levels.py <build-dir> <out.png>
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

import render_iso as R

LEVELS = [(16, "y 15-18: the penstocks"), (21, "y 21: the hall floor, galleries, corridors, boxes"),
          (25, "y 25: the gatehouses"), (28, "y 28: control walk, catwalks, gantry")]


def main(build, out):
    x0, z0, ids, dat = R.load(build)
    tab = R.colour_table()
    ims = []
    for y, label in LEVELS:
        sl, d = ids[:, y, :], dat[:, y, :]
        below, bd = ids[:, y - 1, :], dat[:, y - 1, :]
        img = np.zeros((ids.shape[2], ids.shape[0], 3)) + 12
        c = tab[sl, d & 15].transpose(1, 0, 2)
        cb = tab[below, bd & 15].transpose(1, 0, 2) * 0.6
        img = np.where((sl > 0).T[:, :, None], c, np.where((below > 0).T[:, :, None], cb, img))
        im = Image.fromarray(img.astype(np.uint8)).resize((ids.shape[0] * 4, ids.shape[2] * 4), Image.NEAREST)
        canvas = Image.new("RGB", (im.width, im.height + 18), (12, 12, 12))
        canvas.paste(im, (0, 18))
        ImageDraw.Draw(canvas).text((4, 3), label, fill=(255, 230, 120))
        ims.append(canvas)
    W = ims[0].width * 2 + 10; H = ims[0].height * 2 + 10
    sheet = Image.new("RGB", (W, H), (0, 0, 0))
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % 2) * (im.width + 10), (k // 2) * (im.height + 10)))
    sheet.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
