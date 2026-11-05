"""The mountain band: one continuous surface round the valley, in two styles that meet.

The band is solved as a field over its columns rather than built from separate pieces, so nowhere can one piece
stand as a cliff against the next. Three fields are solved on the same columns, each pinned at fixed columns and
relaxed everywhere else:

- `style`, pinned to 1 where the sketch's mountain was light blue and 0 where it was yellow, which says which of the
  two styles a column takes and where they meet;
- `across`, pinned to 0 against the valley and 1 at the map's edge, which says how far across the band a column is;
- `base`, pinned to the height of whatever the band meets on its inner side and to the edge height outside it.

The surface is the base plus each style's profile across the band and its own detail: a plateau with a gentle swell
for the flatter style, a ridge with jagged noise for the erratic one. A last pass caps the step between neighbouring
columns at each style's own limit, so the surface climbs at a rate a style allows and never more.
"""
import math

N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def relax(domain, fixed, initial, iterations=400, omega=1.9):
    """A Laplace solution over `domain` (a set of columns) with `fixed` columns held at their values. A domain column
    with no fixed or domain neighbour on a side takes no value from that side."""
    order = sorted(domain)
    index = {c: i for i, c in enumerate(order)}
    links, constant, counts = [], [], []
    for (x, z) in order:
        own, held, count = [], 0.0, 0
        for dx, dz in N4:
            n = (x + dx, z + dz)
            if n in index:
                own.append(index[n]); count += 1
            elif n in fixed:
                held += fixed[n]; count += 1
        links.append(own); constant.append(held); counts.append(count)
    value = [initial.get(c, 0.0) for c in order]
    for _ in range(iterations):
        for i in range(len(order)):
            if not counts[i]:
                continue
            total = constant[i]
            for j in links[i]:
                total += value[j]
            value[i] += omega * (total / counts[i] - value[i])
    return {c: value[i] for c, i in index.items()}


def _hash(ix, iz, seed):
    h = (ix * 374761393 + iz * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def value_noise(x, z, period, seed):
    """Smooth noise in [0, 1] with features about `period` blocks across."""
    fx, fz = x / period, z / period
    ix, iz = math.floor(fx), math.floor(fz)
    tx, tz = fx - ix, fz - iz
    sx, sz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
    a = _hash(ix, iz, seed); b = _hash(ix + 1, iz, seed)
    c = _hash(ix, iz + 1, seed); d = _hash(ix + 1, iz + 1, seed)
    return (a + (b - a) * sx) + ((c + (d - c) * sx) - (a + (b - a) * sx)) * sz


def ridged(x, z, periods, seed):
    """Sharp-crested noise in [0, 1]: each octave folded about its middle, so its crests are creases."""
    total, weight, norm = 0.0, 1.0, 0.0
    for k, period in enumerate(periods):
        n = 1.0 - abs(2.0 * value_noise(x, z, period, seed + 17 * k) - 1.0)
        total += weight * n * n; norm += weight; weight *= 0.55
    return total / norm


def smoothstep(a, b, v):
    t = min(1.0, max(0.0, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)


CREST, CREST_ROOM = 78.0, 12.0      # heights above the crest are eased in toward it plus its room, so peaks stop near 90

STYLES = {
    # the flatter style: up from the valley to a plateau, a gentle swell on it, down again at the map's edge
    "flat": {"rise": 17.0, "detail": 2.5, "step": 1.5,
             "profile": lambda t: smoothstep(0.0, 0.35, t) * (1.0 - 0.6 * smoothstep(0.85, 1.0, t))},
    # the erratic style: a ridge across the band with jagged crests, steeper wherever it climbs
    "erratic": {"rise": 32.0, "detail": 11.0, "step": 3.0,
                "profile": lambda t: math.sin(math.pi * min(1.0, max(0.0, t)) ** 0.75)},
}


def surface(band, inner_height, edge_cells, style_pins, floor_under, seed=7):
    """Heights and styles for every band column.

    `inner_height` maps each column the band meets on its inner side to the height it meets it at; `edge_cells` are
    the columns just outside the map; `style_pins` maps columns to 1 (erratic) or 0 (flat); `floor_under` maps band
    columns to the lowest height their surface may take, so whatever is buried under the band stays buried."""
    style = relax(band - set(style_pins), style_pins, {c: 0.5 for c in band})
    style.update({c: v for c, v in style_pins.items() if c in band})
    across = relax(band, {**{c: 0.0 for c in inner_height}, **{c: 1.0 for c in edge_cells}}, {c: 0.5 for c in band})
    weight = {c: smoothstep(0.42, 0.58, style[c]) for c in band}
    edge_height = {}
    for c in edge_cells:
        near = [weight[(c[0] + dx, c[1] + dz)] for dx, dz in N4 if (c[0] + dx, c[1] + dz) in weight]
        edge_height[c] = 40.0 + 14.0 * (sum(near) / len(near) if near else 0.0)
    base = relax(band, {**inner_height, **edge_height}, {c: 40.0 for c in band})

    height = {}
    for c in band:
        x, z = c
        t = across[c]
        w = weight[c]
        flat, erratic = STYLES["flat"], STYLES["erratic"]
        lift_flat = flat["rise"] * flat["profile"](t) + flat["detail"] * (value_noise(x, z, 22, seed) - 0.5)
        lift_erratic = erratic["profile"](t) * (erratic["rise"] + erratic["detail"] * (ridged(x, z, (18, 9, 4), seed) - 0.4))
        raw = base[c] + (1 - w) * lift_flat + w * lift_erratic
        height[c] = raw if raw < CREST else CREST + CREST_ROOM * math.tanh((raw - CREST) / CREST_ROOM)

    # cap the climb between neighbours at each style's step; never below what the band must bury
    for c, low in floor_under.items():
        if c in height and height[c] < low: height[c] = low
    step = {c: (1 - weight[c]) * STYLES["flat"]["step"] + weight[c] * STYLES["erratic"]["step"] for c in band}
    ground = dict(inner_height)
    for _ in range(60):
        changed = 0
        for c in band:
            x, z = c
            lows = [height[n] if n in height else ground[n] for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))
                    if n in height or n in ground]
            if not lows:
                continue
            limit = max(floor_under.get(c, -1e9), min(lows) + step[c])
            if height[c] > limit + 1e-6:
                height[c] = limit; changed += 1
        if not changed:
            break
    # a column lifted over something buried spreads its lift to its neighbours at their own step, so it stands
    # as a slope rather than a pillar
    for _ in range(60):
        changed = 0
        for c in band:
            x, z = c
            highs = [height[n] for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)) if n in height]
            if highs and height[c] < max(highs) - step[c] - 1e-6:
                height[c] = max(highs) - step[c]; changed += 1
        if not changed:
            break
    return {c: (round(height[c]), weight[c] >= 0.5) for c in band}, across
