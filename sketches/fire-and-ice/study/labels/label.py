"""Label the spaces of the fire-and-ice map's built half for the 3D viewer.

Run:  python3 -I label.py <world>/region            (writes labels.json and labels_q*.png beside this file)

Reads the raw world through the mapgen anvil reader and the viewer's layer table through variants/kit.py.
Geometry only: standable air (2 high over a solid floor) under a structure ceiling, split into stairs (the floor
climbs), rooms (a 5x5 square fits) and tunnels (the rest, if long); openings are where a space's air touches air
open to the sky or to the hollow under the terrain shell; the facade is the exterior air in front of the main
building's east face. Names are attached afterwards by anchor cells chosen by hand (NAMES below).
"""
import collections
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.dirname(HERE)
REGION = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("FIRE_ICE_REGION", "")   # the author's world: its region folder
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools")))
sys.path.insert(0, os.path.join(SCRATCH, "variants"))
from anvil import World  # noqa: E402
import kit  # noqa: E402

BOX = (-16, 105, -57, 102)
STAIRS = {53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180}
SLABS = {44, 126, 182}
LADDER = 65
# blocks a player walks through
PASS = {0, 6, 31, 32, 37, 38, 39, 40, 50, 55, 59, 63, 65, 68, 69, 70, 72, 75, 76, 77, 78, 83, 104, 105, 106, 115,
        131, 132, 141, 142, 143, 147, 148, 151, 171, 175, 178, 8, 9}
LAVA = {10, 11}
GLAZING = {20, 95, 102, 160, 101}
H4 = ((1, 0), (-1, 0), (0, 1), (0, -1))

# ------------------------------------------------------------------ the world
W = World(REGION)
BLK = {(x, y, z): (i, d) for x, y, z, i, d in W.blocks() if BOX[0] <= x <= BOX[1] and BOX[2] <= z <= BOX[3]}
LAYER = kit.existing()


def passable(p):
    b = BLK.get(p)
    return b is None or b[0] in PASS


def solid(p):
    b = BLK.get(p)
    return b is not None and b[0] not in PASS and b[0] not in LAVA


def group(p):
    b = BLK.get(p)
    if b is None: return None
    if b[0] == 7: return "Bauwerke"
    return LAYER.get(p, (None, "?"))[1]


def floor_is_step(c):
    b = BLK.get((c[0], c[1] - 1, c[2]))
    return b is not None and (b[0] in STAIRS or (b[0] in SLABS and not b[1] & 8))


# standable cells: feet and head passable, floor solid (ladder cells count as standable too)
STAND = set()
for (x, y, z), b in BLK.items():
    if solid((x, y, z)) and passable((x, y + 1, z)) and passable((x, y + 2, z)):
        STAND.add((x, y + 1, z))
    if b[0] == LADDER and passable((x, y + 1, z)):
        STAND.add((x, y, z))

CEIL = {}
for c in STAND:
    for yy in range(c[1] + 2, c[1] + 30):
        if solid((c[0], yy, c[2])):
            CEIL[c] = yy
            break
COVERED = {c for c, cy in CEIL.items() if group((c[0], cy, c[2])) in ("Bauwerke", "Untergrund")}


def walk(c, cells, drop=1):
    """Neighbours a player reaches from c inside `cells`: a step up of one with headroom, or down by up to `drop`."""
    x, y, z = c
    for dx, dz in H4:
        for dy in [0, 1] + [-k for k in range(1, drop + 1)]:
            n = (x + dx, y + dy, z + dz)
            if n not in cells: continue
            if dy == 1 and not passable((x, y + 2, z)): continue
            if dy < 0 and not all(passable((x + dx, y + k, z + dz)) for k in range(dy + 1, 2)): continue
            yield n
    for dy in (1, -1):                                   # ladders
        n = (x, y + dy, z)
        if n in cells and (BLK.get(c, (0,))[0] == LADDER or BLK.get(n, (0,))[0] == LADDER): yield n


def components(cells, drop=1):
    seen, out = set(), []
    for c in sorted(cells):
        if c in seen: continue
        stack, comp = [c], []
        seen.add(c)
        while stack:
            u = stack.pop(); comp.append(u)
            for n in walk(u, cells, drop):
                if n not in seen: seen.add(n); stack.append(n)
            for n in list(walk_back(u, cells, drop)):
                if n not in seen: seen.add(n); stack.append(n)
        out.append(comp)
    return sorted(out, key=len, reverse=True)


def walk_back(c, cells, drop):
    """Cells from which c is reached (so components are undirected)."""
    x, y, z = c
    for dx, dz in H4:
        for dy in [0, -1] + [k for k in range(1, drop + 1)]:
            n = (x + dx, y + dy, z + dz)
            if n in cells and c in set(walk(n, cells, drop)): yield n


# ------------------------------------------------------------------ enclosure: rays at feet and head height
RAYS = [(math.cos(a * math.pi / 8), math.sin(a * math.pi / 8)) for a in range(16)]


def enclosure(c, reach=20):
    x, y, z = c
    hit = 0
    for dx, dz in RAYS:
        for k in range(1, reach + 1):
            px, pz = round(x + dx * k), round(z + dz * k)
            if solid((px, y, pz)) or solid((px, y + 1, pz)): hit += 1; break
    return hit / 16


# ------------------------------------------------------------------ split one component
def at_level(cells, x, z, y):
    for dy in (0, 1, -1):
        if (x, y + dy, z) in cells: return True
    return False


def split(comp):
    """[(kind, cells)] for one connected space: stair / room / tunnel, small leftovers merged into a neighbour."""
    C = set(comp)
    nb = {c: set(walk(c, C)) | set(walk_back(c, C, 1)) for c in C}
    step = {c for c in C if floor_is_step(c) or any(n[1] != c[1] for n in nb[c])}
    stairs = []
    for sc in components(step):
        ys = [p[1] for p in sc]
        if max(ys) - min(ys) >= 3: stairs.append(set(sc))
    stair_cells = set().union(*stairs) if stairs else set()
    rest = C - stair_cells
    # erosion depth: how many 8-neighbourhood erosions a cell survives (a step of one in y counts as level)
    E, depth, k = set(C), {c: 0 for c in rest}, 0
    while True:
        k += 1
        E2 = {c for c in E if all(at_level(E, c[0] + dx, c[2] + dz, c[1]) for dx in (-1, 0, 1) for dz in (-1, 0, 1))}
        if not E2: break
        for c in E2:
            if c in depth: depth[c] = k
        E = E2
    room = set()
    for c in rest:
        if depth[c] >= 2:
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    for dy in (-1, 0, 1):
                        n = (c[0] + dx, c[1] + dy, c[2] + dz)
                        if n in rest: room.add(n)
    parts = [["stair", s] for s in stairs]
    small = set()
    for rc in components(room):
        if len(rc) >= 30: parts.append(["room", set(rc)])
        else: small |= set(rc)
    narrow = (rest - room) | small
    pending = []
    for nc in components(narrow):
        nc = set(nc)
        xs, zs, ys = [p[0] for p in nc], [p[2] for p in nc], [p[1] for p in nc]
        length = max(max(xs) - min(xs), max(zs) - min(zs)) + 1
        touching = collections.Counter()
        for c in nc:
            for n in nb[c]:
                for i, (kind, cells) in enumerate(parts):
                    if n in cells: touching[i] += 1
        kinds = {parts[i][0] for i in touching}
        if touching and kinds == {"stair"} and len(nc) <= 40 and length <= 8:
            pending.append((nc, touching.most_common(1)[0][0]))      # a landing between flights
        elif length >= 6:
            parts.append(["tunnel", nc])
        elif touching:
            pending.append((nc, touching.most_common(1)[0][0]))      # a niche or doorway
        else:
            parts.append(["room" if len(nc) >= 12 else "tunnel", nc])
    for nc, i in pending: parts[i][1] |= nc
    # stair parts that now touch each other are one stairwell
    merged = True
    while merged:
        merged = False
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                if parts[i][0] == parts[j][0] == "stair" and any(n in parts[j][1] for c in parts[i][1] for n in nb[c]):
                    parts[i][1] |= parts[j][1]; del parts[j]; merged = True; break
            if merged: break
    return parts, nb


# ------------------------------------------------------------------ the spaces
WALL_TOPS = {"Orange", "Rot", "Rosa", "Schwarz"}       # standing on these is standing on a wall, a ceiling or a roof


def build():
    cells = {c for c in COVERED if LAYER.get((c[0], c[1] - 1, c[2]), ("",))[0] not in WALL_TOPS}
    comps = components(cells)
    spaces = []                      # dicts: kind, cells (standable), comp index
    for ci, comp in enumerate(comps):
        if len(comp) < 12: continue
        ys = [p[1] for p in comp]
        enc = sum(enclosure(p) for p in comp) / len(comp)
        has_stair = any(floor_is_step(p) for p in comp) and max(ys) - min(ys) >= 4
        if enc < 0.45 and not has_stair: continue
        if len(comp) < 30 and enc < 0.75: continue        # ledges, window sills, the facade's steps
        parts, nb = split(comp)
        for kind, cells in parts:
            if len(cells) < 6: continue
            spaces.append({"kind": kind, "cells": set(cells), "comp": ci})
    return comps, spaces


def volume(cells, cap=30):
    """The air above standable cells up to the ceiling (at most `cap` high)."""
    out = set()
    for (x, y, z) in cells:
        for yy in range(y, y + cap):
            if not passable((x, yy, z)) or (BLK.get((x, yy, z), (0,))[0] in LAVA): break
            out.add((x, yy, z))
    return out


def roof_group(p):
    """Group of the first solid block above p, or None for open sky."""
    x, y, z = p
    for yy in range(y + 1, 101):
        if solid((x, yy, z)): return group((x, yy, z))
    return None


def exterior(occupied):
    """Air outside every structure: a flood from above the map through air that is no space's and has open sky or
    terrain (the hollow under the terrain shell) over it, never a structure's roof."""
    X0, X1, Z0, Z1 = BOX
    Y1 = 100
    ext = set()
    stack = [(x, Y1, z) for x in range(X0 - 1, X1 + 2) for z in range(Z0 - 1, Z1 + 2)]
    for p in stack: ext.add(p)
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)):
            n = (x + dx, y + dy, z + dz)
            if n in ext or not (X0 - 1 <= n[0] <= X1 + 1 and Z0 - 1 <= n[2] <= Z1 + 1 and -1 <= n[1] <= Y1): continue
            if not passable(n) or n in occupied: continue
            if roof_group(n) in ("Bauwerke", "Untergrund"): continue
            ext.add(n); stack.append(n)
    # then up to four cells in under an overhang, a porch or a facade's recess
    front = list(ext)
    for _ in range(4):
        nxt = []
        for x, y, z in front:
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, -1, 0)):
                n = (x + dx, y + dy, z + dz)
                if n in ext or n in occupied or not passable(n): continue
                if not (X0 - 1 <= n[0] <= X1 + 1 and Z0 - 1 <= n[2] <= Z1 + 1 and n[1] >= -1): continue
                ext.add(n); nxt.append(n)
        front = nxt
    return ext


def sky(p):
    x, y, z = p
    return not any(solid((x, yy, z)) for yy in range(y + 1, 101))


def openings(spaces, vol_of, ext):
    """Per space: clusters of its air cells that touch exterior air sideways or from above.
    Returns [(space index, cells, kind, leads)] where kind is door (reachable on foot) or window, and leads says
    whether the air outside is open sky or the hollow under the terrain."""
    out = []
    for si, s in enumerate(spaces):
        vol = vol_of[si]
        floor = s["cells"]
        touch = {}
        for c in vol:
            for dx, dz in H4:
                n = (c[0] + dx, c[1], c[2] + dz)
                if n in ext and n not in vol: touch.setdefault(c, []).append(n)
        # cluster (26-neighbourhood)
        seen = set()
        for c in sorted(touch):
            if c in seen: continue
            stack, cl = [c], []
            seen.add(c)
            while stack:
                u = stack.pop(); cl.append(u)
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        for dz in (-1, 0, 1):
                            n = (u[0] + dx, u[1] + dy, u[2] + dz)
                            if n in touch and n not in seen: seen.add(n); stack.append(n)
            outside = {n for u in cl for n in touch[u]}
            walk_out = any(u in floor and any(n in STAND or (n[0], n[1] - 1, n[2]) in STAND or (n[0], n[1] + 1, n[2]) in STAND
                                              for n in touch[u]) for u in cl)
            # a door also when the outside cell at feet height has a floor within a 3-block drop
            if not walk_out:
                for u in cl:
                    if u not in floor: continue
                    for n in touch[u]:
                        if any(solid((n[0], n[1] - k, n[2])) for k in range(1, 4)): walk_out = True
            hollow = sum(1 for n in outside if roof_group(n) == "Gelände")
            out.append((si, set(cl), "door" if walk_out else "window", "hollow" if hollow * 2 > len(outside) else "outside"))
    return out


# ------------------------------------------------------------------ names, chosen by hand from the geometry
# Each entry: anchor cells (any standable cell of a part puts that part under this label), id, kind, name, note.
# Parts not named here and not in DROP are written with a generic name.
NAMES = [
    # the main building ("Bunker")
    ([(11, 24, 11)], "hall", "room", "Große Halle (EG)",
     "Erdgeschoss, Boden y23, L-förmig x3–32/z−7…22; Decke hellgrau y37; offen nach Osten zum Talboden"),
    ([(-4, 24, 29)], "gang-west-eg", "tunnel", "Gang West (EG)", "2 breit, y24, vom Südende der Halle zum Treppenhaus West"),
    ([(-8, 44, 24)], "stair-west", "stair", "Treppenhaus West",
     "Wendeltreppe in drei Läufen y24→y48, x−14…−1, z19–25; geschlossen"),
    ([(6, 48, 26)], "gang-og", "tunnel", "Gang OG (y48)", "2–4 breit, vom Treppenhaus West zum Core-Raum"),
    ([(21, 48, 28), (30, 48, 24)], "core-room", "room", "Core-Raum (y48)",
     "westlich des Kerns, Boden y47; der Ostrand steht auf der Oberseite des Obsidian-Kerns x27–31"),
    ([(4, 17, 40)], "stair-down", "stair", "Treppe zum Untergeschoss", "von der Halle (y24) hinab auf y17, x3–4"),
    ([(22, 17, 30)], "tunnel-core", "tunnel", "Gang zur Core-Grube", "y17, 2 breit, x3–26, unter dem Südflügel"),
    ([(29, 17, 28)], "core-pit", "room", "Grube unter dem Core",
     "y17 unter dem Kern (x27–31, z22–33), Boden violett; nach Osten offen zur Rampe"),
    ([(3, 48, 29), (2, 51, 39), (11, 47, 43)], "stair-south", "stair", "Treppe Süd",
     "vom Gang OG (y48) hinauf auf y54, dann nach Osten hinab auf y43; zwei Ausgänge nach Süden ins Freie"),
    ([(19, 66, 26), (19, 63, 44), (19, 61, 38)], "attic", "room", "Dachgeschoss",
     "unter dem schwarzen Dach: U-förmiger Umgang y63, Nordteil bis y67, abgesenkte Mitte y61 (ohne Verbindung); kein Zugang"),
    ([(12, 55, 25), (22, 56, 21)], "room-55", "room", "Raum y55 (Nordwest)", "über dem Gang OG, oben offen; kein Zugang von innen gefunden"),
    ([(3, 28, 26)], "stair-sw", "stair", "Treppe Südwest (y21–28)", "kurze Treppe im Südwestblock, ohne Anschluss an die Halle"),
    ([(22, 26, 33)], "chamber-26", "room", "Kammer westlich des Core (y26)", "geschlossen, kein Zugang gefunden"),
    ([(-7, 33, 23)], "stair-west-out", "stair", "Treppe West außen", "y28→36 an der Westseite, zum Freien offen"),
    ([(22, 56, 33)], "cavity-56", "tunnel", "Hohlraum Südwand (y56)", "2 breit, geschlossen"),
    ([(25, 36, 25)], "chamber-core-36", "room", "Kammer hinter dem Core (y36)", "4×6, direkt westlich der Lava, geschlossen"),
    ([(14, 36, 15)], "shaft-36", "tunnel", "Zwischenraum über der Halle (y36)", "2–4 breit, x12–15, z8–18, in der Hallendecke, oben offen"),
    # the underground and the hill
    ([(90, 7, -5)], "wool-lane", "tunnel", "Wool-Lane",
     "unterirdisch, Boden y4–8, 12–25 breit; Eingänge West (x67–72, z4–9) und Süd (z23–27); Void-Loch x89–94, z−2…3"),
    ([(66, 10, -14), (78, 8, -18)], "lane-west", "tunnel", "Wool-Lane, Westarm", "y10, 13 breit, von der Halle zum Treppenturm"),
    ([(60, 11, -24), (60, 31, -31)], "stair-wool", "stair", "Treppenturm zur Wolle",
     "Wendeltreppe 2 breit y10→y50, x56–61, z−39…−23"),
    ([(57, 50, -38)], "wool-room", "room", "Wollraum (?)",
     "y50 auf dem Hang, Truhen an der Nordwand (x52–56, z−39), Beacon unter Glas bei x55, z−35"),
    ([(55, 27, -25)], "stub-27", "tunnel", "Stichgang (y27)",
     "zweigt auf y27 vom Treppenturm ab, x47–64; beide Enden (x47, x64) offen, ohne Fortsetzung"),
    ([(59, 22, -34)], "stair-blind", "stair", "Zweites Treppenhaus",
     "4 breit y15→y45 neben dem Treppenturm; unten an der Lane-Wand z−24 zu, seitlich zum Hohlraum offen"),
    ([(79, 5, -5)], "lane-pocket", "tunnel", "Kammer unter der Lane", "y3–6, x77–81, z−6…1, geschlossen"),
    ([(84, 8, 23)], "lane-steps", "stair", "Stufen am Lane-Südende", "x83–85, z19–25, y6→9"),
]
# parts that are not spaces: the black roof's eaves and gables, a sill in the wool room
DROP = [(8, 64, 45), (30, 64, 43), (19, 63, 47), (19, 68, 22), (59, 52, -36)]
OPENING_NAMES = [   # anchor (any cell of the opening), id, name
    ((33, 24, 0), "op-hall-east", "Hallentor Ost"),
    ((31, 17, 27), "op-core-pit", "Mündung der Core-Grube zur Rampe"),
    ((30, 48, 27), "op-core-top", "Öffnung über dem Kern"),
    ((68, 5, 6), "op-lane-west", "Lane-Eingang West"),
    ((94, 7, 25), "op-lane-south", "Lane-Eingang Süd"),
    ((91, 8, 0), "op-lane-hole", "Void-Loch in der Lane"),
    ((100, 8, 4), "op-lane-east", "Lane-Ostseite offen"),
]


def facade(occupied, ext):
    """Exterior air directly east of the main building's east face: for every (y, z) row, scan west from x 56
    through exterior air; the last exterior cell before a structure block or a space is a facade cell. Recesses
    deeper than six blocks behind the front of their z are left out."""
    cells = set()
    for z in range(-22, 48):
        for y in range(16, 73):
            last = None
            for x in range(56, 20, -1):
                p = (x, y, z)
                if p in ext:
                    last = p; continue
                if p in occupied or group(p) == "Bauwerke" or BLK.get(p, (0,))[0] in LAVA:
                    if last is not None: cells.add(last)
                break
    # keep the front: at most six blocks behind the eastmost facade cell of the same z
    front = {}
    for x, y, z in cells: front[z] = max(front.get(z, x), x)
    return {c for c in cells if c[0] >= front[c[2]] - 6}


def main():
    comps, spaces = build()
    # attach names: every anchor names the part with the floor cell nearest to it (within four blocks)
    def dist(a, c): return max(abs(a[0] - c[0]), abs(a[1] - c[1]), abs(a[2] - c[2]))

    def nearest(a, candidates):
        best = min(((min(dist(a, c) for c in cells), i) for i, cells in candidates), default=(99, None))
        return best[1] if best[0] <= 4 else None

    cand = [(i, s["cells"]) for i, s in enumerate(spaces)]
    named = {}
    for k, (cells, lid, kind, name, note) in enumerate(NAMES):
        for a in cells:
            i = nearest(a, cand)
            if i is not None and i not in named: named[i] = k
    dropped = {nearest(a, cand) for a in DROP}
    labels, order, generic = {}, [], collections.Counter()
    for i, s in enumerate(spaces):
        if i in dropped: continue
        if i in named:
            k = named[i]
            lid = NAMES[k][1]
            if lid not in labels:
                labels[lid] = {"id": lid, "kind": NAMES[k][2], "name": NAMES[k][3], "note": NAMES[k][4], "floor": set()}
                order.append(lid)
            labels[lid]["floor"] |= s["cells"]
        else:
            generic[s["kind"]] += 1
            lid = f"{s['kind']}-{generic[s['kind']]}"
            word = {"room": "Raum", "tunnel": "Gang", "stair": "Treppe"}[s["kind"]]
            labels[lid] = {"id": lid, "kind": s["kind"], "name": f"{word} {generic[s['kind']]}",
                           "note": "ohne Namen: Zweck aus der Geometrie nicht ablesbar", "floor": set(s["cells"])}
            order.append(lid)
    missing = [n[1] for n in NAMES if n[1] not in labels]
    if missing: print("names without a part:", missing)
    floor_of = {}
    for lid in order:
        lab = labels[lid]
        lab["air"] = volume(lab["floor"])
        for c in lab["floor"]: floor_of[c] = lid
    occupied = set().union(*(labels[l]["air"] for l in order))
    ext = exterior(occupied)
    # links between spaces: a step (or a drop of up to three) from one floor onto another
    allfloor = set(floor_of)
    links = collections.defaultdict(set)
    for c, lid in floor_of.items():
        for n in walk(c, allfloor, drop=3):
            other = floor_of[n]
            if other != lid: links[lid].add(other); links[other].add(lid)
    # openings
    pseudo = [{"cells": labels[l]["floor"]} for l in order]
    ops = openings(pseudo, [labels[l]["air"] for l in order], ext)
    # openings: named ones on their own; the rest gathered per space by (walkable, where it leads)
    groups = collections.OrderedDict()
    for si, cl, kind, leads in ops:
        if len(cl) < 2: continue
        named = [(oid, nm) for a, oid, nm in OPENING_NAMES if min(dist(a, c) for c in cl) <= 3]
        key = named[0] if named else (order[si], "", "")
        g = groups.setdefault(key, {"host": order[si], "kind": set(), "leads": set(), "air": set(), "parts": 0})
        g["air"] |= cl; g["parts"] += 1; g["kind"].add(kind); g["leads"].add(leads)
    opening_labels = []
    count = collections.Counter()
    for key, g in groups.items():
        host = g["host"]
        if len(key) == 2: oid, nm = key
        else:
            count[host] += 1
            oid = f"op-{host}"
            nm = ("Durchgang" if g["kind"] == {"door"} else "Fenster" if g["kind"] == {"window"} else "Öffnungen") + (
                f" ({g['parts']}×)" if g["parts"] > 1 else "")
        where = " und ".join(sorted({"in den Hohlraum unter dem Gelände" if l == "hollow" else "ins Freie" for l in g["leads"]}))
        walkable = "begehbar" if g["kind"] == {"door"} else "nicht begehbar" if g["kind"] == {"window"} else "teils begehbar"
        cl = g["air"]
        xs, ys, zs = [p[0] for p in cl], [p[1] for p in cl], [p[2] for p in cl]
        note = f"{walkable} {where}; x{min(xs)}…{max(xs)}, y{min(ys)}…{max(ys)}, z{min(zs)}…{max(zs)}"
        opening_labels.append({"id": oid, "kind": "opening", "name": nm, "note": note, "air": cl, "links": [host]})
        links[host].add(oid)
    # the facade
    fac = facade(occupied, ext)
    fac_label = {"id": "facade", "kind": "facade", "name": "Fassade Ost",
                 "note": "Außenluft vor der Ostseite des Bunkers zum Talboden, mit dem Kern; "
                         f"x{min(p[0] for p in fac)}…{max(p[0] for p in fac)}, y{min(p[1] for p in fac)}…{max(p[1] for p in fac)}, "
                         f"z{min(p[2] for p in fac)}…{max(p[2] for p in fac)}",
                 "air": fac, "links": []}
    for o in opening_labels:
        if len(o["air"] & {(x + 1, y, z) for (x, y, z) in fac} | (o["air"] & fac)) or any(
                (x + 1, y, z) in fac or (x - 1, y, z) in fac for (x, y, z) in o["air"]):
            fac_label["links"].append(o["id"]); o["links"].append("facade")
    # write
    out = []

    def centre(cells):
        n = len(cells)
        return [round(sum(p[i] for p in cells) / n) for i in range(3)]

    for lid in order:
        lab = labels[lid]
        cells = sorted(lab["air"])
        out.append({"id": lid, "kind": lab["kind"], "name": lab["name"], "note": lab["note"],
                    "cells": [v for p in cells for v in p], "centre": centre(lab["floor"]),
                    "links": sorted(links[lid])})
    for o in opening_labels + [fac_label]:
        cells = sorted(o["air"])
        out.append({"id": o["id"], "kind": o["kind"], "name": o["name"], "note": o["note"],
                    "cells": [v for p in cells for v in p], "centre": centre(cells), "links": sorted(set(o["links"]))})
    path = os.path.join(HERE, "labels.json")
    json.dump({"labels": out}, open(path, "w"), separators=(",", ":"), ensure_ascii=False)
    print(path, os.path.getsize(path), "bytes,", len(out), "labels")
    for o in out:
        print(f"{o['id']:22s} {o['kind']:8s} {len(o['cells']) // 3:6d} {o['centre']} {o['name']} -> {','.join(o['links'])}")
    return out, labels, order, opening_labels, fac


KIND_WOOL = {"room": 1, "tunnel": 4, "stair": 2, "opening": 5, "facade": 3}
SPECIAL_WOOL = {"core-room": 14, "core-pit": 14, "wool-room": 0, "wool-lane": 9, "lane-west": 9, "hall": 11}


def render(out):
    """Iso checks through kit.render: each label's floor cells (openings and facade: all cells) in a wool colour by
    kind; red the core spaces, white the wool room, cyan the lane, blue the hall. Three cuts so the floors show."""
    def paint(keep):
        new = {}
        for o in out:
            wool = SPECIAL_WOOL.get(o["id"], KIND_WOOL[o["kind"]])
            cells = [tuple(o["cells"][i:i + 3]) for i in range(0, len(o["cells"]), 3)]
            if o["kind"] in ("room", "tunnel", "stair"):
                cells = [c for c in cells if not passable((c[0], c[1] - 1, c[2]))]      # the feet layer only
            for c in cells:
                if keep(c): new[c] = wool
        return new
    shots = [("labels_main_y30.png", (-16, 56, 0, 30, -26, 50), 0),
             ("labels_main_y52.png", (-16, 56, 0, 52, -26, 50), 0),
             ("labels_lane_y21.png", (44, 105, 0, 21, -45, 40), 1)]
    for name, box, q in shots:
        new = paint(lambda c: all(box[2 * i] <= c[i] <= box[2 * i + 1] for i in range(3)))
        kit.render(new, os.path.join(HERE, name), q=q, scale=4, box=box, full=False)


if __name__ == "__main__":
    render(main()[0])
