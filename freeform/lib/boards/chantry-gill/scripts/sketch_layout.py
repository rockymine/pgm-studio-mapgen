"""Draw the layout from above: both teams' islands, the gill, the void and the build zone, the places, the
routes onto blue's monument and the numbers the studio would hold the board to.

    python3 sketch_layout.py <out.png>
"""
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                                       # noqa: E402
from matplotlib.patches import Polygon                                                # noqa: E402

import layout as L                                                                    # noqa: E402

fig, ax = plt.subplots(figsize=(11, 14), dpi=110)
ax.set_facecolor("#1d1f26")
x0, x1 = L.X_RANGE
ax.add_patch(plt.Rectangle((x0, L.BUILD_Z[0]), x1 - x0, L.BUILD_Z[1] - L.BUILD_Z[0], color="#3b5a8c", alpha=0.45))
ax.text(x0 + 3, 0, "build zone over the void", color="#cfe0ff", va="center", fontsize=9)
for team, f in (("blue", lambda p: p), ("red", L.turn)):
    pale = team == "red"
    for poly, colour in ((L.MAIN, "#6f9a4a"), (L.SIDE, "#8a8f7a"), (L.GILL, "#4b4f57")):
        ax.add_patch(Polygon([f(p) for p in poly], closed=True, fc=colour, ec="#222", lw=1, alpha=0.55 if pale else 0.95))
    for name, (poly, rise) in L.SCENERY.items():
        ax.add_patch(Polygon([f(p) for p in poly], closed=True, fc="#5a5f55", ec="#ddd", lw=1, hatch="///",
                             alpha=0.5 if pale else 0.9))
        if not pale:
            cx = sum(p[0] for p in poly) / len(poly)
            cz = sum(p[1] for p in poly) / len(poly)
            ax.text(cx, cz, f"{name}\n+{rise}", color="w", ha="center", va="center", fontsize=7)
    for name, (poly, rise) in L.FOOTHILLS.items():
        ax.add_patch(Polygon([f(p) for p in poly], closed=True, fc="#8fb35e", ec="#e8f0c8", lw=1, hatch="..",
                             alpha=0.5 if pale else 0.95))
        if not pale:
            cx = sum(p[0] for p in poly) / len(poly)
            cz = sum(p[1] for p in poly) / len(poly)
            ax.text(cx, cz, f"{name}\n+{rise}", color="#111", ha="center", va="center", fontsize=7)
    sx, sz = f(L.SPAWN)
    c = "#3d7bff" if team == "blue" else "#ff4d4d"
    ax.plot(sx, sz, "s", ms=12, mfc=c, mec="w")
    for m in L.MONUMENTS:
        mx, mz = f(m)
        ax.plot(mx, mz, "D", ms=11, mfc="#222", mec=c, mew=2.5)
    ax.text(sx, sz + (5 if team == "blue" else -5), f"{team} spawn", color="w", ha="center", fontsize=8)
for name, (x, z, _) in L.PLACES.items():
    if name in ("spawn", "town monument", "scar monument"):
        continue
    ax.text(x, z, name, color="w", ha="center", va="center", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.2", fc="#000", alpha=0.35, lw=0))
ax.add_patch(plt.Rectangle((L.CRYPT[0], L.CRYPT[1]), L.CRYPT[2] - L.CRYPT[0], L.CRYPT[3] - L.CRYPT[1], fill=False,
                           ec="#e0c060", ls="--", lw=1.2))
ax.plot([a[0] for a in L.ADIT], [a[1] for a in L.ADIT], ls=":", color="#e0c060", lw=2)
colours = {"town: through": "#ffd23f", "town: around": "#ff9f1c", 
           "town: below": "#e0c060", "town: brig": "#c792ea", "scar: front": "#ff6fb5", "scar: chimney": "#9cff8a"}
for name, pts in L.ROUTES.items():
    p = [q for q in pts if not isinstance(q, str)]
    ax.annotate("", xy=p[-1], xytext=p[-2], arrowprops=dict(arrowstyle="->", color=colours[name], lw=2))
    ax.plot([q[0] for q in p], [q[1] for q in p], color=colours[name], lw=2, alpha=0.9,
            ls="--" if any(k in name for k in ("brow", "below", "chimney")) else "-", label=f"{name}: {L.length(pts):.0f} blocks")
for n, d in enumerate(L.DEFENCES):
    ax.plot([q[0] for q in d], [q[1] for q in d], color="#3d7bff", lw=3, alpha=0.8,
            label=f"defence, spawn to {('town', 'scar')[n]} monument: {L.length(d):.0f}")
title = "  ".join(f"{('town', 'scar')[n]}: {math.dist(m, L.turn(L.SPAWN)):.0f} to red's spawn, "
                  f"{math.dist(m, L.turn(L.SPAWN)) / L.length(d):.1f} x"
                  for n, (m, d) in enumerate(zip(L.MONUMENTS, L.DEFENCES)))
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8, facecolor="#2a2d36", labelcolor="w", framealpha=0.9,
          title=title,
          title_fontsize=8)
ax.set_xlim(x0, x1)
ax.set_ylim(130, -130)
ax.set_aspect("equal")
ax.grid(color="#444", lw=0.4)
ax.set_title("Chantry Gill: layout (north is up; blue south, red its half turn)", color="w")
fig.patch.set_facecolor("#15161b")
ax.tick_params(colors="#aaa")
fig.savefig(sys.argv[1], bbox_inches="tight", facecolor=fig.get_facecolor())
