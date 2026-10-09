"""The study's renders, framed as the originals' were, so the two can be set side by side.

    python3 renders.py <build-dir> <board-dir>
"""
import os
import sys

from pgmvox import World, render

w = World.load(sys.argv[1])
out = os.path.join(sys.argv[2], "renders")


def iso(name, scale, corner, box=None, ymin=0):
    p = os.path.join(out, name)
    render.iso(w.ids, w.dat, w.x0, w.z0, p, scale, corner, box, ymin)
    render.trim(p)


iso("30-iso-se.png", 6, "se")
iso("31-iso-nw.png", 6, "nw")
iso("32-tower-se.png", 14, "se", (12, -27, 24, -12), 10)
iso("33-garden-sw.png", 10, "sw", (-33, -7, -4, 17), 4)
render.cutaway(w, os.path.join(out, "10-section-x-20.png"), [(-19.5, -30), (-19.5, 29)], 0, 30, 8,
               title="through the garden and an islet, along z at x -20")

# the study beside the originals' renders (ref-*, rendered from CommunityMaps ctw/brittlebush_ii with the same
# renderer), at one height so the eye compares like with like
from PIL import Image, ImageDraw  # noqa: E402

PAIRS = [("ref-brittlebush_ii-garden-sw.png", "33-garden-sw.png", "a platform with a bed"),
         ("ref-brittlebush_ii-wool-room-se.png", "32-tower-se.png", "a wool room's tower and its heart")]
rows = []
for a, b, title in PAIRS:
    ims = [Image.open(os.path.join(out, f)).convert("RGB") for f in (a, b)]
    ims = [im.resize((int(im.width * 360 / im.height), 360)) for im in ims]
    row = Image.new("RGB", (ims[0].width + ims[1].width + 60, 400), (206, 221, 234))
    row.paste(ims[0], (20, 30))
    row.paste(ims[1], (ims[0].width + 40, 30))
    d = ImageDraw.Draw(row)
    d.text((20, 8), f"Brittlebush II: {title}", fill=(30, 30, 30))
    d.text((max(ims[0].width + 40, int(d.textlength(f"Brittlebush II: {title}")) + 40), 8), "the study",
           fill=(30, 30, 30))
    rows.append(row)
sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height for r in rows)), (206, 221, 234))
y = 0
for row in rows:
    sheet.paste(row, (0, y))
    y += row.height
sheet.save(os.path.join(out, "01-original-and-study.png"))
