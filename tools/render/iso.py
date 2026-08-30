"""Isometric and orthographic renders of a built world, from the column payload the studio answers with.

`POST /api/map/{slug}/sketch/columns` returns every column's solid runs, palette-indexed, each attributed to
the sketch layer that drew it — the same build the export writes. That payload is the only picture of a
stacked board that carries real block colours, so everything here reads it rather than the documents that
produced it: what is drawn is what was built.

The views:

- `isometric` — the board from above at 2:1, painter's-algorithm cubes, back to front.
- `xray`      — the same camera with whatever hides a roofed void drawn as a wash, which is the only view
  anything underground appears in at all. `cavities` beside it is the read on its own: what covered space
  a board holds, how big, between which blocks, and which of it nothing can walk into.
- `elevation`  — one orthographic face (north, south, east or west), which is what says whether a silhouette
  reads. An isometric view flatters a shape; a straight-on face does not.
- `exploded`   — one isometric per sketch layer, laid out in a row, which is the picture of the decomposition.
"""
import json

from png import Canvas, desaturate, hex_rgb, shade, write_png

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


def draw_iso(canvas, blocks, origin, w, h, k, order=None, alpha=None):
    """Paint every block back to front. Depth along the camera axis is `x + y + z`, so ascending order draws
    the near ones last and no depth buffer is needed.

    `alpha` maps a cell to the opacity its three faces are painted at; a cell it does not name is opaque.
    Back-to-front is what makes that meaningful — a translucent cube is composited over whatever the
    passes behind it already put down."""
    ox, oy = origin
    for cell in sorted(blocks, key=order or (lambda c: c[0] + c[1] + c[2])):
        x, y, z = cell
        colour = blocks[cell]
        opacity = 1.0 if alpha is None else alpha.get(cell, 1.0)
        px = ox + (x - z) * w
        py = oy + (x + z) * h - y * k
        canvas.fill_polygon([(px, py - k), (px + w, py + h - k),
                             (px, py + 2 * h - k), (px - w, py + h - k)], shade(colour, TOP), opacity)
        canvas.fill_polygon([(px + w, py + h - k), (px + w, py + h),
                             (px, py + 2 * h), (px, py + 2 * h - k)], shade(colour, RIGHT), opacity)
        canvas.fill_polygon([(px - w, py + h - k), (px - w, py + h),
                             (px, py + 2 * h), (px, py + 2 * h - k)], shade(colour, LEFT), opacity)


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


def cavities(blocks, min_cells=6, max_headroom=24):
    """Every roofed void in the block set, largest first, as
    `{"cells", "min": (x, y, z), "max": (x, y, z), "sealed": bool, "voids": {cell, ...}}`.

    A void is **air with solid over it in its own column** — the plain meaning of underground, and the
    only test that finds a room without being told where to look: a layer document states what was drawn,
    never what the drawing left hollow, and the hollow is the subject.

    `max_headroom` is what keeps the sky out of the answer. A cloud, a sky-written letter or an observer
    platform roofs everything under it just as a hillside does, and on a board carrying any of them the
    largest "void" is tens of thousands of cells of open air. A room is a floor and a ceiling that belong
    to each other, so the measure is taken per column and per air run: a run of air taller than this is
    not a room, and the sixty-four courses under a cloud say so.

    Sealed-ness is a second, weaker fact and not the test. Air is flooded from one corner of a shell
    padded a block beyond the model's own bounding box, and a void no such air reaches is marked `sealed`.
    A room worth a picture is normally *not* sealed — a chamber with a stair down to it is open to the sky
    through its own shaft — so a sealed void is reported rather than sought: it is a space nothing can
    walk into, which on a board that meant to build a room is a finding."""
    xs = [cell[0] for cell in blocks]
    ys = [cell[1] for cell in blocks]
    zs = [cell[2] for cell in blocks]
    x0, y0, z0 = min(xs) - 1, min(ys) - 1, min(zs) - 1
    span_x, span_y, span_z = max(xs) - x0 + 2, max(ys) - y0 + 2, max(zs) - z0 + 2
    plane = span_x * span_z
    size = plane * span_y

    SOLID, ROOFED, HELD = 1, 2, 3
    state = bytearray(size)
    for x, y, z in blocks:
        state[(y - y0) * plane + (z - z0) * span_x + (x - x0)] = SOLID

    # The model is padded by a block on every side, so the whole outer shell is air and the shell is
    # six-connected — flooding from its corner reaches all of it. That padding is also why the walk needs
    # no per-axis bound test: a step that runs off the end of a row or a plane lands on the opposite
    # shell, which is air the flood has already opened, so a wrapped step can only ever re-open an open
    # cell. A roofed cell is never on the shell, so the same holds for the component walk below.
    steps = (1, -1, span_x, -span_x, plane, -plane)
    sky = bytearray(size)
    sky[0] = 1
    stack = [0]
    while stack:
        index = stack.pop()
        for step in steps:
            ahead = index + step
            if 0 <= ahead < size and not sky[ahead] and state[ahead] != SOLID:
                sky[ahead] = 1
                stack.append(ahead)

    # A column's void is what is hollow between its own lowest block and its own highest: air under the
    # bottom of a stack is not a room, it is the space the board stands in, and air over the top of one is
    # the sky. Between those two the air is taken one run at a time, so a run too tall to be a room can be
    # dropped without dropping the room in the same column.
    stacks = {}
    for x, y, z in blocks:
        low, high = stacks.get((x, z), (y, y))
        stacks[(x, z)] = (min(low, y), max(high, y))
    for (x, z), (floor, ceiling) in stacks.items():
        base = (z - z0) * span_x + (x - x0)
        run = []
        for y in range(floor + 1, ceiling):
            index = (y - y0) * plane + base
            if state[index] == SOLID:
                if len(run) <= max_headroom:
                    for at in run:
                        state[at] = ROOFED
                run = []
            else:
                run.append(index)
        if run and len(run) <= max_headroom:
            for at in run:
                state[at] = ROOFED

    found = []
    for start in range(size):
        if state[start] != ROOFED:
            continue
        state[start] = HELD
        stack, held = [start], []
        while stack:
            index = stack.pop()
            held.append(index)
            for step in steps:
                ahead = index + step
                if 0 <= ahead < size and state[ahead] == ROOFED:
                    state[ahead] = HELD
                    stack.append(ahead)
        if len(held) < min_cells:
            continue
        voids = set()
        for index in held:
            rest, x = divmod(index, span_x)
            y, z = divmod(rest, span_z)
            voids.add((x + x0, y + y0, z + z0))
        found.append({"cells": len(voids),
                      "min": (min(c[0] for c in voids), min(c[1] for c in voids),
                              min(c[2] for c in voids)),
                      "max": (max(c[0] for c in voids), max(c[1] for c in voids),
                              max(c[2] for c in voids)),
                      "sealed": not any(sky[index] for index in held),
                      "voids": voids})
    found.sort(key=lambda entry: -entry["cells"])
    return found


def sightline_mass(blocks, voids):
    """The solid cells standing between the camera and a roofed void.

    The camera is at (+inf, +inf, +inf), so the line of sight out of a block is the diagonal (+1, +1, +1)
    and every block on one line shares the pair `(x - y, z - y)`. A single void cell opens its whole line,
    so only the lowest void on each line has to be found: everything solid above it on that line is
    exactly what the world is hiding the room with, and nothing else is."""
    if not voids:
        return set()
    top = max(cell[1] for cell in blocks)
    lowest = {}
    for x, y, z in voids:
        line = (x - y, z - y)
        if y < lowest.get(line, top + 1):
            lowest[line] = y
    hidden = set()
    for (across, into), floor in lowest.items():
        for y in range(floor + 1, top + 1):
            cell = (across + y, y, into + y)
            if cell in blocks:
                hidden.add(cell)
    return hidden


# What the veil keeps of a block it washes out. Nearly none: a hillside drawn over a room at even a
# sixth of its opacity still tints the whole room its own green, and a room read through a green wash is
# a room whose floor material cannot be named. Grey reads as glass and leaves the chroma to the subject.
VEIL_CHROMA = 0.9


def xray(payload, path, scale=6, layers=None, clip=None, title=None, caption=None, margin=40,
         quarter=0, veil=0.15, calm=0.6, min_void=6, max_headroom=24, keep=None):
    """The board with whatever hides a roofed room taken down to a wash, so the room is in the picture.

    `isometric` cannot show anything underground: the terrain over a chamber is nearer the camera and is
    painted last, so a gaol under a meadow renders as a meadow. What an x-ray has to mean here is
    therefore narrow and mechanical — **nothing that stands between the camera and a roofed void may
    paint over it** — and the three classes fall out of that one sentence:

    - the **veil**, `sightline_mass` above: every solid cell on the (+1, +1, +1) diagonal out of a roofed
      void. Drawn at `veil` opacity and near enough grey, and only its own outer skin, so the hill still
      reads as a hill and the room reads straight through it. This is an automatic cutaway — it opens the
      hillside exactly as far as the sight-line into the room and no further, and on a board with nothing
      roofed it is empty, which makes the view degrade to `isometric` rather than to a wrong picture.
    - the **lining**, every solid cell with a face onto that void: the floor, the far walls, and whatever
      stands on the floor. Drawn opaque at the block's own colour, because it is the subject.
    - everything else, the **mass**. Drawn opaque but pulled `calm` of the way to grey, so the room's real
      block colours are the only chroma in the frame.

    **`keep` names the layers the veil may not touch**, and something has to. A brazier standing on a room's
    floor genuinely stands between the camera and the air behind it, so the sight-line rule washes it out
    exactly as it washes out the ceiling — the rule is right about enclosure and cannot tell a lamp from a
    lid. Nothing in the block set can: a chamber's ceiling is adjacent to its void and so is the fire in the
    middle of it, and every test that separates them by shape needs a number nobody can defend. What does
    separate them is the document, which already says so — a layer of `kind: "prop"` is a *made thing* and
    a made thing in a room is the subject of the picture. So the caller that holds the layout names those
    storeys, and `drive.py` does exactly that. `keep` reads its layer names the way `layers` does, so the
    unattributed runs — the structures and the props the dressing pass placed — come with them.

    Four other readings were weighed. Drawing the whole board at reduced alpha turns twenty courses of
    overburden into an opaque smear and loses the very structure it was supposed to reveal. Cutting at a
    stated Y or plane needs the author to already know where the room is, which is what the picture was
    for. Drawing the void's bounding shell alone reveals nothing either, because a chamber's ceiling is
    part of that shell and is what the camera hits first. And drawing made things opaque over ghosted
    terrain cannot separate them at all here: a cell block and the rock around it are drawn on the same
    sketch layer, so layer attribution says they are one thing while void adjacency says which is which.

    The voids are measured on the whole board, before `layers` and `clip` are applied, so clipping to a
    room frames the camera without opening the room's own roof.

    Returns the cavity table `cavities` answered — cell counts and block bounds, which is what a finding
    about a room is reported with."""
    whole = turned(voxels(payload), quarter)
    if not whole:
        raise SystemExit("nothing to draw")
    found = cavities(whole, min_cells=min_void, max_headroom=max_headroom)
    voids = set().union(*(entry["voids"] for entry in found)) if found else set()

    lining = set()
    for x, y, z in voids:
        for cell in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                     (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if cell in whole:
                lining.add(cell)
    hidden = sightline_mass(whole, voids)
    if keep:
        hidden -= set(turned(voxels(payload, layers=keep), quarter))

    blocks = whole if layers is None and clip is None else \
        turned(voxels(payload, layers=layers, clip=clip), quarter)
    solid, veiled = {}, {}
    for cell, colour in blocks.items():
        if cell in hidden:
            veiled[cell] = desaturate(colour, VEIL_CHROMA)
        elif cell in lining:
            solid[cell] = colour
        else:
            solid[cell] = desaturate(colour, calm)

    # Two culls, not one. A cell hidden only by veiled mass is now visible and has to be drawn, so the
    # opaque pass is culled against the opaque set alone; the veil is culled against itself, which leaves
    # one skin rather than a stack of washes deep enough to be opaque again.
    shown = {cell: solid[cell] for cell in _visible(solid)}
    skin = {cell: veiled[cell] for cell in _visible(veiled)}
    merged = dict(shown)
    merged.update(skin)

    w, h, k = scale, scale // 2 or 1, scale
    u0, u1, v0, v1 = iso_bounds(merged, w, h, k)
    if caption is None:
        caption = (f"nothing roofed - {len(blocks)} blocks"
                   if not found else
                   f"{len(found)} roofed void(s), {sum(1 for e in found if e['sealed'])} sealed. "
                   f"largest {found[0]['cells']} cells at "
                   f"x {found[0]['min'][0]}..{found[0]['max'][0]} "
                   f"y {found[0]['min'][1]}..{found[0]['max'][1]} "
                   f"z {found[0]['min'][2]}..{found[0]['max'][2]}")
    head = 46 if title else 0
    foot = 34 if caption else 0
    width = max(int(u1 - u0) + margin * 2,
                margin * 2 + max(len(title or "") * 18, len(caption or "") * 12))
    canvas = Canvas(width, int(v1 - v0) + margin * 2 + head + foot, BACKGROUND)
    draw_iso(canvas, merged, (margin - u0, margin - v0 + head), w, h, k,
             alpha={cell: veil for cell in skin})
    if title:
        canvas.text(margin, 14, title, (25, 25, 30), 3)
    if caption:
        canvas.text(margin, canvas.height - 24, caption, (110, 110, 118), 2)
    write_png(path, canvas)
    return found


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
