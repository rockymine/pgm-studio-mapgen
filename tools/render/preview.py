"""A model rendered straight from its voxels, before any of it is posted.

The authoritative picture is the one off `sketch/columns` — that is the world the export writes. This is the
draft one: the same isometric drawing, taken from the `{(x, y, z): material}` dict a model is while it is
being written, so a proportion can be corrected in a second rather than in a build. What it cannot show is
anything the studio decides — the paint's rim and wall courses, the relief, a stamped structure — so a model
that looks right here is checked against the real build before it is believed."""
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from iso import BACKGROUND, draw_iso, iso_bounds, _visible
from png import Canvas, hex_rgb, write_png


def sheet(model, palette, path, scale=6, title=None, views=("iso", "front", "side"), gap=24):
    """One model in several views on one image: the isometric, then any orthographic faces asked for."""
    blocks = {cell: hex_rgb(palette[material]) for cell, material in model.items()}
    panels = [_iso_panel(blocks, scale) if view == "iso" else _face_panel(blocks, scale, view)
              for view in views]

    head = 44 if title else 0
    width = sum(p[0] for p in panels) + gap * (len(panels) + 1)
    height = max(p[1] for p in panels) + gap * 2 + head + 26
    canvas = Canvas(width, height, BACKGROUND)
    if title:
        canvas.text(gap, 14, title, (25, 25, 30), 3)

    cursor = gap
    for (w, h, draw, label), view in zip(panels, views):
        draw(canvas, cursor, gap + head)
        canvas.text(cursor, height - 20, label, (120, 120, 128), 2)
        cursor += w + gap
    write_png(path, canvas)
    return canvas.width, canvas.height


def _iso_panel(blocks, scale):
    w, h, k = scale, scale // 2 or 1, scale
    shown = {cell: blocks[cell] for cell in _visible(blocks)}
    u0, u1, v0, v1 = iso_bounds(shown, w, h, k)

    def draw(canvas, x, y):
        draw_iso(canvas, shown, (x - u0, y - v0), w, h, k)
    return int(u1 - u0), int(v1 - v0), draw, f"iso  {len(blocks)} blocks"


# Which plan axis runs across the picture, which runs into it, and which way the camera faces
# along it. The model faces -z, so "front" keeps the smallest z at each cell.
FACE_AXIS = {"front": (0, 2, -1), "back": (0, 2, 1), "side": (2, 0, -1), "other": (2, 0, 1)}


def _face_panel(blocks, scale, view):
    """One orthographic face, nearest-wins with the depth shaded so the form still reads."""
    across, depth, sign = FACE_AXIS[view]
    nearest = {}
    for cell, colour in blocks.items():
        key = (cell[across] * (1 if view in ("front", "back") else 1), cell[1])
        d = cell[depth] * sign
        if key not in nearest or d > nearest[key][0]:
            nearest[key] = (d, colour)

    xs = [key[0] for key in nearest]
    ys = [key[1] for key in nearest]
    ds = [entry[0] for entry in nearest.values()]
    span = (max(ds) - min(ds)) or 1
    flip = view in ("back", "other")

    def draw(canvas, ox, oy):
        for (a, y), (d, colour) in nearest.items():
            px = ox + ((max(xs) - a) if flip else (a - min(xs))) * scale
            py = oy + (max(ys) - y) * scale
            lit = 0.66 + 0.5 * (d - min(ds)) / span
            canvas.rect(px, py, px + scale, py + scale,
                        tuple(max(0, min(255, int(c * lit))) for c in colour))
    return (max(xs) - min(xs) + 1) * scale, (max(ys) - min(ys) + 1) * scale, draw, view
