"""Measure Brassmoor Works' plan before anything is built: the capture rules' walks (spawn to the band, to each
wool, the band to each wool by each of its two ways), the gaps a team bridges, the funnels, the bedrock lines,
the rooms' faces on the void, and fairness.

A walk is octile over the floors (a step up 1.2) and crosses a build zone or a bedrock line by building, a block of
bridge a block: "86 (30 bridged)" is 56 walked and 30 built.

    python3 plan_check.py        prints the table; the sketch draws the same rows and routes
"""
import json
import math
import os

import numpy as np

import plan as P
import common as C
from pgmvox import plangraph as G
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))


def cells_of(R, key, half="red"):
    m = R.mask(key) & ((R.Z < 0) if half == "red" else (R.Z >= 0))
    return [(int(R.X[i, k]), int(R.Z[i, k])) for i, k in np.argwhere(m)]


def gap(a, b):
    """The void between two pieces' rectangles, in whole blocks."""
    ax0, az0, ax1, az1 = P.PIECE[a][3]
    bx0, bz0, bx1, bz1 = P.PIECE[b][3]
    dx = max(0, bx0 - ax1 - 1, ax0 - bx1 - 1)
    dz = max(0, bz0 - az1 - 1, az0 - bz1 - 1)
    return math.hypot(dx, dz) if dx and dz else dx + dz


def measure():
    R = P.build()
    zone = P.zone_mask(R)
    walls = P.wall_mask(R)
    rules = G.PlanRules(diagonals=True)
    E = G.graph(R, P.WALK, wall_kinds=("roomwall", "barrier"), rules=rules, bridge=zone | walls)
    Ew = G.graph(R, P.WALK, wall_kinds=("roomwall", "barrier"), rules=rules)
    sp = (P.SPAWN_AT[0], P.SPAWN_AT[2])
    bsp = P.SYM.point(*sp)
    D, prev = G.dijkstra(E, [sp])
    Dw, prevw = G.dijkstra(Ew, [sp])
    Db, prevb = G.dijkstra(E, [bsp])
    band_edge = [(x, -12) for x in range(-56, 56) if (x, -12) in Ew]
    out = {}
    out["band"] = min(D.get(c, math.inf) for c in band_edge)
    mons = [(o.slot[0], o.slot[2]) for o in P.objectives().items if getattr(o, "slot", None) and o.team == "red-team"]
    out["monuments"] = [G.measure(D, prev, E, [m])[0] for m in mons]
    rooms = {}
    paths = {}
    for key in P.ROOMS:
        red_cells, blue_cells = P.room_cells(R, key), P.room_cells(R, key, "blue")
        own, _, p_own = G.measure(D, prev, E, red_cells)
        own_b = G.measure(Db, prevb, E, blue_cells)[0]
        walked = G.measure(Dw, prevw, Ew, red_cells)[0]
        # blue attacking red's room: from the band's edge on red's side, by the lane over the wall or by the flats
        Dband, prevband = G.dijkstra(E, band_edge)
        best, by, p_best = G.measure(Dband, prevband, E, red_cells)
        wall_cells = [(x, z) for x in range(P.WALLS["gantry" if key == "boiler" else "spur"]["x0"],
                                            P.WALLS["gantry" if key == "boiler" else "spur"]["x1"] + 1)
                      for z in range(-90, -60) if R.kind(x, z) == "barrier"]
        islet = cells_of(R, "slag" if key == "boiler" else "coal")
        lane = C.via(E, band_edge, wall_cells, red_cells)
        flats = C.via(E, band_edge, islet, red_cells)
        brid = {}
        for name, (c, p) in (("lane", lane), ("flats", flats)):
            b = sum(1 for u, v in zip(p, p[1:]) if any(t == "bridge" and w == v for w, _, t in E.get(u, [])))
            brid[name] = (c, b, p)
        # the defenders: red from its spawn to the wall and to the room's south door
        rooms[key] = dict(own=own, own_b=own_b, walked=walked, band=best, band_by=by, ways=brid)
        paths[f"own {key}"], paths[f"band {key}"] = p_own, p_best
        paths[f"lane {key}"], paths[f"flats {key}"] = lane[1], flats[1]
    out["rooms"] = rooms
    # the board's gaps
    out["gaps"] = {
        "Slag Heap to the Boiler House": gap("slag", "boiler"), "Slag Heap to the West Quay": gap("slag", "quay-w"),
        "Slag Heap to the Gantry": gap("slag", "gantry"),
        "Coal Stage to the Water Tower": gap("coal", "tower"), "Coal Stage to the East Quay": gap("coal", "quay-e"),
        "Coal Stage to the Spur": gap("coal", "spur"),
        "the Quays apart (WL12)": gap("quay-w", "quay-e"),
        "a Quay's end to the Crane Island": gap("quay-w", "crane"),
    }
    # the band: from red's Quays to blue's, across
    out["across"] = 2 * 12 - 2
    # the lanes' widths and the walls
    out["funnels"] = {"the Gantry": P.PIECE["gantry"][3][3] - P.PIECE["gantry"][3][1] + 1,
                      "the Spur": P.PIECE["spur"][3][3] - P.PIECE["spur"][3][1] + 1}
    out["walls"] = {"boiler": P.WALLS["gantry"]["x0"] - P.ROOMS["boiler"]["box"][2] - 1,
                    "tower": P.ROOMS["tower"]["box"][0] - P.WALLS["spur"]["x1"] - 1}
    land = R.K != R.kinds["void"]
    faces = {}
    for key in P.ROOMS:
        x0, z0, x1, z1 = P.ROOMS[key]["box"]
        sides = {"n": [(x, z0 - 1) for x in range(x0, x1 + 1)], "s": [(x, z1 + 1) for x in range(x0, x1 + 1)],
                 "w": [(x0 - 1, z) for z in range(z0, z1 + 1)], "e": [(x1 + 1, z) for z in range(z0, z1 + 1)]}
        faces[key] = sum(1 for cs in sides.values()
                         if all(not R.inside(*c) or not land[R.ix(c[0]), R.iz(c[1])] for c in cs))
    out["faces"] = faces
    J = G.jumps(R, P.WALK, wall_kinds=("roomwall", "barrier"))
    lab, _ = ndimage.label(land)
    out["apart"] = sum(1 for a, b, g in J if lab[R.ix(a[0]), R.iz(a[1])] != lab[R.ix(b[0]), R.iz(b[1])])
    b = P.ROOMS["boiler"]["box"]; t = P.ROOMS["tower"]["box"]
    fb, ft = [o.found for o in P.objectives().items if getattr(o, "team", "") == "blue-team" and hasattr(o, "found")]
    out["wool_to_wool"] = math.hypot(fb[0] - ft[0], fb[2] - ft[2])
    # the spawn on the line between its two wools: how far off it
    ax, az, bx, bz = fb[0], fb[2], ft[0], ft[2]
    tt = ((sp[0] - ax) * (bx - ax) + (sp[1] - az) * (bz - az)) / ((bx - ax) ** 2 + (bz - az) ** 2)
    out["interpose"] = math.hypot(sp[0] - (ax + tt * (bx - ax)), sp[1] - (az + tt * (bz - az)))
    out["R"], out["paths"] = R, paths
    return out


def rows(m):
    rs = m["rooms"]
    ratio = max(rs["boiler"]["own"], rs["tower"]["own"]) / min(rs["boiler"]["own"], rs["tower"]["own"])
    out = [
        (f"{m['band']:.0f}", "spawn to the band", "SP10: at least 55", m["band"] >= 55),
        (", ".join(f"{v:.0f}" for v in m["monuments"]), "spawn to its own two monuments", "near and in sight: at most 20",
         max(m["monuments"]) <= 20),
        (f"{m['interpose']:.0f}", "the spawn off the line between its own two wools", "interposed: at most 20",
         m["interpose"] <= 20),
    ]
    for key, r in rs.items():
        out += [
            (f"{r['own']:.1f} / {r['own_b']:.1f}", f"red / blue spawn to its own {key} room", "equal",
             abs(r["own"] - r["own_b"]) < .01),
            ("none" if math.isinf(r["walked"]) else f"{r['walked']:.0f}", f"   the {key} room on foot, no block placed",
             "the wall stops it", math.isinf(r["walked"]) if key else None),
            (f"{r['band']:.0f} ({r['band_by'].get('bridge', 0):.0f} bridged)", f"band to red's {key} room, shortest",
             "WL10e: at least 59", r["band"] >= 59),
        ]
        for way, (c, b, _) in r["ways"].items():
            out.append((f"{c:.0f} ({b} bridged)", f"   by the {'lane, over the wall' if way == 'lane' else 'flats, by the stepping stone'}",
                        "within 1.3 x the shortest", c <= 1.3 * r["band"]))
    out.append((f"{ratio:.2f}", "spawn to the farther room over the nearer", "WL9: at most 1.25", ratio <= 1.25))
    out.append((f"{m['wool_to_wool']:.0f}", "Boiler House wool to Water Tower wool, straight", "WL7: 46 to 143",
                46 <= m["wool_to_wool"] <= 143))
    for name, g in m["gaps"].items():
        tgt, ok = ("at least 16 (a bay at a goal)", g >= 16) if ("House" in name or "Tower" in name) else \
                  (("at least 16", g >= 16) if "apart" in name else
                   (("12 to 16: bridged, not jumped", 12 <= g <= 16) if "Quay" in name and "Stage" in name or "Heap" in name and "Quay" in name
                    else ("at least 4: not a jump", g >= 4)))
        out.append((f"{g:.0f}", name, tgt, ok))
    out.append((f"{m['across']}", "the band, Quay to Quay", "16-26", 16 <= m["across"] <= 26))
    for name, wd in m["funnels"].items():
        out.append((f"{wd}", f"{name}'s width, the funnel", "10-12 (a door is 10 on 79% of objectives)", 10 <= wd <= 12))
    for key, d in m["walls"].items():
        out.append((f"{d}", f"the bedrock line to the {key} room's face", "4-13", 4 <= d <= 13))
    for key, f in m["faces"].items():
        out.append((f"{f}", f"the {key} room's faces on the void", "at least 2: held from its corner", f >= 2))
    out.append((f"{m['apart']}", "running jumps between pieces that do not touch", "none", m["apart"] == 0))
    return out


if __name__ == "__main__":
    m = measure()
    r = rows(m)
    print(C.table(r))
    with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
        json.dump(dict(rows=[(str(a), b, c_, None if d is None else bool(d)) for a, b, c_, d in r],
                       paths={k: [list(c) for c in v] for k, v in m["paths"].items()}), f)
