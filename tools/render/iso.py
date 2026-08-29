"""Isometric and orthographic renders of a built world, from the column payload the studio answers with.

`POST /api/map/{slug}/sketch/columns` returns every column's solid runs, palette-indexed, each attributed to
the sketch layer that drew it — the same build the export writes. That payload is the only picture of a
stacked board that carries real block colours, so everything here reads it rather than the documents that
produced it: what is drawn is what was built.

The four views:

- `isometric` — the board from above at 2:1, painter's-algorithm cubes, back to front.
- `elevation`  — one orthographic face (north, south, east or west), which is what says whether a silhouette
  reads. An isometric view flatters a shape; a straight-on face does not.
- `slices`     — one plan per Y level, the model as the layer system actually holds it.
- `exploded`   — one isometric per sketch layer, laid out in a row, which is the picture of the decomposition.
"""
import json

from png import Canvas, hex_rgb, shade, write_png

# The three visible faces of a cube under this camera, and what each does to the block's colour. The top
# keeps the block's own colour and the two flanks fall away, rather than the top being lit — a sculpture in
# quartz is already near white, and lifting its top face further flattens the whole form into a silhouette.
TOP, RIGHT, LEFT = 1.0, 0.78, 0.55
BACKGROUND = (247, 247, 244)


def read_columns(payload):
    """The payload's flat `cols` array as `(x, z, [(y_top, y_bottom, palette_slot, layer_slot), ...])`.

    The encoding is `[x, z, run_count, (y_top, y_bottom, slot, layer) * run_count, ...]` — flat because a
    board is tens of thousands of runs and a nested shape would be mostly punctuation."""
    cols = payload["cols"]
    out, i = [], 0
    while i < len(cols):
        x, z, count = cols[i], cols[i + 1], cols[i + 2]
        i += 3
        runs = []
        for _ in range(count):
            runs.append((cols[i], cols[i + 1], cols[i + 2], cols[i + 3]))
            i += 4
        out.append((x, z, runs))
    return out


def voxels(payload, layers=None, clip=None):
    """Every block the payload holds, as `{(x, y, z): colour}`.

    `layers` keeps only the runs a named sketch layer drew (plus the unattributed ones, which are the
    structures standing on the terrain rather than being it). `clip` is `(min_x, max_x, min_y, max_y, min_z,
    max_z)`, any bound None for unbounded."""
    palette = [hex_rgb(entry) for entry in payload["palette"]]
    names = payload.get("layers") or []
    wanted = None if layers is None else {names.index(name) for name in layers if name in names}

    out = {}
    for x, z, runs in read_columns(payload):
        if clip and not (_within(x, clip[0], clip[1]) and _within(z, clip[4], clip[5])):
            continue
        for y_top, y_bottom, slot, layer in runs:
            if wanted is not None and layer >= 0 and layer not in wanted:
                continue
            colour = palette[slot]
            for y in range(y_bottom, y_top + 1):
                if clip and not _within(y, clip[2], clip[3]):
                    continue
                out[(x, y, z)] = colour
    return out


def _within(value, low, high):
    return (low is None or value >= low) and (high is None or value <= high)


def turned(blocks, quarter):
    """The block set spun about the vertical in 90-degree steps, so the one camera can look at any face.
    The projection is fixed — turning the model is what turns the view, which is how the studio's own
    preview rotates too."""
    if not quarter % 4:
        return blocks
    out = {}
    for (x, y, z), colour in blocks.items():
        for _ in range(quarter % 4):
            x, z = -z, x
        out[(x, y, z)] = colour
    return out


def _visible(blocks):
    """The blocks with at least one of their three camera-facing neighbours missing. The camera sits at
    (+inf, +inf, +inf), so a block whose +x, +y and +z neighbours are all solid can show nothing."""
    return [cell for cell in blocks
            if (cell[0] + 1, cell[1], cell[2]) not in blocks
            or (cell[0], cell[1] + 1, cell[2]) not in blocks
            or (cell[0], cell[1], cell[2] + 1) not in blocks]


def iso_bounds(blocks, w, h, k):
    us = [(x - z) * w for x, y, z in blocks]
    vs = [(x + z) * h - y * k for x, y, z in blocks]
    return min(us) - w, max(us) + w, min(vs) - k, max(vs) + 2 * h


def draw_iso(canvas, blocks, origin, w, h, k, order=None):
    """Paint every block back to front. Depth along the camera axis is `x + y + z`, so ascending order draws
    the near ones last and no depth buffer is needed."""
    ox, oy = origin
    for cell in sorted(blocks, key=order or (lambda c: c[0] + c[1] + c[2])):
        x, y, z = cell
        colour = blocks[cell]
        px = ox + (x - z) * w
        py = oy + (x + z) * h - y * k
        canvas.fill_polygon([(px, py - k), (px + w, py + h - k),
                             (px, py + 2 * h - k), (px - w, py + h - k)], shade(colour, TOP))
        canvas.fill_polygon([(px + w, py + h - k), (px + w, py + h),
                             (px, py + 2 * h), (px, py + 2 * h - k)], shade(colour, RIGHT))
        canvas.fill_polygon([(px - w, py + h - k), (px - w, py + h),
                             (px, py + 2 * h), (px, py + 2 * h - k)], shade(colour, LEFT))


def isometric(payload, path, scale=6, layers=None, clip=None, title=None, caption=None, margin=40,
              quarter=0):
    """The board as one isometric picture. `scale` is the cube's half-width in pixels; a cube is `2*scale`
    wide, `scale` tall on the ground plane and `scale` tall in Y, which is the 2:1 the studio's own preview
    uses."""
    blocks = turned(voxels(payload, layers=layers, clip=clip), quarter)
    if not blocks:
        raise SystemExit("nothing to draw")
    w, h, k = scale, scale // 2 or 1, scale
    shown = {cell: blocks[cell] for cell in _visible(blocks)}

    u0, u1, v0, v1 = iso_bounds(shown, w, h, k)
    head = 46 if title else 0
    foot = 34 if caption else 0
    width = max(int(u1 - u0) + margin * 2,
                margin * 2 + max(len(title or "") * 18, len(caption or "") * 12))
    canvas = Canvas(width, int(v1 - v0) + margin * 2 + head + foot, BACKGROUND)
    draw_iso(canvas, shown, (margin - u0, margin - v0 + head), w, h, k)
    if title:
        canvas.text(margin, 14, title, (25, 25, 30), 3)
    if caption:
        canvas.text(margin, canvas.height - 24, caption, (110, 110, 118), 2)
    write_png(path, canvas)
    return len(blocks), len(shown), (canvas.width, canvas.height)


FACES = {"north": ("x", "z", False), "south": ("x", "z", True),
         "west": ("z", "x", True), "east": ("z", "x", False)}


def elevation(payload, path, face="north", scale=6, layers=None, clip=None, title=None, caption=None,
              margin=30):
    """One orthographic face. The nearest block along the view axis wins each pixel, and depth is shaded, so
    the picture reads as a silhouette with its own relief rather than as a flat stencil."""
    blocks = voxels(payload, layers=layers, clip=clip)
    if not blocks:
        raise SystemExit("nothing to draw")
    across, depth, flip = FACES[face]
    pick = (lambda c: c[0]) if across == "x" else (lambda c: c[2])
    into = (lambda c: c[2]) if depth == "z" else (lambda c: c[0])

    nearest = {}
    for cell, colour in blocks.items():
        key = (pick(cell), cell[1])
        d = into(cell) if flip else -into(cell)
        if key not in nearest or d > nearest[key][0]:
            nearest[key] = (d, colour)

    xs = [key[0] for key in nearest]
    ys = [key[1] for key in nearest]
    depths = [entry[0] for entry in nearest.values()]
    span = (max(depths) - min(depths)) or 1
    head = 46 if title else 0
    foot = 34 if caption else 0
    width = (max(xs) - min(xs) + 1) * scale
    height = (max(ys) - min(ys) + 1) * scale
    canvas = Canvas(width + margin * 2, height + margin * 2 + head + foot, BACKGROUND)

    for (across_at, y), (d, colour) in nearest.items():
        px = margin + ((max(xs) - across_at) if flip else (across_at - min(xs))) * scale
        py = margin + head + (max(ys) - y) * scale
        lit = 0.72 + 0.42 * (d - min(depths)) / span
        canvas.rect(px, py, px + scale, py + scale, shade(colour, lit))
    if title:
        canvas.text(margin, 14, title, (25, 25, 30), 3)
    if caption:
        canvas.text(margin, canvas.height - 24, caption, (110, 110, 118), 2)
    write_png(path, canvas)
    return canvas.width, canvas.height


def exploded(payload, path, scale=5, gap=26, clip=None, title=None, order=None, quarter=0):
    """One isometric per sketch layer, side by side in the order the document draws them. This is the picture
    of the decomposition itself: what each slab of the stack contributes, and nothing else."""
    names = order or (payload.get("layers") or [])
    if not names:
        raise SystemExit("payload names no layers")
    w, h, k = scale, scale // 2 or 1, scale

    panels = []
    for name in names:
        blocks = turned(voxels(payload, layers=[name], clip=clip), quarter)
        if not blocks:
            continue
        shown = {cell: blocks[cell] for cell in _visible(blocks)}
        panels.append((name, shown, iso_bounds(shown, w, h, k), len(blocks)))

    head, foot, margin = 48, 34, 20
    width = max(sum(max(int(p[2][1] - p[2][0]), (len(p[0]) + len(str(p[3])) + 2) * 12) + gap
                    for p in panels) + margin * 2,
                margin * 2 + len(title or "") * 18)
    height = max(int(p[2][3] - p[2][2]) for p in panels) + margin * 2 + head + foot
    canvas = Canvas(width, height, BACKGROUND)
    if title:
        canvas.text(margin, 14, title, (25, 25, 30), 3)

    cursor = margin
    for name, shown, (u0, u1, v0, v1), count in panels:
        label = f"{name}  {count}"
        # A panel is at least as wide as its own caption: a layer holding four blocks draws a picture six
        # pixels across, and the labels then run into one another and say nothing.
        step = max(int(u1 - u0), canvas.text_width(label, 2))
        draw_iso(canvas, shown, (cursor + (step - int(u1 - u0)) // 2 - u0, margin - v0 + head), w, h, k)
        canvas.text(cursor, height - 26, label, (110, 110, 118), 2)
        cursor += step + gap
    write_png(path, canvas)
    return canvas.width, canvas.height


def contact_sheet(paths, out, columns=2, gap=16, title=None):
    """Several finished PNGs tiled into one sheet, so a gallery is one image to look at rather than eight."""
    import struct
    import zlib as _zlib

    tiles = []
    for path in paths:
        with open(path, "rb") as handle:
            data = handle.read()
        width, height = struct.unpack(">II", data[16:24])
        idat = b""
        i = 8
        while i < len(data):
            length = struct.unpack(">I", data[i:i + 4])[0]
            tag = data[i + 4:i + 8]
            if tag == b"IDAT":
                idat += data[i + 8:i + 8 + length]
            i += 12 + length
        raw = _zlib.decompress(idat)
        stride = width * 3
        rows = [raw[r * (stride + 1) + 1:(r + 1) * (stride + 1)] for r in range(height)]
        tiles.append((width, height, rows))

    rows_of = [tiles[i:i + columns] for i in range(0, len(tiles), columns)]
    head = 50 if title else 0
    sheet_w = max(sum(t[0] for t in row) + gap * (len(row) + 1) for row in rows_of)
    sheet_h = sum(max(t[1] for t in row) + gap for row in rows_of) + gap + head
    canvas = Canvas(sheet_w, sheet_h, BACKGROUND)
    if title:
        canvas.text(gap, 16, title, (25, 25, 30), 3)

    y = gap + head
    for row in rows_of:
        x = gap
        for width, height, pixels in row:
            for r in range(height):
                offset = ((y + r) * canvas.width + x) * 3
                canvas.pixels[offset:offset + width * 3] = pixels[r]
            x += width + gap
        y += max(t[1] for t in row) + gap
    write_png(out, canvas)
    return canvas.width, canvas.height


if __name__ == "__main__":
    import sys
    payload = json.load(open(sys.argv[1]))
    isometric(payload, sys.argv[2] if len(sys.argv) > 2 else "iso.png")
