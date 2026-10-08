"""Walk the built Gullhaven DTM on foot, with no blocks placed: from each team's spawn to each of the other team's
monuments, and the two teams compared. The walk itself is the free-for-all island's (`walk.bfs`), with drops of
any height allowed: this variant keeps fall damage, so a drop over three is noted where it is used.

    python3 walk.py <build-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "opus55-freeform-gullhaven", "scripts"))

import render_iso  # noqa: E402
import walk as W  # noqa: E402

sys.path.insert(0, HERE)
import compose as C  # noqa: E402


def main(build):
    x0, z0, ids, dat = render_iso.load(build)
    passable, water, ladder, solid = W.grid(ids)
    st = W.standable(passable, water, solid) | (ladder & passable)
    sx, sy, sz = C.SPAWN["at"]
    spawns = {"red": (int(sx), sy, int(sz) - 1), "blue": (C.AX - int(sx), sy, C.BZ - (int(sz) - 1))}
    # a monument is reached when a player stands under it: on the beach's pad, or in the water at the harbour
    mons = {"red": {m["key"]: (m["centre"][0], m["y0"] - 3, m["centre"][1]) for m in C.MONUMENTS}}
    mons["blue"] = {k: (C.AX - x, y, C.BZ - z) for k, (x, y, z) in mons["red"].items()}
    out = []
    for team, enemy in (("red", "blue"), ("blue", "red")):
        s = spawns[team]
        ok = st[s[0] - x0, s[1], s[2] - z0]
        d = W.bfs(st, ladder, water, passable, [s], x0, z0)
        parts = []
        for key, (x, y, z) in mons[enemy].items():
            v = W.nearest(d, x0, z0, x, y, z, r=4)
            parts.append(f"{enemy}'s {key} monument {v if v is not None else 'NOT REACHED on foot'}")
        own = []
        for key, (x, y, z) in mons[team].items():
            v = W.nearest(d, x0, z0, x, y, z, r=4)
            own.append(f"own {key} {v if v is not None else 'NOT REACHED'}")
        mid = W.nearest(d, x0, z0, -19, 26, 57, r=3)
        out.append(f"{team} spawn {s} ({'stands' if ok else 'DOES NOT STAND'}): " + "; ".join(parts) +
                   f"; the Skerry {mid}; " + "; ".join(own) + f"; {int((d >= 0).sum())} cells")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
