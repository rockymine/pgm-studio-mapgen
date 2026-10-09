"""Measure Cinder Reach's plan before anything is built: the core's walks against the studio's goal rules, the four
ways onto it and what each costs, the fissure's widths, the spawn's back, and what stands near the core.

Walks are octile over the plan (a step up 1.2); the fissure is crossed by building, a block of bridge a block.

    python3 plan_check.py        prints the table; the sketch draws the same rows and routes
"""
import json
import math
import os

import numpy as np

import plan as P
import common as C
from pgmvox import plangraph as G
from pgmvox import sight

HERE = os.path.dirname(os.path.abspath(__file__))


def cells_near(x, z, r, R, kinds=None):
    out = []
    for dx in range(-r, r + 1):
        for dz in range(-r, r + 1):
            c = (x + dx, z + dz)
            if R.inside(*c) and math.hypot(dx, dz) <= r and (kinds is None or R.kind(*c) in kinds):
                out.append(c)
    return out


def graph(R):
    zone = P.zone(R)
    extra = []
    tube = R.storey(1)
    for img in (False, True):                                    # bridges reach the tube's mouth in the face
        for (x, z), _ in P.tube_cells().items():
            if img:
                x, z = P.SYM.point(x, z)
            if not R.inside(x, z) or tube.kind(x, z) != "tube":
                continue
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, z + dz)
                if R.inside(*q) and zone[R.ix(q[0]), R.iz(q[1])]:
                    extra += [(q, (x, z, 1), 1.0, "bridge"), ((x, z, 1), q, 1.0, "bridge")]
    return G.graph(R, P.WALK, rules=G.PlanRules(diagonals=True), bridge=zone, extra=extra), zone


def measure():
    R = P.build()
    L = P.land()
    E, zone = graph(R)
    red_sp = (P.SPAWN[0], P.SPAWN[2])
    blue_sp = P.SYM.point(*red_sp)
    ring_red, ring_blue = P.core_ring("red"), P.core_ring("blue")
    Dr, prr = G.dijkstra(E, [red_sp])
    Db, prb = G.dijkstra(E, [blue_sp])
    own_red, by_r, path_own = G.measure(Dr, prr, E, ring_red)
    own_blue = G.measure(Db, prb, E, ring_blue)[0]
    enemy_red, by_e, path_enemy = G.measure(Db, prb, E, ring_red)     # blue attacking red's core
    enemy_blue = G.measure(Dr, prr, E, ring_blue)[0]

    # the four ways onto red's core for blue, each through its own waypoint
    cx, cz = P.CORE
    (px, pz), rx, rz, _ = P.POND
    sx, sz = P.SPINE[-1]
    (kx, kz), _, kf = P.SINK
    ways = {
        "around the pond, north": cells_near(px, pz - int(rz) - 3, 2, R, P.WALK),
        "around the pond, south": cells_near(px, pz + int(rz) + 3, 2, R, P.WALK),
        "over the Spine's crag": [c for c in cells_near(sx, sz, 3, R) if R.h(*c) >= P.SPINE_TOP - 2],
        "up the lava tube": [(x, z, 1) for (x, z), _ in P.tube_cells().items() if -20 <= x <= -18],
        "through Pumice Row": cells_near(-70, 2, 3, R, P.WALK),
    }
    approach = {}
    for name, wp in ways.items():
        cost, path = C.via(E, [blue_sp], wp, ring_red)
        at_b = min((Db[c] for c in wp if c in Db), default=math.inf)
        at_r = min((Dr[c] for c in wp if c in Dr), default=math.inf)
        approach[name] = (cost, path, at_b, at_r)

    # the fissure: the void a team bridges, by row
    gaps = C.gaps(R.K != R.kinds["void"], range(R.x_min, R.x_max + 1), range(R.z_min, R.z_max + 1), "x")
    gv = sorted(v for z, v in gaps.items() if abs(z + 0.5) <= 56)          # the rows a crossing is made on

    # the core off the line between the spawns, in degrees
    ang = abs(math.degrees(math.atan2(cz - red_sp[1], cx - red_sp[0]) -
                           math.atan2(blue_sp[1] - red_sp[1], blue_sp[0] - red_sp[0])))
    # the spawn's back: the highest ground within 20 over the terrace, and the land behind it to the west
    back = max(R.h(x, z) for x, z in cells_near(red_sp[0], red_sp[1], 20, R) if R.kind(x, z) not in ("void", "house"))
    behind = sum(1 for x in range(red_sp[0] - 1, R.x_min - 1, -1) if R.kind(x, red_sp[1]) != "void")
    # what stands within four of the casing: houses, the wood
    box = [(x, z) for x in range(cx - 2, cx + 3) for z in range(cz - 2, cz + 3)]

    def dmin(cells):
        return min((math.hypot(a - b, c - d) for a, c in cells for b, d in box), default=99)
    near_house = min(dmin(b["cells"]) for b in P.houses().values())
    wood = [(int(L.X[i, k]), int(L.Z[i, k])) for i, k in np.argwhere(L.wood)]
    near_wood = dmin(wood)
    # the cone: the inner face is a drop, not a climb, outside the breaches
    inner = [(x, z) for x in range(cx - 12, cx + 13) for z in range(cz - 12, cz + 13)
             if 9 <= math.hypot(x - cx, z - cz) < 10 and not L.breach[x - P.X_MIN, z - P.Z_MIN]]
    one_way = sum(1 for x, z in inner if R.h(x, z) - P.BOWL_Y >= 4) / max(1, len(inner))
    # the core seen from the crag (above) and from the Landing on the far shelf (the attackers' look)
    opaque = sight.plan_opaque(R)
    tgt = [sight.target(cx, P.CORE_Y + 4, cz)]            # the casing's top course
    crag = [sight.eye(x, R.h(x, z) + 1, z) for x, z in ways["over the Spine's crag"]]
    seen_crag = sight.visibility(tgt, crag, opaque)[0]
    return dict(R=R, own=(own_red, own_blue), enemy=(enemy_red, enemy_blue), by_e=by_e, approach=approach,
                gaps=gaps, gv=gv, ang=ang, back=back, behind=behind, near_house=near_house, near_wood=near_wood,
                one_way=one_way, seen_crag=seen_crag, path_own=path_own, path_enemy=path_enemy)


def rows(m):
    o_r, o_b = m["own"]
    e_r, e_b = m["enemy"]
    ratio = e_r / o_r
    out = [
        (f"{o_r:.1f} / {o_b:.1f}", "spawn to its own core, red / blue", "GO4: 40-90, equal", 40 <= o_r <= 90 and abs(o_r - o_b) < .01),
        (f"{e_r:.1f} / {e_b:.1f}", "enemy spawn to the core, red's / blue's", "GO3: 85-150, equal", 85 <= e_r <= 150 and abs(e_r - e_b) < .01),
        (f"{m['by_e'].get('bridge', 0):.0f}", "of it bridged over the fissure", "12-30", 12 <= m["by_e"].get("bridge", 0) <= 30),
        (f"{ratio:.2f}", "core to the enemy spawn over core to its own", "GO1: 3-4", 3 <= ratio <= 4),
        (f"{m['ang']:.0f} deg", "the core off the line between the spawns", "20-60 (corpus median 42)", 20 <= m["ang"] <= 60),
    ]
    best = min(v[0] for v in m["approach"].values())
    for name, (c, _, ab, ar) in m["approach"].items():
        flank = name.startswith("through")                       # behind the core: the defenders' own ground
        out.append((f"{c:.0f} (x{c / best:.2f})", f"blue onto red's core {name}",
                    "the long flank, behind the core" if flank else "at most 1.25 x the shortest",
                    None if flank else c <= 1.25 * best))
        out.append((f"blue {ab:.0f}, red {ar:.0f}", f"   who reaches that way's mouth first", "red first", ar < ab))
    out += [
        (f"{m['gv'][0]}-{m['gv'][-1]}", "the fissure's void, narrowest to widest (|z| <= 56)", "14-30", 14 <= m["gv"][0] and m["gv"][-1] <= 30),
        (f"{m['back'] - P.TERRACE_Y}", "ground over the spawn terrace within 20", "at least 8", m["back"] - P.TERRACE_Y >= 8),
        (f"{m['behind']}", "the spawn's own land behind it, to the west", "at least 10", m["behind"] >= 10),
        (f"{m['near_house']:.1f}", "nearest building to the casing", "at least 4 (cover keeps off)", m["near_house"] >= 4),
        (f"{m['near_wood']:.1f}", "nearest of the wood to the casing", "at least 4", m["near_wood"] >= 4),
        (f"{m['one_way']:.0%}", "of the cone's inner face a drop of 4 or more", "at least 80%: in by the rim, out by a breach", m["one_way"] >= 0.8),
        (f"{P.SPINE_TOP - (P.CORE_Y + 4)}", "the crag over the casing's top", "4-12: above, not out of reach", 4 <= P.SPINE_TOP - (P.CORE_Y + 4) <= 12),
        (f"{m['seen_crag']:.0%}", "of the crag's top cells that see the casing's top", "its lip does: over 5%",
         m["seen_crag"] > 0.05),
    ]
    return out


if __name__ == "__main__":
    m = measure()
    r = rows(m)
    print(C.table(r))
    paths = {"own": m["path_own"], "enemy": m["path_enemy"]}
    paths.update({k: v[1] for k, v in m["approach"].items()})
    with open(os.path.join(HERE, "..", "renders", "plan-check.json"), "w") as f:
        json.dump(dict(rows=[(str(a), b, c_, None if d is None else bool(d)) for a, b, c_, d in r], paths={k: [list(c) for c in v] for k, v in paths.items()}), f)
